# Peak research: every peak by where it lands in the price move under way (2026-11-17)

Greg, 2026-11-17: "Seperate the peak data just for reseach purposes into the ones that land exactly where turns
happen, and when this evwnt begins or this group always lands on the ending of something. Don't change the peak
structure or where it's stored, just something to research on."

This folder is a research view only. The peak files on the `root-rows` branches are not changed. Nothing here is a
calculation of ROOT, nothing is averaged, ranked or fitted; the piles are read off two stored facts.

## What is here

`peaks-by-place-in-the-move-<trade day>.parquet`: one line per peak (both kinds: 20-second flow, and no window),
made in the session from the stored facts of `turn_peaks` and `move_steps` (told to Greg first). For each of three
moves in price under way at the peak's high (the trade leg, the run of the best bid, the run of the best ask):
- `place`: where the high sits in that move.
  - at the beginning: the move had made its first step and went on to make more;
  - at the end: the move made no step after the high (and had made more than one);
  - the whole move (one step): the move made one step in all, so the high is at its beginning and its end;
  - in between;
  - empty: the move had not ended in the trade day.
- the move's direction, its steps at the high and in all;
- whether the high is on the exact tick of that step;
- whether the peak's side goes with the move (a buy peak with a move up, a sell peak with a move down).

`COUNTS.json`: the number of peaks in each pile, per trade day, per kind of peak, per move, with three counts
inside each pile: on the exact tick; side goes with the move; and (20-second peaks) flow fully one-sided, or
(peaks with no window) a run of one trade.

## What the counts show (each trade day on its own; all four read the same way)

Trade day Oct 2, 20-second peaks against the run of the best bid (the best ask reads the same):

| Where the high sits | Peaks | Peak's side goes with the move |
|---|---:|---:|
| in between | 1,090 | 859 |
| at the beginning | 2,772 | 1,697 |
| at the end | 1,206 | 543 |
| the whole move (one step) | 4,457 | 1,331 |

Peaks with no window against the run of the best bid, trade day Oct 2: in between 1,437 (888 with the move); at the
beginning 2,847 (1,770 with); at the end 1,846 (450 with); the whole move 5,437 (1,115 with).

- The piles are not alike. A peak in the middle or at the beginning of a move of the quote is mostly on the
  move's side. A peak at the end of a move of the quote is more often on the OTHER side, most clearly for the
  peaks with no window (about three in four on every trade day).
- The largest pile is the one-step move, where beginning and end are the same tick of the move.
- Against the trade leg the peak's side goes with the move in every pile; that is close to built in (a buy prints
  at the ask).
- The high is almost never on the exact tick of a step of the quote: the high is on a trade's tick and the quote
  moves on the resting order's own row, a few ticks later. Against the trade leg it is on the exact tick for
  roughly three peaks in ten.
- Fully one-sided flow and one-trade runs are spread through the piles about evenly.

## What this does not show

- That anything can be traded. A peak is known only after its high, and a move's place is known only when the move
  has ended. Nothing here says what the price did afterwards.
- A peak on the other side at the end of a move is partly built in too: selling into the bid is what stops the
  bid's rise.
- No test of chance was made. These are counts.

## Sizes and shapes inside each pile (Greg: "Do any similarities in the peak sizes or shapes or durations start to stand out?")

Read from the stored files in the session (told to Greg first). Place is taken against the run of the best bid.
Only the tape's own whole numbers and words are compared; clock durations were not compared pile against pile,
because that needs time buckets or a middle value.

Peaks with no window: how many of the pile are runs of 6 lots or more, and how many are runs of a single trade.

| Trade day | In between | At the beginning | At the end | Whole one-step move |
|---|---|---|---|---|
| Oct 2, 6 lots or more | 694 of 1,437 | 1,327 of 2,847 | 654 of 1,846 | 1,652 of 5,437 |
| Oct 3, 6 lots or more | 696 of 1,364 | 1,515 of 3,256 | 645 of 1,850 | 1,874 of 6,214 |
| Oct 17, 6 lots or more | 665 of 1,355 | 1,252 of 2,875 | 585 of 1,763 | 1,245 of 4,408 |
| Oct 18, 6 lots or more | 657 of 1,290 | 1,049 of 2,496 | 468 of 1,579 | 1,139 of 4,180 |
| Oct 2, a single trade | 460 of 1,437 | 871 of 2,847 | 717 of 1,846 | 2,103 of 5,437 |
| Oct 3, a single trade | 431 of 1,364 | 1,076 of 3,256 | 749 of 1,850 | 2,436 of 6,214 |
| Oct 17, a single trade | 430 of 1,355 | 951 of 2,875 | 746 of 1,763 | 1,798 of 4,408 |
| Oct 18, a single trade | 396 of 1,290 | 830 of 2,496 | 732 of 1,579 | 1,740 of 4,180 |

