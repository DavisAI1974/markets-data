"""Retain all recovered workflow rows and index only exact, named source clocks."""
from acquire import ROOT
import csv,gzip,json,re,decimal,collections,bisect,datetime,sys
import pyarrow.parquet as pq
O=ROOT/'current';prefix='remaining' if '--remaining' in sys.argv else 'workflow'
sources=json.loads((ROOT/('remaining_research_sources.json' if prefix=='remaining' else 'workflow_sources.json')).read_text())
DAYS=['20231002','20231003','20231017','20231018'];LO=1577836800000000000;HI=1893456000000000000
cache=ROOT.parent.parent.parent/'unused'
from pathlib import Path
cache=Path('E:/markets-data-frankie-audit-20261109/tasks/family-research-20261022/native-dipole/20261108-33693e180/agent-pass/cache')
groups={d:pq.read_table(cache/f'groups-{d}.parquet',columns=['receive_ns','cursor']).to_pydict() for d in DAYS}
trades={d:collections.defaultdict(set) for d in DAYS}
with (O/'trade_spine.csv').open(newline='',encoding='utf8') as f:
 for r in csv.DictReader(f):
  for k in ['receive_ns','known_by_ns']:trades[r['day']][int(r[k])].add(r['trade_id'])
heads=['source_id','source_row_0based','day','record_identity','primary_clock_field','primary_clock_ns_exact','clock_role','observed_group_receive_ns_exact','observed_group_cursor','exact_trade_ids','all_clock_fields_json','record_status']
files={d:(O/f'{prefix}-pins-{d}.csv').open('w',newline='',encoding='utf8') for d in DAYS+['crossday']}
writers={d:csv.writer(f) for d,f in files.items()}
for w in writers.values():w.writerow(heads)
def clean(v):
 if isinstance(v,(datetime.date,datetime.datetime)):return v.isoformat()
 if isinstance(v,bytes):return {'bytes_hex':v.hex()}
 if isinstance(v,decimal.Decimal):return str(v)
 raise TypeError(type(v).__name__)
def rows(s):
 f=ROOT/'objects'/s['sha'];p=s['path']
 if p.endswith('.parquet'):
  for b in pq.ParquetFile(f).iter_batches(batch_size=4096):yield from b.to_pylist()
 else:
  op=gzip.open(f,'rt',encoding='utf-8-sig') if p.endswith('.gz') else f.open(encoding='utf-8-sig')
  with op:
   if '.csv' in p:yield from csv.DictReader(op)
   else:
    for l in op:
     if l.strip():yield json.loads(l)
def clocks_of(r,prefix='',result=None,issues=None):
 result={} if result is None else result;issues=[] if issues is None else issues
 for k,v in r.items():
  key=prefix+k
  if isinstance(v,dict):clocks_of(v,key+'.',result,issues);continue
  if not (k.endswith('_ns') or k.endswith('_epoch_s') or k in ['second','birth_second','available_second','last_closed_second','event_second']):continue
  try:n=decimal.Decimal(str(v))
  except decimal.InvalidOperation:continue
  if not n.is_finite():continue
  if k.endswith('_ns') and LO<=n<=HI:
   if isinstance(v,float) or 'e' in str(v).lower() or n!=int(n):issues.append('Exact source required: '+key)
   else:result[key]=str(int(n))
  elif not k.endswith('_ns') and LO//10**9<=n<=HI//10**9:
   scaled=n*10**9
   if scaled==int(scaled):result[key]=str(int(scaled))
 return result,issues
priority=['known_by_ns','available_ns','decision_known_by_ns','signal_known_by_ns','source_known_by_ns','trade_known_by_ns','decision_ns','receive_ns','start_recv_ns','signal_receive_ns','recognition_ns','event_ns','start_ns','second','anchor_ns','target_ns']
counts=collections.Counter();seen={};catalog=[]
for s in sources:
 s.update(record_rows=0,pinned_rows=0,attachment_rows=0,issues=0)
 if s['sha'] in seen:
  s.update(handling='Identical complete content retained under '+seen[s['sha']],canonical_source_id=seen[s['sha']]);catalog.append(s);continue
 seen[s['sha']]=s['id'];s['current_attachment']='evidence/'+s['id']+'.jsonl.gz'
 m=re.search(r'202310(?:02|03|17|18)',s['path']);pathday=m[0] if m else ''
 with gzip.open(O/s['current_attachment'],'wt',encoding='utf8',compresslevel=1) as out:
  for i,r in enumerate(rows(s)):
   if not isinstance(r,dict):r={'source_array':r}
   clocks,issues=clocks_of(r);day=pathday or str(r.get('day',r.get('session',r.get('date','')))).replace('-','');day=day if day in DAYS else ''
   primary=next((k for k in priority if k in clocks),next(iter(clocks),''))
   if primary:
    n=int(clocks[primary]);obs='';cursor='';exact=[]
    if day:
     g=groups[day];j=bisect.bisect_right(g['receive_ns'],n)-1
     if j>=0:obs=str(g['receive_ns'][j]);cursor=str(g['cursor'][j])
     exact=sorted(trades[day].get(n,[]))
    identity=next((str(r[k]) for k in ['trade_id','candidate_id','family_id','instance_id','signal_id','case_id','row'] if r.get(k) is not None),str(i))
    role='Source clock; preserved field definition'
    if any(t in primary for t in ['cutoff','target','anchor']):role='Scheduled cutoff/target/anchor; not observed endpoint'
    elif primary.endswith(('second','epoch_s')):role='Second-resolution source label'
    elif 'known_by' in primary or 'available' in primary:role='Source availability clock'
    writers[day or 'crossday'].writerow([s['id'],i,day,identity,primary,clocks[primary],role,obs,cursor,';'.join(exact),json.dumps(clocks,separators=(',',':')),'Included; unresolved fields separately listed' if issues else 'Included'])
    s['pinned_rows']+=1;counts[day or 'crossday']+=1
   else:s['attachment_rows']+=1
   s['record_rows']+=1;s['issues']+=bool(issues)
   out.write(json.dumps({'source_row_0based':i,'data':r,'pin_clocks_ns':clocks,'clock_derivations':{},'clock_issues':issues},separators=(',',':'),default=clean)+'\n')
 s['handling']='Every row retained; exact source clocks indexed; comparisons and unbound rows attached'
 catalog.append(s)
 print(s['id'],s['record_rows'],s['pinned_rows'],flush=True)
 (O/f'{prefix}_source_catalog.progress.json').write_text(json.dumps(catalog,indent=2))
for f in files.values():f.close()
(O/f'{prefix}_source_catalog.json').write_text(json.dumps(catalog,indent=2))
(O/f'{prefix}_coverage.json').write_text(json.dumps({'pins':dict(counts),'rows':sum(s['record_rows'] for s in catalog),'attachments':sum(s['attachment_rows'] for s in catalog),'issue_rows':sum(s['issues'] for s in catalog)},indent=2))
print('WORKFLOW COMPLETE',dict(counts),flush=True)
