"""Sample only (a dry run in the session, nothing stored): the three-tier picture from stored files.

Three separate graphs on one time axis of real timestamps, nothing made on the 20-second window:
  1. price: the best bid, the best ask, every trade
  2. the hitting side: the run of trades on one side, as it grows trade by trade (buying up, selling down)
  3. the standing side: the lean of the resting orders at the best prices
usage: three_tier_sample.py <folder with the stored files> <trade day> <part> <out folder> <first trade number> <trades> ...
"""
import sys
from datetime import datetime, timedelta, timezone

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pyarrow.parquet as pq

folder, day, part, out = sys.argv[1:5]
jobs = [(int(a), int(b)) for a, b in zip(sys.argv[5::2], sys.argv[6::2])]
EASTERN = timezone(timedelta(hours=-4))                      # October 2023: Eastern daylight time
UNIT = 10 ** 9

cols = ['received_time_ns', 'action', 'side', 'price', 'size', 'row_label', 'position_on_tape', 'best_bid', 'best_ask',
        'best_bid_size', 'best_ask_size', 'bid_total_size', 'ask_total_size', 'in_settlement_window']
r = pq.read_table(f'{folder}/rows-{day}-{part}.parquet', columns=cols).to_pandas()
t = pq.read_table(f'{folder}/calc-turn_peaks-{day}-{part}.parquet').to_pandas()
assert (r.position_on_tape.values == t.position_on_tape.values).all()
r['run_side'], r['run_size'] = t.run_side.values, t.run_size.values
print('labels', r.row_label.value_counts().to_dict(), 'run sides', t.run_side.dropna().unique()[:6])
trade_rows = np.flatnonzero((r.action.values == 'T'))
print('trades in this part', len(trade_rows))


def clock(ns):
    return datetime.fromtimestamp(ns / UNIT, EASTERN)


def draw(first, count):
    a, b = trade_rows[first], trade_rows[first + count - 1]
    lo = max(0, a - 1)
    w = r.iloc[lo:b + 2]
    x = [clock(v) for v in w.received_time_ns.values]
    fig, ax = plt.subplots(3, 1, figsize=(7.2, 11.5), sharex=True, gridspec_kw={'hspace': 0.16})

    bid, ask = w.best_bid.values / UNIT, w.best_ask.values / UNIT
    ax[0].step(x, ask, where='post', color='#b03a2e', lw=1.0, label='best ask')
    ax[0].step(x, bid, where='post', color='#1f618d', lw=1.0, label='best bid')
    tr = w[w.action.values == 'T']
    tx = [clock(v) for v in tr.received_time_ns.values]
    for side, colour, name in (('B', '#117a65', 'trade, buyer hitting'), ('A', '#884ea0', 'trade, seller hitting'),
                               ('N', '#7f8c8d', 'trade, no side')):
        m = tr.side.values == side
        if m.any():
            ax[0].scatter(np.array(tx)[m], tr.price.values[m] / UNIT, s=18, color=colour, zorder=3, label=name)
    ax[0].set_ylabel('price, dollars')
    ax[0].set_title('1. PRICE: best bid, best ask, every trade', loc='left', fontsize=11)
    ax[0].legend(fontsize=7, ncol=2, loc='best')

    sign = np.where(w.run_side.astype(str).str.lower().str.startswith('b'), 1.0, -1.0)
    run = np.where(w.run_size.isna().values, np.nan, sign * w.run_size.fillna(0).values)
    ax[1].step(x, run, where='post', color='#17202a', lw=1.1)
    ax[1].axhline(0, color='#aab7b8', lw=0.8)
    ax[1].set_ylabel('lots in the run\n(buying up, selling down)')
    ax[1].set_title('2. THE HITTING SIDE: the run of trades on one side, trade by trade (no window)', loc='left',
                    fontsize=11)

    bs, as_ = w.bid_total_size.values.astype(float), w.ask_total_size.values.astype(float)
    lean = (bs - as_) / (bs + as_)
    ax[2].step(x, lean, where='post', color='#ca6f1e', lw=0.9)
    ax[2].axhline(0, color='#aab7b8', lw=0.8)
    pass
    ax[2].set_ylabel('lean of the resting orders\nin the whole book\n(+1 all bid, -1 all ask)')
    ax[2].set_title('3. THE STANDING SIDE: every resting bid against every resting ask (whole book), every tick',
                    loc='left', fontsize=11)
    ax[2].set_xlabel('Eastern time (the received clock)')
    for g in ax:
        g.grid(alpha=0.25)
        g.tick_params(labelsize=8)
    span = (w.received_time_ns.values[-1] - w.received_time_ns.values[0]) / UNIT
    fig.suptitle(f'Trade day Tue Oct 17, 2023. SAMPLE, not stored.\n{count} trades, {len(w):,} ticks, {span:,.1f} s, '
                 f'from {x[0].strftime("%H:%M:%S.%f")[:-3]} Eastern', fontsize=11, y=0.985)
    fig.autofmt_xdate(rotation=30)
    name = f'{out}/three_tier_wholebook_{day}_{first}_{count}.png'
    fig.savefig(name, dpi=110, bbox_inches='tight')
    plt.close(fig)
    print(name, 'settlement window rows:', int(w.in_settlement_window.fillna(False).astype(bool).sum()),
          'first', x[0], 'last', x[-1])


for first, count in jobs:
    draw(first, count)
