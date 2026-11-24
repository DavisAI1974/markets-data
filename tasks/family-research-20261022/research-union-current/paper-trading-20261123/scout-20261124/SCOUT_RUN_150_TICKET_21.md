# Scout run 150 (Haiku): where things are for ticket 21

Kept word for word as the agent returned it, 2026-11-24 (twenty-fifth session). Nothing below this line is the main session's.

---

Scout run 150, ticket 21. Tool calls used: 26 of 28. Stopped on my own plan with the search complete, not at a limit. No writes, no sub-agents, sqlite not read.

## 1. Adoption plan: lines naming first users, Experiment Arms, orchestrator, D0 to D5
File: /tmp/claude-0/-home-user/3356516d-d71a-5e13-907d-ff8d8ffcb6d4/scratchpad/frankie_handoff_20261123_2/CLAUDE_ARCH_PLAN_GRAPH_ENGINEERING_ADOPTION_20261123.md
- Line 72: "- First users: the Experiment Arms sheet of the build plan workbook (backfill its arms as nodes),"
- Line 73: "  the experiment orchestrator's series and survivors steps, the dipole teacher arms D0-D5."
Same two lines in the Markets checkout copy: /home/user/Markets/research/kalshi/frankie_boss/CLAUDE_ARCH_PLAN_GRAPH_ENGINEERING_ADOPTION_20261123.md:72-73.
No other hits in this plan for "first users", "Experiment Arms", "orchestrator", "D0", "D5" or "teacher arm".

## 2. /home/user/Markets/tools/exp_dag.py
Command-line verbs (main(), line 264; sub-parsers):
- line 268 `add_parser("push")` - WRITES (appends via _append, line 75)
- lines 283-284 loop `for verb in ("fetch", "children", "lineage")`, each `sub.add_parser(verb)` with positional id - fetch/children/lineage READ
- line 285 `add_parser("log")` - READ
- line 286 `add_parser("leaves")` - READ
- line 287 `add_parser("rebuild")` - WRITES experiments/frankie_exp_dag.sqlite (rebuild, line 191; sqlite3.connect at line 197) and the manifest (write_manifest, line 235)
- line 288 `add_parser("diff")` - READ (diff, line 164; --repo-path git diff)
- line 292 `add_parser("set-status")` - WRITES (set_status, line 122)
Read-only methods in class ExpDag: fetch 136, log 140, children 148, leaves 151, lineage 155, diff 164.
Tables and node kinds: no CREATE TABLE, no table-name literal and no node-kind enum in the file. Only: STATUSES = ("kept", "reverted", "crash", "recorded") at line 41; SQLITE = "frankie_exp_dag.sqlite" at line 36; docstring line 10. Record schema name "markets.exp_dag.v1" is in MANIFEST.json, not in this file.
Arms / workbook / orchestrator / teacher / D0 / xlsx: NO hits in exp_dag.py. No function loads the workbook's arms, the orchestrator's steps or the teacher arms.

## 3. experiments/MANIFEST.json and experiments/trials.jsonl
MANIFEST.json (/home/user/markets-data/experiments/MANIFEST.json): 20 lines. Top-level keys: "what" (line 2), "schema" (line 3, "markets.exp_dag.v1"), "how_to_read" (line 4), "files" (lines 5-18).
- files[0] line 7: "path": "experiments/trials.jsonl", line 8 "bytes": 75679, line 9 sha256 7f2d17c7587b4e2056c9f1eb400a4c1ee31670e5907cd40a680662b7d9b838b4, line 10 source "the record: one line for each trial and each change to one"
- files[1] line 13: "path": "experiments/frankie_exp_dag.sqlite", line 14 bytes 102400, line 15 sha256 b71df6419d51d85fc0833442e75a08b694c4b2ced935f03851d438d5887a52dd, line 16 source "rebuilt whole from trials.jsonl by tools/exp_dag.py rebuild"
- Grep of MANIFEST for arm/workbook/orchestrator/D0-D5/teacher: no hits.
trials.jsonl (/home/user/markets-data/experiments/trials.jsonl): 15 lines (15 matches for "^").
- Term hits (arm, workbook, orchestrator, D0-D5, teacher): 2 lines, both the substring "armed" inside counter keys, not an arm: line 1 has `"name": "counts.engine.rules.CL01.armed"`, `...CL02.armed`, `...CL03.armed` (repeated on the line); line 3 also matches "armed" (its text was omitted as a long line). No "Experiment Arms", "workbook", "orchestrator", "teacher" or "D0"-"D5" word in trials.jsonl.

