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

## Set up before anything else (each of these cost time this session)

- The session's branches are cut from an old tip. Put them on top of the heads in the table below before working
  (this session's branches held no commits of their own).
- paper-trading-platform is not attached to a new session: add it with `add_repo`, then fetch its WHOLE history
  (a shallow copy names every rule's commit wrongly).
- markets-data must hold its whole history BEFORE any command that writes into the graph (a shallow copy wrote 62
  wrong-commit lines this session; they were discarded). The same for Markets before a graph write names one of
  its files: this session's Markets copy stayed shallow.
- `tools.kgraph.extract coverage` WRITES into the graph; it is not a read.
- The graph's store refuses a write from a working copy that holds uncommitted code: write from a clean copy.
- The session's disk fills from test scratch folders (`/tmp/pytest-of-root`, any `--basetemp`): delete after each run.
- arxiv.org is allowed in the Markets environment (added this session on his approval).

## Where things are (heads at the time of writing; check each with git before trusting it)

| Repository | Branch | Head |
| --- | --- | --- |
| Markets (code) | `ccr-0ac78691-8zapbb` | `2ac873f` |
| markets-data (records, graph, tickets) | `ccr-0ac78691-8zapbb` | the commit that holds this page |
| paper-trading-platform, today's change | `ccr-0ac78691-8zapbb` (NOT Codex's branch) | `28d4dbb` |
| paper-trading-platform, Codex's branch (draft PR 5; he pushes there; fetch first) | `codex/strategy-trades-and-mbo-capture` | `47fa1c5` |

The platform change stays OFF Codex's branch until one pass of the tape shows a run with nothing plugged in is the
same row for row (ticket 40, his go).

## Where the work stopped (nothing is in flight; every agent has reported and every working copy is on GitHub)

Heads when this was written: Markets `2ac873f`, the platform's `ccr-0ac78691-8zapbb` branch `28d4dbb`.

DO FIRST, in this order:
1. The reviewer re-reads Markets `3a6ac09` (tickets 02 and 03, `tools/kgraph/defend.py`) against its own findings
   in `paper-trading-20261123/reviews-20261124/REVIEW_RUNS_103_105.md`. Then mark tickets 02 and 03 or list what
   is open.
2. Ticket 01: every claim of the first written decider registered and independently challenged (its ticket file
   says what it needs). Batches after that: consecutive numbers, two or three at a time. Ticket 46 (stop the
   consolidation drift) and ticket 45 (the independent review at the end) are added to the 44.
3. Ticket 38 is OPEN and matters to him: "all of the data depth" is not met. Of the 458 columns of the Excel
   daily sheets for 2023-10-02, 27 reach the packet, 13 the after-the-fact file, and 418 are not given to a
   decider (398 are ROOT's per-tick columns, left out for size). Its ticket file has the five open points.
4. The reviewer has not read: Markets `e55da89..2ac873f` (the packet), `7672c8d` (afterwards), `6fdd4e1..1e9a7c5`
   (the loop on the decider program), `9054a00`, `1d0a6dc` (the deciders' door), `04f4378` (the first decider),
   `53d46c9` (the context builder), and the platform's `28d4dbb` (the third review's fixes).

- The platform change (`47fa1c5..28d4dbb`) has been read three times by the reviewer: nothing changes a run with
  nothing plugged in, by reading. It has never met the tape. What the first pass must show, in order, is in the
  reviews file.
- The stored planes of ROOT are on the markets-data branch `root-rows-20231002`, not in the working checkout:
  the packet reads them from a git dir named by `MARKETS_PLANES_GIT` (make one with a blobless mirror of that
  branch; it is not kept anywhere).
- Agent runs are recorded through 106 in `paper-trading-20261123/agent-runs.jsonl` (runs 99 to 106 are not yet
  loaded into the graph: run `ingest_agent_runs` from committed code). The next run is 107.

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
- NO FEES are computed now; Codex's matcher stands as it is (his word).
- The hold rule in force: hold until the trade gives back 20% of its highest open profit. The runs of 2026-11-24
  are not scored and are no judgement of the strategies.
- NEVER deploy the phone page during a run (a deploy empties it).
- His stop button ends agents; a stopped agent is started again unless he says otherwise; brief every agent to
  push each piece. Keys: names and places only, `paper-trading-20261123/KEYS_WHERE_THEY_ARE.md`; never ask him.
- Tell him before anything runs, with its limits. Plain words, the answer first. Record his decisions in git as
  they are made. Use the agents as their own files say: the scout locates and reads, the builder shows its change
  and waits, the reviewer reads every final diff.

## Ask the graph for what it holds; read the file for what it does not

```
cd Markets && MARKETS_DATA=../markets-data python3 -m tools.kgraph.context --budget 6000 --task "<what you are about to do>"
```
Every line carries its claim id, file and line. KNOW ITS LIMITS:
- The graph holds the decisions file only to line 7195. EVERYTHING HE DECIDED AFTER THAT IS NOT IN IT: all of
  the data depth, after-the-fact data, the hybrid, every claim defended, the tickets and their batches, no fees,
  ticket 46, the Excel comparison. Read the decisions file from line 7196 to its end
  (`root-redesign-20261116/ROOT_GAMEPLAN_DECISIONS.md`); it is short.
- The graph is weak on "where things are now" (two tests this session: 7 then 9 of 15 questions answered, one
  wrong both times, the platform's branch). Trust this page and git for that.
- THIS PAGE AND THE GRAPH HAVE NOT BEEN TESTED TOGETHER. That test (a fresh agent, the 15 questions) was promised
  for the close and was not run; it is ticket 32. Do not read this page as proven. It does not say: the one file
  a trial changes (`paper_platform/execution_plans/loop-trial.json`, a byte copy of the give-back plan); how run
  47 was settled (both lines stay; the line marked `corrects` is the run's next revision).
- Also promised for the close and not done: reading the decisions file's tail into the graph.

## Slips of this session, so they are not made again

- Asked him who decides at the tick when the zip already said: the agents. Read the zip and the verifier plan.
- Told builders to commit and not push; told builders not to show their diff first; never used the scout.
- Let a builder leave data out of what a decider is given; nobody chooses what to thin.
- Called a size cut a saving before the content test held.

## ADDED 2026-11-24, twenty-fifth session (his word): READ FIRST, EVERY SESSION

`READ_FIRST_UNTIL_THE_AGENTS_PART_IS_DONE.md` (beside this page): the eight files of the zip `frankie_handoff_20261123_2.zip`, where each is in git, and that THERE ARE FOUR AGENTS. Read them in full before any ticket work, every session, until Greg says the agents part is done.
