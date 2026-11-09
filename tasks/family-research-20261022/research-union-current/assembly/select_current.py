from acquire import ROOT
import json,re,collections,csv,gzip,io
a=json.loads((ROOT/'source_inventory.json').read_text())
chosen={}
for r in a:
    p=r['path']
    if 'reanalysis' in p.lower() or '/no-prefix-' in p: continue
    # The latest branch owns each path; historical snapshots are not active alternatives.
    order=['original_research','desktop','codex','desktop_handoff','workbook','ccode']
    if r['owner']=='Desktop':order=['desktop','original_research','desktop_handoff','codex','workbook','ccode']
    rank=min(order.index(b) for b in r['branches'])
    k=(r['repo'],p)
    if k not in chosen or rank<chosen[k][0]:chosen[k]=(rank,r)
active=[v[1] for v in chosen.values()]
# A later run replaces an older run only for the same output path and study.
latest={}
for r in active:
    p=r['path'];m=re.search(r'/run-(\d+)-(\d+)/',p)
    k=(r['repo'],re.sub(r'/run-\d+-\d+/','/run-CURRENT/',p))
    rank=(int(m[1]),int(m[2])) if m else (0,0)
    if k not in latest or rank>latest[k][0]:latest[k]=(rank,r)
active=sorted([v[1] for v in latest.values()],key=lambda x:x['id'])
(ROOT/'active_sources.json').write_text(json.dumps(active,indent=2))
summary=collections.Counter();counts=[]
for r in active:
    p=r['path'];f=ROOT/'objects'/r['sha']
    if not f.exists() or '/all-row-clock-pins/' in p: continue
    n=None; fields=[]
    if p.endswith(('.csv','.csv.gz')):
        txt=gzip.open(f,'rt',encoding='utf-8-sig') if p.endswith('.gz') else f.open(encoding='utf-8-sig')
        with txt:
            q=csv.reader(txt);fields=next(q,[]);n=sum(1 for _ in q)
    elif p.endswith(('.jsonl','.jsonl.gz')):
        txt=gzip.open(f,'rt') if p.endswith('.gz') else f.open()
        with txt:
            first=next(txt,'');fields=list(json.loads(first)) if first else [];n=1+sum(1 for _ in txt) if first else 0
    if n is not None:
        summary[r['owner']]+=n;counts.append({'id':r['id'],'path':p,'rows':n,'fields':fields})
(ROOT/'table_schemas.json').write_text(json.dumps(counts,indent=2))
print('active files',len(active),'tables',len(counts),'rows',dict(summary))
print('largest',[(x['id'],x['path'].split('/')[-1],x['rows']) for x in sorted(counts,key=lambda x:-x['rows'])[:15]])
