"""Recover published full-book snapshots and static/flow inputs for every case tick.

Reads immutable manifests and verifies SHA256 before using a source shard.
Does not run the stopped S-field calculator or any trading strategy.
"""
import argparse
import collections
import concurrent.futures
import gzip
import hashlib
import json
from pathlib import Path
import shutil
import time
import urllib.request

OUT = Path(__file__).resolve().parent
AUDIT = OUT.parent/'evidence-availability-20261113'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def dump(name, obj):
    p=OUT/name
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf8',newline='\n')


def fetch(item):
    pub, entry = item
    target=OUT/'cache'/pub['day']/entry['path']
    target.parent.mkdir(parents=True,exist_ok=True)
    url=f"https://raw.githubusercontent.com/{pub['repository']}/{pub['revision']}/{pub['prefix']}/{entry['path']}"
    if not target.exists():
        for attempt in range(4):
            try:
                with urllib.request.urlopen(url,timeout=120) as response:
                    raw=response.read()
                assert len(raw)==entry['bytes'] and sha(raw)==entry['sha256']
                target.write_bytes(raw)
                break
            except Exception:
                if attempt==3:
                    raise
                time.sleep(2**attempt)
    raw=target.read_bytes()
    assert len(raw)==entry['bytes'] and sha(raw)==entry['sha256']
    return target,dict(day=pub['day'],source_url=url,**entry)


