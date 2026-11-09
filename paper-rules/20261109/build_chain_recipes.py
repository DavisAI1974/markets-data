import json
from pathlib import Path

ROOT=Path('C:/Users/A/markets-paper-rules-20261109')
review=json.loads((ROOT/'review_chain.json').read_text())
def ref(alias,lo=None,hi=None):
    s=review['sources'][alias]
    return {'source':alias,'git_blob_sha':s['git_blob_sha'],'url':s['url']+(f'#L{lo}'+(f'-L{hi}' if hi else '') if lo else '')}
def cond(op,*args): return {'op':op,'args':list(args)}
F=lambda name:{'field':name}
C=lambda value:{'const':value}

audit=[
 {'id':'R01','issue':'Identical LONG/SHORT overlays can silently replace source direction or change a direction-dependent source predicate.','fix':'Keep native source-directed arm and source predicate unchanged; add absolute LONG and SHORT execution overlays with design provenance. A duplicate side may share fills computationally but must retain separate hypothesis IDs and source lineage.'},
 {'id':'R02','issue':'Bank-positive management based on overlay PnL changes the source condition when overlay side differs from source polarity.','fix':'Source management uses p_current*(mark_at_anchor+h-mark_at_anchor+5)/tick >0. Own-position-PnL management is a separate labelled design arm. No silent substitution.'},
 {'id':'R03','issue':'All inputs known is not a complete predicate unless every dependency has an actual availability timestamp. Source-day close and endpoint confirmation do not prove frozen detector identity or absence of a preconfirmation successor.','fix':'Use dependency closure and TRUE/FALSE/UNKNOWN logic. UNKNOWN produces retained input-unavailable status. Never treat a missing future link as false. No claimed prospective order until actual event identity/negative-overlap evidence is available.'},
 {'id':'R04','issue':'Fixed-clock NO_ENTRY may be written after retrospective target discovery and incorrectly look like an earlier evaluated decision.','fix':'Record planned source time and actual evaluation/record time separately; if target was not knowable at planned time, emit retrospective no-entry diagnostic with no invented earlier snapshot/order.'},
 {'id':'R05','issue':'Delayed first actual decision might move earlier than source entry or rematch a newer predecessor window.','fix':'scheduled_floor=original anchor+5; ready=max(scheduled_floor, all dependencies known_by); freeze target/predecessor IDs and source clock anchor for that occurrence. Delayed arm evaluates that occurrence, not a later nearest matching event.'},
 {'id':'R06','issue':'A fill-relative25/55s hold is a new execution design, including when it coincides with source holding length. It is not the source fixed absolute exit.','fix':'Keep original anchored exits; identify delayed entry plus fill-relative exit as separate design arms. A missed source exit is not rolled forward silently.'},
 {'id':'R07','issue':'All288pair/triplet modules are syntactic candidate expansion, not proof every one was an observed recurring/source-promoted module. Also they are structural continuation hypotheses without a source trade direction/exit.','fix':'Preserve all32pairs+256triplets under common paper protocol. Label named motifs source-mentioned and remaining grammar cells generated design expansion. Keep structural extension outcomes and LONG/SHORT economic overlays as separate outputs.'},
 {'id':'R08','issue':'Prefix watch events do not have a known future current target or its endpoint.','fix':'Prefix recipe anchors to final prefix member maturity/known_by; never use later completed-chain identity to start the watch or trade. Watch completion is an outcome. Prefix execution timing is new design.'},
 {'id':'R09','issue':'Posthoc exact depth, terminal duration, CHOP_ROTATION, timing mixture class or eventual FLIP/SAME could enter early predicates via cohort selection.','fix':'Execution candidate discovery must not filter by these outcomes. Keep them only in retrospective report joins. Explicit causal forecast operands can gate separate forecast hypotheses when model/version/known_by are bound.'},
 {'id':'R10','issue':'Historical tape ends and canonical next-stage boundaries are retrospective; exiting at last observed trade beforehand uses future knowledge.','fix':'Use causal scheduled/observed exit requests. If tape ends before fill or exit, retain censored/no-fill/open-unmarked outcome. Do not force a mark at retrospectively selected last trade and call it an executable exit.'},
 {'id':'R11','issue':'Uniformity can collapse hypotheses with distinct populations or omit nonexecution states.','fix':'Keep canonical679, fixed-focused3429, exact-depth label cohorts, and all candidate events separate. Share execution/reporting protocol, not population redefinition. Every row retains adverse/flat/unknown/censored/late/no-fill/rejected outcomes, with no performance admission.'}
]

