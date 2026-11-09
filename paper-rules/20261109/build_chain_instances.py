import gzip
import hashlib
import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MACHINE = ROOT / 'machine'
RECIPE_PATH = ROOT / 'review_chain_recipes.json'
REVIEW_PATH = ROOT / 'review_chain.json'
RECIPES = json.loads(RECIPE_PATH.read_text(encoding='utf-8'))
REVIEW = json.loads(REVIEW_PATH.read_text(encoding='utf-8'))
BY_RECIPE = {r['id']: r for r in RECIPES['recipes']}
ALPHABET = ['P', 'O', 'S', 'X']
ANCHORS = ['DOC_ONSET', 'PRODUCER_CONFIRM']
TIMINGS = ['SOURCE_FIXED', 'DELAYED_AFTER_KNOWN_FILL_HOLD']
POLARITIES = ['ALL', 'UP', 'DOWN']
HOLD_SECONDS = [25, 55]
SIDES = ['LONG', 'SHORT']
ROWS = []

def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False)

def digest_bytes(data):
    return hashlib.sha256(data).hexdigest()

def pointer(recipe_id):
    idx = next(i for i, r in enumerate(RECIPES['recipes']) if r['id'] == recipe_id)
    return {'file': '../review_chain_recipes.json', 'json_pointer': f'/recipes/{idx}', 'recipe_id': recipe_id, 'definition_sha256': digest_bytes(canonical(BY_RECIPE[recipe_id]).encode())}

def strings(lengths, alphabet=ALPHABET):
    for length in lengths:
        for chars in itertools.product(alphabet, repeat=length):
            yield ''.join(chars)

SOURCE_ORIENTATION_60 = {x['motif']: x['source_orientation'] for x in REVIEW['explicit_maps']['recurrence']['causal_predecessor_motifs']}

def orientation(seed, relation, exit_offset):
    if seed == 'SSOS' and relation == 'UNSPLIT' and exit_offset == 30:
        return 1, 'FROZEN_SSOS_PLUS30', ['ssos_freeze', 'ssos_producer']
    if seed == 'POX' and exit_offset == 60:
        return 1, 'CANONICAL_POX_CONTINUATION_PLUS60', ['pox_correction', 'pox_branches']
    key = f'{seed}->{relation}'
    if exit_offset == 60 and key in SOURCE_ORIENTATION_60:
        return SOURCE_ORIENTATION_60[key], 'RECOVERED_MOTIF_PLUS60', ['novelty', 'postexit']
    return None, 'UNRESOLVED_SOURCE_SELECTED_DIRECTION', []

COMMON_PREREQUISITES = ['instrument_identity', 'tick_size', 'actual_event_order', 'asof_snapshot', 'common_paper_fill_policy', 'common_paper_cost_policy']
SEED_PREREQUISITES = [
    'target_detector_identity_known_by', 'ordered_predecessor_identity_known_by',
    'ordered_predecessor_seed_known_by', 'current_and_predecessor_polarity_known_by',
    'source_h60_history_feature_cells', 'source_h60_history_wall',
    'target_endpoint_onset', 'target_endpoint_confirmation', 'lawful_negative_overlap_evidence'
]

def source_aliases(recipe_id):
    aliases = [x['source'] for x in BY_RECIPE[recipe_id].get('sources', [])]
    return sorted(set(aliases))

def emit(recipe_id, parameters, specification_kind, execution, prerequisites, source_fields, new_designs=None, bindings=None, source_alias_override=None):
    key = {'schema_version': 'CHAIN_INSTANCE_V1', 'recipe_id': recipe_id, 'recipe_definition_sha256': pointer(recipe_id)['definition_sha256'], 'parameters': parameters}
    identifier = 'CHAIN_' + digest_bytes(canonical(key).encode())
    ROWS.append({
        'id': identifier,
        'schema_version': 'CHAIN_INSTANCE_V1',
        'paper_included': True,
        'execution_enabled': False,
        'catalog_type': 'SPECIFICATION',
        'specification_kind': specification_kind,
        'recipe': pointer(recipe_id),
        'parameters': parameters,
        'known_prerequisites': sorted(set(COMMON_PREREQUISITES + prerequisites)),
        'execution_specification': execution,
        'unresolved_bindings': sorted(set(bindings or [])),
        'provenance': {
            'source_aliases': source_alias_override if source_alias_override is not None else source_aliases(recipe_id),
            'source_fields': sorted(set(source_fields)),
            'new_paper_design_fields': sorted(set(new_designs or [])),
        },
        'retention_policy_id': 'ALL_CANDIDATES_ALL_OUTCOMES_NO_PERFORMANCE_ADMISSION',
        'report_protocol_id': 'CHAIN_COMMON_REPORT_V1',
    })

