"""Build additive research maps from frozen prior specifications and audited fields."""
import json
from pathlib import Path
from audit import OUT, dump, write_csv

ROOT = OUT.parent
BINDINGS = {
 'B01': dict(name='Full depth and counts', fields=['L039','L040'],
    operands=['before/during.bid_full_size','before/during.ask_full_size','before/during.bid_full_orders','before/during.ask_full_orders'],
    events=['groups-*.parquet'], clock='L029.values.before.known_by_ns for before; values.during_known_by_ns for during; source group known_by_ns for complete replay',
    availability='Original per-trade joins exist; complete non-trade groups are located, not reconstructed in this pass.', dependency='D01'),
 'B02': dict(name='Quotes and touch liquidity', fields=['L045','L052','L054','L040'],
    operands=['bid_price_raw','ask_price_raw','bid_size','ask_size','bid_orders','ask_orders'], events=['groups-*.parquet'],
    clock='Complete group known_by_ns; use group_ordinal/cursor for strict later-group confirmation, including tied nanoseconds.',
    availability='Original before/during values; L054 repeats L052 prices and L045 overlaps both.', dependency='D01'),
 'B03': dict(name='Fresh, expired and rolling native flow', fields=['L048','L055','L056','L059'],
    operands=['aggressor_side','size','trade_input_cursor','available_ns','incoming_buy/sell','expired_buy/sell','window_buy/sell'],
    events=['trades.parquet','actions-*.parquet','groups-*.parquet','native-flow-source-clocks.parquet'],
    clock='Trade available_ns/group known_by_ns governs admission; (t-W,t] membership uses explicitly registered source time axis; expiry timer processing gets its own decision clock.',
    availability='L048 is individual trade operands only. L055/L056/L059 are missing in the grid. Native completed-second ratio/roll operands are separate contextual columns; they are not arbitrary fast/slow windows.', dependency='D02'),
 'B04': dict(name='Cancellation attribution', fields=['L031','L032','L047','L049'],
    operands=['action','order_id','before_side','before_price','before_size','after_side','after_price','after_size','fill_linked_reduction','old/new_touch_effect_json'],
    events=['actions-*.parquet','groups-*.parquet'], clock='Action known_by_ns and group_close_cursor; classify touch against registered before/after quote context.',
    availability='L047/L049 have aggregate touch effects; unlinked removal is not proof of cancellation. Raw action columns are located; action taxonomy and attribution still require verification.', dependency='D03'),
 'B05': dict(name='Tracked order survival and refill', fields=['L030','L031','L032','L033','L034','L035','L036','L037','L041','L042','L043','L044','L049'],
    operands=['order_id','action','before/after side/price/size','fill_linked_reduction','fill_unchanged_display','first_cursor','close_cursor'],
    events=['actions-*.parquet','groups-*.parquet','source-receipt.json'], clock='Only order state available at current completed group; never join future survival or final fate into setup.',
    availability='Grid aggregates cannot establish exact order identity, FIFO or seed lineage. Source action ledger exists; bootstrap/reset-aware order replay is unresolved.', dependency='D04'),
 'B06': dict(name='Native morphology and its publication clock', fields=['L056','L058','L059','L064','L066'],
    operands=['context.Native dipole ratio at latest completed second','context.Native roll buy/sell','second_rows.native_buy/native_sell','completed_second_known_by_ns','completion_group','completion_cursor'],
    events=['native-flow-source-clocks.parquet','sample-clock-pins.npz'], clock='completed_second_known_by_ns, not label_ns or sample_cut_ns; repeated tick attachments are not new ratio updates.',
    availability='Contextual native series preserved. Named L layers are unavailable; alternative learned-window constructions must get separate version IDs and must not rewrite the archived native ratio.', dependency='D05'),
 'B07': dict(name='Causal recognition', fields=['L076','L029','L075'],
    operands=['life.recognition_ns','life.recognition_clocks.group','life.recognition_clocks.close_cursor','life.recognition_clocks.known_by_ns'],
    events=['whole-lifecycles.parquet','a-dipole-clocks.parquet'], clock='Actual recognition_ns; birth label is retrospective; final end cannot arm or time a live entry.',
    availability='Exact case recognition clocks exist although L076 cells are missing; prior result places recognition after leg end in 25/32 cases.', dependency='D06'),
 'B08': dict(name='State-masked S measurements', fields=[f'S{i:02}' for i in range(1,20)],
    operands=['previous_input','at_trade_input','at_emission_group_close','last_completed_group_before_trade','raw_float64','state_code','state'],
    events=['joined-inputs-*.parquet','compact feature projection (upstream source still to bind)'],
    clock='Map emission close to L029.during.known_by_ns and last-completed to L029.before.known_by_ns; previous_input needs its precise input cursor/clock. State and producer semantics must also be verified.',
    availability='Only Oct18 has these payloads; at_trade_input is missing throughout. PRESENT/state_code=0 is necessary but does not by itself prove live availability.', dependency='D07'),
 'B09': dict(name='External context and publication state', fields=[f'X{i:02}' for i in range(1,14)],
    operands=['series[].original.state','series[].original.value','series[].original.published_ns','series[].original.row.event_time_ns','asof_receive_ns','publication_confidence'],
    events=['joined-inputs-*.parquet','external publication stores referenced by original payload'],
    clock='Declared published_ns <= asof_receive_ns; keep release time, underlying observation time and actual receiver delivery separately.',
    availability='Mixture of published, static and missing values. Some publication timestamps are derived; X13 includes price-derived curve operands. Not independent directional confirmation.', dependency='D08'),
 'B10': dict(name='Information-model inputs and frozen legacy models', fields=['L039','L040','L045','L048','L058','L059','L064','L066'],
    operands=['prior price/range','early/late/fresh buy and sell','entropy','MI','C','flow-change','original M0/M1 coefficient/transform definitions'],
    events=['TRADE_RULES.json.models','prior model input generation and source event tapes'],
    clock='Each component must carry max(input known_by); preprocessing and model training cutoffs precede validation. Frozen R7/R8 remain archived; learned-window forks receive new model IDs.',
    availability='Frozen models retained in prior rules; 141-field grid does not supply all original model features. No predictions generated here.', dependency='D09'),
 'B11': dict(name='Integrity, source identity and session continuity', fields=['L024','L025','L026','L027','L028','L029','L038','L046','L053','L072','L073','L074','L075'],
    operands=['day','trade_ordinal','trade_id','trade_cursor','event_ns','receive_ns','known_by_ns','source_trade_revision','source_trade_path','coverage','snapshot_member','reset_member','bad_receive_clock_member'],
    events=['joined-inputs-*.parquet','source-receipt.json','groups-*.parquet','actions-*.parquet'],
    clock='Exact integer nanoseconds plus cursor order. Decisions cannot precede any required operand known_by or complete-group close.',
    availability='Metadata and before/during integrity flags exist; snapshot/continuity proof must cover all relevant events, not only trade attachments.', dependency='D01'),
 'B12': dict(name='Order submission, fills and costs', fields=[],
    operands=['decision_ns','submit_ns','ack_ns','fill_ns','fill_price','fill_size','no_fill_reason','fees','slippage','latency'],
    events=['future paper adapter execution reports'], clock='decision <= submission <= observed fill; receipt and source event clocks retained independently.',
    availability='No new strategy execution reports exist. Instrument identity, fees and adapter remain unresolved. No simulated midpoint fills claimed.', dependency='D10')
}

