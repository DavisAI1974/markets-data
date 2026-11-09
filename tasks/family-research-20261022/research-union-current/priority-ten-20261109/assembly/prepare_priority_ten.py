"""Freeze ten research additions by practical gap, without selecting winners."""
from pathlib import Path
import csv, gzip, hashlib, json, re, datetime, sys
ROOT=Path(__file__).parent
OUT=ROOT/'priority-now'
OUT.mkdir(exist_ok=True)

DEFS=[
 ('P01 Fresh versus expiring flow','Codex','Distinguish new aggression from rolling-window expiry before a flow trigger.',
  lambda p:p.endswith('/native-flow-source-clocks.parquet')),
 ('P02 Flow depth and refill','Desktop','Add full-depth, touch counts, fills, adds and removals to each family context.',
  lambda p:bool(re.fullmatch(r'claude-pass-3day/tables/202310\d{2}/t1_family_master_flags.csv',p))),
 ('P03 Four arm entry candidates','CCode','Compare flow and book agreement and disagreement across all recorded candidates.',
  lambda p:bool(re.fullmatch(r'claude-code/decision-candidates-four-arm-oct\d{2}-events.jsonl.gz',p))),
 ('P04 Order identity lifecycle','Codex','Tie aggression to later resting display and actual order actions without inferring intent.',
  lambda p:atlas(p,{'aggression-to-rest-events.csv','aggression-to-rest-actions.csv.gz'})),
 ('P05 Observable resting state','Codex','Separate state known at decision time from later fills and removal.',
  lambda p:atlas(p,{'resting-observation-decisions.csv.gz'})),
 ('P06 Matched prebirth controls','Codex','Retain controls, missing matches and adverse precursor differences.',
  lambda p:atlas(p,{'prebirth-cases.csv.gz','prebirth-matched-pairs.csv.gz'})),
 ('P07 One lot order origins','CCode','Expose order age, repeated onsets and later fate of thin-touch orders.',
  lambda p:bool(re.fullmatch(r'claude-code/size-one-orders-oct\d{2}.jsonl.gz',p))),
 ('P08 Event order and lean','Desktop','Compare aggression, size change, price relocation and recognition; preserve control curves.',
  lambda p:bool(re.fullmatch(r'claude-pass-3day/tables/dipole/202310\d{2}/(?:x07_first_events|x09_lean_cohort|x09_lean_control).csv',p))),
 ('P09 Recognition boundary','CCode','Separate observed birth-to-recognition movement from subsequent movement.',
  lambda p:bool(re.fullmatch(r'claude-code/dipole-post-recognition-oct\d{2}-rows.jsonl.gz',p))),
 ('P10 Price flow book context','Codex','Add price path, fresh flow, display changes and explicit empty states at the decision clock.',
  lambda p:atlas(p,{'stack-features.csv.gz'})),
]

def atlas(path,names):
 return (path.startswith('research-atlas-v2/') or bool(re.match(r'replay-comparison/202310(?:02|03|17)/research-atlas-v2/',path))) and path.split('/')[-1] in names

def source_rows(s):
 p=ROOT/'objects'/s['sha']
 if s['path'].endswith('.parquet'):
  import pyarrow.parquet as pq
  for batch in pq.ParquetFile(p).iter_batches(batch_size=4096):yield from batch.to_pylist()
  return
 with (gzip.open(p,'rt',encoding='utf-8-sig') if s['path'].endswith('.gz') else p.open(encoding='utf-8-sig',newline='')) as f:
  if '.csv' in s['path']:yield from csv.DictReader(f)
  else:
   for line in f:
    if line.strip():yield json.loads(line)

def flatten(row,prefix=''):
 result={}
 for k,v in row.items():
  key=prefix+k
  if isinstance(v,dict):result.update(flatten(v,key+'.'))
  else:result[key]=json.dumps(v,separators=(',',':')) if isinstance(v,list) else v
 return result

def main():
 sources={s['id']:s for s in json.loads((ROOT/'active_sources.json').read_text())}
 sources.update({s['id']:s for s in json.loads((ROOT/'workflow_sources.json').read_text())})
 previous=json.loads((OUT/'priority_selection.json').read_text())['families'] if (OUT/'priority_selection.json').exists() else []
 only=next((a.split('=',1)[1] for a in sys.argv if a.startswith('--only=')),None)
 catalog=[]
 for rank,(sheet,owner,why,select) in enumerate(DEFS,1):
  if only and not sheet.startswith(only):
   catalog.append(next(c for c in previous if c['sheet']==sheet));continue
  selected=[s for s in sources.values() if select(s['path'].split('family-research-20261022/',1)[-1])]
  assert selected,sheet
  fields=[];source_counts=[];total=0;days=set()
  output=OUT/(sheet[:3]+'.jsonl.gz')
  with gzip.open(output,'wt',encoding='utf8',compresslevel=1) as f:
   for s in sorted(selected,key=lambda s:s['path']):
    b=(ROOT/'objects'/s['sha']).read_bytes()
    assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==s['sha']
    count=0
    for ordinal,row in enumerate(source_rows(s)):
     flat=flatten(row)
     for k in flat:
      if k not in fields:fields.append(k)
     m=re.search(r'202310(?:02|03|17|18)|oct(?:02|03|17|18)',s['path'])
     day=(m[0].replace('oct','202310') if m else '20231018')
     if sheet.startswith('P01') and 'day' in row:day=str(row['day'])
     days.add(day)
     f.write(json.dumps({'source_id':s['id'],'source_row':ordinal,'day':day,'source_type':s['path'].split('/')[-1], 'values':flat},separators=(',',':'),ensure_ascii=False)+'\n')
     count+=1
    total+=count
    source_counts.append({**{k:s[k] for k in ['id','path','repo','ref','sha','url']},'rows':count})
  entry={'rank':rank,'sheet':sheet,'owner':owner,'reason':why,'rows':total,'days':sorted(days),'fields':fields,'sources':source_counts,'data_file':output.name}
  catalog.append(entry)
  print(sheet,total,len(fields),sorted(days),flush=True)
 (OUT/'priority_selection.json').write_text(json.dumps({'selected_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'selection_basis':'Decision relevance, causal-clock safety and missing comparison coverage; not measured profitability. All rows within selected sources retained.','families':catalog},indent=2))

if __name__=='__main__':main()
