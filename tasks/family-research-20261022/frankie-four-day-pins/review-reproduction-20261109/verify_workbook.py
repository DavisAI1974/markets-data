import collections,hashlib,json,pathlib,xml.etree.ElementTree as ET,zipfile
ROOT=pathlib.Path(__file__).parent
book=next((ROOT/'outputs').rglob('*.xlsx'))
NS={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
with zipfile.ZipFile(book) as archive:
    sheets=ET.fromstring(archive.read('xl/workbook.xml')).find('s:sheets',NS)
    shared=[]
    if 'xl/sharedStrings.xml' in archive.namelist():
        shared=[''.join(x.itertext()) for x in ET.fromstring(archive.read('xl/sharedStrings.xml'))]
    tables={}
    for i,sheet in enumerate(sheets,1):
        tree=ET.fromstring(archive.read(f'xl/worksheets/sheet{i}.xml'))
        assert tree.find('s:sheetProtection',NS) is None
        rows=[]
        for row in tree.findall('s:sheetData/s:row',NS):
            result=[]
            for cell in row.findall('s:c',NS):
                assert cell.find('s:f',NS) is None
                value=cell.find('s:v',NS)
                value='' if value is None else value.text or ''
                if cell.get('t')=='s':value=shared[int(value)]
                elif cell.get('t')=='inlineStr':value=''.join(cell.find('s:is',NS).itertext())
                result.append(value)
            rows.append(result)
        tables[sheet.get('name')]=rows
layers=json.loads((ROOT/'sources/LAYERS.json').read_text())
labels=[x['column'] for x in layers]
assert tables['Layer coverage'][0][3:]==labels
assert tables['Trade layer values'][0][3:]==labels
assert len(tables['Trade layer values'])==14
chunks=collections.defaultdict(list)
for ident,number,total,encoded in tables['Payload text'][1:]:
    chunks[ident].append((int(number),int(total),json.loads(encoded)))
payloads={}
for ident,rows in chunks.items():
    rows.sort()
    assert [x[0] for x in rows]==list(range(1,len(rows)+1))
    assert {x[1] for x in rows}=={len(rows)}
    payloads[ident]=''.join(x[2] for x in rows)
for ident,kind,chars,digest,count in tables['Payload index'][1:]:
    text=payloads[ident]
    assert hashlib.sha256(text.encode()).hexdigest()==digest,ident
    assert len(chunks[ident])==int(count)
sources=json.loads((ROOT/'filled-review/REVIEW_SAMPLES.json').read_text())
static={x['column'] for x in json.loads((ROOT/'static-recovery/LAYER_VALUES.json').read_text())}
for source,row in zip(sources,tables['Trade layer values'][1:]):
    assert row[:3]==[source['trade_id'],'ns '+source['receive_ns'],'ns '+source['known_by_ns']]
    for label,value in zip(labels,row[3:]):
        assert value
        ident=value.split('\n')[-1]
        if label not in static: assert payloads[ident]==source[label],(source['trade_id'],label)
for name,kind,ident,size,digest,origin in tables['Brain contents'][1:]:
    data=(ROOT/'consolidated-recovery/brain/20261109-search'/name).read_bytes()
    assert payloads[ident].encode()==data
expected_pins=len(json.loads((ROOT/'consolidated-recovery/INPUT_PINS.json').read_text())['sources'])
assert len(tables['Source pins'])-1==expected_pins
forecast=json.loads((ROOT/'external-recovery/october02-mos-reconstruction.json').read_text())
for source,row in zip(forecast['forecast_rows'],tables['Forecast recovered'][1:]):
    assert float(row[3])==source['gw_hdd'] and json.loads(payloads[row[7]])==source
for source,row in zip(forecast['disagreement_cycles'],tables['Disagreement recovered'][1:]):
    assert float(row[2])==source['max_abs_spread_gw_hdd'] and json.loads(payloads[row[4]])==source
flow=json.loads((ROOT/'flow-input-recovery/SUMMARY.json').read_text())
for source,row in zip(flow,tables['Flow coverage'][1:]):
    assert row[0]==source['day'] and int(row[1])==source['trades']
    assert int(row[2])==int(row[3])==source['matched_original_emissions']
    assert int(row[4])==source.get('not_yet_emitted',source.get('not_yet_emitted_in_retained_projection',0))
assert sum(int(row[1]) for row in tables['Flow coverage'][1:])==143270
mbo=json.loads((ROOT/'mbo-layer-data/ALL_DAYS.json').read_text())
for source,row in zip(mbo,tables['MBO layer data'][1:]):
    assert row[0]==source['day']
    ident=row[1].split('Full examples and immutable source: ')[1].split('\n')[0]
    assert json.loads(payloads[ident])==source
external=json.loads((ROOT/'filled-review/EXTERNAL_VALUES.json').read_text())
for source,cell in zip(external,tables['Recovered external'][1][1:]):
    ident=cell.split('Full values and source clocks: ')[1]
    assert json.loads(payloads[ident])==source
receipt=dict(workbook_sha256=hashlib.sha256(book.read_bytes()).hexdigest(),bytes=book.stat().st_size,
             sheets=len(tables),layer_columns=len(labels),trade_examples=len(sources),
             payloads=len(payloads),payload_chunks=sum(map(len,chunks.values())),
             checks=['all 131 layer headers preserved in both matrices','all populated source payloads round-trip exactly',
                     f'all {len(tables["Brain contents"])-1} brain documents round-trip exactly','all sample nanosecond clocks preserved exactly',
                     f'{expected_pins} original and recovered source pins retained','all restored forecasts and disagreement rows match sources','all sheets remain unlocked'],complete_all_layers=False)
(ROOT/'saved-workbook-verification.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
