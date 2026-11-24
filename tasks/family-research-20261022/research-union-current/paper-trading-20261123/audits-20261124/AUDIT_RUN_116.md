# Performance auditor run 116 (Sonnet): runs 110, 112 and 113, each its own block

Kept word for word as the auditor returned it, 2026-11-24 (twenty-fifth session). Nothing below this line is the main session's. The main session's note on one point is on the run's line in `agent-runs.jsonl`, not here.

---

# Audit of runs 110, 112 and 113, one block per run

Nothing is averaged or totalled across the runs. Every figure comes from the line in agent-runs.jsonl or from the transcript.

Commands used:
- Run record: `jq -c 'select(.run==110 or .run==112 or .run==113)' agent-runs.jsonl`.
- Token sums: `jq -s` over the subagent transcripts, selecting lines with .message.usage, `group_by(.message.id)|map(.[0])`, summing the four usage fields.
- First and last timestamp: .timestamp min and max.
- Tool calls: tool_use blocks in assistant messages, unique_by(.id).
- Largest results: each tool_result content length in characters, joined to its tool_use by id.
- Run 110's commit: `git show --stat 9ca6a48`.

"Four-figure sum" below means fresh input + cache-written + cache-read + output.

## Run 110 (builder, Sonnet 5.5, ended by Greg's stop mid-work)

**1. Limits against figures reached**

| Limit | Told beforehand | Reached |
|---|---|---|
| Tokens | 600,000 | Harness total: none (a stopped run gets none). Transcript four-figure sum: 2,179,322. Fresh + cache-written + output only: 147,287. |
| Tool calls | 80 | 24 |
| Wall clock | 40 min (2,400 s) | 584 s (12:56:57.351Z to 13:06:41.443Z) |

- The 600,000 limit is passed if the four-figure sum is the measure, and not passed if only fresh + cache-written + output is. The record does not say which the 600,000 meant.
- Tool calls and wall clock were not passed.

**2. Line against transcript**

| Figure | Line | Transcript |
|---|---|---|
| Fresh input | 46 | 46 |
| Cache-written | 118,945 | 118,945 |
| Cache-read | 2,032,035 | 2,032,035 |
| Output | 28,296 | 28,296 |
| Tool calls | 24 | 24 |
| Wall clock | 584,092 ms | 584,090 ms (timestamps) |

- No differences.
- The line's input_tokens of 2,151,026 equals 46 + 118,945 + 2,032,035.

**3. Where the spend went**
- Model replies: 21.
- Cache-read share of the four-figure sum: 2,032,035 / 2,179,322 = 93.2%.
- Three largest tool results:
  1. Read of /home/user/Markets-b456/tools/kgraph/defend.py, 38,117 characters.
  2. Read of /home/user/Markets-b456/tests/agent_program/test_defend.py, 20,237 characters.
  3. Read of a file under .../paper-trading-20261123/reviews-2... (path cut at 110 characters in my output), 17,209 characters.

**4. Produced**
- Commit 9ca6a48, 2 files: tools/kgraph/defend.py (103 lines changed) and tests/agent_program/test_defend.py (135 lines changed).
- Total 197 insertions and 41 deletions, 238 lines changed.
- Per the line, the commit was made after the stop by the main session (commit date 13:08:01), is marked unfinished, was not read by the reviewer, and its checks were not run.
- Against tokens: 238 lines changed for 2,179,322 four-figure tokens, or 147,287 without cache-read.
- No report was returned.

## Run 112 (scout, Haiku 5.5, finished)

**1. Limits against figures reached**

| Limit | Told beforehand | Reached |
|---|---|---|
| Tokens | 150,000 | Harness total 111,756. Transcript four-figure sum: 475,040. |
| Tool calls | 30 | 20 on the line, 21 in the transcript |
| Wall clock | 15 min (900 s) | 103 s (12:57:22.266Z to 12:59:05.541Z) |

- No limit was passed by the harness total, nor by fresh + cache-written + output (118,421).
- The four-figure sum of 475,040 is over 150,000. I do not know which measure the harness uses.

**2. Line against transcript**

| Figure | Line | Transcript |
|---|---|---|
| Fresh input | 12 | 12 |
| Cache-written | 92,212 | 92,212 |
| Cache-read | 356,619 | 356,619 |
| Output | 26,197 | 26,197 |
| Wall clock | 103,292 ms | 103,275 ms (timestamps) |
| Tool calls | 20 | 21 |

- The tool-call count differs by one, line 20 against transcript 21. I did not find which call accounts for it.
- tokens_reported is 111,756. I could not reproduce it from any sum of the usage fields. It is not 475,040, not 118,421, and not 448,843 + 26,197. It is unreconciled.

