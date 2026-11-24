# Where old files are read (the sqlite-triage code and tasks/ code in Markets)

Greg, 2026-11-16: "We will have to make notes to track down where these old files are being read like the old root jsons."

Made from the Markets trunk at `da0101c0`, just before the sqlite-triage outputs and write-ups were deleted (Greg: "Delete output and md").
The code was kept. Every program below reads at least one old input. When a program is rebuilt on the new ROOT, each line
here is an input to repoint or drop. Old ROOT outputs are not carried forward (decisions file).

What the sqlite queries ran on (checked 2026-11-16): `/opt/frankie-box/work/experiment-search/20231018/cycle-00/discovery.partial/recovery/indexed-v1/cells.sqlite`,
built by the old ROOT search run, one trade day (Oct 18), a partial run that was recovered. The family research read the old ROOT run
`experiment-roots/e2e-20231018-...` and the old teacher rows `experiment-teacher-rows/20231018/`. All box paths are on the AWS box.

170 programs. Kinds of old input, counted per program:

- other box path (the old family research work folders on the AWS box): 148
- old search SQLite: 44
- names the sqlite-triage folder (its outputs are deleted): 31
- old teacher rows: 10
- names the recovered-c-drive folder: 3
- old ROOT run: 2
- old ROOT derived structures: 2
- S3: 2

## By folder

### artifacts/sqlite-triage/20261022/exports

- `artifacts/sqlite-triage/20261022/exports/triage_existing_sqlite.py`
  - old search SQLite: `/opt/frankie-box/work/experiment-search/20231018/cycle-00/discovery.partial/recovery/`
  - old search SQLite: `cells.sqlite`
  - old search SQLite: `group-tasks-finite-2-6.sqlite`
  - (names the sqlite-triage folder)
- `artifacts/sqlite-triage/20261022/exports/triage_fresh_sqlite.py`
  - old search SQLite: `/opt/frankie-box/work/experiment-search/20231018/cycle-00/discovery.partial/recovery/`
  - old search SQLite: `cells.sqlite`
  - old search SQLite: `group-tasks-finite-2-6.sqlite`
  - (names the sqlite-triage folder)
- `artifacts/sqlite-triage/20261022/exports/triage_full_sqlite.py`
  - old search SQLite: `/opt/frankie-box/work/experiment-search/20231018/cycle-00/discovery.partial/recovery/`
  - old search SQLite: `cells.sqlite`
  - old search SQLite: `group-tasks-finite-2-6.sqlite`
  - (names the sqlite-triage folder)

### artifacts/sqlite-triage/20261022/sources

- `artifacts/sqlite-triage/20261022/sources/conjunction_query_20261022.py`
  - old search SQLite: `/opt/frankie-box/work/experiment-search/20231018/cycle-00/discovery.partial/recovery/`
  - old search SQLite: `cells.sqlite`
- `artifacts/sqlite-triage/20261022/sources/conjunction_query_uncapped_20261022.py`
  - old search SQLite: `/opt/frankie-box/work/experiment-search/20231018/cycle-00/discovery.partial/recovery/`
  - old search SQLite: `cells.sqlite`
- `artifacts/sqlite-triage/20261022/sources/triage_full_sqlite_20261022.py`
  - old search SQLite: `/opt/frankie-box/work/experiment-search/20231018/cycle-00/discovery.partial/recovery/`
  - old search SQLite: `cells.sqlite`
  - old search SQLite: `group-tasks-finite-2-6.sqlite`
  - (names the sqlite-triage folder)

### full-context-audit

- `artifacts/sqlite-triage/20261022/families/full-context-audit/scripts/archive_full_context_handoff.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/full-context-audit/scripts/audit_full_context_sources.py`
  - old teacher rows: `/opt/frankie-box/work/experiment-teacher-rows/20231018/host-dipole-classroom-source.c15.rows.jsonl`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/full-context-audit/scripts/audit_native_second_feature_identity.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/full-context-audit/scripts/build_expanded_candidate.jl`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/full-context-audit/scripts/build_external_occurrence_links.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/full-context-audit/scripts/build_scoped_external_history.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/full-context-audit/scripts/collect_manifested_external_history.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/full-context-audit/scripts/collect_runtime_knowledge.py`
  - other box path: `/opt/frankie-box/brain/20231018-cycle-00/classroom-external-findings.json`
  - other box path: `/opt/frankie-box/brain/20231018-cycle-00/classroom-findings.json`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/full-context-audit/scripts/collect_supplemental_lifecycle_planes.py`
  - old ROOT run: `/opt/frankie-box/work/experiment-roots/e2e-20231018-a2-20231018-a1`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/full-context-audit/scripts/dipole_book_clock_audit.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/full-context-audit/scripts/dual_box_support.py`
  - other box path: `/opt/frankie-box/archive`