def fixed_or_delayed_execution(parameters, side_orientation):
    anchor_field = 'target.structural_endpoint_onset' if parameters['clock_anchor'] == 'DOC_ONSET' else 'target.structural_endpoint_confirmation'
    if parameters['timing'] == 'SOURCE_FIXED':
        entry = {'operation': 'ADD_SECONDS', 'anchor': anchor_field, 'offset_seconds': 5}
        exit_ = {'operation': 'ADD_SECONDS', 'anchor': anchor_field, 'offset_seconds': parameters['exit_offset_s']}
    else:
        entry = {'operation': 'FIRST_PLATFORM_DECISION_AT_OR_AFTER_MAX', 'source_scheduled_entry': {'anchor': anchor_field, 'offset_seconds': 5}, 'availability_anchor': 'ALL_REQUIRED_INPUTS_ACTUALLY_KNOWN_BY'}
        exit_ = {'operation': 'ADD_SECONDS', 'anchor': 'ACTUAL_ENTRY_FILL', 'offset_seconds': parameters['exit_offset_s'] - 5}
    return {'side_mode': 'SOURCE_DIRECTED', 'orientation': side_orientation, 'polarity_anchor': 'target.polarity', 'entry': entry, 'exit': exit_, 'missing_input_action': 'RETAIN_INPUT_UNAVAILABLE_NO_ENTRY', 'missing_fill_action': 'RETAIN_NO_FILL', 'tape_end_action': 'RETAIN_CENSORED', 'unknown_polarity_action': 'RETAIN_INPUT_UNAVAILABLE_NO_ENTRY'}

def emit_seed(recipe_id, parameters, extra_designs=None, bindings=None, source_side=None):
    side, resolution, aliases = orientation(parameters['seed_string'], parameters['relation'], parameters['exit_offset_s'])
    if source_side is not None:
        side = source_side
        resolution = 'EXPLICIT_RECIPE_SOURCE_DIRECTION'
    params = dict(parameters, source_orientation=side, source_orientation_status=resolution)
    designs = list(extra_designs or [])
    if params['timing'] == 'DELAYED_AFTER_KNOWN_FILL_HOLD':
        designs += ['delayed_after_known_entry', 'fill_relative_hold']
    unresolved = list(bindings or []) + ['frozen_detector_identity_known_by', 'lawful_negative_overlap_evidence', 'platform_paper_adapter_binding']
    if side is None:
        unresolved.append('exact_source_selected_direction')
    emit(recipe_id, params, 'SOURCE_DIRECTED_RULE_SPECIFICATION', fixed_or_delayed_execution(params, side), SEED_PREREQUISITES + ['source_direction_binding'], ['seed_string', 'relation', 'exit_offset_s', 'clock_anchor', 'source_orientation'], designs, unresolved, sorted(set(source_aliases(recipe_id) + aliases)))

# 336 source strings x3 relations x2 exits x2 anchors x2 timings.
for seed, relation, exit_offset, anchor, timing in itertools.product(strings([2, 3, 4]), ['UNSPLIT', 'SAME', 'FLIP'], [30, 60], ANCHORS, TIMINGS):
    emit_seed('CHAIN_EXACT_SOURCE_SEARCH', {'seed_string': seed, 'relation': relation, 'exit_offset_s': exit_offset, 'clock_anchor': anchor, 'timing': timing, 'execution_side': 'SOURCE_DIRECTED'})

# The atlas source generator includes one-predecessor arms.
for seed, relation, anchor, timing in itertools.product(strings([1, 2, 3, 4]), ['SAME', 'FLIP'], ANCHORS, TIMINGS):
    emit_seed('CHAIN_ATLAS_DEPTH1_TO4', {'seed_string': seed, 'relation': relation, 'exit_offset_s': 60, 'clock_anchor': anchor, 'timing': timing, 'execution_side': 'SOURCE_DIRECTED'})

for anchor, timing in itertools.product(ANCHORS, TIMINGS):
    emit_seed('FROZEN_SSOS', {'seed_string': 'SSOS', 'relation': 'UNSPLIT', 'exit_offset_s': 30, 'clock_anchor': anchor, 'timing': timing, 'execution_side': 'SOURCE_DIRECTED'}, source_side=1)

