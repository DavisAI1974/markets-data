"""Time-pinned layers, one image per trade day, on the same clock as the earlier price-and-peak renders.

Layer 1: price, every trade.
Layer 2: every peak at the tick of its high. No family, no group.
Layer 3: the old detector's events (peaks passing its three gates), each at its own tick, with the old family
         found from the 60 seconds before it (known at that tick).
Layer 4: the old state of each of those events, drawn at the tick it became known (60 seconds after), joined to its event.
"""
import sys
sys.path.insert(0, "/home/claude/work/scripts")
from load import *
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt, matplotlib.dates as mdates
from matplotlib.lines import Line2D

SEC = 1_000_000_000
INK = "#0b0b0b"; INK2 = "#52514e"; MUTED = "#898781"; GRID = "#e1e0d9"; SURF = "#fcfcfb"
BUY = "#12866f"; SELL = "#d1492e"                       # as in the earlier renders
FAM = {"A": "#2a78d6", "B": "#eb6834", "C": "#1baf7a"}  # validated set, fixed order
STA = {"S": "#2a78d6", "O": "#eb6834", "P": "#1baf7a", "X": "#eda100"}
NP = 10

T = pd.read_parquet("/home/claude/work/out/peaks_old_family_chain.parquet")


def et(ns):
    return pd.to_datetime(np.asarray(ns, dtype="int64"), utc=True).tz_convert("America/New_York").tz_localize(None)


