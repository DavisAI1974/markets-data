# Item 17 of the paper platform checklist: where the agents' execution plan stands (2026-11-24)

Codex's item 17 (paper-trading-platform, branch `codex/strategy-trades-and-mbo-capture`, draft PR 5): a plan file
under `paper_platform/execution_plans/` holding the tape's contract, its Databento instrument ID, and a placement and
size choice for each rule from the agents. Greg's decision, as the checklist records it: "Paper orders can post a bid
or offer, lift an offer or hit a bid. Frankie and the agents choose placement and size for each strategy."

## In hand

- The instrument ID: 150611 in every record of all seven tape files (read from the files).
- The contract definition: NGX3, converted from the stored exchange definition record by NautilusTrader 1.231.0's
  own loader. `ngx3-nautilus-definitions.json` here holds the conversion of each stored definition file; they are the
  same apart from `ts_event` and `ts_init`. The record on Codex's branch
  (`paper_platform/execution_plans/NG_OCT2023_CONTRACT.md`) uses the Sunday start-up record of 2023-10-01.
- Two things read from the matcher's code that a manager's entry depends on (in that same record).
- The briefs for two decider agents, one for each rule family: `BRIEF_COMMON.md`, `BRIEF_CL.md`, `BRIEF_CX.md`.

## Not in hand

- No choice from any agent. The two decider runs (41 for CL01 to CL15, 42 for CX01 to CX15) were stopped by Greg's
  message at the session change before either wrote an answer. No answer file exists.
- Frankie's choices, for all 30 rules: launch is on HOLD and needs Greg's go.
- So no plan file exists, and item 17 stays open.

## To pick it up

1. The briefs name files in the session's scratch folder that is gone. Before a decider is run again: check out
   Codex's branch, and write the two authors' strategy documents to a folder the decider can read
   (Claude's `strategy-20261123-claude/VERSIONS.md` and `OPEN_QUESTIONS.md` at markets-data `46199c5f`, Codex's
   `strategy-20261123-codex/VERSIONS.md` and `OPEN_QUESTIONS.md` at markets-data `ad109214`), then put those paths
   and the answer path in place of the scratch paths in the three briefs.
2. Run one decider for each family. Check every quote in an answer against its file word for word, by code.
3. Build the plan file from the answers by code (only the keys the matcher reads: `instrument`,
   `databento_instrument_id` as the integer 150611, `rules`). A rule with no decision stays out of `rules` and is
   listed by rule ID under item 17. Keep who decided and why in a file beside the plan.
4. A plan is never edited once a run has used it: a change is a new file.
5. Codex's handoff says this pass is build only: no checks, validation or tests on that branch, and no paper session
   without Greg's go.

## Codex's branch moved while this was written

Codex pushed five more commits (to `5216aa0`) before the record went up; they were merged, not rebased, and the
record is on the branch after them. His changes to `paper_execution.py` are about the run stop (a failed cancel, the
orders still working, the errors kept in the receipt). What `post`, `cross` and `cross_limit` do is unchanged, read
from the diff. The line numbers the briefs give for `paper_execution.py` have moved: read them again before a decider
is run.
