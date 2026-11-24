"""Old family rule and old chain states, built on the stored peaks of the four trade days.

Every peak is kept, on its own tick. Nothing is averaged, ranked or dropped.

Old definitions used, as written in Markets (branch chatgpt/ng-exhaustion-post-phase2-20260818):
  - family A/B/C: research/FRANKIE_NG_PRE_FAMILY_CLASSIFIER_FROZEN_OPERATIONAL_20260817.json
    with family_feature() from research/ng_exhaustion_live_clock.py (copied below, unchanged)
  - the +60 s state S/O/P/X, the endpoint, the links: research/ng_exhaustion_chain_canonical_table_20260817.py
  - chain strings and the "known before" rule: research/ng_exhaustion_chain_phase2_parallel_agents_20260818.py

Calls made here (the old programs ran on a whole-second grid of the UTC clock day):
  - t0 is the peak's own tick (the tick of its high). The 61 samples before and the 60 after are taken
    at t0 - 60 s ... t0 + 60 s, one second apart, counted from that tick, not from the whole second.
  - the flow is the stored one: bought minus sold over bought plus sold, last 20 seconds, the tape's
    own trade side (the old programs took the side from the trade price against the mid).
  - chains stay inside one trade day.
"""
import sys, json, math
sys.path.insert(0, "/home/claude/work/scripts")
from load import *

W = 20_000_000_000
SEC = 1_000_000_000
PRE = 60; POST = 60; PERSIST = 3
TICK = 1_000_000  # price units per tick (0.001)

CL = json.load(open("/home/claude/olddefs/family_classifier.json"))
CENTER = np.array(CL["scaler"]["center"]); SCALE = np.array(CL["scaler"]["scale"])
CENT = np.array([CL["centroids_family_order"][k] for k in "ABC"])


# ---- copied unchanged from research/ng_exhaustion_live_clock.py -------------------------------
def _slope(y, lo, hi):
    vals = [float(v) for v in y[lo:hi]]
    if len(vals) < 2 or max(vals) - min(vals) < 1e-15:
        return 0.0
    n = float(len(vals))
    mx = (n - 1.0) / 2.0
    my = sum(vals) / n
    den = sum((i - mx) ** 2 for i in range(len(vals)))
    return 0.0 if den <= 0 else sum((i - mx) * (v - my) for i, v in enumerate(vals)) / den


def _first_ge(y, level):
    for i, v in enumerate(y):
        if float(v) >= level:
            return i
    return len(y) - 1


