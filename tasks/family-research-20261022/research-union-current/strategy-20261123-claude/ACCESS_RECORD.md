# Access record (Claude, strategy step, 2026-11-23, eighteenth session)

What was opened and verified, what was not opened, and what was visible of the earlier strategy material and of
Codex's work.

## Opened and read

**Documents, `DavisAI1974/markets-data` branch `ccr-349e2ffe-07p8od` (fetched at `07f6767`), under
`tasks/family-research-20261022/research-union-current/`:**
- `NEXT_SESSION_HANDOFF_20261123T.md`, `RESEARCH_PAPER_20261123.md`, `STRATEGY_HANDOFF_FOR_CODEX_20261123.md` (the
  shared task): in full.
- `root-redesign-20261116/peak-research-20261117/TRADE_LIFECYCLE_NOTES.md`: in full.
- `root-redesign-20261116/ROOT_GAMEPLAN_DECISIONS.md`: from "Seventeenth session" to the end.
- `root-audit-20261116/RESEARCH_INTENTIONS.md` and `root-redesign-20261116/FURTHER_RESEARCH_LIST.md`: in full.
- `root-redesign-20261116/peak-research-20261117/HOW_A_LEVEL_EMPTIED.json` and `ATTRIBUTES_BY_PILE.json`: read by
  the script that copied counts into `EVIDENCE.md` (of the second, the lines of the peak with no window only).
  `TWO_KINDS_OF_PEAK.json`: its first lines were printed to see its shape; it holds counts of the 20-second peaks,
  which are not used.
- The names of the files and folders of `research-union-current/`, `root-redesign-20261116/` and
  `root-audit-20261116/` were listed once, at the start.

**The daily branches (each its own shallow copy, files added by name, no table fetched):**
- `root-rows-20231002` (`360fdaa`): the names of its files (no sizes); `FILES.md` in full; `RECEIPT.json`; the
  receipts `CALC-quote_runs`, `CALC-book_totals`, `CALC-refills`, `CALC-sweeps`, `CALC-together`,
  `CALC-turn_peaks`, `CALC-leg_peaks`, `CALC-resting`, `CALC-move_steps`; `crypto-ng-tick/CRYPTO-NG-TICK-20231002.json`;
  `research-threads/RESEARCH-THREADS-20231002.json` and its count file. Fetched and not opened:
  `CALC-research_columns-20231002.json`, `TRADE-LEGS-20231002.json`.
- `root-rows-20231003` (`c8a0b75`), `-20231017` (`733442a`), `-20231018` (`1bd670e`): the research threads receipt,
  the receipts of `refills`, `sweeps`, `quote_runs`, `together`, `turn_peaks` and `leg_peaks`, and the crypto and ng
  receipt. For the column lists only the receipts of trade day Oct 2 were read; the receipt of every trade day
  holds the same 36 count tables (checked).

**Code, `DavisAI1974/Markets` `ccr-dd95052b-3vcrwq` (`a556589`), brought into the session's branch
`ccr-fffbc766-a1gxpl`:** `root/rows.py` (the list of every-tick fields), `root/calcs/quote_runs.py` and
`root/calcs/move_steps.py` in full; the written rule at the top of `resting`, `sweeps`, `together`, `refills`,
`turn_peaks`, `leg_peaks`, `book_totals` and `root/trade_legs.py`; the lines of `root/research_threads.py` that word
"every order filled" and the same exchange event.

**Also:** the agent skills router and the git workflow skill (addyosmani/agent-skills, tag 0.6.8, read from the
public source); the Runpod skills; the Runpod account (no pod exists; the balance was $31.30).

## Verified, and how

- Each daily branch's tip is the commit handoff T names.
- Every count in `EVIDENCE.md` and `EVIDENCE_COUNTS.md` was copied by script from the receipt or count file named
  there; the fingerprint of each research receipt is in `EVIDENCE_COUNTS.md`.
- To word a sentence such as "in seven of the eight rows", pairs of stored counts were set against each other by
  hand. No figure made that way is stored.
- NOT DONE: no stored table of market data was opened, no line of a table was read, nothing was calculated on the
  tape, no version was tried. No pod was started.

## Not opened, not listed, not searched

- Any `codex/` branch. Any folder `strategy-20261123-codex/`. WHAT WAS SEEN OF CODEX'S WORK before the v2 rules
  were pushed: only the handoff note Greg pasted into the session (its branch `codex/ng-blind-20261123`, its
  commit `ad10921`, the names of its files, and that it holds fifteen v2 paper-trading rules with their triggers,
  direction, management, exits and resets). None of its strategies. The v1 proposals and the v2 rules of this
  folder were both written and pushed before that folder was opened, and are not changed by it (Greg: "Don't
  change your strategys based on codex").
- AFTER the v2 rules stood on the remote (`bc8c6c1`): Codex's `VERSIONS.md` (its fifteen v2 sections) and
  `OPEN_QUESTIONS.md` were read, from `codex/ng-blind-20261123` at `ad10921`, to lay out the paper-trading steps
  for all thirty. Nothing in this folder's rules was changed after reading them.
- The old research and strategy documents of earlier sessions (on `main` and elsewhere), Claude's own strategy
  work of last week included. This session has no memory of them.
- The stored tables of the information measure, Native's record, the crypto and ng program's trades and turns,
  and every parquet file.
- AWS (an AWS tool is attached to the session; it was not called).

## Visible without being opened, said plainly

- `RESEARCH_INTENTIONS.md` is the list of research QUESTIONS and it names, with no result, the situations of the
  earlier strategy lists (Codex's of 2026-11-13 and Claude's seven paper strategies). Those names were seen. The
  fifteen versions here were formed from the paper, the running notes and the stored column lists. Where one of
  them carries a like idea (following a move, a defended level, a step back and a return), it is kept on its own
  merits; no rule, value or setting of the earlier lists was available or used.
- The running notes and the decisions file also hold counts that stand on the 20-second peak family and on
  Native's record, and by-eye readings of the crypto and ng program's trades. Read; not used as an input. The one
  place a by-eye reading of a program trade is mentioned is marked as such.
