"""Resume byte verification after publication succeeded but a read timed out."""
import base64
import concurrent.futures
import hashlib
import json
from pathlib import Path
import sys
import time
from publish_package import api,blobsha,PREFIX

ROOT=Path(__file__).resolve().parent

def read_remote(path):
    for attempt in range(3):
        try:return api(path)
        except RuntimeError:
            if attempt==2:raise
            time.sleep(2)

def main(content):
    files={PREFIX+f.relative_to(ROOT/'delivery').as_posix():f for f in sorted((ROOT/'delivery').rglob('*')) if f.is_file()}
    files['MARKET_DATA_INDEX.md']=ROOT/'MARKET_DATA_INDEX.md'
    tree=read_remote('git/trees/'+content+'?recursive=1')
    assert not tree.get('truncated')
    paths={x['path']:x['sha'] for x in tree['tree']}
    records=[]
    for path,file in files.items():
        b=file.read_bytes();sha=blobsha(b)
        assert paths[path]==sha,path
        records.append(dict(path=path,bytes=len(b),git_blob_sha=sha,sha256=hashlib.sha256(b).hexdigest()))
    def verify(record):
        b=base64.b64decode(read_remote('git/blobs/'+record['git_blob_sha'])['content'])
        assert len(b)==record['bytes'] and hashlib.sha256(b).hexdigest()==record['sha256']
        return dict(record,remote_readback_verified=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:verified=list(pool.map(verify,records))
    helper=Path(__file__).read_bytes()
    helper_sha=api('git/blobs',{'encoding':'base64','content':base64.b64encode(helper).decode()})['sha']
    assert helper_sha==blobsha(helper)
    assert base64.b64decode(read_remote('git/blobs/'+helper_sha)['content'])==helper
    helper_record=dict(path=PREFIX+Path(__file__).name,bytes=len(helper),git_blob_sha=helper_sha,
                       sha256=hashlib.sha256(helper).hexdigest(),remote_readback_verified=True)
    receipt=dict(verified_commit=content,files=verified,verification_tool=helper_record,
                 migration_status='paused_by_user',research_worker_restarts=0,platform_orders=0,
                 result='Published snapshot bytes and tree paths verified; verification helper added in receipt commit')
    b=(json.dumps(receipt,indent=2)+'\n').encode()
    receipt_sha=api('git/blobs',{'encoding':'base64','content':base64.b64encode(b).decode()})['sha']
    assert receipt_sha==blobsha(b)
    current=read_remote('git/ref/heads/main')['object']['sha']
    # Fail rather than overwrite a concurrently changed checkpoint.
    if current!=content:raise RuntimeError('Main changed during resumed verification; reconcile before writing receipt')
    entries=[dict(path=helper_record['path'],mode='100644',type='blob',sha=helper_sha),
             dict(path=PREFIX+'PUBLICATION_VERIFICATION.json',mode='100644',type='blob',sha=receipt_sha)]
    newtree=api('git/trees',{'base_tree':tree['sha'],'tree':entries})['sha']
    final=api('git/commits',{'tree':newtree,'parents':[current],
              'message':'research: verify recovered runtime checkpoint after transient read timeout [skip ci]'})['sha']
    assert api('git/refs/heads/main',{'sha':final,'force':False},'PATCH')['object']['sha']==final
    assert base64.b64decode(read_remote('git/blobs/'+receipt_sha)['content'])==b
    committed=read_remote('git/trees/'+newtree+'?recursive=1')
    assert not committed.get('truncated')
    finalpaths={x['path']:x['sha'] for x in committed['tree']}
    assert all(finalpaths[x['path']]==x['git_blob_sha'] for x in verified+[helper_record])
    (ROOT/'PUBLICATION_VERIFICATION.json').write_bytes(b)
    result=dict(content_commit=content,receipt_commit=final,files_verified=len(verified)+1,
                index_blob_sha=paths['MARKET_DATA_INDEX.md'],
                url='https://github.com/DavisAI1974/markets-data/blob/'+final+'/'+PREFIX+'README.md')
    (ROOT/'PUBLISHED.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result),flush=True)

if __name__=='__main__':main(sys.argv[1])
