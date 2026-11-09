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
# Separate inherited scientific caveats from a claim that an input artifact is physically absent.
for x in records:
 if x['kind']=='framework':
  fi=int(x['recipe_ref']['json_pointer'].split('/')[-1]);f=data['framework_recipes'][fi]
  x['source_limitations']=copy.deepcopy(f['irreducible_missing_inputs'])
  x['unavailable_artifacts']=[{'artifact':'live causal feature producer bindings','status':'not_verified_or_bound'},{'artifact':'platform execution adapter','status':'not_bound'}]
 if x['kind']=='model_task':
  x['artifact_dependencies']=x.pop('unavailable_artifacts')
  x['unavailable_artifacts']=[{'artifact':'platform execution adapter','status':'not_bound'}]
  if x['model_artifact_status']=='weights_not_serialized_by_reviewed_completed_run_path':x['unavailable_artifacts'].append({'artifact':'frozen fitted coefficients/tree state','status':'not_serialized_by_reviewed_completed_run_path','substitution_allowed':False})

# A detector opportunity is shared;one arm must never mutate another arm's onset state.
corrections.append({'correction_id':'LC-EARLY-SHARED-STATE','target_recipe_refs':[ptr('/lifecycle_rules')],'issue':'LC03 and LC04 arms reuse previous_early_eligible;updating it per horizon/direction would erase later arms at the same group.','disposition':'Evaluate detector once per instrument/continuity/side/completed group against an immutable prior-state snapshot;broadcast the same eligible/onset result to every arm;commit next state once after all arm evaluations. No new signal math.'})
for r in records:
 r['correction_policy']={'known_wrong_math_or_clocks':'preserve_as_history_only_never_activate_as_alternative_claim','corrected_definition':'new_version_with_explicit_supersession_link','hypothesis_retained':True}
 if r['kind']=='lifecycle' and r['identity']['source_candidate'] in ['LC03','LC04']:
  r['detector_state_contract']={'scope':['instrument','continuity_id','side'],'evaluation_clock':'each completed book group','state_update_order':'read prior snapshot;evaluate once;broadcast to all arms;commit once','initialization':'Set previous_early_eligible=false at algorithm start/reset,tag ALGORITHMIC_INITIALIZATION;this is source detector initialization,not a claim that a prior tape predicate was observed false.','unavailable_history':'No eligibility until3consecutive complete books exist;after a gap reset algorithm state with explicit reset tag.','shared_detector':'LC03 early_falling_touch'}
  r['supplemental_correction_ids'].append('LC-EARLY-SHARED-STATE')
 if r['kind']=='framework':
  r['activation_policy_ref']=ptr('/framework_edge_policy')
  r['activation_policy']='Source recipe event/update/per-prefix schedule when explicitly stated;otherwise first-calculable false-to-true edge of continuous predicate. Initial computable eligible state labelled INITIAL_ELIGIBLE,not observed prior false.'
 if r['kind']=='model_task':
  v=r['identity']['input_version']
  if v in ['joint-models-v1','joint-models-v3']:
   r['implementation_role']='historical_projection_reference_not_current_execution_definition'
   r['activation_allowed_from_this_version']=False
   r['historical_scope_note']='Preserve executed model/output/fold identity as evidence. A historical projection is not a substitute for expanded corrected inputs. Proven erroneous clocks/math must remain history,not a new scientific strategy.'
   if v=='joint-models-v1':r['known_version_correction']='Source checkpoint reports10valid elapsed-duration identities accidentally omitted;v2input corrected those omissions,no v2fits. Do not silently relabel v1 as corrected.'
   else:r['known_version_correction']='V3 remains frozen partial-projection benchmark;expanded candidate preserves its values while adding native/ROOT/history inputs. Semantic completeness not certified.'
  else:
   r['implementation_role']='expanded_source_candidate_definition_pending_recovery_and_binding'
   r['activation_allowed_from_this_expansion']=False
   r['semantic_coverage_status']='NOT_PASSED_in_source;input_and_unit_consumer_ledger_unresolved'

