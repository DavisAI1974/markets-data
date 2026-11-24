# Performance auditor run 156 (Sonnet): run 155, its own block

Kept word for word as the agent returned it, 2026-11-24 (twenty-fifth session). Nothing below this line is the main session's.

---

# Performance auditor run 156

## Run 155

Scout run 155, ticket 47, model `claude-haiku-5-5`. Both runs' files are under `/home/user/markets-data/tasks/family-research-20261022/research-union-current/paper-trading-20261123`. The transcript is `/root/.claude/projects/-home-user/3356516d-d71a-5e13-907d-ff8d8ffcb6d4/subagents/agent-adcd522db0c4a3e52.jsonl`.

Every figure below came from one Bash call. It ran `cat` on `run-plans/run-0155.json`, `grep '"run": *155' agent-runs.jsonl | tail -1`, `git log --diff-filter=A` on the plan file, `wc -c` on the output, `grep -A8 '^\*\*Scouts\*\*'` on `AUDIT_RUN_154.md`, and `jq -s` on the transcript. The `jq` grouped replies by `message.id` and took the last usage of each. It counted `tool_use` items by `name` and took the largest `tool_result` by text length.

### 1. The plan's limits against the figures reached

| Limit in the plan | Written | Reached | Result |
|---|---|---|---|
| `max_tokens` | 130,000 | 102,024 (harness total, on the line) | passed (under the limit) |
| `max_model_calls` | 30 | 5 replies | passed |
| `max_tool_calls` | 30 | 24 | passed |
| `max_wall_clock_s` | 600 | 118.526 s | passed |
| `max_sub_agents` | 0 | 0 | kept |
| `max_graph_writes` | 0 | 0 | kept |
| `max_concurrent_workers` | 1 | no measure in the transcript | not measured |
| `max_retries` | 1 | no measure in the transcript | not measured |

- **Graph writes:** the transcript has only Read, Grep, Glob and the hand-back. There are no write tools and no `Agent` calls.
- **Tokens:** the plan names the harness total as the measure. The transcript's four figures separately are fresh input 12, cache written 93,029, cache read 238,601 and output 32,337. They sum to 363,979. That is a different measure from the harness's 102,024, and the difference is 261,955. I did not derive 102,024 from the four figures.
- **Wall clock:** the transcript runs from 2026-11-24T15:05:21.381Z to 15:07:19.907Z.
- **Plan in git:** `run-0155.json` was added in commit `89fcd2e` at 2026-11-24T15:04:56+00:00. That is 25 s before the transcript's first timestamp, so it was in git before the run began.
- **Output:** `scout-20261124/SCOUT_RUN_155_TICKET_47.md` is 19,515 bytes.

### 2. The line against the transcript

- **Input tokens:** the line's `input_tokens` is 331,642. The transcript gives 12 + 93,029 + 238,601 = 331,642. It matches.
- **Other token fields:** fresh 12, cache written 93,029, cache read 238,601 and output 32,337 all match.
- **Replies:** `model_replies` 5 matches 5.
- **Tool calls:** `tool_calls` 24 matches the transcript's 24, which excludes the hand-back. The `outcome` text "24 tool calls of 30" matches that count and the plan's limit.
- **Wall clock:** `wall_clock_ms` 118,526 matches the transcript's timestamps exactly.
- **Harness total:** `tokens_reported` 102,024 has no counterpart in the transcript. The line says the harness total arrived later.

### 3. Where the spend went

- **Replies:** 5. All are `claude-haiku-5-5`.
- **Cache-read share:** 238,601 of 363,979 is 65.55%.
- **Cache read per reply:** 47,720.2.
- **Tool calls per reply:** 24 / 5 = 4.800.
- **Tool calls by kind:** Grep 12, Read 9, Glob 3 (24 in all), plus 1 `SubagentHandback`.
- **Largest tool result:** 14,599 characters, from Read of `/home/user/Markets/root/tape.py`.

## Set beside the earlier scouts

Figures for 150, 151 and 152 come from the `**Scouts**` table in `audits-20261124/AUDIT_RUN_154.md`.

| | 155 | 150 | 151 | 152 |
|---|---|---|---|---|
| Replies | 5 | 6 | 7 | 5 |
| Tool calls | 24 | 26 | 26 | 24 |
| Tool calls per reply | 4.800 | 4.333 | 3.714 | 4.800 |
| Cache-read tokens | 238,601 | 212,124 | 251,380 | 184,556 |
| Cache-read per reply | 47,720 | 35,354 | 35,911 | 36,911 |

The figures cannot show these things:
- Whether the tasks were the same size or difficulty.
- Whether the scouts' answers were complete or correct.
- Why cache read per reply differs. Context size at each reply is not in these figures.
- How the harness's token totals for 150 to 152 compare, since the table does not carry them.

Tool calls besides the hand-back in this audit: 1.
