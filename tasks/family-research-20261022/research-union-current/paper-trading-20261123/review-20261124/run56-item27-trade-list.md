# Run 56: items 27 and 16, the per-strategy trade list: every way a trade row could be wrong, incomplete or not what was asked

The agent's own report, word for word, as it came back to the session (session_017eY1WPw7p6f6Tyx49EyYD4, 2026-11-24). It is a reading of code and documents. Nothing was run. What was done with each finding is in README.md beside this file and under the item's number in the platform checklist.

---

Review of wishlist items 27 and 16 on branch codex/strategy-trades-and-mbo-capture, repository /home/user/paper-trading-platform.

I ran nothing: no code, tests, workflows, Python or network calls. Everything below comes from reading files with grep, sed and git show. The kgraph grounding check was not run because running anything on this branch is not allowed. I changed no files.

Item wording, from docs/platform/OWN_PLATFORM_WISHLIST_20261123.md:
- Item 16 (line 83): "NO AVERAGING, pooling, ranking or labels. Each trade is its own line." Status: "Built in draft".
- Item 27 (line 155): "Per strategy, a plain list of its trades: time in, time out, both quotes at each end, why it opened, why it closed. No summary number until Greg sets one." Its status text (line 157) says "Eastern tape time", "both observed MBO quotes", "the reason from the corresponding order", and that older fills without quotes show "unavailable".

## Findings

**F1. Each trade time shows a bare calendar date, not the trade day.** Certain from the code.
- **Where:** /home/user/paper-trading-platform/paper_platform/views.py:29-32 (`time_at`).
- **What it does:** prints `YYYY-MM-DD HH:MM:SS.nnnnnnnnn EST/EDT` from `datetime.fromtimestamp(..., America/New_York)`.
- **Failing case:** a fill at 19:30 ET Tuesday belongs to trade day Wednesday, but the row shows Tuesday's date. Nothing marks a time inside the 17:00-18:00 ET halt.
- **What the rule says:** the house rule is to never write a bare date and to name the trade day. The trade day appears only once per run, in the header (monitor.html:15). The "Recent runs" list (views.py:223) shows the date without the words "trade day".
- **Smallest fix:** at views.py:11 add `from root.calendar import label as calendar_label`, then replace lines 29-32 with:
```python
    def time_at(event):
        ns = int(event.get("fill_received_ns", event["received"]))
        seconds, nanos = divmod(ns, 1_000_000_000)
        moment = datetime.fromtimestamp(seconds, ZoneInfo("America/New_York"))
        try:
            name, named = calendar_label(ns)
            day = f"trade day {named:%Y-%m-%d}" if named else name
        except ValueError:
            day = "no trade day"
        return f"{day} · {moment:%H:%M:%S}.{nanos:09d} {moment:%Z} (Eastern clock date {moment:%Y-%m-%d})"
```
- **Note:** root/calendar.py:58 `label()` is documented as deciding by exchange time. The row only carries receive time, so a time within microseconds of 17:00 or 18:00 could be labelled differently than ROOT would label it.

**F2. A close at the end of the trade day is shown as an ordinary final close fill, and its time and quotes come from the first message after the trade day ended.** The code path is certain. Whether that message falls in the halt depends on the tape.
- **Where:** engine.py:229-238 calls `stop("trade day ended", administrative=False)`, so the close has `trade_data=True`. It sets `known_received_ns` to the receive time of the first message with ts_event at or after the halt. inputs.py:52 sets `end_of_day` as the halt bound from `trade_day_bounds`.
- session.py:285 calls `execution.market(message)` for that out-of-session message before `_apply` at session.py:301. So `book_quote` is that message's book, and the Nautilus book has applied it.
- paper_execution.py:100 sets `fill_received_ns` from `known_received_ns`, and :84 emits the fill with those quotes.
- **What the row shows:** "Time out · Final close fill" at 17:00 ET or later, with post-halt quotes. There is no mark that this is a halt-stretch time or that the trade day had ended. CL rules get this path. CX rules get "observation interrupted" instead (engine.py:360-361; see F8).
- **What item 27 and the rules say:** item 27 wants the time out and quotes at the end. The house rule keeps the 17:00-18:00 stretch apart from any trade day.
- **Smallest fix:** at trades.py:37 add `after_trade_day=event.get("known_received_ns") is not None,`. In views.py:67 add `+ (" · After trade-day halt" if point.get("after_trade_day") else "")` to `admin`.
- **Depends on behaviour not readable here:** paper_execution.py:99-101 then sets the venue clock back to the last in-session time with `self.clock.set_time(self.received)`, after market() had moved it to the out-of-session time. Whether Nautilus TestClock accepts going backwards, and what timestamp the fill then gets, is not readable here.

