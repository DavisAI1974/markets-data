"""Recover117frozen constant predictors from original full-precision statistics. No fitting."""
from pathlib import Path
import csv,io,json,hashlib,math,struct,gzip,collections
ROOT=Path(__file__).resolve().parents[1];OUT=Path(__file__).resolve().parent
CACHE=Path(r'E:/Markets/outputs/research-union-20261109/objects')
CATALOG=Path(r'C:/Users/A/markets-carry-forward-20261109/source_catalog.json')
RAW_SHA='5d9e550ebccfd63bf47cbea93643d1325ccf0870'
PRESENTATION_SHA='49758d03d1a77a309088ff831a0cfd6990296f11'
CORE_SHA='dc94b4ded3be7318d7457be9a79cce96c097a76e'
WRAPPER_SHA='e0cb217370e5727afc77f960623548f305bec313'
cat=json.loads(CATALOG.read_text(encoding='utf-8'));bysha={}
for r in cat:bysha.setdefault(r['sha'],r)
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False)
def digest(b):return hashlib.sha256(b).hexdigest()
def filehash(p):return digest(p.read_bytes())
def src(s,line1=None,line2=None):
 r=bysha[s];o={'git_blob_sha':s,'path':r['path'],'url':r['url']}
 if line1 is not None:o['line_range']=[line1,line2 or line1];o['url']+=f'#L{line1}-L{line2 or line1}'
 return o
verified={}
def read(s):
 b=(CACHE/s).read_bytes();actual=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();assert actual==s
 verified[s]=src(s)|{'sha256':digest(b),'bytes':len(b),'git_blob_verified':True};return b.decode('utf-8')
def write(p,o):p.write_text(json.dumps(o,indent=2,ensure_ascii=False,allow_nan=False)+'\n',encoding='utf-8')
def key(r):return (r['outcome'],str(r['horizon_s']),str(r['fold']),r['model'])
# Preserve existing evidence and instance identities byte-for-byte.
protected=[ROOT/'review_broad_model_tasks.json',ROOT/'review_broad_recipes.json',ROOT/'review_broad.json',OUT/'BROAD_INSTANCES.jsonl.gz',OUT/'BROAD_EXPANSION.json']
before={str(p):filehash(p) for p in protected}
raw_text=read(RAW_SHA);core=read(CORE_SHA);wrapper=read(WRAPPER_SHA);read(PRESENTATION_SHA)
assert 'mu=mean(y)' in core
assert 'if modelname in ["training_frequency","training_mean"]\n                    pred=fill(mu,length(test))' in core
assert 'elseif modelname=="zero_change"\n                    pred=zeros(length(test))' in core
assert 'binary && (pred=clamp.(pred,1e-6,1-1e-6))' in core
assert 'train_label_mean=mu' in core
assert "src=(scripts/'run_joint_models.jl').read_text()" in wrapper
# Wrapper alters dispatch/matrix caching,not mu,constant assignments or clamp.
for l in wrapper.splitlines():
 if 'text=once(' in l or 'text=text.replace(' in l:assert not any(s in l for s in ['mu=mean','pred=fill(mu','pred=zeros','train_label_mean=mu','pred=clamp'])
reader=csv.DictReader(io.StringIO(raw_text));source_rows={};source_lines={}
for r in reader:
 k=key(r);assert k not in source_rows;source_rows[k]=r;source_lines[k]=reader.line_num
assert len(source_rows)==2151
alltasks=json.loads((ROOT/'review_broad_model_tasks.json').read_text(encoding='utf-8'))['tasks']
tasks=[t for t in alltasks if t['state_status']=='constant_reference_reconstructable_from_recorded_training_statistic']
assert len(tasks)==117 and collections.Counter(t['model'] for t in tasks)=={'training_mean':54,'training_frequency':9,'zero_change':54}
ids={t['task_id'] for t in tasks};assert len(ids)==117
instance_links=collections.defaultdict(list)
with gzip.open(OUT/'BROAD_INSTANCES.jsonl.gz','rt',encoding='utf-8') as f:
 for line in f:
  r=json.loads(line)
  if r['kind']=='model_task' and r['identity']['task_id'] in ids and r['identity']['input_version']=='joint-inputs-v4-candidate-20261022':instance_links[r['identity']['task_id']].append(r['id'])
