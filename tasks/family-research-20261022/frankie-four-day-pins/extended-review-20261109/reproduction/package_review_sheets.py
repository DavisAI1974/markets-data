"""Package artifact-tool sheet replacements without reserializing unchanged worksheet data."""

from copy import deepcopy
from pathlib import PurePosixPath
import xml.etree.ElementTree as ET
from zipfile import ZIP_DEFLATED, ZipFile

from verify_extended_review import DATA, NS, REL, ROOT, sheet_path


PACKAGE = '{http://schemas.openxmlformats.org/package/2006/relationships}'
TYPES = '{http://schemas.openxmlformats.org/package/2006/content-types}'
WORKBOOK = 'xl/workbook.xml'
LINKS = 'xl/_rels/workbook.xml.rels'
CONTENT = '[Content_Types].xml'
BOOK = 'Frankie_four_day_layer_review.xlsx'
OMIT = {'Delayed outcomes', 'Delayed outcome conditions', 'Whole lifecycle parents',
        'Lifecycle component windows'}


def xml(tree):
    return ET.tostring(tree, encoding='utf-8', xml_declaration=True)


def relationships(part):
    file = PurePosixPath(part)
    return str(file.parent / '_rels' / (file.name + '.rels'))


def main():
    initial = ROOT / 'outputs/extended-four-day-review' / BOOK
    output = ROOT / 'outputs/extended-four-day-review-final' / BOOK
    output.parent.mkdir(exist_ok=True)
    with ZipFile(initial) as base, ZipFile(DATA / 'review-sheet-replacements.xlsx') as delta:
        book = ET.fromstring(base.read(WORKBOOK))
        sheets = book.find(NS + 'sheets')
        links = ET.fromstring(base.read(LINKS))
        types = ET.fromstring(base.read(CONTENT))
        changed = {}
        deleted = set()
        template = next(sheet for sheet in sheets if sheet.get('name') == 'Workflow and research files')
        style_data = ET.fromstring(base.read(sheet_path(base, template))).find(NS + 'sheetData')
        styles = [row.find(NS + 'c').get('s') for row in list(style_data)[:3]]
        assert all(styles)
        next_id = max(int(sheet.get('sheetId')) for sheet in sheets)
        for sheet in list(sheets):
            if sheet.get('name') not in OMIT:
                continue
            part = sheet_path(base, sheet)
            deleted.update((part, relationships(part)))
            links.remove(next(x for x in links if x.get('Id') == sheet.get(REL + 'id')))
            types.remove(next(x for x in types if x.get('PartName') == '/' + part))
            sheets.remove(sheet)
        edits = ET.fromstring(delta.read(WORKBOOK)).find(NS + 'sheets')
        shared = (list(ET.fromstring(delta.read('xl/sharedStrings.xml')))
                  if 'xl/sharedStrings.xml' in delta.namelist() else [])
        for edited in edits:
            name = edited.get('name')
            replacement = ET.fromstring(delta.read(sheet_path(delta, edited)))
            data = replacement.find(NS + 'sheetData')
            for cell in data.iter(NS + 'c'):
                if cell.get('t') == 's':
                    value = cell.find(NS + 'v')
                    string = deepcopy(shared[int(value.text)])
                    cell.remove(value)
                    string.tag = NS + 'is'
                    cell.append(string)
                    cell.set('t', 'inlineStr')
            old = next((x for x in sheets if x.get('name') == name), None)
            if old is None:
                next_id += 1
                part = f'xl/worksheets/sheet{next_id}.xml'
                rid = f'ReviewClockSheet{next_id}'
                ET.SubElement(sheets, NS + 'sheet', {'name': name, 'sheetId': str(next_id), REL + 'id': rid})
                ET.SubElement(links, PACKAGE + 'Relationship',
                              Id=rid, Type=REL[1:-1] + '/worksheet', Target='/' + part)
                ET.SubElement(types, TYPES + 'Override', PartName='/' + part,
                              ContentType='application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml')
            else:
                part = sheet_path(base, old)
            if name == 'Review':
                cover = ET.fromstring(base.read(part))
                cover_data = cover.find(NS + 'sheetData')
                original = {row.get('r'): row for row in cover_data}
                reference = {c.get('r')[0]: c.get('s') for c in original['33'].findall(NS + 'c')}
                for row in data:
                    ident = row.get('r')
                    if ident in original:
                        cover_data.remove(original[ident])
                    for cell in row.findall(NS + 'c'):
                        cell.set('s', reference[cell.get('r')[0]])
                    cover_data.append(row)
                cover_data[:] = sorted(cover_data, key=lambda row: int(row.get('r')))
                replacement = cover
            else:
                for index, row in enumerate(data):
                    style = styles[0 if index == 0 else (1 if index % 2 else 2)]
                    for cell in row.findall(NS + 'c'):
                        cell.set('s', style)
                deleted.add(relationships(part))
            changed[part] = xml(replacement)
        changed.update({WORKBOOK: xml(book), LINKS: xml(links), CONTENT: xml(types)})
        with ZipFile(output, 'w', ZIP_DEFLATED, compresslevel=6) as out:
            for name in base.namelist():
                if name not in deleted and name not in changed:
                    out.writestr(name, base.read(name))
            for name, contents in changed.items():
                out.writestr(name, contents)
    print(output)


if __name__ == '__main__':
    main()