availability={
 'operand_schema':{'value':'typed or null','known_by':'actual observation/derivation timestamp or null','source_ids':'all raw/model/transform dependencies','semantic_kind':['causal_observation','causal_forecast','posthoc_outcome','oracle_cohort']},
 'three_valued_logic':{'AND':'FALSE if any operand FALSE; TRUE if all TRUE; otherwise UNKNOWN','UNKNOWN':'retained INPUT_UNAVAILABLE; never coerce to false or zero','known_by':'derived value cannot precede max(all lawful dependency times) including identity, model evaluation and transform completion'},
 'decision_predicate_forbidden':['actual_final_depth','actual_final_duration','actual_chain_terminal_id','realized_path_shape','realized_timing_family','first_correct','first_durable_correct','future_target_exists','future_target_t0','focused_pox_future_flip_same'],
 'allowed_forecast_substitutes':'Explicit forecast names with causal snapshot hash, immutable prediction timestamp, model/head/view/version and declared probability decision condition; NEVER alias true labels into forecast fields.',
 'canonical_event_identity':'Actual frozen-detector identity_available_at, not t0 or endpoint confirmation. Remains unresolved absent proof. Full-day threshold closure is necessary but not sufficient to establish global prominence/refractory selection.',
 'negative_overlap':'Source asks no next canonical event starts at or before current confirmation. Live absence requires actual lawful negative evidence; a null next_event link is not proof. If unproved, original source arm is UNKNOWN. A causal streaming-detector no-observed-successor arm is separate changed-detector design.',
 'seed':'max(event identity known_by, t0+60, every contributing observed input/transform known_by); predecessor seed-state S is not same-polarity S.',
 'source_history_wall':'predecessor endpoint_confirmation+60<=current t0 is source eligibility comparison. Actual history feature availability additionally must be <=actual decision. For original fixed-clock arm, all used inputs must be available at planned entry.',
 'frozen_history_feature_cells':'signed displacement,MFE,MAE at predecessor confirmation+[5,10,20,30,60], finite/uncensored and predecessor next_same_polarity known. This belongs to frozen source arm; do not replace by merely t0+60 seed maturity.'
}

