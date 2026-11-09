"""Populate newly recovered original SQLite/Julia and screenshot source tables."""
from acquire import ROOT
import json,csv,gzip,re,decimal,collections,hashlib
O=ROOT/'current'
S=json.loads((ROOT/'expanded_sources.json').read_text())
def rows(s):
 f=ROOT/'objects'/s['sha'];p=s['path']
 if p.endswith(('.csv','.csv.gz')):
  op=gzip.open(f,'rt',encoding='utf-8-sig') if p.endswith('.gz') else f.open(encoding='utf-8-sig')
  with op:yield from csv.DictReader(op)
 elif p.endswith(('.jsonl','.jsonl.gz')):
  op=gzip.open(f,'rt',encoding='utf-8-sig') if p.endswith('.gz') else f.open(encoding='utf-8-sig')
  with op:
   for l in op:
    if l.strip():yield json.loads(l)
 else:return
heads=['source_id','source_row_0based','day','record_identity','primary_clock_field','primary_clock_ns_exact','clock_role','observed_group_receive_ns_exact','observed_group_cursor','exact_trade_ids','all_clock_fields_json','record_status']
def recovered_rows(s):
 dest=O/'evidence'/f"{s['id']}.jsonl.gz"
 if dest.exists() and s['id']<'S14704':
  with gzip.open(dest,'rt',encoding='utf8') as f:
   for l in f:
    if '"pin_clocks_ns":{}' in l:yield None
    else:yield json.loads(l)['data']
 else:
  for r in rows(s):yield r if isinstance(r,dict) else {'source_array':r}
hs={};ws={};counts=collections.Counter()
for day in ['20231002','20231003','20231017','20231018','crossday']:
 hs[day]=(O/f'extra-pins-{day}.csv').open('w',newline='',encoding='utf8');ws[day]=csv.writer(hs[day]);ws[day].writerow(heads)
for s in S:
 s.update(record_rows=0,pinned_rows=0,attachment_rows=0,handling='Complete immutable artifact attachment')
 if not s['path'].endswith(('.csv','.csv.gz','.jsonl','.jsonl.gz')):continue
 s['current_attachment']=f"evidence/{s['id']}.jsonl.gz"
 reuse=(O/s['current_attachment']).exists() and s['id']<'S14704'
 import contextlib
 with (contextlib.nullcontext(None) if reuse else gzip.open(O/s['current_attachment'],'wt',encoding='utf8',compresslevel=3)) as out:
  for i,r in enumerate(recovered_rows(s)):
   if r is None:
    s['record_rows']+=1;s['attachment_rows']+=1;continue
   clocks={}
   for k,v in r.items():
    if not k.endswith('_ns') or v in ['',None]:continue
    try:n=decimal.Decimal(str(v))
    except decimal.InvalidOperation:continue
    if n.is_finite() and 1_577_836_800_000_000_000<=n<=1_893_456_000_000_000_000 and n==int(n) and 'e' not in str(v).lower():clocks[k]=str(int(n))
   day=str(r.get('day',r.get('date',''))).replace('-','')
   if day not in hs:day='20231018' if s['path'].startswith('artifacts/sqlite-triage/') else 'crossday'
   if clocks:
    k=next((k for k in ['known_by_ns','available_ns','receive_ns','start_recv_ns','event_ns','cutoff_ns'] if k in clocks),next(iter(clocks)))
    ident=next((str(r[k]) for k in ['trade_id','instance_id','family_id','candidate_id','source_ordinal'] if k in r),str(i))
    ws[day].writerow([s['id'],i,day if day!='crossday' else '',ident,k,clocks[k],'Source field; see producer clock definition','','','',json.dumps(clocks,separators=(',',':')),'Included; trade/cursor binding pending where absent'])
    s['pinned_rows']+=1;counts[day]+=1
   else:s['attachment_rows']+=1
   s['record_rows']+=1
   if out is not None:out.write(json.dumps({'source_row_0based':i,'data':r,'pin_clocks_ns':clocks,'clock_derivations':{},'clock_issues':[]},separators=(',',':'))+'\n')
 s['handling']='Every row retained; source clocks indexed; non-event rows attached'
 if int(s['id'][1:])%50==0:print('expanded source processed',s['id'],flush=True)
for f in hs.values():f.close()
(O/'expanded_source_catalog.json').write_text(json.dumps(S,indent=2))
print('expanded row counts',dict(counts),'rows',sum(s['record_rows'] for s in S),'attachments',sum(s['attachment_rows'] for s in S),flush=True)
