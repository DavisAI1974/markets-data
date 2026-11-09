from acquire import ROOT
from xlsx_stream import build
import csv,json,gzip,itertools,collections,os,sys
O=ROOT/'current';target=O/'research-pins';target.mkdir(exist_ok=True)
catalog=json.loads((O/'source_catalog.json').read_text())
if (O/'expanded_source_catalog.json').exists():catalog+=json.loads((O/'expanded_source_catalog.json').read_text())
if (O/'workflow_source_catalog.json').exists():catalog+=json.loads((O/'workflow_source_catalog.json').read_text())
byid={s['id']:s for s in catalog}
LIMIT=int(next((s.split('=',1)[1] for s in sys.argv if s.startswith('--limit=')),250000))
summary=[]
mode='base' if '--base-only' in sys.argv else 'extra' if '--extra-only' in sys.argv else 'workflow' if '--workflow-only' in sys.argv else 'all'
payloads=[];payload_links={};last_row_bytes=0
class Evidence:
 def __init__(self):self.sid=None;self.f=None;self.ordinal=-1;self.record=None
 def get(self,sid,ordinal):
  if sid!=self.sid or ordinal<self.ordinal:
   if self.f:self.f.close()
   self.f=gzip.open(O/'evidence'/f'{sid}.jsonl.gz','rt',encoding='utf8');self.sid=sid;self.ordinal=-1
  while self.ordinal<ordinal:
   self.record=json.loads(next(self.f));self.ordinal=self.record['source_row_0based']
  assert self.ordinal==ordinal
  return self.record
def rawpins(day):
 for pre in (['pins-'] if mode=='base' else ['extra-pins-'] if mode=='extra' else ['workflow-pins-'] if mode=='workflow' else ['pins-','extra-pins-']):
  p=O/(pre+day+'.csv')
  if not p.exists():continue
  with p.open(encoding='utf8',newline='') as f:yield from csv.DictReader(f)
def rows(day,skip=0):
 global last_row_bytes
 e=Evidence()
 for r in itertools.islice(rawpins(day),skip,None):
  obj=e.get(r['source_id'],int(r['source_row_0based']));data=json.dumps(obj['data'],separators=(',',':'),ensure_ascii=False)
  last_row_bytes=len(data.encode('utf8'))+sum(len(str(v).encode('utf8')) for v in r.values())+2000
  chunks=[data[i:i+30000] for i in range(0,len(data),30000)]
  if len(chunks)>8:
   import hashlib
   key=hashlib.sha256(data.encode()).hexdigest()
   if key not in payload_links:
    start=len(payloads)+2
    payloads.extend([[key,n+1,len(chunks),len(data),c] for n,c in enumerate(chunks)])
    payload_links[key]=f'Complete JSON value: Full payload parts!A{start}:E{len(payloads)+1}; SHA256 {key}'
   chunks=[payload_links[key]]
  r['all_clock_fields_json']=json.dumps(obj['pin_clocks_ns'],separators=(',',':'))
  if not obj.get('clock_issues') and r['record_status'].startswith('Clock precision unresolved'):r['record_status']='Included; source-derived clock correction applied'
  yield list(r.values())+chunks+['']*(8-len(chunks))+[json.dumps(obj.get('clock_derivations',{}),separators=(',',':')),byid[r['source_id']]['url']]
 if e.f:e.f.close()
heads=['Source ID','Source row (zero based)','Trading session','Record identity','Primary clock field','Primary clock ns (exact text)','Clock meaning','Preceding completed group receive ns','Preceding group cursor','Exact-clock trade IDs','All source clocks (JSON)','Population status']+[f'Complete source fields JSON part {n}' for n in range(1,9)]+['Clock derivations','Immutable original source']
def bounded_rows(first,stream):
 # Bound source payload size as well as row count; wide original rows can be enormous.
 total=last_row_bytes;yield first
 for _ in range(LIMIT-1):
  if total>=50_000_000:return
  row=next(stream,None)
  if row is None:return
  total+=last_row_bytes;yield row
days=[s for s in sys.argv[1:] if not s.startswith('--')] or ['20231002','20231003','20231017','20231018','crossday']
for day in days:
 manifest=O/('research_pin_workbooks-'+ '-'.join(days)+('' if mode=='all' else '-'+mode)+'.json')
 if len(days)==1 and manifest.exists():summary=json.loads(manifest.read_text())
 previous=[s for s in summary if s['day']==day]
 if '--first-only' in sys.argv:previous=[]
 stream=iter(rows(day,sum(s['rows'] for s in previous)));part=len(previous)
 while True:
  payloads=[];payload_links={}
  first=next(stream,None)
  if first is None:break
  part+=1;name=f'{day}-research-pins-'+('original-' if mode=='extra' else 'workflow-' if mode=='workflow' else '')+f'{part:02}.xlsx';dest=target/name
  selected=bounded_rows(first,stream)
  report=build(O/'template.xlsx',dest,[{'name':'Research observations','headers':heads,'rows':selected,'widths':[14,18,18,40,28,30,35,32,24,50,70,45]+[80]*8+[80,90]},{'name':'Full payload parts','headers':['Payload SHA256','Part','Total parts','Original characters','Full value text chunk'],'rows':iter(payloads),'widths':[68,12,14,22,100]}],preserve=False)
  summary=[s for s in summary if s['file']!='research-pins/'+name]
  summary.append({'file':'research-pins/'+name,'day':day,'rows':report[0]['rows'],'bytes':dest.stat().st_size})
  assert dest.stat().st_size<100_000_000,'Workbook needs smaller partition before Git publication'
  manifest.write_text(json.dumps(summary,indent=2))
  if '--first-only' in sys.argv:break
print('PIN WORKBOOKS COMPLETE',sum(s['rows'] for s in summary),len(summary),flush=True)