clock_axes={
 'anchor':[
  {'id':'DOC_ONSET','value':'target.structural_endpoint_onset','provenance':'documented source rule','sources':[ref('ssos_freeze'),ref('phase2')]},
  {'id':'PRODUCER_CONFIRM','value':'target.structural_endpoint_confirmation','provenance':'original producer observed semantics; separate from documented rule','sources':[ref('canonical',277,305),ref('canonical',390),ref('ssos_producer',84,114)]}
 ],
 'entry_exit':[
  {'id':'SOURCE_FIXED','entry_request':'anchor+5s','entry_semantics':'Evaluate as-of source planned entry only if event and every predicate operand were actually available then. Request execution at that clock. A later diagnostic may explain absence, never create an earlier trade.','exit_request':'anchor+exit_offset_s','late_or_unavailable':'NO_ENTRY_LATE_IDENTITY or INPUT_UNAVAILABLE retained; never delayed automatically','fill_after_exit':'EXPIRED_BEFORE_FILL retained; do not open after exit request','provenance':'source planned clocks; venue fill handling is common paper-design policy'},
  {'id':'DELAYED_AFTER_KNOWN_FILL_HOLD','entry_request':'first_actual_platform_decision_at_or_after(max(anchor+5s, all predicate operand known_by, all event/polarity/identity known_by))','exit_request':'actual_entry_fill_at+(exit_offset_s-5)s','target_window':'immutable target/predecessor occurrence IDs from source candidate','provenance':'new paper-design: preserve source predicate, delay until lawful, then 25/55-second fill-relative hold','no_expiry_from_performance_or_realized_life':True}
 ],
 'source_binding_warning':'If an original source variant has insufficient identity proof for the entry, retaining NO_ENTRY is required; changing its detector to force fills would be a different design.',
 'side':[
  {'id':'SOURCE_DIRECTED','expression':'source_orientation*target.polarity','availability':'Require recovered source_orientation; UNKNOWN_SOURCE_DIRECTION if absent. Do not estimate sign from evaluation returns.','provenance':'original source map, unless explicitly not specified'},
  {'id':'LONG_OVERLAY','expression':1,'provenance':'new shared paper-design execution overlay; source trigger unchanged'},
  {'id':'SHORT_OVERLAY','expression':-1,'provenance':'new shared paper-design execution overlay; source trigger unchanged'}
 ]
}

seed_match=cond('and',
 cond('eq',F('ordered_immediate_predecessors.seed_codes'),F('params.seed_string')),
 cond('or',cond('eq',F('params.relation'),'UNSPLIT'),cond('eq',F('current_vs_latest_predecessor_polarity_relation'),F('params.relation'))),
 cond('all',F('ordered_immediate_predecessors'),cond('and',cond('lte',cond('add_seconds',F('item.endpoint_confirmation'),C(60)),F('target.t0')),cond('eq',F('item.source_h60_history_complete'),C(True)))),
 cond('lte',F('target.endpoint_confirmation'),cond('add_seconds',F('target.endpoint_onset'),C(5))),
 cond('eq',F('causally_established_successor_start_le_confirmation'),C(False)))

recipes=[]
recipes.append({
 'id':'CHAIN_EXACT_SOURCE_SEARCH','source_family':'exact D2-D4 predecessor seed search','generate':{'seed_alphabet':['P','O','S','X'],'seed_lengths':[2,3,4],'order':'oldest_to_newest','relation':['UNSPLIT','SAME','FLIP'],'exit_offset_s':[30,60],'clock_anchor':['DOC_ONSET','PRODUCER_CONFIRM'],'timing':['SOURCE_FIXED','DELAYED_AFTER_KNOWN_FILL_HOLD'],'execution_side':['SOURCE_DIRECTED','LONG_OVERLAY','SHORT_OVERLAY']},
 'base_condition_cell_count':2016,'count_note':'336strings*3relations*2exits=2016 before clocks/timing/sides; each generated cell has a row even with zero observations.',
 'predicate':seed_match,'known_by_dependencies':['each predecessor identity/seed/polarity','each source h60 history cell','current identity/polarity','endpoint onset confirmation','lawful overlap/negative-overlap evidence'],'direction_map':review['explicit_maps']['recurrence']['causal_predecessor_motifs'],'unspecified_source_direction':'Retain SOURCE_DIRECTED as unresolved; LONG/SHORT overlays remain concrete new designs. The source family did not give all generated cells one fixed side.','sources':[ref('phase2'),ref('ssos_producer',53,114),ref('recurrence_producer',100,116)],
 'source_vs_design':'Alphabet/order/depth/optional relation/exits are source family. Universal LONG/SHORT and delayed fill-hold are new designs. Do not pretend every generated string had a source-selected sign.'})
