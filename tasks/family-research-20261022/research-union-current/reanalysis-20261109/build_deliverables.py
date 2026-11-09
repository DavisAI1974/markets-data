import copy,json
from pathlib import Path
import numpy as np
import pandas as pd

P=Path(__file__).parent;R=P.parent
version='priority-paper-v1.3-reanalysis-20261109'
base={'id':'R1','paper_enabled':True,'engine':'flow_touch_confirmation','parameters':{'flow_windows_seconds':[5,60],'flow_source':'native','fresh_trade_required':True,'arm_edge':'false_to_true','require_direction_agreement':['flow5','flow60','touch_imbalance'],'confirm_bid_ticks':1,'confirm_ask_ticks':1,'confirmation_group':'strictly_later','confirmation_timeout_ms':5000,'invalidation_fields':['flow5','touch_imbalance'],'invalidation_ms':1000,'invalidation_min_groups':2}}
r2={'id':'R2','paper_enabled':True,'engine':'order_support_confirmation','parameters':{'seed_actions':['T','A'],'seed_same_group':True,'seed_same_order_id':True,'seed_same_side':True,'arm_action':'F','arm_fill_group':'strictly_after_seed','arm_requires_positive_residual':True,'arm_requires_at_touch':True,'confirm_requires_original_price':True,'confirm_requires_at_touch':False,'confirm_requires_positive_residual':True,'confirm_bid_ticks':1,'confirm_ask_ticks':1,'confirmation_group':'strictly_after_fill','confirmation_timeout_ms':5000,'require_direction_agreement':['resting_side','native_flow5','touch_imbalance'],'cancel_invalidates':True,'reprice_invalidates':True,'zero_residual_invalidates':True,'entries_per_order_per_session':1,'invalidation_fields':['native_flow5','touch_imbalance'],'invalidation_ms':1000,'invalidation_min_groups':2}}
strategies=[base,r2,
 {'id':'R3','paper_enabled':True,'engine':'quiet_touch','parameters':{'flow_source':'native','flow_window_seconds':5,'classified_quantity_equals':0,'direction':'touch_imbalance_sign','direction_nonzero':True,'arm_edge':'false_to_true','invalidation_fields':['touch_imbalance'],'invalidation_ms':1000,'invalidation_min_groups':2}},
 {'id':'R4','paper_enabled':True,'engine':'delayed_touch','parameters':{'anchor':'causal_recognition','direction_at_anchor':'touch_imbalance_sign','delay_ms':1000,'max_observation_lateness_ms':1000,'confirmation_mid_ticks':1,'direction_multiplier':1,'exit_after_anchor_ms':20000}},
 {'id':'R5','paper_enabled':True,'engine':'delayed_touch','parameters':{'anchor':'causal_recognition','direction_at_anchor':'touch_imbalance_sign','delay_ms':1000,'max_observation_lateness_ms':1000,'confirmation_mid_ticks':1,'direction_multiplier':-1,'exit_after_anchor_ms':20000}},
 {'id':'R6A','paper_enabled':True,'engine':'flow_cancel','parameters':{'flow_source':'native','window_seconds':5,'direction':'flow_sign','cancel_balance':'ask_cancel_lots_minus_bid_cancel_lots','required_relation':'aligned','arm_edge':'false_to_true','max_hold_seconds':20}},
 {'id':'R6B','paper_enabled':True,'engine':'flow_cancel','parameters':{'flow_source':'native','window_seconds':5,'direction':'flow_sign','cancel_balance':'ask_cancel_lots_minus_bid_cancel_lots','required_relation':'opposed','arm_edge':'false_to_true','max_hold_seconds':20}},
 {'id':'R7','paper_enabled':True,'engine':'frozen_linear_prediction','parameters':{'anchor':'causal_recognition','model_id':'M0','direction':'prediction_sign','minimum_absolute_prediction_ticks':0,'max_hold_seconds':20}},
 {'id':'R8','paper_enabled':True,'engine':'frozen_linear_prediction','parameters':{'anchor':'causal_recognition','model_id':'M1','direction':'prediction_sign','minimum_absolute_prediction_ticks':0,'max_hold_seconds':20}}]
expiry=copy.deepcopy(base);expiry['id']='R9';expiry['parameters']['fresh_trade_required']=False;expiry['parameters']['flow_change_driver']='expiry_only';expiry['parameters']['require_flow5_sign_flip']=True;strategies.append(expiry)
strategies.append({'id':'R10','paper_enabled':True,'engine':'one_lot_retreat','parameters':{'anchor':'standing_best_shrank_to_one_lot','origin':'size_cut','direction_by_resting_side':{'bid':-1,'ask':1},'entries_per_order_per_session':1,'max_hold_seconds':20}})

