# Handoff T, end of the seventeenth session (2026-11-23)

Branch: `ccr-349e2ffe-07p8od` in `DavisAI1974/markets-data` for data and documents. This file replaces handoff S as
the starting point. Every decision of this session, with Greg's words, is in
`root-redesign-20261116/ROOT_GAMEPLAN_DECISIONS.md`, section "Seventeenth session" and the entries after it (the
last entries are the newest). Desktop writes to the same branch: fetch before every push.

**Read first, in this order:**
1. This file, in full.
2. `RESEARCH_PAPER_20261123.md` (beside this file): the new research paper. Its counts were read from all four
   trade days.
3. `root-redesign-20261116/peak-research-20261117/TRADE_LIFECYCLE_NOTES.md`: the running notes. ADD to it; never
   start another. Its sections dated 2026-11-23 govern.
4. The decisions file, from "Seventeenth session" to the end of the session entries. AND, before touching any
   Excel file, its entries on the workbook (search "workbook", "parts", "daily sheets", "short stretch") and
   `root-redesign-20261116/WORKBOOK_README_PAGE.md`.
5. `root-redesign-20261116/FURTHER_RESEARCH_LIST.md`: research set aside for later. Not this session's work.

## THE OLD RESEARCH AND STRATEGY DOCUMENTS OF EARLIER SESSIONS ARE NOT TO BE USED (his word)

"Just make a note that old research and strategy docs from previous sessions are not to be used. We should actually
discard those if they have old data."
- NOT USED: every research report, finding, case set, strategy list, candidate, review, gap list and paper rule made
  before the rebuild of 2026-11-16, and Claude's own strategy work of last week ("just don't use what you built
  after"). The one research paper is `RESEARCH_PAPER_20261123.md`. The research QUESTIONS are in
  `root-audit-20261116/RESEARCH_INTENTIONS.md`.
- THE DISCARD IS NOT DONE. It needs the list by name in front of him and his word "delete" (the way it was done on
  2026-11-16). What is known by name only, nothing opened: on `main`,
  `tasks/family-research-20261022/claude-independent-research-20261113/` (246 files), `paper-rules/20261109/` (128)
  and `carry-forward/20261109/` (27), with `claude-code-cases`, `claude-code-derived`, `claude-code-pins` and
  `replay-artifacts` beside them; and 13 `codex/` branches. Removing from `main` or from a `codex/` branch needs his
  explicit word for that branch; the session could not delete a branch on 2026-11-16 (GitHub answered 403).
- A search of Claude's sessions of 2026-11-08 and 09 for Codex's original strategy doc was started this session and
  is not needed any more: nothing of it is used.

## FIRST: THE STRATEGY STEP (his word: "Let's start new session for this")

- TWO SESSIONS IN PARALLEL: Codex and Claude, 15 strategies each. NEITHER CONSULTS THE OTHER'S WORK UNTIL EVERYTHING
  IS FINISHED. Claude opens no `codex/` branch and no folder `strategy-20261123-codex/`, lists none, searches none.
- Codex's handoff is `STRATEGY_HANDOFF_FOR_CODEX_20261123.md` (beside this file). Claude's task is the same.
- Claude's first message: how a version is formed blind to its own trade day (which trade days each version is
  formed on, which it is tried on, and what had already been seen of each: the notes, the research paper and this
  session's counts were read from all four). Then 15 versions in one message. A later trade day may know what was
  found on an earlier one.