recipes.append({
 'id':'CHAIN_ATLAS_DEPTH1_TO4','generate':{'seed_alphabet':['P','O','S','X'],'seed_lengths':[1,2,3,4],'relation':['SAME','FLIP'],'exit_offset_s':[60],'clock_anchor':['DOC_ONSET','PRODUCER_CONFIRM'],'timing':['SOURCE_FIXED','DELAYED_AFTER_KNOWN_FILL_HOLD'],'execution_side':['SOURCE_DIRECTED','LONG_OVERLAY','SHORT_OVERLAY']},
 'base_condition_cell_count':680,'predicate':seed_match,'deduplication':'Shared computation allowed, but references to overlapping exact-search cells retained. Do not count the same economic fill twice in an aggregate portfolio merely because two source lists name it; independent hypothesis results remain separate.','source_filters_not_admission':['minimum supports20/12/6','topN presentation lists','positive mean','novelty overlap exclusion'],'sources':[ref('recurrence_producer',100,116),ref('novelty'),ref('postexit')]})
recipes.append({
 'id':'FROZEN_SSOS','parameters':{'seed_string':'SSOS','relation':'UNSPLIT','exit_offset_s':30,'source_orientation':1},'predicate':seed_match,'axes':'all clock_anchor, timing and execution_side axes above; native DOC_ONSET/SOURCE_FIXED/SOURCE_DIRECTED remains identifiable as documented frozen play','not_a_depth_label':'Four immediate predecessor seeds, never predicate exact_D4.','sources':[ref('ssos_freeze'),ref('ssos_producer',20,114)]})
recipes.append({
 'id':'CANONICAL_POX_PARENT','parameters':{'seed_string':'POX','exit_offset_s':60,'source_orientation':1},'generate':{'relation':['UNSPLIT','SAME','FLIP'],'absolute_current_polarity':['ALL','UP','DOWN'],'clock_anchor':['DOC_ONSET','PRODUCER_CONFIRM'],'timing':['SOURCE_FIXED','DELAYED_AFTER_KNOWN_FILL_HOLD'],'execution_side':['SOURCE_DIRECTED','LONG_OVERLAY','SHORT_OVERLAY']},'predicate':cond('and',seed_match,cond('polarity_in_named_stratum',F('target.polarity'),F('params.absolute_current_polarity'))),'population':'canonical679 source population is evidence ledger, not replacement for focused3429; prospective candidate generation uses canonical-sequence semantics with lawful identity','sources':[ref('pox_branches'),ref('pox_correction')]})
recipes.append({
 'id':'POX_BANK_POSITIVE_PROXY','inherits':'CANONICAL_POX_PARENT','generate':{'bank_offset_s':[10,30],'management_basis':['SOURCE_ORIENTED_REFERENCE_RETURN','OVERLAY_EXECUTED_PNL_DESIGN']},
 'native_fixed_clock_request':'At anchor+bank_offset_s evaluate condition; if TRUE request exit, else maintain normal anchor+60 exit. UNKNOWN -> retain MANAGEMENT_INPUT_UNAVAILABLE and preserve already-specified normal exit; never retroactively substitute a mark.',
 'source_condition':cond('gt',F('target.polarity*(source_mark_price[anchor+bank_offset_s]-source_mark_price[anchor+5s])/tick_size'),C(0)),
 'design_condition':cond('gt',F('execution_side*(causal_mark_now-actual_fill_price)/tick_size'),C(0)),
 'delayed_counterpart':'New paper-design applies banking check at fill+(bank_offset_s-5)s, default exit fill+55s. Source-oriented reference-return basis at fill-relative time is also a design reinterpretation and must not be labelled original fixed-checkpoint proxy.',
 'late_source_checkpoint':'If delayed entry occurs after original source bank time, do not apply a pre-entry profit measurement to the newly opened position as if earned by it. Either source checkpoint is INAPPLICABLE_ALREADY_PASSED or use separately labelled fill-relative proxy.',
 'sources':[ref('management_proxy')]})
