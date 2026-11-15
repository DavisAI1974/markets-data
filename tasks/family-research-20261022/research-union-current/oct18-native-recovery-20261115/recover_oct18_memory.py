"""Memory-only Oct18 recovery from immutable GitHub archives; no S execution."""
import base64,bisect,collections,gzip,hashlib,io,json,subprocess,sys,urllib.request
from concurrent.futures import ThreadPoolExecutor

REPO='DavisAI1974/markets-data'
BRANCH='codex/evidence-availability-20261113'
BASE='fd72c6054947851581f55f2b2fd1ac6cdd869a7f'
SOURCE_REF='3d0b06aa29781d5e39cc3eb45c6d09e174f195a2'
ROOT='tasks/family-research-20261022/research-union-current/'
FIELD_ROOT=ROOT+'field-rebuild-20261113/'
DEST=ROOT+'oct18-native-recovery-20261115/'
SOURCES={
'queue':('b658c980ce69d4af4c4009fa6f4ea6e47207c801',1570550),
'replenishment':('2314610a5f2ca364314d30d7375a381cc1d5adb3',5970027)}
FIELDS={'replenishment':'L050 | resilience_and_recovery','queue':'L051 | churn_and_queue_turnover'}

def packed(x):return json.dumps(x,ensure_ascii=False,separators=(',',':'))
def sha(x):return hashlib.sha256(x).hexdigest()
def gitsha(x):return hashlib.sha1(b'blob '+str(len(x)).encode()+b'\0'+x).hexdigest()
def get(repo,ref,path,want=None):
    with urllib.request.urlopen('https://raw.githubusercontent.com/'+repo+'/'+ref+'/'+path,timeout=120) as f:raw=f.read()
    if want is not None:assert gitsha(raw)==want,(path,gitsha(raw),want)
    return raw
