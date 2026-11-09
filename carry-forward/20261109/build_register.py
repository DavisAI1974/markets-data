import csv,gzip,hashlib,io,json,pathlib,re,zipfile,collections

ROOT=pathlib.Path(__file__).parent
OUT=ROOT/'delivery'
sources=json.loads((ROOT/'source_catalog.json').read_text(encoding='utf-8'))
sections=json.loads((ROOT/'sections.json').read_text(encoding='utf-8'))
byid={s['id']:s for s in sources}
records=[]

def origin(sid,line):
    s=byid[sid]
    section=next((x for x in sections if x['git_blob_sha']==s['sha'] and x['start_line']<=line<=x['end_line']),None)
    return {'source_id':sid,'git_blob_sha':s['sha'],'url':s['url']+'#L'+str(line),'line':line,'section_id':section['section_id'] if section else None}

def add(id,name,kind,definition,sid,line,dimensions=None,needs=None,related=None):
    r={'id':id,'name':name,'kind':kind,'paper_included':True,'execution_status':'definition_or_source_binding_pending','platform_active':False,'source_definition':definition,'dimensions_to_preserve':dimensions or [],'remaining_work':needs or ['Recover and freeze the exact causal trigger, direction, entry, exit and reset definitions from the source; bind required inputs; implement platform paper execution.'],'related_current_rules':related or [],'evidence_policy':'Retain favorable, adverse, flat, undefined, censored, missed and no-fill cases; no historical-performance admission threshold.','sources':[origin(sid,line)]}
    records.append(r)
    return r

prior=OUT/'prior'
rules=json.loads((prior/'reanalysis-20261109/TRADE_RULES.json').read_text(encoding='utf-8'))
titles=list(csv.DictReader(io.StringIO((prior/'reanalysis-20261109/PAPER_HYPOTHESES.csv').read_text(encoding='utf-8'))))
ruleurl='https://github.com/DavisAI1974/markets-data/blob/codex/research-union-four-days-20261109/tasks/family-research-20261022/research-union-current/reanalysis-20261109/TRADE_RULES.json'
for r,t in zip(rules['strategies'],titles):
    assert r['id']==t['ID']
    records.append({'id':r['id'],'name':t['Hypothesis'],'kind':'encoded_strategy_variant','paper_included':True,'execution_status':'encoded_not_connected','platform_active':False,'source_definition':r,'dimensions_to_preserve':[],'remaining_work':['Implement and verify the rule engine in a platform paper account; bind data and adapter.'],'related_current_rules':[],'evidence_policy':t['Evidence and limits'],'sources':[{'url':ruleurl,'git_blob_sha':'e17c21d77f219de143d308031b3bda88bba2c55a','local_snapshot':'prior/reanalysis-20261109/TRADE_RULES.json'}]})

stack=json.loads((prior/'STACK_METHOD.json').read_text(encoding='utf-8'))
for i,(name,layers) in enumerate(stack['arms'].items(),1):
    r=add(f'ST{i:02}',name,'model_comparison_arm',{'always_present':stack['layers']['context'],'additional_layers':{k:stack['layers'][k] for k in layers},'fit':stack['fit']},'S00730',878,stack['targets'],['Recover the frozen model/coefficients for each target and source revision; define how each target informs paper decisions (absolute movement and flow strength are not directional orders); bind a causal opportunity clock and entry/exit logic.'])
    r['sources'].append(origin('S01758',1))
flow=json.loads((prior/'FLOW_BOOK_METHOD.json').read_text(encoding='utf-8'))
for i,(name,features) in enumerate(flow['arms'].items(),1):
    r=add(f'FB{i:02}',name,'model_comparison_arm',{'features':features,'fit':flow['fit']},'S00730',100,['All original signed and absolute targets, horizons and chronological folds'],['Recover model outputs and frozen coefficients, resolve causal opportunity availability, define target-to-order mapping and paper entry/exit.'])
    r['sources'].append(origin('S00778',1))

