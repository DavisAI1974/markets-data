# Building a trade day (recipe, 2026-11-16)

A trade day is the CME session: 17:00 ET the evening before (the halt; trading resumes 18:00 ET) to 17:00 ET on the
named date. The vendor cuts raw tape files by UTC clock day (00:00-24:00 UTC). Everything here is built and labelled
on the trade day; the UTC clock day is only the shape of the download.

A new trade day built this way from the start needs none of the repair work done on the four October 2023 trade days.
That work existed only because the first build was cut on UTC clock days and had to be reconciled afterwards.

## Steps for a new trade day

1. **Download** raw MBO (order-level) tape for the front contract, one file per UTC clock day, from the Sunday that
   opens the trade week through the named date. A Monday trade day needs the Sunday file and the Monday file. A
   Thursday trade day needs Sunday through Thursday. Add each file to the tape `MANIFEST.json` with its byte count and
   SHA256. The Sunday file is small (12,532 and 29,063 records on the two Sundays held; a weekday is about 800,000).
2. **List the warm-up files** for the trade day in `WARMUP` in `scripts/trade_day_stream.py`, oldest first, ending
   with the UTC clock day before the named date.
3. **Run** `python3 scripts/build_trade_day.py <YYYYMMDD> results`. For a trade day with no earlier archive, use
   `trade_day_stream.trade_day(day)` directly: it yields every session message with the live carried book.
4. **Read the receipt.** It must show, for every 00:00 UTC crossed, that the carried book equals the exchange's own
   snapshot: same orders, sides, prices, sizes, and the same queue order on every price level. The replay refuses to
   continue if it does not.

## What the replay does on its own, every time

- Starts the book at the Sunday re-listing block and carries it straight through every 00:00 UTC. Opening snapshots
  after the first file are checked against the carried book and not applied, so no order's time is restarted.
- Cuts the trade day at 17:00 ET on both sides and leaves the hours after the halt in the file, unused, for the next
  trade day.
- Keeps a live list (`floor`) of the resting orders whose time is only a lower bound. With the Sunday file in the
  warm-up these are only the orders the exchange re-listed on Sunday; their real entry time is not on the tape.

## Settled facts that do not need re-checking (`../resting-order-age-20261116/`)

- A snapshot record's event time is the event time of the message that last set that order's queue priority
  (2,926 of 2,926 orders at four 00:00 UTC boundaries).
- The exchange re-lists every order carried over the weekend in one block on Sunday with one stamp.

## Hard-coded for October 2023; change before using on other dates

- `HALT_UTC_NS` is 21:00 UTC, which is 17:00 ET only while daylight time is in force. In standard time the halt is
  22:00 UTC.
- `INSTRUMENT = 150611` and the symbol `NGX3` are the November 2023 contract.
- `WARMUP` and `TAPE` list the October 2023 files by hand. A holiday week, or a week whose Sunday file is missing,
  needs its own entry.
- `build_trade_day.py` compares against the October 2023 archives; a new trade day has none.

## The four October 2023 trade days as built

| Trade day | Warm-up files (UTC clock days) | Session messages | Trades | Floor orders at session start / at the halt |
|---|---|---:|---:|---|
| Oct 2 | Oct 1 | 820,642 | 38,127 | 342 of 342 / 251 of 725 |
| Oct 3 | Oct 1, 2 | 879,830 | 41,410 | 251 of 725 / 217 of 748 |
| Oct 17 | Oct 15, 16 | 846,406 | 33,703 | 210 of 745 / 183 of 790 |
| Oct 18 | Oct 15, 16, 17 | 771,787 | 30,739 | 183 of 790 / 164 of 723 |

On all four: every message equals the archived message at its mapped position, every one of the 143,270 archived
trades is found identical, and 709 trades the archives never held (18:00-20:00 ET on trade days Oct 2 and 17) are
listed in `results/*_trades.parquet`.
