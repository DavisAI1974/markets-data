"""Lossless selected-case audit. No strategy execution or hypothesis selection.

Run: python audit.py --source <dipole-experiment-dir> --prior <review-dir>
                  --catalog <published_source_catalog.json> --objects <objects-dir>
Outputs are written beside this script. Python standard library only.
"""
import argparse
import collections
import csv
import gzip
import hashlib
import json
import math
from pathlib import Path

DAYS = ['20231002', '20231003', '20231017', '20231018']
OUT = Path(__file__).resolve().parent


def clock_int(value):
    if value is None or value == '':
        return None
    if isinstance(value, (float, bool)):
        raise ValueError('Clock must be exact integer or decimal string')
    return int(value)


def available(known_by, decision):
    a, b = clock_int(known_by), clock_int(decision)
    return None if a is None or b is None else a <= b


def decode(value):
    if isinstance(value, str) and value[:1] in '{[':
        return json.loads(value)
    return value


def measured_leaves(value, path=''):
    """Inventory only; availability is a separate question, never inferred here."""
    value = decode(value)
    if isinstance(value, dict):
        if 'state_code' in value:
            if value.get('state') == 'PRESENT' and value['state_code'] == 0:
                yield (path + '.raw_float64').lstrip('.'), value['raw_float64']
            return
        if 'published_ns' in value and value.get('state') != 0:
            return
        for key, child in value.items():
            if key in {'state', 'status', 'reason', 'scope', 'original_index', 'raw_float64_hex'}:
                continue
            if any(part in key for part in ('_ns', 'cursor', 'ordinal', 'sequence', 'order_id',
                                           'instrument_id', 'source_', 'segment', 'group_')):
                continue
            yield from measured_leaves(child, (path + '.' + key).lstrip('.'))
    elif isinstance(value, list):
        for i, child in enumerate(value):
            yield from measured_leaves(child, f'{path}[{i}]')
    elif isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value):
        yield path, value


def all_leaves(value, path=''):
    value = decode(value)
    if isinstance(value, dict):
        for key, child in value.items():
            yield from all_leaves(child, (path + '.' + key).lstrip('.'))
    elif isinstance(value, list):
        for i, child in enumerate(value):
            yield from all_leaves(child, f'{path}[{i}]')
    else:
        yield path, value


def dump(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + '\n', encoding='utf8')


def write_csv(name, rows):
    with (OUT / name).open('w', newline='', encoding='utf8') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def preserve(src, target):
    raw = src.read_bytes()
    dest = OUT / target
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(gzip.compress(raw, mtime=0))
    assert gzip.decompress(dest.read_bytes()) == raw
    return {'path': target, 'original_filename': src.name, 'bytes': len(raw),
            'sha256_uncompressed': sha(raw), 'sha256_compressed': sha(dest.read_bytes())}


def clock_contract(field):
    code = field.split(' | ')[0]
    if ' | ' not in field:
        return 'trade metadata; event_ns != receive_ns != known_by_ns; cursor/ordinal identifies source, not signal'
    if code.startswith('S'):
        return 'state= PRESENT AND state_code=0 required; emission-close joins to L029.during.known_by_ns; last-completed joins to L029.before.known_by_ns; previous_input availability unproven; at_trade_input cannot borrow emission-close'
    if code.startswith('X'):
        return 'original.state=0 and original.published_ns <= values.asof_receive_ns; declared publication is not verified delivery; retain event_time_ns separately'
    if code in ['L072', 'L073', 'L074', 'L075', 'L029']:
        return 'clock/provenance, not predictor; exact integer nanoseconds; complete-group close controls current values'
    return 'when before/during operands exist use L029.before.known_by_ns / values.during_known_by_ns; static/source/missing layers need their own admission proof; never assign trade receive clock by default'