# Each source table row survives separately; these are overlapping comparison conditions, not independent trading rules.
flowcells=[('Recent flow baseline','1s and 5s classified flow agree and are nonzero'),('Long flow opposed','Recent flow baseline with 60s flow opposed'),('Long flow aligned','Recent flow baseline with 60s flow aligned'),('Touch aligned','Recent flow baseline with touch size imbalance aligned'),('Touch opposed','Recent flow baseline with touch size imbalance opposed'),('Near ladder aligned','Recent flow baseline with near-10 imbalance aligned'),('Near ladder opposed','Recent flow baseline with near-10 imbalance opposed'),('Long opposed / touch opposed','60s flow opposed to recent and touch opposed to recent'),('Long opposed / touch aligned','60s flow opposed to recent and touch aligned with recent'),('Saved selling screen','Recent selling with 60s buy-heavy flow; retain original 50-case screen and full denominators'),('Buying mirror','Recent buying with 60s sell-heavy flow')]
for i,(name,definition) in enumerate(flowcells,1):
    add(f'FC{i:02}',name,'conditional_comparison',definition,'S00307',149,['Both sides where defined; original 1/60/600s outcomes and original additional horizons; empty/neutral/missing populations retained'],related=['R1','R6A','R6B'])

for i,(name,definition) in enumerate([
('Weakening / book aligned','Absolute imbalance decreases from early to late 10s half, both nonempty; book aligned'),
('Weakening / book opposed','Same weakening definition; book opposed'),
('Strengthening / book aligned','Absolute imbalance increases from early to late 10s half, both nonempty; book aligned'),
('Strengthening / book opposed','Same strengthening definition; book opposed'),
('One half empty / aligned','Exactly one half-window empty; retain early-versus-late distinction; book aligned'),
('One half empty / opposed','Exactly one half-window empty; retain early-versus-late distinction; book opposed'),
('Both halves empty','Both flow halves empty; this is not measured balanced flow'),
('Balanced and steady states','Keep balanced, unchanged-strength and zero-direction states with their original definitions')],1):
    add(f'DP{i:02}',name,'conditional_comparison',definition,'S00730',832,['Original activity quantities, price context, book signs and outcome horizons'],related=['R3','R7','R8'])

add('CH01','Frozen SSOS continuation','source_defined_play','NG_CHAIN_D4_SSOS_CONTINUATION_V1: four predecessor seed states S,S,O,S oldest to newest known before target t0; endpoint confirmed by onset+5 or no entry; stand down if successor starts before confirmation; enter with current polarity at onset+5, exit onset+30. Preserve detector and source-clock definitions.','S00307',1308,needs=['Bind the frozen detector and seed availability to paper inputs; implement the original play without substituting hindsight identities; preserve the negative four-date result.'])
add('CH02','P-O-X opposite-current','candidate_family','Preserve every causally valid P-O-X case; opposite-current branch is a candidate, not frozen.','S13290',79,['Original base and held populations; contrary outcomes'],related=[])
add('CH03','P-O-X same-current / re-origin','candidate_family','Retain delayed/re-origin thread. Parent still exits normally; later re-origin is a separate candidate.','S13290',82)
add('CH04','P-O-X parent management and trusted re-entry','source_defined_management','Valid parent -> structural endpoint+60 exit -> reset -> later trusted full SSOS or P-O-X-opposite setup; no automatic reversal or use of successor identity before known.','S13290',85,['Parent and later entry separate ledgers; no hindsight successor labels'])
add('CH05','Shallow versus deep post-exit recovery','conditional_comparison','Keep +30/+60 shallow-versus-deep adversity strata and +120/+300 recovery outcomes. Later recovery is not an entry input at the earlier clock.','S13290',89,['Original shallow/deep/other cases; relapse, mean returns, trusted-entry conditions'])
add('CH06','SSOS and P-O-X partial prefixes','candidate_family','Retain complete prefix ladders and partial states; prospective partial-prefix variants require an explicit causal rule.','S13290',91)
motifs=[('OOSS -> FLIP','AGAINST_CURRENT'),('SOOS -> SAME','WITH_CURRENT'),('OOO -> SAME','AGAINST_CURRENT'),('XSX -> FLIP','AGAINST_CURRENT'),('OSP -> SAME','Recover source direction mapping'),('OSP -> FLIP','Recover source direction mapping'),('PSOS -> FLIP','Recover source direction mapping'),('SXOO -> FLIP','Recover source direction mapping'),('OOO -> FLIP','Decompose older predecessor and timing-family subtypes')]
for i,(name,direction) in enumerate(motifs,1):add(f'CM{i:02}',name,'recurrence_candidate',direction,'S13290',96,['All original contexts, timing families and polarity cases; do not count each repeated observation as a new strategy'])
for i,(name,definition,line) in enumerate([
('D1 directional population','Preserve all exact D1s; elapsed duration is an annotation, not an inclusion filter.',100),
('D1 chop / rotation','Retain CHOP_ROTATION as an opportunity class separate from directional D1.',104),
('D2-D5 causal entry timing','Preserve all higher-order populations, predecessor availability, earliest causal entry and later-survivor fallback separately.',109),
('Chain-birth prior-horizon ladder','Preserve the original predecessor-horizon ladder, causal rule_ready clocks and all target depths; do not substitute a fitted timing center for an entry.',114),
('Timing families and rolling re-origin','Retain persistent/fast-collapse runway, D2/D3 timing families, longer-context recurrence and state ownership resets.',73)],1):add(f'CT{i:02}',name,'candidate_family',definition,'S13290',line,['All original depths, horizons, failed folds and reverse-backcast tags'])

