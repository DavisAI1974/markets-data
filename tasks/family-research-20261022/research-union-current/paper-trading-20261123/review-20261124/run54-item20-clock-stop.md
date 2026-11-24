# Run 54: item 20, the 5.75-hour stop: every way the stop could fail to cancel, flatten, mark and report

The agent's own report, word for word, as it came back to the session (session_017eY1WPw7p6f6Tyx49EyYD4, 2026-11-24). It is a reading of code and documents. Nothing was run. What was done with each finding is in README.md beside this file and under the item's number in the platform checklist.

---

Review of checklist item 20 (the run stops itself at 5.75 hours, flattens every position, and marks each closing order "flattened at the 5.75-hour stop" as not trade data). Repository /home/user/paper-trading-platform, branch codex/strategy-trades-and-mbo-capture, tip e12bfde.

Everything below comes from reading the code. No file was changed and no code, test, workflow or network call ran. One shell command I tried would have started a Python interpreter just to find where Nautilus is installed. The permission system refused it, so nothing ran. That is why everything about Nautilus's own matching behaviour is marked "depends".

Nine findings are listed first, each with a smallest fix. Answers to your eight questions and the parts that already meet item 20 follow.

## Findings

**1. The live paper process can be killed before its final journal reaches markets-data**
- **Where:** `paper_platform/run_live.py:107-118`, `paper_platform/journal_publication.py:57-59, 99-109, 144-153`, `.github/workflows/live_ng_paper.yml:81-83`.
- **What the code does:**
  - At the deadline, run_live waits up to 45 s for the recorder, then gives the paper process 120 s. It then sends SIGTERM and waits 90 s before SIGKILL.
  - The paper process's SIGTERM handler only sets an event (`run.py:281-282`), so it keeps working until the kill.
  - Each clock-stop "paper order" and "fill" queues its own git commit and push. Each push can take up to 3 tries × 25 s plus 3 s of backoff.
  - `journal.finish()` waits for all of them with no time limit.
  - The later "Persist" step only publishes the capture, not `paper-trading/<run>`.
- **What item 20 requires:** the flattening orders, their fills and the receipt are the evidence the stop happened.
- **Failing case:** with many open trades or a slow push, SIGKILL lands while the flattening fills and the final receipt are still unpushed. The receipt exists only on the runner, and the phone notice of the stop may not go out.
- **Fix** (`run_live.py:115`), which still fits inside the 20-minute job margin:
  ```
              paper.wait(timeout=480)
  ```
- **Certainty:** the time limits are certain from the code. Whether a real run hits them depends on GitHub push latency and how many trades are open at the stop.

**2. The purchased-replay job has only a 10-minute margin after the clock**
- **Where:** `.github/workflows/purchased_mbo_paper.yml:48`.
- **What the code does:** `timeout-minutes: 355` gives 10 minutes after 345, minus the "Set up job" time that runs before the clock starts. After the stop, `run.py:389-402` waits with no limit for the same per-order git pushes as in finding 1, plus the final relay delivery.
- **What item 20 requires:** the stop has to finish and publish before GitHub kills the job.
- **Fix:**
  ```
      timeout-minutes: 365
  ```
- **Certainty:** depends on push and relay latency.

**3. The recorder-only workflow never starts the shared clock**
- **Where:** `.github/workflows/record_ng_mbo.yml:36-37`, `paper_platform/run_clock.py:13`, `paper_platform/record_mbo.py:207`.
- **What the code does:**
  - This workflow has no step that sets `PAPER_RUN_STARTED_NS`.
  - `run_start_ns()` falls back to the process's own start time.
  - The recorder's 5.75 hours therefore begin after checkout, two markets-data checkouts, pip install and the capture restore.
  - All of that comes out of the 20-minute margin of `timeout-minutes: 365`, and the after-stop "Persist" step still has to fit in what is left.
