import json,hashlib
import pandas as pd
import numpy as np
import discovery_depth as D
O=D.O
seed=pd.read_csv(O/'CASES.csv',dtype=str).fillna('')
cases=seed[seed.claim_id=='D01'].to_dict('records')
urls={s['id']:s['url'] for item in D.S for s in item['sources']}
def add(claim,r,state,extra,rank,decision=''):
 extra={k:None if isinstance(v,float) and np.isnan(v) else v for k,v in extra.items()}
 cases.append({'claim_id':claim,'day':str(r['day']),'event_id':str(r.get('event_id',r.get('candidate_id',r.get('family_id','')))),'order_id':str(r.get('order_id','')),'state':state,'decision_ns':str(decision),'observation_excel_sheet':D.S[rank-1]['sheet'],'observation_excel_row':str(r['excel_row']),'source_id':str(r['source_id']),'source_row':str(r['source_row']),'source_url':urls[str(r['source_id'])],'additional_values':json.dumps(extra,default=str,sort_keys=True),'limit':'Deterministic illustrative case; full-population tables determine the finding.'})
e=pd.read_csv(O/'event_interval_order_cases.csv',dtype=str)
for _,g in e.groupby(['day','interval_order']):
 r=g.sort_values('excel_row',key=lambda s:s.astype(int)).iloc[0].to_dict();add('D02',r,r['interval_order'],{k:r[k] for k in ['k_aggressor_start','k_quote_relocation','delay_s','last_k_on_tape']},8)
r=pd.read_csv(O/'recognition_joined.csv',dtype={'day':str,'recognition_receive_ns':str,'decision_ns':str})
for key,g in r.groupby(['day','flow_vs_touch']):
 for sign in [-1,0,1]:
  v=g[np.sign(g.touch_oriented_20)==sign]
  if not len(v):continue
  row=v.sort_values('excel_row_left').iloc[0].to_dict();row.update(excel_row=row['excel_row_right'],source_id=row['source_id_right'],source_row=row['source_row_right'])
  add('D04',row,key[1]+'; touch-oriented outcome sign '+str(sign),{k:row[k] for k in ['candidate_id','fresh_imb5','touch_imb','prior_ticks20','touch_oriented_20','future20','excel_row_left','source_id_left','source_row_left']},10,row['decision_ns'])
f=pd.read_csv(O/'family_derived.csv',dtype={'day':str,'cutoff_ns':str,'start_recv_ns':str})
for key,g in f[f.f5_vs_f60.isin(['aligned','opposed'])].groupby(['day','f5_vs_f60']):
 for sign in [-1,0,1]:
  v=g[np.sign(g.f5_oriented_20)==sign]
  if len(v):
   row=v.sort_values('excel_row').iloc[0].to_dict();add('D05',row,key[1]+'; flow-oriented outcome sign '+str(sign),{k:row[k] for k in ['f5','f60','tk_20s','f5_oriented_20','start_recv_ns','grp_20s']},2,row['cutoff_ns'])
for day,g in f.groupby('day'):
 row=g.dropna(subset=['ob_fill_b_5s','ob_trade_sellagg_5s']).sort_values('excel_row').iloc[0].to_dict();add('D07',row,'paired passive fill/aggressor quantity',{'ob_fill_b_5s':row['ob_fill_b_5s'],'ob_trade_sellagg_5s':row['ob_trade_sellagg_5s']},2,row['cutoff_ns'])
x=D.load(7).sort_values(['day','onset_ns','onset_cursor']).drop_duplicates(['day','order_id'])
for key,g in x.groupby(['day','origin','onset','outcome']):
 row=g.sort_values('excel_row').iloc[0].to_dict();add('D06',row,'; '.join(key[1:]),{k:row[k] for k in ['origin','onset','age_ms','prior_onsets_by_order','outcome','end_ns','end_ms']},7,row['onset_ns'])