**F3. For a close triggered by a timer, the time out is the timer instant, but the quotes come from an earlier message, and the row cannot show that gap.** Certain from the code.
- **Where:** engine.py:189-196 builds a tick with `received=expiry` and the bid and ask of `self.last`. Session.py:271-272 runs it before the next message. paper_execution.py:99-100 sets `received` and `known_received_ns` to the expiry, while `book_quote` (:84) still holds the previous message, so its `quote_received_ns` is earlier.
- trades.py:29-37 `_endpoint` does not copy `quote_received_ns`, and views.py:68-69 shows only one time.
- **Failing case:** CL07/CL08 "exhaustion hump ended" shows the expiry time with quotes observed at an earlier receive time. Nothing says so.
- **Smallest fix:** at trades.py:37 add `quote_received=event.get("quote_received_ns"),`. At views.py:69, after `{prices(point, profile)}`, add `+ (f" · quotes seen {time_at(dict(received=point['quote_received']))}" if point.get("quote_received") not in (None, point["received"]) else "")`.

**F4. A signal whose order was never sent on a plan run looks like a plain decision trade.** Certain from the code.
- **Where:** session.py:180-182 `break`s out of the instruction loop when the event budget is reached. Nothing records the skipped instruction.
- trades.py:42-49: with no orders, fills, unsubmitted instructions or order states, `native` is False, so the row gets basis "decision". views.py:85-86 then labels it "Entry decision" with the signal's time and quotes.
- **Failing case:** at the run stop, engine.stop closes the trade administratively (engine.py:364-367). The row then reads "Exit decision · Administrative close". Nothing says that no order was sent.
- **Contributing cause:** session.py:196 `needed` counts two events per decision, while native execution emits a paper order, order statuses and fills. A batch can therefore pass the check at :201 and still hit the break at :180 or :209.
- **What item 27 needs:** the row must say what happened. A decision row where an order was expected is not the trade.
- **Smallest fix:** in trade_rows, after line 84 add:
```python
    native_run = db.execute("SELECT 1 FROM events WHERE run=? AND json_extract(body,'$.pricing')='native L3' LIMIT 1", (run,)).fetchone() is not None
```
  At line 138 call `row["timing"] = _timing(row, native_run)`. In `_timing` (line 40), take `native_run=False` and change line 42 to `native = (native_run or row["fills"] or ...)`. In views.py:79-80 add: `if not trade["orders"] and not trade["unsubmitted"]: no_entry = "No order sent"`.

**F5. A trade whose open signal was dropped mid-batch gets a row with only an administrative close.** Certain from the code.
- **Where:** session.py:209-211 stops before `record(decision)`, so the open signal is never written. The engine is not rolled back there, so engine.stop (engine.py:364-367) still closes that key. The close signal creates the row (trades.py:92-96).
- **What the row shows:** "Entry unavailable" or "Entry record unavailable" (views.py:86, :100) and "Exit decision · Administrative close" for a trade_id that has no open anywhere in the journal.
- **Smallest fix:** at session.py:209-211, call `self.engine.rollback_decision_batch(before)` before `self.stop("budget reached")`, so no close is recorded for an open that was never written. The opens already recorded in the batch are then also rolled back in the engine, so this needs Greg's call. The other option is to keep the row and label it, by adding at views.py:100 `"<p>Entry record unavailable: open signal not written before the run stopped</p>"` when `exit_event.get("trade_data") is False`.

