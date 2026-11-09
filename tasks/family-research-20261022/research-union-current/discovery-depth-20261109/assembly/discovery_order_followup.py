"""Narrow follow-up: distinguish observed replenishment accounting from fill-only labels."""
import csv,gzip,hashlib,json
import pandas as pd
import discovery_depth as D
O=D.O
def main():
 e=D.load(4);ev=e[e.source_table=='aggression-to-rest-events.csv'].copy();ac=e[e.source_table=='aggression-to-rest-actions.csv.gz'].copy()
 ob=D.load(5);events={(r.day,r.event_id):r for r in ev.itertuples()};actions={k:g.sort_values('cursor',key=lambda s:s.map(int)).to_dict('records') for k,g in ac.groupby(['day','event_id'])}
 records=[]
 for r in ob.to_dict('records'):
  init=events[(r['day'],r['event_id'])];display=int(init.initial_display);fills=pending=added=unmatched=0;group=None;modifications=0
  for act in actions.get((r['day'],r['event_id']),[]):
   if int(act['group_known_by_ns'])>int(r['decision_cutoff_ns']):continue
   if group is not None and act['group']!=group:unmatched+=pending;pending=0
   group=act['group'];action=act['action'];size=int(act['size'])
   if action=='F':
    if act['side']==init.side and act['price_raw']==init.resting_price_raw:fills+=size;pending+=size
   elif action=='M' and (act['side']!=init.side or act['price_raw']!=init.resting_price_raw):pass
   elif action in ('M','C'):
    after=max(0,display-size) if action=='C' else size;matched=min(pending,max(0,display-after))
    if action=='M':added+=max(0,after-display+pending);pending=0;modifications+=1
    else:pending-=matched
    display=after
  unmatched+=pending
  assert display==int(r['display_known']),(r['day'],r['event_id'],'display')
  assert fills==int(r['fills_known']),(r['day'],r['event_id'],'fills')
  records.append(dict(r,prefix_implied_added_display=added,prefix_unmatched_fills=unmatched,prefix_modifications=modifications))
 x=pd.DataFrame(records)
 for c in ['eligible','at_touch','delay_ms','initial_display','fills_known','prefix_implied_added_display','prefix_unmatched_fills']:x[c]=D.num(x,c)
 x['replenishment_known']=x.prefix_implied_added_display.map(lambda v:'implied added display' if v>0 else 'no implied added display')
 x['fill_seen']=x.fills_known.map(lambda v:'known passive fill' if v>0 else 'no passive fill yet');x['initial_display_band']=x.initial_display.map(lambda v:'1 lot' if v==1 else '>1 lot')
 x.to_csv(O/'resting_prefix_accounting.csv',index=False)
 sources=[];out=[]
 for s in json.loads((D.R/'active_sources.json').read_text()):
  if not s['path'].endswith('/resting-observation-outcomes.csv.gz'):continue
  if '/research-atlas-v2/' not in s['path']:continue
  if '/replay-comparison/20231018/' in s['path']:continue # identical alias of the active Oct18 base table
  raw=(D.R/'objects'/s['sha']).read_bytes();assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==s['sha']
  day=next((d for d in ['20231002','20231003','20231017'] if '/'+d+'/' in s['path']),'20231018');n=0
  with gzip.open(D.R/'objects'/s['sha'],'rt',encoding='utf8') as f:
   for i,r in enumerate(csv.DictReader(f)):
    out.append(dict(r,day=day,outcome_source_id=s['id'],outcome_source_row=i,outcome_source_url=s['url']));n+=1
  sources.append(dict(s,rows=n,role='existing original outcome table; narrow follow-up to frozen P04/P05 observations'))
 y=pd.DataFrame(out)
 for c in ['delay_ms','horizon_s','direction_oriented_change']:y[c]=D.num(y,c)
 key=['day','event_id','delay_ms'];assert not x.duplicated(key).any();assert not y.duplicated(key+['horizon_s']).any()
 joined=y.merge(x[key+['decision_cutoff_ns','replenishment_known','prefix_implied_added_display','prefix_unmatched_fills','fill_seen','initial_display_band','excel_row']],on=key,suffixes=('','_prefix'),validate='many_to_one')
 assert len(joined)==len(y) and joined.excel_row.notna().all()
 assert (joined.decision_cutoff_ns==joined.decision_cutoff_ns_prefix).all()
 joined['future_ticks']=joined.direction_oriented_change/0.001
 for now in [5,25]:
  g=joined[joined.delay_ms==now].copy()
  D.summarize(g,f'rest_price_from_{now}ms',[['horizon_s','fill_seen','initial_display_band'],['horizon_s','replenishment_known'],['horizon_s','fill_seen','initial_display_band','at_touch']],['future_ticks'])
 joined.to_csv(O/'resting_outcomes_joined.csv',index=False)
 (O/'supplementary_source_manifest.json').write_text(json.dumps(sources,indent=2))
 pd.DataFrame(D.tables).to_csv(O/'resting_price_results.csv',index=False)
 (O/'resting_prefix_audit.json').write_text(json.dumps({'prefix_rows_verified_against_P05':len(x),'outcome_rows_exact_joined':len(joined),'source_files':len(sources),'future_labels_used_as_prefix_inputs':False},indent=2))
 print('ORDER FOLLOWUP COMPLETE',len(x),len(joined),flush=True)
if __name__=='__main__':main()
