# Handoff, fifth session of 2026-11-16 (foundation mostly built; next: pin the 13, short sheet, then Step 1 and 2)

Branch: `ccr-349e2ffe-07p8od` in `DavisAI1974/markets-data` for data and documents. This file replaces
`NEXT_SESSION_HANDOFF_20261116D.md` as the starting point.

## Read these, in this order

1. `root-redesign-20261116/ROOT_GAMEPLAN_DECISIONS.md`: every decision in Greg's words. The section "Fifth session"
   and everything after it is new today.
2. `root-redesign-20261116/SPEC-root.md` and `SPEC-outside.md`: both approved.
3. Markets `CLAUDE.md`, "The trading rules": two rules were added today (the four trade days; Markets is code only).

## Where the ROOT code is (read this before building)

**All ROOT code is on Markets branch `claude/plugin-company-customization-z50yb3`** (not on the trunk). A new session
gets a new, empty branch. Bring the code in first:
`git fetch origin claude/plugin-company-customization-z50yb3 && git merge --no-edit FETCH_HEAD`.
Fresh container: `pip install databento pyarrow xlrd openpyxl pytest`.
Greg, 2026-11-16: ROOT code goes to Markets on its own branch; data, outputs and documents go to markets-data. Never
push data to Markets.

## What is built (all on the real tape, nothing made up)

| Part | File | State |
|---|---|---|
| calendar | `root/calendar.py` | done: trade day bounds, labels, the week, the files a trade day needs |
| outside tables | `root/outside.py` | done: all 13 as tables, storage (X11, X12) included; the street estimate is empty with its reason |
| tape | `root/tape.py` | done: reads a week, fingerprints and counts checked, what each record is; the calculation gate |
| book | `root/book.py` | done: equals the vendor restatement at all five file boundaries; adds up at every trade |
| rows | `root/rows.py` | done: one row per tick, 85 fields (sections A to E), empties stored as empty |
| store | `root/store.py` | done: rows and book pictures as Parquet parts, restatement table, receipt |
| checks | `root/checks.py` | done: every row checked, records accounted for, trade counts, playback at cuts |
| run | `root/run.py` | commands: check-week, check-book, build, playback |

Result of the one check run on rows, store and checks: see "Check results" at the end of this file.

Records already in `root-redesign-20261116/receipts/`: check-week and check-book for all four trade days.
Tables in `data/outside/ng_oct2023/made/` (18 tables, receipt, small workbook).

Measured on trade day Oct 2: 820,670 rows, 85 fields, 59 MB as stored; a book picture at each of 38,127 trade
messages, 140 MB; the whole build takes about 83 seconds in the session. All four trade days: roughly 240 MB of rows
and 560 MB of pictures. **No pods are needed for the foundation.** No stored rows have been pushed yet.

## What to do next, in this order

1. **Pin the 13 outside points onto the rows** (section G; criterion 7). Read the tables in
   `data/outside/ng_oct2023/made/`; at each row take the latest value known at or before the row's received time.
   Claude's calls, to state to Greg when it is built: the figures made once per trade day (forecast, disagreement,
   expiry count) are on every row of that trade day and EMPTY on rows that belong to no trade day (the stretches,
   the Sunday start-up); everything else is the latest value known at the row's received time. The Sunday start-up
   rows carry the vendor's flag that their received time is unreliable; they are pinned by the time as stamped and
   keep the flag.
2. **Store the four trade days** in markets-data on fresh branches, one per trade day, with a file list
   (`python3 -m root.run build <day> --out <folder>`), and the playback record for each.
3. **The sheet:** write a short stretch first and report its size to Greg. The full workbook is written ONCE, after
   the calculation columns exist (Greg agreed: "Do your plan").
4. **Delete the old** (Greg: "After we get new data filled in let's delete the old"): show Greg the list and wait
   for his "delete". The list as understood: `trade-day-rebuild-20261116/scripts/` and the four `trade-day-book-*`
   branches of markets-data (143,979 book pictures made with the stand-in scripts, cut at the wrong hour).
5. **Step 1 and Step 2 calculations** (gameplan, on Fable): first the list of hard-coded boundaries in the Step 1
   programs, owed to Greg. Then each calculation laid out his way (what we want, what it did, what changes) and
   approved BEFORE it is built or run. Calculation code goes in `root/calcs/` and receives ticks only through
   `tape.for_calculations()`.

## Rules Greg gave or sharpened today (all recorded in the decisions file)

