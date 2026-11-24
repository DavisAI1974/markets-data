# Handoff X, after the close of the twentieth session (2026-11-23, about 9:30 pm Eastern)

Branch: `ccr-349e2ffe-07p8od` in `DavisAI1974/markets-data`. This file replaces handoff W as the starting point.
Handoff W stays as the record of the paper runner; nothing in it is withdrawn except its "next" list, which this
file replaces. Desktop and Codex write to this branch too: fetch before every push.

**THE DIRECTION (Greg, 2026-11-24): "We need to finish building everything for the agents before we do any more paper
trading"; "Say to finish all the steps".** So the next session builds ALL the steps of the agent program that are
not built yet, in the plan's order, and does not stop after one of them. NO PAPER RUN until they are finished.

**Read first, in this order:**
1. This file, in full.
2. The plan: Markets `research/kalshi/frankie_boss/CLAUDE_ARCH_PLAN_GRAPH_ENGINEERING_ADOPTION_20261123.md` (233
   lines; stages 1 to 8), and beside it `README_HANDOFF_20261123.md` and `CODEX_PROMPT_AMENDMENTS_20261123.md`.
3. The decisions file `root-redesign-20261116/ROOT_GAMEPLAN_DECISIONS.md`, section "Twentieth session", the last
   ten entries.
4. Handoff W (`NEXT_SESSION_HANDOFF_20261124W.md`), only its sections "WHERE THINGS STAND", "THE RUNS" and "THE
   AGENTS": the paper record that stages 2 and 4 have to take in.
5. The list of gaps and misses: `tasty/RUNNING_LIST.md` in `DavisAI1974/paper-trading-platform`, branch
   `claude/tasty-runner`.

## WHAT "EVERYTHING FOR THE AGENTS" IS, AND WHERE EACH STEP STANDS

