from acquire import ROOT
import json,zipfile,re,hashlib,collections,xml.etree.ElementTree as ET
O=ROOT/'current';merged={}
old={r['file']:r for r in json.loads((O/'companion_verification.json').read_text())} if (O/'companion_verification.json').exists() else {}
prior_verification_mtime=(O/'companion_verification.json').stat().st_mtime_ns if old else 0
for p in sorted(O.glob('*_workbooks-*.json'),key=lambda p:p.stat().st_mtime):
 for r in json.loads(p.read_text()):merged[r['file']]=r
results=[];ns='{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
for name,r in sorted(merged.items()):
 p=O/name;assert p.exists();assert p.stat().st_size<100_000_000
 previous=old.get(name)
 unchanged=previous and (previous.get('verified_mtime_ns')==p.stat().st_mtime_ns or ('verified_mtime_ns' not in previous and p.stat().st_mtime_ns<=prior_verification_mtime))
 if unchanged and previous['bytes']==p.stat().st_size and previous['rows']==r['rows']:
  results.append({**previous,'verified_mtime_ns':p.stat().st_mtime_ns});continue
 with zipfile.ZipFile(p) as z:
  parts=[n for n in z.namelist() if n.startswith('xl/worksheets/') and n.endswith('.xml')]
  # The first sheet contains the actual observations. Count serialized rows independently.
  count=0;tail=b'';sample=b''
  with z.open(parts[0]) as f:
   while b:=f.read(1024*1024):
    if not sample:sample=b
    data=tail+b;count+=data.count(b'<x:row ');tail=data[-12:]
    # Boundary tail cannot itself contain the complete 7-byte row marker twice.
    count-=tail.count(b'<x:row ')
  count+=tail.count(b'<x:row ')
  assert count-1==r['rows'],(name,count,r['rows'])
  if name.startswith('research-pins/'):
   m=re.search(rb'<x:c r="F2"[^>]*>(.*?)</x:c>',sample);assert m and b'<x:t' in m[1]
   assert re.search(rb'\d{19}',m[1]),(name,m[1])
  payload_count=0
  if len(parts)>1:
   groups=collections.defaultdict(list)
   root=ET.fromstring(z.read(parts[1]))
   for row in root.find(ns+'sheetData')[1:]:
    vals=[''.join(c.itertext()) for c in row];groups[vals[0]].append(vals)
   for h,rows in groups.items():
    rows.sort(key=lambda x:int(x[1]));v=''.join(x[4] for x in rows)
    assert len(rows)==int(rows[0][2]) and len(v)==int(rows[0][3])
    assert hashlib.sha256(v.encode()).hexdigest()==h
   payload_count=len(groups)
 h=hashlib.sha256()
 with p.open('rb') as f:
  while b:=f.read(4*1024*1024):h.update(b)
 results.append({**r,'bytes':p.stat().st_size,'sha256':h.hexdigest(),'verified_sheet_rows':count-1,'verified_long_payloads':payload_count,'verified_mtime_ns':p.stat().st_mtime_ns})
 print('Verified',name,count-1,flush=True)
(O/'companion_verification.json').write_text(json.dumps(results,indent=2))
print('TOTAL',len(results),sum(r['rows'] for r in results),flush=True)
