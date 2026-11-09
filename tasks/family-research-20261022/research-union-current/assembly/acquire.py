import subprocess, json, pathlib, hashlib, concurrent.futures, sys, urllib.request

ROOT = pathlib.Path(__file__).parent
def api(endpoint, binary=False):
    cmd = ['gh', 'api', endpoint]
    if binary: cmd += ['-H', 'Accept: application/vnd.github.raw+json']
    r = subprocess.run(cmd, capture_output=True, timeout=180)
    if r.returncode: raise RuntimeError(r.stderr.decode(errors='replace'))
    return r.stdout if binary else json.loads(r.stdout)

SOURCES = {
 'desktop': ('Markets','3d0b06aa29781d5e39cc3eb45c6d09e174f195a2'),
 'desktop_handoff': ('Markets','beb2104c079045c24832f2279eac5e8e69bc576e'),
 'ccode': ('Markets','47b62f934e3bfa20328dd7456971693bb7a99fef'),
 'codex': ('Markets','4cf6e85de5de2a9fb479c90b7afb8dd50f1748cb'),
 'original_research': ('Markets','418462afeaf0f14aa8129f6f4d02c3867d772fd0'),
 'workbook': ('markets-data','586b31f65a12fb9215095a9af6851f8e95e7653b'),
}
def tree(name):
    repo, rev = SOURCES[name]
    dest = ROOT / (name+'-tree.json')
    if not dest.exists(): dest.write_text(json.dumps(api(f'repos/DavisAI1974/{repo}/git/trees/{rev}?recursive=1')), encoding='utf-8')
    obj=json.loads(dest.read_text())
    assert not obj.get('truncated'), name
    return obj['tree']

def download(repo, rev, path, dest):
    dest=pathlib.Path(dest);dest.parent.mkdir(parents=True, exist_ok=True)
    if not dest.exists():
        url=f'https://raw.githubusercontent.com/DavisAI1974/{repo}/{rev}/{path}'
        data=urllib.request.urlopen(url,timeout=120).read()
        dest.write_bytes(data)
    return dest

if __name__=='__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        for name, rows in zip(SOURCES,pool.map(tree,SOURCES)):
            paths=[r for r in rows if r['type']=='blob' and ('family-research' in r['path'] or r['path'].startswith('agent-pass/'))]
            groups={}
            for r in paths:
                key='/'.join(r['path'].split('/')[:4]);groups[key]=groups.get(key,0)+1
            print(name,len(paths),json.dumps(groups),flush=True)
    download('markets-data',SOURCES['workbook'][1],'tasks/family-research-20261022/frankie-four-day-pins/extended-review-20261109/Frankie_four_day_layer_review.xlsx',ROOT/'original.xlsx')
    print('workbook downloaded',flush=True)
