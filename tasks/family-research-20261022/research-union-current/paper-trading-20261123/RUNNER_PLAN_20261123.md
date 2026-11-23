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
