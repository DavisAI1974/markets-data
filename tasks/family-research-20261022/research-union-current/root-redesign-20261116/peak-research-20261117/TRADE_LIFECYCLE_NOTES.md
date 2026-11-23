# The life of a price move, and what each piece of data tells about each part of it

Working notes, started 2026-11-17 on Greg's word: "we absolutely need to be writing your notes down or they will be
forgotten about in 10 min". ADD TO THIS FILE as things are learned; do not start a new one.

Greg's frame: "we don't have to pick winners. We just want the story. What part of the story does peak tell us and
what other thing or things fill in the exact parts that peak can't."

How to read the numbers: every count is from one trade day read on its own (trade day Oct 2, 2023 unless named).
The other three trade days (Oct 3, 17, 18) read the same way wherever a line says "all four". Every count for all
four trade days is in the JSON files beside this one and in `README.md`. Nothing is averaged. No test of chance
has been made on anything here: these are counts, and each is a lead, not a result.

## The generic move

One move of the quote in one direction (the best ask going up, or the best bid going down), drawn going up:

```
            (3) last step
              ____
         ____/    \____  (4) the turn: first step back
    ____/  (2) middle  \____
___/ (1) first step          (5) after
(0) before
```

Most real moves are far smaller than this picture: on trade day Oct 2, 10,597 of 13,331 runs of the best bid and
3,878 of 6,118 trade legs were ONE step long. A one-step move is its own beginning and end.

## Stage by stage: what each piece says there

### (0) Before the move
- THE PEAK: nothing yet. A peak is only known after its high.
- THE BOOK AT THE BEST PRICE: holds the size and number of orders the move will have to get through. Read only
  just after a peak's trade so far, not before.
- NOT LOOKED AT: the outside figures (weather, forecasts, storage) changing before a move; how old the standing
  level is; Native's missing 6 pm to 8 pm on trade days Oct 2 and Oct 17.

### (1) The first step
- THE QUOTE'S RUNS say a move has started, at that tick. They are the only thing that holds the price.
- THE PEAK WITH NO WINDOW at the beginning of a move is a TALL one (1,225 of 2,599 are 6 lots or more) and pushes
  WITH the move (1,681 of 2,599). All four.
- THE STANDING ORDERS: at the best price the peak pushed into, an order was filled out at 1,522 of 2,647
  beginning peaks, pulled at 708, every order still there at 813 (20-second peaks). All four.
- KNOWN AT THE TIME: that the quote stepped; the peak's side and height. NOT known: that this is a beginning and
  not a one-step flicker.

### (2) The middle
- THE PEAK WITH NO WINDOW in the middle is the TALLEST pile (630 of 1,339 are 6 lots or more) and pushes with
  the move (854 of 1,339). All four.
- THE STANDING ORDERS: the middle peaks most often ate through an order (733 of 1,038) and least often left every
  order standing (195 of 1,038).
- HOW THE LEVEL EMPTIED says whether the move goes on (see stage 3). The peak cannot see this.

### (3) Whether it takes another step
- THE STANDING ORDERS, on the quote's own clock, are the piece that speaks here. When the quote backs away, the
  level it left emptied: part eaten by trades and part pulled out (959 moves, best ask up), every order pulled out
  (212), every order eaten (123). So about seven times in ten the orders left on a level that is being hit leave.
- Moves that took a third step: every order eaten 53 of 123; some of each 362 of 959; every order pulled 63 of
  212. In ALL EIGHT rows (four trade days, ask up and bid down) the pulled-only moves went on LEAST often.
  A level that was only abandoned leads nowhere; a level that was eaten leads on.
- THE PEAK reads the same in all three: the pushing side was hitting in 118 of 123, 186 of 212 and 944 of 959.
- Size is almost never put back straight away (7 of 1,038 in-between peaks). No quick defending was seen.
- LIMITS: the eaten-only and pulled-only rows hold 100 to 250 moves; only the first level of a move is followed.

### (4) The turn
- THE PEAK ON THE OTHER SIDE marks it. At the end of a move of the quote, the peak with no window there is on the
  OTHER side about three times in four (pushing with the move: only 506 of 1,837). All four. It is the other
  side arriving, not the pushing side running out.
- It is a SHORT peak (627 of 1,837 are 6 lots or more; 521 are a single lot) and it most often hits a level that
  is the thinner one at the best price (1,345 of 1,837).
- A reading to test, not shown: a small quote steps in one tick better, a small trade takes it out, the quote
  snaps back. That would be one event seen three ways (short, other side, thin level).
- THE 20-SECOND PEAK sees this stage worst: the end pile shares its high with a 20-second peak least (719 of
  1,837, against about half elsewhere).
- KNOWN AT THE TIME: the peak's side, its height, the size at the best price. NOT known: that the move has ended;
  that is only known at the first step back.
- Partly built in: selling into the bid is what stops the bid's rise.

### (5) After
- WHERE THE PRICE STOOD at the end of a 20-second peak's story: about even three ways in every pile (in between:
  further the peak's way 344, back against it 318, where it was 376). All four. The peak alone does not say where
  the price goes.
- NOT LOOKED AT: what the price did after a peak with no window; the next move after a turn; the chain (the peak
  after) beyond "the peak before was on the same side", which read the same in every pile.

## What each piece is, in one line each

| Piece | What it tells | What it cannot tell |
|---|---|---|
| The peak with no window | Who was hitting, which side, how many lots, when it changed hands. Every one is a real change of hands. | Any price. Where in a move it is. What the standing orders did. |
| The 20-second peak | The same, smoothed over 20 seconds; the earlier family and chain work stands on it. | A little over half share their high with a no-window peak (5,403 of 9,525). 2,660 of 9,525 have their high on a tick with NO trade: made by old trades dropping out of the window. More than half of the no-window peaks have no 20-second peak at their high. Its height barely differs by pile. |
| The quote's runs, `move_steps` | Whether the price moved, how far, each step, when it ended. | Why. |
| The trade legs | The prints' own path. | Close to built in against the peaks (a buy prints at the ask). 3,878 of 6,118 are one step. |
| The book at the best price | What the peak pushes into. | The whole book's lean told nothing (even in every pile). The gap is one tick nearly always. |
| The standing orders (`resting`) | Whether a level was eaten or abandoned, and so whether the move goes on. | At the moment of a peak, a beginning from an end (they read alike). |
| Native's dipole | That a fully one-sided burst happened: every dipole is born in a second with the flow fully one-sided. | It is known late (526 of 741 exactly 50 seconds after the birth, Native's own fixed span); by then the flow on its side has already reached zero for 515 of 741; over half are born where no peak's high sits; it did not help place a peak. |
| The outside figures | Not looked at. | |
| Refills, orders together, sweeps | Not looked at against the peaks. | |
| Native's stages after recognition, the Bedrock layers | Not read. The Bedrock layers were not found stored for these trade days. | |

## Guesses that turned out wrong (kept so they are not made again)

- "If the peaks sit at the turns, a huge problem is solved." Against the runs of the quote a peak's high is at the
  end of a move as often as ANY print is (5,663 of 9,525 against 22,526 of 38,126). The lean is only toward the
  ends of trade legs, and that is partly built in.
- "The red line in the picture shows the peaks tracking the price." Any 8,619 points off a tape of 33,703 trades
  trace the price; the random points in the lower panel did the same.
- "Orders that stand make an ending; orders that pull away make a beginning." Not borne out: an order was pulled at
  about a quarter of the peaks in every pile. And on the quote's own clock it is the other way round: a level that
  was only pulled leads nowhere.
- "The whole book's lean will matter." It did not. Only the best price did.
- "Native's dipole will help place a peak." It did not, as read so far.

## Curious questions still open

1. How old was the level a peak hit? If the end peaks hit quotes that had just stepped in, the reading under
   stage (4) holds.
2. What did the price do after each pile of peaks with no window (not only the 20-second ones)?
3. The same "eaten or abandoned" read at every level of a move, not only the first.
4. Do the tall peaks sit near an outside figure changing?
5. Refills and orders moving together: are the eaten levels the ones somebody refilled later?
6. Why does Native's dipole not separate the piles at all? What do its stages say after recognition?
7. The five-step process (`DavisAI1974/Basic_equations`, `level2_four_sciences.py` lines 10 to 20): which two
   streams. The natural pair from these notes is the hitting side (the peaks) and the standing side (the resting
   orders). It uses windows and an ensemble as written: Greg's calls before anything is run.
8. Read the step lines by each move's own length: do long moves read differently from one-step flickers?

## Where everything is

- This folder: `README.md` (each read written out), one `peaks-by-place-in-the-move-<trade day>.parquet` per trade
  day (every peak with its pile), and the count files: `COUNTS.json`, `ATTRIBUTES_BY_PILE.json`,
  `HEIGHT_BY_PILE.json`, `TWO_KINDS_OF_PEAK.json`, `BOOK_ANSWER_BY_PILE.json`, `HOW_A_LEVEL_EMPTIED.json`,
  `DIPOLE_AGAINST_PEAKS.json`.