assert set(instance_links)==ids
states=[];checks=[];precision_differences=[];output_precision_differences=[]
for t in tasks:
 k=(t['outcome'],str(t['horizon_s']),str(t['fold']),t['model']);r=source_rows[k];line=source_lines[k]
 assert t['model'] in ['training_mean','training_frequency','zero_change'] and t['model']!='training_median'
 assert all(r[n]==t['source_result_preserved'][n] for n in ['outcome','horizon_s','fold','model','train_n','test_n','fitted_columns'])
 mu_literal=r['train_label_mean'];mu=float(mu_literal);assert math.isfinite(mu)
 original_reported=t['source_result_preserved']['train_label_mean']
 if mu_literal!=original_reported:precision_differences.append({'task_id':t['task_id'],'original_source_literal':mu_literal,'presentation_literal':original_reported})
 if t['model']=='zero_change':
  pre=0.0;value=0.0;mapping='prediction=0.0 for every input;source zeros(length(test));recorded train_label_mean is provenance only and is NOT used.';operands={'source_constant_literal':'0.0'}
 elif t['model']=='training_mean':
  pre=mu;value=mu;mapping='prediction=Float64(original_recorded_train_label_mean);source pred=fill(mu,length(test)),mu=mean(training_y),metric train_label_mean=mu. No mean is recomputed.';operands={'original_train_label_mean_literal':mu_literal,'column':'train_label_mean'}
 else:
  assert t['outcome']=='first_observed_family_within_h'
  pre=mu;value=min(max(mu,1e-6),1-1e-6);mapping='prediction=clamp(Float64(original_recorded_train_label_mean),Float64(1e-6),Float64(1-1e-6));preserves ORIGINAL producer binary clamp;no new fit or new clipping policy.';operands={'original_train_label_mean_literal':mu_literal,'column':'train_label_mean','source_lower_bound_literal':'1e-6','source_upper_bound_expression':'1-1e-6'}
 assert math.isfinite(value)
 old_value=0.0 if t['model']=='zero_change' else float(original_reported)
 if t['model']=='training_frequency':old_value=min(max(old_value,1e-6),1-1e-6)
 if struct.pack('>d',old_value)!=struct.pack('>d',value):output_precision_differences.append({'task_id':t['task_id'],'rounded_table_output':old_value,'recovered_original_output':value,'difference':value-old_value})
 payload={'task_id':t['task_id'],'input_version':t['input_version'],'target':t['outcome'],'horizon_s':t['horizon_s'],'fold':t['fold'],'model':t['model'],'feature_variant':t['feature_variant'],'source_statistic':{'source':src(RAW_SHA,line),'source_artifact_sha256':verified[RAW_SHA]['sha256'],'train_n':int(r['train_n']),'train_label_mean_literal':mu_literal,'original_csv_row_sha256':digest(raw_text.splitlines()[line-1].encode('utf-8'))},'reconstruction':{'mathematical_mapping':mapping,'operands':operands,'output_value':value,'output_binary64_hex':struct.pack('>d',value).hex(),'output_float_hex':value.hex(),'pre_transform_value':pre,'pre_transform_binary64_hex':struct.pack('>d',pre).hex(),'source_clamp_changed_value':pre!=value,'trained_weights_required':False,'feature_matrix_required_for_scalar_inference':False,'no_refit':True},'producer_evidence':[src(CORE_SHA,35,38),src(CORE_SHA,55,58),src(CORE_SHA,83),src(CORE_SHA,94),src(WRAPPER_SHA,75,105)]}
 state={'state_id':'CONSTANT-'+t['task_id'],'paper_included':True,'execution_enabled':False,'resolution_status':'RECONSTRUCTED_FROZEN_CONSTANT_FROM_ORIGINAL_RECORDED_STATISTIC','state_payload':payload,'state_payload_sha256':digest(canonical(payload).encode('utf-8')),'original_task_source_ref':t['source'],'immutable_broad_instance_ids':instance_links[t['task_id']],'remaining_dependencies':['Causal opportunity sampler and immutable target deadline','Current quote/feed where entry translation requires it','Runtime field status/role/definition and known-by clock/cursor bindings','Platform paper adapter and actual execution reports'],'not_a_claim':['Trained model weights recovered','Whole feature provider available','Historical selected-phase sample reproduced prospectively','Platform strategy import or execution verified']}
 states.append(state)
 # Same saved cohort metric identity checks;outcome summaries are used ONLY to verify recovery,never as state operands.
 if t['model']=='training_frequency':
  testmean=float(r['test_label_mean']);derived=value*value-2*value*testmean+testmean;reported=float(r['brier']);assert math.isclose(derived,reported,rel_tol=1e-12,abs_tol=1e-14)
  checks.append({'task_id':t['task_id'],'check':'Brier constant identity p^2-2p*test_mean+test_mean','difference':derived-reported,'verification_only_not_inference_operand':True})
 if t['model']=='training_mean':
  zero=source_rows[(k[0],k[1],k[2],'zero_change')];assert zero['test_n']==r['test_n']
  derived=float(zero['rmse'])**2-2*value*float(r['test_label_mean'])+value*value;reported=float(r['rmse'])**2;assert math.isclose(derived,reported,rel_tol=1e-11,abs_tol=1e-14)
  checks.append({'task_id':t['task_id'],'check':'MSE(p)=MSE(0)-2p*test_mean+p^2','difference':derived-reported,'verification_only_not_inference_operand':True})
