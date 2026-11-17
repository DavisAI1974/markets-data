# Step 1 and Step 2 calculations: the layouts as put to Greg, and his answers

Each calculation is laid out his way (what we want, what it did, what changes) and approved BEFORE it is built or
run. Nothing here is built until its status says APPROVED. Rules that govern all of them are in
`ROOT_GAMEPLAN_DECISIONS.md`: only the four trade days enter a calculation (through `tape.for_calculations()`); a
row holds only what was known at its tick; nothing is written back onto an earlier row; empty cells are never
counted; every trade individually; the caps and limits come off the outputs; trade cost is not a market condition.

"What it did" is read from the frozen programs on Markets branch `chatgpt/ng-exhaustion-chain-phase2-20260817`
(`1bec694`), `research/ng_exhaustion_chain_canonical_table_20260817.py` and the programs it calls.

## Piece 1: the flow and the exhaustion peak (Step 1)

Status: APPROVED by Greg, 2026-11-16 (seventh session): "Yes rewrite", "Yes". BUILT and run on all four trade days
(Markets `5aff999`, `root/calcs/flow_peak.py`); see "Piece 1 as built" below.

**What we want.** On every tick row of the four trade days: the signed trade flow as it stands at that tick, and a
mark each time the flow reaches a peak, with its side and size. Every peak is recorded. None is held back.

**What it did.**
- Put every message into a one-second slot of the UTC clock day (one reading a second).
- Called a trade a buy or a sell by its price against the midpoint of the best bid and ask. A trade exactly at the
  midpoint was left out.
- Flow = (bought minus sold) over (bought plus sold), over the last 20 seconds.
- Recorded a peak only if it passed three gates: above the 0.85 level of that whole UTC clock day; the largest
  reading within 5 seconds on each side; and not within 45 seconds of a stronger peak, the strongest taken first
  across the whole week.
- Looked for no peak in the first 60 seconds after the week's first trade or the last 60 seconds before its last.
- Read the book from the top 10 price levels on each side.