parent_parameters = []
for relation, polarity, anchor, timing in itertools.product(['UNSPLIT', 'SAME', 'FLIP'], POLARITIES, ANCHORS, TIMINGS):
    p = {'seed_string': 'POX', 'relation': relation, 'absolute_current_polarity': polarity, 'exit_offset_s': 60, 'clock_anchor': anchor, 'timing': timing, 'execution_side': 'SOURCE_DIRECTED'}
    parent_parameters.append(p)
    emit_seed('CANONICAL_POX_PARENT', p, source_side=1)

for parent, bank_offset in itertools.product(parent_parameters, [10, 30]):
    p = dict(parent, bank_offset_s=bank_offset, management_basis='SOURCE_ORIENTED_REFERENCE_RETURN')
    side = 1
    execution = fixed_or_delayed_execution(p, side)
    if p['timing'] == 'SOURCE_FIXED':
        execution['bank_check'] = {'anchor': p['clock_anchor'], 'offset_seconds': bank_offset, 'predicate_id': 'SOURCE_ORIENTED_R_BANK_GT_ZERO', 'true_action': 'REQUEST_EXIT', 'false_action': 'KEEP_ORIGINAL_EXIT', 'unknown_action': 'KEEP_ORIGINAL_EXIT_RECORD_UNKNOWN'}
        designs = ['proxy_by_parent_branch_and_polarity_cross_product']
    else:
        execution['bank_check'] = {'anchor': 'ACTUAL_ENTRY_FILL', 'offset_seconds': bank_offset - 5, 'predicate_id': 'CURRENT_POLARITY_ORIENTED_FILL_REFERENCE_RETURN_GT_ZERO', 'true_action': 'REQUEST_EXIT', 'false_action': 'KEEP_FILL_PLUS55_EXIT', 'unknown_action': 'KEEP_FILL_PLUS55_EXIT_RECORD_UNKNOWN'}
        designs = ['proxy_by_parent_branch_and_polarity_cross_product', 'delayed_after_known_entry', 'fill_relative_hold', 'fill_relative_bank_checkpoint', 'fill_reference_mark_in_place_of_source_plus5']
    p.update(source_orientation=1, source_orientation_status='CANONICAL_POX_CONTINUATION_PLUS60')
    emit('POX_BANK_POSITIVE_PROXY', p, 'SOURCE_DIRECTED_MANAGEMENT_SPECIFICATION', execution, SEED_PREREQUISITES + ['source_reference_entry_mark', 'bank_check_mark_known_by'], ['bank_offset_s', 'management_basis', 'source_orientation'], designs, ['frozen_detector_identity_known_by', 'lawful_negative_overlap_evidence', 'platform_paper_adapter_binding'])

def nondirectional(recipe_id, base_params, native_kind, prerequisites, source_fields, bindings, native_output_heads, new_base_fields=None):
    emit(recipe_id, dict(base_params, mode='NATIVE_OBSERVATION', execution_side='NONE', hold_seconds=None), native_kind,
         {'side_mode': 'NONE', 'entry': None, 'exit': None, 'output_heads': native_output_heads},
         prerequisites, source_fields, new_base_fields or [], bindings)
    for side, hold in itertools.product(SIDES, HOLD_SECONDS):
        emit(recipe_id, dict(base_params, mode='PAPER_ECONOMIC_OVERLAY', execution_side=side, hold_seconds=hold), 'NEW_NON_DIRECTIONAL_PAPER_OVERLAY_SPECIFICATION',
             {'side_mode': 'ABSOLUTE', 'absolute_side': side, 'entry': {'operation': 'FIRST_PLATFORM_DECISION_AFTER_REQUIRED_KNOWN_BY'}, 'exit': {'operation': 'ADD_SECONDS', 'anchor': 'ACTUAL_ENTRY_FILL', 'offset_seconds': hold}, 'missing_input_action': 'RETAIN_INPUT_UNAVAILABLE_NO_ENTRY', 'missing_fill_action': 'RETAIN_NO_FILL', 'tape_end_action': 'RETAIN_CENSORED'},
             prerequisites, source_fields, list(new_base_fields or []) + ['absolute_execution_side', 'causal_after_known_entry', 'fill_relative_hold'], bindings)

