"""One image per trade day, one clock: price, then the life of every no-window peak, then the life of every 20-second peak.
A life is drawn from its beginning to its end, at the height of how long it lasted. Every peak is on the image."""
import sys
sys.path.insert(0, "/home/claude/work/scripts")
from load import *
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt, matplotlib.dates as mdates
from matplotlib.collections import LineCollection
from matplotlib.lines import Line2D

INK = "#0b0b0b"; INK2 = "#52514e"; MUTED = "#898781"; GRID = "#e1e0d9"; SURF = "#fcfcfb"
BUY = "#12866f"; SELL = "#d1492e"
FLOOR = 3e-8; TOP = 2e4          # strips: lives with no length, and lives whose beginning or end is not stored
OUT = "/home/claude/work/out/"
for day in DAYS:
    T = pd.read_parquet(f"{OUT}peak-lives-{day}.parquet")
    r = rd(day, "rows", ["received_time_ns", "row_label", "action", "price"]); r = r[(r.row_label == "trade day") & (r.action == "T")]
    tr_et = pd.to_datetime(r.received_time_ns.values, utc=True).tz_convert("America/New_York").tz_localize(None)
    fig, axs = plt.subplots(3, 1, figsize=(16, 15), sharex=True, gridspec_kw={"height_ratios": [2, 3.2, 3.2], "hspace": 0.09}, facecolor=SURF)
    ax = axs[0]; ax.step(tr_et, r.price.values / 1e9, color=MUTED, lw=.6, where="post"); ax.set_ylabel("price", fontsize=9, color=INK2)
    ax.set_title(f"price: {len(r):,} trades", fontsize=9.5, loc="left", color=INK)
    for a_, kind, name in [(axs[1], "no window", "peaks with no window (a run of trades on one side): first trade to last trade"),
                           (axs[2], "20-second flow", "20-second peaks: the low the flow rose from, to the end of the story (came back or beaten)")]:
        g = T[T.kind == kind]; n = 0
        for side, col, mk in [("buy", BUY, "^"), ("sell", SELL, "v")]:
            s = g[g.side == side]
            has = s.begin_to_end_ns.notna()
            d = s[has]; L = d.begin_to_end_ns.values / 1e9
            y = np.where(L > 0, L, FLOOR)
            x0 = mdates.date2num(d.begin_et.values.astype("datetime64[us]").astype(object)); x1 = mdates.date2num(d.end_et.values.astype("datetime64[us]").astype(object))
            a_.add_collection(LineCollection(np.stack([np.stack([x0, y], 1), np.stack([x1, y], 1)], 1), colors=col, linewidths=.7, alpha=.75, zorder=2))
            a_.scatter(d.begin_et, y, marker=mk, s=5, color=col, lw=0, zorder=3, alpha=.8)
            e = s[~has]
            a_.scatter(e.high_et, np.full(len(e), TOP), marker=mk, s=9, color=col, lw=0, zorder=3)
            n += len(d) + len(e)
        assert n == len(g), (day, kind, n, len(g))
        nolen = int((g.begin_to_end_ns == 0).sum()); empty = int(g.begin_to_end_ns.isna().sum())
        a_.set_yscale("log"); a_.set_ylim(1.2e-8, 5e4)
        ticks = [FLOOR, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1, 10, 100, 1000, TOP]
        a_.set_yticks(ticks); a_.set_yticklabels(["no length", "1 µs", "10 µs", "100 µs", "1 ms", "10 ms", "0.1 s", "1 s", "10 s", "100 s", "1,000 s", "not stored"], fontsize=7.5)
        a_.minorticks_off(); a_.set_ylabel("how long the life lasted", fontsize=9, color=INK2)
        a_.set_title(f"{name}   |   {len(g):,} drawn of {len(g):,}: {(g.side == 'buy').sum():,} buy, {(g.side == 'sell').sum():,} sell; "
                     f"{nolen:,} with no length; {empty:,} with a beginning or end not stored (top line, at the high)", fontsize=9.5, loc="left", color=INK)
    for a_ in axs:
        a_.set_facecolor(SURF); a_.grid(color=GRID, lw=.5); a_.tick_params(colors=INK2, labelsize=8)
        for s in a_.spines.values():
            s.set_color("#c3c2b7"); s.set_linewidth(.6)
    axs[2].xaxis.set_major_locator(mdates.HourLocator(interval=1)); axs[2].xaxis.set_major_formatter(mdates.DateFormatter("%H:%M")); axs[2].set_xlabel("Eastern time", fontsize=9, color=INK2)
    axs[0].set_xlim(tr_et[0] - pd.Timedelta(minutes=5), tr_et[-1] + pd.Timedelta(minutes=5))
    fig.legend(handles=[Line2D([], [], marker="^", color=BUY, lw=1, ms=5, label="buy peak: drawn from its beginning to its end"),
                        Line2D([], [], marker="v", color=SELL, lw=1, ms=5, label="sell peak")], loc="upper right", ncol=2, fontsize=8.5, frameon=False, bbox_to_anchor=(.985, .965))
    fig.suptitle(f"{NAME[day]} trade day: the life of every peak on one clock, no defined window. Each life starts at its own beginning and stops at its own end.",
                 fontsize=11, color=INK, y=.975, x=.02, ha="left")
    fig.subplots_adjust(left=.07, right=.985, top=.935, bottom=.045)
    fig.savefig(f"{OUT}peak_lives_{day}.png", dpi=120, facecolor=SURF); plt.close(fig)
    print(day, "drawn", len(T), "of", len(T))
