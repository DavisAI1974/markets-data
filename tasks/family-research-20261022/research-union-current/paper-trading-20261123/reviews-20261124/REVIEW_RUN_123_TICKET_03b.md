# Reviewer run 123 (Opus): ticket 03b (and ticket 12's line), Markets 68d65a6..3a98333

Kept word for word as the agent returned it, 2026-11-24 (twenty-fifth session). Nothing below this line is the main session's.

---

REVIEW, AGENT RUN 123: ticket 03b (and ticket 12's line), Markets 68d65a6..3a98333 on branch ccr-659edd86-di9udt

Commits read: 923a016, 2fc12c7 and 3a98333 in Markets. Head is 3a98333, and `git log -1` confirms it. In markets-data I read the record as it stands (the working tree; the latest commit touching agent-runs.jsonl is 9bfef60), plus the commits 2a2d229, 932f38f, 1f27fc7, 3317d7e, b96fc54, c0d4ff1 and 9cea759.

== 1. The checks ==
`MARKETS_DATA=/home/user/markets-data python3 -m pytest tests/agent_program/test_auditor_called.py -q`: **1 failed, 15 passed in 0.92s.**

The failing check is `test_ticket_03b_and_02_follow_the_record_and_01_fails_on_its_unaudited_run`, at tests/agent_program/test_auditor_called.py:186:
`assert not (unaudited & set(tix["03b"])) and not (unaudited & set(tix["02"]))`
It fails with `{118, 119, 121} & {111, 116, 120, 121}`.

Root cause: the check's expectation is tied to the record at one moment, and the record has since moved. TICKET_RUNS.json at c0d4ff1 had 03b = [111,116,120] and 02 = [104,105,107,110,114]. At 9cea759 it has 03b = [111,116,120,121] and 02 = [...,118]. Run 121's line was added at 9bfef60. Runs 118 and 121 have no auditor row yet, so both tickets now hold an unaudited run. The code reports this correctly; the check asserts it should not be so. BUILDER_RUN_121.md:26 records "13 passed" from before those commits.

== 2. The command on the real record ==
Plain command: exit 1, 148 lines. I cut the 106 rows of list (2) down to their first 60 characters and read the run numbers.

- (1) NOT AUDITED: runs 118 (reviewer), 119 (builder) and 121 (builder). Each row gives the eight plan limits from run-plans/run-01NN.json and the tokens_reported / tool_calls / wall_clock_ms of its newest line.
- (2) record-only: runs 1 to 106, 106 runs. The header says "only an auditor's record_only list names the run". No row names run 111 as the auditor whose report covers them.
- (3) outside the roster: 26 runs. Among them are 107 and 108, whose agent_type is "general-purpose, handed .claude/agents/reviewer.md ..." (and the same for scout.md). All 26 print "audited: yes".
- (4) the auditor's own runs: 111, 116 and 120, each with its report@commit.
- (5) a plan file and no line: runs 122, 123, 124 and 125.
- Counts line: `COUNTS runs=121 not_audited=3 record_only=106 with_own_row=9 outside_roster=26 auditor_runs=3 plan_no_line=4`.

Ticket checks. In my third Bash call I read exit codes through a `sed` pipe, so the "exit 0" values there are sed's and are void. The true codes, from a run without the pipe:
- `--ticket 01`: exit 1. 105 record-only, 108 own row, 119 NOT AUDITED.
- `--ticket 02`: exit 1. 104 and 105 record-only; 107, 110 and 114 own row; 118 NOT AUDITED.
- `--ticket 03b`: exit 1. 111, 116 and 120 "an auditor's own run"; 121 NOT AUDITED.
- `--ticket 99`: exit 1, "no entry".

`--at 2a2d229`: exit 1. COUNTS runs=115, not_audited=113, record_only=0, with_own_row=0, auditor_runs=2 (111 and 116), plan_no_line=2 (114 and 115). Every run 1 to 113 except the two auditors is in list (1), with the note "auditor run 111 (or 116): no line has an audit_report". Run 117 is there with no note. This is true of that commit: neither auditor line there carries an audit_report.

Checked by hand:
- Run 111: the newest line has audits 1..109, record_only of 106 entries (including 50 and 105), and audit_report AUDIT_RUN_111.md@1f27fc7. That report has `L53 r50 ...` (line 71), `L109 r105` (line 127), `L113 r107` (131), `L114 r108` (132), `L115 r109` (133), and `Run 107 (reviewer...)` at line 227. This agrees with 50 and 105 being record-only and 107 to 109 having their own row.
- AUDIT_RUN_116.md@932f38f has headings `## Run 110`, `## Run 112` and `## Run 113` (lines 21, 63, 102). AUDIT_RUN_120.md@3317d7e has `## Run 114`, `## Run 115` and `## Run 117` (lines 23, 78, 127).

== 3. Trying to get a run past it ==
All cases ran on a `git clone --shared --no-checkout` under /tmp/run123, with the record copied and lines appended.

First attempt void: the scratch folder had no MANIFEST.json, so `--data` silently fell through to the real checkout. That read was read-only, and its results are discarded.

Finding (pre-existing code, reached from the new command): tools/kgraph/store.py:33-37 `markets_data_root` takes the first candidate that has MANIFEST.json. tools/kgraph/auditor_called.py:199 calls it. If `--data <folder>` has no MANIFEST.json, the command reports on MARKETS_DATA or the checkout beside Markets, and nothing it prints names the root it read.

Second attempt, with MANIFEST.json copied:
- (a) I added auditor run 900 with audits [119] and AUDIT_RUN_120.md@3317d7e. 119 stays in (1) with the note "auditor run 900: its report has no row for run 119". Exit 1.
- (b) I added a correcting line of run 120 with audits [114] only. Counts did not change, and 115 and 117 stay cleared. The union over lines (auditor_called.py:96) means a later line cannot withdraw a name. This is the plan's rule 2 as written.
- (c) role "the reviewer" with no agent_type: the agent is "the", so the run is in (3) with "audited: no" and also in (1). Exit 1. Role "Reviewer, acting as scout" gives agent "reviewer" (first word, punctuation stripped), in (1). Exit 1.
- (d) plan run-0999.json with no line: listed in (5) as `run 999 | builder | x | max_tool_calls=5`. The exit stays 1 only because 118, 119 and 121 are unaudited. From auditor_called.py:203, a run with a plan, no line and no TICKET_RUNS entry never fails the plain command; only `--ticket` fails it (line 215-217). This is the plan's rule 3 as written.
- (e) A number at the start of a line inside another run's block. A real case exists. I ran `has_row` on AUDIT_RUN_120.md@3317d7e and got `{107: True, 109: False, 110: True, 112: False, 113: False, 114: True, 115: True, 117: True}`. The True for 110 and 107 comes from two indented prose lines inside other runs' blocks: line 71 `   Run 110 has no harness total on its line.` (in ## Run 114) and line 120 `   Run 107 was a re-read of code, not a plan read.` (in ## Run 115). auditor_called.py:37 allows `[#\s]*` before the name, so leading spaces pass. BUILDER_RUN_121.md:102 calls these "an own line for each of them". Today no auditor line names 107 or 110 against report 120, so nothing is cleared wrongly by it now. A string check gave the same result: "## Run 114\nr119 was read beside it" counts as a row for 119.
  Other formats: `| Run 119 | builder |`, `- Run 119: x` and `**Run 119**` are not rows (fail closed). `run 119.5` and `Run  119` are rows.
- (f) audit_report at 2a2d229, where AUDIT_RUN_120.md does not exist: 119 stays in (1), "report not readable at 2a2d229". Exit 1. Code note: `why` at auditor_called.py:100-107 is one variable per auditor run. If one of several reports is unreadable and another is readable but lacks the row, the note names the unreadable one. That is message text only.
- (g1) Builder run 119's newest line carries audits [118] and report 120: ignored, and 118 and 119 both stay in (1).
- (g2) Run 119 appends one line with agent_type "frankie-performance-auditor" and audits []: 119 moved from (1) to (4) with "report: none named", not_audited went 3 to 2, and nothing else was needed. Code: auditor_called.py:92 counts a run as an auditor if ANY of its lines says so, and :117 exempts it before any audit check. The plan says the auditor's own runs form list (4); it does not say a run becomes one by a single line with no report.
- (g3) Not built: I appended a builder line on top of 121, and no older auditor line existed. From the code (line 92, `any`), a run with one older auditor line and a newer builder line would sit in (4), not (1), while line 116 takes its displayed agent from the newest line.

== 4. The checks themselves ==
Every check reads the real record or real commits. Some strings are made up: lines 94-95 and 230-232 test has_row on literal strings ("see r110 and run 110", "L113 r107 reviewer | x", "compared against run 110 here", "## Run 110 (builder, x)"), while the file header (lines 3-4) says "No made-up run line". `_git_show` (line 24-28) skips, and does not fail, when a commit is missing.

Checks pinned to today's record. Each goes red when the record reaches the state "Shown done by" asks for:
- line 65: `== {111, 116, 120}` goes red when run 124's line lands.
- lines 69, 162 and 187 require 119 to be unaudited.
- line 156 requires exit 1 (`== 1`).
- line 164: `re.search(...).group(0)` raises on None once 119 leaves list (1).
- line 186: red now (see section 1).
- line 224 and line 240 require, respectively, a mention without a block in report 120 and a plan with no line.

Consequence: the command exiting 0 and this file passing cannot both happen as the file is written.

Checks that restate the code:
- `_starts_with_run` (test lines 213-215) is the same prefix regex as has_row (`^[#\s]*(L\d+\s+)?`). So test_a_mention_inside_another_runs_block (218-232) cannot disagree with the code on the indented-line case in section 3 (e).
- `_tokens_have_row` (49-55) is looser than has_row: any token anywhere in a line. So test 72-80 checks that a name occurs, not that the run has its own row. Its `notes == {}` part does rest on the code.

Checks with independent expectations: `_expected` (36-46: auditors = lines with an `audits` key, cleared = union of audits on lines with a commit) does not call the code. Tests 106-137 (the at-commit cases) state their facts from the lines at those commits.

== 5. The four text changes (git diff 68d65a6 3a98333; additions only, nothing removed) ==
- CLAUDE.md, at line 19 (+5): "Every run of the scout, the builder and the reviewer is audited by the performance auditor, each run its own row, against the limits written for it before it started. `python3 -m tools.kgraph.auditor_called` lists the runs no auditor's report has a row for and fails while any is listed; it is run before a ticket's box is marked and at the close of every session (Greg, 2026-11-24, ticket 03b)."
- frankie-performance-auditor.md (+18): a new section "## Every run of the other three agents (Greg, 2026-11-24)". It says the auditor is called for scout, builder and reviewer runs; one heading `## Run NNN` per run; the eight plan limits against the figure reached; the line against the transcript; where the spend went; nothing averaged; "from the record alone" when there is no transcript; read-only; its own runs are not audited by anyone else; and its report names the runs it audited.
- builder.md (+1, item 4) and reviewer.md (+1): "You do not search or read whole files to find things; the main session hands you the line ranges the scout located, and if something you need is not located, stop and say what (Greg, 2026-11-24)." This is ticket 12's line; I did not have ticket 12's text to compare against.
- Against Greg's words and the ticket:
  - None of the three places says "a box is not marked while a run that worked on that ticket is unaudited". CLAUDE.md says the command "is run before a ticket's box is marked".
  - None says "the auditor's report for each of its runs kept in git word for word".
  - Wording differs: CLAUDE.md says "limits written for it before it started"; READ_FIRST line 47 says "limits told to Greg before it started".
- READ_FIRST_UNTIL_THE_AGENTS_PART_IS_DONE.md (not in this diff):
  - Lines 45-49 still read "until it is built, the main session calls the auditor..." and do not name the command.
  - Its table (lines 21-26) says builder.md and frankie-performance-auditor.md in Markets are "the same bytes" as the zip's, and reviewer.md is "the zip's text plus 5 lines". After this diff they are +1, +18 and +6. I could not compare against the zip: its location was not given.

== 6. "Shown done by", part by part ==
- "the rule in the three places named": CLAUDE.md and the auditor's file carry it (section 5). The READ_FIRST page carries Greg's quote and the rule, but still in its "until it is built" form, and the two clauses above are missing from all three.
- "the check command run on the real agent-runs.jsonl, printing no unaudited run of the scout, the builder or the reviewer from run 107 on": today it prints 118, 119 and 121. For this part to be met, each of 118, 119 and 121 (and then 122, 123 and 125 once their lines land) needs an auditor line whose `audits` names it, with an `audit_report` carrying a commit, and the report at that commit needs a line starting with the run's name. The command would then exit 0 and list (1) would be empty. The test file would at the same time go red at lines 65, 69, 156, 162, 164 and 187 (section 4).
- "naming truthfully the runs before 107 that only run 111's audit of the whole record covers": list (2) names exactly runs 1 to 106. This matches run 111's record_only list of 106 entries and the `L<line> rN` rows in AUDIT_RUN_111.md@1f27fc7 that I sampled. The rows do not say "run 111"; only list (4) shows 111's report.
- "a check on the real record that a run line added with no auditor run naming it is listed and fails the command": test 98-103 (`--at 2a2d229`, run 117 in (1), main == 1) does this on a real commit. On the record as it stands, 118, 119 and 121 show it as well.
- "the auditor's reports in git": AUDIT_RUN_111.md, AUDIT_RUN_116.md and AUDIT_RUN_120.md are in markets-data (the latest commit on that folder is 3317d7e). Whether they are word for word I could not check: that needs the transcripts.
- "checks before any box is marked and at the close of every session": these exist as words in CLAUDE.md only. No code or hook runs the command.

Speculation (labelled): the g2 way through (a single line declaring the auditor type) seems the most likely real-world slip, for example a mis-typed agent_type on a correcting line.

== Open after this read ==
1. Builder: test file line 186 fails now, and lines 65, 69, 156, 162, 164, 187, 224 and 240 are tied to today's record; they need expectations that follow the record.
2. Builder: auditor_called.py:92/117. One line with the auditor agent_type exempts a run, with no report needed (case g2); an older auditor line also exempts a run whose newest line is another agent (g3, read from code).
3. Builder: auditor_called.py:37. The `\s` before the name lets indented lines inside another run's block count as rows (real case: AUDIT_RUN_120.md lines 71 and 120 count for 110 and 107). Test 213-215 restates the regex, so it cannot see this.
4. Builder: tools/kgraph/store.py:33-37 via auditor_called.py:199. `--data` without MANIFEST.json silently reads another checkout, and the output does not name the root.
5. Builder: test lines 94-95 and 230-232 use made-up strings, against the file's own header.
6. Builder (text): the "box not marked while unaudited" and "reports kept in git word for word" clauses are absent from the three places; READ_FIRST lines 45-49 and the table rows at 24-26 are behind the diff.
7. Settled by the plans: (b), a correction cannot withdraw a name (union, rule 2); (d), a plan with no line does not fail the plain command (rule 3).
8. What code cannot hold: running the command before a box is marked and at session close (words only); whether the auditor's reports are word for word (needs the transcripts); the zip comparison for READ_FIRST's table (location not given).
9. Settles by the record moving: runs 118, 119, 121 (then 122, 123, 125) need the auditor's own rows before "printing no unaudited run from run 107 on" can show.

Exact test counts: 1 failed, 15 passed (16 collected), 0.92s.
Cleanup: /tmp/run123 and /tmp/pytest-of-root are deleted, and the scratchpad script is removed. `git -C /home/user/markets-data status --short` is empty, and so is `git -C /home/user/Markets status --short`.
True tool count: 14 Bash calls (one ended with an error exit; one bypass run is void, as above), 1 advisor call, and this handback: 16 in all. Wall clock was not measured. I wrote nothing into either repository.