DEPENDENCIES = {
 'D01': ('Continuous complete-group book join','Verify source continuity/reset handling and join every event group, including groups without prints. Preserve ties and original cursors. Validate before/during agreement against source.', 'B01/B02/B11'),
 'D02': ('Learned native-flow histories','Reconstruct per-side arrivals and expiry from complete admitted trades. Learn fast/slow/quiet windows by strategy and stage; log source event time and availability time separately. Preserve unknown side, known-empty and balanced states.', 'B03'),
 'D03': ('Cancellation scope and mechanism','Link actual action semantics to full-book, old-touch, new-touch and near/far scope; distinguish fill-linked reductions, cancels, reprices, reset and unknown removals. Preserve each scope as a separate branch.', 'B04'),
 'D04': ('Order identity and lineage','Bootstrap order ledger; track seed, partial fill, residual, refill, reprice and cancellation across complete groups; scope IDs to contract/session/reset segment.', 'B05'),
 'D05': ('Morphology and learned observation scale','Use each distinct completed update once for pattern state while retaining every tick attachment. Learn update-count and elapsed-time definitions separately; freeze their definitions and keep original native series.', 'B06'),
 'D06': ('Recognition cohort join','Verify recognition group and quotes for all candidates, not only selected cases; retain missing/late recognition and never substitute birth. Learn delays and observation-lateness handling.', 'B07'),
 'D07': ('S producer/state/clock mapping','Bind compact feature producer, units, lookbacks and exact input cursors; state-mask each slot independently. Recover other dates if possible without inventing observations.', 'B08'),
 'D08': ('External release and delivery proof','Verify declared publication against source receipt/vintage, actual availability, revisions and contract mapping. Keep static levels and between-day shifts distinct from within-window changes.', 'B09'),
 'D09': ('Model input parity','Reproduce original feature transformations and frozen M0/M1 parity before comparative use; new learned horizons require separate refit/version and untouched validation.', 'B10'),
 'D10': ('Paper execution contract','Bind exact contract, executable quote/order model, latency and fees. Log all setups and no-fill/paused/capped states without deleting opportunities. No new adapter activated.', 'B12'),
 'D11': ('Horizon discovery and validation','Follow HORIZON_RESEARCH.md: use complete development streams, event/time axes, nested temporal validation and untouched sessions. Do not optimize on these outcome-selected cases or report a universal winning horizon.', 'all learned-window strategies')
}

