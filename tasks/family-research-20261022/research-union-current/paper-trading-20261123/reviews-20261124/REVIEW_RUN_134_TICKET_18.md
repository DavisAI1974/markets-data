# Reviewer run 134 (Opus): ticket 18, run_plan

Kept word for word as the agent returned it, 2026-11-24 (twenty-fifth session). Nothing below this line is the main session's.

---

Reviewer run 134: ticket 18 (`tools/kgraph/run_plan.py`, `tests/agent_program/test_run_plan.py`)

Commit read: /home/user/Markets at head 88ffa58 (the merge); ticket 18's own commit is dfb5879. No existing file changed (2 files, 431 lines added). I also read /home/user/markets-data/tasks/family-research-20261022/research-union-current/paper-trading-20261123/builder-20261124/BUILDER_RUN_128.md.

I did not read AGENTS.md and did not run the grounding command. All scratch work was under /tmp/run134, now deleted. The record changed while I was reading: runs 122 and 133 had no line at my first `check` and had one by my last loop.

## 1. Tests
`pytest tests/agent_program/test_run_plan.py -q --basetemp=/tmp/run134/bt`: 7 passed in 2.14s.

## 2. Where each test's expectation comes from, and the scratch mutants

Where each test's expectation comes from:
- **test_check_117_kept_at_the_limit**: 30/30 tool calls, 10/20 replies and "before the run began" are the stated facts. I confirmed them with jq: 30 tool_use not counting the hand-back (Glob 5, Grep 14, Read 11, SubagentHandback 1), 10 unique reply ids, first line 13:10:23.610Z, last 13:11:44.371Z (80.761 s), plan added at 16b14f6 13:08:54. The test does not assert wall clock or max_tokens. Sub-agents 0 and graph writes 0 are not among the stated facts.
- **test_check_116_four_of_25**: 4 of 25 is a stated fact.
- **test_check_109_has_no_plan**: from the record (run 109 has a line and no plan).
- **test_check_passed_branch_paired_plan**: run 117's transcript against run 116's plan. "30 > 25" follows from facts, not from a run going over its own limit.
- **test_write_refusals_and_a_new_plan**: the run number is computed from the scratch record and file names, separately from the module. The refusals come from the record (114 exists, 109 has a line).
- **test_brief_122**: the eight literals match plan 122. The `on_reaching_a_limit` check reads the plan file back through the same field the code prints.
- **test_data_without_run_plans_is_refused**: a constructed empty folder. It covers `check` and `brief` only, not `write`. I tried `write` by hand and it was refused with rc 2.

Mutants, each one change in a scratch copy:
- **M1, `>` changed to `>=` at :237:** test_check_117 and test_check_116 did not run clean (2 failed, 5 passed).
- **M2, hand-back counted at :162:** test_check_117, test_check_116 and test_check_passed_branch did not run clean (3 failed).
- **M3, "already has a line" refusal dropped at :90:** test_write_refusals did not run clean (1 failed).
- **M4, no-plan exit changed to 0 at :198:** test_check_109 did not run clean (1 failed).
- **M5, max_tokens taken from the transcript's four-figure sum (extra):** only test_check_117 did not run clean, and only through its general `"PASSED" not in out` assertion (run 117 then prints `max_tokens: plan 150000, reached 604852, PASSED`). No test asserts the max_tokens line.
- **M6, `bad = True` dropped for a late plan at :252 (extra):** 7 passed. No test covers a plan committed after the run began.

## 3. `check` on real runs

**Run 117:** matches the jq and git figures above. Exit 0. Tokens: harness total 91,604 against the transcript's four figures (20 + 85,089 + 501,509 + 18,234 = 604,852), plan 150,000.

**Run 114, figures from the line:**
- tool calls 26, tokens 119,607, wall clock 499.7 s.
- model calls and sub-agents "cannot be measured".
- plan in git "not measured (no transcript)".

**Run 114 with `--transcript` pointed at agent-a7b300c42b5b933f8.jsonl:**
- tool calls 26 and wall clock 499.7 s agree with the line.
- It adds model calls 22 and sub-agents 0.
- Tokens still come from the line (119,607); the transcript sum is 46 + 110,043 + 1,962,598 + 20,871.
- Plan in git: committed 13:08:54, before the first line at 13:10:23.559Z.

**Run 121:** tool calls 14, tokens 75,440, wall clock 242.4 s, plan in git "not measured". Exit 0.