- **What item 20 requires:** one clock, started at job start.
- **Fix:** insert this as the first step, at line 37:
  ```
        - name: Start the 5.75-hour run clock
          run: python3 -c 'import time; print(f"PAPER_RUN_STARTED_NS={time.monotonic_ns()}")' >> "$GITHUB_ENV"
  ```
- **Certainty:** certain from the code that setup eats the margin. Whether the job is actually killed depends on how long setup takes.

**4. The flattening order is sent even when the market is shut, and is stamped with the last record's time**
- **Where:** `paper_platform/session.py:359-361`, `paper_platform/paper_execution.py:118-122, 154, 289`.
- **What the code does:**
  - The flattening order is sent whenever `liquidation_available` is True, which it always is for a clock stop.
  - It is a MarketOrder IOC (immediate-or-cancel) against the venue's resting L3 book.
  - Nothing checks whether the stop falls in the 5-6 pm Eastern halt or after the trade day.
  - The order and its fill are stamped with `last["raw"]["ts_recv"]`, which is the last processed record, not the time of the stop.
- **What item 20 and the house rules require:** a truthful flatten, and no trades in the 5-6 pm Eastern hour.
- **Failing case:**
  - A run that crosses 5 pm Eastern (for example, started around noon) stops at about 5:45 pm Eastern.
  - The cross fills against resting GTC orders left in the paper book during the halt, a fill no exchange could give.
  - If the feed went quiet before 5 pm, the fill is stamped at an earlier, in-session time.
- **Fix** (send nothing outside the trade day and report the open contracts instead). In `session.py:359-361`:
  ```
                      errors.extend(self.execution.flatten(self.last, reason, self.run,
                                                           executable=self.liquidation_available and self.last.get("in_session", False),
                                                           close_signals=close_signals))
  ```
  In `paper_execution.py:121`:
  ```
                            execution_event="liquidation unavailable: feed interrupted or market outside the trade day")
  ```
  - Limit of this fix: `in_session` comes from the last record's exchange time. A feed that goes quiet before 5 pm still reads as in session, and catching that needs a wall-clock check against `trade_day_bounds`.
  - Whether to hold the order or send it during the halt is Greg's call.
- **Certainty:** certain that no market-state check exists. Whether it fills depends on what is in the book at the halt and on Nautilus's MarketOrder handling.

**5. A failed cancel stops that trade's filled contracts from being closed**
- **Where:** `paper_platform/paper_execution.py:105-115`.
- **What the code does:** during a flatten, if a resting order fails to cancel or is still working, `submit` raises before it reads `held`. No close order is sent for that trade's filled contracts. The other trades still flatten, and the error is recorded.
- **What item 20 requires:** flatten every position. Once the stop has happened, no more market data reaches the venue, so an uncancelled resting order cannot fill afterwards.
- **Fix:**
  - Replace lines 112-115 with:
    ```
                if cancellation_error is not None and not event.get("administrative_flatten"):
                    raise cancellation_error
                if event.get("administrative_flatten") and (cancellation_error or self.active_orders.get(key)):
                    self.cancel_failures.append(dict(stage="liquidation", rule=self.rule, trade_id=key, order_id=order_id,
                                                     error=type(cancellation_error).__name__ if cancellation_error else "order still working"))
    ```
  - Add `self.cancel_failures = []` in `RuleVenue.__init__`.
  - In `flatten`, add `errors.extend(venue.cancel_failures)` after each venue's key loop.
  - The order that is still working continues to show in `remaining_working_orders`, and `native_flat` is False.
- **Certainty:** certain from the code that the close is skipped. Whether `cancel_order` can fail or leave an order working depends on Nautilus.

**6. Resting orders cancelled by the stop are journaled as trade data with no stop reason**
- **Where:** `paper_platform/paper_execution.py:105-107, 68, 77-80`.
- **What the code does:** `on_event` takes `administrative_reason` from the cancelled order's own record, which is None for a strategy order. The OrderCanceled "order status" event the stop causes is therefore written with `trade_data: true` and no 5.75-hour reason.
- **What item 20 requires:** item 20 names closing orders. This is the cancellation the same stop causes.
- **Fix** (`paper_execution.py:105`, inside the loop before the `try`):
  ```
                  if event.get("administrative_flatten"):
                      held_order, held_key, held_action, _ = self.orders[identifier]
                      self.orders[identifier] = (held_order, held_key, held_action, event["reason"])
  ```
  Fills already emitted for that order keep their original trade-data marking.
