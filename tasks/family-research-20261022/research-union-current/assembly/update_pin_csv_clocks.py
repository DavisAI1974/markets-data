from acquire import ROOT
import csv,gzip,json
O=ROOT/'current';fixed={}
for sid in ['S00092','S00096','S00101','S00105']:
 with gzip.open(O/'evidence'/f'{sid}.jsonl.gz','rt',encoding='utf8') as f:
  for l in f:
   r=json.loads(l);fixed[(sid,str(r['source_row_0based']))]=json.dumps(r['pin_clocks_ns'],separators=(',',':'))
for day in ['20231002','20231003','20231017','20231018']:
 p=O/f'pins-{day}.csv';tmp=p.with_suffix('.repair');n=0
 with p.open(encoding='utf8',newline='') as src,tmp.open('w',encoding='utf8',newline='') as dst:
  r=csv.DictReader(src);w=csv.DictWriter(dst,fieldnames=r.fieldnames);w.writeheader()
  for row in r:
   key=(row['source_id'],row['source_row_0based'])
   if key in fixed:row['all_clock_fields_json']=fixed[key];row['record_status']='Included; source-derived horizon correction applied';n+=1
   w.writerow(row)
 tmp.replace(p);print(day,n,flush=True)
