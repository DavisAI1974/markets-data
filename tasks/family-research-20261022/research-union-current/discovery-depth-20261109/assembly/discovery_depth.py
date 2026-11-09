"""Independent conditional discovery from the complete, cell-verified priority populations."""
import collections,gzip,hashlib,json,math,statistics
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
R=Path(__file__).parent;P=R/'priority-now';O=R/'discovery-depth';O.mkdir(exist_ok=True)
S=json.loads((P/'priority_selection.json').read_text())['families']
def load(rank):
 item=S[rank-1];records=[]
 with gzip.open(P/item['data_file'],'rt',encoding='utf8') as f:
  for rowno,line in enumerate(f,2):
   r=json.loads(line);records.append(dict(r['values'],day=r['day'],source_id=r['source_id'],source_row=r['source_row'],source_table=r['source_type'],excel_row=rowno))
 d=pd.DataFrame(records);assert len(d)==item['rows'];return d
def num(d,c):return pd.to_numeric(d[c].replace({'True':1,'False':0,'true':1,'false':0}),errors='coerce')
def sgn(v):
 if pd.isna(v) or v in ('','NA','nan'):return 'missing'
 if v in ('+','-'):return v
 v=float(v);return '+' if v>0 else '-' if v<0 else '0'
def rel(a,b):return 'missing' if 'missing' in (a,b) else 'neutral' if '0' in (a,b) else 'aligned' if a==b else 'opposed'
def exact_join(left,right,key,lc,rc):
 assert not left.duplicated(key).any(),'duplicate left identity'
 assert not right.duplicated(key).any(),'duplicate right identity'
 x=left.merge(right,on=key,how='outer',suffixes=('_left','_right'),indicator=True,validate='one_to_one')
 matched=x[x['_merge']=='both']
 assert all(int(a)==int(b) for a,b in zip(matched[lc],matched[rc])),'clock disagreement'
 return x
def stats(values):
 v=pd.to_numeric(values,errors='coerce').dropna();return {'n':len(v),'mean':float(v.mean()) if len(v) else None,'median':float(v.median()) if len(v) else None,'positive':int((v>0).sum()),'negative':int((v<0).sum()),'flat':int((v==0).sum())}
tables=[];cases=[];audit={};frames={}
def summarize(d,study,groupings,targets):
 for keys in groupings:
  keys=['day']+keys
  for key,g in d.groupby(keys,dropna=False,sort=True):
   key=key if isinstance(key,tuple) else (key,)
   group=dict(zip(keys,[str(k) for k in key]))
   for target in targets:
    tables.append({'study':study,'grouping':' + '.join(keys[1:]) or 'all','day':group.pop('day',str(key[0])) if False else str(key[0]),'condition':json.dumps({k:v for k,v in group.items() if k!='day'},sort_keys=True),'population':len(g),'target':target,**stats(g[target])})
def save_case(d,study,label,cols):
 for day,g in d.groupby('day',sort=True):
  for outcome in ['positive','negative','flat']:
   if 'future20' not in g:continue
   v=g[g.future20>0] if outcome=='positive' else g[g.future20<0] if outcome=='negative' else g[g.future20==0]
   if not len(v):continue
   r=v.sort_values('excel_row_left' if 'excel_row_left' in v else 'excel_row').iloc[0]
   cases.append({'study':study,'condition':label,'day':day,'outcome':outcome,'values':{c:str(r[c]) for c in cols if c in r}})

