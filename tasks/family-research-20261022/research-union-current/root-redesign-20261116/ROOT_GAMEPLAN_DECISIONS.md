# ROOT gameplan: what Greg decided, piece by piece (started 2026-11-16, third session)

This file records decisions only. Nothing here is built yet. It is added to as each piece of the gameplan closes.
Where a line is Greg's own words it is in quotation marks.

## How the gameplan runs

- One step at a time, starting with ROOT only. "Don't worry about any other steps until we're done unless I say to."
- For every step we move through, three things are laid out: **what we want it to calculate, what it calculates
  today, and what changes.**
- No code and no spec is written while a piece is being talked through.

## ROOT's purpose (kept)

ROOT keeps its original purpose: it is the first set of calculations made from a trade day's tape, done once, in one
place, that every later step reads from (the old runbook calls it "the calculations root"; its place in the chain is
fetch, ingest, ROOT, then everything after).

Greg: "I want to keep roots purpose the same. I don't believe we did that well before so let's start fresh."

- ROOT does calculate. It is not a record only. (This corrects the wording of `CAPABILITY_MAP.md` draft 2, which
  describes ROOT as "only the complete record". The map is to be revised when the pieces are settled.)
- ROOT is rebuilt from the ground up and rerun on the four trade days. "Very little of the old root code will be
  salvaged for new root."
- The old ROOT is never the test for the new one. Greg, 2026-11-16 second session: "The old may not be correct, and
  it's definitely not complete."

## Standing rules added or sharpened in this session

- **A tick is each single message on the tape, at its nanosecond clock.** Several messages can carry the same
  nanosecond; each is its own tick, in the order the tape gives them, never merged.
- **"We don't drop any data."**
- **A trade day runs 6 pm Eastern the evening before to 5 pm Eastern on the named date.** Example: Tuesday's trade day
  is 6 pm Monday to 5 pm Tuesday.
- **The 5 pm to 6 pm Eastern hour is its own marked stretch**, belonging to neither trade day, recorded in full. The
  book processes its messages so that it is right at 6 pm.
- **Old ROOT outputs and old ROOT calculations are both discarded.** Greg: "Discard the old root outputs and calcs for
  that matter ... Root was done completely wrong on different levels and we don't want that to continue. That's what
  the replace and delete step is for." None of them goes on the timeline, none is a starting template for a new
  calculation, and none is a test for the new ROOT. The old code is read for one thing only: what question each
  calculation was trying to answer, so that no question is lost. Then it is replaced and deleted (deletion itself
  still waits for Greg's sign-off of the file list and the lineage list).
- **Everything is pinned together by timestamp.** Greg: "Everything will be pinned together by timestamp at some point
  in the process. The calculations don't make sense if they aren't done according to their timestamps." Every value
  is worked out at its own tick and carries that tick's two clocks and its position on the tape (the position is a
  label that tells apart ticks sharing a nanosecond; it is never an input to a calculation).
- **One reading per tick.** Applying the tick to the book, recording what it did, and taking values off the book are
  one step and one record at that tick, not separate runs or separate outputs to be lined up afterwards.
- **A stage is not finished until everything it calculated is pinned correctly.** Greg: "Whatever we calc in any stage
  should be pinned correctly before it moves from that step." This applies to every stage, not only ROOT.
- **Look-ahead is about the clock within the tape, not about the calendar date of a discovery.** Greg: "We consider
  something learned at 3 pm is a look ahead at 2 pm but we don't worry about when something was discovered according
  to the calendar. In a real world situation we will have run enough days prior that it would have discoveries made
  in its memory ... Other than holidays there's nothing that you will learn on the 18th that you couldn't have
  learned on the 1st." So: a value at a tick may use only data that had arrived by that tick. A discovery about how
  the market works (a definition, a family, what dictates what) may come from any of the trade days and be applied to
  all of them, in any order. The exchange calendar (holidays) is the exception, because it is a fact of its date.
- **Old work that gets replaced is not written up.** Greg: "We don't need to document old work that gets replaced.
  If something is wrong it gets fixed and we move on." This file records what is decided for the new build, not what
  the old one did.
- **The book is the week.** It is seated at the exchange's Sunday start-up and carried straight through to Friday. The
  only restart is the exchange's own on Sunday. The trade day is how work is cut and labelled; it is not a point where
  the book starts over.

## Answers to the open questions of `ACTION_PLAN_20261116.md` section 6

1. Where the new ROOT code lives: the Markets repository, folder `root/` with tests in `tests/root/`. "That's fine."
2. Holiday week or missing Sunday file: only the four held trade days are in scope (trade days Mon Oct 2, Tue Oct 3,
   Tue Oct 17, Wed Oct 18, 2023). Nothing is built for a holiday week now; a missing file stops the run and is named.
3. Contract roll inside a trade week: one book per contract, keyed by the tape's own instrument. Agreed.
4. The ingest: the part that cuts the trade day and builds the book is replaced together with ROOT. "That's fine."
5. The order book: "The latest version of book survives." Comparing two old copies with each other is not the test.
6. `c15_dstate.py`: not a question for ROOT any more. ROOT is redone from the ground up, tick by tick.

Sign-offs of the file list, the lineage delete list and the research intentions: not yet given. Nothing is deleted.

## Piece 0: put everything together (CLOSED by Greg, 2026-11-16)

Greg: "Root should be putting everything together before it does the calcs. That's probably a new part of root."
"Our full depth of over 100 fields ... should be pinned together before we calc things. That's the only way we'll
get the true picture. Some calcs may only touch specific pieces but we should have the entire picture together before
we start figuring out how things work." "I understand that it won't have all of the fields initially but it should
have full mbo, and anything else that isn't calc by root."

**What we want**
- One timeline for the trade week: every tick of the full order tape (MBO), each with both clocks and its position on
  the tape.
- Pinned onto it, before any calculation: everything that is not calculated by ROOT, each item at the moment it
  became known.
- ROOT then calculates at each tick with that whole picture in view, and pins every result onto the same timeline at
  its own tick. The pinning is checked before the next stage starts.
- Fields from later stages join the same timeline when those stages are rebuilt. No old calculated value is put on it.


**The check for "pinned correctly"** (agreed by Greg with the five additions, 2026-11-16)
- Every value sits on the tick it was calculated at, with both clocks and its tape position.
- No value used data that arrived after its tick.
- Every tick is accounted for: where a value does not exist at a tick, that is marked with the reason.
- The counts add up: ticks in, ticks on the timeline, values pinned.
- Running the stage twice gives exactly the same result.
- The playback check: run with the tape cut off at a tick, and every row up to that tick is identical to the same
  row in the full run. This proves no row holds anything from later.

**Still to do for this piece (reading only):** sort the workbook's 141 fields one by one into pinned at the start,
calculated by ROOT, calculated by a later stage, or Frankie's; and find where the outside data files for the four
trade days are kept. An outside value that cannot be found stays empty with a note.

## The workbook's 141 fields: start fresh (Greg, 2026-11-16)

Greg: "We should probably delete all of the column data that was calc from something else and just keep raw data
that we get from historic data. Just start fresh and not try to sort out good and bad when most if not all calc data
on there isn't right." And: "I don't know if the raw data is even fine because we didn't use the correct clock."
And: "Step 1 is going to be different initially don't wipe it. Let's do the other column first."

- **Nothing is carried over from the old sheet, not even its raw columns.** The sheet's raw columns came through the
  old archive, which was cut on the wrong clock (two trade days missing their first two hours, numbering off, trades
  only). The starting point is the raw MBO in the vendor's native format (`data/nymex_mbo/ng_v0_oct2023/`, seven UTC
  clock-day files with fingerprints in `MANIFEST.json`) and the outside published numbers with their publication
  times. Everything else is laid down fresh on the new timeline.
- **Exception: the Step 1 fields are not wiped.** They are handled differently and later. The other columns are done
  first.
- **One run.** Greg: "there's no reason to do 2 separate runs." The old split into a "legacy" pass and a "bedrock"
  pass, with a second trip over the tape, goes away. Every ROOT calculation is done in the one pass.
- Nothing has been deleted. The old workbooks and their calculated columns are on the lineage delete list, which
  still waits for Greg's sign-off.

- **The native tape goes on the sheet: one row per tick, nothing ever collapsed.** Greg: "Yes, 1 row per tick, nothing
  ever collapsed." Terms as agreed: *raw MBO* is the vendor's file as downloaded; the *native tape* is that file
  opened into its records, every message exactly as the exchange sent it (adds, cancels, modifies, trades, fills,
  clears), each with its two clocks, side, price, size, order number, flags and sequence number. The Sunday clear and
  the block of re-listed orders are rows too, marked for what they are. Each row carries its trade day, or the mark
  of the 5 pm to 6 pm stretch, and its position on the tape. The old sheet had rows for trades only, with the
  messages grouped inside cells by kind. (A trade day has about 770,000 to 880,000 ticks; an Excel sheet holds
  1,048,576 rows, so each trade day fits on its own sheet.)

How the 141 fields fall (10 trade labels, L001-L099, X01-X13, S01-S19; names from
`field-rebuild-20261113/LAYER_REGISTRY.json`):

| Kind | Fields | Count | Treatment |
|---|---|---:|---|
| Straight from the tape | trade id, event clock, receive clock; L027, L028, L030-L036; L072, L073 | 14 | laid down fresh from the raw MBO |
| Our own labels and bookkeeping | day, trade ordinal, trade cursor, known-by clock, coverage, source revision, source path; L029 | 8 | remade fresh |
| Calculated from the tape | L037-L071; L074-L076; S01-S19 | 57 | start empty, calculated fresh |
| 2021 Step 1 answers | L080, L083-L089 | 8 | NOT wiped; handled differently, later |
| Frankie's outputs | L077-L079, L090-L099 | 13 | blank |
| Reference documents, not data for these trade days | L001-L023, L025, L081, L082; L024, L026 (2021 tape objects) | 28 | not on a per-tick timeline; untouched |
| Outside data points | X01-X13 | 13 | pinned onto every tick, fresh (see below) |

**The 13 outside data points (Greg, 2026-11-16):** "We should have the 13 dp files pinned when appropriately. Their
values will just be handled a little differently. Like the storage number for that day will be the same thing for
every tick until the number changes on a Thursday. Forecast temp will be that temp for every tick in that hour and
change for the next hour."

