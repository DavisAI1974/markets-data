"""The life of every peak on the clock, both kinds, with no defined window.

20-second peak : begins at the low its flow rose from (stored peak_story, fact "build-up"), reaches its high,
                 ends where its story ended (stored chain_peaks: came back or beaten).
no-window peak : a run of trades on one side (stored turn_peaks). Begins at the first trade of the run and ends at
                 the last one, which is its high. It becomes known at the first tick after that.
Every peak is one line. Nothing is averaged, ranked or dropped. An empty cell stays empty.
"""
import sys
sys.path.insert(0, "/home/claude/work/scripts")
from load import *

D2 = "/home/claude/work/data2/"
OUT = "/home/claude/work/out/"
WANT20 = {"20231002": 9525, "20231003": 10577, "20231017": 8619, "20231018": 7967}
WANTNW = {"20231002": 11567, "20231003": 12684, "20231017": 10401, "20231018": 9549}
alltabs = []
for day in DAYS:
    r = rd(day, "rows", ["position_on_tape", "received_time_ns", "row_label"])
    pos = r.position_on_tape.values.astype("int64"); tns = r.received_time_ns.values.astype("int64")

    def time_of(p):
        p = np.asarray(p, dtype="float64"); out = np.full(len(p), np.nan)
        ok = ~np.isnan(p); i = np.searchsorted(pos, p[ok].astype("int64")); assert (pos[i] == p[ok].astype("int64")).all()
        res = np.full(len(p), -1, dtype="int64"); res[ok] = tns[i]
        return res                                                # -1 where empty

    # 20-second peaks
    ps = pd.concat([pd.read_parquet(f) for f in sorted(glob.glob(f"{DATA}{day}/calc-peak_story-facts-{day}-part*.parquet"))])
    bu = ps[ps.fact == "build-up"][["peak_high_position", "low_position", "known_position"]].rename(columns={"known_position": "known_position"})
    assert bu.peak_high_position.is_unique and len(bu) == WANT20[day]
    cf = pd.concat([pd.read_parquet(f) for f in sorted(glob.glob(f"{DATA}{day}/calc-chain_peaks-facts-{day}-part*.parquet"))])
    cf = cf[["peak_high_position", "side", "size", "known_position", "ended_by", "price_at_high"]].rename(columns={"known_position": "end_position"})
    fp = rd(day, "calc-flow_peak", ["position_on_tape", "flow_bought_20s", "flow_sold_20s", "peak_side", "peak_size", "peak_high_position"])
    pk = fp[fp.peak_high_position.notna()][["peak_high_position", "peak_side", "peak_size"]].astype({"peak_high_position": "int64"})
    hi = fp.set_index("position_on_tape").reindex(pk.peak_high_position.values)
    pk["lots"] = (hi.flow_bought_20s.values - hi.flow_sold_20s.values) * np.where(pk.peak_side.values == "buy", 1, -1)
    a = pk.merge(bu, on="peak_high_position", how="left").merge(cf[["peak_high_position", "end_position", "ended_by", "price_at_high"]], on="peak_high_position", how="left")
    assert len(a) == WANT20[day]
    t20 = pd.DataFrame({"trade_day": day, "kind": "20-second flow", "side": a.peak_side.values, "lots": a.lots.values, "trades": np.nan,
                        "begin_position": a.low_position.values, "high_position": a.peak_high_position.values.astype("float64"),
                        "end_position": a.end_position.values, "known_position": a.known_position.values.astype("float64"),
                        "ended_by": a.ended_by.values})
    # no-window peaks
    tp = pd.read_parquet(f"{D2}{day}/calc-turn_peaks-facts-{day}-part000.parquet")
    nw = tp[(tp.peak_kind == "no window") & (tp.fact == "peak known")]
    assert len(nw) == WANTNW[day] and nw.peak_high_position.is_unique
    tnw = pd.DataFrame({"trade_day": day, "kind": "no window", "side": nw.peak_side.values, "lots": nw.peak_number.values, "trades": nw.peak_trades.values,
                        "begin_position": nw.peak_first_trade_position.values.astype("float64"), "high_position": nw.peak_high_position.values.astype("float64"),
                        "end_position": nw.peak_high_position.values.astype("float64"), "known_position": nw.known_position.values.astype("float64"),
                        "ended_by": "the next trade on the other side"})
    t = pd.concat([t20, tnw], ignore_index=True)
    for c in ["begin", "high", "end", "known"]:
        t[f"{c}_received_time_ns"] = time_of(t[f"{c}_position"].values)
    def span(x, y):
        v = (t[f"{y}_received_time_ns"] - t[f"{x}_received_time_ns"]).astype("float64")
        v[(t[f"{x}_received_time_ns"] < 0) | (t[f"{y}_received_time_ns"] < 0)] = np.nan
        return v
    t["begin_to_high_ns"] = span("begin", "high"); t["high_to_end_ns"] = span("high", "end"); t["begin_to_end_ns"] = span("begin", "end")
    t["high_to_known_ns"] = span("high", "known")
    for c in ["begin", "high", "end", "known"]:
        col = t[f"{c}_received_time_ns"]
        t[f"{c}_et"] = pd.to_datetime(col.where(col >= 0), utc=True).dt.tz_convert("America/New_York").dt.tz_localize(None)
        t[f"{c}_received_time_ns"] = col.where(col >= 0).astype("Int64")
    assert (t.begin_to_end_ns.dropna() >= 0).all() and (t.begin_to_high_ns.dropna() >= 0).all()
    t.to_parquet(f"{OUT}peak-lives-{day}.parquet", index=False)
    alltabs.append(t)
    print(day, "20-second peaks", len(t20), "no-window peaks", len(tnw), "| 20-second with no beginning stored:", int(t20.begin_position.isna().sum()),
          "with no end (story still open):", int(t20.end_position.isna().sum()))