recipes.append({
 'id':'POX_POSTEXIT_RECOVERY','inherits':'CANONICAL_POX_PARENT relation=SAME','predicate_for_postexit_annotation':cond('lt',F('source_oriented_R60'),C(0)),
 'classes':{'shallow30':cond('gte',F('R30'),C(-1)),'deep30':cond('lte',F('R30'),C(-2)),'shallow60':cond('eq',F('R60'),C(-1)),'deep60':cond('lte',F('R60'),C(-2))},
 'cartesian_cells':['shallow30/shallow60','shallow30/deep60','deep30/shallow60','deep30/deep60','other_or_unknown'],'recovered_outcome':cond('or',cond('gte',F('R120'),C(0)),cond('gte',F('R300'),C(0))),'relapse_outcome':cond('and',cond('gte',F('R120'),C(0)),cond('lt',F('R300'),C(0))),
 'no_backdating':'R30/R60 path class becomes known at completed exit; R120/R300 never enter the earlier parent decision. Labels computed separately under each source anchor, not merged.',
 'execution_overlay_design':'After parent flat and R30/R60 class actually known, optional LONG/SHORT recovery-test positions may enter at first decision after max(flat_confirmed_at,path_class_known_by), with25/55s fill-relative hold as explicit new design. Keep ALL four classes and other/unknown as outcomes; do not select only shallow. Native source role remains watch, not entry.',
 'sources':[ref('recovery')]})

recipes.append({
 'id':'PAIR_TRIPLET_MODULES','generate':{'seed_alphabet':['P','O','S','X'],'seed_lengths':[2,3],'relative_polarity_alphabet':['S','F'],'relative_polarity_length':'seed_length-1','absolute_first_polarity':['ALL','UP','DOWN']},'unique_structural_modules':288,'count_note':'32pairs+256triplets before optional absolute polarity strata or economic overlays; no permutation invariance.',
 'predicate':cond('and',cond('eq',F('ordered_members.seed_codes'),F('params.seed_string')),cond('eq',F('adjacent_member_polarity_relations'),F('params.relation_string'))),
 'asof_membership':'Ordered consecutive known canonical members; first source-recognizable match requires all module seeds, identities and relative polarities available. Use no strict-D2+ future filter in live matching.',
 'source_structural_reporting':['recurrence across strict all-model-positive source lineages','D1->D2 extension','D2->D3 extension','timing-family/context decomposition'],
 'posthoc_only':['strict_lineage_membership','eventual_extension_success','actual_final_depth','realized_timing_family'],
 'trade_overlay':{'sides':['LONG','SHORT'],'source_directed':'UNSPECIFIED_FOR_GENERAL_MODULE_EXTENSION; source-directed side only if explicit motif map independently supplies it','entry':'first actual decision after all member dependency known_by times','exit':'actual fill+25s or55s','provenance':'new paper-design economic overlay on structural module; no source trade exit was prescribed'},
 'source_named_modules':review['explicit_maps']['recurrence']['pair_modules']+review['explicit_maps']['recurrence']['triplet_modules'],'remaining_generated_modules':'symmetrical grammar expansion, retained with explicit design provenance; do not label all as empirically recurring','sources':[ref('postexit'),ref('recurrence_producer',36,85)]})
recipes.append({
 'id':'PREFIX_LADDERS','generate':{'family_prefixes':{'SSOS':['S','SS','SSO','SSOS'],'POX':['P','PO','POX']}},
 'predicate':cond('eq',F('latest_k_known_consecutive_seed_codes'),F('params.prefix')),'dependencies':'every prefix member identity, seed and polarity; no future completed target needed','watch_anchor':'max(all prefix member dependency known_by)','completion_outcome':'Later next compatible state/current event completes target pattern after anchor; observed failure, replacement, weekly censoring and no completion all retained.','source_roles':review['explicit_maps']['pox']['source_prefix_roles'],
 'trade_overlay':{'sides':['LONG','SHORT'],'source_directed':'source watch has no trade side; do not borrow a future target polarity','entry':'first actual decision at/after watch_anchor','exit':'fill+25s or55s','provenance':'new paper-design; original prefix remains watch-state candidate'},'sources':[ref('watch')]})
