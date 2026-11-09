from acquire import ROOT
from xlsx_stream import build
import json,pyarrow.parquet as pq,sys,itertools,hashlib
O=ROOT/'current';out=O/'trade-layers';out.mkdir(exist_ok=True)
sources=json.loads((ROOT/'active_sources.json').read_text())
sources=[s for s in sources if '/frankie-four-day-pins/run-42608467894-1/' in s['path'] and s['path'].endswith('.parquet')]
report=[]
for day in sys.argv[1:] or ['20231002','20231003','20231017','20231018']:
 selected=sorted([s for s in sources if '/'+day+'/' in s['path']],key=lambda s:s['path'])
 heads=pq.read_schema(ROOT/'objects'/selected[0]['sha']).names+['Source ID','Source row (zero based)','Immutable source']
 def rows():
  for s in selected:
   ordinal=0
   for batch in pq.ParquetFile(ROOT/'objects'/s['sha']).iter_batches(batch_size=1000):
    for r in batch.to_pylist():
     assert str(r['day'])==day
     yield [r[k] for k in heads[:-3]]+[s['id'],ordinal,s['url']];ordinal+=1
 oversized=out/f'{day}-all-trade-layer-values.xlsx'
 if oversized.exists():oversized.unlink() # task-owned failed oversize export only
 stream=iter(rows());part=0;dayreport=[]
 while True:
  first=next(stream,None)
  if first is None:break
  part+=1;dest=out/f'{day}-all-trade-layer-values-{part:02}.xlsx'
  selectedrows=itertools.chain([first],itertools.islice(stream,9999))
  payloads=[];links={}
  def safe_rows():
   for row in selectedrows:
    for j,v in enumerate(row):
     if isinstance(v,str) and len(v)>32767:
      key=hashlib.sha256(v.encode()).hexdigest()
      if key not in links:
       start=len(payloads)+2;chunks=[v[i:i+30000] for i in range(0,len(v),30000)]
       payloads.extend([[key,n+1,len(chunks),len(v),chunk] for n,chunk in enumerate(chunks)])
       links[key]=f'Complete value: Layer payload parts!A{start}:E{len(payloads)+1}; SHA256 {key}'
      row[j]=links[key]
    yield row
  r=build(O/'template.xlsx',dest,[{'name':'All trade layer values','headers':heads,'rows':safe_rows(),'widths':[24]*len(heads)},{'name':'Layer payload parts','headers':['Payload SHA256','Part','Total parts','Original characters','Full value text chunk'],'rows':iter(payloads),'widths':[68,12,14,22,100]}],preserve=False)
  dayreport.append({'day':day,'file':'trade-layers/'+dest.name,'rows':r[0]['rows'],'columns':len(heads),'bytes':dest.stat().st_size})
  assert dest.stat().st_size<100_000_000,'Split workbook for Git'
  (O/('trade_layer_workbooks-'+day+'.json')).write_text(json.dumps(dayreport,indent=2))