- The 13 stay, and are pinned onto every tick of the timeline.
- Order of work (Greg: "And the root calcs are added before the next step happens." "So treat the 13 dp files
  accordingly."): the 13 are prepared, pinned onto every tick and checked in the first step, before ROOT calculates.
  They are in place on every row when ROOT's calculations run, and ROOT's results are pinned and checked before the
  next stage starts.
- Each value holds, unchanged, on every tick from the moment it takes effect until the next value replaces it. Each
  point changes at its own pace (the storage number weekly, a forecast temperature hourly).
- They are pinned fresh onto the new timeline from the outside data files. The old sheet's copy, attached to trades
  only, is not carried.
- What is wrong in the 13 gets fixed, not noted (Greg, same rule):
  - X12 (storage estimate against actual) has no values: the numbers were never taken out of the saved pages. Fix:
    take them out.
  - The storage figures held are the later revised ones. Fix: use the figures as first printed, from the saved pages.
  - The forecast: one forecast per trade day for now, the last one made before the trade day. Greg: "for the
    forecast weather numbers, for this purpose just stick with one forecast for right now. It's not going into the
    actual root calc so it's not super important in this stage. When we forecast price curves it definitely is. But
    not in root." Following each new model run through the day is left for the price-curve forecasting stage.
  - Storage: the figures as they come out on Thursday morning. Greg: "that's what the market uses for trading."
  - The temperature calculation is rebuilt (Greg: "Yes rebuild it that way"): worked out from hourly readings, not
    from the day's high and low; gas-weighted with the weights stated; on the gas day ending 10 am Eastern; wind and
    carry-over from the previous days as their own columns. The hourly readings and hourly forecast temperatures are
    pinned city by city underneath it. Obtaining the European model runs and the many-run averages is a separate,
    later decision.
  - Where a source records the real time a value became public, that time is used. Where it does not, the value is
    pinned at a stated assumed time (today: a forecast run 4.5 hours after it starts, a station reading 10 minutes
    after, a grid hour 2 hours after).
  - The published figures underneath each point are pinned as well, so nothing rests only on a fixed choice made
    inside a worked-out value (the 1-year and 3-year positioning windows, the city weights, the gas-burn conversion,
    the 12 contract months of the curve).
  - One limit that cannot be fixed from what is held: the hourly grid figures are the current revision; the source
    does not keep the first-published values.
- The outside day files and their inputs are on S3 (`frankie/day_external/<trade day>/`, `frankie/day_history/`,
  `nymex/ng_fut_parent_v0/`). The AWS connection needs Greg to sign in again; one attempt was made on 2026-11-16.
  Whether the files exist for the four trade days is not yet confirmed.

## Piece 1: the order book (CLOSED by Greg, 2026-11-16)

**What we want**
- One book for the week, seated at the Sunday start-up and carried straight through. The only restart is the
  exchange's own on Sunday.
- Readable after every tick, not only when an exchange event closes.
- Every price level and every order: its size, its place in line and its times. No top-10 view.
- Both clocks on every order and every tick: the exchange's own time, and the time the message was received by the
  data vendor's recorder at the exchange (the first moment it could be known outside the exchange).
- Each order keeps when it first entered and when it last took its place in line.
- Orders carried over the weekend are marked, because their true entry time is not on the tape.
- Nothing is dropped.


## Piece 2: what ROOT writes down for each tick (CLOSED by Greg, 2026-11-16)

Greg: "That is correct. We want the tape as it comes."

**What we want**
- One record for every tick, in tape order, none skipped.
- The message exactly as the tape has it, every field, with both clocks.
- What that tick did to the book: which order it touched; that order's size before and after; whether the order took
  a place in line, kept it, lost it or left the book; where the order stood in line just before (how many orders and
  how much size were ahead of it); the best bid and best ask just before and just after.
- The exchange's own end-of-event marker, recorded on the tick that carries it.
- Anything irregular, recorded on the tick where it happens: a gap in the exchange's sequence numbers, a cancel for
  more than was resting, a message for an order the book does not know.


**A fact about this tape that the record must respect.** A trade arrives as several ticks: the trade itself, the fill
of each resting order, then the cancel or modify that takes the filled size out of the book (trade, fill and "none"
messages change nothing in the book by themselves; adapter 529-530). Between those ticks the book still shows size
that has just traded. ROOT records each tick as it comes and marks which tick ends the event, so a reader can take
the book after any tick or only at event ends. Nothing is decided ahead of time.

## How the book is held (Greg, 2026-11-16)

Greg: "Option 2 if it's going to have the book in memory."

- ROOT keeps one book in memory for the whole run. A tick changes one order in it; the book is read as it stands.
  It is never rebuilt at a tick. A later stage that walks a trade day in order carries the book the same way.
- On every row: what changed at that tick, the whole-book figures, and the full line at the price that was touched.
- A full picture of the book is kept at every trade (the 143,979 built on 2026-11-16 are on the four
  `trade-day-book-*` branches; they were cut at 5 pm and are to be rebuilt with the new ROOT).
- A full picture on every row (about 62 KB times about 3.3 million ticks, roughly 200 GB) is not written.
- The complete book at any tick is the nearest saved picture plus the changes after it, exactly.

**Group 3, the book columns (L039-L046): CLOSED by Greg** ("group 3 is closed as long as it holds all raw data that
wasn't calculated"). Row content: best bid, best ask
and the gap; total size, orders and levels on each side; size and orders at the best bid and ask; the full line at
the touched price, with its totals before and after; for the touched order its size before and after, orders and size
ahead just before, first-entry and last-place times on both clocks (marked "at least" when carried over the weekend),
and what happened to it (joined, stayed, shrank, lost its place, left by cancel or by fill); the Sunday clear and
re-listing as marked rows; the weekday snapshot check recorded, the snapshot not applied. A single figure for how
concentrated a line is (L043) is deliberately not chosen yet.

## README page for the workbook (Greg, 2026-11-16)

Greg: "Create a read me page in the excel workbook that explains what's going on with it so if anyone else looks at
it they don't think there's missing data."

The wording is in `WORKBOOK_README_PAGE.md` in this folder. It becomes the first sheet of the rebuilt workbook and is
kept current as each piece closes.

**The frame of the rebuilt workbook (2026-11-16).** Greg, at the end of the session: "make sure excel sheet has been
populated ... clear out old data from excel sheet first. Also add any additional columns as needed."
`ROOT_workbook_frame.xlsx` in this folder holds the READ ME page, a COLUMNS sheet that lists every column in plain
words (77 foundation columns, the 13 outside data points, 37 columns for ROOT part 2, 13 for Step 1 and the 2021
work, 13 for Frankie's outputs), and one sheet for each of the four trade days with those 153 column headers and no
rows. It is made by `tools/make_workbook_frame.py`. **It holds no market data.** No old value was carried into it.
The rows are written by the ROOT build, which has not been built; the 13 outside data points are pinned onto every
tick by that build from the outside data files, not copied from the old sheet, because the old sheet holds them on
trade rows only. The foundation column names in it are Claude's draft of the column list for Greg to correct.

Greg also asked for a page in the workbooks that exist today ("Yes add the page"). Done 2026-11-16 for the two held
in git: a first sheet named "READ ME FIRST" saying the workbook predates the rebuild, why its calculated values are
not relied on, its known gaps, and where the current state is written. Added with `tools/add_readme_page.py`, which
copies every existing part unchanged and adds one entry to each of the workbook's three index files; the page was
read back from both files and the next sheet of each still opens. Page text: `tools/page_four_day.txt`,
`tools/page_priority.txt`.

| Workbook | SHA256 before | SHA256 after |
|---|---|---|
| `Frankie_four_day_research_current.xlsx` | `70b57f3d4843997b970d8a78df1fb1d3ce8a897c0ac318a21d62e242f49d6be4` | `9d7b8959a7eecdb31eb13bb66861b6187b9b9ea0eef1f75b4b2d794469ba13aa` |
| `Priority_native_flow.xlsx` | `544a60f22b9d755214b7ade279eb67ca19ac220f68e7c403068694b8ca70ad94` | `543fc05be948018cb0b6fbf1868d3750babe841f0c94076e438b8b0539021e78` |

Fingerprints of these two files recorded in older manifests in this folder are the "before" values.
Not done: the 500 MB R2 workbook is a GitHub release file, not a file in the repository, and this session has no
tool that can replace a release file.

## What ROOT contains: the split (AGREED by Greg, 2026-11-16)

Greg: "Yes I agree with that split. We can keep roots purpose the same as before with the addition of pinning things
together."

**ROOT holds what the tape says directly at each tick. Anything that first needs a pattern to be defined waits for the
stage after ROOT.**

In ROOT:
- the one timeline, with everything not calculated by ROOT pinned onto it (piece 0), including the 13 outside points;
- the order book for the week (piece 1) and the book columns (group 3);
- the per-tick record, the native tape one row per tick (piece 2, group 1), with our labels (group 2);
- the order histories and the contract and session (group 4);
- L047: each action's side and how many levels from the best price it happened at;
- L048: each trade's side and size as the tape gives them (adding trades up into "flow" over a stretch waits);
- L052: the path of the best prices and of trade prices, tick by tick;
- L053: anything irregular or missing, flagged on its tick;
- L074: when each tick could first be known.

After ROOT (each needs a definition first): L049-L051 (depletion and refill, recovery, turnover); L059-L066 (dipoles,
family geometry, ancestry, chains); L067-L071 (pre-births); L075, L076; S01-S19.

With Step 1, handled separately: L054-L058 (the "legacy" columns made to match the 2021 work).

**Additions (Greg, 2026-11-16: "Yes add all five as long as 3 doesn't drop the rest of the bid ask depth when
it's needed"; the fifth was then withdrawn, see below.)** Each is read straight off the tape at its tick, with nothing added up and no pattern defined first.

1. A mark on the row whenever the state of the market changes: the best bid or best ask moves, a price level appears
   or empties, or the order at the front of a line changes.
2. The exchange's event label on every tick, saying which ticks belong to the same exchange event (a trade, its
   fills, the cancels that follow). A label only; nothing is totalled.
3. The front order at the best bid and at the best ask on every row: its size and its times. This is added to what
   the row already holds. Nothing else about the depth is removed: the whole book, every level and every order, stays
   in memory at every tick and every calculation reads all of it; the row still carries the whole-book figures and
   the full line at the touched price; a full picture is still kept at every trade.
4. The playback check, added to the checks for "pinned correctly" (piece 0), which Greg agreed as a whole.
5. (Withdrawn.) Writing out Monday Oct 16 as a fifth trade day. Greg: "Keep Monday as warm up only, stick with the
   4 days." Monday Oct 16 stays warm-up: its ticks are run through the book so the book is right when trade day
   Oct 17 starts; nothing is calculated for it and none of its rows are written out. The four trade days are
   Mon Oct 2, Tue Oct 3, Tue Oct 17 and Wed Oct 18, 2023.

**Vendor snapshot records.** Each raw file opens with the vendor's own restatement of the book. These are not
messages from the exchange at that moment, so they are not ticks. They are kept in their own table beside the
timeline, each compared with the carried book and the result recorded. Records in a raw file = rows written + ticks run
through the book but not written (warm-up and shelved hours) + snapshot records, and the README page states the
counts so they reconcile. (The Sunday clear and the exchange's re-listing of
carried orders are rows on the timeline, marked.)

## Facts established in this session (real tape and exchange documents)

- **Messages between 5 pm and 6 pm Eastern** (received time), counted on the held files: evening of Mon Oct 2, 418
  messages (359 cancels, all in the 17:00 minute; then 57 adds, 1 modify and 1 other from 17:45 on); evening of Tue
  Oct 17, 490 messages (404 cancels, 399 of them in the 17:00 minute; then 85 adds and 1 other from 17:45 on). No
  trade in that hour on either evening.
- **The book is weekly.** CME: day orders (the default) are removed at the daily close; good-till-cancelled and
  good-till-date orders stay on the book across days; at the weekly start-up the carried orders are sent again.
  Databento: those re-sent orders carry the time of the re-send, not their original entry. Our tape agrees: each Sunday
  file opens with a clear and one block of re-listed orders with a single stamp (342 on Oct 1, 350 on Oct 15), and no
  clear on weekday evenings. Sources: CME order qualifiers
  (https://cmegroupclientsite.atlassian.net/wiki/x/ZQHFAg), CME MDP 3.0 event scenarios
  (https://cmegroupclientsite.atlassian.net/wiki/spaces/EPICSANDBOX/pages/457672114/), Databento GLBX.MDP3 notes
  (https://databento.com/docs/venues-and-datasets/glbx-mdp3), CME natural gas trading hours
  (https://www.cmegroup.com/articles/faqs/faq-natural-gas-weekly-options.html).
- **Where the old ROOT code actually is.** It is not on the tip of
  `research/markets-adaptive-wavepacket-migration-20261108` (that tip holds five files under
  `research/kalshi/frankie_boss/`). It is at Markets `7f34afa` (branch `codex/frankie-brain-four-day-pins-20261109`)
  and the producer package at pin `2ebb8ce8ef4834545ad99a4ecdff50c18c5b3134`. Line numbers in the audit files are
  those two revisions.

## Consequences to carry into the specs (not acted on yet)

- Before any full line of orders is promised inside an Excel cell, measure the longest line at one price on the real
  tape: a cell holds at most 32,767 characters. This does not block the gameplan; it does block writing the workbook.
- The 2026-11-16 trade-day rebuild cut each trade day at 5 pm Eastern on both sides, so its message counts
  (820,642 / 879,830 / 846,406 / 771,787) include the 5 pm to 6 pm hour at the front. With the trade day as 6 pm to
  5 pm and that hour as its own stretch, the per-trade-day message counts are restated. Trade counts do not change,
  because no trade falls in that hour. `SPEC-tape-stream.md` criteria 1 and 7 are to be rewritten accordingly.
- `CAPABILITY_MAP.md` draft 2 is to be revised: ROOT calculates.

## Group 4, the order histories (L037, L038): CLOSED by Greg, 2026-11-16

- Each order's life is followed row by row: it enters, shrinks, grows or changes price and goes to the back of the
  line, is filled, leaves. Each of those rows carries, for the order touched: which step of its life this is so far,
  the tick where it first entered, the tick of its previous step, and, on the row where it leaves, how it ended
  (cancelled or filled completely). An order still resting when the record ends is shown in the last book picture,
  not on a row.
- An order carried over the weekend starts its history at the Sunday re-listing, marked.
- The order number ties the rows together. It is a label, never an input to a calculation.
- The tape shows that an order was cancelled, not who cancelled it or why. Cancels just after 5 pm are recorded as
  cancels in the 5 pm to 6 pm stretch, with no cause attached.
- Each row carries its contract, read from the tape (the expiry date is not on the order tape; it joins when the
  exchange's contract definitions are held), and the part of the exchange's session it falls
  in (the trade day, the 5 pm to 6 pm stretch, the 2:28 to 2:30 pm Eastern settlement window).

## Lifecycles: worked out ahead of time, then shown as they happen (Greg, 2026-11-16)

Greg: "If we're doing lifecycles I do want us to figure out lifecycles in advance and populate the sheet as they
happen by tick. So as time flows the fuller picture will be exposed but we'll have to figure that stuff out ahead of
time. That way we can start seeing things as they happen and understand what comes next."

Greg, on which lifecycles: "The bigger ones as well and prebirths and all that. Frankie has to learn to recognize
this stuff and this is the only way to do it. All of the calc data that we have prefilled in for a trade day will be
exposed to him 1 tick at a time but he'll be able to go over what just happened and how it got there and what a ramp
that has this behavior means and what it will do in the future."

- **What the timeline is for.** The calculated data for a trade day is filled in beforehand and then shown to
  Frankie one tick at a time, so he learns to recognize orders, families, dipoles, pre-births, ramps and the rest as
  they unfold, and what follows them.
- **Two jobs.** (1) Ahead of time: work out the lifecycles, what kinds there are, what stages each goes through and
  what each stage looks like while it is happening. A discovery from any trade day may be used on all of them.
  (2) Tick by tick: fill the timeline as each lifecycle unfolds.
- **Every row holds only what could be known at its tick.** Nothing from later ticks is written back onto earlier
  rows. A row can say how far along something is so far; it cannot say how it will end.
- **Scope.** Greg: "For root we don't have to have all that stuff but by the end, we should have every conceivable
  thing mapped out that we feel is important ahead of time on the excel sheets but it will be experienced as it
  occurs in the playback time."
- **Why everything is on one timeline.** Greg: "And he can see what else in the market is changing as these things
  appear or continue or whatever and he can start making connections that we may have missed." At any tick the whole
  picture is side by side: the tape, the book, the outside data points and, later, the lifecycles.
- For a single order the tape gives the stages. For the bigger lifecycles the stages have to be defined first; that
  work belongs to the stage after ROOT and its results go onto the same timeline.

## All calculations in ROOT (Greg's idea, 2026-11-16)

Greg: "I think we should figure out all of the calcs we're wanting to do including sql step and the other new
workflow step and any dipole and anything else, and have those all done in root. Thoughts? That way the other steps
are just analysis, pattern matching and logic." Earlier the same day: "That's just one part of root right? We still
have root calcs to figure out."

- The specification written so far (`SPEC-root.md`) is part 1, the foundation: the timeline, the book, one row per
  tick with what the tape and the book say directly.
- Part 2 is the ROOT calculations built on top. They are not designed yet.
- Claude's proposed shape, awaiting Greg's yes: the foundation plus calculations added one at a time, each named,
  run tick by tick over the timeline, pinning its own columns and passing its own checks; a calculation may only add
  columns; anything that puts a value on a tick is a ROOT calculation, anything that reads rows and draws a
  conclusion is analysis. Working out the calculations is the calculation inventory (old ROOT sections, the SQL
  step, the other workflow step, dipoles, S fields).
- This supersedes the earlier wording of the split ("after ROOT"): those calculations are part 2 of ROOT.
- Greg, on the definitions that have to be worked out before a calculation can be written (a dipole stage, a
  pre-birth): "We'll still do that ahead of time. Frankie will just have to learn why and how dipole works and apply
  what he's learned when he sees it." So we work the definitions out ahead of time and ROOT calculates them onto the
  timeline. Frankie does not calculate; he learns why and how each thing works and recognizes it when it appears in
  playback. Greg, restating the idea: "So everything is calc and pinned correctly for the next steps and we
  eliminate some separate processes and do them all at once instead of split up."

## What Frankie sees, and the answer key that is hidden from him (Greg, 2026-11-16)

Greg: "He can still have the classroom where he learns about dipole and does things on his own to further research
and for his own knowledge base to apply later on things that we have figured out ahead of time. He's still doing his
thing but we have done it for the historical data so when he's doing his analysis in real time it's also been done
already so we can check his analysis against it. We just have to hide that from him and the other calculated pieces.
It'll be like the blind forecast where we know what happens and he's coming up with his answers and we'll score him."

- Frankie keeps his classroom: he learns why and how things such as the dipole work, does his own research and
  builds his own knowledge to apply later.
- For the historical trade days we have already worked the same things out and calculated them in ROOT. That is the
  answer key.
- In playback Frankie does his own analysis tick by tick without seeing the answer key. His answers are then scored
  against it, as in the blind forecast.
- So every column on the timeline carries a mark: shown to Frankie in playback, or answer key (hidden from him, used
  to score him). Playback serves only the shown columns.
- Which calculated columns are shown and which are answer key is decided with Greg, calculation by calculation.
  Until it is decided for a column, a calculated column is treated as hidden.
- This corrects the earlier note in this file that the calculated data is all shown to Frankie one tick at a time.
- **Open, raised by Greg right after:** "After I thought about it, he's going to have to do the calcs too because
  that's what his real time environment will be like unless we have some other piece of calcs instead of him rt."
  Claude's answer, awaiting Greg: ROOT is that other piece. It is built to run the same way on a live feed as on
  the historical tape, tick by tick, so in real time ROOT does the calculating and Frankie reads its columns and does
  the reasoning. A language model cannot keep an exact order book or do exact arithmetic on hundreds of thousands of
  ticks at the speed they arrive. On that view, what is always hidden in playback is what happens next (the later
  rows), which is what he forecasts and is scored on; hiding particular calculated columns on historical trade days
  is a separate training choice, to test whether he recognizes a thing himself.

**Greg's final word in this session (it supersedes the section above where they differ):** "You had what I
initially said. You had it right but I switched it up. He's going to have to learn in the classroom and then apply
that in rt."

- **Classroom:** for the historical trade days, everything we worked out ahead of time is on the rows and is shown
  to Frankie one tick at a time, so he learns how each thing forms, what else is changing with it, and what follows.
- **Real time:** he applies what he learned.
- Each column still carries a mark saying whether it is shown to Frankie, and the default is shown. The mark costs
  nothing and leaves room to run a blind test later; no hidden answer key is being built now.
- Greg: "So root will do this part in the build and then play a similar but slightly different role in rt." In the
  build, ROOT works out whole historical trade days ahead of time for the classroom. In real time it would do the
  same calculations as each tick arrives, with only what has arrived so far. The real-time role is designed for,
  not built now.

**What Frankie learns (Greg, 2026-11-16):** "But we don't want to have Frankie learn from the 4 days. We want him to
learn its relationship to trades, prebirth signals, exhaustion, etc and then apply that to specific situations.
Dipole lifecycle isn't specific to each trade. There are behaviors that apply to all of them but act specifically in
that trade."

- What he learns is general: how a lifecycle such as the dipole's behaves, how it relates to trades, what its
  pre-birth signals and its exhaustion look like. Those behaviors hold across all trades.
- What he applies is specific: in a given situation, each trade individually, the general behavior shows up in that
  trade's own way.
- The four trade days are not the lesson and are not to be memorized. They are where the general behaviors can be
  seen playing out in particular trades.
- For the build: the timeline shows, tick by tick, where each general behavior is in its course, and for each trade
  its own place in it as known at that tick.

## Answers to the open questions of `SPEC-root.md` (fourth session, 2026-11-16)

`SPEC-root.md` itself is brought into line once all five questions are answered; until then this section governs
where the two differ.

**Question 1, which ticks outside the 6 pm to 5 pm trade day get rows: CLOSED by Greg.** "Yes that's right, add the
mark. Give it whatever fills the book in completely. Those days won't be counted on the excel sheet or run through
any calcs. Just use the extra days to complete the book and if anything does need calculated on those days, keep
them completely separate from the 4 days. You can make a completely different excel sheet for those days. I don't
want those days bleeding into the work we're doing on the 4 days."

- Rows are written for: each of the four trade days, 6 pm to 5 pm Eastern; the 5 pm to 6 pm stretch just before and
  just after each of them, marked; and the exchange's Sunday start-up before trade day Mon Oct 2, marked.
- The extra ticks (the Sunday Oct 15 start-up, trade day Mon Oct 16, and the hours after 6 pm on the evenings of
  Oct 3 and Oct 18) exist for one purpose: to complete the book. They are run through the book with whatever the
  book needs to be complete. They are not rows on the four trade-day sheets, they are not counted there, and no
  calculation is run on them.
- If anything ever does have to be calculated on those extra ticks, it is kept completely separate from the four
  trade days: its own output and, if a workbook is wanted, its own workbook. Nothing from it is mixed into the four
  trade days' rows, counts, checks or calculations.
- **The mark.** A row on trade day Tue Oct 17 or Wed Oct 18 can touch an order that entered during the extra ticks.
  Its pointers back (the tick where the order first entered, the tick of its previous step) then name ticks that
  were never written out. Such a row carries a mark saying the order entered before the written record. The order's
  first-entry and last-place times are still on the row, on both clocks, because they are facts of the book.
- Consequence to carry into part 2 (not decided here): since no calculation runs on the extra ticks, a calculation
  starts with nothing behind it at the first written row of each week's record (the Sunday start-up for week 1;
  5 pm Eastern Mon Oct 16 for week 2). Only the book itself arrives complete.

**Questions 3, 4 and 5: settled from what Greg had already said, plus one measurement (2026-11-16).** Greg: "I
thought we covered the excel issues in last chat." The transcripts of the first and third sessions of 2026-11-16 were
read back in full. He was right on the substance:

- **Question 3, the size of the workbook.** Already closed in the third session: one row per tick, one sheet per
  trade day; the whole book is not on every row ("Option 2 if it's going to have the book in memory"); the row
  carries the full line at the touched price (group 3, closed). The 32,767-character cell limit and a trial sheet
  were never put to him; they came only from the spec. The limit is now settled by measurement on the seven raw
  files: the longest line of orders at one price at any tick is 49, the usual line 7 to 8, and 99 of every 100
  ticks have 24 or fewer. The count was checked against the exchange's snapshot at all five file boundaries. A full
  line always fits in one cell. Writing a short stretch first and reporting its size is a step of the build.
- **Question 4, where the stored rows live.** Greg, first session: "I'm not picky about where you save things to as
  long as it's to git and not the e drive and that saving on your old branch isn't going to have old work bleed over
  into new work." So: git, fresh branches made for this build, none that holds old work.
- **Question 5, the column list.** What a row holds was closed piece by piece (piece 2, groups 3 and 4, the split,
  the additions), and Greg's word at the end of the third session was "add any additional columns as needed". The
  column list is kept by the build; a change to what a row holds still comes to him first. Added on that word: the
  second price and its line when an order changes price; the mark for an order that entered before the written
  record; the full set of outside figures. The old names on the part 2 placeholder columns are settled with part 2.
- `SPEC-root.md` is brought into line with all five answers. Part 1 now waits only for Greg's approval.
- Not answered in any session read: the shape of part 2 in so many words (he restated the idea twice and did not
  object), and whether the calculations are worked out first or the foundation is built first.

**The shape of part 2: CONFIRMED by Greg, 2026-11-16 (fourth session).** "Yes that's the shape I want for part 2.
And if we are answering with our new data one of the old columns, you don't have to state it 2x. And if we should
look at our calcs before we run them to make sure they are adding what we want and that its relevant. So to go
against what i said earlier, we might eliminate columns but for the time being everything is kept and that may not
change."

- The shape stands: the foundation, plus calculations added on top one at a time, each named, run tick by tick,
  pinning its own columns and passing its own checks.
- Nothing is stated twice: where a new column already answers what an old column was for, the old column gets no
  column of its own; the column list says which new column answers it.
- Every calculation is looked at before it is run, to make sure it adds what we want and is relevant.
- Columns may be eliminated later, on Greg's decision. For the time being everything is kept, and that may not
  change. No row is ever removed.
- This also settles the old names on the part 2 placeholder columns: a placeholder is kept only until its question is
  looked at; if a new column answers it, it is not repeated.

**Foundation first: DECIDED by Greg, 2026-11-16 (fourth session).** "Foundation first definitely. The calcs come
from the initial foundation." The foundation (timeline, book, rows, the 13) is built before the calculations are
worked out; each calculation is then looked at with real rows in view.

**The old sheet and the old material (Greg, same message):** "I would clear everything from the old excel sheet and
start from scratch. So much of that data is bad or incomplete that it isn't worth separating good from bad. And we
can just delete the old stuff out and we don't need to save old bad data. It gets discarded and replaced with the
correct data. And just delete old stuff so it doesn't creep back into the new calcs."

- The rebuilt workbook starts from nothing. No value from an old workbook is carried, sorted or kept beside it.
- The old material is deleted, not archived, so that it cannot be picked up by a new calculation.
- Greg's rule at the start of this session was that nothing is deleted until he signs off the file list and the
  lineage list. The delete list was put to him in short the same hour for that sign-off; nothing is deleted before
  his word on it. One earlier ruling is kept out of the delete unless he says otherwise: the Step 1 fields ("Step 1
  is going to be different initially don't wipe it").

**Greg's condition for the delete (2026-11-16):** asked to sign off the delete list, he answered: "As long as we know
how and why the old stuff exists we have the important part." That is taken as a condition, not as the sign-off. The
condition is met by `root-audit-20261116/OLD_MATERIAL_REMOVAL_LIST.md`: for every path, what it is, how it was made,
why it existed, how sure that is, and where copies remain. It also lists a fourth group not first shown to him: the
old assembly programs, file lists and old handoffs that would rebuild or point back at the old workbooks. Found while
writing it: the Step 1 fields are empty in the old workbooks, so no Step 1 value is lost; and `main` does not hold
the old workbooks, but three older `codex/` branches do. **Nothing is deleted until Greg says "delete".**

**The raw data collected on 2026-11-16 stays (Greg):** "Correct, any raw data collected today stays but double check it
to make sure its complete." Checked the same hour; the result is in `data/outside/ng_oct2023/README.md` under
"Completeness check". All 142 files match the manifest. Positioning, forecasts and the curve are complete (the curve
trades of the front contract are identical to the trades on the order tape held, on all four clock-day files
checked). The gaps found are in the sources themselves: a handful of single hours in the station records (one of
them, Boston at 8 am Eastern on Oct 2, is inside a trade day) and three hours of one region's demand table. A missing
hour stays missing.

**Step 1 stays and is built on top of (Greg, 2026-11-16, fourth session):** "Forgot about step 1! That stays. Again we
covered it in either last session or the one before. It just gets built on top of. ... The step 1 stays in the
excel sheet. so i don't know if you want to create a 2nd step 1 column for the growth or just make additions in the
same column".

What he had already said, read back from the second session of 2026-11-16:
- "i believe our thinking on the step 1 pops was that we were going to use the initial 2021 data and then add to it.
  We were going to use those initial definitions and data as a base and have the code remove any hard coded cutoffs
  or boundaries and let the new data expand what we started with because that original step 1 outputs weren't run on
  mbo or this depth so we knew that was a starting point that later runs would expand on."
- "That original step 1 data gives family definitions for how the families shaped up across those days. The
  structure is trade agnostic. The smaller families fit thousands of trades while the largest only fit one or two but
  they weren't individually structured by trade. But maybe they should be, I don't know".
- Third session: "Step 1 is going to be different initially don't wipe it. Let's do the other column first".

So:
- **The Step 1 columns stay in the workbook.** They are in the workbook frame and are never removed with the old
  material. The 2021 definitions and data are the base.
- **The new data expands the base.** The hard-coded cutoffs in the Step 1 programs are listed for Greg, then removed,
  and the full order tape is let to add to what 2021 started. Seen so far: the lineage followed back at most 5
  generations, the 52-week and 26-week blocks, and the family classifier frozen on 2026-08-17. That list is still
  owed to him; it belongs with the calculations of part 2, not the foundation.
- **Base and growth are kept in separate columns (Claude's call, on Greg leaving it open).** Each Step 1 column keeps
  the 2021 base exactly as it was, and a second column beside it holds only what the new data adds. Reasons: the two
  come from different data (the base was not made from the full order tape at this depth); what the new data added
  is the very thing being learned and cannot be seen once the two are mixed; the growth can be redone without
  touching the base; and nothing is stated twice, because the growth column never repeats the base.
- **Two facts for whoever fills them.** The Step 1 columns hold no values in any old workbook (they are empty on
  every trade), so nothing of Step 1 is lost when the old workbooks go. The 2021 base outputs themselves were
  reported in the second session to be in the sealed package on AWS, which cannot be reached today.

**ROOT part 1 APPROVED by Greg, 2026-11-16: "Foundation is good."** The build starts on Opus with the Fable advisor:
first the `outside` point tables (approved), then `calendar`, `tape`, `book`, `rows`, `store` and `checks`.

**The old material DELETED, 2026-11-16 (Greg: "Delete for old data that wasn't entered this morning").** One commit,
672 files: groups 1 to 4 of `root-audit-20261116/OLD_MATERIAL_REMOVAL_LIST.md`. The folder went from 2.1 GB to
294 MB. Kept and checked after the delete: the raw order tape, the outside source files collected today, the redesign
and audit folders, the field names and reference documents, the replay used to establish the book, the handoffs.
The workbook frame tool still runs. A new folder README replaces the old one.

**Why the Step 1 columns are empty (Greg, same message):** "We didn't do step1 in excel because we decided to wait
until we entered the new data." So the empty Step 1 columns are by decision, not a gap; they are filled when the new
data is entered, base and growth side by side. Greg: "Look in git for step 1": the search for where the 2021 base is
kept in git is under way.

**First built piece: the `outside` tables (2026-11-16, on Opus).** Markets branch `ccr-ddc0ebeb-do2y3o`, commits
`a1b3ad2` and `6208460`: `root/calendar.py`, `root/outside.py`, `root/DECLARED_CONSTANTS.md`, `tests/root/` (21 tests, all passing on
the real files). The tables, their receipt and a small workbook of them (`outside_tables.xlsx`) are in markets-data at
`data/outside/ng_oct2023/made/`. Read by eye and tested: positioning equals the CFTC file; the release rule moves a
report a business day in a holiday week; the expiry count is 3, 4, 14, 15 for the four trade days (NGV23 expired
Sep 27, 2023); each forecast on a row is the last run known before the open; Boston's missing hour on Oct 2 stays
missing; the curve's front-month trades equal the order tape; the curve's front price at each open equals the last settlement record known before it; two
builds give identical bytes; every number in the code is declared. Two corrections found while reading the output:
the 16 city weights are scaled to add up to 1, as the original did; and last prices on the curve start fresh where
the held curve files have a gap (Oct 4 to 15), so no Oct 3 price is carried into Oct 16. **Not made yet:** storage
(X11) and the storage estimate (X12): reading the EIA's `.xls` files needs one small library (`xlrd`), which the spec
says is asked for first.

- **A rule to settle when the 13 are pinned onto the rows.** The forecast, the disagreement and the expiry count are
  made once per built trade day and known from its open. A written row outside a trade day (the 5 pm to 6 pm stretch,
  the Sunday start-up before trade day Oct 2) would otherwise show the previous trade day's figure or none. The
  pinning step states what such rows show.

**Step 1 in git (Greg: "Look in git for step 1"; searched 2026-11-16).** Greg also sent
`NG_EXHAUSTION_CHAIN_PHASE2_GATE_20260817.json`, the gate into Phase 2 of the natural gas exhaustion chain work. Found:
- **What is in git (Markets):** the programs (the frozen detector `research/ng_exhaustion_chain_canonical_table_20260817.py`,
  the 54-week merge and shard, the held week, the Phase 1 agents and the 55-week reconciliation, on branches
  `chatgpt/ng-exhaustion-chain-full-history-phase1-20260817` and `-phase2-20260817`); the freeze records (the 54-week
  base freeze lists the 55 weeks: 2025-06-29 to 2026-07-12, the week of 2026-03-29 held aside and inserted later); the
  gate and its Step-0 verification (235,170 events over 55 weeks, no mismatches); the Phase 2 findings documents; the
  frozen family classifier (`research/FRANKIE_NG_PRE_FAMILY_CLASSIFIER_FROZEN_OPERATIONAL_20260817.json`, families
  A, B, C as centroids over 78 features); and, for the later 2021 census, its programs and summary counts only.
- **What is NOT in git:** the event tables themselves. The 54-week base (231,532 events), the held week (3,638) and the
  reconciled 55-week set were kept only as GitHub Actions artifacts (ids 9281733364, 9281272840, 9306082330). All
  three were checked on 2026-11-16 and return "not found": they are past GitHub's retention. An earlier version of
  the event set (the "V0" data plane, artifact 9274443976) was published to S3 under `nymex/ng_exhaustion/v0/`; no
  workflow in git publishes the 55-week tables to S3. The 2021 census outputs were written to the AWS worker's disk.
- **Which work Greg means by Step 1 is not settled here.** His words in the second session were "the initial 2021
  data"; the file he sent today is the gate of the 2025-26 55-week work. Both are recorded; he decides.
- The gate file Greg sent has the same content as the copy in git
  (`research/NG_EXHAUSTION_CHAIN_PHASE2_GATE_20260817.json` on `chatgpt/ng-exhaustion-chain-phase2-20260817`).
- **What they were made from:** the continuous order-book tape on S3 (`nymex/nymex_cont/`), not the full order tape
  this rebuild uses. That fits Greg's word that the original Step 1 "weren't run on mbo or this depth".
- **So the base can be rebuilt, not copied:** the frozen code is in git, and the gate records the fingerprint of each
  event table (`event_table_uncompressed_sha256`), so a rebuild can be proved identical to the original. The input
  tape is on AWS, which is off limits today.
- **Hard-coded boundaries seen in the Step 1 programs** (for the list owed to Greg): the lineage followed back at most
  5 generations; 52-week and 26-week blocks; a 20-second roll and a 0.85 quantile threshold per UTC clock day; a
  45-second refractory gap; horizons 5 to 300 seconds; a 2-tick material move; the top 10 book levels; weeks and days
  cut on the UTC clock day (against the trade-day rule); the classifier frozen on 2026-08-17.

**The Step 1 outputs Codex found, and how they relate to the four trade days (2026-11-16).** Greg: "Honestly it's fine
if we can find the output data." Codex listed surviving row-level data; the links did not survive the paste, and the
files were found by name in Markets:
- `chatgpt/ng-exhaustion-post-phase2-20260818` at `59c03e8`: `research/generated/ng_exhaustion_exact_d1_master_20260818/`
  (the exact-D1 master ledger, 18,837 rows, its summary, predictor and rankings), the eight D1 analyses
  (`ng_exhaustion_exact_d1_core8_v2_20260818/`, `..._v2_20260818/`), the focused P-O-X ledger of 3,429 events
  (`ng_exhaustion_pox_focused_20260819/`), and the original Step 1 file map
  (`research/NG_EXHAUSTION_CHAIN_STEP1_ORIGINAL_FILE_MAP_20260820.md`).
- `chatgpt/ng-exhaustion-entry-timing-revival-20260818` at `2852f57`: the entry-timing outputs of 2026-08-18 and the
  D1 to D5 predictability follow-up.
- Codex: the full original 235,170-event table remains unlocated.

Two facts read from these files decide how they relate to the four trade days:
- **No shared dates.** The D1 ledger and the entry rows run from the week of 2025-11-02 to the week of 2026-07-12; the
  55 weeks run 2025-06-29 to 2026-07-12; the census is Sep to Nov 2021. The four trade days are October 2023. No old
  row can be laid against a tick row of the four trade days.
- **Trade cost inside.** The ledger's `with_descendant_net_0_5_ticks`, `_net_1_ticks`, `_net_2_ticks` (and the
  `against_` columns) are the move less an assumed cost of 0.5, 1 or 2 ticks (`ng_exhaustion_exact_d1_master_ledger_
  20260818.py`, lines 53 to 57), and the profit rankings rest on them. Under "trade cost is not a market condition"
  those columns and rankings are not carried into new work.

**Correction to the Step 1 note above.** It said the base column "keeps the 2021 base exactly as it was" and that the
base waits on AWS. On a row of an October 2023 trade day there is no old Step 1 value to keep, because the old outputs
are on other dates. What carries over is the definitions (the families, the chain and its stages, P-O-X, lifespans)
and the questions they answer. They are calculated fresh on the four trade days as part 2 calculations, each laid out
Greg's way and approved before it runs, after the list of hard-coded boundaries is put to him. A definition built on a
fixed window (the family rule reads a 20-second roll over the 60 seconds before) cannot simply drop its window; how
each is carried over is worked out then. The old outputs stay where they are, in git, as the record of what the
definitions found on their own dates.

**What depth the Step 1 rerun uses: raised by Greg, 2026-11-16, not yet decided.** "Yes codex was looking. If we have
the correct step1 for these days, absolutely use that. That solves some problems. But we still have to rerun once we
get the depth that we want to get the best output. The run you have didn't use all of the available data. So we have
to decide is full mbo enough or do we need almost all the layers. But we should decide those things first and the
decision will be made based on best output not easiest to do."

Facts checked the same hour, for that decision:
- **No correct Step 1 exists for the four trade days.** The only family work on any of them is Desktop's for trade day
  Oct 18 (Markets `artifacts/sqlite-triage/20261022/families/`): 749 open-world families read out of the old ROOT
  run's derived structures (`.../experiment-roots/e2e-20231018-.../work/derived/.rows/structures.jsonl`). It rests on
  old ROOT output, covers one trade day of the four, and its own audit says the export does not keep the links from a
  family to its birth, timestamps or terminal state. The frozen Step 1 detector and family classifier were never run
  on October 2023.
- **What "the layers" add beyond the full order tape.** Sorting the 99 layers, the 13 outside points and the 19 S
  fields of `LAYER_REGISTRY.json`: 69 are the front-month order tape itself or are worked out from it (L027 to L076,
  S01 to S19: messages, order lives, the full book and its lines, flow, depletion and refill, dipoles, families,
  pre-births, clocks). The full order tape already contains everything they contain. What is NOT on the front-month
  tape: the 13 outside points (X01 to X13, which include the other contract months through the curve). The rest are
  not market data for a tick: reference documents and knowledge (L001 to L023, L081, L082), the 2021 objects and
  Step 1 answers (L024 to L026, L080, L083 to L089), and Frankie's outputs (L077 to L079, L090 to L099).
- Greg's earlier words bear on it: "our full depth of over 100 fields ... should be pinned together before we calc
  things. That's the only way we'll get the true picture. Some calcs may only touch specific pieces but we should
  have the entire picture together"; "everything that we have gets run"; "when we decide ahead of time, we're killing
  our own research silently".

**The depth of the Step 1 rerun: DECIDED by Greg, 2026-11-16.** Asked "the rerun reads everything we hold, and we
judge depth by laying the outputs side by side once the foundation exists?", he answered: "Yes to your question."
- The rerun reads the whole picture: the full order tape with the full book at every tick, and the 13 outside points
  beside it.
- Whether a definition needs a given piece is shown by the run, not decided ahead. "Best output" is judged with the
  same definition run at each depth and laid side by side, event by event, with no scores.
- That comparison needs the foundation, so the foundation is built first, as already decided.

**The two Step 1 columns (Greg, same message):** "So we can use the data you have for the 1st step 1 column and decide
what goes into making 2nd column." Read as, and played back to him:
- **First column:** Step 1 as it was originally defined (the frozen detector and the family rule), made on the four
  trade days from the data we hold.
- **Second column:** the growth. What goes into making it (which depth, which pieces, which cutoffs removed) is
  decided when that calculation is laid out, with the list of hard-coded boundaries in front of him.
- Both are part 2 calculations, after the foundation, each looked at before it runs.
- To raise when the first column is laid out: the original detector sets its threshold from the 0.85 level of a whole
  UTC clock day's readings. Taken over the whole day, that uses readings from later in the day than the tick it is
  applied to, which a row on the timeline may not do.

**`xlrd` (Claude's call, stated to Greg):** the question was put three times with no objection. It is a small
read-only library for the EIA's own `.xls` files and blocks only the storage tables. It is added at the next build
stretch unless Greg says no.

**Merge, not scrap: the Step 1 knowledge base (Greg, 2026-11-16).** "That's fine about not having the old version of
these days. We will run on the new data and use those outputs to expand on the 55 wk findings and research along with
last week's to come up with a new step 1 outputs knowledge base instead of scrapping our prior work we'll merge. If
there's conflicting findings for things, do a deeper dive. Chances are it's just the new run giving a better answer
but it could be 2 outcomes on what looks like exact situations. Do you have a clean way to merge everything or does
the months old data create problems while also adding nothing? You tell me".

Claude's answer, given to him the same hour (a proposal until he says yes; no specification is written):
- **The old work adds something the four trade days cannot:** breadth. 55 weeks and 235,170 events against four
  trade days; things too rare to appear in four trade days (the gate counts chains 4 deep 9 times and 5 deep once in
  about 153,000); and the vocabulary itself (the families, the chain states P, O, S, X, the repeating pairs and
  triplets).
- **It causes problems only if it is merged as data.** It was measured with a different instrument (one reading a
  second, the top 10 levels, fixed windows, UTC clock days) on different dates, and part of it is stated as lift
  ratios, model scores and profit rankings with assumed costs, which Greg's rules keep out as findings.
- **The clean way:** the knowledge base is a list of statements, never mixed rows. Each old finding enters as one
  statement carrying what it was measured on (dates, tape, definition). Each new-run result is attached to the
  statement it bears on. A statement is then confirmed, sharpened, in conflict, or not seen yet. "Not seen yet" is
  its own status for things too rare for four trade days; it is not a contradiction. Ratios, scores and rankings
  enter as questions to re-ask per event, not as findings.
- **A conflict gets the deeper dive, by cause:** the definition, the depth, the dates, or two real outcomes from
  what looks like the same situation. The two Step 1 columns separate the first two. The dates cannot be separated
  while old and new share no dates.
- **What would make it fully clean, found in git the same hour:** the 5-year full order tape is on S3
  (`nymex/ng_mbo_5y_v0/`, manifest `research/kalshi/NG_EXHAUSTION_MBO_5Y_CANONICAL_OBJECT_MANIFEST_20260822.json`:
  1,565 daily objects, Aug 2021 to Aug 2026, 26.6 GB). It covers every one of the 55 weeks and every weekday of
  October 2023. So the new ROOT can later be run on the old weeks themselves, and old and new measured on the same
  events. It also lets the first Step 1 column be proved a faithful copy, by running one old week through it and
  matching the gate's fingerprints. Both need AWS, which is off limits today.
- **"Last week's" has two readings:** Desktop's family work for trade day Oct 18 (still in Markets), or the Codex and
  Claude research results removed from the branch today, which Greg had ruled not kept. Nothing is lost either way:
  the removed files are in the commit before `ee4da3f` and on three older branches. Nothing is restored without his
  word.

**Step 1 and Step 2 calculations in one run (Greg, 2026-11-16):** "And if we can consolidate step 1 and 2 calcs into 1
run do that". It matches his earlier rulings ("there's no reason to do 2 separate runs"; "do them all at once instead
of split up").
- Read both ways, with the same answer: the two Step 1 columns (the original definition and the growth), and Step 1
  together with the Phase 2 calculations that were run after it (the chain, its stages, timing and recurrence), are
  made in the same single pass over the timeline wherever that can be done.
- How: each stays its own named calculation with its own columns and its own checks, as the shape of part 2 says.
  One pass walks the ticks once; at each tick the calculations run in a fixed order, so one that reads another's
  column runs after it. Nothing is walked twice.
- Where it cannot be one pass (a definition that needs something only known later, such as a threshold taken over a
  whole day), that is put to Greg when the calculation is laid out, not worked around.

**An exception to the no-averaging rule, inside Step 1 (Greg, 2026-11-16):** "There is an exception to my long
standing rule. I think there's a calc in step 1 that does averaging because it adds something in addition to not
averaging the same data. I think it does it both ways for different answers so note that."

- Where a Step 1 calculation works the same data both ways, averaged and not averaged, and the two give different
  answers, both are kept. The averaged form is not removed under "no averages": it is its own calculation with its
  own column beside the un-averaged one, and it never replaces the individual values.
- Which calculation it is has not been confirmed; Greg said "I think". It is identified when the Step 1 calculations
  are laid out, and shown to him as such. Candidates seen in the Step 1 programs, not yet confirmed as the one he
  means: the 20-second roll of the per-second signed flow, which sits beside the per-second values themselves; and
  the family rule, whose families are centres worked out over many events.
- The exception is for that calculation only. The rule stands everywhere else: every trade individually, no rates,
  averages or model scores as a readout.

**Closing decisions of the fourth session (Greg, 2026-11-16):** "We'll wait on the full tape to see if we need it and
we'll run the steps on all 4. Also mention that we need to eliminate all caps and limits and that the new data
shouldn't be limited to what fits in old groupings. The new stuff will have new groups, families, chains, additional
definitions probably. We let the data make the decisions unless it looks like it'll go out of control, then we'll
figure something out."

- **The other contract months' full order tape is not bought now.** It waits until the work shows whether it is
  needed. (Quoted at $4.83 on 2026-11-16.)
- **The steps are run on all four trade days.** The families are grown from the four.
- **All caps and limits come out.** No cap on how far a lineage is followed, no fixed block lengths, no fixed windows,
  no top-N levels, no threshold that keeps an event from being recorded. The list of hard-coded boundaries in the
  Step 1 programs is the list of what comes out.
- **The new data is not forced into the old groupings.** Old families, chains and definitions are the base, not a
  mould. Where the new data shows a group, a family, a chain or a behaviour the old set has no place for, it gets a
  new one, and a new definition where one is needed. Nothing is dropped or squeezed into the nearest old label
  because it does not fit.
- **The data makes the decisions.** The one stop: if something looks like it will run out of control (the number of
  groups, the depth of a chain, the size of the output), the work stops there and it is put to Greg, and a way is
  worked out with him. No limit is put in quietly to keep it manageable.

**AWS (Greg, same session):** "Aws is unavailable so don't try it." One read-only listing was tried at the start of
the session and asked for a sign-in. No further attempt is made until Greg says so.

**Question 2, the 13 outside data points while AWS is unavailable: ANSWERED by Greg's three instructions.** "Why
can't the 13 dp files be made or checked until aws is back? They should already be made and if anything is missing
find the data out there and fix it." "Save those files to git please." "Rebuild the files so we can add them to the
excel sheet." So the outside data is not deferred: it is fetched from its original sources now, saved to git, and
the 13 are rebuilt from it.

**State at the end of the fetch (2026-11-16).** The published source files are in git at
`data/outside/ng_oct2023/` (84 files, about 30 MB, with `MANIFEST.json`, `README.md` and the fetch program). They
are source files exactly as served; no value is calculated yet. Read and confirmed to cover the four trade days:
positioning (X01, X03, X04, X08), forecasts (X02, X09), observed weather (X10), the hourly grid data for six regions
(X05, X07) and weekly storage (X11). The EIA's own file `revisions.xls` holds each week's storage LEVEL as estimated
before any revision (checked on the week ending Jan 20, 2023: 2,729 there, 2,734 in the history), so the level as
first printed does not need the Internet Archive. The weekly change and the five-year comparison exactly as printed
are not in that file. On the usual weekly timetable no positioning report and no storage report comes out inside
any of the four trade days. Still missing, with the reason in the README:
the street estimate for X12 (needs `web.archive.org`), the time each
October 2023 positioning report was published, and a US48 total for the grid data (the file holds 62 balancing
authorities and no national row; adding them up ourselves would be a choice and is not made).

**The `outside` part, group by group (started 2026-11-16).**

- **Positioning (X01, X03, X04, X08): CLOSED by Greg.** "Yes that's right for positioning." On every row, from the
  latest CFTC report known at that tick: the funds' net position (long minus short) in the NYMEX gas contract; its
  change from the week before (X03); where it stands among the last one year (X01) and three years (X04) of weekly
  reports; the same one-year standing for the ICE Henry Hub contract (X08). The published long, short and net
  figures and the number of reports in each window are on the row as their own columns. Window lengths are declared
  by name. Made fresh from the CFTC files in git and pinned on every tick.
- **Greg, same message: "Keep everything as it was in the original 13 dp files."** The 13 keep their original
  content and definitions; they are not redesigned group by group.
- **The four fixes stand (Greg: "A, keep the four fixes").** The 13 are the same as in the original files with
  these four changes on top and nothing else: (1) storage (X11) as first printed on Thursday morning, not the later
  revised figure; (2) the storage estimate against actual (X12) filled in; (3) the temperature (X10) worked out from
  the hourly readings on the gas day ending 10 am Eastern, with wind and carry-over from earlier days as their own
  columns; (4) the published figures underneath each point on the row as well.
- Wind and gas burn (X05, X07): "as it was" means the EIA's own US48 figure, as in the original files, not our sum
  of the regions. Greg gave an EIA key and approved `api.eia.gov` on 2026-11-16; the hourly US48 and six-region data
  and the weekly storage series were fetched the same day (`data/outside/ng_oct2023/raw/eia930/api/`,
  `raw/storage/api/`). The key is in no file. With this, 12 of the 13 have their source files in git; only the
  street estimate (X12) has none, and it waits on `web.archive.org`.

- **`SPEC-outside.md` is drafted (2026-11-16) and is not yet approved.** It states what the original put beside a
  row (30 figures plus an hourly temperature for each of 18 cities), how each point is made, what the four fixes
  change, what is still missing, and four questions that are Greg's to decide: whether a row shows every forecast
  run as it arrives (the original) or the one forecast made before the open (his earlier ruling, which is what
  `SPEC-root.md` section G says today and is pending his answer); which day the forecast describes once the
  observed temperature moves to the gas day; the details of fix 3; and a workbook of the point tables. The source
  folder now holds 127 files: readings for Austin and San Antonio and routine-only hourly files were added.

- **Kept simple for this first ROOT part (Greg, 2026-11-16):** "Just for this initial root part, keep the storage
  and weather forecasts simple. They aren't part of the actual calcs so it's fine for now. We'll update them later."
  So his earlier ruling stands: one forecast per trade day, the last run known before the trade day opens, the same
  on every row of that trade day; and the Thursday storage figure. Every forecast run stays in the point table with
  its time, so nothing is dropped and the later update needs no new fetch. The forecast keeps the original's day and
  method for now. The storage estimate (X12) is not chased now: its column is there, empty, with the reason.
  `SPEC-root.md` section G already says one forecast per trade day and needs no change. The three other questions in
  `SPEC-outside.md` are settled as stated calls in that file (the details of fix 3, and a small workbook of the point
  tables), for Greg to correct when he reads it.

- **`SPEC-outside.md` APPROVED by Greg, 2026-11-16: "Yes I approve it."** This is the first approved part to build.
  It is built on Opus with the Fable advisor. First the 13 point tables and their small workbook; pinning onto ticks
  when the rows exist.

**Making the 13 from these files is the `outside` part of ROOT and is a build:** it gets its short specification
(each point's source, formula and timing, with the fixes already decided), Greg's approval, and then the switch to
Opus. The old builder is not rerun, because it carries what was ruled wrong. The 13 go onto the sheet when the ROOT
build has written the rows; until then what can exist is each point's table of values with the time each became
available.

- The 13 do not wait on AWS. Where a made file or an input cannot be reached, the data is fetched again from its
  original source and anything missing or wrong is fixed.
- What is held where (checked in this session):
  - The made files for the four trade days and the fetched inputs are stored on AWS only
    (`frankie/day_external/`, `frankie/day_history/`, `nymex/ng_fut_parent_v0/`). They are not in either repository.
  - Git holds the programs, for reading: the fetcher `research/kalshi/frankie_boss/operations/fetch_day_history.py`
    and `pull_curve_days.py` (Markets `7f34afa`), and the builder `frankie_day_external.py`.
  - The old workbook holds the 13 on trade rows only, and is not a source (decided earlier).
- Where each point comes from:

| Points | What | Original source | Free? |
|---|---|---|---|
| X01, X03, X04, X08 | positioning (NYMEX and ICE contracts) | CFTC weekly report files, `www.cftc.gov` | yes |
| X02, X09 | forecast temperature, disagreement between models | Iowa State weather archive, `mesonet.agron.iastate.edu` | yes |
| X10 | observed weather, hourly station readings | the same archive | yes |
| X05, X07 | wind, gas burned for power (hourly grid data) | EIA, `www.eia.gov` files or `api.eia.gov` with a free key | yes |
| X11 | weekly storage, as first printed | the level: EIA's own file of original estimates, `ir.eia.gov`; the change and five-year figures as printed: the report page as saved on the Internet Archive | yes |
| X12 | storage estimate against actual | saved pages on the Internet Archive (TradingEconomics, investing.com) and EIA's report | yes |
| X06 | sessions since the front contract expired | the exchange calendar; nothing to fetch | n/a |
| X13 | the futures curve, every contract month | Databento (definitions, statistics, order tape of every month) | paid |

- **The outside data files are saved to git (Greg: "Save those files to git please").** The fetched inputs and the
  files made from them are kept in markets-data, not on AWS alone, with a file list and fingerprints, beside the raw
  order tape, at `data/outside/ng_oct2023/`. GitHub refuses a single file over 100 MB, so large text files are
  stored compressed. Done for the public sources on 2026-11-16 (see "State at the end of the fetch" above).
- Network: the session runs in the "Markets" cloud environment, whose network allows a listed set of sites. A first
  request to add five public sites (with `web.archive.org`) was rejected by the environments service. A second
  request without it was approved by Greg: `www.cftc.gov`, `www.eia.gov`, `ir.eia.gov` and
  `mesonet.agron.iastate.edu` are now allowed. `web.archive.org` and `api.eia.gov` are not; Greg can add them by
  hand (cloud environment menu, Edit, Network access, Allowed domains) if X12 and the US48 total are wanted from
  those sources.
- Databento: the saved key entry was wrong (the right key, saved with a line break and a date after it). Greg
  re-saved it through the secure form on 2026-11-16 and Databento now answers. No key is ever written into either
  repository. Prices quoted by Databento the same day for the futures curve (X13), every natural gas contract month
  (`NG.FUT`), UTC clock days Sep 29, Oct 1 to 3 and Oct 16 to 18, 2023, nothing bought yet: contract definitions
  $0.04; exchange statistics (settlements, open interest) $0.01; trades of every month $0.75; the full order tape of
  every month $4.83 (about 2.9 GB before compression).
- **The futures curve pull (Greg: "Do the 3 now and if we decide we need it we can buy it later").** Pulled
  2026-11-16 for $0.80: contract definitions, exchange statistics and every trade of every contract month, 23 native
  files in `data/outside/ng_oct2023/raw/curve/`, listed in the manifest with fingerprints. Read and confirmed: 146
  outright contract months plus the calendar spreads in each definitions file; settlement-price and open-interest
  records in each statistics file. The full order tape of the other contract months is not bought. The statistics
  files also answer the earlier note under "Held for the later stage": the exchange's settlement prices and open
  interest as published are now held for these clock days.

## Fifth session (2026-11-16, on Opus with the Fable advisor)

**Where things go (Greg, 2026-11-16).** "We made that repo specifically for the data." Asked where the ROOT code is
pushed, he chose: **"Markets (code)". ROOT code goes to Markets on its own branch; only code goes there, never data.
All outputs, tables and documents go to markets-data.**
- The ROOT code from the fourth session (`a1b3ad2`, `6208460`) was brought onto this session's Markets branch,
  `claude/plugin-company-customization-z50yb3` (as `27975f9`, `53469eb`). All 21 tests pass there on the real source
  files.
- How much went to Markets that belonged in markets-data (Greg asked): about 5.9 GB on the trunk, pushed Oct 22 to
  Nov 7: `artifacts/recovered-c-drive/` 4.7 GB, `artifacts/sqlite-triage/` 1.2 GB, `tasks/` 15 MB. The code is
  about 4 MB. The rule "Markets is code only" is now in Markets `CLAUDE.md`, a new `AGENTS.md` (for Codex), the
  `repo-conventions` skill and `.gitignore` (trunk `da0101c`).
- **The sqlite-triage outputs (Greg):** "We can probably delete sqllite outputs because we ran it on bad data and ran
  it for wrong hrs. We want to keep the run code though to make changes to." The split of that folder into run code
  and outputs is put to him before anything is deleted.
- **The move off Markets:** Greg chose S3 for the large parts plus markets-data for the rest, then: "Aws not
  accessible, forgot." So the move waits on AWS for the large parts; nothing has been moved or deleted yet.

**The sqlite-triage outputs: DELETED (Greg, 2026-11-16).** "Inspect the code the sql files ran on. If it was using
incomplete data, then we scrap the outputs and fix the code to run right." It was: the SQL triage read the old ROOT
search database (`experiment-search/20231018/cycle-00/discovery.partial/recovery/indexed-v1/cells.sqlite`, one trade
day, a partial run that was recovered) and the family research read the old ROOT run and teacher rows for Oct 18
only. Greg: "Delete output and md." Markets trunk `420fd65`: 1,514 files, about 1.2 GB (outputs, 818 Markdown and 29
text notes); the 286 code files kept. "We will have to make notes to track down where these old files are being read
like the old root jsons": `root-audit-20261116/OLD_INPUT_READS.md` (170 programs). Fixing that code means rebuilding
it as part 2 calculations on the new rows, after the foundation.

**Compute for the runs (Greg, 2026-11-16).** "We have money on the pods so if they will do the st1 and 2 calcs a lot
faster do that. Or use the git box." Then: **"We can use 4 boxes and run them all in parallel." "Do it."**
- Four boxes, one per trade day, run at the same time.
- The book is the week, so each box walks its own week from the Sunday start-up and writes rows only for its own
  trade day. CORRECTED the same session (see "No commingling" below): the warm-up ticks go through the BOOK only.
  A calculation starts at the first written row of its week (the Sunday start-up for week 1; 5 pm Eastern Mon Oct 16
  for week 2). The Oct 3 box reruns its calculations over trade day Oct 2 (one of the four) so its output is identical
  to one long run; the Oct 17 and Oct 18 boxes walk Oct 16 through the book only, and their calculations cover only
  written rows (Oct 17, and for the Oct 18 box Oct 17 and 18). The "same result twice" check proves each box.
- How it is started: a GitHub workflow uses the saved `RUNPOD_API_KEY` to start CPU pods; each pod takes the code
  from Markets and the tape from markets-data, runs, pushes its outputs to markets-data and shuts itself down.
- Prices read 2026-11-16: CPU pods $0.03 per CPU-hour (compute-optimized), so about $1 an hour per 32-CPU pod, about
  $4 an hour for four. Last week's three 32-CPU pods (Nov 8 to 9) cost $39 in about 13.5 hours. Four pods tried in
  US-CA-2 on Nov 16 never started, so another US data center is used. Greg sees the pod type and the total before
  anything starts. The GitHub runner (4 CPUs, 6 hours a job) stays the fallback.
- The endpoint `frankie-reading-granite42` is the Granite reader on a GPU, not a box for ROOT.

**Every calculation is inspected before it runs (Greg, 2026-11-16).** "Before we run these let's take a look at the
calcs to make sure they're doing any we need." Then: "Build it and we also need to inspect st 1 and 2 calcs before
running." So each calculation is laid out (what we want, what the original did, what changes) and Greg says yes
before it is built or run. The Step 1 and Step 2 calculations get the same inspection before anything runs; laying
them out is gameplan work, done on Fable.

**Storage (X11, X12): laid out, approved ("Build it"), BUILT (2026-11-16).** Markets session branch, `root/outside.py`;
tables in `data/outside/ng_oct2023/made/` (`storage_weekly.csv`, `storage_estimate.csv`).
- Level as first printed: `revisions.xls` holds the EIA's first print for every week from 2015-06-19, so the printed
  pages are not needed for it. Week ending 2023-01-20: first print 2,729, later revised to 2,734.
- Change on the week: this week's first print minus the week before's. It is not called "as printed": in the week
  after a revision the printed change used the revised level (2023-01-27: -146 here, -151 by the EIA). Since 2015 that
  happens on 28 weeks; in 2023 on Jan 20, Jan 27, Jun 30 and Jul 7, none near the four trade days. The EIA's current
  change is a later figure, so it is in the receipt as a check and on no row.
- Five-year comparison: the original's fallback exactly (same ISO week number, five prior calendar years, empty
  unless all five; the five listed). The prior years use the EIA's current values (Claude's call, stated to Greg;
  their first prints are available if he prefers).
- Release time: Thursday 10:30 am Eastern after the week, marked as a rule. Holiday weeks can move it; no shift of
  Sep 28 or Oct 12 could reach into a trade day.
- The four trade days carry: Oct 2 and 3 the week ending Sep 22 (3,359; change 90; five-year +199.0); Oct 17 and 18
  the week ending Oct 6 (3,529; change 84; five-year +168.6). No report comes out inside a trade day.
- Street estimate (X12): empty on every row with its reason (needs `web.archive.org`).
- The history file and the EIA API series agree on all 480 shared weeks. 27 tests pass on the real files; the 16
  earlier tables are byte-identical to the previous build.

**The tape part: BUILT (2026-11-16, Greg: "Do it").** Markets session branch `8333ed0` (`root/calendar.py`,
`root/tape.py`, `root/run.py`); check-week records in `receipts/`.
- **The Sunday re-listed orders carry the vendor's snapshot flag** (the handoff's question): 342 orders on Sunday
  Oct 1 and 350 on Sunday Oct 15, right after the exchange's clear, which is not flagged. They also carry the flag
  saying the received time is unreliable (the clear too). **Claude's call, stated to Greg:** they are the exchange's
  Sunday start-up, as he ruled, so they are ticks with start-up rows; their flags stay on the row. Classification is by
  file and position, never by the flag alone. The unreliable received time matters when the 13 are pinned by received
  time on those rows.
- Every later file opens with the vendor's restatement: a flagged clear and 696 to 740 flagged orders, received
  exactly at 8 pm Eastern (00:00 UTC). These go to the snapshot table and never reach the book.
- Refused with the file named: a missing file, a changed fingerprint, a count that differs from the manifest, a
  file that does not open as above, a flagged record later in a file, a second contract in a week. The held tape
  triggers none of the last three; they are listed as never exercised.
- Facts read: one contract all four trade days (instrument 150611); no record carries the vendor's "maybe bad book"
  flag; actions are adds, cancels, modifies, trades, fills and the exchange's "none" messages; the only clear is the
  Sunday one. Per box, every tick is written, warm-up or shelved, and the counts add up exactly.
- **Speed:** a whole week reads, checks and labels in 8 to 22 seconds here (about 4.3 million records in the seven
  files). The foundation does not need pods; whether the calculations do is measured when they are built.

**No commingling: the warm-up ticks are warm-up only (Greg, 2026-11-16).** "We are only running data runs that we
will use for the 4 days. Any calculations that you need to fill in book data will be kept separate from the 4 day
data. I want to make sure this is very clear. The warm up days are only warm up days. No data is comingled."
- The warm-up ticks (Sunday Oct 15, trade day Mon Oct 16, the shelved hours after 6 pm Eastern on the evenings of
  Oct 2, Oct 3, Oct 17 and Oct 18) are run through the book so that it is complete, and for nothing else. No row is
  written for them; no calculation runs on them; nothing from them enters the four trade days' rows, counts, checks
  or calculations.
- The one thing that crosses is the book itself, as already ruled: an order that entered during warm-up and is still
  resting shows on a written row in its line, with its entry time and the mark that it entered before the written
  record. That is the true book, not a calculation.
- Anything ever calculated on warm-up ticks to fill in book data is kept completely apart: its own output, its own
  workbook, never joined to the four trade days.
- The check-week records count warm-up and shelved ticks only to prove every record of a raw file is accounted for
  (success criterion 1); those counts are bookkeeping about the input files, not data about the four trade days.
- A statement written earlier the same session ("the Oct 18 box through Oct 16 and 17" for calculations) was wrong
  and is corrected above.

**Only the four trade days enter a calculation: SHARPENED and ENFORCED (Greg, 2026-11-16).** "The warm up starts on
those days but none of the hours outside of the 4 trade days are used in our calculations. I've repeated it multiple
times but I'm getting more and more nervous that it's not going to be adhered to. Do whatever you have to do to make
this happen." Then: "Those are only used in our calculations that will affect our research and analysis and creation
of trade strategies based on trade signals that we discover in this 4 day exercise. I don't know if you will have to
use prior days for book info that will be then used in our 4 day data or not. But anything other than that if it's
needed must be discussed with me first."
- Only ticks inside the four trade days (6 pm to 5 pm Eastern on Oct 2, 3, 17, 18) enter any calculation that feeds
  research, analysis or strategies. This is stricter than the note above ("a calculation starts at the first written
  row of its week"): the 5 pm to 6 pm stretches and the Sunday start-up keep their marked rows, and nothing is
  calculated on them.
- Data from outside the four trade days may be used for one thing: seating the book so it is complete on the four.
- Any other use of outside data is put to Greg first, before it is built.
- Enforced: `root/tape.py` `for_calculations()` is the one gate a calculation receives ticks through (tested on the
  real tape for all four boxes); calculation modules live in `root/calcs/` and a test fails if one reads the tape
  itself; the rule is in Markets `CLAUDE.md` and `AGENTS.md` (session branch; not yet on the trunk).
- Greg, same day: "There's a possibility that trades will continue to the next days beyond the 4 but we'll cross that
  bridge if we come to it." Nothing is built for it now; when it comes up it is put to him first.
- **ANSWERED by Greg: "Yes use forward contracts."** The curve stays as approved, with the two points below.
  The question as put: the futures curve (X13) uses forward-contract data from just
  outside the four trade days: at the open of trade day Oct 2 the settlement shape is Friday Sep 29's settlement, and
  on trade day Oct 17 the back months' last-trade prices start as their last trades of Mon Oct 16. Both are in the
  approved `SPEC-outside.md` (call 3) and are figures known at that moment. Asked: keep, or start each trade day's
  curve empty. The other outside points also rest on earlier published reports by their definitions (positioning's
  one-year and three-year standing, storage's five-year comparison, weather's two gas days of carry-over, the
  forecast run made before the open), all as approved in that spec.

**The other contract months' full order tape: still not bought (Greg asked again, 2026-11-16: "Do we need the full
tape? ... Haven't heard definitely").** Claude's answer: not for anything built or specified so far. The foundation's
rows are the front-month tape; the curve needs only the settlements and trades of the other months, which are held.
It would be needed only if a Step 1 or Step 2 calculation reads the ORDER BOOK of another month (its depth, lines or
order lives), not just its prices. That is known when those calculations are laid out; the definite answer is given
to Greg then. If bought, it covers the same UTC clock days only ($4.83 quoted, about 2.9 GB before compression).

**The book part: BUILT (2026-11-16, Greg: "Yes and start").** Markets session branch `2a9df15` (`root/book.py`);
check-book records in `receipts/`. Also done on his yes: the four-trade-days rule is on the Markets trunk (`012586b`,
`CLAUDE.md` and `AGENTS.md` only).
- The rule is written fresh from the exchange's priority rule and passed on the first run: at all five later-file
  boundaries (Oct 2, Oct 3, Oct 16, Oct 17, Oct 18 files) our carried book equals the vendor's restatement exactly:
  the same 696 to 740 orders, sides, prices and sizes, the same order in every line, the same place time for every
  order. No restatement is ever applied to the book.
- The book adds up: the running whole-book figures equal a fresh count at every file boundary and at every trade
  message (38,374 to 108,324 trade messages per box).
- No message was left unapplied: no add for a known order, no cancel or modify for an unknown one, no cancel for
  more than was resting, on either week.
- The exchange's sequence number goes backwards 101 times in each week, all inside the Sunday start-up block, where
  the re-listed orders are grouped by price and not by sequence number. None in trading. Those rows will carry the
  irregular mark, explained on the README page.
- Read from the tape for the `rows` part: every fill is followed inside the same exchange event by the cancel of
  that order (fully filled) or by a modify to a smaller size (partly filled), so "left by fill" against "left by
  cancel" is read from the tape, not assumed. Some trades and fills carry no side and no order number (implied or
  spread trades); they are kept exactly as the tape gives them.
- The checks walk the warm-up ticks too, because the book has to be right when the written rows start. That is the
  one permitted use of data outside the four trade days (seating the book); nothing else is made from it.
- Speed: a week's book pass takes 2 to 3 seconds here; with the every-trade check, 13 to 36 seconds per box.

## Held for the later stage: figuring out what moves the market

Greg: "So keep that in mind for later." "And same for storage. Simple is fine in root stage. Those 2 things will be
more important when we get to the figuring out what moves the market stage."

In the ROOT stage the forecast and storage are kept simple: one forecast per trade day, and the Thursday storage
figure. To bring back when the work reaches what moves the market and price-curve forecasting:

- **Forecast:** follow each new model run through the day (the market trades the change from run to run); obtain the
  European model runs and the many-run averages.
- **Storage:** the expected figure against the actual one (the surprise, X12), the comparison with the five-year
  average, and a daily supply and demand balance (production, LNG plant intake, pipeline flows, gas burned for power).
- **The exchange's own status and statistics messages** (when the market is in pre-open or open, the settlement
  price as published, open interest). Raw exchange data, not in the MBO files held. Check whether the curve inputs on
  S3 already hold them once AWS is reachable.

## Parked by Greg (do not raise unless he asks)

- Downloading the five weekday files that would complete both weeks (UTC clock days Oct 4, 5, 6, 19, 20; about 8 cents
  each). They do not change any output for the four trade days. An order still resting at the end of trade day Oct 3
  or Oct 18 is recorded as still open at the end of the record.
- How the exchange handles the clock-change days. Not an issue for the four trade days. Look it up at CME when a trade
  day outside these four is first built.
- Workbook columns for an order's first entry time and for the second clock. For the sheet-refill step, later.

## Session notes

- The trade-day rule in Markets `CLAUDE.md` was updated on Greg's word at the end of the session ("Update trade rule
  in md"): 18:00 ET to 17:00 ET, the 17:00 to 18:00 ET hour its own stretch, the book the week. Trunk `c056e7e`;
  research branch and session branch `b39ff01`.

- The session runs in the "Default" cloud environment, where the Databento address is refused. Nothing needs pulling
  for the four trade days. A pull would need the "Markets" environment, and the key saved there still has to be
  corrected.
- Model: Fable for the gameplan, inventory and specs, with the advisor set to Fable. The switch to Opus with the Fable
  advisor comes when the first approved module is built.
