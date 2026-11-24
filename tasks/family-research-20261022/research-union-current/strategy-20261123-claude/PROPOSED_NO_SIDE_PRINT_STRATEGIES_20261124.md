# PROPOSED, NOT ADOPTED: two strategies made for the print with no side (Claude, 2026-11-24, twentieth session)

Greg, 2026-11-24, on what a print with no side should do: "We need to create a strategy for that amd not just a
code fix"; "We can make a 31 trade strategy if needed. The 30 is a jumping off point, not the limit".

Nothing here is in the runner's code. Nothing here has been traded. These are drafts for his word; either, both or
neither may go forward, and either may be rewritten.

## What they rest on

- On ROOT's tape a trade the tape gives no side for is an implied or spread trade (`STEP1_STEP2_LAYOUTS.md`). It is
  in neither line, and rule 5 of "what holds for all fifteen" lets it open and close nothing. None of the 30 rules
  reads it.
- On the tastytrade sandbox feed (record: the last section of
  `paper-trading-20261123/step0-20261124/STEP0_TRACE_20261124.md`): 9 of 107 prints and 141 of 440 prints have no
  side. Every one trades exactly at its own bid or its own offer (4 and 5; 108 and 33). They are the first to show
  6 of 52 and 34 of 149 steps of the quote, and 6 of 43 and 80 of 216 new prices. Nothing else in the message
  tells them apart from a print with a side.
- NOT COUNTED ANYWHERE: what the price or the quote did after such a print. Not on this feed, and not on the four
  trade days (Oct 2, 3, 17, 18, 2023). Both rules below have "no count" behind them, like CL06, CL08, CL13, CL15.

## CL16 (proposed). A step of the quote first shown by a print with no side

- WHEN: unknown; that is what paper trading is to show.
- TRIGGER: a print with no side whose own quote shows a step of the best bid or of the best offer (that quote is
  not where it stood at the print before).
- DECIDED AT: that print.
- SIDE: with the step. BUY for a step up. SELL for a step down.
- CLOSES: at that quote's first step back. RIGHT if that quote stepped further the same way first; WRONG if the
  step back came first.
- OPENS AGAIN: at the next such step. The same run of the quote never opens a second trade.
- READS: the prints with no side, the quote at each print, `quote_runs`.
- BEHIND IT: no count.

## CL17 (proposed). The print with no side, taken at the quote it traded at

- WHEN: unknown.
- TRIGGER: a print with no side trades at its own best offer (mirror: at its own best bid), and it is the first
  print with no side at that level.
- DECIDED AT: that print.
- SIDE: the side a marked print there would have had. BUY at the offer. SELL at the bid.
- CLOSES: at the first step back of the quote it traded at. RIGHT if that quote stepped further away first (the
  offer up for a BUY, the bid down for a SELL); WRONG if the step back came first.
- OPENS AGAIN: at the next print with no side at a new level of that quote.
- READS: the prints with no side, the quote at each print, `quote_runs`.
- BEHIND IT: no count. It asks one question on its own: does a print with no side at the offer behave like a buy.
  The two lines are NOT changed by it: no side is written into the dipole or the exhaustion.

## What stays as it is

The 30 are not changed by these. No side is guessed inside the dipole or the exhaustion. Each trade of CL16 and
CL17 is its own ledger line, never netted, not scored on this feed.