assert len(states)==117 and len(checks)==63
assert not any(s['state_payload']['model']=='training_median' for s in states)
output={'schema':'frozen-constant-model-state-v1','scope':'117expanded-candidate constant reference tasks only;not older projections or median references.','original_full_precision_source':verified[RAW_SHA],'producer_sources':[verified[CORE_SHA],verified[WRAPPER_SHA]],'reconstruction_policy':'Read exact original recorded statistic;do not calculate training means from samples,fit a model,substitute a median,or infer original precision from rounded presentation table.','states':states,'all_execution_disabled':True,'trained_model_recovery_claimed':False,'platform_readiness_claimed':False}
write(OUT/'CONSTANT_MODEL_STATE.json',output)
# Readback/re-hash every state and preserve all preexisting missing-state records unchanged.
back=json.loads((OUT/'CONSTANT_MODEL_STATE.json').read_text(encoding='utf-8'))
for s in back['states']:
 assert digest(canonical(s['state_payload']).encode('utf-8'))==s['state_payload_sha256']
 v=s['state_payload']['reconstruction']['output_value'];assert struct.pack('>d',v).hex()==s['state_payload']['reconstruction']['output_binary64_hex']
 assert s['execution_enabled'] is False
unchanged={str(p):filehash(p) for p in protected};assert unchanged==before
remaining=collections.Counter(t['state_status'] for t in alltasks if t['task_id'] not in ids)
resolution={'schema':'constant-state-resolution-v1','output':{'path':str(OUT/'CONSTANT_MODEL_STATE.json'),'sha256':filehash(OUT/'CONSTANT_MODEL_STATE.json'),'states':117},'counts_by_model':dict(collections.Counter(t['model'] for t in tasks)),'resolution_scope':'Scalar frozen prediction state resolved for117expanded tasks;all preexisting broad IDs and evidence bytes untouched. Supplemental resolver keyed by task ID,input version and fold.','remaining_expanded_model_state_counts':dict(remaining),'median_policy':'54training_median references are explicitly unresolved;train_label_mean never substitutes for median.','precision_recovery':{'source':'Original source/all_model_fold_metrics.csv,not rounded tables/all_2151_fold_metrics.csv','tasks_with_different_source_literal':len(precision_differences),'differences':precision_differences},'producer_validation':'Original Julia assigns pred=fill(mu) for training_mean/frequency,zero for zero_change,records train_label_mean=mu and clamps binary predictions. Candidate wrapper preserves these expressions;only dispatch/matrix-preprocessing storage changed.','metric_identity_checks':checks,'field_binding_note':'Constant scalar inference has no feature-matrix dependency. Do not silently mark a broad model.input_contract_complete field observed:an adapter must explicitly bind the frozen constant prediction contract and separate opportunity/execution input requirements. This file changes no recipe or runtime binding.','original_artifacts_unchanged':before,'verified_original_sources':list(verified.values()),'build_script':{'path':str(Path(__file__).resolve()),'sha256':filehash(Path(__file__))},'no_refit':True,'no_worker_or_aws_operation':True,'platform_ready':False}
resolution['precision_recovery']['prediction_outputs_differing_from_rounded_table']=len(output_precision_differences)
resolution['precision_recovery']['output_differences']=output_precision_differences
resolution['precision_recovery']['clarification']=f'The{len(precision_differences)}differing train-statistic literals include zero-reference rows where train mean is not used;{len(output_precision_differences)}prediction outputs differ in binary64from parsing the rounded table.'
write(OUT/'CONSTANT_MODEL_STATE_RESOLUTION.json',resolution)
readme='''# Reconstructed frozen constant predictors

`CONSTANT_MODEL_STATE.json` resolves scalar prediction state for 117 expanded-candidate reference tasks: 54 training means, 9 training frequencies, and 54 exact zero-change references. Each state retains its original task ID, input version, target, horizon, fold, source line/blob, original decimal literal, binary64 representation, mathematical mapping, and SHA256.

The values come from the original full-precision `source/all_model_fold_metrics.csv`. The presentation table rounds these statistics and is not used to reconstruct values. Original Julia producer assignments and the candidate wrapper were inspected and Git-blob verified. The original binary probability clamp is retained as an explicit source transformation.

This is reconstruction of frozen constants, not recovery of trained weights or a refit. No training data were recomputed. No training mean substitutes for any of the 54 median references; those remain unresolved. All other missing or unverified states remain unchanged.

The resolution is supplemental. Original recipes, evidence, broad instance IDs and their execution-disabled state are unchanged. A runtime adapter must bind these constants explicitly; no feature/provider availability or platform support is asserted. Causal opportunities, target deadlines, execution inputs and actual platform fills remain necessary.

`CONSTANT_MODEL_STATE_RESOLUTION.json` records provenance, precision differences, 63 saved-metric identity checks, remaining dependencies, and hashes. Reproduce with `python machine/build_constant_model_state.py`.
'''
(OUT/'CONSTANT_MODEL_STATE_README.md').write_text(readme,encoding='utf-8')
print(json.dumps({'states':117,'by_model':resolution['counts_by_model'],'full_precision_literal_differences':len(precision_differences),'metric_identity_checks':len(checks),'output_sha256':resolution['output']['sha256'],'remaining_expanded_states':dict(remaining),'original_files_unchanged':True},indent=2))