**F6. When an administrative close is not sent, the instruction does not say it is administrative.** Certain from the code.
- **Where:** paper_execution.py:119-121 and :124-126 emit `submitted=False` with `trade_data=False` (from the flatten event, :287-291). views.py:72-76 (summary line) and :112-114 ("Exit instruction · No order sent") do not read `trade_data`.
- **Failing case:** a posted open that is still working at the run stop. The row shows "Time out · Final close fill · No exit fill recorded · Instruction · <stop reason>", with no administrative label.
- **Smallest fix:** at views.py:74-75 use `detail = f"<small>{'Administrative · ' if instruction.get('trade_data') is False else ''}Instruction · {e(reason)}</small>"`. At views.py:113 use `label = ("Entry instruction" if attempt["action"] == "open" else "Administrative close instruction" if attempt.get("trade_data") is False else "Exit instruction")`.

**F7. A rejected open is shown only as "No entry fill recorded" on the summary line.** Certain from the code.
- **Where:** paper_execution.py:139-143 emits `submitted=False` with reason "No bid for post order" (or ask) and `decision_reason`. On the summary line (views.py:88, :93) `entry_intent` is the entry signal, so it shows "No entry fill recorded · Instruction · <signal reason>". The words "No order sent" and "No bid for post order" appear only in the collapsed details (views.py:112-114, :50-53).
- **Smallest fix:** at views.py:79-80 add: `if any(a["action"] == "open" for a in attempts) and not trade["fills"]: no_entry = "No order sent"`. Pass `next(a for a in attempts if a["action"] == "open")` as `entry_intent` so its outcome text is shown.

**F8. A manager row whose own order never existed borrows its parent's entry as "Entry decision".** The code path is certain. Whether it happens with the current plan depends on how the plan's entry_rules line up with the engine (they match in ngx3-12be6ea6...json lines 270-294 and 306-330).
- **Where:** trades.py:118-135 runs `_parent_entry` when a manager row has an "exit" signal and no entry. It attaches the parent's paper order and the parent order's last state.
- trades.py:42-43: the parent's state has `rule` set to the parent, so `native` is False and the basis is "decision". The parent's decision time and quotes then appear as the manager's time in (views.py:66 adds " · <parent>").
- **Failing case:** a manager follow-open skipped by the break at session.py:180-182, followed by the engine's own manager "exit" (engine.py:108-139). paper_execution.py:116-127 then emits nothing because there are no contracts and no working order. The row shows an entry and an exit for a manager that never held a contract.
- **Smallest fix:** at trades.py:121, before calling `_parent_entry`, skip the fallback when the run has native orders: `if native_run: continue`, using `native_run` from F4. Then add at views.py:99-100 `"<p>No entry order for this manager</p>"`.

**F9. The trades API returns raw integer nanoseconds with no Eastern time and no trade day.** Depends on the consumer.
- **Where:** relay.py:166 returns the `trade_rows` dicts as they are. Unlike api.py:17-25 (`wire`), nanosecond ints above 2^53 are not converted to strings, so a browser `JSON.parse` loses precision.
- The phone page is rendered on the server and is not affected.
- **Smallest fix:** at relay.py:166 use `return wire(trade_rows(db, state.get("run"), rule))` with `from .api import wire`.

**F10. On an "Earlier events" page, the trade list is built from events after that page's cut-off.** Certain from the code. Whether this is intended is Greg's call.
- **Where:** relay.py:341 calls `trade_rows(db, state.get("run"), rule)` with no `through`, while the events are cut at `before` (relay.py:340). page() still renders the trade section when `archived_page` is true (views.py:296-301).
- **Smallest fix, if the list should match the page:** at relay.py:341 use `trades = trade_rows(db, state.get("run"), rule, through=None if before is None else before - 1)`.

