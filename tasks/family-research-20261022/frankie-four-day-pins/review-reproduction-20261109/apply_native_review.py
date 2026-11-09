import json,pathlib
ROOT=pathlib.Path(__file__).parent
samples=json.loads((ROOT/'filled-review/REVIEW_SAMPLES.json').read_text())
native=json.loads((ROOT/'filled-review/NATIVE_REVIEW_VALUES.json').read_text())
layers=json.loads((ROOT/'sources/LAYERS.json').read_text());columns={r['layer_id']:r['column'] for r in layers}
by_trade={r['trade_id']:r for r in native}
bindings={'depletion_and_replenishment':['absorption','replenishment'],
          'resilience_and_recovery':['replenishment'],
          'churn_and_queue_turnover':['queue','absorption'],
          'legacy_native_signed_flow':['flow_substrate'],
          'legacy_per_second_roll20':['flow_substrate'],
          'derived_roll20_and_dipole_state':['flow_substrate','episode'],
          'clock_prospective_discovery_confirmation':['candidate','episode']}
count=0
for sample in samples:
    if sample['trade_id'] not in by_trade:continue
    source=by_trade[sample['trade_id']]
    for layer,sections in bindings.items():
        values={k:source['sections'][k] for k in sections if k in source['sections']}
        if not values:continue
        column=columns[layer]
        prior=json.loads(sample[column])
        assert prior.get('status')!='ORIGINAL_NATIVE_EMISSIONS_RESTORED','Regenerate base review before applying Native values twice'
        sample[column]=json.dumps(dict(status='ORIGINAL_NATIVE_EMISSIONS_RESTORED',values=values,source=source['source'],asof_receive_ns=sample['receive_ns'],
                original_assembly_payload=prior,scope=source['scope'],complete_named_layer=False),separators=(',',':'))
        count+=1
(ROOT/'filled-review/REVIEW_SAMPLES.json').write_text(json.dumps(samples,indent=1))
(ROOT/'filled-review/NATIVE_LAYER_BINDINGS.json').write_text(json.dumps(dict(bindings=bindings,scope='Saved Native section evidence, not proof all named semantics are complete',populated_review_cells=count),indent=1))
print('Populated exact Native evidence cells',count)
