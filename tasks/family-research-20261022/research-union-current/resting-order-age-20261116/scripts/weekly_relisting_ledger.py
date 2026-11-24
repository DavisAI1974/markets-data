"""The orders already resting when the UTC clock-day Oct 1 (Sunday) file opens: one row each, and what became of them.

The file opens with a clear record, then a block of snapshot-flagged adds that all carry one receive time and one
event time. This lists every order in that block with its stamps, what the rest of the Oct 1 file does to it
(cancelled, priority reset by a modify, size reduced, untouched), whether it is still resting when trade day Oct 2
starts (21:00 UTC Oct 1) and at 00:00 UTC Oct 2, and the event time the 00:00 UTC Oct 2 and Oct 3 snapshots give it.

usage: weekly_relisting_ledger.py <out dir>
"""
import csv, datetime, importlib, json, sys
import databento as db

sys.path.insert(0, '/home/user/work/pins/research')
A = importlib.import_module('ng_exhaustion_mbo_v4_state_adapter_20260820')
TAPE = '/home/user/markets-data/data/nymex_mbo/ng_v0_oct2023/'
OUT = sys.argv[1]
SESSION_START_NS = int(datetime.datetime(2023, 10, 1, 21, tzinfo=datetime.timezone.utc).timestamp()) * 10**9


def utc(ns):
    if ns in (None, ''): return ''
    s, frac = divmod(int(ns), 10**9)
    return datetime.datetime.fromtimestamp(s, datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S') + f'.{frac:09d}'


def snapshot_block(day):
    out = {}
    for rec in db.DBNStore.from_file(TAPE + f'NG_v0_mbo_{day}.dbn.zst'):
        if not (int(rec.flags) & 32): break
        m = A.V4MboAdapter.normalize(rec, 'NGX3')
        if m.action == 'A': out[m.order_id] = m
    return out


adapter = A.V4MboAdapter(); book = None; block = {}; first_live = None; at_start = None
for i, rec in enumerate(db.DBNStore.from_file(TAPE + 'NG_v0_mbo_20231001.dbn.zst')):
    msg = adapter.normalize(rec, 'NGX3')
    if book is None: book = adapter.books[msg.instrument_id] = A.InstrumentBook(msg.instrument_id)
    if at_start is None and msg.ts_recv_ns >= SESSION_START_NS: at_start = set(book.orders)
    existed = msg.order_id in book.orders
    effect, _, _ = book.apply(msg)
    if msg.is_snapshot and msg.action == 'A':
        block[msg.order_id] = dict(file_index=i, order_id=msg.order_id, side=msg.side, price_raw=msg.price_raw, size=msg.size,
                                   block_event_ns=msg.ts_event_ns, block_event_utc=utc(msg.ts_event_ns), block_recv_ns=msg.ts_recv_ns,
                                   block_recv_utc=utc(msg.ts_recv_ns), block_sequence=msg.sequence, block_flags=msg.flags,
                                   later_messages=0, priority_reset_event_utc='', priority_keeping_changes=0, removed_event_utc='', removed_by='')
        continue
    if first_live is None and not msg.is_snapshot and msg.action != 'R': first_live = dict(file_index=i, recv_utc=utc(msg.ts_recv_ns), action=msg.action)
    row = block.get(msg.order_id)
    if row is None or msg.action not in ('A', 'M', 'C') or row['removed_event_utc']: continue
    row['later_messages'] += 1
    if msg.order_id not in book.orders:
        row['removed_event_utc'] = utc(msg.ts_event_ns); row['removed_by'] = msg.action
    elif msg.action == 'A' or (msg.action == 'M' and effect.priority_lost):
        row['priority_reset_event_utc'] = utc(msg.ts_event_ns)
    else:
        row['priority_keeping_changes'] += 1
at_midnight = set(book.orders)
s2, s3 = snapshot_block('20231002'), snapshot_block('20231003')
rows = []
for oid, row in block.items():
    row['resting_at_trade_day_oct2_start_2100utc'] = oid in at_start
    row['resting_at_0000utc_oct2'] = oid in at_midnight
    for tag, s in (('oct2', s2), ('oct3', s3)):
        m = s.get(oid)
        row[f'in_0000utc_{tag}_snapshot'] = m is not None
        row[f'{tag}_snapshot_event_utc'] = utc(m.ts_event_ns) if m else ''
        row[f'{tag}_snapshot_event_equals_block_event'] = bool(m) and m.ts_event_ns == row['block_event_ns']
    rows.append(row)
with open(f'{OUT}/weekly_relisting_orders_20231001.csv', 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
c = lambda pred: sum(1 for r in rows if pred(r))
receipt = dict(
    file='NG_v0_mbo_20231001.dbn.zst', orders_in_opening_block=len(rows),
    distinct_block_event_times=sorted({r['block_event_utc'] for r in rows}), distinct_block_recv_times=sorted({r['block_recv_utc'] for r in rows}),
    distinct_block_sequences=len({r['block_sequence'] for r in rows}), first_live_message=first_live,
    counts_of_individual_orders=dict(
        never_touched_again_in_oct1_file=c(lambda r: r['later_messages'] == 0),
        removed_in_oct1_file=c(lambda r: r['removed_event_utc'] != ''),
        priority_reset_in_oct1_file=c(lambda r: r['priority_reset_event_utc'] != ''),
        resting_at_trade_day_oct2_start=c(lambda r: r['resting_at_trade_day_oct2_start_2100utc']),
        resting_at_0000utc_oct2=c(lambda r: r['resting_at_0000utc_oct2']),
        in_oct2_snapshot_with_the_block_event_time=c(lambda r: r['oct2_snapshot_event_equals_block_event']),
        in_oct2_snapshot_with_another_event_time=c(lambda r: r['in_0000utc_oct2_snapshot'] and not r['oct2_snapshot_event_equals_block_event']),
        in_oct3_snapshot_with_the_block_event_time=c(lambda r: r['oct3_snapshot_event_equals_block_event']),
        in_oct3_snapshot_with_another_event_time=c(lambda r: r['in_0000utc_oct3_snapshot'] and not r['oct3_snapshot_event_equals_block_event'])),
    orders_in_0000utc_oct3_snapshot_with_an_oct1_event_date=sum(1 for m in s3.values() if utc(m.ts_event_ns).startswith('2023-10-01')),
    of_those_carrying_the_block_event_time=sum(1 for m in s3.values() if utc(m.ts_event_ns) in {r['block_event_utc'] for r in rows}))
json.dump(receipt, open(f'{OUT}/weekly_relisting_orders_20231001_RECEIPT.json', 'w'), indent=1)
print(json.dumps(receipt, indent=1))
