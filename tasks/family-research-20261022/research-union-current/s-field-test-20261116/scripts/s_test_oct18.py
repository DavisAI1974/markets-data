"""Oct 18 test: do the 19 second-set (S) fields add information beyond the fields we already have?

Context = what is known strictly before each trade:
  * S values at 'last_completed_group_before_trade' (state PRESENT only; nothing imputed)
  * the pre-trade book ('before' snapshot)
  * trade flow over the 64 completed groups before the trade (the teacher's own far-side anchor rule)
Outcome = strictly after the trade, event-driven (no fixed clock horizon): which comes first, the mid moving k ticks
WITH the anchoring flow (continuation, +1) or k ticks AGAINST it (reversal, -1). Censored if neither before the
settle window / session end. Settle window 14:28-14:30 ET is excluded. No trade cost anywhere.
Per cell (far side x day part); pooled numbers are never the headline.
"""
import json, sys, numpy as np, pandas as pd
from scipy.stats import spearmanr
TICK = 1_000_000
S = [f'S{i:02d}' for i in range(1, 20)]
NAMES = dict(S01='extension_count_log', S02='far_absorption_share_1024', S03='far_absorption_share_64', S04='far_front_age_log',
    S05='far_identity_survival_1024', S06='far_identity_survival_64', S07='far_priority_loss_rate_1024', S08='far_priority_loss_rate_64',
    S09='far_queue_age_p90_log', S10='far_replenish_log1p_1024', S11='far_replenish_log1p_64', S12='far_size_hhi',
    S13='far_size_retention_1024', S14='far_size_retention_64', S15='pullback_ticks_last_log', S16='pullback_ticks_prev_log',
    S17='step_duration_groups_log', S18='step_ratio_log', S19='unresolved_age_groups_log')
BASE = ['flow_imb', 'top_imb_aligned', 'full_imb_aligned', 'far_top_size', 'near_top_size', 'spread_ticks', 'far_top_orders', 'trade_with_flow']
KS = (1, 2, 4)

def features(df):
    """Everything here uses rows <= i (book 'before' the trade, trades in groups strictly before the trade's group)."""
    g = df.group.values
    sz = df['size'].values.astype(float)
    buyv = np.where(df.side.values == 'B', sz, 0.); sellv = np.where(df.side.values == 'A', sz, 0.)
    cb = np.concatenate([[0], np.cumsum(buyv)]); cs = np.concatenate([[0], np.cumsum(sellv)])
    lo = np.searchsorted(g, g - 64, 'left'); hi = np.searchsorted(g, g, 'left')
    buy = cb[hi] - cb[lo]; sell = cs[hi] - cs[lo]; tot = buy + sell
    d = np.where((tot > 0) & (np.abs(buy - sell) * 20 > tot), np.sign(buy - sell), 0.)
    out = pd.DataFrame(index=df.index)
    out['d'] = d
    out['flow_imb'] = np.where(tot > 0, np.abs(buy - sell) / np.where(tot > 0, tot, 1), np.nan)
    bs, as_ = df.before_bid_size.values.astype(float), df.before_ask_size.values.astype(float)
    bf, af = df.before_bid_full_size.values.astype(float), df.before_ask_full_size.values.astype(float)
    out['top_imb_aligned'] = d * (bs - as_) / (bs + as_)
    out['full_imb_aligned'] = d * (bf - af) / (bf + af)
    out['far_top_size'] = np.where(d > 0, as_, bs); out['near_top_size'] = np.where(d > 0, bs, as_)
    out['spread_ticks'] = (df.before_ask_price_raw.values - df.before_bid_price_raw.values) / TICK
    out['far_top_orders'] = np.where(d > 0, df.before_ask_orders.values, df.before_bid_orders.values).astype(float)
    ts = np.where(df.side.values == 'B', 1., np.where(df.side.values == 'A', -1., 0.))
    out['trade_with_flow'] = d * ts            # this trade's own side is known at the trade; used as a baseline only
    out['mid2'] = df.before_bid_price_raw.values + df.before_ask_price_raw.values   # 2*mid, pre-trade
    return out

def leakage_gate(df, n=40, seed=0):
    rng = np.random.default_rng(seed); cols = ['d'] + BASE; f0 = features(df); fails = 0
    for i in rng.choice(np.arange(200, len(df) - 200), n, replace=False):
        d2 = df.copy(); tail = d2.index[i + 1:]
        perm = rng.permutation(len(tail))
        for c in ['size', 'side', 'before_bid_size', 'before_ask_size', 'before_bid_full_size', 'before_ask_full_size',
                  'before_bid_price_raw', 'before_ask_price_raw', 'before_bid_orders', 'before_ask_orders']:
            d2.loc[tail, c] = d2.loc[tail, c].values[perm]
        f1 = features(d2)
        a, b = f0.loc[i, cols].values.astype(float), f1.loc[i, cols].values.astype(float)
        fails += not np.array_equal(a, b, equal_nan=True)
    return n, fails

