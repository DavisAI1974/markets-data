"""Index the Desktop NG render sources and the separate algebraic research."""

import json
from pathlib import Path


DATA = Path(__file__).parent / 'extended-review-data'
DESKTOP = '3d0b06aa29781d5e39cc3eb45c6d09e174f195a2'
ALGEBRA = 'b9761bcb549d4cf11e7d738e322d55215f98a3bc'
CRYPTO = '1f96b77702e968fcd14bd9d9d3da2f3d3d49f5bb'
PREFIX = 'tasks/family-research-20261022/claude-pass-3day'
GIT = 'https://github.com/DavisAI1974/Markets/blob'
HOLD = 'Review evidence only. Reverify before use in calculations.'


def load(name):
    return json.loads((DATA / name).read_bytes())


def main():
    entries = [e for e in load('desktop-root.json') if e['type'] == 'file']
    for group in ('crossday', 'figures', 'tables'):
        tree = load(f'desktop-{group}.json')
        assert not tree['truncated']
        entries.extend(dict(e, path=f'{PREFIX}/{group}/{e["path"]}')
                       for e in tree['tree'] if e['type'] == 'blob')
    render_rows = []
    for e in entries:
        path = e['path']
        kind = ('Render' if path.endswith(('.png', '.svg')) else
                'Chart reconciliation' if 'reconcil' in path else
                'Source table or workbook' if path.endswith(('.csv', '.parquet', '.xlsx', '.gz')) else
                'Method or handoff')
        render_rows.append([kind, path.removeprefix(PREFIX + '/'), e['size'], e['sha'], DESKTOP,
                            HOLD, f'{GIT}/{DESKTOP}/{path}'])
    priority = ('es-lean-and-price-around-birth.png', 'es-first-event-curves.png',
                'es-share-moved-birth-axis.png', 'es-aggressor-lots-birth-axis.png',
                'es-heatmap-oriented-mid-paths.png', 'es_lean_reconciliation.csv')
    assert all(any(row[1].endswith(name) for row in render_rows) for name in priority)
    order = {f'crossday/{name}': i for i, name in enumerate(priority)}
    render_rows.sort(key=lambda row: (order.get(row[1], len(order)), row[1]))
    pins = load('algebraic-pins.json')
    assert len(pins) == 6 and all(f'/{ALGEBRA}/' in p['html_url'] for p in pins)
    notes = (
        ('Codex NG audit', 'Research and admission status for NG.'),
        ('Independent equation review', 'Centroid Ha/Hb, discrete-entropy coupling and Level 2 are identified separately.'),
        ('Five-step coupling and Level 2', 'Directional donor tests and pair balance. Keep rank and denominator holds.'),
        ('Quadratic and null controls', 'Test Ha² = a + b(HaHb) + c(HaHb)² against the constant-donor null and held-out controls.'),
        ('Standalone verification', 'Offline and synthetic checks. Four-day NG measurements remain open.'),
        ('Centroid projection source', 'Projects 128-dimensional coefficients onto the win and loss centroids for Ha and Hb.'),
    )
    algebra_rows = [[label, definition, p['path'], p['sha'], ALGEBRA, HOLD, p['html_url']]
                    for (label, definition), p in zip(notes, pins)]
    tables = {
        'Desktop NG renders': {
            'headers': ['Evidence type', 'File', 'Bytes', 'Git blob ID', 'Commit', 'Use boundary', 'Immutable URL'],
            'rows': render_rows,
        },
        'Algebraic dipole research': {
            'headers': ['Research item', 'Definition or finding', 'Git file', 'Git blob ID', 'Commit',
                        'Use boundary', 'Immutable URL'],
            'rows': algebra_rows,
        },
    }
    result = dict(
        tables=tables,
        scope={
            'archived_dipole_stage_rows': 193124,
            'archived_dipole_stage_reanalysis_admitted': False,
            'dipole_dive_reanalysis_admitted': False,
            'dipole_dive_source': f'{GIT}/{CRYPTO}/_dipole_price_overlay.py',
            'dipole_dive_original_definition': 'Time derivative of oriented rolling signed flow lean.',
            'ng_dive_reference': f'{GIT}/{DESKTOP}/{PREFIX}/crossday/es-lean-and-price-around-birth.png',
            'ng_dive_rule': 'Verify or recalculate from NG observations using causal clocks before admission.',
            'dipole_lead_timing_rows_selected': [2, 4, 5, 6],
            'dipole_lead_timing_row_2_admitted': False,
            'dipole_lead_timing_row_2_exact_ns': None,
            'dipole_lead_timing_rows_4_to_6_use': 'Research context.',
            'algebraic_dipole_four_day_measurements_admitted': False,
        },
    )
    (DATA / 'ADDITIONAL_DIP_REVIEW.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n',
                                                   encoding='utf-8')
    print({name: len(table['rows']) for name, table in tables.items()})


if __name__ == '__main__':
    main()
