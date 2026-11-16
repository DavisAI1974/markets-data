# Spec: the new ROOT

Status: DRAFT for Greg's approval, 2026-11-16. No code is written until he approves it.
Every decision in it is recorded, in Greg's words where he gave them, in `ROOT_GAMEPLAN_DECISIONS.md`.

## Objective

**ROOT is the first set of calculations made from the tape, done once, in one place, that every later stage reads
from.** It keeps that purpose, with one addition: it first pins everything together on one timeline.

Why it is being rebuilt from the ground up: we are trying to find out which pieces of data dictate what happens, and
the calculated data for a trade day will be shown to Frankie one tick at a time so he learns to recognize things as
they unfold, sees what else in the market is changing at the same moment, and makes connections we may have missed.
That only works if nothing was dropped, nothing was decided ahead of time, and no row holds anything from later.

Scope of this build: front-month natural gas, the four trade days Mon Oct 2, Tue Oct 3, Tue Oct 17 and Wed Oct 18,
2023. A trade day runs 6:00 pm Eastern the evening before to 5:00 pm Eastern on the named date.

## What ROOT produces

### 1. The timeline: one row per tick

A tick is one single message from the exchange. Every tick of the trade week has a row, in tape order. Nothing is
merged, grouped, sampled or left out. Ticks that share a nanosecond stay separate rows.

Each row carries the following. "Touched" means the order or price that this tick acted on.

**A. The message as the tape has it** (the native tape)
- Every field the tape carries: exchange time, received time, action (add, cancel, modify, trade, fill, clear, none),
  side, price, size, order number, the exchange's flags and sequence number, channel, contract number.

**B. Our labels** (never used in a calculation)
- Trade day, or the mark of the 5 pm to 6 pm stretch. The label is decided by exchange time.
- Position on the tape, numbered fresh across the week.
- The raw file the row came from, with that file's fingerprint.
- The contract and its expiry date, read from the tape.
- The part of the exchange's session: the trade day, the 5 pm to 6 pm stretch, the 2:28 to 2:30 pm Eastern settlement
  window.
- The exchange's event label: which ticks belong to the same exchange event. It is the position of the event's first
  tick, so it is known as soon as the event starts. The exchange's own end-of-event flag stays on the tick that
  carries it.

**C. What this tick did to the book**
- The touched order's size before and after.
- Whether it joined, stayed, shrank, lost its place in line, or left; and if it left, whether by cancel or by fill.
- How many orders and how much size were ahead of it in line just before.
- Which step of its life this is so far, the tick where it first entered, and the tick of its previous step.
- When it first entered and when it last took its place in line, each on both clocks, and how long it has rested.
  For an order carried over the weekend this is marked "at least".
- How many price levels from the best price the action happened at.
- Anything irregular, on the tick where it happens: a gap in the exchange's sequence numbers, a cancel for more than
  was resting, a message for an order the book does not know, a message that could not be applied (with the reason).

**D. The book at this tick**
- Best bid, best ask and the gap between them.
- For the bid side and the ask side: total size, number of orders, number of price levels, over the whole book.
- At the best bid and at the best ask: size, number of orders, and the front order's size and times.
- At the touched price: the full line, every order in order with its size and times; and the line's total size and
  number of orders just before and just after.

**E. Change-of-state marks**
- Best bid moved; best ask moved (from what price to what price).
- A price level appeared; a price level emptied.
- The order at the front of a line changed.

**F. Trades**
- Each trade's side and size exactly as the tape gives them, and its price.

**G. The 13 outside data points**
- Each one on every row. A value holds from the moment it became available until the next one replaces it.
- For this stage: one forecast per trade day (the last made before the trade day opens), and the storage figure as
  printed on Thursday morning.
- The temperature figure is worked out from hourly readings, gas-weighted with the weights stated, on the gas day
  ending 10 am Eastern, with wind and carry-over from earlier days as their own columns. The hourly readings are
  kept city by city underneath it.
- A value that could not be obtained is empty with its reason. Nothing is estimated or filled in.

### 2. Kept beside the timeline

- **A full picture of the book at every trade:** every price level and every order.
- **The vendor's snapshot records.** Each raw file opens with the vendor's own restatement of the book. They are not
  messages from the exchange at that moment, so they are not ticks. They are kept in their own table, each compared
  with our carried book, with the result recorded.
- **A receipt for every run:** counts, fingerprints of every input and output, and the result of every check.

### 3. The workbook

- One sheet per trade day, one row per tick, written from the timeline.
- A first sheet, "READ ME FIRST", worded in `WORKBOOK_README_PAGE.md`, so that a reader never mistakes a repeated
  value or an empty column for missing data.
- Columns that later stages will fill are present and empty until then.