| Stage of the plan | What it is | Stands |
|---|---|---|
| 1. The four agents | scout (Haiku), builder (Sonnet), reviewer (Opus), frankie-performance-auditor (Sonnet) | BUILT. One item of it NOT done: the plan says to retire `.claude/agents/aws-*.md` and the `aws-mcp` entry in `.mcp.json`; both are still there. Removing files goes to Greg first. |
| 2. The experiment record | every trial a line with its parent, run, change, figures and status; `tools/exp_dag.py` in Markets; one SQLite file in markets-data `experiments/` | NOT BUILT |
| 3. The keep-if-better loop | a control file for each loop; every trial pushed to stage 2, the reverted and the crashed too | NOT BUILT. Which figure each loop goes by is Greg's; the harness is built so it does not wait on that. |
| 4a. The knowledge graph's layout | what a claim, a source, a run and a link look like; lines in markets-data `graph/nodes/` and `graph/edges/` | NOT BUILT. markets-data has no `graph/` folder. |
| 4b. Filling the graph | calc outputs and manifests with no model; the scout turning the handoffs, kickoffs and research notes into claims tied to their source; then merging names that mean one thing | NOT BUILT |
| 4c. The grounding check | the reviewer checks a claim against the graph and says what evidence is missing | NOT BUILT (the reviewer's definition already names it) |
| 5a. A session starts from the graph | a context builder in place of the pile of handoffs. THIS IS WHAT GREG ASKED ABOUT: "convert the handoffs into graphs so theere isn't so much to read" | NOT BUILT |
| 5b. Frankie's packet from the graph | a new input path beside `stacked_v1`, run side by side | NOT BUILT. Built beside the old one; switched only on Greg's go. |
| 6. The swarm | one Haiku worker for each dipole event, a reducer, a refute wave | NOT BUILT |
| 7. Paper trading | the runner on the tastytrade sandbox | BUILT AND RUN (handoff W). On hold now. 7d (each order and fill linked in the graph) and 7f (the loop and the grounding check on rule versions) waited for stages 2 and 4 and are NOT BUILT. |
| 8. The token test | can Claude agents carry Granite's daily load: every Granite call of one trade day, replayed through five arms | NOT BUILT |

The plan's own order: 2 and 4a together, then 4b, then 3, then 5a, then 5b and 6. Then 7d and 7f, then 8.

## STEP 0, BEFORE ANYTHING IS BUILT

- Bring Markets `ccr-532eaea6-vgz20z` (`65f71a9`) onto the session's own branch first: that is what makes the agent
  types `scout`, `builder` and `reviewer` available. They were not there at the start of the twentieth session.
- Read the plan. Say to Greg in a few lines which steps the session will build and in what order, and declare the
  budget for each agent run before it starts.
- Have the scout locate what stage 4b and stage 6 read (the calc outputs and manifests, the handoff and kickoff
  files, the dipole events' stored layers, the Granite receipts for stage 8). If something a stage needs is not
  reachable without AWS, say so at once: AWS is off limits.

## WHAT IS BUILT FREELY AND WHAT WAITS FOR HIS GO

BUILT WITHOUT ASKING AGAIN (code, checks on real records, records written to markets-data): stages 2, 3, 4a, 4b,
4c, 5a, the code of 5b, the code of 6, 7d, 7f and the code of 8.

STILL NEEDS HIS GO, each said to him first with its budget, because the standing rules were not lifted:
- anything that launches or changes Frankie, Granite or a pod (launch is HOLD);
- switching Frankie's input to the graph-built packet (5b);
- a run of the swarm (6) and a run of the token test (8): both spend model tokens at scale;
- dispatching a loop on the GitHub runner or a pod (3);
- any paper run (7);
- deleting any file already saved (the `aws-*` agent files of stage 1 included);
- anything onto the Markets trunk. Each stage lands on a branch for Codex's review; nothing is merged without Greg.

## WHERE THINGS GO

- Code of the agent program: Markets, on the session's own branch (the plan names `tools/exp_dag.py`). Markets is
  near its GitHub size limit: code only, no output.
- Outputs: markets-data only: `graph/`, `experiments/`, each with a `MANIFEST.json` entry.
- The first things to load into stages 2 and 4, already on this branch: `paper-trading-20261123/agent-runs.jsonl`
  (13 agent runs, each with its model and tokens), the three run folders in `paper-trading-20261123/live-runs/`,
  the `NEXT_SESSION_HANDOFF_*.md` files and the decisions file.
- Paper runner code: `DavisAI1974/paper-trading-platform`, `claude/tasty-runner` (`e077b2e`). Not worked on this
  session except where 7d and 7f read its records. Codex's `main` there is not touched until Greg says he is done.

## THE RULES THAT BEAR ON THE BUILD

No made-up data, not even to check code: a check reads real records or is skipped. No averaging, pooling, ranking
or labels; each trial, claim and trade is its own line. A reverted or cut item stays written down with its status
(the plan's overrule allows the loop's reverts and the reducer's cutoffs; it does not allow losing them). Every
claim has a source or is marked as an inference. A trade day is 6 pm Eastern the evening before to 5 pm Eastern on
the named date. No mid price, no trade cost. AWS is off limits. Plain words, the answer in the first lines. His
decisions recorded in git as they are made.

## THE AGENTS AND BUDGETS

Left from the twentieth session: builder 102,225 of 300,000; reviewer 187,551 of 250,000; no scout budget was
declared. The next session's budgets are Greg's to declare. A run's tokens are read from the notice the harness
sends when it returns, and written to `paper-trading-20261123/agent-runs.jsonl` (runs 1 to 13 are there) until
stage 2 gives them a home. The builder's definition says to show a diff and wait and never to run against market
data: a brief has to say which of those are lifted and why, or the builder stalls.

## STATE LEFT BEHIND (unchanged since handoff W)

- The paper runner: 32 strategies, 26 checks passing, three run records, none scored. Runs are ledger-only when
  they resume (Greg: "We can just observe on ledger"). The runner makes no pictures and no graph links (list C24).
- The sandbox account 5WY79188 is short 13 lots of /NGF7 and is left as it is; sandbox-only issues are parked.
- Richer data is coming; nothing more is built around the thin feed.
- Keys: the three sandbox values are in `paper-trading-20261123/tasty-sandbox.env`. They are not needed while no
  paper run is made.

## OPEN WITH GREG, EACH PUT ONCE (none holds the build up)

1. From the plan: the figure each loop goes by (stage 3); whether Granite takes the grounding check for Frankie's
   own claims (stage 4c); where this sits beside the fresh-run family step.
2. Carried from handoff W: the exit indications of Codex's management rules; whether Codex writes a strategy for
   the print with no side; whether the fifteen read the quote a no-side print carries; Codex's wording not carried;
   and handoff V's and U's lists.

## SLIPS, SO THEY ARE NOT MADE AGAIN (the twentieth session's are in handoff W)

- Claude wrote handoff W as prose and closed the session without saying that the handoff-to-graph step of the agent
  program had never been built. Greg had to ask. When a plan has filed stages, say at the start of a session which
  are built and which are not.

## TO REVISIT (Greg: carry into every handoff until done)

Native's record is built on predetermined windows (a 20-second roll, a level set from 85 in 100 seconds, 60-second
horizons, a 45-second spacing and a 50-second wait before a dipole is made known), which his "no predetermined
windows" rule does not allow for our own work. He chose to keep Native as it was made for now.
