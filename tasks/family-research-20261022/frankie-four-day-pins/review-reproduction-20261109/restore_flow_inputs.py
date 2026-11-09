"""Restore original Native signed-flow and roll20 values for every saved trade."""
import bisect,collections,concurrent.futures,gzip,hashlib,io,json,pathlib,urllib.request
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq
ROOT=pathlib.Path(__file__).parent
OUT=ROOT/'flow-input-recovery';OUT.mkdir(exist_ok=True)
pubs=json.loads((ROOT/'recovered-packets/NATIVE_PUBLICATIONS.json').read_text())
receipts=[]
for pub in pubs:
    day=pub['day'];cache=ROOT/'native-index-cache'/day;directory=OUT/day;directory.mkdir(exist_ok=True)
    manifest=json.loads((ROOT/f'recovered-packets/native/{day}/MANIFEST.json').read_text());files={x['path']:x for x in manifest['files']}
    def locate(name):
        retained=ROOT/'retained-native'/day/name
        return retained if retained.is_file() else cache/name
    indices=[]
    for entry in manifest['files']:
        if not entry['path'].endswith('.parquet'):continue
        table=pq.read_table(locate(entry['path']))
        indices.extend(table.filter(pc.equal(table['emitting_section'],'flow_substrate')).to_pylist())
    wanted=collections.defaultdict(dict)
    for r in indices:wanted[r['shard']][r['shard_row']]=r
    def fetch(name):
        path=locate(name);entry=files[name]
        if not path.is_file():
            with urllib.request.urlopen(f'https://raw.githubusercontent.com/{pub["repository"]}/{pub["revision"]}/{pub["prefix"]}/{name}',timeout=180) as response:data=response.read()
            path.write_bytes(data)
        data=path.read_bytes();assert len(data)==entry['bytes'] and hashlib.sha256(data).hexdigest()==entry['sha256']
        return path
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:paths=list(pool.map(fetch,sorted(wanted)))
    original={}
    for path in paths:
        with gzip.open(path,'rt',encoding='utf-8') as stream:
            for row,line in enumerate(stream):
                if row not in wanted[path.name]:continue
                index=wanted[path.name][row];obj=json.loads(line)
                assert obj['emitting_section']=='flow_substrate' and obj['emitted_at_recv_ns']==index['known_by_ns']
                original[index['source_row']]=dict(index=index,original_json=line.rstrip('\n'))
    assert len(original)==len(indices)
    by_clock=collections.defaultdict(list)
    for r in indices:
        if r['known_by_ns'] is not None:by_clock[r['known_by_ns']].append(original[r['source_row']])
    clocks=sorted(by_clock)
    url=f'https://raw.githubusercontent.com/DavisAI1974/markets-data/87dc338f2e74646eb731b3cd6f8968a5a0a653e2/tasks/family-research-20261022/combined-events/run-42571551209-1/events-{day}/a-trades.parquet'
    with urllib.request.urlopen(url,timeout=180) as response:trade_bytes=response.read()
    trades=pq.read_table(io.BytesIO(trade_bytes)).to_pylist();output=[];matched=0
    for ordinal,trade in enumerate(trades):
        cutoff=int(trade['receive_ns']);i=bisect.bisect_right(clocks,cutoff)-1
        if i<0:payload=dict(status='NOT_YET_EMITTED',reason='No saved Native flow emission exists by this trade clock')
        else:
            selected=by_clock[clocks[i]];assert all(r['index']['known_by_ns']<=cutoff for r in selected)
            payload=dict(status='ORIGINAL_NATIVE_FLOW_ASOF',asof_receive_ns=cutoff,known_by_ns=clocks[i],records=selected,
                source_repository=pub['repository'],source_revision=pub['revision'],source_prefix=pub['prefix'],
                rule='Latest original Native flow emission at or before receive time; every tied source row retained. Original defined/missing/invalid states are unchanged.')
            matched+=1
        raw=json.dumps(payload,separators=(',',':'))
        output.append(dict(day=day,trade_ordinal=ordinal,trade_id=f'{day}:trade:{ordinal}',receive_ns=str(cutoff),
            **{'L055 | legacy_native_signed_flow':raw,'L056 | legacy_per_second_roll20':raw}))
    pq.write_table(pa.Table.from_pylist(output),directory/'trade-flow-inputs.parquet',compression='zstd')
    receipt=dict(day=day,trades=len(trades),matched_original_emissions=matched,not_yet_emitted=len(trades)-matched,
        original_flow_rows=len(indices),trade_source_sha256=hashlib.sha256(trade_bytes).hexdigest(),source=pub,
        calculation_rerun=False,complete_all_layers=False)
    (directory/'RECEIPT.json').write_text(json.dumps(receipt,indent=1));receipts.append(receipt)
    print(json.dumps({k:v for k,v in receipt.items() if k!='source'}),flush=True)
(OUT/'SUMMARY.json').write_text(json.dumps(receipts,indent=1))
manifest=[]
for p in sorted(OUT.rglob('*')):
    if p.is_file() and p.name!='MANIFEST.json':
        data=p.read_bytes();manifest.append(dict(path=p.relative_to(OUT).as_posix(),bytes=len(data),sha256=hashlib.sha256(data).hexdigest()))
(OUT/'MANIFEST.json').write_text(json.dumps(dict(files=manifest),indent=1))
