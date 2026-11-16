# Step 1 and Step 2 calculations: the layouts as put to Greg, and his answers

Each calculation is laid out his way (what we want, what it did, what changes) and approved BEFORE it is built or
run. Nothing here is built until its status says APPROVED. Rules that govern all of them are in
`ROOT_GAMEPLAN_DECISIONS.md`: only the four trade days enter a calculation (through `tape.for_calculations()`); a
row holds only what was known at its tick; nothing is written back onto an earlier row; empty cells are never
counted; every trade individually; the caps and limits come off the outputs; trade cost is not a market condition.

"What it did" is read from the frozen programs on Markets branch `chatgpt/ng-exhaustion-chain-phase2-20260817`
(`1bec694`), `research/ng_exhaustion_chain_canonical_table_20260817.py` and the programs it calls.

## Piece 1: the flow and the exhaustion peak (Step 1)

Status: APPROVED by Greg, 2026-11-16 (seventh session): "Yes rewrite", "Yes". Build started.

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
   The old events can still be picked out from those figures; what the gates threw away is there as well.
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

## The rest of Step 1, laid out together (Greg, 2026-11-16: "Let's do the rest of the st 1 calcs plan in this next swoop so we aren't doing a piece at a time")

Status of pieces 2, 3 and 4: PUT TO GREG 2026-11-16 (seventh session). Not approved yet. Not built.

"What it did" is read from the same frozen detector and the programs it calls (the fade-timing functions, the
frozen family rule and its two rule files), and from the lineage programs of 2026-08-17.

### One thing that shapes all three: where a fact about a peak is written

In the old work each event was one line, filled in afterwards with everything that happened in the minutes after
it. On a tick row that would be writing later facts onto an earlier row. And peaks overlap: on trade day Oct 2 a
new one becomes known about every 9 seconds, and each is followed for minutes.

Claude's call: every fact about a peak is written on the tick row where that fact becomes known, and it names its
peak (by the tick of the high). When facts about more than one peak become known on the same tick, the cell holds
one line for each, in the way the order line cell already does. Nothing is written back, no peak's story is cut
short because a newer peak arrived, and Frankie sees each fact at the moment it could be known.

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

**What changes.**
1. Each fact goes on the row where it becomes known, naming its peak (above).
2. The fade is followed until the peak ends, not for 60 seconds only.
3. Read at every tick, not once a second. "3 seconds in a row" becomes 3 seconds of clock time.
4. The whole book, not the top 10 levels.
5. No peak is dropped. A figure that cannot be made is empty with its reason.
6. Averages are additions (Greg's rule): the late book is an average over 20 seconds; the book at every tick is
   already on the rows beside it.
7. A peak not yet ended at 5 pm is recorded as still open at the end of the trade day.
8. What stays, as the definition of each figure: the 50, 25 and 10 percent marks, the 3 seconds, seconds 41 to 60,
   the seven moments after the ending, the 2 ticks, and the four state names. They hold nothing back: the whole
   path of the flow and of the price is on the rows.

### Piece 3: the family (A, B, C)

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
   the largest). It is now applied to every peak, small ones included.

### Piece 4: the link between events (the chain). NEEDS GREG'S DECISION.

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
- A (Claude's recommendation): on the four trade days, write what a link is made from, per peak: the peak before
  it, the time between them, same side or not, and each one's price moves after its ending. No model and no depth
  number. The chain depth column stays empty with its reason until the old weeks can be run through the new ROOT.
- B: teach the three models on the four trade days themselves and write a depth. It can be done, but it rests on
  four trade days, it is a model score, and it would not be the old chain.
- C: leave the link out of Step 1 for now.

## Still to lay out

5. Step 2: the chain, its stages, timing and recurrence. Greg, 2026-11-16: "We'll have to look at step 2 closer
   before it's run. That might be intentional" (of its pooled results). It is gone through with him result by
   result before anything of it is built.
6. The growth column of the family (new families from the four trade days), after piece 3 is in view.
