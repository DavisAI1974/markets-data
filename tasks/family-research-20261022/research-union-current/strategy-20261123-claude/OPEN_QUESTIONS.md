# What paper trading must settle, and what is open with Greg (Claude, 2026-11-23, v2)

Greg, 2026-11-23: "we will be testing strategies in paper trading. That's what it's there for"; "We will be doing
more research and refining as it is going on. The answers to Your questions will be added to the update". So nothing
here holds the fifteen back. Each item says what is open; where Claude made a call it is stated, his to correct.

## What paper trading must settle, strategy by strategy

Each is read from the paper trades one by one, each trade day and each cell on its own. No strategy is set
against another to pick one.

| Rule | What its paper trades must show |
|---|---|
| CL01 | After an eaten first level, does a third step come in a LATER exchange event, or was it mostly the same event? What the best bid did while the best offer ran. |
| CL02 | After a level only pulled, does the run step back before it steps on? |
| CL03 | Does a first step made by a fill take a second step more than one made by a cancel? |
| CL04 | How often a level that has only been eaten gives way, and how often the state breaks first. Nothing is known here before paper trading. |
| CL05 | Whether the quotes have moved at a trade leg's FIRST step often enough to trade; whether legs up on a trade day like Oct 3 go on reading the other way. |
| CL06 | What comes after both quotes have stepped: a further step, or the step back. Nothing is known here before paper trading. |
| CL07 | Whether fresh trading on the dipole's side is followed by the quote stepping away in a later event. How many of its closes are set by the 20-second span (a hump holding one trade ends when that trade leaves). |
| CL08 | Whether a later step of the hit quote ever comes before the hump ends, and what follows it. |
| CL09 | Whether a first step made by a cancel comes back before it steps on. |
| CL10, CL11 | Which side of a run going against the dipole is right, cell by cell. They hold opposite sides of the same events, so on every event one is right and one is wrong. |
| CL12 | Whether a reloaded level holds, or the order is filled out and the quote steps through. |
| CL13 | Whether the quote goes on after an aggressor paid up, or comes straight back. |
| CL14 | Whether the first print on the other side at a run's top step is followed by the step back. |
| CL15 | Whether a move comes again after a one-step pause. |

FOR ALL FIFTEEN, the first thing paper trading will show: a run's first step back is one tick nearly every time,
so on the followed quote alone a trade closed there is one tick behind unless the move took another step. How
often each rule gets that further step is its whole case.

## What paper trading needs before it can start (Greg's to say)

1. WHICH PLATFORM AND WHICH FEED. The rules need the order-by-order tape (every add, cancel, change and fill, with
   the exchange's event marks) and the two lines made at the tick. A feed of trades and best prices alone cannot
   run CL01, CL02, CL03, CL04, CL09 or CL12.
2. HOW A PAPER FILL IS PRICED. The rules give the tick and the side and write the best bid and the best offer at
   each end, each on its own. No fill or cost is set here (his rule: trade cost is not a market condition).
3. ONE TRADE FOR EACH TRIGGER, OR ONE AT A TIME FOR EACH STRATEGY. Claude's call: one for each trigger, each on its
   own line.
4. A TRADE STILL OPEN AT 5 PM EASTERN. Claude's call: closed at the last tick of the trade day.

## Calls Claude made in the rules, his to correct

5. A rule decides only at the end of an exchange event; only what comes in a later event counts as following.
6. CL09 as first written never opened a trade. It is now rule 6 of all fifteen, and CL09 (v2) is the first step
   made by a cancel, faded.
7. CL10 and CL11 are left as he saw them: opposite sides of the same events.
8. CL04 subtracts a stored running total between two ticks the data sets; CL07 and CL08 read the dipole line just
   before a trade. Treated as reads of stored values, not as new lines.
9. Left out: the crypto and ng program's turns table, with its trades. Still not for strategy: the information
   measure.
10. Two count files of the peak research of 2026-11-17 (Claude's own, last week, on the rebuilt rows) are cited in
    `EVIDENCE.md`: `ATTRIBUTES_BY_PILE.json` (the peak with no window only) behind CL14, and `HOW_A_LEVEL_EMPTIED.json`
    for the fifth-step table under CL01 and CL02. They were read without being named to him first: owned. If he
    rules last week's research out whole, those tables and the sentences drawn from them come out.
11. NUMBERS LEFT OPEN AS HIS: how the largest way a level empties ("some filled, some pulled") would be split. No
    rule trades it today.

## On the later research list, not started

- How many of a run's later steps lie in the same exchange event as the step before (item 18).
- Do large moves come back (item 4). CL15 trades without waiting for it.
