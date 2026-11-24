# Run 63: items 12, 16 and 18: where replay departs from live, what the comparison checks, and every not-scored mark

The agent's own report, word for word, as it came back to the session (session_017eY1WPw7p6f6Tyx49EyYD4, 2026-11-24). It is a reading of code and documents. Nothing was run. What was done with each finding is in README.md beside this file and under the item's number in the platform checklist.

---

Review of items 12, 16 and 18 in /home/user/paper-trading-platform, branch codex/strategy-trades-and-mbo-capture at 37c5e91. This comes from reading only. I ran no code, test, workflow or network call. One command I put together had `python3 -c 1` in it by mistake. The permission check refused it before it ran, so no interpreter started. The notes I appended as I went are in /tmp/claude-0/-home-user/f6fc58bd-1d38-5c78-9832-91292fa09200/scratchpad/review2/items-12-16-18.md (with a corrections section at the end).

Files read: both workflows plus .github/actions/markets-data/action.yml, run.py, session.py, capture.py, capture_backup.py, feed.py, causal_gate.py, run_clock.py, replay_comparison.py, journal_publication.py, engine.py, rulebook.py, claude_rules.py, unsided_print_rules.py, cx_observations.py, inputs.py, paper_execution.py, trades.py, views.py, parts of relay.py, the rule files CL16, CX01 and CX07, the aggressor terms in the CX rules, markets/nymex-ng.json, root/calcs/quote_runs.py, and the `launch` call in run_live.py.

## Findings

**1. [12] A clock stop can leave the live run without the decisions on its last frame; the replay makes them.** session.py:296-297 and :214-217.
- **What the code does:** `step` sets `self.cursor` and `self.last` to the message, and only then does `_apply` check the deadline. If the deadline has passed, it rolls the decisions back and stops. The receipt's `delivered` (cursor+1) still counts that frame.
- **What happens on replay:** `recorded_run` (capture.py:202-205) hands the same frame to a replay whose own deadline is far off. The replay records every decision and paper order for that frame, then stops on `recorded_stop`.
- **What the item requires:** the same code and the same decisions on the same messages.
- **Smallest fix:**
  - session.py, after :92: `self.decisions_withheld_cursor = None`
  - session.py:214-217:
    ```python
    if time.monotonic() >= self.deadline:
        self.engine.rollback_decision_batch(before)
        if not timer:
            self.decisions_withheld_cursor = self.cursor
        self.stop(self.clock_stop)
        return False
    ```
  - Receipt dict, session.py:396-402: add `decisions_withheld_cursor=self.decisions_withheld_cursor,`
  - capture.py, after :203: `message["withhold_decisions"] = message["cursor"] == receipt.get("decisions_withheld_cursor")`
  - session.py, between :319 and :320:
    ```python
    if message.get("withhold_decisions"):
        before = self.engine.begin_decision_batch()
        self.engine.tick(message)
        self.engine.rollback_decision_batch(before)
        return message
    ```
  - replay_comparison.py:106: add `"decisions_withheld_cursor"` to the tuple.
- **Notes on the fix:** the rollback restores only `open`, `unmonitored` and `pending` (engine.py:39-45). The replay goes through the same partial restore, so its stop rows also use `self.last` = that frame. Receipt replay runs the original commit (purchased_mbo_paper.yml:89-101), so this fix covers only live runs made after it lands.
- **Changes:** a journal row and receipt field in live. On replay it removes extra orders.
- **Certainty:** certain from the code. Whether it happens depends on the wall clock crossing the deadline between session.py:292 and :214.

**2. [12] A clock stop inside `record` can skip some of a decision's paper orders in live only.** session.py:196-199.
- **What the code does:** the instruction loop stops on `time.monotonic() >= self.deadline` after the signal row is written. Skipped instructions leave no row. The replay submits all of them.
- **What the item requires:** the same paper orders on the same messages.
- **Fix:**
  ```python
  if self.state == "active" and self.events >= self.output_budget:
      break
  ```
  The deadline is still enforced at :214, :230, :256, :266 and :292.
- **Changes:** an order.
- **Certainty:** certain from the code. Whether it happens depends on the wall clock. It reaches only live runs made after the fix.