def first_passage(mid2, k, stop):
    """For each i: +1/-1 = sign of the first move of >= k ticks in mid after trade i, among later trades j<stop[i]; 0 = censored."""
    n = len(mid2); res = np.zeros(n, dtype=np.int8); lag = np.full(n, -1, dtype=np.int64); thr = 2 * k * TICK
    for i in range(n):
        j0, j1 = i + 1, stop[i]
        while j0 < j1:
            seg = mid2[j0:min(j1, j0 + 512)] - mid2[i]
            hit = np.nonzero(np.abs(seg) >= thr)[0]
            if len(hit):
                res[i] = 1 if seg[hit[0]] > 0 else -1; lag[i] = j0 + hit[0]; break
            j0 += 512
    return res, lag

def shift_p(x, y, stat, n=400, seed=1, min_shift=50):
    rng = np.random.default_rng(seed); obs = stat(x, y); m = len(x)
    if m < 4 * min_shift or not np.isfinite(obs): return obs, np.nan
    null = np.array([stat(np.roll(x, s), y) for s in rng.integers(min_shift, m - min_shift, n)])
    return obs, float((np.sum(np.abs(null) >= abs(obs)) + 1) / (n + 1))

def rho(x, y):
    return spearmanr(x, y).statistic if len(np.unique(x)) > 1 and len(np.unique(y)) > 1 else np.nan

def tercile_table(x, y):
    q = np.quantile(x, [1/3, 2/3]); b = np.digitize(x, q) if q[0] < q[1] else (x > np.median(x)).astype(int) * 2
    return [dict(bin=int(t), n=int((b == t).sum()), cont_rate=float((y[b == t] > 0).mean()) if (b == t).any() else None) for t in (0, 1, 2)]

def main():
    df = pd.read_parquet('/home/user/work/out/flat_20231018.parquet').reset_index(drop=True)
    assert df.cursor.is_monotonic_increasing and (df.before_known_by < df.receive_ns).all() and not df.flag_any.any()
    gate = leakage_gate(df); print('LEAKAGE GATE: checked %d, fails %d' % gate); assert gate[1] == 0
    f = features(df); df = pd.concat([df, f], axis=1)
    et = pd.to_datetime(df.receive_ns, utc=True).dt.tz_convert('America/New_York')
    mins = (et.dt.hour * 60 + et.dt.minute).values; overnight = (et.dt.hour >= 18).values
    settle0, settle1 = 14 * 60 + 28, 14 * 60 + 30
    in_settle = (~overnight) & (mins >= settle0) & (mins < settle1)
    part = np.select([overnight | (mins < 8 * 60), mins < 11 * 60, mins < settle0, mins >= settle1],
                     ['1_overnight_to_0800', '2_0800_1100', '3_1100_to_settle', '4_post_settle'], 'settle')
    df['part'] = part
    n = len(df); first_settle = int(np.argmax(in_settle)) if in_settle.any() else n
    stop = np.where(np.arange(n) < first_settle, first_settle, n)       # outcomes never run through the settle window
    out = dict(leakage_gate=dict(checked=gate[0], fails=gate[1]), n_trades=n, settle_trades_excluded=int(in_settle.sum()), cells={})
    for k in KS:
        y, lag = first_passage(df.mid2.values, k, stop); df[f'y{k}'] = y * df.d.values
        df[f'lag_s{k}'] = np.where(lag >= 0, (df.receive_ns.values[np.clip(lag, 0, n - 1)] - df.receive_ns.values) / 1e9, np.nan)
    df.to_parquet('/home/user/work/out/s_test_frame_20231018.parquet')
    elig = (df.d != 0) & (~in_settle)
    rows = []
    for (p, d), c in df[elig].groupby(['part', 'd']):
        cell = f"{p}|far={'ask(buy flow)' if d > 0 else 'bid(sell flow)'}"
        for k in KS:
            cc = c[c[f'y{k}'] != 0]; y = cc[f'y{k}'].values.astype(float)
            base = dict(cell=cell, k=k, n=len(cc), censored=int((c[f'y{k}'] == 0).sum()), cont_rate=float((y > 0).mean()) if len(y) else None,
                        median_seconds_to_outcome=float(np.nanmedian(cc[f'lag_s{k}'])) if len(cc) else None)
            out['cells'][f'{cell}|k={k}'] = base
            for feat in [s + '_lc' for s in S] + BASE:
                m = cc[feat].notna().values
                if m.sum() < 300: rows.append(dict(cell=cell, k=k, feat=feat, n=int(m.sum()), note='too few present')); continue
                x = cc[feat].values[m].astype(float); yy = y[m]
                r, pv = shift_p(x, yy, rho); tt = tercile_table(x, yy)
                rows.append(dict(cell=cell, k=k, feat=feat, n=int(m.sum()), rho=r, p_shift=pv, lo=tt[0]['cont_rate'], mid=tt[1]['cont_rate'],
                                 hi=tt[2]['cont_rate'], n_lo=tt[0]['n'], n_hi=tt[2]['n'],
                                 first_half_rho=rho(x[:len(x)//2], yy[:len(x)//2]), second_half_rho=rho(x[len(x)//2:], yy[len(x)//2:])))
    res = pd.DataFrame(rows); res.to_csv('/home/user/work/out/s_test_univariate_20231018.csv', index=False)
    json.dump(out, open('/home/user/work/out/s_test_cells_20231018.json', 'w'), indent=1)
    print(pd.DataFrame(out['cells'].values()).to_string())
main()
