"""Oct 18, every trade individually. No rates, correlations or model scores.

1. LEDGER: one row per trade (all 30,739): designation (ids, cursors, clocks), the trade, the book just before it,
   the far side set by the prior 64 groups of flow, all 19 S values with their states, and what happened to THAT
   trade next: which came first, a k-tick move with the flow or against it (k=1,2,4), and how long it took.
2. TWINS: pairs of individual trades that looked the same on the fields already in the sheet (same far side, same
   part of day, identical spread, identical size and order count at the far touch, identical near-touch size, same
   trade side relative to flow), at least 60 s apart, where one continued and the other reversed. For every pair
   and every S field the two values are listed side by side. A field that reads the same on both trades of a pair
   says nothing about why those two trades went different ways.
"""
import numpy as np, pandas as pd
S = [f'S{i:02d}' for i in range(1, 20)]
df = pd.read_parquet('/home/user/work/out/s_test_frame_20231018.parquet')
src = pd.read_parquet('/home/user/work/out/flat_20231018.parquet')[['ordinal', 'cursor'] + [f'{s}_lc_state' for s in S]]
assert (src.cursor.values == df.cursor.values).all()
et = pd.to_datetime(df.receive_ns, utc=True).dt.tz_convert('America/New_York')
L = pd.DataFrame(dict(trade_id='20231018:trade:' + df.ordinal.astype(str), trade_ordinal=df.ordinal, trade_cursor=df.cursor,
    group_ordinal=df.group, event_ns=df.event_ns.astype(str), receive_ns=df.receive_ns.astype(str), known_by_ns=df.known_by_ns.astype(str),
    receive_time_ET=et.dt.strftime('%Y-%m-%d %H:%M:%S.%f'), day_part=df.part, price_raw=df.price, size=df['size'], aggressor_side=df.side,
    bid_price_raw=df.before_bid_price_raw, ask_price_raw=df.before_ask_price_raw, bid_size=df.before_bid_size, ask_size=df.before_ask_size,
    bid_orders=df.before_bid_orders, ask_orders=df.before_ask_orders, bid_full_size=df.before_bid_full_size, ask_full_size=df.before_ask_full_size,
    far_side=np.where(df.d > 0, 'A', np.where(df.d < 0, 'B', '')), flow_imbalance_64_groups=df.flow_imb))
for s in S:
    L[f'{s}_value'] = df[f'{s}_lc']; L[f'{s}_state'] = df[f'{s}_lc_state'] if f'{s}_lc_state' in df else src[f'{s}_lc_state'].values
for k in (1, 2, 4):
    y = df[f'y{k}'].values
    L[f'next_{k}tick_move'] = np.where(df.d == 0, 'no far side', np.where(y > 0, 'with flow', np.where(y < 0, 'against flow', 'not reached before settle/close')))
    L[f'seconds_to_{k}tick_move'] = df[f'lag_s{k}']
L.loc[df.part == 'settle', [f'next_{k}tick_move' for k in (1, 2, 4)]] = 'settle window: excluded'
L.to_csv('/home/user/work/out/oct18_trade_ledger.csv.gz', index=False)
print('ledger rows', len(L), 'cols', L.shape[1])

keys = ['part', 'd', 'spread_ticks', 'far_top_size', 'near_top_size', 'far_top_orders', 'trade_with_flow']
pairs = []
for k in (1, 2, 4):
    e = df[(df.d != 0) & (df.part != 'settle') & (df[f'y{k}'] != 0)]
    for key, g in e.groupby(keys):
        c = g[g[f'y{k}'] > 0]; r = g[g[f'y{k}'] < 0]
        if c.empty or r.empty: continue
        rt = r.receive_ns.values; used = np.zeros(len(r), bool)
        for i, t in zip(c.index, c.receive_ns.values):
            gap = np.abs(rt - t); ok = (~used) & (gap >= 60e9)
            if not ok.any(): continue
            j = np.argmin(np.where(ok, gap, np.inf)); used[j] = True
            pairs.append((k, i, r.index[j]))
P = pd.DataFrame(pairs, columns=['k', 'i_cont', 'i_rev'])
out = pd.DataFrame(dict(k=P.k.values, day_part=df.part.values[P.i_cont], far_side=np.where(df.d.values[P.i_cont] > 0, 'A', 'B'),
    continued_trade_id='20231018:trade:' + df.ordinal.astype(str).values[P.i_cont], reversed_trade_id='20231018:trade:' + df.ordinal.astype(str).values[P.i_rev],
    continued_time_ET=et.dt.strftime('%H:%M:%S.%f').values[P.i_cont], reversed_time_ET=et.dt.strftime('%H:%M:%S.%f').values[P.i_rev],
    spread_ticks=df.spread_ticks.values[P.i_cont], far_top_size=df.far_top_size.values[P.i_cont], near_top_size=df.near_top_size.values[P.i_cont],
    far_top_orders=df.far_top_orders.values[P.i_cont]))
for s in S:
    out[f'{s}_continued'] = df[f'{s}_lc'].values[P.i_cont]; out[f'{s}_reversed'] = df[f'{s}_lc'].values[P.i_rev]
out.to_csv('/home/user/work/out/oct18_twin_pairs.csv.gz', index=False)
print('twin pairs', out.groupby('k').size().to_dict(), 'trades in a pair at k=1:', 2 * int((out.k == 1).sum()))
rows = []
for s in S:
    for k in (1, 2, 4):
        o = out[out.k == k]; a, b = o[f'{s}_continued'].values, o[f'{s}_reversed'].values; m = ~np.isnan(a) & ~np.isnan(b)
        rows.append(dict(field=s, k=k, pairs_both_present=int(m.sum()), same_on_both=int((a[m] == b[m]).sum()),
                         higher_on_continued=int((a[m] > b[m]).sum()), higher_on_reversed=int((a[m] < b[m]).sum())))
T = pd.DataFrame(rows); T.to_csv('/home/user/work/out/oct18_twin_field_counts.csv', index=False)
pd.set_option('display.width', 200); print(T.pivot(index='field', columns='k', values=['pairs_both_present', 'same_on_both', 'higher_on_continued', 'higher_on_reversed']).to_string())
# per cell at k=1 and 2: how many of the 8 cells lean the same way
cell = []
for s in S:
    for k in (1, 2, 4):
        lean = []
        for (p, fs), o in out[out.k == k].groupby(['day_part', 'far_side']):
            a, b = o[f'{s}_continued'].values, o[f'{s}_reversed'].values; m = ~np.isnan(a) & ~np.isnan(b)
            hi, lo = int((a[m] > b[m]).sum()), int((a[m] < b[m]).sum())
            lean.append(f'{hi}/{lo}')
        cell.append(dict(field=s, k=k, per_cell_higher_on_continued_vs_reversed=' '.join(lean)))
pd.DataFrame(cell).to_csv('/home/user/work/out/oct18_twin_field_counts_by_cell.csv', index=False)
print(pd.DataFrame(cell)[lambda x: x.k == 1].to_string())
