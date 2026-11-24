# Handoff Y: end of the twenty-first session (2026-11-24)

**Start here:** in Markets (branch `ccr-075001b3-wcxrxy`), with markets-data beside it (branch `ccr-349e2ffe-07p8od`):

```
python3 -m tools.kgraph.context --budget 6000
python3 -m tools.kgraph.context --budget 4000 --task "<the task>"
```

The manual is Markets `tools/README_AGENT_PROGRAM.md`. Greg's words of the session and what came of each are in
`root-redesign-20261116/ROOT_GAMEPLAN_DECISIONS.md`, "Twenty-first session". This handoff only says where things
stopped.

## Two jobs are open

### 1. The agent program (the graph adoption plan, stages 2 to 8)

Built: every stage, as code with checks on real records. The review (runs 34 and 35) found about seventy things;
four builder runs (37 to 40) and Claude (the Frankie packet) fixed them. The whole suite:
153 passed, 7 skipped, none failed (`python3 -m pytest tests/agent_program -q`, Markets `537749a`). The 7 skipped
  each say why: no real record exists for that case.

Not done:

- THE REAL GRAPH HAS NOT BEEN RUN THROUGH THE FIXED CODE. The fixes were checked on scratch graphs. Still to run
  on the real graph, in this order, each of them code only, no model:
  `python3 -m tools.kgraph check` (lists every breach), `python3 -m tools.kgraph.extract recheck` (writes two
  checks for each of the 1,147 claims: the figures in a claim against its own entry, and who said it),
  `python3 -m tools.kgraph.platform_scope mark`, then `check` again. The store now refuses a write into the real
  graph from uncommitted code, and refuses a source file with uncommitted changes: commit first.
- Under the reader's new rules (a quote needs six words and must stand as whole words) 37 of the 1,142 claims the
  seven reads returned would not be taken today. The claims already in the graph are untouched: nothing is
  replaced. Whether those 37 get a mark is not decided.
- No pass writes the link between a stale claim and the claim that says otherwise (review F7.1), so the session
  start can still show both with nothing to say which stands. CLAUDE.md is not in the reader's scope (F7.2).
- The lines of the decisions file after line 6152, and this handoff, are not read into claims. 97 documents are
  not read at all (`python3 -m tools.kgraph.extract coverage`).
- The manual does not yet name what the fixes added: `tools.token_test.replay count` and the two budget flags
  `plan` now needs, `tools.kgraph.extract recheck` and `load --pieces`, the three column groups of the packet.

### 2. Codex's draft PR 5 (paper-trading-platform, branch `codex/strategy-trades-and-mbo-capture`)

Greg: help Codex; item 17 first, then 2, 23, 26; item 35 waits. One number at a time; the checklist text under
the number is updated in the same commit (`docs/platform/OWN_PLATFORM_WISHLIST_20261123.md`). Codex's handoff
(`docs/platform/HANDOFF.md`) says this pass is build only: no checks, validation or tests on that branch, and no
paper session without Greg's go.

Item 17 stands here (all of it in `paper-trading-20261123/item17-20261124/README.md`):

- On his branch (`f475465`): `paper_platform/execution_plans/NG_OCT2023_CONTRACT.md` with the tape's instrument ID
  (150611) and the NGX3 contract definition, converted from the stored exchange record by NautilusTrader's own
  loader; and the status under item 17 with what is missing, by rule ID.
- NOT done: the plan file. No agent has chosen placement or size for any rule. Two decider runs (41, 42) were
  briefed and were stopped at the session change before they answered. Their briefs are kept and need their
  paths re-pointed before a new run.
- Frankie's choices are missing for all 30 rules: launch is on HOLD and needs Greg's go.

Item 23 (added after this handoff was first written; Greg: "go to a different number while I get 17 straight with
codex"): BUILT IN DRAFT, NOTHING RUN, on his branch as `297f8a4`. `paper_platform/agent_launcher.py` stops an agent
run at its token or clock budget and sends the reason to the phone; `.github/workflows/agent_run.yml` starts it on
Greg's go. Missing, his to say, and written under item 23: the budget figures for an agent run, the
`ANTHROPIC_API_KEY` Actions secret, and the open gap that an agent started inside a Claude Code session cannot be
stopped part-way. Item 23 stays open until it has been run.

Item 2 waits on the item 17 plan. Item 26 is not started. Greg is settling item 17 with Codex himself: leave item
17 and its deciders alone until he says. Codex added both authors' rule text and the plan format to
`paper-trading-20261123/item17-20261124/` (`41ec052`).

## Put to Greg, not answered

1. THE FRANKIE PACKET. Native's polarity, magnitude, threshold, baseline and prominence: Native works them out at
   the second it calls the event knowable, and the line that carries them was written 4 to 1,028 seconds later
   on the four trade days. The packet now holds them back, with the one column made from the polarity. Which
   reading governs is his.
2. FRIDAY 5 PM TO 6 PM EASTERN in the token test's trade-day placing: the builder read it as belonging to no trade
   day (no trade day follows Friday's), not as the daily halt. His to correct.
3. Each still needs his go, with its budget told first: a run of the swarm (counted at 3.2 to 3.7 million input
   tokens a trade day before the fix changed the briefs; count again with `tools.swarm.run plan`), a run of the
   token test, reading the 97 documents, dispatching a loop, switching Frankie's input, any paper run.

## Standing, unchanged

A TRADE DAY is 6 pm Eastern the evening before to 5 pm Eastern on the named date. No mid price. No trade cost. No
averaging, pooling, ranking or labels. No made-up numbers. Nothing is replaced: what does not hold up is marked
and called last. No new claim rests on a tastytrade platform issue. AWS is off limits. Launch is HOLD. Nothing
goes onto the Markets trunk without his word. Nothing is run without telling him first.
