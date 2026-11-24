# Performance auditor run 178 (Sonnet): run 162, its own block

Everything below this line is the agent's own report, word for word; nothing below it is the main session's.

## Hand-back 1 of 1

# Performance auditor run 178

## Run 162
Scout, claude-haiku-5-5, group G07, ticket 38, run 158 started again. I checked it against its transcript, its plan and its line. Two `jq -s` passes over the transcript gave the figures below (`group_by(.message.id)`, last usage of each id). Tool-call counts come from `tool_use` items by name. My first `jq` pass had a syntax error, so I ran it a second time.

**1. Limits in run-plans/run-0162.json against the figure reached**

| Limit | Written | Reached | Passed, kept or at the limit |
|---|---|---|---|
| max_model_calls | 30 | 8 replies | kept |
| max_tool_calls | 30 | 28 (Grep 16, Read 12), plus 1 SubagentHandback not counted | kept |
| max_tokens | 130,000 | harness total on the line: 118,753 | kept |
| max_wall_clock_s | 600 | 95.827 s (17:36:20.004Z to 17:37:55.831Z) | kept |
| max_sub_agents | 0 | 0 (no Task or Agent call) | kept |
| max_concurrent_workers | 1 | not measurable from the transcript | none |
| max_retries | 0 | not measurable from the transcript | none |
| max_graph_writes | 0 | 0 (only Read, Grep and the hand-back were called) | kept |

- The transcript's four figures are fresh input 16, cache written 102,288, cache read 543,302 and output 21,570. They sum to 667,176, which is above 130,000. The plan defines max_tokens as the harness total, so I set the harness figure against it. I did not reconcile 118,753 with the four figures. The transcript does not show how the harness total is made up.
- The plan file entered git in commit e60eeaa at 2026-11-24T17:33:37+00:00. That is 2 min 43 s before the first transcript timestamp, so it was in git before the run began.

**2. The line against the transcript**
- The line is the newest `"run": 162` in agent-runs.jsonl.
- It matches the transcript on fresh input 16, cache written 102,288, cache read 543,302, output 21,570, and input_tokens 645,606 (the sum of the first three).
- It also matches on model_replies 8, tool_calls 28, hand_backs 1 and sub_agent_calls 0.
- wall_clock_ms 95,827 and the started_at and ended_at timestamps match.
- I found no difference between the line and the transcript.
- tokens_reported (118,753) has no transcript counterpart, so I could not check it.
- The scout's report (`wc -c`: 18,207 bytes) gives three counts of its tool calls.
  - "28 of 30" differs by 0 from the transcript's 28.
  - "28 tool calls, 28 total" differs by 0.
  - "29 tool calls of 30" is 1 above the transcript's 28.
  - Its own numbered list runs to 28 entries and then calls the last Read "call 29". The transcript has 28 calls besides the hand-back.
  - It also says "Read 12, Grep 10". The transcript has Read 12 and Grep 16.

**3. Where the spend went**
- Model replies: 8.
- Cache read is 543,302 of 667,176 (81.4%). Cache written is 15.3%, output 3.2%, and fresh input is under 0.01%.
- Cache read per reply is 67,913 (543,302 / 8).
- Tool calls per reply: 3.5 (28 / 8).
- Tool calls by kind: Grep 16, Read 12, Glob 0.
- The largest tool result is a Grep of `/home/user/Markets/root` for "position_on_tape|exchange_time_ns|received_time_ns|def rows_for_calculations|mbo|…", at 14,496 characters. The second largest is a Grep of `/home/user/Markets` for "MARKETS_PLANES_GIT|planes_since|…", at 13,478 characters.

## Set beside the stopped run
| | Run 158 at its stop | Run 162 |
|---|---|---|
| Model replies | 9 | 8 |
| Tool calls | 24 (Grep 14, Read 10) | 28 (Grep 16, Read 12) |
| Cache read | 628,279 | 543,302 |
| Wall clock | 73.078 s | 95.827 s |

- The two runs together made 17 replies and 52 tool calls over about 169 s of wall clock. Cache read across both is 1,171,581.
- Run 158 was stopped before it handed back and had no harness token total. Run 162 ended with a hand-back and a harness total of 118,753.
- The figures cannot show how much of run 158's reading run 162 repeated. They cannot show whether the one added sentence ("Hand back early…") changed the run. They cannot show how the harness total is made up. They also say nothing about the report's content.

My true count of tool calls besides the hand-back: 3.