- `artifacts/sqlite-triage/20261022/families/full-context-audit/scripts/episode_path_checks.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/full-context-audit/scripts/export_model_context_quotes.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/full-context-audit/scripts/external_classroom_reconstruction.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
  - other box path: `/opt/frankie-box/work/source-indexed-consumers-20261021/research/kalshi/frankie_boss/operations/frankie_day_external.py`
- `artifacts/sqlite-triage/20261022/families/full-context-audit/scripts/external_scope_history.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/full-context-audit/scripts/extract_full_native_second_contexts.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/full-context-audit/scripts/family_completion_hook.py`
  - other box path: `/opt/frankie-box/archive`
  - other box path: `/opt/frankie-box/archive/family-save-stop-20261022`
- `artifacts/sqlite-triage/20261022/families/full-context-audit/scripts/four_box_handoff.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/full-context-audit/scripts/handoff_dual_box_20261022.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/full-context-audit/scripts/make_four_box_assignment.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/full-context-audit/scripts/materialize_external_asof_observations.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/full-context-audit/scripts/multibox_support.py`
  - other box path: `/opt/frankie-box/archive`
- `artifacts/sqlite-triage/20261022/families/full-context-audit/scripts/prepare_complete_dipole_checks.py`
  - old teacher rows: `/opt/frankie-box/work/experiment-teacher-rows/20231018/host-dipole-classroom-source.c15.rows.jsonl`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/full-context-audit/scripts/reconcile_B_serial_originals_20261022.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/full-context-audit/scripts/reconstruct_dipole_event_phases.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/full-context-audit/scripts/redeploy_parallel_candidate.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/full-context-audit/scripts/resume_actual_memory_candidate.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/full-context-audit/scripts/resume_dual_box_candidate.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/full-context-audit/scripts/resume_dual_box_candidate_b.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/full-context-audit/scripts/resume_dual_box_candidate_b_io.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/full-context-audit/scripts/resume_memory_candidate.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/full-context-audit/scripts/resume_memory_candidate_v2.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/full-context-audit/scripts/resume_multibox_candidate.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/full-context-audit/scripts/review_complete_dipole_claims.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/full-context-audit/scripts/review_external_classroom_checks.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/full-context-audit/scripts/root_full_context.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
  - old ROOT derived structures: `structures.jsonl.gz`
- `artifacts/sqlite-triage/20261022/families/full-context-audit/scripts/run_complete_dipole_checks.jl`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/full-context-audit/scripts/run_external_classroom_checks.jl`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/full-context-audit/scripts/source_reference/frankie_box_brain.py`
  - other box path: `/opt/frankie-box/work/experiment-calcs`
- `artifacts/sqlite-triage/20261022/families/full-context-audit/scripts/stage_dual_box_B_20261022.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/full-context-audit/scripts/stage_four_box_CD_20261022.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/full-context-audit/scripts/test_dual_box_support.py`
  - other box path: `/opt/frankie-box/archive`
- `artifacts/sqlite-triage/20261022/families/full-context-audit/scripts/test_multibox_transfer.py`
  - other box path: `/opt/frankie-box/archive`

### joint-inputs-v2

- `artifacts/sqlite-triage/20261022/families/joint-inputs-v2/scripts/archive_joint_checkpoint.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
  - old search SQLite: `artifacts/sqlite-triage/20261022/families`
  - (names the sqlite-triage folder)
- `artifacts/sqlite-triage/20261022/families/joint-inputs-v2/scripts/build_joint_model_inputs.jl`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/joint-inputs-v2/scripts/verify_duration_inputs.jl`
  - other box path: `/opt/frankie-box/work/family-research-20261022`

### joint-inputs-v3

- `artifacts/sqlite-triage/20261022/families/joint-inputs-v3/scripts/archive_full_depth_checkpoint.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
  - old search SQLite: `artifacts/sqlite-triage/20261022/families`
  - S3: `s3://bento-568968024170-us-east-2-an/frankie/family-prebirth/20261022/family-full-depth-inputs-v3-2d4f2553.tar.gz`
  - (names the sqlite-triage folder)
