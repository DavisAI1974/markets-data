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

**What the old ROOT does today**
- It takes in the tape and nothing else.
- The 13 outside data points and the other fields were attached near the end of the chain, by a separate step, and
  only to trades (the 141-field grid; `OLD_ROOT_LINEAGE.md` section B, steps 5 and 6).

**What changes**
- The pinning moves to the start, is done once, and covers every tick.

**Proposed check for "pinned correctly"** (Claude's proposal; Greg has not corrected or confirmed it line by line)
- Every value sits on the tick it was calculated at, with both clocks and its tape position.
- No value used data that arrived after its tick.
- Every tick is accounted for: where a value does not exist at a tick, that is marked with the reason.
- The counts add up: ticks in, ticks on the timeline, values pinned.
- Running the stage twice gives exactly the same result.

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
- Each value holds, unchanged, on every tick from the moment it takes effect until the next value replaces it. Each
  point changes at its own pace (the storage number weekly, a forecast temperature hourly).
- They are pinned fresh onto the new timeline from the outside data files. The old sheet's copy, attached to trades
  only, is not carried.
- Claude's earlier note stands as information only: several of the 13 are worked out by our own builder from published
  numbers (1-year and 3-year positioning percentiles, a week-over-week change, estimate against actual, a curve
  shape). Greg has chosen to pin the 13.
- Still to do (reading only): read the builder (`frankie_day_external.py`, Markets `7f34afa`) for each point's
  publication time and pace, and find where the outside data files for the four trade days are kept. A value that
  cannot be found stays empty with a note.

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

**What the old ROOT does today** (read at Markets `7f34afa`,
`research/ng_exhaustion_mbo_v4_state_adapter_20260820.py`, and pin `2ebb8ce8`, `native_rt_book.py`,
`native_full_capture_adapter.py`, `native_replay_driver.py`)
- The rule that applies each message to the book is sound (adapter lines 421-531); it matched the exchange on every
  order checked on 2026-11-16.
- The book was restarted inside every trade day at 00:00 UTC (from the 2026-11-16 audit of the ingest; not re-read in
  this session).
- The book is only looked at when an exchange event closes (adapter 596-598, 709-735).
- What is written out is the top 10 levels (adapter 648-659, 730), with each level summarized (front order, median and
  90th-percentile queue age, largest share; 615-631) instead of listing its orders.
- Each order keeps one time, the receive time at which it last took its place in line (adapter 157-166, 431-433,
  483-485). Its first entry time is overwritten when it loses its place, and the exchange's event time is not kept on
  the order.
- Three separate books are kept for the same market (driver 505-516).

**What changes**
- One book. Read after every tick. Every level and every order. No restart except Sunday's.
- Both clocks and both times (first entry, last place in line) on every order.

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

**What the old ROOT does today** (read at the same two revisions)
- The book rule works out, for every message, the size before and after, the change, whether the place in line was
  lost, whether the order left, whether the reference was missing, and the best price just before (adapter 169-182,
  439-531).
- The basic adapter then discards it (adapter 827). The full-capture wrapper keeps it (wrapper 458-460) but hands it
  out bundled at the close of an exchange event (wrapper 602-631), and only on the "bedrock" path, which the
  experiment ROOT ran with switched off by default.
- An order's place in line just before a message is worked out only in a second book, for the queue section
  (`native_rt_book.py` 159-187; driver 1400-1405).
- A message that fails to apply is written to a failure list and skipped, and the run carries on
  (`frankie_box_boss_session.py` 836-840). The stand-alone adapter program skips records that are not order messages
  without counting them (adapter 912-913).

**What changes**
- The record is written for every tick and kept, never bundled or discarded.
- Place in line is on every tick.
- Nothing is skipped; a message that cannot be applied is still recorded, with the reason.

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

**Group 3, the book columns (L039-L046): laid out for Greg, not yet closed.** Proposed row content: best bid, best ask
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

## Piece 3 (WITHDRAWN as first drafted)

The first draft of "what ROOT reads off the book" was the old ROOT's book readings with edits (best prices, top-10
and whole-book totals, imbalance, per-level summaries, up/down labels). That carried the old ROOT forward, so it is
withdrawn. What ROOT calculates after the book and the per-tick record is decided fresh. The shape agreed on
2026-11-16 (second session) already names the next fresh piece: every change of state the tape shows (a level
appears or empties, the best price moves, an order joins, shrinks, grows, moves or leaves, the front of a line
changes), each at its own tick, defined from the tape and not from the old sections.

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

- The 2026-11-16 trade-day rebuild cut each trade day at 5 pm Eastern on both sides, so its message counts
  (820,642 / 879,830 / 846,406 / 771,787) include the 5 pm to 6 pm hour at the front. With the trade day as 6 pm to
  5 pm and that hour as its own stretch, the per-trade-day message counts are restated. Trade counts do not change,
  because no trade falls in that hour. `SPEC-tape-stream.md` criteria 1 and 7 are to be rewritten accordingly.
- `CAPABILITY_MAP.md` draft 2 is to be revised: ROOT calculates.

## Parked by Greg (do not raise unless he asks)

- Downloading the five weekday files that would complete both weeks (UTC clock days Oct 4, 5, 6, 19, 20; about 8 cents
  each). They do not change any output for the four trade days. An order still resting at the end of trade day Oct 3
  or Oct 18 is recorded as still open at the end of the record.
- How the exchange handles the clock-change days. Not an issue for the four trade days. Look it up at CME when a trade
  day outside these four is first built.
- Workbook columns for an order's first entry time and for the second clock. For the sheet-refill step, later.

## Session notes

- The session runs in the "Default" cloud environment, where the Databento address is refused. Nothing needs pulling
  for the four trade days. A pull would need the "Markets" environment, and the key saved there still has to be
  corrected.
- Model: Fable for the gameplan, inventory and specs, with the advisor set to Fable. The switch to Opus with the Fable
  advisor comes when the first approved module is built.
