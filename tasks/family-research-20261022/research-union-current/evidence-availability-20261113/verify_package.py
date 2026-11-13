"""Standalone publication integrity checks; does not require the original local data."""
import collections
import csv
import gzip
import hashlib
import json
from pathlib import Path

P = Path(__file__).resolve().parent


def load(name):
    return json.loads((P/name).read_text(encoding='utf8'))


def main():
    manifest = load('preservation_manifest.json')
    for r in manifest:
        packed = (P/r['path']).read_bytes()
        raw = gzip.decompress(packed)
        assert hashlib.sha256(packed).hexdigest() == r['sha256_compressed']
        assert hashlib.sha256(raw).hexdigest() == r['sha256_uncompressed']
        assert len(raw) == r['bytes']
    package = json.loads(gzip.decompress((P/'raw/package.json.gz').read_bytes()))
    fields = package['all_layer_fields']
    assert len(fields) == len(set(fields)) == 141
    total, appearances, row_groups = 0, set(), {}
    cases = load('case_manifest.json')
    for c in cases:
        d = json.loads(gzip.decompress((P/'raw'/f"{c['case_id']}.json.gz").read_bytes()))
        h = {x:i for i,x in enumerate(d['headers'])}
        assert len(h) == 167 and set(fields).issubset(h)
        assert len(d['rows']) == c['tick_appearances']
        ords = [int(r[h['trade_ordinal']]) for r in d['rows']]
        assert ords == list(range(ords[0],ords[-1]+1))
        for i,row in enumerate(d['rows']):
            appearances.add((c['case_id'],i))
            row_groups[(c['case_id'],i)] = json.loads(row[h['L029 | raw_source_identity_provenance_clocks_integrity']])['values']
        total += len(d['rows'])
    assert total == 5513 and len(cases) == 32
    assert collections.Counter(c['day'] for c in cases) == {'20231002':8,'20231003':8,'20231017':8,'20231018':8}
    assert len({c['trade_type'] for c in cases}) == 8
    clocks = [json.loads(x) for x in gzip.decompress((P/'tick_clock_ledger.jsonl.gz').read_bytes()).splitlines()]
    assert {(r['case_id'],r['row']) for r in clocks} == appearances
    assert len(clocks) == len(appearances)
    for r in clocks:
        assert int(r['before_known_by_ns']) <= int(r['receive_ns']) <= int(r['known_by_ns'])
        assert int(r['during_known_by_ns']) == int(r['known_by_ns'])
    joins = [json.loads(x) for x in gzip.decompress((P/'source_group_joins.jsonl.gz').read_bytes()).splitlines()]
    source_blobs = {r['sha'] for r in load('source_event_inventory.json')}
    assert len(joins) == 11026
    assert {(r['case_id'],r['row'],r['slot']) for r in joins} == {(c,i,s) for c,i in appearances for s in ['before','during']}
    for r in joins:
        assert r['source_blob'] in source_blobs
        original = row_groups[(r['case_id'],r['row'])][r['slot']]
        assert int(r['known_by_ns']) == int(original['known_by_ns'])
        assert r['group_ordinal'] == original['group_ordinal']
    with (P/'field_case_audit.csv').open(encoding='utf8', newline='') as f:
        audit = list(csv.DictReader(f))
    assert len(audit) == 4512
    assert {(r['case_id'],r['field']) for r in audit} == {(c['case_id'],f) for c in cases for f in fields}
    mapped = load('strategy_evidence_map.json')
    assert {s['id'] for s in mapped['strategies']} == {f'C{i}' for i in range(1,16)}
    assert len(mapped['original_five']) == 5 and len(mapped['legacy_eleven']) == 11
    assert len(mapped['additive_hypotheses']) == 6
    for s in mapped['strategies']:
        assert s['retained'] and set(s['required_fields']).issubset(fields)
        assert all(b in mapped['bindings'] for b in s['required_bindings']+s['context_bindings'])
        assert 'D11' in s['unresolved_dependencies']
    assert {r['field'] for r in load('field_inventory.json')} == set(fields)
    horizons = load('HORIZON_REGISTRY.json')
    assert not horizons['execution_enabled'] and not horizons['fitting_executed']
    assert all(p['value'] is None and not p['training_source_hashes'] for p in horizons['parameters'])
    result = {'status':'PASS','preserved_archives_verified':len(manifest),'cases':32,
        'tick_appearances':5513,'field_case_records':4512,'source_group_joins':11026,
        'strategies_mapped':15,'original_five_retained':5,'legacy_arms_retained':11,
        'additive_research_hypotheses':6,'exact_nanosecond_checks':True,
        'horizons':'unset; historical 5s/60s retained only as archived baselines',
        'new_strategy_execution':False}
    (P/'PACKAGE_VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