**F11. A silent drop with no row.** Certain from the code.
- **Where:** session.py:180-182 breaks out of the loop between a parent's instruction and its manager follow instructions. The skipped manager follow-open leaves no event. At the stop, flatten (paper_execution.py:283-284) finds no key for it.
- **Result:** no row, and no record that the follow was skipped. Under item 16/27 this is a dropped trade line, not a wrong one.
- **Smallest fix:** at session.py:180-182, before `break`, emit one `self.write("order status", **instruction, order_id=tag, pricing="native L3", submitted=False, execution_event="event budget reached before order")` for that instruction and each one after it. This goes past the event budget by the number of skipped instructions, which is Greg's call.

**F12. Manager closes are all labelled "Manager exit", whatever caused them.** Certain from the code.
- **Where:** views.py:110 uses "Manager exit" for every close order with `management_only`. That covers the manager's own "exit" and a close caused by its parent closing (paper_execution.py:264-266 sets `management_only=True` on both). Only the reason prefix "<parent>: " tells them apart.
- **Smallest fix:** at views.py:110 use `label = ("Manager exit" if order.get("signal_action") == "exit" else "Close after parent close") if order.get("management_only") else "Exit order"`.

## The four walks (from the code; native plan run)

**Walk a. Crossing open fills at once, then the trade closes on its own rule.**
- Open signal at message m: engine.py:57-67, written at session.py:170.
- Instruction: paper_execution.py:255. Paper order (:158-160) with the decision bid and ask, `order_id=<run>-<seq>`, a MarketOrder IOC (style "cross", :154). It fills inside `process_order` (:165).
- The fill (:84) has `bid/ask = book_quote` of message m, which is the source book after m was applied (feed.py:80-81). That equals the decision quotes because it is the same message. `fill_received_ns` is m's receive time.
- The close at message n follows the same path with action "close".
- `_timing` (trades.py:53-64):
  - Time in = the open fill: m's time, m's bid and ask, reason = open order reason = signal reason.
  - Time out = the close fill that brings the position to 0: n's time, n's bid and ask, reason = close signal reason.
- Labels: "Time in · First fill" and "Time out · Final close fill" (views.py:79). Times are as in F1.
- If the book side is empty and the order does not fill, the row shows "No entry fill recorded". The later close emits nothing (paper_execution.py:123-127 with `working` empty). How Nautilus rejects or cancels is not readable here.

**Walk b. Posted open fills in two parts on later messages; a crossing close also fills in two parts.**
- This cannot happen under the current plan, because every rule has `"contracts": 1` (ngx3-12be6ea6...json). It is walked here from the code for a size of 2.
- Paper order at m (post-only GTC limit, :151-152) with m's decision quotes. Accepted, then an "order status" event (:90).
- Fills at p1 and p2 come through `market()` (:233-244). Each fill carries the source book after p1 or p2 and that message's receive time.
- `_timing`: time in = the p1 fill (p1 time and quotes), reason = open order reason. Position after p2 = 2.
- Close at n: there are no working orders to cancel, so a MarketOrder sells 2. Two fills at n. After the first, the position is 1 and `exited` stays None (:61-62). After the second, the position is 0 and time out = the second fill: n's time and n's quotes (the same `book_quote` for both parts), reason = close reason.
- Both partial fills are listed in the details (views.py:125-129) with the fill price, liquidity, time and both quotes.
- If only p1 had filled before the close, the open order is cancelled (an "order status" event with action open, CANCELED) and the close sells 1.

