"""Recover original action intervals and as-of native observations; never run S."""
import argparse
import bisect
import collections
import gzip
import hashlib
import json
from pathlib import Path
import sys
import urllib.request

OUT=Path(__file__).resolve().parent
AUDIT=OUT.parent/'evidence-availability-20261113'
FULL_POPULATION=False


def read(path):
    return json.loads(path.read_text(encoding='utf8'))


def write(path, value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,indent=2)+'\n',encoding='utf8',newline='\n')


def jsonlines(path, records):
    path.parent.mkdir(parents=True,exist_ok=True)
    with gzip.GzipFile(filename=str(path),mode='wb',mtime=0) as stream:
        for row in records:
            stream.write((json.dumps(row,separators=(',',':'))+'\n').encode())


def verified(root, pub, entry, kind):
    candidates=[root/'retained-native'/pub['day']/entry['path'],
                root/kind/pub['day']/entry['path'],OUT/'cache'/pub['day']/entry['path']]
    path=next((p for p in candidates if p.exists()),candidates[-1])
    if not path.exists():
        path.parent.mkdir(parents=True,exist_ok=True)
        with urllib.request.urlopen(f"https://raw.githubusercontent.com/{pub['repository']}/{pub['revision']}/{pub['prefix']}/{entry['path']}",timeout=120) as response:
            path.write_bytes(response.read())
    raw=path.read_bytes()
    assert len(raw)==entry['bytes'] and hashlib.sha256(raw).hexdigest()==entry['sha256'],str(path)
    return path


def targets(day):
    result=[]
    if FULL_POPULATION:
        import pyarrow.parquet as pq
        prior=-1
        receipt=read(OUT/f'source_manifests/book-{day}.json')['receipt']
        warmup=receipt['original_replay_receipt'].get('opening_warmup_records',0)
        for path in sorted((OUT/'original_full_population'/day).glob('*.parquet')):
            for row in pq.read_table(path,columns=['trade_ordinal','trade_cursor','receive_ns']).to_pylist():
                cursor=int(row['trade_cursor'])
                result.append(dict(case_id=day+'-full',case_row=row['trade_ordinal'],cursor=cursor,
                    start_cursor=prior+1,clock=int(row['receive_ns']),stream_ordinal=cursor+warmup))
                prior=cursor
        return result
    for path in sorted((OUT/'book_records').glob(day+'-*.jsonl.gz')):
        with gzip.open(path,'rt',encoding='utf8') as stream:
            rows=sorted((json.loads(line) for line in stream),key=lambda r:r['case_row'])
        prior=None
        for row in rows:
            trade=row['original']['original_trade']
            cursor=trade['trade_input_cursor']
            start=prior+1 if prior is not None else trade['strict_prior_clocks']['close_cursor']+1
            result.append(dict(case_id=row['case_id'],case_row=row['case_row'],
                               cursor=cursor,start_cursor=start,clock=trade['receive_ns'],
                               stream_ordinal=row['original']['source_stream_ordinal']))
            prior=cursor
    return result