# Five completed-parent path states retained under each SAME parent clock/polarity/timing arm.
recovery_classes = ['SHALLOW30_SHALLOW60', 'SHALLOW30_DEEP60', 'DEEP30_SHALLOW60', 'DEEP30_DEEP60', 'OTHER_OR_UNKNOWN']
for parent, path_class in itertools.product([p for p in parent_parameters if p['relation'] == 'SAME'], recovery_classes):
    p = {k: v for k, v in parent.items() if k != 'execution_side'}
    p['path_class'] = path_class
    p['parent_path_reference'] = 'SOURCE_ANCHORED_MARKS'
    nondirectional('POX_POSTEXIT_RECOVERY', p, 'SOURCE_POSTEXIT_WATCH_SPECIFICATION', SEED_PREREQUISITES + ['parent_flat_confirmed_at', 'R30_R60_path_class_known_by'], ['path_class', 'parent_path_reference', 'clock_anchor'], ['parent_path_marks', 'parent_flat_binding', 'frozen_detector_identity_known_by'], ['RECOVERY_AT120_OR300', 'RELAPSE_120_TO300', 'PARENT_PATH_CLASS'], ['cross_product_with_parent_delayed_variant'] if p['timing'] != 'SOURCE_FIXED' else [])

# Module grammar and source named-module evidence are distinct fields.
named_modules = set(BY_RECIPE['PAIR_TRIPLET_MODULES']['source_named_modules'])
for seed in strings([2, 3]):
    for relation_string, polarity in itertools.product(strings([len(seed) - 1], ['S', 'F']), POLARITIES):
        module = seed + '|' + relation_string
        p = {'seed_string': seed, 'relative_polarity_string': relation_string, 'absolute_first_polarity': polarity, 'module': module, 'source_mention_status': 'NAMED' if module in named_modules else 'GRAMMAR_GENERATED'}
        nondirectional('PAIR_TRIPLET_MODULES', p, 'STRUCTURAL_MODULE_SPECIFICATION', ['member_identities_known_by', 'member_seeds_known_by', 'member_relative_polarities_known_by'], ['seed_alphabet', 'seed_length', 'relative_polarity_encoding', 'ordered_module'], ['frozen_detector_identity_known_by', 'module_state_provider_binding'], ['RECURRENCE', 'D1_TO_D2_EXTENSION', 'D2_TO_D3_EXTENSION', 'TIMING_CONTEXT'], ['full_grammar_expansion', 'absolute_first_polarity_stratum'])

for family, prefixes in BY_RECIPE['PREFIX_LADDERS']['generate']['family_prefixes'].items():
    for prefix in prefixes:
        p = {'family': family, 'prefix': prefix, 'source_watch_role': BY_RECIPE['PREFIX_LADDERS']['source_roles'][prefix]}
        nondirectional('PREFIX_LADDERS', p, 'SOURCE_PREFIX_WATCH_SPECIFICATION', ['prefix_member_identities_known_by', 'prefix_member_seeds_known_by', 'prefix_member_polarities_known_by'], ['family', 'prefix', 'source_watch_role'], ['frozen_detector_identity_known_by', 'prefix_provider_binding'], ['PREFIX_COMPLETE', 'PREFIX_FAILED', 'PREFIX_REPLACED', 'PREFIX_CENSORED'])

# Outcomes are target definitions, never event membership filters in these specifications.
forecast_targets = [{'head': 'EXACT_DEPTH_FORECAST', 'stage_scope': 'ALL_CAUSAL_CANDIDATES', 'target': depth} for depth in range(6)]
forecast_targets += [{'head': 'PATH_CLASS_FORECAST', 'stage_scope': 'D1_TARGET', 'target': label} for label in ['DIRECTIONAL', 'CHOP_ROTATION']]
forecast_targets += [{'head': 'TIMING_FAMILY_FORECAST', 'stage_scope': 'D2_TARGET', 'target': label} for label in ['SHORT', 'MIDDLE', 'LONG']]
forecast_targets += [{'head': 'TIMING_FAMILY_FORECAST', 'stage_scope': 'D3_TARGET', 'target': label} for label in ['SHORT', 'LONG']]
for target in forecast_targets:
    p = dict(target, cohort_filter='NONE_BY_REALIZED_LABEL', signal_condition='CAUSAL_FORECAST_AND_FROZEN_LOCK', target_label_role='REPORTING_AND_MODEL_TARGET_ONLY')
    prereq = ['causal_candidate_provider', 'forecast_model_hash', 'forecast_feature_revision', 'forecast_snapshot_hash', 'forecast_evaluated_at', 'forecast_available_at', 'frozen_lock_rule_hash', 'frozen_lock_rule_parameters']
    bindings = ['causal_candidate_provider', 'trained_forecast_artifact', 'frozen_lock_rule_parameters']
    if target['head'] in ['PATH_CLASS_FORECAST', 'TIMING_FAMILY_FORECAST']:
        bindings += ['frozen_label_model_parameters', 'label_reveal_contract']
    nondirectional('D0_D5_CONTINUOUS_CAUSAL_FORECAST', p, 'CAUSAL_FORECAST_SPECIFICATION', prereq, ['target_label', 'continuous_one_second_resolution'], bindings, ['IMMUTABLE_PROBABILITY_MOVIE', 'FIRST_CAUSAL_LOCK', 'OUTCOME_JOIN'], ['forecast_to_trade_mapping'])

