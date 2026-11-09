from acquire import *
import shutil,sys
source_file=sys.argv[1] if len(sys.argv)>1 else 'workflow_sources.json'
S=json.loads((ROOT/source_file).read_text());local=pathlib.Path('E:/markets-data-frankie-audit-20261109')
def one(s):
 dest=ROOT/'objects'/s['sha']
 if not dest.exists():
  f=local/s['path']
  if f.exists():
   b=f.read_bytes()
   if hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==s['sha']:shutil.copyfile(f,dest)
 download(s['repo'],s['ref'],s['path'],dest)
 b=dest.read_bytes();assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==s['sha']
 s['read_status']='Downloaded; Git blob verified'
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
 for i,_ in enumerate(pool.map(one,S),1):
  if i%50==0:print('Workflow sources',i,flush=True)
(ROOT/source_file).write_text(json.dumps(S,indent=2))
print('Verified all',len(S),'workflow source files')
