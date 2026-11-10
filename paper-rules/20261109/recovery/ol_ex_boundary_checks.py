"""Synthetic boundary checks for recovered definitions; no market/tape access."""
import json
from bisect import bisect_left, bisect_right
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def onset(previous, current):
    if previous is None or current is None:
        return 'UNAVAILABLE'
    if current[1] != 1:
        return 'NO_ONSET'
    if current[0] != previous[0]:
        return 'NEW_BEST'
    return 'STANDING_BEST_SHRANK' if previous[1] > 1 else 'NO_ONSET'

def end_event(side, original_price, later_touch):
    if later_touch is None:
        return 'UNAVAILABLE'
    price, size = later_touch
    if price == original_price:
        return None if size == 1 else 'SIZE_RECOVERED_AT_SAME_PRICE'
    return 'RETREATED' if ((price < original_price) if side == 'B' else (price > original_price)) else 'IMPROVED'

def history(onset_price, rows):
    if len(rows) != 3:
        return 'INSUFFICIENT_PRIOR_BOOKS'
    if any(p != onset_price for p, size in rows):
        return 'PRIOR_BEST_PRICE_CHANGED'
    a, b, c = (size for p, size in rows)
    if a == b == c:
        return 'FLAT'
    if a >= b >= c:
        return 'FALLING'
    return 'BUILDING' if a <= b <= c else 'MIXED'

def history_coordinates(signal, prior):
    # [book_index, group, cursor, known_by_ns]
    return all(signal[1]-p[1] == signal[0]-p[0] and p[2] < signal[2] and p[3] <= signal[3] for p in prior)

def timing(end_cursor, entry_cursor):
    if end_cursor is None:
        return 'NO_OBSERVED_END'
    if entry_cursor is None:
        return 'NO_OBSERVED_ENTRY'
    return 'BY_ENTRY' if end_cursor <= entry_cursor else 'AFTER_ENTRY'

def endpoint(times, target):
    if target > times[-1] or target < times[0]:
        return None
    return bisect_right(times, target)-1

def next_change(rows, j, decision):
    # row = [clock, twice_mid_raw, valid, segment]
    for k in range(j+1, len(rows)):
        if not rows[k][2] or not rows[j][2] or rows[k][3] != rows[j][3]:
            return None
        if rows[k][1] != rows[j][1]:
            return k if rows[k][0] > decision else None
    return None

def age_bin(ms):
    if ms is None:
        return 'none'
    ms = round(ms, 3)
    return 'under_10ms' if ms < 10 else '10ms_to_1s' if ms < 1000 else '1s_to_60s' if ms < 60000 else 'over_60s'

def causal_alive(display, terminating_clocks, decision, coverage):
    if not coverage or display is None:
        return 'UNAVAILABLE'
    return bool(display > 0 and not any(t <= decision for t in terminating_clocks))

def flow_class(linked, unlinked):
    if linked is None or unlinked is None:
        return 'UNAVAILABLE'
    return 'fill_linked' if linked > 0 else 'unlinked_reduction' if unlinked > 0 else 'no_reduction'

def next_level(lots, book_complete):
    if not book_complete:
        return 'UNAVAILABLE'
    return 'no_next' if lots is None else 'next_lt10' if lots < 10 else 'next_ge10'

