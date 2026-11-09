"""Retain omitted existing October 2 external evidence without changing clocks."""
import collections,concurrent.futures,gzip,hashlib,json,pathlib,subprocess,urllib.request
ROOT=pathlib.Path(__file__).parent/'external-recovery'
REV='ef89f83b6298983052f94080be64240d7abc0056'
BASE='research/kalshi/adaptive_wavepacket_20261108/markets_bridge/tasks/october02-external-recovery'
FILES=['README.md','october02-external-recovery.json','october02-mos-reconstruction.json','october02-ngx3-curve-trades-crosscheck.json','october02-normalized-evidence.jsonl.gz','cftc-disaggregated-futures-only-through-2023-09-26.json','recover_october02.py','reconstruct_october02_mos.py']
def fetch(name):
    url=f'https://raw.githubusercontent.com/DavisAI1974/Markets/{REV}/{BASE}/{name}'
    with urllib.request.urlopen(url,timeout=180) as response:data=response.read()
    if name.endswith('.json'):json.loads(data)
    (ROOT/name).write_bytes(data)
    return dict(path=name,source_path=BASE+'/'+name,revision=REV,repository='DavisAI1974/Markets',bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),url=url)
def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:files=list(pool.map(fetch,FILES))
    ledger=next(x for x in files if x['path']=='october02-normalized-evidence.jsonl.gz')
    assert ledger['sha256']=='0e3227cb1df9d4d10ca26a246784f2c0acd95ff168e84344b511009e4de11c43'
    counts=collections.Counter();fields=set();samples={};rows=0
    with gzip.open(ROOT/ledger['path'],'rt',encoding='utf-8') as stream:
        for line in stream:
            obj=json.loads(line);rows+=1;fields.update(obj)
            key=str(obj['point_name'])
            counts[key]+=1;samples.setdefault(key,obj)
    assert rows==146800,rows
    receipt=dict(schema='FRANKIE_EXTERNAL_RESTORATION_V1',day='20231002',rows=rows,fields=sorted(fields),series_counts=dict(counts),complete_source_restored=True,complete_all_layers=False,rule='Original numeric values and all publication, availability, held and causal flags are retained unchanged. Restoring a value does not prove its historical availability.')
    (ROOT/'MANIFEST.json').write_text(json.dumps(dict(files=files),indent=2))
    (ROOT/'RECOVERY_RECEIPT.json').write_text(json.dumps(receipt,indent=2))
    (ROOT/'REVIEW_SAMPLES.json').write_text(json.dumps(samples,indent=2))
    print(json.dumps(receipt))
if __name__=='__main__':main()