- `artifacts/sqlite-triage/20261022/families/joint-inputs-v3/scripts/audit_counter_anchors.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/joint-inputs-v3/scripts/augment_full_depth_inputs.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/joint-inputs-v3/scripts/build_full_depth_matrix.jl`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/joint-inputs-v3/scripts/compare_full_depth_models.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/joint-inputs-v3/scripts/export_timestamped_mbo_window.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/joint-inputs-v3/scripts/finish_parallel_full_depth_suite.sh`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
  - other box path: `/opt/frankie-box/work/family-research-20261022/joint-models-v3`
- `artifacts/sqlite-triage/20261022/families/joint-inputs-v3/scripts/flag_research_contradictions.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/joint-inputs-v3/scripts/prepare_full_depth_rerun.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/joint-inputs-v3/scripts/resume_core_parallel.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/joint-inputs-v3/scripts/review_saved_layers.jl`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/joint-inputs-v3/scripts/run_full_depth_suite.sh`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
  - other box path: `/opt/frankie-box/work/family-research-20261022/joint-models-v3`
- `artifacts/sqlite-triage/20261022/families/joint-inputs-v3/scripts/summarize_layer_review.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`

### joint-models-v1

- `artifacts/sqlite-triage/20261022/families/joint-models-v1/scripts/analyze_joint_interactions.jl`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/joint-models-v1/scripts/analyze_observed_price_paths.jl`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/joint-models-v1/scripts/build_joint_model_inputs.jl`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/joint-models-v1/scripts/run_joint_models.jl`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/joint-models-v1/scripts/run_neural_models.jl`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/joint-models-v1/scripts/summarize_joint_models.jl`
  - other box path: `/opt/frankie-box/work/family-research-20261022`

### joint-models-v3

- `artifacts/sqlite-triage/20261022/families/joint-models-v3/core-resume/run_core_task.jl`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/joint-models-v3/scripts/analyze_joint_interactions.jl`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/joint-models-v3/scripts/analyze_observed_price_paths.jl`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/joint-models-v3/scripts/review_saved_layers.jl`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/joint-models-v3/scripts/run_joint_models.jl`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/joint-models-v3/scripts/run_neural_models.jl`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/joint-models-v3/scripts/summarize_joint_models.jl`
  - other box path: `/opt/frankie-box/work/family-research-20261022`

### joint-models-v4-candidate-20261022

- `artifacts/sqlite-triage/20261022/families/joint-models-v4-candidate-20261022/run_suite.sh`
  - other box path: `/opt/frankie-box/work/family-research-20261022`

### layer-review-v1

- `artifacts/sqlite-triage/20261022/families/layer-review-v1/scripts/review_saved_layers.jl`
  - other box path: `/opt/frankie-box/work/family-research-20261022`

### scripts

- `artifacts/sqlite-triage/20261022/families/scripts/analyze_joint_interactions.jl`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/analyze_observed_price_paths.jl`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/archive_descriptive.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/archive_enriched_results.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
  - old search SQLite: `artifacts/sqlite-triage/20261022/families`
  - (names the sqlite-triage folder)
- `artifacts/sqlite-triage/20261022/families/scripts/archive_full_context_handoff.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/archive_full_depth_checkpoint.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
  - old search SQLite: `artifacts/sqlite-triage/20261022/families`
  - S3: `s3://bento-568968024170-us-east-2-an/frankie/family-prebirth/20261022/family-full-depth-inputs-v3-2d4f2553.tar.gz`
  - (names the sqlite-triage folder)