# Bounded validation:strict expressions,bindings,identity cardinalities and UNKNOWN handling. No market-data calculation.
ids=set();raw_hash=hashlib.sha256();by_version=collections.Counter();by_template=collections.Counter();by_framework=collections.Counter();seen_model_instance=set()
for r in records:
 assert r['paper_included'] is True and r['execution_enabled'] is False
 assert r['id'] not in ids;ids.add(r['id'])
 validate_rule(r)
 for e in r.get('context_tags',{}).values():validate_expression(e)
 for metadata in r['requires'].values():
  assert metadata['required_runtime_status']=='observed'
  assert metadata['runtime_binding_verified'] is False and metadata['availability_asserted'] is False
 unknown=evaluate_rule(r,{'decision_ns':'100','decision_cursor':'10','fields':{}})
 assert unknown['condition'] is UNKNOWN
 counts[r['kind']]+=1
 if r['kind']=='model_task':
  identity=r['identity'];key=canonical(identity);assert key not in seen_model_instance;seen_model_instance.add(key)
  by_version[identity['input_version']]+=1;by_template[identity['template_id']]+=1
 elif r['kind']=='framework':by_framework[r['identity']['framework_id']]+=1
 for n in fields_in([r['entry'],r['direction'],r['exit']]):assert n in r['requires']
 # Validate serialized form cannot contain nonfinite numbers.
 canonical(r)
assert counts['lifecycle']==270
assert counts['model_task']==sum(mapping_expansion.values())
assert counts['framework']==sum(framework_expansion.values())
assert len(seen_tasks)==4581 and len(framework_expansion)==31
assert dict(by_framework)==framework_expansion

# Strict clock/status/role positive+negative smoke checks on exactly one source LC predicate.
early=next(r for r in records if r['kind']=='lifecycle' and r['identity']['recipe_rule_id']=='LC03-B-h1-source_directed')
vals={'book.instrument':1,'book.prev_instrument':1,'book.prev2_instrument':1,'book.continuity_id':'x','book.prev_continuity_id':'x','book.prev2_continuity_id':'x','book.group':12,'book.prev_group':11,'book.prev2_group':10,'book.cursor':120,'book.prev_cursor':110,'book.B.price0':100,'book.B.price1':100,'book.B.price2':100,'book.B.size0':2,'book.B.size1':3,'book.B.size2':4,'state.B.previous_early_eligible':False}
ctx={'decision_ns':'1000','decision_cursor':'120','fields':{n:{'value':v,'known_by_ns':'1000','known_by_cursor':'120','definition_id':early['requires'][n]['definition_id'],'role':early['requires'][n]['role'],'status':'observed'} for n,v in vals.items()}}
assert evaluate_rule(early,ctx)['condition'] is True
for field,attribute,value in [('book.B.size0','status','missing'),('book.B.size0','role','outcome'),('book.B.size0','known_by_ns','1001'),('book.B.size0','known_by_cursor','121'),('book.B.size0','definition_id','different-definition')]:
 c=copy.deepcopy(ctx);c['fields'][field][attribute]=value;assert evaluate_rule(early,c)['condition'] is UNKNOWN

# Write deterministic gzip with no filename header and fixed mtime.
gzip_path=DEST/'BROAD_INSTANCES.jsonl.gz'
with gzip_path.open('wb') as rawout:
 with gzip.GzipFile(filename='',fileobj=rawout,mode='wb',mtime=0,compresslevel=9) as out:
  for r in records:
   line=(canonical(r)+'\n').encode('utf-8');raw_hash.update(line);out.write(line)
