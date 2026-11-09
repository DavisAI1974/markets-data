"""Snapshot this task's public artifacts; never traverses the paused migration."""
import hashlib,json,pathlib,shutil
ROOT=pathlib.Path(__file__).parent
OUT=ROOT/'delivery';OUT.mkdir(exist_ok=True)
DIRECTORIES={'machine','paper_rules','tests','tasks','reconciliation','review_sources','review_chain_sources'}
EXCLUDE={'MARKET_DATA_INDEX.md','PUBLISHED.json','PUBLICATION_VERIFICATION.json','publish-payload.json','ref-payload.json'}
files=[]
for f in sorted(ROOT.rglob('*')):
    if not f.is_file():continue
    relative=f.relative_to(ROOT)
    if '__pycache__' in relative.parts or f.suffix=='.pyc':continue
    if len(relative.parts)>1 and relative.parts[0] not in DIRECTORIES:continue
    if len(relative.parts)==1 and f.name in EXCLUDE:continue
    if len(relative.parts)==1 and f.suffix not in {'.md','.json','.py'}:continue
    destination=OUT/relative;destination.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(f,destination)
    b=destination.read_bytes()
    files.append({'path':relative.as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
(OUT/'FILE_MANIFEST.json').write_text(json.dumps({'files':files,'scope':'this task public research and rule artifacts','migration':'paused'},indent=2)+'\n',encoding='utf-8')
print('Staged',len(files),'files',sum(f['bytes'] for f in files),'bytes')
