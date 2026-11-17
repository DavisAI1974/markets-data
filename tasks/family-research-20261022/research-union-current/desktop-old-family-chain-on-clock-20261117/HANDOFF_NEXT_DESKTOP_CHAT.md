# Handoff for the next Desktop chat (written 2026-11-17, about 04:55 Eastern)

Branch `ccr-349e2ffe-07p8od` of `DavisAI1974/markets-data`. Code writes to the same branch: fetch before every push.
This chat's workspace does not last. Everything it made that is kept is in this folder.

## What Greg wants (his words, this chat, in order)

- "Do you want to start looking at new family and chain data to see what it's showing us? New structures? New
  groupijgs? But we want the data to guide us"
- "And we don't associate peaks with anything other than the data but they really should be pinned to the timestanp
  like price curve and dipole. They happen at certain times and for certain reasons. I don't think groupling applies
  at all to them"
- "If calculations happen over a time period the sensible thing is to pin them to timestamps rignt?" (Yes: the tick
  a result is about, the stretch it read, and the tick it became known.)
- "It's definitely thin tape but it's a start point and it helped us figure out initial definitions. I said over and
  again in the chats that we use it as a.base to grow from"
- "I was trying to explain to you to use the same process and procedure as we used on the 55 we run and apply those
  to the new run. We don't need the old ut puts with the new data, but we want to know how they were defined and
  grouped"
- "And we should have plenty of new groups and families that we didn't before. I guess I'm saying to do that work to
  continue ising that framework on completely new and different data"
- "And let's get away from defined windows a d see how long or short these groups and families actually last and
  where their true begininngs and ends are pinned to the timestamps"
- On storing: "Push data to markets data repo and print here so we can discuss"; "List output files and renders for
  code to use to.ipdate excel sheets". He does not want calculations run and then forgotten.

## So the work is

Run the 55-week run's PROCESS AND PROCEDURE fresh on the new run (the four trade days' stored rows and
calculations). Carry in none of the old outputs: no old centres, no old state names, no old named chains.
No defined windows: no 60 seconds before, no 60 seconds after, no 45-second spacing, no level gate. Each event's
true beginning and end come from the data and are pinned to timestamps, and how long each group or family lasts is
measured, not set.

## How the 55-week run defined and grouped (read from its programs, Markets `59c03e8`,
branch `chatgpt/ng-exhaustion-post-phase2-20260818`)

1. Events (`research/ng_exhaustion_chain_canonical_table_20260817.py`, `research/ng_dipole_native_shape_audit.py`):
   the 20-second flow each second; an event is a high in its size that passed three gates (85 in 100 of the day,
   highest within 5 s, 45 s spacing by prominence).
2. Families (`research/ng_exhaustion_family_quantify_v2_20260816.py`): the flow curve over the 60 s before each
   event, turned so the event's side is up; 78 shape numbers (the build-up curve and the curve relative to the high,
   every 2 s, and 16 shape figures); no price and nothing after the event; RobustScaler (20 to 80); identical shapes
   (rounded to 5 places) counted once; KMeans for 2 through 8 groups, 50 starts, all reported; checked by leaving one
   day out; groups put in a fixed order. Three were kept: A, B, C.
3. States: what the flow did in the 60 s after (stayed P, reloaded same side S, reversed O, sparse X).
4. Chains (`research/ng_exhaustion_chain_phase2_characterize_20260817.py`,
   `research/ng_exhaustion_chain_phase2_parallel_agents_20260818.py`): events in time order; each carries the
   states of the ones before it that were already known; strings found on one block of weeks, repeated on later
   blocks, then untouched weeks, then the held week; depth counted only where three models agreed; lifespans read as
   timing families.
5. A string that failed a block was flagged and taken apart, never deleted.

## Where to start (Claude's calls, not yet confirmed by Greg; put each to him once)

- Not started: nothing of the fresh run exists. Only the tools were installed.
- What the family step runs on. Greg said grouping does not apply to peaks, then said to do the framework on the new
  data. Claude's stated call, which he did not stop: start with every stored peak (36,688), each staying on its own
  tick, then the other new kinds of events the 55-week run never had (quote runs, sweeps, refills, orders leaving
  together). Confirm with him before building on it.
- Without defined windows: the stored `peak_story` already gives each peak its own beginning and end with no fixed
  marks (the low it rose from, each new low of the fade, reached zero, came back, beaten), and `chain_peaks` gives
  `low_to_high_ns` and `high_to_end_ns`. Proposal: an event's shape is its own flow path from its low, through its
  high, to its end, pinned to those three ticks, instead of 60 s either side.
- To revisit, already flagged by Greg to Code: the 20-second flow is itself a window. Code has his go to work the
  peak out without it. The 20-second version stays beside it.

## What this folder holds, and its standing

Old outputs laid on the new data: NOT what he asked for. Kept as a record only. Not for the daily sheets or the
workbook (see the note at the top of `README.md`). Useful to the next chat only as plumbing: `load.py` and
`build_old_defs.py` show how the stored rows and the flow are read and reproduced exactly (tick order, the received
clock, side B is bought).

## Rules that hold

Every peak and event individually, on its own tick. No averages as the answer, no ranks, nothing dropped. Charts and
tables first; plotted points equal the rows. Report what was measured; label readings as readings. Push outputs to
markets-data in their own folder with a MANIFEST, print the findings in chat, and list the files for Code. Nothing
goes to a trunk. Do not re-ask what he has decided.

## Not stored anywhere

The renders and counts of the chat of 2026-11-16 evening ("ST1 and ST2 findings": price with every peak, price with
the peak line, Oct 17 against random points). They can be drawn again from the stored files.