## What ROOT does not do

- It does not define or find the bigger lifecycles (families, dipoles, pre-births, ramps, refill, recovery,
  turnover), and it does not answer what the S fields were measuring. Those need definitions worked out first and
  belong to the stage after ROOT, which adds its results to the same timeline.
- It does not add trades up into "flow" over any stretch.
- It does not fill the Step 1 columns or the "legacy" columns (handled separately) or Frankie's outputs (blank).
- It uses no fixed window, cap, threshold, top-N view, sample, average or rate.
- No trading cost, fee or fill assumption enters anything.

## How it runs

1. **Put everything together.** Read the raw files of the trade week in order. Prepare the 13 outside data points
   and pin them, and check them.
2. **One pass.** Walk the tape once from the exchange's Sunday start-up. One book is kept in memory for the whole
   week and is never restarted. Each tick is applied to the book, its row is written, and everything in sections A
   to G is taken at that tick, in that one step.
3. **Warm-up.** Ticks before a trade day we are building (Sunday evening, and Monday Oct 16) are run through the book
   so that it is right when the trade day starts. Nothing is written out for them.
4. **Check the pinning.** Only when every check below passes is ROOT finished for that trade day. No later stage
   starts before that.

## Parts and build order

| Part | What it does | Depends on |
|---|---|---|
| `calendar` | The exchange's times: trade day, the 5 pm to 6 pm stretch, the week, the settlement window. | none |
| `tape` | Reads the raw files of a trade week in order, every record; separates the vendor's snapshot records; takes the contract from the tape; refuses, naming the file, if one is missing. | `calendar` |
| `book` | One book per contract for the week: every order with its place in line and its times; the running whole-book figures; the front orders. | `tape` |
| `rows` | The one pass: builds each tick's row, sections A to F. | `book` |
| `outside` | Prepares the 13 outside data points and pins them onto the rows, section G. | `calendar`, `rows` |
| `store` | Writes the rows, the book pictures at every trade, the snapshot table and the receipt. | `rows` |
| `checks` | Every check in "Success criteria". | all of the above |
| `sheet` | Writes the workbook from the stored rows. | `store`, `checks` |

Build order: `calendar`, `tape`, `book`, `rows`, `store` and `checks` together, then `outside`, then `sheet`.
Each part is built in small slices, tested on real tape only, tried on a short stretch of one trade day, then run on
all four.

## Success criteria

ROOT is done for a trade day when all of these hold, each shown in the receipt.

1. **Every record is accounted for.** For each raw file, records in the file = tick rows + vendor snapshot records,
   counted independently of the pass. No tick is skipped, merged or reordered.
2. **The trade day is cut right.** Rows labelled with a trade day have exchange times from 6:00 pm Eastern the evening
   before to 5:00 pm Eastern on the named date. Rows from 5:00 pm to 6:00 pm carry the separate mark.
3. **The book matches the exchange.** At the opening of every raw file after the first of the week, our carried book
   equals the snapshot there: the same orders, sides, prices and sizes, and the same order in every line. The
   snapshot's time for each order equals the exchange time at which we say that order last took its place.
4. **The book adds up at every tick.** After each tick, the running whole-book figures equal the figures before plus
   that tick's change. At every trade they also equal a fresh count of the whole book.
5. **Every order has one history.** Each order that enters has consecutive steps and exactly one ending, or is marked
   as still resting when the record ends.
6. **The trades are all there.** The number of trade rows in each trade day equals an independent count of trade
   messages in the raw files for the same span.
7. **The outside data points are pinned right.** On every row, each outside value became available at or before that
   row's received time, and it is the latest such value.
8. **Playback holds.** With the tape cut off at a tick, every row up to that tick is identical to the same row of
   the full run. This is run at several cut points, including inside an exchange event, across 5 pm, across 6 pm and
   across the vendor's file boundary.
9. **Same result twice.** Two runs on the same inputs give byte-identical outputs.
10. **No hidden numbers.** The build fails if ROOT code contains a window length, threshold, top-N or sample. The only
    constants are on a short declared list with their reasons: the exchange's times (5 pm, 6 pm, the settlement
    window), and the stated times and weights used by the outside data points.
11. **The workbook says the same as the stored rows.** Each sheet's row count equals the stored row count for that
    trade day, and rows read back from the sheet equal the stored rows.

## Assumptions

These are Claude's calls. Correct any that are wrong.

1. The trade-day label is decided by exchange time. The received time is on the row beside it.
2. The rows are stored in data files (Parquet) as the exact record, and the workbook is written from them. Both hold
   the same rows. A workbook alone could not hold the book pictures or be checked byte for byte.