- **Certainty:** certain from the code. It assumes Nautilus sends OrderCanceled back through "ExecEngine.process" synchronously.

**7. The flattening order mixes fields from two different source records**
- **Where:** `paper_platform/paper_execution.py:287-291`, `paper_platform/engine.py:15-16, 72-80`.
- **What the code does:**
  - The flattening event starts from the engine's close signal, whose `position` and `exchange` come from `engine.last`, the last in-session tick.
  - `flatten` then replaces `received`, `reference`, `bid` and `ask` with values from `session.last`.
  - After 5 pm Eastern, or when the last record is a vendor snapshot, these are different records, so one paper order names two source records.
- **What item 20 requires:** every row must reconcile to one source record.
- **Fix** (add to the dict at line 289):
  ```
                               position=last.get("position_on_tape"), exchange=last["raw"]["ts_event"],
  ```
  `position_on_tape` is the field `inputs.py:75` reads into `position`.
- **Certainty:** certain from the code whenever the two records differ.

**8. Fill lines in the trades view carry no administrative mark**
- **Where:** `paper_platform/views.py:125-129`, `paper_platform/trades.py:61-64`.
- **What the code does:**
  - Under "Paper fills", each fill line prints its side, size and price with no administrative mark, even when `trade_data` is False.
  - `_timing` uses the clock-stop fill as the trade's "Time out · Final close fill" endpoint. That endpoint is labelled " · Administrative close" (`views.py:67`), and the order leg is labelled "Administrative close · excluded from trade data" (`views.py:107-108`).
- **What item 20 requires:** marked as not trade data.
- **Fix:**
  - At `views.py:129`:
    ```
                              f" · Order {e(fill['order_id'])}"
                              f"{' · Administrative close, excluded from trade data' if fill.get('trade_data') is False else ''}</small>")
    ```
  - If Greg wants no trade exit time taken from an administrative fill, change `trades.py:63` to:
    ```
            elif previous and entered is not None and fill["action"] in ("close", "exit") and fill.get("trade_data", True):
    ```
- **Certainty:** certain from the code. Whether the exit time should be taken from an administrative fill is Greg's call.

**9. The watchdog can be blocked behind the session lock in purchased replay**
- **Where:** `paper_platform/session.py:233-244`, `paper_platform/feed.py:121-125`.
- **What the code does:** `step()` holds `session.lock` while calling `next(self.stream)`. At each new UTC file in purchased replay, that call runs `compare_with_restatement` and `verify_queues` inside the generator. The watchdog's `s.stop(CLOCK_STOP)` waits for the lock until this finishes.
- **What item 20 requires:** stop at 5.75 hours.
- **Fix:** no small fix. This only matters if those checks take long.
- **Certainty:** depends on how long the book comparison takes, which cannot be read here.

## Answers to the questions

**1. Where the clock starts**
- **live_ng_paper.yml:43-44:** the first step writes `PAPER_RUN_STARTED_NS` from `time.monotonic_ns()`. `run_live.py:53-54` reads it and puts the same value back into the environment. The recorder (`record_mbo.py:207`) and the paper runner (`run.py:194`, `session.py:38`) inherit it, so recorder, preflight (`session.py:100` through `capture.py:290, 319`) and paper share one clock.
- **purchased_mbo_paper.yml:52-53:** same step, one process.
- **record_ng_mbo.yml:** the clock is not started by the workflow (finding 3).
- **Margins:** in the two paper workflows, the steps before the runner shorten the run, not the margin. Only GitHub's "Set up job" and the work after the stop use the margin: 20 minutes for live, 10 for purchased (findings 1 and 2).

