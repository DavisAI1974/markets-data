"""Assemble exact source-backed dipole records and expanded book review tables."""

import collections
import concurrent.futures
import csv
import gzip
import hashlib
import json
from pathlib import Path
import urllib.request

import pyarrow.parquet as pq


ROOT = Path(__file__).parent
OUT = ROOT / 'extended-review-data'
OUT.mkdir(exist_ok=True)
OCT18 = ROOT / 'oct18-original'
MARKETS_REV = 'ef89f83b6298983052f94080be64240d7abc0056'
MARKETS_PATH = 'artifacts/sqlite-triage/20261022/families/trade-lifecycle-targeted-v1'
OCT18_BLOBS = {
    'source-candidate.jsonl.gz': '436195c06ea6303179ec76d7fda362f35b833ac8',
    'source-episode.jsonl.gz': 'def40b6e86a420931a585d02adf5128ce8a93d04',
    'source-detector_coverage.jsonl.gz': 'f19bb9626e54f651e1e294f36867ebccabdab0f3',
    'supporting-dipole-paths.csv.gz': '4a14fb3f382211433cfbeef676e889975c363638',
    'supporting-path-phase-annotations.jsonl.gz': '6bcfa78ee2a5df3f18ffd5a8ab5ddfe6f2e002ed',
    'trade-to-supporting-path-links.csv.gz': '948b6d6d00405cd44409d305059a12282c57ed8c',
    'every-trade-original-second-set.jsonl.gz': 'eef6a8aeb33417c84761b9fef69236d2c05332a9',
}
SECTIONS = ('candidate', 'episode', 'detector_coverage', 'exhaustion')


def load(path):
    return json.loads(path.read_bytes())


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, allow_nan=False, separators=(',', ':')),
                    encoding='utf-8')


def clock(value):
    return None if value is None else 'ns ' + str(value)


def git_url(repo, revision, path):
    return f'https://github.com/{repo}/blob/{revision}/{path}'


def check_oct18(name):
    data = (OCT18 / name).read_bytes()
    assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == OCT18_BLOBS[name]
    return dict(repository='DavisAI1974/Markets', revision=MARKETS_REV, path=f'{MARKETS_PATH}/{name}',
                bytes=len(data), sha256=hashlib.sha256(data).hexdigest(),
                role='Saved October 18 dipole evidence', status='BYTES_VERIFIED')


def native_rows(pub):
    day = pub['day']
    base = ROOT / 'recovered-packets/native' / day
    files = {entry['path']: entry for entry in load(base / 'MANIFEST.json')['files']}
    cache = ROOT / 'native-index-cache' / day
    cache.mkdir(exist_ok=True)

    def fetch(name):
        pin = files[name]
        paths = [ROOT / 'retained-native' / day / name, cache / name]
        path = next((p for p in paths if p.exists()), paths[-1])
        if not path.exists():
            url = f'https://raw.githubusercontent.com/{pub["repository"]}/{pub["revision"]}/{pub["prefix"]}/{name}'
            for attempt in range(3):
                try:
                    with urllib.request.urlopen(url, timeout=120) as response:
                        data = response.read()
                    assert len(data) == pin['bytes'] and hashlib.sha256(data).hexdigest() == pin['sha256'], name
                    path.write_bytes(data)
                    break
                except OSError:
                    if attempt == 2:
                        raise
        data = path.read_bytes()
        assert len(data) == pin['bytes'] and hashlib.sha256(data).hexdigest() == pin['sha256'], name
        return path

    wanted = collections.defaultdict(dict)
    indexes = [n for n in files if n.endswith('.parquet')]
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        for index in pool.map(fetch, indexes):
            rows = pq.read_table(index, filters=[('emitting_section', 'in', SECTIONS)]).to_pylist()
            for row in rows:
                ordinal = row['shard_row']
                assert ordinal not in wanted[row['shard']]
                wanted[row['shard']][ordinal] = row
        result = []
        for path in pool.map(fetch, sorted(wanted)):
            selection = wanted[path.name]
            with gzip.open(path, 'rb') as stream:
                for i, line in enumerate(stream):
                    if i not in selection:
                        continue
                    value = json.loads(line)
                    row = selection[i]
                    assert value['emitting_section'] == row['emitting_section']
                    assert value.get('emitted_at_recv_ns') == row['known_by_ns']
                    result.append((row['source_row'], path.name, i + 1, line, value))
    expected = load(base / 'RECOVERY_RECEIPT.json')['sections']
    assert collections.Counter(row[4]['emitting_section'] for row in result) == {
        section: expected[section] for section in SECTIONS if expected.get(section)
    }
    assert len({r[0] for r in result}) == len(result)
    return sorted(result)