# These are evidence requirements, not executable rules or exclusion filters.
REQUIREMENTS = {
 'C1':(['B01','B02','B03'],['B04','B06'],['D01','D02']),
 'C2':(['B01','B02','B03'],['B04','B06'],['D01','D02']),
 'C3':(['B02','B03','B05'],['B01','B04','B08'],['D01','D02','D04']),
 'C4':(['B01','B02','B03'],['B04','B05','B06'],['D01','D02']),
 'C5':(['B02','B03','B11'],['B01','B04','B06'],['D01','D02']),
 'C6':(['B01','B02','B03'],['B04','B06'],['D01','D02']),
 'C7':(['B02','B07'],['B01','B03','B04','B06'],['D01','D06']),
 'C8':(['B02','B07'],['B01','B03','B04','B06'],['D01','D06']),
 'C9':(['B02','B03','B04'],['B01','B06'],['D01','D02','D03']),
 'C10':(['B02','B03','B04'],['B01','B06'],['D01','D02','D03']),
 'C11':(['B02','B03'],['B01','B04','B06'],['D01','D02']),
 'C12':(['B02','B04','B05'],['B01','B03'],['D01','D03','D04']),
 'C13':(['B02','B03','B06'],['B01','B04','B08','B10'],['D01','D02','D05']),
 'C14':(['B02','B03'],['B01','B04','B06','B10'],['D01','D02']),
 'C15':(['B02','B03'],['B01','B04','B06','B08','B10'],['D01','D02'])
}

