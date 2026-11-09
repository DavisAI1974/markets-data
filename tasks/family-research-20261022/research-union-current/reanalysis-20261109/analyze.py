"""Reanalysis on frozen, cell-verified populations; no execution or native replay."""
import gzip, hashlib, json, math, sys, types
from pathlib import Path
import numpy as np
import pandas as pd

O=Path(__file__).parent; R=O.parent
sys.path.insert(0,str(R))
from priority_cell_analysis import sheets, rows
import zipfile

def sign(v):
    return 'missing' if pd.isna(v) else '+' if v>1e-10 else '-' if v< -1e-10 else '0'

def relation(a,b):
    return 'missing' if 'missing' in (a,b) else 'neutral' if '0' in (a,b) else 'aligned' if a==b else 'opposed'

def stats(v):
    v=pd.to_numeric(v,errors='coerce').dropna()
    return dict(n=len(v),mean=float(v.mean()) if len(v) else None,median=float(v.median()) if len(v) else None,
                positive=int((v>1e-9).sum()),negative=int((v< -1e-9).sum()),flat=int((v.abs()<=1e-9).sum()))

def ridge(train,y,test):
    finite=np.isfinite(train)
    m=np.divide(np.where(finite,train,0).sum(axis=0),finite.sum(axis=0),out=np.zeros(train.shape[1]),where=finite.sum(axis=0)>0)
    a=np.c_[np.where(finite,train,m),~finite];b=np.c_[np.where(np.isfinite(test),test,m),~np.isfinite(test)]
    mean=a.mean(axis=0);std=a.std(axis=0);std[std==0]=1
    a=(a-mean)/std;b=(b-mean)/std;ym=y.mean()
    coef=np.linalg.solve(a.T@a+10*np.eye(a.shape[1]),a.T@(y-ym))
    return ym+b@coef

def delayed_return(final,confirmation,direction):
    return direction*(final-confirmation)

def window_availability(values,decision_ns):
    if not all(v is not None for v in values):return False,'missing_bins',None
    if not all(v[3] is not None for v in values):return False,'unknown_completion',None
    latest=max(v[3] for v in values)
    return latest<=decision_ns,'available' if latest<=decision_ns else 'not_yet_known',latest

