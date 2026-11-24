# Scout run 157 (Haiku): where things are for tickets 18 and 19

Everything below this line is the agent's own report, word for word; nothing below it is the main session's.

## Hand-back 1 of 1

Scout run 157, tickets 18 and 19.

Repo state: /home/user/Markets/.git/HEAD = ref ccr-144315dd-pta2ze; .git/refs/heads/ccr-144315dd-pta2ze = 74006f29a47e0aab9189c83afcff2d2c7a136bb4 (matches 74006f2). Line numbers below are as the files stand on disk, read with Read/Grep only; no git command was run.

Files read: /home/user/Markets/tools/kgraph/run_plan.py, /home/user/Markets/tools/kgraph/run_record.py, /home/user/Markets/tests/agent_program/test_run_plan.py, /home/user/Markets/tests/agent_program/test_run_record.py.

=== TICKET 18 (run_plan.py / test_run_plan.py) ===

Point 1: a --plan that does not exist exits 1 with "its limits were not written before it started".
1. Behaviour: _check, /home/user/Markets/tools/kgraph/run_plan.py def _check at :253.
   - :255-257 prints PAIRED CHECK when a.plan is set.
   - :259 plan, path = _load_plan(paper, a)
   - /home/user/Markets/tools/kgraph/run_plan.py def _load_plan :148-152: path = Path(a.plan) if given; `if not path.exists(): return None, path`.
   - :317-319: `if plan is None: print(f"run {a.run} has no plan file at {path}: its limits were not written before it started"); return 1`
   - :320-324: `if a.plan:` prints "plan in git: not measured..." and `return 3`. The --plan branch is reached only if the plan exists.
   - Docstring: run_plan.py :19-21 ("PAIRED CHECKS: ... the exit code is 3"), exact at :20.
   - Also :8 usage line: `check --data <markets-data> --run N [--transcript F] [--plan F]`.
2. Existing checks touching it: test_run_plan.py def test_check_109_has_no_plan :81 (line :83 asserts "no plan file" in output, without --plan); test_check_96_with_no_plan_still_counts_its_graph_writes :191 (line :195 asserts "no plan file"). No check passes a missing --plan file. test_paired_check_of_an_edited_copy_of_the_runs_own_plan_is_exit_3_not_0 :350 covers the existing --plan case only.
3. Separated section header: /home/user/Markets/tests/agent_program/test_run_plan.py :220-227 (comment block "CASES THE REAL RECORD DOES NOT HOLD ..."), through the file's last def at :420 (test_git_order_... and onward; file read only to :402). Cases with "# change:"-style comments are not used here; the section uses its own scratch-described comment.
4. NOT ALREADY IN CODE: no test or code branch exits 1 for a missing --plan path.

Point 2: no check holds the earliest-add choice at run_plan.py :246.
1. Behaviour: _git_state, /home/user/Markets/tools/kgraph/run_plan.py def _git_state :235; :240-242 run git log --diff-merges=first-parent --diff-filter=A --name-only; :246 `h, when = min(rows, key=lambda x: datetime.fromisoformat(x[1]))`; :250 returns the state.
2. Checks touching it: test_plan_added_inside_a_merge_commit_is_found :365 (single add in a merge commit, asserts "unchanged since it was added" and "before the run began"); test_plan_committed_before_its_run_began_is_exit_0 :261; test_plan_committed_after_its_run_began_is_exit_1 :252; test_plan_edited_after_its_add_commit_is_exit_1 :271. None has two add commits of the plan.
3. Section: test_run_plan.py :220-227 header (through end of file).
4. NOT ALREADY IN CODE: no test with a plan added on two branches (E3 shape). Searched "min(rows" and "earliest" in tests/agent_program: no hit.

Point 3: no check holds tracked_no_add (run_plan.py :245, :331-333).
1. Behaviour: run_plan.py :244-245 (`ls-files --error-unmatch`, returns "tracked_no_add" when tracked); :331-333 in _check: `elif state == "tracked_no_add": bad = True; print("plan in git: tracked, and the commit that added it could not be found")`.
2. Checks touching it: none. Grep for "tracked_no_add" in tests/agent_program: no hit. Related but different: test_plan_not_in_git_is_exit_1 :288 (the not_in_git branch, :327-330). test_write_refuses_a_run_whose_plan_is_in_git_history_though_the_file_is_gone :327 is a write-side test, not this check.
3. Section: test_run_plan.py :220-227.
4. NOT ALREADY IN CODE: no test for tracked_no_add.

Point 4: shallow clone or graft gives the boundary commit as the add (AFTER, exit 1).
1. Behaviour: _git_state run_plan.py :240-250; the AFTER comparison is _check :346-350 (`elif when.astimezone(start.tzinfo) <= start:` ... `print(f"git order: committed ... AFTER the run began ...")`, bad=True).
2. Checks touching it: test_plan_committed_after_its_run_began_is_exit_1 :252; test_plan_committed_before_its_run_began_is_exit_0 :261.
3. Section: test_run_plan.py :220-227.
4. NOT ALREADY IN CODE: searched "shallow" and "graft" in run_plan.py and tests/agent_program/test_run_plan.py: NO HITS. No shallow-clone detection exists.

