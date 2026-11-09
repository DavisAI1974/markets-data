"""Join exact saved Native emissions to review clocks; retain every tied row.

These are latest-emission examples, not replacements for the full pinned ledger.
Unknown emission clocks are excluded rather than treated as zero or historical.
"""
import collections,concurrent.futures,gzip,hashlib,json,pathlib,urllib.request
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq
ROOT=pathlib.Path(__file__).parent
def read(p):return json.loads((ROOT/p).read_text())
samples=read('filled-review/REVIEW_SAMPLES.json');pubs=read('recovered-packets/NATIVE_PUBLICATIONS.json')
result=[]
for pub in pubs:
    day=pub['day'];directory=ROOT/'native-index-cache'/day;directory.mkdir(parents=True,exist_ok=True)
    manifest=read(f'recovered-packets/native/{day}/MANIFEST.json');files={r['path']:r for r in manifest['files']}
    def fetch(item):
        path=directory/item['path'];retained=ROOT/'retained-native'/day/item['path']
        if retained.is_file():path=retained
        if not path.is_file():
            with urllib.request.urlopen(f'https://raw.githubusercontent.com/{pub["repository"]}/{pub["revision"]}/{pub["prefix"]}/{item["path"]}',timeout=180) as response:data=response.read()
            path.write_bytes(data)
        data=path.read_bytes();assert len(data)==item['bytes'] and hashlib.sha256(data).hexdigest()==item['sha256']
        return path
    index_files=[r for r in manifest['files'] if r['path'].endswith('.parquet')]
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:paths=list(pool.map(fetch,index_files))
    day_samples=[s for s in samples if s['day']==day]
    best={s['trade_id']:{} for s in day_samples}
    for path in paths:
        table=pq.read_table(path)
        for sample in day_samples:
            cutoff=int(sample['receive_ns']);eligible=table.filter(pc.less_equal(table['known_by_ns'],cutoff))
            if not len(eligible):continue
            maxima=eligible.group_by('emitting_section').aggregate([('known_by_ns','max')]).to_pylist()
            for maximum in maxima:
                section=maximum['emitting_section'];clock=maximum['known_by_ns_max'];prior=best[sample['trade_id']].get(section)
                if prior and prior['clock']>clock:continue
                rows=eligible.filter(pc.and_(pc.equal(eligible['emitting_section'],section),pc.equal(eligible['known_by_ns'],clock))).to_pylist()
                if prior and prior['clock']==clock:prior['index_rows'].extend(rows)
                else:best[sample['trade_id']][section]=dict(clock=clock,index_rows=rows)
    wanted=collections.defaultdict(set)
    for sections in best.values():
        for value in sections.values():
            for row in value['index_rows']:wanted[row['shard']].add(row['shard_row'])
    originals={}
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:shards=list(pool.map(fetch,[files[name] for name in sorted(wanted)]))
    for path in shards:
        with gzip.open(path,'rt',encoding='utf-8') as stream:
            for ordinal,line in enumerate(stream):
                if ordinal in wanted[path.name]:originals[path.name,ordinal]=json.loads(line)
    for sample in day_samples:
        section_values={}
        for section,entry in best[sample['trade_id']].items():
            values=[]
            for index in sorted(entry['index_rows'],key=lambda x:x['source_row']):
                original=originals[index['shard'],index['shard_row']]
                assert original['emitting_section']==section
                assert original['emitted_at_recv_ns']==index['known_by_ns']<=int(sample['receive_ns'])
                values.append(dict(index=index,original=original))
            section_values[section]=dict(latest_emission_ns=entry['clock'],records=values)
        result.append(dict(trade_id=sample['trade_id'],day=day,asof_receive_ns=sample['receive_ns'],source=pub,sections=section_values,
            scope='Latest saved emission at or before this trade clock, all same-section time ties retained. Full prior history remains in the immutable ledger and clock indices. This does not establish complete named-layer semantics.'))
    print(day,'joined samples',len(day_samples),'original records',len(originals),flush=True)
out=ROOT/'filled-review/NATIVE_REVIEW_VALUES.json';out.write_text(json.dumps(result,indent=1))
print('retained native examples',len(result),'bytes',out.stat().st_size,flush=True)