- SIZE stands out, the same way on all four trade days: the peaks in the middle or at the beginning of a move of
  the quote are the larger runs (about half are 6 lots or more); the peaks at the end of a move and in one-step
  moves are smaller (about a third or less are 6 lots or more) and more often a single trade. Partly built in: a
  long run of trades on one side lasts through more steps.
- SHAPE, as far as the 20-second peaks' stories go, does NOT stand out: how the story ended (came back, or beaten)
  reads about the same in every pile (trade day Oct 2, came back: 664 of 1,090 in between; 1,758 of 2,772 at the
  beginning; 795 of 1,206 at the end; 2,728 of 4,457 whole one-step moves). The peaks in between make a few more
  new lows (4 or more: 403 of 1,090 against 366 of 1,206 at the end).
- Durations: not compared (see above).

## Attributes and height by pile, each peak placed against the quote it pushes into (Greg: "Are there distinctive attributes that are mostly associated with the end or beginning or the middle or the other? ... What about peak height")

Read from the stored files in the session (told to Greg first). Here a buy peak is placed in the run of the best
ASK and a sell peak in the run of the best BID: the price it is trying to move. Counts are in
`ATTRIBUTES_BY_PILE.json` and `HEIGHT_BY_PILE.json`, one entry per trade day, kind of peak and pile. Height is in
lots: for a peak with no window the size traded in the run; for a 20-second peak bought minus sold at the high.

Trade day Oct 2, peaks with no window (the other three trade days read the same way):

| | In between | At the beginning | At the end | Whole one-step move |
|---|---:|---:|---:|---:|
| Peaks | 1,339 | 2,599 | 1,837 | 5,792 |
| Pushing with the move | 854 | 1,681 | 506 | 1,252 |
| Height of 6 lots or more | 630 | 1,225 | 627 | 1,845 |
| Height of 1 lot | 321 | 497 | 521 | 1,408 |
| Pushed side thinner at the best price | 846 | 1,707 | 1,345 | 4,614 |
| Pushed side thinner in the whole book | 673 | 1,338 | 907 | 2,881 |
| Gap of one tick | 1,151 | 2,285 | 1,525 | 5,053 |

- Differ by pile: which way the peak pushes against the move; its height; and how often the side it pushes into is
  the thinner one at the best price (most often at the end and in one-step moves).
- Do not differ by pile: the gap between bid and ask; which side of the whole book is thinner; for the 20-second
  peaks, whether the peak before was on the same side, whether a Native dipole was known, and whether that dipole
  was on the peak's side.
- The 20-second peak's height differs only a little by pile (6 lots or more, trade day Oct 2: 770 of 1,038 in
  between; 1,826 of 2,647 at the beginning; 817 of 1,251 at the end; 3,209 of 4,589 one-step moves).
- A reading to test, not a finding: the peaks at the end of a move and in one-step moves look like a small trade
  taking out a thin quote that had just stepped in (the other side, small, the pushed level thin), and the peaks in
  between and at the beginning look like a larger run moving the quote. The book figures are read once the high's
  tick is done, so a trade that has just eaten into a level makes it thinner: partly built in. Not yet asked: how
  old the level was that the peak hit, and what the price did after each pile.

## The two kinds of peak against each other (Greg: "And look at the peak 20 sec win and with now window")

Read from the stored files in the session (told to Greg first); counts in `TWO_KINDS_OF_PEAK.json`.

| Trade day | 20-second peaks | No-window peaks | Highs they share | 20-second high on a trade inside a run that went on | 20-second high on a tick with no trade |
|---|---:|---:|---:|---:|---:|
| Oct 2 | 9,525 | 11,567 | 5,403 | 1,377 | 2,660 |
| Oct 3 | 10,577 | 12,684 | 5,941 | 1,619 | 2,907 |
| Oct 17 | 8,619 | 10,401 | 4,833 | 1,251 | 2,478 |
| Oct 18 | 7,967 | 9,549 | 4,405 | 1,250 | 2,250 |

