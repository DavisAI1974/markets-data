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
