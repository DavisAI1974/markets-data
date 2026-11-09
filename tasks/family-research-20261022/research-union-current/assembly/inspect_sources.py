from acquire import ROOT
import json,gzip,csv,io,collections,itertools
a=json.loads((ROOT/'source_inventory.json').read_text())
patterns=['a-state-direction-knowable-oct02-events','decision-candidates-four-arm-oct02-events','exhaustion-clock-oct02-events','size-one','t6_cohort_features.csv','x03_cohort_stats.csv.gz','x07_first_events.csv','t1_family_master.csv','all-row-clock-pins','native-dipole/20261108-33693e180/agent-pass/tables/','research-atlas-v2/']
for pat in patterns:
    matches=[r for r in a if pat in r['path'] and (ROOT/'objects'/r['sha']).exists()]
    if not matches: continue
    r=matches[0]; b=(ROOT/'objects'/r['sha']).read_bytes()
    if r['path'].endswith('.gz'): b=gzip.decompress(b)
    if '.csv' in r['path']:
        rows=csv.DictReader(io.StringIO(b.decode('utf-8-sig'))); rec=next(rows,None)
    elif '.jsonl' in r['path']: rec=json.loads(b.splitlines()[0])
    elif '.json' in r['path']: rec=json.loads(b)
    else: continue
    print(r['id'],r['path'],json.dumps(rec)[:4500])
