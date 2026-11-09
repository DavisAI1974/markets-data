"""Publish a scoped snapshot to GitHub and verify every byte and tree path."""
import base64,concurrent.futures,hashlib,json,pathlib,subprocess
ROOT=pathlib.Path(__file__).parent
REPO='repos/DavisAI1974/markets-data'
PREFIX='paper-rules/20261109/'
ORIGINAL_INDEX='4b382a78f52c88d6bbe17d2bb9b3f7daf30251b6'

def api(path,payload=None,method=None):
    args=['gh','api',REPO+'/'+path]
    data=None
    if payload is not None:
        data=json.dumps(payload).encode()
        args+=['--method',method or 'POST','--input','-']
    p=subprocess.run(args,input=data,capture_output=True,timeout=180)
    if p.returncode:raise RuntimeError(p.stderr.decode(errors='replace')[-1500:])
    return json.loads(p.stdout)

def blobsha(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()

def publish():
    base=api('git/ref/heads/main')['object']['sha']
    oldindex=api('contents/MARKET_DATA_INDEX.md?ref='+base)['sha']
    allowed={ORIGINAL_INDEX}
    previous=ROOT/'PUBLISHED.json'
    if previous.exists():allowed.add(json.loads(previous.read_text())['index_blob_sha'])
    if oldindex not in allowed:raise RuntimeError('Central index changed; reconcile before publication')
    files={PREFIX+f.relative_to(ROOT/'delivery').as_posix():f for f in sorted((ROOT/'delivery').rglob('*')) if f.is_file()}
    files['MARKET_DATA_INDEX.md']=ROOT/'MARKET_DATA_INDEX.md'
    snapshots={path:f.read_bytes() for path,f in files.items()}
    def upload(item):
        path,b=item
        blob=api('git/blobs',{'encoding':'base64','content':base64.b64encode(b).decode()})['sha']
        assert blob==blobsha(b)
        return {'path':path,'bytes':len(b),'git_blob_sha':blob,'sha256':hashlib.sha256(b).hexdigest()}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:records=list(pool.map(upload,snapshots.items()))
    def commit(parent,entries,message):
        tree=api('git/commits/'+parent)['tree']['sha']
        tree=api('git/trees',{'base_tree':tree,'tree':entries})['sha']
        sha=api('git/commits',{'tree':tree,'parents':[parent],'message':message})['sha']
        assert api('git/refs/heads/main',{'sha':sha,'force':False},'PATCH')['object']['sha']==sha
        return sha
    entries=[{'path':r['path'],'mode':'100644','type':'blob','sha':r['git_blob_sha']} for r in records]
    content=commit(base,entries,'research: preserve complete paper-rule expansion and causal review checkpoint [skip ci]')
    print('CONTENT_COMMIT',content,flush=True)
    def verify(r):
        b=base64.b64decode(api('git/blobs/'+r['git_blob_sha'])['content'])
        assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256']
        return dict(r,remote_readback_verified=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:verified=list(pool.map(verify,records))
    tree=api('git/trees/'+content+'?recursive=1')
    assert not tree.get('truncated')
    paths={v['path']:v['sha'] for v in tree['tree']}
    assert all(paths[v['path']]==v['git_blob_sha'] for v in verified)
    receipt={'verified_commit':content,'files':verified,'migration_status':'paused_by_user','research_worker_restarts':0,'platform_orders':0,'result':'All bytes and committed tree paths verified'}
    b=(json.dumps(receipt,indent=2)+'\n').encode()
    (ROOT/'PUBLICATION_VERIFICATION.json').write_bytes(b)
    sha=api('git/blobs',{'encoding':'base64','content':base64.b64encode(b).decode()})['sha']
    assert sha==blobsha(b)
    current=api('git/ref/heads/main')['object']['sha']
    final=commit(current,[{'path':PREFIX+'PUBLICATION_VERIFICATION.json','mode':'100644','type':'blob','sha':sha}],'research: record verified paper-rule publication [skip ci]')
    assert base64.b64decode(api('git/blobs/'+sha)['content'])==b
    result={'content_commit':content,'receipt_commit':final,'files_verified':len(verified),'index_blob_sha':blobsha(snapshots['MARKET_DATA_INDEX.md']),'url':'https://github.com/DavisAI1974/markets-data/blob/'+final+'/'+PREFIX+'README.md'}
    (ROOT/'PUBLISHED.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result),flush=True)

if __name__=='__main__':publish()
