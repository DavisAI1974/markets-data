# Capability Map: ROOT redesign (draft for Greg's review, 2026-11-16)

Status: DRAFT. No module spec is written and no code changes until Greg approves this map.

## Decisions already made by Greg (2026-11-16)

- ROOT runs at the tape's own resolution: nanoseconds, each message, in tape order. No whole-second stepping.
- No fixed windows anywhere. The data defines the spans.
- All of these spans are computed, and the data decides which apply: an order's life; a price level's time at the
  front; a run of one-sided trading; a queue's drain and refill; a family's or dipole's own life.
- Full depth everywhere: every price level and every order. No top-10 or top-of-book views.
- Everything we hold gets run.
- Redundant passes and builds are removed.
- Input is the trade-day stream: Sunday warm-up, book carried through every 00:00 UTC, no order age restarted.
- The old ROOT and its outputs are not a reference and are not kept.
- Standing rules still apply: trade day only; every trade individually; IDs and clocks designate and are not inputs;
  never invent data; no trade cost in any calculation; leakage gate before any backtest.

## Assumptions (correct any that are wrong)

1. This is new code that reads the trade-day stream. The pinned producer package is not edited.
2. The order-book rule stays the one the pinned adapter uses. It matched the exchange on all 2,926 orders checked.
3. Orders, fills and flow are stepped message by message. Book readings are taken when an exchange event's group of
   messages closes, because the book between two messages of one group never existed publicly. (Greg to confirm.)
4. Receive time is "when it could be known"; event time is kept beside it.
5. First target: the front-month tape for the four October 2023 trade days. Other contract months join only where
   we hold them.
6. Saved output is derived values with their designations. The full book is reproduced by replay, not saved at every
   message. (The per-trade book records are the exception and are already stored.)
7. Historical and live use one code path.
8. Runs happen on Runpod CPU pods, after a short trial stretch passes here.

## Modules

| Module id | Responsibility | Depends on |
|---|---|---|
| `tape-stream` | One trade day of messages in tape order with nanosecond clocks, warmed from the Sunday open and carried through every 00:00 UTC, with the list of orders whose age is only a lower bound. Same interface for a live feed. | — |
| `book-core` | One full-depth order book per instrument: every order, its queue position and its times. One pass over the tape. Checked against the exchange's own snapshots. | `tape-stream` |
| `event-ledger` | One record per message: each order's adds, changes, cancels and fills; each trade with its side; signed flow per trade, unbinned. | `book-core` |
| `spans` | The data-defined spans, all kinds: order life, level at the front, one-sided run, drain and refill. Each with its start and end messages, nanosecond clocks and what happened inside it. No fixed lengths. | `event-ledger`, `book-core` |
| `measures` | The ROOT calculations (queue, replenishment, absorption, mirror, response, exhaustion, flow shares) restated on spans, replacing fixed horizons. | `spans` |
| `structures` | Candidates, episodes, dipoles, families and lineage, found from the data with no percentile bar, warm-up or spacing rule. Includes each structure's own life as a span. | `spans`, `measures` |
| `trade-join` | For every trade individually: the spans and structures it sits inside, where in their life, and the values at that moment. Feeds the sheet. | `spans`, `structures` |
| `store` | What is saved and how: files, lists with sizes and fingerprints, receipts. | each producing module |
| `checks` | How we know it is right without the old ROOT: snapshot equality at every 00:00 UTC, queue sums, every message accounted for, historical-versus-live agreement on a recorded stretch, the leakage gate. | each producing module |

Build order: `tape-stream` → `book-core` → `event-ledger` → `spans` → `measures` → `structures` → `trade-join`,
with `store` and `checks` built alongside each one.

Already existing: `tape-stream` and the per-trade part of `book-core` are in
`../trade-day-rebuild-20261116/scripts/` (`trade_day_stream.py`, `build_book_records.py`). They are hard-coded for
October 2023 (the 17:00 ET halt as 21:00 UTC, the contract, the file list) and have no live adapter yet.

## What each later module spec must answer

- `spans`: the exact start and end rule for each span kind, written against tape messages.
- `measures`: for each of the old sections, what its fixed horizon becomes. The audit list of every fixed window,
  cap and collapse is `../root-audit-20261116/ROOT_WINDOWS_AND_CAPS.md`.
- `structures`: what makes something a candidate, an episode, a dipole or a family once the bar, the warm-up and the
  spacing rule are gone; and how the 2021 Step 1 family definitions are used as the base and expanded.
- `store`: sizes. A trade day has about 580,000 to 650,000 exchange events and 770,000 to 880,000 messages.
