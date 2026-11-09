"""Expand frozen broad recipes;no source edits,model fits,feeds,orders or worker operations."""
from pathlib import Path
import collections,copy,gzip,hashlib,json,math,sys
ROOT=Path(__file__).resolve().parents[1]
DEST=Path(__file__).resolve().parent
RECIPE=ROOT/'review_broad_recipes.json'
CONTRACT=ROOT/'paper_rules'/'contract.py'
sys.path.insert(0,str(ROOT))
from paper_rules.contract import validate_rule,validate_expression,evaluate_rule,UNKNOWN,fields_in

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def canonical(obj):return json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False)
def write_json(path,obj):path.write_text(json.dumps(obj,indent=2,ensure_ascii=False,allow_nan=False)+'\n',encoding='utf-8')
def ptr(pointer):return {'artifact':'review_broad_recipes.json','sha256':recipe_sha,'json_pointer':pointer}
def F(n):return {'field':n,'definition_id':'broad-paper-v1:'+n}
def op(name,*args):return {'op':name,'args':list(args)}
def C(v):return {'const':v}
def requirement(name):
 return {'definition_id':'broad-paper-v1:'+name,'role':'execution_state' if name.startswith('execution.') else 'decision_state' if name.startswith(('state.','opportunity.')) else 'feature'}
def bind_requires(exprs,provided):
 out=copy.deepcopy(provided)
 for n in set(fields_in(exprs)):
  if n not in out:out[n]=requirement(n)
 for n,m in out.items():
  m.update({'runtime_binding_verified':False,'availability_asserted':False,'required_runtime_status':'observed','runtime_clock_fields_required':['known_by_ns','known_by_cursor'],'runtime_producer_status':'not_bound_by_this_expansion'})
 return out

def horizon(h):
 if type(h) not in (int,float) or not math.isfinite(h) or h<=0 or int(h)!=h:raise ValueError('Nonfinite/nonpositive/noninteger horizon')
 return int(h)

def make_base(kind,identity,recipe_pointer,source_refs):
 key=canonical({'kind':kind,'identity':identity,'recipe_artifact_sha256':recipe_sha,'recipe_pointer':recipe_pointer})
 return {'schema':'broad-paper-machine-instance-v1','id':'BROAD-'+hashlib.sha256(key.encode()).hexdigest(),'kind':kind,'identity':identity,'paper_included':True,'execution_enabled':False,'feature_availability_asserted':False,'platform_support_verified':False,'platform_adapter_status':'not_bound','recipe_ref':ptr(recipe_pointer),'source_refs':copy.deepcopy(source_refs),'unavailable_artifacts':[],'runtime_requirements':['Causal feature producer bindings','Strict observed-status/role/definition/known-by clock and cursor metadata','Isolated platform paper attribution and actual execution reports'],'order_submission_authorized_by_this_file':False}

def fixed_exit(h,anchor):
 return {'after_ns':str(h*1_000_000_000),'anchor':anchor,'condition':op('ge',F('opportunity.decision_ns'),F('opportunity.target_deadline_ns')),'target_deadline_policy':'immutable','late_submission_policy':'NO_ENTRY_EXPIRED'}

