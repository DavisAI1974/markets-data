"""Index immutable branch evidence and project exact published rows into the review."""

import csv
import gzip
import hashlib
import json
from pathlib import Path
import re


DATA = Path(__file__).parent / 'extended-review-data'
TASK = 'tasks/family-research-20261022/'
DESKTOP = TASK + 'claude-pass-3day/'
BRANCHES = (
    ('ccode', 'CCode discovery', '418462afeaf0f14aa8129f6f4d02c3867d772fd0'),
    ('desktop', 'Desktop and CCode shared suite', '3d0b06aa29781d5e39cc3eb45c6d09e174f195a2'),
    ('codex', 'Codex independent research', 'ef89f83b6298983052f94080be64240d7abc0056'),
    ('native', 'Codex Native dipole', '4cf6e85de5de2a9fb479c90b7afb8dd50f1748cb'),
)
DAYS = ('20231002', '20231003', '20231017', '20231018')
OMIT = re.compile(r'(b-delayed-outcomes|cross-study-condition-outcomes)\.parquet')
LIFE_ROOT = 'run-42581055248-1'
LIFE_REV = 'b1123a72115a0fb65cdcde74ba5450e0d40adb68'
LIFE_PATH = TASK + 'claude-lifecycle-renders/'


def read(name):
    return json.loads((DATA / name).read_bytes())


def link(rev, path, repo='Markets'):
    return f'https://github.com/DavisAI1974/{repo}/blob/{rev}/{path}'


def in_scope(label, path):
    relative = path.removeprefix(TASK)
    if label == 'ccode':
        return path.startswith(TASK) and (relative.startswith(('claude-code/', 'claude-pass/'))
               or relative in ('claude-october-discovery-20261108.md', 'october-discovery-log-claude.md', 'data-manifest.json'))
    if label == 'desktop':
        return path.startswith(DESKTOP)
    if label == 'codex':
        return path.startswith('agent-pass/reanalysis/') or (path.startswith(TASK) and relative.startswith(
            ('codex-', 'research-atlas-v2/', 'flow-book-discovery-v1/', 'replay-comparison/',
             'research_', 'october-discovery-log.md', 'october18-prebirth-and-exhaustion-log.md')))
    return path.startswith('agent-pass/') and '/reanalysis/' not in path


def role(path):
    if path.endswith(('.png', '.svg', '.pdf', '.html')) or '/renders/' in path:
        return 'Render or presentation'
    if re.search(r'receipt|manifest|reconcil|verification', path, re.I):
        return 'Receipt or reconciliation'
    if path.endswith(('.csv', '.csv.gz', '.jsonl.gz', '.parquet', '.xlsx', '.npz', '.json.gz')):
        return 'Source rows or research table'
    return 'Report, method or configuration'


def table(headers, rows):
    return dict(headers=headers, rows=rows)


def csv_rows(name, entries):
    path = DATA / 'branch-artifacts' / name
    raw = path.read_bytes()
    e = entries[DESKTOP + name]
    assert len(raw) == e['size'] and hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest() == e['sha']
    with path.open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream)), e


