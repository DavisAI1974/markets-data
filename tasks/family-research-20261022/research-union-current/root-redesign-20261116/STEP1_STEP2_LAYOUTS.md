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

Results (each in `CALC-flow_peak-<trade day>.json` on its `root-rows` branch):

| Trade day | Rows | Peaks | Trades with no side | Recount | Playback |
|---|---:|---:|---:|---|---|
| Mon Oct 2 | 820,670 | 8,894 | 2,230 | equal on every row | equal at two cuts |
| Tue Oct 3 | 879,497 | 9,910 | 1,870 | equal on every row | equal at two cuts |
| Tue Oct 17 | 846,158 | 8,051 | 2,647 | equal on every row | equal at two cuts |
| Wed Oct 18 | 771,468 | 7,423 | 2,408 | equal on every row | equal at two cuts |

34,278 peaks over the four trade days, about one every 9 or 10 seconds. The old detector recorded about 850 a
UTC clock day. About 21 to 30 seconds a trade day to run; 2.3 to 2.9 MB stored a trade day. The check caught one
fault on its first run (a peak's standing left out the stretch of flow still running at the tick it became known);
it was fixed before anything was stored.

## The rest of Step 1, laid out together (Greg, 2026-11-16: "Let's do the rest of the st 1 calcs plan in this next swoop so we aren't doing a piece at a time")

Status: piece 2 APPROVED to build by Greg 2026-11-16 ("Build"), as revised below. Piece 3 not built (his rule on
labels). Piece 4 decided as B, to be laid out in detail after piece 2 exists.

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

## Still to lay out

5. Step 2: the chain, its stages, timing and recurrence. Greg, 2026-11-16: "We'll have to look at step 2 closer
   before it's run. That might be intentional" (of its pooled results). It is gone through with him result by
   result before anything of it is built.
6. The growth column of the family (new families from the four trade days), after piece 3 is in view.
