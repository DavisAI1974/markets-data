# The two Codex pieces (the SQL step and the family workflow): what each was for, whether the code does it, whether its kind of output is useful

Asked for by Greg, 2026-11-16 (seventh session): "look at what info they are giving us and does it move us forward
to understanding the trades better to get better signals"; "That was old data so don't lean on the findings. Just
intent and is the code accomplishing the intent and is the data useful"; "But if those perspective would be good
to use on the new data then include it".

How this was made: a read-only pass over Markets commit `dd9c797a` (729 files under
`artifacts/sqlite-triage/20261022/`) and over `420fd65^`, the last commit that still held the later write-ups.
Nothing was run and nothing in either repository was changed. Old numbers appear only where they describe what the
code does; they carry no weight as findings. Four of its statements were checked against the code by the session
that asked for it and hold: a family's start is the first place its shape is seen in the file
(`build_family_alignment.py`); the "is a family first seen within N seconds" target counts the sample's own
family (`build_joint_model_inputs.jl`); a dipole path ends in "reversal" at the third opposed second in a row, by
rule (`reconstruct_dipole_event_phases.py`); the SQL step lists labels that share a selection
(`triage_full_sqlite_20261022.py`). The rest is the reader's account and is not re-checked line by line.

Claude's short verdict and what is proposed from it are in `ROOT_GAMEPLAN_DECISIONS.md`, seventh session, "The
look at Codex's two pieces: result".

---

CODEX SQL STEP + FAMILY WORKFLOW: INTENT, WHETHER THE CODE DOES IT, WHETHER THE OUTPUT IS A USEFUL KIND, PERSPECTIVES TO CARRY

Read-only. Nothing was run, changed or written to the repository. Old numbers appear only where they describe what the code does.
Reached: commit dd9c797a (729 files) and 420fd65^ (1,800 files: the later write-ups and the finished model run).
Paths: P = artifacts/sqlite-triage/20261022 ; F = P/families ; S = F/scripts ; R = F/full-context-audit/scripts/source_reference ; T = tasks/family-research-20261022 (only at 420fd65^).
Could not determine: the upstream function `describe_structure` that makes a family ID; the script that wrote F/family-start-candidates.json; which column-grouping rule the final model run used. None is in the saved tree.
"Tape day" below means the one old, wrongly cut day of data (Oct 17-18, 2023), not a trade day.

## A. THE SQL STEP (P/sources/*.py, P/queries/, P/exports/)
What it reads: a 33.8 GB catalog `cells.sqlite` left by an earlier "experiment search" on the one tape day (P/exports/sqlite-schema.txt). A row of its `labels` table is one label, "field = value", attached to a "selection". A selection is a set of observations (a mask). A second file holds 1,594,763 "tasks", each pointing at one selection.
1. INTENT. Find which labels sit together on the same selections, so they could be read as joint conditions. P/queries/README.txt: "All kept catalog labels are scanned ... Counts are label occurrences, not predictive effects or unique selections."
2. DOES THE CODE DO THAT. It counts; it tests nothing. The first program (sources/triage_full_sqlite_20261022.py) drops identifier fields and counts what is left per field; the second counts which labels share a selection. Gaps:
   - Labels on one selection are different NAMES for the same set of rows, not two conditions true together. The code says so: triage_full_sqlite_20261022.py:38 "labels on one selection are aliases, not proof of an explicit AND hypothesis". "Conjunction" is a misnomer.
   - Three "handle" groups are fixed by hand in advance (conjunction_query_uncapped_20261022.py:15-24). Everything is counted only relative to those three.
   - Field paths are cut to their last word and array positions removed (:7), so the link from a label back to a record, a time or a family is lost.
   - A hand-written list drops order ids, cursors, trading day and more before counting (:5).
   - "Uncapped" only removes an output limit of the top 1,000 rows per handle (capped file :53 `most_common(1000)`; uncapped :53, :59). No threshold on the counts existed in either.
