"""Read-only join of every selected before/during group to immutable source shards.

Requires pyarrow. Run with --objects <content-addressed object directory>.
Optional --python-deps adds an existing dependency directory, without installing.
"""
import argparse
import collections
import gzip
import json
import sys
from pathlib import Path
from audit import OUT, dump


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--objects', type=Path, required=True)
    parser.add_argument('--python-deps', type=Path)
    args = parser.parse_args()
    if args.python_deps:
        sys.path.insert(0, str(args.python_deps))
    import pyarrow.parquet as pq
    sources = json.loads((OUT/'source_event_inventory.json').read_text())
    clocks = [json.loads(line) for line in gzip.decompress((OUT/'tick_clock_ledger.jsonl.gz').read_bytes()).splitlines()]
    needed = collections.defaultdict(set)
    for row in clocks:
        needed[row['case_id'][:8]].update([row['before_group'],row['during_group']])
    found, schemas = {}, []
    columns = ['group_ordinal','first_cursor','close_cursor','known_by_ns','bid_price_raw','ask_price_raw',
               'bid_size','ask_size','bid_full_size','ask_full_size','bid_orders','ask_orders','bid_full_orders','ask_full_orders']
    for source in sources:
        file = args.objects/source['sha']
        if not source['path'].endswith('.parquet') or not file.exists():
            continue
        pf = pq.ParquetFile(file)
        schemas.append({'path':source['path'],'sha':source['sha'],'rows':pf.metadata.num_rows,
                        'columns':pf.schema_arrow.names,'url':source['url']})
        if '/run-42569937357-1/' not in source['path'] or not Path(source['path']).name.startswith('groups-'):
            continue
        day = next(day for day in needed if day in source['path'])
        offset = 0
        for batch in pf.iter_batches(batch_size=32768, columns=columns):
            for i, group in enumerate(batch.to_pylist()):
                if group['group_ordinal'] in needed[day]:
                    key = (day,group['group_ordinal'])
                    assert key not in found, key
                    found[key] = {'source_path':source['path'],'source_blob':source['sha'],
                                  'source_row':offset+i,'source_url':source['url'],'values':group}
            offset += batch.num_rows
    joins, errors = [], []
    cases = {}
    for row in clocks:
        cid = row['case_id']
        if cid not in cases:
            d = json.loads(gzip.decompress((OUT/'raw'/f'{cid}.json.gz').read_bytes()))
            cases[cid] = (d,{h:i for i,h in enumerate(d['headers'])})
        d,index = cases[cid]
        rawrow = d['rows'][row['row']]
        for slot in ['before','during']:
            key = (cid[:8],row[slot+'_group'])
            if key not in found:
                errors.append([cid,row['row'],slot,'source_group_missing'])
                continue
            hit = found[key]
            vals = hit['values']
            if int(row[slot+'_known_by_ns']) != vals['known_by_ns']:
                errors.append([cid,row['row'],slot,'known_by_mismatch'])
            for field in ['L039 | full_bid_ask_depth','L040 | price_level_and_order_counts','L045 | spread_and_depth_imbalance']:
                payload = json.loads(rawrow[index[field]])['values'][slot]
                for name,value in payload.items():
                    if name in vals and value != vals[name]:
                        errors.append([cid,row['row'],slot,name,'value_mismatch'])
            if slot == 'during':
                for keyname in ['first_cursor','close_cursor']:
                    if int(row['group_'+keyname]) != vals[keyname]:
                        errors.append([cid,row['row'],slot,keyname,'cursor_mismatch'])
            joins.append({'case_id':cid,'row':row['row'],'slot':slot,
                          'group_ordinal':vals['group_ordinal'],'known_by_ns':str(vals['known_by_ns']),
                          **{k:hit[k] for k in ['source_path','source_blob','source_row','source_url']}})
    assert len(joins) == 2*5513
    assert not errors, errors[:20]
    (OUT/'source_group_joins.jsonl.gz').write_bytes(gzip.compress(
        ''.join(json.dumps(r,separators=(',',':'))+'\n' for r in joins).encode(),mtime=0))
    dump('source_schemas.json',schemas)
    verification = {'group_joins':len(joins),'unique_source_groups':len(found),'errors':errors,
        'compared':'before/during availability; source group cursors for during; all scalar book members in L039/L040/L045',
        'limitations':'Does not reconstruct all non-trade groups, flows, action semantics or order lifecycles.',
        'strategy_execution':False}
    dump('SOURCE_JOIN_VERIFICATION.json',verification)
    print(json.dumps(verification,indent=2))


if __name__ == '__main__':
    main()
