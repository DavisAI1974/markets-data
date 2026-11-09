from acquire import ROOT
import json,csv,gzip,re,hashlib,collections,bisect,shutil,datetime,decimal,os
from pathlib import Path
import pyarrow.parquet as pq

OUT=ROOT/'current';OUT.mkdir(exist_ok=True);(OUT/'evidence').mkdir(exist_ok=True)
sources=json.loads((ROOT/'active_sources.json').read_text())
schemas={x['id']:x for x in json.loads((ROOT/'table_schemas.json').read_text())}
cache=Path('E:/markets-data-frankie-audit-20261109/tasks/family-research-20261022/native-dipole/20261108-33693e180/agent-pass/cache')
DAY0={'20231002':1696194000,'20231003':1696280400,'20231017':1697490000,'20231018':1697576400}
DAYTAG={'oct02':'20231002','oct03':'20231003','oct17':'20231017','oct18':'20231018'}
LO,HI=1_577_836_800_000_000_000,1_893_456_000_000_000_000
groups={};raws={};trades={d:[] for d in DAY0};trade_exact={d:collections.defaultdict(list) for d in DAY0}
for day in DAY0:
    g=pq.read_table(cache/f'groups-{day}.parquet',columns=['receive_ns','cursor','group']).to_pydict()
    groups[day]=g
print('group clocks loaded',flush=True)