# Focused POX is not reconstructed from canonical POX adjacency.
focused_prereq = ['fixed3429_master_ledger_binding', 'honest_candidate_control_universe', 'causal_membership_signal_known_by', 'initial_event_identity_known_by', 'initial_event_polarity_known_by']
focused_bindings = ['fixed3429_master_ledger_binding', 'honest_candidate_control_universe', 'causal_membership_model', 'initial_entry_rule', 'source_exit_rule']
initial_base = {'population_id': 'FOCUSED_POX_FIXED3429', 'phase': 'INITIAL_CONTINUATION', 'source_orientation': 1, 'polarity_anchor': 'INITIAL_EVENT_POLARITY', 'cohort_filter': 'NONE_BY_FUTURE_FLIP_SAME'}
emit('FOCUSED_POX_FIXED3429', dict(initial_base, mode='SOURCE_RULE_UNBOUND', hold_seconds=None), 'SOURCE_DIRECTED_UNBOUND_RULE_SPECIFICATION', {'side_mode': 'SOURCE_DIRECTED', 'orientation': 1, 'polarity_anchor': 'INITIAL_EVENT_POLARITY', 'entry': {'operation': 'UNBOUND_SOURCE_ENTRY'}, 'exit': {'operation': 'UNBOUND_SOURCE_EXIT'}}, focused_prereq, ['initial_continuation_orientation', 'fixed_population_identity'], [], focused_bindings)
for hold in HOLD_SECONDS:
    emit('FOCUSED_POX_FIXED3429', dict(initial_base, mode='SOURCE_DIRECTION_NEW_CAUSAL_TIMING_DESIGN', hold_seconds=hold), 'NEW_SOURCE_DIRECTED_TIMING_SPECIFICATION', {'side_mode': 'SOURCE_DIRECTED', 'orientation': 1, 'polarity_anchor': 'INITIAL_EVENT_POLARITY', 'entry': {'operation': 'FIRST_PLATFORM_DECISION_AFTER_CAUSAL_MEMBERSHIP_SIGNAL'}, 'exit': {'operation': 'ADD_SECONDS', 'anchor': 'ACTUAL_ENTRY_FILL', 'offset_seconds': hold}}, focused_prereq, ['initial_continuation_orientation', 'fixed_population_identity'], ['causal_membership_signal_entry', 'fill_relative_hold'], focused_bindings)
for branch, knowledge in itertools.product(['FLIP', 'SAME'], ['CAUSAL_FORECAST', 'ACTUAL_REVEALED']):
    p = {'population_id': 'FOCUSED_POX_FIXED3429', 'phase': 'LATER_BRANCH', 'branch': branch, 'branch_knowledge_mode': knowledge, 'cohort_filter': 'NONE_BY_UNREVEALED_BRANCH'}
    prerequisites = focused_prereq + (['branch_forecast_known_by', 'branch_forecast_model_hash', 'branch_forecast_lock_rule_hash'] if knowledge == 'CAUSAL_FORECAST' else ['actual_branch_label_revealed_at'])
    bindings = focused_bindings + (['branch_forecast_model', 'branch_forecast_lock_rule'] if knowledge == 'CAUSAL_FORECAST' else ['actual_branch_label_reveal_contract'])
    nondirectional('FOCUSED_POX_FIXED3429', p, 'BRANCH_STATE_SPECIFICATION', prerequisites, ['fixed_population_identity', 'branch_labels'], bindings, ['BRANCH_PREDICTION', 'BRANCH_REVEAL'], ['forecast_or_revealed_branch_lane_split'])
nondirectional('FOCUSED_POX_FIXED3429', {'population_id': 'FOCUSED_POX_FIXED3429', 'phase': 'POSTEXIT_DELAYED_REEXPRESSION', 'branch': 'SAME', 'cohort_filter': 'NONE_BY_FUTURE_RECOVERY'}, 'SOURCE_DELAYED_REEXPRESSION_WATCH_SPECIFICATION', focused_prereq + ['parent_flat_confirmed_at', 'actual_same_branch_revealed_at'], ['fixed_population_identity', 'delayed_same_watch'], focused_bindings + ['actual_same_branch_reveal_contract'], ['LATER_RECOVERY', 'FRESH_REENTRY'])

