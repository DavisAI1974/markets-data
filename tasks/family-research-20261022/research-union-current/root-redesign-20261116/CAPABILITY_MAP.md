# Capability Map: ROOT redesign (draft 2 for Greg's review, 2026-11-16)

Status: DRAFT. No module spec is written and no code changes until Greg approves this map.

## The governing rule (Greg, 2026-11-16)

"This is what we're trying to figure out, what pieces of data are dictating things and when we decide ahead of time,
we're killing our own research silently."

So ROOT decides nothing ahead of time. It records what the tape says, completely, at the tape's own resolution. It
does not select, threshold, summarize, sample, rank or drop. Which pieces of data matter is the research question,
answered afterwards from the full record, trade by trade.

Where a choice cannot be avoided, it is never silent: it is written down by name next to the thing it affects, and
the alternative is kept beside it so the choice can be undone from the saved record without rerunning.

Draft 1 of this map broke that rule in four places, corrected below: it listed five kinds of span as the set; it
carried the old calculations forward as a fixed "measures" piece; it put the finding of candidates, episodes and
families inside ROOT; and it assumed the book is read only when an exchange event closes.

## Other decisions already made by Greg (2026-11-16)

- Nanosecond resolution, each message, in tape order. No whole-second stepping.
- No fixed windows anywhere. Full depth everywhere: every price level and every order.
- All kinds of span are computed and the data decides which apply.
- Everything we hold gets run. Redundant passes and builds are removed.
- Input is the trade-day stream: Sunday warm-up, book carried through every 00:00 UTC, no order age restarted.
- The old ROOT and its outputs are not a reference and are not kept.
- Standing rules: trade day only; every trade individually; IDs and clocks designate and are not inputs; never
  invent data; no trade cost in any calculation; leakage gate before any backtest.

## ROOT: the complete record (no choices inside)

| Module id | Responsibility | Depends on |
|---|---|---|
| `tape-stream` | One trade day of messages in tape order with nanosecond clocks, warmed from the Sunday open and carried through every 00:00 UTC, with the list of orders whose age is only a lower bound. Same interface for a live feed. | — |
| `book-core` | One full-depth order book per instrument: every order, its queue position and its times. One pass over the tape. Checked against the exchange's own snapshots. | `tape-stream` |
| `event-ledger` | One record per message, nothing left out: what the message was, what it did to which order, and every change it caused in the book. The end-of-event flag is recorded on the message that carries it, so a reader can take the book after any message or only at event closes. | `book-core` |
| `change-points` | Every change of state the tape shows, of every kind, each as its own record with the message that caused it: a price level appears or empties; the best bid or ask moves; an order joins, shrinks, grows, moves or leaves; a queue's front changes; the side doing the trading flips; a level that was eaten is refilled. This is the raw material for any span. ROOT does not pair them into chosen spans. | `event-ledger` |
| `store` | What is saved and how: files, lists with sizes and fingerprints, receipts. Nothing is saved as a summary in place of its detail. | each producing module |
| `checks` | How we know the record is right without the old ROOT: snapshot equality at every 00:00 UTC, queue sums, every message accounted for, historical-versus-live agreement on a recorded stretch. Also a guard that fails the build if ROOT code contains a window length, a threshold, a top-N or a sample that is not on a short declared list with its reason (for example the exchange's tick size). | each producing module |

Build order: `tape-stream` → `book-core` → `event-ledger` → `change-points`, with `store` and `checks` alongside.

## Research on top of the record (every definition visible, none built into ROOT)

| Module id | Responsibility | Depends on |
|---|---|---|
| `spans` | Spans formed by pairing change points: order life, level at the front, one-sided run, drain and refill, a structure's own life, and any other pairing the record supports. All are formed; none is preferred. Each pairing rule is a named definition that can be added to or changed without touching ROOT. | `change-points` |
| `structures` | Candidates, episodes, dipoles, families and lineage as named, versioned definitions read off the record and the spans. No percentile bar, warm-up or spacing rule. The 2021 Step 1 family definitions are the base and are expanded by what the new data shows. A definition never removes anything from the record. | `spans` |
| `trade-join` | For every trade individually: every span and structure it sits inside, where in their life, and the values at that moment. Feeds the sheet. | `spans`, `structures` |

The old calculation sections (queue, replenishment, absorption, mirror, response, exhaustion, flow shares) are not
carried forward as fixed pieces. Whatever each was trying to measure is re-asked of the full record, and its fixed
horizon is gone. The audit list of every fixed window, cap and collapse in the old ROOT is
`../root-audit-20261116/ROOT_WINDOWS_AND_CAPS.md`.

## Assumptions (correct any that are wrong)

1. This is new code that reads the trade-day stream. The pinned producer package is not edited.
2. The order-book rule stays the one the pinned adapter uses. It matched the exchange on all 2,926 orders checked.
3. Receive time is "when it could be known"; event time is kept beside it.
4. First target: the front-month tape for the four October 2023 trade days. Other contract months join where held.
5. The record is the tape plus the ledger and change points. The full book at any message is reproduced exactly by
   replay rather than saved as a picture at every message. Nothing is lost by this; it is only where the bytes live.
6. Historical and live use one code path.
7. Runs happen on Runpod CPU pods, after a short trial stretch passes here.

Already existing: `tape-stream` and the per-trade part of `book-core` are in
`../trade-day-rebuild-20261116/scripts/` (`trade_day_stream.py`, `build_book_records.py`). They are hard-coded for
October 2023 (the 17:00 ET halt as 21:00 UTC, the contract, the file list) and have no live adapter yet.
