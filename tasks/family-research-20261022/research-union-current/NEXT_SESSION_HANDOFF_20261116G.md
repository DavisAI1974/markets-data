# Handoff, seventh session of 2026-11-16 (Step 1 pieces 1 and 2 built; Step 2 A to K approved; next: the book totals and the quote's runs)

Branch: `ccr-349e2ffe-07p8od` in `DavisAI1974/markets-data` for data and documents. This file replaces
`NEXT_SESSION_HANDOFF_20261116F.md` as the starting point. Greg asked for a new chat because this one grew long;
nothing was left half done.

## Read these, in this order

1. `root-redesign-20261116/ROOT_GAMEPLAN_DECISIONS.md`: every decision in Greg's words. The section "Seventh
   session" is new and long; it governs where anything differs.
2. `root-redesign-20261116/STEP1_STEP2_LAYOUTS.md`: the Step 1 layouts, with "as built" for pieces 1 and 2.
3. `root-redesign-20261116/STEP2_PLAN.md`: the Desktop session's Step 2 plan. Pieces A through K are approved by
   Greg as laid out in "The suggestions laid out together". Read it in full before building any of it.
4. `root-redesign-20261116/SPEC-root.md` and `SPEC-outside.md`: the approved foundation.
5. Markets `CLAUDE.md`, "The trading rules".

## Where everything is

- **ROOT code:** Markets branch `ccr-ebe7e38d-wwccru`, tip `6a468af`. Not on the trunk. A new session gets a new
  branch: `git fetch origin ccr-ebe7e38d-wwccru && git merge --no-edit FETCH_HEAD` (or start the session's branch
  at that tip if the merge refuses for unrelated histories).
  Fresh container: `pip install databento pyarrow xlrd openpyxl pytest`; set `MARKETS_DATA` to the markets-data
  checkout.
- **Stored rows and Step 1 outputs:** markets-data branches `root-rows-20231002` (`603f1f9`), `-20231003`
  (`b7f6f49`), `-20231017` (`fd056f2`), `-20231018` (`9b29c64`). Each holds the 217-field rows, the book pictures,
  and now the Step 1 files (`calc-flow_peak-*`, `calc-peak_story-*`, their `CALC-*.json` receipts), listed in
  `FILES.md`. To work on a trade day: `git fetch --depth 1 origin root-rows-<day>` and add a worktree.
- **Run a calculation:** `python3 -m root.run calc <name> <day> --rows <rows folder> --out <folder>`, then copy
  the output files into the rows folder and commit to that `root-rows` branch with `FILES.md` updated. One trade
  day at a time in the session (three at once ran out of memory). About 25 seconds a trade day per calculation.

## What is built in part 2 (all on the real tape, each with its one check passed on all four trade days)

| Calculation | File | What it writes |
|---|---|---|
| `flow_peak` (Step 1, piece 1) | `root/calcs/flow_peak.py` | On every row: bought, sold and no-side size of the last 20 seconds and the flow. On the row a peak becomes known: its side, size, the tick of its high, its standing so far, how long it had been the highest, the time since the peak before. 36,688 peaks over the four trade days. |
| `peak_story` (Step 1, piece 2) | `root/calcs/peak_story.py` | A facts table beside the rows, one line per fact at the tick it became known: build-up, new low, reached zero, came back, beaten. 226,077 facts. A small file of the peaks still open at the last tick. A column on each row with the number of facts known there. |

The runner is `root/part2.py`; the checks are `root.checks.flow_peak` and `root.checks.peak_story` (a full recount
by a different method, and playback at two cuts). A calculation can keep a table beside the rows (`TABLES`).
`tests/root/test_flow_peak.py` and `test_peak_story.py` run on a short real stretch.

## What to do next, in this order

