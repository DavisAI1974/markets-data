"""Preserve the large master; insert Artifact-authored result sheets and policy corrections."""
import copy,hashlib,json,sys,zipfile
from pathlib import Path
import xml.etree.ElementTree as ET
P=Path(__file__).parent;R=P.parent;sys.path.insert(0,str(R))
from xlsx_stream import NS,RNS,PNS,CNS,tag,xml
from priority_cell_analysis import sheets,rows
base=R/'current/Frankie_four_day_research_current.xlsx'
summary=P/'Priority_summary.xlsx';dest=P/'Frankie_four_day_reanalysis.xlsx'
def value(c):
    if c is None:return None
    return ''.join(c.find(tag('is')).itertext()) if c.get('t')=='inlineStr' else c.findtext(tag('v'))
def set_value(c,v):
    for e in list(c):c.remove(e)
    c.set('t','inlineStr');ET.SubElement(ET.SubElement(c,tag('is')),tag('t')).text=str(v)
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
    sid=max(int(s.get('sheetId')) for s in ws);added=[];oldmap=sheets(old)
    for i,(name,part) in enumerate(sheets(new).items()):
        assert name not in oldmap;sid+=1;newpart=f'xl/worksheets/reanalysis{sid}.xml';rid=f'rIdReanalysis{sid}';s=ET.fromstring(new.read(part))
        for c in s.iter(tag('c')):
            if c.get('s') is not None:c.set('s',str(int(c.get('s'))+offset['cellXfs']))
            if c.get('t')=='s':set_value(c,shared[int(c.find(tag('v')).text)])
        out.writestr(newpart,xml(s));ws.insert(i,ET.Element(tag('sheet'),name=name,sheetId=str(sid),attrib={'{'+RNS+'}id':rid}))
        ET.SubElement(rel,'{'+PNS+'}Relationship',Id=rid,Type=RNS+'/worksheet',Target=newpart[3:]);ET.SubElement(ct,'{'+CNS+'}Override',PartName='/'+newpart,ContentType='application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml');added.append(name)
    for dn in wb.iter(tag('definedName')):
        if dn.get('localSheetId') is not None:dn.set('localSheetId',str(int(dn.get('localSheetId'))+len(added)))
    for view in wb.iter(tag('workbookView')):view.set('activeTab','0');view.set('firstSheet','0')
    replacements={}
    for name in ['Discovery findings','Paper discovery update','Paper rules v1']:
        part=oldmap[name];tree=ET.fromstring(old.read(part));cells={c.get('r'):c for c in tree.iter(tag('c'))}
        if name=='Discovery findings':
            text=value(cells['D2'])
            text=text.replace('Recommend R2 observation-only pending a direct test of the complete price-confirmed rule; log initial display, residual and replenishment separately.','R2 is included in paper trading by user instruction. Log initial display, residual and replenishment separately; survival is not a price-return claim.')
            set_value(cells['D2'],text)
            set_value(cells['C5'],value(cells['C5']).replace('Fresh 5s flow','Midpoint-classified 5s flow'))
        elif name=='Paper discovery update':
            updates={2:'priority-paper-v1.3-reanalysis-20261109; see Paper hypotheses and TRADE_RULES.json.',3:'Included in platform paper trading; preserve native-flow and executable-entry definitions.',4:'Included in platform paper trading. At touch when armed; tracked order may remain at original price behind the improved best quote.',7:'Earlier v1/v1.1 labels are historical. Every defined strategy is included; no observation-only evidence veto.',8:'No platform connected and no orders submitted. Analysis is complete; platform paper execution is separate.',9:'Test the rules through automated trades in a platform paper account. Historical/playback data is acceptable; standalone historical strategy backtests are deferred.'}
            for n,text in updates.items():set_value(cells['B'+str(n)],text)
        else:set_value(cells['B1'],'Frozen v1 history; current paper inclusion is in Paper hypotheses')
        replacements[part]=tree
    special={'xl/styles.xml','xl/workbook.xml','xl/_rels/workbook.xml.rels','[Content_Types].xml'}
    for name in old.namelist():
        if name not in special and name not in replacements:out.writestr(name,old.read(name))
    for name,tree in replacements.items():out.writestr(name,xml(tree))
    for name,tree in [('xl/styles.xml',st),('xl/workbook.xml',wb),('xl/_rels/workbook.xml.rels',rel),('[Content_Types].xml',ct)]:out.writestr(name,xml(tree))
assert dest.stat().st_size<100_000_000
preserved=[];checked=0
with zipfile.ZipFile(base) as old,zipfile.ZipFile(dest) as final:
    fm=sheets(final)
    for name,part in sheets(old).items():
        if part in replacements:continue
        assert old.read(part)==final.read(fm[name]),name
        preserved.append(name)
    for spec in json.loads((P/'summary_sheets.json').read_text(encoding='utf-8')):
        data=list(rows(final,fm[spec['name']]))
        assert len(data)==len(spec['rows'])
        for (_,actual),expected in zip(data,spec['rows']):
            for key,v in zip(spec['headers'],expected):
                av=actual.get(key)
                if isinstance(v,(int,float)):
                    assert av is not None and abs(float(av)-v)<=max(1e-12,abs(v)*1e-12),(spec['name'],key,av,v)
                else:assert av==v or (av is None and v==''),(spec['name'],key,av,v)
                checked+=1
    assert 'Included in platform paper trading' in dict(rows(final,fm['Paper discovery update']))[4]['Current decision']
receipt={'file':dest.name,'bytes':dest.stat().st_size,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'input_sha256':hashlib.sha256(base.read_bytes()).hexdigest(),
         'preserved_sheet_payloads':preserved,'updated_reader_views':list(replacements),'appended_sheets':added,'summary_cells_verified':checked,'raw_source_data_changed':False}
(P/'WORKBOOK_VERIFICATION.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8',newline='\n')
print('Verified workbook',dest.stat().st_size,'bytes;',checked,'new cells;',len(preserved),'unchanged worksheet payloads',flush=True)
