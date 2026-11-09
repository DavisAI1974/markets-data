"""Index all saved workflow output files and load their original review tables."""

from collections import Counter, defaultdict
import json
from pathlib import Path
import re

import pyarrow.parquet as pq


ROOT = Path(__file__).parent / 'extended-review-data'
CACHE = ROOT / 'workflow-cache'
REV = '2fe4aaffe596e01167af24a979bf07a69f40771f'
PREFIX = 'tasks/family-research-20261022'
REPO = 'DavisAI1974/markets-data'
TIMING_REV = 'c493ae7388212fa3ce029c505d4a052d85cf5799'
DAYS = ('20231002', '20231003', '20231017', '20231018')
DIRS = {
    'dipole': ('native-dipole', 'Native dipole research'),
    'combined': ('combined-events', 'Four-date combined event studies'),
    'lifecycle': ('whole-lifecycles', 'Whole lifecycle audit'),
    'renders': ('claude-lifecycle-renders', 'Claude lifecycle renders'),
    'links': ('lifecycle-data-links', 'Lifecycle clock and row links'),
    'review': ('codex-independent-review', 'Codex independent review'),
    'analysis': ('codex-independent-analysis', 'Codex independent analysis'),
    'renderbooks': ('dipole-render-books', 'Audited dipole render books'),
    'informational': ('user-informational-renders', 'Informational research renders'),
    'replication': ('family-replication', 'Family replication'),
    'extensions': ('four-day-extensions', 'Four-day extensions'),
    'shared': ('shared-reanalysis-inputs', 'Shared reanalysis inputs'),
}


def load(p):
    return json.loads(p.read_bytes())


def exact(v, key=''):
    if isinstance(v, int) and not isinstance(v, bool) and (key.endswith('_ns') or abs(v) >= 10**15):
        return str(v)
    if isinstance(v, (dict, list)):
        return json.dumps(v, separators=(',', ':'), ensure_ascii=False, default=str, allow_nan=False)
    return v


def url(path):
    return f'https://github.com/{REPO}/blob/{REV}/{PREFIX}/{path}'


def parquet_table(name, path_pattern, label):
    parts = []
    columns = []
    for day in DAYS:
        path = path_pattern.format(day=day)
        table = pq.read_table(CACHE / path)
        columns.extend(k for k in table.column_names if k not in columns)
        parts.append((day, path, table))
    rows = [[day, label, *[exact(row.get(k), k) for k in columns], url(path)]
            for day, path, table in parts for row in table.to_pylist()]
    return dict(headers=['Trading date', 'Role', *columns, 'Immutable Git file'], rows=rows)


def flatten(row, prefix=''):
    for key, value in row.items():
        field = prefix + key
        if isinstance(value, dict):
            yield from flatten(value, field + '.')
        else:
            yield field, exact(value, key)


