"""Sample only (a dry run in the session, nothing stored): tick-timed lines against the 20-second line.

Four separate graphs on one time axis of real timestamps:
  1. price: the best bid, the best ask, every trade
  2. TICK-TIMED: the running total of lots bought minus lots sold (each trade its own step; no window)
  3. TICK-TIMED: the lean of every resting bid against every resting ask (whole book; no window)
  4. VALIDATION ONLY: the 20-second flow (bought minus sold over bought plus sold, last 20 seconds)
usage: tick_against_20s_sample.py <folder> <trade day> <part> <out folder> <first trade number> <trades> ...
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

cols = ['received_time_ns', 'action', 'side', 'price', 'size', 'position_on_tape', 'best_bid', 'best_ask',
        'bid_total_size', 'ask_total_size']
r = pq.read_table(f'{folder}/rows-{day}-{part}.parquet', columns=cols).to_pandas()
f = pq.read_table(f'{folder}/calc-flow_peak-{day}-{part}.parquet', columns=['position_on_tape', 'flow_20s']).to_pandas()
assert (r.position_on_tape.values == f.position_on_tape.values).all()
r['flow_20s'] = f.flow_20s.values
is_trade = r.action.values == 'T'
signed = np.where(is_trade & (r.side.values == 'B'), r['size'].values, 0.0) - np.where(
    is_trade & (r.side.values == 'A'), r['size'].values, 0.0)
r['running'] = np.cumsum(signed)
trade_rows = np.flatnonzero(is_trade)


def clock(ns):
    return datetime.fromtimestamp(ns / UNIT, EASTERN)


def draw(first, count):
    a, b = trade_rows[first], trade_rows[first + count - 1]
    w = r.iloc[max(0, a - 1):b + 2]
    x = [clock(v) for v in w.received_time_ns.values]
    fig, ax = plt.subplots(4, 1, figsize=(7.2, 14.0), sharex=True, gridspec_kw={'hspace': 0.2})

    ax[0].step(x, w.best_ask.values / UNIT, where='post', color='#b03a2e', lw=1.0, label='best ask')
    ax[0].step(x, w.best_bid.values / UNIT, where='post', color='#1f618d', lw=1.0, label='best bid')
    tr = w[w.action.values == 'T']
    ax[0].scatter([clock(v) for v in tr.received_time_ns.values], tr.price.values / UNIT, s=10, color='#17202a',
                  zorder=3, label='trade')
    ax[0].set_ylabel('price, dollars')
    ax[0].set_title('1. PRICE: best bid, best ask, every trade', loc='left', fontsize=11)
    ax[0].legend(fontsize=7, ncol=3, loc='best')

    run = w.running.values - w.running.values[0]
    ax[1].step(x, run, where='post', color='#117a65', lw=1.2)
    ax[1].axhline(0, color='#aab7b8', lw=0.8)
    ax[1].set_ylabel('lots bought minus lots sold,\ncounted from the left edge')
    ax[1].set_title('2. TICK-TIMED. The hitting side: running total, one step per trade (no window)', loc='left',
                    fontsize=11)

    bs, as_ = w.bid_total_size.values.astype(float), w.ask_total_size.values.astype(float)
    ax[2].step(x, (bs - as_) / (bs + as_), where='post', color='#ca6f1e', lw=1.0)
    ax[2].set_ylabel('lean of the whole book\n(+1 all bid, -1 all ask)')
    ax[2].set_title('3. TICK-TIMED. The standing side: every resting bid against every resting ask', loc='left',
                    fontsize=11)

    ax[3].step(x, w.flow_20s.values, where='post', color='#7f8c8d', lw=1.0)
    ax[3].axhline(0, color='#aab7b8', lw=0.8)
    ax[3].set_ylim(-1.05, 1.05)
    ax[3].set_ylabel('20-second flow\n(+1 all buying, -1 all selling)')
    ax[3].set_title('4. VALIDATION ONLY, never a signal: the 20-second flow (the old exhaustion line)', loc='left',
                    fontsize=11)
    ax[3].set_xlabel('Eastern time (the received clock)')
    for g in ax:
        g.grid(alpha=0.25)
        g.tick_params(labelsize=8)
    span = (w.received_time_ns.values[-1] - w.received_time_ns.values[0]) / UNIT
    fig.suptitle(f'Trade day Tue Oct 17, 2023. SAMPLE, not stored.\n{count} trades, {len(w):,} ticks, {span:,.1f} s, '
                 f'from {x[0].strftime("%H:%M:%S.%f")[:-3]} Eastern', fontsize=11, y=0.975)
    fig.autofmt_xdate(rotation=30)
    name = f'{out}/tick_against_20s_{day}_{first}_{count}.png'
    fig.savefig(name, dpi=110, bbox_inches='tight')
    plt.close(fig)
    print(name)


for first, count in jobs:
    draw(first, count)