recipes.append({
 'id':'D0_D5_CONTINUOUS_CAUSAL_FORECAST','stage_targets':[0,1,2,3,4,5],'candidate_generation':'All causally discovered candidate/predecessor occurrences; NEVER prefilter by eventual exact depth. Preserve exact-D0 and censored controls.','live_predicate':cond('and',cond('eq',F('forecast.state'),F('params.target_state')),cond('passes_frozen_lock_rule',F('forecast'),F('params.lock_rule_id'))),
 'required_forecast_binding':['model/head/view hash','feature provider revision','asof snapshot hash','prediction_evaluated_at','actual decision_available_at','immutable lock-rule revision and exact thresholds','training chronology/reveal discipline'],
 'clock':'Evaluate every causal second; freeze first lock. PRIOR/T0/H assigned after scoring using canonical target t0. Old finite grids retained as comparison history, not current V4 signal search.','side_overlays':['LONG','SHORT'],'entry':'first actual decision after sealed first-lock signal is available','exit_design':'fill+25s or55s for common economic overlays; independently preserve any exact source-defined exits if recovered','no_source_threshold_invention':'Lock thresholds/model parameters absent in reviewed proposals. Without binding, retain UNBOUND_FORECAST/NO_ENTRY and every outcome row. Do not substitute realized label or retrospectively first-correct second.',
 'depth_and_shape_reporting':review['explicit_maps']['depth_and_timing']['retrospective_definition'],
 'path_class_targets':['DIRECTIONAL','CHOP_ROTATION'],'timing_family_targets':'Frozen GMM model classes only; means are not nearest-center rules. Posthoc GMM labels do not enter live predicate; separate causal forecast required.','sources':[ref('continuous'),ref('v4'),ref('lineage',120,155),ref('d1_rawpath',31,68)]})
recipes.append({
 'id':'FOCUSED_POX_FIXED3429','population':'Authoritative master ledger exactly3429, futureFLIP1546/SAME1883; never enumerate canonicalPOX adjacency as substitute.','live_candidate_gate':'Needs independently defined honest candidate universe and causal membership forecast or actual lawful identity; master future case IDs alone are oracle cohort, not signal.','phases':['initial_continuation','later_predicted_or_revealed_branch','postexit_delayed_reexpression'],
 'future_branch_handling':'FLIP/SAME truth only scoring until actual label_revealed_at. Early branch-conditioned execution requires causal forecast with immutable model/lock; no backdating.','execution_overlays':'Same LONG/SHORT mechanism, held duration designs and reporting as all hypotheses; lack of lawful input yields retained INPUT_UNAVAILABLE rather than deletion.','unknown_binding':['master case join','candidate/control definition','causal identity model','branch reveal timestamps','source exact initial/branch order math'],'sources':[ref('focused_pox'),ref('v4')]})