def lifecycle_pins():
    tree = read('tree-renders.json')
    assert not tree['truncated']
    pins = []
    for day, count, omissions in zip(DAYS, (741, 833, 741, 863), (0, 9, 1, 11)):
        paths = {e['path'].rsplit('_', 1)[-1].removesuffix('.png'): e
                 for e in tree['tree'] if e['path'].startswith(f'{LIFE_ROOT}/{day}/{day}_')
                 and e['path'].endswith('.png')}
        root = DATA / 'lifecycle-reconciliation' / day
        with (root / 'sources/coverage.csv').open(encoding='utf-8-sig', newline='') as stream:
            coverage = list(csv.DictReader(stream))
        with gzip.open(root / 'sources/candidate-inputs.jsonl.gz', 'rt', encoding='utf-8') as stream:
            candidates = [json.loads(line) for line in stream]
        assert len(paths) == len(candidates) == len(coverage) == count
        results = {}
        for source in sorted(root.glob('reconciliation-*.json')):
            for result in json.loads(source.read_bytes()):
                assert result['rendered_cells'] == result['finite_cells']
                assert result['source_cells'] == result['finite_cells'] + result['missing_cells']
                pos = result['input_row']
                by_variable = results.setdefault(pos, {})
                variable = result['variable']
                assert variable not in by_variable
                by_variable[variable] = (source.name, result)
        assert set(results) == set(range(count))
        assert sum(bool(c['uncovered_reason']) for c in coverage) == omissions
        for pos, candidate in enumerate(candidates):
            candidate_id = candidate['candidate_id']
            variables = results[pos]
            assert len(variables) == 23
            source, midpoint = variables['mid_o']
            assert all(row['candidate_id'] == candidate_id and row['array_row'] == midpoint['array_row']
                       for _, row in variables.values())
            c = coverage[pos]
            assert int(c['row']) == pos and bool(c['uncovered_reason']) == (midpoint['array_row'] is None)
            recognition = candidate.get('recognition_receive_ns')
            if int(c['rec_ns']) > 0:
                assert int(c['rec_ns']) == recognition
            e = paths[candidate_id]
            birth = candidate.get('birth_second')
            pins.append([day, candidate_id, pos, midpoint['array_row'], str(birth) if birth is not None else None,
                         str(recognition) if recognition is not None else None, candidate.get('recognition_cursor'),
                         c['uncovered_reason'] or 'Covered',
                         midpoint['first_k'], midpoint['last_k'], len(variables),
                         e['sha'], link(LIFE_REV, LIFE_PATH + e['path'], 'markets-data'),
                         link(LIFE_REV, f'{LIFE_PATH}{LIFE_ROOT}/{day}/{source}', 'markets-data')])
    assert len(pins) == 3178
    return pins


