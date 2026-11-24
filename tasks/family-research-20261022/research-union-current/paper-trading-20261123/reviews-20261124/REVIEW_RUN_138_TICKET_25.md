# Reviewer run 138 (Opus): ticket 25, ingest_artifacts

Kept word for word as the agent returned it, 2026-11-24 (twenty-fifth session). Nothing below this line is the main session's.

---

REVIEWER RUN 138: ticket 25, commit b245ee3 (read in /home/user/Markets-r138, detached at b848096)

Nothing was written into the real graph. Every ingest ran on a copy at /tmp/run138/graph. /tmp/run138 and /tmp/pytest-of-root are deleted. `git status --short` prints nothing for /home/user/markets-data or for /home/user/Markets-r138.

## 1. The checks

- **tests/agent_program/test_ingest_artifacts.py, first run after the merge:** 1 failed, 15 passed (98 s).
  - The failure was `test_a_second_ingest_writes_nothing_new_and_the_checks_find_nothing_new`, at the assert on line 166 (`"'new': 0, 'revised': 0" in printed_second`).
  - Running that test again on its own: 1 passed (63 s).
  - On my scratch copy the second ingest wrote `{'new': 0, 'revised': 0, 'unchanged': 401}`, and after the newer runs were loaded, `{'new': 0, 'revised': 0, 'unchanged': 642}`.
  - Speculation, not confirmed: four markets-data commits landed while the first test run was going (bcd4764 at 13:58:42, 02e93c7 and f1e3be4 at 14:00:44, 7fac847 at 14:01:35, all UTC). The fixture ingests twice against the live markets-data checkout. If its head or agent-runs.jsonl moved between the two ingests, `artifact:markets-data:working-branch` gets revised, or a new run's Metrics are written. I did not capture the failing run's printed output.
- **tests/agent_program/test_stage5a_context.py:** 18 passed, 2 xfailed (141 s).
  - `grep -c xfail` gives 2 at 3a98333 and 2 now.
  - The two xfail reasons are budget cuts of the keys claims and the phone-page claims. They existed before this change.

## 2. What the ingest wrote (scratch copy, `--markets /home/user/Markets --platform /home/user/paper-trading-platform`)

- **Artifacts by set:** control files 4, decider programs 5, rule files 32, execution plans 7, run plans 29, plan files 2, plus 4 branch artifacts. That is 83 Artifacts, not the 77 in BUILDER_RUN_130 (the record has grown since, for example the run plans). 0 files skipped.
- **Metrics:**
  - Run before the newer runs were loaded: 203 Metrics. 44 runs were left out as "not an AgentRun node" (run:0088 to run:0139) and listed in the output.
  - After `iar.agent_runs(store)` on the scratch store (`{'new': 88, 'revised': 41, 'unchanged': 174}`): 444 Metrics, 0 runs left out.
  - So the order of the two ingests decides how many Metrics exist.
- **Versions against `git log -1 --format=%H -- <path>`, all equal:**
  - decider_v1.py: 04f4378612
  - paper_platform/rules/CL16.json: 95400eba11
  - run-plans/run-0138.json: 299407f6ee
- **Branch artifacts against `rev-parse`, all equal:**
  - Markets: ccr-659edd86-di9udt, 974e208b49
  - paper-trading-platform: ccr-0ac78691-8zapbb, 28d4dbb080
  - markets-data: ccr-659edd86-di9udt, 7fac847aa7
  - codex-branch: origin/codex/strategy-trades-and-mbo-capture, 47fa1c52f5, the same as `rev-parse` of that ref.
- **Metrics against the run's newest line, all equal:**
  - run:0114 tool_calls = 26 (line 122)
  - run:0130 output_tokens = 29338 (line 146)
  - run:0135 wall_clock_ms = 235635 (line 143)
  - Each is of one run and copied as is. Nothing is summed.
- **First ingest on a fresh copy wrote `{'new': 399, 'revised': 1, 'unchanged': 1}`:**
  - So one Commit node that already existed was revised. `commit:paper-trading-platform:1757145fa7` already had rev 1 (ingest_platform) and rev 2 in the real graph.
  - I did not confirm which node was revised. Earlier revisions stay as lines, so nothing was lost.

## 3. "Every artifact has an authoring run"

- All 83 Artifacts carry "not recorded: no agent run's line names commit <sha7>". That includes the 4 branch artifacts.
- **Newest lines that name a commit in `code_commit` / `data_commits`:**
  - 110: 9ca6a48
  - 114: 68d65a6
  - 119: 11fe552, 9079b22
  - 121: 3a98333
  - 122: dc44b3a
  - 128: 313c7da
  - 129: 1f51fac (a merge, parents 35bad34 and 44b345e)
  - 130: b245ee3
  - 131: 120579e
