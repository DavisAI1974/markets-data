"""What does the event time on a 00:00 UTC snapshot record mean? One row per resting order, no summary statistic.

For one pair of consecutive UTC clock-day tape files (prior, next):
  1. Replay the whole prior file with the pinned book adapter (unchanged rule: a new order, or a modify that changes
     price or raises size, sets the order's priority time; a size-down modify or a partial cancel keeps it).
  2. Beside the adapter, keep for every resting order the exchange EVENT time and sequence of the message that set its
     priority, of the message that first showed it, and of every later priority-keeping change.
  3. Read the snapshot block that opens the next file and write one row per order: the snapshot's event time and
     sequence next to what the replay holds.

IDs and clocks designate the order and its messages. Nothing here is an input to a market calculation.

usage: snapshot_event_time_check.py <prior UTC clock day> <next UTC clock day> <out dir>
"""
import csv, importlib, json, sys
import databento as db

sys.path.insert(0, '/home/user/work/pins/research')
A = importlib.import_module('ng_exhaustion_mbo_v4_state_adapter_20260820')
TAPE = '/home/user/markets-data/data/nymex_mbo/ng_v0_oct2023/'
PRIOR, NEXT, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
F_SNAPSHOT = 32


def utc(ns):
    if ns is None: return ''
    s, frac = divmod(int(ns), 10**9)
    import datetime
    return datetime.datetime.fromtimestamp(s, datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S') + f'.{frac:09d}'


adapter = A.V4MboAdapter()
info = {}                                   # order_id -> what the replay saw of this order
n = 0
for rec in db.DBNStore.from_file(TAPE + f'NG_v0_mbo_{PRIOR}.dbn.zst'):
    msg = adapter.normalize(rec, 'NGX3')
    book = adapter.books.get(msg.instrument_id)
    if book is None:
        book = adapter.books[msg.instrument_id] = A.InstrumentBook(msg.instrument_id)
    existed = msg.order_id in book.orders
    effect, _, _ = book.apply(msg)
    n += 1
    if msg.action == 'R':
        info.clear(); continue
    if msg.action not in ('A', 'M', 'C'): continue
    order = book.orders.get(msg.order_id)
    if order is None:                        # cancelled, or modified to zero
        info.pop(msg.order_id, None); continue
    stamp = dict(event_ns=msg.ts_event_ns, recv_ns=msg.ts_recv_ns, sequence=msg.sequence)
    sets_priority = msg.action == 'A' or (msg.action == 'M' and (effect.priority_lost or not existed))
    if sets_priority:
        kind = ('opening_block_of_prior_file' if msg.is_snapshot else 'live_add') if msg.action == 'A' else \
               ('priority_losing_modify' if existed else 'modify_of_unseen_order')
        first = info[msg.order_id]['first'] if existed and msg.order_id in info else dict(stamp, kind=kind)
        info[msg.order_id] = dict(first=first, priority=dict(stamp, kind=kind), keeps=[])
        if order.priority_recv_ns != msg.ts_recv_ns: raise ValueError('replay priority time does not follow this message')
    else:                                     # size-down modify or partial cancel: priority kept
        info[msg.order_id]['keeps'].append(dict(stamp, action=msg.action))
adapter.assert_groups_closed()
book = adapter.books[150611]
if set(info) != set(book.orders): raise ValueError('side ledger and adapter book hold different orders')

rows = []; snap_n = 0
for rec in db.DBNStore.from_file(TAPE + f'NG_v0_mbo_{NEXT}.dbn.zst'):
    if not (int(rec.flags) & F_SNAPSHOT): break
    snap_n += 1
    msg = adapter.normalize(rec, 'NGX3')
    if msg.action != 'A': continue
    o, i = book.orders.get(msg.order_id), info.get(msg.order_id)
    if o is None:
        rows.append(dict(order_id=msg.order_id, in_carried_book=False)); continue
    p, f, k = i['priority'], i['first'], i['keeps']
    last_keep = k[-1] if k else None
    rows.append(dict(
        order_id=msg.order_id, in_carried_book=True, side=msg.side, price_raw=msg.price_raw, size=msg.size,
        same_side_price_size=(o.side, o.price_raw, o.size) == (msg.side, msg.price_raw, msg.size),
        snapshot_event_ns=msg.ts_event_ns, snapshot_event_utc=utc(msg.ts_event_ns), snapshot_sequence=msg.sequence,
        replay_priority_set_by=p['kind'],
        replay_priority_event_ns=p['event_ns'], replay_priority_event_utc=utc(p['event_ns']),
        replay_priority_recv_ns=o.priority_recv_ns, replay_priority_recv_utc=utc(o.priority_recv_ns),
        replay_priority_sequence=o.priority_sequence,
        first_seen_by=f['kind'], first_seen_event_ns=f['event_ns'], first_seen_event_utc=utc(f['event_ns']),
        priority_keeping_changes_after=len(k),
        last_priority_keeping_change_action=last_keep['action'] if last_keep else '',
        last_priority_keeping_change_event_ns=last_keep['event_ns'] if last_keep else '',
        last_priority_keeping_change_event_utc=utc(last_keep['event_ns']) if last_keep else '',
        snapshot_event_equals_replay_priority_event=msg.ts_event_ns == p['event_ns'],
        snapshot_sequence_equals_replay_priority_sequence=msg.sequence == o.priority_sequence,
        snapshot_event_equals_first_seen_event=msg.ts_event_ns == f['event_ns'],
        snapshot_event_equals_last_priority_keeping_change=bool(last_keep) and msg.ts_event_ns == last_keep['event_ns'],
        priority_was_reset_after_first_seen=p['event_ns'] != f['event_ns'] or p['sequence'] != f['sequence'],
        replay_priority_recv_minus_snapshot_event_ns=o.priority_recv_ns - msg.ts_event_ns))

name = f'{OUT}/snapshot_orders_{PRIOR}_to_{NEXT}'
cols = max(rows, key=len).keys()
with open(name + '.csv', 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=list(cols)); w.writeheader(); w.writerows(rows)

R = [r for r in rows if r['in_carried_book']]
count = lambda pred: sum(1 for r in R if pred(r))
reset = [r for r in R if r['priority_was_reset_after_first_seen']]
kept = [r for r in R if r['priority_keeping_changes_after']]
receipt = dict(
    prior_utc_clock_day=PRIOR, next_utc_clock_day=NEXT, prior_file_records=n, snapshot_block_records=snap_n,
    snapshot_orders=len(rows), snapshot_orders_in_carried_book=len(R), carried_orders=len(book.orders),
    same_side_price_size=count(lambda r: r['same_side_price_size']),
    counts_of_individual_orders=dict(
        snapshot_event_equals_replay_priority_event=count(lambda r: r['snapshot_event_equals_replay_priority_event']),
        snapshot_event_differs_from_replay_priority_event=count(lambda r: not r['snapshot_event_equals_replay_priority_event']),
        snapshot_sequence_equals_replay_priority_sequence=count(lambda r: r['snapshot_sequence_equals_replay_priority_sequence']),
        orders_whose_priority_was_reset_after_first_seen=len(reset),
        of_those_snapshot_event_equals_the_reset_event=sum(r['snapshot_event_equals_replay_priority_event'] for r in reset),
        of_those_snapshot_event_equals_the_first_seen_event=sum(r['snapshot_event_equals_first_seen_event'] for r in reset),
        orders_with_priority_keeping_changes_after_priority_was_set=len(kept),
        of_those_snapshot_event_equals_replay_priority_event=sum(r['snapshot_event_equals_replay_priority_event'] for r in kept),
        of_those_snapshot_event_equals_the_last_priority_keeping_change=sum(r['snapshot_event_equals_last_priority_keeping_change'] for r in kept),
        priority_set_by={k: count(lambda r, k=k: r['replay_priority_set_by'] == k) for k in sorted({r['replay_priority_set_by'] for r in R})},
        replay_priority_recv_more_than_1s_after_snapshot_event=count(lambda r: r['replay_priority_recv_minus_snapshot_event_ns'] > 10**9),
        replay_priority_recv_before_snapshot_event=count(lambda r: r['replay_priority_recv_minus_snapshot_event_ns'] < 0)),
    per_order_file=name.split('/')[-1] + '.csv')
json.dump(receipt, open(name + '_RECEIPT.json', 'w'), indent=1)
print(json.dumps(receipt, indent=1))