def main(args):
    legacy=args.recovery
    layers=json.loads((legacy/'sources/LAYERS.json').read_text())
    dump('LAYER_REGISTRY.json',layers)
    cases=json.loads((AUDIT/'case_manifest.json').read_text())
    targets=collections.defaultdict(dict)
    for c in cases:
        d=json.loads(gzip.decompress((AUDIT/'raw'/f"{c['case_id']}.json.gz").read_bytes()))
        indexes={h:i for i,h in enumerate(d['headers'])}
        for i,row in enumerate(d['rows']):
            ordinal=int(row[indexes['trade_ordinal']])
            targets[c['day']][ordinal]={'case_id':c['case_id'],'row':i,
                'receive_ns':int(row[indexes['receive_ns']]),'event_ns':int(row[indexes['event_ns']]),
                'trade_cursor':int(row[indexes['trade_cursor']])}
    static=json.loads((legacy/'static-recovery/LAYER_VALUES.json').read_text())
    static_payloads, sources={},{}
    for layer in static:
        entries=[]
        for entry in layer['original_sources']:
            source=legacy/'static-recovery/brain/20261109-search'/entry['name']
            raw=source.read_bytes()
            assert len(raw)==entry['bytes'] and sha(raw)==entry['sha256']
            name='static_content/'+entry['sha256']+'.gz'
            if name not in sources:
                (OUT/name).parent.mkdir(parents=True,exist_ok=True)
                (OUT/name).write_bytes(gzip.compress(raw,mtime=0))
                sources[name]={'path':name,'sha256_uncompressed':entry['sha256'],
                    'bytes_uncompressed':len(raw),'original_source':entry['source']}
            entries.append({'content_path':name,'sha256':entry['sha256'],'bytes':len(raw),
                            'original_registry_path':entry['original_registry_path'],'source_pin':entry['pin']})
        static_payloads[layer['column']]={'status':layer['status'],'values':entries,
            'role':layer['policy'],'availability':'Recovered research knowledge/source content; not a historical market observation or proof of runtime invocation.'}
    dump('STATIC_FIELD_VALUES.json',static_payloads)
    dump('STATIC_CONTENT_MANIFEST.json',list(sources.values()))
    flow_manifest=json.loads((legacy/'flow-input-recovery/MANIFEST.json').read_text())
    flow_pins=[]
    for entry in flow_manifest['files']:
        if not entry['path'].endswith('.parquet'):
            continue
        source=legacy/'flow-input-recovery'/entry['path']
        raw=source.read_bytes()
        assert len(raw)==entry['bytes'] and sha(raw)==entry['sha256']
        dest=OUT/'flow_inputs'/entry['path']
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_bytes(raw)
        receipt=source.parent/'RECEIPT.json'
        shutil.copyfile(receipt,dest.parent/'RECEIPT.json')
        flow_pins.append(dict(entry,published_path='flow_inputs/'+entry['path']))
    dump('FLOW_INPUT_MANIFEST.json',flow_pins)
    pubs=json.loads((legacy/'recovered-packets/PUBLICATIONS.json').read_text())
    jobs=[]
    for pub in pubs:
        manifest=json.loads((legacy/f"recovered-packets/book/{pub['day']}/MANIFEST.json").read_text())
        dump(f"source_manifests/book-{pub['day']}.json",dict(publication=pub,manifest=manifest,
            receipt=json.loads((legacy/f"recovered-packets/book/{pub['day']}/RECOVERY_RECEIPT.json").read_text())))
        offset=0
        for entry in manifest['files']:
            if not entry['path'].startswith('trade-book-fifo-'):
                continue
            if any(offset<=ordinal<offset+entry['rows'] for ordinal in targets[pub['day']]):
                jobs.append((pub,entry))
            offset+=entry['rows']
    print('Recovering',sum(map(len,targets.values())),'ticks from',len(jobs),'verified full-book shards',flush=True)
    pins=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for path,pin in pool.map(fetch,jobs):
            pins.append(pin)
            if len(pins)%10==0:
                print('Fetched',len(pins),'of',len(jobs),flush=True)
    dump('BOOK_SOURCE_SHARDS.json',pins)
    counts=collections.Counter()
    streams={}
    for case in cases:
        p=OUT/'book_records'/f"{case['case_id']}.jsonl.gz"
        p.parent.mkdir(parents=True,exist_ok=True)
        streams[case['case_id']]=gzip.GzipFile(filename=str(p),mode='wb',compresslevel=3,mtime=0)
    try:
        for pub,entry in jobs:
            path=OUT/'cache'/pub['day']/entry['path']
            with gzip.open(path,'rt',encoding='utf8') as f:
                for source_row,line in enumerate(f):
                    record=json.loads(line)
                    target=targets[pub['day']].get(record['trade_ordinal'])
                    if target is None:
                        continue
                    trade=record['original_trade']
                    assert record['known_by_ns']==target['receive_ns']==trade['receive_ns']
                    assert trade['event_ns']==target['event_ns']
                    assert trade['trade_input_cursor']==target['trade_cursor']
                    assert record['phase']=='at_trade_input'
                    for side in ['bid','ask']:
                        levels=record['book_full'][side+'_levels_full']
                        assert sum(level['size'] for level in levels)==record['book_full'][side+'_depth_full']
                        for level in levels:
                            ahead=0
                            for order in level['fifo_queue']:
                                assert order['volume_ahead']==ahead
                                ahead+=order['size']
                            assert ahead==level['size'] and len(level['fifo_queue'])==level['order_count']
                    output=dict(case_id=target['case_id'],case_row=target['row'],original=record,
                        source=dict(repository=pub['repository'],revision=pub['revision'],
                            path=pub['prefix']+'/'+entry['path'],sha256=entry['sha256'],row=source_row))
                    streams[target['case_id']].write((json.dumps(output,separators=(',',':'))+'\n').encode())
                    counts[target['case_id']]+=1
    finally:
        for stream in streams.values():
            stream.close()
    for case in cases:
        assert counts[case['case_id']]==case['tick_appearances']
    dump('INPUT_RECOVERY_VERIFICATION.json',dict(static_fields=len(static_payloads),
        static_content_files=len(sources),book_source_shards=len(pins),book_snapshots=sum(counts.values()),
        per_case_snapshots=dict(counts),flow_days=len(flow_pins),source_hash_checks=True,
        trade_identity_and_exact_clock_checks=True,full_depth_and_fifo_sum_checks=True,
        s_calculations_restarted=False,complete_all_fields=False))
    print('Recovered all',sum(counts.values()),'book/FIFO snapshots,',len(static_payloads),'static fields and four flow tables.',flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--recovery',type=Path,required=True)
    main(parser.parse_args())