trade_fields=['day','trade_ordinal','trade_id','trade_cursor','event_ns','receive_ns','known_by_ns','coverage','source_trade_revision','source_trade_path']
with (OUT/'trade_spine.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f);w.writerow(trade_fields+['source_id','source_row_0based'])
    for s in sources:
        if '/frankie-four-day-pins/run-42608467894-1/' not in s['path'] or not s['path'].endswith('.parquet'):continue
        for i,r in enumerate(pq.read_table(ROOT/'objects'/s['sha'],columns=trade_fields).to_pylist()):
            day=r['day'];w.writerow([r[k] for k in trade_fields]+[s['id'],i]);trades[day].append(r)
            for key in ['receive_ns','known_by_ns']:trade_exact[day][int(r[key])].append(r['trade_id'])
for d in trades:trades[d].sort(key=lambda r:int(r['receive_ns']))
trade_times={d:[int(r['receive_ns']) for r in rs] for d,rs in trades.items()}
print('trade rows',sum(map(len,trades.values())),flush=True)

def rows(s):
    f=ROOT/'objects'/s['sha'];p=s['path']
    op=gzip.open(f,'rt',encoding='utf-8-sig') if p.endswith('.gz') else f.open(encoding='utf-8-sig')
    with op:
        if '.csv' in p: yield from csv.DictReader(op)
        else:
            for line in op:
                if line.strip():yield json.loads(line)

def dayof(s,r):
    # A tape is a UTC calendar member, not necessarily its trading session.
    # odcfg.SESS_TAPES explicitly puts the prior evening in the following session.
    m=re.search(r'/tables/dipole/(202310(?:02|03|17|18))/',s['path'])
    if m:return m[1]
    if '/claude-pass/tables/dipole/' in s['path']:return '20231018'
    for k in ['day','session','trading_date','date','tape']:
        v=str(r.get(k,''));v=DAYTAG.get(v,v.replace('-',''))
        if v in DAY0:return v
    m=re.search(r'(202310(?:02|03|17|18))',s['path'])
    if m:return m[1]
    for tag,d in DAYTAG.items():
        if tag in s['path']:return d
    return ''

def nsvalue(k,v):
    if v is None or isinstance(v,bool):return None
    try:
        n=decimal.Decimal(str(v))
        if not n.is_finite():return None
        if (k.endswith('_ns') or k in ['ns']) and LO<=n<=HI and n==int(n):return int(n)
        if (k.endswith(('_epoch_s','_second')) or k in ['second','exact_second','event_s','epoch_s','available_s']) and LO//10**9<=n<=HI//10**9:
            return int(n*10**9)
    except (decimal.InvalidOperation,ValueError):pass
    return None

# Explicit Desktop row identity -> candidate clocks. An array of offsets is a trajectory,
# not hundreds of invented independent candidates.
parents={}
parent_boundaries={}
for s in sources:
    if s['path'].endswith('t6_cohort_coverage.csv') and '/claude-pass' in s['path'] and (ROOT/'objects'/s['sha']).exists():
        for r in rows(s):
            day=dayof(s,r)
            if day and r.get('row') is not None and r.get('pre_ns'):
                parent_boundaries[(day,str(r['row']))]=int(r['pre_ns'])
for s in sources:
    if s['path'].endswith('t6_cohort_features.csv') and '/claude-pass' in s['path'] and (ROOT/'objects'/s['sha']).exists():
        for r in rows(s):
            day=dayof(s,r)
            if day and r.get('row') is not None:
                parents[(day,str(r['row']))]=(r.get('prov_candidate_id',''),int(r['prov_birth_second'])*10**9,int(r['prov_recognition_ns']))

PINHEAD=['source_id','source_row_0based','day','record_identity','primary_clock_field','primary_clock_ns_exact','clock_role','observed_group_receive_ns_exact','observed_group_cursor','exact_trade_ids','all_clock_fields_json','record_status']
writers={};handles={};counts=collections.Counter();file_summary=[];field_rows=[];problem_counts=collections.Counter();parent_count=0
for day in list(DAY0)+['crossday']:
    f=(OUT/f'pins-{day}.csv').open('w',newline='',encoding='utf-8');handles[day]=f;writers[day]=csv.writer(f);writers[day].writerow(PINHEAD)

priority=['known_by_ns','receive_ns','start_recv_ns','onset_ns','raw_receive_ns','group_ns','event_ns','cut_ns','cutoff_ns','recognition_receive_ns','prov_recognition_ns','recognition_ns','recovered_recognition_ns','first_event_ns','start_ns','first_ns','anchor_ns','pre_ns','t0_epoch_s','birth_second','prov_birth_second','event_second','second']
seen_content={}
for si,s in enumerate(sources):
    f=ROOT/'objects'/s['sha'];p=s['path'];schema=schemas.get(s['id'])
    s['record_rows']=0;s['pinned_rows']=0;s['attachment_rows']=0;s['issues']=0;s['current_attachment']=''
    if not f.exists():
        s['handling']='Immutable source attachment (not downloaded)';continue
    if schema is None:
        s['handling']='Attachment: complete source artifact'
        # Non-tabular studies, charts and methods stay linked to their exact source.
        continue
    if s['sha'] in seen_content:
        s['handling']='Same content as '+seen_content[s['sha']];s['canonical_source_id']=seen_content[s['sha']];continue
    seen_content[s['sha']]=s['id']
    dest=OUT/'evidence'/f"{s['id']}.jsonl.gz"
    s['current_attachment']='evidence/'+dest.name;s['handling']='All rows processed; exact clocks pinned or study attached'
    fields=collections.Counter();pin_n=0;attach_n=0;issue_n=0
    with gzip.open(dest,'wt',encoding='utf-8',compresslevel=3) as out:
        for ordinal,r in enumerate(rows(s)):
            day=dayof(s,r); clocks={};issue=[];derived={}
            for k,v in r.items():
                fields[k]+=1;n=nsvalue(k,v)
                if n is not None:
                    if ('e' in str(v).lower() or isinstance(v,float)) and k.endswith('_ns'):
                        issue.append('Clock precision requires exact-source recovery: '+k)
                        continue
                    # A session origin is provenance, never a record event timestamp.
                    if k=='day0_epoch_s':continue
                    # These generated absolute fields need their duration semantics verified.
                    if k.startswith('info_horizon_'):
                        issue.append('Horizon offset clock needs producer semantics: '+k);continue
                    clocks[k]=str(n)
            if not clocks and day and isinstance(r.get('t0'),(int,float)) and 0<=r['t0']<86400:
                clocks['t0_session_second']=str((DAY0[day]+int(r['t0']))*10**9)
                derived['t0_session_second']='Documented DAY0 plus original t0; second-resolution event label'
            if s['owner']=='Desktop' and day and r.get('row') is not None and (day,str(r['row'])) in parents:
                cid,birth,recognition=parents[(day,str(r['row']))]
                if not clocks:
                    clocks={'parent_birth_second':str(birth),'parent_recognition_ns':str(recognition)}
                    derived['parent']='Exact (day,row) link to t6_cohort_features; parent context, not row observation'
                    parent_count+=1
                for k,v in r.items():
                    if k in ['k_aggressor_start','k_touch_size_change','k_quote_relocation'] and v not in ['',None,'nan']:
                        try:
                            offset=int(v)
                            if offset<0:continue # documented no-event sentinel
                            boundary=parent_boundaries[(day,str(r['row']))]
                            clocks[k+'_boundary_ns']=str(boundary+offset*10**9)
                            derived[k+'_boundary_ns']='Exact cohort pre_ns plus original relative second; interval start for aggressor, book-state boundary for touch/quote; not first raw event clock'
                        except ValueError:pass
            identity=next((str(r[k]) for k in ['case_id','record_id','candidate_id','prov_candidate_id','family_id','instance','row','t0','definition'] if r.get(k) not in [None,'']),str(ordinal))
            primary=next((k for k in priority if k in clocks),next(iter(clocks),'') )
            if primary:
                ns=int(clocks[primary]); role='source timestamp'
                if any(x in primary for x in ['cut','anchor']):role='scheduled cutoff or anchor'
                elif 'parent_' in primary:role='linked parent context'
                elif primary.endswith(('second','epoch_s')) or primary=='t0_session_second':role='second-resolution label'
                elif 'known' in primary:role='known-by source clock'
                obs='';cursor='';exact=[]
                if day:
                    g=groups[day];j=bisect.bisect_right(g['receive_ns'],ns)-1
                    if j>=0:
                        obs=str(g['receive_ns'][j]);cursor=str(g['cursor'][j])
                    exact=sorted(set(trade_exact[day].get(ns,[])))
                status='Clock precision unresolved in '+str(len(issue))+' field(s)' if issue else 'Included'
                writers[day or 'crossday'].writerow([s['id'],ordinal,day,identity,primary,str(ns),role,obs,cursor,';'.join(exact),json.dumps(clocks,separators=(',',':')),status])
                pin_n+=1;counts[day or 'crossday']+=1
            else:attach_n+=1
            if issue:
                issue_n+=1
                for msg in issue:problem_counts[(s['id'],msg)]+=1
            # Complete original variables plus explicit mapping; no candidate-performance filter.
            out.write(json.dumps({'source_row_0based':ordinal,'data':r,'pin_clocks_ns':clocks,'clock_derivations':derived,'clock_issues':issue},separators=(',',':'),ensure_ascii=False)+'\n')
        s['record_rows']=pin_n+attach_n;s['pinned_rows']=pin_n;s['attachment_rows']=attach_n;s['issues']=issue_n
    for field,n in fields.items():field_rows.append([s['id'],field,n])
    if (si%50)==0: print('processed',si,'pins',sum(counts.values()),flush=True)
for f in handles.values():f.close()

with (OUT/'field_inventory.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f);w.writerow(['source_id','field','populated_record_presence']);w.writerows(field_rows)
with (OUT/'clock_gaps.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f);w.writerow(['source_id','gap','affected_rows']);w.writerows([list(k)+[v] for k,v in problem_counts.items()])
(OUT/'source_catalog.json').write_text(json.dumps(sources,indent=2),encoding='utf-8')
summary={'active_source_files':len(sources),'parsed_records':sum(s.get('record_rows',0) for s in sources),'pinned_records':dict(counts),'attached_non_event_records':sum(s.get('attachment_rows',0) for s in sources),'clock_issue_records':sum(s.get('issues',0) for s in sources),'trade_rows':{d:len(rs) for d,rs in trades.items()},'parent_context_rows':parent_count,'superseded_versions_in_current_catalog':0,'performance_exclusions':0}
(OUT/'coverage.json').write_text(json.dumps(summary,indent=2))
shutil.copyfile(ROOT/'corrected_price_response.json',OUT/'corrected_price_response.json')
shutil.copyfile(ROOT/'price_clock_verification.json',OUT/'price_clock_verification.json')
print(json.dumps(summary),flush=True)
