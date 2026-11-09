"""Read the exported Excel XML independently and compare every added cell."""

import hashlib
import json
import math
from pathlib import Path
import posixpath
import re
import sys
import xml.etree.ElementTree as ET
import zipfile


ROOT = Path(__file__).parent
DATA = ROOT / 'extended-review-data'
NS = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
REL = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'


def sheet_path(archive, sheet):
    links = ET.fromstring(archive.read('xl/_rels/workbook.xml.rels'))
    target = next(link.get('Target') for link in links if link.get('Id') == sheet.get(REL + 'id'))
    return target.lstrip('/') if target.startswith('/') else posixpath.join('xl', target)


def compare_cell(got, expected):
    if expected is None or expected == '':
        return got in (None, '')
    if isinstance(expected, bool):
        return got in (('1', 'true', 'TRUE') if expected else ('0', 'false', 'FALSE'))
    if isinstance(expected, int):
        return got is not None and float(got) == expected
    if isinstance(expected, float):
        return got is not None and math.isclose(float(got), expected, rel_tol=1e-14, abs_tol=1e-15)
    return got == expected


def column_index(address):
    col = 0
    for ch in re.match(r'[A-Z]+', address).group():
        col = col * 26 + ord(ch) - ord('A') + 1
    return col - 1


def main(path):
    expected = {}
    final = 'extended-four-day-review-final' in path.parts
    for name in ('WORKBOOK_TABLES.json', 'WORKFLOW_FINAL_TABLES.json' if final else 'WORKFLOW_TABLES.json'):
        expected.update(json.loads((DATA / name).read_bytes()))
    checked = {}
    with zipfile.ZipFile(path) as zip_file:
        sheets = ET.fromstring(zip_file.read('xl/workbook.xml')).find(NS + 'sheets')
        shared = []
        if 'xl/sharedStrings.xml' in zip_file.namelist():
            shared = [''.join(node.itertext()) for node in ET.fromstring(zip_file.read('xl/sharedStrings.xml'))]
        for sheet in sheets:
            name = sheet.get('name')
            data = expected.get(name)
            count = 0
            with zip_file.open(sheet_path(zip_file, sheet)) as stream:
                for event, node in ET.iterparse(stream, events=('end',)):
                    assert node.tag != NS + 'sheetProtection', name
                    if node.tag != NS + 'row':
                        continue
                    if data is not None:
                        row = data['headers'] if count == 0 else data['rows'][count - 1]
                        cells = {}
                        for c in node.findall(NS + 'c'):
                            assert c.find(NS + 'f') is None, name
                            value = c.findtext(NS + 'v')
                            if c.get('t') == 's' and value is not None:
                                value = shared[int(value)]
                            elif c.get('t') == 'inlineStr':
                                value = ''.join(c.find(NS + 'is').itertext())
                            cells[column_index(c.get('r'))] = value
                        for col, value in enumerate(row):
                            got = cells.get(col)
                            assert compare_cell(got, value), (name, count + 1, col + 1, str(got)[:100], str(value)[:100])
                    count += 1
                    node.clear()
            if data is not None:
                assert count == len(data['rows']) + 1, (name, count)
                checked[name] = count - 1
    assert set(checked) == set(expected)
    stages = sum(row[4] for row in expected['Dipole stage series']['rows'])
    if final:
        assert all(sheet.get('name') not in (
            'Delayed outcomes', 'Delayed outcome conditions', 'Whole lifecycle parents', 'Lifecycle component windows')
                   for sheet in sheets)
        assert all('b-delayed-outcomes.parquet' not in row[2] and 'cross-study-condition-outcomes.parquet' not in row[2]
                   for row in expected['Workflow and research files']['rows'])
        assert all(row[1] != 'Whole lifecycle audit' and row[2] not in ('B.delayed_outcomes', 'B.definitions')
                   for row in expected['Workflow findings']['rows'])
        assert all(row[6].startswith('Archived') for row in expected['Workflow and research files']['rows']
                   if row[2].startswith('whole-lifecycles/'))
        assert len(expected['Late-session clock tables']['rows']) == 529
        assert sum('precision-fix' in row[1] and row[1].endswith('.jsonl.gz')
                   for row in expected['Late-session clock files']['rows']) == 4
    receipt = dict(workbook_sha256=hashlib.sha256(path.read_bytes()).hexdigest(), workbook_sheets=len(sheets),
                   added_sheet_rows=checked, saved_dipole_stage_rows=stages,
                   delayed_outcomes_excluded=final, prior_second_workflow_excluded=final, unlocked=True,
                   every_added_cell_verified=True, complete_all_layers=False)
    (DATA / 'EXTENDED_VERIFICATION.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(receipt))


if __name__ == '__main__':
    main(Path(sys.argv[1]))
