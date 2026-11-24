# Reviewer run 149 (Opus): ticket 18, the third read, Markets 643ca97

Kept word for word as the agent returned it, 2026-11-24 (twenty-fifth session). Nothing below this line is the main session's.

---

# Reviewer run 149: third read of ticket 18 (builder run 128, third part, Markets 643ca97)

I read commit 643ca97. My working copy `/home/user/Markets-r149` is detached at cd9c7fd. `git diff --stat 643ca97 cd9c7fd` on the two files is empty, and 643ca97 is an ancestor of cd9c7fd. `git show --stat 643ca97` shows that the commit touches only `tools/kgraph/run_plan.py` (84 lines) and `tests/agent_program/test_run_plan.py` (110 lines), so its scope matches the second read's list. It adds no AWS, boto3, S3 or aws-mcp dependency.

## Tests
- At 643ca97 code, with `MARKETS_DATA=/home/user/markets-data`: **26 passed, 0 skipped, 0 failed** in 36.35 s. This matches the builder's 26.

## One-line changes put back
I made these changes on a `git archive` copy of cd9c7fd under /tmp/run149, never in the working copy, with one copy per change. The unchanged copy (BASE) gave 26 passed.

| Change | Fail | Checks that failed |
|---|---|---|
| M1 `>` to `>=` | 7 | check_116_four_of_25, check_116_no_harness_total..., check_117_kept_at_the_limit, git_order_without_start_time..., plan_added_inside_a_merge_commit, plan_committed_before..., start_time_forms |
| M2 hand-back counted as a tool call | 6 | check_116_four_of_25, check_117_kept_at_the_limit, check_passed_branch_paired_plan, paired_check_of_an_edited_copy..., plan_added_inside_a_merge_commit, plan_committed_before... |
| M3 "already has a line" refusal dropped | 1 | write_refusals_and_a_new_plan |
| M4 no plan exits 0 | 2 | check_109_has_no_plan, check_96_with_no_plan... |
| M5 tokens taken from the transcript's sum | 4 | check_117_kept_at_the_limit, check_117_tokens_and_wall_clock_lines, merge_commit, plan_committed_before |
| M6 git-order test made `True` | 3 | git_order_from_the_lines_start_time..., plan_committed_after..., start_time_forms |
| N1 `changed` dropped | 1 | plan_edited_after_its_add_commit_is_exit_1 |
| N2 `not_in_git` does not set bad | 1 | plan_not_in_git_is_exit_1 |
| N3 `_git_history` dropped | 1 | write_refuses_a_run_whose_plan_is_in_git_history... |
| P1 `return 3` to `return 0` | 2 | check_passed_branch_paired_plan, paired_check_of_an_edited_copy... |
| P2 plain `git log --diff-filter=A` | 1 | plan_added_inside_a_merge_commit_is_found |
| Q1 no-zone start time read as UTC-05:00 | 1 | start_time_forms |
| Q1b "read as UTC" note dropped | 1 | start_time_forms |
| Q2 earlier-line total taken from the newest line (`[-1:]`) | 1 | an_earlier_line_with_a_harness_total_is_named |
| Q3 non-git refusal dropped (:120) | 1 | write_into_a_folder_that_is_not_a_git_repository_is_refused |
| **Q4** `min(rows, ...)` to `rows[0]` (:246, newest add instead of earliest) | **0** | all 26 clean |
| **Q5** `tracked_no_add` always read as `not_in_git` (:245) | **0** | all 26 clean |
| Q6 `except ValueError` to `except KeyError` in `_start` (traceback) | 1 | start_time_forms |
| Q7 "PAIRED CHECK" header text changed | 2 | check_passed_branch_paired_plan, paired_check_of_an_edited_copy... |

- The counts for M1 to P2 match the builder's list.
- No check holds Q4 or Q5. The two cases below make both states with real git.

## Points 1 to 7

### 1. Paired check
**Code:**
- :255-257 prints "PAIRED CHECK: ..." as the first line.
- :321-324 prints "plan in git: not measured" and "git order: not measured", then `return 3`.
- The docstring at :19-21 says "whenever `check` is given `--plan` ... the exit code is 3".

**Tried on a scratch repository:**
- **E6:** run 116's real plan on run 117 prints `max_tool_calls: plan 25, reached 30, PASSED` and exits 3.
- **E6b:** run 117's own unedited plan given with `--plan` exits 3. It prints the same header and the same two "not measured" lines.
  - The only difference between E6 and E6b is the PASSED limit line.
