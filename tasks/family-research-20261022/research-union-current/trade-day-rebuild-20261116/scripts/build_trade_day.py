"""Build one trade day and verify it against what already exists.

Checks, each counted and written to the receipt:
  1. Every message equals the archived message at the mapped cursor (archive = book-recovery branch for that date).
  2. Every non-snapshot effect equals the archived effect; the order after each message equals the archived order
     except for its priority time (which is what carrying across 00:00 UTC is meant to change).
  3. Every trade already in the trade list is found at the mapped cursor and group, with identical clocks, price,
     size, side, order id and sequence. Trades in the newly covered evening hours are listed as new.
"""
import gzip, io, json, subprocess, sys, time
from dataclasses import asdict
import pandas as pd, pyarrow.parquet as pq
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from trade_day_stream import trade_day
DAY, OUT = sys.argv[1], sys.argv[2]
REPO = '/home/user/markets-data'
ARCH = {'20231002': '7eebebadef89c4281cdb25c236ac39f5da814839', '20231003': '010a9970ff23e981b9870350177bb9ace7a3100b',
        '20231017': 'f41a7de50c19ffc5875690542f87dac7d9cd90b3', '20231018': '02ea4b6e340ed1b35a43be23fe21bd01fc82c66f'}[DAY]
SRC = f'tasks/family-research-20261022/frankie-four-day-pins/book-recovery-42617700678-1/{DAY}'
TRADE_REV = '87dc338f2e74646eb731b3cd6f8968a5a0a653e2'
show = lambda rev, path: subprocess.check_output(['git', '-C', REPO, 'show', f'{rev}:{path}'])
t0 = time.time()
arch_receipt = json.loads(show(ARCH, SRC + '/RECOVERY_RECEIPT.json')); o = arch_receipt['original_replay_receipt']
partial = o.get('scope') == 'PARTIAL_TRADE_DATE'
shards = [f for f in json.loads(show(ARCH, SRC + '/MANIFEST.json'))['files'] if f['path'].startswith('native-messages-')]
def archive_rows():
    for f in shards:
        for line in gzip.GzipFile(fileobj=io.BytesIO(show(ARCH, SRC + '/' + f['path']))):
            yield json.loads(line)
old_trades = pq.read_table(io.BytesIO(show(TRADE_REV, f'tasks/family-research-20261022/combined-events/run-42571551209-1/events-{DAY}/a-trades.parquet'))).to_pylist()
old_by_cursor = {int(t['trade_input_cursor']): t for t in old_trades}
assert len(old_by_cursor) == len(old_trades)
receipt = {}
arch = archive_rows(); arch_skip = None; next_arch = None
C = dict(messages=0, archive_rows_compared=0, message_equal=0, effect_equal=0, order_after_equal=0, order_after_equal_except_priority_time=0,
         order_after_other_difference=0, snapshot_rows_not_applied=0, new_evening_messages=0)
