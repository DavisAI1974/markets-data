# Remaining 35 fields: actual recovery and exact dependencies

This repair adds 33,078 cell values across six previously empty fields and all 5,513 selected ticks. One is exact source-window metadata; five contain explicitly scoped recovered data. **This is not completion of all 35 fields.** Twenty-nine still have no produced values. Scope limitations remain inside the populated cells.

All 32 cases, eight types, four dates and original S cells remain. No stopped S producer, model inference, new strategy, arbitrary horizon, or new independent Claude result was used. The complete 143,270-trade rebuild remains unfinished.

AWS is unavailable. Local archives and the pinned Git source catalog were inspected. Canonical 2021 object identities are preserved separately, but the 2023 tapes are not relabeled as those objects. The native calculation runner explicitly says it does not execute Frankie or create locks; missing model output fields cannot be truthfully filled from it.

| Field | Rows populated | Status | Evidence or remaining dependency |
|---|---:|---|---|
| L024 — canonical_sep_nov_2021_dbn_mbo_objects | 0 | UNRESOLVED | Exact 2021 object identities/bytes/SHA256 are recovered in CANONICAL_2021_OBJECT_IDENTITIES.json. Raw DBN bytes were not fetched or replayed. The four 2023 tapes are not substitutes. AWS is unavailable per user. |
| L025 — october_first_source_window | 5513 | EXACT_METADATA | Exact inventory metadata: [2021-10-01, 2021-11-01). Explicitly does not apply as the date window of a 2023 trade. |
| L026 — canonical_predecessor_bootstrap_objects | 0 | UNRESOLVED | Needs the exact bootstrap object selection and continuous replay receipt for the intended canonical run. A guessed predecessor date or a 2023 opening snapshot is insufficient. |
| L060 — derived_d_family_geometry | 0 | UNRESOLVED | Needs the binding D-family geometry producer and its full causal input sequence. The saved C15 D1-D6 implementation is a different, explicitly scoped surface and would also recompute stopped S components; it was not run. |
| L061 — derived_open_world_predecessor_state | 0 | UNRESOLVED | Needs the binding P/O/S/X predecessor-state producer and complete state transitions. Latest native observations do not establish active predecessor state. |
| L062 — derived_ancestry_gaps | 0 | UNRESOLVED | Needs structural ancestry identities and gap calculations under the same binding geometry definition. Native order lineage and inter-message recurrence gaps are not substitutes. |
| L063 — derived_unresolved_age_chain_trajectory | 0 | UNRESOLVED | Needs the complete unresolved-age and chain/extension state history from its exact producer. Existing S values were preserved, not recalculated or repurposed as full state. |
| L064 — derived_price_flow_book_paths | 5513 | SCOPED_CONTENT_RECOVERED | Complete selected-case trade prefix, exact price/flow/book values and consecutive-tick deltas. Intervening non-trade/per-second state is not asserted. |
| L065 — derived_v4_mechanics_fifo_features | 5513 | SCOPED_CONTENT_RECOVERED | Original full FIFO/book and adapter activity contents with archived window definitions. Not a complete V4 geometry feature vector. |
| L067 — prebirth_predecessor_at_risk_state | 0 | UNRESOLVED | Needs a prospective predecessor-defined risk-set producer and complete opportunity ledger, including opportunities with no later discovery. |
| L068 — prebirth_unresolved_chain_extension_state | 0 | UNRESOLVED | Needs prospective unresolved chain/extension state before onset, with explicit availability. A candidate emitted after detection is not pre-birth state. |
| L069 — prebirth_ancestry_successor_opportunity | 0 | UNRESOLVED | Needs causal ancestry/successor opportunity identities and the matching producer, not retrospective candidate membership. |
| L070 — prebirth_stopped_chain_false_context_controls | 0 | UNRESOLVED | Needs the exact stopped-chain/false-context control population and producer. No arbitrary timeout or fabricated negative label was introduced. |
| L071 — prebirth_negative_opportunity_cases | 0 | UNRESOLVED | Needs the complete prospectively defined negative-opportunity denominator and observation/censoring outcomes. Missing discoveries are not automatically negative cases. |
| L077 — clock_model_evaluation | 0 | UNRESOLVED | Needs actual model evaluation records bound to the intended run and market cutoff. The recovered native calculation runner explicitly does not execute Frankie. |
| L078 — clock_lock_time | 0 | UNRESOLVED | Needs actual immutable first-lock records from the intended model run. Candidate recognition times are not model lock times. |
| L079 — later_outcome_reveal | 0 | UNRESOLVED | Needs the exact target outcome/reveal package and run binding. Retrospective printed-leg endpoints and native flow reversal labels are not substituted. |
| L080 — target_ground_truth_onset_time | 0 | UNRESOLVED | Needs answer-derived Step-1 ground-truth onset values under the exact target definition. Native candidate event seconds are a different clock. |
| L083 — step1_existing_october_seconds | 0 | UNRESOLVED | Needs exact October Step-1 seconds from the sealed target package. Native 2023 flow seconds do not identify the canonical Step-1 package. |
| L084 — step1_populations | 0 | UNRESOLVED | Needs exact Step-1 target populations and population manifest, not the selected 32 cases or the trade population relabeled as Step-1. |
| L085 — step1_crosswalks | 0 | UNRESOLVED | Needs exact Step-1 identity crosswalks to the intended source/target run. No positional join or inferred identity was used. |
| L086 — step1_target_membership_receipts | 0 | UNRESOLVED | Needs target-membership receipts from the exact Step-1 package. Candidate membership is not Step-1 target membership. |
| L087 — step1_labels_and_classifications | 0 | UNRESOLVED | Needs original Step-1 labels/classifications and source identities. The eight print-leg category labels remain separate provenance. |
| L088 — step1_result_prefixes | 0 | UNRESOLVED | Needs the exact produced Step-1 result locations and artifact identities; launch configuration alone is not proof outputs exist. |
| L089 — step1_reconciliation_outputs | 0 | UNRESOLVED | Needs Step-1 reconciliation products tying the precise target population, clocks, classifications and source manifest together. |
| L090 — output_state_and_state_delta_movie | 5513 | SCOPED_CONTENT_RECOVERED | New hash-chained selected-tick state/delta movie for the recovered price/flow/book surface. Not a full experimental state movie or model run. |
| L091 — output_frankie_reasoning_movie | 0 | UNRESOLVED | Needs actual Frankie reasoning records from the intended model run; native calculation evidence is not model reasoning. |
| L092 — output_probability_movie | 0 | UNRESOLVED | Needs actual immutable probability outputs from the intended model run. No fitted probabilities, zero vectors or unrelated forecasts were substituted. |
| L093 — output_candidate_discoveries | 5513 | SCOPED_CONTENT_RECOVERED | Every original archived native candidate discovery eligible at each trade clock/cursor. Calculation discoveries are not principal-model execution. |
| L094 — output_first_locks_and_no_locks | 0 | UNRESOLVED | Needs genuine first-lock/no-lock run ledgers; not-running is not evidence for a completed no-lock decision. |
| L095 — output_negative_sparse_inconclusive_ledger | 0 | UNRESOLVED | Needs actual model abstention/weak/negative/sparse/inconclusive results. Reconstruction missingness is not a model result. |
| L096 — output_knowledge_retrieval_receipts | 0 | UNRESOLVED | Needs actual knowledge-retrieval invocation receipts bound to the intended run. Static source files are not evidence the model retrieved them. |
| L097 — output_provider_invocation_response_receipts | 0 | UNRESOLVED | Needs actual provider requests/responses and invocation receipts. No provider was invoked by this repair. |
| L098 — output_answer_wall_access_receipts | 0 | UNRESOLVED | Needs actual answer-wall access/no-access audit records for the intended run. The current retrospective user permission is not a historical no-access receipt. |
| L099 — output_source_state_manifest_code_model_run_hashes | 5513 | SCOPED_CONTENT_RECOVERED | Actual reconstruction source/state/manifest/code hashes. Model and primary experiment run remain absent and explicitly null. |

Oct18 L050/L051 also remain missing on 1,447 selected rows. Existing non-S partial semantics from the first repair remain documented in the cells.

Workbook readback is reported separately in WORKBOOK_READBACK_VERIFICATION.json. Supplemental source comparisons and hash-chain checks are in REMAINING_FIELD_VERIFICATION.json.