TABLES = {}
COLS = {
    'Full book sources': ['Date', 'Scope', 'Trades', 'Snapshot files', 'Snapshot compressed bytes',
                          'MBO files', 'Git revision', 'Manifest URL', 'Trade phase'],
    'Book packet files': ['Date', 'Kind', 'File', 'Rows', 'Bytes', 'SHA-256', 'Pinned Git file'],
    'Full book examples': ['Date', 'Trade ordinal', 'Input cursor', 'At-trade receive ns', 'Bid levels', 'Ask levels',
                           'Bid orders', 'Ask orders', 'Bid size', 'Ask size', 'Best bid', 'Best ask', 'Source'],
    'FIFO order examples': ['Date', 'Trade ordinal', 'L041 | Side', 'L041 | Raw price', 'L041 | FIFO rank',
                            'L041 | Order ID exact text', 'L041 | Size', 'L041 | Volume ahead',
                            'L042 | Priority receive ns', 'L042 | Age seconds', 'L041 | Priority sequence'],
    'Dipole coverage': ['Date', 'Original candidate rows', 'Original episode rows', 'Episodes with path',
                        'Stored stage rows', 'Detector records', 'Exhaustion records',
                        'Second-set trade rows', 'Source scope', 'Use boundary'],
    'Dipole candidates': ['Date', 'Candidate ID', 'Event second', 'Available second', 'Emission receive ns',
                          'Input cursor', 'Polarity', 'Magnitude', 'Baseline', 'Threshold', 'Prominence',
                          'Detection lag sec', 'Continuity segment', 'Source file', 'Source line'],
    'Dipole episodes': ['Date', 'Candidate ID', 'Emission kind', 'Emission receive ns', 'Input cursor',
                        'Birth receive ns', 'Recognition receive ns', 'Orientation', 'Terminal phase',
                        'Stage count', 'Sign reversal count', 'Price coupling raw', 'Path state',
                        'Source file', 'Source line'],
    'Dipole stage series': ['Date', 'Candidate ID', 'Emission receive ns', 'First stage', 'Stages in row',
                            'Stage receive ns array (exact)', 'Signed flow array', 'Direction array',
                            'Magnitude array', 'Raw price array', 'Bid depth array', 'Ask depth array',
                            'Bid orders array', 'Ask orders array', 'Normalized imbalance array',
                            'Source file', 'Source line'],
    'Dipole detector checks': ['Date', 'Section', 'Emission receive ns', 'Input cursor', 'Continuity segment',
                               'Exact original JSON', 'Source file', 'Source line'],
    'Dipole source files': ['Date', 'Data', 'Rows', 'Repository', 'Commit', 'Path', 'SHA-256', 'Source scope'],
    'Retrieval status': ['Date', 'Layer or data family', 'Status', 'What is available', 'Remaining gap'],
}
for name, headers in COLS.items():
    TABLES[name] = dict(headers=headers, rows=[])


def add(name, *values):
    assert len(values) == len(COLS[name]), name
    TABLES[name]['rows'].append(list(values))