report={
 'artifact_under_review':'Parent-proposed translation summary; no compiler code or actual executable platform artifacts were supplied for this review.','verdict':'Viable as explicit source-preserving paper design after listed corrections; not evidence of operational integration or recovered model parameters.','audit_findings':audit,'operand_and_clock_contract':availability,'common_axes':clock_axes,'recipes':recipes,
 'shared_execution_protocol':{
  'scope':'PAPER only; independent virtual ledger per hypothesis/version/clock/timing/side arm; same fill/cost/rejection/report schema for every arm',
  'signal_id':'hash(source family + version + canonical or causal occurrence IDs + predicate revision + clock variant + timing variant + side arm + parameter tuple)',
  'duplicate_policy':'At most one entry per signal_id; overlapping source candidates remain separate hypotheses. Any aggregate portfolio exposure/dedup policy is separate from per-arm reporting and must not silently delete cases.',
  'fill_ordering':'Use actual observed event/receive/sequence order. Do not sort within-second trades by price, backfill a predecision price, or reinterpret source carried marks as broker fills.',
  'symbol_tick':'Resolve instrument identity and source tick=0.001 for original NG price math; platform instrument mapping must be pinned. Retain roll/source differences.',
  'costs':'Same predefined fee/spread/slippage treatment and same stress grid for every arm; source gross marks kept separate from actual paper simulation.',
  'tape_boundary':'Censored if entry/exit cannot be observed or filled before available tape ends; no retrospective liquidation at last trade unless explicitly labelled valuation-only.',
  'retention_statuses':['PREDICATE_TRUE','PREDICATE_FALSE','INPUT_UNAVAILABLE','UNKNOWN_SOURCE_DIRECTION','UNBOUND_FORECAST','NO_ENTRY_LATE_IDENTITY','EXPIRED_BEFORE_FILL','NO_FILL','RISK_REJECTED','DUPLICATE_SIGNAL','ENTRY_FILLED','EXIT_FILLED','OPEN_AT_TAPE_END','CENSORED','MISSING_MARK','POSITIVE','ZERO','NEGATIVE'],
  'admission':'No historical return/sign/pvalue/sample count/fold success/novelty-overlap ranking or exclusion. Source-specific causal predicates remain distinct.'},
 'unresolved_sources':review['unresolved_definitions'],
 'coverage_assertions':{'exact_search_cells':2016,'atlas_cells':680,'pair_modules':32,'triplet_modules':256,'total_module_cells':288,'prefix_states':7,'side_overlay_count':2,'source_directed_arm_retained':True,'current_or_future_outcome_labels_used_as_early_live_inputs':False},
 'provenance':'All source refs resolve to byte-verified receipts in review_chain.json. These recipes distinguish source facts from new paper-design choices and leave unbound forecasts/detector marks explicit. No refit, worker, suite, migration, agent or parent-artifact mutation performed.'}

assert (4**2+4**3+4**4)*3*2==report['coverage_assertions']['exact_search_cells']
assert sum(4**k for k in range(1,5))*2==report['coverage_assertions']['atlas_cells']
assert 4**2*2+4**3*2**2==288
# Latest parent steering: uniform process is not a blanket opposite-side control.
report['current_direction_policy']={
 'source_direction_defined':'Instantiate the original source-directed side. Do not add blanket LONG/SHORT controls to that directional hypothesis.',
 'source_explicit_contrary_branches':'Preserve each explicit source contrary orientation/branch under its own original semantics.',
 'structural_hypothesis_has_no_trade_side':'Use labelled LONG and SHORT paper-design arms for nondirectional modules/prefixes/structural state forecasts; same inclusion and reporting.',
 'source_selected_direction_missing':'UNRESOLVED_DIRECTION input/implementation status; do not infer a sign from evaluation outcomes and do not pretend absence of recovered source sign means the source was nondirectional.',
 'not_identical_orders':'Same inclusion/process/reporting retains natural hypothesis differences in direction, trigger, clock, lifecycle and exits.'}
report['audit_findings'][0]={
 'id':'R01','issue':'A blanket LONG/SHORT overlay on every already directional rule is outside the latest requested interpretation and can obscure original hypothesis semantics.',
 'fix':'Preserve source-directed originals and explicitly sourced contrary branches. Only genuinely nondirectional structural hypotheses receive labelled LONG/SHORT designs. Missing source-selected signs stay unresolved.'}
report['audit_findings'][1]['fix']='Native bank-positive management uses p_current*(mark_at_anchor+h-mark_at_anchor+5)/tick>0. A hypothesis that explicitly changes orientation or management basis requires its own labelled rule. Do not silently replace source predicate with PnL from a differently oriented overlay.'
report['common_axes']['side'][0]['applies_to']='Source-directed hypotheses with recovered exact direction.'
for side in report['common_axes']['side'][1:]:
 side['applies_to']='Genuinely nondirectional module/prefix/structural-state hypotheses only, or separately explicitly requested contrary experiment; not automatic on directional originals.'
