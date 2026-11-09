from acquire import ROOT,api
import json,hashlib,urllib.request,datetime
O=ROOT/'current';repo=ROOT/'git-publication';rel='tasks/family-research-20261022/research-union-current/'
pub=json.loads((O/'latest_publication.json').read_text());commit=pub['commit']
manifest=json.loads((repo/rel/'CHECKPOINT_MANIFEST.json').read_text())
tree=api(f'repos/DavisAI1974/markets-data/git/trees/{commit}?recursive=1');assert not tree.get('truncated')
by={r['path']:r for r in tree['tree'] if r['type']=='blob'};checked=[];normalized=[]
for r in manifest:
 p=repo/rel/r['path'];data=p.read_bytes();h=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
 remote=by[rel+r['path']]
 if h!=remote['sha']:
  assert r['path'].endswith(('.csv','.md','.json')),r['path']
  data=data.replace(b'\r\n',b'\n');h=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest();normalized.append(r['path'])
 assert h==remote['sha'] and len(data)==remote['size'],r['path'];checked.append(r['path'])
selected=next(r for r in manifest if r['path']=='research-pins/20231002-research-pins-01.xlsx')
url=f'https://raw.githubusercontent.com/DavisAI1974/markets-data/{commit}/{rel}{selected["path"]}'
h=hashlib.sha256();size=0
with urllib.request.urlopen(url,timeout=180) as response:
 while b:=response.read(4*1024*1024):h.update(b);size+=len(b)
assert h.hexdigest()==selected['sha256'] and size==selected['bytes']
receipt={'verified_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commit':commit,'remote_git_blob_matches':len(checked),'text_files_normalized_to_LF_by_git':normalized,'remote_binary_readback':{'path':selected['path'],'bytes':size,'sha256':h.hexdigest()},'files':checked}
(O/'publication_verification.json').write_text(json.dumps(receipt,indent=2));print('REMOTE VERIFIED',commit,len(checked),'files; binary readback',size,flush=True)