- `artifacts/sqlite-triage/20261022/families/scripts/archive_joint_checkpoint.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
  - old search SQLite: `artifacts/sqlite-triage/20261022/families`
  - (names the sqlite-triage folder)
- `artifacts/sqlite-triage/20261022/families/scripts/audit_analysis_inputs.jl`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/audit_counter_anchors.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/audit_full_context_sources.py`
  - old teacher rows: `/opt/frankie-box/work/experiment-teacher-rows/20231018/host-dipole-classroom-source.c15.rows.jsonl`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/audit_native_second_feature_identity.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/augment_external_observations.jl`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/augment_full_depth_inputs.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/build_expanded_candidate.jl`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/build_external_occurrence_links.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/build_family_alignment.py`
  - old teacher rows: `/opt/frankie-box/work/experiment-teacher-rows/20231018/host-dipole-classroom-source.c15.rows.jsonl`
- `artifacts/sqlite-triage/20261022/families/scripts/build_full_depth_matrix.jl`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/build_joint_model_inputs.jl`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/build_scoped_external_history.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/collect_enriched_inputs.py`
  - old teacher rows: `/opt/frankie-box/work/experiment-teacher-rows/20231018/host-dipole-classroom-source.c15.rows.jsonl`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/collect_manifested_external_history.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/collect_runtime_knowledge.py`
  - other box path: `/opt/frankie-box/brain/20231018-cycle-00/classroom-external-findings.json`
  - other box path: `/opt/frankie-box/brain/20231018-cycle-00/classroom-findings.json`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/collect_supplemental_lifecycle_planes.py`
  - old ROOT run: `/opt/frankie-box/work/experiment-roots/e2e-20231018-a2-20231018-a1`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/compare_context_changes.jl`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/compare_full_depth_models.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/complete_context_measurements.jl`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/complete_pullback_inputs.jl`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/dipole_book_clock_audit.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/enrich_group_measurements.jl`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/episode_path_checks.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/export_model_context_quotes.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/export_timestamped_mbo_window.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/external_classroom_reconstruction.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
  - other box path: `/opt/frankie-box/work/source-indexed-consumers-20261021/research/kalshi/frankie_boss/operations/frankie_day_external.py`
- `artifacts/sqlite-triage/20261022/families/scripts/external_scope_history.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/extract_full_native_second_contexts.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/extract_geometry_context.py`
  - old teacher rows: `/opt/frankie-box/work/experiment-teacher-rows/20231018/host-dipole-classroom-source.c15.rows.jsonl`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/extract_prebirth_context.py`
  - old teacher rows: `/opt/frankie-box/work/experiment-teacher-rows/20231018/host-dipole-classroom-source.c15.rows.jsonl`
- `artifacts/sqlite-triage/20261022/families/scripts/finalize_enrichment_gate.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/finish_parallel_full_depth_suite.sh`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
  - other box path: `/opt/frankie-box/work/family-research-20261022/joint-models-v3`
- `artifacts/sqlite-triage/20261022/families/scripts/flag_research_contradictions.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/materialize_external_asof_observations.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/prepare_complete_dipole_checks.py`
  - old teacher rows: `/opt/frankie-box/work/experiment-teacher-rows/20231018/host-dipole-classroom-source.c15.rows.jsonl`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/prepare_enriched_analysis.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/prepare_full_depth_rerun.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/reconstruct_dipole_event_phases.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/redeploy_parallel_candidate.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/report_descriptive.jl`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/report_quote_comparison.jl`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/resume_core_parallel.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/review_complete_dipole_claims.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/review_external_classroom_checks.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/review_saved_layers.jl`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/root_full_context.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
  - old ROOT derived structures: `structures.jsonl.gz`
- `artifacts/sqlite-triage/20261022/families/scripts/run_complete_dipole_checks.jl`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/run_descriptive.jl`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/run_enriched_once.jl`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/run_external_classroom_checks.jl`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/run_family_clock.py`
  - old teacher rows: `/opt/frankie-box/work/experiment-teacher-rows/20231018/host-dipole-classroom-source.c15.rows.jsonl`
- `artifacts/sqlite-triage/20261022/families/scripts/run_full_depth_suite.sh`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
  - other box path: `/opt/frankie-box/work/family-research-20261022/joint-models-v3`
- `artifacts/sqlite-triage/20261022/families/scripts/run_joint_models.jl`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/run_neural_models.jl`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/summarize_descriptive.jl`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/summarize_joint_models.jl`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/summarize_layer_review.py`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/verify_duration_inputs.jl`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `artifacts/sqlite-triage/20261022/families/scripts/verify_price_clocks.py`
  - old search SQLite: `/opt/frankie-box/work/ingest-20231018-gh-36571235912-1/journal.compact.sqlite`

### tasks/family-research-20261022

- `tasks/family-research-20261022/analyze_quote_order_gapfill.py`
  - old search SQLite: `artifacts/sqlite-triage/20261022/families`
  - (names the sqlite-triage folder)
- `tasks/family-research-20261022/attach_trade_external_evidence.py`
  - old search SQLite: `artifacts/sqlite-triage/20261022/families`
  - (names the sqlite-triage folder)
- `tasks/family-research-20261022/attach_trade_root_and_order_evidence.py`
  - old search SQLite: `artifacts/sqlite-triage/20261022/families`
  - (names the sqlite-triage folder)
