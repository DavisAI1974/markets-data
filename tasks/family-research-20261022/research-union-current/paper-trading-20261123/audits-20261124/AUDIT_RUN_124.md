# Performance auditor run 124 (Sonnet): runs 118, 119 and 121, each its own block, and the briefing with line ranges set beside the earlier builder runs

Kept word for word as the agent returned it, 2026-11-24 (twenty-fifth session). Nothing below this line is the main session's. Its hand-back call only pointed at its last message; that message is what is kept here.

---

## Run 118

Reviewer, claude-opus-5-5. Transcript `agent-acd74e5550ed6e466.jsonl`. The line is the newest `run==118` line in `agent-runs.jsonl`.

**1. The eight limits** (from `run-plans/run-0118.json`)

| Limit | Plan | Reached | Passed? |
|---|---|---|---|
| max_model_calls | 30 | 17 replies | no |
| max_sub_agents | 0 | 0 (no Task or Agent tool call in the transcript) | no |
| max_concurrent_workers | 1 | not measured (see below) | not measured |
| max_tool_calls | 30 | 16 Bash, plus 1 hand-back that is not counted | no |
| max_tokens | 300,000 | harness total: none (the line has `tokens_reported: null`). Transcript four figures summed: 1,165,422. Fresh input + cache-written + output: 111,908 | see below |
| max_wall_clock_s | 1500 | 683.589 s | no |
| max_retries | 1 | not measured (no retry is visible in the line) | not measured |
| max_graph_writes | 0 | not measured. I did not inspect the graph; the line's outcome says both checkouts were left untouched | not measured |

- On the tokens limit, the four-figure sum of 1,165,422 is over 300,000. Fresh input + cache-written + output is 111,908, which is under it. The plan defines the limit as the harness total, which this run does not have, so I cannot say which measure the 300,000 meant.
- The overlap in transcript start times is a fact, not a finding. Runs 118 and 119 both start at 13:23:23.7Z, so two workers ran at the same moment. Each is one worker within its own plan. I did not test what "concurrent" meant in the plan.
- Plan file in git: `git log` gives `b96fc54 2026-11-24T13:22:10+00:00`. The first transcript timestamp is 13:23:23.720Z. The plan is 73 s before the run.
- Wall clock: `jq` on the first and last `.timestamp` gives 13:23:23.720Z to 13:34:47.309Z, which is 683.589 s.

**2. The line against the transcript**

Method: `jq -s` on the assistant lines, grouped by `message.id`, then summed.
- Fresh input is 36, cache-written 87,558, cache-read 1,053,514, output 24,314. All match the line's fields.
- The line's `input_tokens` is 1,141,108. That equals 36 + 87,558 + 1,053,514 exactly.
- `tool_calls` 16 on the line matches 16 Bash calls in the transcript.
- `wall_clock_ms` 683,589 matches.
- There is no difference.

**3. Where the spend went**
- Model replies: 17, all claude-opus-5-5.
- Cache-read share of the four-figure sum: 1,053,514 / 1,165,422 = 90.40%.
- Cache-read per reply: 61,971.
- Tool calls per reply: 16/17 = 0.94.
- Three largest tool results, in characters. Each was measured by the length of the tool_result content, joined to its tool_use by id.
  1. Bash `git diff -U2 2ac873f 68d65a6 -- tools/kgraph/defend.py tools/kgraph/BUILD_NOTES_DEFEN…`: 25,907.
  2. Bash `git diff -U1 2ac873f 68d65a6 -- tests/agent_program/test_defend.py | cut -c1-220`: 17,057.
  3. Bash `R=…/paper-trading-20261123; sed -n …`: 7,648.

**4. What it produced**
- `reviews-20261124/REVIEW_RUN_118.md`: 15,114 bytes (`wc -c`).
- The line's outcome field says 53 checks ran clean at 68d65a6, and 16 did not with `defend.py` put back to 2ac873f. It also says 12 points were open afterwards. I did not re-check those counts.

## Run 119

Builder as proposer, claude-sonnet-5-5. Transcript `agent-aab0e9aa79c507339.jsonl`. It has two parts and two hand-backs.

**1. The eight limits** (from `run-plans/run-0119.json`)

