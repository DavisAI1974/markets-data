"""Flatten the Oct 18 full-population joined inputs into one row per trade.
Only values known strictly before the trade ('before' book, last_completed_group_before_trade S) plus the trade itself."""
import pyarrow.parquet as pq, glob, json, sys, pandas as pd
D='/home/user/markets-data/tasks/family-research-20261022/research-union-current/field-rebuild-20261113/original_full_population/'+sys.argv[1]
rows=[]
for f in sorted(glob.glob(D+'/*.parquet')):
    t=pq.read_table(f).to_pylist()
    for r in t:
        o=dict(ordinal=r['trade_ordinal'],cursor=int(r['trade_cursor']),event_ns=int(r['event_ns']),receive_ns=int(r['receive_ns']),known_by_ns=int(r['known_by_ns']),coverage=r['coverage'])
        tr=json.loads(r['L034 | order_lifecycle_trades'])
        if tr.get('status')=='ORIGINAL_VALUES_JOINED':
            v=tr['values']; o.update(price=v['price_raw'],size=v['size'],side=v['aggressor_side'],group=v['group_ordinal'],stretch=v.get('stretch_id'),print_step=v.get('print_step_raw'))
        sp=json.loads(r['L045 | spread_and_depth_imbalance'])
        if sp.get('status')=='ORIGINAL_VALUES_JOINED':
            for ph in ('before','during'):
                b=sp['values'][ph]
                for k in ('bid_price_raw','ask_price_raw','bid_size','ask_size','bid_full_size','ask_full_size'): o[f'{ph}_{k}']=b.get(k)
            o['before_known_by']=json.loads(r['L029 | raw_source_identity_provenance_clocks_integrity'])['values']['before']['known_by_ns']
        oc=json.loads(r['L040 | price_level_and_order_counts'])
        if oc.get('status')=='ORIGINAL_VALUES_JOINED':
            for k,v in oc['values']['before'].items(): o['before_'+k]=v
        fl=json.loads(r['L053 | missingness_and_integrity_flags'])
        if fl.get('status')=='ORIGINAL_VALUES_JOINED':
            o['flag_any']=any(fl['values'][ph][k] for ph in ('before','during') for k in fl['values'][ph])
        for n in r:
            if n[0]=='S' and n[1:3].isdigit():
                s=json.loads(r[n])
                if s.get('status')=='ORIGINAL_SECOND_SET_WITH_STATES':
                    for ph,short in (('last_completed_group_before_trade','lc'),('previous_input','pi')):
                        x=s['values'].get(ph)
                        if x: o[f'{n[:3]}_{short}']=x['raw_float64'] if x['state']=='PRESENT' else None; o[f'{n[:3]}_{short}_state']=x['state']
        rows.append(o)
df=pd.DataFrame(rows).sort_values('cursor').reset_index(drop=True)
df.to_parquet(f'/home/user/work/out/flat_{sys.argv[1]}.parquet')
print(len(df)); print(df.notna().sum().to_string())