def run(args):
    package = json.loads((args.source / 'package.json').read_text(encoding='utf8'))
    fields = package['all_layer_fields']
    assert len(fields) == len(set(fields)) == 141
    manifest = [preserve(args.source / 'package.json', 'raw/package.json.gz')]
    for name in ['HANDOFF.md', 'PROVISIONAL_STRATEGIES_20261113.json', 'inventory.json',
                 'case_results.json', 'individual_series.json', 'trade_type_review.json', 'review_by_trade_type.py']:
        manifest.append(preserve(args.prior / name, 'prior/' + name + '.gz'))
    field_case, case_rows, tick_clocks, member_rows, intervals = [], [], [], [], []
    field_status = {field: collections.Counter() for field in fields}
    field_days = {field: {} for field in fields}
    full_value_digests = {field: hashlib.sha256() for field in fields}
    errors = []
    s_states = collections.Counter()
    external_states = collections.Counter()
    for day in DAYS:
        for category in range(8):
            filename = f'{day}-{category}.json'
            record = preserve(args.source / filename, 'raw/' + filename + '.gz')
            manifest.append(record)
            d = json.loads((args.source / filename).read_text(encoding='utf8'))
            headers, rows = d['headers'], d['rows']
            index = {h: i for i, h in enumerate(headers)}
            assert len(headers) == 167 and all(f in index for f in fields)
            ords = [int(r[index['trade_ordinal']]) for r in rows]
            assert ords == list(range(ords[0], ords[-1] + 1))
            assert len(rows) == d['tick_count']
            times = [clock_int(r[index['receive_ns']]) for r in rows]
            assert times == sorted(times)
            leg = [i for i, r in enumerate(rows) if r[index['Inside selected price leg']]]
            assert leg == list(range(leg[0], leg[-1] + 1))
            case_id = f'{day}-{category}'
            recognition = clock_int(d['life']['recognition_ns'])
            relation = ('missing' if recognition is None else 'before' if recognition < times[leg[0]]
                        else 'after' if recognition > times[leg[-1]] else 'during')
            case_rows.append({'case_id': case_id, 'day': day, 'trade_type': d['category'],
                'candidate_id': d['life']['candidate_id'], 'tick_appearances': len(rows),
                'first_trade_ordinal': ords[0], 'last_trade_ordinal': ords[-1],
                'first_receive_ns': str(times[0]), 'last_receive_ns': str(times[-1]),
                'leg_start_ns': str(times[leg[0]]), 'leg_end_ns': str(times[leg[-1]]),
                'leg_duration_ns': str(times[leg[-1]] - times[leg[0]]),
                'birth_label_ns': str(d['life']['anchor_label_ns']),
                'birth_known_by_ns': str(d['life']['lifecycle_start_known_by_ns']),
                'recognition_ns': '' if recognition is None else str(recognition),
                'recognition_relative_to_leg': relation,
                'end_label_ns': str(d['life']['lifecycle_end_label_ns']),
                'end_known_by_ns': str(d['life']['lifecycle_end_known_by_ns']),
                'source_sha256': record['sha256_uncompressed']})
            for i, row in enumerate(rows):
                prov = json.loads(row[index['L029 | raw_source_identity_provenance_clocks_integrity']])['values']
                during, before = prov['during'], prov['before']
                known = clock_int(row[index['known_by_ns']])
                if available(before['known_by_ns'], times[i]) is not True:
                    errors.append([case_id, i, 'before_after_receive'])
                if clock_int(during['known_by_ns']) != known:
                    errors.append([case_id, i, 'during_known_mismatch'])
                native_clock = row[index['Dipole completed-known-by ns']]
                if native_clock and available(native_clock, times[i]) is not True:
                    errors.append([case_id, i, 'native_after_receive'])
                tick_clocks.append({'case_id': case_id, 'row': i, 'trade_ordinal': ords[i],
                    'trade_id': row[index['trade_id']], 'trade_cursor': row[index['trade_cursor']],
                    'event_ns': str(row[index['event_ns']]), 'receive_ns': str(times[i]),
                    'known_by_ns': str(known), 'before_group': before['group_ordinal'],
                    'before_known_by_ns': str(before['known_by_ns']), 'during_group': during['group_ordinal'],
                    'group_first_cursor': during['first_cursor'], 'group_close_cursor': during['close_cursor'],
                    'during_known_by_ns': str(during['known_by_ns']),
                    'native_completed_known_by_ns': str(native_clock),
                    'native_label_ns': str(row[index['Dipole label ns']]),
                    'layer_source_id': row[index['Layer source ID']], 'layer_source_row': row[index['Layer source row']],
                    'during_after_trade_receive': known > times[i],
                    's_previous_input_clock': 'unresolved exact cursor join',
                    's_emission_close_clock': str(during['known_by_ns']),
                    's_last_completed_clock': str(before['known_by_ns'])})
                if i:
                    intervals.append({'case_id': case_id, 'from_row': i-1, 'to_row': i,
                        'from_receive_ns': str(times[i-1]), 'to_receive_ns': str(times[i]),
                        'elapsed_ns': str(times[i]-times[i-1]), 'kind': 'consecutive trade appearances'})
            for field in fields:
                statuses, states, nums, clocks = collections.Counter(), collections.Counter(), {}, {}
                values = [row[index[field]] for row in rows]
                for value in values:
                    full_value_digests[field].update(json.dumps(value, sort_keys=True).encode() + b'\n')
                for i, value in enumerate(values):
                    parsed = decode(value)
                    status = parsed.get('status', 'METADATA') if isinstance(parsed, dict) else 'METADATA'
                    statuses[status] += 1
                    payload = parsed.get('values') if isinstance(parsed, dict) else None
                    measured_payload = None if field.split(' | ')[0] in {'L029','L072','L073','L074','L075'} else payload
                    for path, number in measured_leaves(measured_payload):
                        nums.setdefault(path, []).append((i, number))
                    for path, val in all_leaves(payload):
                        if path.endswith(('.state', '.state_code')):
                            states[path + '=' + str(val)] += 1
                        if path.endswith('_ns') and val is not None and val != '':
                            n = clock_int(val)
                            clocks.setdefault(path, []).append(n)
                    if field.startswith('S') and isinstance(payload, dict):
                        for position, v in payload.items():
                            s_states[(day, position, v.get('state'), v.get('state_code'))] += 1
                    if field.startswith('X') and isinstance(payload, dict):
                        for series in payload.get('series', []):
                            original = series.get('original', {})
                            external_states[(day, field, series.get('series'), original.get('state'))] += 1
                            p = original.get('published_ns')
                            if p is not None and available(p, payload.get('asof_receive_ns')) is False:
                                errors.append([case_id, i, field, 'publication_after_asof'])
                field_status[field].update(statuses)
                field_days[field].setdefault(day, collections.Counter()).update(statuses)
                variable_paths = []
                for path, samples in nums.items():
                    unique = set(v for _, v in samples)
                    if len(unique) > 1:
                        variable_paths.append(path)
                    member_rows.append({'case_id': case_id, 'field': field, 'member': path,
                        'observed_values': len(samples), 'distinct_values': len(unique),
                        'first_row': samples[0][0], 'last_row': samples[-1][0],
                        'first_value': samples[0][1], 'last_value': samples[-1][1],
                        'minimum': min(unique), 'maximum': max(unique),
                        'consecutive_observed_changes': sum(a[1] != b[1] for a,b in zip(samples,samples[1:])),
                        'availability': 'inventory only; apply field clock contract before use'})
                field_case.append({'case_id': case_id, 'day': day, 'trade_type': d['category'],
                    'field': field, 'tick_appearances': len(rows), 'statuses': json.dumps(dict(statuses), sort_keys=True),
                    'distinct_original_cells': len({json.dumps(v, sort_keys=True) for v in values}),
                    'measured_numeric_paths': len(nums), 'varying_numeric_paths': len(variable_paths),
                    'varying_members': json.dumps(variable_paths), 'states': json.dumps(dict(states), sort_keys=True),
                    'clock_ranges_ns': json.dumps({p: {'min': str(min(v)), 'max': str(max(v))} for p,v in clocks.items()}, sort_keys=True)})
    assert len(case_rows) == 32 and len(field_case) == 141 * 32 and len(tick_clocks) == 5513
    assert not errors, errors[:10]
    source_records = []
    catalog = json.loads(args.catalog.read_text(encoding='utf8'))
    sources_by_sha = {r['sha']: r for r in package['sources']}
    for r in catalog:
        if '/combined-events/run-42569937357-1/events-' in r['path'] and r['path'].endswith('.parquet'):
            name = Path(r['path']).name
            if name.startswith(('actions-', 'groups-')) or name == 'trades.parquet':
                if any(day in r['path'] for day in DAYS):
                    sources_by_sha[r['sha']] = r
    for r in sources_by_sha.values():
        local = args.objects / r['sha']
        record = {k:r.get(k) for k in ('id', 'path', 'sha', 'size', 'repo', 'ref', 'url')}
        record['local_blob_hash_verified'] = False
        if local.exists():
            raw = local.read_bytes()
            assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest() == r['sha']
            record['local_blob_hash_verified'] = True
        record['reconstruction_executed'] = False
        source_records.append(record)
    field_summary = []
    for field in fields:
        code = field.split(' | ')[0]
        rows_for_field = [r for r in field_case if r['field'] == field]
        family = 'metadata' if ' | ' not in field else code[0]
        field_summary.append({'field': field, 'family': family, 'statuses': dict(field_status[field]),
            'by_day_status': {day: dict(v) for day,v in field_days[field].items()},
            'cases_with_numeric_members': sum(r['measured_numeric_paths'] > 0 for r in rows_for_field),
            'cases_with_varying_numeric_members': sum(r['varying_numeric_paths'] > 0 for r in rows_for_field),
            'clock_contract': clock_contract(field), 'preserved': True,
            'role': 'unassigned research field; retained for inspection',
            'original_cell_stream_sha256': full_value_digests[field].hexdigest()})
    duplicates = collections.defaultdict(list)
    for field in fields:
        duplicates[full_value_digests[field].hexdigest()].append(field)
    dump('field_inventory.json', field_summary)
    dump('case_manifest.json', case_rows)
    dump('preservation_manifest.json', manifest)
    dump('source_event_inventory.json', source_records)
    dump('exact_cell_duplicate_groups.json', [v for v in duplicates.values() if len(v)>1])
    dump('s_state_audit.json', [dict(zip(['day','position','state','state_code'], k), count=v) for k,v in s_states.items()])
    dump('external_state_audit.json', [dict(zip(['day','field','series','state'], k), count=v) for k,v in external_states.items()])
    write_csv('field_case_audit.csv', field_case)
    write_csv('numeric_member_audit.csv', member_rows)
    write_csv('observed_trade_intervals.csv', intervals)
    with gzip.GzipFile(filename=str(OUT/'tick_clock_ledger.jsonl.gz'), mode='wb', mtime=0) as f:
        for row in tick_clocks:
            f.write((json.dumps(row, separators=(',', ':'))+'\n').encode())
    summary = {'cases': len(case_rows), 'source_fields': len(fields), 'columns': 167,
        'tick_appearances': len(tick_clocks), 'unique_day_trade_ordinals': len({(r['case_id'][:8],r['trade_ordinal']) for r in tick_clocks}),
        'field_case_records': len(field_case), 'numeric_member_case_records': len(member_rows),
        'days': DAYS, 'trade_types_per_day': 8, 'all_original_case_bytes_roundtrip_verified': True,
        'clock_errors': errors, 'recognition_relative_to_leg': dict(collections.Counter(r['recognition_relative_to_leg'] for r in case_rows)),
        'during_after_trade_receive_appearances': sum(r['during_after_trade_receive'] for r in tick_clocks),
        'source_blobs': len(source_records), 'source_blobs_hash_verified': sum(r['local_blob_hash_verified'] for r in source_records),
        'new_strategy_execution': False, 'horizon_fitting_executed': False,
        'claude_new_results_consulted': False,
        'status': 'lossless audit completed; source availability is not strategy readiness'}
    dump('AUDIT_VERIFICATION.json', summary)
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--prior', type=Path, required=True)
    parser.add_argument('--catalog', type=Path, required=True)
    parser.add_argument('--objects', type=Path, required=True)
    run(parser.parse_args())