T = pd.concat(alltabs, ignore_index=True)
T.to_parquet(OUT + "peak-lives-all.parquet", index=False)

# the scale: how long each life lasted, counted in powers of ten (a scale, not a grouping of the peaks)
edges = [-1, 0, 1e6, 1e7, 1e8, 1e9, 1e10, 1e11, 1e12, 1e13, 1e15]
labels = ["no length (begins and ends on one tick)", "under 1 ms", "1 to 10 ms", "10 to 100 ms", "0.1 to 1 s", "1 to 10 s", "10 to 100 s", "100 to 1,000 s", "1,000 to 10,000 s", "over 10,000 s"]
for kind in ["no window", "20-second flow"]:
    g = T[T.kind == kind]
    for col, name in [("begin_to_end_ns", "beginning to end"), ("begin_to_high_ns", "beginning to high"), ("high_to_end_ns", "high to end")]:
        if kind == "no window" and col != "begin_to_end_ns":
            continue
        b = pd.cut(g[col], edges, labels=labels)
        x = pd.crosstab(b, g.trade_day, dropna=False).reindex(labels, fill_value=0)
        x["all four"] = x.sum(axis=1)
        print(f"\n{kind}: {name} (count of peaks; empty cells: {int(g[col].isna().sum())})"); print(x.to_string())
print("\nno-window peaks: trades in the run (count of peaks)")
g = T[T.kind == "no window"]
b = pd.cut(g.trades, [0, 1, 2, 3, 5, 10, 20, 50, 100, 100000], labels=["1", "2", "3", "4-5", "6-10", "11-20", "21-50", "51-100", "over 100"])
x = pd.crosstab(b, g.trade_day); x["all four"] = x.sum(axis=1); print(x.to_string())
print("\nthe longest lives, one by one (no window): trade day, side, begins, ends, seconds, trades, lots")
for day in DAYS:
    gg = g[g.trade_day == day].sort_values("begin_to_end_ns", ascending=False).head(4)
    for _, q in gg.iterrows():
        print(" ", day, q.side, q.begin_et.strftime("%H:%M:%S.%f")[:-3], "to", q.end_et.strftime("%H:%M:%S.%f")[:-3], round(q.begin_to_end_ns / 1e9, 1), "s", int(q.trades), "trades", int(q.lots), "lots")
print("\nthe longest lives, one by one (20-second flow, beginning to end)")
g2 = T[T.kind == "20-second flow"]
for day in DAYS:
    gg = g2[g2.trade_day == day].sort_values("begin_to_end_ns", ascending=False).head(3)
    for _, q in gg.iterrows():
        print(" ", day, q.side, q.begin_et.strftime("%H:%M:%S"), "high", q.high_et.strftime("%H:%M:%S"), "end", q.end_et.strftime("%H:%M:%S"), round(q.begin_to_end_ns / 1e9, 1), "s", q.ended_by, int(q.lots), "lots")