for day in DAYS:
    r = rd(day, "rows", ["received_time_ns", "row_label", "action", "price"])
    r = r[r.row_label == "trade day"]
    t_first, t_last = int(r.received_time_ns.iloc[0]), int(r.received_time_ns.iloc[-1])
    tr = r[r.action == "T"].copy(); tr["et"] = et(tr.received_time_ns.values)
    tt = T[T.trade_day == day].sort_values("peak_high_position").copy(); tt["et"] = et(tt.peak_high_received_time_ns.values)
    ev = tt[tt.old_gates_all_three].copy()
    ev["known_ns"] = ev.peak_high_received_time_ns + 60 * SEC
    ev["known_et"] = et(ev.known_ns.values)
    st = ev[ev.old_state_at_60s != ""]
    # ten panels, each holding about the same number of peaks
    q = np.quantile(tt.peak_high_received_time_ns.values.astype("float64"), np.linspace(0, 1, NP + 1)).astype("int64")
    q[0] = t_first; q[-1] = t_last + 61 * SEC
    cuts = et(q)
    fig = plt.figure(figsize=(15, 4.6 * NP), facecolor=SURF)
    gs = fig.add_gridspec(NP * 2, 1, height_ratios=[3.2, 1.0] * NP, hspace=0.42, top=0.972, bottom=0.01, left=0.09, right=0.985)
    n_tr = n_pk = n_ev = n_st = 0
    for i in range(NP):
        a, b = cuts[i], cuts[i + 1]
        ax = fig.add_subplot(gs[2 * i]); lane = fig.add_subplot(gs[2 * i + 1], sharex=ax)
        for z in (ax, lane):
            z.set_facecolor(SURF)
            for s in z.spines.values():
                s.set_color("#c3c2b7"); s.set_linewidth(.6)
        w = tr[(tr.et >= a) & (tr.et < b)]; g = tt[(tt.et >= a) & (tt.et < b)]
        e = ev[(ev.et >= a) & (ev.et < b)]; s_ = st[(st.known_et >= a) & (st.known_et < b)]
        n_tr += len(w); n_pk += len(g); n_ev += len(e); n_st += len(s_)
        ax.step(w.et, w.price / 1e9, color=MUTED, lw=.6, where="post", zorder=1)
        gb = g[g.side == "buy"]; gsell = g[g.side == "sell"]
        ax.scatter(gb.et, gb.price_at_high_all / 1e9, marker="^", s=9, color=BUY, lw=0, zorder=3)
        ax.scatter(gsell.et, gsell.price_at_high_all / 1e9, marker="v", s=9, color=SELL, lw=0, zorder=2)
        ax.set_title(f"{a:%H:%M:%S} to {b:%H:%M:%S} Eastern   |   {len(w):,} trades   {len(g):,} peaks ({len(gb):,} buy, {len(gsell):,} sell)   "
                     f"{len(e):,} old-detector events   {len(s_):,} old states known here", fontsize=8.5, color=INK, loc="left")
        ax.tick_params(labelsize=7, colors=INK2); ax.grid(color=GRID, lw=.5); ax.set_ylabel("price", fontsize=7, color=INK2)
        plt.setp(ax.get_xticklabels(), visible=False)
        # lanes: y=1 the old event at its own tick (family); y=0 its old state at the tick it became known
        for fam in "ABC":
            for side, mk in (("buy", "^"), ("sell", "v")):
                d = e[(e.old_family == fam) & (e.side == side)]
                lane.scatter(d.et, np.ones(len(d)), marker=mk, s=26 if fam != "A" else 14, color=FAM[fam], lw=0, zorder=3)
        for _, row in e[e.old_family != "A"].iterrows():
            lane.annotate(row.old_family, (row.et, 1), xytext=(0, 5), textcoords="offset points", ha="center", fontsize=6.5, color=INK, fontweight="bold")
        # the join from each event to the tick its state became known (drawn for states that fall in this panel or start in it)
        j = st[((st.et >= a) & (st.et < b)) | ((st.known_et >= a) & (st.known_et < b))]
        for x0, x1 in zip(j.et.values, j.known_et.values):
            lane.plot([x0, x1], [1, 0], color="#c3c2b7", lw=.5, zorder=1)
        for k in "SOPX":
            d = s_[s_.old_state_at_60s == k]
            lane.scatter(d.known_et, np.zeros(len(d)), marker="o", s=13, color=STA[k], lw=0, zorder=3)
            for x in d.known_et.values:
                lane.annotate(k, (x, 0), xytext=(0, -8.5), textcoords="offset points", ha="center", fontsize=5.2, color=INK)
        lane.set_ylim(-.75, 1.6); lane.set_yticks([1, 0]); lane.set_yticklabels(["old event, at its tick", "its old state, when known"], fontsize=6.5, color=INK2)
        lane.tick_params(labelsize=7, colors=INK2); lane.grid(axis="x", color=GRID, lw=.5)
        span = (b - a).total_seconds()
        lane.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M" if span > 1800 else "%H:%M:%S"))
        ax.set_xlim(a, b)
    # nothing left out: every trade, peak, old event and old state is on the image
    assert n_tr == len(tr) and n_pk == len(tt) and n_ev == len(ev) and n_st == len(st), (n_tr, len(tr), n_pk, len(tt), n_ev, len(ev), n_st, len(st))
    fam_n = ev.old_family.value_counts().reindex(list("ABC"), fill_value=0); st_n = st.old_state_at_60s.value_counts().reindex(list("SOPX"), fill_value=0)
    handles = [Line2D([], [], color=MUTED, lw=1, label=f"price: {n_tr:,} trades"),
               Line2D([], [], marker="^", ls="", color=BUY, ms=5, label=f"buy peak at its high: {(tt.side == 'buy').sum():,}"),
               Line2D([], [], marker="v", ls="", color=SELL, ms=5, label=f"sell peak at its high: {(tt.side == 'sell').sum():,}")]
    handles += [Line2D([], [], marker="s", ls="", color=FAM[f], ms=6, label=f"old family {f}: {fam_n[f]:,}") for f in "ABC"]
    handles += [Line2D([], [], marker="o", ls="", color=STA[k], ms=5, label=f"old state {k}: {st_n[k]:,}") for k in "SOPX"]
    fig.legend(handles=handles, loc="upper center", ncol=5, fontsize=8, frameon=False, bbox_to_anchor=(.5, .9905))
    fig.suptitle(f"{NAME[day]} trade day, everything on one clock: price ({n_tr:,} trades), every peak ({n_pk:,} of {len(tt):,}), "
                 f"the old detector's events ({n_ev:,} of {len(ev):,}) with their old family,\nand each event's old state drawn at the tick it became known "
                 f"({n_st:,} of {len(st):,}). Up-triangle buy, down-triangle sell.",
                 fontsize=10, color=INK, y=0.9985)
    out = f"/home/claude/work/out/pinned_layers_{day}.png"
    fig.savefig(out, dpi=105, facecolor=SURF); plt.close(fig)
    print(day, "trades", n_tr, "peaks", n_pk, "old events", n_ev, dict(fam_n), "states", n_st, dict(st_n), out)