correction_doc={'schema':'broad-expansion-supplemental-corrections-v1','source_recipe':{'path':str(RECIPE),'sha256':recipe_sha},'evidence_policy':'Original recipe/evidence not overwritten;generated machine records apply these design-label corrections.','corrections':corrections}
write_json(DEST/'BROAD_SUPPLEMENTAL_CORRECTIONS.json',correction_doc)
# Read-back count/inclusion/IDs and uncompressed hash.
backhash=hashlib.sha256();backids=set();backcounts=collections.Counter()
with gzip.open(gzip_path,'rb') as f:
 for line in f:
  backhash.update(line);r=json.loads(line);assert r['id'] not in backids;backids.add(r['id']);backcounts[r['kind']]+=1
  assert r['paper_included'] is True and r['execution_enabled'] is False
assert backids==ids and backcounts==counts and backhash.hexdigest()==raw_hash.hexdigest()
assert sha(RECIPE)==recipe_sha,'Source recipe was unexpectedly modified'
manifest={'schema':'broad-expansion-manifest-v1','source_recipe':{'path':str(RECIPE),'sha256':recipe_sha},'build_script':{'path':str(Path(__file__).resolve()),'sha256':sha(Path(__file__))},'validator':{'path':str(CONTRACT),'sha256':sha(CONTRACT)},'output':{'path':str(gzip_path),'compressed_sha256':sha(gzip_path),'uncompressed_sha256':raw_hash.hexdigest(),'compressed_bytes':gzip_path.stat().st_size,'records':len(records)},'counts':dict(counts),'input_cardinality':{'model_task_mappings':4581,'lifecycle_expressions':270,'frameworks':31},'model_instances_by_input_version':dict(by_version),'model_instances_by_template':dict(by_template),'framework_instances_by_id':framework_expansion,'model_task_template_cardinalities':mapping_expansion,'lifecycle_supplemental_design_markings':dict(lifecycle_new_markings),'supplemental_corrections':{'path':str(DEST/'BROAD_SUPPLEMENTAL_CORRECTIONS.json'),'sha256':sha(DEST/'BROAD_SUPPLEMENTAL_CORRECTIONS.json'),'records':len(corrections)},'all_paper_included':True,'all_execution_enabled':False,'performance_filters_applied':False,'validation':{'unique_instance_ids':len(ids),'unique_model_task_mappings':len(seen_tasks),'strict_rule_validations':len(records),'empty_input_unknown_checks':len(records),'causal_status_role_clock_cursor_binding_checks':6,'gzip_readback_records':len(backids),'counts_and_hashes_match':True,'source_recipe_unchanged':True},'reproduction':'python machine/build_broad_instances.py;deterministic JSON order,gzip mtime0 and no gzip filename. Rebuild outputs only,does not alter original recipes or evidence.','scope_limits':['Machine expressions depend on unimplemented/unverified causal producers and missing fitted artifacts.','No platform API/import support or feature availability asserted.','No refit,AWS,workers,market-data suite,backtest or orders.','PF06 source recipe mentions3slow indicator operands but lacks a machine indicator axis;expanded daily contexts must not be claimed as3executable slow strategies. See supplemental correction.'],'commentary_policy':'Scientific interpretation/evidence remains in immutable recipe/source pointers and manifest;instance records contain only execution contracts,design identity and explicit dependencies.'}
manifest['implementation_role_counts']=dict(collections.Counter(r.get('implementation_role',r['kind']) for r in records))
manifest['historical_implementation_policy']='Every hypothesis remains included. Exact old version/fold/output records are provenance. Proven wrong math/clocks are not active alternate scientific claims;old projections do not substitute for expanded corrected inputs. No record is execution enabled.'
manifest['detector_state_policy']='LC03/LC04 share one immutable prior-state snapshot per instrument/continuity/side/group;broadcast onset to all horizons/directions then commit once.'
write_json(DEST/'BROAD_EXPANSION.json',manifest)
print(json.dumps({'counts':dict(counts),'records':len(records),'output':str(gzip_path),'sha256':sha(gzip_path),'framework_counts':framework_expansion,'paired_lc_marked_new':lifecycle_new_markings['paired_direction_marked_new']},indent=2))