def recover_actions(root, pubs):
    totals={}
    for pub in pubs:
        day=pub['day']; ticks=targets(day)
        bundle=read(OUT/f'source_manifests/book-{day}.json')
        warmup=bundle['receipt']['original_replay_receipt'].get('opening_warmup_records',0)
        by_case=collections.defaultdict(list)
        for tick in ticks:
            by_case[tick['case_id']].append(tick)
            assert tick['stream_ordinal']==tick['cursor']+warmup
        buckets={(t['case_id'],t['case_row']):[] for t in ticks}
        searches={case:([t['cursor'] for t in seq],seq) for case,seq in by_case.items()}
        pins=[]
        offset=0
        for entry in bundle['manifest']['files']:
            if not entry['path'].startswith('native-messages-'):continue
            lo,hi=offset-warmup,offset+entry['rows']-1-warmup
            offset+=entry['rows']
            if not any(lo<=seq[-1]['cursor'] and hi>=seq[0]['start_cursor'] for seq in by_case.values()):continue
            path=verified(root,pub,entry,'mbo-message-cache');pins.append(entry)
            with gzip.open(path,'rt',encoding='utf8') as stream:
                for line_no,line in enumerate(stream):
                    original=json.loads(line)
                    if original['source_stream_ordinal']<warmup:continue
                    cursor=original['adapter_input_cursor']
                    for case,(ends,seq) in searches.items():
                        pos=bisect.bisect_left(ends,cursor)
                        if pos==len(seq) or cursor<seq[pos]['start_cursor']:continue
                        t=seq[pos]
                        buckets[case,t['case_row']].append(dict(original=original,
                            source=dict(path=entry['path'],row=line_no,sha256=entry['sha256'])))
        counts=collections.Counter()
        for case,seq in by_case.items():
            records=[]
            for tick in seq:
                values=buckets[case,tick['case_row']]
                assert len(values)==tick['cursor']-tick['start_cursor']+1,(tick,len(values))
                assert [v['original']['adapter_input_cursor'] for v in values]==list(range(tick['start_cursor'],tick['cursor']+1))
                clocks=[v['original']['original_message']['ts_recv_ns'] for v in values]
                records.append(dict(case_row=tick['case_row'],start_cursor=tick['start_cursor'],
                    end_cursor=tick['cursor'],phase='through_trade_input',
                    known_by_ns=max(clocks),trade_receive_ns=tick['clock'],
                    available_by_trade_receive=max(clocks)<=tick['clock'],events=values))
                counts.update(v['original']['original_message']['action'] for v in values)
            jsonlines(OUT/f'event_records/{case}.jsonl.gz',records)
        write(OUT/f'source_manifests/actions-{day}.json',dict(publication=pub,shards=pins,
            scope='Every message between consecutive retained trades within each case; first tick begins after its strict-prior group close. No fixed time horizon.'))
        totals[day]=dict(counts)
        print(day,'recovered complete selected-case action intervals',dict(counts),flush=True)
    write(OUT/'ACTION_RECOVERY_VERIFICATION.json',totals)


