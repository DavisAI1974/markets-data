# Performance auditor run 171 (Sonnet): run 157, its own block

Everything below this line is the agent's own report, word for word; nothing below it is the main session's.

## Hand-back 1 of 1

# Performance auditor run 171

## Run 157

Scout run 157, group G08, tickets 18 and 19, model `claude-haiku-5-5` on all 6 replies. The files are under `/home/user/markets-data/tasks/family-research-20261022/research-union-current/paper-trading-20261123`. The transcript is `/root/.claude/projects/-home-user/3e104f60-b369-56be-82d1-295b070262b0/subagents/agent-a9e48461f5f4f0068.jsonl`.

I took the figures from two Bash calls:
- **First call:**
  - `jq -s` on the transcript. It grouped replies by `message.id` and took the last usage of each. It counted `tool_use` items by `name`, and it took the largest `tool_result` by text length.
  - `grep '"run": *157' agent-runs.jsonl | tail -1`.
  - `cat run-plans/run-0157.json`.
  - `git log --diff-filter=A --format='%h %cI'` on the plan file.
  - `wc -c` on the output file.
  - `grep -n '17 of 30'` on the scout's report.
- **Second call:** `sed -n 14,70p` on `AUDIT_RUN_156.md`.

### 1. The plan's limits against the figures reached

| Limit in the plan | Written | Reached | Result |
|---|---|---|---|
| `max_tokens` | 130,000 | 82,148 (harness total, on the line) | passed (under the limit) |
| `max_model_calls` | 30 | 6 replies | passed |
| `max_tool_calls` | 30 | 17 | passed |
| `max_wall_clock_s` | 600 | 57.773 s | passed |
| `max_sub_agents` | 0 | 0 | kept |
| `max_graph_writes` | 0 | 0 | kept |
| `max_concurrent_workers` | 1 | no measure in the transcript | not measured |
| `max_retries` | 1 | no measure in the transcript | not measured |

- **Graph writes:** the transcript has only Read (12), Grep (5) and the hand-back. There are no write tools and no `Agent` or `Task` calls.
- **Tokens, transcript:** the four figures separately are fresh input 12, cache written 76,316, cache read 258,037 and output 12,573. They sum to 346,938. That is a different measure from the harness's 82,148. The difference is 264,790, and I did not derive 82,148 from the four figures.
- **Wall clock:** the transcript runs from 2026-11-24T17:30:40.656Z to 17:31:38.429Z.
- **Plan in git:** `run-0157.json` was added in commit `d70527a` at 2026-11-24T17:28:54+00:00. That is 106 s before the transcript's first timestamp, so it was in git before the run began.
- **Output:** `scout-20261124/SCOUT_RUN_157_TICKETS_18_19.md` is 13,886 bytes.

### 2. The line against the transcript

- **Input tokens:** the line's `input_tokens` is 334,365. The transcript gives 12 + 76,316 + 258,037 = 334,365. It matches.
- **Other token fields:** fresh 12, cache written 76,316, cache read 258,037 and output 12,573 all match.
- **Replies:** `model_replies` 6 matches 6.
- **Tool calls:** `tool_calls` 17 matches the transcript's 17, which excludes the hand-back. The scout's report line 97 says "TOOL CALLS: 17 of 30 used". That matches the transcript's count.
- **Model calls in the scout's report:** the same line 97 says "Model calls: 0 of 30 by me beyond this run". The transcript shows 6 replies. The report's figure does not match the transcript.
- **Wall clock:** `wall_clock_ms` 57,773 matches the transcript's timestamps exactly.
- **Harness total:** `tokens_reported` 82,148 has no counterpart in the transcript.
- **Hand-backs and sub-agents:** `hand_backs` 1 and `sub_agent_calls` 0 match the transcript.

### 3. Where the spend went

- **Replies:** 6.
- **Cache-read share:** 258,037 of 346,938 is 74.38%.
- **Cache read per reply:** 43,006.2.
- **Tool calls per reply:** 17 / 6 = 2.833.
- **Tool calls by kind:** Read 12, Grep 5, Glob 0 (17 in all), plus 1 `SubagentHandback`.
- **Largest tool result:** 12,359 characters, from Read of `/home/user/Markets/tools/kgraph/run_record.py` (offset 160, limit 216). The next two are 7,728 characters (Read of `run_plan.py`, offset 226, limit 147) and 6,505 characters (a Read under `/home/user/markets-data/tasks/...`).

## Set beside the earlier scouts

Scout 155's figures are from `audits-20261124/AUDIT_RUN_156.md`, section 3 and its table.

| | 157 | 155 |
|---|---|---|
| Replies | 6 | 5 |
| Tool calls | 17 | 24 |
| Tool calls per reply | 2.833 | 4.800 |
| Cache-read tokens | 258,037 | 238,601 |
| Cache-read per reply | 43,006 | 47,720 |

What the figures show:
- Run 157 has one more reply and 7 fewer tool calls than 155.
- Its calls per reply are lower, and its cache read per reply is lower.
- Its total cache read is higher.
- Its tool calls were Read and Grep only, with no Glob.

What the figures cannot show:
- **What changed:** whether the brief's exact line ranges changed the count of calls.
- **What changed:** whether the request for several calls in one reply was followed. Calls per reply is an average, not a per-reply count.
- **Task size:** whether tickets 18 and 19 are the same size or difficulty as ticket 47.
- **Answer quality:** whether the answers were complete or correct.
- **Cache read per reply:** why it differs. Context size at each reply is not in these figures.

Tool calls besides the hand-back in this audit: 2.
