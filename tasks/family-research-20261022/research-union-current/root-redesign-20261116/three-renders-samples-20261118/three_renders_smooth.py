"""Sample only (a dry run in the session, nothing stored): Greg's three renders, timed at the tick.

Three separate graphs on one time axis of real timestamps. No window of any kind.
  1. the trade price curve: the price of every trade, joined in time order
  2. the dipole at the tick: buying against selling, the run of trades under way against the run it took over from
  3. the exhaustion at the tick: the run of trades on one side as it builds, with its high (its last trade)
usage: three_renders_nano.py <folder> <trade day> <part> <out folder> <first trade number> <trades> ...
"""
import sys
from datetime import datetime, timedelta, timezone

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pyarrow.parquet as pq
from scipy.interpolate import PchipInterpolator

folder, day, part, out = sys.argv[1:5]
jobs = [(int(a), int(b)) for a, b in zip(sys.argv[5::2], sys.argv[6::2])]
EASTERN = timezone(timedelta(hours=-4))                      # October 2023: Eastern daylight time
UNIT = 10 ** 9

r = pq.read_table(f'{folder}/rows-{day}-{part}.parquet',
                  columns=['received_time_ns', 'action', 'side', 'price', 'size', 'position_on_tape']).to_pandas()
t = pq.read_table(f'{folder}/calc-turn_peaks-{day}-{part}.parquet').to_pandas()
assert (r.position_on_tape.values == t.position_on_tape.values).all()
is_trade = r.action.values == 'T'
trade_rows = np.flatnonzero(is_trade)

# the run of trades on one side, as stored (the peak with no window): its side, its size so far, its first trade
side = np.where(t.run_side.astype(str).str.startswith('b'), 1.0, -1.0)
size = t.run_size.values.astype(float)
first = t.run_first_trade_position.values
known = ~np.isnan(size)
# the run before the one under way: its size at its last trade (its high)
change = np.flatnonzero(known[1:] & known[:-1] & (first[1:] != first[:-1])) + 1
before = np.full(len(size), np.nan)
for i, c in enumerate(change):
    end = change[i + 1] if i + 1 < len(change) else len(size)
    before[c:end] = size[c - 1]
bought = np.where(side > 0, size, before)
sold = np.where(side > 0, before, size)
dipole = (bought - sold) / (bought + sold)                    # empty until there is a run before this one
exhaustion = side * size
highs = change - 1                                            # the row holding each ended run's last size


def clock(ns):
    return datetime.fromtimestamp(ns / UNIT, EASTERN)


def draw(first_trade, count):
    a, b = trade_rows[first_trade], trade_rows[first_trade + count - 1]
    lo, hi = max(0, a - 1), b + 2
    w = r.iloc[lo:hi]
    x = np.array([clock(v) for v in w.received_time_ns.values])
    tr = (w.action.values == 'T')
    fig, ax = plt.subplots(3, 1, figsize=(7.2, 11.5), sharex=True, gridspec_kw={'hspace': 0.17})

    tns, tpx = w.received_time_ns.values[tr].astype(float), w.price.values[tr] / UNIT
    last = np.append(np.diff(tns) > 0, True)                  # the last trade of each instant
    shared = int((~last).sum())
    curve = PchipInterpolator(tns[last], tpx[last])           # passes through every one of those trades exactly
    grid = np.linspace(tns[0], tns[-1], 4000)
    ax[0].plot([clock(v) for v in grid], curve(grid), color='#b03a2e', lw=1.4)
    ax[0].scatter(x[tr], tpx, s=5, color='#17202a', zorder=3)
    ax[0].set_ylabel('trade price, dollars')
    ax[0].set_title('1. THE TRADE PRICE CURVE, drawn smooth: through every trade, nothing averaged', loc='left',
                    fontsize=11)
    print('trades', int(tr.sum()), 'sharing an instant with a later trade', shared)

    ax[1].step(x, dipole[lo:hi], where='post', color='#1f618d', lw=1.0)
    ax[1].axhline(0, color='#aab7b8', lw=0.8)
    ax[1].set_ylim(-1.05, 1.05)
    ax[1].set_ylabel('buying against selling\n(+1 all buying, -1 all selling)')
    ax[1].set_title('2. THE DIPOLE, at the tick: the run of trades under way against the run before it', loc='left',
                    fontsize=11)

    ax[2].step(x, exhaustion[lo:hi], where='post', color='#17202a', lw=1.0)
    h = highs[(highs >= lo) & (highs < hi)]
    ax[2].scatter([clock(v) for v in r.received_time_ns.values[h]], exhaustion[h], s=14, color='#ca6f1e', zorder=3,
                  label='the high of a run (its last trade): the peak with no window')
    ax[2].axhline(0, color='#aab7b8', lw=0.8)
    ax[2].set_ylabel('lots in the run\n(buying up, selling down)')
    ax[2].set_title('3. THE EXHAUSTION, at the tick: each run of trades on one side, built trade by trade',
                    loc='left', fontsize=11)
    ax[2].legend(fontsize=7, loc='best')
    ax[2].set_xlabel('Eastern time (the received clock)')
    for g in ax:
        g.grid(alpha=0.25)
        g.tick_params(labelsize=8)
    span = (w.received_time_ns.values[-1] - w.received_time_ns.values[0]) / UNIT
    fig.suptitle(f'Trade day Tue Oct 17, 2023. SAMPLE, not stored. No window anywhere.\n{count} trades, '
                 f'{span:,.1f} s, from {x[0].strftime("%H:%M:%S.%f")[:-3]} Eastern', fontsize=11, y=0.985)
    fig.autofmt_xdate(rotation=30)
    name = f'{out}/three_renders_smooth_{day}_{first_trade}_{count}.png'
    fig.savefig(name, dpi=110, bbox_inches='tight')
    plt.close(fig)
    print(name, 'runs ended in the picture:', len(h))


for first_trade, count in jobs:
    draw(first_trade, count)
