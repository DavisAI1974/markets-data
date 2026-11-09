"""Append Artifact-authored discovery sheets and correct three derived reader views."""
import copy,csv,json,hashlib,zipfile
from pathlib import Path
import xml.etree.ElementTree as ET
from xlsx_stream import NS,RNS,PNS,CNS,tag,xml
from priority_cell_analysis import sheets,rows
R=Path(__file__).parent;P=R/'priority-now';O=R/'discovery-depth'
base=P/'Frankie_four_day_priority_ten.xlsx';summary=O/'Priority_summary.xlsx';dest=O/'Frankie_four_day_discovery.xlsx'
correction={}
with (O/'event_interval_order_counts.csv').open(newline='') as f:
 for r in csv.DictReader(f):correction[(r['day'],r['interval_order'])]=int(r['n'])
def value(c):
 if c is None:return None
 return ''.join(c.find(tag('is')).itertext()) if c.get('t')=='inlineStr' else c.findtext(tag('v'))
def set_value(c,v):
 for e in list(c):c.remove(e)
 if isinstance(v,int):c.set('t','n');ET.SubElement(c,tag('v')).text=str(v)
 else:c.set('t','inlineStr');ET.SubElement(ET.SubElement(c,tag('is')),tag('t')).text=v
with zipfile.ZipFile(base) as old,zipfile.ZipFile(summary) as new,zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=3) as out:
 st=ET.fromstring(old.read('xl/styles.xml'));add=ET.fromstring(new.read('xl/styles.xml'));offset={};fmtmap={}
 for section in ['numFmts','fonts','fills','borders','cellStyleXfs','cellXfs','dxfs']:
  a=st.find(tag(section));b=add.find(tag(section))
  if b is None:continue
  if a is None:a=ET.SubElement(st,tag(section),count='0')
  offset[section]=len(a);maxfmt=max([int(e.get('numFmtId')) for e in a if e.get('numFmtId')]+[163]) if section=='numFmts' else 0
  for child in b:
   c=copy.deepcopy(child)
   if section=='numFmts':maxfmt+=1;fmtmap[int(c.get('numFmtId'))]=maxfmt;c.set('numFmtId',str(maxfmt))
   if section in ['cellXfs','cellStyleXfs']:
    for key,sec in [('fontId','fonts'),('fillId','fills'),('borderId','borders'),('xfId','cellStyleXfs')]:
     if c.get(key) is not None:c.set(key,str(int(c.get(key))+offset.get(sec,0)))
    fid=int(c.get('numFmtId','0'))
    if fid in fmtmap:c.set('numFmtId',str(fmtmap[fid]))
   a.append(c)
  a.set('count',str(len(a)))
 wb=ET.fromstring(old.read('xl/workbook.xml'));rel=ET.fromstring(old.read('xl/_rels/workbook.xml.rels'));ct=ET.fromstring(old.read('[Content_Types].xml'));ws=wb.find(tag('sheets'))
 shared=[''.join(s.itertext()) for s in ET.fromstring(new.read('xl/sharedStrings.xml'))] if 'xl/sharedStrings.xml' in new.namelist() else []
 sid=max(int(s.get('sheetId')) for s in ws);mapping=sheets(new);added=[]
 for i,(name,part) in enumerate(mapping.items()):
  assert name not in sheets(old);sid+=1;newpart=f'xl/worksheets/discovery{sid}.xml';rid=f'rIdDiscovery{sid}';s=ET.fromstring(new.read(part))
  for c in s.iter(tag('c')):
   if c.get('s') is not None:c.set('s',str(int(c.get('s'))+offset['cellXfs']))
   if c.get('t')=='s':set_value(c,shared[int(c.find(tag('v')).text)])
  out.writestr(newpart,xml(s));ws.insert(i,ET.Element(tag('sheet'),name=name,sheetId=str(sid),attrib={'{'+RNS+'}id':rid}))
  ET.SubElement(rel,'{'+PNS+'}Relationship',Id=rid,Type=RNS+'/worksheet',Target=newpart[3:]);ET.SubElement(ct,'{'+CNS+'}Override',PartName='/'+newpart,ContentType='application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml');added.append(name)
 for dn in wb.iter(tag('definedName')):
  if dn.get('localSheetId') is not None:dn.set('localSheetId',str(int(dn.get('localSheetId'))+len(added)))
 for view in wb.iter(tag('workbookView')):view.set('activeTab','0');view.set('firstSheet','0')
 replacements={};oldmap=sheets(old)
 for name in ['Priority findings','Priority counts','Paper rules v1']:
  part=oldmap[name];tree=ET.fromstring(old.read(part));cells={c.get('r'):c for c in tree.iter(tag('c'))}
  if name=='Priority findings':
   set_value(cells['C9'],'Corrected interval comparison: 1,139 aggression intervals first; 682 quote intervals first; 1,335 overlapping and unresolved; 1 censored. See Discovery findings D02.')
   set_value(cells['D9'],'Raw indices use different interval/boundary definitions. Overlap cannot establish event order; original source cells are unchanged.')
  elif name=='Priority counts':
   rename={'first_event_aggression_first':'aggression_interval_before_quote_interval','first_event_price_first':'quote_interval_before_aggression_interval','first_event_same_bin':'overlapping_intervals_order_unresolved'}
   for row in tree.iter(tag('row')):
    n=row.get('r');key=value(cells.get('B'+n))
    if key in rename:
     category=rename[key];day=value(cells['A'+n]);set_value(cells['B'+n],'first_event_'+category);set_value(cells['C'+n],correction.get((day,category),0))
  else:set_value(cells['B1'],'Frozen v1 specification — current readiness is in Paper discovery update')
  replacements[part]=tree
 for n in old.namelist():
  if n not in ['xl/styles.xml','xl/workbook.xml','xl/_rels/workbook.xml.rels','[Content_Types].xml'] and n not in replacements:out.writestr(n,old.read(n))
 for n,e in replacements.items():out.writestr(n,xml(e))
 for n,e in [('xl/styles.xml',st),('xl/workbook.xml',wb),('xl/_rels/workbook.xml.rels',rel),('[Content_Types].xml',ct)]:out.writestr(n,xml(e))