- A little over half of the 20-second peaks have their high on the last trade of a run of trades on one side: the
  same tick as a peak with no window, and (but for a handful) the same side.
- Between a quarter and three in ten 20-second peaks have their high on a tick where nothing traded. The flow
  rose there because older trades dropped out of the 20 seconds. Those highs are made by the window, not by a
  trade.
- More than half of the peaks with no window have no 20-second peak at their high (trade day Oct 2: 6,164 of
  11,567).
- On a shared high the two are nearly always known on the same tick; where they differ the 20-second peak is
  known first (trade day Oct 2: same tick 4,716; 20-second first 674; no-window first 13).
- The taller a peak with no window, the more often a 20-second peak shares its high (trade day Oct 2: 1 lot 1,111
  of 2,747; 6 lots or more 2,391 of 4,327).
- By pile (the quote it pushes into), peaks with no window that share their high with a 20-second peak, trade day
  Oct 2: in between 713 of 1,339; at the beginning 1,292 of 2,599; at the end 719 of 1,837; one-step moves 2,679 of
  5,792. The end pile shares least.

## The story: what the peak tells, and what fills in the parts it cannot (Greg: "we don't have to pick winners. We just want the story")

No kind of data is being chosen over another here. Each is asked which part of the story it tells.

| Part of the story | What tells it | What the stored files showed tonight |
|---|---|---|
| Who was hitting, on which side, how much, and when it stopped or changed hands | THE PEAK (its side, its height, its tick) | This is the whole of what a peak holds. It is about the aggressor only. |
| Whether the price moved, and how far | The quote's runs and `move_steps` | A peak has no price in it. The largest pile of peaks sits in moves of one step. |
| Where in a move it is (beginning, middle, end) | The quote's runs, once the move has ended | At the time, two things lean one way or the other: the peak's height, and whether it pushes with the quote's last step or against it. |
| What it was pushing into | The book at the best price (the rows) | The size at the best price differs by pile. Which side of the whole book is thinner does not. |
| How the resting orders answered | `resting` (filled, pulled, stood), `refills`, `together` | First read below: it did not tell a beginning from an end. |
| What ended the move | The peak on the OTHER side | At the end of a move of the quote the peak there is on the other side about three times in four. |
| What the price did afterwards | `chain_peaks`, `move_steps` | First read below: about even three ways in every pile. |
| Why then | The outside figures (`outside_changes`) | Not looked at yet. |
| Native's dipole | `dipole_peaks` | The same in every pile: it did not help place a peak. |

### The first read of the book's answer (counts in `BOOK_ANSWER_BY_PILE.json`)

20-second peaks, each placed against the quote it pushes into; the orders at the best price it pushed into at
its high, by the tick the peak became known. Trade day Oct 2 (the other three read the same way):

| | In between | At the beginning | At the end | Whole one-step move |
|---|---:|---:|---:|---:|
| Peaks | 1,038 | 2,647 | 1,251 | 4,589 |
| An order there was filled out | 733 | 1,522 | 716 | 3,029 |
| An order there was pulled | 261 | 708 | 316 | 1,023 |
| Every order still there | 195 | 813 | 373 | 1,058 |
| Size added back to them | 7 | 28 | 12 | 35 |
| Price at the end of the peak's story: further the peak's way | 344 | 735 | 372 | 1,229 |
| back against the peak | 318 | 867 | 378 | 1,312 |
| where it was | 376 | 1,044 | 501 | 2,048 |

- The peaks in between more often ate through an order and less often left every order standing.
- The beginning and the end read alike. Claude's guess (orders that stand make an ending, orders that pull away
  make a beginning) is NOT borne out by this read: an order was pulled at about a quarter of the peaks in every
  pile.
- Size is almost never added back to those orders in that stretch.
- Where the price stood when the peak's story ended is about even three ways in every pile.
- Limits of this read: it uses the 20-second peaks (a quarter or more have highs on a tick with no trade); the
  stretch from the high to the tick the peak became known is short; and the end of a peak's story is set by the
  flow, not by the price. Not yet read: the resting orders through each run of the QUOTE (stored in `resting`),
  which is the book's answer measured over the price move itself.

