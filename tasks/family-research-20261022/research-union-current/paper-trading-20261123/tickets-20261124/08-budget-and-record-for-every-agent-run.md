# 08: A budget and a full record for every agent run

**What to build:** No agent run starts without its limits written down, something holds it to them, and its record carries what the plan asks.

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

- [ ] Before each run a plan holds the eight limits (model calls, sub-agents, concurrent workers, tool calls, tokens, wall clock, retries, graph writes)
- [ ] A run that reaches a limit stops and returns what is done, what is open and why
- [ ] Each run's record has the exact model, input tokens, output tokens, wall clock and outcome
- [ ] Today's runs are filled in from their own transcripts, the stopped ones too
- [ ] Missing pieces covered: C18, C19