# Freeze coefficients from all available historical discovery rows for prospective comparison.
x=pd.read_csv(P/'reanalysis_rows.csv')
baseline=['prior_ticks20','range_ticks20','spread_ticks','touch_imb','touch_count_imb','log_touch_lots','log_touch_orders','early_buy','early_sell','late_buy','late_sell','fresh_buy5','fresh_sell5']
info=['ent_dipole','mi_flow','log_signed_C','imb_flow']
models={}
for name,cols in [('M0',baseline),('M1',baseline+info)]:
    train=x[x.future20.notna()];a=train[cols].to_numpy(float);y=train.future20.to_numpy(float);valid=np.isfinite(a)
    impute=np.divide(np.where(valid,a,0).sum(axis=0),valid.sum(axis=0),out=np.zeros(a.shape[1]),where=valid.sum(axis=0)>0)
    a=np.c_[np.where(valid,a,impute),~valid];mean=a.mean(axis=0);scale=a.std(axis=0);scale[scale==0]=1
    a=(a-mean)/scale;coef=np.linalg.solve(a.T@a+10*np.eye(a.shape[1]),a.T@(y-y.mean()))
    models[name]={'features':cols,'missing_indicators':'append_in_feature_order','imputation':impute.tolist(),'center':mean.tolist(),'scale':scale.tolist(),'coefficients':coef.tolist(),'intercept':float(y.mean()),'ridge_penalty':10}
config={'schema':'markets-paper-rules/1','version':version,'mode':'paper','execution_enabled':False,'instrument':{'exchange':'NYMEX','product':'NG','contract_month':'2026-12','symbol_hint':'NGZ6','broker_contract_id':None},
 'execution':{'adapter':None,'account_id':None,'ledger_mode':'independent_per_strategy','quantity':1,'order_type':'marketable_limit','time_in_force':'IOC','buy_limit':'current_ask','sell_limit':'current_bid','entry_fill_source':'adapter_execution_report','exit_fill_source':'adapter_execution_report','live_orders_enabled':False},
 'session':{'start_utc':None,'end_utc':None,'timezone':'America/New_York'},
 'data':{'clock_encoding':'integer_ns','complete_groups_required':True,'continuous_snapshot_replay_required':True,'admit_future_known_by':False,'native_aggressor_classification_required':True,'order_id_ledger_required':True,'flow_window_left_boundary':'exclusive','flow_window_right_boundary':'inclusive','warmup_seconds':60,'max_quote_age_ms':1000,'max_group_silence_ms':1000,'max_spread_ticks':2,'minimum_quote_lots':1},
 'risk':{'scope':'per_strategy','max_open_contracts':1,'max_entries_per_session':20,'stop_ticks':4,'session_loss_ticks':12,'max_hold_seconds':120,'cooldown_seconds':30,'entry_cutoff_before_session_end_seconds':120,'profit_target_ticks':None,'exit_unfilled_action':'retry_next_valid_group','data_failure_action':'cancel_entries_request_exit_pause','resume':'explicit_operator_after_snapshot_and_warmup'},
 'costs':{'tick_size':'0.001','tick_value_usd':10,'round_turn_fees_usd':None,'stress_entry_ticks':1,'stress_exit_ticks':1},'strategies':strategies,'models':models}
(P/'TRADE_RULES.json').write_text(json.dumps(config,indent=2,allow_nan=False)+'\n',encoding='utf-8',newline='\n')
assert all(s['paper_enabled'] for s in config['strategies'])
assert len({s['id'] for s in strategies})==len(strategies)
for model in models.values():assert len(model['coefficients'])==2*len(model['features'])==len(model['center'])==len(model['scale'])

findings=[
 ['D09','Flow definitions','Native/proxy buy and sell quantities match in 3,159/3,176 contexts. Nonzero 5s directions agree in 777/778.','Different source definitions; retain both. All native windows passed known-by checks.'],
 ['D10','Sparse information estimates','965/1,818 defined windows have activity in at most two bins. 631 have zero estimated MI and large logged C.','Large ratios can reflect a small denominator. Include the information paper variant and log sparsity.'],
 ['D11','Incremental prediction','Information features worsened 20s MAE on all 3 later-date tests, including separated subsets.','One fixed linear model; all dates already studied. Paper-test baseline and information variants.'],
 ['D12','Movement after confirmation','After 1-tick touch-direction confirmation at +1s, remaining 20s means: -0.449, +0.474, -0.033, -0.519 ticks.','Midpoint diagnostic, not fills. Paper-test immediate, delayed-follow and delayed-fade.'],
 ['D13','Book and flow disagreement','Cancellation-support agreement beats disagreement in flow-oriented 20s means on 3/4 dates; Oct17 reverses.','Native cancellations differ from aggregate size changes. Include both agreement and disagreement paper arms.'],
 ['PIN','Next analysis','Keep D01-D13, source/cell evidence, all adverse/flat/missing cases, and every paper strategy.','No session setup now. JSON contains rules/parameters only; no commentary or eligibility opinions.']]