**What changes.**
1. The trade day, not the UTC clock day. The flow starts empty at the 6 pm open of each trade day.
2. Every tick, not one reading a second. The 20 seconds are still measured on the clock.
3. The side of a trade is the side the tape gives. Trades at the midpoint are no longer left out. A trade the tape
   gives no side for (an implied or spread trade) stays on its row and is counted on its own; it is in neither the
   bought nor the sold figure (Claude's call).
4. The three gates stop holding peaks back, and none of them looks ahead any more:
   - A peak is written on the row where it becomes known: the first tick at which the flow has come off its high.
     The row names the tick of the high. Nothing is written back onto the earlier row.
   - The 0.85 level becomes a figure on the row: where this peak stands among the readings so far in that trade
     day. (The old level used the whole day, later hours included.)
   - The 5 seconds becomes a figure: how long that reading had been the highest.
   - The 45 seconds becomes a figure: the time since the peak before. No peak is removed because a stronger one
     came later.
   CORRECTED after the build: these figures give the part of each old gate that looks backward (was anything
   larger in the seconds before; where the peak stands so far). The part that looked forward (nothing larger in
   the 5 seconds after; no stronger peak later) is not on the peak's own row, because it is not known yet; a
   reader finds it on the rows that follow. And the flow itself differs from the old one (the tape's side, every
   tick). So the old events are not reproduced one for one. What the gates threw away is there.
5. No dead time at the start or end of a trade day.
6. The whole book, not the top 10 levels (the row already carries it).
7. The 20-second roll stays. It is the definition of the flow: without a span there is no flow, only single
   trades. It sits beside the single trades, which are already on their own rows. CONFIRMED by Greg, 2026-11-16:
   "I believe that was the exception but there might be another somewhere too." His rule for any averaging: it is
   an addition to the individual outputs, never a replacement of them.

**What it writes.** New columns on every row (no row is added or removed): bought, sold and no-side size in the
last 20 seconds; the flow; and, on a row where a peak becomes known, the peak's side, size, the tick of its high,
its standing so far in the trade day, how long it had been the highest, and the time since the peak before.

**Not promised.** The number of peaks. With the gates off there will be many more than the old events. The count
is reported after the first trade day, and Greg hears before anything is capped if it looks like running away.

### Piece 1 as built (2026-11-16): Claude's calls, stated to Greg, his to correct

- The 20 seconds are measured on the received clock (when each trade could be known). The original used the
  exchange's time. The received time never goes backwards on these trade days; the program stops if it does.
- A trade side of B on the tape is the aggressor buying. Checked on trade day Oct 2: of 18,534 B trades, 17,731
  printed at the best ask and 254 above it, none at the bid; of 17,363 A trades, 16,440 at the best bid and 390
  below it, none at the ask.
- "Where the peak stands so far" is a share of TIME: of the time so far in the trade day while there was a flow,
  the share during which the flow was smaller than this peak. (The approved wording said "among the readings so
  far". The original level was taken over one reading a second, which is time; counting ticks would weight busy
  minutes more.)
- "How long it had been the highest" is the time since the flow was last strictly larger. An equal reading does
  not count as larger. When it never was larger in the trade day, the figure is the time since the first trade and
  a yes/no column says so.
- A peak becomes known at the first tick where the size of the flow is lower than at the tick before, or the flow
  has gone empty. If the flow holds level, the high is the first tick at that level.
- A high that has not come off by the last tick of the trade day (5 pm) is not written as a peak: there is no row
  inside the trade day on which it could become known. The receipt says whether one was standing. Trade days Oct 2,
  3 and 17 each ended with one; Oct 18 did not.
- The flow starts empty at the first tick of the trade day. Trades the tape gives no side for are counted in their
  own column.

**Corrected after piece 2's check (same session).** As first built, a high was judged on the size of the flow
alone. When the flow changed side at an equal or larger size (all buying turning to all selling in one tick), the
high was carried across the change: the peak became known late, or was not recorded at all. Piece 2's recount
found facts that came before their own peak was known, which exposed it. Now a change of side ends a high, and the
flow on the new side starts its own. All four trade days were run again and the earlier piece 1 files replaced.

Results (each in `CALC-flow_peak-<trade day>.json` on its `root-rows` branch):

| Trade day | Rows | Peaks | Peaks as first built | Recount | Playback |
|---|---:|---:|---:|---|---|
| Mon Oct 2 | 820,670 | 9,525 | 8,894 | equal on every row | equal at two cuts |
| Tue Oct 3 | 879,497 | 10,577 | 9,910 | equal on every row | equal at two cuts |
| Tue Oct 17 | 846,158 | 8,619 | 8,051 | equal on every row | equal at two cuts |
| Wed Oct 18 | 771,468 | 7,967 | 7,423 | equal on every row | equal at two cuts |

36,688 peaks over the four trade days, about one every 9 seconds. The old detector recorded about 850 a UTC
clock day. About 21 to 32 seconds a trade day to run. The check also caught one fault on its first run (a peak's
standing left out the stretch of flow still running at the tick it became known); fixed before anything was stored.

## The rest of Step 1, laid out together (Greg, 2026-11-16: "Let's do the rest of the st 1 calcs plan in this next swoop so we aren't doing a piece at a time")

Status: piece 2 APPROVED by Greg 2026-11-16 ("Build"), BUILT and run on all four trade days (see "Piece 2 as
built"). Piece 3 not built (his rule on labels). Piece 4 decided as B, to be laid out in detail next.

"What it did" is read from the same frozen detector and the programs it calls (the fade-timing functions, the
frozen family rule and its two rule files), and from the lineage programs of 2026-08-17.

### One thing that shapes all three: where a fact about a peak is written

In the old work each event was one line, filled in afterwards with everything that happened in the minutes after
it. On a tick row that would be writing later facts onto an earlier row. And peaks overlap: on trade day Oct 2 a
new one becomes known about every 9 seconds, and each is followed for minutes.

Claude's proposal, an explicit ask because it changes what is kept beside a row: every fact about a peak is
recorded at the tick where that fact becomes known, and it names its peak (by the tick of the high). The facts are
stored as their own table beside the rows, one line per fact, as the book pictures are: the tick it became known
at, the peak it is about, what the fact is, its value. In the workbook each fact is shown on its tick row. Several
facts can become known on one tick (peaks on the same side end together when the flow turns), so no promise is
made that they fit in one cell; the count is reported after the first trade day. Nothing is written back, no
peak's story is cut short because a newer peak arrived, and Frankie sees each fact at the moment it could be known.

**The halt and the open, for every figure in pieces 2 and 3.** Only ticks inside the trade day enter. A figure whose
stretch would run past 5 pm (the price moves after an ending late in the trade day, seconds 41 to 60 after a late
peak, family A's second label) is empty with that reason. A figure that needs the 60 seconds before a peak is
empty with its reason when the peak comes inside the first 60 seconds of the trade day. A stretch inside those 60
seconds with no flow is filled from the reading before it, as the original did; that is stated on the fact.

### Piece 2: what happens after a peak (the fade, the ending, the after-state, the price after)

**What we want.** For every peak, as it plays out: how fast the flow faded, when it ended, what state it was left
in, and what price did after the ending. Each fact on the row where it becomes known.

**What it did.** For each event, read once a second:
- The fade: the first second at which the flow had stayed at or below 50, 25 and 10 percent of the peak for 3
  seconds in a row, and the first at which it had stayed at or below zero. Looked for only in the 60 seconds after
  the peak, so nothing later than 58 seconds could be recorded.
- The ending: the first time after the peak that the flow had been at or through zero for 3 seconds in a row.
- Late pressure: bought minus sold over bought plus sold, in seconds 41 to 60 after the peak. The late book: the
  average book imbalance of the top 10 levels over the same seconds, and its change from the 20 seconds before the
  peak.
- The after-state: one of four fixed names, from whether the flow reached zero inside 60 seconds and the sign of
  the late pressure.
- The price after the ending: the move in ticks at 5, 10, 20, 30, 60, 120 and 300 seconds, with the best and the
  worst move inside each; each called continuation, reversal or chop by a 2-tick rule.
- An event with no reading in its 121 seconds was dropped.

**What changes (REVISED on Greg's word, 2026-11-16: "change this. Let the data be what it is and then we group
after we see how they separate").** No fixed mark is kept. No 50, 25 and 10 percent, no 3 seconds, no seconds 41
to 60, no seven moments, no 2 ticks, no state names, no continuation, reversal or chop. What a peak did is
recorded as it happened, and the grouping is made afterwards from what the data shows.

For each peak, every turn in its story is recorded at the tick it happens, naming its peak:
1. **The fade.** Each time the flow sets a new low since the high: how much of the peak is left, and the time
   since the high. That is the whole way down, step by step, with no level picked in advance.
2. **Reaching zero.** The first tick the flow is at zero, has crossed to the other side, or has gone empty: the
   time since the high.
3. **Coming back.** The first tick after that at which the flow is back on the peak's side: how long it had
   stayed away. The 3 seconds becomes a measured length, whatever it turns out to be.
4. **Beaten.** If, before reaching zero, the flow rises above the peak's own size, the peak has been overtaken by a
   larger one: recorded with the time since the high and how far it had faded.
5. **Still open** at 5 pm, if none of those has happened.

Every one of these facts carries, at its own tick: the last trade price, and the highest and lowest trade price
since the high (for "coming back": also since reaching zero). The move in price is whatever it was, in the
tape's own prices. The bought, sold and book figures at that tick are already on the row the fact names.

Where a peak's story ends (Claude's call): at "coming back", or at "beaten", or at 5 pm. Without an end, every
later turn of the trade day would be a fact about every earlier peak. A peak that is never beaten and never
reaches zero stays open to the end of the trade day.

Also as before: read at every tick; the whole book; no peak dropped; nothing from outside the trade day; each
fact stored in the facts table beside the rows. The number of facts is reported after the first trade day, and
Greg hears before anything is capped.

### Piece 2 as built (2026-11-16): Claude's calls, stated to Greg, his to correct

Markets `6a468af`, `root/calcs/peak_story.py`; the runner can now keep a table beside the rows.
- The facts are their own table, one line per fact: the tick it became known, the peak it is about (the tick of
  its high), the kind of moment, the time since the high, how much of the peak is left, and the prices. A column
  on each row gives how many facts became known at that tick.
- The low a rise started from is read on the peak's own side: among the ticks after the high of the peak before
  and before this high, the last one at which the flow on this side was lowest (no flow counts as zero). After a
  peak on the other side, that is where the other peak's high ended.
- A peak's first facts come at the tick it becomes known (its build-up, and its first step down or reaching zero).
- "Beaten" is the flow on the peak's side going strictly above the peak's size before it reached zero.
- A peak whose story has not ended at the last tick of the trade day is listed in its own small file, not on a
  row: there is no tick inside the trade day at which "still open" could become known.
- The kinds of moment (build-up, new low, reached zero, came back, beaten) are kinds of moment, not kinds of peak.
  No peak is given a name, a state or a group.

Results (each in `CALC-peak_story-<trade day>.json` on its `root-rows` branch):

| Trade day | Peaks | Facts | New low | Reached zero | Came back | Beaten | Still open at the end | Most facts on one tick |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Mon Oct 2 | 9,525 | 58,828 | 33,833 | 5,946 | 5,945 | 3,579 | 1 | 25 |
| Tue Oct 3 | 10,577 | 68,185 | 40,754 | 6,278 | 6,277 | 4,299 | 1 | 36 |
| Tue Oct 17 | 8,619 | 53,106 | 30,453 | 5,416 | 5,415 | 3,203 | 1 | 22 |
| Wed Oct 18 | 7,967 | 45,958 | 24,758 | 5,268 | 5,267 | 2,698 | 2 | 25 |

226,077 facts over the four trade days, about six a peak. Nothing ran away and nothing is capped. One check, as
ruled: every fact found again by a second method that looks ahead along whole columns, equal on all four trade
days; playback equal at two cuts. 1.2 to 1.8 MB of facts a trade day; 21 to 31 seconds a trade day to run. The
check found three faults before anything was stored: the piece 1 fault above, and two in how the low was taken.
A fact that can be read from these counts, with no grouping applied: about six in ten peaks reached zero and came
back; about four in ten were beaten by a larger peak first.

### Piece 3: the family (A, B, C). NOT BUILT NOW (Greg, 2026-11-16)

Greg: "we hold off on labels and groups and identifiers until all 4 days have run all their calcs and we'll see how
they define themselves. We don't want to do that for them and that goes for all outputs in st1 and 2." No family
is assigned in advance. In its place, put to him as Claude's call: the build-up of each peak is recorded the way
the fade is, with no mark picked in advance: the low the rise started from (the tick, the flow there, the price
there) and the time from that low to the high. The layout below is kept as the record of what the old rule did.

Greg, same hour: "We have the families from our original st1 run to start with once they are done. We'll see if
they still group like that or differently or the same but with additions. But the old family info will be the
base." So the old family rule is used after all four trade days have run, as the base of the grouping, not inside
the calculations.


**What we want.** For every peak, at the moment it becomes known: which family its build-up belongs to, as Step 1
originally defined families. This is the first of the two Step 1 columns. The growth column (new families from
the four trade days) is laid out after this one is in view, as Greg ruled.

**What it did.**
- Took the flow at each of the 61 whole seconds from 60 seconds before the peak to the peak.
- Turned that curve into 78 numbers: the curve itself two ways (every second reading), and 16 measures of its
  shape (where it started, how far it rose, how early or late it rose, how rough it was).
- Measured the distance from those 78 numbers to three fixed centres, A, B and C, and took the nearest.
- The centres are averages. They were worked out once, on 3,429 events of 2025, and frozen on 2026-08-17. A held
  94 of every 100 of those events.
- Family A alone got a second label from the 60 seconds after the peak (nearest of two fixed centres).
- Every event was forced into the nearest family. There was no "none of these".

**What changes.**
1. The family is written on the row where the peak becomes known. It uses only the 60 seconds up to the high.
2. The three distances are written beside the family, so a peak that is far from all three centres can be seen.
   Nothing is forced silently.
3. Family A's second label is written 60 seconds after the high, when it can be known.
4. The 60 seconds, the 78 numbers and the three centres stay: they are the original definition, and this column
   is that definition. The two frozen rule files are in git and are read as they are.
5. The centres are averages over many events. Under Greg's rule this column is an addition: every peak's own
   curve is on the rows, and the growth column will be made from the peaks themselves.
6. To know when reading the result: the rule was made from the old events, which were about a tenth as many (only
   the largest), and on the old flow (side by the midpoint, one reading a second). It is now applied to every
   peak, small ones included, on the new flow (the tape's side, every tick).

### Piece 4: the link between events (the chain). DECIDED by Greg 2026-11-16: B, with A's two facts.

Greg: "Let it produce full values. That will be the base going forward that we build off of." The detailed layout
(what the models are asked to predict, how they are taught, where the depth stops) is put to him after piece 2
exists, because what a peak "did" is now what piece 2 records. Not built.

The shape, as played back to him:
- What a model predicts: what a peak did (its piece 2 story), from the stories of the peaks before it.
- How it is taught: each trade day's peaks are scored by models taught on the other three trade days, so no peak
  is scored by a model that saw its own trade day.
- What is written, per peak: for each step back, each of the three models' own gain. Full values, nothing thinned.
  No chain depth and no "member of a chain" is written from them (Greg: no labels or groups in advance).
- Where it stops: no depth cap picked in advance. The first steps back are run and shown to Greg, and how far to
  go is settled with him from what the values show.
- When it is known: a peak's link values are known when its own story has ended, and are recorded at that tick.

**The layout, APPROVED by Greg 2026-11-16: "Do it." Not built. It is called "the chain link models" from here on,
because Step 2 now has its own piece B.**

What we want: for every peak, how much knowing the peaks before it helps say what it did. Written per peak, for
each step back, for each of the three models. Full values and no depth number.

What it did: three models (ridge, nearest neighbours, extra trees) predicted what an event did from the events
before it. "What it did" was 22 numbers: same side as the next event or not, and the price move, best move and
worst move at seven fixed moments after the ending. The gain at a step back was the error without that earlier
event minus the error with it. Taught on 18 to 48 weeks; rows above a limit were thinned out; depth stopped at 12;
an event missing any of the seven moments was dropped.

What changes:
1. What a peak "did" comes from piece 2, with no fixed moments. For every peak whose story has ended: its size,
   the time from the low to the high, how its story ended (came back or beaten), how long that took, how far it
   faded, the number of steps down, the price move from the high to the end, the best and worst price along the
   way, and same side as the peak before or not.
2. Taught on the other three trade days: each trade day's peaks are scored by models that never saw that trade
   day.
3. Only what was known: the peaks before are the ones whose stories had already ended when this peak became
   known. A peak's own values are written at the tick its story ends.
4. Nothing thinned, nothing dropped. Every peak with an ended story is scored. The one or two still open at 5 pm
   are empty with that reason.
5. No depth and no "member of a chain". Only the values.
6. How far back: the first six steps back are run and shown to Greg; how much further is settled with him from
   what they show.
7. Model settings stay as the original's fixed lists, chosen inside the three teaching trade days.
It reads the links of Step 2's piece A, so it is built after A. It is the piece for the pods: four at once, one
per held-out trade day. No pod starts without his go at the time.

The choice as it was put:

**What it did.** A chain link was not read off the tape. Three models were taught, on blocks of 18 to 48 weeks,
to predict what an event would do (same side as the next event, and the price moves after it) from the events
before it. An event's chain depth was the number of earlier events, counted back one at a time, for which all
three models predicted better with that earlier event than without it. Depth was followed back at most 12
events (6 in the causal version; the three-month 2021 run capped it at 5).

**Why it cannot simply be run.**
- The models were never saved. Only their settings and results are in git.
- Teaching them again needs many weeks of events. Four trade days are not enough, and the old weeks are on AWS.
- As the 2021 program is written, a run shorter than 53 weeks scores no chain depth at all.
- A chain depth made this way is a model score.

**The choice.**
- A (Claude's recommendation): no model and no depth number on the four trade days. Most of what a link was made
  from is already written by pieces 1 and 2 (the time between peaks; each peak's price moves after its ending). A
  adds two facts per peak: which peak came before it, and whether it is on the same side. The chain depth column
  stays empty with its reason until the old weeks can be run through the new ROOT.
- B: teach the three models on the four trade days themselves and write a depth. It can be done, but it rests on
  four trade days, it is a model score, and it would not be the old chain.
- C: leave the link out of Step 1 for now.

## Step 2 as built (2026-11-16, eighth session): Claude's calls, stated to Greg, his to correct

The layouts are in `STEP2_PLAN.md`, "The suggestions laid out together", approved by Greg. What follows is what
was built, each with its one check passed on all four trade days. Code: Markets branch `ccr-30cca01c-bgs4az`.

### C. The book running totals (`root/calcs/book_totals.py`)

24 new columns on every row: for the bid side and the ask side, size added, pulled, filled and moved since the
first tick of the trade day; each also at the best price (moved has two: left the best, joined the best); the size
put back on orders as they traded; and the filled size whose fill message has no side.

- **One rule for every row.** b is the order's size before the tick, a its size after, f the size the fill
  messages of the same exchange event named for it. Filled goes up by f. What is left is b minus f. If a is above
  that, the difference is added; if below, pulled. If the order changed price, moved goes up by the smaller of a
  and what was left. With no fill this is the handoff's table.
- **A fill is counted on the row where the book shows it** (the order's own cancel or modify), not on the fill
  message's row. That keeps the side's total size equal to its size at the open plus added minus pulled minus
  filled on every row.
- **A fill the book shows no change for counts as filled and as added both** (the open call of the handoff). The
  size put back is kept in its own column. On trade day Oct 2 the rule counts 1,863 rows differently from the
  handoff's table: 1,232 "stayed", 321 "size raised", 126 "price changed", 124 "left by fill", 60 "shrank by
  fill". On every one a fill came with a book change of a different size.
- **A change of price that also changes size** (1,957 on Oct 2): the smaller of the two sizes moved; the
  difference is added or pulled.
- **A fill message with no side** is counted on the side of the order it names, and also in its own column.
- **At the best price.** For an order already resting: its price was the best just before the tick. For an order
  that joins or arrives at a new price: its price is the best just after.
- **Fills are not all at the best price.** On Oct 2, 60,868 of 61,168 rows that show a fill were at the best
  price; 300 were behind it, some far behind (up to 193 levels). Each row carries how far, so nothing is cut.
- More left than was filled on 3 or 4 rows a trade day (an order filled in part and the rest cancelled in the same
  event): the rest is counted as pulled.
- A clear, a message that was not applied, or a fill whose order shows no row in its event would stop the run.
  None occurs on the four trade days.

The check: every column worked out again from whole columns by a different method (the best price taken from the
count of better levels, which the calculation does not read); the foundation's own total sizes on every row; the
size filled against the fill messages; playback at two cuts, one between a fill message and the row where the
book shows it.

| Trade day | Fill messages, size | Counted as filled | Rows with a fill put back | Bid added / pulled / filled / moved | Ask added / pulled / filled / moved |
|---|---:|---:|---:|---|---|
| Mon Oct 2 | 85,688 | 85,688 | 1,763 | 406,585 / 363,428 / 42,718 / 42,000 | 422,692 / 379,439 / 42,970 / 44,240 |
| Tue Oct 3 | 93,202 | 93,202 | 1,634 | 450,069 / 400,670 / 48,889 / 62,455 | 481,132 / 436,600 / 44,313 / 63,687 |
| Tue Oct 17 | 72,782 | 72,782 | 1,440 | 466,967 / 431,411 / 34,830 / 83,280 | 387,389 / 348,961 / 37,952 / 28,451 |
| Wed Oct 18 | 62,673 | 62,673 | 1,527 | 392,063 / 361,298 / 30,249 / 39,891 | 367,409 / 334,662 / 32,424 / 36,589 |

### I, first part. The quote's own runs (`root/calcs/quote_runs.py`)

Facts beside the rows, one line per turn of a run: run started, new furthest price, first step back. The best bid
and the best ask are followed separately. On every row: the run in progress on each side (the tick it started,
up or down, the price before it, how many moves, how far, how long).

- A run is the best price moving one way. It ends at the first move the other way, whatever its size. No minimum
  length and no minimum size.
- A tick that ends one run starts the next. It carries two facts: the step back, then the start.
- **Crossed book** (the best bid at or above the best ask for a moment during a sweep): each side is followed as
  the book has it. No tick is set aside, and every fact carries the gap at its tick.
- A run never crosses 6 pm. A move made by the first tick of the trade day would be measured from a price before
  the trade day and is not counted; none occurs on the four trade days.
- Up and down are read off the prices. They are not groups.
- The calculation reads the best-price columns; the check finds every run again from the foundation's marks of a
  best price moving.

| Trade day | Facts | Runs of the best bid | Runs of the best ask | Ticks with the book crossed | Still going at the end |
|---|---:|---:|---:|---:|---:|
| Mon Oct 2 | 62,505 | 13,332 | 13,680 | 1,858 | 2 |
| Tue Oct 3 | 67,118 | 14,780 | 14,767 | 2,084 | 2 |
| Tue Oct 17 | 67,295 | 14,813 | 13,864 | 1,886 | 2 |
| Wed Oct 18 | 64,050 | 13,877 | 13,268 | 1,910 | 2 |

About three runs in four are a single move. Nothing ran away and nothing is capped.

### A. The links between peaks (`root/calcs/peak_links.py`)

Facts beside the rows. At the tick a peak becomes known: the last peak before it on its own side and on the other
side (the tick of its high, the time between the two highs, the price at its high, whether its story was still
open), and the peak before, same side or not. At the tick a story ends: how many later peaks became known while
it was open, and the first of them.

- "Before" goes by the tick a peak became known.
- "Still open" is read as the stories stand once the tick is done. A story that ends on the tick a later peak
  becomes known is not open for that peak.
- The first peak of a trade day on a side has that link empty, and the fact says why.
- Pieces 1 and 2 are worked out again in the same pass by the same code, so playback covers all of it.

| Trade day | Peaks | Facts | Peak before on the same side | On the other side | Known while the peak before was still open | Most later peaks inside one story |
|---|---:|---:|---:|---:|---:|---:|
| Mon Oct 2 | 9,525 | 19,049 | 6,862 | 2,662 | 6,002 | 112 |
| Tue Oct 3 | 10,577 | 21,153 | 7,843 | 2,733 | 6,619 | 196 |
| Tue Oct 17 | 8,619 | 17,237 | 6,176 | 2,442 | 5,343 | 55 |
| Wed Oct 18 | 7,967 | 15,932 | 5,540 | 2,426 | 5,030 | 68 |

Read from these counts, with no grouping applied: about seven peaks in ten follow a peak on the same side, and
about six in ten become known while the peak before is still open. Overlap is the usual case, not the exception.

### B. The state at each tick (`root/calcs/open_stories.py`)

10 new columns on every row: for buy peaks and for sell peaks, how many stories are open, how many of those have
reached zero and not come back, and the tick of the high of the oldest, the newest and the largest open one.

- The state is read once the tick is done: a peak that becomes known at this tick is open on its row; a story that
  ends at this tick is not.
- Of two open peaks of the same size, the largest is the one known earlier.

| Trade day | Most buy stories open at one tick | Most sell stories open at one tick |
|---|---:|---:|
| Mon Oct 2 | 21 | 24 |
| Tue Oct 3 | 35 | 30 |
| Tue Oct 17 | 20 | 19 |
| Wed Oct 18 | 14 | 19 |

## Additions from the look at Codex's two pieces (Greg, 2026-11-16: "Try them all")

Status: all nine APPROVED to try by Greg, 2026-11-16, seventh session ("Try them all"), from the short form put
to him. Laid out here in full with Claude's calls, his to correct. Nothing is built. They follow the same rules
as everything else: only the four trade days; a row holds only what was known at its tick; nothing written back;
no fixed marks, labels, caps or minimum counts; empty is never zero; every case individually; no cost of trading.
Stored the same way: facts in a table beside the rows, one line per fact at the tick it became known; one check
per part (a recount by a second method, and playback at two cuts).

Named L to O so they do not collide with Step 2's A to K in `STEP2_PLAN.md`.

### Four new calculations

**L. Refilled orders.**
- What we want: every time a resting order is traded against and shows the same size, or more, straight after.
  It marks a price where someone is taking trades and reloading.
- What the rows show (trade day Oct 2): 1,688 fill messages name an order that is not reduced in that exchange
  event; the order's next row reads "stayed" (1,236), "size raised" (321) or "price changed" (126).
- What is written: a fact at the tick of that next row, naming the order (a label): its side, its price, how many
  price levels it was from the best, the size the fill took, its size after, how many times this order has been
  refilled so far in the trade day and the total taken from it so far, and when the order first entered.
- Claude's calls: a refill is a fill message that names a resting order whose next row, in the same exchange
  event, leaves it the same size or larger. A fill followed by a change of price is written as its own kind of
  moment, not as a refill. This also settles the open call in C: such a fill counts as filled and as added, both.
- Needs: the rows. Built with C.

**M. Sweeps, and the moments the quote touches or crosses.**
- What we want: how hard a trade hit the book. A trade that fills through more than one price level is someone
  paying up to get done.
- What is written: one fact for every exchange event that holds a trade, at the tick that ends the event: the
  side of the aggressor, the size traded, the number of resting orders filled, the number of price levels filled
  through, the first and the last fill price, and whether the best price moved. And a fact when the best bid and
  ask touch or cross, and another when they part again, with how long it lasted.
- What the rows show (trade day Oct 2): fills at the best price 60,868; one level back 150; two to five levels
  back 92. The gap is zero or less on 1,858 rows.
- Claude's calls: every trade event gets a fact, not only the ones that go through several levels, so nothing is
  picked in advance. The exchange's own event marks define an event.
- Needs: the rows. Built with C and the quote's runs.

**N. Orders that act together.**
- What we want: which orders are one hand. Orders that enter, move or leave at the same instant are likely placed
  by the same party.
- What is written: a fact for each set of two or more orders whose entries carry the same exchange time, to the
  nanosecond: the orders (labels), their sides, prices and sizes. The same for orders leaving at the same exchange
  time. On a leaving fact: which of them had also entered together.
- Claude's calls: "the same instant" is an exact match of the exchange's own time stamp, so no stretch of time is
  picked. The fact is written at the first tick with a later exchange time, when the set is known to be complete.
- Not promised: how many sets there are. Reported after the first trade day, and Greg hears before anything is
  capped.
- Needs: the rows. Built with K.

**O. What an outside figure changing did.**
- What we want: when one of the 13 outside data points changes inside a trade day, what the flow and the quote
  were doing, and what they did next.
- What is written: a fact at the first tick on which an outside figure on the row differs from the row before:
  which figure, its old and new value, and the time it became known. On that fact line, the peaks in play and the
  run of the quote in progress, as D and I write them.
- Claude's calls: only real changes inside a trade day are written; nothing is written for a figure that does not
  change. What happens after is read from the rows and facts that follow, not copied onto this line.
- Needs: A, B and I.

### Three ways of working, applied to every piece

**Two clocks on every fact.** Each fact carries when it happened and when it could first be known, and so the
time between them. In piece 1 that is the high and the tick the peak became known. For the dipole (D) it is
Native's own time for a stage and the tick it is placed at.

**More than one way to end.** Nothing is given an ending that its own definition forces. A peak can come back, be
beaten, or stay open. For the dipole (D): beside Native's own ending, the fact line of each birth names the flow
peak in play at that tick, so that peak's own ending (reached zero and came back, beaten, still open) stands
beside Native's.

**The cases that did not happen.** Wherever something is read backward from a birth, a peak, a leg or a dipole,
the same reading is listed for the ticks where the same things were present and nothing followed. Every tick and
every peak is kept, so the list exists; it is made at the grouping stage and kept case by case.

### Two readings made at the grouping stage, from the facts

**The earliest tell.** For every peak, leg and dipole: the first tick at which it could be told apart from the
ones that came to nothing. Read from the facts in tick order.

**Order, and how long between.** For any two kinds of fact: which came first and the time between, each case
listed. Every fact carries its tick, so this is a subtraction, with no pairing picked in advance.

## Written in the ninth session (2026-11-17), not yet run: L, M and the chain link models

Code: Markets branch `ccr-d9ae98a9-65go6q`. Each has its one check written. The first run of each is on the pods,
on Greg's go. Counts are added here when they have run. Every call below is in `ROOT_GAMEPLAN_DECISIONS.md`,
"Ninth session", stated to Greg, his to correct.

### L. Refilled orders (`root/calcs/refills.py`)

Facts beside the rows: at the tick of an order's own row in the exchange event that filled it, whenever that row
shows size put back, and whenever a filled order changes price in that row.
- Every row with size put back gets a fact, with the row's own words. A yes/no says whether the order is the same
  size or larger than before the fill (the layout's "refill"). Nothing is picked.
- The size put back is never more than the fill took: the same figure as `refilled` in the book totals, so the
  facts of a side add up to that side's total. (Corrected before the first run; see the decisions file.)
- A fill followed by a change of price is its own kind of moment.

### M. Sweeps, and the quote touching or crossing (`root/calcs/sweeps.py`)

Facts beside the rows: one for every exchange event that holds a trade, at the tick with the exchange's end mark;
one when the best bid and ask touch or cross; one when they part, with how long it lasted and the lowest the gap
went.
- Every trade event gets a fact, not only the ones that fill through several price levels.
- All trade sides of an event are written when there is more than one, in the order they came.
- A price level filled through is a distinct price among the event's fill messages.

### The chain link models (`root/calcs/chain_peaks.py`, `root/chain_models.py`)

As laid out in piece 4 above and approved ("Do it"). Two parts:
- `chain_peaks`: a peak line at the tick each peak's story ends (the ten figures of what it did, both clocks), and
  before lines at the tick each peak becomes known (the nearest peaks before it whose stories had already ended,
  one line a step, six steps written out now).
- `chain_models`: for each trade day, three models taught on the other three trade days. One line per peak, model
  and step back: each figure's squared error without and with the peak at that step, the mean beside them, the
  gain. Its own table, keyed by peak. The values are not known at a tick.

## Still to lay out

5. Step 2: the chain, its stages, timing and recurrence. Greg, 2026-11-16: "We'll have to look at step 2 closer
   before it's run. That might be intentional" (of its pooled results). It is gone through with him result by
   result before anything of it is built.
6. The growth column of the family (new families from the four trade days), after piece 3 is in view.
