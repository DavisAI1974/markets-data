"""Populate recovered review values from immutable packets, preserving earlier phases."""
import ast,copy,datetime,gzip,hashlib,importlib.util,json,pathlib,sys
ROOT=pathlib.Path(__file__).parent
def read(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def dump(p,value):
    path=ROOT/p;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value,ensure_ascii=False,indent=1),encoding='utf-8')
layers=read('sources/LAYERS.json');by_id={x['layer_id']:x for x in layers}
samples=read('sources/REVIEW_SAMPLES.json')+[read('sources/FIFO_SAMPLE.json')]
days=read('sources/DAY_COVERAGE.json');updates={};pins=[]
bookfields={
 'full_bid_ask_depth':['bid_levels_full','ask_levels_full','bid_depth_full','ask_depth_full'],
 'price_level_and_order_counts':['bid_price_level_count_full','ask_price_level_count_full','bid_order_count_full','ask_order_count_full'],
 'fifo_queues':['bid_levels_full','ask_levels_full'],
 'queue_age_and_survival':['bid_levels_full','ask_levels_full'],
 'queue_concentration':['bid_levels_full','ask_levels_full'],
 'orders_and_volume_ahead':['bid_levels_full','ask_levels_full'],
 'spread_and_depth_imbalance':['spread','depth_imbalance_full','bid_depth_full','ask_depth_full'],
 'legacy_price':['best_bid','best_ask','mid'],
 'legacy_book_imbalance':['depth_imbalance_n','depth_imbalance_full']}
pubs=read('recovered-packets/PUBLICATIONS.json')
for pub in pubs:
    if not pub['published']:continue
    d=pub['day'];source=read(f'recovered-packets/book/{d}/REVIEW_SAMPLES.json')
    receipt=read(f'recovered-packets/book/{d}/RECOVERY_RECEIPT.json')
    assert receipt['completed_book_fifo_recovery'] and receipt['recovered_trades']==receipt['expected_trades']
    for sample in samples:
        if sample['day']!=d:continue
        hits=[r for r in source if r['trade_ordinal']==sample['trade_ordinal']]
        if not hits:continue
        row=hits[0];assert int(sample['trade_cursor'])==row['original_trade']['trade_input_cursor']
        assert int(sample['receive_ns'])==row['known_by_ns']
        for name,fields in bookfields.items():
            column=by_id[name]['column'];old=json.loads(sample[column])
            values={k:row['book_full'][k] for k in fields}
            sample[column]=json.dumps(dict(status='VERIFIED_BOOK_VALUES_RESTORED',values=values,
                phase=row['phase'],known_by_ns=row['known_by_ns'],source=dict(repository=pub['repository'],revision=pub['revision'],path=pub['prefix']+'/REVIEW_SAMPLES.json',trade_ordinal=row['trade_ordinal']),
                original_assembly_payload=old,scope='Original adapter values; queue age is present-state age, not a claim of complete cross-time survival.'),separators=(',',':'))
    for name in bookfields:
        column=by_id[name]['column'];updates.setdefault(d,{})[column]=dict(status='VERIFIED_BOOK_VALUES_RESTORED',rows=receipt['recovered_trades'],phase='at_trade_input',complete_named_semantics=name not in ('queue_age_and_survival',),source_revision=pub['revision'],source_prefix=pub['prefix'])
    for f in read(f'recovered-packets/book/{d}/MANIFEST.json')['files']:
        pins.append(dict(repository=pub['repository'],revision=pub['revision'],path=pub['prefix']+'/'+f['path'],bytes=f['bytes'],sha256=f['sha256'],role='recovered MBO/book/FIFO; original adapter',status='PUBLICATION_HASH_VERIFIED'))
