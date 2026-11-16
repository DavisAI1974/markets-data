# Step 1 and Step 2 calculations: the layouts as put to Greg, and his answers

Each calculation is laid out his way (what we want, what it did, what changes) and approved BEFORE it is built or
run. Nothing here is built until its status says APPROVED. Rules that govern all of them are in
`ROOT_GAMEPLAN_DECISIONS.md`: only the four trade days enter a calculation (through `tape.for_calculations()`); a
row holds only what was known at its tick; nothing is written back onto an earlier row; empty cells are never
counted; every trade individually; the caps and limits come off the outputs; trade cost is not a market condition.

"What it did" is read from the frozen programs on Markets branch `chatgpt/ng-exhaustion-chain-phase2-20260817`
(`1bec694`), `research/ng_exhaustion_chain_canonical_table_20260817.py` and the programs it calls.

## Piece 1: the flow and the exhaustion peak (Step 1)

Status: PUT TO GREG 2026-11-16 (seventh session). Not approved yet. Not built.

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
   trades. It sits beside the single trades, which are already on their own rows. To confirm with Greg: this is
   the calculation he meant as the one exception to "no averaging" (the same data both ways, both kept).

**What it writes.** New columns on every row (no row is added or removed): bought, sold and no-side size in the
last 20 seconds; the flow; and, on a row where a peak becomes known, the peak's side, size, the tick of its high,
its standing so far in the trade day, how long it had been the highest, and the time since the peak before.

**Not promised.** The number of peaks. With the gates off there will be many more than the old events. The count
is reported after the first trade day, and Greg hears before anything is capped if it looks like running away.

## Pieces still to lay out, in order

2. What is written about each peak as it plays out: the 60 seconds before and after, the timing of the fade, the
   ending, the after-state.
3. The family rule (A, B, C). Both frozen rule files are in git.
4. The chain link between events. Needs Greg's decision first: in the old work a link was a model score learned
   over blocks of 18 to 48 weeks, which four trade days cannot produce.
5. Step 2: the chain, its stages, timing and recurrence.