# Expected values are hand-authored boundary assertions, independent of producer output.
FIXTURES = [
 ('OL_onset_standing', 'onset', [[100,2],[100,1]], 'STANDING_BEST_SHRANK'),
 ('OL_one_to_one_same', 'onset', [[100,1],[100,1]], 'NO_ONSET'),
 ('OL_worse_new_best', 'onset', [[100,1],[99,1]], 'NEW_BEST'),
 ('OL_missing_previous', 'onset', [None,[99,1]], 'UNAVAILABLE'),
 ('OL_bid_retreat', 'end_event', ['B',100,[99,9]], 'RETREATED'),
 ('OL_ask_retreat', 'end_event', ['A',100,[101,9]], 'RETREATED'),
 ('OL_bid_improve', 'end_event', ['B',100,[101,1]], 'IMPROVED'),
 ('OL_not_ended', 'end_event', ['A',100,[100,1]], None),
 ('OL_zero_size_source_label', 'end_event', ['A',100,[100,0]], 'SIZE_RECOVERED_AT_SAME_PRICE'),
 ('OL_missing_end', 'end_event', ['A',100,None], 'UNAVAILABLE'),
 ('OL_history_flat', 'history', [100,[[100,3],[100,3],[100,3]]], 'FLAT'),
 ('OL_history_weak_fall', 'history', [100,[[100,4],[100,4],[100,2]]], 'FALLING'),
 ('OL_history_weak_build', 'history', [100,[[100,2],[100,4],[100,4]]], 'BUILDING'),
 ('OL_history_mixed', 'history', [100,[[100,4],[100,2],[100,3]]], 'MIXED'),
 ('OL_history_price_change', 'history', [100,[[99,4],[100,4],[100,2]]], 'PRIOR_BEST_PRICE_CHANGED'),
 ('OL_history_short', 'history', [100,[[100,4],[100,2]]], 'INSUFFICIENT_PRIOR_BOOKS'),
 ('OL_history_equal_clock_prior_cursor', 'history_coordinates', [[3,13,100,1000],[[0,10,97,990],[1,11,98,1000],[2,12,99,1000]]], True),
 ('OL_history_gap_rejected', 'history_coordinates', [[3,14,100,1000],[[0,10,97,990],[1,11,98,1000],[2,12,99,1000]]], False),
 ('OL_history_future_rejected', 'history_coordinates', [[3,13,100,1000],[[0,10,97,990],[1,11,98,1000],[2,12,99,1001]]], False),
 ('OL_end_equal_entry', 'timing', [7,7], 'BY_ENTRY'),
 ('OL_end_after_entry', 'timing', [8,7], 'AFTER_ENTRY'),
 ('OL_entry_missing', 'timing', [8,None], 'NO_OBSERVED_ENTRY'),
 ('OL_no_end', 'timing', [None,7], 'NO_OBSERVED_END'),
 ('EX_latest_le_target', 'endpoint', [[100,120,160],150], 1),
 ('EX_equal_clock_last_cursor', 'endpoint', [[100,120,120,160],120], 2),
 ('EX_target_beyond_end', 'endpoint', [[100,120,160],161], None),
 ('EX_flat_endpoint_is_allowed', 'endpoint', [[100,160],120], 0),
 ('EX03_first_changed', 'next_change', [[[100,200,True,0],[110,200,True,0],[120,202,True,0]],0,100], 2),
 ('EX03_reset_blocks', 'next_change', [[[100,200,True,0],[110,200,False,1],[120,202,True,1]],0,100], None),
 ('EX03_no_change_not_flat', 'next_change', [[[100,200,True,0],[120,200,True,0]],0,100], None),
 ('EX03_equal_clock_not_later', 'next_change', [[[100,200,True,0],[100,202,True,0]],0,100], None),
 ('EX03_birth_one_ns_is_diagnostic', 'next_change', [[[99,200,True,0],[100,202,True,0]],0,99], 1),
 ('OL_age_missing', 'age_bin', [None], 'none'),
 ('OL_age_rounds_to_10', 'age_bin', [9.9996], '10ms_to_1s'),
 ('OL_age_1000', 'age_bin', [1000], '1s_to_60s'),
 ('OL_age_60000', 'age_bin', [60000], 'over_60s'),
 ('EX05_termination_equal_timer', 'causal_alive', [1,[125],125,True], False),
 ('EX05_future_end_not_consumed', 'causal_alive', [1,[],125,True], True),
 ('EX05_missing_is_not_false', 'causal_alive', [None,[],125,True], 'UNAVAILABLE'),
 ('EX05_gap_is_not_alive', 'causal_alive', [1,[],125,False], 'UNAVAILABLE'),
 ('EX05_gone_at_initial_close', 'causal_alive', [0,[100],100,True], False),
 ('OL_linked_precedence', 'flow_class', [1,4], 'fill_linked'),
 ('OL_unlinked', 'flow_class', [0,4], 'unlinked_reduction'),
 ('OL_missing_reductions', 'flow_class', [None,0], 'UNAVAILABLE'),
 ('OL_next_exactly10', 'next_level', [10,True], 'next_ge10'),
 ('OL_next9', 'next_level', [9,True], 'next_lt10'),
 ('OL_observed_no_next', 'next_level', [None,True], 'no_next'),
 ('OL_missing_book', 'next_level', [None,False], 'UNAVAILABLE'),
]

def main():
    cases = []
    for name, operation, inputs, expected in FIXTURES:
        actual = globals()[operation](*inputs)
        assert actual == expected, (name, actual, expected)
        cases.append(dict(id=name,operation=operation,inputs=inputs,expected=expected,actual=actual,passed=True))
    assert bisect_left([1000000,1999999,2000000],2000000) == 2
    definitions = json.loads((ROOT/'ol_ex_source_bound_definitions.json').read_text())
    assert definitions['EX05_observation']['horizons_s'] == [0.1,1,5,20]
    assert definitions['EX05_inventory_outcomes']['horizons_s'] == [1,5,20,60,300]
    out = dict(schema='OL-EX-INDEPENDENT-SYNTHETIC-FIXTURES-v1', source_definitions='ol_ex_source_bound_definitions.json',
               scope='Synthetic inputs only; no original research result or producer rerun.', passed=len(cases), fixtures=cases)
    (ROOT/'ol_ex_independent_boundary_fixtures.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(dict(passed=len(cases),source_horizon_assertions=2,entry_threshold_assertions=1)))

if __name__ == '__main__':
    main()
