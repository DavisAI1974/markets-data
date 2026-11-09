"""Extend the existing Artifact Tool template with the ten complete populations."""
import gzip, json, re, shutil, hashlib
from pathlib import Path
from xlsx_stream import build
R=Path(__file__).parent;O=R/'current';P=R/'priority-now'

def typed(key,value):
 if value is None:return None
 if any(t in key.lower() for t in ('_ns','_id','cursor','ordinal','epoch','second','raw_record')):
  return str(value)
 if isinstance(value,str):
  if value in ('True','False'):return value=='True'
  if re.fullmatch(r'-?\d{1,14}',value):return int(value)
  if re.fullmatch(r'-?\d+\.\d+',value) and len(value.replace('-','').replace('.',''))<=15:return float(value)
 return value

def data_rows(item):
 sources={s['id']:s for s in item['sources']}
 with gzip.open(P/item['data_file'],'rt',encoding='utf8') as f:
  for line in f:
   r=json.loads(line)
   yield [r['source_id'],r['source_row'],r['day'],r['source_type'],sources[r['source_id']]['url']]+[typed(k,r['values'].get(k)) for k in item['fields']]

def main():
 selected=json.loads((P/'priority_selection.json').read_text())
 baseline=P/'before-priority.xlsx'
 if not baseline.exists():shutil.copyfile(O/'Frankie_four_day_research_current.xlsx',baseline)
 styles=json.loads((O/'template_style_map.json').read_text())
 specs=[]
 items=selected['families']
 specs.append({'name':'Priority ten','headers':['Priority','Addition','Research origin','Source records','Sessions','Why included now','Source files','Use boundary'],
  'rows':[[s['rank'],s['sheet'],s['owner'],s['rows'],', '.join(s['days']),s['reason'],len(s['sources']),'Original observations; future labels and retrospective cohorts are not online inputs.'] for s in items],
  'widths':[12,38,18,22,48,105,18,105],**styles})
 for item in items:
  specs.append({'name':item['sheet'],'headers':['Source ID','Source row zero based','Trading date','Source table','Immutable source']+item['fields'],
                'rows':data_rows(item),'widths':[14,22,18,48,90]+[32]*len(item['fields']),**styles})
 target=P/'Frankie_four_day_priority_ten.xlsx'
 report=build(baseline,target,specs,preserve=True)
 assert target.stat().st_size<100_000_000, 'Split companion required before publication'
 (P/'priority_workbook_receipt.json').write_text(json.dumps({'file':target.name,'bytes':target.stat().st_size,'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'sheets':report,'original_workbook_sha256':hashlib.sha256(baseline.read_bytes()).hexdigest()},indent=2))
 print('PRIORITY WORKBOOK COMPLETE',target.stat().st_size,flush=True)

if __name__=='__main__':main()
