"""Read-only checks against Desktop's original source tables and lifecycle arrays."""

from collections import Counter
import csv
from datetime import datetime, timezone
import gzip
import json
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).parent / 'extended-review-data'
DATA = ROOT / 'desktop-original-audit'
DAYS = ('20231002', '20231003', '20231017', '20231018')
REV = 'beb2104c079045c24832f2279eac5e8e69bc576e'
PREFIX = 'tasks/family-research-20261022/claude-pass-3day'
SOURCE = f'https://github.com/DavisAI1974/Markets/blob/{REV}/{PREFIX}'
NS = 10**9
EVENTS = ('k_aggressor_start', 'k_touch_size_change', 'k_quote_relocation')


def read_csv(path):
    with path.open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream))


def index(rows, key):
    indexed = {r[key]: r for r in rows}
    assert len(indexed) == len(rows), key
    return indexed


def close(a, b):
    return math.isclose(float(a), float(b), rel_tol=1e-10, abs_tol=1e-10)


def day_audit(day, curve_rows):
    root = DATA / 'tables/dipole' / day
    cover = index(read_csv(root / 't6_cohort_coverage.csv'), 'row')
    features = index(read_csv(root / 't6_cohort_features.csv'), 'row')
    events = index(read_csv(root / 'x07_first_events.csv'), 'row')
    omitted = Counter(row['uncovered_reason'] for row in cover.values() if row['uncovered_reason'])
    eligible = {key for key, row in cover.items() if not row['uncovered_reason']}
    assert eligible == set(features) == set(events)
    for key, row in features.items():
        cov = cover[key]
        event = events[key]
        assert cov['rec_ns'] == row['prov_recognition_ns']
        assert int(cov['pre_ns']) == int(row['prov_birth_second']) * NS - 1
        assert int(event['polarity']) == int(row['polarity']) and event['tape'] == row['tape']
        assert close(event['delay_s'], (int(cov['rec_ns']) - int(cov['pre_ns'])) / NS)
    no_events = {}
    for name in EVENTS:
        expected = sorted(float(row['delay_s']) - int(row[name]) for row in events.values() if int(row[name]) >= 0)
        actual = [r for r in curve_rows if r['day'] == day and r['event'] == name]
        assert len(actual) == len(expected)
        assert all(int(r['order']) == i and close(r['y'], y) for i, (r, y) in enumerate(zip(actual, expected)))
        no_events[name] = len(events) - len(actual)

    with np.load(root / 'instances/x13_life_paths.npz', allow_pickle=False) as arrays:
        assert set(map(str, arrays['row'])) == eligible and len(arrays['row']) == len(eligible)
        assert all(int(pol) == int(features[str(row)]['polarity']) for row, pol in zip(arrays['row'], arrays['pol']))
        assert np.array_equal(arrays['ks'], np.arange(-60, 1261))
        series_names = [name for name in arrays.files if name not in ('ks', 'row', 'pol')]
        series = {name: dict(columns=arrays[name].shape[1], finite=int(np.isfinite(arrays[name]).sum()),
                             missing=int((~np.isfinite(arrays[name])).sum())) for name in series_names}
        assert all(arrays[name].shape[0] == len(eligible) for name in series_names)
        assert np.all(arrays['mid_o'][:, 60] == 0), day

    recorded = index(read_csv(DATA / f'crossday/detector/ledger_recorded_births_{day}.csv'), 'candidate_id')
    saturated = index(read_csv(DATA / f'crossday/detector/ledger_saturated_seconds_{day}.csv'), 'second')
    emulated = {s for s, r in saturated.items() if r['disposition'] == 'emitted'}
    births = {r['birth_second'] for r in recorded.values()}
    matches = births & emulated
    assert len(births) == len(recorded)
    assert sum(r['emulated_as_birth'] == '1' for r in recorded.values()) == len(matches)
    assert all(r['prov_candidate_id'] in recorded for r in features.values())
    missing_recorded = [r['candidate_id'] for r in recorded.values() if r['birth_second'] not in emulated]
    extra_seconds = sorted(map(int, emulated - births))
    assert len(missing_recorded) + len(matches) == len(births)
    assert len(extra_seconds) + len(matches) == len(emulated)

    lean = index(read_csv(root / 'x09_lean_cohort.csv'), 'k')
    lean_checks = {}
    for k in ('-20', '-10', '-1', '0', '1', '10', '20'):
        row = lean[k]
        n = int(row['n'])
        assert n == len(eligible)
        defined = round(n * float(row['share_defined']))
        assert close(defined, n * float(row['share_defined']))
        plus = round(defined * float(row['share_lean_plus1'])) if defined else 0
        minus = round(defined * float(row['share_lean_minus1'])) if defined else 0
        assert close(plus, defined * float(row['share_lean_plus1']))
        assert close(minus, defined * float(row['share_lean_minus1']))
        lean_checks[k] = dict(all_candidates=n, defined=defined, plus_one=plus, minus_one=minus)
    min_birth = min(int(row['prov_birth_second']) for row in features.values())
    max_birth = max(int(row['prov_birth_second']) for row in features.values())
    return dict(date=day, source_candidates=len(cover), covered=len(eligible), omitted=omitted,
                coverage_ordinals=[int(k) for k, row in cover.items() if row['uncovered_reason']],
                actual_recognition_ns_matches=len(eligible),
                first_events_unobserved=no_events, first_event_curves_checked=3,
                first_covered_birth_utc=datetime.fromtimestamp(min_birth, timezone.utc).isoformat(),
                last_covered_birth_utc=datetime.fromtimestamp(max_birth, timezone.utc).isoformat(),
                same_flip_label_present=sum(bool(r['orient']) for r in features.values()),
                array_variables=series, array_boundary_seconds=[-60, 1260],
                detector=dict(recorded=len(births), emulated=len(emulated), exact_birth_matches=len(matches),
                              disposition_counts=Counter(r['disposition'] for r in saturated.values()),
                              missed_recorded_candidate_ids=missing_recorded, extra_emulated_birth_seconds=extra_seconds),
                lean_denominators=lean_checks)


