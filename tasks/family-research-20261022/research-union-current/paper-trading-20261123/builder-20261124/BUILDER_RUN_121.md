# Builder run 121 (Sonnet): ticket 03b, the check that every run has an auditor's row, and ticket 12's line

Kept word for word as the builder returned it, 2026-11-24 (twenty-fifth session), its first hand-back and then its second (the main session sent it back for a plan with no line, and for a row being a line that starts with the run). Nothing below this line is the main session's.

---

Ticket 03b and the ticket 12 piece are built, committed and pushed (`wt-b456` to `ccr-659edd86-di9udt`, no force). The real record does not match the plan on two points: runs 118 and 121 have no line in it, and the plan's expectation for `--at 2a2d229` contradicts its own rule 2. I followed rule 2. Nothing else was loosened.

**Commits**
- 923a016: PROPOSED ... auditor_called ... (ticket 03b) [skip ci]. This holds A, B and C.
- 2fc12c7: PROPOSED ... the builder and the reviewer do not search (ticket 12) [skip ci]. This holds D.
- Both end with the Co-Authored-By and Claude-Session lines. The push range was 68d65a6..2fc12c7.

**`git diff --stat 68d65a6 HEAD`**
```
.claude/agents/builder.md                     |   1 +
.claude/agents/frankie-performance-auditor.md |  18 +++
.claude/agents/reviewer.md                    |   1 +
CLAUDE.md                                     |   5 +
tests/agent_program/test_auditor_called.py    | 208 +++
tools/kgraph/auditor_called.py                | 201 +++
6 files changed, 434 insertions(+)
```
`tools/kgraph/schema.py` is untouched. The CLAUDE.md paragraph sits in "Agent roles" before the "main session does not grep" paragraph, and nothing existing was removed.

**Last pytest run:** `13 passed in 0.84s`. One earlier run skipped a check because `TICKET_RUNS.json` does not exist at 2a2d229. I changed that check to `--at b96fc54`, the first commit that holds the file.

**Command output on the real record, exit code 1**
- The full output is 141 lines, not short. List (2) alone is 106 lines, one per run named only in 111's `record_only`.
- List (1) holds one run: `run 119 | builder | claude-sonnet-5-5 | limit told: plan run-plans/run-0119.json: max_model_calls=40 max_sub_agents=0 max_concurrent_workers=1 max_tool_calls=60 max_tokens=400000 max_wall_clock_s=1800 max_retries=1 max_graph_writes=0 | reached: tokens_reported=87372 tool_calls=12 wall_clock_ms=359458`
- Counts line: `COUNTS runs=119 not_audited=1 record_only=106 with_own_row=9 outside_roster=26 auditor_runs=3`
- `--ticket 03b` exits 0 (runs 111, 116, 120). `--ticket 02` exits 0. `--ticket 01` exits 1 because of run 119. A ticket with no entry exits 1 and says "no entry".

**Each check and the real record it rests on**
1. `test_real_record_as_it_stands_each_run_in_exactly_one_place` uses `agent-runs.jsonl` at HEAD 9e145fc. The expectation comes from the auditor lines in four independent lines in the test. The sets must cover all 119 runs without overlap, the auditors are {111, 116, 120}, and 119 is in list (1).
2. `..._names_no_run_whose_row_is_missing` uses the reports named by the lines of 111, 116 and 120. A separate tokeniser in the test finds a row for every named run, and the command's `notes` come out empty.
3. `test_run_107_...run_50...` uses the 111 lines and AUDIT_RUN_111. Run 107 has its own row and is not in (2). Run 50 is in (2).
4. `test_whole_token_run_11_is_not_run_110` uses AUDIT_RUN_116.md at 932f38f. It has `## Run 110` and no block for 11, so `has_row(110)` is true and `has_row(11)` is false. It also checks `r110` against 11 and `r107` against 10.
5. `test_at_2a2d229_run_117_is_not_audited`: 117 is in (1) and the exit code is 1.
6. `test_at_2a2d229_an_auditor_line_with_no_audit_report_clears_nothing`: at 2a2d229 the lines of 111 and 116 have no `audit_report`. Runs 110, 112 and 113 are in (1), each with a note naming `audit_report`.
7. `test_at_932f38f_...`: the report file exists there, but 116's line does not name it yet. 110, 112 and 113 are in (1).
8. `test_at_1f27fc7_...`: 111's line names 1 to 109 with no report. All of them are in (1), and (2) and the own-row list are empty.
9. `test_at_3317d7e_report_named_without_a_commit...`: 120's line names a path with no commit. 114, 115 and 117 are in (1), each with a note naming `commit`.
10. `test_command_on_the_real_record_prints_the_four_lists...` covers the four headings, the exit code, the limit told (read from `run-plans/run-0119.json`) and the figure reached for run 119. It also checks that 111 is not in (1) and that "main session" appears in (3).
11. `test_ticket_03b_and_02_follow_the_record_and_01_fails...` uses `TICKET_RUNS.json` as it stands.
12. `test_ticket_with_no_entry_exits_1_and_says_why` uses ticket id 99.
13. `test_ticket_at_a_commit_reads_the_file_and_the_record_as_they_were` uses `--at b96fc54`, with every ticket's expectation derived independently.

