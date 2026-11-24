# Performance auditor run 177 (Sonnet): run 167, its own block

Everything below this line is the agent's own report, word for word; nothing below it is the main session's.

## Hand-back 1 of 1

# Performance auditor run 177

## Run 167
Scout, model claude-haiku-5-5, ended by handing back. Ticket 04, group G03. I measured everything below with one `jq -s` pass over the transcript and one pass over the plan, the run line and git. Both ran inside a single Bash call.

**1. The eight limits in `run-plans/run-0167.json`, against the figures reached**

| Limit | Plan | Reached | Result |
|---|---|---|---|
| max_model_calls | 30 | 9 | under the limit |
| max_sub_agents | 0 | 0 (the line has `sub_agent_calls` 0; the transcript has no Task or Agent tool call) | at the limit, kept |
| max_concurrent_workers | 1 | not measured (no figure in the transcript or the line) | not measured |
| max_tool_calls | 30 | 27, plus 1 `SubagentHandback` that the line does not count | under the limit |
| max_tokens | 130,000 | harness total on the line, `tokens_reported`: 113,415 | under the limit |
| max_wall_clock_s | 600 | 91.643 s (transcript first timestamp 17:36:20.114Z, last 17:37:51.757Z; the line says `wall_clock_ms` 91643) | under the limit |
| max_retries | 0 | not measured (no retry figure in the transcript or the line) | not measured |
| max_graph_writes | 0 | no write tool appears in the tool calls (Read 13, Grep 14, `SubagentHandback` 1); the line has no graph-write figure | not measured as a number |

- The transcript's four token figures are fresh input 18, cache written 97,321, cache read 532,461 and output 20,693. They add up to 650,493.
- The plan says the 130,000 limit is the harness total, not the transcript sum. The transcript sum is 650,493 and was not compared with the limit.
- The harness total of 113,415 does not equal any combination of the four transcript figures that I tried.
- The plan file was added to git in commit `e60eeaa` at 2026-11-24T17:33:37+00:00. That is 2 min 43 s before the transcript's first timestamp of 17:36:20.114Z, so it was in git before the run began.

**2. The line against the transcript**
- `input_tokens_fresh` 18, `input_tokens_cache_written` 97,321, `input_tokens_cache_read` 532,461 and `output_tokens` 20,693 all match the transcript exactly.
- `input_tokens` 629,800 equals 18 + 97,321 + 532,461. That is the three input figures summed, without output.
- `model_replies` 9 matches the 9 distinct `message.id` values.
- `tool_calls` 27 matches the transcript's 27 calls besides the hand-back. `hand_backs` 1 matches. `started_at` and `ended_at` match the first and last transcript timestamps.
- By name, the transcript has Read 13 and Grep 14, with no Glob. The scout's report at `SCOUT_RUN_167_TICKET_04.md` line 9 says "27 of 30 (Read 9, Grep 16... counted as 27 total...)". Read 9 plus Grep 16 is 25, not 27. The transcript has 4 more Read calls and 2 fewer Grep calls than the report names, but its total of 27 matches.
- The same line says "Model calls: 0 advisor calls". The transcript has 9 model replies, so the line and the report count model calls differently.
- The report file is 15,798 bytes (`wc -c`).

**3. Where the spend went**
- There were 9 model replies, all from claude-haiku-5-5.
- Cache read is 532,461 of the 650,493 transcript total, which is 81.9%. It is 84.6% of the input side (629,800).
- Cache read per reply averages 59,162 (532,461 / 9). Cache written is 97,321 and output is 20,693.
- Tool calls per reply average 3.0 (27 / 9).
- Tool calls by kind are Read 13 and Grep 14, with no Glob.
- The largest tool result is a Read of `.../paper-trading-20261123/reviews-20261124/REVIEW_RUN_146_TICKET_04.md`, at 15,735 characters.
- The second largest is a Read of `/home/user/Markets/tests/agent_program/test_outcome.py` (offset 90, limit 195), at 11,887 characters.

Tool calls besides the hand-back in this run (177): 1 (one Bash call).
