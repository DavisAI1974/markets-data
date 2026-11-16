"""The book record at every trade of one trade day, on the carried book.

One row per trade, taken when the trade message arrives (before any later message): the full book on both sides,
every price level's FIFO queue with each order's size, priority time, age and volume ahead, the adapter's rolling
activity, and its integrity counters. Built with the pinned adapter's own `book_snapshot` and `rolling_activity`,
unchanged. The book is the trade-day book: warmed from the Sunday open and carried straight through every 00:00 UTC.

Added to what the adapter returns, because the tape cannot show an older time for these orders:
  on each order      priority_age_is_lower_bound   the order is one the exchange re-listed on Sunday (or otherwise
                                                   predates the tape); its real age is at least priority_age_s
  on each level      front_order_age_is_lower_bound, queue_age_lower_bound_orders
  on the row         lower_bound_orders_in_book

Checks made on every row (the run stops if one fails): the trade is the next trade of the trade-day trade list, with
identical cursor, clocks, price, size, side, order id and sequence; level sizes sum to the side's depth; volume ahead
accumulates exactly along each queue; each queue's length equals the level's order count; the queues hold every
resting order exactly once.

usage: build_book_records.py <trade day YYYYMMDD> <out dir> [first N trades only]
"""
import gzip, hashlib, json, os, pathlib, sys, time
import pyarrow.parquet as pq

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from trade_day_stream import trade_day

DAY, OUT = sys.argv[1], pathlib.Path(sys.argv[2])
LIMIT = int(sys.argv[3]) if len(sys.argv) > 3 else None
OUT.mkdir(parents=True, exist_ok=False)
DESIGNATION = ('trade_day', 'trade_ordinal', 'trade_cursor', 'utc_clock_day_file', 'file_index', 'event_ns', 'receive_ns', 'price_raw',
               'size', 'aggressor_side', 'order_id', 'sequence', 'flags', 'group_ordinal', 'group_close_cursor', 'available_ns')
trades = pq.read_table(f'{HERE}/../results/trade_day_{DAY}_trades.parquet', columns=list(DESIGNATION)).to_pylist()
ROWS_PER_SHARD = 100


class Shards:
    def __init__(self):
        self.rows = self.part = 0; self.stream = None; self.files = []
    def write(self, row):
        if self.stream is None or self.rows % ROWS_PER_SHARD == 0:
            self.close()
            self.path = OUT / f'trade-book-fifo-{self.part:04d}.jsonl.gz'
            self.stream = gzip.GzipFile(filename=str(self.path), mode='wb', compresslevel=3, mtime=0)
            self.part += 1; self.part_rows = 0
        self.stream.write((json.dumps(row, separators=(',', ':'), allow_nan=False) + '\n').encode())
        self.part_rows += 1; self.rows += 1
    def close(self):
        if self.stream is None: return
        self.stream.close(); data = self.path.read_bytes()
        self.files.append(dict(path=self.path.name, rows=self.part_rows, bytes=len(data), sha256=hashlib.sha256(data).hexdigest()))
        self.stream = None


out = Shards(); receipt = {}; n = 0; t0 = time.time()
C = dict(trades_with_lower_bound_orders_in_book=0, trades_whose_best_bid_front_order_age_is_a_lower_bound=0,
         trades_whose_best_ask_front_order_age_is_a_lower_bound=0, trade_price_at_best_opposite=0, trade_price_through_best_opposite=0,
         trade_price_inside_spread=0, trade_with_empty_opposite_side=0, trade_without_aggressor_side=0)
