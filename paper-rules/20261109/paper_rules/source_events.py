"""Recovered OL/EX source semantics. Outcome endpoints are not entry features.
These primitives preserve source labeling; callers enforce data availability.
"""
from bisect import bisect_right

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
    if len(prior)!=3:return False
    if any(p[0]!=signal[0]-3+i or p[1]!=signal[1]-3+i for i,p in enumerate(prior)):return False
    if any(a[2]>=b[2] or a[3]>b[3] for a,b in zip(prior,prior[1:])):return False
    return all(p[2] < signal[2] and p[3] <= signal[3] for p in prior)

def timing(end_cursor, entry_cursor):
    if end_cursor is None:
        return 'NO_OBSERVED_END'
    if entry_cursor is None:
        return 'NO_OBSERVED_ENTRY'
    return 'BY_ENTRY' if end_cursor <= entry_cursor else 'AFTER_ENTRY'

def endpoint(times, target):
    if not times or target > times[-1] or target < times[0]:
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

