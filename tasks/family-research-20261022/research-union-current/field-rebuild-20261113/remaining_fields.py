"""Recover supported missing fields without substituting model or target outputs.

All clocks are integer nanoseconds. No S producer is imported or executed.
The path/state movie is explicitly scoped to the preserved selected ticks.
"""
import bisect
import collections
import gzip
import hashlib
import json
from pathlib import Path
import sys

from prepare_sheet_repair import col, packed, read, lines
from recover_event_inputs import verified

OUT = Path(__file__).resolve().parent
RECOVERY = Path('E:/frankie-excel-review-20261109')
DAYS = ('20231002', '20231003', '20231017', '20231018')
NEW = OUT / 'remaining-field-recovery'


def eligible_end(keys, clock, cursor):
    return bisect.bisect_right(keys, (clock, cursor))


def path_delta(prior, current):
    result = {}
    for name, out in [('receive_ns', 'elapsed_receive_ns'), ('price_raw', 'price_raw_change'),
                      ('bid_depth', 'bid_depth_change'), ('ask_depth', 'ask_depth_change')]:
        a = prior.get(name) if prior else None
        b = current.get(name)
        result[out] = b - a if a is not None and b is not None else None
    return result


def state_hash(payload, prior_hash):
    return hashlib.sha256(packed({'prior_sha256': prior_hash, 'state': payload}).encode()).hexdigest()