for row in trade_day(DAY, on_receipt=receipt.update):
    msg = row['msg']
    if msg.action != 'T': continue
    if LIMIT is not None and n >= LIMIT: break
    t = trades[n]
    seen = (row['cursor'], msg.ts_recv_ns, msg.ts_event_ns, msg.sequence, msg.order_id, msg.price_raw, msg.size, msg.side)
    want = tuple(t[k] for k in ('trade_cursor', 'receive_ns', 'event_ns', 'sequence', 'order_id', 'price_raw', 'size', 'aggressor_side'))
    if seen != want or t['trade_ordinal'] != n: raise ValueError(f'{DAY}: trade {n} differs from the trade-day trade list: {seen} {want}')
    book, floor = row['book'], row['floor']
    full = book.book_snapshot(msg.ts_recv_ns, depth_levels=10, include_full_depth=True, include_order_ids=True)
    queued = 0; lower = 0
    for side in ('bid', 'ask'):
        levels = full[side + '_levels_full']
        if sum(level['size'] for level in levels) != full[side + '_depth_full']: raise ValueError('level sizes do not sum to depth')
        for level in levels:
            ahead = 0; level_lower = 0
            for entry in level['fifo_queue']:
                if entry['volume_ahead'] != ahead: raise ValueError('volume ahead does not accumulate along the queue')
                ahead += entry['size']; queued += 1
                entry['priority_age_is_lower_bound'] = entry['order_id'] in floor
                level_lower += entry['priority_age_is_lower_bound']
            if ahead != level['size'] or len(level['fifo_queue']) != level['order_count']: raise ValueError('queue does not match its level')
            level['front_order_age_is_lower_bound'] = bool(level['fifo_queue']) and level['fifo_queue'][0]['priority_age_is_lower_bound']
            level['queue_age_lower_bound_orders'] = level_lower; lower += level_lower
    if queued != len(book.orders): raise ValueError('queues do not hold every resting order exactly once')
    if lower != sum(1 for o in floor if o in book.orders): raise ValueError('lower-bound marks do not match the floor list')
    C['trades_with_lower_bound_orders_in_book'] += lower > 0
    for side in ('bid', 'ask'):
        levels = full[side + '_levels_full']
        C[f'trades_whose_best_{side}_front_order_age_is_a_lower_bound'] += bool(levels) and levels[0]['front_order_age_is_lower_bound']
    best = book.best_price_raw('A' if msg.side == 'B' else 'B') if msg.side in ('A', 'B') else None
    if msg.side not in ('A', 'B'): C['trade_without_aggressor_side'] += 1
    elif best is None: C['trade_with_empty_opposite_side'] += 1
    elif msg.price_raw == best: C['trade_price_at_best_opposite'] += 1
    elif (msg.side == 'B') == (msg.price_raw > best): C['trade_price_through_best_opposite'] += 1
    else: C['trade_price_inside_spread'] += 1
    out.write(dict(day=DAY, trade_ordinal=n, source_stream_ordinal=row['cursor'], original_trade=t, known_by_ns=msg.ts_recv_ns,
                   phase='at_trade_input', book_full=full, lower_bound_orders_in_book=lower, activity=book.rolling_activity(msg.ts_recv_ns),
                   integrity=dict(book.integrity), fifo_priority_reconstructed=True, native_priority_id_exposed=False))
    n += 1
    if n % 5000 == 0: print(DAY, n, 'trades', round(time.time() - t0), 's', flush=True)
out.close()
if LIMIT is None and n != len(trades): raise ValueError(f'{DAY}: wrote {n} records for {len(trades)} trades')
manifest = dict(trade_day=DAY, rows_per_shard=ROWS_PER_SHARD, files=out.files)
json.dump(manifest, open(OUT / 'MANIFEST.json', 'w'), indent=1)
json.dump(dict(schema='TRADE_DAY_BOOK_RECORDS_V1', trade_day=DAY, trades_in_trade_day=len(trades), records_written=n, first_trades_only=LIMIT,
               shards=len(out.files), bytes=sum(f['bytes'] for f in out.files), snapshot_phase='at trade input; the book before any later message',
               book='trade-day book: warmed from the Sunday open, carried through every 00:00 UTC, no opening snapshot applied after the first',
               counts=C, stream_receipt=receipt if LIMIT is None else None, wall_seconds=round(time.time() - t0, 1)),
          open(OUT / 'BOOK_RECEIPT.json', 'w'), indent=1)
print(json.dumps(dict(trade_day=DAY, records=n, shards=len(out.files), megabytes=round(sum(f['bytes'] for f in out.files) / 1e6, 1), counts=C,
                      wall_seconds=round(time.time() - t0, 1))))