Point 5: date-only started_at reads as 00:00 UTC and fails the order (exit 1).
1. Behaviour: _start, run_plan.py :354-369. :358 `v = line.get("started_at")`; :364 `datetime.fromisoformat(v.replace("Z", "+00:00"))`; :367-368 `if t.tzinfo is None: return t.replace(tzinfo=timezone.utc), None, "read as UTC: the line names no zone"`. A date-only string gives naive midnight, so it goes to :368.
2. Checks touching it: test_start_time_forms_without_a_transcript :387 (cases at :392-396 use "...13:10:23.610000Z", "...13:10:23.610000" (no zone, asserts "read as UTC: the line names no zone"), an int, and "yesterday"; :401-402 "2026-11-24T13:00:00" with no zone gives exit 1). No date-only value ("2026-11-24") is in any case. test_git_order_from_the_lines_start_time_without_a_transcript :305 and test_git_order_without_start_time_and_without_transcript_says_so :317 also exist.
3. Section: test_run_plan.py :220-227.
4. NOT ALREADY IN CODE: no date-only branch in _start; no test with a date-only value.

Point 6 (minor): test header does not name other.txt, main.txt or the real run-0128.json copy.
1. Header: test_run_plan.py :220-227. Quoted :226-227: "Real: run-0117.json, run 117's kept transcript and line, run-0116.json, and for run 128 the record as it was at markets-data 04d8a0f (read with git)." Also :222-225 names the merge commit, the edited plan, max_tokens_is, uncommitted plan, the start-time copies, the git-history case, the --plan copies, and the non-git folder.
2. The names are in the test body: other.txt at test_run_plan.py :370 and :371; main.txt at :374-375 (test_plan_added_inside_a_merge_commit_is_found :365). run-0128.json copy at :410 (test_an_earlier_line_with_a_harness_total_is_named :405, shutil.copy of run-0128.json at :410).
3. Section: :220-227.
4. NOT ALREADY IN CODE: the header does not name them (as the reviewer says).

=== TICKET 19 (run_record.py / test_run_record.py) ===

Point 1 (N3a, :362): model_replies value differs; no check holds it.
1. Behaviour: _differences, /home/user/Markets/tools/kgraph/run_record.py def _differences :354; :358-363:
   `mine, theirs = r.get(k), f[k]` / `if k == "model_replies":` / `if mine is None: out.append(f"model_replies: the line holds none, transcript {theirs}")` / `elif mine != theirs: out.append(f"model_replies: line {mine}, transcript {theirs}")`.
   Also cmd_append sets model_replies at :268 and figures_of sets "model_replies" at :140.
2. Checks touching it: test_trap_a_line_whose_figures_differ_from_its_kept_transcript_is_named :492 (its model_replies removed at :499, asserts `"model_replies" in l` for the none-case at :505, i.e. the :360-361 branch only). test_figures_run_117_match_the_auditors_measure :93 and test_figures_run_116 :108 (figures, not _differences). Grep "model_replies" across tests/agent_program: hits at test_run_record.py :100, :131, :207, :494, :499, :505; no assertion on the value-differs message "model_replies: line". Grep "_differences" in tests: no hit.
3. Section: /home/user/Markets/tests/agent_program/test_run_record.py "# change:" section begins at :438-441 (separator at :438 and :441; header of section not quoted here). Its def at :492 carries "# change:" at :493.
4. NOT ALREADY IN CODE: no test for line-holds-a-different-value; the code branch exists at run_record.py :362-363.

