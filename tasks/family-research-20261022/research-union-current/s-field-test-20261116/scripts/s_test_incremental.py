"""Incremental value of S beyond existing fields, per cell, out of sample in time (train = first 60% of the cell's
trades, purge gap, test = last 35%). Three feature sets: existing baselines; baselines + S; S only.
Also: does S04 (far_front_age_log) still sort outcomes inside strata of the existing top-of-book fields?"""
import numpy as np, pandas as pd, warnings
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import roc_auc_score, log_loss
warnings.filterwarnings('ignore')
df = pd.read_parquet('/home/user/work/out/s_test_frame_20231018.parquet')
BASE = ['flow_imb', 'top_imb_aligned', 'full_imb_aligned', 'far_top_size', 'near_top_size', 'spread_ticks', 'far_top_orders', 'trade_with_flow']
SD = [f'S{i:02d}_lc' for i in (1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 19)]     # S08 has 16% extra missing; S15-18 are sparse
rows = []
for k in (1, 2, 4):
    for (p, d), c in df[(df.d != 0) & (df.part != 'settle') & (df[f'y{k}'] != 0)].groupby(['part', 'd']):
        c = c.dropna(subset=BASE + SD); n = len(c); a, b = int(n * .60), int(n * .65)
        tr, te = c.iloc[:a], c.iloc[b:]; ytr, yte = (tr[f'y{k}'] > 0).astype(int), (te[f'y{k}'] > 0).astype(int)
        if ytr.nunique() < 2 or yte.nunique() < 2: continue
        row = dict(k=k, cell=f"{p}|{'ask' if d > 0 else 'bid'}", n_train=len(tr), n_test=len(te), test_cont=float(yte.mean()))
        prior = np.full(len(te), ytr.mean()); row['ll_prior'] = log_loss(yte, prior, labels=[0, 1])
        for name, cols in (('base', BASE), ('base+S', BASE + SD), ('S', SD)):
            for mname, mk in (('lin', lambda: make_pipeline(StandardScaler(), LogisticRegression(C=0.3, max_iter=2000))),
                              ('gb', lambda: HistGradientBoostingClassifier(max_depth=3, max_iter=150, learning_rate=0.05, min_samples_leaf=40, random_state=0))):
                m = mk().fit(tr[cols], ytr); pr = np.clip(m.predict_proba(te[cols])[:, 1], 1e-4, 1 - 1e-4)
                row[f'auc_{mname}_{name}'] = roc_auc_score(yte, pr); row[f'll_{mname}_{name}'] = log_loss(yte, pr, labels=[0, 1])
        rows.append(row)
r = pd.DataFrame(rows); r.to_csv('/home/user/work/out/s_test_incremental_20231018.csv', index=False)
pd.set_option('display.width', 260)
print(r[['k', 'cell', 'n_test', 'test_cont', 'auc_lin_base', 'auc_lin_base+S', 'auc_gb_base', 'auc_gb_base+S', 'auc_lin_S', 'auc_gb_S']].round(3).to_string())
r['d_auc_lin'] = r['auc_lin_base+S'] - r['auc_lin_base']; r['d_auc_gb'] = r['auc_gb_base+S'] - r['auc_gb_base']
r['d_ll_lin'] = r['ll_lin_base+S'] - r['ll_lin_base']; r['d_ll_gb'] = r['ll_gb_base+S'] - r['ll_gb_base']
print(r.groupby('k').agg(cells=('cell', 'size'), auc_up_lin=('d_auc_lin', lambda v: (v > 0).sum()), auc_up_gb=('d_auc_gb', lambda v: (v > 0).sum()),
      ll_better_lin=('d_ll_lin', lambda v: (v < 0).sum()), ll_better_gb=('d_ll_gb', lambda v: (v < 0).sum()),
      min_d_auc_lin=('d_auc_lin', 'min'), max_d_auc_lin=('d_auc_lin', 'max'), S_only_auc_gt_052=('auc_lin_S', lambda v: (v > .52).sum())).round(3).to_string())
# S04 inside strata of existing top-of-book fields (k=1): terciles of top_imb_aligned x terciles of far_top_orders
print('\nS04 (far_front_age_log) high-minus-low continuation rate inside 9 strata of existing fields, k=1 and k=2')
for k in (1, 2):
    for (p, d), c in df[(df.d != 0) & (df.part != 'settle') & (df[f'y{k}'] != 0) & df.S04_lc.notna()].groupby(['part', 'd']):
        c = c.copy(); c['a'] = pd.qcut(c.top_imb_aligned, 3, labels=False, duplicates='drop'); c['b'] = pd.qcut(c.far_top_orders.rank(method='first'), 3, labels=False)
        sp = []
        for _, s in c.groupby(['a', 'b']):
            if len(s) < 90: continue
            q = s.S04_lc.quantile([1/3, 2/3]).values; lo = s[s.S04_lc <= q[0]]; hi = s[s.S04_lc >= q[1]]
            sp.append(((hi[f'y{k}'] > 0).mean() - (lo[f'y{k}'] > 0).mean()))
        sp = np.array(sp); print(f"k={k} {p}|{'ask' if d > 0 else 'bid'}: strata={len(sp)} negative={int((sp < 0).sum())} spreads={np.round(np.sort(sp), 2).tolist()}")
