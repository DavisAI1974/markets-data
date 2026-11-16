"""Add a first sheet of plain text to an existing .xlsx without touching any other part.

Every existing part is copied byte for byte (after decompression); only the workbook's three index files gain one
entry each. Usage: add_readme_page.py <workbook.xlsx> <lines.txt>
"""
import re, shutil, sys, zipfile
from xml.sax.saxutils import escape

SHEET_PART = 'xl/worksheets/readme_rebuild_20261116.xml'
REL_ID = 'rIdReadmeRebuild20261116'
SHEET_NAME = 'READ ME FIRST'
WS_TYPE = 'application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml'
WS_REL = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet'


def sheet_xml(lines):
    rows = []
    for i, line in enumerate(lines, 1):
        if line == '':
            continue
        rows.append(f'<row r="{i}"><c r="A{i}" t="inlineStr"><is><t xml:space="preserve">{escape(line)}</t></is></c></row>')
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
            '<cols><col min="1" max="1" width="150" customWidth="1"/></cols>'
            '<sheetData>' + ''.join(rows) + '</sheetData></worksheet>').encode('utf-8')


def one(pattern, text, what):
    found = re.findall(pattern, text)
    if len(found) != 1:
        raise SystemExit(f'{what}: expected exactly one match, found {len(found)}')
    return found[0]


def main(path, lines_path):
    lines = open(lines_path, encoding='utf-8').read().split('\n')
    src = zipfile.ZipFile(path)
    names = src.namelist()
    if SHEET_PART in names:
        raise SystemExit('this workbook already has the page')
    wb = src.read('xl/workbook.xml').decode('utf-8')
    rels = src.read('xl/_rels/workbook.xml.rels').decode('utf-8')
    types = src.read('[Content_Types].xml').decode('utf-8')

    if f'name="{SHEET_NAME}"' in wb:
        raise SystemExit('a sheet with this name already exists')
    open_tag = one(r'<(\w+:)?sheets>', wb, 'sheets element')          # the namespace prefix in use, e.g. "x:"
    rid_prefix = one(r'<(?:\w+:)?sheet [^>]*?(\w+):id="', wb[:wb.index('/>') + 2], 'relationship prefix')
    new_id = max(int(v) for v in re.findall(r'sheetId="(\d+)"', wb)) + 1
    entry = f'<{open_tag}sheet {rid_prefix}:id="{REL_ID}" name="{SHEET_NAME}" sheetId="{new_id}"/>'
    wb2 = wb.replace(f'<{open_tag}sheets>', f'<{open_tag}sheets>' + entry, 1)

    rp = one(r'<(\w+:)?Relationships ', rels, 'relationships element')
    rels2 = rels.replace(f'</{rp}Relationships>',
                         f'<{rp}Relationship Type="{WS_REL}" Target="/{SHEET_PART}" Id="{REL_ID}"/></{rp}Relationships>', 1)
    tp = one(r'<(\w+:)?Types ', types, 'types element')
    types2 = types.replace(f'</{tp}Types>',
                           f'<{tp}Override PartName="/{SHEET_PART}" ContentType="{WS_TYPE}"/></{tp}Types>', 1)
    for before, after, what in ((wb, wb2, 'workbook.xml'), (rels, rels2, 'workbook.xml.rels'), (types, types2, '[Content_Types].xml')):
        if before == after:
            raise SystemExit(f'{what} was not changed')
    changed = {'xl/workbook.xml': wb2.encode('utf-8'), 'xl/_rels/workbook.xml.rels': rels2.encode('utf-8'),
               '[Content_Types].xml': types2.encode('utf-8')}

    tmp = path + '.adding-page'
    with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as out:
        for info in src.infolist():
            fresh = zipfile.ZipInfo(info.filename, date_time=info.date_time)
            fresh.compress_type = zipfile.ZIP_DEFLATED
            fresh.external_attr = info.external_attr
            if info.filename in changed:
                out.writestr(fresh, changed[info.filename])
                continue
            with src.open(info) as r, out.open(fresh, 'w', force_zip64=True) as w:
                shutil.copyfileobj(r, w, 16 * 1024 * 1024)
        page = zipfile.ZipInfo(SHEET_PART, date_time=(2026, 11, 16, 0, 0, 0))
        page.compress_type = zipfile.ZIP_DEFLATED
        out.writestr(page, sheet_xml(lines))

    # check: every other part is unchanged, and the archive is sound
    new = zipfile.ZipFile(tmp)
    if new.testzip() is not None:
        raise SystemExit('new archive failed its own check')
    old_crc = {i.filename: (i.CRC, i.file_size) for i in src.infolist()}
    new_crc = {i.filename: (i.CRC, i.file_size) for i in new.infolist()}
    untouched = [n for n in old_crc if n not in changed]
    differing = [n for n in untouched if old_crc[n] != new_crc.get(n)]
    if differing or set(new_crc) - set(old_crc) != {SHEET_PART}:
        raise SystemExit(f'parts differ: {differing[:5]}')
    src.close(); new.close()
    shutil.move(tmp, path)
    print(f'{path}: page added as first sheet (sheetId {new_id}); {len(untouched)} other parts unchanged')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
