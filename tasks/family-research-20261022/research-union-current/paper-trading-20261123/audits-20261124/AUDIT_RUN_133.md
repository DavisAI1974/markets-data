# Performance auditor run 133 (Sonnet): runs 123, 125, 126, 127 and 129, each its own block

Kept word for word as the agent returned it, 2026-11-24 (twenty-fifth session). Nothing below this line is the main session's.

---

## Run 123 (reviewer, claude-opus-5-5, transcript agent-a573a75c19b5cc986.jsonl)

Sources: the run line from `jq` on `agent-runs.jsonl` for run 123, `run-plans/run-0123.json`, and one `jq -s` pass over the transcript that groups replies by `message.id` and takes the last usage record of each. All five runs share this method. "Cache-read share" is the cache-read tokens divided by the sum of all four figures (fresh, cache-written, cache-read, output).

1. Limits against the figures reached
   - The plan file was added to git at 13:36:21Z (commit 9bfef60, from `git log --diff-filter=A`). The transcript's first timestamp is 13:37:55.877Z, so the plan was in git before the run began.
   - max_model_calls 25: 14 replies. Not passed.
   - max_sub_agents 0: 0. The tool names are Bash 13 plus the hand-back. Kept.
   - max_concurrent_workers 1: not measured. Every reply carried one tool call.
   - max_tool_calls 20: 13 besides the hand-back. Not passed.
   - max_tokens 200,000:
     - The harness total on the line is 81,986. Not passed on that measure.
     - The transcript figures are fresh 30, cache-written 69,231, cache-read 825,377 and output 18,834. They add to 913,472.
     - Fresh + cache-written + output is 88,095. Neither sum gives 81,986.
   - max_wall_clock_s 1200: 260.746 s (13:37:55.877 to 13:42:16.623). Not passed.
   - max_retries 1: the transcript holds 1 tool result with `is_error` true. It is a Bash command that exited 1, and its text starts with a table row. Whether it was retried was not read.
   - max_graph_writes 0: there was no Edit or Write call. Its Bash commands name `graph/auditor_called.py`, `graph/store.py` and `graph.auditor_called` as module paths, but I did not read their bodies. A write into the real graph is not measured.

2. The line against the transcript
   - Input 894,638 = 30 + 69,231 + 825,377 exactly. Output 18,834, replies 14, tool calls 13 and wall clock 260,745 ms all match. The transcript gives 260,746 ms, a difference of 1 ms.
   - No other difference found.

3. Where the spend went
   - 14 replies. Cache-read share: 825,377 / 913,472 = 90.4%.
   - Cache-read per reply: 58,955. Tool calls per reply: 13/14 = 0.93.
   - The largest tool result is a Bash call of 18,016 characters, a `pytest tests/agent_program/test_auditor_called.py` run piped through `tail`. The second largest is a Bash `cat -n` of that test file, 14,185 characters.

4. What it produced
   - `reviews-20261124/REVIEW_RUN_123_TICKET_03b.md`, 16,142 bytes (`wc -c`).
   - By its line: 15 checks ran clean and 1 did not, and the line lists six points for the builder.

## Run 125 (scout, claude-haiku-5-5, transcript agent-af855fd72e77ad5bd.jsonl)

1. Limits against the figures reached
   - The plan file was added to git at 13:36:21Z (commit 9bfef60). The first transcript timestamp is 13:37:55.905Z, so the plan was in git before the run began.
   - max_model_calls 15: 6 replies. Not passed.
   - max_sub_agents 0: 0. The tool names are Glob 1, Grep 5 and Read 11, plus the hand-back. Kept.
   - max_concurrent_workers 1: not measured. The first reply issued 6 tool calls at once.
   - max_tool_calls 20: 17 besides the hand-back. Not passed.
   - max_tokens 100,000:
     - The harness total on the line is 95,606. Not passed on that measure.
     - The transcript figures are fresh 12, cache-written 82,497, cache-read 323,831 and output 17,719. They add to 424,059.
     - Fresh + cache-written + output is 100,228, which is above 100,000 by 228. The harness total is not that sum.
   - max_wall_clock_s 600: 70.512 s (13:37:55.905 to 13:39:06.417). Not passed.
   - max_retries 1: 0 tool results with `is_error` true.
   - max_graph_writes 0: no Edit, Write or Bash call. Only Glob, Grep and Read were used.