**3. [12] A replay's recorded constants do not match a live run that stopped before 5 pm, and nothing compares them.** session.py:42-43 and :151-156.
- **What the code does:** a replay always writes `stop_seconds=20700.0`, `clock_stop_seconds=20700.0` and `clock_stop=CLOCK_STOP` (run_clock.py:10-11). The live receipt may carry HALT_STOP (run_clock.py:13) and a shorter `clock_stop_seconds`.
- **Stop reason and endpoint:** the replay's final status is the live receipt's status (session.py:282, capture.py:208). It ends on the same frame (capture.py:202), apart from finding 1 and findings 4 and 6 below.
- **Nothing compares the constants:** replay_comparison.py:76 and :105-119 leave `constants` out.
- **Fix (receipt field only):**
  - session.py, after :160:
    ```python
    if replay_receipt is not None:
        self.initial["original_constants"] = replay_receipt["constants"]
    ```
  - replay_comparison.py, after :78:
    ```python
    if replay.get("original_constants") != live["constants"]:
        raise ValueError("replay does not carry the original constants")
    ```
- **Certainty:** certain from the code.

**4. [12] A replay can run on smaller budgets than the live run.** run.py:254-255.
- **What the code does:** each budget is `min(workflow input, receipt)`. A smaller input makes the replay stop with "budget reached" before the live endpoint.
- **Fix:**
  ```python
  if (args.message_budget < receipt["constants"]["message_budget"]
          or args.event_budget < receipt["constants"]["event_budget"]):
      raise ValueError("receipt replay needs at least the original budgets")
  args.message_budget = receipt["constants"]["message_budget"]
  args.event_budget = receipt["constants"]["event_budget"]
  ```
- **Changes:** only stops a replay from starting with smaller budgets. No order.
- **Certainty:** certain from the code.

**5. [12] The comparison reports only the first difference, matched by position.** replay_comparison.py:84-103 and :123-130.
- **What the code does:** it pairs the two journals by position (`zip_longest` ordinal). After the first difference it only counts. One extra row in either journal shifts every later pair.
- **Figures it prints:** `live_decisions`, `replay_decisions`, `live_execution_events` and `replay_execution_events` are plain counts. There is no rate, match count or pooled figure.
- **What the task asks:** each difference on its own line.
- **Fix:**
  - Drop :88-89.
  - Replace :103 with `differences.append(dict(decision=ordinal, locations=locations, differing_fields=fields))`, with `differences = []` before the loop.
  - Return `differences=differences`.
  - In `main`, add `for d in report["differences"]: print(json.dumps(d, separators=(",", ":")))`.
- **Limit of the fix:** with positional pairing, the lines after an inserted row are a cascade. Pairing by (rule, mapped trade id, action, reference) is a separate design choice.
- **Changes:** the comparison's output only.
- **Certainty:** certain from the code.

**6. [12] A purchased-archive replay is paced at tape speed, so it covers only the first part of the trade day.** run.py:343-353 with run_clock.py:10.
- **What the code does:** pacing starts at the first in-session record. The 5.75-hour wall limit means the replay reaches at most about 6 pm to 11:45 pm Eastern of the trade day, less the preflight time. The captured path is not paced, for live and replay alike (run.py:337-340).
- **What the item requires:** a stored trade day's tape, run through.
- **Fix:**
  - Add `p.add_argument("--unpaced", action="store_true")`.
  - Change :347 and :352 to `if not args.unpaced and ...`.
  - Due timers still fire before the next message in `step` (session.py:288), in the same order.
- **Changes:** wall timing only. No decision changes. Whether to do it is Greg's call.
- **Certainty:** certain from the code.

**7. [12] The paper-execution comparison checks a fixed list of fields and ignores everything else.** replay_comparison.py:42-46.
- **Set aside without comparison:** `submitted_ns`, `quote_received_ns`, `known_received_ns`, `signal_sequence`, `fill_id`, `pricing`, `decision_reason`, `signal_action`, `management_only`, `administrative_flatten`, and the signal fields carried onto orders (`entry`, `conditions`, `trigger`, `arm_reference`, `known_at`).
- **Strategy-decision pass:** it sets aside exactly `run`, `recorded_ns` and `sequence`, and maps `trade_id` / `source_trade_id` to ordinals (:55-61). That fits the item: the trade id is `uuid5(run_id, ...)` (engine.py:52), and the order id is `{run}-{sequence}`.
- **Not compared at all:** receipt `shutdown` (`errors`, `native_flat`, `remaining_working_orders`) and `remaining_paper_inventory`.
- **Fix:**
  ```python
  signal = {k: v for k, v in event.items() if k not in ("run", "recorded_ns", "sequence", "order_id", "working_order_ids", "fill_id")}
  ```
  Keep the order-ordinal mapping. Also add:
  ```python
  if {k: v for k, v in live["shutdown"].items() if k != "elapsed_ns_at_stop"} != {k: v for k, v in replay["shutdown"].items() if k != "elapsed_ns_at_stop"}: window_differences.append("shutdown")
  if live["remaining_paper_inventory"] != replay["remaining_paper_inventory"]: window_differences.append("remaining paper inventory")
  ```
  The inventory keys are trade ids that contain the run id, so they need the same ordinal mapping before comparing.