def main():
    tables = {}
    index = []
    render_index = []
    research = []
    for key, (directory, family) in DIRS.items():
        tree_path = ROOT / f'tree-{key}.json'
        if not tree_path.exists():
            continue
        tree = load(tree_path)
        assert not tree['truncated'], key
        blobs = [x for x in tree['tree'] if x['type'] == 'blob']
        for e in blobs:
            path = directory + '/' + e['path']
            day = next((d for d in DAYS if d in e['path']), None)
            role = ('Look-ahead outcomes. Keep separate from earlier inputs.' if re.search(
                r'outcomes|next-group-arrival|quote-ending|path-points|whole-lifecycles', e['path']) else
                'Stored research output. Preserve its original clock role.')
            row = [family, day, path, e['size'], e['sha'], REV, role, url(path)]
            (render_index if key == 'renders' else index).append(row)
        research.append([family, len(blobs), sum(x['size'] for x in blobs), REV,
                         f'https://github.com/{REPO}/tree/{REV}/{PREFIX}/{directory}'])
    headers = ['Research or workflow', 'Trading date', 'Git file', 'Bytes', 'Git blob ID',
               'Commit', 'Use boundary', 'Immutable URL']
    tables['Workflow and research files'] = dict(headers=headers, rows=index)
    tables['Dipole render files'] = dict(headers=headers, rows=render_index)
    tables['Research sets'] = dict(headers=['Research set', 'Files', 'Bytes', 'Git revision', 'Source folder'],
                                  rows=research)
    combined = 'combined-events/run-42571551209-1/events-{day}/'
    lifecycle = 'whole-lifecycles/run-42573465249-1/audit-{day}/'
    tables['Generated dipole clocks'] = parquet_table(
        'Generated dipole clocks', combined + 'a-dipole-clocks.parquet',
        'Birth, live recognition and lifetime endpoint clocks retained separately')
    tables['Whole lifecycle parents'] = parquet_table(
        'Whole lifecycle parents', lifecycle + 'whole-lifecycles.parquet',
        'Retrospective path and matched controls; use the stated recognition clock for availability')
    tables['Lifecycle component windows'] = parquet_table(
        'Lifecycle component windows', lifecycle + 'component-windows.parquet',
        'Stored windows may extend before or after a lifecycle')
    tables['Delayed outcome conditions'] = parquet_table(
        'Delayed outcome conditions', combined + 'cross-study-condition-outcomes.parquet',
        'Retrospective grouped outcomes')

    workflow_summary = []
    look_ahead = []
    for day in DAYS:
        for name, pattern in [('Four-date combined event studies', combined + 'analysis-summary.json'),
                              ('Whole lifecycle audit', lifecycle + 'audit.json')]:
            path = pattern.format(day=day)
            summary = load(CACHE / path)
            workflow_summary.extend([day, name, key, value, url(path)] for key, value in flatten(summary))
        path = (combined + 'b-delayed-outcomes.parquet').format(day=day)
        counts = Counter()
        mid = defaultdict(Counter)
        spread = defaultdict(Counter)
        data = pq.ParquetFile(CACHE / path)
        columns = ['event_type', 'side', 'horizon_s', 'disposition',
                   'signed_midpoint_change_twice_raw', 'spread_crossing_raw']
        for batch in data.iter_batches(columns=columns):
            for row in batch.to_pylist():
                key = tuple(row[name] for name in columns[:4])
                counts[key] += 1
                for histogram, field in ((mid, columns[4]), (spread, columns[5])):
                    value = row[field]
                    bucket = 'missing' if value is None else 'positive' if value > 0 else 'negative' if value < 0 else 'flat'
                    histogram[key][bucket] += 1
        assert sum(counts.values()) == data.metadata.num_rows
        for key, count in sorted(counts.items(), key=lambda x: tuple(map(str, x[0]))):
            look_ahead.append([day, *key, count,
                               *[histogram[key][bucket] for histogram in (mid, spread)
                                 for bucket in ('positive', 'flat', 'negative', 'missing')],
                               url(path)])
    tables['Workflow findings'] = dict(headers=['Trading date', 'Workflow', 'Original metric',
                                               'Original value', 'Immutable Git file'], rows=workflow_summary)
    tables['Delayed outcomes'] = dict(
        headers=['Trading date', 'Signal type', 'Side', 'Horizon sec', 'Disposition', 'Source rows',
                 'Mid positive', 'Mid flat', 'Mid negative', 'Mid missing',
                 'Spread positive', 'Spread flat', 'Spread negative', 'Spread missing', 'All exact outcome rows'],
        rows=look_ahead)
    timing_base = f'https://github.com/DavisAI1974/Markets/blob/{TIMING_REV}/'
    tables['Dipole lead timing'] = dict(
        headers=['Evidence', 'Market', 'Measured quantity', 'Value or definition', 'Source status',
                 'Source', 'Runtime role'],
        rows=[
            ['Later subsecond calculation', 'NYMEX natural gas', 'Reported warning horizon',
             'Approximately 0.5 seconds, shorter than the Bitcoin lead',
             'User identified the earlier result. Exact saved calculation and per-event clock rows still open.',
             'Current research handoff', 'Timing and execution context. Keep the exact measured value open.'],
            ['S36/S37 timing', 'Bitcoin', 'Entry distance from historical turn',
             'About 5–6 bps using 1-second timing and 9–11 bps using minute timing',
             'Historical timing result with a true-pivot filter in the timing-only experiment',
             timing_base + '_info_dipole_timing_test_results.json', 'Historical reference with separate timing units.'],
            ['S90 exhaustion canary', 'NYMEX natural gas', 'One-second-bin reversal rate contrast',
             '0.410 oppose plus exhaust versus 0.382 trend plus strengthen. Difference 2.7 percentage points as reported.',
             'One July 17, 2025 trend day. Coarse historical measurement.',
             timing_base + 'SESSION_HANDOFF_2026-07-13_S90.md', 'Historical context for the native-resolution lead.'],
            ['S94 brain entry', 'Bitcoin and NYMEX natural gas', 'Subsecond reversal/exhaustion',
             'Dipole exhaustion filters a maturing leg. Fine-resolution price reversal times the entry.',
             'Historical brain hypothesis carried forward',
             timing_base + 'SESSION_HANDOFF_2026-07-14_S94.md', 'Intraday turn timing.'],
            ['NG dipole crosswalk', 'NYMEX natural gas', 'Prior flow authority weakens near a turn',
             'Separate exhaustion/collapse from a sign crossing. The family runway is a separate quantity.',
             'Frozen historical interpretation',
             timing_base + 'research/FRANKIE_NG_DIPOLE_BRAIN_CROSSWALK_20260816.md', 'Context for the lead calculation.'],
            ['Delayed-outcome study', 'Four archived NG dates', 'Retrospective 1/5/30 second outcomes',
             'Future quote outcomes grouped by signal, side and horizon',
             'Original records and derived coverage preserved',
             'Delayed outcomes and Delayed outcome conditions sheets', 'Research outcomes with later availability.'],
        ])
    (ROOT / 'WORKFLOW_TABLES.json').write_text(json.dumps(tables, separators=(',', ':'), ensure_ascii=False,
                                                         allow_nan=False), encoding='utf-8')
    print(json.dumps({key: len(table['rows']) for key, table in tables.items()}), flush=True)


if __name__ == '__main__':
    main()