def main():
    curves = read_csv(DATA / 'crossday/x08_first_event_curve_rows.csv')
    days = [day_audit(day, curves) for day in DAYS]
    assert sum(row['covered'] for row in days) * 3 - 1 == len(curves)
    tree = {}
    for group in ('tables', 'crossday', 'figures', 'run'):
        payload = json.loads((ROOT / f'desktop-original-{group}.json').read_bytes())
        assert not payload['truncated']
        tree[group] = [row for row in payload['tree'] if row['type'] == 'blob']
    later = json.loads((ROOT / 'tree-renders.json').read_bytes())
    assert not later['truncated']
    later_files = {e['path']: e for e in later['tree'] if e['type'] == 'blob'}
    for row in days:
        day = row['date']
        original = next(e for e in tree['tables'] if e['path'] == f'dipole/{day}/instances/x13_life_paths.npz')
        base = f'run-42581055248-1/{day}'
        assert later_files[f'{base}/sources/x13_life_paths.npz']['sha'] == original['sha']
        row['later_render_source_array_git_blob'] = original['sha']
        source_path = ROOT / 'lifecycle-reconciliation' / day / 'sources/candidate-inputs.jsonl.gz'
        with gzip.open(source_path, 'rt', encoding='utf-8') as stream:
            candidates = [json.loads(line) for line in stream]
        cover = index(read_csv(DATA / 'tables/dipole' / day / 't6_cohort_coverage.csv'), 'row')
        row['missing_array_candidates'] = [
            dict(input_row=i, candidate_id=candidates[i]['candidate_id'],
                 reason=cover[str(i)]['uncovered_reason'],
                 recognition_receive_ns=candidates[i].get('recognition_receive_ns'))
            for i in row['coverage_ordinals']
        ]
        row['covered_pages_reaching_display_limit'] = sum(
            p['variable'] == 'mid_o' and p['array_row'] is not None and p['last_k'] == 1260
            for f in (ROOT / 'lifecycle-reconciliation' / day).glob('reconciliation-*.json')
            for p in json.loads(f.read_bytes())
        )
    lifecycle_pngs = [e for entries in tree.values() for e in entries
                      if e['path'].endswith('.png') and ('dip-' in e['path'] or '/instances/' in e['path'])]
    assert not lifecycle_pngs
    assert not [e for e in tree['tables'] if '/t1_' in e['path']]
    result = dict(revision=REV, source_handoff=SOURCE + '/HANDOFF_NEXT_SESSION_20261109.md',
                  source_event_study=SOURCE + '/FINDINGS_EVENT_STUDY_20261108.md',
                  scope='Desktop original snapshot before six later CCode commits',
                  original_pngs=sum(e['path'].endswith('.png') for entries in tree.values() for e in entries),
                  original_individual_lifecycle_pngs=len(lifecycle_pngs),
                  original_tier1_tables=0, sorted_first_event_points_checked=len(curves),
                  later_render_run='https://github.com/DavisAI1974/markets-data/actions/runs/42581055248',
                  days=days,
                  open_boundaries=[
                      'Original arrays cover 3,157 of 3,178 candidates. The later render publication has 3,178 pages with 21 explicit missing arrays.',
                      'The first-event curves use second bins and sorted rank. They do not measure the native-resolution warning lead.',
                      'The flow overlay plus/minus one lines divide by candidates with defined flow. The dashed line divides by all candidates.',
                      'Detector emulation missed recorded births and added others. Preserve the mismatch ledgers and separate identities.',
                      'The pre-CCode snapshot has per-day Tier 2 output, including top-400 pair tables. Full pair comparison and cross-day Tier 1 were later work.',
                  ])
    (ROOT / 'DESKTOP_BRANCH_AUDIT.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    for row in days:
        print(row['date'], row['source_candidates'], row['covered'], row['omitted'],
              row['same_flip_label_present'], {k: v for k, v in row['detector'].items() if isinstance(v, int)},
              row['lean_denominators']['-10'])
    print('Verified sorted first-event points:', len(curves))


if __name__ == '__main__':
    main()
