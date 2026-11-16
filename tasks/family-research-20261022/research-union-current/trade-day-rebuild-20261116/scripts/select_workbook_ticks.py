"""The trade-day book record for each of the 5,513 selected workbook ticks (32 cases), one file per case.

Each selected tick is located in the trade-day trade list by the trade it designates, then checked on receive time,
event time, sequence, order id, price, size and side before its record is copied out of the trade-day book shards.
The row keeps the case id and case row, the trade-day book record, and where that record came from.

usage: select_workbook_ticks.py <old selected-tick dir> <trade-day book shard root> <out dir>
"""
import glob, gzip, hashlib, json, os, sys
import pyarrow.parquet as pq
OLD, BOOK, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
HERE = os.path.dirname(os.path.abspath(__file__))
PROGRAM = 'tasks/family-research-20261022/research-union-current/trade-day-rebuild-20261116/scripts/build_book_records.py'
total = 0; summary = []
by_day = {}
for f in sorted(glob.glob(OLD + '/*.jsonl.gz')):
    case = os.path.basename(f)[:-len('.jsonl.gz')]; day = case.split('-')[0]
    if day not in by_day:
        t = pq.read_table(f'{HERE}/../results/trade_day_{day}_trades.parquet').to_pylist()
        by_day[day] = ({r['prior_archive_trade_cursor']: r for r in t if r['prior_archive_trade_cursor'] is not None},
                       {m['path']: m for m in json.load(open(f'{BOOK}/{day}/MANIFEST.json'))['files']}, {})
    locate, manifest, cache = by_day[day]
    rows = []
    for line in gzip.open(f):
        old = json.loads(line); o = old['original']['original_trade']
        t = locate[int(o['trade_input_cursor'])]
        same = all(int(o[a]) == t[b] for a, b in (('receive_ns', 'receive_ns'), ('event_ns', 'event_ns'), ('sequence', 'sequence'),
                   ('order_id', 'order_id'), ('price_raw', 'price_raw'), ('size', 'size'))) and o['aggressor_side'] == t['aggressor_side']
        if not same: raise ValueError(f'{case} row {old["case_row"]}: the located trade is not the same trade')
        shard = f"trade-book-fifo-{t['trade_ordinal'] // 100:04d}.jsonl.gz"
        if shard not in cache:
            data = open(f'{BOOK}/{day}/{shard}', 'rb').read()
            if hashlib.sha256(data).hexdigest() != manifest[shard]['sha256']: raise ValueError('shard differs from its manifest')
            cache.clear(); cache[shard] = [json.loads(x) for x in gzip.decompress(data).splitlines()]
        rec = cache[shard][t['trade_ordinal'] % 100]
        if rec['trade_ordinal'] != t['trade_ordinal'] or rec['original_trade']['receive_ns'] != t['receive_ns']: raise ValueError('wrong record')
        rows.append(dict(case_id=old['case_id'], case_row=old['case_row'], record=rec,
                         source=dict(program=PROGRAM, trade_day=day, shard=shard, shard_sha256=manifest[shard]['sha256'], row_in_shard=t['trade_ordinal'] % 100)))
    out = f'{OUT}/{case}.jsonl.gz'
    with gzip.GzipFile(filename=out, mode='wb', compresslevel=6, mtime=0) as g:
        for r in rows: g.write((json.dumps(r, separators=(',', ':'), allow_nan=False) + '\n').encode())
    data = open(out, 'rb').read(); total += len(rows)
    summary.append(dict(case_id=case, ticks=len(rows), bytes=len(data), sha256=hashlib.sha256(data).hexdigest()))
json.dump(dict(selected_ticks=total, cases=len(summary), files=summary), open(f'{OUT}/MANIFEST.json', 'w'), indent=1)
print('selected ticks', total, 'cases', len(summary), 'MB', round(sum(s['bytes'] for s in summary) / 1e6, 1))
