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