- **E5:** a `--plan` that does not exist prints the PAIRED header, then "run 117 has no plan file at /tmp/run149/nope.json: its limits were not written before it started", and exits **1**.
  - That sentence is untrue of run 117, which has its own plan in git.
  - The exit contradicts the docstring's "whenever ... 3". This happens because the `plan is None` return (:316-318) comes before the paired return (:321).

**The question asked:**
- The ticket's text says nothing about paired checks.
- The second read put the paired case as "outside the root is allowed only for the paired check", and left open that an edited or uncommitted plan given by `--plan` exits 0. That is now closed: every `--plan` exits 3.
- A paired check in which a limit is PASSED reads differently from one with none only in the limit lines. The exit code is 3 in both.
- Whether a PASSED pair should also differ in its exit code is not written in the ticket or in the second read. It is a decision for the main session or Greg.

### 2. Merge commits and the "tracked" branch
**Code:** :240-246 runs `git log --diff-merges=first-parent --diff-filter=A --name-only` and takes the add with the earliest committer time. When it finds no add row, :244-245 uses `ls-files --error-unmatch` to tell `tracked_no_add` from `not_in_git`, and :331-333 prints the message and sets exit 1.

**Tried with real git:**
- **E1, staged and never committed:** `git add` of the plan with no commit gives "plan in git: tracked, and the commit that added it could not be found", exit 1.
  - So the state the builder said it could not make can be made.
  - The wording names a commit that never existed.
- **E2, shallow clone (`--depth 1`):** the plan was added at 13:08:54 and the boundary commit is at 14:00.
  - `git log --diff-filter=A` in the clone lists only the boundary commit, ef5c742 at 14:00, as the add.
  - The check prints "committed 2026-11-24T14:00:00+00:00 AFTER the run began 2026-11-24T13:10:23.61", exit 1.
  - On the full source repository it prints "before", exit 0.
- **E2c:** `git replace --graft HEAD` on the full repository gives the same "AFTER", exit 1.
  - So a shallow clone and a graft do not reach `tracked_no_add`. They produce a wrong add time.
- **E3, plan added in the second parent** (side branch 13:05, merge `--no-ff` 13:20): `git log --diff-merges=first-parent --diff-filter=A` lists both commits as adds, the merge at 13:20 and the side commit at 13:05.
  - The code takes 13:05, prints "before", and exits 0.
  - With Q4 (`rows[0]`, the newest row) this case would read 13:20, AFTER the run. No check builds this shape: the merge test adds the plan only in the merge, so it has one row.
- **E3b, rebase:** the side commit was re-committed at 13:30 and fast-forwarded. The check prints "AFTER", exit 1. The docstring at :23-25 states that a rebase moves the time.
- **Not retried:** the second read's move-to-`old/` case. The docstring at :25-27 now states that a rename's time is the add time.

### 3. Start time
**Code:** `_start` at :354-369. A non-string value, or one `fromisoformat` cannot read, gives "not measured: ... cannot be read (<v>)". A value with no zone is set to UTC with the note "read as UTC: the line names no zone".

**Tried without a transcript** (plan committed at 13:08:54):

| `started_at` | Printed | Exit |
|---|---|---|
| `1795000000`, `true`, `{"a":1}` | "cannot be read (...)" | 0, no traceback |
| `""` | "holds no start time" | 0 |
| `"2026-11-24 13:10:23"` (space separator) | read as UTC, before | 0 |
| `"2026-11-24T08:10:23-05:00"` | before | 0 |
| `"2026-11-24"` (date only) | read as 00:00 UTC, "committed 13:08:54 AFTER the run began 2026-11-24T00:00:00+00:00" | **1** |

- Every row prints the UTC note where it applies. The date-only value is the one case where a start time that does not name a time of day fails the git order.

### 4. Earlier line
**Code:**
- `_of_run` at :91-93 matches a line by `run` only.
- :308-312 names the newest earlier total when the newest line holds none.
- `_write` (about :126) still refuses on `_num(d.get("corrects")) == a.run`. With the sentence values in the real record this reads as None.

**Measured:**
- Q2 is held by `test_an_earlier_line_with_a_harness_total_is_named`, which reads the record at markets-data 04d8a0f.
- On the record as it stands, run 128's newest line now holds 110617, so the message no longer prints for run 128.
- I did not re-measure the second read's run 131 (three lines).

### 5. `write` outside git
**Code:** :120-121 with `_is_repo` at :222-224.