raw=RECIPE.read_bytes();recipe_sha=hashlib.sha256(raw).hexdigest();data=json.loads(raw)
assert len(data['lifecycle_rules'])==270
assert len(data['model_task_recipe_mappings'])==4581
assert len(data['framework_recipes'])==31
records=[];corrections=[];counts=collections.Counter();mapping_expansion={};framework_expansion={};lifecycle_new_markings=collections.Counter()
# Frozen source recipe is preserved. Corrections only affect generated instances.
for i,r in enumerate(data['lifecycle_rules']):
 identity={'source_candidate':r['source_candidate'],'recipe_rule_id':r['id'],'arm':r['arm'],'horizon_s':horizon(r['horizon_seconds'])}
 x=make_base('lifecycle',identity,f'/lifecycle_rules/{i}',r['sources'])
 for key in ['entry','direction','exit']:x[key]=copy.deepcopy(r[key])
 x['requires']=bind_requires([x['entry'],x['direction'],x['exit']],r['requires'])
 x['entry_reference_contract']='First strictly subsequent completed quote with known_by>=signal_known_by+1000000;same instrument/continuity. Quote reference is not a fill.'
 x['target_deadline_contract']='entry_reference_ns+horizon_s*1000000000;never shift on actual delayed fill.'
 x['state_machine_ref']=ptr(f'/lifecycle_rules/{i}/state_updates') if r.get('state_updates') else None
 choices=list(r.get('new_design_choices',[]));new=[]
 if r['arm'] in ['paired_long','paired_short']:
  new.append('NEW_PAPER_DESIGN:paired direction is an independent comparison arm,not the source-directed rule;includes directions contrary to source signal.')
  lifecycle_new_markings['paired_direction_marked_new']+=1
 if r['source_candidate']=='LC04':
  new.append('NEW_PAPER_DESIGN:strict fresh/rolling-flow contextual partition added aroundLC03;original availability comparison did not implement these selection arms.')
  lifecycle_new_markings['lc04_context_marked_new']+=1
 new.append('NEW_PAPER_EXECUTION:actual platform orders/fills are not established by historical source quote-crossing replay.')
 x['design_classification']='new_paper_comparison' if r['arm'] in ['paired_long','paired_short'] or r['source_candidate']=='LC04' else 'source_trigger_direction_with_new_platform_execution'
 x['design_choices']=choices+new
 correction={'correction_id':'LC-DESIGN-'+r['id'],'target_recipe_ref':ptr(f'/lifecycle_rules/{i}'),'original_new_design_choices':r.get('new_design_choices',[]),'supplemental_new_design_choices':new,'reason':'Frozen recipes lost explicit NEW marking while correcting exit anchors;paired and context arms must not be represented as original source rules.'}
 corrections.append(correction);x['supplemental_correction_ids']=[correction['correction_id']]
 x['unavailable_artifacts']=['Live completed-book/action producer binding not verified','Platform execution adapter not implemented by audit']
 x['opportunity_policy']={'emit_before_input_evaluation':True,'unknown':'INPUT_UNAVAILABLE','false':'NO_TRIGGER','true_but_unfilled':'NO_FILL_OR_EXPLICIT_NO_ENTRY_REASON','zero_direction':'ZERO_DIRECTION_NO_ORDER','return_for_unfilled':None}
 records.append(x)

# Every exact version/fold/model/target/task maps to ALL specified templates.
seen_tasks=set()
for i,t in enumerate(data['model_task_recipe_mappings']):
 taskkey=(t['input_version'],t['task_id'],t['model'],t['feature_variant'],t['target'],horizon(t['horizon_s']),t['fold'])
 assert taskkey not in seen_tasks;seen_tasks.add(taskkey)
 tids=t['recipe_templates'];assert tids and len(tids)==len(set(tids))
 mapping_expansion[t['input_version']+'::'+t['task_id']]=len(tids)
 for tid in tids:
  template=data['model_recipe_templates'][tid]
  identity={'task_id':t['task_id'],'input_version':t['input_version'],'model':t['model'],'feature_variant':t['feature_variant'],'target':t['target'],'horizon_s':horizon(t['horizon_s']),'fold':t['fold'],'template_id':tid}
  x=make_base('model_task',identity,f'/model_task_recipe_mappings/{i}',[t['source']]);x['template_ref']=ptr('/model_recipe_templates/'+tid)
  x['entry']=copy.deepcopy(template['entry']);x['direction']=copy.deepcopy(template['direction']);x['exit']=fixed_exit(identity['horizon_s'],'opportunity.origin_ns')
  x['requires']=bind_requires([x['entry'],x['direction'],x['exit']],template['requires'])
  x['design_classification']='source_signed_activation_with_new_platform_execution' if tid=='signed_source_spread' else 'new_target_type_paper_translation'
  x['design_choices']=['NEW:causal prospective1-second completed-group sampler replaces retrospective selected-phase opportunity schedule;source history retained separately.']
  if tid!='signed_source_spread':x['design_choices'].append('NEW:target-type direction/context translation;not a recovered historical source trade.')
  x['model_artifact_status']=t.get('artifact_availability','not_individually_verified')
  x['unavailable_artifacts']=[{'artifact':'frozen model state/preprocessing/feature schema','status':x['model_artifact_status'],'substitution_allowed':False},{'artifact':'live exact feature producer bindings','status':'unverified'},{'artifact':'platform execution adapter','status':'not_bound'}]
  x['sampling_policy_ref']=ptr(f'/model_task_recipe_mappings/{i}/sampling_design')
  x['forecast_score_contract_ref']=ptr(f'/model_task_recipe_mappings/{i}/forecast_scoring')
  x['raw_output_policy']={'new_clipping':False,'finite_out_of_support':'retain_output_context_and_tag','inherited_source_transform':'retain_versioned;raw_pretransform_only_if_observed','target_outcome_role':'outcome_only_never_entry','no_fill_return':None}
  if t['target']=='absolute_mid_price_change':x['context_tags']={'invalid_target_support':op('lt',F('model.prediction'),C(0))}
  elif t['target']=='first_observed_family_within_h':x['context_tags']={'invalid_probability_support':op('or',op('lt',F('model.prediction'),C(0)),op('gt',F('model.prediction'),C(1)))}
  else:x['context_tags']={'zero_prediction':op('eq',F('model.prediction'),C(0))}
  records.append(x)