**2. Clock checks and waits**
- **Every check:**
  - `session.py:40, 180-181, 187-188, 197, 249, 275`
  - `run.py:155` (pace_to_record), `243, 305` (watchdog), `332, 353`
  - `causal_gate.py:52, 89, 93`
  - `capture.py:290, 319`
  - `record_mbo.py:66, 172, 221, 227`
  - `run_live.py:56, 85, 90, 99`
- **Waits on the main thread with no clock check:**
  - `journal.wait_for_orders` (`journal_publication.py:70-77`, no timeout)
  - relay posts in `deliver_pending` (`run.py:106-126`, 8 s per post, with 409 recovery)
  - Neither holds the session lock. The watchdog thread (`run.py:287-307`) checks `due()` every 0.25 s and stops the session independently.
- **The live feed cannot block on an empty feed:** it is read with `poll=True`, so it returns `{"idle": True}` and never sleeps under the lock (`capture.py:239-246`).
- **Only lock-held delay found:** finding 9.

**3. What the clock stop cancels and closes**
- **Every rule venue is visited:** `flatten` goes through every venue and every key that has working orders or non-zero inventory (`paper_execution.py:282-284`).
- **Resting orders:** cancelled (`104-107`).
- **One close per trade:** one MarketOrder IOC (a crossing order) per (rule, trade), sized to `abs(inventory)` from actual fills (`116-117, 128, 154`).
- **Positions the engine marked unmonitored:** `engine.stop` moves them into `open` and closes them as administrative (`engine.py:364-367`). Their venue inventory is flattened by the same key loop.
- **Manager positions:** they sit in their own venues under `trade/manager` keys and are flattened there. This includes managers set to `on_parent_close: hold`.
- **Nothing is flattened twice:** `_record_stop_signals` only writes signals, `flatten` sends the orders, and `stop()` runs once under an RLock with a state guard (`session.py:344-347`).
- **Gaps:** findings 5 and 6.

**4. Following one order through to the journal**
- `flatten` (`paper_execution.py:287-291`) sets `reason` to `CLOCK_STOP`, `trade_data=False` and `administrative_flatten=True`.
- `RuleVenue.submit:155` takes the reason as `administrative_reason`.
- The "paper order" event (`158`) carries `reason` and `trade_data: false`.
- `on_event:77-80` writes `trade_data: false` and the `administrative_reason` on every "fill" and "order status" event. The "unfilled administrative remainder" event (`166-168`) carries the same.
- The engine's own close signal (`engine.py:69-80`) has the same reason and `trade_data: false`.
- **Exact phrase:** `run_clock.py:8` reads `CLOCK_STOP = "flattened at the 5.75-hour stop"`, the exact phrase.
- **Gaps:** findings 6, 7 and 8.

**5. Market closed or empty book at the stop**
- **Empty opposite side:**
  - What Nautilus does with the MarketOrder (reject it, or leave it with no event) depends on Nautilus.
  - Either way, the remaining contracts are emitted as "unfilled administrative remainder" (`paper_execution.py:166-168`).
  - `remaining_paper_inventory` and `remaining_working_orders` come from actual venue state (`session.py:362-370, 390-394`).
  - `native_flat` is False, and `run.py:378-379` turns that into a shutdown failure with a phone notice.
  - The receipt's `shutdown.errors` list stays empty in this case because only exceptions go into it. `native_flat` and `remaining_paper_inventory` carry the truth.
- **Halt or after the trade day:** finding 4.
- **Run status text:** the run's state and receipt `status` read "flattened at the 5.75-hour stop" even when `native_flat` is False (`session.py:349, 371, 378`). Only `native_flat` says whether it really flattened.

**6. A failure on one trade**
- A failure on one trade does not stop the others: each submit is wrapped in its own try (`paper_execution.py:292-298`), and errors go into the receipt under `shutdown.errors` (`session.py:370, 379`).
- Exception: the failed-cancel case in finding 5, where that trade's close is skipped.

