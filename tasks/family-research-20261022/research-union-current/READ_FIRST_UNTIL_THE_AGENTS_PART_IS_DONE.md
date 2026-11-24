# Read first, every session, until the agents part is done (Greg, 2026-11-24)

Greg sent the zip `frankie_handoff_20261123_2.zip` again in the twenty-fifth session (sha256
`3da59107ddad6b71b4ff7f58212fa46dd1e447d1c2a02f37af192f6317f539bd`, 8 files) with: "Please put tjese files in
your local memory until we are finished with this part", and then: "Not this session but your claude local mem
through many sessions until we are done with the agents part".

What is so: a cloud session has no memory of its own that outlasts it; its machine is given back when it ends.
The only thing every later session can read is git. So this page is that memory. Every session reads the eight
files below IN FULL before it does anything on the agents part (the 46 tickets), and keeps doing so until Greg
says the agents part is done. This page is named on every start page until then. It is taken away only on his word.

## The eight files, and where each one is in git

Checked byte for byte against the zip on 2026-11-24 (Markets `2ac873f`).

| File in the zip | In git | Against the zip |
|---|---|---|
| `CLAUDE_ARCH_PLAN_GRAPH_ENGINEERING_ADOPTION_20261123.md` (the plan, stages 1 to 8) | Markets `research/kalshi/frankie_boss/` | the same bytes |
| `README_HANDOFF_20261123.md` (the handoff index) | Markets `research/kalshi/frankie_boss/` | the same bytes |
| `CODEX_PROMPT_AMENDMENTS_20261123.md` (one system with Codex's verifier; "Four agents in total; no more") | Markets `research/kalshi/frankie_boss/` | the same bytes |
| `CLAUDE.md.patch` (the Agent roles section) | Markets `CLAUDE.md`, section "Agent roles (Greg, 2026-11-23)" | applied on the working branch; NOT in a session's own copy when it is cut from the old tip |
| `.claude/agents/scout.md` | Markets `.claude/agents/scout.md` | the zip's text plus 5 lines added later (the brief made by code, stage 4b) |
| `.claude/agents/builder.md` | Markets `.claude/agents/builder.md` | the same bytes |
| `.claude/agents/reviewer.md` | Markets `.claude/agents/reviewer.md` | the zip's text plus 5 lines added later (the grounding check as built, stage 4c) |
| `.claude/agents/frankie-performance-auditor.md` | Markets `.claude/agents/frankie-performance-auditor.md` | the same bytes |

Also read with them, because the zip names it: Markets `research/kalshi/FRANKIE_INDEPENDENT_SCIENTIFIC_VERIFIER_PLAN.md`.

## THERE ARE FOUR AGENTS (Greg, 2026-11-24: "Isn't there 4 agents??"; "There's 4 agents!")

scout (Haiku), builder (Sonnet), reviewer (Opus), frankie-performance-auditor (Sonnet). The main session routes
work to all four; none is left out of a batch of tickets without saying why. The amendments: "Four agents in
total; no more."

## A trap that cost time (twenty-fifth session)

A session is cut from an old tip, so it loads its agent list before the four agent files exist: the types
`scout`, `builder`, `reviewer` and `frankie-performance-auditor` are refused by name at first. Put the session's
Markets branch on the working head first; the types load by name a few minutes later. Do not start a general
agent in a role's place.

## THE AUDITOR IS CALLED ON EVERY RUN OF THE OTHER THREE (Greg, 2026-11-24; ticket 03b)

"The per aud should have been called every run that we've done with the other 3 agents and hasn't been until
now." Every run of the scout, the builder and the reviewer is audited by the performance auditor, each run its
own row, against the limits told to Greg before it started. Through run 110 it was called on none. The check
that holds this is ticket 03b (`paper-trading-20261123/tickets-44-20261124/03b.md`); until it is built, the
main session calls the auditor on each batch's runs before any box of that batch is marked.

## ADDED LATER ON 2026-11-24 (the reviewer's read of ticket 03b, agent run 123): what is so now

- The check exists: from the Markets checkout, `MARKETS_DATA=<markets-data> python3 -m tools.kgraph.auditor_called`
  lists every run that no auditor's report has its own row for and ends with a failing exit code while any is
  listed; `--ticket NN` does the same for the runs that worked on one ticket (`paper-trading-20261123/
  tickets-44-20261124/TICKET_RUNS.json`). It is built and read once; its ticket is not marked.
- A TICKET'S BOX IS NOT MARKED WHILE A RUN THAT WORKED ON IT IS UNAUDITED. The command is run before any box is
  marked and at the close of every session. Nothing runs it by itself: the main session does.
- THE AUDITOR'S REPORT FOR EACH OF ITS RUNS IS KEPT IN GIT WORD FOR WORD (`paper-trading-20261123/
  audits-20261124/`), and each sub-agent's own transcript is kept in `paper-trading-20261123/transcripts/`, so a
  later session can check a run's line and its report against what the agent actually did.
- THE TABLE ABOVE, AS THE FILES STAND NOW IN MARKETS (`3a98333`): `builder.md` is the zip's text plus 1 line and
  `reviewer.md` the zip's text plus 6 lines (each gained "you do not search or read whole files to find things",
  Greg, 2026-11-24); `frankie-performance-auditor.md` is the zip's text plus a section of 18 lines, "Every run of
  the other three agents"; `scout.md` is unchanged since the table was written. Nothing of the zip's text was
  taken out of any of them.
- MORE THAN ONE BUILDER WORKS AT A TIME (Greg, 2026-11-24: "We need more builder agents working in parallel"),
  each in its own working copy on files no other builder is on.

## ADDED at the close of the twenty-fifth session: the zip's own eight files are in git, in one folder

Greg, 2026-11-24: "Make sure you have bext sess load the zip files into local memory".

`frankie_handoff_20261123_2/` (beside this page) holds the eight files exactly as they are in the zip, byte for
byte, at the zip's own paths. THE FIRST THING A SESSION DOES, before the start page's other steps and before any
ticket work: read all eight IN FULL into the session (with the Read tool, each file whole, not a search of it),
and read the verifier plan named above with them. If the session has a memory folder of its own, copy the eight
files into it as well and say so; if it has none, say that to him plainly and name this folder as where they
are kept. Two of the agent files in Markets have 5 lines added since the zip (the table above says which); this
folder holds the zip's own text.
