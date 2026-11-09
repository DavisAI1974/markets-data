from acquire import *
import time
base='tasks/family-research-20261022/'
active=json.loads((ROOT/'active_sources.json').read_text())
keys={(s['repo'],s['path']) for s in active}
new=[]
rev=api('repos/DavisAI1974/markets-data/commits/main')['sha']
latest=api(f'repos/DavisAI1974/markets-data/git/trees/{rev}?recursive=1')
assert not latest.get('truncated')
(ROOT/'latest-data-tree.json').write_text(json.dumps(latest))
(ROOT/'latest-data-revision.txt').write_text(rev)
for repo,ref,rows in [('Markets',SOURCES['original_research'][1],tree('original_research')),('markets-data',rev,latest['tree'])]:
 for r in rows:
  p=r['path']
  if r['type']!='blob' or 'reanalysis' in p.lower():continue
  wanted=p.startswith('artifacts/sqlite-triage/20261022/families/') or (repo=='markets-data' and p.startswith(base+'claude-code-cases/'))
  if not wanted or (repo,p) in keys:continue
  s={**r,'repo':repo,'ref':ref,'branches':['original_sqlite_julia' if repo=='Markets' else 'latest_data'],'id':f'S{13000+len(new):05}','owner':'Original SQLite / Julia' if repo=='Markets' else 'CCode','url':f'https://github.com/DavisAI1974/{repo}/blob/{ref}/{p}','read_status':'Immutable attachment','fetch':True}
  new.append(s)
print('new sources',len(new),'MB',round(sum(s['size'] for s in new)/1e6),flush=True)
def one(s):
 dest=ROOT/'objects'/s['sha']
 try:
  download(s['repo'],s['ref'],s['path'],dest)
  b=dest.read_bytes();assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==s['sha']
  s['read_status']='Downloaded; Git blob verified'
 except Exception as e:s['read_status']='Download failed: '+str(e)
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
 for i,_ in enumerate(pool.map(one,new),1):
  if i%100==0:print('expanded',i,flush=True)
(ROOT/'expanded_sources.json').write_text(json.dumps(new,indent=2))
print('done',len(new),'failed',sum('failed' in s['read_status'] for s in new),flush=True)