**Walk c. Posted open that never fills, cancelled when the close comes.**
- Paper order at m, accepted. At close n, `submit` cancels it (paper_execution.py:104-107). on_event emits an "order status" event with action "open" and status CANCELED.
- Position is 0 and `working` is non-empty, so an "order status" event with `submitted=False` and "no filled contracts to close" is emitted (:123-126). No close paper order is written.
- `_timing`: basis "fill", no fills, `open_contracts=0`.
- Summary line: "Time in · First fill · No entry fill recorded · Instruction · <open reason>" and "Time out · Final close fill · No exit fill recorded · Instruction · <close reason>" (exit_intent is the unsubmitted event, views.py:89-91).
- Details: the "Entry order" leg with CANCELED and 0 remaining, "Exit instruction · No order sent · no filled contracts to close", "Exit signal", "No exit order recorded", and "Paper fills · No execution recorded".
- The cancellation is visible only in the details. If this happens at the run stop, see F6.

**Walk d1. A manager follows its parent's open, then exits on its own "exit" signal.**
- Parent open signal for parent P with trade id K. `instructions` (paper_execution.py:256-266) yields, for each manager M on the same side, `trade_id="K/M"`, `entry_rule=P`, `source_trade_id=K`, `management_only=True` and `reason="P: <reason>"`. No "signal" event is written for M's open.
- M's paper order creates row (M, "K/M") (trades.py:92-100). The open uses "cross" (plan :296-298), so it fills at the parent's message.
- Time in = parent's message time and quotes, reason "P: <reason>". This is the parent's open, not M's own confirmation. Details show "Entry signal from P · K" (views.py:101-103).
- Later the engine emits M's "exit" signal (engine.py:126-139: same trade id "K/M", reason = first line of M's specification). The instruction is rewritten to action "close" with `signal_action="exit"` (paper_execution.py:250-253).
- Time out = that close fill: its time, its source-book quotes, reason = M's specification line. Labelled "Manager exit" (views.py:110).
- A later parent close then emits nothing for M (:116-127).

**Walk d2. A manager closed because its parent closed.**
- Parent close at n. With `on_parent_close` "exit" (all six managers in the plan), `instructions` yields a close for "K/M" with reason "P: <close reason>".
- Time out = that fill: n's time and quotes, reason "P: <close reason>". Also labelled "Manager exit" (F12).
- If the parent close is the run-stop close, the close for M is held in `close_signals` (session.py:340-342). flatten replaces the reason with the stop reason (paper_execution.py:287-291), sets `trade_data=False`, and the row shows "Time out ... · Administrative close" with the stop reason.

## Answers to questions 2-8 not covered above

