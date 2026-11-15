"""Extract six exact saved cells for a bounded-memory content preview."""
import gzip
import itertools
import json
import xml.etree.ElementTree as ET
import zipfile
from stream_sheet_repair import OUT, TARGET, CELL, rows

updates = [json.loads(s) for s in itertools.islice(gzip.open(OUT/'cache/supplement_updates.jsonl.gz','rt'), 6)]
wanted = {r['cell']: r for r in updates}
found = {}
with zipfile.ZipFile(TARGET) as z:
    with z.open('xl/worksheets/sheet1.xml') as f:
        for isrow, data in rows(f):
            if not isrow:
                continue
            for m in CELL.finditer(data):
                address = (m[1]+m[2]).decode()
                if address in wanted:
                    found[address] = ''.join(ET.fromstring(m[0]).itertext())
            if len(found) == len(wanted):
                break
matrix = [['Saved cell', 'Field', 'Saved status', 'Saved scope / value']]
for address, r in wanted.items():
    assert found[address] == r['value']
    value = json.loads(found[address])
    summary = value.get('scope') or json.dumps(value.get('values'), ensure_ascii=False)
    if r['field'].startswith('L093'):
        summary = f"{value['values']['record_count']} original discoveries eligible at exact clock/cursor. " + value['values']['rule']
    matrix.append([address, r['field'], value['status'], summary])
(OUT/'cache/preview-values.json').write_text(json.dumps(matrix), encoding='utf8')