onecells=[('Fresh new best','NEW_BEST with no reduction'),('Standing fill-linked','STANDING_BEST_SHRANK with fill-linked reduction'),('Standing unlinked','STANDING_BEST_SHRANK with unlinked reduction'),('Standing crowded prior touch','Standing shrank with prior touch more than two orders'),('Standing smaller prior touch','Standing shrank with prior touch two or fewer orders'),('New best / thin next level','NEW_BEST with next displayed level under 10 lots'),('New best / deeper next level','NEW_BEST with next displayed level at least 10 lots'),('Fill-linked / thin next level','Fill-linked reduction and next displayed level under 10 lots, retain both onset arms')]
for i,(name,definition) in enumerate(onecells,1):add(f'OL{i:02}',name,'conditional_comparison',definition,'S00307',1199,['Bid/ask, onset origin, still-open at actual arrival, original first-end outcomes and latency distribution'],related=['R10'])
add('OL09','Order-history survival and replenishment','candidate_family','Keep fresh adds, repriced arrivals, older resting orders, repeat survivors and original-order refill/depletion histories separately.','S00307',1258,['Original identity and queue history; distinguish observed replenishment from hidden-liquidity speculation'],related=['R2','R10'])

for i,(name,definition,line) in enumerate([
('State/activity direction matrix','Retain all nine direction sources, activity bands, state combinations and every two-source agreement, including sign reversals across dates.',803),
('Expected versus unexpected burst absorption','Preserve forecast-next-burst-side contrasts and the exact burst-window outcome; do not transfer the result to later play horizons.',850),
('Quiet-tape momentum reversal','Preserve quiet/fast-collapse-low/persistent-mid momentum contrasts and contrary days; original 300/600s horizons remain outcomes.',1066)],1):add(f'RG{i:02}',name,'candidate_family',definition,'S00307',line,['Every original cell, not only the highlighted favorable cells'])

for i,(name,definition,line) in enumerate([
('Prebirth versus ordinary controls','Preserve prebirth flow/price/book paths, all controls and missing states. Retrospective birth orientation cannot be a live trigger.',570),
('Window-aging versus fresh-arrival mechanisms','Preserve native arrivals, expiry, mixed and unknown-side causes; state persistence is distinct from price response.',732),
('Event-clock versus fixed-time states','Retain original event-time and fixed-time definitions, quote age and reset/missing states.',652),
('Fast-collapse mid-activity next-seed direction','Retain favorable Oct17/18 and unfavorable Oct2/3 outcomes, weaker book variant and all other cells.',1063),
('Order path and weakening authority','Preserve same-order creation/removal, fixed-delay survival and flow/book changes; retain alternative mechanisms.',545)],1):add(f'EX{i:02}',name,'candidate_family',definition,'S00730',line)

# A source-preservation queue is deliberately separate from the named hypothesis register.
gaps=list(csv.DictReader(io.StringIO((prior/'research_gap_queue.csv').read_text(encoding='utf-8'))))
claims=list(csv.DictReader(io.StringIO((prior/'discovery-depth-20261109/CLAIMS.csv').read_text(encoding='utf-8'))))
for c in claims:
    c['current_policy']='All hypotheses remain included for paper testing. Original observation-only/admission wording is superseded; original measurements and limitations remain intact.'