- **Only the four trade days enter a calculation.** Data from outside them seats the order book and nothing else.
  Any other use of outside data is put to Greg FIRST. Nothing is commingled. Enforced by the gate in `root/tape.py`.
- **Markets is code only; data and results go to markets-data.** Do not push to Markets except code on the session's
  own branch. The trunk gets nothing without his word.
- **Every calculation is inspected by Greg before it runs,** Step 1 and 2 included.
- **Empty cells are never counted in a calculation** and never stored as zero.
- **Keep the forward contracts** as approved. The other months' full order tape is not bought; the definite answer
  comes when the Step 1 and 2 calculations are laid out.
- **Checks: one per new part, run once, on that part only.** Do not re-run everything from the beginning; do not add
  checks beyond what the spec lists. Greg: "These turn into major time sucks and we need to be progressing and not
  constantly testing."
- A trade may continue past the four trade days: nothing is built for it; it goes to Greg if it comes up.
- Four boxes in parallel were approved for the calculation runs if they are needed; Greg sees the pod type and price
  first. The foundation does not need them.

## Waiting on Greg

- His "delete" for the old material (item 4 above), once the new rows are stored.
- `artifacts/recovered-c-drive/` (4.7 GB) is still in Markets. It is to move to S3 with an index in markets-data;
  AWS is not reachable, so it waits. It is not part of "the old" above unless he says so.
- `web.archive.org` on the cloud environment, if the street estimate (X12) is wanted.

## Facts read from the tape today (for whoever builds next)

- The Sunday re-listed orders carry the vendor's snapshot flag and the unreliable-received-time flag; they are the
  exchange's start-up, so they are ticks. Every later raw file opens with the vendor's restatement (about 700
  orders), which is kept in its own table and never applied.
- Every fill is followed inside the same exchange event by the cancel of that order (fully filled) or a modify to a
  smaller size (partly filled). A fill counts as a step of the order's life.
- The sequence number goes backwards 101 times per week, all inside the Sunday start-up block.
- Five fills at 6:00 pm Sunday Oct 15 (the open of trade day Mon Oct 16, warm-up) name orders the book does not
  hold. They are on no row of the four trade days.
- One contract (instrument 150611) on all four trade days. No "maybe bad book" flag anywhere.

## Other work done in this session (not ROOT)

- The GitHub plugin was customized for DavisAI (`plugins/davisai-github/`, skills copied to `.claude/skills/`), on the
  Markets trunk.
- The sqlite-triage outputs and write-ups were deleted from the Markets trunk (1,514 files, about 1.2 GB), the run
  code kept; `root-audit-20261116/OLD_INPUT_READS.md` lists where the kept programs read old files.

## How Greg wants the work done

- Plain words, one piece at a time. He reads on a phone. Answer his question first, then return to the open item.
- Do not re-ask what he has decided. Record decisions in git as they are made.
- Where a point is a detail, make the call, state it, let him correct it.
- Keep moving: build, one check on the new part, report what passed and what did not, next part.

## Check results

Markets `claude/plugin-company-customization-z50yb3` at `33d1586`. One check run on rows, store and checks, on the
real tape:

- PASSED: every row of all four boxes checked (the cut, one history per order, empties empty, the line on the row
  adds up, best-price moves marked, "by fill" follows a fill); every record accounted for and the trade counts equal
  the raw files (criteria 1, 2, 5, 6).
- PASSED: the stretch between two built trade days is the same rows in both boxes.
- PASSED: playback at four cuts on trade day Oct 3: inside an exchange event, across 6 pm, across the vendor file
  boundary, across 5 pm (criterion 8).
- PASSED: two builds of trade day Oct 2 are byte-identical (criterion 9); stored empties are empty.
- PASSED: the vendor restatement is kept in its own table and matches our book.
- One test failed on a wrong expectation of mine, not on the data: the first written row of trade day Oct 2 is the
  exchange's clear, so the first book picture holds no orders. The receipt now states each picture's order count
  (first 0, last 423 on Oct 2). Re-checked with one build: passes.

Not done yet: the four trade days are not stored in markets-data (step 2 of "What to do next"); the 13 are not
pinned onto the rows; no sheet; criterion 7 (outside pinning) and criterion 11 (workbook equals stored rows) come
with those parts. The store and checks tests were not re-run in full after the last small change, on Greg's rule
(one check per part; only the changed piece was re-checked).