| Limit | Plan | Reached | Passed? |
|---|---|---|---|
| max_model_calls | 40 | 13 replies | no |
| max_sub_agents | 0 | 0 | no |
| max_concurrent_workers | 1 | not measured (see run 118 for the overlap in start times) | not measured |
| max_tool_calls | 60 | 12 Bash, plus 2 hand-backs that are not counted | no |
| max_tokens | 400,000 | harness total 87,372 at the first hand-back; none for the second. Transcript four figures summed: 979,555. Fresh + cache-written + output: 112,154 | harness total under it; four-figure sum over it |
| max_wall_clock_s | 1800 | 359.458 s, first to last line, including the wait between the two parts | no |
| max_retries | 1 | the record says it was sent back once; I did not test this against the limit's meaning | not measured |
| max_graph_writes | 0 | not measured | not measured |

- Plan file in git: `b96fc54 2026-11-24T13:22:10+00:00`. The first transcript timestamp is 13:23:23.738Z. The plan is 73 s before the run.
- Wall clock: 13:23:23.738Z to 13:29:23.196Z.

**2. The line against the transcript**
- Fresh input is 28, cache-written 83,385, cache-read 867,401, output 28,741. All match the line.
- The line's `input_tokens` is 950,814. That equals 28 + 83,385 + 867,401.
- `tool_calls` 12 matches.
- `wall_clock_ms` 359,458 matches.
- The line's `tokens_reported` of 87,372 is the first hand-back's harness figure. I cannot reproduce it from the four figures.
- There is no difference.

**3. Where the spend went**
- Model replies: 13.
- Cache-read share of the four-figure sum: 867,401 / 979,555 = 88.55%.
- Cache-read per reply: 66,723.
- Tool calls per reply: 12/13 = 0.92.
- Three largest tool results, in characters:
  1. Bash `cd …/paper-trading-20261123; cat s…` (command cut at 110 characters): 21,866.
  2. Bash `cd /home/user/Markets; git -C /home/user/markets-data-b118 log --oneline -1; git -C …`: 13,826.
  3. Bash `cd /home/user/Markets; sed -n 1,110p tools/kgraph/defend.py; echo ======; cat tools/decider/programs/decider_v…`: 12,312.

**4. What it produced**
- `git show --stat 11fe552` (13:28:14Z) shows 10 files and 687 insertions in `claims-20261124/decider_v1/`: README.md plus nine JSON files.
  - The JSON files are condition-1 to condition-4, inference-1, inference-3, inference-4a, inference-4b and inference-4c.
- `9079b22` (13:29:16Z) shows 2 files and 85 insertions: `inference-2.json` plus 1 line in the README.
- The commit messages are marked "PROPOSED, NOT YET REGISTERED".

## Run 121

Builder, claude-sonnet-5-5. Transcript `agent-a90a42cc900cc13e5.jsonl`. It has two parts and two hand-backs. It is the first run briefed with line ranges handed over and told not to search.

**1. The eight limits** (from `run-plans/run-0121.json`)

| Limit | Plan | Reached | Passed? |
|---|---|---|---|
| max_model_calls | 40 | 16 replies | no |
| max_sub_agents | 0 | 0 | no |
| max_concurrent_workers | 1 | not measured | not measured |
| max_tool_calls | 50 | 14 Bash, plus 2 hand-backs that are not counted | no |
| max_tokens | 350,000 | harness total 66,280 at the first hand-back and 75,440 at the second. Transcript four figures summed: 936,767. Fresh + cache-written + output: 96,528 | harness total under it; four-figure sum over it |
| max_wall_clock_s | 1800 | 242.399 s, including the wait between the two parts | no |
| max_retries | 1 | the record says it was sent back once; I did not test this against the limit's meaning | not measured |
| max_graph_writes | 0 | not measured | not measured |

- Plan file in git: `9e145fc 2026-11-24T13:30:12+00:00`. The first transcript timestamp is 13:31:00.781Z. The plan is 48 s before the run.
- Wall clock: 13:31:00.781Z to 13:35:03.180Z.

**2. The line against the transcript**
- Fresh input is 34, cache-written 66,746, cache-read 840,239, output 29,748. All match the line.
- The line's `input_tokens` is 907,019. That equals 34 + 66,746 + 840,239.
- `tool_calls` 14 matches.
- `wall_clock_ms` 242,399 matches.
- The line's 75,440 is the second hand-back's harness figure. I cannot reproduce it from the four figures.
- There is no difference.