1. **A gate for calculations that read the stored rows** (Claude's call, to state to Greg when it is built). C, the
   quote's runs, A, B and K all need what a tick did to the book, which is in the stored rows; today
   `tape.for_calculations()` gives raw tape records only. Add one rows gate in `root/tape.py` that uses the same
   `calculation_eligible`, test that it passes exactly the positions `for_calculations()` does for that trade day,
   have the runner hand the rows to the calculation, extend the forbidden-words test so no file in `root/calcs/`
   opens a stored file itself, and bring the wording in Markets `CLAUDE.md` (session branch) into line.

2. **C, the book running totals** (`STEP2_PLAN.md`, piece C; approved). Rules read off trade day Oct 2 in this
   session, not yet built:
   - With these rules the side's total size equals its size at the open plus added minus pulled minus filled on
     EVERY row of trade day Oct 2 (checked, zero mismatches): joined = added (the order's size); left by cancel
     and shrank = pulled; left by fill and shrank by fill = filled; size raised, price changed and stayed = added
     when the size went up, pulled when it went down. Use that identity as one of the checks.
   - A change of price that also changes size: 1,957 of 28,271 on Oct 2 (1,022 larger, 935 smaller). Count the
     moved size and the size change separately and state the rule.
   - **Filled size cannot be checked against the fill messages one for one.** On Oct 2 the fill messages total
     85,688 and the resting size removed by fill is 80,711. 1,688 fill messages name an order that is not reduced in
     that exchange event; the order's next row is "stayed" (1,236), "size raised" (321) or "price changed" (126).
     That looks like an order being refilled as it trades (the fill takes size, the same message restores it), so
     the book shows no net change. **Open call for the builder, to state to Greg:** whether such a fill counts as
     filled and added both (using the fill message's size), or stays uncounted because the book did not change.
     Trades with no side come with fill messages of side N that DO name resting orders (3,804 on Oct 2), and their
     reductions carry the order's own side; they are not plain cancels.
   - "At the best price": `levels_from_best` is read just before the tick and `best_bid`/`best_ask` just after.
     For a new order, `levels_from_best` = 0 is the same as its price being the best after the tick (132,320 of
     132,320). Say which is used for the line an order leaves and the line it joins. Fills are mostly at the best
     price (60,868) but some are 1 to 5 levels back, during a sweep (the better levels' removals have not arrived
     yet).
   - The totals start at zero at the first tick of the trade day.

3. **The quote's runs of piece I** (the best bid and the best ask followed separately; a run starts, each new
   furthest price, its first step back). Build for a tick that both ends a run and starts the next: that shape
   caused the piece 1 fault this session. The best bid and ask are never empty on trade day Oct 2; the gap is zero
   or less on 1,858 rows (the book is crossed for a moment during a sweep): decide and state how a run treats those.
   Drive the calculation from the best-price columns and the check from the moved marks, or the other way round.
   A run still going at the last tick goes in an open-at-the-end file.

4. **A and B** (the links between peaks; the state at each tick). They need piece 2, which exists.

5. **The chain link models (Step 1). APPROVED by Greg: "Do it."** The layout is in `STEP1_STEP2_LAYOUTS.md` and in
   the decisions file. It reads the links of A, so it is built after A. It is the piece for the pods.

6. **The two checks before D and the print legs of I are placed: DONE, results put to Greg, his decision
   needed.** Both Native's dipole record and the earlier print legs cover the whole trade day on Oct 3 and Oct 18,
   and are missing the first two hours (they start at 00:00 UTC) on Oct 2 and Oct 17. The full result, where each
   record is kept, and Claude's recommendation are in the decisions file under "Result of the two checks". Do not
   place either until he has answered. Nothing is restored without his word.

7. Then D and the rest of I, K, H (the renders, every instance), and the grouping with Greg.

8. **Nine additions, approved by Greg ("Try them all")**, laid out in `STEP1_STEP2_LAYOUTS.md` under "Additions
   from the look at Codex's two pieces". Four calculations, L to O: build **L (refilled orders) and M (sweeps, and
   the quote touching or crossing) together with C and the quote's runs** (they need only the rows; L settles C's
   open call on fills: such a fill counts as filled and added both); **N (orders that act together) with K**;
   **O (what an outside figure changing did) after A, B and I**. Three ways of working apply to every piece (two
   clocks on every fact; more than one way to end; the cases that did not happen). Two readings are made at the
   grouping stage.

9. **The two Codex pieces** (the SQL step and the family workflow, Markets `dd9c797a`,
   `artifacts/sqlite-triage/20261022/`): Greg wants them judged on intent, whether the code does what the intent
   says, whether the kind of output is useful, and which of their perspectives are worth using on the new data.
   Their old numbers carry no weight. A read on those terms was running when this session ended; if its result is
   not in the decisions file, run it again and bring the result to him.

## Pods

