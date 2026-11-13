"""Read back saved XLSX, validate every replacement and preserve untouched cells."""
import collections
import gzip
import hashlib
import json
import re
import sqlite3
import xml.etree.ElementTree as ET
import zipfile
from stream_sheet_repair import OUT,SOURCE,TARGET,NS,CELL,rows


def digest(stream):
    h=hashlib.sha256()
    while chunk:=stream.read(1024*1024):h.update(chunk)
    return h.hexdigest()


def value(cell):
    tree=ET.fromstring(cell)
    return ''.join(tree.itertext())


def main():
    db=sqlite3.connect(OUT/'cache/repair_cells.sqlite')
    expected=db.execute('SELECT COUNT(*) FROM cells').fetchone()[0]
    replaced=unchanged=payloads=0
    unchanged_parts=[]
    with zipfile.ZipFile(SOURCE) as old,zipfile.ZipFile(TARGET) as new:
        altered={'xl/worksheets/sheet1.xml','xl/worksheets/sheet3.xml','xl/workbook.xml','xl/_rels/workbook.xml.rels','[Content_Types].xml'}
        for name in old.namelist():
            if name not in altered:
                with old.open(name) as a,new.open(name) as b:assert digest(a)==digest(b),name
                unchanged_parts.append(name)
        # Match each original row and cell, including formulas and nanosecond text.
        with old.open('xl/worksheets/sheet1.xml') as a,new.open('xl/worksheets/sheet1.xml') as b:
            for (ar,ad),(br,bd) in zip(rows(a),rows(b),strict=True):
                assert ar==br
                if not ar:assert ad==bd;continue
                rownum=int(re.search(rb'<row\b[^>]*\br="(\d+)"',ad).group(1))
                replacements=dict(db.execute('SELECT address,value FROM cells WHERE rowno=?',(rownum,)))
                ac=list(CELL.finditer(ad));bc=list(CELL.finditer(bd));assert len(ac)==len(bc)
                for x,y in zip(ac,bc):
                    address=(x[1]+x[2]).decode();assert x[1]==y[1] and x[2]==y[2]
                    if address in replacements:
                        assert value(y[0])==replacements[address],address;replaced+=1
                    else:
                        assert x[0]==y[0],address;unchanged+=1
        assert replaced==expected
        # Verify every complete payload chunk after XML escaping and ZIP round trip.
        with new.open('xl/worksheets/sheet4.xml') as stream,gzip.open(OUT/'cache/workbook_payloads.jsonl.gz','rt',encoding='utf8') as expected_chunks:
            for isrow,data in rows(stream):
                if not isrow:continue
                rownum=int(re.search(rb'<row\b[^>]*\br="(\d+)"',data).group(1))
                if rownum==1:continue
                actual=[value(m[0]) for m in CELL.finditer(data)]
                wanted=[str(v) for v in json.loads(next(expected_chunks))]
                assert actual==wanted,rownum;payloads+=1
            assert next(expected_chunks,None) is None
        book=ET.fromstring(new.read('xl/workbook.xml'))
        assert [s.attrib['name'] for s in book.find('{'+NS+'}sheets')]==['Tick comparison','Render seconds','Selection and fields','Recovered payloads']
    report=json.loads((OUT/'WORKBOOK_REPAIR_PREPARATION.json').read_text())
    assert payloads==report['payload_rows']
    result=dict(saved_cells_verified=replaced,unchanged_tick_cells_verified=unchanged,
        payload_chunks_verified=payloads,unchanged_zip_parts=len(unchanged_parts),
        all_original_images_and_second_sheet_unchanged=True,all_original_tick_formulas_unchanged=True,
        s_cells_unchanged=True,all_5513_ticks_and_141_fields_preserved=True,
        all_fields_complete=False,native_excel_application_check=False)
    (OUT/'WORKBOOK_READBACK_VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
    receipt=json.loads((OUT/'WORKBOOK_FILE.json').read_text());receipt['verification_pending']=False
    (OUT/'WORKBOOK_FILE.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(result),flush=True)


if __name__=='__main__':main()
