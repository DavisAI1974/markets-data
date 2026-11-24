# Start page AC, 2026-11-24 (twenty-fifth session). The page before this one: `NEXT_SESSION_START_20261124AB.md`.

## READ FIRST, EVERY SESSION (his word)

Greg, 2026-11-24: "Make sure you have bext sess load the zip files into local memory".

THE FIRST THING THIS SESSION DOES, before anything below: read ALL EIGHT files of the zip
`frankie_handoff_20261123_2.zip` IN FULL, each whole with the Read tool. They are in git byte for byte in one
folder beside this page: `frankie_handoff_20261123_2/` (the plan, the handoff index, Codex's amendments, the
CLAUDE.md patch, and the four agent files under `.claude/agents/`). Read the verifier plan with them (Markets
`research/kalshi/FRANKIE_INDEPENDENT_SCIENTIFIC_VERIFIER_PLAN.md`). If the session has a memory folder of its
own, copy the eight files into it and say so; if it has none, tell him so plainly. Then read
`READ_FIRST_UNTIL_THE_AGENTS_PART_IS_DONE.md` (beside this page): THERE ARE FOUR KINDS OF AGENT (scout, builder,
reviewer, performance auditor). This holds every session until Greg says the agents part is done. Do not ask him what the zip or a plan already answers ("Do whatever our plan says").

## The one job, and how he wants it worked from here

Greg, 2026-11-24: "Do each number as a ticket. We do nothing else right niw but do the complete build plan we
agreed on and all 44 or whatever steps there are one at a time. This is our only focus."

Greg, 2026-11-24, the last word of the twenty-fifth session: "You said that these tickets were grouped together
before. Let's get a full suite of 4 types of agents on each ticket group. We can start new sess first though".

- The tickets (48, with ticket 47 added at the close): `paper-trading-20261123/tickets-44-20261124/` (README first). ONE IS MARKED DONE (03b). A box is
  marked only with its evidence beside it, and only when `python3 -m tools.kgraph.auditor_called --ticket NN`
  exits 0 (no run that worked on it is unaudited).
- The groups: `paper-trading-20261123/tickets-44-20261124/GROUPS.md` says which ticket is in which of the
  fourteen groups, which groups a builder may work on without his go, and where each stood at this close. Ten
  placements in it are Claude's, marked "(placed)", his to correct.
- A SUITE for a group is the four kinds, in the order their own files give: the scout locates (exact files and
  lines), the builder builds from those places (its change is a commit marked PROPOSED and pushed), the reviewer
  reads the change in its own working copy, the performance auditor audits that group's runs, each run its own
  `## Run NNN` block. Then the builder is sent the reviewer's points, and round again until the reviewer leaves
  nothing for the builder.
- BEFORE ANY SUITE STARTS: each run's limits are written with `run_plan write`, pushed, and he is told the limits
  and the total across the suites.
- What limits how many suites work at once is at the foot of GROUPS.md (one builder for one chain of files; one
  writer into the real graph at a time; run numbers from the main session only; no build on a group that waits on
  his go).
- Ticket 45 at the end: the Pocock `code-review` skill, two readers who built none of it.

## Set up before anything else

- The session's branches are cut from an old tip. Put them on top of the heads in the table below before working.
- markets-data must hold its WHOLE history before any command that writes into the graph, and so must Markets
  before a graph write names one of its files. The graph's store refuses a write from a working copy that holds
  uncommitted code: write from a clean copy. NOTHING WAS WRITTEN INTO THE REAL GRAPH in the twenty-fifth session.
- paper-trading-platform: THIS SESSION WAS NOT IN IT (he asked). `add_repo` with push access was REFUSED; it
  was cloned read-only and nothing was changed there. For a session to work on the platform, the repository must
  be selected with push access WHEN THE SESSION IS STARTED (it bears on tickets 41, 42 and 43).
- A builder gets its own working copy (`git worktree add`, sparse: tools tests .claude
  research/kalshi/frankie_boss odcore root) and pushes `<its branch>:<the session's branch>`; when the push is
  refused it fetches and merges, never forces, never rebases. A reviewer gets a detached working copy at the
  pushed head.