3. IS THE DATA USEFUL. No. It is a tally of how often label names share a mask inside a catalog built by other code. It says nothing about a trade, a dipole or a time. Its only lasting use was as the list of 749 family IDs the next stage picked up.
4. PERSPECTIVES. "Which facts always arrive together because they are one fact written twice?" Takes: on the new rows, list columns that are exact functions of each other so they are never counted as two pieces of evidence.

## B1. WHAT A "FAMILY" IS (S/build_family_alignment.py, F/family-start-candidates.json, F/family-audit.txt)
1. INTENT. Study the market before, at and after the "birth" of a family. F/family-audit.txt asks first: "What exact record and identity rule create an ow- ID?"
2. DOES THE CODE DO THAT. No; the object is not what the word suggests.
   - A family ID is the `candidate_family_id` stored on each message group (build_family_alignment.py:54). Upstream it is `describe_structure(actions)["candidate_family_id"]`, "a hash over the full structural descriptor" (R/native_replay_driver.py:1425-1435). The saved knowledge file says "a family ID IS the literal action string" (F/full-context-audit/canonical-sources/research/kalshi/frankie_raw_mbo_benchmark/A_MEMORY_SEED_20260902.json:3267). So a family is the SHAPE of one burst of messages (one add; one cancel; trade-fill-modify), not a set of related orders and not a lineage.
   - "Birth" is the first row in the file where that shape appears (:25-26, FIRST_OBSERVED_STRUCTURAL_FAMILY). The notes admit "not a proven original order birth".
   - Read from the saved lists: 445 of the 749 shapes occur exactly once; four shapes hold about 455,000 of the 583,127 occurrences and all four are "born" in the first 110 rows of the tape (F/descriptive-v1/family_master.csv); about twenty shapes are "born" in the first 30 seconds after the 18:00 ET open (F/instance-market-review-20261023/instance-by-instance.md). A "birth" is mostly where the tape starts plus the first time a rare burst shape happens.
   - The 749 are the IDs that surfaced in the SQL export (family-audit.txt), not a census: 561 of 583,688 groups match none of them.
3. IS THE DATA USEFUL. Partly. A label for the shape of each burst is a real, cheap fact per tick. "First time seen on this tape" is not a market event and should anchor nothing.
4. PERSPECTIVES. (a) "What shape is this burst and how rare is it?" Takes: a direct read of the message and what it did to the book, per tick. (b) "Are the rare long shapes (many fills, then cancels) the sweeps that sit at flow peaks?" Takes: join burst shape to each flow peak's story.

## B2. THE DESCRIPTIVE WORK (S/run_descriptive.jl, S/summarize_descriptive.jl, S/report_quote_comparison.jl; F/descriptive-v1, F/enriched-v2. S/run_family_clock.py and S/verify_price_clocks.py not opened; judged from F/family-clock-results.txt)
1. INTENT. F/family-clock-research-scope.txt: "reconstruct and observe the market timeline around families. No predictive model, target variable ... is selected." Then describe direction, continuation and reversal around each start.
2. DOES THE CODE DO THAT. The timing discipline is there: each value is taken as last known at or before a cutoff, by receive time and cursor (run_descriptive.jl:29-34, :82-85, :133). The description does not match a per-case intent:
   - Five fixed sample points per family: 120 s before, just before, at, 600 s before, 600 s after (:72). Nine fixed horizons, 1 s to 1 hour (:104). "Prior direction" is the sign of the trade-price change over a fixed 120 s (:78-79).
   - Output is pooled counts and means by point x horizon x direction x quarter of the tape (:148-154), and a Pearson correlation across families for every measure x horizon (summarize_descriptive.jl:72-91). Per-case rows are saved (elapsed_windows, nearby_price_pairs) but are only ever summarised.
   - The "nearby control" 600 s away is the same market with other starts inside it; the code counts them (summarize_descriptive.jl:124-128) but does not separate them.
   - Price freshness: four age limits are computed (run_descriptive.jl:149); the headline tables use 5 s (summarize_descriptive.jl:132).