def recover_native(root,pubs):
    import pyarrow.parquet as pq
    all_counts={}
    # Source observations only. These do not manufacture missing model runs or ancestry state.
    wanted_sections={'candidate','episode','queue','absorption','replenishment','detector_coverage',
                     'recurrence','mirror','ladder','response','lineage'}
    for pub in pubs:
        day=pub['day']; ticks=targets(day)
        manifest=read(root/f'recovered-packets/native/{day}/MANIFEST.json')
        files={e['path']:e for e in manifest['files']}
        best=[{} for _ in ticks]
        for entry in manifest['files']:
            if not entry['path'].endswith('.parquet'):continue
            path=verified(root,pub,entry,'native-index-cache')
            sections=collections.defaultdict(list)
            for row in pq.read_table(path).to_pylist():
                if row['emitting_section'] in wanted_sections and row['known_by_ns'] is not None:
                    sections[row['emitting_section']].append(row)
            for section,rows in sections.items():
                rows.sort(key=lambda r:(r['known_by_ns'],r['input_cursor'] if r['input_cursor'] is not None else -1))
                keys=[(r['known_by_ns'],r['input_cursor'] if r['input_cursor'] is not None else -1) for r in rows]
                for i,tick in enumerate(ticks):
                    end=bisect.bisect_right(keys,(tick['clock'],tick['cursor']))
                    if not end:continue
                    clock=rows[end-1]['known_by_ns']
                    start=bisect.bisect_left(keys,(clock,-1))
                    previous=best[i].get(section)
                    if previous is None or previous['clock']<clock:
                        best[i][section]=dict(clock=clock,rows=rows[start:end])
                    elif previous['clock']==clock:previous['rows'].extend(rows[start:end])
        wanted=collections.defaultdict(set)
        for values in best:
            for v in values.values():
                for row in v['rows']:wanted[row['shard']].add(row['shard_row'])
        originals={}
        for shard,positions in sorted(wanted.items()):
            path=verified(root,pub,files[shard],'native-index-cache')
            with gzip.open(path,'rt',encoding='utf8') as stream:
                for pos,line in enumerate(stream):
                    if pos in positions:
                        obj=json.loads(line);key=f'{shard}:{pos}'
                        originals[key]=dict(id=key,original=obj,source=dict(path=shard,row=pos,sha256=files[shard]['sha256']))
        joins=collections.defaultdict(list)
        for tick,values in zip(ticks,best):
            sections={}
            for section,value in values.items():
                ids=[]
                for idx in sorted(value['rows'],key=lambda r:r['source_row']):
                    key=f"{idx['shard']}:{idx['shard_row']}";obj=originals[key]['original']
                    assert obj['emitted_at_recv_ns']==value['clock']<=tick['clock']
                    assert obj['emitting_section']==section
                    ids.append(key)
                sections[section]=dict(known_by_ns=value['clock'],record_ids=ids)
            joins[tick['case_id']].append(dict(case_row=tick['case_row'],asof_receive_ns=tick['clock'],sections=sections))
        jsonlines(OUT/f'native_records/{day}.jsonl.gz',originals.values())
        for case,records in joins.items():jsonlines(OUT/f'native_joins/{case}.jsonl.gz',records)
        write(OUT/f'source_manifests/native-{day}.json',dict(publication=pub,manifest=manifest,
            join='Latest saved emission per section at or before trade receive/cursor; all same-clock eligible ties. An observation, not a complete active-state reconstruction.'))
        all_counts[day]=dict(ticks=len(ticks),unique_records=len(originals))
        print(day,'native observations',all_counts[day],flush=True)
    # Oct 18 original extracted candidate/episode/coverage ledger; no newer independent research.
    day='20231018';ticks=targets(day);originals={};sections={};pins=[]
    for section in ['candidate','episode','detector_coverage']:
        path=root/f'oct18-original/source-{section}.jsonl.gz';raw=path.read_bytes()
        pin=dict(path=str(path),sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw));pins.append(pin)
        rows=[]
        with gzip.open(path,'rt',encoding='utf8') as stream:
            for pos,line in enumerate(stream):
                record=json.loads(line);key=f'{section}:{pos}'
                if record.get('known_by_ns') is None:continue
                rows.append((record['known_by_ns'],record.get('input_cursor') or -1,key,record))
        rows.sort(key=lambda r:r[:3]);sections[section]=rows
    joins=collections.defaultdict(list)
    for tick in ticks:
        values={}
        for section,rows in sections.items():
            keys=[r[:2] for r in rows]
            end=bisect.bisect_right(keys,(tick['clock'],tick['cursor']))
            if not end:continue
            clock=rows[end-1][0];start=bisect.bisect_left(keys,(clock,-1));ids=[]
            for _,_,key,record in rows[start:end]:
                originals[key]=dict(id=key,original=record['original_record'],source=record)
                ids.append(key)
            values[section]=dict(known_by_ns=clock,record_ids=ids)
        joins[tick['case_id']].append(dict(case_row=tick['case_row'],asof_receive_ns=tick['clock'],sections=values))
    jsonlines(OUT/f'native_records/{day}.jsonl.gz',originals.values())
    for case,records in joins.items():jsonlines(OUT/f'native_joins/{case}.jsonl.gz',records)
    write(OUT/f'source_manifests/native-{day}.json',dict(local_source_pins=pins,
        scope='Original Oct18 candidate/episode/coverage source extraction, actual selected original records bundled. Queue/absorption/replenishment not asserted available from this extraction.'))
    all_counts[day]=dict(ticks=len(ticks),unique_records=len(originals))
    write(OUT/'NATIVE_RECOVERY_VERIFICATION.json',all_counts)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--recovery',type=Path,required=True)
    parser.add_argument('--python-deps',type=Path)
    parser.add_argument('--mode',choices=['actions','native','both'],default='both')
    parser.add_argument('--full-population',action='store_true')
    args=parser.parse_args()
    FULL_POPULATION=args.full_population
    if args.python_deps:sys.path.insert(0,str(args.python_deps))
    if args.mode in ('actions','both'):recover_actions(args.recovery,read(args.recovery/'recovered-packets/PUBLICATIONS.json'))
    if args.mode in ('native','both'):recover_native(args.recovery,read(args.recovery/'recovered-packets/NATIVE_PUBLICATIONS.json'))