- `tools.kgraph.extract coverage` WRITES into the graph; it is not a read.
- The disk fills from test scratch folders (`/tmp/pytest-of-root`, any `--basetemp`): delete after each run.
- A NEW SESSION CANNOT REACH THIS SESSION'S AGENTS OR THEIR LIVE TRANSCRIPTS. What is kept of each run is in git:
  its report word for word, its line in `agent-runs.jsonl`, and its transcript in
  `paper-trading-20261123/transcripts/run-NNNN.jsonl.gz` with a sidecar. The auditor reads the kept transcripts.
- The main session's own helper for recording a run was a scratch file and is gone with the session. Use the
  tools below; they are the same thing, built under tickets 18 and 19.

## The tools built this session (ALL MARKED PROPOSED; on the session's branch, not on the trunk)

Run from the Markets checkout; `<data>` is the markets-data checkout.

```
python3 -m tools.kgraph.run_plan write --data <data> --run <N> --agent <scout|builder|reviewer|frankie-performance-auditor> --model <exact model id> --task "<...>" --tickets <a,b> [--max-tool-calls K ...]
python3 -m tools.kgraph.run_plan brief --data <data> --run <N>          # the limits paragraph for the agent's brief
python3 -m tools.kgraph.run_plan check --data <data> --run <N>          # each limit against what the run reached
python3 -m tools.kgraph.run_record keep   --data <data> --run <N> --transcript <subagents folder>/agent-<id>.jsonl --agent-id <id>
python3 -m tools.kgraph.run_record append --data <data> --run <N> --transcript <file> --agent-id <id> --role <role> --stage "<...>" --task "<...>" --outcome "<...>" --tokens-reported <the harness's total> [--tickets a,b] [--code-commit C] [--corrects "<what it corrects>"]
python3 -m tools.kgraph.run_record missing --data <data> [--live <subagents folder>]
python3 -m tools.kgraph.auditor_called --data <data> [--ticket NN] [--at <commit>]   # exit 1 while a run is unaudited
python3 -m tools.kgraph.defend ...        # register, challenge-brief, challenge, show (tickets 02, 03, 04)
python3 -m tools.kgraph.ingest_artifacts  # ticket 25: WRITES into the graph; not run on the real graph yet
```

The steps for one run: write its plan and push; tell him the limits; start the agent in the background and note
the agent id it is given; when it hands back, save its report word for word, `run_record append` and `keep`,
add the run to `tickets-44-20261124/TICKET_RUNS.json`, commit and push. An auditor's report begins
`# Performance auditor run N`; its run line carries `audits` (the runs) and `audit_report` (repo, path, and the
commit that holds the report, added with a correcting line after the report is committed).

BRIEFING (measured by the auditor this session, his word to fix it): the scout locates first; a builder or a
reviewer is handed exact line ranges or the diff, is told it does not search, and bundles its commands. A builder
writes the failing check FIRST. The words "the brief is the go" must be IN a builder's brief, or it stops after
showing its plan and waits (run 147 did).

CASES THE REAL RECORD DOES NOT HOLD: one separated section in each test file; each case is a real line, record
or transcript with exactly the named thing changed and a `# change:` comment; no market data and no figure is
made up. This is the main session's decision, told to him; he has not objected.

## Where things are (heads at the time of writing; check each with git before trusting it)

