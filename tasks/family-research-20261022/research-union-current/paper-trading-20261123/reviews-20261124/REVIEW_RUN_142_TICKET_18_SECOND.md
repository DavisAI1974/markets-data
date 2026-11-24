# Reviewer run 142 (Opus): ticket 18, the second read, Markets dfb5879..974e208

Kept word for word as the agent returned it, 2026-11-24 (twenty-fifth session). Nothing below this line is the main session's.

---

REVIEW, agent run 142: ticket 18, second read. Markets dfb5879..974e208, files tools/kgraph/run_plan.py and tests/agent_program/test_run_plan.py.

I read only. Nothing was edited or committed, and no sub-agent was used. The scratch git repositories were under /tmp/run142 and are now deleted.

## Scope of the change
- In dfb5879..974e208 the builder's ticket-18 commits are 313c7da (run_plan.py +119/-30, test_run_plan.py +200) and d7962d0 (test_run_plan.py +9/-2). They touch no other file.
- The other commits in that range are merges of other tickets' branches: run_record (19), outcome (04), auditor_called (03b), ingest_artifacts, defend (02, 03).
- d7962d0's subject says "the next unused run number is computed in the write check". The builder's note says this subject differs from the one it was given.
- No new AWS, boto3 or S3 dependency. No market data and no figures are involved.

## The tests
`MARKETS_DATA=/home/user/markets-data python3 -m pytest tests/agent_program/test_run_plan.py -q`: **22 passed in 25.91 s**.