**Tried:**
- **E8:** a plain folder gives "refused: ... is not a git repository", exit 2, and no file is written.
- **E8b:** a data root that is an untracked subfolder of a git repository is written (exit 0). `_is_repo` asks only "inside a work tree", so a plan there can be committed.

### 6. Docstring
- :19-27 holds the paired rule, the committer time and rebase sentence, and the rename sentence.
- The paired sentence "whenever ... exit code is 3" does not hold for a `--plan` that does not exist (E5).

### 7. Header of the separated section
- Test file :220-227 lists the scratch-owned items: the merge commit, the 999 copy, the deleted `max_tokens_is`, the uncommitted plan, the line copies and the bad start times, the emptied record, the `--plan` copies and the non-git folder.
- Read, not listed:
  - the merge test's `other.txt` and `main.txt` files;
  - the real `run-0128.json` copied into the earlier-line test. The header names only "for run 128 the record as it was at 04d8a0f".

## Real record (read-only)
I ran `check` against `/home/user/markets-data` for four runs.
- **Exit codes:** my first loop printed "exit 0" for every run, but that was `sed`'s exit. Run alone, the exits are 117 → 0, **128 → 1**, 135 → 0, 148 → 0.

**Run 117:** the same output as the builder pasted. Plan added at 13:08:54, before the transcript's first line at 13:10:23.61.

**Run 128:**
- It now reads from the newest of its three lines: model calls 32 of 40, tool calls 29 of 50, tokens 110617 of 350000.
- **`max_wall_clock_s: plan 1800, reached 2314.5, PASSED`**, exit 1. Git order "not measured", and there is no run-0128 transcript in `transcripts/`.
- The builder's pasted output (exit 0, 919.6 s, 13 tool calls) was made before this line existed.
- The line's `tool_calls` is 29. The builder's report says 24, not counting hand-backs. I did not reconcile the 5.

**Run 135:**
- Transcript figures: model calls 15 of 25, tool calls 14 of 18, wall clock 235.6 of 1200.
- Tokens are "cannot be measured": the line's `tokens_reported` is None.
- Plan add fe43fdb at 13:49:49, before the run began at 13:50:17.738. 3 of 8 limits not measured.

**Run 148:**
- The plan is present, with no line and no transcript.
- 7 of 8 limits not measured; graph writes 0 of 0. Plan unchanged; git order not measured. Exit 0.

**Three figures checked by hand:**
1. Run 128 `wall_clock_ms` 2314475 is 2314.5 s, against the plan's 1800.
2. Run 135's line has `tool_calls` 14 and `model_replies` 15, which equal the transcript figures printed.
3. Run 135's plan add is `git log --diff-filter=A` fe43fdb at 2026-11-24T13:49:49+00:00, which equals the printed add time.

Every printed line I checked agrees with the record. The tokens note for run 128 ("at its third hand-back; 52,854 at the first, 81,129 at the second") agrees with the 110617 used.

## Against "Shown done by"
The line reads: "before each run a plan holds the eight limits; a run that reaches one stops and returns what is done, what is open and why".

- **"a plan holds the eight limits":** `write` refuses a missing, negative or below-1 limit and writes all eight. Plans 114 to 149 exist in markets-data.
- **"before each run":** `check` shows a plan in git before the run's first line only where a transcript or `started_at` exists. Runs 128 and 148 have neither, so the order is "not measured".
  - Shallow clones, grafts and rebases move the add time (E2, E2c, E3b).
  - A run started with no plan at all is listed by nothing.
- **"a run that reaches one stops":** code does not stop a run. Run 128 reached and went past its 1800 s wall clock (2314.5 s, over three parts) and was sent back twice. `check` now reports this, exit 1.
- **"returns what is done, what is open and why":** `brief` prints this sentence into the brief. Whether a hand-back does it is read by a person.

## Commands as they stand at 643ca97
`<PAPER>` is `tasks/family-research-20261022/research-union-current/paper-trading-20261123`.

**Write a run's plan before it starts.** `write` does not commit; the commit must land before the run's first line.
```
python3 -m tools.kgraph.run_plan write --data <markets-data checkout> --run <N> --agent <scout|builder|reviewer|frankie-performance-auditor> --model <model id> --task "<task>" [--session <session id>] [--tickets <a,b>] [--note "<note>"] --max-model-calls <n> --max-sub-agents <n> --max-concurrent-workers <n> --max-tool-calls <n> --max-tokens <n> --max-wall-clock-s <n> --max-retries <n> --max-graph-writes <n>
git -C <markets-data checkout> add <PAPER>/run-plans/run-<NNNN>.json && git -C <markets-data checkout> commit -m "<message>" && git -C <markets-data checkout> push
```
- I measured exit 2 when `write` refuses (E8).