- **Why nothing matches:**
  - `git show --name-only` of each of these commits touches no file under tools/ratchet/programs, tools/decider/programs, paper_platform/rules or paper_platform/execution_plans. 11fe552 and 9079b22 touch no run-plan and no PLAN_ file.
  - The prefix comparison (ingest_artifacts.py:69) handles short shas: run:0119 and run:0114 resolve in the tests.
  - So the reason is not short shas. The commits the record names are not the commits that last changed the set files.
- **Three by hand, plus five more, searched in agent-runs.jsonl:**
  - 04f4378 (decider_v1.py): named only in run 87's `outcome` text (file line 90).
  - 131a9dc (loop_decider.py, platform_decider.md): named only in run 88's `outcome` (line 98).
  - 47fa1c5 (the Codex head): named only in `task` of runs 79, 82, 86, 101 and 103.
  - 92a0cf4, 1757145, 95400eb, 299407f and 16b14f6: named nowhere in the record.
  - 1757145 is authored by DavisAI1974 (the platform side), not by an agent run of this record.
  - Speculation: the run plans and PLAN files are committed by the main session, which has no run line of its own.
- **What would have to be recorded to meet the rule:**
  - every commit a run makes, listed in a structured field (`code_commit` holds one sha; runs 87 and 88 named theirs only in prose);
  - a run line for the main session's own commits;
  - a line for the platform-side (Codex / Greg) commits.