EXPECTED = {'CHAIN_EXACT_SOURCE_SEARCH': 8064, 'CHAIN_ATLAS_DEPTH1_TO4': 2720, 'FROZEN_SSOS': 4, 'CANONICAL_POX_PARENT': 36, 'POX_BANK_POSITIVE_PROXY': 72, 'POX_POSTEXIT_RECOVERY': 300, 'PAIR_TRIPLET_MODULES': 4320, 'PREFIX_LADDERS': 35, 'D0_D5_CONTINUOUS_CAUSAL_FORECAST': 65, 'FOCUSED_POX_FIXED3429': 28}
counts = Counter(r['recipe']['recipe_id'] for r in ROWS)
assert dict(counts) == EXPECTED, (dict(counts), EXPECTED)
assert set(counts) == set(BY_RECIPE)
assert len({r['id'] for r in ROWS}) == len(ROWS)
assert all(r['paper_included'] and not r['execution_enabled'] for r in ROWS)

def project(recipe, keys):
    return {tuple(r['parameters'][key] for key in keys) for r in ROWS if r['recipe']['recipe_id'] == recipe}

assert project('CHAIN_EXACT_SOURCE_SEARCH', ['seed_string','relation','exit_offset_s','clock_anchor','timing']) == set(itertools.product(strings([2,3,4]), ['UNSPLIT','SAME','FLIP'], [30,60], ANCHORS, TIMINGS))
assert project('CHAIN_ATLAS_DEPTH1_TO4', ['seed_string','relation','clock_anchor','timing']) == set(itertools.product(strings([1,2,3,4]), ['SAME','FLIP'], ANCHORS, TIMINGS))
assert project('CANONICAL_POX_PARENT', ['relation','absolute_current_polarity','clock_anchor','timing']) == set(itertools.product(['UNSPLIT','SAME','FLIP'], POLARITIES, ANCHORS, TIMINGS))
assert len(project('PAIR_TRIPLET_MODULES', ['module'])) == 288
assert len(project('PREFIX_LADDERS', ['family','prefix'])) == 7
module_expected=set()
for seed in strings([2,3]):
    for rel,pol in itertools.product(strings([len(seed)-1],['S','F']),POLARITIES):
        module_expected.add((seed+'|'+rel,pol,'NATIVE_OBSERVATION','NONE',None))
        for side,hold in itertools.product(SIDES,HOLD_SECONDS):module_expected.add((seed+'|'+rel,pol,'PAPER_ECONOMIC_OVERLAY',side,hold))
assert project('PAIR_TRIPLET_MODULES',['module','absolute_first_polarity','mode','execution_side','hold_seconds'])==module_expected
assert project('FROZEN_SSOS',['clock_anchor','timing'])==set(itertools.product(ANCHORS,TIMINGS))
assert project('POX_BANK_POSITIVE_PROXY',['relation','absolute_current_polarity','clock_anchor','timing','bank_offset_s','management_basis'])==set(itertools.product(['UNSPLIT','SAME','FLIP'],POLARITIES,ANCHORS,TIMINGS,[10,30],['SOURCE_ORIENTED_REFERENCE_RETURN']))
mode_sides_holds=[('NATIVE_OBSERVATION','NONE',None)]+[('PAPER_ECONOMIC_OVERLAY',side,hold) for side,hold in itertools.product(SIDES,HOLD_SECONDS)]
recovery_expected={(pol,anchor,timing,path_class,mode,side,hold) for pol,anchor,timing,path_class in itertools.product(POLARITIES,ANCHORS,TIMINGS,recovery_classes) for mode,side,hold in mode_sides_holds}
assert project('POX_POSTEXIT_RECOVERY',['absolute_current_polarity','clock_anchor','timing','path_class','mode','execution_side','hold_seconds'])==recovery_expected
prefix_expected={(family,prefix,mode,side,hold) for family,prefixes in BY_RECIPE['PREFIX_LADDERS']['generate']['family_prefixes'].items() for prefix in prefixes for mode,side,hold in mode_sides_holds}
assert project('PREFIX_LADDERS',['family','prefix','mode','execution_side','hold_seconds'])==prefix_expected
forecast_expected={(target['head'],target['stage_scope'],target['target'],mode,side,hold) for target in forecast_targets for mode,side,hold in mode_sides_holds}
assert project('D0_D5_CONTINUOUS_CAUSAL_FORECAST',['head','stage_scope','target','mode','execution_side','hold_seconds'])==forecast_expected
focused=[r for r in ROWS if r['recipe']['recipe_id']=='FOCUSED_POX_FIXED3429']
assert Counter(r['parameters']['phase'] for r in focused)=={'INITIAL_CONTINUATION':3,'LATER_BRANCH':20,'POSTEXIT_DELAYED_REEXPRESSION':5}
assert {(r['parameters']['branch'],r['parameters']['branch_knowledge_mode'],r['parameters']['mode'],r['parameters']['execution_side'],r['parameters']['hold_seconds']) for r in focused if r['parameters']['phase']=='LATER_BRANCH'}=={(branch,knowledge,mode,side,hold) for branch,knowledge in itertools.product(['FLIP','SAME'],['CAUSAL_FORECAST','ACTUAL_REVEALED']) for mode,side,hold in mode_sides_holds}
assert {(r['parameters']['mode'],r['parameters']['hold_seconds']) for r in focused if r['parameters']['phase']=='INITIAL_CONTINUATION'}=={('SOURCE_RULE_UNBOUND',None),('SOURCE_DIRECTION_NEW_CAUSAL_TIMING_DESIGN',25),('SOURCE_DIRECTION_NEW_CAUSAL_TIMING_DESIGN',55)}
assert {(r['parameters']['mode'],r['parameters']['execution_side'],r['parameters']['hold_seconds']) for r in focused if r['parameters']['phase']=='POSTEXIT_DELAYED_REEXPRESSION'}==set(mode_sides_holds)

