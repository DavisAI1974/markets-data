from acquire import ROOT
import json,csv,gzip,hashlib,collections,decimal
import pyarrow.parquet as pq
inventory=json.loads((ROOT/'source_inventory.json').read_text())
cases=json.loads((ROOT/'price_response_clock_fields.json').read_text())
cache=ROOT.parent.parent.parent.parent/'markets-data-frankie-audit-20261109/tasks/family-research-20261022/native-dipole/20261108-33693e180/agent-pass/cache'
# This explicit path is a read-only existing Git-source cache.
cache=__import__('pathlib').Path('E:/markets-data-frankie-audit-20261109/tasks/family-research-20261022/native-dipole/20261108-33693e180/agent-pass/cache')
out=[]; fixes=0
for day in sorted({c['day'] for c in cases}):
    sr=next(r for r in inventory if r['path'].endswith(f'/agent-pass/tables/{day}-paths.csv.gz'))
    rows=list(csv.DictReader(gzip.open(ROOT/'objects'/sr['sha'],'rt')))
    bykey={(r['candidate_id'],r['kind'],int(float(r['relative_s']))):(i,r) for i,r in enumerate(rows)}
    sources={}
    for kind in ['groups','raw']:
        f=cache/f'{kind}-{day}.parquet'
        ref=next(r for r in inventory if r['path'].endswith(f'/agent-pass/cache/{kind}-{day}.parquet'))
        b=f.read_bytes();assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==ref['sha']
        t=pq.read_table(f)
        sources[kind]=(ref,{int(r['cursor']):r for r in t.to_pylist()})
    for ordinal,c in [(i,c) for i,c in enumerate(cases) if c['day']==day]:
        _,cid,kind,rel=c['case_id'].split(':');rel=int(rel.removeprefix('rel'))
        rownum,start=bykey[cid,kind,rel]; endrow,end=bykey[cid,kind,rel+20]
        cut=int(start['cut_ns']);scheduled=cut+20_000_000_000
        assert cut==int(c['observation_clock_ns'])
        fixes+=int(decimal.Decimal(c['outcome_clock_ns'])!=scheduled)
        obs=sources['groups'][1][int(start['cursor'])];endpoint=sources['groups'][1][int(end['cursor'])]
        raw=sources['raw'][1][int(end['cursor'])]
        assert raw['receive_ns']==endpoint['receive_ns']
        assert endpoint['receive_ns']<=scheduled
        assert int(endpoint['bid_raw'])==round(float(end['bid'])*1e9)
        assert int(endpoint['ask_raw'])==round(float(end['ask'])*1e9)
        out.append(dict(example_ordinal=ordinal+1,case_id=c['case_id'],day=day,candidate_id=cid,relative_s=rel,
          scheduled_observation_cutoff_ns=str(cut),observed_start_receive_ns=str(obs['receive_ns']),
          scheduled_outcome_cutoff_ns=str(scheduled),observed_endpoint_receive_ns=str(endpoint['receive_ns']),
          observation_cursor=str(start['cursor']),endpoint_cursor=str(end['cursor']),endpoint_raw_record_index=raw['record_index'],
          endpoint_tape_day=raw['tape_day'],start_mid=(float(start['bid'])+float(start['ask']))/2,
          endpoint_mid=(float(end['bid'])+float(end['ask']))/2,path_source=sr['id'],path_source_row=rownum,
          endpoint_path_row=endrow,group_source=sources['groups'][0]['id'],raw_source=sources['raw'][0]['id'],
          clock_status='Verified against source path, group cursor and raw record; scheduled and observed clocks distinct'))
(ROOT/'corrected_price_response.json').write_text(json.dumps(sorted(out,key=lambda x:x['example_ordinal']),indent=2))
(ROOT/'price_clock_verification.json').write_text(json.dumps({'examples_verified':len(out),'exported_scheduled_cutoffs_corrected':fixes,'observed_endpoints_verified':len(out),'faulty_values_retained_in_current_records':False},indent=2))
print('VERIFIED',len(out),'scheduled corrections',fixes,'observed endpoints',len(out))
