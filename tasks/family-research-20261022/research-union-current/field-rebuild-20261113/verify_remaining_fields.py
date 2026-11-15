"""Independent readback of the supplemental values and their source bindings."""
import collections
import hashlib
import json
from remaining_fields import OUT, NEW, DAYS, lines, read, packed, write


def main():
    report = read(OUT / 'REMAINING_FIELD_RECOVERY.json')
    cases = {r['case']: r for r in report['cases']}
    checked = 0
    candidate_counts = {}
    candidate_cache = {}
    cutoffs = {}
    for day in DAYS:
        candidates = list(lines(NEW / f'candidates-{day}.jsonl.gz'))
        candidate_cache[day] = candidates
        candidate_counts[day] = len(candidates)
        keys = [(r['known_by_ns'], r['input_cursor']) for r in candidates]
        assert keys == sorted(keys)
    for case, audit in cases.items():
        prior_hash = '0' * 64
        prior = None
        count = 0
        for row, source in zip(lines(NEW / f'path-state-{case}.jsonl.gz'),
                               lines(OUT / f'book_records/{case}.jsonl.gz'), strict=True):
            b = source['original']; t = b['original_trade']; state = row['state']
            assert row['source'] == source['source']
            assert row['prior_sha256'] == prior_hash
            expected = hashlib.sha256(packed({'prior_sha256': prior_hash, 'state': state}).encode()).hexdigest()
            assert row['state_sha256'] == expected
            for dest, origin in [('receive_ns','receive_ns'),('event_ns','event_ns'),
                                 ('input_cursor','trade_input_cursor'),('price_raw','price_raw')]:
                assert state[dest] == t[origin]
            assert state['trade_ordinal'] == b['trade_ordinal']
            cutoffs[(case, row['case_row'])] = (t['receive_ns'], t['trade_input_cursor'])
            assert state['bid_depth'] == b['book_full']['bid_depth_full']
            assert state['ask_depth'] == b['book_full']['ask_depth_full']
            for name, delta in [('receive_ns','elapsed_receive_ns'),('price_raw','price_raw_change'),
                                ('bid_depth','bid_depth_change'),('ask_depth','ask_depth_change')]:
                want = None if prior is None or prior[name] is None or state[name] is None else state[name]-prior[name]
                assert row['delta'][delta] == want
            assert state['latest_completed_native_flow'].get('known_by_ns') is None or state['latest_completed_native_flow']['known_by_ns'] <= t['receive_ns']
            prior_hash = expected; prior = state; count += 1
        assert count == audit['ticks'] and prior_hash == audit['terminal_sha256']
        checked += count
    updates = collections.Counter()
    for r in lines(OUT / 'cache/supplement_updates.jsonl.gz'):
        assert not r['field'].startswith('S')
        updates[r['field']] += 1
        value = json.loads(r['value'])
        assert len(r['value']) <= 30000
        if r['field'].startswith('L093'):
            day = r['case'].split('-')[0]
            candidates = candidate_cache[day]
            cutoff = cutoffs[(r['case'], r['row'])]
            end = value['values']['record_count']
            assert end == sum((c['known_by_ns'],c['input_cursor']) <= cutoff for c in candidates)
            if end:
                assert candidates[end-1]['known_by_ns'] <= value['known_by_ns']
            if end < len(candidates):
                assert candidates[end]['known_by_ns'] >= value['known_by_ns']
    assert dict(updates) == report['fields_populated']
    assert checked == 5513 and sum(updates.values()) == 33078
    result = dict(path_states_source_verified=checked, supplemental_cells_verified=sum(updates.values()),
                  candidate_records=candidate_counts, exact_integer_clock_tests_passed=True,
                  s_fields_changed=0, complete_35_field_semantics=False)
    write(OUT / 'REMAINING_FIELD_VERIFICATION.json', result)
    print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()