## How a level emptied, and whether the move went on (the resting orders on the quote's own clock)

Read from the stored files in the session (told to Greg first); counts in `HOW_A_LEVEL_EMPTIED.json`. When the
quote backs away (the best ask going up, or the best bid going down) the level it leaves has emptied. For every
such move of two steps or more: of the orders that stood at the best price when the move started, were they all
filled, all pulled, or some of each, by the move's second step; and did the move take a third step.

Moves that took a third step, out of the moves in that row:

| Trade day and quote | Every order filled | Every order pulled | Some filled, some pulled |
|---|---|---|---|
| Oct 2, best ask up | 53 of 123 | 63 of 212 | 362 of 959 |
| Oct 2, best bid down | 60 of 135 | 37 of 144 | 383 of 1,060 |
| Oct 3, best ask up | 39 of 150 | 20 of 101 | 368 of 1,099 |
| Oct 3, best bid down | 51 of 149 | 26 of 126 | 321 of 947 |
| Oct 17, best ask up | 91 of 228 | 24 of 135 | 419 of 1,097 |
| Oct 17, best bid down | 60 of 173 | 43 of 196 | 461 of 1,245 |
| Oct 18, best ask up | 83 of 162 | 26 of 177 | 438 of 1,035 |
| Oct 18, best bid down | 74 of 154 | 50 of 245 | 422 of 1,130 |

- In all eight rows the moves whose first level emptied ONLY by orders pulling out took a third step least often
  (about 15 to 30 in 100, against about 26 to 51 where trades ate the level and about 33 to 42 where both
  happened).
- At the second step the side that pushes was the one hitting in nearly every case, whichever way the level had
  emptied (trade day Oct 2, best ask up: buyers hitting in 118 of 123, 186 of 212 and 944 of 959). The peak's side
  of the story reads the same in all three; the difference is in what the resting orders did. This is a part of
  the story the peak cannot tell.
- It is the opposite of Claude's earlier guess (that orders pulling away mark a beginning).
- Limits: only the first level of each move is followed; the rows with every order filled or every order pulled
  hold 100 to 250 moves each; no test of chance was made; most moves of the quote are one step long and are not in
  this table (about 5,200 to 6,100 a side a trade day).

## What Native's dipole says, laid against the peaks (Greg: "What does your just finished dipole research say")

Read from the stored `dipole_peaks` lines in the session (told to Greg first); counts in
`DIPOLE_AGAINST_PEAKS.json`. Native's record is Native's; nothing of it was worked out again.

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| Dipoles | 741 | 833 | 741 | 863 |
| Magnitude exactly 1 (the flow fully one-sided in its birth second) | 741 | 833 | 741 | 863 |
| A 20-second peak's high on its side in its birth second | 329 | 381 | 294 | 350 |
| A no-window peak's high on its side in its birth second | 133 | 144 | 118 | 130 |
| No peak's high of either kind in its birth second | 402 | 447 | 437 | 501 |
| Recognized exactly 50 seconds after its birth | 526 | 584 | 545 | 599 |
| At recognition, the latest peak on its side had already reached zero | 515 | 552 | 510 | 575 |
| At recognition, that peak's story was still open | 86 | 87 | 91 | 119 |
| At recognition, a rise under way on its side | 184 | 224 | 170 | 213 |
| At recognition, a rise under way on the other side | 151 | 160 | 132 | 170 |

- Every dipole is born in a second in which the flow was fully one-sided.
- Under half are born in the same second as a 20-second peak's high on the same side; more than half are born in a
  second with no peak's high at all.
- A dipole is known late: most are recognized exactly 50 seconds after the birth (Native's own fixed span), the
  rest a few seconds sooner.
- By the time it is known, the flow peak on its side has usually already faded to zero (about seven in ten).
- From the recognized line to the closing line: under 5 seconds for 193, 214, 158 and 205 dipoles; 60 seconds or
  more for 213, 216, 209 and 238 (these two marks are only to describe the spread). Nearly every closing line reads
  REVERSAL.
- A dipole was known at about one 20-second peak in seven, on the peak's side about three times in four, and the
  same in every pile: it did not help place a peak in a move.
- Its part of the story, as read so far: it marks that a fully one-sided burst happened about 50 seconds ago. What
  Native recorded about each dipole after that (its stages) has not been read.