def emit_record(day, value, section, source_file, source_line, emission=None, cursor=None):
    details = value.get('frankie_emission') or {}
    emission = value.get('emitted_at_recv_ns') if emission is None else emission
    cursor = details.get('input_cursor') if cursor is None else cursor
    if section == 'candidate':
        add('Dipole candidates', day, value.get('candidate_id'), value.get('event_second'),
            value.get('available_second'), clock(emission), cursor, value.get('polarity'), value.get('magnitude'),
            value.get('baseline'), value.get('threshold'), value.get('prominence'),
            value.get('detection_lag_seconds'), value.get('continuity_segment'), source_file, source_line)
        return 0
    if section != 'episode':
        raw = json.dumps(value, ensure_ascii=False, separators=(',', ':'))
        add('Dipole detector checks', day, section, clock(emission), cursor, value.get('continuity_segment'),
            raw if len(raw) <= 30000 else 'Full record in pinned source', source_file, source_line)
        return 0
    dipole = value.get('dipole') or {}
    stages = dipole.get('stages') or []
    recognition = value.get('recognition') or {}
    candidate = value.get('candidate') or {}
    add('Dipole episodes', day, value.get('candidate_id'), value.get('emitted_on'), clock(emission), cursor,
        clock(value.get('birth_recv_ns', recognition.get('birth_recv_ns'))),
        clock(value.get('recognized_recv_ns', recognition.get('recognized_recv_ns'))),
        value.get('orientation', dipole.get('orientation')), value.get('terminal_phase'),
        value.get('stage_count', dipole.get('stage_count')), dipole.get('sign_reversal_count'),
        dipole.get('price_coupling_raw'),
        'Path stored' if stages else ('Path withheld' if value.get('dipole_path_withheld') else 'Recognition or summary row'),
        source_file, source_line)
    stage_keys = ('recv_ns', 'signed_flow', 'direction', 'magnitude', 'price_raw', 'bid_depth', 'ask_depth',
                  'bid_order_count', 'ask_order_count', 'normalized_imbalance')
    for start in range(0, len(stages), 40):
        batch = stages[start:start + 40]
        series = [json.dumps([s.get(key) for s in batch], separators=(',', ':')) for key in stage_keys]
        assert max(map(len, series)) <= 30000
        add('Dipole stage series', day, value.get('candidate_id', candidate.get('candidate_id')), clock(emission),
            batch[0].get('stage_index'), len(batch), *series, source_file, source_line)
    return len(stages)