hypotheses=[
 ['R1','Fresh native flow with touch','Original flow/price-confirmation rule','D03/D05; exact composite execution not tested','Included'],
 ['R2','Surviving order support','At touch on arm; original order may remain behind improved best at confirmation','D01 plus geometric correction; log size/replenishment strata','Included'],
 ['R3','Quiet-flow touch','Trade nonzero touch direction when native 5s classified volume is zero','D04/D09; distinguish known-empty from feed missing','Included'],
 ['R4','Delayed follow','Follow touch direction after one-tick midpoint confirmation at +1s','D12; only post-confirmation fills/outcomes count','Included'],
 ['R5','Delayed fade','Opposite direction to R4 after the same confirmation','D12; comparative hypothesis, no net profit established','Included'],
 ['R6A','Flow with cancellation support','5s native flow direction when cancellation support agrees','D13; source-defined native cancel events','Included'],
 ['R6B','Flow against cancellation support','5s native flow direction when cancellation support opposes','D13; preserves adverse and contradictory regime','Included'],
 ['R7','Baseline model','Frozen count/price/book prediction sign; 20s maximum hold','D11; trained on all four historical discovery dates','Included'],
 ['R8','Information model','Same model plus information features; same hold','D10/D11; keep zero-MI and sparse cases tagged','Included'],
 ['R9','Expiry-driven flow','R1 comparison triggered by expiry-only native 5s sign flip','D03; fresh-arrival requirement removed only for this variant','Included'],
 ['R10','One-lot retreat','Standing best shrinks to one through size-cut; trade away from that resting side','D06; source-defined onset, never future fate','Included']]
pd.DataFrame(hypotheses,columns=['ID','Hypothesis','Operational distinction','Evidence and limits','Paper inclusion']).to_csv(P/'PAPER_HYPOTHESES.csv',index=False)
comparison=[]
for filename in ['classification_comparison.csv','entropy_sparsity.csv','incremental_models.csv','confirmation_remaining.csv','family_book_activity.csv']:
    d=pd.read_csv(P/filename)
    for index,rec in d.iterrows():
        if filename=='entropy_sparsity.csv':
            for metric in d.columns[1:]:comparison.append([filename,index+2,str(int(rec.day)),metric,'all','',int(rec.rows),int(rec[metric]),'','','','','','',''])
            continue
        condition={k:rec[k] for k in ['availability','native_sign','proxy_sign','model','direction','delay','state','driver','comparison'] if k in rec}
        def val(key,default=''):
            v=rec.get(key,default)
            return '' if pd.isna(v) else v.item() if isinstance(v,np.generic) else v
        comparison.append([filename,index+2,str(int(rec.day)),json.dumps(condition,default=str,sort_keys=True),val('subset','all'),val('horizon',val('window')),
            val('population',val('test_rows',val('rows'))),val('n',val('test_rows',val('rows'))),val('mean'),val('from_recognition_mean'),val('mae'),val('mse'),val('positive'),val('negative'),val('flat')])
cases=pd.read_csv(P/'CASES.csv',dtype=str).fillna('')
case_rows=[[v.finding,v.day,v.candidate_id,v.decision_ns,f'P09 row {v.p09_excel_row}; P10 row {v.p10_excel_row}; P01 rows {v.p01_first_row}-{v.p01_last_row}',
            f'touch={v.touch}; proxy5={v.proxy5}; native5={v.native5}; MI={v.mi_level}; logC={v.log_C}; move1={v.move1}; move20={v.move20}; remaining20={v.remaining_touch20}',v.flow_source_url] for _,v in cases.iterrows()]
specs=[{'name':'Reanalysis findings','headers':['Finding','Question','Measured result','Interpretation and next test'],'widths':[12,30,75,75],'rows':findings},
       {'name':'Paper hypotheses','headers':['ID','Hypothesis','Operational distinction','Evidence and limits','Paper inclusion'],'widths':[12,32,72,70,18],'rows':hypotheses},
       {'name':'Reanalysis comparisons','headers':['Source table','CSV row','Date','Condition or metric','Subset','Horizon or window s','Population','Defined n or count','Mean ticks','From recognition mean ticks','MAE ticks','MSE ticks squared','Positive','Negative','Flat'],'widths':[38,12,15,85,18,18,14,18,17,22,17,20,14,14,14],'rows':comparison},
       {'name':'Reanalysis cases','headers':['Case type','Date','Candidate','Decision ns','Source cells','Observed values','Immutable flow source'],'widths':[30,14,36,28,65,100,85],'rows':case_rows}]
(P/'summary_sheets.json').write_text(json.dumps(specs,indent=2,allow_nan=False),encoding='utf-8',newline='\n')
(P/'MODEL_FREEZE.json').write_text(json.dumps({'version':version,'training_dates':sorted(x.day.unique().astype(str).tolist()),'training_rows':int(x.future20.notna().sum()),'target':'midpoint change from recognition to +20s, ticks','features_source':'P10; original midpoint-classified flow','prospective_validation':False},indent=2),encoding='utf-8',newline='\n')
print('Created JSON spec;',len(strategies),'paper arms;',len(comparison),'comparison rows;',len(case_rows),'cases')