trades = []; pending = []; examples = []
for row in trade_day(DAY, on_receipt=receipt.update):
    msg = row['msg']; C['messages'] += 1
    if arch_skip is None:                                  # where does the archive start relative to this trade day?
        # full-session archives hold the warm-up first, then the session from cursor 0; partial ones start at 00:00 UTC
        arch_skip = 0
        if not partial:
            for _ in range(o['opening_warmup_records']): next(arch)
    in_archive = (not partial) or row['utc_clock_day'] == DAY
    if in_archive:
        a = next(arch); C['archive_rows_compared'] += 1
        if 'first_archive_cursor_offset' not in receipt: receipt['first_archive_cursor_offset'] = row['cursor'] - a['adapter_input_cursor']
        assert row['cursor'] - a['adapter_input_cursor'] == receipt['first_archive_cursor_offset']
        me = msg.public_dict() == a['original_message']; C['message_equal'] += me
        if not me: raise ValueError(f"message differs at trade-day cursor {row['cursor']}")
        if row['midnight_snapshot_not_applied']:
            C['snapshot_rows_not_applied'] += 1
        else:
            C['effect_equal'] += asdict(row['effect']) == a['original_effect']
            x, y = row['order_after'], a['resting_order_after']
            if x == y: C['order_after_equal'] += 1
            elif x is not None and y is not None and {k: v for k, v in x.items() if k != 'priority_recv_ns'} == {k: v for k, v in y.items() if k != 'priority_recv_ns'}:
                C['order_after_equal_except_priority_time'] += 1
            else:
                C['order_after_other_difference'] += 1
                if len(examples) < 5: examples.append(dict(cursor=row['cursor'], ours=x, archive=y, effect=asdict(row['effect']), archive_effect=a['original_effect']))
    else:
        C['new_evening_messages'] += 1
    if msg.action == 'T':
        pending.append(dict(trade_day=DAY, trade_cursor=row['cursor'], utc_clock_day_file=row['utc_clock_day'], file_index=row['file_index'],
                            event_ns=msg.ts_event_ns, receive_ns=msg.ts_recv_ns, price_raw=msg.price_raw, size=msg.size, aggressor_side=msg.side,
                            order_id=msg.order_id, sequence=msg.sequence, flags=msg.flags))
    if row['group'] is not None and not row['midnight_snapshot_not_applied']:
        for t in pending: t.update(group_ordinal=row['group'], group_close_cursor=row['cursor'], available_ns=msg.ts_recv_ns)
        trades.extend(pending); pending = []
    if C['messages'] % 200000 == 0: print(DAY, C['messages'], round(time.time() - t0), 's', flush=True)
assert not pending and next(arch, None) is None
T = pd.DataFrame(trades)
found = same = 0; off = receipt.get('first_archive_cursor_offset', 0); prior_ord = []; prior_cur = []
for t in trades:
    old = old_by_cursor.get(t['trade_cursor'] - off)
    prior_ord.append(None if old is None else old.get('source_ordinal')); prior_cur.append(None if old is None else int(old['trade_input_cursor']))
    if old is None: continue
    found += 1
    same += (int(old['trade_input_cursor']) + off == t['trade_cursor'] and int(old['group_close_input_cursor']) + off == t['group_close_cursor']
             and int(old['receive_ns']) == t['receive_ns'] and int(old['sequence']) == t['sequence'] and int(old['order_id']) == t['order_id']
             and int(old['event_ns']) == t['event_ns'] and int(old['price_raw']) == t['price_raw'] and int(old['size']) == t['size']
             and old['aggressor_side'] == t['aggressor_side'] and int(old['available_ns']) == t['available_ns'])
T['prior_archive_trade_cursor'] = pd.array(prior_cur, dtype='Int64'); T['in_prior_trade_list'] = T.prior_archive_trade_cursor.notna()
old_groups = {int(t['trade_input_cursor']): int(t['group_ordinal']) for t in old_trades}
g = T[T.in_prior_trade_list]; goff = (g.group_ordinal - g.prior_archive_trade_cursor.map(old_groups)).unique().tolist()
T.insert(1, 'trade_ordinal', range(len(T)))
T.to_parquet(f'{OUT}/trade_day_{DAY}_trades.parquet', index=False)
receipt.update(counts=C, trades_in_trade_day=len(T), trades_in_prior_trade_list=len(old_trades), prior_trades_found=found,
               prior_trades_identical_at_mapped_cursor=same, new_trades_not_in_prior_list=int((~T.in_prior_trade_list).sum()),
               cursor_offset_new_minus_prior=off, group_ordinal_offsets_new_minus_prior=goff, order_after_difference_examples=examples,
               prior_archive=dict(revision=ARCH, path=SRC, scope=arch_receipt['scope']), wall_seconds=round(time.time() - t0, 1))
json.dump(receipt, open(f'{OUT}/trade_day_{DAY}_RECEIPT.json', 'w'), indent=1)
print(json.dumps({k: receipt[k] for k in ('trade_day', 'session_records', 'completed_groups', 'midnight_utc_carry', 'counts', 'trades_in_trade_day',
      'prior_trades_found', 'prior_trades_identical_at_mapped_cursor', 'new_trades_not_in_prior_list', 'cursor_offset_new_minus_prior',
      'group_ordinal_offsets_new_minus_prior', 'wall_seconds')}, indent=1))