def main():
    files = []
    seen = set()
    desktop_entries = {}
    for label, team, rev in BRANCHES:
        tree = read(f'branch-tree-{label}.json')
        assert not tree['truncated']
        for e in tree['tree']:
            p = e['path']
            key = (p, e['sha'])
            if e['type'] != 'blob' or not in_scope(label, p) or OMIT.search(p) or key in seen:
                continue
            seen.add(key)
            if label == 'desktop':
                desktop_entries[p] = e
            use = 'Research reference. Confirm availability before admission.'
            if '/no-prefix-' in p or '/20231018_legacy/' in p:
                use = 'Historical comparison population. Keep separate.'
            files.append([team, role(p), p, e['size'], e['sha'], rev, use, link(rev, p)])
    main_tree = read('tree-main-late.json')
    assert not main_tree['truncated']
    for e in main_tree['tree']:
        p = e['path']
        if e['type'] != 'blob' or not p.startswith(TASK + 'claude-code-'):
            continue
        rev = 'c01caaf4f327e8fdff21e4e8b9c5153aba8604a8'
        files.append(['CCode data', role(p), p, e['size'], e['sha'], rev,
                      'Original evidence. Corrected Tier 1 nanosecond pins take precedence.',
                      link(rev, p, 'markets-data')])
    rev = BRANCHES[1][2]
    families, first_events, reconciliations = [], [], []
    family_cols = ['family_id', 'start_recv_ns', 'cutoff_ns', 'ref_recv_ns', 'input_cursor',
                   'cursor_cap', 'start_utc', 'root.best_bid', 'root.best_ask', 'root.mid', 'root.spread',
                   'root.depth_imbalance_n', 'root.depth_imbalance_full', 'root.bid_depth_full',
                   'root.ask_depth_full', 'root.activity.1.trade_aggressor_imbalance',
                   'root.activity.5.trade_aggressor_imbalance', 'root.activity.60.trade_aggressor_imbalance']
    first_cols = ['row', 'tape', 'polarity', 'delay_s', 'last_k_on_tape', 'k_aggressor_start',
                  'k_touch_size_change', 'k_quote_relocation']
    for day, n_family, n_first in zip(DAYS, (795, 848, 823, 749), (741, 824, 740, 852)):
        name = f'tables/{day}/t1_family_master.csv'
        rows, e = csv_rows(name, desktop_entries)
        assert len(rows) == n_family and all(c in rows[0] for c in family_cols), (day, set(family_cols) - set(rows[0]))
        for ordinal, row in enumerate(rows):
            assert int(row['start_recv_ns']) - 1 == int(row['cutoff_ns'])
            assert int(row['ref_recv_ns']) <= int(row['cutoff_ns'])
            values = [row[c] or None for c in family_cols]
            values[family_cols.index('start_utc')] = 'UTC ' + row['start_utc']
            families.append([day, ordinal, *values, e['sha'], link(rev, DESKTOP + name)])
        name = f'tables/dipole/{day}/x07_first_events.csv'
        rows, e = csv_rows(name, desktop_entries)
        assert len(rows) == n_first and list(rows[0]) == first_cols
        first_events.extend([day, ordinal, *[row[c] or None for c in first_cols], e['sha'],
                             link(rev, DESKTOP + name)] for ordinal, row in enumerate(rows))
    names = ('crossday-chart-reconciliation.csv', 'es_chart_reconciliation.csv', 'es_heatmap_reconciliation.csv',
             'es_lean_reconciliation.csv', 'x08_reconciliation.csv', 't2x_chart_reconciliation.csv')
    names = [f'crossday/{n}' for n in names] + [f'figures/{day}/t5_chart_reconciliation.csv' for day in DAYS]
    for name in names:
        rows, e = csv_rows(name, desktop_entries)
        for ordinal, row in enumerate(rows):
            reconciliations.append([name, ordinal, row.get('day'), row.get('fig') or row.get('figure'),
                                    row.get('panel') or row.get('var') or row.get('event'),
                                    row.get('points_plotted') or row.get('plotted') or row.get('rows_plotted'),
                                    row.get('table_rows') or row.get('rows_in_table') or row.get('rows'),
                                    json.dumps(row, separators=(',', ':')), e['sha'], link(rev, DESKTOP + name)])
    ccode_notes = link(BRANCHES[0][2], TASK + 'claude-october-discovery-20261108.md')
    desktop_events = link(rev, DESKTOP + 'FINDINGS_EVENT_STUDY_20261108.md')
    desktop_cohort = link(rev, DESKTOP + 'FINDINGS_THREE_DAYS_20261108.md')
    receipt = link(rev, DESKTOP + 'CCODE_FINAL_SUITE_RECEIPT.md')
    findings = [
        ['Desktop', 'Birth-aligned flow and midpoint', '741 / 824 / 740 / 852 covered candidates.',
         'The midpoint-share V is anchored at birth. The two flow bursts near -20 s and birth are visible on all four days.',
         'Compare each side of the shape with controls. The birth-axis overlay remains retrospective.', desktop_events],
        ['Desktop', 'First-event and recognition curves', 'Three event types, each day sorted independently.',
         'Same-type cross-day KS distances were 0.031 to 0.122. Oct 3 quote relocation had the longest late-event tail.',
         'Preserve event definition and tape scope. Ordinal rank is separate from time within an event.', desktop_events],
        ['Desktop', 'Recognition cohorts', 'Actual archived recognition, with 0 / 9 / 1 / 11 uncovered source candidates.',
         'Birth-to-recognition in-direction share exceeded the controls; the +1 s and +5 s shares fell below them.',
         'Keep flats, uncovered rows and both clocks. Direction before recognition was already observed.', desktop_cohort],
        ['Desktop', 'Detector emulation', 'Recorded vs emulated births, separately by day.',
         'Exact birth matches 675 / 700 / 658 / 688. Competing midpoint and cluster-release rules remain open.',
         'Keep emulated and archived recognitions separate.',
         link(rev, DESKTOP + 'HANDOFF_NEXT_SESSION_20261109.md')],
        ['Desktop and Codex', 'Authoritative individual lifecycle renders', '3,178 candidate pages across four dates.',
         '3,157 pages have saved arrays. Of 21 pages without arrays, 19 keep their actual recognition clocks and two are finalization-only.',
         'Use run 42581055248 for the final pages. Run 42580756823 is superseded. Whole path availability stays explicit.',
         link(BRANCHES[2][2], 'agent-pass/claude-render-completion/STATUS.md')],
        ['CCode', '375 and 391, size-one cases and order traces', 'Actual tape order IDs and cursors, with recovery and retreat cases.',
         'The first end of a one-lot quote and the later fate of the surviving order are different events.',
         'Keep fills, linked reductions, cancellations and refills separate. Treat psychology as a hypothesis.',
         ccode_notes],
        ['CCode', 'Frozen exhaustion state and runway', 'Four sessions and four time-to-distance scales.',
         'Persistent states took longer at all 16 day-by-scale comparisons. Absolute duration varied with session activity.',
         'Keep birth, first knowable time, archived recognition, structural onset and confirmation separate.',
         ccode_notes],
        ['CCode', 'Actual family starts and refill', '795 / 848 / 823 / 749 families, with strict prior cutoffs.',
         'Full depth skewed bid-heavy. Near depth was more balanced. Refill on the hit side kept its short-run sign across all four dates.',
         'Retain both book layers and null results from the four-arm tests.', receipt],
        ['CCode', 'Tier 2 condition and pair comparisons', '2,669 condition/outcome pairs and 5,166 common full-family triplets.',
         '99 condition/outcome pairs cleared each day’s shifted line. 93 concerned book activity. The nine common pair interactions beyond the line concerned spread.',
         'Preserve shifted references, day-level denominators and distinct legacy and dense Oct 18 populations.', receipt],
        ['CCode', 'Ten cases in five views', 'Lifecycle, fresh vs expiring flow, liquidity, event sequence and continuation.',
         'The archived examples include failed and flat moves. Each view points to the case’s original observations.',
         'Keep all five views linked to the individual case and its clocks.', ccode_notes],
        ['CCode', 'SSOS chart caption check', 'Oct 2 / 3 / 17 / 18, per dated source table.',
         'Section 19.2 reports 7 / 3 / 10 / 10 instances. The caption above fig-ssos.png lists 10 / 10 / 3 / 7 in that date order.',
         'Use the dated source table for counts. Preserve the original image for traceability.',
         link(BRANCHES[0][2], TASK + 'claude-october-discovery-20261108.md#192-the-frozen-ssos-play-and-the-absorption-filter-at-its-horizon')],
        ['Codex', 'Independent full evidence and price feedback', 'Separate source report and case, claims and field ledgers.',
         'The source report distinguishes evidence inventories from completed interpretation.',
         'Keep its unresolved cases open and preserve analyst-specific conclusions.',
         link(BRANCHES[2][2], 'agent-pass/reanalysis/codex/REPORT.md')],
        ['Codex', 'Native dipole shapes and clocks', 'Candidate, matched-control and SAME/FLIP research views.',
         'Some plots use SAME-only and different aggressor definitions from Desktop’s all-covered curves.',
         'Compare by candidate ID, event definition and clock before interpreting agreement.',
         link(BRANCHES[3][2], 'agent-pass/NEXT_CHAT_HANDOFF.md')],
    ]
    tables = {
        'Branch review findings': table(['Analyst', 'Study', 'Population or scope', 'Saved measurement or observation',
                                        'How to read it', 'Original report'], findings),
        'Branch research pins': table(['Research branch', 'Evidence type', 'Git path', 'Bytes', 'Git blob ID',
                                       'Commit', 'Use boundary', 'Immutable Git source'], files),
        'CCode family source rows': table(['Trading date', 'Original row ordinal', *family_cols, 'Git blob ID',
                                          'Immutable source with all columns'], families),
        'Desktop first event rows': table(['Trading date', 'Original row ordinal', *first_cols, 'Git blob ID',
                                           'Immutable original relative-clock source'], first_events),
        'Render row checks': table(['Original reconciliation file', 'Original row ordinal', 'Day', 'Figure',
                                   'Panel or measure', 'Plotted', 'Source rows', 'All original check fields',
                                   'Git blob ID', 'Immutable Git source'], reconciliations),
        'Final lifecycle render pins': table(['Trading date', 'Candidate ID', 'Input row ordinal',
                                             'Saved array row ordinal', 'Original birth epoch second',
                                             'Recognition receive ns', 'Recognition cursor', 'Coverage',
                                             'First displayed second', 'Last displayed second',
                                             'Variables reconciled', 'Render Git blob ID',
                                             'Final render', 'Variable-by-variable reconciliation'], lifecycle_pins()),
    }
    (DATA / 'BRANCH_RESEARCH_TABLES.json').write_text(json.dumps(tables, ensure_ascii=False), encoding='utf-8')
    print({name: len(value['rows']) for name, value in tables.items()})


if __name__ == '__main__':
    main()
