# The paper runner on the tastytrade sandbox: the build plan (2026-11-23), for the reviewer before the builder

Greg's go, 2026-11-23: run the 30 on the tastytrade sandbox feed, ungraded ("Let's see if our strategies sell even
with thin data. We won't give it a bad mark if it doesn't but maybe it will"). Read beside this:
`RULES_ON_TASTY_FEED_20261123.md` (which rules run, the stand-ins S1 to S4), the 7e records in `7e/`, handoff U
(the runner rules), and the rules themselves (Claude's `strategy-20261123-claude/VERSIONS.md` v2; Codex's
`strategy-20261123-codex/VERSIONS.md` on branch `codex/ng-blind-20261123`).

## What is built (Markets, session branch `ccr-532eaea6-vgz20z`; every file NEW; nothing existing is replaced)

All under `strategies/paper/`:

1. `feed_tasty.py`. Turns DXLink FEED_DATA into two plain events, in arrival order, each with our receive time in
   nanoseconds and its place in the recording: PRINT (TimeAndSale: feed time in ms, sequence, price, size, side
   BUY/SELL or none, the print's own bid and offer) and QUOTE (bid, offer, sizes; no time). It reads either the live
   socket or a 7e recording file (`sandbox-stream-*.jsonl`), the same code path for both. Sign-in, the recorder, the
   scrubbing of secrets and the DXLink handshake are IMPORTED from `strategies/tasty_7e_check.py`, not rewritten.
2. `lines.py`. The two lines at each print: calls `crypto_ng.tick.reads` and `crypto_ng.tick.line` as they are, on
   the prints that carry a side, in feed order (time in ms made into ns, then sequence), spans `tick.LINE_NS` (20 s)
   and `tick.LEAN_NS` (60 s). Nothing else of `crypto_ng` is imported. A hump of the 20-second line as
   `root/crypto_ng_tick.py` defines it (the time the line stays on one side of zero). A moment at which trades only
   LEAVE a span has no message on this feed: it becomes known when the next print arrives (its feed time passes it).
   A line or hump change at such a moment opens nothing (CL rule 6); a close that depends on it is made at that
   next print and marked "known late: no feed message at the moment".
3. `quotes_live.py`. The quote's runs: `root.calcs.quote_runs.QuoteRuns` as it is, fed the best bid and best offer
   of every PRINT and QUOTE event in arrival order. The trade legs: `root.calcs.leg_peaks.Legs` as it is, fed every
   print. If either class cannot be used without the stored rows, the builder STOPS and hands back; it does not
   write its own.
4. `rules_cl.py`, `rules_cx.py`. One small class for each of the 24 rules that run; each sees only events up to
   now and its own open trades, and returns OPEN (side) or CLOSE (which trade, why). No I/O, no clock of its own,
   no knowledge of tastytrade: so another platform can reuse them. The 6 that cannot run are listed with the
   missing input and never open. Each rule's text is the authority; where a rule's wording cannot be carried on
   this feed beyond S1 to S4 the builder STOPS and lists it, and makes no choice of its own.
5. `ledger.py`. One line for each paper trade of each strategy, never netted across strategies: the events that
   opened and closed it, both quotes at each end each on its own, the rule's own trigger values, the stand-ins
   used, "not scored: tastytrade sandbox feed". No result figure, no mid price, no cost.
6. `broker_tasty.py`. For each OPEN or CLOSE: dry-run, then one Market Day order of 1 lot with a unique
   `external-identifier` that carries the strategy and the trade; never re-sent; an order's outcome is read from
   its FILLS and the POSITIONS, never from status alone (order 2207911 stayed "Live" with a recorded fill).
7. `runner.py`. The loop. Arguments, none defaulted by the code: `--out` (a markets-data folder; refuses Markets),
   `--account`, `--symbol`, `--streamer-symbol`, `--seconds` (how long to run), `--max-orders` (the order budget:
   at that count it stops opening, flattens and stops), `--replay FILE` (read a recording instead of the socket;
   sends NO orders), `--orders` (without it nothing is sent to the sandbox even on the live feed).
   - Start: confirms the account holds no position and no live order; otherwise stops.
   - Stop at 5.75 hours, at `--seconds`, at `--max-orders`, or when the feed shows 4:44 pm Eastern: flatten every
     position with closing orders marked "flattened at the stop" (not trade data), then a final pull of orders,
     fills and positions.
   - No order is sent from 5 to 6 pm Eastern (the sandbox refuses futures then).
   - Everything is appended as it happens to JSONL in `--out` (feed messages whole, events, signals, orders, fills,
     ledger lines) with a receipt at the end, as the 7e check writes them.

## The checks (real data only; no made-up message anywhere)

- The only inputs for a check are the real recordings in `7e/` (run 5, ten minutes; a 25-minute one is being
  recorded now). A test that cannot find them is skipped, not fed invented data.
- CUT EQUALS WHOLE (Greg's check): for a recording, the trades the 24 rules open and close on the recording cut at
  message k equal those on the whole recording up to message k, for every k tried.
- LIVE EQUALS REPLAY: the lines at each print from `lines.py` equal `tick.reads`/`tick.line` run once over the
  whole recording.
- The receipt counts: prints, prints with no side, quote messages, and for each of the 30 rules how many times it
  armed, opened, closed, and how many times an input was missing.

## Not in this build

GitHub Actions, the live page and the phone notice (outside services are named to Greg first); the second ROOT;
the graph links; any scoring.

## Questions for the reviewer

1. Is calling `crypto_ng.tick.reads` and `tick.line` consistent with Markets `CLAUDE.md` (the package rule as amended
   2026-11-23, and "do not reinvent")?
2. Does anything here let a rule see a message later than the one it decides at?
3. Are S1 to S4 and the "known late" handling stated honestly, or does any of them quietly change a rule?
4. Is anything here a trade cost, a mid price, an average, a ranking or a label?
5. Is the order path safe: can it send twice, send to production, or leave a position after a stop?
6. What is missing that would make the canary's record unusable?

---

# CHANGES AFTER THE REVIEW (reviewer agent, Opus, run 9; verdict: go with changes). These replace the text above where they differ.

## Waiting on Greg's word (the builder does not start before it)

- G1 ONE SOURCE FOR THE QUOTE. The reviewer measured, on stream run 5: bid changes 38 from the prints' own bid, 37
  from the Quote messages, 74 when the two are interleaved; 42 of the 73 changes fall at a switch between the two.
  Feeding both into one run-follower makes steps that are not in the market. Claude's call: the rules read the
  quote from the PRINTS' OWN bid and offer only (they carry a time and an order); the Quote messages are recorded
  and followed in a second, separate run-follower that no rule reads. Cost of it: a step of the quote is seen only
  when a trade prints.
- G2 THE LINES' CODE. `crypto_ng/tick.py` lines 34-35 say nothing of it is imported by a strategy; the amendment of
  2026-11-23 makes the lines strategy inputs and does not lift that. Calling `tick.reads` and `tick.line` from the
  runner needs Greg's word, written down.
- G3 THE START. A run that starts after the feed's 6 pm open has a wrong 60-second line for its first 60 seconds, a
  cut first run of each quote and a cut first trade leg. Claude's call: those are counted as missing inputs (a rule
  that reads them does not open until they are whole: 60 seconds of prints for the dipole, 20 for the exhaustion,
  the first run and the first leg ended), not a start only at the open.
- G4 COPYING, NOT IMPORTING, THE 7e STREAM AND SUBMIT CODE. `stream()` and the submit in `tasty_7e_check.py` are
  written inline and hand back no events, so they cannot be imported. Claude's call: a new module copies those
  parts with the source lines named; the 7e file is not edited.

## Adopted (Claude's, from the review)

- S5, a named stand-in: a moment at which trades only leave a span is known at the next print; a close that depends
  on it is made then and says so. This suppression of OPENS at such a moment is for Claude's rules only (rule 6);
  Codex's preamble lets trades leaving a span count, at the next print.
- S6, a named stand-in: the end-of-trade-day close (5 pm) cannot be sent; the flatten at the stop takes its place.
- The lines: the time is the feed's milliseconds made into nanoseconds exactly; the sequence only orders prints
  that share a time; `until` is the latest print's time plus one, as `root/crypto_ng_tick.py` does. EMPTY is carried
  apart from zero: a rule that reads an empty line is "indeterminate" (Codex) or does not open (Claude's rule 5),
  never "the line reached zero".
- A NaN bid or offer is a missing input, never a price.
- Prints with no side: counted on every receipt (39 of 97 in the second recording at the time it was read, 9 of
  107 in run 5). A rule that needs a side does not act on such a print.
- GAPS: the feed misses prints. A gap is read from the Trade message's day volume against the sizes of the prints
  seen; at a detected gap Codex's rules reset as their preamble says, and every rule's record carries the count.
- Codex's management rules (CX05, CX06, CX11 to CX14): an "exit indication" closes that position of Codex's; a
  "hold", "maintain" or "suspend additions" sends no order and is written on the ledger line. Codex's rules hold
  one active entry for each strategy at a time; Claude's may hold several (rule 2).
- ORDERS: a fresh sign-in token before every submit; an uncertain submit goes to the look-up and then the flatten,
  never a second send; a close is sent only after its open's fill is confirmed, and once; outcomes are read from
  fills by `external-identifier`, the account's position is the account-level check only; the runner is fixed to
  the sandbox address; the order budget keeps back enough orders to flatten; a kill signal runs the flatten.
- STOPS: by the wall clock as well as the feed, whichever comes first: no opening after 4:44 pm on the feed or
  4:50 pm Eastern on the wall clock; no order from 5 to 6 pm Eastern by the wall clock. The refusal in that hour is
  on record: `7e/sandbox-order-20261123T223131712768164Z.jsonl`, HTTP 422 `tif.futures_session_not_active` at
  17:31 Eastern.
- THE LEAKAGE GATE: the cut-equals-whole check stands in for `odcore/leakage.py` on a replay and the receipt says
  so; nothing here is a backtest result.
- NOT YET TESTABLE ON REAL DATA: the 4:44 pm stop, the halt hour and the settlement window (the recordings cover
  about 6:00 to 6:26 pm on the feed). Said on the receipt; a recording across those hours is needed before a run
  through them.