Greg wants the step runs on pods, all four trade days at the same time. Shown to him on 2026-11-16 from the Runpod
catalog (no pods were running): General Purpose CPU, 8 CPUs and 32 GB, $0.32 an hour each, $1.28 for four
(recommended); Compute-Optimized, 32 CPUs and 64 GB, $0.96 each, $3.84 for four. Disk is extra and is quoted
before anything starts. **No pod starts without his go at the time**, and the launch path (how a pod gets the code
and the rows and pushes its output) is not built. Pieces 1 and 2 took about 25 seconds a trade day in the session.

## Rules (all recorded in the decisions file)

- A TRADE DAY runs 6 pm Eastern the evening before to 5 pm Eastern on the named date. The 5 pm to 6 pm hour is its
  own marked stretch. Never a bare "day" or a bare date.
- ONLY THE FOUR TRADE DAYS (Oct 2, 3, 17, 18, 2023) enter any calculation. Data from outside them seats the order
  book and nothing else. Any other use goes to Greg FIRST. Nothing is commingled.
- Rows are ticks, columns are fields. One row per tick, nothing collapsed, nothing dropped. A row holds only what
  was known at its tick; nothing is written back onto an earlier row.
- Empty cells are never counted and never stored as zero or blank text.
- Every trade individually. No rates, averages or model scores, with two exceptions he made: the 20-second roll of
  the flow, and the chain link models. **Any averaging is an addition to the individual outputs, never a
  replacement.**
- Caps and limits come off the Step 1 and Step 2 outputs. He wants no master list of them.
- **No fixed marks:** "Let the data be what it is and then we group after we see how they separate."
- **No labels, groups or identifiers until all four trade days have run all their calculations.** The old Step 1
  families (A, B, C) and the old Step 2 groupings of chains are the BASE of the grouping afterwards. He expects
  more than one grouping, "with different pieces in different groups".
- Every calculation is laid out for him (what we want, what it did, what changes) and approved BEFORE it is built.
  A to K and the chain link models are approved. Where the build needs a call the layout does not make, make it,
  state it to him, record it.
- The old programs are rewritten into `root/calcs/`, not patched. The old files stay untouched on their branches.
- Checks: one per new part, run once, on that part only. Keep moving.
- Never invent data. Real tape only. Trade cost is not a market condition.
- **Bad or incomplete data that will not be used is not saved.** A rebuild replaces what it corrects in the same
  change. Scratch work stays out of git. A deletion of something already saved still goes to him first.
- The workbook is written once, at the end, in parts split by rows (about 80,000 rows a part). The eight
  selected-trade sheets wait until the end.
- AWS is off limits until he says. Markets is code only; nothing goes to the Markets trunk without his word.
- Do not re-ask what he has decided.

## Waiting on Greg

- The four old `trade-day-book-2023…` branches of markets-data: this session's connection cannot delete a branch
  (403). He removes them on GitHub (Branches page), or says how.
- The Markets trunk does not have this session's `CLAUDE.md` changes (the trade-day rule pointer; the rule on bad
  data). They are on the session branch and need his word.
- GitHub warns the Markets repository is near its size quota (`artifacts/recovered-c-drive/`, 4.7 GB, waits on AWS).
- His go for pods, when the chain link models are ready to run.
- Any correction to the calls listed under "as built" for pieces 1 and 2.

## Facts from this session (for whoever builds next)

- A trade side of B on the tape is the aggressor buying: on Oct 2, 17,731 of 18,534 B trades printed at the best
  ask and none at the bid.
- The received time never goes backwards on the trade-day rows; the longest gap between two ticks on Oct 2 is 124
  seconds.
- The check that recounts by a second method is worth its cost: it caught four faults this session before anything
  was stored, one of them in a piece already believed finished (a high carried across a change of side).
- `using-agent-skills` did not load in this code session either (the plugin is named in the settings and was not
  installed in the container). The repository's own skills load.
- The Desktop plan quotes 34,278 peaks in places; after the piece 1 correction the count is 36,688.
- The session's memory limit is about 3 GB.

## How Greg wants the work done

- Plain words. He reads on a phone. Answer his question first, then return to the open item once.
- He now prefers a whole plan laid out in one go ("in one swoop"), not a piece at a time.
- Record decisions in git as they are made. Keep moving: build, one check on the new part, report, next part.
- Long builds run in the background with a log.