**Print the brief's limits paragraph:**
```
python3 -m tools.kgraph.run_plan brief --data <markets-data checkout> --run <N>
```
- I ran it for run 149. It printed my limits exactly as written in run-0149.json, exit 0.

**Check a finished run:**
```
python3 -m tools.kgraph.run_plan check --data <markets-data checkout> --run <N> [--transcript <path>]
```
- Exit 0: no limit passed, and the plan is in git, unchanged and before the run.
- Exit 1: a limit passed, no plan, the plan is not in git, it was edited, or it was committed after the run began.
- Exit 3: any `--plan <file>` that exists, i.e. a paired check, never the run's own check.

## What code cannot hold (as it should be written into the ticket)
- Stopping an agent when it reaches a limit mid-run (run 128 went past 1800 s and finished).
- Requiring a plan before a run started from the chat. Nothing lists a run with no plan, no line and no transcript.
- Concurrent workers and retries: no transcript records them.
- Tokens for a run whose line holds no harness total. Run 135 now, and every run with no line yet such as run 148. I did not re-measure the second read's count of 14 of 30.
- The git order where no transcript is kept and the line holds no `started_at` (runs 128 and 148).
- The git order across a rebase, a shallow clone or a graft: committer time and history are what git holds.
- Whether a hand-back says what is done, what is open and why.

## Speculation (labelled)
- Run 128's 2314.5 s may be the three parts' times added together, not one span. I did not read how `wall_clock_ms` was summed for a run sent back twice.

## Open after this read
**For the builder:**
1. A `--plan` that does not exist exits 1 and prints "its limits were not written before it started" about the named run (:316-318 run before :321). The docstring at :19-21 says every `--plan` exits 3.
2. No check holds the earliest-add choice (:246). The E3 shape (plan added on a side branch at 13:05, merge at 13:20; both are listed as adds) would.
3. No check holds `tracked_no_add` (:245, :331-333). E1 (`git add` with no commit) makes it with real git, and its wording names an add commit that never existed.
4. A shallow clone or a graft gives the boundary commit as the add, "AFTER", exit 1, for a plan committed before the run (E2, E2c). Nothing says the history is shallow.
5. A date-only `started_at` reads as 00:00 UTC and fails the order, exit 1.
6. Minor: the test header (:220-227) does not name `other.txt` and `main.txt` or the real `run-0128.json` copy.

**For the main session:**
1. Whether a paired check with a PASSED limit should differ in exit code from one with none. Today they differ only in the limit lines, and both exit 3.
2. Run 128 PASSED its 1800 s wall-clock plan (2314.5 s, exit 1), and how a run sent back counts against one plan.
3. Run 128's tool calls: 24 by the builder's report, 29 on its line.
4. Whether `write` into an untracked subfolder of a git repository (E8b) is acceptable.
5. The token "14 of 30" count, not re-measured.
6. The ticket's "what code cannot hold" text, as listed above.

**What code cannot hold:** the list in the section above.

## Housekeeping and tool calls
- /tmp/run149 and /tmp/pytest-of-root are deleted.
- `git -C /home/user/markets-data status --short`: empty.
- `git -C /home/user/Markets-r149 status --short`: empty.
- Nothing was written, committed or pushed in either repository.
- **Tool calls: 9 in all** (7 Bash, 1 advisor, plus this hand-back), against a limit of 12. No sub-agents.
- Wall clock was not measured by me. The put-back loop alone ran about 4.5 minutes, so the run is under the 20 minutes by my estimate only.
- Token total: the harness's figure, not known to me.

## Files
- /home/user/Markets-r149/tools/kgraph/run_plan.py
- /home/user/Markets-r149/tests/agent_program/test_run_plan.py
- /home/user/markets-data/tasks/family-research-20261022/research-union-current/paper-trading-20261123/builder-20261124/BUILDER_RUN_128.md
- /home/user/markets-data/tasks/family-research-20261022/research-union-current/paper-trading-20261123/reviews-20261124/REVIEW_RUN_142_TICKET_18_SECOND.md
- /home/user/markets-data/tasks/family-research-20261022/research-union-current/paper-trading-20261123/tickets-44-20261124/18.md
- /home/user/markets-data/tasks/family-research-20261022/research-union-current/paper-trading-20261123/agent-runs.jsonl
- /home/user/markets-data/tasks/family-research-20261022/research-union-current/paper-trading-20261123/run-plans/run-0149.json
