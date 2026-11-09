"""Pin every restored packet together and load the updated native brain format."""
import hashlib,json,pathlib,shutil,sys
ROOT=pathlib.Path(__file__).parent;OUT=ROOT/'consolidated-recovery';OUT.mkdir(exist_ok=True)
def read(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def dump(path,value):path.write_text(json.dumps(value,indent=1,ensure_ascii=False)+'\n',encoding='utf-8')
layers=read('sources/LAYERS.json');books=read('recovered-packets/PUBLICATIONS.json');natives=read('recovered-packets/NATIVE_PUBLICATIONS.json')
pins=read('sources/INPUT_PINS.json')['sources']+read('filled-review/RECOVERY_PINS.json')
packets=[]
for kind,pubs in [('book',books),('native',natives)]:
    for pub in pubs:
        receipt=read(f'recovered-packets/{kind}/{pub["day"]}/RECOVERY_RECEIPT.json')
        manifest=read(f'recovered-packets/{kind}/{pub["day"]}/MANIFEST.json')
        packets.append(dict(kind=kind,**pub,receipt=receipt))
        if kind=='native':
            for f in manifest['files']:
                pins.append(dict(repository=pub['repository'],revision=pub['revision'],path=pub['prefix']+'/'+f['path'],bytes=f['bytes'],sha256=f['sha256'],role='original Native lifecycle rows and exact clock indices',status='PUBLICATION_HASH_VERIFIED'))
for entry in read('external-recovery/MANIFEST.json')['files']:
    pins.append(dict(**entry,role='restored original external evidence; retain held availability states',status='BYTES_VERIFIED'))
unique={}
for p in pins:
    key=(p['repository'],p['revision'],p.get('source_path',p['path']))
    unique[key]=p
dump(OUT/'INPUT_PINS.json',dict(schema='FRANKIE_CONSOLIDATED_RECOVERY_PINS_V1',sources=list(unique.values()),complete_all_layers=False))
dump(OUT/'RECOVERED_PACKETS.json',packets);dump(OUT/'LAYERS.json',layers)
shutil.copyfile(ROOT/'filled-review/CALENDAR_VALUES.json',OUT/'CALENDAR_VALUES.json')
shutil.copyfile(ROOT/'filled-review/COVERAGE_UPDATES.json',OUT/'BOOK_COVERAGE.json')
brain=OUT/'brain/20261109-search';shutil.copytree(ROOT/'static-recovery/brain/20261109-search',brain,dirs_exist_ok=True)
manifest=json.loads((brain/'MANIFEST.json').read_text());entries=manifest['entries']
findings=dict(schema='FRANKIE_RECOVERY_FINDINGS_20261109_V2',complete_all_layers=False,
    verified_book_trades=sum(p['receipt']['recovered_trades'] for p in packets if p['kind']=='book'),
    recovered_native_rows=sum(p['receipt']['source_rows'] for p in packets if p['kind']=='native'),
    restored_external_rows=146800,calendar=read('filled-review/CALENDAR_VALUES.json'),packets=packets,
    causes=['The 99-layer registry contains mixed source, runtime-output, target and knowledge roles; a source pin alone is not a populated runtime output.',
      'Static source paths were already retained under canonical-sources but the exporter failed to resolve that prefix.',
      'The older exporter explicitly selected levels[0]; full depth and FIFO required the original adapter recovery.',
      'The earlier assembly omitted the retained October 2 external-recovery directory.',
      'The original Native ledger existed in the first archive parts despite incomplete publication of the larger remainder archive.',
      'Large Git tree publication requests timed out; bounded tree batches preserve and verify every file.'],
    remaining=['Complete full-population layer joins and independently verify their semantics.',
      'Restore or execute missing original second-set calculations for October 2, 3 and 17.',
      'Resolve held external availability/vintage requirements without promoting modeled clocks to verified historical release clocks.',
      'Retain absent runtime outputs as unproduced; source code is not evidence of execution.',
      'Only after every required input is complete, lock Excel and connect the code by layer identity with consumption receipts.'],
    execution_claim='Saved source recovery and native brain-loader verification only. No Frankie model invocation or live brain deployment is claimed.')
additions={'RECOVERY_FINDINGS_20261109_V2.json':json.dumps(findings,indent=1).encode(),
           'RESTORED_EXTERNAL_SCOPE.md':(ROOT/'external-recovery/README.md').read_bytes(),
           'RECOVERED_LAYER_DIRECTORY.json':json.dumps(layers,indent=1).encode()}
for name,data in additions.items():
    (brain/name).write_bytes(data)
    entries.append(dict(name=name,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),include=True,source='four-day recovery, immutable source coordinates recorded in RECOVERY_FINDINGS_20261109_V2.json',kind='verified recovery findings and original limitations'))
dump(brain/'MANIFEST.json',manifest)
sys.path.insert(0,'E:/Markets-frankie-brain-20261109/deploy/aws/box');import frankie_box_brain
corpus,members=frankie_box_brain.load(OUT/'brain',0,day='20231018')
loaded={m.get('sha256') for m in members if m.get('treatment','').startswith('brain:')}
assert {e['sha256'] for e in entries}<=loaded
dump(OUT/'BRAIN_LOAD_RECEIPT.json',dict(native_loader='deploy/aws/box/frankie_box_brain.py',manifest_entries=len(entries),loaded_member_records=len(members),unique_sha256=len(loaded),corpus_utf8_bytes=len(corpus.encode()),model_called=False,live_runtime_deployed=False))
dump(OUT/'STATUS.json',dict(complete_all_layers=False,locked=False,source_pins=len(unique),book_trades=findings['verified_book_trades'],native_rows=findings['recovered_native_rows'],external_rows=146800,remaining=findings['remaining']))
print(json.dumps(dict(pins=len(unique),brain_entries=len(entries),book_trades=findings['verified_book_trades'],native_rows=findings['recovered_native_rows'])))
