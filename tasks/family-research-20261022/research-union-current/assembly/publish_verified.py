from acquire import ROOT
import json,hashlib,shutil,subprocess,zipfile,xml.etree.ElementTree as ET
O=ROOT/'current';repo=ROOT/'git-publication';rel='tasks/family-research-20261022/research-union-current';dst=repo/rel
verified=json.loads((O/'companion_verification.json').read_text())
names=['Frankie_four_day_research_current.xlsx','README.md','research_gap_queue.csv','CCODE_GAP_FILLER_HANDOFF.md','nineteen_field_reuse.csv','corrected_price_response.json','price_clock_verification.json','dipole_gap_summary.json','dipole_map_source_verification.json','case_table_inventory.json','screenshot_source_map.csv','historical_shape_sources.json','dipole_dive_chat_evidence.json','workbook_population.json','companion_verification.json','published_source_catalog.json','horizon_clock_corrections.json','ccode_render_review.csv','latest_screenshot_source.json','dipole_trade_gaps.csv']
names += [r['file'] for r in verified]+['evidence/'+s+'.jsonl.gz' for s in ['S00092','S00096','S00101','S00105']]
names += [str(p.relative_to(O)).replace('\\','/') for p in (O/'historical-shape-attachments').iterdir()]
manifest=[]
for name in names:
 p=O/name;target=dst/name;target.parent.mkdir(parents=True,exist_ok=True)
 h=hashlib.sha256(p.read_bytes()).hexdigest()
 expected=next((r for r in verified if r['file']==name),None)
 if expected:assert h==expected['sha256'],name
 shutil.copyfile(p,target);manifest.append({'path':name,'bytes':p.stat().st_size,'sha256':h})
(dst/'CHECKPOINT_MANIFEST.json').write_text(json.dumps(manifest,indent=2))
subprocess.run(['git','-C',str(repo),'add','--',rel],check=True)
changes=subprocess.check_output(['git','-C',str(repo),'diff','--cached','--name-status'],text=True)
assert all(l.startswith(('A\t','M\t')) and rel+'/' in l for l in changes.splitlines()),changes
print('Staged verified files',len(changes.splitlines()),flush=True)
if changes:
 subprocess.run(['git','-C',str(repo),'commit','-m','data: publish complete saved trade layers and timestamped research Excel companions'],check=True)
subprocess.run(['git','-C',str(repo),'push','origin','codex/research-union-four-days-20261109'],check=True)
commit=subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip()
(O/'latest_publication.json').write_text(json.dumps({'commit':commit,'files':len(manifest),'research_rows':sum(r['rows'] for r in verified if r['file'].startswith('research-pins/')),'trade_layer_rows':sum(r['rows'] for r in verified if r['file'].startswith('trade-layers/'))},indent=2))
print('PUBLISHED',commit,flush=True)
