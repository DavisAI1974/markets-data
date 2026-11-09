import hashlib,json,pathlib,sys
ROOT=pathlib.Path(__file__).parent;OUT=ROOT/'consolidated-recovery'
def dump(p,x):p.write_text(json.dumps(x,indent=1)+'\n',encoding='utf-8')
pins=json.loads((OUT/'INPUT_PINS.json').read_text());seen={(p['repository'],p['revision'],p['path']) for p in pins['sources']}
sources=[('flow-input-recovery','5828b1ad78d09ebf8da995c822408e759f41ae06'),('mbo-layer-data','21a8bf9ec122a8156d662e60809d5efe98c043f9')]
for folder,rev in sources:
    for p in sorted((ROOT/folder).rglob('*')):
        if not p.is_file():continue
        data=p.read_bytes();path=f'tasks/family-research-20261022/frankie-four-day-pins/{folder}-20261109/'+p.relative_to(ROOT/folder).as_posix();key=('DavisAI1974/markets-data',rev,path)
        if key not in seen:pins['sources'].append(dict(repository=key[0],revision=rev,path=path,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),role='recovered layer data and full-population joins',status='PUBLICATION_HASH_VERIFIED'));seen.add(key)
dump(OUT/'INPUT_PINS.json',pins)
flow=json.loads((ROOT/'flow-input-recovery/SUMMARY.json').read_text());mbo=json.loads((ROOT/'mbo-layer-data/ALL_DAYS.json').read_text())
record=dict(schema='FRANKIE_FINAL_RECOVERY_CHECKPOINT_V1',complete_all_layers=False,locked=False,
    saved_trade_rows=sum(r['trades'] for r in flow),flow_joined_rows=sum(r['matched_original_emissions'] for r in flow),
    true_not_yet_emitted_rows=4,october18_flow_stream_scope='retained historical projection; not asserted complete',
    mbo_archived_messages=sum(r['counts']['archived_session']['all_messages'] for r in mbo),
    mbo_warmup_messages=sum(r['counts']['opening_warmup'].get('all_messages',0) for r in mbo),
    complete_source_pins=len(pins['sources']),flow=flow,mbo_counts=[dict(day=r['day'],counts=r['counts']) for r in mbo],
    access_blocker=dict(service='AWS connector',operation='S3 ListObjectsV2 under the known Frankie archive prefix',error='This app connection requires reauthentication. Reconnect the app and try again.',effect='Additional archive checks cannot proceed through the connected AWS app until it is reauthenticated.'),
    remaining=['Original second-set data for October 2, 3 and 17 remains unfilled.',
      'Some named derived, prebirth, target and runtime-output layers remain unverified or unproduced. No source definition is represented as an executed result.',
      'Held historical publication clocks and data vintages remain held even where numeric observations were restored.',
      'Final locking and runtime sheet consumption remain deferred until completeness is verified.'])
dump(OUT/'LATEST_STATUS.json',record)
brain=OUT/'brain/20261109-search';manifest=json.loads((brain/'MANIFEST.json').read_text());name='LATEST_RECOVERY_CHECKPOINT.json';data=json.dumps(record,indent=1).encode();(brain/name).write_bytes(data)
manifest['entries']=[r for r in manifest['entries'] if r['name']!=name]+[dict(name=name,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),include=True,source='latest four-day recovery checkpoint; immutable flow and MBO source coordinates retained',kind='current verified recovery findings and remaining blockers')]
dump(brain/'MANIFEST.json',manifest)
sys.path.insert(0,'E:/Markets-frankie-brain-20261109/deploy/aws/box');import frankie_box_brain
corpus,members=frankie_box_brain.load(OUT/'brain',0,day='20231018');loaded={m.get('sha256') for m in members if m.get('treatment','').startswith('brain:')}
assert {e['sha256'] for e in manifest['entries']}<=loaded
dump(OUT/'BRAIN_LOAD_RECEIPT.json',dict(native_loader='deploy/aws/box/frankie_box_brain.py',manifest_entries=len(manifest['entries']),loaded_member_records=len(members),unique_sha256=len(loaded),corpus_utf8_bytes=len(corpus.encode()),model_called=False,live_runtime_deployed=False))
print(json.dumps({k:v for k,v in record.items() if k not in ('flow','mbo_counts','remaining','access_blocker')}))