- The stored data it was read from: the four `root-rows-<trade day>` branches (`calc-turn_peaks-*`,
  `calc-move_steps-*`, `calc-resting-*`, `calc-leg_peaks-*`, `dipole-peaks-*`, `calc-chain_peaks-*`,
  `calc-peak_story-*`, `calc-flow_peak-*`, the rows). Each branch's `FILES.md` explains every file.
- Every read here used all four trade days. None of it may be used to form a strategy version for the trade day
  that version is traded on.

## Native's dipole, reverse engineered (2026-11-17, Greg: "That 50 sec line sounds like an artifact ... pin the dipoles to their timestamps and then see what there's to see")

Read from Native's stored lines and from OUR tape (the stored rows and our own 20-second flow), in the session,
told to Greg first. Each trade day on its own; the four read the same way.

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| Dipoles | 741 | 833 | 741 | 863 |
| Native's threshold exactly 1 | 741 | 833 | 741 | 863 |
| Native's magnitude exactly 1 | 741 | 833 | 741 | 863 |
| Native's prominence exactly 0 | 71 | 96 | 65 | 80 |
| NO trade at all in the birth second | 453 | 498 | 474 | 548 |
| One trade in the birth second | 210 | 254 | 207 | 227 |
| OUR flow fully one-sided, its side, at the end of the birth second | 538 | 610 | 476 | 596 |
| OUR flow NOT fully one-sided there | 194 | 207 | 243 | 236 |
| OUR flow already fully one-sided on its side one second earlier | 219 | 236 | 185 | 247 |
| Seconds of the trade day with OUR flow fully one-sided | 18,960 of 82,799 | 20,068 | 18,987 | 18,773 |
| Smallest number of seconds between one birth and the next | 45 | 45 | 45 | 45 |
| Births exactly 45 seconds after the one before | 99 | 116 | 105 | 112 |
| Known exactly 50 seconds after the birth | 526 | 584 | 545 | 599 |

What this says:
- A dipole, as recorded on these trade days, is a mark put on a second in which the 20-second flow is fully
  one-sided. The level it must clear is 1 on every dipole, so the level selects nothing.
- Our flow is fully one-sided in about 19,000 to 20,000 seconds of each trade day. Native marks 741 to 863 of
  them. What decides which: spacing. No two births are closer than 45 seconds, and exactly 45 seconds is the
  most common gap by far. The 45 seconds and the 50 seconds are both constants of the detector, not of the market.
- More than six dipoles in ten are "born" in a second in which nothing traded. The flow was one-sided there only
  because earlier trades were still inside the 20 seconds.
- For about a quarter of the dipoles our own 20-second flow is not fully one-sided at the birth second. Native's
  record and the tape do not agree there. Why is not established (Native bins by whole seconds and may use a
  different clock; its per-second flow lines are in the stored ledger and have not been read).
- For about three in ten the flow had already been fully one-sided a second earlier, so the birth is not where
  the one-sidedness began.
- So Greg's reading stands on the evidence so far: the 50-second line is made by the detector. And more than
  that: the dipoles themselves, as recorded, are mostly marks spaced by a rule along stretches of one-sided flow,
  not separate market events. This is what Native's stored record shows; it does not say the DIPOLE DIVE (the flow
  lean diving into a turn and recovering) is not real. That is looked at in the renders, one per dipole, pinned at
  the birth second.

### The dipoles born WITH a trade are a different thing from the rest (Greg: "That's fine if some were born with no trades, what about the ones that were")

Read from the stored files in the session (told to Greg first); counts in `DIPOLES_BORN_WITH_A_TRADE.json`.

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| Born WITH a trade in the birth second | 288 | 335 | 267 | 315 |
| ... every trade in that second on the dipole's side | 281 | 327 | 255 | 295 |
| ... our flow fully one-sided on its side right after | 274 | 321 | 250 | 288 |
| ... the birth second is where our flow BECAME fully one-sided | 271 | 311 | 256 | 308 |
| ... a 20-second peak's high on its side in that second | 264 | 302 | 240 | 281 |
| ... a no-window peak's high on its side in that second | 133 | 144 | 118 | 130 |
| ... born exactly 45 seconds after the one before | 6 | 6 | 5 | 7 |
| ... a single lot traded on its side | 169 | 203 | 159 | 159 |
| Born with NO trade in the birth second | 453 | 498 | 474 | 548 |
| ... our flow fully one-sided on its side right after | 264 | 289 | 226 | 308 |
| ... a 20-second peak's high on its side in that second | 65 | 79 | 54 | 69 |
| ... born exactly 45 seconds after the one before | 93 | 110 | 100 | 105 |

