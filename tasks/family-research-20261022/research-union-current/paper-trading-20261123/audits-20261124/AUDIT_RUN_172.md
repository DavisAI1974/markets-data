# Performance auditor run 172 (Sonnet): run 158, its own block

Everything below this line is the agent's own report, word for word; nothing below it is the main session's.

## Hand-back 1 of 1

# Performance auditor run 172

## Run 158
Scout, claude-haiku-5-5, group G07, ticket 38. Stopped by Greg's stop before it handed back. Source for every figure: the run's transcript, read with one `jq -s` pass (`group_by(.message.id)`, last usage of each id). I audited it from the transcript, and the plan and the line against it.

**1. Limits in run-plans/run-0158.json against the figure reached at the stop**

| Limit | Written | Reached | Measured by |
|---|---|---|---|
| max_model_calls | 30 | 9 replies | group_by message.id count |
| max_tool_calls | 30 | 24 (Grep 14, Read 10) | tool_use items by name |
| max_tokens | 130,000 | no harness total. Transcript sum of the four figures is 755,587 (fresh input 18, cache written 115,484, cache read 628,279, output 11,806). This sum is above 130,000 | jq sum over replies |
| max_wall_clock_s | 600 | 73.078 s, from 17:30:40.659Z to 17:31:53.737Z | first and last `.timestamp` |
| max_sub_agents | 0 | 0 | no Task or Agent tool_use |
| max_concurrent_workers | 1 | not measured, no workers seen | none |
| max_retries | 1 | not measurable from the transcript | none |
| max_graph_writes | 0 | 0 | the 24 tool calls are Read and Grep only |

- The plan defines max_tokens as "the harness's total for the run when it ends". That total was not given, so the comparison against 130,000 uses the transcript sum.
- Three limits are not measurable from the transcript: concurrent workers, retries and the harness token total.
- The plan file was added to git in commit d70527a at 2026-11-24T17:28:54+00:00. That is 1 min 46 s before the first transcript timestamp, 17:30:40.659Z. The plan's `written_before_the_run_started` field is true.

**2. The line (newest `"run": 158` in agent-runs.jsonl) against the transcript**
- The line's input_tokens_fresh (18), input_tokens_cache_written (115,484), input_tokens_cache_read (628,279) and output_tokens (11,806) equal the transcript's four figures.
- The line's input_tokens is 743,781, which is 18 + 115,484 + 628,279. Matches.
- The line's model_replies (9) and tool_calls (24) match.
- The line's wall_clock_ms is 73,078, and started_at and ended_at match the first and last timestamps.
- Sub-agent calls are 0 in both.
- The line has tokens_reported: null.
- The line says hand_backs 0. The transcript holds no hand-back. A jq count of `tool_use` items named SubagentHandback is 0. A plain grep for the string finds 2 lines, which are text, not tool calls (grep -c SubagentHandback).
- I found no difference between the line and the transcript.

**3. Where the spend went**
- Model replies: 9.
- Cache read share of the four figures: 628,279 / 755,587 = 83.2%. Cache written is 15.3%, output 1.6%, fresh input 0.002%.
- Cache read per reply: about 69,809 (628,279 / 9).
- Tool calls per reply: 24 / 9 = 2.67.
- Tool calls by kind: Grep 14, Read 10, Glob 0.
- Largest tool result by characters: Grep, 18,588 characters, on /home/user/Markets/tools/decider/afterwards.py (a Read). The tool_result id toolu_01472... is the `Read` of that file.
- Second largest: Grep, 16,659 characters, pattern `MARKETS_PLANES_GIT|planes_since|layers\.json|afterwards_layers|state\.json|MBO|paper-trading-platform|skip` over /home/user/Markets, glob limited to signal_packet.py and tools/decider.
- The last reply before the stop was running a Grep for `F\. [A-Z]` in /home/user/Markets/root/rows.py (content mode, head_limit 20).

My count of tool calls besides the hand-back: 2 Bash calls.