def api(path,method='GET',data=None):
    args=['gh','api','repos/'+REPO+'/'+path]
    if method!='GET':args+=['--method',method]
    if data is not None:args+=['--input','-']
    r=subprocess.run(args,input=None if data is None else packed(data).encode(),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if r.returncode:raise RuntimeError(r.stderr.decode()[:1000])
    return json.loads(r.stdout)
def git_commit(files,message):
    head=api('git/ref/heads/'+BRANCH)['object']['sha']
    tree=api('git/commits/'+head)['tree']['sha'];entries=[]
    for name,raw in files.items():
        print(packed({'publishing':name,'bytes':len(raw)}),flush=True)
        b=api('git/blobs','POST',{'content':base64.b64encode(raw).decode(),'encoding':'base64'})
        assert b['sha']==gitsha(raw)
        entries.append({'path':DEST+name,'mode':'100644','type':'blob','sha':b['sha']})
    newtree=api('git/trees','POST',{'base_tree':tree,'tree':entries})['sha']
    commit=api('git/commits','POST',{'message':message,'tree':newtree,'parents':[head]})['sha']
    assert api('git/ref/heads/'+BRANCH)['object']['sha']==head,'Branch advanced; leave commit unreferenced and retry after inspection'
    api('git/refs/heads/'+BRANCH,'PATCH',{'sha':commit,'force':False})
    assert api('git/ref/heads/'+BRANCH)['object']['sha']==commit
    for name,raw in files.items():assert get(REPO,commit,DEST+name)==raw,name
    return commit
def indices(records,clock,cursor):
    keys=[(r['known_by_ns'],r['input_cursor']) for r in records]
    assert all(keys[i][1]<=keys[i+1][1] for i in range(len(keys)-1)),'Receive/cursor order mismatch'
    end=bisect.bisect_right(keys,(clock,cursor))
    if not end:return []
    start=bisect.bisect_left(keys,(keys[end-1][0],-1))
    result=list(range(start,end))
    assert all(records[i]['known_by_ns']<=clock and records[i]['input_cursor']<=cursor for i in result)
    return result
def self_test():
    ns=1696247018981998588
    rs=[{'known_by_ns':ns,'input_cursor':2},{'known_by_ns':ns,'input_cursor':3},{'known_by_ns':ns+1,'input_cursor':4}]
    assert indices(rs,ns,2)==[0]
    assert indices(rs,ns,3)==[0,1]
    assert indices(rs,ns-1,4)==[]
    try:indices([{'known_by_ns':ns-1,'input_cursor':9},{'known_by_ns':ns,'input_cursor':1}],ns,2)
    except AssertionError:pass
    else:raise AssertionError('Must reject incompatible clocks/cursors')
def col(n):
    out=''
    while n>=0:n,r=divmod(n,26);out=chr(65+r)+out;n-=1
    return out

def main(script_source):
    self_test()
    sys.path.insert(0,'E:/frankie-excel-review-20261109/python-deps')
    import pyarrow.parquet as pq
    records={};pins={};all_counts={};output_files={}
    for section,(blob,nbytes) in SOURCES.items():
        path='artifacts/sqlite-triage/20261022/families/trade-lifecycle-targeted-v1/source-'+section+'.jsonl.gz'
        raw=get('DavisAI1974/Markets',SOURCE_REF,path,blob);assert len(raw)==nbytes
        rows=[json.loads(line) for line in gzip.decompress(raw).splitlines()]
        for r in rows:
            o=r['original_record']
            assert r['known_by_ns']==o['emitted_at_recv_ns']
            assert r['input_cursor']==o['frankie_emission']['input_cursor']
            assert r['instrument_id']==150611 and o['source_day']=='20231018'
        all_counts[section]=len(rows)
        if section=='replenishment':rows=[r for r in rows if 'outcome' in r['original_record']]
        rows.sort(key=lambda r:(r['known_by_ns'],r['input_cursor'],r['source_line']))
        assert len({r['source_line'] for r in rows})==len(rows)
        indices(rows,2**63-1,2**63-1)
        records[section]=rows
        pins[section]={'repository':'DavisAI1974/Markets','revision':SOURCE_REF,'path':path,'git_blob':blob,'bytes':nbytes,'sha256':sha(raw),'records':len(rows)}
        output_files[section+'-source-records.jsonl.gz']=gzip.compress((''.join(packed(r)+'\n' for r in rows)).encode(),mtime=0)
    manifest=json.loads(get(REPO,BASE,FIELD_ROOT+'ORIGINAL_FULL_POPULATION_MANIFEST.json'))
    shards=[e for e in manifest['sources'] if '/20231018/' in e['path']]
    def load(e):
        raw=get('DavisAI1974/'+e['repo'],e['ref'],e['path'],e['sha'])
        assert len(raw)==e['size']
        table=pq.read_table(io.BytesIO(raw),columns=['trade_ordinal','trade_cursor','receive_ns'])
        assert table.num_rows==e['rows']
        return table.to_pylist()
    trades=[]
    with ThreadPoolExecutor(max_workers=4) as pool:
        for rows in pool.map(load,shards):trades.extend(rows)
    trades.sort(key=lambda r:int(r['trade_ordinal']))
    assert len(trades)==30739
    assert [int(t['trade_ordinal']) for t in trades]==list(range(30739))
    lookup={};counts=collections.Counter();keys={s:[(r['known_by_ns'],r['input_cursor']) for r in rs] for s,rs in records.items()}
    patch_names=[]
    for offset in range(0,len(trades),1000):
        output=io.BytesIO()
        with gzip.GzipFile(fileobj=output,mode='wb',mtime=0) as stream:
            for t in trades[offset:offset+1000]:
                clock=int(t['receive_ns']);cursor=int(t['trade_cursor']);ordinal=int(t['trade_ordinal']);fields={}
                for section,rs in records.items():
                    ks=keys[section];end=bisect.bisect_right(ks,(clock,cursor));start=bisect.bisect_left(ks,(ks[end-1][0],-1)) if end else 0
                    chosen=rs[start:end]
                    assert all(r['known_by_ns']<=clock and r['input_cursor']<=cursor for r in chosen)
                    if chosen:
                        counts[section]+=1
                        fields[FIELDS[section]]={
                        'status':'RECOVERED_ORIGINAL_OUTCOME_OBSERVATIONS' if section=='replenishment' else 'RECOVERED_ORIGINAL_TERMINAL_QUEUE_OBSERVATIONS',
                        'asof_receive_ns':clock,'asof_input_cursor':cursor,'known_by_ns':chosen[-1]['known_by_ns'],
                        'values':{'records':chosen},'source':pins[section],
                        'scope':'Latest eligible original '+section+' outcome emission, with every same-clock eligible tie. Original measured values and missing states retained. Not proof of complete active-state or named-layer semantics.',
                        'all_field_semantics_complete':False,
                        'horizon_policy':'Original outcome horizons are archived provenance only. No new horizon or S calculation was run.'}
                    else:
                        fields[FIELDS[section]]={'status':'NO_ELIGIBLE_ORIGINAL_OUTCOME','values':None,'asof_receive_ns':clock,'asof_input_cursor':cursor,'source':pins[section]}
                row={'trade_ordinal':ordinal,'trade_cursor':cursor,'receive_ns':clock,'fields':fields}
                stream.write((packed(row)+'\n').encode());lookup[ordinal]=row
        name=f'20231018-all-trade-native-patch-{offset//1000:03d}.jsonl.gz'
        output_files[name]=output.getvalue();patch_names.append(name)
        assert len(output_files[name])<45_000_000,(name,len(output_files[name]))
        print(packed({'patch':name,'bytes':len(output_files[name])}),flush=True)
    layout=json.loads(get(REPO,BASE,FIELD_ROOT+'WORKBOOK_LAYOUT.json'))
    package=json.loads(gzip.decompress(get(REPO,BASE,ROOT+'evidence-availability-20261113/raw/package.json.gz')))
    updates=[];maxchars=0
    for case in package['cases']:
        if case['day']!='20231018':continue
        caseid='20231018-'+str(case['category_index'])
        original=json.loads(gzip.decompress(get(REPO,BASE,ROOT+'evidence-availability-20261113/raw/'+caseid+'.json.gz')))
        headers=original['headers'];location=next(x for x in layout['loc'] if x['candidate']==case['life']['candidate_id'])
        for i,row in enumerate(original['rows']):
            ordinal=int(row[headers.index('trade_ordinal')]);matched=lookup[ordinal]
            for field,value in matched['fields'].items():
                j=headers.index(field);prior=json.loads(row[j])
                assert prior['status'] in ('MISSING_STATIC_SOURCE','NO_MATCHING_VALUE_IN_RETAINED_INPUT')
                assert value['status']!='NO_ELIGIBLE_ORIGINAL_OUTCOME'
                address=col(location['base']+layout['tickPositions'][j])+str(location['headRow']+i+2)
                text=packed(value);maxchars=max(maxchars,len(text))
                updates.append({'cell':address,'value':text,'field':field,'case':caseid,'row':i,'trade_ordinal':ordinal})
    assert len(updates)==2894 and len({u['cell'] for u in updates})==2894
    output_files['workbook-native-updates.jsonl.gz']=gzip.compress((''.join(packed(r)+'\n' for r in updates)).encode(),mtime=0)
    # Independently re-read every emitted patch and compare exact original archive records by index.
    reread_count=0
    for patch_name in patch_names:
        reread=[json.loads(x) for x in gzip.decompress(output_files[patch_name]).splitlines()]
        reread_count+=len(reread)
        for row in reread:
            for section,field in FIELDS.items():
                value=row['fields'][field];rs=records[section];ks=keys[section]
                end=bisect.bisect_right(ks,(row['receive_ns'],row['trade_cursor']))
                if not end:assert value['values'] is None;continue
                chosen=value['values']['records'];latest=ks[end-1][0]
                start=bisect.bisect_left(ks,(latest,-1))
                assert chosen==rs[start:end]
                assert all(r['input_cursor']<=row['trade_cursor'] for r in chosen)
    assert reread_count==30739
    result={'source_pins':pins,'archived_section_rows':all_counts,'retained_outcome_records':{s:len(r) for s,r in records.items()},
            'full_population_trades_preserved':len(trades),'trades_with_outcomes':dict(counts),'selected_workbook_cells':len(updates),
            'max_prepared_cell_characters':maxchars,'full_field_semantics_complete':False,'s_calculations_started':False,
            'files_saved_to_local_disk':0,'full_patch_roundtrip_verified':True,'all_selected_ticks_retained':1447,
            'tests':['integer nanoseconds','same-clock ties','cursor cutoff','incompatible clock order rejection','all-source-byte Git hashes','all-trade patch roundtrip'],
            'patch_shards':patch_names,
            'output_sha256':{name:sha(raw) for name,raw in output_files.items()}}
    output_files['RECOVERY_VERIFICATION.json']=(json.dumps(result,indent=2)+'\n').encode()
    output_files['recover_oct18_memory.py']=script_source.encode()
    output_files['README.md']=('# Oct18 omitted native outcome recovery\n\nRecovered the original queue and replenishment outcomes directly from pinned GitHub archives. All 30,739 Oct18 trades remain, including trades with no eligible earlier outcome. The prepared workbook patch fills 2,894 formerly empty cells across all 1,447 selected Oct18 ticks. No S calculation or new fixed horizon was run. These are original observations, not a claim that full active-state semantics or all 35 missing fields are complete.\n\nAll processing and publication used memory only; zero task files were saved to local drives. Complete source record dictionaries and the all-trade patch are preserved in this directory. The workbook update is a separate verified step.\n').encode()
    commit=git_commit(output_files,'research: recover omitted Oct18 native outcomes entirely in memory')
    print(json.dumps({'commit':commit,'report':result}),flush=True)

if __name__=='__main__':
    if '--self-test' in sys.argv:self_test();print('4 focused boundary checks passed')
    else:main(SCRIPT_SOURCE)