- The dipoles born with a trade agree with our tape almost every time. They mark the second in which a trade
  made the 20-second flow fully one-sided, and about nine in ten are the same event as an exhaustion peak (a
  20-second peak's high in that same second, on the same side). Almost none are spacing marks.
- The dipoles born with no trade are where the 45-second spacing rule shows up.
- More than half of the dipoles born with a trade are a single lot: on a thin tape one small trade after a quiet
  stretch makes the 20-second flow fully one-sided.
- So the part of Native's dipole record that is a real event on the tape is, as far as read, the exhaustion peak
  whose flow is fully one-sided. Whether it does the dipole dive is what the renders are for.

## SAVED FOR THE NEXT SESSION: the stacked pair of graphs (Greg, 2026-11-17)

His words: "we should have 2 graphs stacked on top and bottom of each other for the dipoles and trades that are
associated with each other with the x axis being the timestamps and the y axis being price for one graph that has
the the line for that ones trade and the other grapd being the dipole line as it moves up and down. I wonder if
there are changes that happen at the same time ir very close and they might be in different directions which
doesn't matter. It's the movement thay matters". Then: "Save rhat for next session".

What it asks for:
- One picture for each dipole and the trade associated with it. Two graphs, one above the other, on the SAME
  time axis (the real timestamps).
- Top graph: price, with the line for that trade.
- Bottom graph: the dipole line as it moves up and down.
- The question: do the two change at the same moment, or very close to it? Direction does not matter (they may
  move opposite ways). What matters is that they MOVE together.

To settle with him before it is built (not decided here):
- Which "trade" goes with a dipole: the trade leg under way, the run of the quote, or the run of trades on one
  side.
- What "the dipole line" is drawn from: our own 20-second flow lean, the flow with no window, or Native's own
  per-second flow lines (stored in its ledger, not read yet).
- How "at the same time or very close" is counted without choosing a span of time. One way with no window: for
  every tick where the dipole line changes, the number of ticks to the nearest tick where the price line changes,
  each change on its own line.
The dipole renders made on 2026-11-17 (`renders/dipole-render-*.png` on each `root-rows` branch) already stack the
price above the flow lean on one clock; this idea is the sharper version, built around the moments of change.

## (CORRECTED BELOW by Greg the same hour: the 20-second version is KEPT and the tick version ADDED) The flow lean at the tick

Greg, on seeing the first renders: "We need to make flow lean nano too and not 20 sec windows." Claude first
recorded this as the 20-second exception being withdrawn. THAT WAS WRONG: the same hour he said "You can keep the
20 sec but we need to add nano". The 20-second flow is KEPT and a line made at the tick is ADDED beside it. Twelve
of the seventeen stored calculations stand on the 20-second window in whole or in part (listed in the decisions
file). They stay stored; the versions made at the tick are made beside them. Still to settle with him: what the lean compares once the clock is gone
(Claude's pick: buying against selling since the price move under way started, with the run of trades on one side
beside it). The first renders were too crowded for him to read; the next ones are his stacked pair, price above
and one flow line below.

## FOR THE NEXT SESSION, in Greg's words (2026-11-17): the three-tier picture, and nano beside the 20 seconds

"Do a 3 tier. Make notes for next session. Price, dipole and exhaustion in 3 different graphs. You can keep the 20
sec but we need to add nano if we're going to be pinning and comparing to nano timed things."

What to build:
- ONE picture, THREE graphs stacked, sharing one time axis of real timestamps:
  1. the price;
  2. the dipole;
  3. the exhaustion.
  Three separate graphs. Not lines laid over each other (the first renders were too crowded for him to read: "I can
  tell that they are the same length but it's a little confusing for me to see anything else").
- KEEP the 20-second flow and everything made on it. ADD a version made at the tick ("nano") beside it. Reason, his:
  a line that is pinned and compared against things timed to the nanosecond must be timed the same way.
- This joins his earlier saved idea (the stacked pair: do the price and the dipole line MOVE at the same moments,
  whatever the direction). The three-tier picture is the fuller form of it.

To settle with him before it is built:
- What the tick-level line compares once the clock is gone (three ways are in the decisions file; Claude's pick:
  buying against selling since the price move under way started, with the run of trades on one side beside it).
- What goes in the dipole graph: Native's dipole marks (born with a trade, born with none), our own flow lean, or
  both. And what goes in the exhaustion graph: the 20-second exhaustion peaks and their stories, the peaks with no
  window, or both.
- Which stretch of time one picture covers, with no span chosen by us (the first renders ran from the dipole
  before to the dipole after).
Known faults of the first renders to fix: the black line on the exhaustion pages is the last print and flips a tick
as trades alternate between bid and ask (use the quote); the page title is cut off at the top.

## Cautions added at the close of the session (2026-11-17)

- "About nine in ten dipoles born with a trade are the same event as an exhaustion peak" is close to built in. A
  trade that makes the 20-second flow fully one-sided sets a high of that flow by definition. It shows the two
  records agree where a trade prints; it is not a separate discovery.
- The counts of "our flow NOT fully one-sided at the birth second" (194, 207, 243, 236) were read on the last tick
  received before the second ended. Trades can drop out of the 20 seconds between that tick and the end of the
  second, with no tick to show it. So part of that disagreement between Native's record and our tape may be our own
  sampling at ticks, not Native. A line made at the tick with its own clock (the "nano" line) is what settles it.
- Everything in this file was read from all four trade days. A strategy version has to be formed blind to the trade
  day it is traded on. How the next session can read these notes and still keep that is Greg's call (see the
  handoff).

## Greg, at the close (2026-11-17)

- "I don't want to do the lines laid over initially. We might but not first." The three-tier picture is three
  SEPARATE graphs first. Lines laid over each other may come later; they are not the first thing built.
- "You might see some other additions to excel that desktop contributes." Desktop may add sheets or columns to the
  Excel files on the data branch. Fetch before touching them, expect its additions, and never write over them. If
  `ROOT_dipoles_pinned.xlsx` is written again, Desktop's sheets are kept.

## 2026-11-18: the 20 seconds go out of every calculation; exhaustion is worked out again with no window

Greg: "Then we need to recalc exhaustion like we did months ago and for cryptomo. I don't think we had 20 sec
windows then. Why does everything have 20 sec windows now? We can't use that data in any calculation". Before it,
of the three-tier picture: "I think the 3 renders stacked that i mentioned will give us a lot of insight."

- READ EVERYTHING ABOVE THIS LINE WITH THIS IN MIND: every count in this file that stands on a 20-second peak, on
  the 20-second flow or on Native's dipole is kept as a record and enters no calculation. That is most of "Stage
  by stage" wherever it says "20-second peak", the two tables on Native's dipole, and the 20-second rows of "What
  each piece is". What does not stand on it: the peaks with no window, the quote's runs, the trade legs, the
  standing orders through a run of the quote or a leg, the book totals, refills, sweeps, orders together.
- Where the 20 seconds came from: the exhaustion chain programs of August 2026 and Native. The rebuild's first
  piece was a rewrite of that detector and kept the roll; twelve of seventeen calculations took it in from there.
- What exhaustion was in July 2026 (natural gas, `month_characterize.py`): a read of the BOOK between two events of
  one move. The resting orders' lean toward the move at its start, minus their lean toward it at its high. With it:
  how much the side being eaten had thinned, and the gap at the high against the gap at the start. In crypto: the
  buy-against-sell balance moving back toward even (the late half of the bars before entry against the early half).
- Neither used 20 seconds. Both used some span (60 seconds, 30 minutes, 300 seconds, 30 bars). Under the rules of
  this work the span goes and the idea stays: the stretch is a move's own life, start to each step to end.
- A caution carried from stage (3) and "Guesses that turned out wrong": against the piles of peaks "the whole
  book's lean told nothing; only the best price did". That was read at the tick of a peak, not start-against-high
  of a move. It is not the same read, so it does not settle this one; both the best price and the whole side are
  written.
- A fact that limits it: most moves are one step long (trade day Oct 2: 10,597 of 13,331 runs of the best bid;
  3,878 of 6,118 trade legs). A one-step move has no "start against later". Its lines are written and are empty
  there. Nothing is filtered.
- The layout is in `STEP1_STEP2_LAYOUTS.md`, "Exhaustion with no window". Not approved, nothing built.
- The three-tier picture after it: price; the dipole made at the tick; the new exhaustion. Three different things.


## 2026-11-18: reference pictures Greg pasted into the session ("Here's some reference data. I'll paste more.")

The pictures themselves are in the chat, not in git. What each shows, as read off the image (nothing measured here):

1. "Dipole (flow) over Price, 2000 winners, aligned to the turn (x=0)". Top: the flow lean and the price (in bps,
   turned to the winning side) from 60 seconds before the turn to 60 after. Both fall into the turn and rise out
   of it: the DIPOLE DIVE. Bottom: the rate of change of each (the picture says corr +0.26); both spike at the
   turn. This is the crypto-era picture. It is 2,000 cases laid on top of each other and it is cut at 60 seconds
   each side: under the rules of this work the same thing is drawn one turn at a time, on real timestamps, with no
   span. Its lean line runs straight through the turn without restarting. A line that restarts when a move starts
   would break exactly there: an open point for the flow form of the layout, to settle with him.
2. Three pictures titled "SAME births: four days overlaid": "Aggressor run start", "Touch-size change", "Quote
   relocation". Each: Native's recognition time minus the time of the first such event, every birth in order of
   size, one line per trade day (387, 449, 387, 472 births; "Oct 2 and 17 are partial sessions"). All three sit on
   a flat shelf at about +50 seconds: the 50-second wait of the detector. Greg circled the left end of each, where
   the lines leave the shelf (recognition up to several hundred seconds BEFORE the first event on two of them).
   These carry the look of the earlier, partial run; where they were made is not known to this session.
3. "Share of candidates whose midpoint is above / below its anchor-boundary level, oriented by birth direction",
   four trade days (741, 824, 740, 852), against a grey band of 500 matched-control draws, 60 seconds before the
   birth second to 160 after. After the birth the price is on the birth's side more often than the controls on
   all four. Before it, on all four panels and in both rows, the line breaks sharply about 20 seconds before the
   birth. A reading, not measured: that break is the 20-second window showing itself (a birth is the second the
   20-second flow turns fully one-sided, which is when the last trade of the other side drops out of the 20
   seconds).

## 2026-11-18: how exhaustion was made in crypto, and the first three-tier samples

(THE FIRST TWO POINTS UNDER "FOUND IN THE CODE" ARE WRONG. See the correction in the next section: the July 7
crypto exhaustion graphs were a 20-second roll of trades.)

Greg, of the crypto exhaustion graphs (July 7, "Kraken onset->exhaustion"): "this is how we should be calcing
exhaustion"; "The crypto exhaustion graphs were basically good wnough on their own to trade from"; of Desktop's
earlier pictures: "desktop started doen this road. We need to continue down.it ... the foundation has been laid to
get to the crypto level putput renders".

- FOUND IN THE CODE (`archive/crypto`: `research/shape_s71/`, `S77_REVIEW_FOR_CHATGPT.md`): the crypto line was the
  lean of the RESTING BOOK (bid size against ask size, ten levels nearest the price, once a second). No roll of
  trades, no 20 seconds. A book's lean is a state at a tick; it needs no window. The July natural gas exhaustion
  (the book's support for a move, at its start against at its high) is the same idea.
- So "exhaustion" in this work is the STANDING side: the resting orders leaning toward a move and then letting
  go. The 20-second trade flow was a different thing that took the name in August.
- Each crypto trade was followed whole (before its onset; onset to where it flattened). Four kinds were kept
  apart: short or long by the median length, winner or loser by the result. Those are labels made afterwards and
  a median; here the cases are drawn one by one and the data does the grouping.
- From the same work, four days later, kept so it is not forgotten: matching the entry shape to the winner shapes
  did not lift the result; winner and losing twin shared the entry shape; direction came from the book's lean,
  the shape told how much and how long.
- His July 7 graphs break at exactly 0 and exactly 20 seconds on every line. Made by the picture, not the market;
  the script is not kept, so which way is not known.
- Desktop's earlier picture "Flow lean and midpoint around the birth" shows the 20-second window plainly: the
  lean sits at +1 from the birth and drops at 20 seconds after; its dotted lines are at 0 and at 20 before.

THE FIRST SAMPLES (trade day Oct 17, from 11:58:32.200 Eastern; in the session; not stored): price; the hitting
side (the run of trades on one side); the standing side (the resting orders' lean).
- By eye, one stretch, nothing measured: the lean at the best bid against the best ask alone flips end to end tick
  by tick. The lean of the whole book is a steady line that rose and fell with the price over eight minutes.
  Earlier in this file: "the whole book's lean told nothing" at the tick of a peak. Read along a move it may tell
  more. A lead to follow, not a result.
- Missing between the two: the lean over the few levels nearest the price (crypto's ten). Not on the rows; a new
  calculation.
- Still to settle with Greg: the stretch one picture covers; what an "onset" is with no span and no level to
  clear (the first step of a move of the quote is the stored candidate); whether a picture that lays cases
  together is wanted, by name.

## 2026-11-18, CORRECTION: the crypto exhaustion graphs WERE the 20-second flow (kept so it is not got wrong again)

Found on Greg's question about refrag. The script that drew his July 7 picture is on Markets branch
`claude/davisai-s71-counterparty-capacity-sf1168`: `research/shape_s71/regroup2.py` (with `shape_arc.py`,
`arc_gate.py`, `two_shapes.py`, `SESSION_HANDOFF_2026-07-07_S71.md`, `SIGNAL_SHAPE_DIRECTION_S71.md`).

- The line: bought minus sold over bought plus sold, over a ROLLING 20 SECONDS of trades, on a time
  grid, turned to the trade's side, 45 seconds before the trade's entry to 60 after. Each drawn line is the mean
  over the trades of one kind. Not the book. Not window-free.
- Why 20 seconds, in that script's words: trades were sparse; a shorter window made each trade's line "a saturated
  0/1 square wave". The 20 seconds began there (crypto, July 7) and the August natural gas detector kept it.
- Refrag (now DeepNova) was not used for those graphs. It was used on crypto in June for the per-trade fingerprints.
- The onset there was the entry of a trade made by the platform's own turn detector (a zigzag of the lean with a
  reversal level), not a mark on the tape by itself.
- What that session found (its handoff): the arc "rhymes" from trade to trade; the part before the onset told the
  kind of trade out of sample on all five coins (the taller the peak at the onset, the longer and the more often
  a winner); how long the trade lasted set where the collapse landed.
- What it means here: the picture Greg wants and the 20-second flow are one thing. Either the 20 seconds is kept
  as the one exception (his drop-in's rule) and the arcs are drawn now from the stored flow, one trade at a time;
  or the 20 seconds stays out and the arc is made on a stretch the market sets, which on a sparse tape is the
  square wave again. His call, put to him.
- The book's lean (the standing side) remains worth drawing beside it: it is what the July 8 to 11 crypto signal
  and the July 14 natural gas exhaustion read, and in today's sample the whole-book lean moved with the price.

## 2026-11-18: Greg on the first samples: the big movements happen in all three at the same time

"I am seeing spikes and dips at the same timestamps so thats promising. Since they are measurijg different data
types the graphs will look different but I wanted to see if the big movements happened in all 3 at the same time
and they do".
- By eye, one stretch (trade day Oct 17, 11:58:32 to 12:07:03 Eastern). Not measured yet.
- Partly built in: a trade at the best ask moves the price graph, the run of trades and the lean at the best
  prices on one and the same tick. The whole-book lean is not moved much by one trade and still followed the
  price: the lead to follow.
- To do, on his word: count it with no window, every case listed (each move of one line, the distance in ticks
  and time to the nearest move of the others), and draw all four trade days.

## 2026-11-18: NO EXCEPTIONS on the 20 seconds; the three renders are trade price, dipole and exhaustion at the tick

Greg: "No exceptions! That window gives us nothing but a visual to confirm frkm."; "I said dipole and exhaustion
ticked by nano"; "And i asked for the trade price curve too"; "We can add those to your selections once you have
nano versoons of them all".

- The 20-second window: a picture to confirm from, nothing else. Never a signal, never in a calculation. Do not
  propose it as an exception again.
- The three renders, each its own graph, one axis of real timestamps, no window:
  1. the trade price curve (the price of every trade, in order);
  2. the dipole at the tick: the latest run of buying against the latest run of selling (the run under way and
     the run it took over from), changing at every trade;
  3. the exhaustion at the tick: each run of trades on one side as it builds; its high is its last trade (the
     peak with no window, already stored in `turn_peaks`).
- Other lines (the resting orders' lean, the running total of lots, the quote) are additions for later, beside
  these, never in place of them.
- Samples of exactly these three were sent (trade day Oct 17, from 11:58:32.200 Eastern, 150 and 600 trades).
- Next: his word on the three as drawn; then the dipole at the tick laid out as a calculation for his yes, and
  the pictures for all four trade days on pods (one launch, the price put to him at the time).

## 2026-11-18: the dipoles born on a trade leg's first trade (Greg: "Let's start there")

- Trade day Oct 17: 267 recorded dipoles were born with a trade in their birth second; for 90 of them that second
  holds the FIRST trade of a trade leg. Not yet set beside "any second with a trade", and not yet counted on the
  other three trade days.
- The first two in time order were drawn as the stacked pair (trade leg's price above, the dipole at the tick
  below): born 20:28:01 (trade leg 79, up, 1 step, 110.9 s) and 20:46:56 Eastern (trade leg 85, up, 2 steps,
  261.7 s). Both are evening, thin tape, one trade in the birth second.
- The recorded dipole only says where to look (a mark). The line drawn is the dipole at the tick.
- To do on his word: all 90 of trade day Oct 17 and the same on the other three trade days (pods, one launch).

## 2026-11-18, close: the exhaustion calculation is to be EXACTLY the crypto one; only the market differs

Greg: "Whatever crypto did to generate those renders do that. If one of the calcs was a 20 sec. Use it just like
crypto did. Look at if the crypto data was altered to be different that what we have in any way. I want everything
in our new exhaustion calc to be exactly like the old calc."; "The only difference between the two should be that
was crypto and we're doing ng".

- The crypto calculation, as its script has it (Markets branch `claude/davisai-s71-counterparty-capacity-sf1168`
  `75b15fa`, `research/shape_s71/regroup2.py`, `arc_gate.py`, `shape_arc.py`): spelled out in handoff O.
- Do not swap in a "better" line. Do not drop the 20 seconds from this calculation. Do not relabel another line as
  exhaustion. Carry it over as it was; list every difference between the crypto data and ours; put each to him.
- The tick versions (the dipole and the exhaustion at the tick) are built BESIDE it, not in place of it.

## 2026-11-18: winner and loser are disregarded (Greg)

"We looked at winner and loser incorrectly. We corrected our thinking later so completely disregard those labels".
- No winner or loser label anywhere. The crypto exhaustion calculation is carried over exactly EXCEPT for that.
- Likely the correction he means (the crypto review of July 11): a winner and its losing twin had the same shape
  at entry; win or lose was the side taken, not the shape.

## 2026-11-18 (thirteenth session): the crypto exhaustion calculation read WHOLE, and the finished list of differences

Read whole this session, on Markets branch `claude/davisai-s71-counterparty-capacity-sf1168` (`75b15fa`):
`research/shape_s71/regroup2.py`, `arc_gate.py`, `two_shapes.py`, `shape_arc.py` (its first 140 lines; it is not
used by the picture), `_birth_probe.py`, `_liquidity_dive.py`, `odcore/platform.py`, `odcore/flip_detector.py`,
`odcore/swing_maker.py`, `kraken_book_collector.py`, the July 7 handoff and `SIGNAL_SHAPE_DIRECTION_S71.md`. Also
opened: that session's own saved arc values, `research/shape_s71/quad_means.npz` (told to Greg first).
Nothing of ours was read or run.

### What handoff O left open, now settled from the code

- THE ENTRY GATE WAS NOT USED. `run_kraken_cell` never switches it on (`dipole_entry` stays off), so the
  divergence read played no part in which trades the arcs follow.
- THE ONSET IS A FILL, NOT THE TURN. The turn finder marks a turn; the trade then starts at the first later grid step holding a trade on the OTHER side (a sell for a trade going long, a buy for one going short), and
  only if that comes before the next turn. So every onset holds a trade against the trade's own side.
- THAT IS WHAT BREAKS HIS PICTURE AT 0 AND AT 20 SECONDS. The against-side trade at the onset pushes the line down
  at 0; exactly 20.0 seconds later it leaves the 20-second roll and the line jumps back up. Checked on the saved
  crypto values: on all 20 lines (five coins, four kinds) the two largest steps of the whole line are at 0.0
  (down, 0.17 to 0.66) and at 20.0 (up, 0.15 to 0.63); every other step is about 0.003. The notes above said
  "which way is not known": it is the roll plus the fill rule. Any other onset on our tape puts a different
  built-in step there.
- WHAT FEEDS AN ARC. Only three things from the data: the size bought and the size sold in each grid step,
  and (for two coins only) the mid price. The resting sizes at the best prices are passed in but never used on
  this path (`fill_model="front"`). The fees (maker 0, taker 5) go into `net_bps` and nowhere else: with winner
  and loser gone, no fee touches any drawn value.
- WHAT SETS WHERE A TRADE STARTS AND ENDS (the executor's rules, all still inside the arcs):
  1. the turn finder: a zigzag on the lean of trades over the last 600 cells, which on this grid is 60 SECONDS,
     turning when the lean comes back from its furthest point by a set amount (0.10 for btc, eth, sol; 0.13 xrp;
     0.30 doge);
  2. for btc and eth only, an earlier entry when the mid price comes back from its furthest point by 5 or 10 bps;
  3. the fill rule above (in at the next trade on the other side, first in line);
  4. the end: the next turn's fill ends this trade and starts the next one; if that fill does not come, a wait of
     30 seconds (60 for doge) for a trade on the other side, then out;
  5. for btc and eth only, a stop when the price is 80 or 100 bps against the trade.
  Under the plain setup (sol's: none of 2 and 5) the mid price is not used at all: the trades and their arcs come
  from the bought and sold sizes alone.
- SHORT OR LONG needs an END as well as an onset: the length is end minus onset, both from the executor.
- PARTLY BUILT IN, kept so it is not read as a finding: a turn is only marked once recent trading has moved the
  trade's way, so the line rising into the onset is partly made by how the trades are chosen.

### The finished list: crypto against what we hold

Made the same in the natural gas calculation (Claude's calls, stated to Greg, his to correct):
1. THE GRID. Our trades are summed into grid steps on the received clock, each trade in the grid step it was
   received in; the grid starts at the open of the trade day (6 pm Eastern). Crypto's records were made the same
   way by the collector, on its own receive clock. The stored rows are untouched; this is inside the calculation.
2. THE 20-SECOND LINE is worked out fresh on that grid with crypto's own formula (the last 200 cells, the cell
   itself included). The stored `flow_20s` is NOT used for it: it exists only at ticks, and crypto's line is read
   every grid step, also where a trade drops out with no message. It is checked once against the stored
   `flow_20s` where the two must agree.
3. ZERO WHERE NOTHING TRADED. Crypto wrote 0 when no trade was inside the 20 seconds, and those zeros are inside
   every mean. Ours is stored empty there. In this calculation the crypto 0 is used, with a mark beside it saying
   "nothing traded", so both are kept.
4. A TRADE WITH NO SIDE goes into neither bought nor sold. Same as crypto in effect.
5. EACH TRADE DAY takes the place of a coin: its own trades, its own middle length, its own line. Nothing crosses
   from one trade day to another. The 5 pm to 6 pm stretch is not in it.
6. 45 seconds before the onset to 60 after; a trade whose 105 seconds do not fit inside the trade day is left
   out; a kind is drawn only with at least 8 trades. As crypto.

Cannot be made the same; said to him as facts:
- Crypto never had the single trades or orders. Its collector kept one record per grid step with the
  trades already summed, and the ten best levels of the book. We hold every message.
- Crypto's clock was our collector's computer; trades during a dropped connection were lost; when the feed went
  quiet the collector could stamp a trade early by the length of the quiet. Faults of the collector, not steps
  of the calculation: not copied.
- Crypto ran round the clock, five coins, about 40 hours each in one unbroken stretch. Ours: one contract, four
  trade days of 23 hours, each on its own, with the settlement window (2:28 to 2:30 pm Eastern) marked and nothing
  removed.
- Sizes are coins there and lots here.
- NO NATURAL GAS SETUP EXISTS. The turn amount, the early entry, the stop and the wait were set coin by coin on
  Kraken results. "Only the market differs" cannot choose one for natural gas.

Still needing his word, put once and together (the message of this session):
1. THE TRADES the arcs follow: the crypto turn finder and its in and out rules brought back for natural gas (with
   a setup named), or his own onset and end.
2. THE MEAN AND THE MEDIAN: each line an AVERAGE of many trades' arcs; short or long by the middle length.

### Desktop's start, found (corrects handoff O, which said it was not on the branch)

`desktop-old-family-chain-on-clock-20261117/flow-60s-before-and-after-<trade day>.parquet`: for every 20-second
peak of the four trade days, the 20-second flow turned to the peak's side, one reading a second from 60 seconds
before the peak's high to 60 after, on the rebuilt rows. It is the same kind of line as the crypto arc with a
different anchor (the peak's high, not a trade's onset) and a different step (one second, not a grid step). That
folder carries Greg's note "record only", so it is cited as what Desktop anchored on and is never an input.
Desktop's earlier pictures on the old data ("Flow lean and midpoint around the birth") are still not on the branch.

## 2026-11-18 (thirteenth session): Greg brings the crypto program back, named "crypto and ng"

"Bring back the program and just designate it crypto and ng so we know what it is at a later date. And it's crypto
iutpots if are any will now go into our excel sheet. They would be for observation or vaelrification purpose only".
- The trades the exhaustion arcs follow are made by the crypto trading program, run on the natural gas tape as it
  was (Markets `75b15fa`), under the name "crypto and ng".
- Its outputs go into the Excel sheet. Observation and verification only: never a signal, never an input.
- The mean and the median were not answered; Claude's call (the stored output is per trade; the averaging is in
  the picture only and is named on it) is stated to him and is his to correct.

## 2026-11-18 (thirteenth session): no average and no split; our trades individually (Greg)

"And i think we took the average of the trade trlypes to get a simplified version to run for each type to
validaylte the equations and outputs. We will want to door our trades individually and see how they seperate
organically. Like the reversal of that crypto process".
- The crypto mean line per kind was a simplified check of the equations. It is NOT made for natural gas.
- No short or long split, no middle length, no kind put on a trade by us. Every trade's own arc, on its own.
- How the trades separate is looked for in the single arcs. Any method that would group them is named to him
  first (his standing rule).
- Left out of the crypto calculation on his word, in all: winner and loser; the average; the short or long split.

Greg, same session: "We will want to see how the long and short dprints behave but not give them that label prior
to run". Each trade's length is a stored number; no short or long label before the run or in the store; how the
longer and shorter ones behave is looked at afterwards from the single trades.

Greg, same session: "Each trade should have its own exhaustion graph. No more than one graph per render". One
picture for each trade of the crypto and ng program, one graph in it. No pages of panels, no picture holding many
trades.

## 2026-11-18 (thirteenth session, close): NANO TICKS; the first crypto and ng run was wrong data and is deleted

Greg: "Definitely run it on nano ticks. [the old time step] is losing too much data"; "Delete [the old time step] outputs and renders. We don't keep
wring dayta"; "We've gone over numerois times".
- The first natural gas run of the crypto calculation put the trades on a time grid, as the
  Kraken collector did. Wrong on our tape: it collapses ticks. Its outputs are deleted; nothing of it is stored
  or to be used. The rerun is at the tick, every trade at its own nanosecond.
- It also made lines only for the trades of the PROGRAM (which makes its own, of the order of 1,300 a trade day
  in that run), not for each of the 30,000 and more trades on the tape, which is what he had in mind. Which
  trades get a line is his word, first thing in the next session.
- What he wants the exhaustion work to do, in his words of this session: every trade individually, "see how they
  seperate organically", "like the reversal of that crypto process"; "see how the long and short dprints behave
  but not give them that label prior to run"; "Each trade should have its own exhaustion graph. No more than one
  graph per render"; "We also want to be measuring exhaustion prior to trade start and after trade ends"; "Part of
  exhaustion research is to see if there are prebirth signals"; the render must not cut the line off at the
  start and the end; the line as a curve or as steps is still his to say (the July curves were averages; one
  trade's line moves in steps).
- KEPT SO IT IS NOT GOT WRONG AGAIN: "exactly like crypto" never outranks "rows are ticks, timed to the
  nanosecond". Where a crypto step would collapse ticks, it is said to him and done at the tick.

### Made at the tick this session and stored (`tick-renders/` on each daily branch)

- The dipole and the exhaustion at the tick, on every tick of all four trade days; his three renders for the whole
  trade day; the stacked pair for every recorded dipole born on a trade leg's first trade.
- A count, each trade day on its own, no test of chance: a recorded dipole born with a trade has the first trade
  of a trade leg in its birth second in 99 of 288, 118 of 335, 90 of 267, 97 of 315 cases. ANY second of the
  trade day with a trade holds the first trade of a trade leg in 4,088 of 10,330; 4,595 of 11,482; 3,803 of
  9,963; 3,532 of 9,405. About a third either way: by this count the dipoles born with a trade do not pick out
  the starts of trade legs. It answers the twelfth session's "90 of 267 ... not yet set beside any second with a
  trade".

## 2026-11-18 (fourteenth session): the exhaustion calculation is written at the tick; the rerun goes first

Greg: "We have to rerun the exhaustion data on the pods first. Pull renders whike it's running"; "A we have tonchange
is output time from [the old time step] to nano tick.time".
- The only change from the July calculation is the TIME: grid steps become the nanosecond. Every rule and
  number is the July one. The turn finder is the July function itself, walked over every moment its 60-second
  lean changes.
- THERE IS ONE 20-SECOND LINE FOR THE WHOLE TRADE DAY. It changes only when a trade is received or when a trade
  leaves the 20 seconds (a moment with no tick). Every single trade's exhaustion line, a trade of the program or
  a trade on the tape, is a cut of that one line around the trade, as far before and after as is wanted. So
  "prebirth" is not a separate calculation: what the line did before any trade is already on it.
- Both kinds of trade get a line in the one run (Claude's call, his to correct): the program's own trades, and
  every trade on the tape.
- KEPT SO IT IS NOT DONE AGAIN: a made-up list of numbers on grid steps was used in the session to check
  the new code against the July program. He objected at once ("Why are we using made up data and why are we using
  [the old time step] timing?"). It is deleted. No made-up numbers, not even for a code check, and nothing on a grid for any
  purpose. A new calculation is checked on real tape on the pods.
- Built in, to remember when the lines are read: every onset is a trade AGAINST the program's own side, so the
  line steps against the trade at 0 and steps back exactly 20 seconds later when that trade leaves. On thin tape
  a turn can be marked when old trades leave the 60 seconds with nothing new traded; those are counted in the
  receipt and nothing is filtered.
- Greg, same session: "Any [the old time step] code and data need to be delivered. Any [the old time step] mentions as time needs to be deleted"
  (read as "deleted"). The July program's files are removed from the code branch; the rules stand on their own,
  written in seconds at the nanosecond. In these notes the old wording is changed to "time grid" and "grid
  step"; his own quoted words are kept as he said them. Do not bring a time grid, or the word for one, back.

## 2026-11-18 (fourteenth session): the dipole and the exhaustion are SINGLE EVENT outputs (Greg)

Greg, after the rerun, on the stored full trade day renders and the four trade days of stacked pairs: "I don't
think I see anything useful for the Full day and the 4 day dipole outputs"; "the goal is to give better
understanding of trade data ... I mean price/trade.curve"; "I feel like dipole and exhaustion are single trade
event outputs and dona great job explaining those events"; "Or maybe a few teades in a row but not entire days";
"how canwe see with the data we have if there are any dipoles or wxhaustions that continue on to cover more than
one trade? We ahoukd probably expand our searches for those".

- THE UNIT IS THE EVENT (one trade, one trade leg, or a few trades in a row), NOT THE TRADE DAY. Inside one event
  the dipole shows whose hands it was in and when that changed, and the exhaustion shows the run building and
  letting go. Laid end to end over a trade day the event is lost.
- THE MEASURE of any output: does it help us understand the price / trade curve.
- Nothing of the full trade day or four trade day outputs, old or new, goes into the Excel sheets or gets a type
  or a label until it is decided with him.
- Why the full-day dipole pictures say little (Claude's read, his to weigh): the dipole at the tick and the
  exhaustion at the tick are made from the same two runs of trades, so they are one story drawn twice; and both
  are made from the very prints that draw the price curve, so they move when it moves. They describe an event;
  they do not say why the curve moved or what it does next.
- THE NEXT SEARCH, his: dipoles and exhaustions that CONTINUE over more than one trade. The stored data can show
  them without any window of ours, because each sets its own start and end:
  1. a run of trades on one side (the exhaustion at the tick): from one change of the hitting side to the next.
     Stored for every run: its trades, its lots, its first trade (`turn_peaks`); and the trade leg under way is
     stored on every tick (`leg_peaks`). Side by side they say how many trades and how many trade legs each run
     lasted through.
  2. the dipole at the tick: each stretch it stays on the buying side or the selling side, through several
     changes of hands (`tick-renders/tick-dipole-*`).
  3. the 20-second line: each stretch it stays on one side of zero (`crypto-ng-tick/crypto-ng-tick-line-20s-*`).
  For each stretch found: how many trades and trade legs it covers and what the trade price did from its start
  to its end, each on its own line, none combined, no label.
- By eye only, one stretch, not measured: on trade day Oct 17 the 20-second line stayed on the buying side from
  before 11:58:32 to about 11:59:00 Eastern, while four trades of the program came and went and the price went
  from 3.038 to 3.045. One exhaustion over several trades.
- A first look at that one stretch was written to be read in the session; the session's own check refused to
  run it (a calculation on market data), so it was not run and nothing was worked around. It goes on a pod on
  his go.
- OWNED: the 920 exhaustion sheets removed this session were the eleventh session's, made on the REBUILT rows
  (the 20-second peaks), not on the earlier bad data. His words were "made on old or bad data". Said to him,
  with the offer to put them back from git.

## 2026-11-18 (fourteenth session): the data says where an exhaustion begins and ends; the humps

Greg: "We need the data to be telling us what thise times are". No picture or output takes its start or end from a
number of seconds, a typed clock time or a count of trades.
- On the 20-second line an exhaustion is a HUMP: the line comes onto one side of zero, goes as far as it goes,
  and comes back to zero (or empties, or crosses). Its two ends are the line's own moments. Stored for every hump
  of all four trade days, each on its own line, with the trades and the trade legs it covers and what the trade
  price did across it.
- First counts (each trade day on its own; a lead, not a result): about half of the humps hold more than one
  trade, and about three in ten had more than one trade leg under way (trade day Oct 17: 2,128 and 1,280 of
  4,103). Roughly three in ten hold no trade at all: the line changed side only because old trades left the 20
  seconds. Those are made by the 20 seconds, not by the market.
- To weigh when the humps are read: a brief dip through zero splits what the eye sees as one build into two
  humps. In the stretch he knows the buying before 11:58:20 and the buying after it are two humps with a dip of
  a fraction of a second between them.
- Kept so it is not done again: a pod that says "container is starting" for more than a few minutes is not coming
  up. Delete it and run its trade day on a healthy pod. And a pod left up while the session restarts keeps
  billing: read the account first thing after any restart.


## 2026-11-23 (fifteenth session): one picture per TRADE LEG, set against the dipole and the exhaustion, prebirth shown

Greg, on being put the unit of a picture: "And I want every trade leg compared against the exhaustion and the
dipole. And show the prebirtths for the dipole and exhaustion before the trade starts".
- The unit of the individual trade renders is the TRADE LEG (the trade price curve cut into its own moves).
- Each picture: the four graphs on one clock, the trade leg marked on all four (its life shaded; the print where it
  became known; the print that showed it had ended).
- The prebirth is what the dipole and the exhaustion did before the trade leg's first trade. To be sure it is in
  every picture, a picture starts at the first trade of the trade leg BEFORE (and ends at the last trade of the
  trade leg after), moved outward so no run of trades, dipole stretch or hump of the 20-second line is cut.
  Starting only from the hump the trade leg touches could leave no lead-in at all.
- To remember when the pictures are read (said before, still true): the dipole and the exhaustion at the tick are
  made from the very prints that draw the trade price curve, so inside a trade leg they move when it moves. What
  is not built in is what they did BEFORE the trade leg's first trade. That is what these pictures are for.
- Also built in: a trade leg starts on the stretch where the one before it turned, so the lead-in of every picture
  is the trade leg before, and neighbouring pictures overlap. Each picture shades only its own trade leg.
- Nothing is typed, labelled, measured or put in the Excel sheets from these pictures until decided with him.
- Code: Markets `ccr-b66f34d5-h6ra1t`, `root/leg_renders.py`. Built, not run.

Greg, same session: "For the time being, just pick 10 random ones per day with those 3 to start"; "Those 3 renders i
mean"; "Per trade".
- The first pictures are 10 trade legs picked at random on each of the four trade days (40), not every trade leg yet.
- Each picture is HIS THREE RENDERS (trade price curve, dipole at the tick, exhaustion at the tick), one picture per
  trade leg. The 20-second line is not in them. The line above that says "the four graphs" is superseded by this.
- A picture's edges: the trade leg before to the trade leg after, moved outward so no run of trades or dipole
  stretch is cut.

The first 40 pictures were drawn and stored the same session (`leg-renders/` on each `root-rows` branch; 10 trade
legs picked at random per trade day; counts of trade legs 6,119; 6,907; 5,660; 5,120).
- By eye only, a handful of pictures, nothing measured: inside a trade leg the dipole and the exhaustion step at
  the same prints the price steps at, as expected (they are made from those prints). The part to read is the
  lead-in before the shaded stretch.
- The lead-in is as long as the trade leg before. After a one-step trade leg it can be a few seconds and a single
  trade, which shows little prebirth. Open with Greg: whether a picture should reach further back, and by what the
  data says (two trade legs before; the run of the quote under way; something else of his).

## 2026-11-23 (fifteenth session): DIPOLE AND EXHAUSTION ARE THE CRYPTO FORMULAS. Read this before drawing either.

Greg: "We should not be reinventing the wheel! The instructions should have been explicit to folow the crypot
formulas. That's why we brought that part back and did all of that work last session."

- THE 40 PICTURES ABOVE ARE DELETED. They drew Claude's tick versions (the run of trades under way against the run
  before it) under the names dipole and exhaustion. Everything in the section above that speaks of "the dipole at
  the tick" and "the exhaustion at the tick" as his three renders is superseded by this section.
- The crypto formulas, from the crypto code (Markets `75b15fa`): one figure, bought minus sold over bought plus
  sold, over the trades of a span of time.
  - EXHAUSTION LINE: over 20 seconds (`research/shape_s71/regroup2.py`, the July 7 graphs).
  - DIPOLE LINE: over 60 seconds (`_dipole_price_overlay.py`, the "Dipole (flow) over Price" picture, with the
    rate of change of the lean, the "dipole dive", under it).
  - BEFORE AN ENTRY (`odcore/info_dipole.py`): the lean over the bars before entry; divergence is its sign against
    the price's drift; exhaustion is the late half weaker than the early half. Not built for natural gas.
- BOTH LINES ARE ALREADY STORED AT THE NANOSECOND for all four trade days, made in the fourteenth session with the
  July rules: `crypto-ng-tick-line-20s-<trade day>.parquet` and `crypto-ng-tick-lean-60s-<trade day>.parquet`.
  Nothing new has to be worked out to draw a trade leg against them.
- "TICKED BY NANO" IS THE TIME OF THE READ, NOT A NEW FORMULA. The tick versions of the twelfth session came from
  misreading that. They are Claude's own, never approved as a calculation; they are not dipole and not exhaustion.
- In crypto the two were never independent: one flow lean, two spans, two reads (its level; its fall toward even).
- Still true of the crypto lines too, to remember when they are read against the price: they are made from the
  prints, so a print moves them on the same nanosecond. Unlike the tick versions they also move with NO print
  (when an old trade leaves the 20 or the 60 seconds), and they carry what happened before a trade leg starts.

Greg, same session: "Delete anything that you ran your way. I want the other 2 graphs exactly like thry were in
crypto. And no hardcoded start and stop time for graphs. Dipole and exhaustion start and stop by when the data says
and not our predetermined values".
- Deleted: `tick-renders/`, `continuing/`, `four-graphs/` on the daily branches, the twelfth session's sample folder,
  and the three programs that made them. Every count in this file that stands on "the dipole at the tick", "the
  exhaustion at the tick", "runs of trades on one side" as an exhaustion, or "stretches of the dipole" is a record
  of what was done and is NOT to be used.
- The trade leg picture now: trade price curve; the crypto dipole (the 60-second lean); the crypto exhaustion (the
  20-second line); both read from the stored crypto and ng lines and turned to the trade leg's side.
- A picture's start and stop: the trade legs frame it, and every hump of either line it touches is whole. No
  number of seconds anywhere.

Greg, same session, two things to keep:
- EXCEL: "We only want the crypto calc styles as the source of output for exhaustion and dipole to put on excel
  sheets". Checked: neither Excel file holds any of Claude's versions.
- SAVED FOR AFTER THE CURRENT WORK, his idea: the best bid and the best ask as two separate graphs, each flowing up
  and down by tick through the trade day, no trades in them. Not to be raised until the trade leg pictures are done.

The 40 pictures on the crypto lines are drawn and stored (`leg-renders/` on each `root-rows` branch; the same 40
trade legs). By eye only, a handful, nothing measured:
- The lines do start before the first trade leg in the picture.
- Thin tape: both lines are a square wave between +1 and -1 with empty gaps (one or two trades fill the span).
- Busy tape: a picture can hold hundreds of trades with the trade leg a thin band, because a hump of the 60-second
  line is long.
- A lead, one case (trade day Oct 18, trade leg 2990, a fall of 6 steps): the 60-second dipole was on the buying
  side through the whole fall and crossed to the selling side only after it ended. To look for in the others
  before anything is said about it.
- Unlike the deleted versions, these lines move with no print (a trade leaving the 20 or the 60 seconds) and can
  sit against the trade leg for its whole life. So agreement or disagreement with the price is not built in the
  same way; a print still moves both lines on its own nanosecond.

The 40 were redrawn the same session (price as it printed; each line on its own scale). By eye in five, nothing
measured, to carry into the next look:
- A sharp price move and a jump in both lines fall on the same prints (built in).
- After it, both lines drift back toward zero as old trades leave the span while the price holds or returns: the
  lean falling back toward even, which is what crypto called exhaustion. This is the part that is not built in.
- In these five the lines turn after the price, never before: they carry the last 20 and 60 seconds.
- THE STORED TRADE LEG IS A POOR MARK FOR "THE TRADE": it ends at any single print one tick back, so the shaded band
  is often a piece of the move the eye sees (trade day Oct 2, trade leg 3016; trade day Oct 3, trade leg 2554 is
  0.4 seconds long inside a two-minute rise). Put to Greg: shade the crypto and ng program's own trade instead
  (what the crypto graphs were drawn around). Not answered yet.

## 2026-11-23 (fifteenth session): the pictures set up as the crypto pictures were (`trade-renders/`)

Greg: "I just want to make sure we are setting them up the same. Show each individual trade and their prebirths like
this without designated start times for dipole and exhaustion"; "instead of per sec, we are doing per tick like price".
- One picture per trade of the crypto and ng program; zero at the trade's start; the mid price from where it stood
  there; the 60-second dipole; the 20-second exhaustion; the dipole's rate and the price's rate per tick. All
  turned to the trade's side. No designated start: two trades back, and every hump whole.
- What the crypto code showed (Markets `75b15fa`), kept so it is not looked up again: the dipole picture's price is
  the MID price; its zero is the lowest (or highest) mid in the half hour before, so the price V there is made by
  the choice of zero and the dipole V is not; every line is an average of many trades.
- By eye in three of the first 40: one trade (trade day Oct 18, trade 982) shows the dive before zero and the
  recovery after it in all three lines; two others show the dipole against the trade through its life.
- Per tick, the price rate is always half a tick up or down: it carries timing and direction only.
- To look for across the 40 before anything is said: whether the dive before zero comes with the trades that then
  go the trade's way, each trade on its own, none combined.

The best bid and the best offer were tested on two trades the same session (`trade-renders-quotes-test/`): each its
own graph by tick, a rounded curve that is straight where the price is not changing. By eye: close to steps (the
book ticks too often for the rounding to show); the two do part company at times (one steps, the other stays, the
gap is two ticks for a few seconds). Greg's read is awaited.

## 2026-11-23 (sixteenth session): the price graph is two points and a line, no mid price; where the mid price is

Greg: "For the trade price graph, I literally want only two points and a line connecting them. No midprice. Just two
dots (or whatever symbol we're using) and a line. Put the 2 separate dotted lines showing when the buy-sell combo
happens. Keep the other graps the same. And shorten the y axis scale for that graph."
- THE PRICE GRAPH OF A TRADE'S PICTURE: where the trade was bought and where it was sold, each at the price of the
  trade on the tape that filled it, joined by a straight line. A dotted line at the moment of each. The scale is
  the two prices and nothing else. No mid price. This supersedes "the price line is the mid price" in the section
  above.
- A trade that ended at no tick has no price at its end: the dotted line is drawn, no point, and no `end_price` is
  stored. A price where nothing traded is not drawn or stored.
- The last graph (how fast the price changes) is still the mid price's change per tick: kept on his "Keep the other
  graphs the same" until he says.
- Code: Markets `ccr-26ff219b-72monm`, `6562821`. Built, not run.

The mid price, kept so it is not looked up again (the full list is in the decisions file, sixteenth session):
- It is an average of two prices, and the rebuild's own plan had already said the best bid and the best ask are
  followed separately and never combined into a midpoint (`STEP2_PLAN.md`). Bringing it in with the crypto picture
  went against that. Before a line is copied from a crypto picture, check it against the rebuild's own rules.
- It is in two programs only: the picture program and the crypto and ng run. It is not a stored column, is in no
  calculation of `root/calcs/` and in no Excel sheet.
- IT DOES NOT CHOOSE THE PROGRAM'S TRADES. The trades, their starts and ends come from the turns of the 60-second
  line, the sides of the trades and the 30-second wait. The mid only prices them (the program's own open and close
  price and its three results in hundredths of a percent, and one half spread figure for the trade day). So the
  dipole, the exhaustion, the humps and every picture's frame do not stand on it.

The two test pictures were reprinted this way the same session (`trade-renders-quotes-test/`, trade day Oct 2 trade
883 and trade day Oct 18 trade 982; Markets `6562821`).
- Trade 883 (a sell): sold 2.865, bought 2.865: one price, a level line. Trade 982 (a buy): bought 3.111, sold 3.112.
- To remember when a price graph of two points is read: the two points are the program's own start and end, each
  the first trade on the OTHER side after a turn. They say where and when, not what the price did in between; the
  best bid and the best offer graphs carry that.
- Trades of the program that ended at no tick and so have no end price: 99 of 1,794 (trade day Oct 2), 134 of 1,682
  (trade day Oct 18). Their pictures will carry one point and the dotted line where the wait ran out.

Greg, same session: "We should not have originally picked a zero price movement to look at our best bid offer
graphs." Trade 883 was sold and bought at one price. Before a trade is picked to look at the best bid and the best
offer on, read its two prices in the stored index table. Trade day Oct 2, trade 1672 (a sell: sold 2.839, bought
2.836, 31.248 seconds) was drawn beside it the same way (`trade-renders-quotes-test/`, `root-rows-20231002`).
- By eye, one trade: at its start the best bid and the best offer both stood a tick higher for a moment and stepped
  down together; after that the offer moved back and forth a tick several times while the bid stood. The bid and
  the offer do not always step together: the thing the mid price hid.

## 2026-11-23 (sixteenth session): Desktop's earlier pictures, read for their concepts (Greg: "look the concepts over to see if they have value")

His pictures: the flow lean and the midpoint around Native's birth; the share of candidates above or below their
level against matched controls; recognition minus the first event (aggressor lots, touch size, quote move). His word
on them: "We didn't have the full depth of the data and we ran the days wrong so these values aren't right".
- Built in, so not a finding: the lean reaching fully one-sided at the birth and dropping 20 seconds later (that is
  what a birth and a 20-second span are); the flat shelf at 50 seconds (Native's fixed wait); the price rising
  into the birth (20 seconds of one-sided trading).
- Not built in, worth making again properly: after a birth the price stood on the birth's side more often than at
  control moments on all four trade days. In our terms: does a one-sided burst carry the price its way afterwards,
  one event at a time, best bid and best offer each on its own, ends set by the data.
- The concept under the first-event curves: around one event, which came first and how long each took: a trade on
  that side, a change of size at the best price, a step of the best bid or offer. Stepped before it was hit =
  pulled; stepped after = eaten. The same lead as stage (3) above, read at the start of an event.
- The event to use is the HUMP of the stored 20-second line (17,304 on the four trade days), not Native's birth.
- Laid out to him as one table and one workbook; not built until his word (the full list is in the decisions file).

## 2026-11-23 (sixteenth session): the natural gas dipole and exhaustion are used for strategy; crypto data is not

Greg: "The crypto data is not to be in our analysis or on excel sheets. The ng version of these absolutely should be
used for strategy".
- The two lines made on the natural gas tape (60 seconds, 20 seconds) and the humps are strategy inputs and go into
  the Excel sheets. Where this file says "observation and verification only" of the crypto and ng outputs (the
  thirteenth session), that now holds for the program's own trades, prices and fee marks, not for the two lines.
- Crypto data (anything measured on a crypto market) is in no analysis and no sheet. The formulas only.
- The program's trades stay observation only (Claude's reading, his to correct): their starts and ends come from
  settings tuned on crypto results.

## 2026-11-23 (seventeenth session): the research threads read again on the rebuilt data (`research-threads/`)

One line per move (a trade leg, a run of the best bid, a run of the best ask) and one line per hump of the 20-second
exhaustion line, stored values laid side by side; all four trade days, each on its own. The counts are in the
decisions file (seventeenth session) and in each receipt. Leads, no test of chance:
- MOST MOVES ARE OVER AT THE MOMENT THEY CAN FIRST BE KNOWN. Of the runs of the quote about four in five make one
  step only (trade day Oct 2: 21,420 of 27,010); of the trade legs about six in ten (3,878 of 6,118).
- A ONE-STEP TRADE LEG IS MOSTLY THE PRINT BOUNCING. On trade day Oct 2 the best bid and the best offer both stood
  where they were at 2,323 of 3,878 one-step trade legs, at 114 of 1,399 two-step ones and at 4 of 841 with three
  or more. All four read alike (a little over half on trade days Oct 17 and Oct 18). So the stored trade leg is a
  real move of the price from its second step on. This answers "the stored trade leg is a poor mark" above: it is
  the one-step legs that are poor.
- WHERE THE EXHAUSTION OR THE DIPOLE LINE STANDS AT A MOVE'S FIRST STEP SAYS LITTLE ABOUT WHETHER IT GOES ON. About
  one run of the quote in five takes a second step, with the line on the move's side or against it (Oct 2: 2,793
  of 13,163 against 2,473 of 12,712). Added up over the four kinds of run there is a small lean toward "on the
  move's side" on every trade day, least on trade day Oct 3, where the runs of the best ask up read the other way
  (681 of 3,687 on its side against 682 of 3,470). The side alone is not the read; how far the line stands, and
  what it did before, are not counted yet.
- A HUMP THAT BEGINS ONLY BECAUSE OLD TRADES LEFT THE 20 SECONDS CARRIES NO DIRECTION: the next trade is on its side
  about as often as on the other (Oct 2: 845 against 786). A hump that begins on a trade is followed first by the
  quote it was hitting stepping (1,055) or by more trading on its side (880), seldom by the other side (176).
  Partly built in: a buy that takes out the best offer steps it in the same exchange event. The table has a column
  for that (`next_..._same_event`); not counted yet.
- THE STORED EXHAUSTION LINE AND THE STEP LINE'S OWN 20-SECOND FLOW DIFFER at 104; 144; 136; 130 first steps (equal
  at 32,656; 35,999; 33,678; 31,409). Not explained. Do not use the exhaustion value on those lines until it is.
- "Do large moves come back" is NOT answered: the stored `given_back` is only the first step back (one tick). It
  needs the moves that follow.
- Kept so it is not done again: the fetch program had never met this receipt's layout. A new job's receipt is to be
  read against `root/pod_fetch.py` before the launch, not after.

## 2026-11-23 (seventeenth session): a stored line is read BY PLACE ON THE TAPE, never by time; and the information measure

- THE FAULT, kept so it is not made again: `root/research_threads.py` read the stored exhaustion and dipole lines,
  and the quote, "as it stood at that nanosecond": the last read at or before the tick's received time. Several
  trades often share one nanosecond (one order filling several resting orders), so that read holds trades that
  came AFTER the tick on the tape. Traced on a pod (`research-trace/`): every one of the 104; 144; 136; 130 first
  steps where the stored exhaustion line was not the step line's own flow is equal once read by place. A look-up
  of anything stored at the tick is made by the tick's position on the tape. Time alone does not order the tape.
- The first counts of the research threads (the section above) stand on tables with that fault on a few lines in
  every thousand. They are leads as before; the tables are being made again.
- THE INFORMATION MEASURE (`info-measure/`): Codex's measure is the crypto information dipole operator
  (`odcore/info_dipole.py`) called on twenty one-second pieces. Made here with the pieces counted back from each
  read's own nanosecond. Its first figure is the exhaustion line, and equals the stored line at every read on all
  four trade days. Its other figures (the entropy lean, the information ratio, the information flow, the lean's
  change) are NOT the dipole and NOT the exhaustion of the crypto pictures, which used the first figure only.
- What the counts say so far: where all the trading of the 20 seconds is on one side (4,594; 4,869; 4,360; 5,268
  reads) the two lists share exactly nothing and the ratio is made by the division. With trading on both sides
  the shared information was above zero at every read but one. A sizeable part of the reads stand on one or two
  pieces of twenty (trade day Oct 2: 3,750 on one, 5,068 on two, of 70,393).
- NOT PROVED, his deep dive: that the operator matches the original dipole equations (`Basic_equations`, not
  attached to the session). Until then it is in no sheet and no strategy.
- 2026-11-23, later the same session: on Greg's word the information measure IS in the "moves" and "humps" sheets
  (columns named `info_...`, with `info_ratio_made_by_division` marking the reads where the ratio says nothing).
  Set aside by him for further research: the operator against the original equations; how large the ratio is on
  two-sided reads; and everything deeper than a move's first step (the steps in between, whether moves come back,
  what the lines did before the first step).
- 2026-11-23, kept so it is not done again: THE PLAN FOR THE EXCEL WORKBOOK WAS DECIDED ON 2026-11-16 AND 17 and
  is in the decisions file: one row per tick, one sheet per trade day; the stored rows on the daily branches are
  the "daily sheets" and are kept up to date by adding each calculation's column files beside the rows; the Excel
  workbook is written once, at a slow time, in parts with the days broken up by rows (`root/sheet.py`,
  `WORKBOOK_README_PAGE.md`). Read that before touching any Excel file. Add columns to what exists; do not design
  a new sheet or a new layout.

## 2026-11-23 (eighteenth session): the strategy step; fifteen versions laid along the stages of a move

Greg: "Use all 4 days to make strategies". Every version is formed on all four trade days, so a try on them is a
record and not a blind test. The versions are in `research-union-current/strategy-20261123-claude/` (`VERSIONS.md`,
`EVIDENCE.md`). None has been tried; no stored table was opened to write them. What the work added to these notes:

- THE STAGES NOW EACH HAVE A VERSION. (0) before: a level that has only been eaten (CL04); fresh trading on the
  dipole's side (CL07). (1) the first step: made by a fill or by a cancel (CL03); the exhaustion line on its side
  (CL05). (2) the middle: both quotes have stepped (CL06); the price running against the dipole, read both ways
  (CL10, CL11); paying up through more than one level (CL13). (3) another step: the eaten level (CL01); the
  abandoned level (CL02). (4) the turn: fresh trading against the dipole (CL08); the reloaded level (CL12); the
  other side arriving at the top step of a run (CL14). (5) after: the step back and the return (CL15). At any stage: a
  change of side made by the span is no signal (CL09).
- A BUILT-IN NOT SAID BEFORE, to face before finding 4 of the paper is leaned on: one order that trades through
  several price levels makes several steps of the quote in ONE exchange event. A third step in the same event as
  the second is not something that "followed" an eaten level; nobody could act between them. It has not been
  counted. Every version therefore takes its stance at the tick with the exchange's own end-of-event mark and
  counts as following only what comes in a later exchange event.
- WHAT IS LEFT AFTER A DECISION, in plain arithmetic on the followed quote alone: the first step back of a run is
  one tick nearly every time (stored). So a stance taken at a run's second step and let go at its first step back
  stands one tick BEHIND when the run ended at two steps, LEVEL when it took a third, and one tick ahead for each
  step after that. Knowing a move has ended only at its first step back costs a tick; that is why a sign of the
  end that comes earlier (CL12, CL14) and what the OTHER quote is doing (CL06) matter.
- A stored line is compared with a trade by reading it JUST BEFORE that trade (the read before, by place), so the
  trade is not inside the value it is set against (CL07, CL08). Put to Greg.
- From the stored counts, kept so they are not read past: by the FIFTH step the lead of the eaten level is not
  there in every row (trade day Oct 3, best offer up: 3 of 150 eaten runs reached a fifth step, against 42 of
  1,099 and 3 of 101); and the dipole at a first step reads the other way in four of sixteen cells.
- NOT ANSWERED, as before: anything before a first step; whether moves come back.
