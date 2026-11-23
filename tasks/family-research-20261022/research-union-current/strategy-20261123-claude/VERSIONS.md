# The 15 versions (Claude, 2026-11-23, eighteenth session)

Fifteen strategy versions for the natural gas front-month future, each for one situation and one stage of a move.
Every one is a HYPOTHESIS. None has been tried on the tape. None is ranked against another, none is merged into
another, and versions that overlap or oppose each other are both kept (Greg's instruction in the shared task).

Formed on all four trade days (Oct 2, 3, 17, 18, 2023), on Greg's word of this session: "Use all 4 days to make
strategies". What that means for any try is in `BLIND_FORMATION.md`. The counts behind each version, each trade day
on its own, are in `EVIDENCE.md`; what could not be settled is in `OPEN_QUESTIONS.md`.

## The stages (the generic move of the running notes)

(0) before the move; (1) the first step; (2) the middle; (3) whether it takes another step; (4) the turn; (5) after.

| Stage | Versions |
|---|---|
| (0) before the move | CL04, CL07 |
| (1) the first step | CL03, CL05 |
| (2) the middle | CL06, CL10, CL13 |
| (3) whether it takes another step | CL01, CL02 |
| (4) the turn | CL08, CL11, CL12, CL14 |
| (5) after | CL15 |
| any stage: what is not a signal | CL09 |
| use during an open stance (management) | CL06, CL09, CL12, CL14 |

## What holds for all fifteen

1. THE CLOCK AND THE ORDER. Every read is made at a tick, on the received clock (`received_time_ns`), in the order
   of `position_on_tape`. A stored value is read at a tick BY ITS PLACE ON THE TAPE, never by time alone.
2. WHERE A VERSION MAY SPEAK. Only on rows labelled "trade day" of the four trade days. No stance is taken on a row
   inside the settlement window (`in_settlement_window`); a stance open when the window begins is marked and kept
   out of any try. A stance still open at the last tick of a trade day is listed as open; no end is made up for it.
3. THE EXCHANGE EVENT. A stance is taken at the tick that carries the exchange's own end-of-event mark
   (`ends_exchange_event`) for the event in which its state became true, never inside an event. Whatever happens
   later INSIDE THAT SAME EXCHANGE EVENT is not counted as following it. Reason: one order that trades through
   several price levels makes several steps of the quote in one event, and nothing could be decided between them.
4. THE TWO LINES. Exhaustion is the stored 20-second line and dipole is the stored 60-second line (the crypto
   formulas made on the natural gas tape), read from `calc-research_columns` on the tick's own row (`exhaustion_20s`,
   `dipole_60s`). Only the states the line itself makes exact are used: above zero, below zero, at zero, empty.
   No level, rate, difference or other line is made from them. Where a version would need one, it says so and is
   marked "put to Greg before it is built".
5. NO NUMBER OF OURS. No count of seconds, ticks, trades or lots is chosen. The only lines drawn are the ones the
   tape draws: a second step exists or it does not; every order of a level was filled or it was not; an event
   filled one price level or more than one. Any other number is Greg's and is left open.
6. WHAT IS WRITTEN FOR A STANCE. One line for each stance, on its own: the tick it was taken at and the tick it was
   let go at, and at each the best bid and the best offer as they stood once that tick was done, EACH ON ITS OWN.
   Between them, the steps each quote made and the prints as they printed. No mid price, no fill, no cost, no size.
7. NO VOTE, NO NETTING, NO LABEL. Each stance is its own event. Versions do not vote and are not combined. Nothing
   is named by what happened next.
8. A MISSING INPUT. Where a stored value a version reads is empty, no stance is taken and the tick is counted as
   "input empty". A trade the tape gives no side for is in neither line; it neither starts nor ends a stance.
9. THE LEAKAGE GATE comes before any try: the stances a version takes on the tape cut at a tick must equal the
   stances it takes on the whole tape up to that tick.
10. OUT of every version: the 20-second peak family (so the `buy_peak_*`, `sell_peak_*` and `rise_*` columns of
    `move_steps` and `leg_peaks`, the `20-second flow` lines of `turn_peaks` and the peak lines of `resting`), Native's
    dipole record, the crypto and ng program's own trades and its turns table (its turn amount was set on crypto
    results; Claude's call, his to correct), the mid price, crypto data, the information measure (`info_*`), and
    the old research and strategy documents.
11. WORDS. "Best offer" is the column `best_ask`. "With the move" means up for a move up and down for a move down.
    A "run" is a run of the best bid or of the best offer as `quote_runs` follows it; its "first step back" is the
    tick it ends. "The run of trades on one side" (`run_side`, `run_size`, `run_trades`) is called that and nothing
    else.

