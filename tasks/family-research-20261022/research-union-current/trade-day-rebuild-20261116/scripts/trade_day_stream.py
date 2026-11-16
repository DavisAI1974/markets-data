"""One CME trade day of NG messages, replayed with the pinned book adapter (unchanged).

TRADE DAY  = 17:00 ET the evening before (the daily halt; trading resumes 18:00 ET) to 17:00 ET on the named date.
             In October 2023 (EDT) that is 21:00 UTC to 21:00 UTC.
UTC CLOCK DAY = how the raw tape files are cut (00:00-24:00 UTC). One trade day spans the last 3 hours of one file
             and the first 21 hours of the next.

The only difference from the original replay: the exchange snapshot that opens the second UTC-clock-day file is NOT
applied. The book is carried straight through 00:00 UTC, after checking that the carried book equals that snapshot
(same orders, sides, prices, sizes, and the same queue order on every price level). Applying the snapshot, as the
original did, restarts every resting order's age and identity history at 00:00 UTC (20:00 ET), two hours into the
trade day. Cursors and group ordinals are numbered exactly as the original numbered them (snapshot records still
take a cursor), so existing trade designations on the full-session archives do not move.
"""
import hashlib, importlib, json, sys
from dataclasses import asdict
import numpy as np
import databento as db
sys.path.insert(0, '/home/user/work/pins/research')
A = importlib.import_module('ng_exhaustion_mbo_v4_state_adapter_20260820')
TAPE = '/home/user/markets-data/data/nymex_mbo/ng_v0_oct2023/'
INSTRUMENT = 150611
HALT_UTC_NS = 21 * 3600 * 10**9          # 17:00 ET in EDT
PRIOR = {'20231002': '20231001', '20231003': '20231002', '20231017': '20231016', '20231018': '20231017'}

def _file(day):
    path = TAPE + f'NG_v0_mbo_{day}.dbn.zst'
    spec = next(f for f in json.load(open(TAPE + 'MANIFEST.json'))['files'] if f['file'] == f'NG_v0_mbo_{day}.dbn.zst')
    data = open(path, 'rb').read()
    if len(data) != spec['bytes'] or hashlib.sha256(data).hexdigest() != spec['sha256']:
        raise ValueError(f'tape bytes differ from the tape manifest: {day}')
    store = db.DBNStore.from_bytes(data)
    ts = store.to_ndarray()['ts_recv'].astype('int64')
    midnight = int(np.datetime64(f'{day[:4]}-{day[4:6]}-{day[6:]}', 'ns').astype('int64'))
    return store, spec, int(np.searchsorted(ts, midnight + HALT_UTC_NS, 'left')), len(ts)

def trade_day(day, on_receipt=None):
    """Yield one dict per session record. `book` is the live carried book AFTER the record (do not mutate)."""
    prior_day = PRIOR[day]
    prior, pspec, pskip, plen = _file(prior_day)
    cur, cspec, ctake, clen = _file(day)
    adapter = A.V4MboAdapter()
    for i, rec in enumerate(prior):                       # warm-up: the prior trade day, only to seat the book
        if i == pskip: break
        adapter.apply(rec, 'NGX3')
    adapter.assert_groups_closed()
    book = adapter.books[INSTRUMENT]
    receipt = dict(trade_day=day, definition='17:00 ET prior evening to 17:00 ET named date (21:00-21:00 UTC, EDT)',
                   sources=[dict(utc_clock_day=prior_day, file=pspec['file'], sha256=pspec['sha256'], records=plen, warmup_records=pskip,
                                 session_records=plen - pskip),
                            dict(utc_clock_day=day, file=cspec['file'], sha256=cspec['sha256'], records=clen, session_records=ctake,
                                 after_halt_records_not_used=clen - ctake)],
                   resting_orders_at_session_start=len(book.orders))
    cursor = group = 0
    def emit(rec, source_day, index):
        nonlocal cursor, group
        msg = adapter.normalize(rec, 'NGX3')
        prior_order = book.orders.get(msg.order_id)
        before = None if prior_order is None else asdict(prior_order)
        effect, frame, _ = book.apply(msg)
        after_order = book.orders.get(msg.order_id)
        closed = frame is not None
        row = dict(cursor=cursor, group=group if closed else None, utc_clock_day=source_day, file_index=index, msg=msg, effect=effect,
                   order_before=before, order_after=None if after_order is None else asdict(after_order), frame=frame,
                   midnight_snapshot_not_applied=False, book=book)
        cursor += 1; group += closed
        return row
    for i, rec in enumerate(prior):
        if i < pskip: continue
        yield emit(rec, prior_day, i)
    adapter_orders = {oid: (o.side, o.price_raw, o.size) for oid, o in book.orders.items()}
    carried_q = {(s, p): list(q) for s in ('B', 'A') for p, q in book.levels[s].items() if q}
    snap, snap_q, n_snap, true_event = {}, {}, 0, {}
    for i, rec in enumerate(cur):
        if i == ctake: break
        if int(rec.flags) & 32:                           # the 00:00 UTC exchange snapshot: checked, not applied
            if i != n_snap: raise ValueError('snapshot record after the opening block')
            msg = adapter.normalize(rec, 'NGX3'); n_snap += 1
            if msg.action == 'A':
                snap[msg.order_id] = (msg.side, msg.price_raw, msg.size)
                snap_q.setdefault((msg.side, msg.price_raw), []).append(msg.order_id); true_event[msg.order_id] = msg.ts_event_ns
            yield dict(cursor=cursor, group=group if msg.is_last else None, utc_clock_day=day, file_index=i, msg=msg, effect=None,
                       order_before=None, order_after=None, frame=None, midnight_snapshot_not_applied=True, book=book)
            cursor += 1; group += msg.is_last
            continue
        if i == n_snap:                                   # first live record of the second file: settle the check
            ok = snap == adapter_orders and snap_q == carried_q
            receipt['midnight_utc_carry'] = dict(snapshot_records=n_snap, snapshot_orders=len(snap), carried_orders=len(adapter_orders),
                same_orders_sides_prices_sizes=snap == adapter_orders, price_levels=len(snap_q),
                levels_with_identical_queue_order=sum(carried_q.get(k) == q for k, q in snap_q.items()), carried_equals_snapshot=ok,
                orders_whose_snapshot_event_time_is_over_1s_older_than_the_carried_priority_time=sum(
                    book.orders[o].priority_recv_ns - t > 10**9 for o, t in true_event.items()))
            if not ok: raise ValueError(f'{day}: carried book differs from the 00:00 UTC snapshot; refusing to carry')
        yield emit(rec, day, i)
    adapter.assert_groups_closed()
    receipt.update(session_records=cursor, completed_groups=group, resting_orders_at_halt=len(book.orders), integrity=dict(book.integrity))
    if on_receipt: on_receipt(receipt)
