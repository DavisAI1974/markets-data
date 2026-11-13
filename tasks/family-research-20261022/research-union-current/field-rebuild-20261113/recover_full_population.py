"""Verify all archived full-book snapshots and preserve the original 141-field population."""
import argparse
import concurrent.futures
import gzip
import hashlib
import json
from pathlib import Path
import sys
from recover_inputs import fetch, dump, OUT


def main(args):
    import pyarrow.parquet as pq
    cat=json.loads((args.union/'git-publication/tasks/family-research-20261022/research-union-current/published_source_catalog.json').read_text())
    originals=[r for r in cat if '/run-42608467894-1/' in r['path'] and '/joined-inputs-' in r['path']]
    pins=[];counts={}
    for row in sorted(originals,key=lambda r:r['path']):
        path=args.union/'objects'/row['sha'];raw=path.read_bytes()
        assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==row['sha']
        day=row['path'].split('/')[-2];dest=OUT/'original_full_population'/day/Path(row['path']).name
        dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw)
        table=pq.read_table(dest,columns=['trade_ordinal'])
        counts[day]=counts.get(day,0)+len(table)
        pins.append(dict(row,published_path=str(dest.relative_to(OUT)).replace('\\','/'),rows=len(table)))
    assert counts=={'20231002':37670,'20231003':41410,'20231017':33451,'20231018':30739}
    dump('ORIGINAL_FULL_POPULATION_MANIFEST.json',dict(rows_by_day=counts,sources=pins))
    print('Preserved all 143270 original 141-field rows',flush=True)
    jobs=[]
    for day in counts:
        source=json.loads((OUT/f'source_manifests/book-{day}.json').read_text())
        jobs.extend((source['publication'],entry) for entry in source['manifest']['files'] if entry['path'].startswith('trade-book-fifo-'))
    pins=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for path,pin in pool.map(fetch,jobs):
            pins.append(pin)
            if len(pins)%50==0:print('Full-population book shards verified',len(pins),'/',len(jobs),flush=True)
    dump('FULL_POPULATION_BOOK_SHARDS.json',pins)
    print('All full-population sources fetched and hash verified',flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--union',type=Path,required=True)
    p.add_argument('--python-deps',type=Path,required=True)
    args=p.parse_args();sys.path.insert(0,str(args.python_deps));main(args)
