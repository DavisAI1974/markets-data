from xlsx_stream import *
from acquire import ROOT
O=ROOT/'current'
with zipfile.ZipFile(ROOT/'original.xlsx') as old,zipfile.ZipFile(O/'template.xlsx') as new,zipfile.ZipFile(O/'merged-template.xlsx','w',zipfile.ZIP_DEFLATED) as out:
 st=ET.fromstring(old.read('xl/styles.xml'));add=ET.fromstring(new.read('xl/styles.xml'));offset={}
 # Each template style component keeps its original meaning after index rebasing.
 for section in ['numFmts','fonts','fills','borders','cellStyleXfs','cellXfs','dxfs']:
  a=st.find(tag(section));b=add.find(tag(section))
  if b is None:continue
  if a is None:a=ET.SubElement(st,tag(section),count='0')
  offset[section]=len(a)
  for child in b:
   c=copy.deepcopy(child)
   if section=='numFmts':c.set('numFmtId',str(int(c.get('numFmtId'))+1000))
   if section in ['cellXfs','cellStyleXfs']:
    for key,sec in [('fontId','fonts'),('fillId','fills'),('borderId','borders'),('xfId','cellStyleXfs')]:
     if c.get(key) is not None:c.set(key,str(int(c.get(key))+offset.get(sec,0)))
    if int(c.get('numFmtId','0'))>=164:c.set('numFmtId',str(int(c.get('numFmtId'))+1000))
   a.append(c)
  a.set('count',str(len(a)))
 wb=ET.fromstring(old.read('xl/workbook.xml'));rel=ET.fromstring(old.read('xl/_rels/workbook.xml.rels'));ct=ET.fromstring(old.read('[Content_Types].xml'));sheets=wb.find(tag('sheets'))
 nr={x.get('Id'):x.get('Target') for x in ET.fromstring(new.read('xl/_rels/workbook.xml.rels'))}
 for sh in ET.fromstring(new.read('xl/workbook.xml')).find(tag('sheets')):
  n=len(sheets)+1;part=f'xl/worksheets/union-template{n}.xml';rid=f'rIdTemplate{n}'
  target=nr[sh.get('{'+RNS+'}id')];target=target.lstrip('/') if target.startswith('/') else 'xl/'+target
  s=ET.fromstring(new.read(target))
  for c in s.iter(tag('c')):
   if c.get('s') is not None:c.set('s',str(int(c.get('s'))+offset['cellXfs']))
  out.writestr(part,xml(s));ET.SubElement(sheets,tag('sheet'),name=sh.get('name'),sheetId=str(n),attrib={'{'+RNS+'}id':rid})
  ET.SubElement(rel,'{'+PNS+'}Relationship',Id=rid,Type=RNS+'/worksheet',Target=part[3:])
  ET.SubElement(ct,'{'+CNS+'}Override',PartName='/'+part,ContentType='application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml')
 for n in old.namelist():
  if n not in ['xl/styles.xml','xl/workbook.xml','xl/_rels/workbook.xml.rels','[Content_Types].xml']:out.writestr(n,old.read(n))
 for n,e in [('xl/styles.xml',st),('xl/workbook.xml',wb),('xl/_rels/workbook.xml.rels',rel),('[Content_Types].xml',ct)]:out.writestr(n,xml(e))
(O/'template_style_map.json').write_text(json.dumps({'header_style':offset['cellXfs']+4,'body_style':offset['cellXfs']+1}))
print('preserved original sheets plus',len(sheets),'total template sheets')