**Ambiguities and things the plan did not match**
1. **Contradiction at 2a2d229.** The plan says runs 110, 112 and 113 are not in (1) at 2a2d229. At that commit 116's line has no `audit_report` (it was added at 932f38f), so rule 2 does not clear them. I followed rule 2 and tested what the record shows: they are in (1) there. They are cleared only in the record as it stands.
2. **Runs 118 and 121 have no line in `agent-runs.jsonl`.** Only run plans exist for them. The command works from the record, so only 119 shows now. I did not add a "plan but no line" list, which would widen the plan. Say if you want it, since otherwise an unrecorded run can escape.
3. **No real case of a report lacking a row.** Every number named by the lines of 111, 116 and 120 has a row in its report, so I invented none. The real not-cleared cases are the two above: a line with no report (items 6 to 8) and a report named without a commit (item 9). Run 120's first line names a report without a commit, and the later line names it at 3317d7e. That is why the output shows `AUDIT_RUN_120.md@None, ...@3317d7e`.
4. **Row matching is loose, as the plan words it.** A run counts as having a row if any line of the report names it as a whole token. So a cross-mention inside another run's block counts, and 111's report may clear some runs that way. Say if you want only the heading or row start to count.
5. **Role parsing keeps the hyphen** when stripping punctuation. Otherwise `frankie-performance-auditor` would never match the roster.
6. **Ticket mode** prints only the ticket's runs and exits 1 for a run with no line in the record. That last rule is my addition.
7. **Red before green was done in two slices.** Slice A was the classification checks, and slice B was the command and ticket checks. Slice A's later checks (whole-token, no-report) went green at once on the same code. Nothing needed a second fix attempt.

**Cleanup and count:** /tmp/run121 and /tmp/pytest-of-root are deleted. `git -C /home/user/markets-data status --short` is empty, and so is the Markets worktree. I made 11 tool calls before this hand-back, against the limit of 50. I did not search, and I made no sub-agent, AWS or engine calls.

---

## The second hand-back

Both changes are built, committed and pushed as commit **3a98333** (`wt-b456` to `ccr-659edd86-di9udt`, 2fc12c7..3a98333, no force). I wrote the tests first, and all three new ones failed before the code. The last pytest run on `tests/agent_program/test_auditor_called.py` gave `16 passed in 0.89s`.

**1. List (5), a plan file and no line in the record**
- On the real record the command still exits 1, because of run 119 in list (1).
- Its heading says in one sentence that this list alone does not fail, since a run still in flight has no line yet. `--ticket NN` is unchanged and still fails for a listed run with no line.
- Each line shows the run, the agent, the first 12 words of the task and the eight limits.
- At `--at` it reads the `run-plans` folder as it was with `git ls-tree`. If the folder is not there, the list is empty.

Output on the real record as it stands:

List (1):
```
run 119 | builder | claude-sonnet-5-5 | limit told: plan run-plans/run-0119.json: max_model_calls=40 max_sub_agents=0 max_concurrent_workers=1 max_tool_calls=60 max_tokens=400000 max_wall_clock_s=1800 max_retries=1 max_graph_writes=0 | reached: tokens_reported=87372 tool_calls=12 wall_clock_ms=359458
```

List (5):
```
run 118 | reviewer | tickets 02 and 03: the third read, Markets 68d65a6 against the 15 | max_model_calls=30 max_sub_agents=0 max_concurrent_workers=1 max_tool_calls=30 max_tokens=300000 max_wall_clock_s=1500 max_retries=1 max_graph_writes=0
run 121 | builder | ticket 03b: the command that lists every run no auditor's report has | max_model_calls=40 max_sub_agents=0 max_concurrent_workers=1 max_tool_calls=50 max_tokens=350000 max_wall_clock_s=1800 max_retries=1 max_graph_writes=0
```

COUNTS line:
```
COUNTS runs=119 not_audited=1 record_only=106 with_own_row=9 outside_roster=26 auditor_runs=3 plan_no_line=2
```

I added `plan_no_line=` to the COUNTS line.

The checks:
- **`test_plans_with_no_line_in_the_record_are_listed_exactly`**
  - The test works out which plans have no line from the `run-plans` folder and the record, independently, and asserts the command lists exactly those.
  - It also checks the one-sentence note and that a plan's agent, task and limits appear.
- **`test_plans_with_no_line_at_b96fc54_read_the_folder_as_it_was`**
  - It does the same at b96fc54.

**2. A row is the run's own row.** A report line must start with the run's name, after any `#` marks and spaces or an `L<digits> ` prefix. `has_row` now anchors to the start of the line.
- **`test_a_mention_inside_another_runs_block_is_not_a_row_in_audit_run_120`**
  - AUDIT_RUN_120.md at 3317d7e mentions runs 109, 112, 113 and 120 with no block of their own. All four have no row, and 114, 115 and 117 do.
  - Runs 107 and 110 are mentioned there too. The report has an own line for each of them, so they are not in that no-block set.
  - The test also covers the middle-of-line mention and the `## Run 110`, `run 110:`, `r110` and `L113 r107` forms.

**Nothing was un-cleared by point 2.** Before I changed the rule, I ran the start-of-line rule alone on the three reports. Every run still has its own row: all of 1 to 109 in AUDIT_RUN_111.md at 1f27fc7, runs 110, 112 and 113 in AUDIT_RUN_116.md at 932f38f, and runs 114, 115 and 117 in AUDIT_RUN_120.md at 3317d7e. After the change all 16 checks pass, and the earlier ones, including the exact-placement check, did not need touching. I loosened no check.

**Cleanup:** /tmp/run121 and /tmp/pytest-of-root are deleted. `git -C /home/user/markets-data status --short` is empty.

**Tool calls:** the first part of the run used 11 and this follow-up used 4, so 15 of 50 in all.