**Run 109:** "no plan file ... its limits were not written before it started", exit 1. The auditor found it 1 over its told tool calls (41). `check` cannot show that, since no plan exists.

**Run 128 (the builder's own run):**
- It printed tool calls 6, model calls 7, tokens 52,854, wall clock 116.5 s, plan in git "not measured (no transcript)".
- The builder's own report says "I made 11 tool calls". The line says 6. Neither is over 50. Run 128's live transcript id was not given to me, so I did not locate it. Run 129's line also carries 6 and 7.
- By hand, derived and not measured: plan added at b51ed27, 13:42:20. dfb5879 is 13:47:19 and the merge 88ffa58 is 13:47:23, both made inside the run. With 116.5 s of wall clock the run began no earlier than about 13:45:26, so after the plan was committed.
- The builder's note expected "not measured" because the plan was never committed. Git shows it was committed; the printed reason is the missing transcript.
- Run 128's line was added in 76723de (13:48:12), the same commit that added run 134's plan.

**In flight (130, 132, 134, 135 at the last loop; 122 and 133 at first):**
- Exit 0, with up to seven of eight limits "cannot be measured".
- `max_graph_writes: plan 0, reached 0, kept (at the limit, not passed)` is printed for a run that is still going.

**Loop over runs 114 to 135:**
- No PASSED line, and every exit code was 0.
- Runs 117, 126 and 127 are at their tool-call limit and print "(at the limit, not passed)".
- Runs with no harness token total on their line: 116, 118, 120, 126, 129, plus 122 at the time of reading.

## 4. Breaking it (scratch `--data` under /tmp/run134)

**`write` limits:**
- **Every limit 0:** written, exit 0. `brief` then prints "0 model calls ... 0 tool calls, 0 tokens". `run_plan.py:82-84` refuses only negatives.
- **Run 0 and run -5:** both written. Run -5 wrote `run--005.json`. `run_plan.py:265` takes any int.

**Plan files and git:**
- **A run lower than runs with lines but with no line itself:** none exists among 1 to 130 that also has no plan. With plan 130 removed from the scratch copy, `write --run 130` wrote it again, exit 0. "Never written twice" is held only by the file existing (`:88`, plus `open(path, "x")` at `:106`), not by git history.
- **`write` twice:** the second was refused ("a plan file already exists", exit 2).
- **Plan edited after commit:**
  - In the real repo, each plan 0114 to 0135 has exactly 1 commit.
  - In a scratch git, I committed plan 117 at 13:08:54, changed max_tool_calls to 999 and committed again at 13:20. `check` printed `plan 999, reached 30, kept` and "committed 13:08:54 before the run began", exit 0.
  - `run_plan.py:117` reads the working file. `:186` takes the time the file was first added (`--diff-filter=A`) and never compares the content at that commit.
- **Plan committed in the same commit as the line, at 13:12:**
  - Run 117 (has a transcript) printed "AFTER the run began", exit 1. That came from the commit time, not from seeing a shared commit.
  - Run 121 (no transcript) printed "not measured", exit 0.
  - Git order is measured only with a transcript (`:245-255`). Only 2 of 22 real plans have a kept transcript.
- **Plan never committed (run 143) with run 117's transcript:** "not measured (plan file not in this checkout's git history)", exit 0. The plan given to the builder lists "committed after the run began" as exit 1; a plan never committed is not counted either way.
- **`--plan` outside the data root:** "not measured", and not counted (`:183-185`).

**`check` on the token and graph-write limits:**
- **tokens_reported null (116, 118, 120, 126, 129):**
  - Each prints `max_tokens ... cannot be measured here`, exit 0 (`:218-221`).
  - For 116 the transcript sum is 147,325 against a plan of 150,000, and no harness total exists.
  - `_check` never reads the plan's `max_tokens_is`. The rule that tokens go by the harness total is hard-coded at `:218`.
- **Run 96:**
  - `check --run 96` stops at `:196-198` ("no plan file", exit 1) before graph writes are counted.
  - With `--plan run-0116.json` it printed `max_graph_writes: plan 0, reached 32, PASSED`. That is 32 lines with `written_by: run:0096`, which matches grep.
  - Runs 25 and 36 have 11 and 123 graph lines with `attrs.made_by: run:00NN` and `written_by: code:...`. `:176` counts these as 0.
  - `graph/reads`, `graph/merges` and `graph/evaluations` hold `run-00NN` files that the glob at `:170` never reads.
- **`--data` on a folder with no run-plans:** `write` and `check` were both refused with exit 2, naming the folder.

