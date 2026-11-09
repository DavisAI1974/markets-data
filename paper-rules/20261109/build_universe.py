"""Join preserved inventories without confusing records with independent strategies."""
import collections,gzip,hashlib,json,pathlib
from functools import cache
from paper_rules.contract import validate_rule
ROOT=pathlib.Path(__file__).parent
M=ROOT/'machine'

def read(path):return json.loads(path.read_text(encoding='utf-8'))
def lines(path):return [json.loads(x) for x in gzip.decompress(path.read_bytes()).decode('utf-8').splitlines()]
def save(path,obj):path.write_text(json.dumps(obj,indent=2,ensure_ascii=False,allow_nan=False)+'\n',encoding='utf-8')
@cache
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def zipped(path,rows):
    b=(''.join(json.dumps(r,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n' for r in rows)).encode()
    path.write_bytes(gzip.compress(b,mtime=0))

def build():
    parts=[('broad','BROAD_INSTANCES.jsonl.gz'),('chain','CHAIN_INSTANCES.jsonl.gz'),('october_models','OCTOBER_MODEL_INSTANCES.jsonl.gz')]
    sourceparts={kind:lines(M/name) for kind,name in parts}
    sourceparts['october_predicates']=read(M/'OCTOBER_PREDICATE_RULES.json')['rules']
    sourceparts['initial']=read(M/'INITIAL_RULES_V2.json')['strategies']
    records=[];crosswalk=[];counts={};validated=0
    for kind,rows in sourceparts.items():
        counts[kind]=len(rows)
        for index,r in enumerate(rows):
            identifier=('INITIAL.' if kind=='initial' else '')+r['id']
            file=dict(parts).get(kind,'OCTOBER_PREDICATE_RULES.json' if kind=='october_predicates' else 'INITIAL_RULES_V2.json')
            ref={'path':file,'sha256':digest(M/file),'index':index}
            core={'id':identifier,'paper_included':True,'execution_enabled':False,'family':kind,'definition_ref':ref,'uniform_policy_id':'ALL_PAPER_V1','requires_full_definition':True,'standalone_execution_allowed':False}
            for key in ['activation_allowed_from_this_expansion','activation_allowed_from_this_version','active_math_allowed','implementation_role','state_machine_ref','sampling_policy_ref','activation_policy_ref','template_ref','operand_specification_ref','forecast_score_contract_ref']:
                if key in r:core[key]=r[key]
            if kind in {'broad','october_predicates'}:
                validate_rule(r);validated+=1
                core['program_type']='restricted_predicate_ast'
                for key in ['entry','direction','exit','invalidation','state_updates']:
                    if key in r:core[key]=r[key]
                core['requires']={name:{k:v for k,v in meta.items() if k in {'definition_id','role','value_type','unit'}} for name,meta in r['requires'].items()}
            elif kind=='chain':
                core.update(program_type='parameterized_recipe',recipe=r['recipe'],parameters=r['parameters'],execution_specification=r['execution_specification'],known_prerequisites=r['known_prerequisites'])
            elif kind=='october_models':
                core.update(program_type='unbound_frozen_model',target=r['target'],horizon_s=r['horizon_s'],arm=r['arm'],fold=r['fold'],required_state=r.get('needed_state'),original_fitted_state_required=True,unavailable_binding=r['unavailable_binding'],target_translation_ref=r.get('target_type_recipe_pointer'))
            else:
                core.update(program_type='initial_runtime_specification',engine=r['engine'],parameters=r['parameters'],runtime_ref='INITIAL_RULES_V2.json')
            records.append(core)
            crosswalk.append({'id':identifier,'source':ref,'original_id':r['id'],'paper_included':True,'excluded':False})
    assert len({r['id'] for r in records})==len(records)
    zipped(M/'PAPER_RULE_CORE.jsonl.gz',records)
    zipped(ROOT/'reconciliation/RULE_CROSSWALK.jsonl.gz',crosswalk)
    prior=ROOT.parents[1]/'carry-forward/20261109/HYPOTHESIS_REGISTER.json'
    if not prior.exists():prior=ROOT.parent/'markets-carry-forward-20261109/delivery/HYPOTHESIS_REGISTER.json'
    inherited=read(prior);coverage=[]
    for r in inherited:
        ident=r['id']
        if ident.startswith(('CH','CM','CT')):refs=['review_chain.json','review_chain_recipes.json','machine/CHAIN_INSTANCES.jsonl.gz']
        elif ident.startswith(('ST','FB')):refs=['review_october_recipes.json','machine/OCTOBER_MODEL_INSTANCES.jsonl.gz']
        elif ident.startswith(('FC','DP')) or ident=='EX01':refs=['review_october_recipes.json','machine/OCTOBER_PREDICATE_RULES.json']
        elif ident.startswith(('OL','RG','EX')):refs=['review_october_recipes.json','october_expansion_index.json','machine/OCTOBER_SOURCE_CELLS.jsonl.gz']
        else:refs=['machine/INITIAL_RULES_V2.json']
        coverage.append({'inherited_id':ident,'name':r['name'],'paper_included':True,'dropped':False,'continuation_refs':refs,'original_record':r})
    assert len(coverage)==82 and len({r['inherited_id'] for r in coverage})==82
    save(ROOT/'reconciliation/INHERITED_82_CROSSWALK.json',coverage)
    sourcecells=lines(M/'OCTOBER_SOURCE_CELLS.jsonl.gz')
    assert all(r.get('paper_included') is True for r in sourcecells)
    result={
        'schema':'paper-universe-v1','all_paper_included':True,'performance_exclusions':0,'observation_only_candidates':0,
        'source_records_preserved':14712,'inherited_candidates_carried':82,
        'core_record_count':len(records),'core_counts':counts,'validated_predicate_records':validated,
        'source_report_cells_separate':len(sourcecells),'independent_strategy_count':None,
        'count_interpretation':'Records include versions, folds, aliases, historical implementations and new protocols; counts are not independent strategies.',
        'core':{'path':'PAPER_RULE_CORE.jsonl.gz','sha256':digest(M/'PAPER_RULE_CORE.jsonl.gz')},
        'source_cells':{'path':'OCTOBER_SOURCE_CELLS.jsonl.gz','sha256':digest(M/'OCTOBER_SOURCE_CELLS.jsonl.gz')},
        'execution_enabled':False,'platform_adapter_bound':False,'platform_fills':0,
        'full_semantic_reconciliation_certified':False,
        'standalone_execution_allowed':False,'full_definition_dereference_required':True,
        'required_definition_fields':['detector_state_contract','entry_reference_contract','target_deadline_contract','runtime_requirements','sampling_policy_ref','activation_policy','correction_policy','source_clock','execution_design_ids','readiness'],
        'unresolved_rule_definitions_retained':True,'migration_status':'paused_by_user','research_worker_restarts':0
    }
    save(M/'PAPER_UNIVERSE_MANIFEST.json',result)
    print(json.dumps({k:v for k,v in result.items() if k in {'core_record_count','core_counts','validated_predicate_records','source_report_cells_separate'}}))

if __name__=='__main__':build()