3. IS THE DATA USEFUL. Partly. The as-of join with ages, and the same move measured in trade prices and in mid-quote, are good kinds of output. The pooled direction tables and the mass of pairwise correlations are not: they blur each case and, anchored on first-seen shapes, describe the tape more than any event.
4. PERSPECTIVES. (a) "Is a short reversal real, or the trade bouncing between bid and ask?" Takes: measure each move twice, in trade prices and in mid-quote; best bid and ask are on every row. (b) "How many other events sit inside this event's window?" Takes: count flow peaks overlapping each peak's span. (c) "How old is each value when used?" Takes: an age column beside each of the 13 outside points.

## B3. PRE-BIRTH (S/extract_prebirth_context.py, S/compare_context_changes.jl, F/family-prebirth-scope.txt)
1. INTENT. F/family-prebirth-scope.txt: "Window: [recorded family start - 120 seconds, recorded family start) ... A row can support a prebirth observation only when its availability time is strictly before the recorded start."
2. DOES THE CODE DO THAT. The time rule is kept (extract_prebirth_context.py:11, :40-41). The content is thin:
   - "Pre-birth context" is two snapshots: the book 120 s before and the last book before the start (:10). The file says "no claim that two snapshots exhaust all dynamic patterns" (:51). Nothing in between is walked.
   - Changes are taken over fixed 120/300/600 s (compare_context_changes.jl:18) and compared with the same family 600 s earlier or later (:37-44), pooled by quarter of the tape.
   - The birth is first-seen (B1), so "before the birth" means "before a shape was first seen on this tape".
   - The upstream code states the deeper problem for dipole candidates: "PRIOR is structurally unreachable for a candidate defined by its own detection" (R/native_candidate_adapter.py:16-27).