# Reuse the exact pinned calendar implementation, only its single named builder function.
calendar_path=ROOT/'source-code/calendar.py'
raw=calendar_path.read_bytes();assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()=='06fa0ad2c73695da5311102ecc057a91afb8db66'
spec=importlib.util.spec_from_file_location('flow_calendar',calendar_path);fc=importlib.util.module_from_spec(spec);sys.modules['flow_calendar']=fc;spec.loader.exec_module(fc)
builder=(ROOT/'source-code/external_builder.py').read_bytes();assert hashlib.sha1(b'blob '+str(len(builder)).encode()+b'\0'+builder).hexdigest()=='11e3d1436fb46bcd5a97cb433b73f8409a4c233d'
node=next(n for n in ast.parse(builder).body if isinstance(n,ast.FunctionDef) and n.name=='sessions_since_prompt_expiry')
scope={};exec(compile(ast.Module(body=[node],type_ignores=[]),'pinned_calendar_builder','exec'),scope)
calendar={d:scope['sessions_since_prompt_expiry'](datetime.datetime.strptime(d,'%Y%m%d').date()) for d in ['20231002','20231003','20231017','20231018']}
assert calendar['20231002']['sessions_since_prompt_expiry']==3 and calendar['20231018']['sessions_since_prompt_expiry']==15
dump('filled-review/CALENDAR_VALUES.json',dict(values=calendar,calendar_blob='06fa0ad2c73695da5311102ecc057a91afb8db66',builder_blob='11e3d1436fb46bcd5a97cb433b73f8409a4c233d',availability_rule='Deterministic calendar calculation for the labeled trading date. This is not a historical publication receipt.'))
external=read('external-recovery/october02-external-recovery.json')
external_rev='975d79bcb59ecaa7b128c53a774edee5274df8ca'
latest={}
with gzip.open(ROOT/'external-recovery/october02-normalized-evidence.jsonl.gz','rt',encoding='utf-8') as stream:
    for line in stream:
        r=json.loads(line)
        if r['available_ns'] is None or r['available_ns']>=external['halt_exclusive_ns'] or not r['numeric']:continue
        key=r['point_name'];prior=latest.get(key)
        if prior is None or (r['available_ns'],r['observation_id'])>(prior['available_ns'],prior['observation_id']):latest[key]=r
external_values=[]
for point in external['points']:
    examples=[]
    for table in point['original_tables']:
        if table in latest:
            r=latest[table]
            examples.append({k:r[k] for k in ['point_name','numeric','observation_id','event_ns','source_published_ns','available_ns','disposition','clock_rule']})
    external_values.append(dict(point_id=point['id'],status=point['status'],original_available_reconstruction=point['available_reconstruction'],latest_retained_examples=examples,
        example_rule='Latest declared availability before archived halt, separately per original table; held clocks and vintages remain held. These examples do not replace the 146800-row pinned dataset.'))
dump('filled-review/EXTERNAL_VALUES.json',external_values)
for point in external_values:dump(f'filled-review/external-point-{point["point_id"]:02d}.json',point)
for sample in samples:
    if sample['day']!='20231002':continue
    for point in external['points']:
        layer=next(x for x in layers if x.get('point',{}).get('point_id')==point['id'])
        original=point['available_reconstruction']
        if original is None or int(original.get('available_ns',2**63))>int(sample['receive_ns']):continue
        sample[layer['column']]=json.dumps(dict(status='RESTORED_EXTERNAL_ORIGINAL_VALUE',values=original,
            original_recovery_status=point['status'],source_revision=external_rev,source_path='tasks/family-research-20261022/frankie-four-day-pins/external-recovery-20261109/october02-external-recovery.json',
            original_assembly_payload=json.loads(sample[layer['column']]),percentile_vintage_limit=external.get('cftc_percentile_vintage_limit')),separators=(',',':'))
dump('filled-review/REVIEW_SAMPLES.json',samples)
dump('filled-review/COVERAGE_UPDATES.json',updates)
dump('filled-review/RECOVERY_PINS.json',pins)
print(json.dumps(dict(published_book_days=[p['day'] for p in pubs if p['published']],review_examples=len(samples),new_source_pins=len(pins),calendar=calendar,complete_all_layers=False)))
