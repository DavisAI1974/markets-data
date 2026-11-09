import collections,json,pathlib
import pyarrow.parquet as pq
ROOT=pathlib.Path(__file__).parent;days=[]
for path in sorted((ROOT/'flow-input-recovery').glob('*/trade-flow-inputs.parquet')):
    receipt=json.loads(path.with_name('RECEIPT.json').read_text());count=matched=missing=0;seen=set()
    for batch in pq.ParquetFile(path).iter_batches(batch_size=1024):
        for row in batch.to_pylist():
            assert row['trade_ordinal']==count and row['trade_id'] not in seen;seen.add(row['trade_id']);count+=1
            first=row['L055 | legacy_native_signed_flow'];assert first==row['L056 | legacy_per_second_roll20']
            value=json.loads(first)
            if value['status'].startswith('NOT_YET_EMITTED'):
                assert 'records' not in value;missing+=1;continue
            matched+=1;assert value['asof_receive_ns']==int(row['receive_ns'])
            assert value['known_by_ns']<=int(row['receive_ns']) and value['records']
            for record in value['records']:
                if 'index' in record:
                    original=json.loads(record['original_json']);clock=record['index']['known_by_ns']
                else:
                    original=record['original_record']['original_record'];clock=record['original_record']['known_by_ns']
                assert original['emitting_section']=='flow_substrate'
                assert original['emitted_at_recv_ns']==clock==value['known_by_ns']
    assert count==receipt['trades'] and matched==receipt['matched_original_emissions']
    assert missing==receipt.get('not_yet_emitted',receipt.get('not_yet_emitted_in_retained_projection',0))
    days.append(dict(day=receipt['day'],trades=count,joined=matched,not_yet_emitted=missing))
mbo=json.loads((ROOT/'mbo-layer-data/ALL_DAYS.json').read_text());totals=collections.Counter()
for day in mbo:
    for phase,counts in day['counts'].items():
        assert sum(counts.get(action,0) for action in 'ACMRTFN')==counts.get('all_messages',0)
        totals[phase]+=counts.get('all_messages',0)
    assert day['counts']['archived_session']['T']==next(r['trades'] for r in days if r['day']==day['day'])
result=dict(days=days,trade_rows=sum(r['trades'] for r in days),mbo=dict(totals),checks=['Every saved trade retained exactly once in source order','Every joined flow emission is known by its trade receive clock','All tied source records retain their original emission clock','Original flow payloads retain their original section and emission provenance','All A/C/M/R/T/F/N messages reconcile exactly, separately for session and warmup','Session trade-action counts match all four trade populations'],complete_all_layers=False)
(ROOT/'FULL_RECOVERY_VERIFICATION.json').write_text(json.dumps(result,indent=1));print(json.dumps(result))
