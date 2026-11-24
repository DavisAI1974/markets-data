# Old ROOT code, file by file: keep, lift a part, replace and delete, or not ROOT (2026-11-16)

For Greg's sign-off. Nothing has been deleted. Produced by a read-through of two checkouts:
`A` = the pinned producer package, Markets pin `2ebb8ce8`, `research/kalshi/frankie_raw_mbo_benchmark/` (249 files);
`B` = Markets `7f34afa`. Files noted "header only" or "by name only" were not read through. Tests follow the module
they test. Rule being applied (Greg): whatever is replaced is deleted in the same change that replaces it.

Totals: keep 8; lift a part 10; replace and delete 91; not ROOT about 288 (90 of them records and documents);
unsure about 25 files plus about 13 workflows.

## Keep

| File or group | Count | Why |
|---|---|---|
| B `research/kalshi/frankie_boss/fast_mbo_decode.py` | 1 | tape decoder; checks every record, skips nothing (lines 33-36) |
| B `operations/frankie_day_external.py` and its box wrapper (`frankie_box_day_external.py`, `.sh`) | 3 | builder of the 13 external points |
| B `operations/fetch_day_history.py`, `pull_curve_days.py` | 2 | inputs to that builder (header only) |
| B `operations/stage_block_sources.py`, `derive_trading_day_manifest.py` | 2 | tape staging and the trading-day file list. Caveat: the halt is a fixed 21:00 UTC |

## Lift a part, delete the rest

| File | Lift | Leave behind |
|---|---|---|
| B `research/ng_exhaustion_mbo_v4_state_adapter_20260820.py` | the message record (119-157); the resting-order and effect records; the order-book core: add, cancel, modify, queue priority, cached totals (376-531); integrity counters; `normalize` (792); the file-hash and deterministic gzip writer (840-875) | the fixed activity windows (51, 185-271); the top-10 and legacy views (296-375, 750-784); legacy rows written inside `apply` (554-613); the 10-level `book_snapshot` (648); `rolling_activity` and `event_frame` (692-736); `process_dbn_files` |
| B `frankie_boss/mbo_source.py` | pinning, verified copy, decompression, metadata, record reader (22-190) | `ingest_sources` (191-231) |
| A `native_session.py` | exchange close and reopen, the 14:28-14:30 ET settlement window, holidays, trade-day and phase rules (81-294) | the segmenter and assignment ledger (309 on) |
| B `operations/ingest_block_sources.py` | the CME trading-day policy (93-114), source fetching, file hash, write-once | the builder loop (178 on); splitting sessions at each UTC-day file (95); the fixed 21:00 UTC halt (75) |
| A `raw_mbo_source_manifest.py` | hashing, canonical form, file-list hash, record counting (61-130) | the fixed roster and roles (32-39) |
| A `benchmark_checkpoint.py` | canonical hash, atomic write and load, chain check | controller and memory-mode parts (12-37) |
| A `periodic_checkpointer.py` | canonical hash, atomic gzip write (48-107) | the old-state checkpointer class (121 on) |
| A `mbo_resume_state.py` (a copy also sits in B) | order and level export and restore, atomic write | the activity-window keys (59-70) |
| A `native_row_sink.py` | the append-only writer that checks its own file against its counter | key sampling every 97 rows (37) |
| A `native_mbo_field_census.py` | the per-field census | the cap of 64 distinct values (50) |

## Replace and delete

| File or group | Count | Evidence |
|---|---|---|
| A per-second and window core: `native_roll20`, `native_flow_substrate`, `native_candidate`, `native_candidate_adapter`, `native_detector_coverage`, `native_replay_driver` | 6 | 20 s window (roll20:40); candidate constants (candidate:70-75); 10 levels (candidate_adapter:72); whole-second stamping (replay_driver:1034) |
| A section calculators: absorption, response, mirror, replenishment and its adapter, queue and its adapter, ladder, lineage, recurrence, recognition, exhaustion, dipole, discovery, book regime, clocks, cross-section agreement, group adapters, stratum | 19 | sampled quantiles above 50,000 (stratum:26-28, imported by all); 60 s (absorption:49; calculation_runner:89); tick thresholds (replenishment_adapter:185) |
| A assembly: `native_calculation_runner`, `native_full_capture_adapter`, `native_key_alias`, `a_memory_member_first_recalculation`, `native_a_arm_launch` | 5 | 10 levels (full_capture_adapter:634) |
| A tape replays for the A arm: `a_clean_forecaster_{prepare,replay,resume}`, `a_clean_rt_replay`, `a_memory_prepare`, `a_memory_rt_resume` (and `_latest`) | 7 | old-adapter replay (a_clean_rt_replay:31) |
| B `research/ng_exhaustion_mbo_v4_full_state_replay_20260820.py` | 1 | silently skips non-MBO records (126-127); one callback per closed group |
| B box ROOT run: bedrock, bedrock_side, monday_read, monday_calculations, experiment_root, native_parallel, native_emission, native_checkpoint, native_auxiliary, parallel_evidence, segmented_ledger, projection, finalization, adopt_merge, adopt_digest, cleanup_bedrock, pod_root and its loop, root_claims, pause_root, root_cpu, experiment_native / journal / dipole, experiment_data, export_calcs, brain_calcs (`.py` and `.sh`) | 39 | per-second binner and roll (monday_read:76, 125); 10 levels (native_auxiliary:246) |
| B `deploy/aws/box/frankie_box_boss_session.py`: only `derive()` (700 to about 1013); the rest is the Frankie session | 1 | per-second binner (797), roll (898) |
| B staging: `frankie_box_stage_producers.sh`, `producers_checkout.sh`, `frankie_box_producer_tests.sh` | 3 | pull the pinned package into a run |
| B `operations/day_pipeline.py` and its configuration | 2 | stage list (31) |
| B `four_day_pins/recover_book_layers.py`, `recover_native_lifecycle.py` | 2 | fetch and run code from pinned revisions |
| Workflows: `frankie_box_codecs_ci`, `frankie_trading_day_checks`, `frankie_digest_document_ci`, `frankie_journal_stack` | 4 | check out the pinned package |