**3. Where the spend went**
- Model replies: 16.
- Cache-read share of the four-figure sum: 840,239 / 936,767 = 89.70%.
- Cache-read per reply: 52,515.
- Tool calls per reply: 14/16 = 0.875.
- Three largest tool results, in characters:
  1. Bash `git log --oneline -1 && git branch --show-current && sed -n 34,66p tools/kgraph/ingest_agent_runs.py && cat te…`: 11,557.
  2. Bash `M=/home/user/markets-data; P=$M/tasks/…`: 4,204.
  3. Bash `cd /home/user/markets-data && P=tasks/…/paper-trading-20261123; …`: 2,259.

**4. What it produced**
- `git -C /home/user/Markets diff --stat 68d65a6 3a98333` shows 6 files and 506 insertions:

| File | Insertions |
|---|---|
| `.claude/agents/builder.md` | 1 |
| `.claude/agents/frankie-performance-auditor.md` | 18 |
| `.claude/agents/reviewer.md` | 1 |
| `CLAUDE.md` | 5 |
| `tests/agent_program/test_auditor_called.py` | 262 |
| `tools/kgraph/auditor_called.py` | 219 |

- `git log` shows commits 923a016 and 2fc12c7 at 13:33:34Z, and 3a98333 at 13:34:49Z.

## The briefing with line ranges, set beside the earlier builder runs

**Builder: run 121 beside runs 110 and 114** (figures for 110 and 114 are from `AUDIT_RUN_116.md` and `AUDIT_RUN_120.md`, not re-measured by me)

| | Run 121 | Run 110 | Run 114 |
|---|---|---|---|
| Replies | 16 | 21 | 22 |
| Tool calls | 14 | 24 | 26 |
| Tool calls per reply | 0.875 | 1.14 | 1.18 |
| Cache-read tokens | 840,239 | 2,032,035 | 1,962,598 |
| Cache-read per reply | 52,515 | 96,764 | 89,209 |
| Output tokens | 29,748 | 28,296 | 20,871 |
| Largest single tool result (characters) | 11,557 | 38,117 | 28,265 |

- Per-reply and per-call figures are my own divisions: 2,032,035 / 21, 1,962,598 / 22, 24 / 21 and 26 / 22.
- Run 110 was ended by Greg's stop mid-work.

**Reviewer: run 118 beside runs 115 and 107.** Run 118 was briefed before the change and only told to bundle its commands.

| | Run 118 | Run 115 | Run 107 |
|---|---|---|---|
| Replies | 17 | 19 | 14 |
| Tool calls | 16 | 26 | 14 |
| Tool calls per reply | 0.94 | 1.37 | 1.00 |
| Cache-read tokens | 1,053,514 | 1,504,731 | 1,599,935 |
| Cache-read per reply | 61,971 | 79,196 | 114,281 |
| Output tokens | 24,314 | 27,296 | not in the sources I read |
| Largest single tool result (characters) | 25,907 | 13,888 | not in the sources I read |

**What these figures can show**
- On the same measures, run 121's replies, tool calls and cache-read tokens are smaller than those of runs 110 and 114. Run 118's are smaller than those of runs 115 and 107, except that its 16 tool calls exceed run 107's 14.
- Cache-read per reply is lower in runs 118 and 121 than in the earlier runs.
- Tool calls per reply are below 1 in runs 118, 119 and 121.
- Run 121's largest result is smaller than the largest in runs 110 and 114. Run 118's largest is larger than run 115's.

**What they cannot show**
- The tasks differ in size and content. Run 121 wrote a 219-line script, a 262-line test and a few lines of rules. Runs 110 and 114 were reads and writes of other files, so the work done is not the same.
- Run 118 read a git diff of defend.py, which run 115 did not read. Its largest result is a different kind of object.
- Each comparison is one run per cell, with no repeat. Cache-read depends on how long the context grows, and that in turn depends on the task.
- Run 121 was briefed differently from runs 110 and 114, but so was everything else about its task. The figures cannot separate the briefing from the task.
- Run 118 was not briefed under the new rule, so it is not a test of that briefing.
- Output tokens are higher in run 121 than in runs 110 and 114, and lower in run 118 than in run 115.

My true count of tool calls besides the hand-back: 4 (three Bash calls, one to read the audit reports, and one more Bash call). Let me state it plainly: **4 Bash calls**.