**Q2, quotes on a fill row.**
- The bid and ask are the source book after the fill's message was applied (paper_execution.py:232; feed.py:80-81). They are not the decision quotes and not from a later message.
- For a posted order that fills later, the quotes are from the message that filled it.
- Exceptions: F2 (first message after the trade day) and F3 (timer instant with the earlier message's quotes).
- No mid price, spread, difference, return or P&L appears in trades.py, views.py, relay.py or monitor.html (grep for mid, pnl, profit, return, spread, sum, count, sorted found none in these).
- The fill price and MAKER/TAKER are shown next to both quotes in the per-fill list (views.py:126-128), not in their place. The summary lines show only the bid and ask (views.py:69).
- paper_execution.py:52 builds the matcher with `MakerTakerFeeModel()`. No commission field is emitted (:84-88) or shown.

**Q3, times.**
- Fill rows use `fill_received_ns`, the tape receive time (trades.py:32; views.py:30). Decision rows use the signal's `received`. Times are in Eastern with nanoseconds. The trade day is not named (F1).
- A trade still open shows "N contracts still open" (views.py:81-83) or, on decision basis, "No exit decision recorded".
- Run-stop closes go through flatten with `trade_data=False`. A fill exists, so the row shows "Administrative close" (views.py:67) and the detail leg shows "Administrative close · excluded from trade data" (:107-108). That close still sits in the "Time out" slot. When no administrative order was sent, there is no label (F6).

**Q4, reasons.**
- Fill reasons come from the paper order with the fill's `order_id` (trades.py:57-58). They fall back to `administrative_reason`, then "Reason unavailable".
- Follow-open reason: "P: <reason>". Administrative close reason: the stop reason (paper_execution.py:289 and :155).
- I found no fill row whose reason comes from a different event. Exceptions are F8 (parent's reason used for a manager with no order) and F5 (no entry reason).

**Q5, one row per trade.**
- The key is (rule, trade_id) (trades.py:89). The strategy filter adds only `rule=?`, so filtered rows equal the full-run rows for that rule.
- Parent lookups ignore the filter, and parent rows are referenced, not merged.
- Order: by the sequence of each row's first event, newest first (trades.py:136). The stream inserts new rows at the top and replaces updated rows in place (monitor.html:56-66), so the order is the same.
- No sums, counts, rankings or summary figures in trade_rows, trade_card or monitor.html. The only `len()` calls are pagination limits (relay.py:249, :313).

**Q6, signals that never became orders.**
- Run without a plan: a "paper order" with `pricing` "open" and a decision row (session.py:175-178).
- Budget stop: F4, F5, F11.
- `submitted=False`: F6, F7, and walk c.
- "No bid for post order": F7.

**Q7, older events.**
- Fills from before commit 2986b3c have no bid or ask, so they show "unavailable" (views.py:20). They are never filled in from decision quotes.
- Their `received` was set by the old `market()` to the fill message's time, as `git show 2986b3c` shows `venue.received = received` unchanged. So the time in and time out of old posted fills are message times.
- A one-sided book (a bid or ask of None) also shows "unavailable", with the same word.

**Q8, `through` and paging.**
- In trade_rows, `through` bounds the main query (trades.py:78-80) and the parent-state lookup (:126-131). `_parent_entry` is bounded by the exit event's sequence, which is at or before `through` (:13, :17).
- The stream builds each changed row with `through=seq` (relay.py:222-225).
- The plain dashboard reads the event list and the trade list in the same transaction (relay.py:335-341).
- Exception: F10 (archived page).
- A manager row that uses the parent fallback is not re-rendered when only the parent's order status changes (relay.py:212-219 matches on the row's own rule and trade_id).

## Read and found doing what the items require
- One row per (rule, trade_id) in both the full run and the strategy filter, with no sums, counts, ranks or summary figures: trades.py:85-139, views.py, monitor.html.
- Both quotes at each end, taken from the source book at the fill's message: paper_execution.py:232-237 and :84.
- Time out set only when the position returns to zero, so partial exits leave the trade open: trades.py:61-64.
- Fill reasons from the fill's own order; follow-open reason "P: <reason>"; stop reason on administrative closes: trades.py:57-58, paper_execution.py:266, :289.
- Administrative fills labelled when a fill exists: views.py:67, :107-108.
- Old fills without quotes show "unavailable", never filled in: views.py:20.
- `through` respected in the stream: trades.py:78-80, :126-131.
- No mid price, return or trade cost in the trade row.
- Every partial fill listed individually: views.py:125-129.

## Speculation (outside the trade row)
cx_observations.py:59 gives each "print observed" event `price_response` "with" or "against", shown on event cards (views.py:176). It is not part of the trade row, since trade_rows filters those events out at trades.py:81-83. Whether it counts as a "label" under item 16 is Greg's reading.

## Files read
All under /home/user/paper-trading-platform:
- paper_platform/trades.py
- paper_platform/views.py
- paper_platform/relay.py
- paper_platform/api.py
- paper_platform/monitor.html
- paper_platform/paper_execution.py
- paper_platform/session.py
- paper_platform/engine.py
- paper_platform/rulebook.py:74-95
- paper_platform/inputs.py:50-99
- paper_platform/feed.py:46-96
- paper_platform/cx_observations.py:55-89
- root/calendar.py:1-70
- paper_platform/execution_plans/ngx3-12be6ea6e40347def5f574b1c2f36093bba99200.json
- docs/platform/OWN_PLATFORM_WISHLIST_20261123.md:80-90 and :150-157
- `git show 2986b3c`