for recipe in recipes:
 if recipe['id'] in ['CHAIN_EXACT_SOURCE_SEARCH','CHAIN_ATLAS_DEPTH1_TO4','CANONICAL_POX_PARENT']:
  recipe['generate']['execution_side']=['SOURCE_DIRECTED']
 if recipe['id']=='CHAIN_EXACT_SOURCE_SEARCH':
  recipe['unspecified_source_direction']='Retain UNRESOLVED_DIRECTION for a cell whose source-selected sign is unbound. Do not fabricate a sign or install blanket opposite-direction control.'
  recipe['source_vs_design']='Alphabet/order/depth/optional relation/exits are source family. Delayed fill-hold is new design. Preserve recovered source direction; no blanket LONG/SHORT additions to directional originals.'
 if recipe['id']=='FROZEN_SSOS':
  recipe['axes']='Both source clock anchors and fixed/delayed timing axes; SOURCE_DIRECTED only. Native DOC_ONSET/SOURCE_FIXED/SOURCE_DIRECTED remains identifiable as documented frozen play.'
 if recipe['id']=='FOCUSED_POX_FIXED3429':
  recipe['execution_overlays']='Preserve source-directed initial continuation where defined. Nondirectional branch-state hypotheses may get labelled LONG/SHORT designs only after their causal trigger is independently specified. Missing lawful input produces retained INPUT_UNAVAILABLE.'
 if recipe['id']=='POX_BANK_POSITIVE_PROXY':
  recipe['generate']['management_basis']=['SOURCE_ORIENTED_REFERENCE_RETURN']
  recipe['non_default_design_alternative']='Own-position-PnL banking is documented here only as a possible differently defined experiment; do not instantiate it by default.'
report['coverage_assertions']['side_overlay_count']=2
report['coverage_assertions']['side_overlay_scope']='Only nondirectional structural/module/prefix/state hypotheses; no blanket opposite-side controls on directional originals.'
report['expression_dsl']={
 'literal':'{const:value}; bare primitive args also mean constants, never field names.',
 'field':'{field:name}; resolve typed value and known_by from immutable as-of snapshot; absent or not-yet-available -> UNKNOWN.',
 'op':'{op:name,args:[...]}; supported and/or/eq/lt/lte/gt/gte/mul/div/sub/add_seconds/all; all binds item for each list member; arithmetic propagates UNKNOWN and div byzero is UNKNOWN.',
 'source_mark_price_at':'Latest source-defined causal last-trade mark actually available at requested timestamp, preserving proper source/tape order; carries its observation timestamp. Never prospective broker fill.',
 'polarity_in_named_stratum':'ALL=true; UP means polarity=+1; DOWN means polarity=-1; missing polarity -> UNKNOWN.',
 'passes_frozen_lock_rule':'Resolve actual frozen predicate by immutable rule ID. Missing rule/threshold/model receipt -> UNKNOWN; do not invent threshold or evaluate using outcome.',
 'chronology':'No field semantic_kind=posthoc_outcome/oracle_cohort can enter earlier live predicate; diagnostic/classification expressions are explicitly named separately.'}
for recipe in recipes:
 if recipe['id']=='POX_BANK_POSITIVE_PROXY':
  r_now=cond('source_mark_price_at',cond('add_seconds',F('clock.anchor'),F('params.bank_offset_s')))
  r_entry=cond('source_mark_price_at',cond('add_seconds',F('clock.anchor'),C(5)))
  recipe['source_condition']=cond('gt',cond('div',cond('mul',F('target.polarity'),cond('sub',r_now,r_entry)),F('instrument.tick_size')),C(0))
  recipe['design_condition']=cond('gt',cond('div',cond('mul',F('execution.side'),cond('sub',F('causal_mark_now'),F('execution.actual_fill_price'))),F('instrument.tick_size')),C(0))
p=ROOT/'review_chain_recipes.json'; p.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'path':str(p),'recipe_count':len(recipes),'issues':len(audit),'bytes':p.stat().st_size}))
