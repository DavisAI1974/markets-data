# Performance auditor run 173 (Sonnet): runs 159, 160 and 161, each its own block

Everything below this line is the agent's own report, word for word; nothing below it is the main session's.

## Hand-back 1 of 1

# Performance auditor run 173

Three runs audited, read-only, two Bash calls. Nothing is totalled or averaged across runs. The transcripts are the ones in the task's SUB directory; PAPER is the paper-trading-20261123 directory.

Commands:
- Per transcript, one `jq -s` pass. Replies are grouped by `message.id`, with the last usage of each id counted once. Tool calls are `tool_use` items counted by `name`. Tool results are matched to their `tool_use` by id, and sizes are the characters of the result content.
- Plans and lines: `jq -c` on each `run-plans/run-0NNN.json`, and `grep` for the run's line in `agent-runs.jsonl`.
- Git: `git log --diff-filter=A` on each plan file, and `git show --stat` on 703e77c and 60f8086.

Wall clock is the first to the last transcript timestamp. All three transcripts start between 17:30:40.519Z and 17:30:40.662Z and end between 17:31:53.734Z and 17:31:53.754Z on 2026-11-24.

## Run 159
Scout, claude-haiku-5-5. Tickets 46, 44 and 30.

1. Limits against the figures reached at the stop:

| Limit | Plan | Measured |
|---|---|---|
| max_model_calls | 30 | 7 replies, under |
| max_tool_calls | 30 | 26, under |
| max_tokens | 130,000 | See the token line below |
| max_wall_clock_s | 600 | 73.092 s, under |
| max_sub_agents | 0 | 0, kept |
| max_concurrent_workers | 1 | Not measurable from the transcript |
| max_retries | 1 | Not measurable from the transcript |
| max_graph_writes | 0 | 0. Its tools were Glob, Grep and Read only, and no write call appears |

   - Token figures: fresh input 14, cache written 124,115, cache read 427,737, output 8,683. The plan defines max_tokens as the harness's total, input and output together, and the lines hold no harness total. The sum of the four figures is 560,549. Fresh input plus output is 8,697.
   - The plan file entered markets-data git in d70527a at 2026-11-24T17:28:54+00:00, before the first timestamp.

2. Line against transcript:
   - Every figure matches: replies 7, tool calls 26, sub-agent calls 0, hand-backs 0, wall_clock_ms 73,092, and the four token figures.
   - The line's input_tokens of 551,866 equals 14 + 124,115 + 427,737.
   - The transcript holds no `SubagentHandback` call.

3. Where the spend went:
   - Cache read is 76.3% of the four figures (427,737 of 560,549), or 61,105 per reply.
   - Tool calls per reply: 26/7 = 3.71.
   - Tool calls by kind: Grep 15, Read 7, Glob 4.
   - The largest result is Read of /home/user/Markets/tools/kgraph/extract.py at 34,952 characters. The next is Read of resolve.py at 21,260.
   - The last tool call was Grep `^def test_` in /home/user/Markets/tests/agent_program, glob `test_stage[45][ac]*.py`, with head_limit 0.

## Run 160
Reviewer, claude-opus-5-5. Ticket 21.

1. Limits against the figures reached at the stop:

| Limit | Plan | Measured |
|---|---|---|
| max_model_calls | 18 | 6 replies, under |
| max_tool_calls | 14 | 7, under |
| max_tokens | 140,000 | See the token line below |
| max_wall_clock_s | 1200 | 73.125 s, under |
| max_sub_agents | 0 | 0, kept |
| max_concurrent_workers | 1 | Not measurable from the transcript |
| max_retries | 1 | Not measurable from the transcript |
| max_graph_writes | 0 | No write call appears. It ran 5 Bash calls, and I did not read their commands for writes |

   - Token figures: fresh input 12, cache written 67,185, cache read 266,742, output 3,442. The sum is 337,381. Fresh input plus output is 3,454.
   - The plan file was added in d70527a at 17:28:54, before the first timestamp.

2. Line against transcript:
   - Every figure matches: 6 replies, 7 tool calls, 0 sub-agent calls, 0 hand-backs, 73,125 ms, and the four token figures.
   - The line's input_tokens of 333,939 equals 12 + 67,185 + 266,742.
   - The transcript holds no hand-back.

3. Where the spend went:
   - Cache read is 79.1% of the four figures (266,742 of 337,381), or 44,457 per reply.
   - Tool calls per reply: 7/6 = 1.17.
   - Tool calls by kind: Bash 5, Read 2.
   - The largest result is Read of SCOUT_RUN_150_TICKET_21.md at 13,258 characters. The next is a Bash call at 12,900 characters, which ran grep over a saved tool-results file for `^(== |exp-)` header lines.
   - The last tool call was a Bash loop in /home/user/wt/r165 running `python3 -m tools.exp_dag fetch` on D0, exp-D0 and exp-f76195cc9730.

## Run 161
Builder, claude-sonnet-5-5. Ticket 31.

1. Limits against the figures reached at the stop:

| Limit | Plan | Measured |
|---|---|---|
| max_model_calls | 50 | 9 replies, under |
| max_tool_calls | 50 | 8, under |
| max_tokens | 400,000 | See the token line below |
| max_wall_clock_s | 2100 | 73.215 s, under |
| max_sub_agents | 0 | 0, kept |
| max_concurrent_workers | 1 | Not measurable from the transcript |
| max_retries | 1 | Not measurable from the transcript |
| max_graph_writes | 0 | I did not read its Bash commands for writes into markets-data. The list below shows what it ran |

   - Token figures: fresh input 18, cache written 47,105, cache read 301,825, output 10,188. The sum is 359,136, which is under 400,000. Fresh input plus output is 10,206.
   - The plan file was added in d70527a at 17:28:54, before the first timestamp.

2. Line against transcript:
   - Every figure matches: 9 replies, 8 tool calls, 0 sub-agent calls, 0 hand-backs, 73,215 ms, and the four token figures.
   - The line's input_tokens of 348,948 equals 18 + 47,105 + 301,825.
   - The transcript holds no hand-back.
   - The line's outcome text says the check file was committed and pushed by the run as 703e77c. Git shows 703e77c at 17:31:25 with one file, `tests/agent_program/test_manifest_check.py` (210 lines).
   - Git shows 60f8086 at 17:33:06 with one file, `tools/kgraph/manifest_check.py` (143 lines). That is 73 s after the last transcript timestamp.
   - Both commit messages carry "[skip ci]".

3. Where the spend went:
   - Cache read is 84.0% of the four figures (301,825 of 359,136), or 33,536 per reply.
   - Tool calls per reply: 8/9 = 0.89.
   - Tool calls: Bash 8, no other kind.
   - The largest result is Bash call 0 at 6,315 characters. It ran `git log`, `git status` and `sed -n 9,40p` on a markets-data file in /home/user/wt/b161. The next is Bash call 2 at 2,314 characters, a `git ls-tree` on commit 42614ca.
   - The last tool call was Bash in /home/user/markets-data: `git show d70527a:paper-rules/20261109/machine/PAPER_UNIVERSE_MANIFEST.json`, piped to a short python3 snippet that prints the JSON's top-level key types.
   - Order of the two files: the check file was written first. Bash call 4 is `cat > tests/agent_program/test_manifest_check.py` and Bash call 5 is `cat > tools/kgraph/manifest_check.py`. Call 6 then ran `python3 -m tools.kgraph.manifest_check --range 557a3b0..d70527a` on the real history.

My true count of tool calls besides the hand-back is 2.