## One-line changes put back
Each was applied alone to a scratch copy of the two files and run against the real record.
- **M1** ("at the limit" counts as PASSED, run_plan.py:276 `>=`): 6 failed. check_117_kept_at_the_limit, check_116_four_of_25, check_116_no_harness_total..., plan_committed_before..., paired_plan_outside..., git_order_without_start_time...
- **M2** (the hand-back counted as a tool call, :180): 5 failed. check_117_kept_at_the_limit, check_116_four_of_25, check_passed_branch_paired_plan, plan_committed_before..., paired_plan_outside...
- **M3** (the "already has a line" refusal dropped, :109): 1 failed, write_refusals_and_a_new_plan.
- **M4** (no plan exits 0, :289): 2 failed, check_109_has_no_plan and check_96_with_no_plan...
- **M5** (the token line from the transcript's sum, :254): 4 failed. check_117_kept_at_the_limit, check_117_tokens_and_wall_clock_lines, plan_committed_before..., paired_plan_outside...
- **M6** (a late plan does not fail, :313 `bad = True` dropped): 2 failed, plan_committed_after... and git_order_from_the_lines_start_time...
- **N1** (the edited-plan comparison dropped, :228 always "unchanged"): 1 failed, plan_edited_after_its_add_commit_is_exit_1.
- **N2** (a plan not in git does not fail, :298 `bad = True` dropped): 1 failed, plan_not_in_git_is_exit_1.
- **N3** (`write` accepts a run whose plan path is in git history, :106 `if False`): 1 failed, write_refuses_a_run_whose_plan_is_in_git_history...

## The nine points

### 1. A plan edited after it was committed
**Code:** `_git_state` (run_plan.py:214-228) runs `git log --diff-filter=A --format="%H %cI" -- <rel>`. It takes the oldest add (`rows[-1]`, :224) and compares the sha256 of the file read with the sha256 of `git show <add>:<rel>`. :302-305 prints both hashes and sets exit 1.

**Real record:** all 30 plans, 114 to 143, read "unchanged since it was added".

**My scratch cases**, run 117's real plan, line and transcript, with only the commit dates the scratch's own:
- **Edited after the add:** held by the test, and N1 is caught.
- **Committed at 13:08:54 as draft.json, renamed to run-0117.json at 13:20:** "unchanged" and "committed 13:20:00 AFTER the run began", exit 1. Because the log is limited to the new path, it treats the rename commit as the add.
- **Added at 13:08:54, moved to old/ at 13:20:** `check` reads "no plan", exit 1. With `--plan old/run-0117.json` (inside the root) it reads "AFTER", exit 1, because the move commit is taken as the add.
- **Added on a branch at 13:08:54, merged --no-ff at 13:09:30** (B1b, a real two-parent merge): measured from the branch commit, "before", exit 0.
- **Added inside the merge commit itself** (B2b: two parents, `git ls-files` lists the plan): `check` prints "the plan file is not in git", exit 1. The cause is that `git log` without `-m`/`--diff-merges` shows no diff for a merge (:219-223). This message is not true for that repository.
- **Branch add authored 13:08:54, rebased at 13:20** (B3: committer 13:20, author 13:08:54, same bytes): "AFTER", exit 1. The git order is the committer date (`%cI`, :219), which a rebase moves and which anyone committing can set. The tests set it themselves with GIT_COMMITTER_DATE.
- My first attempt at the merge cases (B1/B2) made no merge: checkout failed on an invalid date variable and the log showed a single parent. Only B1b and B2b above are merges.

**Open:** the plan added in a merge commit (wrong message), and what a rename or move means for the add time.

### 2. A plan never committed, or a `--plan` outside the repository
**Code:** :297-300, a plan not in git sets exit 1. :295-296, any `--plan` outside the data root prints "not measured for a paired plan" and does not set exit 1.

**Tried:**
- Plan in the root, never committed: exit 1.
- Untracked plan inside the root under another name, passed as `--plan`: exit 1.
- The same run-117 bytes copied outside the root, as `--plan`: exit 0.
- An outside copy with max_tool_calls set to 999 (C2): prints "max_tool_calls: plan 999, reached 30, kept" and "not measured for a paired plan", exit 0.

**What the builder was told:** outside the root is allowed "only for the paired check". The code has no way to know a check is paired. Nothing compares the plan's `run` field with `--run`. The test test_paired_plan_outside_the_data_root_is_allowed_and_git_order_not_measured (test_run_plan.py:289-297) itself uses run 117's own plan with run 117, which is not a pair, and asserts exit 0.

**Open:** an uncommitted or edited plan given through an outside `--plan` reads exit 0.

### 3. Whether a plan came before its run
**Code:** :292-294 take the transcript's first timestamp, else the line's `started_at`. :308-309 print the exact sentence "not measured: the run's line holds no start time and no transcript is kept". No wall clock is used.

**Real record:** `jq -c 'select(.started_at) | .run'` returns nothing. 0 of 156 lines carry `started_at`.

**Tried** on a copy of run 117's line, with no transcript:
- `"2026-11-24T13:10:23.610Z"`: "before", exit 0.
- `""`: treated as absent, prints the sentence, exit 0.
- `"2026-11-24T13:10:23"` (no zone): uncaught `TypeError: can't compare offset-naive and offset-aware datetimes` at :310, traceback, exit 1.
- `1764000000` (epoch): uncaught `ValueError: Invalid isoformat string` at :294, traceback, exit 1.

**Not measured:** the newer recorder's real `started_at` format, because no real line holds one. I did not read run_record.py.

**Independent comparison of every kept transcript** (first timestamp against `git log --diff-filter=A --format=%cI` of its plan in /home/user/markets-data): the plan add came before the first line for all 14 kept transcripts that have a plan.

| Run | Plan added | First line |
|---|---|---|
| 115, 116, 117 | 13:08:54 | 13:10:23 |
| 118, 120 | 13:22:10 | 13:23:23 |
| 123, 124, 125 | 13:36:21 | 13:37:55 |
| 126, 127 | 13:38:52 | 13:39:31 |
| 132, 133 | 13:47:52 | 13:49:28 |
| 134 | 13:48:12 | 13:49:28 |
| 135 | 13:49:49 | 13:50:17 |

- The smallest margin is 28 s, for run 135.
- Transcripts 109, 111, 112 and 113 have no plan (they come before 114).
- No real run has its plan added after its first transcript line.
- `check` measures the git order for those same 14. It cannot measure it for 16: 114, 119, 121, 122, 128, 129, 130, 131 and 136-143.

**Open:** start-time parsing that ends in a traceback.

### 4. `write` refusals
**Code:**
- :89-90 refuses a run below 1.
- :97-100 refuse max_model_calls, max_tokens, max_wall_clock_s and max_concurrent_workers below 1.
- :106-108 refuse a run whose plan path is in git history (`_git_history`, :206-211).

**Tried:**
- Runs 0 and -3: refused.
- All limits 0: refused, naming the four keys.
- Plan added, then its deletion committed, with another plan left in the folder: refused "in git history", rc 2.
- Plan deleted from the worktree only: refused the same way.
- One case of mine where deleting the only plan removed the run-plans folder was refused by the folder check (:60-61), not by the history check.
- A data root that is not a git repository: `write` writes the plan, because `git log` fails and :211 returns False. `check` then exits 1 with "not in git".

**Open:** nothing beyond what is listed.

### 5. The plan's own `max_tokens_is`
**Code:** :281-282 print the plan's sentence or "the plan holds no max_tokens_is". :253-256 give "no harness total on the run's line: this limit cannot be shown kept". :286 counts the unmeasured limits.

**Run 117:** "max_tokens: plan 150000, reached 91604, kept", wall clock 80.8 of 900, 2 of 8 unmeasured. This matches the independent figures.

**Count for the ticket:** at my second loop, 14 of 30 plans have a token limit that cannot be shown kept. At my first loop the count was 15.
- 4 of the 14 (137, 138, 142, 143) have no line in the record yet.
- 10 have a line without a harness total: 116, 118, 120, 122, 126, 128, 129, 135, 136, 141.
- The record moved while I read: 131, 136, 140 and 141 gained lines, and plan 143 appeared.

**Only the newest line is read (:77-79):**
- Run 128's lines are (52,854 tokens, 6 tool calls) then (no total, 13 tool calls). `check` reports the token limit as not measurable even though an earlier line holds a total.
- Run 131 has three lines: 91,151/14, none/20, 115,790/25.
- Runs 124, 133 and 139 have identical duplicate lines.
- Speculation: two-part builder runs write one line per hand-back. Which line stands for the whole run is not decided in code.

**Open:** which line holds a run's figures.

### 6. `check` on a run with no plan
**Code:** :287-289 print every figure, then the no-plan sentence, then exit 1.

**Measured directly** (not through sed): `check --run 96` rc=1. The test asserts "max_graph_writes: no plan, reached 32". `check --run 9999` (no plan, no line, no transcript) rc=1, "7 of 8".

### 7. `brief` repeated the stop sentence
**Code:** :145-149. The test asserts "what is open" appears once. M-style removal not tried.

### 8. The docstring
:15-17 state that the graph-writes count holds `written_by == run:NNNN` lines in graph/nodes and graph/edges, and does not hold `made_by` lines or graph/reads, graph/merges and graph/evaluations. :19-21 describe the git rule. :19-21 do not mention the outside-`--plan` exemption.

### 9. Tests for the two changes, and the separated section
M5 and M6 are now caught (4 and 2 failing). The section header is at test_run_plan.py:215-219, "CASES THE REAL RECORD DOES NOT HOLD".

**What the section says is the scratch's own:** the git repository, the commit dates, one edited copy, one uncommitted plan, and a copy of run 117's line with a start time added. FIRST (:220) is the real first timestamp of run 117's transcript. The 13:20:00 "late" date is one of the named commit dates.

**Three scratch-owned things not in the header list:**
- The key deleted from the plan in test_plan_without_max_tokens_is_says_so. Its own comment at :341 says so.
- The record emptied in test_write_refuses_a_run_whose_plan_is_in_git_history... Its comment is at :335.
- The plan copied outside the root in the "paired" test, which is not a pair.

No market data and no figure is made up. Every figure asserted comes from real plan, line or transcript files.

## Real `check` on every plan, 114 to 143
- Exit 0 on all 30. No PASSED, no "not in git", no "changed", no AFTER.
- Run 117: tool calls 30/30 "kept (at the limit, not passed)". Run 116: 4/25.
- Runs that have a plan and no line also get exit 0, with graph writes 0 "kept": 137, 138, 142 (this run), 143.

## The ticket's "Shown done by"

**First half: a plan exists before each run.**
- Code: `write` refuses once a line exists (:109) or the path is in history (:106). `check` fails a run with a line and no plan (:287-289). `check` also fails a run with neither plan nor line (run 9999, rc 1), but only when someone names that number.
- Nothing in run_plan.py lists runs that have no plan, no line and no transcript. I did not read ticket 03b's command, so whether it covers that case is not measured. My answer comes from reading :248-249 and :287-289.
- On the real record the main session's habit holds for 14 of 14 kept transcripts. For the other 16 plans the order cannot be measured.

**Second half: a run that reaches a limit stops and returns what is done, what is open and why.**
- Runs 117, 126 and 127 read "at the limit, not passed" at 30/30, 20/20 and 20/20.
- Their final SubagentHandback texts:
  - 117 ends "TRUE TOOL CALL COUNT: 30 (limit reached; stopping)" after a "NOT FOUND" list.
  - 126 says "TOOL CALLS: 20 (the limit)" and has a "NOT FOUND / NOT DONE" list.
  - 127 has a "NOT FOUND / NOT CAPTURED" list. The last 700 characters I printed do not include a count line.
- No code reads the hand-back text. `check` shows only the counts. Run 126's tokens are not measurable (no harness total).

## Speculation (labelled)
- A plan committed through a merge, rename or rebase seems unlikely given the main session's present habit of plain commits. The B2b and B3 cases would only arise if that habit changes.
- The newer recorder may write `started_at` with a zone, in which case :294/:310 parse it. This is unverified.

## Open after this read

**For the builder:**
- A plan added inside a merge commit reads "not in git" (:219-223).
- A rename or move commit is taken as the add time. The order rests on the committer date (B3).
- Any `--plan` outside the root, including the run's own plan or an edited copy (999), exits 0. "Paired" is not checked (:295-296). The paired test uses an unpaired plan.
- `started_at` without a zone, or as a number, ends in a traceback (:294, :310).
- Only the newest line is read (:77-79): run 128's earlier total of 52,854 is not used, and run 131's three lines differ.
- `write` into a data root that is not a git repository writes the plan (:211).
- The docstring does not mention the outside-`--plan` exemption.
- (Carried from the builder's own list) a `corrects` field holding a sentence is not matched (:78).

**Settled by the plans:**
- Tokens are held against the harness total.
- "At the limit" is kept.
- Graph writes are counted by `written_by`.

**What code cannot hold** (for the ticket):
- Stopping an agent mid-run.
- Requiring a plan before a run started from the chat. Nothing lists a run with no plan, no line and no transcript.
- Workers and retries, which no transcript records.
- Tokens for runs with no harness total: 14 of 30 plans at my second loop (10 with a line, 4 with no line yet), and the count moves as the record grows.
- Whether a hand-back says what is done, what is open and why.

## Test counts and commits
- 22 passed at 974e208.
- Commits read: dfb5879, 313c7da, d7962d0, 974e208 (the merge). Other merged commits were listed only.

## Housekeeping and tool calls
- /tmp/run142 and /tmp/pytest-of-root are deleted.
- `git status --short` is empty in /home/user/markets-data and in /home/user/Markets-r142 (still at 974e208).
- A scratch file /tmp/claude-0/-home-user/3356516d-d71a-5e13-907d-ff8d8ffcb6d4/scratchpad/mut.py and c9999.txt remain, outside any repository.
- Tool calls: 10 Bash calls plus 1 advisor call, so 11 before this hand-back, or 12 counting it. The limit is 15.
- One of the 10 Bash calls did not run. The safety check refused an `rm` of a path built from shell variables. I re-issued it in `"${d:?}/${R:?}/..."` form.

## Files
- /home/user/Markets-r142/tools/kgraph/run_plan.py
- /home/user/Markets-r142/tests/agent_program/test_run_plan.py
- /home/user/markets-data/tasks/family-research-20261022/research-union-current/paper-trading-20261123/run-plans/
- /home/user/markets-data/tasks/family-research-20261022/research-union-current/paper-trading-20261123/agent-runs.jsonl
- /home/user/markets-data/tasks/family-research-20261022/research-union-current/paper-trading-20261123/transcripts/
- /home/user/markets-data/tasks/family-research-20261022/research-union-current/paper-trading-20261123/builder-20261124/BUILDER_RUN_128.md
- /home/user/markets-data/tasks/family-research-20261022/research-union-current/paper-trading-20261123/reviews-20261124/REVIEW_RUN_134_TICKET_18.md