2. The line against the transcript
   - Input 406,340 = 12 + 82,497 + 323,831 exactly. Output, replies 6, tool calls 17 and wall clock 70,512 ms all match.
   - No difference found.

3. Where the spend went
   - 6 replies. Cache-read share: 323,831 / 424,059 = 76.4%.
   - Cache-read per reply: 53,972. Tool calls per reply: 17/6 = 2.83. Calls per reply were 6, 4, 3, 2, 2 and 1.
   - The largest tool result is a Read of `/home/user/Markets/tools/ratchet/proposer.py`, 16,336 characters. The second is a Read of `tools/kgraph/defend.py` from line 463, limit 262, 16,143 characters.

4. What it produced
   - `scout-20261124/SCOUT_RUN_125_TICKET_04.md`, 25,042 bytes, 336 lines.
   - It stopped at 17 of 20 tool calls. Its own "NOT FOUND" list is:
     - No `rests_on` key per trial in the loop's history, and no per-trial claim list in the push body.
     - No code in `tools/ratchet` or `tools/kgraph` that checks every registered claim of a trial has a challenge. The closest is `defend.undefended` (defend.py:694).
     - No `ratchet.py`.
     - Not opened: `tests/agent_program/realrecords.py`, the PLATFORM and PLAN constants of `test_stage3_proposer.py`, and the test bodies beyond the names in the grep.
   - A closing note adds that it did not grep the tests for `MailboxFileProposer`.

## Run 126 (scout, claude-haiku-5-5, transcript agent-a381cdf273414b6c6.jsonl)

1. Limits against the figures reached
   - The plan file was added to git at 13:38:52Z (commit 773a6db). The first transcript timestamp is 13:39:31.484Z, so the plan was in git before the run began.
   - max_model_calls 15: 3 replies. Not passed.
   - max_sub_agents 0: 0. The tool names are Glob 1, Grep 11 and Read 8, plus the hand-back. Kept.
   - max_concurrent_workers 1: not measured. The first reply issued 17 tool calls at once.
   - max_tool_calls 20: 20 besides the hand-back. Exactly at the limit. The report says "TOOL CALLS: 20 (the limit)".
   - max_tokens 100,000:
     - The line has `tokens_reported` null, so there is no harness total to compare.
     - The transcript figures are fresh 6, cache-written 100,923, cache-read 103,478 and output 18,893. They add to 223,300.
     - Fresh + cache-written + output is 119,822.
     - On the transcript figures the limit is passed by either sum. On the harness measure it is unmeasured.
   - max_wall_clock_s 600: 79.127 s (13:39:31.484 to 13:40:50.611). Not passed.
   - max_retries 1: 0 tool results with `is_error` true.
   - max_graph_writes 0: no Edit, Write or Bash call.

2. The line against the transcript
   - Input 204,407 = 6 + 100,923 + 103,478 exactly. Output, replies 3, tool calls 20 and wall clock 79,127 ms all match.
   - No difference found.

3. Where the spend went
   - 3 replies. Cache-read share: 103,478 / 223,300 = 46.3%.
   - Cache-read per reply: 34,493. Tool calls per reply: 20/3 = 6.67. Calls per reply were 17, 3 and 1.
   - The largest tool result is a Read of `agent-runs.jsonl`, offset 66, limit 57, `allow_large` true, 55,447 characters. The second is a Grep over `tests/agent_program`, 13,895 characters.

4. What it produced
   - `scout-20261124/SCOUT_RUN_126_TICKETS_18_19.md`, 13,836 bytes, 93 lines.
   - It stopped at its tool-call limit. Its own "NOT FOUND / NOT DONE" list is:
     - (h) the first 3 lines of a sub-agent transcript. Glob gave 59 files in the transcripts folder and no sizes, and it read no transcript line.
     - (i) the ingest test function names and line numbers.
     - (j) the text of item 10 of AUDIT_RUN_111's findings. The Grep stopped at an omitted line.
   - It also names hit caps reached on three searches: 60 on the `run.py` grep, 40 on the ratchet grep and 100 on the tests def-grep.

