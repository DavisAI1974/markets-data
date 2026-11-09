from acquire import ROOT
import subprocess,json,shutil,hashlib,datetime
O=ROOT/'current';repo=ROOT/'git-publication';rel='tasks/family-research-20261022/research-union-current';dst=repo/rel
subprocess.run(['git','-C',str(repo),'config','core.autocrlf','false'],check=True)
subprocess.run(['git','-C',str(repo),'config','pack.window','0'],check=True)
subprocess.run(['python',str(ROOT/'stamp_handoff.py')],check=True)
names=['NEW_CHAT_HANDOFF.md','NEW_CHAT_HANDOFF.json','FILE_CLOCKS_AND_STATUS.json','publication_verification.json','latest_publication.json','Frankie_four_day_research_current.xlsx','extra_pin_session_audit.json']
for name in names:shutil.copyfile(O/name,dst/name)
assembly=dst/'assembly';assembly.mkdir(exist_ok=True)
for p in ROOT.glob('*.py'):shutil.copyfile(p,assembly/p.name)
for name in ['active_sources.json','expanded_sources.json','workflow_sources.json','remaining_research_sources.json','remaining_tabular_sources.json','table_schemas.json','workflow_schemas.json']:
 shutil.copyfile(ROOT/name,assembly/name)
(assembly/'USAGE.md').write_text('Assembly scripts from the live workspace. The live work root is recorded in NEW_CHAT_HANDOFF.md. Inspect running workers before restarting. These scripts expect acquire.py beside them and current/, objects/, original/template inputs under that work root. Immutable source manifests reconstruct source objects; local caches are not bundled. No completed run is implied by script presence.\n')
# Canonical text bytes make manifest hashes agree with Git on Windows.
for p in dst.rglob('*'):
 if p.is_file() and p.suffix in ['.csv','.md','.json','.py']:
  b=p.read_bytes();normalized=b.replace(b'\r\n',b'\n')
  if b!=normalized:p.write_bytes(normalized)
manifest=[]
for p in sorted(dst.rglob('*')):
 if p.is_file() and p.name!='CHECKPOINT_MANIFEST.json':
  b=p.read_bytes();manifest.append({'path':str(p.relative_to(dst)).replace('\\','/'),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
(dst/'CHECKPOINT_MANIFEST.json').write_text(json.dumps(manifest,indent=2))
subprocess.run(['git','-C',str(repo),'add','--',rel],check=True)
changes=subprocess.check_output(['git','-C',str(repo),'diff','--cached','--name-status'],text=True)
assert all(l.startswith(('A\t','M\t')) and rel+'/' in l for l in changes.splitlines()),changes
subprocess.run(['git','-C',str(repo),'commit','-m','docs: save clock-stamped research continuation and verified artifact status'],check=True)
subprocess.run(['git','-C',str(repo),'push','origin','codex/research-union-four-days-20261109'],check=True)
commit=subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip()
(O/'handoff_publication.json').write_text(json.dumps({'commit':commit,'published_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'handoff_url':f'https://github.com/DavisAI1974/markets-data/blob/{commit}/{rel}/NEW_CHAT_HANDOFF.md'},indent=2))
print('HANDOFF PUBLISHED',commit,flush=True)