## 4. Where D0 to D5 are defined
- Teacher-arm definitions of D0 to D5: NONE found. Whole-repo grep /home/user/Markets for \bD0\b|\bD5\b (all file types) returns one hit: /home/user/Markets/research/kalshi/frankie_boss/CLAUDE_ARCH_PLAN_GRAPH_ENGINEERING_ADOPTION_20261123.md:73 (the mention quoted in section 1). Grep of research/kalshi/frankie_boss *.md for D0|D5|teacher: same single hit.
- Orchestrator skill: /home/user/Markets/.claude/skills/experiment-orchestrator/SKILL.md (only file in that folder). Steps as the skill names them:
  - line 3 (frontmatter): "fetch -> ingest -> derive without bedrock -> export calculations -> series/search -> survivors -> confirmation"
  - Section 1 table, lines 23-34: 1 fetch (line 25); 2 ingest (26); 3 calculations (27, "NOT built"); 4 export (28, built); "-" orchestrator (29, "NOT built"); 5 series (30); 6 search (31); 7 survivors (32); 8 confirmation (33); C classroom arm (34)
  - Section 2 build order, lines 38-44: items 1 to 6 (line 38 "Add the track to the Excel build plan", 40 bedrock switch, 41 orchestrator steps 1-4, 42 series + search, 43 survivors + confirmation, 44 classroom arm)
- Mentions of D0-D5 only (not definitions), in markets-data graph and tasks: graph/nodes/Entity.jsonl:350 (name "D0-D5"); graph/nodes/Claim.jsonl:435 (quote "the dipole teacher arms D0-D5"); graph/reads/run-0024-GRAPH_ADOPTION_PLAN_and_companions.json:52; tasks/family-research-20261022/research-union-current/paper-trading-20261123/MISSING_PIECES_20261124.md:79 ("the dipole teacher arms D0 to D5").

