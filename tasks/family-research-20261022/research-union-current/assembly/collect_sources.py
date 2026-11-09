from acquire import *
import collections, time

base='tasks/family-research-20261022/'
sources={}
for name in SOURCES:
    for r in tree(name):
        if r['type']!='blob': continue
        p=r['path']
        if not p.startswith(base): continue
        # Metadata records the prohibited material but its contents are never fetched.
        key=(SOURCES[name][0],p,r['sha'])
        if key not in sources:
            sources[key]={**r,'repo':SOURCES[name][0], 'ref':SOURCES[name][1], 'branches':[]}
        sources[key]['branches'].append(name)

items=list(sources.values())
for n,r in enumerate(sorted(items,key=lambda r:(r['repo'],r['path'],r['sha'])),1):
    r['id']=f'S{n:05}'
    p=r['path']
    rel=p[len(base):]
    r['url']=f"https://github.com/DavisAI1974/{r['repo']}/blob/{r['ref']}/{p}"
    r['owner']='CCode' if rel.startswith('claude-code/') else 'Desktop' if rel.startswith(('claude-pass/','claude-pass-3day/','desktop-lean/')) else 'Codex / retained inputs'
    prohibited=('reanalysis' in p.lower())
    research=rel.startswith(('claude-code/','claude-pass/','claude-pass-3day/','research-atlas-v2/','flow-book-discovery-v1/')) or ('/' not in rel and pathlib.Path(rel).suffix in ['.csv','.gz','.json','.md','.py'])
    native=rel.startswith('native-dipole/') and '/agent-pass/' in rel and '/cache/' not in rel
    saved_pins=rel.startswith(('all-row-clock-pins/','claude-code-pins/','timestamp-pins/','desktop-lean/','lifecycle-data-links/')) and not rel.endswith('.png')
    r['read_status']='Not fetched: prohibited reanalysis' if prohibited else 'Attachment: retained source or supporting artifact'
    r['fetch']=not prohibited and (research or native or saved_pins)
    # Original CCode prose is attached by immutable URL, not read as requested.
    if r['owner']=='CCode' and p.endswith(('.md','.pdf')):
        r['fetch']=False;r['read_status']='Attached unopened: CCode prose'

(ROOT/'source_inventory.json').write_text(json.dumps(items,indent=2),encoding='utf-8')
print('inventory',len(items),'fetch',sum(r['fetch'] for r in items),'MB',round(sum(r.get('size',0) for r in items if r['fetch'])/1e6,1),flush=True)

def one(r):
    if not r['fetch']: return
    dest=ROOT/'objects'/r['sha']
    try:
        for attempt in range(3):
            try:
                download(r['repo'],r['ref'],r['path'],dest)
                data=dest.read_bytes()
                actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
                if actual!=r['sha']: raise ValueError('Git blob mismatch')
                break
            except Exception:
                if attempt==2: raise
                time.sleep(1)
        r['read_status']='Downloaded; Git blob verified'
    except Exception as e: r['read_status']='Download failed: '+str(e)

with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
    for n,_ in enumerate(pool.map(one,[r for r in items if r['fetch']]),1):
        if n%100==0: print('fetched',n,flush=True)
(ROOT/'source_inventory.json').write_text(json.dumps(items,indent=2),encoding='utf-8')
print(collections.Counter(r['read_status'] for r in items),flush=True)