report=(prior/'reanalysis-20261109/REPORT.md').read_text(encoding='utf-8')
for m in re.finditer(r'^## (D\d+) [^\n]*\n',report,re.M):
    end=report.find('\n## ',m.end())
    claims.append({'claim_id':m.group(1),'full_source_section':report[m.start():end if end>=0 else len(report)],'source':'prior/reanalysis-20261109/REPORT.md','current_policy':'All paper hypotheses included; discovery evidence is not platform fills or untouched validation.'})
assert len(claims)==13

mapped=collections.defaultdict(list)
for r in records:
    for s in r['sources']:
        if s.get('section_id'):mapped[s['section_id']].append(r['id'])
crosswalk=[]
for s in sections:
    crosswalk.append({'section_id':s['section_id'],'source_blob':s['git_blob_sha'],'heading':s['heading'],'start_line':s['start_line'],'end_line':s['end_line'],'linked_register_ids':sorted(set(mapped[s['section_id']])),'mapping_status':'named_items_linked_full_section_review_pending' if mapped[s['section_id']] else 'preserved_pending_semantic_mapping','excluded_from_paper_on_evidence':False})

def writejson(name,obj):
    (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
writejson('HYPOTHESIS_REGISTER.json',records)
writejson('FINDINGS_REGISTER.json',claims)
writejson('GAP_REGISTER.json',gaps)
with (OUT/'HYPOTHESIS_REGISTER.csv').open('w',encoding='utf-8-sig',newline='') as f:
    columns=['id','name','kind','paper_included','execution_status','platform_active','source_definition','dimensions_to_preserve','remaining_work','related_current_rules','source_urls']
    w=csv.DictWriter(f,fieldnames=columns);w.writeheader()
    for r in records:
        d={k:r[k] for k in columns if k!='source_urls'}
        for k,v in d.items():
            if isinstance(v,(dict,list)):d[k]=json.dumps(v,ensure_ascii=False)
        d['source_urls']=' | '.join(s['url'] for s in r['sources']);w.writerow(d)
with gzip.open(OUT/'SECTION_CROSSWALK.jsonl.gz','wt',encoding='utf-8') as f:
    for r in crosswalk:f.write(json.dumps(r,ensure_ascii=False)+'\n')

with zipfile.ZipFile(OUT/'SOURCE_DOCUMENTS.zip','w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in sorted((ROOT/'documents').glob('*.md')):
        b=p.read_bytes();assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==p.stem
        z.writestr(p.name,b)
counts=dict(collections.Counter(r['kind'] for r in records))
coverage=json.loads((OUT/'SOURCE_COVERAGE.json').read_text(encoding='utf-8'))
coverage.update({'registered_entries':len(records),'entry_types':counts,'encoded_strategy_variants':len(rules['strategies']),'platform_active_strategies':0,'findings_retained':len(claims),'gap_workstreams_retained':len(gaps),'sections_with_named_item_links':sum(bool(v) for v in mapped.values()),'sections_requiring_full_semantic_review':len(sections),'original_markdown_blobs_verified':len(list((ROOT/'documents').glob('*.md'))),'counts_are_not_unique_executable_strategy_totals':True,'migration_status':'paused_by_user','workers_restarted':False})
writejson('SOURCE_COVERAGE.json',coverage)
writejson('PAPER_UNIVERSE.json',{'schema':'markets-paper-universe/1','mode':'paper','execution_enabled':False,'instrument':{'product':'NG','contract_month':'2026-12','symbol_hint':'NGZ6'},'candidate_ids':[r['id'] for r in records],'all_retained_source_hypotheses_in_scope':True,'performance_based_exclusions':[],'unmapped_sections':'SECTION_CROSSWALK.jsonl.gz','semantic_reconciliation_complete':False,'runtime_rules_snapshot':'prior/reanalysis-20261109/TRADE_RULES.json','instruction':'This is a complete-preservation manifest with an initial named-candidate register, not a native platform import. Implement remaining definitions without filtering weak or adverse candidates out of paper scope.'})

assert len({r['id'] for r in records})==len(records)
assert all(r['paper_included'] and not r['platform_active'] for r in records)
assert len(crosswalk)==len(sections)==6400
assert len({c['section_id'] for c in crosswalk})==6400
assert all(s.get('section_id') in {x['section_id'] for x in sections} for r in records for s in r['sources'] if s.get('section_id'))
assert not rules['execution_enabled'] and len(rules['strategies'])==11
print(json.dumps(coverage,indent=2))