## 5. Build plan workbook
- Named in the record as Frankie_BOSS_Build_Plan_R4_20260921.xlsx, under artifacts/ (SKILL.md line 38: "artifacts/Frankie_BOSS_Build_Plan_R4_20260921.xlsx"). Markets/artifacts is gitignored.
- File found on disk: NONE. Glob **/*[Bb]uild*[Pp]lan* in /home/user/Markets: no files. Glob in /home/user/markets-data: no files. Glob **/*Frankie_BOSS* in /home/user/Markets: no files. Glob **/*.xlsx in markets-data: 3 files, none the build plan: data/outside/ng_oct2023/made/outside_tables.xlsx; tasks/family-research-20261022/research-union-current/root-redesign-20261116/ROOT_dipoles_pinned.xlsx; tasks/family-research-20261022/research-union-current/root-redesign-20261116/ROOT_short_stretch_20231002_0900.xlsx.
- Record's own note that the workbook is unreachable: graph/reads/run-0022-ROOT_GAMEPLAN_DECISIONS_L5853-L6152.json:228 ("its folder is not on the branch"); tasks/family-research-20261022/research-union-current/root-redesign-20261116/ROOT_GAMEPLAN_DECISIONS.md:6106-6108.
- /home/user/markets-data/MARKET_DATA_INDEX.md: no "Experiment Arms" hit; "workbook" only in the generic line 3.
- Text export of the Experiment Arms sheet (csv/md/json): NONE found. Hits for "Experiment Arms" in markets-data are only mentions: graph/edges/RESOLVED_TO.jsonl:75; graph/merges/run-0025-merges.json:24-25; graph/nodes/Entity.jsonl:347 and :526; graph/nodes/Claim.jsonl:434, :435, :844; graph/nodes/Task.jsonl:134; graph/nodes/AgentRun.jsonl:14 and tasks/.../paper-trading-20261123/agent-runs.jsonl:14 (long lines, omitted by the tool); tasks/.../paper-trading-20261123/run-plans/run-0150.json:9; tasks/.../tickets-44-20261124/21.md:1,3,9; tasks/.../tickets-44-20261124/README.md:38; tasks/.../root-redesign-20261116/ROOT_GAMEPLAN_DECISIONS.md:6106; graph/reads/run-0024-GRAPH_ADOPTION_PLAN_and_companions.json:51.

## 6. Tests covering exp_dag (tests/agent_program)
Files importing tools.exp_dag: test_decider_loop.py:20; test_live_platform.py:13; test_stage2_exp_dag.py:8; test_stage3_proposer.py:67; test_stage3_ratchet.py:23; test_stage7d_platform.py:10; test_stage7f_rule_versions.py:10. test_stage4a_graph_store.py:114 has only the string "tools/exp_dag.py" (no import).
test_stage2_exp_dag.py (the file that tests the record directly): test_one_trial_for_each_run_folder_and_each_figure_is_the_receipts (:24); test_loading_twice_adds_nothing (:43); test_the_verbs (:50); test_a_reverted_and_a_crashed_trial_stay_in_the_record (:62); test_what_is_refused (:77).
test_decider_loop.py: :75 test_replay_over_real_signals_one_line_a_signal_and_the_counts_add_up; :97 test_replay_main_prints_the_counts_as_its_last_line; :106 test_dry_prints_the_two_commands_and_starts_nothing; :137 test_dry_reports_a_program_without_decide; :212 test_the_brief_holds_the_present_file_the_contract_and_every_earlier_trial; :256 test_a_file_that_breaks_a_rule_is_refused_with_its_reason; :274 test_a_proposal_without_a_source_or_with_an_unknown_claim_is_refused; :284 test_source_problem_accepts_a_plain_program; :288 test_a_refused_file_is_a_recorded_crash_through_the_loop; :301 test_platform_decider_loads_and_the_guard_splits_mutable_from_protected; :312 test_an_existing_control_file_still_loads_with_the_default_proposer.
test_live_platform.py: :50 test_follow_push_by_push_equals_one_load_of_the_finished_run; :90 test_a_branch_with_no_receipt_has_no_trial; :110 test_first_middle_last_packets_pass_and_a_later_row_fails_naming_it; :142 test_all_opens_gives_a_line_for_each_with_no_breach; :153 test_a_packet_built_at_an_early_commit_equals_the_one_at_the_tip; :164 test_a_packet_from_a_local_journal_file_equals_the_one_from_the_branch; :221 test_the_four_days_carry_the_same_columns_in_the_same_order_on_every_kind_of_sheet; :235 test_every_column_of_the_2023_10_02_daily_sheets_is_placed_in_one_of_three_places.
test_stage3_proposer.py: :29 test_run_47_two_lines_load_as_two_revisions; :42 test_same_run_number_without_corrects_or_across_sessions_is_still_refused; :154 test_the_plan_file_round_trips_byte_for_byte; :161 test_one_value_is_applied_and_every_earlier_trial_is_in_the_next_brief; :206 test_a_proposal_that_breaks_a_rule_is_refused_with_its_reason; :218 test_a_missing_usage_file_is_a_recorded_crash_and_the_loop_goes_on; :231 test_usage_reaches_the_report_and_stops_the_loop_at_max_tokens; :245 test_replay_still_works_and_states_no_proposal; :259 test_exactly_one_of_replay_and_mailbox_is_required; :268 test_ready_check_on_a_good_control_file_and_it_never_runs_the_command; :284 test_ready_check_reports_a_shallow_repository; :291 test_ready_check_reports_a_missing_mutable_file_and_an_unset_variable; :300 test_ready_check_reads_the_manifest_of_the_stored_tape_by_name_and_size.
test_stage3_ratchet.py: :106 test_the_base_follows_the_record_commit_by_docs_only_commits; :111 test_keep_and_revert_on_real_commits; :154 test_a_protected_file_is_a_crash_undone_and_escalated; :174 test_a_file_outside_mutable_is_a_crash_too; :181 test_no_figure_chosen_records_every_trial_and_reverts_nothing; :195 test_budget_stop_names_the_unresolved_commits; :206 test_after_trials_without_a_keep_is_a_plain_stop; :213 test_an_unreadable_figure_is_a_crash_with_its_reason; :221 test_a_timeout_is_a_crash; :232 test_the_template_loads_with_every_field; :244 test_a_missing_field_is_refused_and_named; :252 test_an_unknown_field_is_refused_and_named; :264 test_command_line; :304 test_a_new_ignored_file_is_a_change_outside_mutable_and_is_cleaned_between_trials; :320 test_a_proposer_that_raises_is_a_recorded_crash_and_the_loop_goes_on; :331 test_the_report_is_returned_and_written_when_the_loop_itself_fails; :344 test_a_crashed_trial_keeps_every_attempt_and_the_figures_that_were_parsed; :362 test_the_limit_of_the_guard_is_written_in_the_loop_and_in_the_control_file_template.
test_stage7d_platform.py: :48 test_every_paper_order_and_fill_row_has_its_node; :71 test_each_fill_fills_one_order_and_each_order_has_a_rule_version; :93 test_the_trial_counts_equal_counts_made_from_the_journal; :123 test_a_second_load_writes_nothing_new; :133 test_no_mid_no_cost_no_result_figure.
test_stage7f_rule_versions.py: :38 test_each_edit_of_the_rules_is_a_trial_in_the_order_it_was_made; :52 test_each_paper_run_is_tied_to_the_rule_version_it_ran_under; :72 test_a_rule_version_rests_on_no_finding_yet_and_the_check_says_so; :85 test_the_rules_loop_has_its_control_file_guards_the_right_files_and_waits_for_no_figure.
No test grep hit for "arm", "workbook", "orchestrator" or "D0" in these files was checked beyond the names above.

## NOT FOUND
- Teacher arms D0 to D5 definitions: none in /home/user/Markets (*.md, *.py, tools, research/kalshi/frankie_boss, .claude/skills, whole repo for \bD0\b and \bD5\b), nor in markets-data experiments/.
- Build plan workbook file (Frankie_BOSS_Build_Plan_R4_20260921.xlsx): not on disk in either checkout (Glob *.xlsx, Glob *[Bb]uild*[Pp]lan*, Glob *Frankie_BOSS*). Its text export of the Experiment Arms sheet: none.
- Experiment Arms, workbook arms, orchestrator steps or teacher arms inside experiments/trials.jsonl, MANIFEST.json, or tools/exp_dag.py: none.
- Table names and node kinds in exp_dag.py: none (only STATUSES and SQLITE name).
- Not read: frankie_exp_dag.sqlite (binary, excluded by instruction).
- Searches made: plan file (Grep first users|Experiment Arms|orchestrator|D0|D5|teacher arm); exp_dag.py (Grep add_parser, arm, orchestrator, teacher, workbook, xlsx, D0-D5, TABLE, CREATE, STATUSES, class/def); tests/ (Grep exp_dag); markets-data *.xlsx and build-plan globs; MARKET_DATA_INDEX.md; trials.jsonl (Grep, -o and count); MANIFEST.json (Read); graph/nodes (Grep); markets-data (Grep for Experiment Arms and D0-D5).
- Also the mentions in markets-data graph/ and tasks/ listed in sections 4 and 5 are notes about the record, not the record's own content.
