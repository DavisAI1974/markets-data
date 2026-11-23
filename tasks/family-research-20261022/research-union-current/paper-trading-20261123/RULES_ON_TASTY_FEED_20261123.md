# The 30 rules on the tastytrade sandbox feed: what each reads and whether the feed has it (2026-11-23)

Made before any runner code, on Greg's "Go". What each rule reads was listed by the scout agent (run 8 in
`agent-runs.jsonl`) from Claude's `strategy-20261123-claude/VERSIONS.md` (v2) and Codex's
`strategy-20261123-codex/VERSIONS.md` (branch `codex/ng-blind-20261123`). What the feed carries is from the 7e
records in `7e/` (stream run 5, `sandbox-stream-20261123T231453*`). Every trade made on this feed is NOT SCORED
(Greg: "We just won't grade them"). A rule that never opens a trade gets no bad mark; its record names the input
that was missing.

## What the feed carries (measured)

- TRADE PRINTS (TimeAndSale): price, size, the buy/sell side (9 of 107 had none), the exchange time in MILLISECONDS
  with a sequence number, and the best bid and best offer at the print. Not every trade: sizes added to 149 where the
  feed's own day volume said 172.
- QUOTES: best bid and best offer with sizes, in about half-second steps, with no time on them.
- 900 seconds behind the market, on every print.
- NOT CARRIED: single orders (no ids, no add, cancel or change), the exchange's end-of-event mark, nanoseconds.

## The stand-ins every runnable rule gets (each is written on every trade's record)

- S1 THE CLOCK. ROOT makes the two lines on the receive time in nanoseconds. Here several prints arrive in one
  message, so the lines are made on the feed's own trade time (milliseconds) and sequence.
- S2 THE EVENT MARK. The feed has none. A rule decides at the feed message that shows its trigger. "A different
  exchange event" (CX01, CX02) is read as "a different trade time on the feed".
- S3 THE QUOTES. At a print: the print's own bid and offer. Between prints: the quote messages in the order they
  arrive (half-second steps), so steps of the quote between two messages are not seen.
- S4 THE TRADES. The two lines are made from the prints that carry a side, as ROOT does; prints with no side are
  kept and counted. Prints the feed does not carry are not in the lines.

## The table

| Rule | Needs beyond prints, sides, the two lines and the quotes | On this feed |
|---|---|---|
| CL01 the eaten level | every order at a level left by FILL | CANNOT RUN: no single orders |
| CL02 the abandoned level | every order at a level was PULLED | CANNOT RUN: no single orders |
| CL03 first step made by a fill | the order whose leaving moved the quote was FILLED | CANNOT RUN: no single orders |
| CL04 a level only eaten | size filled and none pulled, added or moved at the level | CANNOT RUN: no single orders |
| CL05 a leg's first step, exhaustion on its side | trade leg, quotes at the print, 20s line | RUNS with S1 to S4 |
| CL06 both quotes stepped the same way | quote steps | RUNS with S2, S3 |
| CL07 fresh trading on the dipole's side | hump of the 20s line, 60s line, quote steps | RUNS with S1 to S4 |
| CL08 fresh trading against the dipole | as CL07 | RUNS with S1 to S4 |
| CL09 first step made by a cancel | the order whose leaving moved the quote was CANCELLED | CANNOT RUN: no single orders |
| CL10 price runs against the dipole, with the price | quote run's second step, 60s line | RUNS with S1 to S4 |
| CL11 price runs against the dipole, against the price | as CL10 | RUNS with S1 to S4 |
| CL12 the reloaded level | one order traded against and put back | CANNOT RUN: no single orders |
| CL13 paying up through more than one level | one event filling through more than one level | RUNS with a further stand-in: prints of one side sharing one trade time at more than one price |
| CL14 the other side arrives at the top step | quote steps, the first sell at the level | RUNS with S2, S3 |
| CL15 the step back and the return | quote runs | RUNS with S2, S3 |
| CX01 buying that carries into a new event | both lines, print and bid rise, a different event | RUNS with S1 to S4 (S2 for "different event") |
| CX02 selling moves the bid down | both lines, a reported seller, a different event | RUNS with S1 to S4 (S2 for "different event") |
| CX03 re-enter upward after a pullback | both lines, a buyer at the offer | RUNS with S1, S3, S4 |
| CX04 re-enter downward after a bounce | both lines, a seller at the bid | RUNS with S1, S3, S4 |
| CX05 exit an upward position when the bid gives way | an open upward position, both lines, the bid | RUNS on Codex's own entries, with S1, S3, S4 |
| CX06 exit a downward position as the offer lifts | an open downward position, both lines, the offer | RUNS on Codex's own entries, with S1, S3, S4 |
| CX07 follow a buyer to a higher offer | prints at the offer, a buyer, both quotes | RUNS with S3 |
| CX08 follow a seller to a lower bid | prints at the bid, a seller, both quotes | RUNS with S3 |
| CX09 reverse down from a stationary offer | 20s line, prints, both quotes | RUNS with S1, S3, S4 |
| CX10 reverse up from a stationary bid | 20s line, prints, both quotes | RUNS with S1, S3, S4 |
| CX11 stay up when a seller tests a higher bid | an open upward position, 60s line, quotes | RUNS on Codex's own entries, with S1, S3, S4 |
| CX12 stay down when a buyer tests a lower offer | an open downward position, 60s line, quotes | RUNS on Codex's own entries, with S1, S3, S4 |
| CX13 question a rise the bid does not follow | an open upward position, both lines, quotes | RUNS on Codex's own entries, with S1, S3, S4 |
| CX14 question a decline the offer does not follow | an open downward position, both lines, quotes | RUNS on Codex's own entries, with S1, S3, S4 |
| CX15 a pressure turn at an unchanged price | 20s line at two prints, print and both quotes unchanged | RUNS with S1, S3, S4 |

## The counts

- CANNOT RUN on this feed: 6 (CL01, CL02, CL03, CL04, CL09, CL12). All six need single orders.
- RUN with the stand-ins named: 24 (9 of Claude's, 15 of Codex's). CL13 has one more stand-in of its own.
- Of Codex's 15, six (CX05, CX06, CX11 to CX14) manage a position already open: they attach to Codex's own entries
  only, never to Claude's (Claude's call of the eighteenth session).

## Open, Claude's calls, Greg's to strike

1. THE LINES' CODE. The two lines are made by two functions of `crypto_ng/tick.py` (`reads` and `line`). The runner
   calls those two functions as they are, and nothing else of that package. Markets `CLAUDE.md` says nothing of that
   package is imported by a strategy, and also that the two lines ARE strategy inputs and are not to be reinvented.
   Calling the same two functions is the only way to do both.
2. THE END OF THE TRADE DAY. The feed is 900 seconds behind and the sandbox refuses futures orders from 5 to 6 pm
   Eastern, so the feed's last tick (5 pm) arrives at 5:15 pm when nothing can be sent. The runner stops opening and
   flattens when the FEED shows 4:44 pm (4:59 pm by the wall clock). Those closing orders are marked as such and are
   not trade data.
3. The settlement window (2:28 to 2:30 pm Eastern) is read on the feed's own time.