def main():
    x=pd.read_csv(R/'discovery-depth/recognition_joined.csv',dtype=str)
    numeric=['early_buy','early_sell','late_buy','late_sell','fresh_buy5','fresh_sell5','fresh_imb5','touch_imb','touch_count_imb','prior_ticks20','range_ticks20','spread_ticks','ent_dipole','mi_flow','imb_flow','imb_level','log_signed_C','strength_change','bid_add5','bid_remove5','ask_add5','ask_remove5','quote_price_changes5','log_touch_lots','log_touch_orders','log_unknown_lots5']
    for c in numeric+[f'future{h}' for h in (1,5,20,60,300)]:x[c]=pd.to_numeric(x[c],errors='coerce')
    assert len(x)==3176 and not x.duplicated(['day','candidate_id']).any()
    # Check consequential original worksheet values directly, not only cached CSVs.
    checked=0
    with zipfile.ZipFile(R/'current/Frankie_four_day_research_current.xlsx') as z:
        mapping=sheets(z)
        for rank,cols,suffix in [(9,[f'move_ticks_after_recognition.{h}' for h in (1,5,20,60,300)],'left'),(10,numeric+['decision_ns','quote_known_by_ns','flow_closed_by_ns'],'right')]:
            selection=json.loads((R/'priority-now/priority_selection.json').read_text())['families'][rank-1]
            byrow=x.set_index('excel_row_'+suffix)
            for n,rec in rows(z,mapping[selection['sheet']]):
                row=byrow.loc[str(n)]
                for c in cols:
                    actual=rec.get(c);expected=row[c] if c in row else None
                    if c.startswith('move_ticks_after_recognition.'):
                        expected=row['future'+c.rsplit('.',1)[1]]
                    if c.endswith('_ns'):
                        assert int(actual)==int(expected)
                    elif expected is None or pd.isna(expected):assert actual in (None,'','nan','None','NA')
                    else:assert np.isclose(float(actual),float(expected),atol=1e-12,rtol=1e-12),(n,c,actual,expected)
                    checked+=1
    sources=json.loads((R/'active_sources.json').read_text(encoding='utf-8'))
    src={v['path'].split('/')[3]:v for v in sources if 'replay-comparison/' in v['path'] and v['path'].endswith('dipole-completed-group-flow.csv.gz')}
    native={};native_locations={}
    with gzip.open(R/'priority-now/P01.jsonl.gz','rt',encoding='utf-8') as f:
        for excelrow,line in enumerate(f,2):
            rec=json.loads(line);v=rec['values'];key=(rec['day'],int(v['second']))
            clock=v['completed_second_known_by_ns']
            native[key]=(float(v['native_buy']),float(v['native_sell']),float(v['native_unknown']),int(clock) if clock is not None else None)
            native_locations[key]=(excelrow,rec['source_id'],rec['source_row'])
    raw=(R/'objects/c04751cbe5f92952e33328f6c04fcae6392e05e5').read_bytes()
    assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()=='c04751cbe5f92952e33328f6c04fcae6392e05e5'
    operator=types.ModuleType('pinned_operator');exec(compile(raw,'pinned_operator','exec'),operator.__dict__)
    audits=[];data=[]
    for day,part in x.groupby('day'):
        source=src[day];blob=R/'objects'/source['sha'];blobraw=blob.read_bytes()
        assert hashlib.sha1(b'blob '+str(len(blobraw)).encode()+b'\0'+blobraw).hexdigest()==source['sha']
        f=pd.read_csv(blob,compression='gzip').set_index('second')
        for idx,row in part.iterrows():
            end=int(row.flow_closed_by_ns)//10**9-1;t=int(row.decision_ns)
            bins=f.loc[end-19:end];assert len(bins)==20
            b=bins.buy.to_numpy();s=bins.sell.to_numpy()
            op=operator.signed_flow_features(b,s)
            base=dict(index=idx,active_buy_bins=int((b>0).sum()),active_sell_bins=int((s>0).sum()),active_either_bins=int(((b+s)>0).sum()),
                      source_flow_id=source['id'],source_flow_sha=source['sha'],source_flow_url=source['url'],proxy_first_second=end-19,proxy_last_second=end)
            assert np.isclose(b[-5:].sum(),row.fresh_buy5) and np.isclose(s[-5:].sum(),row.fresh_sell5)
            for feature in ['imb_level','ent_dipole','mi_flow','imb_flow']:
                expected=None if op is None else op[feature];actual=row[feature]
                assert pd.isna(actual) if expected is None else np.isclose(actual,expected,atol=1e-10),feature
            if op is not None:
                logged=np.sign(op['C_signed'])*np.log1p(abs(op['C_signed']))
                assert np.isclose(row.log_signed_C,logged)
            base['mi_level']=operator.mutual_info(b,s)
            base['total_proxy20']=float((b+s).sum())
            base['entropy_defined']=op is not None
            for window in (5,20):
                keys=[(day,sec) for sec in range(end-window+1,end+1)]
                vals=[native.get(k) for k in keys]
                present=all(v is not None for v in vals)
                known,reason,latest=window_availability(vals,t)
                base[f'native{window}_available']=known
                base[f'native{window}_max_known_by_ns']=str(latest) if latest is not None else ''
                base[f'native{window}_reason']=reason
                for j,label in enumerate(['buy','sell','unknown']):base[f'native{window}_{label}']=sum(v[j] for v in vals) if known else np.nan
                buy=base[f'native{window}_buy'];sell=base[f'native{window}_sell']
                base[f'native{window}_imb']=(buy-sell)/(buy+sell) if known and buy+sell else np.nan
                base[f'native{window}_first_excel']=native_locations[keys[0]][0] if present else None
                base[f'native{window}_last_excel']=native_locations[keys[-1]][0] if present else None
            data.append(base)
        audits.append(dict(day=day,source_id=source['id'],sha=source['sha'],rows=len(f)))
    x=x.join(pd.DataFrame(data).set_index('index'))
    x['native5_sign']=x.native5_imb.map(sign);x['proxy5_sign']=x.fresh_imb5.map(sign)
    x['native20_sign']=x.native20_imb.map(sign);x['proxy20_sign']=x.imb_level.map(sign)
    x['native_proxy5_relation']=[relation(a,b) for a,b in zip(x.native5_sign,x.proxy5_sign)]
    x['native_proxy20_relation']=[relation(a,b) for a,b in zip(x.native20_sign,x.proxy20_sign)]
    x['display5']=(x.bid_add5-x.bid_remove5)-(x.ask_add5-x.ask_remove5)
    table=[]
    for window in (5,20):
        for key,g in x.groupby(['day',f'native{window}_reason',f'native{window}_sign',f'proxy{window}_sign'],dropna=False):
            table.append(dict(day=key[0],window=window,availability=key[1],native_sign=key[2],proxy_sign=key[3],rows=len(g)))
    pd.DataFrame(table).to_csv(O/'classification_comparison.csv',index=False)
    entropy=[]
    for day,g in x.groupby('day'):
        defined=g[g.entropy_defined]
        entropy.append(dict(day=day,rows=len(g),defined=len(defined),both_empty=int((g.total_proxy20==0).sum()),
            active_at_most2=int((defined.active_either_bins<=2).sum()),mi_zero=int((defined.mi_level.abs()<1e-12).sum()),
            mi_flow_zero=int((defined.mi_flow.abs()<1e-12).sum()),log_C_gt15=int((defined.log_signed_C.abs()>15).sum()),
            ent_exact_extreme=int(np.isclose(defined.ent_dipole.abs(),1,atol=1e-7).sum())))
    pd.DataFrame(entropy).to_csv(O/'entropy_sparsity.csv',index=False)
    # Fixed earlier-day training; no search, test-set scaling or complete-case deletion.
    baseline=['prior_ticks20','range_ticks20','spread_ticks','touch_imb','touch_count_imb','log_touch_lots','log_touch_orders','early_buy','early_sell','late_buy','late_sell','fresh_buy5','fresh_sell5']
    info=['ent_dipole','mi_flow','log_signed_C','imb_flow']
    display=['bid_add5','bid_remove5','ask_add5','ask_remove5','quote_price_changes5']
    models={'counts_price_book':baseline,'plus_information':baseline+info,'plus_display':baseline+display,'plus_both':baseline+info+display}
    model_results=[];predictions=[]
    days=sorted(x.day.unique())
    for day in days[1:]:
        train=x[(x.day<day)&x.future20.notna()];test=x[(x.day==day)&x.future20.notna()]
        for name,cols in models.items():
            pred=ridge(train[cols].to_numpy(float),train.future20.to_numpy(float),test[cols].to_numpy(float))
            for subset,mask in [('all',np.ones(len(test),dtype=bool)),('separated60',test.separated60.eq('True').to_numpy())]:
                y=test.future20.to_numpy()[mask];pr=pred[mask]
                model_results.append(dict(day=day,model=name,subset=subset,train_rows=len(train),test_rows=len(y),
                    mse=float(np.mean((y-pr)**2)),mae=float(np.mean(abs(y-pr))),mean_prediction=float(pr.mean()),
                    directional_mean_ticks=float(np.mean(np.sign(pr)*y)),positive=int((np.sign(pr)*y>0).sum()),negative=int((np.sign(pr)*y<0).sum()),flat=int((y==0).sum())))
            for (_,row),pr in zip(test.iterrows(),pred):predictions.append(dict(day=day,candidate_id=row.candidate_id,model=name,prediction=pr,actual=row.future20))
    pd.DataFrame(model_results).to_csv(O/'incremental_models.csv',index=False)
    pd.DataFrame(predictions).to_csv(O/'model_predictions.csv',index=False)
    delay_results=[]
    for label,col in [('touch','touch_imb'),('proxy_flow','fresh_imb5'),('native_flow','native5_imb')]:
        direction=np.sign(x[col]).replace(0,np.nan)
        for delay in (1,5):
            first=direction*x[f'future{delay}']
            state=np.where(first.isna(),'unavailable',np.where(first>=1-1e-9,'confirmed_1tick',np.where(first<=-1+1e-9,'opposite_1tick',np.where(first.abs()<1e-9,'flat','subtick'))))
            temp=x.assign(confirm_state=state)
            for horizon in (20,60):
                temp['remaining']=delayed_return(x[f'future{horizon}'],x[f'future{delay}'],direction)
                temp['from_recognition']=direction*x[f'future{horizon}']
                for subset,mask in [('all',np.ones(len(x),dtype=bool)),('separated60',x.separated60.eq('True').to_numpy())]:
                    for (day,st),g in temp[mask].groupby(['day','confirm_state']):
                        delay_results.append(dict(day=day,direction=label,delay=delay,horizon=horizon,subset=subset,state=st,population=len(g),
                            from_recognition_mean=float(g.from_recognition.mean()) if g.from_recognition.notna().any() else None,**stats(g.remaining)))
    pd.DataFrame(delay_results).to_csv(O/'confirmation_remaining.csv',index=False)
    f=pd.read_csv(R/'discovery-depth/family_derived.csv',dtype=str)
    for c in ['f5','f60']:f[c+'_direction']=f[c].map({'+':1,'-':-1,'0':0})
    for c in ['touch_imb','tk_5s','tk_20s','tk_60s','root.mid','ref_mid','ob_add_touch_b_5s','ob_add_touch_a_5s','ob_rm_cx_touch_b_5s','ob_rm_cx_touch_a_5s']:
        f[c]=pd.to_numeric(f[c],errors='coerce')
    f['addition_balance']=f.ob_add_touch_b_5s-f.ob_add_touch_a_5s
    f['cancel_support_balance']=f.ob_rm_cx_touch_a_5s-f.ob_rm_cx_touch_b_5s
    f['net_add_cancel']=f.addition_balance+f.cancel_support_balance
    family_results=[]
    for driver in ('addition_balance','cancel_support_balance','net_add_cancel'):
        f[driver+'_vs_flow']=[relation(sign(a),sign(b)) for a,b in zip(f[driver],f.f5_direction)]
        f[driver+'_vs_touch']=[relation(sign(a),sign(b)) for a,b in zip(f[driver],f.touch_imb)]
        for grouping in (driver+'_vs_flow',driver+'_vs_touch'):
            for (day,state),g in f.groupby(['day',grouping]):
                for horizon in (5,20,60):
                    outcome=g[f'tk_{horizon}s']
                    family_results.append(dict(day=day,driver=driver,comparison=grouping,state=state,horizon=horizon,population=len(g),**stats(np.sign(g[driver]).replace(0,np.nan)*outcome)))
    pd.DataFrame(family_results).to_csv(O/'family_book_activity.csv',index=False)
    x.to_csv(O/'reanalysis_rows.csv',index=False)
    f[['day','family_id','source_id','excel_row','addition_balance','cancel_support_balance','net_add_cancel','f5_direction','touch_imb','tk_5s','tk_20s','tk_60s']].to_csv(O/'family_activity_rows.csv',index=False)
    audit=dict(recognition_rows=len(x),family_rows=len(f),direct_excel_cells_checked=checked,entropy_operator_reproduced_rows=len(x),source_flow=audits,
        parameters=dict(ridge_penalty=10,confirmation_ticks=1,delays=[1,5],horizons=[20,60],model_train='all strictly earlier dates',evaluation='already-used discovery dates'),
        paper_policy='Every defined strategy is included in paper testing. Weak or conflicting results are retained.',session_setup='Deferred by user; Henry Hub December 2026 assumed; Tradovate demo selected.')
    (O/'AUDIT.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
    print(json.dumps(audit,indent=2),flush=True)

if __name__=='__main__':main()
