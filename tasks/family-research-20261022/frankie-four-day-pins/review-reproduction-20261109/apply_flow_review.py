import json,pathlib
import pyarrow.parquet as pq
ROOT=pathlib.Path(__file__).parent
samples=json.loads((ROOT/'filled-review/REVIEW_SAMPLES.json').read_text());summaries=json.loads((ROOT/'flow-input-recovery/SUMMARY.json').read_text())
coverage={}
for summary in summaries:
    day=summary['day'];ordinals=[s['trade_ordinal'] for s in samples if s['day']==day]
    rows={r['trade_ordinal']:r for r in pq.read_table(ROOT/f'flow-input-recovery/{day}/trade-flow-inputs.parquet',filters=[('trade_ordinal','in',ordinals)]).to_pylist()}
    for sample in samples:
        if sample['day']!=day:continue
        original=rows[sample['trade_ordinal']];assert original['receive_ns']==sample['receive_ns']
        for column in ['L055 | legacy_native_signed_flow','L056 | legacy_per_second_roll20']:
            sample[column]=original[column]
    coverage[day]=dict(matched=summary['matched_original_emissions'],not_yet_emitted=summary.get('not_yet_emitted',summary.get('not_yet_emitted_in_retained_projection',0)),complete_flow_stream=summary.get('complete_flow_stream',True))
(ROOT/'filled-review/REVIEW_SAMPLES.json').write_text(json.dumps(samples,indent=1))
(ROOT/'filled-review/FLOW_COVERAGE.json').write_text(json.dumps(coverage,indent=1))
print(json.dumps(coverage))