- **Changes:** comparison only.
- **Certainty:** certain from the code.

**8. [12] Order-status reasons are compared as text.** paper_execution.py:90.
- **What the code does:** `reason=str(event.reason)` is among the compared fields. If a Nautilus reason string contains the ClientOrderId, it differs by construction, because the order id contains the run id.
- **Fix:** none unless that is seen. If it is, replace the run id in `reason` with the ordinal mapping in replay_comparison.py:47.
- **Certainty:** depends on Nautilus's message text, which is not readable here.
- **Related, also not readable here:** the `UUID4()` values at paper_execution.py:136 and :166 are not passed to `emit` (read). Whether `FillModel()` and the engine's trade ids are deterministic is Nautilus behaviour.

**9. [12] The replay restores the newest capture checkpoint, not one fixed by the live receipt.** purchased_mbo_paper.yml:104-108 and capture_backup.py:37-41.
- **What the code does:** it takes the latest checkpoint on `mbo-captures/nymex-ng/<week>/live`. run_live does not pass `--capture-commit`, so the live receipt has no checkpoint commit. Before replay, capture.py:195-198 checks only the hash of the final frame. The earlier frames are checked only afterwards, through `capture_frame_hashes_sha256` (replay_comparison.py:113-116).
- **Fix:** after capture.py:198:
  ```python
  frames = hashlib.sha256()
  for (body,) in db.execute("SELECT body FROM frames WHERE position < ? ORDER BY position", (delivered,)):
      frames.update(hashlib.sha256(body).digest())
  if receipt.get("capture_frame_hashes_sha256") not in (None, frames.hexdigest()):
      raise ValueError("checkpoint frames differ from the recorded run")
  ```
  This matches session.py:301.
- **Changes:** no order. The replay refuses earlier instead of being caught afterwards.
- **Certainty:** certain from the code.

**10. [12] The phone notice reads the same for a replay as for a live run, and the comparison workflow may lack Python.**
- **Phone and relay:** run.py:28-34, :313 and :387 send "NG paper run ..." for a replay too. The relay and the run branch are the same as for live.
  - Fix: pass `activity="paper replay" if args.replay_capture or not args.capture else "paper run"` to both `notify` calls.
  - Changes: phone/page only. Certain from the code.
- **Snapshot-failure replay:** a replay of a live run whose status was "markets-data snapshot failed" goes through run.py:398 and exits with an error even when it matches the live run. Exit code only.
- **Python in the comparison workflow:** compare_recorded_replay.yml:46 calls `python` with no setup-python step.
  - Fix: insert before :45
    ```yaml
    - uses: actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065
      with:
        python-version: '3.13'
    ```
  - Depends on the runner image.

**11. [18] A CX manager's "not scored" row is not marked out of trade data.** engine.py:120-140.
- **What the code does:** the row has no `trade_data=False`. session.py:186 skips it (`management_only`), so no exposure row is written. After the reset (engine.py:111-112, :97-101) the manager can act again on the same trade id `key/name`.
- **What the item requires:** the trade is marked and stays out of scoring.
- **Fix:** at engine.py:137, add `**({"trade_data": False} if missing else {}),`
- **Changes:** a journal field.
- **Certainty:** certain from the code. Whether a manager may act again after "not scored" is Greg's call.

**12. [18] A CX entry that cannot be checked writes a "not scored" row with no trade id and no `trade_data=False`.** engine.py:345-354.
- **What the code does:** because the trade id is None, trades.py:71 leaves the row off every trade row. One row is written for each print where every other condition holds and one value is None. Each row spends event budget.
- **Conflict with CX02's rule text:** "a print can have an unknown aggressor. Neither establishes this particular selling sequence." The code instead writes "not scored: the feed lacks q.aggressor". `q.aggressor` appears in CX02-04, CX07-08, CX11-15.
- **Fix A, keep the row:** pass `trade_data=False` to the `self.event(...)` at :347.
- **Fix B, read an unknown aggressor as "condition not met":** in rulebook.py:41, before `missing.extend`:
  ```python
  if "aggressor" in (left.split(".")[-1], right.split(".")[-1]):
      outcomes.append(False)
      continue
  ```
- **Changes:** journal rows only; neither reading places an order. Which reading applies is Greg's call.
- **Certainty:** certain from the code. How many rows it writes depends on the tape.