How each version below is laid out: the situation and stage; what is observed and at which tick it is known; the
exact state; the direction; when the stance is taken, let go and may be taken again; management and what
invalidates it; what is built in and what is left after the decision; observation against proposed rule; what
would show it wrong; the cells it is reported by; and whether it can be read from what is stored today.

---

## CL01. The eaten level: with the run

- STAGE AND SITUATION: (3) whether a move takes another step. A run of the best offer up, or of the best bid down,
  has just taken its SECOND step.
- OBSERVED, AND KNOWN AT: the second step is the fact `new furthest price` with `moves` 2 in
  `calc-quote_runs-facts` (tick T2). At that same tick the stored `resting` line of the run says what became of the
  orders that stood at that quote's best price when the run started (in `research-moves`: `level_orders_at_turn`,
  `level_left_by_fill`, `level_left_by_cancel`, `level_still_resting_orders`, `level_moved_orders`). Known at T2
  and not before: the level finishes emptying at T2.
- THE STATE: every one of those orders left by being filled (`level_left_by_fill` equals `level_orders_at_turn`).
- DIRECTION: with the run (up for the best offer up, down for the best bid down).
- TAKEN / LET GO / AGAIN: taken at the end of the exchange event that holds T2. Let go at the run's `first step
  back`. May be taken again at the next run's second step.
- MANAGEMENT AND INVALIDATION: nothing of its own between the two ticks. CL06, CL12 and CL14 speak during it. The
  state is a finished fact and cannot be undone; the stance simply ends at the first step back.
- BUILT IN, AND WHAT IS LEFT: the fill that empties the level and the second step are one exchange event, so the
  state completes on a trade. What is not built in is a third step in a LATER exchange event. NOT YET COUNTED: how
  many of the third steps behind the paper's finding 4 lie in the same exchange event as the second step (a sweep
  through several levels). On the followed quote alone, a run that ends at two steps stands one tick behind T2 at
  its first step back, a run of three steps stands level, and each further step is one tick ahead (the stored
  figure for what a move gave back is one tick nearly every time).
- OBSERVATION / PROPOSED RULE: observation: in all eight rows (four trade days, offer up and bid down) the runs
  whose first level was every order filled took a third step more often than the runs whose first level was every
  order pulled. Proposed rule: take the run's side at T2 when the level was every order filled.
- WHAT WOULD SHOW IT WRONG: on a trade day beyond the four, in a cell, the eaten runs take a third step (in a
  later exchange event) no more often than the pulled-only runs. On the four it cannot be tested: it was formed
  on them.
- CELLS: quote and direction (best offer up; best bid down) by trade day. The other two directions (best offer
  down, best bid up: a better quote stepping in front) hold the same stored read, but an old level stays behind
  there and the mechanism is not understood: no stance is taken on them; they are counted apart.
- READ FROM WHAT IS STORED TODAY: yes (`calc-quote_runs-facts`, `calc-resting-facts`, `research-moves`, the rows).

## CL02. The abandoned level: not followed

- STAGE AND SITUATION: (3) whether a move takes another step. The same tick as CL01: a run of the best offer up or
  of the best bid down has just taken its second step.
- OBSERVED, AND KNOWN AT: the same stored `resting` line, at T2.
- THE STATE: every one of the orders that stood at the first level left by being pulled (`level_left_by_cancel`
  equals `level_orders_at_turn`); none was filled.
- DIRECTION: two uses, kept apart. (a) A WARNING with no direction: no version that follows the run takes or keeps
  a with-the-run stance because of this second step. (b) The proposed rule: AGAINST the run (down for the best
  offer up, up for the best bid down).
- TAKEN / LET GO / AGAIN: taken at the end of the exchange event that holds T2. Let go at the run's first step
  back, which is the event it expects. Again at the next run's second step.
- MANAGEMENT AND INVALIDATION: invalidated by a third step of the run (`new furthest price` with `moves` 3).
- BUILT IN, AND WHAT IS LEFT: nothing traded at the level, so nothing of the two lines is built into the state.
  What is left for (b), on the followed quote alone: one tick when the run ends at two steps; one tick against it,
  and invalidated, when the run takes a third step.
- OBSERVATION / PROPOSED RULE: observation: in all eight rows the pulled-only runs went on least often (the
  running notes' words: "a level that was only abandoned leads nowhere"). Proposed rules: (a) and (b) above.
- WHAT WOULD SHOW IT WRONG: on a trade day beyond the four, in a cell, the pulled-only runs take a third step as
  often as the eaten ones.
- CELLS: quote and direction by trade day. THE MIDDLE CELL, "some filled, some pulled", is the largest (about a
  thousand runs a trade day in each direction): neither CL01 nor CL02 takes a stance there. How much filled
  against how much pulled would split it is a number of Greg's; the sizes are stored.
- READ FROM WHAT IS STORED TODAY: yes (the same files as CL01).

## CL03. The first step made by a fill

- STAGE AND SITUATION: (1) the first step. A run of the best offer up, or of the best bid down, has just started:
  the quote has left a price. The same question as CL01, one step earlier, where more of a move is still ahead.
- OBSERVED, AND KNOWN AT: the row at the tick that moved the quote (T1: `best_ask_moved_from`, `best_ask_moved_to`,
  `level_emptied`, `what_happened`, `exchange_event`); the `trade event` fact of that exchange event in
  `calc-sweeps-facts` (`size_bought`, `size_sold`, `best_ask_moved`, `price_levels_filled`); and in
  `calc-together-facts` whether the orders that left did so together at one exchange time. Known at the tick that
  ends that exchange event.
- THE STATE: "made by a fill": the order whose leaving moved the quote left by fill (`what_happened` is "left by
  fill") in an event that holds a trade by the hitting side. The other cells: "made by a cancel" (the order left by
  cancel, no trade in the event) and "made by a change of price".
- DIRECTION: with the step when it was made by a fill. No stance when it was made by a cancel or a change of
  price.
- TAKEN / LET GO / AGAIN: taken at the end of that exchange event. Let go at the run's first step back. Again at
  the next run's start.
- MANAGEMENT AND INVALIDATION: at the second step CL01 and CL02 read the level in full and take over.
- BUILT IN, AND WHAT IS LEFT: the step IS the trade (a buy that takes out the best offer steps it in the same
  exchange event), so nothing about the first step is foretold. The version is about the second step. What is
  left: most runs end at one step (the paper's finding 1), and a one-step run stands one tick behind at its first
  step back.
- OBSERVATION / PROPOSED RULE: no count has been made at the first step. It is the paper's finding 4 carried one
  step earlier, with one difference said plainly: finding 4 reads EVERY order of a level, this reads only the
  order whose leaving moved the quote. Proposed rule: follow a first step made by a fill, not one made by a
  cancel.
- WHAT WOULD SHOW IT WRONG: in a cell, first steps made by a fill take a second step (in a later exchange event)
  no more often than first steps made by a cancel.
- CELLS: quote and direction, by how the step was made, by trade day.
- READ FROM WHAT IS STORED TODAY: yes (the rows, `calc-sweeps-facts`, `calc-together-facts`,
  `calc-quote_runs-facts`). NOT COUNTED YET.

## CL04. A level that has only been eaten, before it gives

- STAGE AND SITUATION: (0) before the move. The best offer (or the best bid) has stood at one price since the tick
  that last moved it (T0). The level is being traded into and has not yet given way.
- OBSERVED, AND KNOWN AT: the stored running totals of `calc-book_totals` at the best price, at T0 and at the
  present tick: `ask_filled_at_best`, `ask_pulled_at_best`, `ask_added_at_best`, `ask_moved_from_best`,
  `ask_moved_to_best` (and the same for the bid). The amount between two ticks is one subtraction, which is what
  those totals were stored for; both ticks are set by the data (the quote's own last move, and now). Known at each
  tick as the book shows it.
- THE STATE: since T0, at that best price, size has been filled, and none has been pulled, added or moved in or
  out.
- DIRECTION: with the eating (up while the best offer is being eaten, down for the best bid).
- TAKEN / LET GO / AGAIN: taken at the end of the first exchange event in which the state holds. Let go at the
  first tick at which size is pulled, added or moved at that price (the state is broken), or at the tick the level
  gives way (the quote steps; CL03 then reads how). Again from the next T0.
- MANAGEMENT AND INVALIDATION: invalidated when the quote steps the OTHER way (a better quote comes in front) or
  when size is added at the level (it is being reloaded; see CL12).
- BUILT IN, AND WHAT IS LEFT: the trades that eat the level are the trades the two lines are made from, so the
  lines will stand on the eating side; that is not a second finding. Nothing of the step itself is built in: it
  has not happened. This is the only version that can hold a stance before a first step; what is left is the first
  step itself and whatever follows it.
- OBSERVATION / PROPOSED RULE: NO OBSERVATION. The paper says so: "Nothing yet warns BEFORE a move's first step".
  The whole version is a proposed rule, carried back from finding 4.
- WHAT WOULD SHOW IT WRONG: in a cell, levels in this state give way (the quote steps away from them by a fill)
  no more often than levels that were traded into and also pulled from.
- CELLS: side (best offer eaten; best bid eaten) by trade day.
- READ FROM WHAT IS STORED TODAY: yes (`calc-book_totals`, the rows' marks of the quote moving). NOT COUNTED YET.
  Put to Greg: the subtraction of a stored running total between two ticks the data sets is not a new line in
  Claude's reading; his to strike.

## CL05. A move's first step with the exhaustion line on its side

- STAGE AND SITUATION: (1) the first step. Any of the three stored moves has just made its first step: a trade leg,
  a run of the best bid, a run of the best offer.
- OBSERVED, AND KNOWN AT: the stored exhaustion line at the tick of the first step (`exhaustion_20s` on that row;
  in `research-moves`, `exhaustion_20s_at_first_step`), read by place. For a trade leg also the best bid and the
  best offer at that tick against where each stood once the tick of the leg's first trade was done
  (`best_bid_at_first_trade`, `best_ask_at_first_trade`).
- THE STATE: the line is on the move's side (above zero for a move up, below zero for a move down). FOR A TRADE LEG
  ONE MORE CONDITION: at least one of the two quotes is no longer where it stood at the leg's first trade. A trade
  leg whose quotes have both stood still is the print going back and forth between the bid and the offer; it gives
  no direction and no stance is taken on it.
- DIRECTION: with the move.
- TAKEN / LET GO / AGAIN: taken at the end of the exchange event of the first step. Let go at the move's end (the
  run's first step back; the print that ends the trade leg). Again at the next move's first step.
- MANAGEMENT AND INVALIDATION: for a run, CL01 and CL02 speak at the second step. Invalidated when the line crosses
  to the other side ON A TRADE before a second step (a crossing made by old trades leaving is not one: CL09).
- BUILT IN, AND WHAT IS LEFT: for a trade leg the first step is a print, and that print is in the line. For a run
  made by a fill, the same. So "on its side" is partly made by the move's own first trade. What is left: about one
  run of the quote in five and about two trade legs in five take a second step at all.
- OBSERVATION / PROPOSED RULE: observation (the paper's finding 3): where the line stands at the first step says
  little for a run of the quote and somewhat more for a trade leg. Proposed rule: follow only first steps the line
  is behind.
- WHAT WOULD SHOW IT WRONG: in a cell, first steps with the line on their side take a second step no more often
  than first steps with the line against them. ALREADY SEEN ON THE FOUR: it reads the other way in three cells,
  all on trade day Oct 3 and all upward (best offer up, best bid up, trade leg up).
- CELLS: move and direction (six) by trade day, each with "on its side", "against", "at zero" and "empty".
- READ FROM WHAT IS STORED TODAY: yes for the line (counted in the paper). The condition on a trade leg's quotes
  AT its first step is not counted yet: the paper counted it at the leg's end.

## CL06. Both quotes have stepped the same way

- STAGE AND SITUATION: (2) the middle, and management. One quote stepping is a level changing. The best bid and the
  best offer both stepping the same way is the price having moved. They are followed separately and never
  combined.
- OBSERVED, AND KNOWN AT: the rows' own marks of each quote moving (`best_bid_moved_from/to`,
  `best_ask_moved_from/to`) and the runs in `calc-quote_runs`. Known at each tick.
- THE STATE: since the last tick at which EITHER quote stepped down, the best bid has stepped up at least once and
  the best offer has stepped up at least once (and the mirror for down). It begins at the tick the second of the
  two steps. No stance while the quote is touched or crossed (the best offer at or below the best bid).
- DIRECTION: with the two quotes.
- TAKEN / LET GO / AGAIN: taken at the end of the exchange event in which the state begins. Let go at the first
  step the other way by either quote. Again when the state next begins.
- MANAGEMENT AND INVALIDATION: as a ride rule for any with-the-move stance of another version: held while the
  state holds, let go when either quote steps back. CL12 and CL14 may speak earlier.
- BUILT IN, AND WHAT IS LEFT: the bid and the offer are different orders, so one stepping does not make the other
  step. Inside one sweep both can move in one event: the state then begins at that event's end. What is left is
  NOT KNOWN: nothing has been counted on it.
- OBSERVATION / PROPOSED RULE: observation, by analogy only: a trade leg of two steps or more has nearly always
  moved a quote, a one-step leg mostly has not (the paper's finding 2); and, by eye on one trade, the bid and the
  offer do not always step together. Proposed rule: treat a move as real only once both quotes have stepped.
- WHAT WOULD SHOW IT WRONG: in a cell, after the state begins, a further step the same way by either quote comes
  before a step back no more often than it does after one quote stepping alone.
- CELLS: direction (up, down) by which quote stepped second, by trade day.
- READ FROM WHAT IS STORED TODAY: yes (the rows, `calc-quote_runs-facts`). NOT COUNTED YET.

## CL07. Fresh trading on the dipole's side (renewal)

- STAGE AND SITUATION: (0) to (1): the birth of a push. The exhaustion line comes onto one side of zero ON A TRADE,
  and the 60-second flow was already on that side: buying (or selling) that had paused or been answered starts
  again.
- OBSERVED, AND KNOWN AT: a hump of the stored exhaustion line that begins on a trade (`began_on` is "a trade was
  received", `began_position` is that trade; `calc-research_columns` sets it on that tick). The stored dipole line
  AS IT STOOD JUST BEFORE THAT TRADE: the read of `crypto-ng-tick-lean-60s` before the trade's own read, by place.
  Known at the trade's tick.
- THE STATE: the hump began on a trade, and the dipole line just before the trade stood on the hump's side.
- DIRECTION: with the hump (up for a buying hump, down for a selling one).
- TAKEN / LET GO / AGAIN: taken at the end of the exchange event of the trade the hump began on. Let go when the
  hump ends (the line next stands at zero, is empty, or has crossed: the hump's own stored end). Again at the next
  hump that begins on a trade.
- MANAGEMENT AND INVALIDATION: invalidated when the hump ends by crossing to the other side on a trade. A hump that
  ends because old trades left is the push not being renewed: the stance is let go, not turned.
- BUILT IN, AND WHAT IS LEFT: (1) the trade that begins the hump can itself take out the best offer and step it in
  the same exchange event (the stored column `next_ask_step_same_event` says so; not counted). (2) A hump that
  holds one trade ends exactly 20 seconds after it when nothing else trades: that end is set by the span, not by
  the market. (3) The dipole is read BEFORE the trade so that the trade itself is not in it. What is left: after a
  hump that began on a trade, what came first was the quote it was hitting stepping, or more trading on its side,
  far more often than the other side (the paper's finding 6).
- OBSERVATION / PROPOSED RULE: observation: finding 6, not yet split by where the dipole stood. Proposed rule: take
  the side of fresh trading that agrees with the 60-second flow.
- WHAT WOULD SHOW IT WRONG: in a cell, after such a hump the quote it is hitting steps away (in a later exchange
  event) no more often than after a hump that began against the dipole (CL08).
- CELLS: side (buy, sell) by how the hump began (from empty, from zero, from the other side) by trade day. A hump
  that begins on a trade while the dipole line just before is EMPTY or AT ZERO is its own cell: no stance, counted.
- READ FROM WHAT IS STORED TODAY: yes (`research-humps`, `crypto-ng-tick-lean-60s`, `calc-research_columns`).
  The split by the dipole's side is NOT COUNTED YET.

## CL08. Fresh trading against the dipole (changeover)

- STAGE AND SITUATION: (4) the turn, as a transition. The exhaustion line comes onto one side ON A TRADE while the
  60-second flow still stands on the OTHER side: the first fresh trading against the flow that has been in charge.
- OBSERVED, AND KNOWN AT: as CL07 (a hump that begins on a trade; the dipole line just before that trade), and then
  the first step of the quote the hump is hitting with its stored mark `next_bid_step_same_event` or
  `next_ask_step_same_event`.
- THE STATE: the hump began on a trade, and the dipole line just before the trade stood on the other side.
- DIRECTION: two uses, kept apart. (a) A WARNING, no direction: a with-the-old-flow stance of any version is let
  go. (b) The proposed rule: with the NEW hump, but only once the quote it is hitting has stepped away in a LATER
  exchange event than the hump's first trade, and before the hump has ended.
- TAKEN / LET GO / AGAIN: (a) at the end of the exchange event of the hump's first trade. (b) at the end of the
  exchange event of that later quote step. Let go when the hump ends or at that quote's first step back,
  whichever comes first. Again at the next such hump.
- MANAGEMENT AND INVALIDATION: (b) is never taken if the hump ends first. Invalidated by the other quote stepping
  the old way before the confirming step.
- BUILT IN, AND WHAT IS LEFT: the confirming step must lie in a later exchange event so that the hump's own trade
  is not counted as its own confirmation. What is left after the confirming step is a run that has just started,
  and most runs end at one step.
- OBSERVATION / PROPOSED RULE: no count. Against it, by eye on five pictures (running notes, fifteenth session):
  the two lines turned after the price, never before. Proposed rules: (a) and (b) above.
- WHAT WOULD SHOW IT WRONG: in a cell, after such a hump the first quote step in a later exchange event is the
  other quote stepping the old way as often as the hit quote stepping the new way.
- CELLS: side by how the hump began by trade day.
- READ FROM WHAT IS STORED TODAY: yes (the same files as CL07). NOT COUNTED YET.

## CL09. A change of side made by the span: no signal

- STAGE AND SITUATION: any stage. The exhaustion line changes side, or a hump begins, at a moment with NO TICK:
  old trades have left the 20 seconds and nothing new has traded.
- OBSERVED, AND KNOWN AT: the stored read's own words (`what` in the line table; `began_on` and `ended_on` in
  `research-humps`: "trades left the span at a moment with no tick"). Known at that moment, and placed on the
  last tick received before it.
- THE STATE: the hump began as old trades left.
- DIRECTION: none.
- TAKEN / LET GO / AGAIN: no stance is ever taken on it by any version. It never counts as "the other side
  arriving", never invalidates a stance, and never turns one.
- MANAGEMENT AND INVALIDATION: it still ENDS a hump: a with-the-hump stance (CL07, CL08) is let go when its hump
  ends this way, because the push was not renewed inside the span.
- BUILT IN, AND WHAT IS LEFT: the whole event is made by the 20-second span. Nothing is left: after such a hump
  the next trade is on its side about as often as on the other side.
- OBSERVATION / PROPOSED RULE: observation (the paper's findings 5 and 6): about three humps in ten are made by
  the span, and such a hump carries no direction. Proposed rule: none is acted on.
- WHAT WOULD SHOW IT WRONG: in a cell, the first trade after a span-made hump is on its side much more often than
  on the other side. How much more is a number of Greg's.
- CELLS: side by trade day, with and without a trade inside the hump.
- READ FROM WHAT IS STORED TODAY: yes, and counted in the paper.

## CL10. The price runs against the dipole: with the price

- STAGE AND SITUATION: (2) the middle. A run of the quote has taken its second step while the 60-second flow stands
  on the OTHER side: the price is falling while the hitting side is buying (or rising while it is selling). The
  hitting side is being met and the standing side is leaning on it.
- OBSERVED, AND KNOWN AT: the run's second step (`new furthest price`, `moves` 2) and the stored dipole line on
  that tick's row (`dipole_60s`), by place. Known at that tick.
- THE STATE: the dipole line stands against the direction of the run at its second step.
- DIRECTION: WITH THE PRICE (the run's direction).
- TAKEN / LET GO / AGAIN: taken at the end of the exchange event of the second step. Let go at the run's first
  step back. Again at the next run's second step.
- MANAGEMENT AND INVALIDATION: the dipole crossing to the price's side is written on the stance's line when it
  comes; in the one case seen it came only after the move had ended, so it is not used to let go.
- BUILT IN, AND WHAT IS LEFT: nothing is built in between a quote's steps and the side of the 60-second flow when
  they disagree. What is left on the followed quote: as CL01 (one tick behind at two steps, level at three).
- OBSERVATION / PROPOSED RULE: one case, by eye (running notes, fifteenth session: trade day Oct 18, trade leg
  2990, a fall of six steps with the dipole on the buying side throughout). At the FIRST step the counts say
  little either way. Proposed rule: stay with a move the hitting side is fighting.
- WHAT WOULD SHOW IT WRONG: in a cell, runs in this state take a third step no more often than runs whose second
  step had the dipole on their side. CL11 is the opposite stance on the same events.
- CELLS: quote and direction (four) by trade day.
- READ FROM WHAT IS STORED TODAY: yes (`calc-quote_runs-facts`, `calc-research_columns`). NOT COUNTED YET at the
  second step.

## CL11. The price runs against the dipole: against the price

- STAGE AND SITUATION: (2) into (4). The same state as CL10, read the opposite way: a move of the price that the
  60-second flow does not back is expected to fail.
- OBSERVED, AND KNOWN AT: as CL10.
- THE STATE: as CL10.
- DIRECTION: AGAINST THE PRICE (toward the dipole's side).
- TAKEN / LET GO / AGAIN: taken at the end of the exchange event of the second step. Let go at the run's first
  step back, which is the event it expects. Again at the next run's second step.
- MANAGEMENT AND INVALIDATION: invalidated by a third step.
- BUILT IN, AND WHAT IS LEFT: as CL10. What is left, on the followed quote alone: one tick when the run ends at
  two steps.
- OBSERVATION / PROPOSED RULE: no count at the second step. At the first step, runs with the dipole against them
  took a second step a little less often than runs with it behind them in most cells, not all. This is the plain
  form of the crypto divergence read (which side the flow is on against which way the price goes); the crypto
  formula `divergence` itself is not built for natural gas and no crypto figure is carried. Proposed rule: fade a
  move the flow is against.
- WHAT WOULD SHOW IT WRONG: the mirror of CL10: in a cell, runs in this state take a third step as often as runs
  with the dipole behind them. Every event is on one line read two ways: where CL10 is right, CL11 is wrong.
- CELLS: as CL10.
- READ FROM WHAT IS STORED TODAY: yes. NOT COUNTED YET at the second step.

## CL12. The reloaded level

- STAGE AND SITUATION: (2) into (4), and management. A resting order at the best price is traded against and shows
  the same size or more straight after: somebody is taking the trades and reloading.
- OBSERVED, AND KNOWN AT: a fact of `calc-refills-facts` with size put back (`size_put_back` above nothing,
  `same_size_or_larger` yes) on an order at the best price (`levels_from_best` 0), with its `side`, `price`,
  `order_number` and `times_put_back_so_far`. Known at the tick of the order's own row in the exchange event that
  filled it.
- THE STATE: an order at the best price being hit has had size put back and is the same size or larger.
- DIRECTION: two uses, kept apart. (a) MANAGEMENT, no direction: a stance that pushes INTO that level (CL01, CL03,
  CL04, CL05, CL07) is let go. (b) The proposed rule: AGAINST the push (down when an offer is reloaded, up when a
  bid is).
- TAKEN / LET GO / AGAIN: taken at the end of that exchange event. Let go at the tick that order leaves (its own
  row says "left by fill" or "left by cancel") or the tick the level empties, whichever comes first. Again at the
  next reload on another order.
- MANAGEMENT AND INVALIDATION: invalidated when the reloading order leaves by fill and the level then gives way:
  the defence was eaten, which is CL03's state at a level that had been defended.
- BUILT IN, AND WHAT IS LEFT: the reload is in the same exchange event as the fill, so the book shows less change
  than the fill, or none: that the quote does not step in that event is built in. What is left is NOT KNOWN.
- OBSERVATION / PROPOSED RULE: no count against the moves (the running notes: refills "not looked at"). What is
  stored: how many such facts and orders each trade day holds. Proposed rules: (a) and (b) above.
- WHAT WOULD SHOW IT WRONG: in a cell, levels with a reloaded order give way to the push as often as levels being
  hit with none.
- CELLS: side (offer reloaded; bid reloaded) by first reload or a repeat on the same order, by trade day.
- READ FROM WHAT IS STORED TODAY: yes (`calc-refills-facts`, the rows). NOT COUNTED YET.

## CL13. Paying up through more than one level

- STAGE AND SITUATION: (2) the middle. One exchange event holds a trade that fills through MORE THAN ONE price
  level: somebody paid up to get done at once.
- OBSERVED, AND KNOWN AT: the `trade event` fact of `calc-sweeps-facts` (`price_levels_filled`, `aggressor_sides`,
  `size_bought`, `size_sold`, `best_bid_moved`, `best_ask_moved`, the best prices before and after). Known at the
  tick that carries the exchange's end-of-event mark.
- THE STATE: `price_levels_filled` is more than one, and the event has one aggressor side.
- DIRECTION: with the aggressor (up for a buy that paid up).
- TAKEN / LET GO / AGAIN: taken at that end-of-event tick. Let go at the first step back of the quote that was
  swept. Again at the next such event.
- MANAGEMENT AND INVALIDATION: an event with more than one aggressor side takes no stance. CL12 and CL14 speak
  during it.
- BUILT IN, AND WHAT IS LEFT: the event has already moved the quote by the levels it filled; those steps are the
  event, not what follows it. What is left is only what happens in LATER exchange events, and that is NOT KNOWN.
  The opposite reading is as likely on its face: the book fills in behind a sweep and the quote comes straight
  back. Each event's line shows which happened.
- OBSERVATION / PROPOSED RULE: no count. Stored: every trade event of each trade day and the most levels one event
  filled. Proposed rule: follow an aggressor who paid up.
- WHAT WOULD SHOW IT WRONG: in a cell, after such an event the swept quote's next step in a later exchange event
  is a step back as often as it is after an event that filled one level and moved the quote.
- CELLS: aggressor side by trade day. How many levels (two, three, more) is written on each line, not grouped.
- READ FROM WHAT IS STORED TODAY: yes (`calc-sweeps-facts`, `calc-quote_runs-facts`). NOT COUNTED YET.

## CL14. The other side arrives at a fresh quote

- STAGE AND SITUATION: (4) the turn, and management. The best bid has been stepping up. Its top step is a new,
  better bid that has just come in. A SELL prints at it: the other side has arrived at the newest and usually
  thinnest level of the move. (The mirror: the best offer stepping down and a BUY printing at it.)
- OBSERVED, AND KNOWN AT: the run of the best bid in progress is up (`bid_run_direction`) and has not stepped back;
  a trade row with the tape's own side selling, at the best bid's price; and at the tick before it the size at the
  best bid against the size at the best offer (`best_bid_size`, `best_ask_size`). Known at the end of the trade's
  exchange event.
- THE STATE: a trade on the other side has printed at the top level of a run of the quote that is still under way,
  and that level still stands at the end of the exchange event. (When the trade empties it, the run has already
  taken its first step back and there is nothing left to decide.)
- DIRECTION: two uses, kept apart. (a) MANAGEMENT, no direction: a with-the-move stance of any version is let go
  here, one event before the first step back would show the end. (b) The proposed rule: AGAINST the run.
- TAKEN / LET GO / AGAIN: taken at the end of that exchange event. (b) is let go at the run's first step back,
  which is the event it expects. Again at the next run.
- MANAGEMENT AND INVALIDATION: (b) is invalidated by the run's next step the same way.
- BUILT IN, AND WHAT IS LEFT: selling into the bid is what stops the bid's rise, so that the other side is found
  at the end of a move is partly built in. What is NOT built in is the level still standing after the print. What
  is left for (b), on the followed quote: one tick at the first step back.
- OBSERVATION / PROPOSED RULE: observation (running notes of 2026-11-17, stage 4, on the rebuilt rows, the peak
  with no window): at the end of a move of the quote the run of trades in play was on the OTHER side about three
  times in four, was short, and most often hit the thinner of the two best levels. The notes call the reading
  itself "to test, not shown". Proposed rules: (a) and (b) above.
- WHAT WOULD SHOW IT WRONG: in a cell, after the state the run's next step is a step back no more often than it
  is at any other tick of a run still under way.
- CELLS: quote and direction (best bid up hit by a sell; best offer down hit by a buy) by whether the level hit
  was the thinner of the two best levels, by trade day.
- READ FROM WHAT IS STORED TODAY: yes (the rows, `calc-quote_runs`, `calc-turn_peaks`). NOT COUNTED YET in this
  form.

## CL15. The step back and the return

- STAGE AND SITUATION: (5) after. A run of the quote that took two steps or more has ended with its first step
  back. The step back is one step. The quote then steps the ORIGINAL way again.
- OBSERVED, AND KNOWN AT: three facts of `calc-quote_runs-facts` in a row for one quote: a `first step back` whose
  run made two moves or more (tick TB, which also starts the run back); that run back ending after ONE move (tick
  TR, which also starts a new run the original way). Known at TR.
- THE STATE: at TR the quote is again at the price the first run ended at, having given back one step and taken
  it again.
- DIRECTION: the original direction.
- TAKEN / LET GO / AGAIN: taken at the end of the exchange event that holds TR. Let go at the new run's first step
  back. Again at the next such return.
- MANAGEMENT AND INVALIDATION: a run back of two steps or more takes no stance: the move is no longer a one-step
  pause.
- BUILT IN, AND WHAT IS LEFT: nothing is built in. What is left is NOT KNOWN: "do large moves come back" is not
  answered (the stored figure is only the first step back), and Greg has saved that question for later.
- OBSERVATION / PROPOSED RULE: observation: the first step back of a run is one tick nearly every time. That says
  the step back is small; it does not say the move comes again. Proposed rule: a one-step pause after a real move
  is a place to rejoin it.
- WHAT WOULD SHOW IT WRONG: in a cell, the new run takes a second step no more often than any run does.
- CELLS: quote and direction (four) by trade day. The number of steps of the first run is written on each line,
  not grouped.
- READ FROM WHAT IS STORED TODAY: the facts are stored, but COUNTING IT IS PART OF THE RESEARCH GREG HAS SAVED FOR
  LATER (`FURTHER_RESEARCH_LIST.md`, item 4). It cannot be evaluated until he opens that item.