3. The rule that applies each message to the book is the exchange's own priority rule: a cancel reduces an order in
   place; a modify that changes price or raises size sends the order to the back of the line; trade and fill
   messages change nothing by themselves. It is written fresh in the new code, and its test is the exchange's
   snapshot (criterion 3), not any earlier program.
4. Yesterday's stand-in scripts (`trade-day-rebuild-20261116/scripts/`) and the 143,979 book pictures built with them
   are replaced by this build and deleted in the same change that brings in their replacement.
5. Runs are tried on a short stretch in the session first. If a full trade day does not fit the session, it runs on
   Runpod CPU pods, and Greg sees the pod type and price before anything starts.

## Tech stack

Python 3.12 or later. `databento` to read the raw files, `numpy`, `pyarrow` for the stored rows. A streaming
workbook writer is chosen at the planning step. No other dependency without asking.

## Commands

```
python3 -m root.run check-week 20231002            # files present, fingerprints, record counts
python3 -m root.run build 20231002 --out <dir>     # one trade day: rows, book pictures, snapshot table, receipt
python3 -m root.run playback 20231002 --cuts <n>   # the playback check
python3 -m root.sheet 20231002 --rows <dir>        # the workbook sheet for one trade day
python3 -m pytest tests/root                        # all checks, on the held tape
```

## Project structure

```
Markets repository, branch ccr-1adaee3f-6ame3b
  root/                 the new ROOT: calendar.py, tape.py, book.py, rows.py, outside.py, store.py, checks.py,
                        sheet.py, run.py, DECLARED_CONSTANTS.md
  tests/root/           tests, real tape only

markets-data repository, branch ccr-349e2ffe-07p8od
  data/nymex_mbo/ng_v0_oct2023/                 the raw MBO files (input)
  .../research-union-current/root-redesign-20261116/
      SPEC-root.md, ROOT_GAMEPLAN_DECISIONS.md, WORKBOOK_README_PAGE.md
      receipts/                                 one receipt per run
  stored rows and book pictures                 on their own branches, one per trade day, with a file list
```

## Code style

Small functions with one job; one generator for the pass; refusal by exception with the reason in plain words;
every constant declared in one place with its reason.

```python
def trade_day_bounds(trade_day: date) -> tuple[int, int]:
    """Exchange-time span of a trade day in UTC nanoseconds: 6 pm Eastern the evening before to 5 pm Eastern."""
    opens = datetime.combine(trade_day - timedelta(days=1), OPEN_EASTERN, tzinfo=NEW_YORK)
    halts = datetime.combine(trade_day, HALT_EASTERN, tzinfo=NEW_YORK)
    return to_ns(opens), to_ns(halts)
```

## Testing strategy

- Real tape only. No made-up message, order, price or outside value, ever.
- Tests run on the seven raw files held and assert the success criteria directly.
- Each refusal has a test that makes it fire on real files, for example by withholding one file.
- Calendar functions are tested on real dates.
- A part is not called done until its checks pass on a short stretch and then on all four trade days.

## Boundaries

- **Always:** stop with the reason when a check fails; write a receipt for every run; declare every constant; keep
  both clocks; delete what a change replaces in that same change.
- **Ask first:** any paid download; any pod; any new dependency; any change to what a row holds; any deletion from the
  research folder or of old ROOT code (Greg signs off the file list and the lineage list first).
- **Never:** drop, merge, sample or reorder a tick; restart the book inside the week; write anything onto a row from
  a later tick; apply a vendor snapshot after the week's start; use an order number, trade number, position or clock
  as an input to a calculation; put a cost or fee into anything; invent data; use the old ROOT, its outputs or the
  old sheet as a source or as a test.

## Open questions for Greg

1. **The outside data files are on S3 and AWS needs your sign-in.** Until then the `outside` part cannot be built or
   checked. By your rule the 13 are pinned before ROOT calculates, so a finished run for a trade day waits on this.
   The tape and book parts can be built and tried in the meantime. Is that order acceptable?
2. **How large the workbook will be is not known.** A sheet of about 800,000 rows with a full line of orders in a
   cell may be too big for Excel to open comfortably, and one cell holds at most 32,767 characters. Proposed: write
   a trial sheet for a short stretch first, measure it and the longest line on the tape, and bring you the numbers
   before the full workbook is written.
3. **Where the stored rows live.** Proposed: git, on one branch per trade day with a file list, as the book pictures
   were stored yesterday.

## When this lands

Replaced and deleted in the same change as their replacement: `CAPABILITY_MAP.md` and `SPEC-tape-stream.md` (now, by
this spec); `trade-day-rebuild-20261116/scripts/` and the `trade-day-book-*` branches (when `tape`, `book` and
`store` pass their checks). Old ROOT code and old outputs are deleted only after Greg signs off the file list and
the lineage list.
