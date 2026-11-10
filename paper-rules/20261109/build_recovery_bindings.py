"""Publish supplemental source recovery without rewriting prior research evidence."""
import hashlib
import json
from pathlib import Path
from paper_rules.recovered import verify_recovery

ROOT=Path(__file__).resolve().parent

def read(path):return json.loads((ROOT/path).read_text(encoding='utf-8'))
def write(path,value):(ROOT/path).write_text(json.dumps(value,indent=2,allow_nan=False)+'\n',encoding='utf-8')
def ref(path):return dict(path=path,sha256=hashlib.sha256((ROOT/path).read_bytes()).hexdigest())

def main():
    models=verify_recovery(ROOT)
    median=read('recovery/model_source_audit/MEDIAN_SCALAR_RECOVERY.json')
    tasks={t['task_id']:t for t in read('review_broad_model_tasks.json')['tasks']}
    recovered=[];unresolved=[]
    for task in median['tasks']:
        original=tasks[task['task_id']]
        assert original['model']=='training_median'
        assert all(original[k]==task[k] for k in ['outcome','horizon_s','fold'])
        record=dict(task_id=task['task_id'],paper_included=True,execution_enabled=False,
                    target=task['outcome'],horizon_s=task['horizon_s'],fold=task['fold'],
                    input_version=original['input_version'],
                    evidence_pointer='/tasks/'+str(median['tasks'].index(task)),
                    evidence=ref('recovery/model_source_audit/MEDIAN_SCALAR_RECOVERY.json'))
        if task['recovery_status']=='exact_zero_constant_recovered_from_saved_constant_predictions':
            assert task['scalar']==0 and all(float(d['mean_prediction'])==0 for d in task['diagnostics'])
            recovered.append(dict(record,model='training_median',value=0.0,refit=False))
        else:unresolved.append(dict(record,status='ORIGINAL_NONZERO_SCALAR_BITS_UNCERTIFIED'))
    assert len(recovered)==22 and len(unresolved)==32
    write('machine/RECOVERY_BINDINGS.json',dict(schema='supplemental-source-recovery-v1',
        previous_constant_states=ref('machine/CONSTANT_MODEL_STATE.json'),
        recovered_median_states=recovered,unresolved_median_states=unresolved,
        total_resolved_constant_states=117+len(recovered),
        m0_m1_source_binding=ref('recovery/model_source_audit/M0M1_BINDING_RECOVERY.json'),
        ol_ex_source_binding=ref('recovery/ol_ex_source_bound_definitions.json'),
        ol_ex_boundary_checks=ref('recovery/ol_ex_independent_boundary_fixtures.json'),
        runtime_components=[ref(p) for p in ['paper_rules/recovered.py','paper_rules/source_events.py','paper_rules/source_information.py','paper_rules/models.py']],
        paper_included=True,execution_enabled=False,
        remaining=['Source recognition detector and normalized complete-group/flow feed adapter',
                   'Historical floating-library bit parity is not established; present numpy version is recorded separately',
                   'Remaining fitted states, full corpus semantic reconciliation, order ownership and platform execution'],
        migration='paused',research_workers_restarted=0,platform_fills=0))
    write('machine/MODEL_BINDING_REQUIREMENTS.json',dict(schema='model-binding-requirements-v2',
        models=['M0','M1'],paper_included=True,execution_enabled=False,
        recovered_binding=ref('recovery/model_source_audit/M0M1_BINDING_RECOVERY.json'),
        resolved_fields=['ordered_feature_definition_ids','artifact_content_sha256','producer_revision_binding'],
        required_unresolved_fields=['actual_paper_session_artifact_load_receipt','causal_recognition_and_feed_binding','historical_library_bit_parity'],
        availability_status='SOURCE_BOUND_RUNTIME_IMPLEMENTED_PLATFORM_UNBOUND',
        clock_policy='Feature clocks retain original market time; artifact availability uses a separate recorded prospective session clock. Never backdate an artifact.',
        training_cutoff_is_artifact_available_by=False,replay_clock_may_be_backdated=False,
        substitute_native_for_midpoint_features=False,refit_substitution_allowed=False))
    print(json.dumps(dict(recovered_median_states=len(recovered),unresolved_medians=len(unresolved),total_constant_states=139,models=list(models['models']))))

if __name__=='__main__':main()