## Run 127 (scout, claude-haiku-5-5, transcript agent-a26374fd2d98f4b5d.jsonl)

1. Limits against the figures reached
   - The plan file was added to git at 13:38:52Z (commit 773a6db). The first transcript timestamp is 13:39:31.502Z, so the plan was in git before the run began.
   - max_model_calls 15: 2 replies. Not passed.
   - max_sub_agents 0: 0. The tool names are Glob 7, Grep 6 and Read 7, plus the hand-back. Kept.
   - max_concurrent_workers 1: not measured. The first reply issued 20 tool calls at once.
   - max_tool_calls 20: 20 besides the hand-back. Exactly at the limit, all in the first reply.
   - max_tokens 100,000:
     - The harness total on the line is 94,921. Not passed on that measure.
     - The transcript figures are fresh 4, cache-written 72,340, cache-read 27,571 and output 23,047. They add to 122,962.
     - Fresh + cache-written + output is 95,391.
     - 94,921 is not either sum.
   - max_wall_clock_s 600: 88.772 s (13:39:31.502 to 13:41:00.274). Not passed.
   - max_retries 1: 0 tool results with `is_error` true.
   - max_graph_writes 0: no Edit, Write or Bash call.

2. The line against the transcript
   - Input 99,915 = 4 + 72,340 + 27,571 exactly. Output, replies 2, tool calls 20 and wall clock 88,772 ms all match.
   - No difference found.

3. Where the spend went
   - 2 replies. Cache-read share: 27,571 / 122,962 = 22.4%.
   - Cache-read per reply: 13,786 (13,785.5 rounded). Tool calls per reply: 20/2 = 10.00. Calls per reply were 20 and 1.
   - The largest tool result is a Read of `tests/agent_program/test_stage5a_context.py`, 24,447 characters. The second is a Read of `tools/kgraph/schema.py`, 8,614 characters.

4. What it produced
   - `scout-20261124/SCOUT_RUN_127_TICKET_25.md`, 23,831 bytes, 284 lines.
   - It stopped at its tool-call limit. Its own "NOT FOUND / NOT CAPTURED" list is:
     - `Artifact.jsonl` and `Metric.jsonl` are not in `graph/nodes`.
     - The `store.py` `check_all` body after line 373 was not captured, because the grep -A window ended there.
     - Where the fifteen questions are kept is not named in any hit.
     - `ingest_platform.py` has no Metric or Artifact hit, and its existence was not separately verified.
     - No git was used, per its instructions.

## Run 129 (builder, claude-sonnet-5-5, transcript agent-a1e36d84b29f4ab5b.jsonl)

1. Limits against the figures reached
   - The plan file was added to git at 13:42:20Z (commit b51ed27). The first transcript timestamp is 13:45:44.363Z, so the plan was in git before the run began.
   - max_model_calls 40: 7 replies. Not passed.
   - max_sub_agents 0: 0. The tool names are Bash 6 plus the hand-back. Kept.
   - max_concurrent_workers 1: not measured. Every reply carried one tool call. The plan note says several builders were working at once, each in its own copy.
   - max_tool_calls 50: 6 besides the hand-back. Not passed.
   - max_tokens 350,000:
     - The line has `tokens_reported` null, so there is no harness total to compare.
     - The transcript figures are fresh 14, cache-written 44,235, cache-read 256,628 and output 15,540. They add to 316,417.
     - Fresh + cache-written + output is 59,789.
     - By either sum it is not passed.
   - max_wall_clock_s 1800: 101.374 s (13:45:44.363 to 13:47:25.737). Not passed.
   - max_retries 1: 0 tool results with `is_error` true.
   - max_graph_writes 0: there was no Edit or Write call. Its Bash commands name `ingest_agent_runs.py` and `run_record.py` as files, and one contains `git add`, `git commit` and `git push`. I did not read the bodies for a write into the real graph, so that figure is not measured.

2. The line against the transcript
   - Input 300,877 = 14 + 44,235 + 256,628 exactly. Output, replies 7, tool calls 6 and wall clock 101,374 ms all match.
   - No difference found.

