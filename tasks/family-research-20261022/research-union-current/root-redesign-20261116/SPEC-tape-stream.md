# Spec: `tape-stream` (draft for Greg's review, 2026-11-16)

First module of the ROOT redesign (`CAPABILITY_MAP.md`). Everything else reads from it.

## Objective

Give every later module one trade day of exchange messages exactly as the tape has them: every message, in tape
order, with nanosecond clocks, on a book that was seated at the Sunday open of the trade week and carried through
every 00:00 UTC without restarting any order's age. The same interface must serve a live feed, so historical and live
runs compute the same way.

It exists today for the four October 2023 trade days (`../trade-day-rebuild-20261116/scripts/trade_day_stream.py`),
with dates, the contract and the halt hour written in by hand. This spec is what it must do for any trade day.

## Success criteria

1. **The trade day is cut by exchange time, not a fixed UTC hour.** It yields exactly the messages received from
   17:00 ET the evening before to 17:00 ET on the named date, in standard time and in daylight time.
2. **Warm-up comes from the calendar.** It works out which UTC clock-day files are needed, from the Sunday that opens
   the trade week through the named date, and refuses to run, naming the file, if one is missing.
3. **Nothing is restarted.** Only the first file's opening block seats the book. Every later opening snapshot is
   compared with the carried book (same orders, sides, prices, sizes, and the same queue order on every price level)
   and not applied. A mismatch stops the run.
4. **Every message is delivered.** The count of messages delivered equals the count in the tape for that span; no
   message is skipped, merged or reordered. The end-of-event flag is passed through on the message that carries it.
5. **Lower-bound ages are marked.** The live list of resting orders whose age is only a lower bound is kept, with
   the kind of floor.
6. **The contract comes from the tape.** The instrument is taken from the tape's own symbol mapping for that trade
   day, not written in. A contract roll inside a trade week is reported, not guessed through.
7. **It reproduces what is already verified.** On the four October 2023 trade days it yields 820,642, 879,830,
   846,406 and 771,787 session messages and 38,127, 41,410, 33,703 and 30,739 trades, identical to the committed
   trade lists.
8. **Live uses the same interface.** A live adapter yields the same message record. When a recorded live stretch
   exists, replaying it through the historical path gives identical messages.
9. **No hidden numbers.** The only constants are exchange facts (the 17:00 ET halt, the 18:00 ET reopen), each
   declared in one place with its reason.

## Tech stack

Python 3.12 or later, `databento` for reading the tape, `numpy`. No new dependencies.

## Commands

```
python3 -m root.tape_stream check <trade day YYYYMMDD>      # cut, warm-up files, carry checks, counts; writes a receipt
python3 -m pytest tests/root/test_tape_stream.py            # the checks below, on the held tape
```

## Project structure

Proposed, pending Greg (see open questions): new code in the Markets repository under `root/` with tests under
`tests/root/`; receipts and the redesign documents stay in this folder in markets-data.

## Code style

Small pure functions for the calendar; one generator for the stream; refusal by exception with the reason in words.

```python
def trade_day_bounds(trade_day: date) -> tuple[int, int]:
    """Receive-time span of a trade day in UTC nanoseconds: 17:00 ET the evening before to 17:00 ET that date."""
    start = datetime.combine(trade_day - timedelta(days=1), HALT_ET, tzinfo=NEW_YORK)
    end = datetime.combine(trade_day, HALT_ET, tzinfo=NEW_YORK)
    return to_ns(start), to_ns(end)
```

## Testing strategy

Real tape only; no made-up messages, ever. Tests run on the October 2023 files already held and compare with the
committed receipts and trade lists (criterion 7). Calendar functions are tested on real dates either side of the
daylight-time changes. Each refusal in criteria 2, 3 and 6 has a test that makes it fire on real files (for example
by withholding one file).

## Boundaries

- Always: stop with the reason when a check fails; write a receipt for every run; declare every constant.
- Ask first: any change to the order-book rule; any paid download; any new dependency.
- Never: apply a snapshot after the first file; skip, merge or reorder a message; write a date, contract or UTC hour
  into the code; invent data.

## Open questions for Greg

1. Where the new ROOT code lives. Proposed: the Markets repository, new top-level folder `root/`. This session can
   only push to its own Markets branch.
2. A week with an exchange holiday, or one whose Sunday file we do not hold: stop and name what is missing (proposed),
   or run with ages marked as lower bounds from the earliest file held?
3. A contract roll inside a trade week: carry both contracts' books through the week (proposed), or only the one
   being traded most?