assert dest.stat().st_size<100_000_000
preserved=[];cells_checked=0
with zipfile.ZipFile(base) as old,zipfile.ZipFile(dest) as final:
 fm=sheets(final)
 for name,part in sheets(old).items():
  if name in ['Priority findings','Priority counts','Paper rules v1']:continue
  assert old.getinfo(part).CRC==final.getinfo(fm[name]).CRC and old.getinfo(part).file_size==final.getinfo(fm[name]).file_size,name;preserved.append(name)
 for spec in json.loads((O/'summary_sheets.json').read_text(encoding='utf8')):
  rs=list(rows(final,fm[spec['name']]));assert len(rs)==len(spec['rows'])
  for (n,actual),expected in zip(rs,spec['rows']):
   for key,v in zip(spec['headers'],expected):
    av=actual.get(key)
    if isinstance(v,(int,float)):assert float(av)==v,(spec['name'],n,key,av,v)
    else:assert av==v or (av is None and v==''),(spec['name'],n,key,av,v)
    cells_checked+=1
 corrections=list(rows(final,fm['Priority findings']))[7][1];assert '1,335' in corrections['Cell-derived finding']
receipt={'file':dest.name,'bytes':dest.stat().st_size,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'input_priority_sha256':hashlib.sha256(base.read_bytes()).hexdigest(),'preserved_sheet_payloads':preserved,'explicitly_corrected_reader_views':['Priority findings P08 ordering','Priority counts P08 interval counts','Paper rules v1 header points to newer readiness'],'artifact_summary_cells_verified':cells_checked,'appended_sheets':added,'original_source_data_changed':False}
(O/'WORKBOOK_VERIFICATION.json').write_text(json.dumps(receipt,indent=2))
print('DISCOVERY WORKBOOK VERIFIED',dest.stat().st_size,cells_checked,'new summary cells',len(preserved),'preserved sheets')
