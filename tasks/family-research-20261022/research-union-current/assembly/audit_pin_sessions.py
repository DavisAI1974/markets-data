from acquire import ROOT
import csv,json,collections,datetime,sys
O=ROOT/'current';prefix=sys.argv[1] if len(sys.argv)>1 else 'extra'
result=[]
for p in sorted(O.glob(prefix+'-pins-*.csv')):
 day=p.stem.split('-')[-1];counts=collections.Counter();outside=collections.Counter();n=0;lo=None;hi=None
 if day!='crossday':
  d=datetime.datetime.strptime(day,'%Y%m%d').replace(tzinfo=datetime.timezone.utc)
  # Broad calendar envelope to detect wrong-date assignment; exact session authority remains source-specific.
  start=int((d-datetime.timedelta(days=1)).timestamp())*10**9;end=int((d+datetime.timedelta(days=1)).timestamp())*10**9
 with p.open(newline='',encoding='utf8') as f:
  for r in csv.DictReader(f):
   ns=int(r['primary_clock_ns_exact']);n+=1;lo=ns if lo is None else min(lo,ns);hi=ns if hi is None else max(hi,ns)
   if day!='crossday' and not start<=ns<end:outside[(r['source_id'],r['primary_clock_field'])]+=1
 result.append({'file':p.name,'rows':n,'min_primary_ns':str(lo),'max_primary_ns':str(hi),'outside_broad_session_date':[[*k,v] for k,v in outside.items()]})
 print(p.name,n,'outside',sum(outside.values()),flush=True)
(O/f'{prefix}_pin_session_audit.json').write_text(json.dumps(result,indent=2))
