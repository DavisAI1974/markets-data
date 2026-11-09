"""Stream large data into Artifact Tool-authored worksheet formatting.

Artifact Tool owns the styled template. XML streaming avoids materialising millions
of rows in the JS workbook object. Original workbook parts remain byte-identical.
"""
import zipfile,xml.etree.ElementTree as ET,copy,re,json,math
from pathlib import Path
from xml.sax.saxutils import escape
NS='http://schemas.openxmlformats.org/spreadsheetml/2006/main'
RNS='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
PNS='http://schemas.openxmlformats.org/package/2006/relationships'
CNS='http://schemas.openxmlformats.org/package/2006/content-types'
ET.register_namespace('x',NS);ET.register_namespace('r',RNS)
def tag(s):return '{'+NS+'}'+s
def col(n):
 s=''
 while n:n,k=divmod(n-1,26);s=chr(65+k)+s
 return s
def xml(e):return ET.tostring(e,encoding='utf-8',xml_declaration=True)
def cell(v,addr,style):
 if v is None:return ''
 if isinstance(v,(dict,list)):v=json.dumps(v,separators=(',',':'),ensure_ascii=False)
 # Exact integer clocks cannot pass through Excel's 15-digit numeric precision.
 if isinstance(v,bool):return f'<x:c r="{addr}" s="{style}" t="b"><x:v>{int(v)}</x:v></x:c>'
 if isinstance(v,(int,float)) and not isinstance(v,bool) and math.isfinite(v) and abs(v)<10**15:
  return f'<x:c r="{addr}" s="{style}" t="n"><x:v>{v}</x:v></x:c>'
 v=str(v);assert len(v)<=32767,('Cell exceeds Excel limit',addr,len(v))
 v=re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]','',v)
 return f'<x:c r="{addr}" s="{style}" t="inlineStr"><x:is><x:t xml:space="preserve">{escape(v)}</x:t></x:is></x:c>'

def write_sheet(z,path,headers,rows,header_style=4,body_style=1,widths=None):
 widths=widths or [22]*len(headers)
 with z.open(path,'w',force_zip64=True) as f:
  f.write((f'<?xml version="1.0" encoding="utf-8"?><x:worksheet xmlns:x="{NS}"><x:sheetViews><x:sheetView showGridLines="0" workbookViewId="0"><x:pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/></x:sheetView></x:sheetViews><x:sheetFormatPr defaultRowHeight="22"/><x:cols>'+''.join(f'<x:col min="{i+1}" max="{i+1}" width="{w}" customWidth="1"/>' for i,w in enumerate(widths))+'</x:cols><x:sheetData>').encode())
  n=0
  for n,row in enumerate(iter_with_header(headers,rows),1):
   assert n<=1048576
   assert len(row)<=len(headers)
   f.write((f'<x:row r="{n}" ht="{44 if n==1 else 22}" customHeight="1">'+''.join(cell(v,f'{col(j+1)}{n}',header_style if n==1 else body_style) for j,v in enumerate(row))+'</x:row>').encode('utf8'))
  f.write((f'</x:sheetData><x:autoFilter ref="A1:{col(len(headers))}{n}"/></x:worksheet>').encode())
 return n-1
def iter_with_header(headers,rows):
 yield headers
 yield from rows

def build(template,dest,sheets,preserve=True):
 """Append data sheets to the template, or use only its styles for split data books."""
 with zipfile.ZipFile(template) as src,zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=3,allowZip64=True) as out:
  wb=ET.fromstring(src.read('xl/workbook.xml'));rels=ET.fromstring(src.read('xl/_rels/workbook.xml.rels'));ct=ET.fromstring(src.read('[Content_Types].xml'))
  ws=wb.find(tag('sheets'));skip=set()
  replacements={s['name'] for s in sheets if s.get('replace')}
  for sh in list(ws):
   if sh.get('name') not in replacements:continue
   rid=sh.get('{'+RNS+'}id')
   relem=next(r for r in rels if r.get('Id')==rid)
   target=relem.get('Target');part=target.lstrip('/') if target.startswith('/') else 'xl/'+target
   skip.add(part);ws.remove(sh);rels.remove(relem)
   for ce in list(ct):
    if ce.get('PartName')=='/'+part:ct.remove(ce)
  if not preserve:
   ws.clear()
   for e in list(rels):
    if e.get('Type','').endswith('/worksheet'):rels.remove(e)
   for e in list(ct):
    if '/worksheets/' in e.get('PartName',''):ct.remove(e)
   skip.update(n for n in src.namelist() if n.startswith('xl/worksheets/'))
  for n in src.namelist():
   if n not in skip and n not in ['xl/workbook.xml','xl/_rels/workbook.xml.rels','[Content_Types].xml','docProps/app.xml']:out.writestr(n,src.read(n))
  names={x.get('name') for x in ws};ids={e.get('Id') for e in rels};sid=max([int(e.get('sheetId')) for e in ws]+[0]);report=[]
  for spec in sheets:
   name=spec['name'];assert len(name)<=31 and name not in names;names.add(name);sid+=1
   rid='rIdUnion'+str(sid);assert rid not in ids
   part=f'xl/worksheets/union{sid}.xml'
   ET.SubElement(ws,tag('sheet'),name=name,sheetId=str(sid),attrib={'{'+RNS+'}id':rid})
   ET.SubElement(rels,'{'+PNS+'}Relationship',Id=rid,Type=RNS+'/worksheet',Target='worksheets/union'+str(sid)+'.xml')
   ET.SubElement(ct,'{'+CNS+'}Override',PartName='/'+part,ContentType='application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml')
   n=write_sheet(out,part,spec['headers'],spec['rows'],spec.get('header_style',4),spec.get('body_style',1),spec.get('widths'))
   report.append({'sheet':name,'rows':n,'columns':len(spec['headers'])});print(dest.name,name,n,flush=True)
  out.writestr('xl/workbook.xml',xml(wb));out.writestr('xl/_rels/workbook.xml.rels',xml(rels));out.writestr('[Content_Types].xml',xml(ct))
 return report