**3. Where the spend went**
- Model replies: 6, carrying 21 tool calls, so several calls were issued per reply.
- Cache-read share of the four-figure sum: 356,619 / 475,040 = 75.1%.
- Three largest tool results:
  1. Read of /home/user/paper-trading-platform/paper_platform/trial.py, 22,010 characters.
  2. Read of /home/user/Markets/tools/kgraph/defend.py, 15,844 characters.
  3. Read of /home/user/Markets/tools/kgraph/context.py, 12,859 characters.

**4. Produced**
- A report at scout-20261124/SCOUT_RUN_112_GAPS.md, 42,317 characters (`wc -c`).
- Not opened, per the line: the swarm's R module, the platform's session module, and pin() and recount() in dipole_renders.py. defend.py 427-546 was returned as load-bearing lines only.

## Run 113 (reviewer, Opus 5.5, ended by Greg's stop, returned nothing)

**1. Limits against figures reached**

| Limit | Told beforehand | Reached |
|---|---|---|
| Tokens | 250,000 | Harness total: none. Transcript four-figure sum: 1,770,665. Fresh + cache-written + output only: 136,996. |
| Tool calls | 30 | 21 |
| Wall clock | 20 min (1,200 s) | 320 s (13:01:21.092Z to 13:06:41.357Z) |

- The 250,000 limit is passed on the four-figure sum and not passed on the fresh + cache-written + output sum, the same ambiguity as run 110.
- Tool calls and wall clock were not passed.

**2. Line against transcript**

| Figure | Line | Transcript |
|---|---|---|
| Fresh input | 44 | 44 |
| Cache-written | 122,925 | 122,925 |
| Cache-read | 1,633,669 | 1,633,669 |
| Output | 14,027 | 14,027 |
| Tool calls | 21 | 21 |
| Wall clock | 320,265 ms | 320,265 ms (timestamps) |

- No differences.

**3. Where the spend went**
- Model replies: 21.
- Cache-read share of the four-figure sum: 1,633,669 / 1,770,665 = 92.3%.
- Three largest tool results:
  1. Read of a file under .../scout-202... (path cut at 110 characters in my output), 36,506 characters.
  2. Read of /home/user/Markets/tools/kgraph/defend.py, 20,097 characters.
  3. Bash, `cd /home/user/Markets/research/kalshi/frankie_boss && nl -ba CLAUDE_ARCH_PLAN_GRAPH_ENGINEERING_ADOPTION_20261...`, 9,765 characters.

**4. Produced**
- Nothing returned. The line says the plan was then changed and read again as run 115.

## Candidates for less spend on the next run of the same kind

All are candidates, not shown savings. I give no percentages.

- **Cache-read dominates the builder and reviewer runs** (93.2% and 92.3%), because each of their 21 replies re-reads a context that grows with every large Read.
  - Mechanism: fewer or smaller large reads early in the run, or reads of line ranges instead of whole files.
  - Example: defend.py was read whole as 38,117 characters in run 110. It was also read in runs 112 (15,844 characters) and 113 (20,097 characters). The three sizes differ, which suggests ranges or different repo copies. I did not check which.
  - To measure: per-reply cache_read_input_tokens against context length, and whether a ranged read changes the number of replies.
- **Parallel tool calls per reply.**
  - Mechanism: run 112 made 21 calls in 6 replies and its cache-read share was 75.1%. The other two made about one call per reply (24 calls in 21 replies, and 21 in 21), and their shares were above 92%.
  - To measure: the same task with batched and unbatched calls, comparing replies and cache-read.
- **Run 110 re-read of files it had open.**
  - Mechanism: I did not check whether defend.py or test_defend.py was read more than once.
  - To measure: count Read calls per path in the transcript.
- **The budget measure is ambiguous.**
  - Mechanism: the line records token limits, but the harness total for run 112 (111,756) does not reconcile to the transcript.
  - To measure: which fields the harness sums. Without that, a limit cannot be compared with a transcript figure.

## Finding on the stop

- **By the transcript, at the moment of the stop:**
  - Run 110 had used a four-figure sum of 2,179,322 (147,287 without cache-read) over 21 replies, 24 tool calls and 584 s.
  - Run 113 had used 1,770,665 (136,996 without cache-read) over 21 replies, 21 tool calls and 320 s.
  - Both transcripts end at about 13:06:41, so the stop reached them at the same time.
- **In git:** run 110's work is commit 9ca6a48. It was made after the stop (13:08:01), is marked unfinished, and is not reviewed or run.
- **Lost:** run 113's reading. It returned nothing and produced no file, so its findings exist only as the transcript. The run record's outcome field says the plan was changed afterwards and read again as run 115.

True tool-call count for this audit: 4 (plus this handback).