c=pd.read_csv(O/'lean_control_comparisons.csv',dtype={'day':str})
for _,row in c[(c.seconds_from_birth==-5)&(c.metric=='p50')].iterrows():
 rr=row.to_dict();rr.update(source_id=rr['source_id_cohort'],source_row=rr['source_row_cohort'],excel_row=rr['excel_row_cohort'])
 add('D08',rr,'aggregate lean at retrospective birth minus 5 seconds',{k:rr[k] for k in ['cohort','control_median','control_draw_lo','control_draw_hi','source_id_control','source_row_control','excel_row_control']},8)
flow=D.load(1);flow['sec']=flow.second.map(int)
for col in ['native_ratio','native_buy','native_sell','native_roll_buy','native_roll_sell']:flow[col]=D.num(flow,col)
flow=flow.sort_values(['day','sec']);prev=flow.groupby('day').shift();future=flow.groupby('day').shift(-5)
flow['flip']=(flow.sec-prev.sec==1)&(flow.native_ratio*prev.native_ratio<0)
expiry=prev.native_roll_buy+prev.native_roll_sell+flow.native_buy+flow.native_sell-flow.native_roll_buy-flow.native_roll_sell
flow['driver']=np.where(flow.native_buy+flow.native_sell==0,'expiry without classified arrivals',np.where(expiry>1e-9,'mixed arrival and expiry','classified arrival without expiry'))
flow['future_ratio_5']=future.native_ratio;flow['future_excel_row']=future.excel_row;flow['same_sign_5']=np.sign(flow.native_ratio)==np.sign(future.native_ratio)
for key,g in flow[flow.flip&(future.sec-flow.sec==5)].groupby(['day','driver','same_sign_5']):
 row=g.sort_values('excel_row').iloc[0].to_dict();add('D03',row,key[1]+'; same sign after 5s '+str(key[2]),{k:row[k] for k in ['second','native_ratio','native_buy','native_sell','future_ratio_5','future_excel_row']},1,row['completed_second_known_by_ns'])
pd.DataFrame(cases).to_csv(O/'CASES.csv',index=False)
claims=pd.read_csv(O/'CLAIMS.csv')
support={'D01':'resting_price_results.csv; all_conditional_results.csv; resting_prefix_audit.json','D02':'event_interval_order_counts.csv; timing_definition_correction.json','D03':'all_conditional_results.csv; INDEPENDENT_CHECKS.json','D04':'recognition_paired_comparison.csv; all_conditional_results.csv','D05':'all_conditional_results.csv; candidate_control_results.csv','D06':'origin_onset_results.csv; all_conditional_results.csv','D07':'family_field_screen.csv; field_redundancy.csv','D08':'lean_control_comparisons.csv; all_conditional_results.csv'}
claims['dates']='2023-10-02;2023-10-03;2023-10-17;2023-10-18';claims['supporting_tables']=claims.claim_id.map(support);claims['case_file']='CASES.csv (claim_id)';claims['source_authority']='priority_selection.json at input commit 1c234d511e26a0d1d054a39dbafc8a436232e7bb; supplementary_source_manifest.json';claims['measured_warning_lead']='Not established; source intervals/recognition delays/outcome horizons are separate quantities';claims.to_csv(O/'CLAIMS.csv',index=False)
receipt={'projection_files':[{'file':item['data_file'],'rows':item['rows'],'sha256':hashlib.sha256((D.P/item['data_file']).read_bytes()).hexdigest()} for item in D.S],'illustrative_cases':len(cases),'case_claims':sorted({c['claim_id'] for c in cases}),'source_population_policy':'No case selection changes statistical populations. Multiple cases/events and outcomes can be correlated.','shared_brief_path':'E:/frankie-excel-review-20261109/extended-review-data/branch-reading/codex/agent-pass/reanalysis/SHARED_BRIEF.md'}
bp=__import__('pathlib').Path(receipt['shared_brief_path']);receipt['shared_brief_sha256']=hashlib.sha256(bp.read_bytes()).hexdigest()
(O/'INPUT_AND_CASE_RECEIPT.json').write_text(json.dumps(receipt,indent=2))
print('ALL CLAIMS HAVE SOURCE CASES',len(cases),receipt['case_claims'])
