"""One CME trade day of NG messages, replayed with the pinned book adapter (unchanged).

TRADE DAY  = 17:00 ET the evening before (the daily halt; trading resumes 18:00 ET) to 17:00 ET on the named date.
             In October 2023 (EDT) that is 21:00 UTC to 21:00 UTC.
UTC CLOCK DAY = how the raw tape files are cut (00:00-24:00 UTC). One trade day spans the last 3 hours of one file
             and the first 21 hours of the next.

Two differences from the original replay.
1. The exchange snapshot that opens the second UTC-clock-day file is NOT applied.
2. The warm-up starts at the earliest file held for the trade week (WARMUP below), not at the file before the trade
   day, and every later opening snapshot it passes is checked against the carried book and not applied either.
On difference 1: The book is carried straight through 00:00 UTC, after checking that the carried book equals that snapshot
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
# Warm-up files, oldest first. The warm-up starts at the earliest UTC clock-day file held for that trade week, so an
# order placed earlier in the week keeps the receive time the replay saw it arrive with. The last file listed is the
# one whose final three hours (from 21:00 UTC) open the trade day.
WARMUP = {'20231002': ['20231001'], '20231003': ['20231001', '20231002'],
          '20231017': ['20231015', '20231016'], '20231018': ['20231015', '20231016', '20231017']}
DAY_NS = 86400 * 10**9

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
    """Yield one dict per session record. `book` is the live carried book AFTER the record (do not mutate).

    `floor` is a live dict of the resting orders whose priority time is only a FLOOR (the order is older than what
    the tape can show): order_id -> {kind, floor_recv_ns, snapshot_event_ns}. Two kinds:
      weekly_relisting_block        the exchange re-lists every order carried over the weekend in one block on Sunday,
                                    all with one stamp; the order's real entry time is not on the tape at all.
      opening_snapshot_of_earliest_held_file
                                    the earliest file held for the week opens at 00:00 UTC with a snapshot; the order
                                    was placed before that. The snapshot's own event time is kept beside it.
    An order leaves `floor` the moment it is removed or a modify resets its priority.
    """
    warm_days = WARMUP[day]; prior_day = warm_days[-1]
    files = {d: _file(d) for d in warm_days + [day]}
    prior, pspec, pskip, plen = files[prior_day]
    cur, cspec, ctake, clen = files[day]
    adapter = A.V4MboAdapter(); floor = {}; state = dict(book=None)

    def step(rec, seat_floor=False):
        """Apply one record to the carried book and keep `floor` true."""
        msg = adapter.normalize(rec, 'NGX3')
        if state['book'] is None: state['book'] = adapter.books[msg.instrument_id] = A.InstrumentBook(msg.instrument_id)
        b = state['book']
        prior_order = b.orders.get(msg.order_id)
        before = None if prior_order is None else asdict(prior_order)
        effect, frame, _ = b.apply(msg)
        if msg.action == 'R': floor.clear()
        elif msg.action in ('A', 'M', 'C'):
            o = b.orders.get(msg.order_id)
            if seat_floor and msg.is_snapshot and msg.action == 'A' and o is not None:
                floor[msg.order_id] = dict(kind='opening_snapshot_of_earliest_held_file' if msg.ts_recv_ns % DAY_NS == 0 else 'weekly_relisting_block',
                                           floor_recv_ns=msg.ts_recv_ns, snapshot_event_ns=msg.ts_event_ns)
            elif msg.order_id in floor and (o is None or o.priority_recv_ns != floor[msg.order_id]['floor_recv_ns']):
                del floor[msg.order_id]
        return msg, before, effect, frame

    def carry_check(d, store, take):
        """Read the snapshot block that opens file `d`; it is compared with the carried book and NOT applied."""
        b = state['book']
        carried = {oid: (o.side, o.price_raw, o.size) for oid, o in b.orders.items()}
        carried_q = {(s, p): list(q) for s in ('B', 'A') for p, q in b.levels[s].items() if q}
        snap, snap_q, event, block = {}, {}, {}, []
        for i, rec in enumerate(store):
            if i == take or not (int(rec.flags) & 32): break
            msg = adapter.normalize(rec, 'NGX3'); block.append((i, rec, msg))
            if msg.action == 'A':
                snap[msg.order_id] = (msg.side, msg.price_raw, msg.size)
                snap_q.setdefault((msg.side, msg.price_raw), []).append(msg.order_id); event[msg.order_id] = msg.ts_event_ns
        ok = snap == carried and snap_q == carried_q
        kinds = {}
        for f in floor.values(): kinds[f['kind']] = kinds.get(f['kind'], 0) + 1
        result = dict(at_0000_utc_of=d, snapshot_records=len(block), snapshot_orders=len(snap), carried_orders=len(carried),
            same_orders_sides_prices_sizes=snap == carried, price_levels=len(snap_q),
            levels_with_identical_queue_order=sum(carried_q.get(k) == q for k, q in snap_q.items()), carried_equals_snapshot=ok,
            orders_whose_snapshot_event_time_is_over_1s_older_than_the_carried_priority_time=sum(
                b.orders[o].priority_recv_ns - t > 10**9 for o, t in event.items() if o in b.orders),
            resting_orders_whose_priority_time_is_a_floor=dict(sorted(kinds.items())))
        if not ok: raise ValueError(f'{day}: carried book differs from the 00:00 UTC snapshot of {d}; refusing to carry')
        return result, block

    warm_carries = []; sources = []
    for n, d in enumerate(warm_days):                      # warm-up: only to seat the book and its order times
        store, spec, skip, length = files[d]
        stop = skip if d == prior_day else length
        applied = 0; block_len = 0
        if n:                                              # a later warm-up file: its opening snapshot is checked, not applied
            result, block = carry_check(d, store, stop); warm_carries.append(result); block_len = len(block)
        for i, rec in enumerate(store):
            if i == stop: break
            if i < block_len: continue
            if n and int(rec.flags) & 32: raise ValueError('snapshot record after the opening block')
            step(rec, seat_floor=(n == 0)); applied += 1
        sources.append(dict(utc_clock_day=d, file=spec['file'], sha256=spec['sha256'], records=length, warmup_records=stop,
                            **({'session_records': length - stop} if d == prior_day else {})))
    adapter.assert_groups_closed()
    book = state['book']
    sources.append(dict(utc_clock_day=day, file=cspec['file'], sha256=cspec['sha256'], records=clen, session_records=ctake,
                        after_halt_records_not_used=clen - ctake))
    receipt = dict(trade_day=day, definition='17:00 ET prior evening to 17:00 ET named date (21:00-21:00 UTC, EDT)',
                   warmup='from the earliest UTC clock-day file held for the trade week; later opening snapshots checked, not applied',
                   sources=sources, warmup_midnight_utc_carries=warm_carries, resting_orders_at_session_start=len(book.orders),
                   resting_orders_at_session_start_whose_priority_time_is_a_floor=len(floor))
    cursor = group = 0
    def emit(rec, source_day, index):
        nonlocal cursor, group
        msg, before, effect, frame = step(rec)
        after_order = book.orders.get(msg.order_id)
        closed = frame is not None
        row = dict(cursor=cursor, group=group if closed else None, utc_clock_day=source_day, file_index=index, msg=msg, effect=effect,
                   order_before=before, order_after=None if after_order is None else asdict(after_order), frame=frame,
                   midnight_snapshot_not_applied=False, book=book, floor=floor)
        cursor += 1; group += closed
        return row
    for i, rec in enumerate(prior):
        if i < pskip: continue
        yield emit(rec, prior_day, i)
    result, block = carry_check(day, cur, ctake)            # the 00:00 UTC exchange snapshot inside the trade day
    receipt['midnight_utc_carry'] = result
    for i, rec, msg in block:
        yield dict(cursor=cursor, group=group if msg.is_last else None, utc_clock_day=day, file_index=i, msg=msg, effect=None,
                   order_before=None, order_after=None, frame=None, midnight_snapshot_not_applied=True, book=book, floor=floor)
        cursor += 1; group += msg.is_last
    for i, rec in enumerate(cur):
        if i == ctake: break
        if i < len(block): continue
        if int(rec.flags) & 32: raise ValueError('snapshot record after the opening block')
        yield emit(rec, day, i)
    adapter.assert_groups_closed()
    receipt.update(session_records=cursor, completed_groups=group, resting_orders_at_halt=len(book.orders),
                   resting_orders_at_halt_whose_priority_time_is_a_floor=len(floor), integrity=dict(book.integrity))
    if on_receipt: on_receipt(receipt)