| Repository | Branch | Head |
| --- | --- | --- |
| Markets (code) | `ccr-659edd86-di9udt` | `74006f2` |
| markets-data (records, graph, tickets) | `ccr-659edd86-di9udt` | the commit that holds this page |
| paper-trading-platform, the change of the twenty-fourth session | `ccr-0ac78691-8zapbb` (NOT Codex's branch) | `28d4dbb` (read-only this session) |
| paper-trading-platform, Codex's branch (draft PR 5) | `codex/strategy-trades-and-mbo-capture` | fetch first |
| markets-data, Codex's rules | `codex/ng-blind-20261123` | fetch first |
| Markets, the April operator search as Codex found it (ticket 47) | `od-autoresearch/apr5-handoff` | `e65441a` |

Agent runs are recorded through 156. The next run is 157.

## Where the work stopped

NOTHING IS IN FLIGHT. Every agent of the twenty-fifth session handed back and is recorded: its report word for
word, its run line, its kept transcript (runs 107 to 156). NO TICKET IS MARKED DONE. Nothing went through the
engine or the tape. NOTHING WAS WRITTEN INTO THE REAL GRAPH. Everything named here is on GitHub.

Each worked ticket's own file ends with "State at the close of the twenty-fifth session": what was built, what
the reviewer left for the builder, what code cannot hold. Start each suite from that section, not from memory.

DO FIRST, group by group (GROUPS.md has the whole table):

0. G15, ticket 47, ADDED AT THE VERY CLOSE ON HIS WORD AND WANTED ("We absolutely want to do this"): find an
   operator for the natural gas market with the operator search. Read `47.md`. A scout located the pieces (run
   155, `scout-20261124/SCOUT_RUN_155_TICKET_47.md`). NEXT: the plan is written from those pointers (the state,
   the target, the forms searched, the guards, one feasibility piece first), the REVIEWER READS THE PLAN BEFORE
   ANY BUILDER (it touches ROOT's calculations, the tape and the leakage gate), and his word on the state and the
   target and his go with the budget are on record BEFORE ANYTHING IS CALCULATED. The April engine is a physics
   engine and is not pointed at the tape as it is: the method is what is taken. Where it stands in the order
   beside the other groups is his to say; it shares no file with them, so its suite can work beside them.

1. G01, tickets 02, 03, 01. The reviewer reads Markets `931b2b3..b12d8ef` on `tools/kgraph/defend.py` and
   `tests/agent_program/test_defend.py` (builder run 147's change, NOT READ YET) against the open list of its own
   fourth read (`reviews-20261124/REVIEW_RUN_136.md`). Then ticket 01 in the four steps written in `01.md` (the
   proposer adds `commit` to three claim files; the runs are put into the real graph; the ten claims are
   registered; the reviewer challenges each from the sealed brief). The last three write into the real graph.
2. G03, ticket 04. The builder takes the list in `04.md` (reviewer run 146). G04 (tickets 05, 06, 09) is built
   after it, from `PLAN_03b_04_05_06_v2.md`. G01, G03 and G04 are ONE chain of files: one builder at a time.
3. G05, ticket 25. The reviewer reads Markets `b245ee3..6de2e47` (builder run 130's second part, NOT READ YET).
   After that read, `ingest_artifacts` is run on the real graph (a graph write). Ticket 37 may need only a
   showing: scout run 152 found the code that already writes rule versions into the experiment record.
4. G08, tickets 18 and 19. The builder takes the lists in `18.md` and `19.md`. The main session's own part of
   ticket 19: the run lines of 107 to 154 were written by a scratch helper and lack fields (`started_at` on all,
   `model_replies` on 109 to 121, `agent_id` on most); put them right with `run_record append --corrects`
   from the kept transcripts; `run_record missing` lists each.
5. G09, ticket 03b: see the line below on the check at this close. Tickets 12, 13, 14 are shown by how the runs
   were made this session (scout first, the builder's change shown as a PROPOSED commit, the reviewer reading
   every change) and are not written up in their files yet.
6. G11: ticket 31 has its pointers (scout run 151) and needs a builder; ticket 21 has its pointers (scout run
   150) and needs the reviewer; 44, 46, 27 and 30 are not started.
7. G07, ticket 38, is OPEN and matters to him ("all of the data depth"): 418 of 458 columns of the daily sheets
   are not given to a decider. Not touched this session. Its ticket file has the five open points.

STILL NOT READ BY THE REVIEWER, from the twenty-fourth session: Markets `e55da89..2ac873f` (the packet), `7672c8d`
(afterwards), `6fdd4e1..1e9a7c5` (the loop on the decider program), `9054a00`, `1d0a6dc` (the deciders' door),
`04f4378` (the first decider), `53d46c9` (the context builder), and the platform's `28d4dbb`.

THE CHECK AT THIS CLOSE (ticket 03b, the one ticket marked done): at markets-data `9a8f404`, from Markets `74006f2`,
`python3 -m tools.kgraph.auditor_called --data <markets-data> --at 9a8f404` exited 0, no run unaudited:
`COUNTS runs=154 not_audited=0 record_only=106 with_own_row=40 outside_roster=26 auditor_runs=8 no_report=0 plan_no_line=0`
Run it again before any box is marked and at the close of every session.
WHAT THE AUDITOR'S LAST TWO REPORTS LEAVE FOR THE MAIN SESSION (`audits-20261124/AUDIT_RUN_153.md`, `AUDIT_RUN_154.md`):
a run that is sent back keeps ONE plan, and its wall clock from first line to last then holds the waits for the
main session (builders 128, 129 and 131 passed their limit only on that span; builder 130 passed it on its own
working time too, 2,943 seconds against 2,400, waiting on its own put-back loops); and no plan says whether a
send-back is a retry. Settle both in the plan's own words before the suites start (a limit for each part, or a
new plan for each part).

- Agent runs 99 to 154 are NOT loaded into the graph (`ingest_agent_runs`, from committed code, a graph write).
- The stored planes of ROOT are on the markets-data branch `root-rows-20231002`; the packet reads them from a git
  dir named by `MARKETS_PLANES_GIT` (a blobless mirror of that branch; it is not kept anywhere).
- Markets printed "Repository is approaching its size quota" on a push this session.
- THE OPERATOR SEARCH (his words run from "Only consider it if it can fill gaps. This isn't a directive" to, at
  the very close, "That may find an operator for the ng market!! We absolutely want to do this. Proceed"): it is
  ticket 47 and item 0 above. The April files Codex found are on GitHub: Markets branch
  `od-autoresearch/apr5-handoff`, commit `e65441a` (seven files, no data, no history shared with the trunk; left
  as Codex pushed it). The whole trail (what was read, what the April loop has that the stage 3 loop's control
  file does not name, what goes against his rules and is not taken) is at the end of the decisions file.
- The decisions file grew this session: read it from the line "FOUR AGENTS" of the twenty-fifth session to its
  end as well as from line 7196; it is not in the graph.

## Waiting on him (nothing here is started without his word)

- Tickets 07 and 08: the reads into the graph, their budget told then (sizes of the rule documents are in the
  decisions file and in scout run 117's report).
- Tickets 10, 22, 24, 28, 33, 34, 35, 40: his go, each with its budget. Tickets 15, 16, 17, 29, 36, 42: his
  decision. Ticket 27 is a model run: its budget is told first.
- His, if he chooses: an objection to the scratch-case convention above; whether one auditor run for a batch of
  runs is what he wants (it is how it was done: each run its own block); the ten placements in GROUPS.md.
- How a confidence is given after validation is answered by no plan; the main session's plan is in
  `tickets-44-20261124/PLAN_03b_04_05_06_v2.md` (the section Confidence): his own words recorded by a command, no
  agent states a confidence, nothing is removed for low confidence ("Everything stays as a possibility").

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

ADDED IN THE TWENTY-FIFTH SESSION (each is his word, in the decisions file):
- THERE ARE FOUR KINDS OF AGENT and the performance auditor is called on EVERY run of the other three, each run
  its own row (ticket 03b). No general agents.
- MORE BUILDERS AT ONCE, on files that do not overlap; and a full suite of the four kinds on each ticket group.
- "Do whatever our plan says": ask him only what the plans leave to him by name.
- "Everything stays as a possibility. it's a matter of 0 confidence or highly confident": a claim is contested
  and validated, then carries a confidence; no verdict words, no pass or fail.
- The zip's files are kept in git and read every session until he says the agents part is done.

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

## Slips of the twenty-fifth session, so they are not made again

- Asked him questions the zip answers. Used three kinds of agent until he said there are four. Ran two general
  agents with a role's file before the four agent types had loaded.
- Told builders and reviewers to read whole files; the auditor measured the cost.
- Sent a builder a brief without the words that it may write; it stopped and waited.
- Two builders at once changed things the other's checks read (CLAUDE.md lines a claim file cites): a cited
  ground now names its commit.
- Wrote outcome texts with counts that did not match the run's own figures (runs 136 and 145: the auditor named
  them). Dropped the harness's total from two correcting lines. Take the counts from the tool, not from memory.
