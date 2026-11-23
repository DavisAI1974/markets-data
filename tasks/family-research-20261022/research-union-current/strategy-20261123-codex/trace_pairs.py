import json
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import pyarrow.parquet as pq

# Arguments are one shallow data checkout and one destination directory.
repo, dest = map(Path, sys.argv[1:])
day = repo.name
dest.mkdir(parents=True, exist_ok=True)
receipt = json.loads((repo/'RECEIPT.json').read_text())
rc = json.loads((repo/f'CALC-research_columns-{day}.json').read_text())
assert receipt['checks']['rows']['passed'] and rc['checks']['passed']
fields = ['position_on_tape','received_time_ns','exchange_time_ns','row_label','action','side','price','best_bid','best_ask','best_bid_size','best_ask_size','in_settlement_window','exchange_event']
parts = []
for rec in receipt['row_files']:
    rf = repo/rec['file']
    a = pq.read_table(rf, columns=fields).to_pandas()
    b = pq.read_table(repo/rf.name.replace('rows-', 'calc-research_columns-'), columns=['position_on_tape','dipole_60s','exhaustion_20s']).to_pandas()
    assert a.position_on_tape.equals(b.position_on_tape) and len(a)==rec['rows']
    parts.append(a.assign(D=b.dipole_60s,E=b.exhaustion_20s))
a=pd.concat(parts,ignore_index=True)
assert (a.position_on_tape.diff().dropna()==1).all()
a=a.loc[a.row_label.eq('trade day')].copy()
assert len(a)==receipt['checks']['rows']['rows_by_label']['trade day']
assert a.received_time_ns.is_monotonic_increasing
# Compare stored output with the eligible stored read, even within a timestamp.
for k,stem in [('D','lean-60s'),('E','line-20s')]:
    line=pq.read_table(repo/'crypto-ng-tick'/f'crypto-ng-tick-{stem}-{day}.parquet',columns=['moment_received_ns','position_on_tape','flow']).to_pandas()
    keys=np.rec.fromarrays([line.moment_received_ns.to_numpy(),line.position_on_tape.fillna(-1).astype('int64').to_numpy()],names=['ns','pos'])
    assert np.array_equal(keys.argsort(kind='stable'),np.arange(len(keys)))
    target=np.rec.fromarrays([a.received_time_ns.to_numpy(),a.position_on_tape.to_numpy()],names=['ns','pos'])
    i=np.searchsorted(keys,target,side='right')-1
    expected=np.where(i<0,np.nan,line.flow.to_numpy()[np.maximum(i,0)])
    assert np.array_equal(expected,a[k].to_numpy(),equal_nan=True), k
a['segment']=(a.in_settlement_window.ne(False)|a.position_on_tape.diff().gt(1)).cumsum()
t=a.loc[a.action.eq('T') & a.in_settlement_window.eq(False)].copy()
names={'position_on_tape':'pos','received_time_ns':'recv_ns','exchange_time_ns':'exch_ns','exchange_event':'event','price':'px','best_bid':'bid','best_ask':'offer','best_bid_size':'bid_qty','best_ask_size':'offer_qty'}
t=t.rename(columns=names)
fields=['segment','pos','recv_ns','exch_ns','event','side','px','bid','offer','bid_qty','offer_qty','D','E']
t=t[fields].reset_index(drop=True)
# Check the aggressor mapping against the independent stored tape of prints.
ref=pq.read_table(repo/'crypto-ng-tick'/f'crypto-ng-tick-tape-trades-{day}.parquet',
                  columns=['position_on_tape','side','received_time_ns']).to_pandas().set_index('position_on_tape')
actual=ref.loc[t.pos]
assert np.array_equal(t.recv_ns.to_numpy(),actual.received_time_ns.to_numpy())
assert np.array_equal(t.side.map({'B':'buy','A':'sell'}).fillna('').to_numpy(),
                      actual.side.fillna('').to_numpy())
# Pair by position. Avoid shift on int64 nanoseconds, which coerces through float.
p=t.iloc[:-1].reset_index(drop=True)
q=t.iloc[1:].reset_index(drop=True)
ok=p.segment.eq(q.segment)
bp=(p.D>0)&(p.E>0); bn=(p.D<0)&(p.E<0)
up=(q.D>0)&(q.E>0); dn=(q.D<0)&(q.E<0)
pairs=[
(bp & up & (q.px>p.px)),(bn & dn & (q.px<p.px)),
((p.D>0)&(p.E<=0)&up),((p.D<0)&(p.E>=0)&dn),
(bp&(q.D>0)&(q.E<0)),(bn&(q.D<0)&(q.E>0)),
((p.px==p.offer)&(q.offer>p.offer)&(q.px==q.offer)),
((p.px==p.bid)&(q.bid<p.bid)&(q.px==q.bid)),
((p.px==p.offer)&(p.E>0)&(q.offer==p.offer)&(q.px<p.px)),
((p.px==p.bid)&(p.E<0)&(q.bid==p.bid)&(q.px>p.px)),
((p.D>0)&(q.bid>p.bid)&(q.offer==p.offer)&(q.D>0)),
((p.D<0)&(q.offer<p.offer)&(q.bid==p.bid)&(q.D<0)),
((p.D<0)&(q.px>p.px)&(q.E<0)),
((p.D>0)&(q.px<p.px)&(q.E>0)),
((p.E*q.E<0)&(p.px==q.px))]
case=pd.concat([p.drop(columns='segment').add_prefix('p_'),q.drop(columns='segment').add_prefix('q_')],axis=1)
for n,mask in enumerate(pairs,1):
    case[f'CX{n:02}']=mask & ok
ids=[f'CX{n:02}' for n in range(1,16)]
# Qualifying market observations only. Active positions exist only in paper trading.
extra=[
    (q.event!=p.event)&(q.bid>p.bid),
    (q.event!=p.event)&(q.bid<p.bid)&(q.side=='A'),
    (q.side=='B')&(q.px==q.offer),
    (q.side=='A')&(q.px==q.bid)&(q.offer<=p.offer),
    (q.bid<p.bid), (q.offer>p.offer),
    (q.bid==p.bid)&(q.side=='B'), (q.offer==p.offer)&(q.side=='A'),
    (q.bid<p.bid), (q.offer>p.offer),
    (q.px==q.bid)&(q.side=='A'), (q.px==q.offer)&(q.side=='B'),
    (q.bid<=p.bid)&(q.side=='B'), (q.offer>=p.offer)&(q.side=='A'),
    (q.bid==p.bid)&(q.offer==p.offer)&(((q.E>0)&(q.side=='B'))|((q.E<0)&(q.side=='A')))]
for name,condition in zip(ids,extra):
    case[name+'_v2_market']=case[name] & condition
case=case.loc[case[ids].any(axis=1)]
case.to_parquet(dest/f'pairs-{day}.parquet',compression='zstd',index=False)
print(day, len(a),'aligned trade-day ticks')
for n in ids:
    view=case.loc[case[n],['p_pos','q_pos','p_px','q_px','p_bid','q_bid','p_offer','q_offer','q_side','p_event','q_event']]
    print(n, view.head(1).to_string(header=False,index=False).strip())
