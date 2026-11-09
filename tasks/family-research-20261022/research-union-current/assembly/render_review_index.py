from acquire import ROOT
import json,csv,re,hashlib,shutil
O=ROOT/'current';sources=json.loads((ROOT/'expanded_sources.json').read_text())
with (O/'case-case-identities.csv').open(newline='',encoding='utf8') as f:cases=list(csv.DictReader(f))
notes={1:'Continuation example; confirmation precedes archived recognition.',2:'Reversal example retained; recognition precedes confirmation.',3:'Adverse SOS example retained; sparse prints and late recognition.',4:'Long-runway example: confirmation is +675 s, outside displayed +600 s lifecycle window; full endpoint coverage still required.',5:'Positive initial response then opposite move retained; no outcome filter.',6:'Absorbed-pair first-burst example retained; later price path is not a pre-event input.',7:'Continuation example retained; recognition follows confirmation.',8:'Flat overnight example retained; sparse prints and long constant quotes must remain visible.',9:'Continuation after early adverse excursion retained.',10:'Failed initial move retained; later adverse path remains attached.'}
rows=[]
for s in sources:
 m=re.search(r'case-(\d+)-view([1-5])\.png$',s['path'])
 if not m:continue
 case,view=map(int,m.groups());composite=next(x for x in sources if x['path'].endswith(f'/case-{case:02}.png'))
 rows.append([case,view,s['id'],s['url'],s['sha'],composite['url'],'Visually reviewed in original five-view case composite','Case clocks / Case series / Case prints and other full underlying tables',notes[case],'Original illustrated selection rule retained as provenance; not an admission rule for complete research'])
assert len(rows)==50 and len({(r[0],r[1]) for r in rows})==50
with (O/'ccode_render_review.csv').open('w',newline='',encoding='utf8') as f:
 w=csv.writer(f);w.writerow(['Case','View','Source ID','Original view','Git blob','Reviewed five-view composite','Visual review status','Excel data trace','Observed limitation or description','Population handling']);w.writerows(sorted(rows))
src=ROOT.parent.parent/'.codex-remote-attachments/01a1c130-bdd5-7313-9947-e12f4efa8f09/31dce4a6-f5af-4e23-abc6-5b23b7e0b828/1-1000144857.jpg'
dst=O/'historical-shape-attachments'/'NG-request-1000144857.jpg';shutil.copyfile(src,dst)
(O/'latest_screenshot_source.json').write_text(json.dumps({'original_attachment':str(src),'published_copy':'historical-shape-attachments/'+dst.name,'sha256':hashlib.sha256(dst.read_bytes()).hexdigest(),'selected_rows':[2,4,5,6],'excluded_lookahead_option':7},indent=2))
print('50 original view links; all 10 five-view composites visually inspected')