- `tasks/family-research-20261022/audit_trade_dipole_overlay.py`
  - old search SQLite: `artifacts/sqlite-triage/20261022/families`
  - (names the sqlite-triage folder)
- `tasks/family-research-20261022/build_model_perspectives.py`
  - old search SQLite: `artifacts/sqlite-triage/20261022/families/final-model-analysis-20261023`
  - (names the sqlite-triage folder)
- `tasks/family-research-20261022/compare_trading_episode_375_391.py`
  - old search SQLite: `artifacts/sqlite-triage/20261022/families`
  - (names the sqlite-triage folder)
- `tasks/family-research-20261022/continue_trade_chronology.py`
  - old search SQLite: `artifacts/sqlite-triage/20261022/families/trade-lifecycle-targeted-v1`
  - (names the sqlite-triage folder)
- `tasks/family-research-20261022/export_bounded_quote_order_sources.py`
  - old teacher rows: `/opt/frankie-box/work/experiment-teacher-rows/20231018/host-dipole-classroom-source.c15.rows.jsonl`
  - other box path: `/opt/frankie-box/work/family-research-20261022`
- `tasks/family-research-20261022/export_oct17_liquidity.py`
  - old search SQLite: `artifacts/sqlite-triage/20261022/families`
  - (names the sqlite-triage folder)
- `tasks/family-research-20261022/finalize_quote_order_interpretation.py`
  - old search SQLite: `artifacts/sqlite-triage/20261022/families/trade-lifecycle-targeted-v1/quote-order-gapfill-v1`
  - (names the sqlite-triage folder)
- `tasks/family-research-20261022/finalize_trade_evidence.py`
  - old search SQLite: `artifacts/sqlite-triage/20261022/families`
  - (names the sqlite-triage folder)
- `tasks/family-research-20261022/plot_exact_quote_order_path.py`
  - old search SQLite: `artifacts/sqlite-triage/20261022/families/trade-lifecycle-targeted-v1/quote-order-gapfill-v1`
  - (names the sqlite-triage folder)
- `tasks/family-research-20261022/plot_trade_overlay.py`
  - old search SQLite: `artifacts/sqlite-triage/20261022/families/trade-lifecycle-targeted-v1`
  - (names the sqlite-triage folder)
- `tasks/family-research-20261022/preserve_prior_local_files.py`
  - (names the recovered-c-drive folder)
- `tasks/family-research-20261022/query_saved_run_connections.py`
  - old search SQLite: `artifacts/sqlite-triage/20261022/families`
  - (names the sqlite-triage folder)
  - (names the recovered-c-drive folder)
- `tasks/family-research-20261022/read_bounded_second_set.py`
  - old search SQLite: `artifacts/sqlite-triage/20261022/families`
  - (names the sqlite-triage folder)
- `tasks/family-research-20261022/receive_quote_order_sources.py`
  - old search SQLite: `artifacts/sqlite-triage/20261022/families/trade-lifecycle-targeted-v1/quote-order-gapfill-v1`
  - (names the sqlite-triage folder)
- `tasks/family-research-20261022/render_instance_cards.py`
  - old search SQLite: `artifacts/sqlite-triage/20261022/families/instance-market-review-20261023`
  - (names the sqlite-triage folder)
- `tasks/family-research-20261022/review_individual_instances.py`
  - old search SQLite: `artifacts/sqlite-triage/20261022/families`
  - (names the sqlite-triage folder)
- `tasks/family-research-20261022/summarize_trading_episode_375_391.py`
  - old search SQLite: `artifacts/sqlite-triage/20261022/families`
  - (names the sqlite-triage folder)
- `tasks/family-research-20261022/targeted_trade_lifecycle_pass.py`
  - old search SQLite: `artifacts/sqlite-triage/20261022/families`
  - (names the sqlite-triage folder)
  - (names the recovered-c-drive folder)
- `tasks/family-research-20261022/verify_trade_checkpoint.py`
  - old search SQLite: `artifacts/sqlite-triage/20261022/families`
  - (names the sqlite-triage folder)
- `tasks/family-research-20261022/verify_trade_external_overlay.py`
  - old search SQLite: `artifacts/sqlite-triage/20261022/families`
  - (names the sqlite-triage folder)
- `tasks/family-research-20261022/verify_trade_handoff.py`
  - old search SQLite: `artifacts/sqlite-triage/20261022/families`
  - (names the sqlite-triage folder)
