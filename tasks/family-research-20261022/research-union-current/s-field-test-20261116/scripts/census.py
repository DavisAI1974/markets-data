import re, json, sys, collections
LAY=json.load(open('/home/user/work/out/layout.json'))
def col2n(c):
    n=0
    for ch in c: n=n*26+ord(ch)-64
    return n-1
blocks=[]
for l in LAY['loc']:
    m=re.match(r'([A-Z]+)(\d+)',l['dataCell']); hr=int(m.group(2))
    blocks.append(dict(day=l['day'],cat=l['category'],base=l['base'],hr=hr,n=l['tickCount']))
byrow={}
for b in blocks:
    for r in range(b['hr'],b['hr']+b['n']+1): byrow.setdefault(r,[]).append(b)
W=LAY['tickWidth']
hdr={}   # (blockidx)->{off:name}
cnt=collections.defaultdict(lambda: collections.Counter())  # (day,cat)->field->nonempty
samples={}
rowre=re.compile(rb'<row r="(\d+)"[^>]*>(.*?)</row>',re.S)
cre=re.compile(rb'<c r="([A-Z]+)\d+"([^>]*?)(?:/>|>(.*?)</c>)',re.S)
tre=re.compile(rb'<t[^>]*>(.*?)</t>|<v>(.*?)</v>|<f>(.*?)</f>',re.S)
buf=b''
f=open('/home/user/work/r2/xl/worksheets/sheet1.xml','rb')
while True:
    ch=f.read(64<<20)
    if not ch: break
    buf+=ch
    last=0
    for m in rowre.finditer(buf):
        last=m.end(); r=int(m.group(1))
        if r not in byrow: continue
        for cm in cre.finditer(m.group(2)):
            cn=col2n(cm.group(1).decode()); body=cm.group(3)
            if not body: continue
            t=tre.search(body)
            if not t: continue
            val=(t.group(1) or t.group(2) or t.group(3) or b'')
            if not val.strip(): continue
            for b in byrow[r]:
                off=cn-b['base']
                if 0<=off<W:
                    k=(b['day'],b['cat'])
                    if r==b['hr']: hdr.setdefault(k,{})[off]=val.decode()
                    else:
                        cnt[k][off]+=1
                        samples.setdefault(off,val[:160].decode('utf8','replace'))
    buf=buf[last:]
names=hdr[next(iter(hdr))]
out=dict(blocks=blocks,names={str(k):v for k,v in names.items()},
         counts={f"{k[0]}|{k[1]}":dict(v) for k,v in cnt.items()},samples={str(k):v for k,v in samples.items()})
json.dump(out,open('/home/user/work/out/census.json','w'))
print(len(names),'header cols; blocks',len(cnt))
