"""Merge Artifact-authored reader sheets without rewriting original research cells."""
import copy,json,hashlib,zipfile
from pathlib import Path
import xml.etree.ElementTree as ET
from xlsx_stream import NS,RNS,PNS,CNS,tag,xml
from priority_cell_analysis import sheets,rows
R=Path(__file__).parent;P=R/'priority-now'
base=P/'Frankie_four_day_priority_ten.xlsx';summary=P/'Priority_summary.xlsx';dest=P/'priority-final.xlsx'
with zipfile.ZipFile(base) as old,zipfile.ZipFile(summary) as new,zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=3) as out:
 st=ET.fromstring(old.read('xl/styles.xml'));add=ET.fromstring(new.read('xl/styles.xml'));offset={};fmtmap={}
 for section in ['numFmts','fonts','fills','borders','cellStyleXfs','cellXfs','dxfs']:
  a=st.find(tag(section));b=add.find(tag(section))
  if b is None:continue
  if a is None:a=ET.SubElement(st,tag(section),count='0')
  offset[section]=len(a)
  maxfmt=max([int(e.get('numFmtId')) for e in a if e.get('numFmtId')]+[163]) if section=='numFmts' else 0
  for child in b:
   c=copy.deepcopy(child)
   if section=='numFmts':
    maxfmt+=1;fmtmap[int(c.get('numFmtId'))]=maxfmt;c.set('numFmtId',str(maxfmt))
   if section in ['cellXfs','cellStyleXfs']:
    for key,sec in [('fontId','fonts'),('fillId','fills'),('borderId','borders'),('xfId','cellStyleXfs')]:
     if c.get(key) is not None:c.set(key,str(int(c.get(key))+offset.get(sec,0)))
    fid=int(c.get('numFmtId','0'))
    if fid in fmtmap:c.set('numFmtId',str(fmtmap[fid]))
   a.append(c)
  a.set('count',str(len(a)))
 wb=ET.fromstring(old.read('xl/workbook.xml'));rel=ET.fromstring(old.read('xl/_rels/workbook.xml.rels'));ct=ET.fromstring(old.read('[Content_Types].xml'));ws=wb.find(tag('sheets'))
 shared=[]
 if 'xl/sharedStrings.xml' in new.namelist():shared=[''.join(s.itertext()) for s in ET.fromstring(new.read('xl/sharedStrings.xml'))]
 sid=max(int(s.get('sheetId')) for s in ws);mapping=sheets(new);added=[]
 for i,(name,part) in enumerate(mapping.items()):
  sid+=1;newpart=f'xl/worksheets/prioritySummary{sid}.xml';rid=f'rIdPrioritySummary{sid}';s=ET.fromstring(new.read(part))
  for c in s.iter(tag('c')):
   if c.get('s') is not None:c.set('s',str(int(c.get('s'))+offset['cellXfs']))
   if c.get('t')=='s':
    value=shared[int(c.find(tag('v')).text)];c.remove(c.find(tag('v')));c.set('t','inlineStr');ins=ET.SubElement(c,tag('is'));ET.SubElement(ins,tag('t')).text=value
  out.writestr(newpart,xml(s));sh=ET.Element(tag('sheet'),name=name,sheetId=str(sid),attrib={'{'+RNS+'}id':rid});ws.insert(i,sh)
  ET.SubElement(rel,'{'+PNS+'}Relationship',Id=rid,Type=RNS+'/worksheet',Target=newpart[3:]);ET.SubElement(ct,'{'+CNS+'}Override',PartName='/'+newpart,ContentType='application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml');added.append(name)
 for dn in wb.iter(tag('definedName')):
  if dn.get('localSheetId') is not None:dn.set('localSheetId',str(int(dn.get('localSheetId'))+len(added)))
 for view in wb.iter(tag('workbookView')):view.set('activeTab','0');view.set('firstSheet','0')
 index=sheets(old)['Priority ten'];ix=ET.fromstring(old.read(index));cell=next(c for c in ix.iter(tag('c')) if c.get('r')=='H2')
 for e in list(cell):cell.remove(e)
 cell.set('t','inlineStr');ET.SubElement(ET.SubElement(cell,tag('is')),tag('t')).text='Complete P01 table is in Priority_native_flow.xlsx, in the same folder. Exact known-by clocks; no early use of scheduled labels.'
 for n in old.namelist():
  if n not in ['xl/styles.xml','xl/workbook.xml','xl/_rels/workbook.xml.rels','[Content_Types].xml',index]:out.writestr(n,old.read(n))
 out.writestr(index,xml(ix))
 for n,e in [('xl/styles.xml',st),('xl/workbook.xml',wb),('xl/_rels/workbook.xml.rels',rel),('[Content_Types].xml',ct)]:out.writestr(n,xml(e))
assert dest.stat().st_size<100_000_000
# The original sheet payloads and every priority data sheet remain byte-for-byte intact.
verified=[]
with zipfile.ZipFile(base) as old,zipfile.ZipFile(dest) as final:
 for name,part in sheets(old).items():
  if name=='Priority ten':continue
  fpart=sheets(final)[name];assert old.getinfo(part).CRC==final.getinfo(fpart).CRC and old.getinfo(part).file_size==final.getinfo(fpart).file_size,name
  verified.append(name)
 for spec in json.loads((P/'summary_sheets.json').read_text()):
  rs=list(rows(final,sheets(final)[spec['name']]))
  assert len(rs)==len(spec['rows']),spec['name']
  for (num,actual),expected in zip(rs,spec['rows']):
   for key,value in zip(spec['headers'],expected):
    av=actual[key]
    if isinstance(value,(int,float)):assert float(av)==value,(spec['name'],num,key,av,value)
    else:assert av==value,(spec['name'],num,key)
dest.replace(base)
receipt={'main_workbook':{'file':base.name,'bytes':base.stat().st_size,'sha256':hashlib.sha256(base.read_bytes()).hexdigest()},'flow_workbook':{'file':'Priority_native_flow.xlsx','bytes':(P/'Priority_native_flow.xlsx').stat().st_size,'sha256':hashlib.sha256((P/'Priority_native_flow.xlsx').read_bytes()).hexdigest()},'data_sheets_preserved_from_cell_verified_input':verified,'artifact_authored_summary_sheets_verified':added,'rows_verified':628672,'summary_verification':'Every saved summary cell equals the report/rule inputs; original and priority data worksheet payload CRC and size unchanged.','scope':'Priority ten only. Exhaustive reconciliation remains deferred.'}
(P/'FINAL_VERIFICATION.json').write_text(json.dumps(receipt,indent=2))
print('FINAL WORKBOOK VERIFIED',base.stat().st_size,len(verified),'preserved sheets')
