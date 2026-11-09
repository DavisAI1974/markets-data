"""Read the saved Excel cells, then compute reproducible descriptive findings."""
import collections, csv, hashlib, json, math, statistics, zipfile
from pathlib import Path
from lxml import etree as ET

R=Path(__file__).parent; P=R/'priority-now'
NS='{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
RN='{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'

def number(value):
 try:
  result=float(value)
  return result if math.isfinite(result) else None
 except (TypeError,ValueError):return None

def sign(value):
 if value in ('+','-'):return 1 if value=='+' else -1
 v=number(value)
 return None if v is None else (v>0)-(v<0)

def truth(v):return str(v).lower() in ('true','1')

def sheets(z):
 rel={e.get('Id'):e.get('Target') for e in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
 result={}
 for sh in ET.fromstring(z.read('xl/workbook.xml')).find(NS+'sheets'):
  target=rel[sh.get(RN+'id')]
  result[sh.get('name')]=target.lstrip('/') if target.startswith('/') else 'xl/'+target
 return result

def rows(z,part,shared=None):
 headers=None
 with z.open(part) as f:
  for _,el in ET.iterparse(f,events=('end',),tag=NS+'row'):
   cells={}
   for c in el:
    if c.tag!=NS+'c':continue
    v=c.find(NS+'v');t=c.get('t')
    value=''.join(c.find(NS+'is').itertext()) if t=='inlineStr' else shared[int(v.text)] if t=='s' else v.text if v is not None else None
    cells[''.join(x for x in c.get('r') if x.isalpha())]=value
   rowno=int(el.get('r'))
   if headers is None:headers=cells
   else:yield rowno,{name:cells.get(col) for col,name in headers.items()}
   el.clear()
   while el.getprevious() is not None:del el.getparent()[0]

def main():
 file=P/'Frankie_four_day_priority_ten.xlsx'
 selection=json.loads((P/'priority_selection.json').read_text())
 counts=collections.defaultdict(collections.Counter)
 values=collections.defaultdict(list)
 examples=[];seen_examples=set();previous={};source_counts=collections.Counter();coverage=[]
 def add(day,metric,n=1):counts[day][metric]+=n
 def val(day,metric,v):
  n=number(v)
  if n is not None:values[(day,metric)].append(n)
 def example(item,rowno,r,label):
  key=(item['rank'],r['Trading date'],label)
  if key not in seen_examples:
   seen_examples.add(key);examples.append({'sheet':item['sheet'],'excel_row':rowno,'day':r['Trading date'],'source_id':r['Source ID'],'source_row':r['Source row zero based'],'case_type':label,'cells':r})
 with zipfile.ZipFile(file) as z, zipfile.ZipFile(P/'Priority_native_flow.xlsx') as flow_zip:
  mapping=sheets(z);flow_mapping=sheets(flow_zip)
  for item in selection['families']:
   n=0
   archive=flow_zip if item['rank']==1 else z
   part=flow_mapping[item['sheet']] if item['rank']==1 else mapping[item['sheet']]
   for rowno,r in rows(archive,part):
    n+=1;day=r['Trading date'];rank=item['rank'];source_counts[r['Source ID']]+=1
    add(day,f'P{rank:02}_rows')
    if rank==1:
     b,s,rb,rs=map(number,[r['native_buy'],r['native_sell'],r['native_roll_buy'],r['native_roll_sell']])
     ratio=number(r['native_ratio']);t=int(r['second']);known=number(r['completed_second_known_by_ns'])
     if known is None:add(day,'flow_completion_clock_missing')
     else:
      # Convert the exact text directly to int; float is used only to test missingness.
      lag=int(r['completed_second_known_by_ns'])-(t+1)*10**9
      add(day,'flow_completion_before_second_end',int(lag<0));val(day,'flow_completion_delay_ms',lag/1e6)
     add(day,'flow_empty_seconds',int((rb or 0)+(rs or 0)==0))
     prev=previous.get(day)
     if prev and t==prev[0]+1 and ratio is not None and prev[1] is not None:
      changed=abs(ratio-prev[1])>1e-12
      age_only=changed and b==0 and s==0
      flip=ratio*prev[1]<0
      add(day,'flow_ratio_changes',int(changed));add(day,'flow_age_only_changes',int(age_only))
      add(day,'flow_direction_flips',int(flip));add(day,'flow_age_only_flips',int(age_only and flip))
      if age_only:example(item,rowno,r,'expiry_only_change')
     previous[day]=(t,ratio)
    elif rank==2:
     f=sign(r.get('f5'));d=sign(r.get('dsg'));relation='missing' if f is None or d is None else 'neutral' if f==0 or d==0 else 'aligned' if f==d else 'opposed'
     add(day,'family_flow_depth_'+relation)
     for h in [5,20,60]:
      v=number(r.get(f'tk_{h}s'))
      if v is not None and f not in (None,0):val(day,f'family_{relation}_flow_oriented_{h}s_ticks',f*v)
     if r.get('cutoff_ns') and r.get('start_recv_ns'):add(day,'family_cutoff_not_before_start',int(int(r['cutoff_ns'])>=int(r['start_recv_ns'])))
     example(item,rowno,r,relation)
    elif rank==3:
     f,d=sign(r.get('flow60')),sign(r.get('book'));relation='missing' if f is None or d is None else 'neutral' if f==0 or d==0 else 'aligned' if f==d else 'opposed'
     add(day,'candidate_flow_book_'+relation)
     for h in [60,300,600]:
      v=number(r.get('moves.'+str(h)))
      if v is not None and f not in (None,0):val(day,f'candidate_{relation}_flow_oriented_{h}s_ticks',f*v)
     example(item,rowno,r,relation)
    elif rank==4:
     if r['Source table']=='aggression-to-rest-events.csv':
      add(day,'rest_events');add(day,'rest_visible_at_close',int(truth(r['visible_at_start_close'])))
      add(day,'rest_end_'+str(r['end_kind']))
      duration=number(r['duration_from_start_close_ns'])
      if duration is not None:
       val(day,'rest_duration_ms',duration/1e6)
       for ms in [1,5,25,100]:add(day,f'rest_duration_le_{ms}ms',int(duration<=ms*1e6))
      example(item,rowno,r,'end_'+str(r['end_kind']))
     else:add(day,'rest_action_'+str(r.get('action')))
    elif rank==5:
     delay=str(r['delay_ms']);add(day,'rest_scheduled_'+delay+'ms')
     add(day,'rest_eligible_'+delay+'ms',int(truth(r['eligible'])))
     add(day,'rest_touch_'+delay+'ms',int(truth(r['eligible']) and truth(r['at_touch'])))
     if r.get('last_action_known_by_ns') and r.get('decision_cutoff_ns'):
      add(day,'rest_future_action_at_decision',int(int(r['last_action_known_by_ns'])>int(r['decision_cutoff_ns'])))
     example(item,rowno,r,'eligible_'+str(r['eligible'])+'_delay_'+delay)
    elif rank==6:
     if r['Source table']=='prebirth-matched-pairs.csv.gz':
      metric='prebirth_'+str(r.get('population'))+'_lead'+str(r.get('lead_s'))+'_'+str(r.get('feature'))
      val(day,metric,r.get('difference'))
      example(item,rowno,r,'matched_'+str(r.get('population')))
     else:
      for k in ['matched','available','input_disposition','control_status','status']:
       if r.get(k) is not None:add(day,'prebirth_case_'+k+'_'+str(r[k]))
    elif rank==7:
     add(day,'one_lot_origin_'+str(r['origin']));add(day,'one_lot_outcome_'+str(r['outcome']))
     add(day,'one_lot_fate_'+str(r['fate']));val(day,'one_lot_duration_ms',r['end_ms']);val(day,'one_lot_age_ms',r['age_ms'])
     ms=number(r['end_ms'])
     for limit in [1,5,25,100]:add(day,f'one_lot_duration_le_{limit}ms',int(ms is not None and ms<=limit))
     example(item,rowno,r,str(r['outcome'])+'_'+str(r['origin']))
    elif rank==8:
     if r['Source table']=='x07_first_events.csv':
      add(day,'first_event_candidates');val(day,'recognition_delay_seconds',r['delay_s'])
      a,q=number(r['k_aggressor_start']),number(r['k_quote_relocation'])
      if a is not None and q is not None and a>=0 and q>=0:
       label='aggression_first' if a<q else 'price_first' if q<a else 'same_bin'
       add(day,'first_event_'+label);example(item,rowno,r,label)
      else:add(day,'first_event_missing_or_censored')
     else:add(day,'lean_curve_rows_'+r['Source table'])
    elif rank==9:
     add(day,'recognition_flow_'+str(r['flow_state']))
     val(day,'recognition_elapsed_s',(int(r['recognition_receive_ns'])-int(r['birth_second'])*10**9)/1e9)
     for h in [1,5,20,60,300]:
      v=number(r.get('move_ticks_after_recognition.'+str(h)));direction=number(r['polarity'])
      if v is not None and direction is not None:val(day,f'after_recognition_oriented_{h}s_ticks',v*direction)
     example(item,rowno,r,'flow_'+str(r['flow_state']))
    elif rank==10:
     for key in ['input_disposition','dipole_state','book_vs_flow','price_vs_flow']:add(day,'context_'+key+'_'+str(r[key]))
     decision=int(r['decision_ns'])
     for key in ['quote_known_by_ns','flow_closed_by_ns']:
      if r.get(key):add(day,'context_future_'+key,int(int(r[key])>decision))
     example(item,rowno,r,'book_'+str(r['book_vs_flow']))
   assert n==item['rows'],(item['sheet'],n,item['rows'])
   coverage.append({'sheet':item['sheet'],'rows_read':n,'fields':len(item['fields']),'analysis':'All rows read from saved Excel cells; descriptive metrics and sequence/availability checks'})
   print('ANALYZED',item['sheet'],n,flush=True)
 for item in selection['families']:
  for src in item['sources']:assert source_counts[src['id']]==src['rows'],src
 distributions=[]
 for (day,metric),vs in sorted(values.items()):
  distributions.append({'day':day,'metric':metric,'n':len(vs),'mean':statistics.mean(vs),'median':statistics.median(vs),'minimum':min(vs),'maximum':max(vs),'positive':sum(v>0 for v in vs),'negative':sum(v<0 for v in vs),'flat':sum(v==0 for v in vs)})
 result={'input_file':file.name,'input_sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'counts':dict(counts),'distributions':distributions,'coverage':coverage,'rows_analyzed':sum(x['rows_read'] for x in coverage),'limits':['Descriptive retrospective discovery, not a strategy backtest or unseen validation.','Fixed-horizon original responses are separate diagnostics, never warning lead or prescribed exit time.','Retrospective cohort selection and future labels are excluded from online rule inputs.']}
 (P/'cell_analysis.json').write_text(json.dumps(result,indent=2))
 (P/'analysis_cases.json').write_text(json.dumps(examples,indent=2))
 with (P/'cell_metrics.csv').open('w',newline='',encoding='utf8') as f:
  w=csv.DictWriter(f,fieldnames=list(distributions[0]));w.writeheader();w.writerows(distributions)
 print('CELL ANALYSIS COMPLETE',result['rows_analyzed'],flush=True)

if __name__=='__main__':main()
