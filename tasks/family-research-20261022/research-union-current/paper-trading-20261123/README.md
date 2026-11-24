# Paper trading, stage 7 of the graph engineering adoption plan (2026-11-23)

Greg's direction: tastytrade sandbox paper trading, signals from tastytrade's production quote stream, orders only to
the sandbox. The code is on Markets `ccr-fffbc766-a1gxpl` (`strategies/`). Everything a run sees is written here,
append-only.

- `agent-runs.jsonl`: one line for every agent run of the stage (role, model, task, tokens as the harness reports
  them, tool calls, wall clock, outcome), as the plan's token rules ask. Not yet in a graph: stages 2 and 4 are filed.
- `7e/` (not yet made): the output of the one-time 7e check, when it runs.