3. Where the spend went
   - 7 replies. Cache-read share: 256,628 / 316,417 = 81.1%.
   - Cache-read per reply: 36,661. Tool calls per reply: 6/7 = 0.86. Every reply carried one call.
   - The largest tool result is a Bash call of 8,315 characters. It runs `cd /home/user/Markets-b19 && git log --oneline -1 && …` and then `cat tests/agent_program/realre…`. The second is a Bash call of 2,585 characters that opens transcripts for runs 116 and 117 with gzip and json.

4. What it produced
   - `git -C /home/user/Markets show --stat 5c5ceb8` lists 3 files: `tools/kgraph/run_record.py` (291 lines added), `tests/agent_program/test_run_record.py` (149 lines added) and `tools/kgraph/ingest_agent_runs.py` (6 lines changed). The total is 444 insertions and 2 deletions.
   - By its line, the commit is marked PROPOSED and pushed, and 9 checks ran clean by its own report.

## Set beside the earlier runs

The earlier figures come from `AUDIT_RUN_124.md` (builders 121, 114, 110 and reviewers 118, 115, 107) and `AUDIT_RUN_120.md`, block "## Run 117" (scouts 117, 112, 109). I did not re-measure them. Per-reply figures are divisions of the figures shown.

**Builder: run 129 beside 121, 114 and 110**

| | 129 | 121 | 114 | 110 |
|---|---|---|---|---|
| Replies | 7 | 16 | 22 | 21 |
| Tool calls | 6 | 14 | 26 | 24 |
| Tool calls per reply | 0.86 | 0.875 | 1.18 | 1.14 |
| Cache-read tokens | 256,628 | 840,239 | 1,962,598 | 2,032,035 |
| Cache-read per reply | 36,661 | 52,515 | 89,209 | 96,764 |

**Reviewer: run 123 beside 118, 115 and 107**

| | 123 | 118 | 115 | 107 |
|---|---|---|---|---|
| Replies | 14 | 17 | 19 | 14 |
| Tool calls | 13 | 16 | 26 | 14 |
| Tool calls per reply | 0.93 | 0.94 | 1.37 | 1.00 |
| Cache-read tokens | 825,377 | 1,053,514 | 1,504,731 | 1,599,935 |
| Cache-read per reply | 58,955 | 61,971 | 79,196 | 114,281 |

**Scouts: runs 125, 126 and 127 beside 117, 112 and 109**

| | 125 | 126 | 127 | 117 | 112 | 109 |
|---|---|---|---|---|---|---|
| Replies | 6 | 3 | 2 | 10 | 6 | 10 |
| Tool calls | 17 | 20 | 20 | 30 | 20 | 41 |
| Tool calls per reply | 2.83 | 6.67 | 10.00 | 3.00 | 3.33 | 4.10 |
| Cache-read tokens | 323,831 | 103,478 | 27,571 | 501,509 | 356,619 | 655,995 |
| Cache-read per reply | 53,972 | 34,493 | 13,786 | 50,151 | 59,437 | 65,600 |

What the figures can show:
- On these five measures, runs 125, 126 and 127 each have fewer replies and less cache-read than the earlier scouts.
- Run 129 has fewer replies, fewer tool calls and less cache-read than the earlier builders.
- Run 123 has fewer cache-read tokens than the earlier reviewers.
- Tool calls per reply for the three scouts (2.83, 6.67 and 10.00) are above the earlier scouts' 3.00 to 4.10 in runs 126 and 127. Run 125's 2.83 is slightly below run 117's 3.00.
- Runs 126 and 127 sent 17 and 20 calls in their first reply.

What the figures cannot show:
- The tasks differ in size and content. Run 129 wrote a 291-line module and a 149-line test. Run 123 ran a test and a command on the real record, and the scouts located different things.
- Each cell is one run, with no repeat.
- Cache-read depends on how long the context grows, which depends on the task.
- Fewer replies means fewer cache reads by arithmetic.
- The briefing method of each run is not isolated from its task.
- These figures say nothing about the quality or completeness of any run's output.

Tool calls I made besides the hand-back: 6, all Bash.
