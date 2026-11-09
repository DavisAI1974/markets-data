"""Move the full flow table into a companion without changing any cell XML."""
import json,zipfile,shutil,hashlib
from pathlib import Path
from lxml import etree as E
R=Path(__file__).parent;P=R/'priority-now';N='{http://schemas.openxmlformats.org/spreadsheetml/2006/main}';RN='{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'
source=P/'Frankie_four_day_priority_ten.xlsx'
large=P/'priority-assembly-input.xlsx'
if not large.exists():source.replace(large)
result=[]
for companion,dest in [(True,P/'Priority_native_flow.xlsx'),(False,source)]:
 with zipfile.ZipFile(large) as src,zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=3) as out:
  wb=E.fromstring(src.read('xl/workbook.xml'));rels=E.fromstring(src.read('xl/_rels/workbook.xml.rels'));ct=E.fromstring(src.read('[Content_Types].xml'));ss=wb.find(N+'sheets');removed=set()
  for sh in list(ss):
   keep=sh.get('name').startswith('P01 ')
   if keep==companion:continue
   relation=next(r for r in rels if r.get('Id')==sh.get(RN+'id'))
   target=relation.get('Target');part=target.lstrip('/') if target.startswith('/') else 'xl/'+target
   removed.add(part);ss.remove(sh);rels.remove(relation)
  if companion:
   for e in list(wb):
    if E.QName(e).localname in ('definedNames','bookViews'):wb.remove(e)
  for e in list(ct):
   if e.get('PartName','').lstrip('/') in removed:ct.remove(e)
  for name in src.namelist():
   if name in removed or name in ['xl/workbook.xml','xl/_rels/workbook.xml.rels','[Content_Types].xml']:continue
   with src.open(name) as a,out.open(name,'w',force_zip64=True) as b:shutil.copyfileobj(a,b,1024*1024)
  for name,el in [('xl/workbook.xml',wb),('xl/_rels/workbook.xml.rels',rels),('[Content_Types].xml',ct)]:out.writestr(name,E.tostring(el,xml_declaration=True,encoding='utf-8'))
 assert dest.stat().st_size<100_000_000
 result.append({'file':dest.name,'bytes':dest.stat().st_size,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()})
(P/'priority_workbook_receipt.json').write_text(json.dumps({'files':result,'flow_companion':'Priority_native_flow.xlsx','assembly_input_sha256':hashlib.sha256(large.read_bytes()).hexdigest()},indent=2))
print(result)