def family_feature(raw):
    raw = tuple(float(x) for x in raw)
    assert len(raw) == 61
    peak = raw[-1]
    assert peak > 0.0
    rel = tuple(v / peak for v in raw)
    base10 = sum(raw[:10]) / 10.0
    excursion = peak - base10
    if abs(excursion) > 1e-9:
        build = tuple((v - base10) / excursion for v in raw)
    else:
        build = tuple(0.0 for _ in raw)
    prominence_base = sorted(abs(v) for v in raw[30:51])
    m = len(prominence_base)
    prom_med = prominence_base[m // 2] if m % 2 else 0.5 * (prominence_base[m // 2 - 1] + prominence_base[m // 2])
    prominence = abs(peak) - prom_med
    c10 = _first_ge(build, .10); c25 = _first_ge(build, .25); c50 = _first_ge(build, .50)
    c75 = _first_ge(build, .75); c90 = _first_ge(build, .90)
    early = _slope(build, 0, 21); mid = _slope(build, 20, 41); late = _slope(build, 40, 61)
    roughness = sum(abs(build[i + 1] - build[i]) for i in range(60)) / 60.0
    bmean = sum(build) / 61.0
    bstd = math.sqrt(sum((v - bmean) ** 2 for v in build) / 61.0)
    scalar = (base10, math.log1p(abs(excursion)), math.log1p(abs(prominence)),
              (60 - c10) / 60.0, (60 - c25) / 60.0, (60 - c50) / 60.0, (60 - c75) / 60.0, (60 - c90) / 60.0,
              max(0, c90 - c10) / 60.0, early, mid, late, late - mid, mid - early, roughness, bstd)
    feat = tuple(build[::2]) + tuple(rel[::2]) + scalar
    assert len(feat) == 78 and all(math.isfinite(v) for v in feat)
    return feat, dict(base10=base10, excursion=excursion, prominence=prominence,
                      rise50_s_before_t0=60 - c50, rise90_s_before_t0=60 - c90,
                      slope_early=early, slope_mid=mid, slope_late=late, roughness=roughness)
# ------------------------------------------------------------------------------------------------


def fill_rows(A):
    """fill_curve of the old programs, row by row: forward fill, then backward fill."""
    A = A.copy()
    n, m = A.shape
    for j in range(1, m):
        bad = np.isnan(A[:, j]); A[bad, j] = A[bad, j - 1]
    for j in range(m - 2, -1, -1):
        bad = np.isnan(A[:, j]); A[bad, j] = A[bad, j + 1]
    return A


def first_persist(post, lim):
    """first i >= 1 with post[i], post[i+1], post[i+2] all <= lim; -1 when none (old first_zero / first_persist_below)."""
    n, m = post.shape
    ok = post <= lim[:, None]
    run = ok[:, 1:m - 2] & ok[:, 2:m - 1] & ok[:, 3:m]          # columns for i = 1 .. m-3
    hit = run.any(axis=1)
    return np.where(hit, run.argmax(axis=1) + 1, -1)


def build_day(day):
    r = rd(day, "rows", ["position_on_tape", "received_time_ns", "row_label", "action", "side", "size", "price"])
    fp = rd(day, "calc-flow_peak", ["position_on_tape", "flow_20s", "peak_side", "peak_size", "peak_high_position"])
    assert (r.position_on_tape.values == fp.position_on_tape.values).all()
    r = pd.concat([r, fp.drop(columns="position_on_tape")], axis=1)
    r = r[r.row_label == "trade day"].reset_index(drop=True)
    t = r.received_time_ns.values.astype("int64"); pos = r.position_on_tape.values.astype("int64")
    assert (np.diff(t) >= 0).all() and (np.diff(pos) > 0).all()
    isT = (r.action == "T").values
    sz = r["size"].fillna(0).values.astype("int64")
    cb = np.concatenate([[0], np.cumsum(sz * (isT & (r.side == "B").values))])
    cs = np.concatenate([[0], np.cumsum(sz * (isT & (r.side == "A").values))])
    t_first, t_last = t[0], t[-1]

    def flow_at(times):
        hi = np.searchsorted(t, times, side="right"); lo = np.searchsorted(t, times - W, side="right")
        b = (cb[hi] - cb[lo]).astype(float); s = (cs[hi] - cs[lo]).astype(float); z = b + s
        f = np.full(times.shape, np.nan); m = z > 0
        f[m] = (b[m] - s[m]) / z[m]
        f[(times < t_first) | (times > t_last)] = np.nan
        return f

    pk = r[r.peak_high_position.notna()][["position_on_tape", "received_time_ns", "peak_side", "peak_size", "peak_high_position"]].copy()
    pk.columns = ["known_position", "known_received_time_ns", "side", "size", "high_position"]
    pk["high_position"] = pk.high_position.astype("int64")
    pk = pk.sort_values("high_position").reset_index(drop=True)
    assert pk.high_position.is_unique
    ih = np.searchsorted(pos, pk.high_position.values); assert (pos[ih] == pk.high_position.values).all()
    tau = t[ih]; pol = np.where(pk.side.values == "buy", 1.0, -1.0)
    f_high = r.flow_20s.values[ih]
    assert np.allclose(pol * f_high, pk["size"].values), "flow at the high tick does not equal the stored peak size"
    N = len(pk)

    # the arc: t0-60 s .. t0+60 s, one second apart, from the peak's own tick
    K = np.arange(-PRE, POST + 1)
    times = tau[:, None] + K[None, :] * SEC
    F = flow_at(times)
    same_as_time = np.isclose(F[:, PRE], f_high, equal_nan=False).sum()
    F[:, PRE] = f_high                                  # the high tick itself, in tick order
    arc_raw = pol[:, None] * F
    filled = fill_rows(arc_raw)
    pre = filled[:, :PRE + 1]; post = filled[:, PRE:]
    peak = pre[:, -1]; assert (peak > 0).all()
    pre_empty = np.isnan(arc_raw[:, :PRE + 1]).sum(axis=1); post_empty = np.isnan(arc_raw[:, PRE + 1:]).sum(axis=1)
    pre_before_first = times[:, 0] < t_first
    post_after_last = times[:, -1] > t_last

    # old family
    fam = []; dist = np.zeros((N, 3)); geo = []
    for i in range(N):
        f, g = family_feature(pre[i])
        x = (np.array(f) - CENTER) / SCALE
        d = np.sqrt(((CENT - x) ** 2).sum(axis=1))
        dist[i] = d; fam.append("ABC"[int(np.argmin(d))]); geo.append(g)
    geo = pd.DataFrame(geo)

    # old +60 s state
    zero_s = first_persist(post, np.zeros(N))
    t50 = first_persist(post, .50 * peak); t25 = first_persist(post, .25 * peak); t10 = first_persist(post, .10 * peak)
    late = arc_raw[:, -1]                               # flow of the 20 s ending at t0+60 s, oriented; empty when nothing traded
    state = np.where(zero_s < 0, "P", np.where(np.isnan(late) | (np.abs(late) < 1e-12), "X", np.where(late > 0, "S", "O")))
    state = np.where(post_after_last, "", state)

    # old endpoint, with no horizon: first second after t0 where the flow (last value carried) is at or
    # across zero three seconds running. onset = the first of the three, confirmation = the third.
    onset = np.full(N, -1, dtype="int64"); confirm = np.full(N, -1, dtype="int64")
    last = np.full(N, np.nan); run = np.zeros(N, dtype="int64"); alive = np.ones(N, dtype=bool)
    k0 = 1; B = 600
    max_k = int((t_last - tau.min()) // SEC) + 2
    while alive.any() and k0 <= max_k:
        idx = np.where(alive)[0]
        ks = np.arange(k0, k0 + B)
        tt = tau[idx, None] + ks[None, :] * SEC
        Fb = pol[idx, None] * flow_at(tt)
        beyond = tt > t_last
        for j in range(B):
            v = Fb[:, j]; fin = ~np.isnan(v)
            l = last[idx]; l[fin] = v[fin]; last[idx] = l
            have = ~np.isnan(l)
            rr = run[idx]
            rr = np.where(have & ~beyond[:, j], np.where(l <= 0, rr + 1, 0), rr)
            run[idx] = rr
            done = (rr >= PERSIST) & (confirm[idx] < 0) & ~beyond[:, j]
            if done.any():
                d = idx[done]; confirm[d] = ks[j]; onset[d] = ks[j] - (PERSIST - 1)
        alive[idx] = (confirm[idx] < 0) & ~beyond[:, -1]
        k0 += B

    out = pd.DataFrame({
        "trade_day": day, "peak_high_position": pk.high_position.values, "peak_high_received_time_ns": tau,
        "peak_known_position": pk.known_position.values, "side": pk.side.values, "size": pk["size"].values,
        "old_family": fam, "dist_A": dist[:, 0], "dist_B": dist[:, 1], "dist_C": dist[:, 2],
        "old_state_at_60s": state,
        "zero_within_60s_at_s": np.where(zero_s < 0, np.nan, zero_s),
        "below_half_at_s": np.where(t50 < 0, np.nan, t50), "below_quarter_at_s": np.where(t25 < 0, np.nan, t25),
        "below_tenth_at_s": np.where(t10 < 0, np.nan, t10),
        "flow_at_60s_with_side": late,
        "endpoint_onset_s": np.where(onset < 0, np.nan, onset), "endpoint_confirmed_s": np.where(confirm < 0, np.nan, confirm),
        "pre_samples_empty": pre_empty, "post_samples_empty": post_empty,
        "pre_reaches_before_first_tick": pre_before_first, "post_reaches_past_last_tick": post_after_last,
    })
    out = pd.concat([out, geo.add_prefix("pre_")], axis=1)
    for c in ["zero_within_60s_at_s", "below_half_at_s", "below_quarter_at_s", "below_tenth_at_s", "flow_at_60s_with_side"]:
        out.loc[post_after_last, c] = np.nan

    # the three gates of the old detector, as facts about each peak (no peak is removed)
    grid = np.arange(t_first, t_last + 1, SEC)
    gflow = np.abs(flow_at(grid)); gflow = gflow[~np.isnan(gflow)]
    a = np.sort(gflow); z = 0.85 * (len(a) - 1); i0 = int(np.floor(z)); j0 = min(i0 + 1, len(a) - 1)
    thr = a[i0] * (1 - (z - i0)) + a[j0] * (z - i0)
    absraw = np.abs(F)
    g1 = pk["size"].values >= thr
    loc = absraw[:, PRE - 5:PRE + 6]
    g2 = pk["size"].values >= np.nanmax(loc, axis=1) - 1e-12
    basew = absraw[:, PRE - 30:PRE - 9]
    with np.errstate(all="ignore"):
        base = np.nanmedian(basew, axis=1)
    base = np.where(np.isnan(base), 0.0, base)
    prom = pk["size"].values - base
    cand = np.where(g1 & g2 & ~pre_before_first & ~post_after_last)[0]
    order = sorted(cand, key=lambda i: (prom[i], pk["size"].values[i]), reverse=True)
    picked = []; picked_t = []
    for i in order:
        if any(abs(tau[i] - x) < 45 * SEC for x in picked_t):
            continue
        picked.append(i); picked_t.append(tau[i])
    g3 = np.zeros(N, dtype=bool); g3[picked] = True
    out["old_gate_size_at_or_over_85_in_100"] = g1
    out["old_gate_highest_within_5s"] = g2
    out["old_gate_kept_after_45s_spacing"] = g3
    out["old_gate_size_level"] = thr
    out["old_prominence"] = prom

    # what the peak did, from the stored chain_peaks facts (one line per ended peak)
    cf = pd.concat([pd.read_parquet(f) for f in sorted(glob.glob(f"{DATA}{day}/calc-chain_peaks-facts-{day}-part*.parquet"))])
    cf = cf[["peak_high_position", "ended_by", "high_to_end_ns", "lowest_share", "steps_down", "price_at_high", "price_at_end",
             "price_move_with_side", "furthest_price_with_side", "furthest_price_against_side", "low_to_high_ns"]]
    assert cf.peak_high_position.is_unique
    out = out.merge(cf, on="peak_high_position", how="left")
    pl = pd.concat([pd.read_parquet(f) for f in sorted(glob.glob(f"{DATA}{day}/calc-peak_links-facts-{day}-part*.parquet"))])
    pl = pl[pl.fact == "peak known"][["peak_high_position", "price_at_high"]].rename(columns={"price_at_high": "price_at_high_all"})
    assert pl.peak_high_position.is_unique
    out = out.merge(pl, on="peak_high_position", how="left")
    assert len(out) == N
    np.save(f"/home/claude/work/out/arc_raw_{day}.npy", arc_raw)
    print(day, "peaks", N, "| flow at the high tick same by time and by tick order:", int(same_as_time), "| old gate level", round(float(thr), 4),
          "| peaks passing the three old gates:", int(g3.sum()), "| endpoint never reached:", int((confirm < 0).sum()))
    return out


def add_chains(T, key, flag=None):
    """Chain strings from the peaks before each peak, inside its trade day. key = column prefix."""
    cols = {f"{key}_before_states": [], f"{key}_before_sides": [], f"{key}_to_last_before": [], f"{key}_known_before": [],
            f"{key}_pair": [], f"{key}_triplet": []}
    res = {c: np.full(len(T), "", dtype=object) for c in cols}
    known = np.zeros(len(T), dtype="int64")
    for day, g in T.groupby("trade_day", sort=False):
        if flag is not None:
            g = g[g[flag]]
        ix = g.index.values; st = g.old_state_at_60s.replace("", "?").values; sd = g.side.values
        tau = g.peak_high_received_time_ns.values; conf = g.endpoint_confirmed_s.values
        avail_time = np.where(np.isnan(conf), np.iinfo("int64").max, tau + (np.nan_to_num(conf) + 60).astype("int64") * SEC)
        for i in range(len(g)):
            lo = max(0, i - 4); prev = list(range(lo, i))
            res[f"{key}_before_states"][ix[i]] = "".join(st[j] for j in prev)
            res[f"{key}_before_sides"][ix[i]] = "".join("S" if sd[j] == sd[j - 1] else "F" for j in prev[1:])
            if prev:
                res[f"{key}_to_last_before"][ix[i]] = "SAME" if sd[i] == sd[i - 1] else "FLIP"
                res[f"{key}_pair"][ix[i]] = st[i - 1] + st[i] + "|" + ("S" if sd[i] == sd[i - 1] else "F")
            if i >= 2:
                res[f"{key}_triplet"][ix[i]] = st[i - 2] + st[i - 1] + st[i] + "|" + ("S" if sd[i - 1] == sd[i - 2] else "F") + ("S" if sd[i] == sd[i - 1] else "F")
            k = 0
            for j in reversed(prev):                      # how many of the peaks just before were known 60 s after their endpoint, before this high
                if avail_time[j] <= tau[i]:
                    k += 1
                else:
                    break
            known[ix[i]] = k
    for c in res:
        T[c] = res[c]
    T[f"{key}_known_before"] = known
    if flag is not None:
        T.loc[~T[flag], f"{key}_known_before"] = -1
    s4 = T[f"{key}_before_states"]; rel = T[f"{key}_to_last_before"]; kn = T[f"{key}_known_before"]
    T[f"{key}_SSOS"] = (s4 == "SSOS")
    T[f"{key}_SSOS_known"] = (s4 == "SSOS") & (kn >= 4)
    T[f"{key}_POX_opposite"] = s4.str[-3:].eq("POX") & (s4.str.len() >= 3) & (rel == "FLIP")
    T[f"{key}_POX_same"] = s4.str[-3:].eq("POX") & (s4.str.len() >= 3) & (rel == "SAME")
    T[f"{key}_POX_opposite_known"] = T[f"{key}_POX_opposite"] & (kn >= 3)
    T[f"{key}_POX_same_known"] = T[f"{key}_POX_same"] & (kn >= 3)
    return T


if __name__ == "__main__":
    T = pd.concat([build_day(d) for d in DAYS], ignore_index=True)
    T["old_gates_all_three"] = T.old_gate_size_at_or_over_85_in_100 & T.old_gate_highest_within_5s & T.old_gate_kept_after_45s_spacing
    T = add_chains(T, "all")
    T = add_chains(T, "gated", flag="old_gates_all_three")
    T["et"] = pd.to_datetime(T.peak_high_received_time_ns, utc=True).dt.tz_convert("America/New_York").dt.tz_localize(None)
    for c in ["price_move_with_side", "furthest_price_with_side", "furthest_price_against_side"]:
        T[c.replace("price", "ticks")] = T[c] / TICK
    T.to_parquet("/home/claude/work/out/peaks_old_family_chain.parquet", index=False)
    print("total peaks", len(T), T.groupby("trade_day").size().to_dict())