Added by Greg's decision of 2026-11-16 on the S fields: the S-field code (`c15_teacher.py`, `c15_teacher_r3.py`,
`teacher_changes.py`, `four_day_pins/recover_second_set.py`) is not run as it stands; it uses fixed 64- and
1,024-group windows and the top 3 levels. The read-through filed these under "not ROOT (teacher side)". They are
replaced when the S questions are re-asked of the full record.

## Not ROOT (left alone)

| Group | Count | What it is |
|---|---|---|
| A principal, knowledge and spawn tooling | 25 | the Frankie principal, knowledge delivery, sealing |
| A records: top-level documents, `principal_runs/`, `prior_memory/` | 90 | run records (not read) |
| B `c15_normalizer` (and `_r3`) | 2 | teacher side |
| B `operations/`: host, restore, audit, archive, Granite pod control, transport, serverless reading, and others | 36 | header only |
| B `four_day_pins/assemble.py`, `publish_verified_packet.py` | 2 | packaging |
| B box remainder: classroom, Granite, teacher, digest and render, brain, session, host configuration, disk and cleanup | about 124 | mostly by name only |

## Unsure: needs Greg or a closer read

- **The ingest (C15)**: `c15_builder`, `c15_builder_none`, `c15_observer`, `c15_journal`, `c15_registry`,
  `operations/parallel_ingest`, the ingest shell scripts, `run_journal_stack`, `benchmark_reduction_stack`,
  `profile_journal_drain` (14 files). They read every record at full depth, but they run the old adapter's `apply`,
  which drags the top-10 views and activity windows along, and the registry hashes the old adapter file into its
  identity (`c15_registry.py:17`). Question: is the ingest replaced together with ROOT, or only ROOT?
- **`c15_dstate.py`**: has thresholds of 1 and 3 ticks (31-32). Is this a ROOT dipole stage or the teacher's?
- **A `native_rt_book.py`**: a second copy of the order-book rule. Only one book should survive.
- **A `native_causal_stream`, `native_ingestion_layer_registry`, `native_layer_crosswalk`**: the contract that hands
  old layers to the principal.
- **A `report_ledger_size`, `verify_ledger_size_witness`**: size witnesses for the old ledgers.
- **B `frankie_box_experiment.py` / `.sh`** (the orchestrator) and **`frankie_box_run.yml`** (a general launcher that
  names the old ROOT scripts).
- **The Step 1 workflows** (about 13, plus `v4_5y_*`): seen only by name. The Step 1 definitions and the frozen
  family classifier are kept as the base.
- About 180 other workflows were not examined.

## Paths by which old ROOT code gets pulled into a new run (to be closed)

- `deploy/aws/box/producers_checkout.sh:10, 34` (a checkout at the pinned commit)
- `frankie_box_stage_producers.sh:9, 58-65` (pins the ten producer files)
- `frankie_box_pod_root.sh:47` and `frankie_boss/pod_root/pod_bootstrap.sh:63` (clone a named old branch)
- `pod_root/pod_agent.py:62-73` (producer pins)
- `frankie_box_bedrock.py:22, 230-236, 448-467`
- `frankie_box_boss_session.py:58, 268, 771-774` (adds the producers to the import path; loads the old adapter by path)
- `frankie_box_monday_read.py:29, 69-70`; `frankie_box_monday_calculations.py:128`; `frankie_box_host_config.py:23`
- `frankie_box_native_parallel.py:58, 197`; `native_emission.py:34, 51, 66, 84`; `native_checkpoint.py:13`;
  `parallel_evidence.py:86`; `segmented_ledger.py:17`; `frankie_box_teach.py:94`
- `frankie_box_producer_tests.sh:21, 26`
- `research/kalshi/frankie_boss/frankie_principal_adapter.py:556, 772` (runs modules of the old package)
- `four_day_pins/recover_book_layers.py:21-23, 82-85`; `recover_native_lifecycle.py:23-27`
- `tests/_producers.py:13-16`
- Workflows: `frankie_box_codecs_ci.yml:56, 68`; `frankie_trading_day_checks.yml:23, 33`;
  `frankie_digest_document_ci.yml:30`; `frankie_journal_stack.yml:359`;
  `ng_exhaustion_step1_october_shards_20260824.yml:61` and five more lines
- Duplicates that could shadow the salvaged copies: `frankie_boss/mbo_resume_state.py`,
  `frankie_boss/raw_mbo_source_manifest.py`
- `frankie_box_run.yml:655` and the staging scripts stage whatever commit is dispatched, so old ROOT comes along for
  as long as it is still in the tree.

## Notes

- This read-through reported that it did not find where order ages restart at 00:00 UTC. The earlier ROOT depth
  audit did: the opening book is warmed from a partition's 00:00 UTC snapshot and the next partition is appended
  whole (`operations/ingest_block_sources.py` 187-265). That is in the ingest, which is one reason the ingest
  question above matters.
- Only this session's own Markets branch can be pushed from a cloud session. Deleting from the Markets trunk and
  other branches needs Greg or a permission change.