- He was told before it starts so he can raise the effort setting. He has not said start in this session.
- Claude's strategy work goes under `strategy-20261123-claude/` beside this file.
- WHAT FEEDS IT (Claude's reading of his rulings, put to him, not corrected): IN: the rows; the calculations with
  no window (`quote_runs`, `book_totals`, `refills`, `sweeps`, `together`, the trade legs, the peaks with no
  window, `resting`, `move_steps`); the natural gas dipole line, exhaustion line and humps; the research tables.
  OUT: the 20-second peak family; Native's dipole record; the crypto and ng program's own trades and prices; the
  mid price; crypto data; the old research and strategy documents. NOT YET FOR STRATEGY: the information measure.

## What he decided this session (do not re-ask)

- ONLY ADD TO WHAT EXISTS. DO NOT REBUILD IT. "Why are you rebuilding things that are already there? Just update
  what already exists." A new result goes in as columns on what is there. No file or layout is replaced without
  his word.
- THE PLAN FOR THE BIG FILES STANDS (2026-11-16 and 17): one row per tick, one sheet per trade day; the daily
  sheets are the every-tick tables on the daily branches, kept up to date by adding column files beside the rows;
  the Excel workbook is written once, at a slow time, in parts with the days broken up (`root/sheet.py`). Read the
  plan before any Excel work.
- NO MORE TESTS of the output's correctness on this data. A job's own checks and the compare of each fetched file
  with its receipt stay.
- A STORED VALUE IS READ AT A TICK BY ITS PLACE ON THE TAPE, never by time alone.
- THE CODEX MEASURE IS USED NOW where it is marked (the ratio is made by the division where all trading is on one
  side). The comparison of its operator with the original equations is on the research list.
- THE FURTHER RESEARCH IS SAVED FOR LATER. The list is kept so nothing is forgotten.
- THE WRONG VERSIONS ARE DELETED and no history of them is wanted. Not done: rewriting git history (a forced push
  on branches Desktop shares): only on his explicit word.
- `ROOT_dipoles_pinned.xlsx` is back byte for byte as it stood at the start of the session (`4262074`).

## What exists now

**Code:** Markets `ccr-dd95052b-3vcrwq`, `a556589` (this session's own branch; nothing on the trunk). New:
`root/research_threads.py` (reads by place), `root/research_trace.py`, `root/info_measure.py`,
`root/research_columns.py`, `root/research_excel.py` (its look-ups are used by `research_columns`; its sheet
writer made the removed sheets). The pod runner takes several programs in one launch.

**Stored:** `root-rows-20231002` `360fdaa`, `-20231003` `c8a0b75`, `-20231017` `733442a`, `-20231018` `1bd670e`.
New on each: `research-threads/` (one line per move, one per hump; made again by place), `research-trace/`,
`info-measure/`, and `calc-research_columns-<trade day>-part*.parquet` beside the rows (327 columns: exhaustion,
dipole and the measure at every tick; each move and hump on its tick). Everything else as handoff S lists it.

**Documents (this branch):** `RESEARCH_PAPER_20261123.md`, `STRATEGY_HANDOFF_FOR_CODEX_20261123.md`,
`root-redesign-20261116/FURTHER_RESEARCH_LIST.md`, the decisions and the notes.

## Open with him, each put once

1. The discard of the old research and strategy documents (above): the list by name, then his "delete".
2. `root/research_excel.py` still holds the code that wrote the removed "moves" and "humps" sheets. His to strike.
3. The Excel workbook in parts: at his word, by the plan, with the research columns in it.
4. Rewriting git history to take the wrong versions out: only on his explicit word.
5. `DavisAI1974/Basic_equations` is not attached to the session (the session refused to attach it); the operator's
   deep dive needs it.
6. Carried from handoff S, items 1 to 3 and 5 to 9 there (the mid price's change per tick in the pictures; the 40
   pictures; the program's trades as observation only; the every-tick workbooks; the byte-for-byte proof, now
   ruled out by "no more tests"; Desktop's report; the stale receipts; Native's two hours).

## How a launch goes (five pods this session, every run passed first time)

- NO POD STARTS UNTIL HE HAS TYPED THE WORD "go" AFTER THE PRICE IS ON HIS SCREEN. A conditional go ("After you read
  then go"; "Go if we're sure") was taken once its condition was met and said to him. He can stop a start; then
  the word is needed again.
- Environment "Markets", limited network: every new pod address needs his approval card. THE LAST POD'S ADDRESS IS
  STILL ALLOWED AND MUST COME OFF IN THE NEXT CARD: `sg5jzl7k7kp5ud-8000.proxy.runpod.net`.
- General Purpose `cpu3g`, 8 CPUs, $0.32 an hour; United States `dataCenterIds`; image `python:3.12`; port
  `8000/http`; entrypoint `/bin/bash -c`; `disk` 20. The command clones the code branch with
  `sparse-checkout set root crypto_ng odcore`, then
  `DAYS='...' bash code/root/pod_leg_renders.sh <FULL 40-character commit> <program[,program]>`, then
  `sleep infinity`. Check the commit in the command before sending it.
- The daily branches: one shallow clone each, sparse, files by name. NEVER list one with file sizes.
- BEFORE A LAUNCH read a new job's receipt against `root/pod_fetch.py` (it once stopped on a new layout).
- Store, push, confirm each push, THEN delete the pod and read the account. Write the pod's times from the clock.
- After ANY restart of the session, read the account first.
- The session's container needs `pip install pyarrow==26.0.1` before it can read a stored table.

## Slips of this session, so they are not made again

- "Read the last 2 sessions" was taken as the written record; he meant the chats. They can be read through the
  session list.
- The workbook plan was not read before Excel work: new sheets, then a rebuilt layout, then every tick laid out as
  a new thing. He had to stop it three times.
- A stored line was read by time; several trades share a nanosecond. Found by the handoff's own second check.
- "Trade legs read the same way" and "the humps sheets can be written now" were said without support and withdrawn.
- A table of how many values a fault had touched was read by him as a finding: say what a table is in its title.
- Long answers. He reads on a phone: the answer in the first lines.

## TO REVISIT (Greg: carry into every handoff until done)

Native's record is built on predetermined windows (a 20-second roll, a level set from 85 in 100 seconds, 60-second
horizons, a 45-second spacing and a 50-second wait before a dipole is made known), which his "no predetermined
windows" rule does not allow for our own work. He chose to keep Native as it was made for now. Not used this
session.
