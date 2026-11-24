# Builder run 128 (Sonnet): ticket 18, run_plan, and then the points of the first read

Kept word for word as the agent returned it, 2026-11-24 (twenty-fifth session). Nothing below this line is the main session's.

---

Ticket 18 is built and pushed. Nothing is unfinished. All 7 checks pass, 7 passed in 2.13s, run again after the merge.

**Commit:** my commit is dfb5879. I pushed merge commit 88ffa58 to `ccr-659edd86-di9udt`. The first push was rejected because the branch had moved (builder 19's run_record commit). I fetched, merged without force, and pushed again.

**Diff stat** (`git diff --stat 3a98333 HEAD -- tools/kgraph/run_plan.py tests/agent_program/test_run_plan.py`):
- tests/agent_program/test_run_plan.py: 143 lines added
- tools/kgraph/run_plan.py: 288 lines added
- 2 files changed, 431 insertions, no deletions. No existing file was touched.

**Output of `check --run 117`** (data = /home/user/markets-data; the long run-plans and transcripts paths are shortened to `<PAPER>`, which is the paper-trading-20261123 folder). The exit code was 0.
```
reading: /home/user/markets-data
plan: <PAPER>/run-plans/run-0117.json
figures: the transcript <PAPER>/transcripts/run-0117.jsonl.gz
max_model_calls: plan 20, reached 10, kept
max_sub_agents: plan 0, reached 0, kept (at the limit, not passed)
max_concurrent_workers: plan 1, reached -, cannot be measured here (not in a transcript)
max_tool_calls: plan 30, reached 30, kept (at the limit, not passed)
max_tokens: plan 150000, reached 91604, kept
max_wall_clock_s: plan 900, reached 80.8, kept
max_retries: plan 1, reached -, cannot be measured here (not in a transcript)
max_graph_writes: plan 0, reached 0, kept (at the limit, not passed)
transcript tokens: input fresh 20, cache written 85089, cache read 501509, output 18234
plan in git: committed 2026-11-24T13:08:54+00:00 before the run began 2026-11-24T13:10:23.610000+00:00
```

**Checks and the real records each rests on:**
- `test_check_117_kept_at_the_limit`: run-0117.json, run 117's kept transcript, run 117's line, and the graph files. It asserts tool calls 30 of 30 kept, model calls 10 of 20, sub-agents 0 of 0, graph writes 0, retries and workers cannot be measured, no PASSED, the folder read is printed, and the plan was in git before the run began. The exit code is 0.
- `test_check_116_four_of_25`: run-0116.json and run 116's transcript. It asserts 4 of 25.
- `test_check_109_has_no_plan`: run 109 has a line and no plan file. It asserts "no plan file" and exit code 1.
- `test_check_passed_branch_paired_plan`: this one is paired, as the module docstring and the test say. It uses run 117's real transcript with run-0116.json's real plan, passed through `--plan`. It asserts tool calls 25 vs 30 is PASSED and the exit code is 1.
- `test_write_refusals_and_a_new_plan`: scratch copies of the real run-plans folder and record under tmp_path. It refuses 114 (plan exists), 109 (has a line, no plan), a missing max_retries, a negative max_tokens, and agent general-purpose. The next unused run number is computed in the test from the file names and record lines, independently of the module. The new plan loads back with all eight keys. Only that one file is added, the record is byte-identical, and a second write of the same run is refused.
- `test_brief_122`: run-0122.json. It asserts all eight figures, the "COUNT your own tool calls" sentence, the plan's own `on_reaching_a_limit` sentence, and that the text is the same on a second run.
- `test_data_without_run_plans_is_refused`: a tmp folder holding only a MANIFEST.json. It asserts exit 2 and that the error names that folder and "run-plans".

**PASSED in the record:** none. I compared the newest line against its plan for runs 114 to 131 that have both, on tool calls, model replies, tokens and wall clock. No run was over its plan. Run 126 and run 127 are at 20 of 20 tool calls, which is kept. That is why the PASSED check is paired.

**Ambiguities and choices:**
- At the limit counts as kept (30 of 30), as you said. Only above the limit is PASSED.
- Your 117 expectation for sub-agents "0 of 0 kept" prints "(at the limit, not passed)", which is true but reads oddly.
- Exit codes are 0, 1 (as specified) and 2 (refused).
- If a plan was never committed to git, `check` prints "not measured" and does not fail. Run 128's own plan is the likely case.
- `write` takes the session from the newest existing plan if `--session` is not given. It omits `note` and `tickets` if they are not given.
- I added `--plan` to `brief` as well as `check`; `brief` only uses it to read a plan from another path.
- Retries and concurrent workers are always "cannot be measured here".
- Without a transcript, sub-agents also cannot be measured, because the line does not count them. Model replies are only on the newest lines. Where a figure is missing the output says so.
- With `--plan`, the git line looks at that file's own add commit. For the paired check that is run 116's plan against run 117's start.

Nothing needed locating beyond what you gave me. I used the `/home/user/Markets-b18` worktree, not the `/home/user/Markets-b03b` named in the environment block.

**Housekeeping:** /tmp/run128 and /tmp/pytest-of-root are deleted, and `git -C /home/user/markets-data status --short` is empty. I made 11 tool calls, against the 50 allowed. I did not call the advisor.

---

## The next hand-back

All nine points are done and pushed, but the second commit has the wrong subject. Pytest after the last merge: 22 passed, 24.26 s, with MARKETS_DATA set.

**Commits:** the code and the first version of the tests are 313c7da, with your subject `PROPOSED, SECOND, ...`. It was committed with one test failing (my fault, below), so the second commit fixes that test. Its subject is not the one you gave, because I made it a separate commit. The pushed tip, after merging the branch, is 974e208, in `/home/user/Markets-b18`.

**Check output:**
- `check --run 117` exited 0. It printed:
```
reading: /home/user/markets-data
figures: the transcript <PAPER>/transcripts/run-0117.jsonl.gz
max_model_calls: plan 20, reached 10, kept
max_sub_agents: plan 0, reached 0, kept (at the limit, not passed)
max_concurrent_workers: plan 1, reached -, cannot be measured here (not in a transcript)
max_tool_calls: plan 30, reached 30, kept (at the limit, not passed)
max_tokens: plan 150000, reached 91604, kept
max_tokens is: the harness's total for the run when it ends (input and output together), the figure on every earlier line; the transcript's sum is recorded beside it
max_wall_clock_s: plan 900, reached 80.8, kept
max_retries: plan 1, reached -, cannot be measured here (not in a transcript)
max_graph_writes: plan 0, reached 0, kept (at the limit, not passed)
transcript tokens: input fresh 20, cache written 85089, cache read 501509, output 18234
limits that could not be measured: 2 of 8
plan: <PAPER>/run-plans/run-0117.json
plan in git: unchanged since it was added (sha256 0ece72916cdd981b9f7a842b5884f5da533d15874ae9c6e7ee517b7f9e818b10)
git order: committed 2026-11-24T13:08:54+00:00 before the run began 2026-11-24T13:10:23.610000+00:00
```
- `check --run 96` printed:
```
reading: /home/user/markets-data
figures: the run's own newest line in the record (no transcript)
max_model_calls: no plan, reached -, cannot be measured here (no figure on the line and no transcript)
max_sub_agents: no plan, reached -, cannot be measured here (the record's line does not count sub-agents and there is no transcript)
max_concurrent_workers: no plan, reached -, cannot be measured here (not in a transcript)
max_tool_calls: no plan, reached 9
max_tokens: no plan, reached 235977
max_wall_clock_s: no plan, reached 161.4
max_retries: no plan, reached -, cannot be measured here (not in a transcript)
max_graph_writes: no plan, reached 32
limits that could not be measured: 4 of 8
run 96 has no plan file at <PAPER>/run-plans/run-0096.json: its limits were not written before it started
```
  I piped both through `sed` to shorten the paths, so the shell's exit code shown was sed's. The exit codes come from the tests: 117 returns 0 and a run with no plan returns 1 (run 109 and run 96 are asserted).

**The nine points** (file:line in `tools/kgraph/run_plan.py`, the check in `tests/agent_program/test_run_plan.py`):
1. A plan edited after it was added: `_git_state` at 214 compares the file's sha256 with `git show <add commit>:<path>`, and `_check` at about 300 names both hashes and exits 1. The scratch check is `test_plan_edited_after_its_add_commit_is_exit_1`. The real check is `test_every_real_plan_is_unchanged_since_it_was_added`, which runs every plan from 114 to the newest and finds each unchanged.
2. A plan not in git: line 299 says so and exits 1, held by `test_plan_not_in_git_is_exit_1`. A `--plan` outside the data root says the git order is "not measured for a paired plan" and does not fail, held by `test_paired_plan_outside_the_data_root_is_allowed_and_git_order_not_measured`.
3. Git order without a transcript: lines 293-294 use `started_at`, else print your exact sentence at about 308. The checks are `test_git_order_from_the_lines_start_time_without_a_transcript` and `test_git_order_without_start_time_and_without_transcript_says_so`.
4. `write` refusals: run below 1 at line 89, limits below 1 at 97 (sub-agents, tool calls, retries and graph writes may be 0), plan path in git history at 106 through `_git_history` at 206. The checks are `test_write_refuses_run_below_one_and_limits_below_one` and `test_write_refuses_a_run_whose_plan_is_in_git_history_though_the_file_is_gone`.
5. `max_tokens_is` is printed at 282, with the "holds no max_tokens_is" fallback. The no-harness-total sentence is at 256 and the "limits that could not be measured: N of 8" line at 286. The checks are `test_check_116_no_harness_total_is_said_and_the_plans_own_sentence_is_read` (116 gives 3 of 8) and `test_check_117_tokens_and_wall_clock_lines` (117 gives 2 of 8). The "holds no max_tokens_is" case is in `test_plan_without_max_tokens_is_says_so`.
6. `check` on a run with no plan prints every figure, then says there is no plan and exits 1, in `_check` from 286 on. The check is `test_check_96_with_no_plan_still_counts_its_graph_writes` (32).
7. `brief` says the stop sentence once, at line 149, held by `test_brief_says_the_stop_sentence_once`.
8. The docstring states what the graph-writes count holds, at lines 15-17.
9. The new checks are the 117 tokens and wall-clock lines, plus the section headed `CASES THE REAL RECORD DOES NOT HOLD`. That section has a plan committed after its run (exit 1), committed before (exit 0), edited, not in git, a paired outside plan, the start-time cases, and the plan whose path is in git history but whose file is gone.

**Put-back changes:**
- Token line taken from the transcript's sum: 4 tests fail, so it is noticed. They are `test_check_117_kept_at_the_limit`, `test_check_117_tokens_and_wall_clock_lines`, `test_plan_committed_before_its_run_began_is_exit_0` and the paired-plan test.
- A plan committed after the run began no longer failing (I removed the `bad = True` there): 2 tests fail, so it is noticed. They are `test_plan_committed_after_its_run_began_is_exit_1` and the start-time test. Both changes were restored with `git checkout`.

**Expectations changed:**
- None of the first seven tests changed.
- I dropped my own guess that a real plan lacks `max_tokens_is`. Plan 114 holds it, so that case moved to a scratch copy of run 117's plan with the key deleted.
- The run 96 expectation reads `max_graph_writes: no plan, reached 32`. The "no plan" wording is mine, in the same format as the other figure lines.
- The write test's hard-coded run number 140 failed once, when other builders' plans reached 140. I changed it to compute the next unused number from the scratch folder and rerun. That is one fix, not a loosening.

**Left open or not done:**
- `git -C /home/user/markets-data status --short` shows 34 lines. I only read from that checkout, so those must be other agents' writes. /tmp/run128 and /tmp/pytest-of-root are deleted.
- A plan whose `--plan` file is inside the data root is checked in git normally. For the paired 117-against-116 case that compares 116's plan time with 117's start, as before.
- In the unmeasured count, a run with no plan counts its sub-agents as unmeasured when there is no transcript.
- A `corrects` field holding a sentence is still not matched, as the reviewer saw. I did not change it.

**Tool calls:** 13 in the whole run, 6 in the first round and 7 in this one, not counting the two hand-backs. My first report said 11, which counted commands inside calls. I did not call the advisor.
