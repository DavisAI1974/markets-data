import json
import numpy as np
import pandas as pd
import discovery_depth as D
x=D.load(3)
for c in ['flow60','book','pressure','moves.60','moves.300','moves.600']:x[c]=D.num(x,c)
x['relation']=[D.rel(D.sgn(a),D.sgn(b)) for a,b in zip(x.flow60,x.book)]
for h in [60,300,600]:
 x[f'flow_oriented_{h}']=x.flow60.replace(0,np.nan)*x[f'moves.{h}']
 x[f'book_oriented_{h}']=x.book.replace(0,np.nan)*x[f'moves.{h}']
 x[f'pressure_oriented_{h}']=x[f'moves.{h}']
D.summarize(x,'candidate_pressure_context',[[],['relation'],['relation','side'],['relation','tercile']],[f'{direction}_oriented_{h}' for direction in ['flow','book','pressure'] for h in [60,300,600]])
last={};keep=[]
for i,r in x.sort_values(['day','known_by_ns']).iterrows():
 t=int(r.known_by_ns)
 if t-last.get(r.day,-10**30)>=60*10**9:keep.append(i);last[r.day]=t
separated=x.loc[keep]
D.summarize(separated,'candidate_pressure_separated60',[[],['relation'],['relation','side']],[f'{direction}_oriented_60' for direction in ['flow','book','pressure']])
pd.DataFrame(D.tables).to_csv(D.O/'candidate_control_results.csv',index=False)
(D.O/'candidate_control_audit.json').write_text(json.dumps({'rows':len(x),'separated60_rows':len(separated),'clock':'Exact known_by_ns; first candidate then >=60seconds from last retained candidate within day, outcome-independent selection','orientation':'flow60/book and moves are all pressure-relative; multiplying them cancels pressure twice. Zero direction is unavailable, not a flat outcome.','tercile_limit':'Original within-session volume terciles use complete-session thresholds; retrospective context only, not an online regime classifier.'},indent=2))
print('CANDIDATE CONTEXT COMPLETE',len(x),len(separated))
