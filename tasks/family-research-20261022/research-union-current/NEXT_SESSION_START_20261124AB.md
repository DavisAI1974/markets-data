# Start page AB, 2026-11-24 (twenty-fourth session). Short on purpose: the rest is asked of the graph.

## The one job

Greg, 2026-11-24: "Do each number as a ticket. We do nothing else right niw but do the complete build plan we
agreed on and all 44 or whatever steps there are one at a time. This is our only focus." Then: "we can do 2 or 3
at a time ... but they are consecutively numbered." And: "when we're done, I want a independent review agent skill
run to compare our work to the work on the tickets" (ticket 45).

- The tickets: `paper-trading-20261123/tickets-44-20261124/` (README first). The list they were cut from:
  `paper-trading-20261123/MISSING_PIECES_20261124.md`. The morning's list: `AGENT_BUILD_CHECKLIST_20261124.md`.
- A ticket's box is marked only with its evidence beside it. One waiting on his go or his decision is left open,
  said so, and the next is taken.
- The Pocock skills (public repository mattpocock/skills, read-only): `implement` a ticket at a time; ticket 45
  is `code-review` by two readers who built none of it.

## Where things are (heads at the time of writing; check each with git before trusting it)

| Repository | Branch | Head |
| --- | --- | --- |
| Markets (code) | `ccr-0ac78691-8zapbb` | `071777f` |
| markets-data (records, graph, tickets) | `ccr-0ac78691-8zapbb` | the commit that holds this page |
| paper-trading-platform, today's change | `ccr-0ac78691-8zapbb` (NOT Codex's branch) | `27f7261` |
| paper-trading-platform, Codex's branch (draft PR 5; he pushes there; fetch first) | `codex/strategy-trades-and-mbo-capture` | `47fa1c5` |

The platform change stays OFF Codex's branch until one pass of the tape shows a run with nothing plugged in is the
same row for row (ticket 40, his go).

## In flight when this page was written (read each one's last commits and notes before starting anything)

- Ticket batch 1, 2, 3 (worked 2, 3, 1): agent run 104 builds `tools/kgraph/defend.py` (a claim registered before
  its outcome; an independent challenge blind to the proposer's reasoning). It pushes a commit whose subject
  starts "PROPOSED, NOT YET READ BY THE REVIEWER" and stops; the reviewer reads it; then it goes on.
- Half-done work being finished: agent run 102, the packet that carries every data layer
  (`tools/kgraph/signal_packet.py`, `tools/decider/serve.py`; notes `tools/decider/BUILD_NOTES.md`); agent run 103,
  the reviewer's third read of the platform change (`47fa1c5..27f7261`).
- Not yet recorded in `paper-trading-20261123/agent-runs.jsonl`: runs 99 to 104. The next run is 105.

## His rules (each is his word, in the decisions file, twenty-fourth session)

- A TRADE DAY is 6 pm Eastern the evening before to 5 pm Eastern on the named date. No mid price. No trade cost.
  No averaging, pooling, ranking or labels. No made-up numbers. Nothing is replaced: only add.
- NO PAPER RUNS: not the workflow, not the trial runner, not the loop. Nothing puts the tape through the engine
  without his go, told first with its budget. No go for Frankie, Granite, a pod, the swarm or the token test.
  AWS is off limits. Launch is HOLD. Nothing goes to the trunk without his word.
- ZERO OUTSIDE GIT: "Zero on local drives and 100% in git." Every agent commits and pushes each piece as it
  stands. Say "not yet on GitHub", never "committed locally".
- EVERY CLAIM DEFENDED: the proposer of a claim is not its sole verifier (the verifier plan in Markets
  `research/kalshi/FRANKIE_INDEPENDENT_SCIENTIFIC_VERIFIER_PLAN.md`).
- THE AGENTS ARE THE DECIDERS at the tick; a decider may be a live agent or a program an agent wrote.
- NO DATA LAYER IS DROPPED for a decider: the MBO data, the planes and ROOT's calculations, the dipole above all,
  the market conditions. After-the-fact data is kept and joined to every decision for learning; it is kept out
  only of the packet a decider reads at the instant it decides.
- DO NOT RELY ONLY ON GRAPHS where they fall short: the plain source stands beside the graph.
- The hold rule in force: hold until the trade gives back 20% of its highest open profit. The runs of 2026-11-24
  are not scored and are no judgement of the strategies.
- His stop button ends agents; a stopped agent is started again unless he says otherwise; brief every agent to
  push each piece. Keys: names and places only, `paper-trading-20261123/KEYS_WHERE_THEY_ARE.md`; never ask him.
- Tell him before anything runs, with its limits. Plain words, the answer first. Record his decisions in git as
  they are made. Use the agents as their own files say: the scout locates and reads, the builder shows its change
  and waits, the reviewer reads every final diff.

## Ask the graph, do not read the pile

```
cd Markets && MARKETS_DATA=../markets-data python3 -m tools.kgraph.context --budget 6000 --task "<what you are about to do>"
```
Every line carries its claim id, file and line. The graph is weak on "where things are now" (two tests today):
trust this page and git for that. The session's disk fills from test scratch folders: delete them after each run.

## Slips of this session, so they are not made again

- Asked him who decides at the tick when the zip already said: the agents. Read the zip and the verifier plan.
- Told builders to commit and not push; told builders not to show their diff first; never used the scout.
- Let a builder leave data out of what a decider is given; nobody chooses what to thin.
- Called a size cut a saving before the content test held.
