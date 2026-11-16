"""Does the book carried through the prior UTC file equal the exchange snapshot that opens the next UTC file?
Compares content (order id, side, price, size) and queue order per price level. Pinned adapter, unchanged."""
import sys, json, importlib, collections
sys.path.insert(0, '/home/user/work/pins/research')
import databento as db
A = importlib.import_module('ng_exhaustion_mbo_v4_state_adapter_20260820')
D = '/home/user/markets-data/data/nymex_mbo/ng_v0_oct2023/'
def run(prior, nxt):
    ad = A.V4MboAdapter()
    for rec in db.DBNStore.from_file(D + f'NG_v0_mbo_{prior}.dbn.zst'):
        ad.apply(rec, 'NGX3')
    book = ad.books[150611]
    carried = {oid: (o.side, o.price_raw, o.size, o.priority_recv_ns) for oid, o in book.orders.items()}
    carried_q = {(s, p): list(q) for s in ('B', 'A') for p, q in book.levels[s].items()}
    snap = {}; snap_q = collections.defaultdict(list); n = 0; ts_event = {}
    for rec in db.DBNStore.from_file(D + f'NG_v0_mbo_{nxt}.dbn.zst'):
        if not (int(rec.flags) & 32): break
        n += 1
        act = rec.action.value if hasattr(rec.action, 'value') else str(rec.action)
        if act == 'A':
            side = rec.side.value if hasattr(rec.side, 'value') else str(rec.side)
            snap[rec.order_id] = (side, int(rec.price), int(rec.size)); snap_q[(side, int(rec.price))].append(rec.order_id); ts_event[rec.order_id] = int(rec.ts_event)
    same_ids = set(carried) == set(snap)
    content = sum(1 for o in snap if o in carried and carried[o][:3] == snap[o])
    q_equal = sum(1 for k, q in snap_q.items() if carried_q.get(k) == q)
    # do snapshot records keep each order's original event time, and does it equal the carried priority time?
    prio_eq = sum(1 for o in snap if o in carried and carried[o][3] == ts_event[o])
    older = sum(1 for o in snap if o in carried and ts_event[o] < carried[o][3])
    return dict(prior=prior, next=nxt, snapshot_records=n, snapshot_orders=len(snap), carried_orders=len(carried), same_order_ids=same_ids,
                only_in_carried=len(set(carried) - set(snap)), only_in_snapshot=len(set(snap) - set(carried)), same_side_price_size=content,
                price_levels=len(snap_q), levels_with_identical_queue_order=q_equal,
                snapshot_event_time_equals_carried_priority_time=prio_eq, snapshot_event_time_older_than_carried=older)
for a, b in (('20231001', '20231002'), ('20231002', '20231003'), ('20231016', '20231017'), ('20231017', '20231018')):
    print(json.dumps(run(a, b)), flush=True)
