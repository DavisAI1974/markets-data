import bisect,collections,gzip,hashlib,io,json,pathlib,urllib.request
import pyarrow as pa
import pyarrow.parquet as pq
ROOT=pathlib.Path(__file__).parent;OUT=ROOT/'flow-input-recovery';directory=OUT/'20231018';directory.mkdir(exist_ok=True)
path=ROOT/'oct18-original/all-8088-original-flow-seconds-with-tape.jsonl.gz'
source_path='artifacts/sqlite-triage/20261022/families/trade-lifecycle-targeted-v1/day-wide-mechanisms-v1/'+path.name
pin=next(p for p in json.loads((ROOT/'sources/INPUT_PINS.json').read_text())['sources'] if p['path']==source_path)
assert hashlib.sha256(path.read_bytes()).hexdigest()==pin['sha256']
by_clock=collections.defaultdict(list);rows=0
with gzip.open(path,'rt',encoding='utf-8') as stream:
    for number,line in enumerate(stream):
        row=json.loads(line);original=row['original_flow_record'];rows+=1
        by_clock[original['known_by_ns']].append(dict(source_line=number,original_record=original))
clocks=sorted(by_clock)
url='https://raw.githubusercontent.com/DavisAI1974/markets-data/87dc338f2e74646eb731b3cd6f8968a5a0a653e2/tasks/family-research-20261022/combined-events/run-42571551209-1/events-20231018/a-trades.parquet'
with urllib.request.urlopen(url,timeout=180) as response:data=response.read()
trades=pq.read_table(io.BytesIO(data)).to_pylist();output=[];matched=0
for ordinal,trade in enumerate(trades):
    cutoff=int(trade['receive_ns']);index=bisect.bisect_right(clocks,cutoff)-1
    if index<0:payload=dict(status='NOT_YET_EMITTED_IN_RETAINED_PROJECTION',reason='No original retained flow emission is known by this trade clock')
    else:
        selected=by_clock[clocks[index]]
        assert all(r['original_record']['known_by_ns']<=cutoff for r in selected)
        payload=dict(status='ORIGINAL_RETAINED_FLOW_ASOF',known_by_ns=clocks[index],asof_receive_ns=cutoff,records=selected,source=pin,
            rule='Latest emission in the saved projection at or before receive time; every tied source row retained. The projection is not asserted to contain the complete Native flow stream.',complete_flow_stream=False)
        matched+=1
    raw=json.dumps(payload,separators=(',',':'))
    output.append(dict(day='20231018',trade_ordinal=ordinal,trade_id=f'20231018:trade:{ordinal}',receive_ns=str(cutoff),**{'L055 | legacy_native_signed_flow':raw,'L056 | legacy_per_second_roll20':raw}))
pq.write_table(pa.Table.from_pylist(output),directory/'trade-flow-inputs.parquet',compression='zstd')
receipt=dict(day='20231018',trades=len(trades),matched_original_emissions=matched,not_yet_emitted_in_retained_projection=len(trades)-matched,original_flow_rows=rows,source=pin,trade_source_sha256=hashlib.sha256(data).hexdigest(),complete_flow_stream=False,calculation_rerun=False,complete_all_layers=False)
(directory/'RECEIPT.json').write_text(json.dumps(receipt,indent=1))
summaries=[json.loads(p.read_text()) for p in sorted(OUT.glob('*/RECEIPT.json'))]
(OUT/'SUMMARY.json').write_text(json.dumps(summaries,indent=1))
manifest=[]
for p in sorted(OUT.rglob('*')):
    if p.is_file() and p.name!='MANIFEST.json':
        data=p.read_bytes();manifest.append(dict(path=p.relative_to(OUT).as_posix(),bytes=len(data),sha256=hashlib.sha256(data).hexdigest()))
(OUT/'MANIFEST.json').write_text(json.dumps(dict(files=manifest),indent=1))
print(json.dumps({k:v for k,v in receipt.items() if k!='source'}))
