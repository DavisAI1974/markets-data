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
