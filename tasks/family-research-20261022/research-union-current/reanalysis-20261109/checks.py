from pathlib import Path
import pandas as pd,numpy as np,json,zipfile,sys
P=Path(__file__).parent; R=P.parent
sys.path.insert(0,str(R))
from priority_cell_analysis import sheets,rows
f=pd.read_csv(R/'discovery-depth/family_derived.csv',dtype=str).set_index('excel_row')
cols=['ob_add_touch_b_5s','ob_add_touch_a_5s','ob_rm_cx_touch_b_5s','ob_rm_cx_touch_a_5s','tk_20s','f5']
with zipfile.ZipFile(R/'current/Frankie_four_day_research_current.xlsx') as z:
    selection=json.loads((R/'priority-now/priority_selection.json').read_text())['families'][1]
    checked=0
    for rowno,rec in rows(z,sheets(z)[selection['sheet']]):
        saved=f.loc[str(rowno)]
        for col in cols:
            a=rec.get(col);b=saved[col]
            if pd.isna(b):assert a in ('',None,'nan','None','NA')
            elif col=='f5':assert a==b
            else:assert np.isclose(float(a),float(b),atol=1e-12)
            checked+=1
x=pd.read_csv(P/'reanalysis_rows.csv',dtype=str)
for c in ['touch_imb','future1','future20','mi_level','log_signed_C','native5_imb','fresh_imb5']:x[c]=pd.to_numeric(x[c],errors='coerce')
cases=[];recount=[]
for day,g in x.groupby('day'):
    d=np.sign(g.touch_imb).replace(0,np.nan);rem=d*(g.future20-g.future1);confirm=d*g.future1>=1
    masks={'zero_MI_large_C':(g.mi_level.abs()<1e-12)&(g.log_signed_C.abs()>15),'native_proxy_opposite':g.native_proxy5_relation.eq('opposed'),
           'confirmed_then_positive':confirm&(rem>0),'confirmed_then_negative':confirm&(rem<0),'confirmed_then_flat':confirm&rem.eq(0),
           'native_proxy_count_difference':(pd.to_numeric(g.native5_buy)!=pd.to_numeric(g.fresh_buy5))|(pd.to_numeric(g.native5_sell)!=pd.to_numeric(g.fresh_sell5))}
    for label,mask in masks.items():
        for _,v in g[mask].sort_values('decision_ns').head(2).iterrows():
            cases.append(dict(finding=label,day=day,candidate_id=v.candidate_id,decision_ns=v.decision_ns,p09_excel_row=v.excel_row_left,p10_excel_row=v.excel_row_right,
                p01_first_row=v.native5_first_excel,p01_last_row=v.native5_last_excel,touch=v.touch_imb,proxy5=v.fresh_imb5,native5=v.native5_imb,mi_level=v.mi_level,
                log_C=v.log_signed_C,move1=v.future1,move20=v.future20,remaining_touch20=float(np.sign(v.touch_imb)*(v.future20-v.future1)),source_id_p09=v.source_id_left,source_id_p10=v.source_id_right,flow_source_url=v.source_flow_url))
    vals=[]
    for _,v in g.iterrows():
        direction=1 if v.touch_imb>0 else -1 if v.touch_imb<0 else None
        if direction is not None and pd.notna(v.future1) and direction*v.future1>=1 and pd.notna(v.future20):vals.append(direction*(v.future20-v.future1))
    recount.append(dict(day=day,n=len(vals),mean=sum(vals)/len(vals)))
pd.DataFrame(cases).to_csv(P/'CASES.csv',index=False)
prior=pd.read_csv(P/'confirmation_remaining.csv',dtype={'day':str})
for v in recount:
    row=prior[(prior.day==v['day'])&(prior.direction=='touch')&(prior.delay==1)&(prior.horizon==20)&(prior.subset=='all')&(prior.state=='confirmed_1tick')].iloc[0]
    assert row['n']==v['n'] and np.isclose(row['mean'],v['mean'])
(P/'INDEPENDENT_CHECKS.json').write_text(json.dumps(dict(family_cells_rechecked=checked,confirmation_recount=recount,source_linked_cases=len(cases)),indent=2),encoding='utf-8')
print('Independent checks',checked,'family cells;',len(cases),'cases')