**Other observations:**
- `max_concurrent_workers` and `max_retries` are "cannot be measured" for every run (`:222-223`).
- `:68` and `:90` match on `corrects`. In the real record `corrects` holds a sentence, so `_num` returns None and that branch never matches.
- Real plan 0114 has no `max_graph_writes_is` key. `brief` falls back to its default text.

## 5. The ticket's "Shown done by"

**"Before each run a plan holds the eight limits":**
- Nothing in this change keeps a run from starting without a plan. `write` and `brief` print and write only. `check --run 109` reports the missing plan after the run.
- Plans 114 to 131 were committed before dfb5879 (13:47:19) existed, so `write` did not make them.
- Run 114's keys differ from `write`'s (no `max_graph_writes_is`). Plans 132 to 135 carry `write`'s keys plus note and tickets; whether `write` made them I cannot tell from the files.
- `brief --run 134` gives 25 model calls, 0 sub-agents, 1 worker, 20 tool calls, 200,000 tokens and 1200 s. The paragraph I was briefed with states five figures in other words (for example "20 minutes") and leaves out model calls, workers and retries. My brief was not the verb's output.

**"A run that reaches one stops and returns what is done, what is open and why":**
- The docstring (`:10-13`) says code cannot stop an agent started from a chat. The agent is told, counts and stops, and `check` shows afterwards.
- That is accurate for this code: nothing interrupts a run, and the brief text carries the stop instruction.
- Runs 117, 126 and 127 print "(at the limit, not passed)", which agrees with the docstring.
- What `check` cannot show afterwards:
  - a token limit on null-token runs;
  - workers and retries on any run;
  - whether the plan preceded the run, when there is no transcript;
  - an edited plan;
  - whether the returned report said what was done, open and why. No code here reads the report.

## Speculation (labelled)
- Hand-written plans could be committed after a run began and `check` would print "not measured" for most runs, since only 2 have kept transcripts.
- The 6 against 11 tool-call disagreement for run 128 may come from the harness's count against the agent's own count (for example, parallel calls). This is unverified without the transcript.

## Open after this read
- **For the builder:**
  - The plan's content at the add commit is not compared with the file `check` reads.
  - Git order is not measured without a transcript; an uncommitted plan or a `--plan` outside the root reads "not measured" with exit 0.
  - Run 0, negative runs and all-zero limits are accepted by `write`.
  - `write` can recreate a deleted plan.
  - `max_tokens_is` in the plan is not read.
  - No test covers a late plan (M6 left all 7 clean), the max_tokens line or wall clock.
  - The `brief` text repeats the stop sentence ("...why it stopped: stop, and return what is done, what is open and why you stopped").
  - `check` on a run with no plan does not print the figures it could measure (run 96: 32 graph writes not shown).
  - The run 128 tool-call figure disagrees (6 on the line, 11 in the builder's report).
- **Settled by the plans:**
  - Graph writes are counted by `written_by` only, so `made_by` lines written through code (runs 25 and 36) and the reads, merges and evaluations folders are not counted. The plan names `written_by`; whether that matches "writes into the real graph" is Greg's call.
  - Tokens are held against the harness total, not the transcript sum (91,604 against 604,852 for run 117).
  - "At the limit" counts as kept.
- **What code cannot hold:**
  - Stopping an agent mid-run.
  - Requiring that a plan exists before a run is started from the chat.
  - Workers and retries, which no transcript records.
  - Tokens for runs with no harness total.

Housekeeping: /tmp/run134 and /tmp/pytest-of-root are deleted. `git status --short` is empty in both /home/user/markets-data and /home/user/Markets.

Tool calls: 11 Bash calls and 1 advisor call, so 12 before this hand-back, or 13 counting it. Run 134's limit is 20.

Files:
- /home/user/Markets/tools/kgraph/run_plan.py
- /home/user/Markets/tests/agent_program/test_run_plan.py
- /home/user/Markets/tools/swarm/plan.py (BUDGET_KEYS, line 24)
- /home/user/markets-data/tasks/family-research-20261022/research-union-current/paper-trading-20261123/run-plans/
- /home/user/markets-data/tasks/family-research-20261022/research-union-current/paper-trading-20261123/agent-runs.jsonl
- /home/user/markets-data/graph/edges/SUPERSEDES.jsonl (the 32 lines written by run:0096 sit across this file and DERIVED_FROM.jsonl and nodes/AgentRun.jsonl)
