import collections,gzip,json,zipfile
import pandas as pd
import numpy as np
import discovery_depth as D
from priority_cell_analysis import rows,sheets
O=D.O

# Origin is entangled with the mechanism that made the touch one lot.
x=D.load(7);x['retreat']=(x.outcome=='RETREATED').astype(int)
D.summarize(x,'one_lot_onset_conditioned',[['onset','origin'],['onset','origin','side']],['retreat'])
first=x.sort_values(['day','onset_ns','onset_cursor']).drop_duplicates(['day','order_id'])
D.summarize(first,'one_lot_first_onset_conditioned',[['onset','origin']],['retreat'])
pd.DataFrame(D.tables).to_csv(O/'origin_onset_results.csv',index=False)

# Check redundancy rather than interpreting mechanical co-measurements as independent confirmation.
f=pd.read_csv(O/'family_derived.csv',dtype={'day':str})
red=[]
for day,g in f.groupby('day'):
 for other in ['ob_rm_fill_b_5s','ob_trade_sellagg_5s','root.activity.5.trade_sell_aggressor_qty']:
  pair=g[['ob_fill_b_5s',other]].dropna();red.append({'day':day,'field_1':'ob_fill_b_5s','field_2':other,'n':len(pair),'spearman':pair.corr(method='spearman').iloc[0,1]})
pd.DataFrame(red).to_csv(O/'field_redundancy.csv',index=False)

# Same-population comparisons prevent availability differences from masquerading as predictive superiority.
r=pd.read_csv(O/'recognition_joined.csv',dtype={'day':str})
paired=[]
for day,g in r.groupby('day'):
 for horizon in [20,60]:
  v=g[[f'touch_oriented_{horizon}',f'flow_oriented_{horizon}']].dropna()
  paired.append({'day':day,'horizon_seconds':horizon,'n_joint_defined':len(v),'touch_mean':v.iloc[:,0].mean(),'flow_mean':v.iloc[:,1].mean(),'paired_difference':(v.iloc[:,0]-v.iloc[:,1]).mean()})
pd.DataFrame(paired).to_csv(O/'recognition_paired_comparison.csv',index=False)

# Independently reconstruct the critical survival table from actual Excel cells, not the analysis dataframe.
obs={};verified=collections.Counter()
with zipfile.ZipFile(D.P/'Frankie_four_day_priority_ten.xlsx') as z:
 m=sheets(z)
 for no,row in rows(z,m['P05 Observable resting state']):
  key=(row['Trading date'],row['event_id'],int(row['delay_ms']));assert key not in obs
  obs[key]=dict(row,excel_row=no)
 for (day,event,delay),row in obs.items():
  if delay!=5 or row['eligible']!='1':continue
  size='1 lot' if int(row['initial_display'])==1 else '>1 lot';fill='known passive fill' if int(row['fills_known'])>0 else 'no passive fill yet'
  verified[(day,size,fill,'n')]+=1;verified[(day,size,fill,'alive25')]+=int(obs[(day,event,25)]['eligible'])
a=pd.read_csv(O/'all_conditional_results.csv',dtype={'day':str})
t=a[(a.study=='rest_survival_5_to_25')&(a.grouping=='fill_seen + initial_display_band')&(a.target=='next_alive')]
for row in t.itertuples():
 c=json.loads(row.condition);base=(row.day,c['initial_display_band'],c['fill_seen'])
 assert row.n==verified[base+('n',)] and row.positive==verified[base+('alive25',)]

# Choose first observed adverse and surviving cases per date and source-defined size/fill state.
case=[]
prefix=pd.read_csv(O/'resting_prefix_accounting.csv',dtype={'day':str,'event_id':str,'order_id':str,'decision_cutoff_ns':str})
outcome=pd.read_csv(O/'resting_outcomes_joined.csv',dtype={'day':str,'event_id':str,'decision_cutoff_ns':str})
outcome=outcome[(outcome.delay_ms==5)&(outcome.horizon_s==20)].set_index(['day','event_id'])
for key,group in prefix[(prefix.delay_ms==5)&(prefix.eligible==1)].groupby(['day','initial_display_band','fill_seen']):
 day,size,fill=key
 for survival in [0,1]:
  choices=[rr for rr in group.sort_values('excel_row').to_dict('records') if int(obs[(day,rr['event_id'],25)]['eligible'])==survival]
  if not choices:continue
  rr=choices[0];yy=outcome.loc[(day,rr['event_id'])];source=next(s for s in D.S[4]['sources'] if s['id']==rr['source_id'])
  case.append({'claim_id':'D01','day':day,'event_id':rr['event_id'],'order_id':rr['order_id'],'state':size+'; '+fill,'decision_ns':rr['decision_cutoff_ns'],'observation_excel_sheet':'P05 Observable resting state','observation_excel_row':rr['excel_row'],'source_id':rr['source_id'],'source_row':rr['source_row'],'source_url':source['url'],'survived25':survival,'prefix_implied_added_display':rr['prefix_implied_added_display'],'prefix_unmatched_fills':rr['prefix_unmatched_fills'],'future20_ticks':yy.future_ticks,'outcome_source_id':yy.outcome_source_id,'outcome_source_row':yy.outcome_source_row,'outcome_source_url':yy.outcome_source_url,'outcome_target_ns':str(yy.target_ns),'limit':'Outcome is a later directional midpoint change, not our executed return.'})
pd.DataFrame(case).to_csv(O/'CASES.csv',index=False)

# Independent loop calculation for the key native flow persistence contrast.
flow=[]
with gzip.open(D.P/'P01.jsonl.gz','rt',encoding='utf8') as fh:
 for line in fh:
  rr=json.loads(line);v=rr['values'];flow.append((rr['day'],int(v['second']),*[float(v[k]) if v[k] not in (None,'') else float('nan') for k in ['native_ratio','native_buy','native_sell','native_roll_buy','native_roll_sell']]))
flow_lookup={(r[0],r[1]):r for r in flow};loop=collections.Counter()
for rr in flow:
 day,sec,ratio,b,s,rb,rs=rr;prev=flow_lookup.get((day,sec-1));future=flow_lookup.get((day,sec+5))
 if not prev or not future or not ratio*prev[2]<0:continue
 expiry=prev[5]+prev[6]+b+s-rb-rs;driver='expiry without classified arrivals' if b+s==0 else 'mixed arrival and expiry' if expiry>1e-9 else 'classified arrival without expiry'
 loop[(day,driver,'n')]+=1;loop[(day,driver,'same')]+=int(np.sign(ratio)==np.sign(future[2]))
ff=a[(a.study=='flow_sign_flip')&(a.grouping=='driver')&(a.target=='same_sign_5s')]
for row in ff.itertuples():
 driver=json.loads(row.condition)['driver'];assert row.n==loop[(row.day,driver,'n')] and row.positive==loop[(row.day,driver,'same')]

receipt={'actual_excel_rest_observations_read':len(obs),'survival_group_counts_independently_verified':len(t),'flow_five_second_group_counts_independently_verified':len(ff),'source_rows_used_in_flow_check':len(flow),'case_selection':'First Excel row per day, initial display band, observed-fill state and survive/not-survive outcome. Full populations, not selected cases, determine findings.','rules_v1_modified':False}
(O/'INDEPENDENT_CHECKS.json').write_text(json.dumps(receipt,indent=2))
print('INDEPENDENT CHECKS COMPLETE',receipt)