**13. [18] An empty dipole or exhaustion window is reported as the feed lacking something, and CX and CL read it differently.**
- **What the code does:** when the 20-second window has no sided print, `Flow.value` is None (inputs.py:21). For an open CX trade, `management` with `require_complete` (rulebook.py:77-80) writes "not scored: the feed lacks t.exhaustion" and ends the observation. For CL07 and CL08, the same empty window reads as zero (`sign(None)=0`, claude_rules.py:9-10) and produces a scored close (engine.py:185-209). CL05, CL10 and CL11 also read None as zero when arming.
- **Wording:** a lacking field is named as a term (q.aggressor, p.dipole, t.exhaustion). For CL16/17 it is "bid", "ask" or "bid, ask". The feed lacks nothing when a window is empty.
- **Fix for the wording (journal field):** at engine.py:122, :292 and :350, use
  ```python
  "not scored: " + "; ".join(x for x in (
      ("the feed lacks " + ", ".join(f)) if (f := sorted({m for m in missing if m.split(".")[-1] not in ("dipole", "exhaustion")})) else "",
      ("no sided print in the window of " + ", ".join(w)) if (w := sorted({m for m in missing if m.split(".")[-1] in ("dipole", "exhaustion")})) else "") if x)
  ```
- **Open question:** whether CX and CL should treat an empty window the same way is Greg's call.
- **Certainty:** certain from the code. How often it happens depends on the tape.

**14. [18] Open CL01-CL15 trades get no mark when one side of the book is empty, and can then close as a scored exit.** inputs.py:77-80 with engine.py:264-271.
- **What the code does:** an empty side resets `QuoteRuns`, but `ClaudeRules.runs` keeps the old run. No row is written. When the side returns, the next move starts a new run, `active()` turns false, and the trade closes with "written close condition reached: CLxx" and `trade_data` True.
- **Fix:** replace engine.py:265-271 with
  ```python
  reads_unsided = rule.get("reads_unsided_prints", False)
  missing = [name for name in ("bid", "ask") if t[name] is None]
  if missing and (t["trade"] or not reads_unsided):
      reason = "not scored: the feed lacks " + ", ".join(missing)
      events.append(self.interrupt_trade(key, reason, t, missing=True))
      continue
  ```
- **Changes:** an order (no scored close; an administrative close at the stop instead) and a journal row.
- **Certainty:** certain from the code. Whether it occurs depends on the tape; quote_runs.py:25 says none occurs on the four trade days.

**15. [18] On a print with no side, CL01-CL15 neither open nor close, as their written rule 5 says; no row records a dropped entry.** engine.py:273-275 and :322-323.
- **What the code does:** this matches the rule as written (the CL16.json spec quotes it). The only open question: no row is written for a confirmed entry that is dropped, and its key stays in `emitted` (claude_rules.py:302), so it cannot confirm later.
- **Fix, only if Greg wants a row:** at :322-323,
  ```python
  if t["trade"] and t["aggressor"] is None:
      events.extend(self.event(s["rule"], "not opened", "print with no side (rule 5)", t, None, side=s["side"], trigger=s["identity"], trade_data=False) for s in signals if s["rule"] in self.rules)
      signals = []
  ```
- **Changes:** journal only.
- **Certainty:** certain from the code.

**16. [18] When a paper order has no quote to price from, its row uses different wording and the research trade stays marked as trade data.** paper_execution.py:143-146.
- **What the code does:** it writes "No bid|ask for post|cross_limit order" with `submitted=False`. The research signal keeps `trade_data` True.
- **Fix, if Greg ties this to item 18:** `reason=f"not sent: the feed lacks {field} for {style} order"`
- **Changes:** journal/page.
- **Certainty:** certain from the code.

**17. [18] The CL16/CL17 trade row on the phone page shows only the reason text.** views.py:140-141.
- **What the journal has:** everything the status says. The row is written by engine.py:266-270 through `interrupt_trade` (:156-169). It carries `trade_id`, `reference` = [sha, record_index] of the source print, `bid`/`ask` (None on the missing side), the entry quote, side, `trade_data=False` and "not scored: the feed lacks bid|ask|bid, ask". The print's price is not on it.
- **What the page lacks:** the time and source reference, and any mark in the summary line.
- **Fix:**
  ```python
  if trade["observation"]:
      observation = trade["observation"]
      fields.append(f"<p>{e(observation['reason'])} · {time_at(observation)}</p>"
                    f"<small>Source print · {e(observation.get('reference'))}</small>")
  ```
  Also add `(f"<small>{e(trade['observation']['reason'])}</small>" if trade["observation"] else ""),` to the summary list at views.py:111-114.
- **Changes:** page only.
- **Certainty:** certain from the code.