ADDITIONS = [
 ('H16','Flow-to-price response delay', ['B02','B03','B04'],
  'Does fresh flow transmit to both quotes at different delays depending on refill/cancellation state?',
  'Keep every arrival, no-response, delayed-response and adverse-response episode. Estimate elapsed-time and complete-group response distributions, censored at known observation end. Use as timing/management information without assuming direction.'),
 ('H17','Displayed size versus order-count divergence', ['B01','B02','B05'],
  'Do falling lots with rising order counts, or the converse, distinguish fragmentation, resistance and later quote movement?',
  'Keep all four change-sign combinations and exact zero changes. Treat the ratio as optional derived context, with separate raw operands; resolve identities before attributing fragmentation to a mechanism.'),
 ('H18','Liquidity withdrawal and return', ['B02','B04','B05'],
  'Does the time and event count from actual cancellation to same-price liquidity return distinguish continuation from failed release?',
  'Track same-order versus replacement-order return and original versus new touch. Retain absent return and unresolved identity. Learn time scales; never use eventual refill to classify a live setup.'),
 ('H19','Trade-print movement versus quote movement', ['B02','B03'],
  'Can print-side alternation explain small/brief moves while quote relocation marks a different state?',
  'Preserve every print and bid/ask path. Record previous-price returns, same-side prints, spread changes and both-quote relocation separately across all types. This is an additional explanatory and management branch, never a rule for removing bounce-like cases.'),
 ('H20','Information-state context and lifecycle age', ['B06','B08','B10'],
  'Do separately observed age, survival, replenishment and information inputs distinguish stalls, renewed activity or management needs?',
  'Keep all 19 S fields and each state slot; do not make available-on-Oct18 observations a four-day claim. Missing and zero-MI states remain visible. Source-clock and producer dependencies precede any live use.'),
 ('H21','External vintage and market-state interaction', ['B01','B02','B03','B09'],
  'Do publication-vintage context and contract curve state change the interpretation of local flow/liquidity response?',
  'Preserve all 13 X fields, revisions and original states. Four selected days cannot isolate a day-level external effect; expand independent sessions before fitting. Separate price-derived curve context from independent external observations.')
]


