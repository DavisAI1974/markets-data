"""Bounded-memory OOXML repair after the bundled editor's import OOM.

Preserves every unaffected cell, formula, style, drawing and second-series member.
Large recovered values are embedded as lossless JSON chunks inside the workbook.
"""
import gzip
import hashlib
import json
from pathlib import Path
import re
import sqlite3
from xml.sax.saxutils import escape
import xml.etree.ElementTree as ET
import zipfile

OUT=Path(__file__).resolve().parent
SOURCE=OUT/'Claude-Eight-Trade-Types-Original.xlsx'
TARGET=OUT/'Claude-Eight-Trade-Types-Rebuilt.xlsx'
NS='http://schemas.openxmlformats.org/spreadsheetml/2006/main'
REL='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
CELL=re.compile(rb'<c\b[^>]*\br="([A-Z]+)(\d+)"[^>]*(?:/>|>.*?</c>)',re.S)
XML=b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'


def inline(address,value,style=None):
    s=f' s="{style}"' if style is not None else ''
    return f'<c r="{address}"{s} t="inlineStr"><is><t xml:space="preserve">{escape(value)}</t></is></c>'.encode()


def rows(stream):
    buffer=b''
    while True:
        chunk=stream.read(1024*1024)
        if not chunk:
            yield False,buffer;break
        buffer+=chunk
        while True:
            start=buffer.find(b'<row ')
            if start<0:break
            end=buffer.find(b'</row>',start)
            if end<0:
                if start:yield False,buffer[:start];buffer=buffer[start:]
                break
            if start:yield False,buffer[:start]
            yield True,buffer[start:end+6]
            buffer=buffer[end+6:]


def main():
    db=sqlite3.connect(OUT/'cache/repair_cells.sqlite')
    db.execute('DROP TABLE IF EXISTS cells')
    db.execute('CREATE TABLE cells (address TEXT PRIMARY KEY, rowno INTEGER, value TEXT)')
    with gzip.open(OUT/'cache/workbook_updates.jsonl.gz','rt',encoding='utf8') as f:
        for line in f:
            r=json.loads(line);row=int(re.search(r'\d+',r['cell']).group())
            db.execute('INSERT INTO cells VALUES (?,?,?)',(r['cell'],row,r['value']))
    db.execute('CREATE INDEX cell_rows ON cells(rowno)');db.commit()
    expected=db.execute('SELECT COUNT(*) FROM cells').fetchone()[0]
    report=json.loads((OUT/'WORKBOOK_REPAIR_PREPARATION.json').read_text())
    changed=0
    with zipfile.ZipFile(SOURCE) as original, zipfile.ZipFile(TARGET,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=1,allowZip64=True) as result:
        rels=ET.fromstring(original.read('xl/_rels/workbook.xml.rels'))
        ids={x.attrib['Id'] for x in rels};number=1
        while 'rId'+str(number) in ids:number+=1
        rid='rId'+str(number)
        for info in original.infolist():
            name=info.filename
            if name=='xl/worksheets/sheet1.xml':
                with original.open(name) as src,result.open(name,'w',force_zip64=True) as dst:
                    for isrow,data in rows(src):
                        if isrow:
                            rownum=int(re.search(rb'<row\b[^>]*\br="(\d+)"',data).group(1))
                            replacements=dict(db.execute('SELECT address,value FROM cells WHERE rowno=?',(rownum,)))
                            def replace(m):
                                nonlocal changed
                                address=(m[1]+m[2]).decode()
                                if address not in replacements:return m[0]
                                style=re.search(rb'\bs="(\d+)"',m[0].split(b'>',1)[0])
                                changed+=1
                                return inline(address,replacements[address],style[1].decode() if style else None)
                            data=CELL.sub(replace,data)
                        dst.write(data)
            elif name=='xl/workbook.xml':
                data=original.read(name)
                addition=f'<sheet name="Recovered payloads" sheetId="4" r:id="{rid}"/>'.encode()
                result.writestr(name,data.replace(b'</sheets>',addition+b'</sheets>'))
            elif name=='xl/_rels/workbook.xml.rels':
                data=original.read(name)
                addition=f'<Relationship Id="{rid}" Type="{REL}/worksheet" Target="worksheets/sheet4.xml"/>'.encode()
                result.writestr(name,data.replace(b'</Relationships>',addition+b'</Relationships>'))
            elif name=='[Content_Types].xml':
                data=original.read(name)
                addition=b'<Override PartName="/xl/worksheets/sheet4.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
                result.writestr(name,data.replace(b'</Types>',addition+b'</Types>'))
            elif name=='xl/worksheets/sheet3.xml':
                data=original.read(name)
                def note(m):
                    address=(m[1]+m[2]).decode()
                    if address=='A2':
                        style=re.search(rb'\bs="(\d+)"',m[0].split(b'>',1)[0])
                        return inline(address,'Rebuilt non-S fields. Remaining dependencies and stopped S states are retained.',style[1].decode() if style else None)
                    if b'Stored status' in m[0]:return m[0].replace(b'Stored status',b'Original status before repair')
                    if address=='A38':return inline(address,f"{expected:,} cells rebuilt. {len(report['formerly_empty_fields_with_recovered_content'])} formerly empty fields now contain recovered content. S unchanged. Remaining fields are listed in the Git repair report.")
                    return m[0]
                result.writestr(name,CELL.sub(note,data))
            else:
                with original.open(name) as src,result.open(name,'w',force_zip64=True) as dst:
                    while chunk:=src.read(1024*1024):dst.write(chunk)
        with result.open('xl/worksheets/sheet4.xml','w',force_zip64=True) as dst:
            dst.write(XML+f'<worksheet xmlns="{NS}"><dimension ref="A1:D{report["payload_rows"]+1}"/><sheetViews><sheetView workbookViewId="0" showGridLines="0"><pane ySplit="1" topLeftCell="A2" state="frozen"/></sheetView></sheetViews><sheetFormatPr defaultRowHeight="18"/><cols><col min="1" max="1" width="38" customWidth="1"/><col min="2" max="3" width="12" customWidth="1"/><col min="4" max="4" width="120" customWidth="1"/></cols><sheetData>'.encode())
            dst.write(b'<row r="1">'+b''.join(inline(chr(65+i)+'1',v) for i,v in enumerate(['Payload ID','Chunk','Chunks','Complete JSON: concatenate chunks in order']))+b'</row>')
            with gzip.open(OUT/'cache/workbook_payloads.jsonl.gz','rt',encoding='utf8') as f:
                for rownum,line in enumerate(f,2):
                    values=json.loads(line)
                    dst.write(f'<row r="{rownum}">'.encode())
                    for i,value in enumerate(values):dst.write(inline(chr(65+i)+str(rownum),str(value)))
                    dst.write(b'</row>')
            dst.write(b'</sheetData></worksheet>')
    assert changed==expected,(changed,expected)
    db.close()
    h=hashlib.sha256()
    with TARGET.open('rb') as f:
        while chunk:=f.read(1024*1024):h.update(chunk)
    receipt={'file':TARGET.name,'bytes':TARGET.stat().st_size,'sha256':h.hexdigest(),
        'cells_replaced':changed,'payload_chunks':report['payload_rows'],
        'authoring_fallback':'Bundled artifact-tool import raised Arg_OutOfMemoryException. Bounded-memory OOXML edit preserves original formulas/styles/drawings.',
        'all_fields_complete':False,'verification_pending':True}
    (OUT/'WORKBOOK_FILE.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt),flush=True)


if __name__=='__main__':main()