Point 2: R1 alone and R2 alone; no check holds either. The sha refusal is unreachable for any sidecar keep writes (reading of the code).
1. Behaviour, R1 (one transcript is one run's): _tie, /home/user/Markets/tools/kgraph/run_record.py def _tie :161. Sha refusal: :198-199 `if what == "kept sidecar" and d.get("sha256") == f["_sha256"]: raise Refused(f"these bytes (sha256 {f['_sha256']}) are already kept as run ...")`. Agent-id refusals: :186-188 (newest line), :195-197 (plans and kept sidecars). Known-plan/sidecar check :172-181.
   Behaviour, R2 (line already on record compared): _compare_with_line, run_record.py def :203; :212-214 model check (only if model string startswith "claude-"); :215-217 input_tokens/output_tokens check. Called at :232 (cmd_append) and :315 (cmd_keep).
2. Checks touching R1: test_one_transcript_is_one_runs_not_two :405 (asserts "run 107" in refusal for keep and append of run 107's bytes as 108); test_a_transcript_that_is_run_108s_own_agrees_with_its_line_and_run_107s_does_not :414; test_the_agent_id_must_be_the_transcripts_own :377; test_a_brief_that_names_no_run_is_tied_by_the_agent_id_alone :393; test_trap_a_run_whose_line_holds_another_agent_id_refuses_this_one :546 (agentId replaced, "aother0000000000"); test_keep_refuses_a_kept_file_with_another_sha :227 (different sha on kept gz, not the R1 sha refusal at :199).
   Checks touching R2: test_append_refuses_a_run_that_has_a_line_then_writes_a_correction :118; test_a_correcting_line_keeps_the_earlier_tokens_reported_unless_given_again :138; test_trap_a_line_already_on_record_is_compared_with_the_transcript :556; test_trap_a_line_with_more_tokens_than_its_transcript_refuses_a_correction :571.
3. Section: test_run_record.py :438-441 separator; "# change:" cases from :453 (test_trap_a_sentence_naming_another_run... :453) through :627 (test_trap_a_short_text... :626).
4. NOT ALREADY IN CODE: the sha refusal at :198-199 has no test that reaches it (test_one_transcript, :405, is refused on the agent id at :188, and the sidecar-without-agent_id case is not tested). R1 alone and R2 alone: no test isolates them.

Point 3: --agent-type X --outside-roster X is accepted with any X; --outside-roster "" falls back to the role without a refusal.
1. Behaviour: cmd_append, /home/user/Markets/tools/kgraph/run_record.py def cmd_append :228; :235-236 (refuses only when both given and differ); :239-240 `if a.outside_roster: agent_type = a.outside_roster`; :241-244 else path (ROLES check at :243-244); "" is falsy, so :241-242 runs and agent_type = a.agent_type or a.role. Role check :237-238. ROLES at run_record.py (ROLES tuple; grep found none under that exact name in the hits list; see NOT FOUND).
2. Checks touching it: test_outside_the_roster_the_agent_type_is_the_text_given :424 (line :428 general-purpose "what" accepted; :431 with --agent-type builder refused "exactly one" asserted at :432; :433 wizard refused via agent type; :434-435 plain reviewer). No test passes "--agent-type X --outside-roster X" with X equal, and no test passes --outside-roster "". Grep "outside-roster" "" in tests: no hit.
3. Section: test_run_record.py :438-441 separator; the test :424 sits before it, in the "# change:"-free part. The "# change:" section starts at :453.
4. NOT ALREADY IN CODE: the equal-value accept case and the "" fallback are not tested (per the reviewer and by grep).

Point 4: test :329/:331 have the two written-in zeros; the 108 test asserts only the accept side.
1. Behaviour under test: COUNTS line from cmd_missing, /home/user/Markets/tools/kgraph/run_record.py def cmd_missing :382 (live counts; reviewer says the counts line is at :473-474 in main-era text; not re-read here).
2. Checks touching: test_missing_with_live_counts_on_the_record_as_it_was_at_7de89a4 :308. Written-in zeros at test_run_record.py :329 `assert f"live transcripts {n}, of which {n} name one run and 0 name none" in counts` and :331 `assert f"live transcripts not kept 0;" in counts`. Also :330 asserts "live transcripts with no line ...". The 108 test is test_a_transcript_that_is_run_108s_own_agrees_with_its_line_and_run_107s_does_not :414, asserting only the accept side (:419 rc 0; :421 assertions); t107 is assigned at :415 and not used.
3. Section: test_run_record.py :438-441 separator; :308 is in the earlier part (before :438).
4. NOT ALREADY IN CODE: the zeros are written into the assertion; the reviewer's point stands (no test asserts the refusal side of the 108 case). The test at :414 is in the separated section (after :441, real-record cases), so the 108 accept-only test sits in section "# change:" area per its range. (Its def is at :414, i.e. before the "# change:" section starting :453; within the :438-441 separator block region.)

NOT FOUND (patterns and paths searched, no hit):
- "shallow", "graft" in /home/user/Markets/tools/kgraph/run_plan.py and /home/user/Markets/tests/agent_program/test_run_plan.py.
- "tracked_no_add" in /home/user/Markets/tests/agent_program (only in run_plan.py :245, :331).
- "min(rows" and "earliest" in /home/user/Markets/tests/agent_program.
- "_differences" in /home/user/Markets/tests/agent_program.
- "outside-roster" with an empty value "" in /home/user/Markets/tests/agent_program.
- ROLES definition: grep for ROLES in run_record.py not separately run; the tuple name is used at run_record.py :237-244 but its def line was not located.
- Not read: run_record.py cmd_missing body (:382-475) and the COUNTS line itself; test_run_record.py :1-92 header and :442-492 bodies; the run_plan.py/test_run_plan.py tail after :402.

TOOL CALLS: 17 of 30 used (3 + 4 + 1 + 3 + 3 + 1 + ... ; reads/greps counted as made). Model calls: 0 of 30 by me beyond this run. Stopped because all ten points were covered and the remaining gaps were listed above.
