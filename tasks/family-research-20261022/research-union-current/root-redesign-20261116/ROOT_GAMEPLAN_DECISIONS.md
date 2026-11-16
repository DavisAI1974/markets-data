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