- **Schema against meaning:**
  - schema.py:23 requires `authoring_run`. The test (test_ingest_artifacts.py:68-69) asserts only that the value is truthy.
  - `check_all` after the ingest raised nothing new (the test's line 168 subset holds on the reruns).
  - So the text "not recorded: ..." fills the required field and passes those checks. It does not meet the write rule "every artifact has an authoring run" (plan lines 95-97): 0 of 83 have one.
  - I did not read store.check_all's code to see whether it checks anything beyond presence.

## 4. The session text (built after the ingest from the scratch graph, with `--markets /home/user/Markets --platform /home/user/paper-trading-platform`)

- **Position and size:**
  - At 6,000 tokens: the block starts at line 7 of 158 (character offset 600), straight after the fixed head. The text is 23,883 characters against 24,000. The block is 1,428 characters against a 10 per cent mark of 2,400.
  - At 2,000 tokens: the text is 7,959 characters against 8,000. The block is 733 characters against 800, and "9 control files and decider programs are not shown for want of budget".
- **The lines as shown:**
  ```
  - Markets: branch ccr-659edd86-di9udt, head 974e208 (2026-11-24), as read at 2026-11-24T14:02:24Z
  - markets-data: branch ccr-659edd86-di9udt, head 7fac847 (2026-11-24), as read at ...
  - paper-trading-platform codex: branch origin/codex/strategy-trades-and-mbo-capture, head 47fa1c5 (2026-11-24), as read at ...
  - paper-trading-platform: branch ccr-0ac78691-8zapbb, head 28d4dbb (2026-11-24), as read at ...
  ```
- With `--markets /home/user/Markets`, the Markets line shows the right branch. Called without it, or from a worktree, it shows whatever that checkout is on. The test fixture itself uses MARKETS = the test file's own tree (test_ingest_artifacts.py:23), so in the test it reads that checkout's branch or "HEAD" when detached.
- **What could still mislead a fresh agent:**
  - (a) The Codex line comes before the platform working-branch line. ingest_artifacts.py:177 sorts by id, and "codex-branch" < "working-branch".
  - (b) Both platform lines carry the same date. Neither says "working branch", and nothing in the block says which kind of work lives in which repository.
  - (c) ingest_artifacts.py:84-89 keeps `as_read_at` from the FIRST read while the state is unchanged. A later re-read that confirms the head still prints the old time.
  - (d) A head is stale on the next push. markets-data took 4 commits in about 3 minutes during this read.
  - (e) "made by run:NNNN" is never shown. Every file line says "authoring run not recorded".
- **The 10 per cent cap:**
  - The loop at ingest_artifacts.py:199 drops only file lines. The four branch lines and the tail are never cut.
  - At budgets of 1,500, 1,000 and 500 tokens the block is 733 characters against 600, 400 and 200.
  - The test at line 199 checks the 10 per cent bound only when file lines are shown, so it does not cover this case.

## 5. One-line mutants, the builder's 16 checks run against each

| Mutant | Failed / passed | Checks that noticed it |
|---|---|---|
| (a) `_meta` line 79: `"--", rel` changed to `"HEAD"` | 4 / 12 | decider_v1 version; authoring_run; PRODUCED link; block held to a tenth |
| (b) line 159: `continue` changed to `v = 0` | 1 / 15 | test_a_null_figure_writes_no_metric |
| (c) line 71: `== 1` changed to `>= 1` | 0 / 16 | none |
| (d) context.py:456: `fixed` computed without the block's lines | 0 / 16 | none |
| (e) line 86: `if old and` changed to `if False and` | 1 / 15 | the second-ingest check |

- For (b), my first attempt edited line 158, changed nothing and passed 16. The figure above is from the corrected edit on line 159.
- (c): no real commit is named by two runs. The test's own comment at lines 112-113 says so.
- (d): test_session_text_is_within_its_budget still passes at 6,000 and 3,000.

## 6. The edge choice

- schema.py:47 reads `"PRODUCED": "src (a run, a commit) made dst"`. A commit is named as a source in the schema's own words.
- schema.py:54 reads `"PINNED_AT": "src is pinned to dst (a trade day, a time, a place on the tape)"`.
- ingest_det.py:213 already writes PRODUCED from a commit node.
- grep of the literal `PRODUCED` in tools/kgraph/*.py finds only `link("PRODUCED", ...)` writers: defend.py:491, 517 and 728; extract.py:323, 428, 469 and 516; grounding.py:379; resolve.py:214 and 258; ingest_det.py:213; ingest_artifacts.py:105 and 108. No line filters edges by the type "PRODUCED" to infer that an agent run made the node. A reader that gets the type from a variable would not show up in this grep.
- When a run is named, ingest_artifacts.py:105 and 108 give an Artifact two PRODUCED in-edges: one from the run and one from the commit.

## 7. Against the ticket's "Shown done by"

- **Observed and met:**
  - Artifact nodes for control files (4), decider programs (5), rule files (32), execution plans (7), run plans (29), plan files (2) and each repository's branch and head, with Codex's branch separate. All have repo, path and version; the versions and heads equal what git gives.
  - Metric nodes, one per figure per run, never summed.
  - The session text shows current versions near the top, within budget at 6,000 and 2,000 tokens.
- **Observed and not met:**
  - "with authoring run": 0 of 83 carry a run. The field holds "not recorded" text (section 3).
  - The block does not say which repository holds the platform work. The Codex line comes before the working line (section 4).
  - The block goes over 10 per cent below about 1,800 tokens.
- **Not checked:**
  - "Plans": SETS (ingest_artifacts.py:41-42) is limited to one folder, tickets-44-20261124. I did not look for PLAN_ files or the zip's plan elsewhere. CLAUDE_ARCH_PLAN_*.md in Markets is not in any set.
  - Whether a fresh agent would actually answer correctly. I only read the text.
- The main session has not run the ingest into the real graph yet. It is to do so after this read.

## Exact counts

- test_ingest_artifacts.py: 1 failed, 15 passed on the first run; the failing test alone: 1 passed on rerun.
- test_stage5a_context.py: 18 passed, 2 xfailed; xfail markers 2 at 3a98333 and 2 now.

## Commit read

b245ee3: tools/kgraph/ingest_artifacts.py (read whole), tests/agent_program/test_ingest_artifacts.py (read whole), and its 4-line diff to tools/kgraph/context.py. I did not open BUILDER_RUN_130.md; the builder's statements were checked against the code and the record instead.

## Open after this read

1. For the builder: the second-ingest check depends on live checkouts that other sessions push to (one fail and one pass seen); make it hold against a moving markets-data head.
2. For the builder: the test checks do not notice mutants (c) and (d).
3. For the builder: the block exceeds 10 per cent below about 1,800 tokens; branch lines and the tail are never cut.
4. For the builder: block order and wording — the Codex line comes first and no line says "working branch" or what each repository holds.
5. For the builder: `as_read_at` shows the first read, not the latest confirmation.
6. Settled by the plans (Greg's call): PRODUCED from a Commit, against the plan's PINNED_AT.
7. Settled by the plans (Greg's call): whether "not recorded" in a required field is acceptable, or whether the record must change.
8. What code cannot hold: true authoring runs for these 79 files. The record names their commits only in prose (runs 87 and 88), in `task` (Codex head), or not at all (rule files by DavisAI1974, main-session run plans and PLANs). Each run line would need to list every commit it made in a structured field, with the main session and the platform side recorded too.
9. What code cannot hold: a head shown in the text is stale on the next push.
10. For the builder: which pre-existing Commit node the first ingest revised was not confirmed.
11. For the builder: the plan-file set covers one folder only.

## Tool calls

11 Bash calls plus this hand-off makes 12 of 20. Wall time was about 18 minutes of 25. No sub-agents, no AWS, nothing written to any repository.