def main():
    saved = json.loads((ROOT/'fifteen-strategies-20261113/STRATEGIES_15.json').read_text())
    legacy = json.loads((ROOT/'reanalysis-20261109/TRADE_RULES.json').read_text())
    original = json.loads((ROOT/'fifteen-strategies-20261113/ORIGINAL_FIVE.json').read_text())
    fields = json.loads((OUT/'field_inventory.json').read_text())
    names = {x['field'].split(' | ')[0]: x['field'] for x in fields}
    for key, b in BINDINGS.items():
        b['id'] = key
        b['exact_grid_fields'] = [names[f] for f in b['fields']]
    strategies = []
    for s in saved['strategies']:
        req, context, deps = REQUIREMENTS[s['id']]
        strategies.append({'id':s['id'], 'name':s['name'], 'retained':True,
            'original_spec': '../fifteen-strategies-20261113/STRATEGIES_15.json#'+s['id'],
            'prior_evidence': s['evidence'], 'prior_sources': s['sources'],
            'required_bindings':req+['B11','B12'], 'context_bindings':context,
            'required_fields':sorted({f for bid in req+['B11'] for f in BINDINGS[bid]['exact_grid_fields']}),
            'unresolved_dependencies':sorted(set(deps+['D10','D11'])),
            'context_dependencies':sorted({BINDINGS[b]['dependency'] for b in context}),
            'decision_clock':'max(required input known_by_ns, complete_group.known_by_ns); later confirmations require later group identity/cursor, not only a larger timestamp',
            'horizon_policy':'Original constants archived only. New variants learn W_fast, W_slow, W_book, W_quiet, confirmation/observation and management horizons where applicable; none has a fixed 5s/60s default.',
            'execution_status':'not implemented or executed; source/evidence map only'})
    oldmap = {'R1':['B02','B03'],'R2':['B02','B03','B05'],'R3':['B02','B03'],
              'R4':['B02','B07'],'R5':['B02','B07'],'R6A':['B02','B03','B04'],
              'R6B':['B02','B03','B04'],'R7':['B02','B03','B07','B10'],
              'R8':['B02','B03','B07','B10'],'R9':['B02','B03'],'R10':['B02','B04','B05']}
    legacy_maps = [{'id':s['id'], 'original_spec':'../reanalysis-20261109/TRADE_RULES.json#'+s['id'],
        'required_bindings':oldmap[s['id']]+['B11','B12'], 'retained':True,
        'dependencies': sorted({BINDINGS[b]['dependency'] for b in oldmap[s['id']]}|{'D10'}),
        'clock':'complete group and per-binding clocks; R7/R8 feature provenance and training cutoff also required',
        'status':'historical specification preserved verbatim; archived constants are baselines, not defaults for new variants'} for s in legacy['strategies']]
    original_maps = []
    for s in original['strategies']:
        sid = s['id']
        original_maps.append({'id':'original-'+sid, 'original_spec':'../fifteen-strategies-20261113/ORIGINAL_FIVE.json#'+sid,
            'required_bindings': REQUIREMENTS[sid][0]+['B11','B12'], 'retained':True,
            'dependencies':REQUIREMENTS[sid][2]+['D10','D11'],
            'difference_warning':'Original C4 upward-failure evidence and original C5 delayed-confirmation rule remain separate from revised mirrored C4/immediate C5; do not overwrite earlier definitions.'})
    additions = [dict(id=i, name=n, question=q, research_protocol=p, required_bindings=b,
        dependencies=sorted({BINDINGS[x]['dependency'] for x in b}|{'D11'}),
        retained=True, origin='independent Codex availability continuation',
        status='new additive research hypothesis; no fitted rule or execution') for i,n,b,q,p in ADDITIONS]
    for f in fields:
        code = f['field'].split(' | ')[0]
        f['bindings'] = [b for b,v in BINDINGS.items() if code in v['fields'] or f['field'] in v['operands']]
        f['strategies_requiring_or_contextualizing'] = [s['id'] for s in strategies if any(b in s['required_bindings']+s['context_bindings'] for b in f['bindings'])]
        if code.startswith('S') and ' | ' in f['field']:
            f['role'] = 'individual second-set feature; inspect each clock slot and producer definition'
        elif code.startswith('X') and ' | ' in f['field']:
            f['role'] = 'external context/vintage/state; not an automatically admitted predictor'
        elif code.startswith('L'):
            n = int(code[1:])
            f['role'] = ('knowledge/provenance/policy context' if n<=23 else
                         'source, book, order or mechanics evidence' if n<=53 else
                         'legacy/derived/prebirth research measurement' if n<=71 else
                         'clock or later-label boundary' if n<=80 else
                         'runtime/retrieval/population/output evidence')
        else:
            f['role'] = 'source identity or clock metadata'
        f['next_action'] = ('Keep missing/static state; locate authoritative source and admission clock before interpretation.'
            if not f['cases_with_numeric_members'] else
            'Inspect member audit per case; apply states and clock contract; distinguish repeated source operands from independent evidence.')
    dump('field_inventory.json', fields)
    dump('strategy_evidence_map.json', {'schema':'codex-evidence-map/1','source_commit':'fe45d2eff9b389e00c80807b6e2240003ba4885d',
        'policy':'All hypotheses retained. No single winner, elimination, tick filtering or execution. Claude new results not consulted.',
        'bindings':BINDINGS,'dependencies':{k:dict(title=v[0],next_action=v[1],binding=v[2]) for k,v in DEPENDENCIES.items()},
        'strategies':strategies,'original_five':original_maps,'legacy_eleven':legacy_maps,'additive_hypotheses':additions})
    applicability = {
        'W_fast':['C1','C2','C3','C5','C6','C9','C10','C11','C13','C14','C15'],
        'W_slow':['C1','C2','C6','C11','C14'],
        'W_book':['C1','C2','C6'], 'W_quiet':['C5'],
        'confirmation_horizon':['C1','C2','C3','C4','C11','C13','C14','C15'],
        'recognition_observation_delay':['C7','C8'], 'observation_lateness':['C7','C8'],
        'morphology_steps':['C13'], 'morphology_elapsed_span':['C13'],
        'pullback_reference':['C15'], 'participation_return_deadline':['C15'],
        'management_persistence':['C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','C11','C12','C13','C14','C15']}
    dump('HORIZON_REGISTRY.json', {'schema':'codex-learned-horizon-research/1',
        'execution_enabled':False, 'fitting_executed':False,
        'policy':'No fallback to 5s, 60s or other archived constants. Learn separately per strategy and observable trade stage. Preserve all variants and unresolved support.',
        'parameters':[{'name':k,'strategies':v,'value':None,'unit':None,
                       'candidate_derivation':None,'training_source_hashes':[],
                       'training_cutoff_ns':None,'validation_sessions':[],
                       'status':'unfitted research parameter'} for k,v in applicability.items()],
        'protocol':'HORIZON_RESEARCH.md',
        'archive_compatibility':'Original specifications and native ratio construction remain unchanged as historical evidence; new learned variants require distinct version IDs.'})
    write_csv('strategy_dependency_edges.csv', [{'strategy':s['id'],'binding':b,'role':role,
        'source_events':' ; '.join(BINDINGS[b]['events']), 'exact_clock':BINDINGS[b]['clock'],
        'fields':' ; '.join(BINDINGS[b]['exact_grid_fields']), 'unresolved_dependency':BINDINGS[b]['dependency']}
        for s in strategies for role in ['required_bindings','context_bindings'] for b in s[role]])
    lines = ['# Evidence and availability map','',
        'All candidates remain retained. This map is not an execution runner. Fixed historical windows remain only in archived specifications; see [Horizon research](HORIZON_RESEARCH.md).','',
        '| Strategy | Required evidence | Context kept separately | Unresolved work |',
        '|---|---|---|---|']
    for s in strategies:
        lines.append(f"| {s['id']} {s['name']} | {', '.join(s['required_bindings'])} | {', '.join(s['context_bindings'])} | {', '.join(s['unresolved_dependencies'])} |")
    lines += ['', '## Operand and clock contracts','']
    for k,b in BINDINGS.items():
        lines += [f"### {k}: {b['name']}", '', '**Fields:** '+(', '.join(b['exact_grid_fields']) or 'Execution-report fields outside the original 141'), '',
                  '**Operands:** '+ '; '.join(b['operands']), '', '**Source events:** '+', '.join(b['events']), '',
                  '**Clock:** '+b['clock'], '', '**Availability:** '+b['availability'], '']
    lines += ['## Every prior arm remains','',
              'Original C1–C5 are archived unchanged, alongside revised C1–C15 and the eleven legacy arms R1–R10 (R6A and R6B separately). The machine-readable map has distinct records for each. No family is replaced by a winner.','',
              '## Additive questions beyond fifteen','']
    for h in additions:
        lines += [f"### {h['id']}: {h['name']}",'',h['question'],'',h['research_protocol'],'',
                  'Evidence: '+', '.join(h['required_bindings'])+'. Dependencies: '+', '.join(h['dependencies'])+'.','']
    (OUT/'EVIDENCE_MAP.md').write_text('\n'.join(lines).rstrip()+'\n', encoding='utf8')
    lines = ['# All 141 fields: retained evidence and availability', '',
        'One row per original field. Case counts describe measurements after state masking, not trading signals or independent evidence. Clocks and identifiers are excluded from numeric-measurement counts. Complete originals remain in raw/; every field/case is in field_case_audit.csv and individual numeric members in numeric_member_audit.csv.', '',
        '| Field | Stored statuses | Cases with numeric members | Cases with varying numeric members | Evidence bindings | Research role |',
        '|---|---|---:|---:|---|---|']
    for f in fields:
        lines.append('| '+f['field'].replace('|','/')+' | '+', '.join(f['statuses'])+' | '+str(f['cases_with_numeric_members'])+' | '+str(f['cases_with_varying_numeric_members'])+' | '+', '.join(f['bindings'])+' | '+f['role']+' |')
    lines += ['', 'Missing layers are retained research dependencies. An empty binding means no current strategy has a verified operand in that field; it is not an exclusion. Exact per-field clock contracts and next actions are in field_inventory.json.']
    (OUT/'ALL_141_FIELDS.md').write_text('\n'.join(lines)+'\n', encoding='utf8')
    print('Mapped 15 revised + 5 original + 11 legacy records; added 6 research hypotheses; retained all 141 fields.')


if __name__ == '__main__':
    main()
