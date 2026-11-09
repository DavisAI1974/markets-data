from acquire import ROOT
import json,gzip,datetime,csv
O=ROOT/'current';catalog=json.loads((O/'source_catalog.json').read_text());repaired=[]
for s in catalog:
 if s['id'] not in ['S00092','S00096','S00101','S00105']:continue
 p=O/s['current_attachment'];tmp=p.with_suffix('.repair');n=0
 with gzip.open(p,'rt',encoding='utf8') as inp,gzip.open(tmp,'wt',encoding='utf8',compresslevel=3) as out:
  for l in inp:
   obj=json.loads(l);r=obj['data'];t0=int(r['t0_epoch_s']);assert t0==int(r['day0_epoch_s'])+int(r['t0'])
   for field,offset in [('info_horizon_local_s',5),('info_horizon_refractory_s',50)]:
    assert r[field]==offset
    epoch=t0+offset;r[field+'_epoch_s']=epoch;r[field+'_utc']=datetime.datetime.fromtimestamp(epoch,datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    obj['pin_clocks_ns'][field+'_epoch_s']=str(epoch*10**9)
    obj['clock_derivations'][field+'_epoch_s']='Corrected scheduled horizon: event t0_epoch_s + original duration offset. Not a raw observed endpoint.'
   obj['clock_issues']=[v for v in obj['clock_issues'] if not v.startswith('Horizon offset clock needs producer semantics:')]
   out.write(json.dumps(obj,separators=(',',':'),ensure_ascii=False)+'\n');n+=1
 tmp.replace(p);s['issues']=0;s['clock_corrections']=n;s['handling']='All rows retained; scheduled horizon labels corrected from event origin';repaired.append({'source_id':s['id'],'records':n,'fields_per_record':2,'basis':'Original event t0 plus producer local/refractory offsets 5/50 seconds; source attach_clocks.py incorrectly used DAY0; case-context clock dictionaries corroborate duration meaning'})
(O/'source_catalog.json').write_text(json.dumps(catalog,indent=2));(O/'horizon_clock_corrections.json').write_text(json.dumps(repaired,indent=2))
coverage=json.loads((O/'coverage.json').read_text());coverage['clock_issue_records']=0;coverage['corrected_horizon_records']=sum(r['records'] for r in repaired);(O/'coverage.json').write_text(json.dumps(coverage,indent=2))
with (O/'clock_gaps.csv').open('w',newline='') as f:csv.writer(f).writerow(['source_id','gap','affected_rows'])
print('Repaired',sum(r['records'] for r in repaired),'records without retaining wrong generated values in active evidence')
