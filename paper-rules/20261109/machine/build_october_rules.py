"""Compile retained finite metadata and source predicates. No replay, fit or order routing."""
from pathlib import Path
import gzip, hashlib, itertools, json, sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
from paper_rules.contract import UNKNOWN, evaluate, evaluate_rule, fields_in, validate_expression, validate_rule

def load(name):
    return json.loads((ROOT / name).read_text(encoding='utf-8'))

def write(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')

def expand(g):
    if g['op'] == 'literal':
        for x in g['records']:
            yield x if isinstance(x, dict) else {'value': x}
    elif g['op'] == 'product':
        keys = list(g['axes'])
        for values in itertools.product(*(g['axes'][k] for k in keys)):
            yield {**g.get('fixed', {}), **dict(zip(keys, values))}
    elif g['op'] == 'union':
        for child in g['children']:
            for row in expand(child):
                yield {**({'table': child['name']} if 'name' in child else {}), **row}
    else:
        raise ValueError(g['op'])

def c(v): return {'const': v}
def op(name, *args): return {'op': name, 'args': list(args)}
def AND(*xs): return op('and', *xs)
def OR(*xs): return op('or', *xs)
def eq(a, b): return op('eq', a, c(b))
def gt(a, b=0): return op('gt', a, c(b))
def lt(a, b=0): return op('lt', a, c(b))
def add(*xs): return op('add', *xs)
def sub(a, b): return op('sub', a, b)
def mul(a, b): return op('mul', a, b)
def sign(a): return op('sign', a)
def ab(a): return op('abs', a)
def ratio(b, s): return op('div', sub(b, s), add(b, s))

DEFS = {}
def field(name, formula, source, clock, role='feature'):
    ident = 'october.v1.' + name
    DEFS[name] = dict(definition_id=ident, role=role, formula=formula, source=source,
                     known_by_contract=clock, producer_status='MISSING_PLATFORM_PRODUCER',
                     missing_policy='UNKNOWN; never zero, false, or neutral by default')
    return {'field': name, 'definition_id': ident}

FC_SOURCE = 'S00131 git_blob205c9eccee3f4fd150fe3419b259fa70264c7ce9 lines88-160,193-227'
DP_SOURCE = 'S01770 git_blobebf6c4c0968f7d077506c4cd8e009fe235a198cc lines58-98,167-183'
EX_SOURCE = 'research_atlas_continuous.py git_blob9efd0ef52cee211dd9ba04b50e507d237e3787ed lines23-101,120-139'

def build():
    index = load('october_expansion_index.json')
    recipes = load('review_october_recipes.json')
    cells, counts, base_counts = [], {}, {}
    for family, generator in index['generators'].items():
        rows = list(expand(generator)); base_counts[family] = len(rows)
        if 'scope_axis' in generator:
            rows = [{**row, 'report_scope': scope} for scope in generator['scope_axis'] for row in rows]
        counts[family] = len(rows)
        for i, row in enumerate(rows, 1):
            kind = ('source_model_target_cell' if family in ('ST', 'FB', 'supplemental_models') else
                    'existing_rule_reference' if family == 'R' else
                    'declared_report_domain_cell' if family.startswith('OL') else 'source_report_cell')
            cells.append(dict(id=f'OCTCELL.{family}.{i:04d}', family=family, kind=kind,
                              axes=row, generator_pointer=f'october_expansion_index.json#/generators/{family}',
                              source=generator.get('source'), register_ids=generator.get('register_ids', []),
                              paper_included=True, execution_enabled=False,
                              is_unique_strategy=False, is_observed_source_row=None if family.startswith('OL') else 'see_source_version',
                              provenance_axes_expanded=False,
                              disposition_policy='Retain zero, empty, missing, undefined, false, no-fill and censored outcomes'))
    assert base_counts == index['validation']['generator_cardinalities_verified']
    blob = ''.join(json.dumps(x, sort_keys=True, separators=(',', ':')) + '\n' for x in cells).encode()
    (HERE / 'OCTOBER_SOURCE_CELLS.jsonl.gz').write_bytes(gzip.compress(blob, mtime=0))

    # Expand preserved fit identities, never model fitting. Source aliases remain visible.
    instances, evidence_seen = [], {}
    for family in ('ST', 'FB'):
        inventory = recipes[family + '_inventory']
        for version_number, version in enumerate(inventory['versions'], 1):
            folds = [f for f in version['metric_fold_ids'] if f >= 0]
            for arm, target_pair, fold in itertools.product(version['arms'], version['target_horizon_pairs'], folds):
                target, horizon = target_pair
                ident = f'OCTMODEL.{family}.v{version_number:02d}.{arm}.{target}.h{horizon}.f{fold}'
                key = (version['metrics']['sha'], version['splits']['sha'], arm, target, horizon, fold)
                alias = evidence_seen.get(key)
                evidence_seen.setdefault(key, ident)
                split_rows = [s for s in version['splits_content'] if int(s['fold']) == fold and int(s['horizon_s']) == horizon and ('target' not in s or s['target'] == target)]
                assert len(split_rows) == 1
                features = inventory['expanded_features'][arm] if family == 'ST' else inventory['method_arms'][arm]
                translation = ('absolute_price' if target in ('absolute', 'absolute_ticks') else
                               'flow_strength_change' if target == 'flow_strength_change' else 'signed_price')
                instances.append(dict(id=ident, family=family, source_version_number=version_number,
                    source_scope=version['scope'], source_role=version['role'], arm=arm, target=target,
                    horizon_s=horizon, fold=fold, features=features, split=split_rows[0],
                    method_source=version['method'], metrics_source=version['metrics'], splits_source=version['splits'],
                    identical_metrics_and_splits_alias_of=alias, independently_countable_fit=False if alias else None,
                    paper_included=True, execution_enabled=False,
                    active_math_allowed=not (family == 'FB' and version_number == 1),
                    unavailable_binding='ORIGINAL_FROZEN_MODEL_STATE_NOT_BOUND',
                    needed_state=['imputation', 'feature_order', 'center', 'scale', 'coefficients', 'intercept', 'train_label_known_by', 'producer_revision'],
                    target_type_recipe_pointer='review_october_recipes.json#/common_protocol/target_translation/' + translation,
                    translation_is_new_paper_design=True,
                    method_binding_limit=inventory.get('replication_method_limitation') if version['method'] is None else None,
                    provenance_note='Identical metric/split bytes are linked as evidence aliases, not asserted additional independent fits. Different output bytes alone also do not prove independent evidence.'))
    supplemental = load('supplemental_reanalysis_models.json')
    for arm in supplemental['arms']:
        for day in supplemental['common_fit']['test_dates']:
            row = next(x for x in supplemental['metric_row_keys'] if x['day'] == day and x['model'] == arm['name'] and x['subset'] == 'all')
            instances.append(dict(id=f'OCTMODEL.CANONICAL.{arm["name"]}.test{day}', family='canonical_supplemental',
                arm=arm['name'], features=arm['features'], target='future20', horizon_s=20, fold={'test_day':day},
                train_rule='all strictly earlier source dates with future20 defined', split=row,
                source=supplemental['sources']['analyze.py']['url'], source_sha=supplemental['sources']['analyze.py']['git_blob_sha'],
                source_lines='132-150', additional_architecture_over_R7_R8=arm['additional_architecture'],
                feature_architecture_alias_rule=arm['related_current_rule'],
                freeze_alias_warning='M0/M1 all-four-day freeze is not this earlier-day fit state',
                unavailable_binding='ORIGINAL_EARLIER_DAY_FIT_STATE_NOT_SERIALIZED_HERE',
                paper_included=True, execution_enabled=False,
                target_type_recipe_pointer='review_october_recipes.json#/common_protocol/target_translation/signed_price',
                translation_is_new_paper_design=True))
    assert len(instances) == 5 * 231 + 7 * 120 + 12
    assert len({x['id'] for x in instances}) == len(instances)
    model_blob = ''.join(json.dumps(x, sort_keys=True, separators=(',', ':')) + '\n' for x in instances).encode()
    (HERE / 'OCTOBER_MODEL_INSTANCES.jsonl.gz').write_bytes(gzip.compress(model_blob, mtime=0))

    fc_clock = 'Strict-pre snapshot: source cutoff_ns (fallback start_recv_ns-1), exact saved pre_input_cursor; group receive<=cutoff and matching cursor. Order decision cannot precede causal availability of family identity.'
    fc = {}
    for h in (1, 5, 60):
        for side in ('buy', 'sell'):
            fc[f'{side}{h}'] = field(f'fc.{side}{h}', f'root.activity.{h}.trade_{side}_aggressor_qty', FC_SOURCE, fc_clock)
    for side in ('bid', 'ask'):
        fc[f'{side}_depth'] = field(f'fc.{side}_depth', f'root.{side}_depth_full', FC_SOURCE, fc_clock)
        fc[f'{side}_touch'] = field(f'fc.{side}_touch', f'{side} size of selected strict-pre group', FC_SOURCE, fc_clock)
    fc['near'] = field('fc.near', 'root.depth_imbalance_n; missing remains UNKNOWN (legacy source coerced None to0)', FC_SOURCE, fc_clock)
    d1 = sign(sub(fc['buy1'], fc['sell1'])); recent = d1
    d5 = sign(sub(fc['buy5'], fc['sell5'])); d60 = sign(sub(fc['buy60'], fc['sell60']))
    depth = sign(sub(fc['bid_depth'], fc['ask_depth']))
    eligible = AND(op('ne', d1, c(0)), op('eq', d1, d5))
    flow_opp = op('eq', d60, mul(c(-1), recent)); flow_agree = op('eq', d60, recent)
    depth_opp = op('eq', depth, mul(c(-1), recent)); depth_agree = op('eq', depth, recent)
    both = AND(eligible, flow_opp, depth_opp)
    main = {
        'baseline': eligible,
        'baseline_plus_flow': AND(eligible, flow_opp),
        'baseline_flow_agrees': AND(eligible, flow_agree),
        'baseline_plus_book': AND(eligible, depth_opp),
        'baseline_book_agrees': AND(eligible, depth_agree),
        'baseline_plus_both': both,
        'both_agree': AND(eligible, flow_agree, depth_agree),
        'flow_opposes_depth_agrees': AND(eligible, flow_opp, depth_agree),
        'flow_agrees_depth_opposes': AND(eligible, flow_agree, depth_opp),
        'original_stack_sell_side': AND(gt(sub(fc['buy60'], fc['sell60'])), gt(sub(fc['sell5'], fc['buy5'])), gt(sub(fc['sell1'], fc['buy1'])), gt(sub(fc['bid_depth'], fc['ask_depth']))),
        'inverse_stack_buy_side': AND(gt(sub(fc['sell60'], fc['buy60'])), gt(sub(fc['buy5'], fc['sell5'])), gt(sub(fc['buy1'], fc['sell1'])), gt(sub(fc['ask_depth'], fc['bid_depth']))),
        'both_recent_sell': AND(both, lt(recent)),
        'both_recent_buy': AND(both, gt(recent)),
    }
    opportunity_fc = field('fc.causal_family_opportunity', 'True only when source family identity has actually become causally known; historical strict-pre selected row alone is insufficient', FC_SOURCE, 'known_by and cursor must precede/equal actual decision; never backdate', 'decision_state')
    opportunity_dp = field('dp.causal_recognition_opportunity', 'Recognition candidate emitted at original recognition_receive_ns/group; finalization-only identities unavailable live', DP_SOURCE, 'actual recognition completion/receipt, never birth', 'decision_state')
    # Explicit counts allow observed empty states without asking the evaluator to turn NaN into zero.
    dp_clock = 'At causal recognition, last20 completed-second midpoint-classified bins end at last_closed_second; each closed_by<=recognition; quote is recognition group, same valid segment.'
    dp = {k: field('dp.' + k, formula, DP_SOURCE, dp_clock) for k, formula in {
        'early_buy': 'sum buys first10 of current20 completed bins', 'early_sell': 'sum sells first10 of current20',
        'late_buy': 'sum buys last10 of current20', 'late_sell': 'sum sells last10 of current20',
        'bid_lots': 'bid touch lots at recognition group', 'ask_lots': 'ask touch lots at recognition group',
        'input_available': 'Original validity test at S01770:59-68; all required boundaries/groups valid and same segment'}.items()}
    et = add(dp['early_buy'], dp['early_sell']); lt_ = add(dp['late_buy'], dp['late_sell'])
    tb = add(dp['early_buy'], dp['late_buy']); ts = add(dp['early_sell'], dp['late_sell'])
    total = add(tb, ts); current = ratio(tb, ts)
    delta = sub(ab(ratio(dp['late_buy'], dp['late_sell'])), ab(ratio(dp['early_buy'], dp['early_sell'])))
    state = {'both_empty': eq(total, 0), 'one_half_empty': AND(gt(total), OR(eq(et, 0), eq(lt_, 0))),
             'steady': AND(gt(et), gt(lt_), eq(delta, 0)), 'strengthening': AND(gt(et), gt(lt_), gt(delta)),
             'weakening': AND(gt(et), gt(lt_), lt(delta))}
    product = mul(current, ratio(dp['bid_lots'], dp['ask_lots']))
    relation = {'undefined_flow': eq(total, 0), 'aligned': gt(product), 'balanced': eq(product, 0), 'opposed': lt(product)}

    ex_clock = 'Completed-second decision=(second+1)*NS;21 consecutive bins; strict earlier quotes at decision and decision-21s must be valid same segment. No birth/future outcome operands.'
    ex = {k: field('ex.' + k, formula, EX_SOURCE, ex_clock) for k, formula in {
        'input_available': '21 consecutive flow bins plus strict-pre valid same-segment book context (source23-68)',
        'buy': 'current completed-second classified buy lots', 'sell': 'current completed-second classified sell lots',
        'roll_buy': 'sum buy current20 bins', 'roll_sell': 'sum sell current20 bins',
        'before_buy': 'sum buy previous20 bins', 'before_sell': 'sum sell previous20 bins',
        'expired_buy': 'buy shifted20 bins', 'expired_sell': 'sell shifted20 bins',
        'early_buy': 'sum first10 current20 bins', 'early_sell': 'sum first10 current20 bins',
        'late_buy': 'sum last10 current20 bins', 'late_sell': 'sum last10 current20 bins',
        'fresh_buy5': 'sum last5 completed bins', 'fresh_sell5': 'sum last5 completed bins',
        'touch_imb': '(bidlots-asklots)/(bidlots+asklots) at strictly earlier quote',
        'prior_ticks20': '(mid_raw2(strictpredecision)-mid_raw2(strictpredecision-20s))/2e6'}.items()}
    er = ratio(ex['roll_buy'], ex['roll_sell']); before = ratio(ex['before_buy'], ex['before_sell'])
    early = ratio(ex['early_buy'], ex['early_sell']); late = ratio(ex['late_buy'], ex['late_sell'])
    fresh = ratio(ex['fresh_buy5'], ex['fresh_sell5'])
    step = AND(ex['input_available'], op('lt', ab(er), ab(before)))
    half = AND(ex['input_available'], op('lt', ab(late), ab(early)))
    predicates = {
        'step_weakening': step,
        'expiry_only_weakening': AND(step, eq(add(ex['buy'], ex['sell']), 0), gt(add(ex['expired_buy'], ex['expired_sell']))),
        'fresh_opposed_weakening': AND(step, lt(mul(sub(ex['buy'], ex['sell']), before))),
        'flow_vanished': AND(ex['input_available'], gt(add(ex['before_buy'], ex['before_sell'])), eq(add(ex['roll_buy'], ex['roll_sell']), 0)),
        'flow_resumed': AND(ex['input_available'], eq(add(ex['before_buy'], ex['before_sell']), 0), gt(add(ex['roll_buy'], ex['roll_sell']))),
        'half_weakening': half,
        'half_weakening_book_aligned': AND(half, gt(mul(ex['touch_imb'], er))),
        'half_weakening_book_opposed': AND(half, lt(mul(ex['touch_imb'], er))),
        'half_weakening_price_opposed': AND(half, lt(mul(ex['prior_ticks20'], er))),
        'half_weakening_fresh_book_opposed': AND(half, lt(mul(fresh, er)), lt(mul(ex['touch_imb'], er))),
    }
    invalid = field('execution.reset_or_data_failure', 'Common platform reset/feed-failure invalidation state; source research did not define trade invalidation', 'NEW OCT-EXEC-01', 'observed no later than decision', 'execution_state')
    rules = []
    def rule(cell, name, predicate, direction, gate, h, source, clock):
        entry = AND(gate, predicate)
        expressions = [entry, direction, invalid]
        used = set(fields_in(expressions))
        r = dict(id='OCTRULE.' + name + '.h' + str(h), paper_included=True, execution_enabled=False,
                 source_cell_id=cell['id'], source=source, source_predicate=predicate,
                 source_outcome_horizon_s=h, source_clock=clock,
                 entry={'condition': entry, 'sampling_decision_id': 'OCT-SAMPLING-' + cell['family']},
                 direction=direction, exit={'after_ns': str(h * 10**9), 'origin': 'actual_entry_fill', 'decision_id': 'OCT-EXEC-01'},
                 invalidation=invalid, requires={k: DEFS[k] for k in sorted(used)},
                 execution_design_ids=['OCT-EXEC-01', 'OCT-DIRECTION-01'],
                 readiness='PREDICATE_AST_VALIDATED_FEATURE_PRODUCERS_NOT_BOUND',
                 disposition_policy='Evaluate and retain TRUE/FALSE/UNKNOWN; undefined/zero direction retained, not coerced to a trade direction')
        validate_expression(predicate); validate_rule(r); rules.append(r)
    for cell in cells:
        a = cell['axes']; family = cell['family']
        if family == 'FC':
            named = a['named_cell']; h = a['horizon_s']
            if named['family'] == 'main':
                name = named['arm']; pred = main[name]
            else:
                book = sign(fc['near']) if named['book'] == 'near_sign' else sign(sub(fc['bid_touch'], fc['ask_touch']))
                product_fc = mul(book, recent)
                rel = {'opposes': lt(product_fc), 'agrees': gt(product_fc), 'equal': eq(product_fc, 0)}[named['relation']]
                subset = {'all': c(True), 'recent_sell': lt(recent), 'recent_buy': gt(recent), '60s_opposes': flow_opp}[named['subset']]
                pred = AND(eligible, rel, subset); name = '.'.join(named[k] for k in ('book', 'relation', 'subset'))
            rule(cell, 'FC.' + name, pred, recent, opportunity_fc, h, FC_SOURCE, fc_clock)
        elif family == 'DP':
            pair = a['state_book_pair']; pred = AND(dp['input_available'], state[pair['state']], relation[pair['book']])
            rule(cell, 'DP.' + pair['state'] + '.' + pair['book'], pred, sign(current), opportunity_dp, a['horizon_s'], DP_SOURCE, dp_clock)
        elif family == 'EX01_continuous':
            name = a['predicate']
            onset = field('ex.onset.' + name, 'First true observed bin after false/unavailable/gap for this predicate; first eligible true is left-censored, not proven physical onset. Source event_rows92-101. Unknown never silently treated as ordinary false.', EX_SOURCE, ex_clock, 'decision_state')
            rule(cell, 'EX01.' + name, predicates[name], sign(er), onset, a['horizon_s'], EX_SOURCE, ex_clock)

    assert len(rules) == 259 + 39 + 30
    assert len({r['id'] for r in rules}) == len(rules)
    decisions = dict(schema='october-rule-decisions/v1', execution_enabled=False,
        decisions=[
            dict(id='OCT-EXEC-01', classification='NEW_EXECUTION_DESIGN', entry='Platform execution only after actual causal decision; no research midpoint treated as fill', exit='Actual entry fill+h seconds, each original horizon separate. Original source anchor+h outcomes retained separately; no claim of equivalence to this entry-relative trade.', invalidation='Observed reset/data failure requests platform exit; missing invalidation input is UNKNOWN', source_limits='No original stop, fill, slippage, position collision or session risk rule invented here; inherit common parent paper protocol when bound.'),
            dict(id='OCT-DIRECTION-01', classification='NEW_TRADE_TRANSLATION_OF_SOURCE_SCORING', FC='sign(recent raw buy1-sell1), source follow-recent scoring direction', DP='sign(current20 flow ratio), source current-flow scoring direction', EX01='sign(current20 flow ratio), source flow-aligned scoring direction', empty_or_balanced='Keep UNKNOWN or0 directional trial and report it; this file adds no unapproved fixed-side alternative and never pretends empty flow supplies a direction.'),
            dict(id='OCT-SAMPLING-FC', classification='SOURCE_SELECTED_CLOCK_WITH_CAUSAL_GATE', source='Family strict-pre snapshot and start+h outcomes', paper='One attempt per source event ID only after family opportunity actually known; do not use retrospective family identity at strict-pre time', missing='Causal family-opportunity producer unresolved; INPUT_UNAVAILABLE retained'),
            dict(id='OCT-SAMPLING-DP', classification='SOURCE_RECOGNITION_OPPORTUNITY', paper='One attempt per causally emitted recognition candidate, all39 source cells evaluated; finalization-only identities unavailable live and retained'),
            dict(id='OCT-SAMPLING-EX01_continuous', classification='SOURCE_ONSET_SAMPLING', paper='One attempt per source predicate onset; all active seconds separately logged; preserve first-eligible/gap left-censor label and no-birth events'),
            dict(id='OCT-MISSING-01', classification='EXPLICIT_SOURCE_IMPLEMENTATION_CORRECTION', source='S00131:134 near_sign uses sign(fnum(value) or0); pandas comparisons with NaN also collapse toFalse in some original masks', paper='Missing/undefined operands remain UNKNOWN in AST; observed empty counts are explicit0. Retain legacy source report values separately; do not use missing->equal or unknown->false entry gates.')],
        unresolved_source_pointers=index['nonfinite_or_not_resolved_here'],
        source_cells_without_new_predicate_ast=['R existing parent rules', 'ST/FB/supplemental model cells: exact model state required', 'OL source-domain cells: no new predicate invented here', 'RG01 report cells: future/whole-day operands not silently causalized'],
        interpretation='Source-cell inventory is not a count of unique independent strategies.328 predicate/horizon ASTs are conditional templates with missing producers, not328 deployed strategies.')

    # Small semantic checks test causal boundaries, empty-state truth and undefined propagation.
    def context(values, future=None):
        fs = {k: dict(value=v, status='observed', role=DEFS[k]['role'], definition_id=DEFS[k]['definition_id'], known_by_ns='99', known_by_cursor='9') for k,v in values.items()}
        if future: fs[future]['known_by_ns'] = '101'
        return dict(decision_ns='100', decision_cursor='10', fields=fs, definitions={k:DEFS[k]['definition_id'] for k in fs})
    checks = []
    fvals = {'fc.buy1':1, 'fc.sell1':4, 'fc.buy5':2, 'fc.sell5':6, 'fc.buy60':9, 'fc.sell60':2, 'fc.bid_depth':20, 'fc.ask_depth':10}
    assert evaluate(main['original_stack_sell_side'], context(fvals)) is True; checks.append('original sell screen true')
    assert evaluate(main['original_stack_sell_side'], context(fvals, 'fc.buy60')) is UNKNOWN; checks.append('future-known flow cannot activate screen')
    assert evaluate(main['baseline'], context({'fc.buy1':0,'fc.sell1':0,'fc.buy5':0,'fc.sell5':0})) is False; checks.append('observed zero recent direction is not eligible')
    alt = next(r for r in rules if r['id']=='OCTRULE.FC.near_sign.equal.all.h1')
    assert evaluate(alt['source_predicate'], context(fvals)) is UNKNOWN; checks.append('missing near depth never equal')
    dpzero = {'dp.input_available':True,'dp.early_buy':0,'dp.early_sell':0,'dp.late_buy':0,'dp.late_sell':0}
    dr = next(r for r in rules if r['id']=='OCTRULE.DP.both_empty.undefined_flow.h5')
    assert evaluate(dr['source_predicate'], context(dpzero)) is True
    assert evaluate(dr['direction'], context(dpzero)) is UNKNOWN; checks.append('observed both-empty state true but price direction undefined')
    dpbal = {'dp.input_available':True,'dp.early_buy':2,'dp.early_sell':2,'dp.late_buy':3,'dp.late_sell':3,'dp.bid_lots':5,'dp.ask_lots':2}
    br = next(r for r in rules if r['id']=='OCTRULE.DP.steady.balanced.h5')
    assert evaluate(br['source_predicate'], context(dpbal)) is True
    assert evaluate(br['direction'], context(dpbal)) == 0; checks.append('nonempty balanced flow is defined0, distinct from empty')
    ev = {'ex.input_available':True,'ex.before_buy':3,'ex.before_sell':1,'ex.roll_buy':0,'ex.roll_sell':0}
    assert evaluate(predicates['flow_vanished'], context(ev)) is True
    assert evaluate(sign(er), context(ev)) is UNKNOWN; checks.append('flow vanished detected from counts without assigning direction')
    assert evaluate(predicates['flow_vanished'], context({k:v for k,v in ev.items() if k!='ex.roll_sell'})) is UNKNOWN; checks.append('missing roll sell is not empty0')
    # AST expression binding and cardinality validation for every template.
    for r in rules: validate_rule(r)
    payload = dict(schema='october-predicate-rules/v1', execution_enabled=False, paper_included=True,
                   feature_definitions=DEFS, rules=rules, source_recipe='review_october_recipes.json',
                   decisions='OCTOBER_RULE_DECISIONS.json', unresolved_source_pointers=index['nonfinite_or_not_resolved_here'])
    write('OCTOBER_PREDICATE_RULES.json', payload)
    write('OCTOBER_RULE_DECISIONS.json', decisions)
    validation = dict(source_cell_count=len(cells), source_cell_counts=counts, base_generator_counts=base_counts, predicate_rule_count=len(rules),
                      predicate_counts={'FC':259,'DP':39,'EX01_continuous':30}, checks=checks,
                      model_instance_count=len(instances), model_instances_by_family={'ST':1155,'FB':840,'canonical_supplemental':12},
                      identical_metric_split_alias_count=sum(bool(x.get('identical_metrics_and_splits_alias_of')) for x in instances),
                      model_instance_uncompressed_sha256=hashlib.sha256(model_blob).hexdigest(),
                      contract_all_rules_valid=True, execution_enabled=False, replay_or_refit_performed=False,
                      source_cell_uncompressed_sha256=hashlib.sha256(blob).hexdigest(),
                      inputs_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in ('october_expansion_index.json','review_october_recipes.json','supplemental_reanalysis_models.json')})
    write('OCTOBER_VALIDATION.json', validation)
    print(json.dumps(validation, indent=2))

if __name__ == '__main__':
    build()
