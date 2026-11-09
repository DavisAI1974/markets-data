from acquire import ROOT
import json,csv,gzip,re,collections
O=ROOT/'current'
sources=json.loads((ROOT/'active_sources.json').read_text())+json.loads((ROOT/'expanded_sources.json').read_text())
by_path={s['path']:s for s in sources}
maps=[]
examples={
 '1000144833.jpg':('es-lean-and-price-around-birth.png','x09_lean_cohort.csv','Chronological flow lean and midpoint; all four sessions'),
 '1000144837.jpg':('es-first-event-curves.png','x07_first_events.csv','Sorted timing distributions; use underlying candidate rows for chronological pins'),
 '1000144839.jpg':('es-share-moved-birth-axis.png','x06_','Birth-relative midpoint shares; aggregate attachment plus original candidate paths'),
 '1000144841.jpg':('es-aggressor-lots-birth-axis.png','x06_','Direction-specific aggressor lots'),
 '1000144843.jpg':('es-heatmap-oriented-mid-paths.png','x06_','Individual candidate midpoint paths'),
 '1000144845.jpg;1000144847.jpg':('ng-case-views.pdf','claude-code-cases/','Ten illustrated cases; retain all surrounding original studies'),
 '1000144751.jpg':('pinning-starter.pdf','whole-lifecycles/','Four-day lifecycle packet and full underlying collection'),
 '1000144753.jpg':('ng-dipole-renders.pdf','claude-code/','Informational aggregates; underlying event rows pinned separately'),
}
for screenshot,(render,table,note) in examples.items():
 hits=[s for s in sources if s['path'].endswith(render)]
 for h in hits:
  refs=[s['id'] for s in sources if table in s['path']]
  maps.append([screenshot,h['id'],h['path'],h['url'],';'.join(refs),note])
for h in json.loads((O/'historical_shape_sources.json').read_text()):
 maps.append([h['file'].split('/')[-1],'HISTORICAL',h['file'],'chat:'+h['origin_chat'],'G09','Direction-specific prebirth/event/tail concept; historical values not transferred to NG'])
with (O/'screenshot_source_map.csv').open('w',newline='',encoding='utf8') as f:
 w=csv.writer(f);w.writerow(['Screenshot','Source ID','Located file','Source URL or chat','Underlying collections','Meaning']);w.writerows(maps)

# Preserve each original field. Each case's nested event collections remain separate.
tables=collections.defaultdict(list)
for s in sources:
 if '/claude-code-cases/case-' not in s['path'] or not s['path'].endswith('.json.gz'):continue
 d=json.loads(gzip.decompress((ROOT/'objects'/s['sha']).read_bytes()))
 for key,c in d.items():
  case=c['case'];day='202310'+case['tag'][-2:];origin=c['day0'];cid=case['candidate_id']
  pre={'session_day':day,'candidate_id':cid,'source_id':s['id'],'case_key':key}
  for name,values in c.items():
   if name in ['case','clocks']:
    tables['Case identities' if name=='case' else 'Case clocks'].append({**pre,**values})
   elif isinstance(values,list) and values and isinstance(values[0],dict):
    for n,r in enumerate(values):
     row={**pre,'source_collection':name,'source_row_0based':n,**r}
     if 'epoch_s' in r:row['second_label_ns']=str(int(r['epoch_s'])*10**9)
     elif 'sec' in r:row['second_label_ns']=str((origin+int(r['sec']))*10**9)
     tables['Case '+name].append(row)
   elif name in ['per_second','touch_by_second']:
    for sec,r in values.items():tables['Case '+name].append({**pre,'source_second_key':sec,'second_label_ns':str((origin+int(sec))*10**9),**r})
spec=[]
for name,rs in tables.items():
 heads=list(dict.fromkeys(k for r in rs for k in r))
 filename='case-'+re.sub('[^a-z0-9]+','-',name.lower())+'.csv'
 with (O/filename).open('w',newline='',encoding='utf8') as f:
  w=csv.DictWriter(f,fieldnames=heads);w.writeheader()
  for r in rs:w.writerow({k:json.dumps(v,separators=(',',':')) if isinstance(v,(list,dict)) else v for k,v in r.items()})
 spec.append({'name':name[:31],'file':filename,'rows':len(rs),'fields':len(heads)})
(O/'case_table_inventory.json').write_text(json.dumps(spec,indent=2))
print('screenshot links',len(maps),'case tables',spec,flush=True)
