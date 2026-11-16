# Resting-order age: what the tape can and cannot say (2026-11-16)

Question carried from the last handoff: an order already resting when the replay's warm-up file opens gets stamped
with that file's opening receive time, so its age is a floor, not its age. Two checks were run before choosing what
to do. Every result below is a count of individual orders; the per-order rows are in `results/`. Order IDs and
clocks designate orders and messages. None is an input to a market calculation.

Raw tape: `data/nymex_mbo/ng_v0_oct2023/`, UTC clock-day files Oct 1, 2, 3, 16, 17, 18. Book rule: the pinned adapter
(Markets `7f34afa`), unchanged.

## Check 1: what the event time on a 00:00 UTC snapshot record means

`scripts/snapshot_event_time_check.py`, one row per resting order in `results/snapshot_orders_<prior>_to_<next>.csv`.

At each of the four 00:00 UTC file boundaries the whole prior file was replayed, keeping beside the book the exchange
event time and sequence of the message that last set each order's priority. That was compared with the snapshot
record for the same order.

| 00:00 UTC of | Orders | Snapshot event time and sequence equal the replay's priority-setting message | Priority reset by a later modify: snapshot shows the reset / shows the original entry | Size reduced after priority was set: snapshot unchanged / moved to the change |
|---|---:|---:|---:|---:|
| Oct 2 | 732 | 732 | 31 / 0 | 19 / 0 |
| Oct 3 | 740 | 740 | 35 / 0 | 9 / 0 |
| Oct 17 | 737 | 737 | 42 / 0 | 3 / 0 |
| Oct 18 | 717 | 717 | 46 / 0 | 2 / 0 |

On all 2,926 orders the snapshot's event time is, to the nanosecond, the event time of the message that last set the
order's queue priority, and the sequence number matches too. It is not the original entry time when a modify has
since changed the price or raised the size (154 orders, 154 show the reset). It does not move when the size is only
reduced (33 orders, 33 unchanged). The pinned adapter's priority rule and the exchange's agree on every order checked.

The snapshot carries that event time across files: an order unchanged since Oct 1 still shows its Oct 1 event time in
the Oct 3 snapshot.

## Check 2: the orders already resting when the Sunday file opens

`scripts/weekly_relisting_ledger.py`, one row per order in `results/weekly_relisting_orders_20231001.csv`.

The UTC clock-day Oct 1 file opens with a clear record at 11:05:07 UTC, then a block of 342 adds. All 342 carry one
event time, 12:00:04.281532035 UTC (08:00:04 ET Sunday), and one receive time, 12:00:04.481274710 UTC. The first live
message is at 21:01:00 UTC. So the exchange re-lists every order carried over the weekend in one block, with one
stamp. The real entry time of those orders is not on the tape at all, in any file.

Of the 342: all 342 are resting when trade day Oct 2 starts (21:00 UTC Oct 1); 319 are untouched for the rest of the
file; 21 are removed; 4 have their priority reset by a modify. 319 are in the 00:00 UTC Oct 2 snapshot with the block's
event time, and 247 are still in the 00:00 UTC Oct 3 snapshot with it.

That is why trade day Oct 2 showed 0 orders "more than a second older than the replay knows": the replay stamps the
block 0.2 seconds after its event time. The 0 does not mean those ages are true ages.

The second week has the same block: in the 00:00 UTC Oct 16 snapshot the oldest event time is 12:54:42.688701461 UTC
Oct 15, shared by 207 of the orders still resting at 00:00 UTC Oct 17 and 182 at 00:00 UTC Oct 18.

## What was done (Greg, 2026-11-16: the third option)

The adapter rule is left alone. No event time is mixed into the receive-time ages. Instead the warm-up now starts at
the earliest UTC clock-day file held for the trade week, and every later opening snapshot it passes is checked against
the carried book and not applied (`trade-day-rebuild-20261116/scripts/trade_day_stream.py`, `WARMUP`).

| Trade day | Warm-up files | Floor orders at session start / at 00:00 UTC / at the halt | Kind of floor | Orders over 1 s older than the replay at 00:00 UTC: first build / now |
|---|---|---|---|---|
| Oct 2 | Oct 1 | 342 of 342 / 319 of 732 / 251 of 725 | weekly re-listing block | 0 / 0 |
| Oct 3 | Oct 1, Oct 2 | 251 of 725 / 247 of 740 / 217 of 748 | weekly re-listing block | 252 / 0 |
| Oct 17 | Oct 15, Oct 16 | 210 of 745 / 207 of 737 / 183 of 790 | weekly re-listing block | 225 / 0 |
| Oct 18 | Oct 15, Oct 16, Oct 17 | 183 of 790 / 182 of 717 / 164 of 723 | weekly re-listing block | 278 / 0 |

Verified after the change (`trade-day-rebuild-20261116/results/*_RECEIPT.json`): on all four trade days every message
still equals the archived message, every one of the 143,270 existing trades is still found identical at its mapped
cursor and group, the trade lists are byte-for-byte the lists from the first rebuild, and the carried book equals the
exchange snapshot at every 00:00 UTC crossed, the extra ones in the longer warm-ups included.

The replay keeps a live list (`floor`) of every resting order whose priority time is a floor, with the kind of floor
and the snapshot's event time beside it, so each age value built on such an order can be marked as a lower bound,
order by order. An order leaves the list when it is removed or a modify resets its priority.

## The UTC clock-day Oct 15 file (added 2026-11-16)

Downloaded at Greg's request: `NG_v0_mbo_20231015.dbn.zst`, 29,063 records, the same single instrument, cost $0.0027.
It opens like the Oct 1 file: a clear record, then a block of 350 re-listed orders with one event time
(12:54:42.688701461 UTC) and one receive time (12:54:42.891809140 UTC). With it in the warm-up, trade days Oct 17 and
18 are on the same footing as the first week: no order at 00:00 UTC is more than a second older than the replay
knows, and the only floors left are the Sunday re-listed orders.

## How far receive time sits from event time

For the 1,852 orders at the four boundaries that have their own live message, receive time minus event time runs from
0.076 ms to 245 ms; 111 are over 1 ms, 29 over 10 ms, 1 over 100 ms, none over 1 second. This is the size of the
difference that reading an order's time from a snapshot (event time) instead of replaying earlier files (receive
time) would introduce.