## Answers to the settle-points that are not findings above

**Q1. Where replay takes a different branch from live:**
- session.py:42-43 (clock stop), :45-47, :93-125 (feed, preflight, stream, `warm_through`), :263-283 (`capture_end`, `recorded_stop`), :300-302 (frame hash).
- run.py:212-215, :248-257, :298-305 (the guard reads the recorder only when `capture_connection` is set), :337-353 (pacing), :363-367.
- Workflow :89-103 (original revision).
- Only findings 1, 2 and 4 can make the replay's decisions or orders differ. Live wall-clock stops (guard, SIGTERM, publication failure, recorder end) land between steps under the session lock, and the replay reproduces them through `recorded_stop` / `recorded_capture_end`.
- Notice, relay and publication do not touch decisions. `wait_for_orders` only adds wall time; whether that pushes a replay past its own 5.75 hours depends on push latency.

**Q2. What a receipt replay takes and what it recomputes:**
- **Takes from the receipt:**
  - the plan and budgets (run.py:252-255);
  - `code_commit` (session.py:67; workflow :95-101);
  - `inputs[0].mode` / `capture`, `trade_day`, `market` (session.py:99-105);
  - `first_live_decision_cursor`, `delivered`, `last_source` (capture.py:185-203);
  - `status`, `capture_end`, `timers_after_last_input_ns` (capture.py:208-209).
- **Recomputes:** the book, calculations, decisions, orders, fills, frame hash, receive-time file, weekly boundaries, calculation digests and its own causal preflight. The preflight cutoff is not compared.

**Q3. Timers against messages:**
- A timer fires only before the next admitted message, when its expiry is strictly earlier than that message's receive time (session.py:288; run.py:158 for the paced path).
- At an equal nanosecond, the message goes first. For a sided print the expiry is folded into the same read (engine.py:217-218, inputs.py:64-67). For an unsided message, `engine.advance_clock(received)` drains it in the same batch.
- Live and replay run the same code here, and a live captured run never fires timers when idle. I found no case where they order a timer and a message differently.
- Outside these items: the causal preflight traces only `engine.tick` (causal_gate.py:59, capture.py:300), so the timer path is outside the cutoff check.

**Q4. What differs between journals by construction:** `run`, `recorded_ns`, the trade id (uuid5 of the run), `order_id` / tags, `elapsed_ns_at_stop`, and possibly `fill_id`. The comparison handles these as described in findings 7 and 8.

**Q6. The default purchased-tape replay, first minute:**
- **Start-up path:** the plan is required (workflow :78-82). The archive is pinned at 46199c5; its sparse path matches nymex-ng.json:9. The markets-data action makes the SSH push URL that `writer_remote` accepts. Full history is fetched (:59), which the rule-commit logs need. `/health` has a 90-second timeout. `check_prefix` makes two passes from Sunday, under the deadline. Pacing starts at 6 pm Eastern.
- **Things that would stop it early:**
  - A message budget smaller than the Sunday seating records stops it with "budget reached".
  - A plan whose `databento_instrument_id` differs from the archive raises at the first message (paper_execution.py `market`); the archive's id is not readable here.
  - Nothing else found.
- **Run branch:** the new parentless branch is fine. The replay workflow (:83-88) and the comparison workflow (:35-44) read only `paper-trading/<run>` from `paper-runs/<run>`.

## Item 16 (exposure)
- trades.py:116-117 keeps the "observation ended with paper exposure" order-status row on its own (rule, trade_id) row.
- `record_interruption` (paper_execution.py:274-292) writes one per parent and per same-direction manager, with that trade's signed inventory and working order ids.
- views.py:142-147 shows the time, the net contracts and each working order on that row.
- I found no sum across trades in trades.py, views.py, relay.py or monitor.html. The status packet has `open_positions`, a count (session.py:430), which is not rendered.

## Read and doing what the items require
- **The recorded window:** the receipt replay admits exactly the live prefix and stop reason.
- **Clock and identifiers:** nothing in the matcher reads the wall clock (the venue clock is set to tape times, paper_execution.py:110 and :217). The random UUIDs do not reach the journal.
- **CL16/CL17:** their row holds the trade id, the source print reference and the missing quote, as the status says.
- **Scoring:** no code scores or counts trades; `trade_data` is read only for page labels and administrative order styling.

## Outside these items, one line each
- `MakerTakerFeeModel()` is built at paper_execution.py:52; no commission field reaches `emit`.
- The labels "with" / "against" (cx_observations.py:72) are shown as "Print response" on the page.
- The CL16 rule text carries RIGHT / WRONG.