3. IS THE DATA USEFUL. No as built. Good question, wrong anchor, and two snapshots cannot show a build-up.
4. PERSPECTIVES. (a) "What did the book and the order queue do in the run-up to a flow peak, tick by tick, using only what was known then?" Takes: the rows before each peak (book totals, touched line, each order's history). (b) "Can the event be known before it is detected, or is the detection the event?" Takes: for each peak, the first tick at which its story could have been stated.

## B4. SAMPLES, TARGETS AND FOLDS (S/build_joint_model_inputs.jl, S/run_joint_models.jl:16-28)
1. INTENT. Give the models rows to learn from and things to predict, cut forward in time so later data never trains earlier predictions.
2. DOES THE CODE DO THAT. Mostly, with one built-in answer and several fixed choices.
   - 3,745 samples = 749 families x the 5 fixed points. 10,486 "contexts" = those samples times the look-backs (0/120/300/600 s) each point gets; they read 6,265 distinct book rows.
   - Targets: signed and absolute mid-quote change at 9 horizons (build_joint_model_inputs.jl:71-80), and "is any family first seen within 120/300/600 s" (:84-90). 21 targets x 3 folds = the 63 cohorts.
   - ANSWER BUILT IN (:60-63, :84-90 with run_descriptive.jl:73): the list of start times includes the sample's own family, so for the point 120 s before a start, for the point just before a start (every horizon), and for the point 600 s before with the 600 s horizon, the label is "yes" by construction: 7 of the 12 point-by-horizon cells. run_joint_models.jl:32 removes the look-back columns from these fits so the kind of row is harder to see, but the label stays fixed, and a model can score by recognising the kind of row.
   - Folds are quarters of ONE tape day by elapsed time; quarters 2, 3, 4 are tested; training is everything earlier minus 600 s (run_joint_models.jl:16-24). They are not separate trade days.
   - Fixed gates: quote age at most 5 s (build_joint_model_inputs.jl:75); at least 30 training and 10 test rows (run_joint_models.jl:26).
   - Samples exist only around family starts, so every row is chosen by the thing being studied.
3. IS THE DATA USEFUL. Partly. Forward-only folds with a gap and no filling of missing values are sound habits. The occurrence target is circular. Fixed-horizon end-point targets say nothing about the path.
4. PERSPECTIVES. (a) "Does the label already contain the answer?" Takes: for any target, test whether the row's own event sits inside its own window. (b) "Train on the past only, with a gap as long as the longest look-ahead." Takes: cut by trade day once more than a few exist.

## B5. THE JOINT MODELS (S/run_joint_models.jl, S/run_neural_models.jl, S/model_rules.jl, S/build_expanded_candidate.jl, S/analyze_joint_interactions.jl, S/analyze_observed_price_paths.jl, S/review_saved_layers.jl, S/flag_research_contradictions.py; F/joint-models-v1, -v3, -v4-candidate; F/layer-review-v1; F/final-model-analysis-20261023 at 420fd65^)
1. INTENT. F/family-full-context-analysis-handoff.txt: use "ALL available depth behind the 99 planes, all 13 historical concepts ... then RERUN ALL MODELS", to see whether the layers together predict direction, size of move, or the next family.
2. DOES THE CODE DO THAT. It runs what it lists: ridge, boosted trees (two depths, median loss, 10% and 90% tails), three neural nets at a fixed 25 rounds (run_neural_models.jl:49), refits with one block of columns removed (run_joint_models.jl:41-52), 12 principal components plus k-means fitted on the first quarter (:103-116). Gaps against "understand the layers":
   - Size: the final matrix is 1,154,928 columns for 3,745 rows (build_expanded_candidate.jl:109-111); the write-up gives training cohorts of 110 to 1,376 rows. Each value appears four times (now, and its change over 120/300/600 s); every text category becomes its own yes/no column (:31, :48).
   - Block removal rests on a name-matching rule whose last line sends anything unrecognised to "native_timing_measurements" (model_rules.jl:41-61). The expanded columns are named "v4...." (build_expanded_candidate.jl:27), which the rule's book test `startswith(n,"native.book")` does not match, so under the saved rule the deep-book columns would be removed as "timing". The handoff warned of exactly this ("do not let new features default to a misleading timing block"). The same rule is the only one saved at 420fd65^; whether the run used another: could not determine.
   - Outside series barely change inside one tape day, so a tree can use them as a clock. The notes say so ("can proxy the day's evolution").
   - Interactions: the top 5 column pairs by training gain, cut at training quartiles, needing 10 cases per corner (analyze_joint_interactions.jl:50, :54, :69-70). The model picks the pairs; the test is pooled means.
   - Layer review (review_saved_layers.jl:67-77) re-cuts those pairs by sample point, prior direction and half-hour, "post-hoc, not a new validation". The contradiction registry (flag_research_contradictions.py) lists every place two answers disagree and keeps both. Honest bookkeeping of the same pooled model outputs; no new measurement.
   - The "quote crossing" score acts only when the forecast exceeds the spread and charges the spread (run_joint_models.jl:88-89): an execution assumption inside a research score, against the standing rule.
   - Everything is scored as pooled error per cohort. Nothing is per case until the later instance cards (B9).
3. IS THE DATA USEFUL. Mostly no. Model scores on first-seen shapes, one tape day, a million columns and a built-in answer cannot inform a trade. One piece is a useful kind: analyze_observed_price_paths.jl:19-29 measures, per case, range, distance travelled, net change, their ratio, and largest run up and down.
4. PERSPECTIVES. (a) "How far did price travel compared with where it ended?" Takes: per peak, from tick rows: range, distance travelled, largest move for and against, and when. (b) "Is the size of a move knowable when its direction is not?" Takes: two separate facts per peak, never merged. (c) "If a whole kind of information is taken away, does the reading of a case change?" Takes: read the same peaks with and without that kind of column. (d) "Is an outside series doing anything, or only telling the time?" Takes: compare the same clock time across trade days. (e) "Where do two honest answers disagree?" Takes: a kept list of disagreeing cases, both sides.

## B5a. FULL-DEPTH INPUTS (S/full_context_measurements.py, S/augment_full_depth_inputs.py, F/full-depth-input-findings.md)
1. INTENT. full-depth-input-findings.md: "The old numerical inputs stopped at ten levels on each side"; recover every level and the order queue at each.
2. DOES THE CODE DO THAT. Yes. For every level and every queue position it takes size, volume ahead and time at that priority, and checks the volume-ahead sums (full_context_measurements.py:72-83); per level it adds how concentrated the queue is in a few orders and the size-weighted age (augment_full_depth_inputs.py:54-56). Gap: rank and queue position are column names, so the same price or order moves between columns as the book shifts; and it was all poured into the model matrix.
3. IS THE DATA USEFUL. Yes as measurements, no as model columns.
4. PERSPECTIVES. "At the touched price: how much is ahead of each order, how old is the queue, is it one big order or many small?" Takes: the full line at the touched price plus each order's history, keyed by price and order, not by rank.

## B6. THE DIPOLE AUDITS (S/dipole_book_clock_audit.py, S/reconstruct_dipole_event_phases.py, S/episode_path_checks.py, S/dipole_pair_math.jl; F/dipole-audit-v1, F/dipole-book-clock-audit-v1, F/episode-path-audit-v1, F/dipole-event-phase-audit-v1. S/run_complete_dipole_checks.jl not opened)
1. INTENT. Check the stored dipole paths against their own rules and clocks. dipole_book_clock_audit.py:1 "Compare retained stage books, caller-assigned groups and strictly past books."
2. DOES THE CODE DO THAT. Yes. What it exposes about the upstream dipole code:
   - Each stage carries a whole-second label, but the book attached is "the first complete group in a later receive second" (:63, :70). The audit also fetches the last book known at or before the label (:62, :71), flags every stage where they differ (:96-100), and recomputes the path's price change both ways (:110-113). The stored book is later than its label by rule.
   - Phases: stage zero is BIRTH; the first non-opposed second starts PERSISTENCE; "the third consecutive opposed completed second is REVERSAL and terminates" (reconstruct_dipole_event_phases.py:11-23, :59). A path is complete only when that happens, otherwise censored (:41-42). "Every complete path ends in reversal" is therefore the definition of complete, decided by a fixed count of 3 seconds.
   - A candidate is born at its own detection and stamped on the event second while knowable only later; the audit flags "stage zero event stamp precedes candidate availability" (episode_path_checks.py:96-105, :121-124).
   - The rest of episode_path_checks.py:28-52 asserts that stored fields equal their own formulas: bookkeeping, not meaning.
   - The 171-pair check among the 19 dipole columns uses first-versus-last value over the tape, a Pearson needing 8 points, and step counts that skip over missing rows unless told not to (dipole_pair_math.jl:5-15, :27, :31-43). "Reproduced" means the arithmetic was replayed.
3. IS THE DATA USEFUL. Yes as a kind of check: beside each stage, the book it was given, the book that was really known, and the time gap. The pair tables are not useful.
4. PERSPECTIVES. (a) "Is the book attached to a dipole stage one that was known then, and how different is the last truly known book?" Takes: for each stage, the last tick row at or before its stamp. (b) "Does every path end the same way, or only by the rule that ends it?" Takes: record each peak's ending as a fact with the rule that ended it, and keep unfinished ones. (c) "When was each fact first knowable?" Takes: two times on every peak fact: happened, first visible. (d) "Does a path's price change survive when measured from known books only?" Takes: recompute from the rows in (a).

## B7. THE TIMESTAMPED BID/ASK WORK (S/export_timestamped_mbo_window.py, S/export_model_context_quotes.py; F/timestamped-mbo-window-v1)
1. INTENT. export_timestamped_mbo_window.py:1 "Export actual consecutive completed MBO books around one retained family ... no sampling, interpolation or tick fill."
2. DOES THE CODE DO THAT. Yes. Limits: one window only, the 375th family by time, 120 s before to 600 s after (:21-22), chosen without looking at the outcome; books are states at the close of each message group, "not partial intra-group states" (:56); each level carries size, order count, front-order age, median and 90th-percentile queue age, largest-order share (:26). The all-contexts export is snapshots at the sample points, not a continuous run.
3. IS THE DATA USEFUL. Yes. A continuous, exactly timed ladder with queue ages around one moment lets a person watch a trade form. The new rows already give it everywhere.
4. PERSPECTIVES. (a) "Follow one PRICE, not one rank." Takes: the full line at the touched price, keyed by price. (b) "Does the near book lean the opposite way from the whole book?" Takes: whole-book totals against the lines nearest the touch, per tick. (c) "How old is the front order when a level breaks?" Takes: each order's history at the tick the level empties.

## B8. THE EXTERNAL CLASSROOM (S/external_classroom_math.jl, S/run_external_classroom_checks.jl, S/dipole_pair_math.jl; F/external-classroom-audit-v1; upstream R/dipole_classroom_external.py. S/external_classroom_reconstruction.py not opened)
1. INTENT. Upstream docstring: put "Frankie's 13 historical data points beside the 19 Dipole columns" and state how each outside series moved relative to each dipole column. Codex's part: reproduce those statements exactly.
2. DOES THE CODE DO THAT. It reproduces them. What they measure is weak:
   - Each outside series is held at its last published value on every one of 771,787 tick rows (external_classroom_math.jl:2-19).
   - A series' "direction" is its last present value against its first over the whole tape; a pair is "same", "opposite" or "unresolved" from those two signs alone (dipole_pair_math.jl:5-18).
   - Pearson is taken across tick rows (:29), so a series that steps a few times is correlated against thousands of repeats of itself.
   - 2,040 pairs = 48 series x 19 dipole columns plus every pair of the 48 (run_external_classroom_checks.jl:44-45). "441 of 441 reproduced" (:46-47) is an arithmetic replay, not support.
3. IS THE DATA USEFUL. No. Two end points of one tape day cannot relate weather or positioning to order flow. The as-of alignment underneath is sound.
4. PERSPECTIVES. (a) "What was the latest value of each outside point actually published before this tick, and how old?" Takes: the 13 points per row plus an age. (b) "Did the book or flow change at the moment an outside value was published?" Takes: the tick rows around each publication time, case by case.

## B9. LATER WORK, ONLY AT 420fd65^ (F/instance-market-review-20261023, F/trading-episode-375-391, F/trade-lifecycle-targeted-v1; code T/review_individual_instances.py, T/analyze_quote_order_gapfill.py, T/analyze_local_liquidity.py, T/replay_local_liquidity.py, each skimmed for its deciding rules only)
1. INTENT. After the owner said averages are not a signal, the unit became one event, then one trade. F/trade-lifecycle-targeted-v1/README.md: "All 30,739 recorded market trades remain the primary population ... Families and dipoles supply supporting context."
2. DOES THE CODE DO THAT. Yes in kind, on small hand-picked stretches.
   - Instance cards: one page per family start with what was seen before, each model's forecast and what followed. Still anchored on first-seen shapes.
   - Trade-by-trade reading: for trades 118 to 149 only, hard-coded (analyze_quote_order_gapfill.py:33, :94), with a hand-listed subset for the write-up (:186). It names the resting orders each trade filled and calls a cancel "clean-up" when it carries the same order id as a fill (:113).
   - Local liquidity: whole-book lean against first-ten-levels lean against touch lean (analyze_local_liquidity.py:159-165), and sizes at fixed prices; "near" is fixed at ten levels (:52-53); the code asserts the one saved window's exact row counts (:202), so it runs on that window only. It refuses to name causes: "never infer action causes from deltas" (:1).
   - Paper replay of two rules (touch has size one; best retreats to the old second level): entry fixed 1 ms after the signal (replay_local_liquidity.py:15), exits fixed at 1, 5, 30 s (:64), result charged the spread (:70-71), tested on the same window that suggested the rules. Fixed marks and a cost assumption decide the outcome.
3. IS THE DATA USEFUL. Yes for the trade-by-trade reading and the fixed-price liquidity tables: they explain individual trades from recorded orders. No for the paper replay as built.
4. PERSPECTIVES. (a) "For each trade: which resting order was hit, was it the last at its price, did the quote move, what replaced it?" Takes: each order's history and the touched line at the trade's tick. (b) "Was a cancel after a fill clean-up or a real withdrawal?" Takes: same order id on the fill and the cancel. (c) "Did the print change while the quote did not?" Takes: trade price against best bid and ask on consecutive rows. (d) "Had price and queue already given way before the flow turned?" Takes: for each flow peak, the tick of the first quote retreat against the tick the peak's story turns.

NOT RESEARCH: about 40 scripts in F/full-context-audit/scripts (resume_*, multibox_*, family_reuse_*, family_save_stop*) and most handoff files are machine-running and bookkeeping (boxes, archives, hashes, "99 planes" inventories). No market question in them.

## PIECES WORTH KEEPING
- Stage-book check: given book against last truly known book, per stage. S/dipole_book_clock_audit.py
- As-of joining on receive time plus cursor, with an age on every value. S/run_descriptive.jl:29-34, S/external_classroom_math.jl
- Per-case path measures: range, distance travelled, net change, largest run for and against. S/analyze_observed_price_paths.jl:19-29
- The same move in trade prices and in mid-quote. S/report_quote_comparison.jl
- Per-order queue measures: volume ahead, time at priority, concentration. S/full_context_measurements.py:72-83, S/augment_full_depth_inputs.py:54-56
- Continuous full ladder around a moment. S/export_timestamped_mbo_window.py
- Trade-by-trade order reading; fixed-price size tracking; near lean against whole lean. T/analyze_quote_order_gapfill.py, T/analyze_local_liquidity.py
- Count of events overlapping each other's windows. S/summarize_descriptive.jl:124-128
- Forward folds with a gap; preparation fitted on training rows only; no filling of missing values. S/run_joint_models.jl:24, S/model_rules.jl:15-39

## PIECES TO DROP
- The whole SQL label tally. P/sources/conjunction_query*.py, P/queries/
- "Family birth" as an event, and the 749 as a population. S/build_family_alignment.py:25-26
- The occurrence target. S/build_joint_model_inputs.jl:84-90
- The million-column matrix and every model score, block-removal table and clustering built on it. S/build_expanded_candidate.jl, S/run_joint_models.jl, S/run_neural_models.jl
- The first-versus-last "same/opposite" pair tables, native and external. S/dipole_pair_math.jl, S/run_external_classroom_checks.jl
- The mass of marginal correlations and pooled direction tables. S/summarize_descriptive.jl:72-91, S/run_descriptive.jl:148-154
- Spread-charging scores. S/run_joint_models.jl:88-89, T/replay_local_liquidity.py:70-71

## GOOD IDEA DONE THE WRONG WAY
- What happens before an event forms: anchored on first-seen burst shapes and two snapshots. S/extract_prebirth_context.py
- Burst shape as a fact: misused as a lineage with a birth. S/build_family_alignment.py:54
- Nearby control: a fixed 600 s offset inside overlapping events. S/run_descriptive.jl:72, S/compare_context_changes.jl:37-44
- Dipole phases: a fair description of a flow episode, but the ending is set by a count of 3 seconds. S/reconstruct_dipole_event_phases.py:11-23
- "Take a block away and see what changes": asked through refits on name-matched column groups. S/model_rules.jl:41-61
- Outside data beside the tape: careful alignment, then reduced to two end points of one tape day. S/dipole_pair_math.jl:5-18
- Deep book and queue detail: measured well, then keyed by rank and fed to a model. S/full_context_measurements.py:72-83
- Paper replay of a liquidity rule: in-sample, fixed entry and exit marks, spread charged. T/replay_local_liquidity.py:15, :64
- Do two conditions together matter: pairs picked by a model on a million columns. S/analyze_joint_interactions.jl:50

## PERSPECTIVES TO CARRY TO THE NEW DATA
- Is the book attached to each dipole stage one that was known then; how different is the last known book.
- Does every dipole path end the same way, or only by the rule that ends it; keep the rule and the unfinished cases.
- Two times on every fact: when it happened, when it could first be seen.
- What the book and queue did, tick by tick, in the run-up to a flow peak.
- Every move measured in trade prices and in mid-quote.
- Distance travelled against net change, and largest move for and against, per peak.
- Follow fixed prices, not ranks; near-touch lean against whole-book lean.
- At the touched price: volume ahead, queue age, one big order or many small.
- Per trade: which resting order, last at its price or not, did the quote move, what replaced it; clean-up cancel against withdrawal.
- Had price and queue given way before the flow turned.
- Burst shape and its rarity as a fact on each tick.
- Age of every outside value when used; what the tape did at each publication time.
- How many other events overlap each event's window.
- Does a label contain its own answer; is an outside series only telling the time.
