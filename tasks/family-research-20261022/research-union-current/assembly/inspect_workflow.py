from acquire import ROOT
import json,collections,gzip,csv,pyarrow.parquet as pq
ss=json.loads((ROOT/'workflow_sources.json').read_text());schemas=collections.Counter();count=0;details=[]
for s in ss:
 f=ROOT/'objects'/s['sha'];p=s['path'];n=None
 if p.endswith('.parquet'):
  t=pq.ParquetFile(f);keys=t.schema_arrow.names;n=t.metadata.num_rows;count+=n
 else:
  op=gzip.open(f,'rt',encoding='utf-8-sig') if p.endswith('.gz') else f.open(encoding='utf-8-sig')
  with op:
   if '.csv' in p:keys=next(csv.reader(op))
   else:
    r=json.loads(next(op));keys=list(r) if isinstance(r,dict) else []
 clocks=[k for k in keys if any(t in k.lower() for t in ['_ns','epoch','timestamp','clock','cursor','second'])]
 schemas[tuple(clocks)]+=1;details.append({'id':s['id'],'path':p,'rows':n,'fields':keys,'clock_candidates':clocks})
(ROOT/'workflow_schemas.json').write_text(json.dumps(details,indent=2))
print('Parquet rows',count,'schema count',len(schemas))
for k,v in schemas.items():print(v,k)
