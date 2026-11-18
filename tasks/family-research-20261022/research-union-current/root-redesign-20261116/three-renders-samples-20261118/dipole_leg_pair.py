"""Sample only (a dry run in the session, nothing stored): the stacked pair for a dipole born on a trade leg's first trade.

Two graphs on one axis of real timestamps, no window:
  top:    the trade price curve (every trade a dot, drawn smooth through them), the trade leg's own life shaded
  bottom: the dipole at the tick (the run of trades under way against the run before it)
The birth second of the recorded dipole is marked on both. The picture runs from the first trade of the trade leg
before to the last trade of the trade leg after, so no span of time is chosen.
usage: dipole_leg_pair.py <folder> <trade day> <part> <out folder> <how many>
"""
import sys
from datetime import datetime, timedelta, timezone

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pyarrow.parquet as pq
from scipy.interpolate import PchipInterpolator

folder, day, part, out, many = sys.argv[1:6]
EASTERN = timezone(timedelta(hours=-4))                      # October 2023: Eastern daylight time
UNIT = 10 ** 9

r = pq.read_table(f'{folder}/rows-{day}-{part}.parquet',
                  columns=['received_time_ns', 'action', 'side', 'price', 'size', 'position_on_tape']).to_pandas()
t = pq.read_table(f'{folder}/calc-turn_peaks-{day}-{part}.parquet').to_pandas()
assert (r.position_on_tape.values == t.position_on_tape.values).all()
pos = r.position_on_tape.values
pins = pq.read_table(f'{folder}/renders/dipoles-pinned-{day}.parquet').to_pandas()
facts = pq.read_table(f'{folder}/calc-leg_peaks-facts-{day}-part000.parquet').to_pandas()
ended = facts[facts.fact == 'leg ended'].set_index('leg_number')
started = facts[facts.fact == 'leg started'].sort_values('leg_first_trade_position')

side = np.where(t.run_side.astype(str).str.startswith('b'), 1.0, -1.0)
size = t.run_size.values.astype(float)
first = t.run_first_trade_position.values
known = ~np.isnan(size)
change = np.flatnonzero(known[1:] & known[:-1] & (first[1:] != first[:-1])) + 1
before = np.full(len(size), np.nan)
for i, c in enumerate(change):
    before[c:(change[i + 1] if i + 1 < len(change) else len(size))] = size[c - 1]
bought, sold = np.where(side > 0, size, before), np.where(side > 0, before, size)
dipole = (bought - sold) / (bought + sold)


def clock(ns):
    return datetime.fromtimestamp(ns / UNIT, EASTERN)


def row_of(position):
    return int(np.searchsorted(pos, position))


with_trade = pins[pins.trades_in_birth_second > 0].sort_values('native_birth_ns')
firsts = started.leg_first_trade_position.values
drawn = 0
for _, d in with_trade.iterrows():
    a, b = d.first_position_in_birth_second, d.last_position_in_birth_second
    i = np.searchsorted(firsts, a, 'left')
    if i >= len(firsts) or firsts[i] > b or a < pos[0] or b > pos[-1]:
        continue                                              # no trade leg starts in this birth second
    leg = int(started.leg_number.values[i])
    if leg - 1 not in ended.index or leg + 1 not in ended.index or leg not in ended.index:
        continue
    lo = row_of(ended.loc[leg - 1].leg_first_trade_position)
    hi = row_of(ended.loc[leg + 1].leg_last_trade_position) + 1
    if lo < 1 or hi >= len(r):
        continue
    w = r.iloc[lo - 1:hi + 1]
    x = np.array([clock(v) for v in w.received_time_ns.values])
    tr = w.action.values == 'T'
    tns, tpx = w.received_time_ns.values[tr].astype(float), w.price.values[tr] / UNIT
    last = np.append(np.diff(tns) > 0, True)
    fig, ax = plt.subplots(2, 1, figsize=(7.2, 9.0), sharex=True, gridspec_kw={'hspace': 0.16})

    if last.sum() > 1:
        grid = np.linspace(tns[0], tns[-1], 4000)
        ax[0].plot([clock(v) for v in grid], PchipInterpolator(tns[last], tpx[last])(grid), color='#b03a2e', lw=1.4)
    ax[0].scatter(x[tr], tpx, s=9, color='#17202a', zorder=3, label='a trade')
    own = ended.loc[leg]
    s0 = clock(r.received_time_ns.values[row_of(own.leg_first_trade_position)])
    s1 = clock(r.received_time_ns.values[row_of(own.leg_last_trade_position)])
    ax[0].axvspan(s0, s1, color='#f9e79f', alpha=0.45, label="this trade leg's own life (first trade to last)")
    ax[0].set_ylabel('trade price, dollars')
    ax[0].set_title('THE TRADE LEG: the price of every trade, drawn smooth through them', loc='left', fontsize=11)

    ax[1].step(x, dipole[lo - 1:hi + 1], where='post', color='#1f618d', lw=1.1)
    ax[1].axhline(0, color='#aab7b8', lw=0.8)
    ax[1].set_ylim(-1.05, 1.05)
    ax[1].set_ylabel('buying against selling\n(+1 all buying, -1 all selling)')
    ax[1].set_title('THE DIPOLE, at the tick: the run of trades under way against the run before it', loc='left',
                    fontsize=11)
    ax[1].set_xlabel('Eastern time (the received clock)')
    b0, b1 = clock(d.native_birth_ns), clock(d.native_birth_ns + UNIT)
    for g in ax:
        g.axvspan(b0, b1, color='#5d6d7e', alpha=0.35, label='the second the recorded dipole was born')
        g.grid(alpha=0.25)
        g.tick_params(labelsize=8)
        g.legend(fontsize=7, loc='best')
    span = (w.received_time_ns.values[-1] - w.received_time_ns.values[0]) / UNIT
    kind = 'buying' if d.native_polarity > 0 else 'selling'
    fig.suptitle(f'Trade day Tue Oct 17, 2023. SAMPLE, not stored. No window.\nRecorded dipole born {b0.strftime("%H:%M:%S")} '
                 f'Eastern ({kind}; {int(d.trades_in_birth_second)} trade in that second, the first trade of trade leg '
                 f'{leg}).\nLeg {leg}: {own.direction}, {int(own.steps)} step(s), {own.since_first_trade_ns / UNIT:,.1f} s. '
                 f'Picture: {int(tr.sum())} trades, {span:,.1f} s.', fontsize=10, y=0.995)
    fig.autofmt_xdate(rotation=30)
    name = f'{out}/dipole_leg_pair_{day}_{d.dipole}.png'
    fig.savefig(name, dpi=110, bbox_inches='tight')
    plt.close(fig)
    print(name, 'leg', leg, own.direction, 'trades in picture', int(tr.sum()), 'seconds', round(span, 1))
    drawn += 1
    if drawn == int(many):
        break