def pin(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        while chunk := f.read(1024 * 1024):
            h.update(chunk)
    return {'path': str(path), 'bytes': path.stat().st_size, 'sha256': h.hexdigest()}


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf8')


def recover_candidates():
    """Read every candidate, not only the latest section observation per tick."""
    import pyarrow.parquet as pq
    NEW.mkdir(exist_ok=True)
    audit = {}
    for pub in read(RECOVERY / 'recovered-packets/NATIVE_PUBLICATIONS.json'):
        day = pub['day']
        manifest = read(RECOVERY / f'recovered-packets/native/{day}/MANIFEST.json')
        entries = {e['path']: e for e in manifest['files']}
        wanted = collections.defaultdict(dict)
        for entry in manifest['files']:
            if not entry['path'].endswith('.parquet'):
                continue
            path = verified(RECOVERY, pub, entry, 'native-index-cache')
            table = pq.read_table(path, filters=[('emitting_section', '=', 'candidate')])
            for row in table.to_pylist():
                wanted[row['shard']][row['shard_row']] = row
        records = []
        for shard, positions in sorted(wanted.items()):
            path = verified(RECOVERY, pub, entries[shard], 'native-index-cache')
            with gzip.open(path, 'rt', encoding='utf8') as f:
                for i, line in enumerate(f):
                    if i not in positions:
                        continue
                    value = json.loads(line)
                    idx = positions[i]
                    assert value['emitting_section'] == 'candidate'
                    assert value['emitted_at_recv_ns'] == idx['known_by_ns']
                    records.append({'known_by_ns': idx['known_by_ns'],
                                    'input_cursor': idx['input_cursor'], 'original': value,
                                    'source': dict(publication=pub, shard=shard, row=i,
                                                   sha256=entries[shard]['sha256'])})
        expected = read(RECOVERY / f'recovered-packets/native/{day}/RECOVERY_RECEIPT.json')['sections']['candidate']
        assert len(records) == expected, (day, len(records), expected)
        records.sort(key=lambda r: (r['known_by_ns'], r['input_cursor']))
        with gzip.open(NEW / f'candidates-{day}.jsonl.gz', 'wt', encoding='utf8') as f:
            for record in records:
                f.write(packed(record) + '\n')
        audit[day] = dict(records=len(records), entire_archived_candidate_section=True,
                          publication=pub, output=pin(NEW / f'candidates-{day}.jsonl.gz'))
        print(day, 'all original candidates recovered', len(records), flush=True)
    source = RECOVERY / 'oct18-original/source-candidate.jsonl.gz'
    records = []
    source_pin = pin(source)
    for r in lines(source):
        assert r['known_by_ns'] is not None and r['input_cursor'] is not None
        records.append(dict(known_by_ns=r['known_by_ns'], input_cursor=r['input_cursor'],
                            original=r['original_record'], source=r))
    records.sort(key=lambda r: (r['known_by_ns'], r['input_cursor']))
    with gzip.open(NEW / 'candidates-20231018.jsonl.gz', 'wt', encoding='utf8') as f:
        for record in records:
            f.write(packed(record) + '\n')
    audit['20231018'] = dict(records=len(records), source=source_pin,
                            scope='Every candidate in the original saved extraction',
                            output=pin(NEW / 'candidates-20231018.jsonl.gz'))
    write(NEW / 'CANDIDATE_RECOVERY.json', audit)


class SupplementStore:
    def __init__(self, first_row):
        self.row = first_row
        self.refs = {}
        self.file = gzip.open(OUT / 'cache/supplement_payloads.jsonl.gz', 'wt', encoding='utf8', compresslevel=1)

    def add(self, key, value):
        assert key not in self.refs
        text = packed(value)
        chunks = [text[i:i+20000] for i in range(0, len(text), 20000)]
        start = self.row
        for i, chunk in enumerate(chunks):
            self.file.write(packed([key, i+1, len(chunks), chunk]) + '\n')
            self.row += 1
        ref = dict(sheet='Recovered payloads', first_row=start, last_row=self.row-1,
                   json_column='D', sha256_utf8=hashlib.sha256(text.encode()).hexdigest(), id=key)
        self.refs[key] = ref
        return ref


def prepare():
    import pyarrow.parquet as pq
    audit = read(NEW / 'CANDIDATE_RECOVERY.json')
    baseline = read(OUT / 'WORKBOOK_REPAIR_PREPARATION.json')
    store = SupplementStore(baseline['payload_rows'] + 2)
    package = json.loads(gzip.decompress((OUT.parent / 'evidence-availability-20261113/raw/package.json.gz').read_bytes()))
    layout = read(OUT / 'WORKBOOK_LAYOUT.json')
    # Reuse verified payload references from the first repair, without re-embedding full books.
    old_refs = {}
    for r in lines(OUT / 'cache/workbook_updates.jsonl.gz'):
        if r['field'].startswith('L041 | '):
            old_refs[(r['case'], r['row'])] = json.loads(r['value'])['values_in_workbook']
    counts = collections.Counter()
    candidate_refs, candidates = {}, {}
    for day in DAYS:
        candidates[day] = list(lines(NEW / f'candidates-{day}.jsonl.gz'))
        candidate_refs[day] = [store.add(f'discovery:{day}:{i}', row)
                               for i, row in enumerate(candidates[day])]
    output = gzip.open(OUT / 'cache/supplement_updates.jsonl.gz', 'wt', encoding='utf8', compresslevel=1)
    manifests = {day: pin(OUT / f'source_manifests/book-{day}.json') for day in DAYS}
    code_pin = pin(Path(__file__))
    source_inventory = RECOVERY / 'consolidated-recovery/brain/20261109-search/K-31ff5a9d7e5d-NG_EXHAUSTION_FRANKIE_DATA_FEED_INVENTORY_20260824.md'
    inventory_text = source_inventory.read_text(encoding='utf8')
    assert '[2021-10-01, 2021-11-01)' in inventory_text
    inventory_ref = store.add('canonical-source-window-inventory', {'content_utf8': inventory_text, 'source': pin(source_inventory)})
    case_audits = []
    for day in DAYS:
        flow_table = pq.read_table(OUT / f'flow_inputs/{day}/trade-flow-inputs.parquet',
                                  columns=['trade_ordinal', 'L055 | legacy_native_signed_flow'])
        flows = {r['trade_ordinal']: json.loads(r['L055 | legacy_native_signed_flow']) for r in flow_table.to_pylist()}
        keys = [(r['known_by_ns'], r['input_cursor']) for r in candidates[day]]
        for case in [c for c in package['cases'] if c['day'] == day]:
            case_id = f"{day}-{case['category_index']}"
            original = json.loads(gzip.decompress((OUT.parent / f'evidence-availability-20261113/raw/{case_id}.json.gz').read_bytes()))
            heads = original['headers']
            loc = next(x for x in layout['loc'] if x['candidate'] == case['life']['candidate_id'])
            prior = None
            prior_hash = '0' * 64
            path_first_row = None
            path_last_row = None
            case_count = 0
            with gzip.open(NEW / f'path-state-{case_id}.jsonl.gz', 'wt', encoding='utf8') as ledger:
                for record in lines(OUT / f'book_records/{case_id}.jsonl.gz'):
                    i = record['case_row']; b = record['original']; trade = b['original_trade']; book = b['book_full']
                    clock = trade['receive_ns']; cursor = trade['trade_input_cursor']; ordinal = b['trade_ordinal']
                    flow = flows[ordinal]
                    assert flow.get('known_by_ns') is None or flow['known_by_ns'] <= clock
                    point = dict(trade_ordinal=ordinal, receive_ns=clock, event_ns=trade['event_ns'],
                                 input_cursor=cursor, price_raw=trade['price_raw'],
                                 bid_depth=book['bid_depth_full'], ask_depth=book['ask_depth_full'],
                                 best_bid=book['best_bid'], best_ask=book['best_ask'],
                                 signed_trade_size=trade['size'] * (1 if trade['aggressor_side']=='B' else -1)
                                 if trade['aggressor_side'] in ('A','B') else None,
                                 latest_completed_native_flow=flow,
                                 complete_book_in_workbook=old_refs[(case_id, i)])
                    delta = path_delta(prior, point)
                    current_hash = state_hash(point, prior_hash)
                    movie = dict(case=case_id, case_row=i, known_by_ns=clock, state=point,
                                 delta=delta, prior_sha256=prior_hash, state_sha256=current_hash,
                                 source=record['source'])
                    ledger.write(packed(movie)+'\n')
                    ref = store.add(f'path-state:{case_id}:{i}', movie)
                    if path_first_row is None:
                        path_first_row = ref['first_row']
                    path_last_row = ref['last_row']
                    # Other payload kinds are not interleaved within each case's path block.
                    path_ref = dict(sheet='Recovered payloads', first_row=path_first_row,
                                    last_row=path_last_row, json_column='D', terminal_sha256=current_hash,
                                    decoding='Group contiguous rows by Payload ID; concatenate chunks for each ID.')
                    end = eligible_end(keys, clock, cursor)
                    discoveries = dict(record_count=end, first_payload=candidate_refs[day][0] if end else None,
                                       last_payload=candidate_refs[day][end-1] if end else None,
                                       rule='All original candidate discoveries with (emission receive ns, cursor) <= current trade. No model execution implied.',
                                       source_coverage=audit[day])
                    common = dict(phase='at_trade_input', known_by_ns=clock, all_field_semantics_complete=False)
                    changes = {
                        'L025': dict(status='RECOVERED_EXACT_SOURCE_WINDOW', values=dict(start_inclusive='2021-10-01', end_exclusive='2021-11-01',
                                     scope='Canonical inventory window; not the four 2023 research dates.', applies_to_current_trade=False),
                                     source_in_workbook=inventory_ref, historical_market_clock=None),
                        'L064': dict(common, status='RECONSTRUCTED_SELECTED_TICK_PATH', values=dict(current=point, delta=delta, prefix_in_workbook=path_ref),
                                     scope='Every retained tick from this case start through this trade; no intervening non-trade state or unobserved path asserted.'),
                        'L065': dict(common, status='RECOVERED_MECHANICS_FIFO_FEATURES', values=dict(activity=b['activity'],
                                     complete_fifo_book_in_workbook=old_refs[(case_id,i)], integrity=b['integrity'],
                                     fifo_priority_reconstructed=b['fifo_priority_reconstructed'], native_priority_id_exposed=b['native_priority_id_exposed']),
                                     scope='Original adapter mechanics activity and every FIFO level/order. Archived activity windows retained as provenance; no new fixed horizon selected. Not a completed V4 geometry feature vector.'),
                        'L090': dict(common, status='RECONSTRUCTED_STATE_DELTA_MOVIE', values=dict(current_in_workbook=ref, prefix_in_workbook=path_ref),
                                     scope='Append-only hash chain of selected-tick price/flow/book states and deltas. Other unproduced state fields remain unresolved; not a Frankie run.'),
                        'L093': dict(common, status='RECOVERED_ORIGINAL_CANDIDATE_DISCOVERIES', values=discoveries),
                        'L099': dict(status='RECONSTRUCTION_RUN_HASHES', values=dict(state_sha256=current_hash, prior_state_sha256=prior_hash,
                                     code=code_pin, book_manifest=manifests[day], source=record['source'], model=None, model_run=None),
                                     historical_market_clock=None, all_field_semantics_complete=False,
                                     scope='Actual reconstruction hashes. No model or primary experiment run exists in these recovered producer outputs.')
                    }
                    for code, value in changes.items():
                        field = next(h for h in heads if h.startswith(code+' | '))
                        j = heads.index(field)
                        prior_cell = json.loads(original['rows'][i][j])
                        assert prior_cell['status'] in ('MISSING_STATIC_SOURCE', 'NO_MATCHING_VALUE_IN_RETAINED_INPUT')
                        address = col(loc['base']+layout['tickPositions'][j])+str(loc['headRow']+i+2)
                        text = packed(value)
                        assert len(text) <= 30000, (field, len(text))
                        output.write(packed(dict(sheet=1, cell=address, value=text, field=field, case=case_id, row=i))+'\n')
                        counts[field] += 1
                    prior = point; prior_hash = current_hash; case_count += 1
            assert case_count == len(original['rows'])
            case_audits.append(dict(case=case_id, ticks=case_count, terminal_sha256=prior_hash))
            print('Prepared missing-field values', case_id, case_count, flush=True)
    output.close(); store.file.close()
    result = dict(fields_populated=dict(counts), cells_added=sum(counts.values()),
                  payload_rows_added=store.row-2-baseline['payload_rows'], cases=case_audits,
                  all_35_fields_complete=False, s_fields_changed=0,
                  scope='One exact source-window metadata field plus five explicitly scoped recoveries; no fabricated model outputs.')
    write(OUT / 'REMAINING_FIELD_RECOVERY.json', result)


if __name__ == '__main__':
    sys.path.insert(0, str(RECOVERY / 'python-deps'))
    if '--candidates' in sys.argv:
        recover_candidates()
    else:
        prepare()