def recognition():
 l=load(9);r=load(10)
 x=exact_join(l,r,['day','candidate_id'],'recognition_receive_ns','decision_ns')
 audit['recognition_join']={k:int(v) for k,v in x['_merge'].value_counts().items()};x=x[x['_merge']=='both'].copy()
 for c in ['prior_ticks20','touch_imb','touch_count_imb','fresh_imb5','strength_change','spread_ticks','range_ticks20','realised_by_recognition_ticks_in_birth_direction','polarity','bid_add5','ask_add5','bid_remove5','ask_remove5','log_touch_lots','log_touch_orders']:x[c]=num(x,c)
 for h in [1,5,20,60,300]:x[f'future{h}']=num(x,f'move_ticks_after_recognition.{h}')
 x['flow_sign']=x.fresh_imb5.map(sgn);x['touch_sign']=x.touch_imb.map(sgn);x['count_sign']=x.touch_count_imb.map(sgn);x['prior_price_sign']=x.prior_ticks20.map(sgn)
 x['touch_vs_count']=[rel(a,b) for a,b in zip(x.touch_sign,x.count_sign)];x['flow_vs_touch']=[rel(a,b) for a,b in zip(x.flow_sign,x.touch_sign)]
 x['prior_vs_touch']=[rel(a,b) for a,b in zip(x.prior_price_sign,x.touch_sign)];x['prior_vs_flow']=[rel(a,b) for a,b in zip(x.prior_price_sign,x.flow_sign)]
 x['spread_band']=x.spread_ticks.map(lambda v:'1 tick' if v==1 else '>1 tick' if v>1 else 'other/missing')
 x['price_runup_birth_sign']=x.realised_by_recognition_ticks_in_birth_direction.map(sgn)
 x['net_display5']=(x.bid_add5-x.bid_remove5)-(x.ask_add5-x.ask_remove5);x['net_display_sign']=x.net_display5.map(sgn)
 x['price_vs_net_display']=[rel(a,b) for a,b in zip(x.prior_price_sign,x.net_display_sign)]
 for label,col in [('flow','fresh_imb5'),('touch','touch_imb'),('count','touch_count_imb'),('prior','prior_ticks20'),('net_display','net_display5'),('birth','polarity')]:
  for h in [5,20,60]:x[f'{label}_oriented_{h}']=np.sign(x[col]).replace(0,np.nan)*x[f'future{h}']
 x['quarter']=x.recognition_receive_ns.map(lambda t:str((int(t)//10**9%86400)//21600))
 x['polarity_sign']=x.polarity.map(sgn)
 x=x.sort_values(['day','recognition_receive_ns'])
 keep=[];last={}
 for i,row in x.iterrows():
  t=int(row.recognition_receive_ns);yes=t-last.get(row.day,-10**30)>=60*10**9;keep.append(yes)
  if yes:last[row.day]=t
 x['separated60']=keep
 targets=['flow_oriented_20','touch_oriented_20','count_oriented_20','prior_oriented_20','net_display_oriented_20','birth_oriented_20','flow_oriented_60','touch_oriented_60','prior_oriented_60','birth_oriented_60']
 groups=[[],['flow_sign'],['dipole_state'],['flow_vs_touch'],['prior_vs_touch'],['prior_vs_flow'],['touch_vs_count'],['price_runup_birth_sign'],['price_vs_net_display'],['flow_vs_touch','prior_vs_flow'],['dipole_state','prior_vs_touch'],['flow_vs_touch','spread_band'],['flow_vs_touch','polarity_sign'],['flow_vs_touch','quarter']]
 summarize(x,'recognition_context',groups,targets);summarize(x[x.separated60],'recognition_context_separated60',[[],['dipole_state'],['flow_vs_touch'],['prior_vs_touch'],['prior_vs_flow'],['touch_vs_count'],['price_runup_birth_sign']],targets)
 for key in ['prior_vs_touch','flow_vs_touch','dipole_state']:
  for value,g in x.groupby(key):save_case(g,'recognition_context',key+'='+value,['candidate_id','excel_row_left','excel_row_right','source_id_left','source_row_left','source_id_right','source_row_right','recognition_receive_ns','decision_ns','flow_closed_by_ns','quote_known_by_ns','fresh_imb5','touch_imb','prior_ticks20','future20','future60'])
 x.to_csv(O/'recognition_joined.csv',index=False);frames['recognition']=x
 print('DISCOVERY recognition',len(x),flush=True)

def family():
 d=load(2)
 for h in [5,20,60]:d[f'future{h}']=num(d,f'tk_{h}s')
 for c in ['touch_imb','touch_n_imb','prior_tk_20s','root.depth_imbalance_full','root.depth_imbalance_n','spread_ticks']:d[c]=num(d,c)
 for name,c in [('touch','touch_imb'),('count','touch_n_imb'),('prior','prior_tk_20s'),('full','root.depth_imbalance_full'),('near','root.depth_imbalance_n')]:d[name+'_sign']=d[c].map(sgn)
 for c in ['f1','f5','f60']:d[c+'_sign']=d[c].map(sgn)
 for a,b in [('f5','f60'),('f1','f5'),('full','touch'),('near','touch'),('prior','f5'),('prior','touch')]:d[a+'_vs_'+b]=[rel(x,y) for x,y in zip(d[a+'_sign'],d[b+'_sign'])]
 for name,c in [('touch','touch_imb'),('full','root.depth_imbalance_full'),('near','root.depth_imbalance_n'),('prior','prior_tk_20s')]:
  for h in [5,20,60]:d[f'{name}_oriented_{h}']=np.sign(d[c]).replace(0,np.nan)*d[f'future{h}']
 for name in ['f1','f5','f60']:
  direction=d[name].map({'+':1,'-':-1})
  for h in [5,20,60]:d[f'{name}_oriented_{h}']=direction*d[f'future{h}']
 d['spread_band']=d.spread_ticks.map(lambda v:'1 tick' if v==1 else '>1 tick' if v>1 else 'other/missing')
 summarize(d,'family_depth_flow',[[],['full_vs_touch'],['near_vs_touch'],['f5_vs_f60'],['f1_vs_f5'],['prior_vs_f5'],['prior_vs_touch'],['f5_vs_f60','full_vs_touch'],['prior_vs_f5','spread_band']], [f'{name}_oriented_{h}' for name in ['touch','full','near','prior','f1','f5','f60'] for h in [5,20,60]])
 exclude=['_ns','cursor','ordinal','sample_id','family_id','instance','instrument_id','ref_group','source_id','source_row','excel_row','utc_hour','quarter','grp_','known_by','future','oriented','chg_','tk_']
 features=[];fieldaudit=[]
 for c in S[1]['fields']:
  if c.startswith(('prior_tk_','quote_changes_','groups_')):eligible=True
  else:eligible=not any(t in c for t in exclude)
  v=pd.to_numeric(d[c],errors='coerce')
  if eligible and v.notna().sum()>=40 and v.nunique()>1:features.append(c)
  fieldaudit.append({'field':c,'rows':len(d),'finite_numeric':int(v.notna().sum()),'unique_numeric':int(v.nunique()),'univariate_review':bool(eligible and v.notna().sum()>=40 and v.nunique()>1),'role':'outcome or administrative/clock' if not eligible else 'numeric context' if v.notna().sum() else 'categorical/provenance context'})
 screen=[]
 for c in features:
  allv=pd.to_numeric(d[c],errors='coerce')
  for day,g in d.groupby('day'):
   train=allv[d.day!=day].dropna();v=allv.loc[g.index];lo,hi=train.quantile([.25,.75]);valid=v.notna() & g.future20.notna()
   corr=float(spearmanr(v[valid],g.loc[valid,'future20']).statistic) if v[valid].nunique()>1 and g.loc[valid,'future20'].nunique()>1 else None
   low=g.loc[v<=lo,'future20'];high=g.loc[v>=hi,'future20']
   screen.append({'field':c,'day':day,'finite_pairs':int(valid.sum()),'spearman':corr,'other_days_q25':float(lo),'other_days_q75':float(hi),'low_n':int(low.notna().sum()),'high_n':int(high.notna().sum()),'low_mean':float(low.mean()),'high_mean':float(high.mean()),'high_minus_low':float(high.mean()-low.mean()),'constant_training_threshold':bool(lo==hi)})
 pd.DataFrame(screen).to_csv(O/'family_field_screen.csv',index=False);pd.DataFrame(fieldaudit).to_csv(O/'family_field_coverage.csv',index=False);audit['family_numeric_fields_reviewed']=len(features)
 d.to_csv(O/'family_derived.csv',index=False);frames['family']=d
 print('DISCOVERY family',len(d),len(features),'fields',flush=True)

def resting():
 e=load(4);e=e[e.source_table=='aggression-to-rest-events.csv'].copy();d=load(5)
 assert not e.duplicated(['day','event_id']).any();assert not d.duplicated(['day','event_id','delay_ms']).any()
 x=d.merge(e[['day','event_id','order_id','start_known_by_ns','end_known_by_ns','end_kind','duration_from_start_close_ns','excel_row','source_id']],on=['day','event_id'],how='left',suffixes=('','_event'),validate='many_to_one')
 assert x.end_known_by_ns.notna().all();assert (x.order_id==x.order_id_event).all()
 assert all(int(t)==int(s)+int(float(delay))*10**6 for t,s,delay in zip(x.decision_cutoff_ns,x.start_known_by_ns,x.delay_ms))
 assert all(int(t)<=int(c) for t,c in zip(x.last_action_known_by_ns,x.decision_cutoff_ns))
 for c in ['eligible','at_touch','fills_known','display_known','initial_display','delay_ms','initial_trade_lots','initial_trade_price_count','quote_age_ns']:x[c]=num(x,c)
 assert x.eligible.notna().all() and x.at_touch.notna().all()
 assert int(x.loc[x.delay_ms==0,'eligible'].sum())==len(e)
 assert all(bool(alive)==(int(end)>int(t)) for alive,end,t in zip(x.eligible,x.end_known_by_ns,x.decision_cutoff_ns))
 x['fill_seen']=np.where(x.fills_known>0,'known passive fill','no passive fill yet')
 x['display_vs_initial']=np.where(x.display_known>x.initial_display,'larger',np.where(x.display_known==x.initial_display,'same','smaller'))
 x['initial_display_band']=np.where(x.initial_display==1,'1 lot','>1 lot')
 for nextms in [25,100]:
  later=x[x.delay_ms==nextms][['day','event_id','eligible','at_touch']].rename(columns={'eligible':f'alive_{nextms}','at_touch':f'touch_{nextms}'})
  x=x.merge(later,on=['day','event_id'],validate='many_to_one')
 for now,later in [(5,25),(25,100)]:
  g=x[(x.delay_ms==now)&(x.eligible==1)].copy();g['next_alive']=g[f'alive_{later}'];g['next_touch']=g[f'alive_{later}']*g[f'touch_{later}']
  summarize(g,f'rest_survival_{now}_to_{later}',[[],['fill_seen'],['fill_seen','initial_display_band'],['fill_seen','side'],['display_vs_initial'],['fill_seen','at_touch']],['next_alive','next_touch'])
 x.to_csv(O/'resting_joined.csv',index=False);audit['resting_join_rows']=len(x);frames['resting']=x
 print('DISCOVERY resting',len(x),flush=True)

def origins():
 d=load(7)
 for c in ['age_ms','end_ms','prior_onsets_by_order']:d[c]=num(d,c)
 d['retreat']=(d.outcome=='RETREATED').astype(int);d['recover']=(d.outcome=='SIZE_RECOVERED_AT_SAME_PRICE').astype(int);d['improve']=(d.outcome=='IMPROVED').astype(int)
 d['repeated']=np.where(d.prior_onsets_by_order>0,'prior onset','first known onset')
 d['age_band']=pd.cut(d.age_ms,[-np.inf,1,5,25,100,1000,np.inf],labels=['<=1ms','1-5ms','5-25ms','25-100ms','100-1000ms','>1000ms']).astype(str)
 summarize(d,'one_lot_origins',[[],['origin'],['origin','repeated'],['origin','side'],['origin','age_band']],['retreat','recover','improve','end_ms'])
 first=d.sort_values(['day','onset_ns','onset_cursor']).drop_duplicates(['day','order_id'])
 summarize(first,'one_lot_first_observed_order',[[],['origin'],['origin','side']],['retreat','recover','improve','end_ms'])
 audit['one_lot_unique_day_order']=len(first);frames['origins']=d
 print('DISCOVERY origins',len(d),len(first),flush=True)

def controls_and_flow():
 d=load(6);pairs=d[d.source_table=='prebirth-matched-pairs.csv.gz'].copy();pairs['difference']=num(pairs,'difference')
 summarize(pairs,'prebirth_pairs',[['population','lead_s','feature']],['difference'])
 audit['prebirth_rows']=len(d);audit['prebirth_pair_feature_rows']=len(pairs)
 f=load(1).sort_values(['day','second']);f['second']=f.second.map(int)
 for c in ['native_buy','native_sell','native_roll_buy','native_roll_sell','native_ratio']:f[c]=num(f,c)
 previous=f.groupby('day').shift();consecutive=f.second-previous.second==1
 f['direction']=np.sign(f.native_ratio);f['delta_ratio']=f.native_ratio-previous.native_ratio;f['ratio_changed']=consecutive&(f.delta_ratio.abs()>1e-12)
 f['fresh_total']=f.native_buy+f.native_sell;f['expired_buy']=previous.native_roll_buy+f.native_buy-f.native_roll_buy;f['expired_sell']=previous.native_roll_sell+f.native_sell-f.native_roll_sell
 f['driver']=np.where(f.fresh_total==0,'expiry without classified arrivals',np.where((f.expired_buy+f.expired_sell)>1e-9,'mixed arrival and expiry','classified arrival without expiry'))
 f['flip']=consecutive&(f.native_ratio*previous.native_ratio<0)
 for h in [1,5,20]:
  future=f.groupby('day').shift(-h);valid=future.second-f.second==h
  f[f'same_sign_{h}s']=np.where(valid,(np.sign(future.native_ratio)==f.direction).astype(float),np.nan)
  f[f'defined_{h}s']=np.where(valid,(future.native_roll_buy+future.native_roll_sell>0).astype(float),np.nan)
 summarize(f[f.ratio_changed],'flow_ratio_change',[[],['driver']],['same_sign_1s','same_sign_5s','same_sign_20s','defined_5s','defined_20s'])
 summarize(f[f.flip],'flow_sign_flip',[[],['driver']],['same_sign_1s','same_sign_5s','same_sign_20s','defined_5s','defined_20s'])
 audit['flow_negative_inferred_expiry']=int((consecutive & ((f.expired_buy< -1e-9)|(f.expired_sell< -1e-9))).sum())
 print('DISCOVERY flow and controls',len(f),len(pairs),flush=True)

def main():
 receipt=json.loads((P/'FINAL_VERIFICATION.json').read_text())
 for key in ['main_workbook','flow_workbook']:
  r=receipt[key];assert hashlib.sha256((P/r['file']).read_bytes()).hexdigest()==r['sha256']
 recognition();family();resting();origins();controls_and_flow()
 pd.DataFrame(tables).to_csv(O/'all_conditional_results.csv',index=False)
 (O/'case_candidates.json').write_text(json.dumps(cases,indent=2))
 audit['group_target_results']=len(tables);audit['input_workbook_receipt']=receipt;audit['all_results_retained']=True
 (O/'analysis_audit.json').write_text(json.dumps(audit,indent=2))
 print('DISCOVERY COMPLETE',len(tables),'group-target results',flush=True)
if __name__=='__main__':main()