ROWS.sort(key=lambda r: (r['recipe']['recipe_id'], r['id']))
raw = ''.join(canonical(r)+'\n' for r in ROWS).encode('utf-8')
MACHINE.mkdir(parents=True, exist_ok=True)
output = MACHINE/'CHAIN_INSTANCES.jsonl.gz'
with output.open('wb') as handle:
    with gzip.GzipFile(fileobj=handle, mode='wb', filename='', mtime=0, compresslevel=9) as archive:
        archive.write(raw)
with gzip.open(output,'rt',encoding='utf-8') as handle:
    reread=[json.loads(line) for line in handle]
assert reread==ROWS

direction_counts=Counter(r['parameters'].get('source_orientation_status','NOT_SOURCE_SEARCH_DIRECTION_AXIS') for r in ROWS)
coverage=[{'recipe_id':k,'expected':EXPECTED[k],'actual':counts[k],'status':'EXACT_COUNT_MATCH'} for k in EXPECTED]
manifest={
 'schema_version':'CHAIN_EXPANSION_V1',
 'catalog_type':'SPECIFICATION_CATALOG',
 'platform_execution_claim':False,
 'execution_enabled':False,
 'source_recipe_file':'../review_chain_recipes.json',
 'source_recipe_sha256':digest_bytes(RECIPE_PATH.read_bytes()),
 'source_review_file':'../review_chain.json',
 'source_review_sha256':digest_bytes(REVIEW_PATH.read_bytes()),
 'build_script':'../build_chain_instances.py',
 'build_script_sha256':digest_bytes(Path(__file__).read_bytes()),
 'build_command':'python build_chain_instances.py',
 'output':'CHAIN_INSTANCES.jsonl.gz',
 'gzip_sha256':digest_bytes(output.read_bytes()),
 'uncompressed_jsonl_sha256':digest_bytes(raw),
 'gzip_mtime':0,
 'instance_count':len(ROWS),
 'per_recipe_counts':coverage,
 'dimension_accounting':{
  'CHAIN_EXACT_SOURCE_SEARCH':{'seed_strings':336,'relations':3,'exits':2,'clocks':2,'timings':2,'source_side_axes':1},
  'CHAIN_ATLAS_DEPTH1_TO4':{'seed_strings':340,'relations':2,'exits':1,'clocks':2,'timings':2,'source_side_axes':1},
  'FROZEN_SSOS':{'source_rule':1,'clocks':2,'timings':2},
  'CANONICAL_POX_PARENT':{'relations':3,'absolute_polarity_strata':3,'clocks':2,'timings':2},
  'POX_BANK_POSITIVE_PROXY':{'parent_cells':36,'bank_offsets':2,'management_bases':1},
  'POX_POSTEXIT_RECOVERY':{'same_parent_cells':12,'path_classes':5,'native_plus_long_short_hold_designs':5},
  'PAIR_TRIPLET_MODULES':{'pair_modules':32,'triplet_modules':256,'absolute_polarity_strata':3,'native_plus_long_short_hold_designs':5},
  'PREFIX_LADDERS':{'source_prefixes':7,'native_plus_long_short_hold_designs':5},
  'D0_D5_CONTINUOUS_CAUSAL_FORECAST':{'depth_targets':6,'D1_path_targets':2,'D2_timing_family_targets':3,'D3_timing_family_targets':2,'native_plus_long_short_hold_designs':5},
  'FOCUSED_POX_FIXED3429':{'initial_source_unbound':1,'initial_source_direction_new_hold_designs':2,'branch_labels':2,'branch_knowledge_modes':2,'branch_native_plus_long_short_hold_designs':5,'delayed_same_native_plus_long_short_hold_designs':5}},
 'unexpanded_recipe_axes':[
  {'recipe_id':'D0_D5_CONTINUOUS_CAUSAL_FORECAST','axis':'trained_model_head_view_revision','reason_code':'EXACT_TRAINED_ARTIFACT_SET_UNBOUND','retained_in_instances':True},
  {'recipe_id':'D0_D5_CONTINUOUS_CAUSAL_FORECAST','axis':'lock_rule_threshold_parameter_grid','reason_code':'NO_FINITE_SOURCE_PARAMETER_SET','retained_in_instances':True},
  {'recipe_id':'D0_D5_CONTINUOUS_CAUSAL_FORECAST','axis':'D1_dynamic_GMM_timing_classes_and_D4_D5_timing_classes','reason_code':'NO_BOUND_FROZEN_CLASS_SET','retained_in_instances':True},
  {'recipe_id':'FOCUSED_POX_FIXED3429','axis':'individual3429_case_rows','reason_code':'CASE_LEDGER_NOT_BOUND_RULE_CATALOG_ONLY','source_case_count':3429,'future_label_counts':{'FLIP':1546,'SAME':1883}},
  {'recipe_id':'ALL','axis':'realized_event_case_ids_and_outcome_labels','reason_code':'SPECIFICATION_CATALOG_NOT_EVENT_LEDGER'},
  {'recipe_id':'CHAIN_EXACT_SOURCE_SEARCH','axis':'missing_source_selected_orientation_values','reason_code':'EXACT_SOURCE_DIRECTION_UNRESOLVED','retained_as_null_in_instances':True},
  {'recipe_id':'POX_BANK_POSITIVE_PROXY','axis':'OVERLAY_EXECUTED_PNL_DESIGN','reason_code':'RECIPE_EXPLICITLY_NONDEFAULT_NOT_IN_GENERATE_AXIS'},
  {'recipe_id':'ALL_DIRECTIONAL_SOURCE_RULES','axis':'blanket_LONG_SHORT_contrary_controls','reason_code':'NOT_DECLARED_UNDER_CURRENT_DIRECTION_POLICY'}],
 'report_output_heads_not_cartesian_trade_axes':['module_recurrence','module_D1_to_D2_extension','module_D2_to_D3_extension','module_timing_context','recovery_at120_or300','relapse','prefix_completion_failure_replacement_censoring'],
 'original_new_provenance':{
  'original_source_clock_versions':['DOC_ONSET','PRODUCER_CONFIRM'],
  'new_design_axes':['DELAYED_AFTER_KNOWN_FILL_HOLD','nondirectional_LONG_SHORT_fill_hold','full_module_grammar_expansion','proxy_parent_branch_polarity_cross_product','focused_initial_source_direction_causal_timing_design'],
  'orientation_scope':'RECOVERED_PLUS60_SIGNS_NOT_TRANSFERRED_TO_PLUS30;SSOS_PLUS30_ONLY;POX_PLUS60_ONLY',
  'source_manifest':{alias:{'git_blob_sha':s['git_blob_sha'],'verified_git_blob_sha':s['verified_git_blob_sha'],'url':s['url']} for alias,s in REVIEW['sources'].items()}},
 'source_direction_status_counts':dict(sorted(direction_counts.items())),
 'validation':{'count_coverage':True,'unique_ids':True,'source_search_cartesian_projection':True,'atlas_cartesian_projection':True,'pox_parent_cartesian_projection':True,'ssos_cartesian_projection':True,'bank_proxy_cartesian_projection':True,'recovery_cartesian_projection':True,'module_cartesian_projection':True,'prefix_cartesian_projection':True,'forecast_cartesian_projection':True,'focused_all_declared_axes_projection':True,'all_execution_disabled':True,'all_paper_included':True,'gzip_roundtrip':True},
 'id_algorithm':'CHAIN_ + SHA256(canonical JSON of schema_version,recipe_id,recipe_definition_sha256,parameters)',
 'ordering':['recipe_id','id'],
}
(MACHINE/'CHAIN_EXPANSION.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n',encoding='utf-8')
print(canonical({'instance_count':len(ROWS),'per_recipe':dict(counts),'gzip_bytes':output.stat().st_size,'gzip_sha256':manifest['gzip_sha256']}))
