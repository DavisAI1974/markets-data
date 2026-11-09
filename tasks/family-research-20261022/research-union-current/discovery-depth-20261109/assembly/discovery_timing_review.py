"""Respect interval versus boundary definitions in the saved event-order studies."""
import json,pandas as pd,numpy as np
import discovery_depth as D
def order_class(a,q):
 if not np.isfinite(a) or not np.isfinite(q) or a<0 or q<1:return 'missing_or_censored'
 # Aggression falls in (a,a+1]; first sampled quote change falls in (q-1,q].
 if a+1<=q-1:return 'aggression_interval_before_quote_interval'
 if q<=a:return 'quote_interval_before_aggression_interval'
 return 'overlapping_intervals_order_unresolved'
def main():
 p=D.load(8);e=p[p.source_table=='x07_first_events.csv'].copy()
 for c in ['k_aggressor_start','k_quote_relocation','delay_s']:e[c]=D.num(e,c)
 e['interval_order']=[order_class(a,q) for a,q in zip(e.k_aggressor_start,e.k_quote_relocation)]
 e.groupby(['day','interval_order']).size().reset_index(name='n').to_csv(D.O/'event_interval_order_counts.csv',index=False)
 e.to_csv(D.O/'event_interval_order_cases.csv',index=False)
 t=D.num(e,'k_touch_size_change');q=e.k_quote_relocation
 e['touch_quote_order']=['missing/censored' if not np.isfinite(a) or not np.isfinite(b) or a<1 or b<1 else 'same sampled interval' if a==b else 'touch-size sampled interval first' if a<b else 'quote sampled interval first' for a,b in zip(t,q)]
 e.groupby(['day','touch_quote_order']).size().reset_index(name='n').to_csv(D.O/'touch_quote_interval_counts.csv',index=False)
 co=p[p.source_table=='x09_lean_cohort.csv'].copy();ct=p[p.source_table=='x09_lean_control.csv'].copy()
 x=co.merge(ct,on=['day','k'],suffixes=('_cohort','_control'),validate='one_to_one');assert len(x)==404
 result=[]
 for metric in ['p25','p50','p75','share_defined','share_lean_plus1','share_lean_minus1']:
  for r in x.to_dict('records'):
   value=float(r[metric+'_cohort']);lo=float(r['ctl_'+metric+'_lo_control']);med=float(r['ctl_'+metric+'_med_control']);hi=float(r['ctl_'+metric+'_hi_control']);k=int(r['k'])
   result.append({'day':r['day'],'seconds_from_birth':k,'phase':'prebirth' if k<0 else 'birth' if k==0 else 'postbirth','metric':metric,'cohort':value,'control_median':med,'difference':value-med,'control_draw_lo':lo,'control_draw_hi':hi,'relative_to_control_draw_band':'below' if value<lo else 'above' if value>hi else 'within','source_id_cohort':r['source_id_cohort'],'source_row_cohort':r['source_row_cohort'],'excel_row_cohort':r['excel_row_cohort'],'source_id_control':r['source_id_control'],'source_row_control':r['source_row_control'],'excel_row_control':r['excel_row_control']})
 pd.DataFrame(result).to_csv(D.O/'lean_control_comparisons.csv',index=False)
 method={'source_definition':'aggressor k is interval (birth+k,birth+k+1]; quote q is first sampled boundary with changed best quote, so its observed transition lies in (birth+q-1,birth+q]. Transient earlier quote changes may be missed. These are not native event clocks.', 'correction':'The prior smaller-k comparison overstated distinct-bin ordering; replacement counts use non-overlapping intervals and explicitly unresolved overlap. No raw cell values change.','producer_git_blob':'98287f18f68139baedb6e063fce088379477d6bc','lean_producer_git_blob':'f0f8fb57d32bf99b55fe520a11ec082800511453','lean_band_meaning':'2.5/50/97.5 percentiles across 200 matched-control draws, not uncertainty over independent trading days and not multiple-testing-adjusted significance.'}
 (D.O/'timing_definition_correction.json').write_text(json.dumps(method,indent=2))
 print('TIMING/CONTROL REVIEW COMPLETE',len(e),len(result))
if __name__=='__main__':main()