def main():
    pins = [check_oct18(name) for name in OCT18_BLOBS]
    for pub in load(ROOT / 'recovered-packets/PUBLICATIONS.json'):
        day, revision, prefix, repo = (pub[key] for key in ('day', 'revision', 'prefix', 'repository'))
        base = ROOT / 'recovered-packets/book' / day
        receipt = load(base / 'RECOVERY_RECEIPT.json')
        files = load(base / 'MANIFEST.json')['files']
        books = [entry for entry in files if entry['path'].startswith('trade-book-fifo-')]
        mbo = [entry for entry in files if entry['path'].startswith('native-messages-')]
        assert sum(e['rows'] for e in books) == receipt['recovered_trades']
        assert sum(e['rows'] for e in mbo) == receipt['raw_messages_including_opening_warmup']
        add('Full book sources', day, receipt['scope'], receipt['recovered_trades'], len(books),
            sum(e['bytes'] for e in books), len(mbo), revision, git_url(repo, revision, prefix + '/MANIFEST.json'),
            'Snapshot at the exact trade input. MBO includes the opening warmup where available.')
        for kind, entries in [('Full book and FIFO', books), ('Raw MBO', mbo)]:
            for e in entries:
                add('Book packet files', day, kind, e['path'], e['rows'], e['bytes'], e['sha256'],
                    git_url(repo, revision, prefix + '/' + e['path']))
        for sample in load(base / 'REVIEW_SAMPLES.json'):
            b = sample['book_full']
            add('Full book examples', day, sample['trade_ordinal'], sample['original_trade']['trade_input_cursor'],
                clock(sample['known_by_ns']), len(b['bid_levels_full']), len(b['ask_levels_full']),
                b['bid_order_count_full'], b['ask_order_count_full'], b['bid_depth_full'], b['ask_depth_full'],
                b['best_bid'], b['best_ask'], git_url(repo, revision, prefix + '/REVIEW_SAMPLES.json'))
            for side in ('bid', 'ask'):
                for level in b[side + '_levels_full']:
                    queue = level['fifo_queue']
                    assert sum(q['size'] for q in queue) == level['size']
                    ahead = 0
                    for rank, q in enumerate(queue, 1):
                        assert q['volume_ahead'] == ahead
                        add('FIFO order examples', day, sample['trade_ordinal'], side, str(level['price_raw']), rank,
                            'id ' + str(q['order_id']), q['size'], q['volume_ahead'], clock(q['priority_recv_ns']),
                            q['priority_age_s'], q['priority_sequence'])
                        ahead += q['size']

    source_stats = {}
    for pub in load(ROOT / 'recovered-packets/NATIVE_PUBLICATIONS.json'):
        day = pub['day']
        rows = native_rows(pub)
        by_section = collections.Counter()
        stage_count = path_count = 0
        path = OUT / f'native-dipole-{day}.jsonl.gz'
        with gzip.GzipFile(filename=str(path), mode='wb', compresslevel=3, mtime=0) as target:
            for ordinal, shard, line_number, raw, value in rows:
                target.write(raw)
                section = value['emitting_section']
                by_section[section] += 1
                stages = emit_record(day, value, section, pub['prefix'] + '/' + shard, line_number)
                stage_count += stages
                path_count += stages > 0
        manifest_pin = next(e for e in pub['files'] if e['path'] == 'MANIFEST.json')
        add('Dipole source files', day, 'Original Native candidates, episodes and detector/exhaustion rows',
            len(rows), pub['repository'], pub['revision'], pub['prefix'] + '/MANIFEST.json',
            manifest_pin['sha256'], 'Full retained Native ledger')
        add('Dipole coverage', day, by_section['candidate'], by_section['episode'], path_count, stage_count,
            by_section['detector_coverage'], by_section['exhaustion'], 0,
            'Complete saved Native ledger for the archived scope',
            'Episode/path contents use their own emission clock. Second-set replay remains separate.')
        source_stats[day] = dict(sections=by_section, stored_paths=path_count, stage_rows=stage_count,
                                 extract_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
        print(day, source_stats[day], flush=True)

    oct_counts = collections.Counter()
    stage_count = path_count = 0
    for section in ('candidate', 'episode', 'detector_coverage'):
        name = f'source-{section}.jsonl.gz'
        with gzip.open(OCT18 / name, 'rt', encoding='utf-8') as stream:
            for i, line in enumerate(stream, 1):
                row = json.loads(line)
                value = row['original_record']
                assert value['emitting_section'] == section
                stages = emit_record('20231018', value, section, name, i, row['known_by_ns'], row['input_cursor'])
                path_count += stages > 0
                stage_count += stages
                oct_counts[section] += 1
        pin = next(p for p in pins if p['path'].endswith('/' + name))
        add('Dipole source files', '20231018', section, oct_counts[section], pin['repository'], pin['revision'],
            pin['path'], pin['sha256'], 'Retained projection')

    layer_names = [(row['column'], row['layer_id']) for row in load(ROOT / 'sources/LAYERS.json')
                   if row['group'] == 'second_set_components']
    phases = ('last_completed_group_before_trade', 'at_emission_group_close', 'at_trade_input', 'previous_input')
    sample_ids = {s['trade_ordinal'] for s in load(ROOT / 'filled-review/REVIEW_SAMPLES.json') if s['day'] == '20231018'}
    second_values = []
    coverage = {phase: {name: collections.Counter() for _, name in layer_names} for phase in phases}
    with gzip.open(OCT18 / 'every-trade-original-second-set.jsonl.gz', 'rt', encoding='utf-8') as stream:
        for ordinal, line in enumerate(stream):
            row = json.loads(line)
            assert row['trade_ordinal'] == ordinal
            for phase in phases:
                record = row[phase]
                numbers = record.get('numbers', {})
                for _, name in layer_names:
                    v = numbers.get(name)
                    coverage[phase][name][v['state'] if v else record['disposition']] += 1
                if ordinal in sample_ids:
                    second_values.append(['20231018', ordinal, phase, record.get('clocks', {}).get('input_cursor'),
                                          clock(record.get('clocks', {}).get('known_by_ns')),
                                          *[numbers[name]['raw_float64'] if name in numbers and numbers[name]['state'] == 'PRESENT'
                                            else numbers[name]['state'] if name in numbers else record['disposition']
                                            for _, name in layer_names]])
    assert ordinal + 1 == 30739
    TABLES['Second set examples'] = dict(headers=['Date', 'Trade ordinal', 'Source phase', 'Input cursor',
                                                'Known-by ns', *[label for label, _ in layer_names]], rows=second_values)
    TABLES['Second set states'] = dict(
        headers=['Date', 'Source phase', 'Layer', 'Present', 'Missing', 'Invalid', 'Ablated', 'Other source state'],
        rows=[['20231018', phase, label, counts['PRESENT'], counts['MISSING'], counts['INVALID'], counts['ABLATED'],
               ', '.join(f'{state}: {n}' for state, n in counts.items()
                         if state not in ('PRESENT', 'MISSING', 'INVALID', 'ABLATED')) or None]
              for phase in phases for label, name in layer_names for counts in [coverage[phase][name]]])
    for name in OCT18_BLOBS:
        if not name.startswith('source-'):
            pin = next(p for p in pins if p['path'].endswith('/' + name))
            with gzip.open(OCT18 / name, 'rb') as stream:
                count = sum(1 for _ in stream) - name.endswith('.csv.gz')
            add('Dipole source files', '20231018', name, count, pin['repository'], pin['revision'], pin['path'],
                pin['sha256'], 'Original retained evidence. Preserve its source phase and timing.')
    add('Dipole coverage', '20231018', oct_counts['candidate'], oct_counts['episode'], path_count, stage_count,
        oct_counts['detector_coverage'], None, 30739, 'Original retained projection and full trade second-set join',
        'Candidate file and episode file have different coverage. Missing states remain explicit.')
    source_stats['20231018'] = dict(sections=oct_counts, stored_paths=path_count, stage_rows=stage_count,
                                    second_set_trades=30739)

    for day in ('20231002', '20231003', '20231017', '20231018'):
        add('Retrieval status', day, 'MBO / book / FIFO', 'Verified',
            'All trade snapshots for the archived scope, full shard index, 3 expanded FIFO examples',
            'October 2 and 17 retain the original partial-session scope.' if day in ('20231002', '20231017') else None)
        add('Retrieval status', day, 'Saved dipole paths and detections', 'Recovered',
            'Candidate and episode rows, selected stage fields for every stored stage, exact source references',
            'Candidate and episode coverage are separate. Path emission time gates use.')
        add('Retrieval status', day, '19 calculated second-set components',
            'Original values available' if day == '20231018' else 'Replay in progress' if day == '20231002' else 'Open',
            '30,739 trades with four source phases and exact states' if day == '20231018' else
            'Segmented GitHub replay with verified checkpoint handoff' if day == '20231002' else 'Pinned replay inputs',
            None if day == '20231018' else 'Complete result and coverage verification pending')
    for args in [
        ('All four', 'Remaining named derived inputs L058–L071', 'Partial',
         'Raw MBO, books and Native rows support some fields', 'Full per-layer joins and semantic verification remain open'),
        ('All four', 'External input timing and vintages', 'Partial',
         'Recovered forecast, weather and external data values', 'First publication, vintages and some curve definitions remain held'),
        ('20231018', 'Full Native flow stream', 'Partial',
         '30,739 joins to original retained flow projection', 'Complete stream outside retained projection remains unverified'),
        ('All four', 'Sealed evaluation and runtime outputs', 'Separate',
         'Registry and some source definitions', 'Actual runtime outputs require their own authorized execution'),
    ]:
        add('Retrieval status', *args)
    write_json(OUT / 'WORKBOOK_TABLES.json', TABLES)
    write_json(OUT / 'DIPOLE_SOURCE_PINS.json', pins)
    write_json(OUT / 'DIPOLE_SUMMARY.json', source_stats)
    print(json.dumps(dict(source_stats=source_stats, tables={k: len(v['rows']) for k, v in TABLES.items()})), flush=True)


if __name__ == '__main__':
    main()
