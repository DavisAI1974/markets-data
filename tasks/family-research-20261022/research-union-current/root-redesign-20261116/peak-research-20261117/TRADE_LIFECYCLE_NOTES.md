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

- The line: bought minus sold over bought plus sold, over a ROLLING 20 SECONDS of trades, on a tenth-of-a-second
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

