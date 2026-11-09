from acquire import ROOT
from xlsx_stream import build
import json,csv,gzip,collections,datetime
from zoneinfo import ZoneInfo
O=ROOT/'current';styles=json.loads((O/'template_style_map.json').read_text());spec=[]
def sheet(name,heads,rows,widths=None):
 spec.append({'name':name,'headers':heads,'rows':rows,'widths':widths,'replace':True,**styles})
def cs(name,file):
 def rows():
  with (O/file).open(encoding='utf8',newline='') as f:
   r=csv.reader(f);next(r);yield from r
 with (O/file).open(encoding='utf8',newline='') as f:heads=next(csv.reader(f))
 sheet(name,heads,rows())
catalog={s['id']:s for s in json.loads((O/'source_catalog.json').read_text())}
for file in ['expanded_sources.json']:
 for s in json.loads((ROOT/file).read_text()):catalog.setdefault(s['id'],s)
for file in ['expanded_source_catalog.json','workflow_source_catalog.json']:
 if (O/file).exists():
  for s in json.loads((O/file).read_text()):catalog[s['id']]=s
sources=list(catalog.values());verified=json.loads((O/'companion_verification.json').read_text())
published_sources=[]
for s in sources:
 q=dict(s);q['complete_original_attachment']=s['url']
 if s['id'] in ['S00092','S00096','S00101','S00105']:q['active_corrected_attachment']='evidence/'+s['id']+'.jsonl.gz'
 q.pop('current_attachment',None);published_sources.append(q)
(O/'published_source_catalog.json').write_text(json.dumps(published_sources,indent=2))
gaps=json.loads((O/'dipole_gap_summary.json').read_text())
rows=[]
for g in gaps:
 d=g['day'];pins=sum(r['rows'] for r in verified if r['day']==d and r['file'].startswith('research-pins/'));layers=sum(r['rows'] for r in verified if r['day']==d and r['file'].startswith('trade-layers/'))
 rows.append([d,g['trades'],layers,pins,g.get('Covered by saved prebirth and complete observed lifecycle',0),g['trades']-g.get('Covered by saved prebirth and complete observed lifecycle',0),'Saved trade universe; additional recovered source ingestion continues'])
sheet('Research coverage',['Trading date','Saved trades','Full layer rows in Excel','Timestamp-indexed research rows in Excel','Saved lifecycle association','Missing lifecycle association or segment','Scope'],rows,[18,18,25,32,28,32,90])
sheet('Excel companion index',['File','Trading session','Actual rows verified','Bytes','SHA256'],[[r['file'],r['day'],r['rows'],r['bytes'],r['sha256']] for r in verified],[75,18,24,20,70])
now=datetime.datetime.now(datetime.timezone.utc)
sheet('File clocks',['File or status','UTC clock','America New York clock','Meaning'],[['Master refresh',now.isoformat(),now.astimezone(ZoneInfo('America/New_York')).isoformat(),'Workbook assembly time; not market observation time']]+[[r['file'],datetime.datetime.fromtimestamp((O/r['file']).stat().st_mtime,datetime.timezone.utc).isoformat(),datetime.datetime.fromtimestamp((O/r['file']).stat().st_mtime,ZoneInfo('America/New_York')).isoformat(),'Completed local export last-write clock; market clocks are inside the research rows'] for r in verified],[75,38,38,100])
for name,file in [('Research gap queue','research_gap_queue.csv'),('19-field reuse','nineteen_field_reuse.csv'),('Screenshot source trace','screenshot_source_map.csv'),('Full saved trade clocks','trade_spine.csv'),('Every trade dipole map','trade_dipole_map.csv'),('Saved lifecycle intervals','dipole_lifecycle_index.csv')]:cs(name,file)
heads=['Source ID','Research owner','Git path','Bytes','Git blob','Commit','Immutable original source','Source handling','Rows parsed','Clock-indexed rows','Non-event or unbound rows','Unresolved clock rows','Active corrected artifact']
rs=[[s['id'],s.get('owner',''),s['path'],s.get('size',0),s['sha'],s['ref'],s['url'],s.get('handling',s.get('read_status','')),s.get('record_rows',0),s.get('pinned_rows',0),s.get('attachment_rows',0),s.get('issues',0),('evidence/'+s['id']+'.jsonl.gz') if s['id'] in ['S00092','S00096','S00101','S00105'] else ''] for s in sources]
sheet('Research source inventory',heads,rs)
sheet('Render and array attachments',heads,[r for r in rs if r[2].lower().endswith(('.png','.svg','.pdf','.html','.npz'))])
sheet('Workflow calculations',['Calculation family','October 2','October 3','October 17','October 18','Status'],[['Original SQLite clock and family calculations','Exact run reconciliation open','Exact run reconciliation open','Exact run reconciliation open','Original extraction registry recovered','All retained output families included; exact two user-requested runs not yet conclusively identified'],['Julia model and full-depth calculations','Exact run reconciliation open','Exact run reconciliation open','Exact run reconciliation open','Original source recovered','Additional four-day outputs are being populated; no completed-run claim from names alone']])
corrections=json.loads((O/'horizon_clock_corrections.json').read_text())
sheet('Verified clock corrections',['Source ID','Corrected records','Fields per record','Correction basis'],[[r['source_id'],r['records'],r['fields_per_record'],r['basis']] for r in corrections],[16,22,22,120])
def corrected_rows():
 for s in corrections:
  with gzip.open(O/'evidence'/f"{s['source_id']}.jsonl.gz",'rt',encoding='utf8') as f:
   for l in f:
    r=json.loads(l);yield [s['source_id'],r['source_row_0based'],json.dumps(r['data'],separators=(',',':')),json.dumps(r['pin_clocks_ns'],separators=(',',':')),json.dumps(r['clock_derivations'],separators=(',',':'))]
sheet('Corrected horizon records',['Source ID','Source row','Complete corrected fields','Exact source and scheduled clocks','Correction derivations'],corrected_rows(),[16,18,100,100,100])
for s in json.loads((O/'case_table_inventory.json').read_text()):cs(s['name'],s['file'])
sheet('NG screenshot work',['Screenshot row','Research item','Current status','Required four-day output'],[[2,'Subsecond warning lead','Approximately 0.5 seconds is unverified; not an active numeric result','Recover prior math and measure native source-clock lead per event; no fixed-delay outcome substitute'],[4,'S90 exhaustion canary','Original study attached; four-day replication pending','Retain original cells and denominators; distinguish one-second contrast from warning lead'],[5,'S94 reversal/exhaustion','Original hypothesis attached; NG calculation pending','Native-resolution NG event and availability clocks, all cases and outcomes'],[6,'NG authority crosswalk','Original definition attached; four-day mapping pending','Prebirth, event, tail/exhaustion direction-specific paths; family runway kept separate'],[7,'Fixed-delay retrospective study','Excluded from requested look-ahead calculation','Historical source retained as research context only; do not use 1/5/30-second outcomes as measured warning lead']],[18,35,85,110])
if (O/'ccode_render_review.csv').exists():cs('CCode 50 view trace','ccode_render_review.csv')
dest=O/'Frankie_four_day_research_current.next.xlsx';report=build(O/'merged-template.xlsx',dest,spec)
dest.replace(O/'Frankie_four_day_research_current.xlsx')
(O/'workbook_population.json').write_text(json.dumps(report,indent=2))
print('MASTER UPDATED',len(sources),len(verified),flush=True)
