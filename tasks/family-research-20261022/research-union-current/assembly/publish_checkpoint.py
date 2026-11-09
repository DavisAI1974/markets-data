from acquire import ROOT
from pathlib import Path
import shutil,json,hashlib,subprocess
O=ROOT/'current';repo=ROOT/'git-publication';dst=repo/'tasks/family-research-20261022/research-union-current';dst.mkdir(parents=True,exist_ok=True)
names=['Frankie_four_day_research_current.xlsx','README.md','research_gap_queue.csv','CCODE_GAP_FILLER_HANDOFF.md','nineteen_field_reuse.csv','corrected_price_response.json','price_clock_verification.json','dipole_gap_summary.json','dipole_map_source_verification.json','case_table_inventory.json','screenshot_source_map.csv','historical_shape_sources.json','dipole_dive_chat_evidence.json','workbook_population.json']
names += [f.name for f in O.glob('case-*.csv')]
manifest=[]
for name in names:
 shutil.copyfile(O/name,dst/name);b=(dst/name).read_bytes();manifest.append({'path':name,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
shutil.copytree(O/'historical-shape-attachments',dst/'historical-shape-attachments',dirs_exist_ok=True)
(dst/'CHECKPOINT_MANIFEST.json').write_text(json.dumps(manifest,indent=2))
subprocess.run(['git','-C',str(repo),'add','--','tasks/family-research-20261022/research-union-current'],check=True)
stat=subprocess.check_output(['git','-C',str(repo),'diff','--cached','--name-status'],text=True);assert all(l.startswith(('A\t','M\t')) and 'research-union-current/' in l for l in stat.splitlines()),stat
subprocess.run(['git','-C',str(repo),'commit','-m','data: populate four-day Excel with recovered screenshot sources and exact clocks'],check=True)
subprocess.run(['git','-C',str(repo),'push','-u','origin','codex/research-union-four-days-20261109'],check=True)
print(subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip())
