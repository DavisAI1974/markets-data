# Builder run 128 (Sonnet): ticket 18, run_plan

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