# Directions are explicit recipe arms;retain separately labelled directional operationalization even when its order sign duplicates a paired control.
for i,f in enumerate(data['framework_recipes']):
 directions=[(name,direction,'new_paired_context_direction') for name,direction in f['long_short_arms'].items()]
 if 'new_directional_operationalization' in f:directions.append(('new_directional_operationalization',f['new_directional_operationalization'],'new_hypothesis_direction_operationalization'))
 assert len({n for n,_,_ in directions})==len(directions)
 hs=f['horizons_s'];assert len(hs)==len(set(hs))
 framework_expansion[f['id']]=len(directions)*len(hs)
 for h in hs:
  for arm,direction,classification in directions:
   identity={'framework_id':f['id'],'direction_arm':arm,'horizon_s':horizon(h)}
   x=make_base('framework',identity,f'/framework_recipes/{i}',f['source_refs'])
   x['entry']=copy.deepcopy(f['condition_expression']);x['direction']=copy.deepcopy(direction);x['exit']=fixed_exit(identity['horizon_s'],'opportunity.origin_ns')
   x['requires']=bind_requires([x['entry'],x['direction'],x['exit']],f['requires'])
   x['design_classification']=classification;x['design_choices']=copy.deepcopy(f['new_design_choices'])
   x['operand_specification_ref']=ptr(f'/framework_recipes/{i}/operand_definitions');x['sampling_policy_ref']=ptr(f'/framework_recipes/{i}/opportunity_sampling')
   x['feature_producer_status']='specified_not_implemented_or_bound_by_audit'
   x['unavailable_artifacts']=[{'artifact':s,'status':'irreducible_source_input_or_math_unresolved'} for s in f['irreducible_missing_inputs']]+[{'artifact':'all live causal feature producers','status':'unverified'},{'artifact':'platform execution adapter','status':'not_bound'}]
   x['opportunity_policy']={'unknown':'INPUT_OR_MODEL_UNAVAILABLE','false':'NO_TRIGGER','finite_context_out_of_support':'retain_with_tag_not_automatic_drop','no_fill_return':None}
   records.append(x)

# Correction preserves unfinished PF06 indicator dimensions without inventing undocumented AST variants.
corrections.append({'correction_id':'PF06-INNER-INDICATOR-DIMENSIONS','target_recipe_ref':ptr('/framework_recipes/'+str(next(i for i,f in enumerate(data['framework_recipes']) if f['id']=='PF06'))),'issue':'PF06 operand text names tsm20,carry,basis_momentum20,but frozen condition only tests daily_decision and has no separate machine indicator axis.','disposition':'Expand exact frozen31-framework directions/horizons as requested;PF06 records are contextual daily-opportunity trials,not proof that3indicator-specific strategies were materialized. Preserve all3input definitions via recipe pointer. Additional indicator-specific activation/direction variants require explicit supplemental recipe,not fabricated here.','blocks_claim':'Do not claim all3slow strategies executable from these PF06 records.'})