**7. Other stops**
- Budget reached, end of input, failure, run stopped, "markets-data publication failed" and "capture: …" all go through the same `Session.stop` → `flatten`, using their own reason string, not the 5.75-hour phrase.
- A recorder stop with status "clock limit" maps to `CLOCK_STOP` (`session.py:314`).
- Capture failures outside the allowed list send no order and report the open contracts as "liquidation unavailable after feed interruption" (`paper_execution.py:118-122`).
- Leftover inventory is a shutdown failure only for the clock stop (`run.py:378`). Other stop reasons that leave contracts open exit without a failure.

**8. Trades view**
- **Shown with a label:** clock-stop closes stay inside each trade row. The order legs and the exit endpoint are labelled administrative.
- **Not labelled:** fill lines are not, and the exit time comes from the administrative fill (finding 8).
- **No totals:** there is no trade-data total or summary in `api.py`, which has no `trade_data`, `trade_rows` or fill references.

## Related observations outside item 20 (not proposed fixes)
- **Trade-day end into the halt:** at the first record at or after 5 pm Eastern, `engine.py:228-238` closes CL trades as trade data and submits them using the plan's usual close style into the halt (`session.py:212` → `record`). CX trades become unmonitored and stay open until the clock stop flattens them, inside the halt (see finding 4).
- **Fee model in the matching engine:** `paper_execution.py:52` builds each venue with `MakerTakerFeeModel()`. No commission figure is emitted anywhere I read, but a fee model sits inside the matching engine.
- **GitHub cancellation:** if timeout-minutes is hit, GitHub's cancel signal reaches the runner as "run stopped". The time GitHub allows after that signal before it kills the process is not readable here.

## What I read that already does what item 20 requires
- One monotonic clock is shared through the environment, and `run_start_ns` rejects a start time that is not on this runner's clock (`run_clock.py:11-16`).
- `due()` checks the clock before the budgets (`session.py:186-191`).
- The watchdog stops the run independently of the main thread (`run.py:287-307`).
- At the deadline the recorder stops with status "clock limit", including on SIGTERM after the deadline (`record_mbo.py:66-67, 172-173, 227`). That status maps to the same phrase in the paper runner.
- One close per filled trade, sized to inventory, crossing, across all venues, with no double flatten (question 3).
- The exact phrase, with `trade_data: false` and `administrative_reason`, on the paper order, the fills, the order-status events and the close signal (question 4).
- The receipt carries elapsed time, outstanding order tags, remaining contracts, errors and `native_flat` (`session.py:348, 362-386`).
- An incomplete clock-stop flatten turns into a shutdown failure with a phone notice (`run.py:378-379, 403-408`).

## Files read
- /home/user/paper-trading-platform/docs/platform/OWN_PLATFORM_WISHLIST_20261123.md (item 20, line 105, and its status, line 107)
- /home/user/paper-trading-platform/paper_platform/run_clock.py
- /home/user/paper-trading-platform/paper_platform/session.py
- /home/user/paper-trading-platform/paper_platform/paper_execution.py
- /home/user/paper-trading-platform/paper_platform/engine.py
- /home/user/paper-trading-platform/paper_platform/run.py
- /home/user/paper-trading-platform/paper_platform/run_live.py
- /home/user/paper-trading-platform/paper_platform/record_mbo.py
- /home/user/paper-trading-platform/paper_platform/capture.py
- /home/user/paper-trading-platform/paper_platform/journal_publication.py
- /home/user/paper-trading-platform/paper_platform/feed.py (lines 85-160)
- /home/user/paper-trading-platform/paper_platform/causal_gate.py
- /home/user/paper-trading-platform/paper_platform/trades.py
- /home/user/paper-trading-platform/paper_platform/views.py (lines 50-175)
- /home/user/paper-trading-platform/.github/workflows/live_ng_paper.yml
- /home/user/paper-trading-platform/.github/workflows/purchased_mbo_paper.yml
- /home/user/paper-trading-platform/.github/workflows/record_ng_mbo.yml
