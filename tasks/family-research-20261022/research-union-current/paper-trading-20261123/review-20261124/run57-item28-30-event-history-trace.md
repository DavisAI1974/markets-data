# Run 57: items 28 and 30, the append-only event history and the fill-to-finding trace: the table of every event and what each carries

The agent's own report, word for word, as it came back to the session (session_017eY1WPw7p6f6Tyx49EyYD4, 2026-11-24). It is a reading of code and documents. Nothing was run. What was done with each finding is in README.md beside this file and under the item's number in the platform checklist.

---

REVIEW OF WISHLIST ITEMS 28 AND 30 (journal coverage and order traceability). Every statement below comes from reading the code. Nothing was executed.

BASELINE. The review started at e12bfde. Fifteen commits landed while I was reading. The findings are at de048e0e50a004e1124104dfaf22d8710e8c0256. Between 55e54fd and de048e0 the in-scope files (session.py, engine.py, paper_execution.py, claude_rules.py, cx_observations.py, inputs.py, journal_publication.py, unsided_print_rules.py) are unchanged. trades.py gained one line, at 35. The changes from e12bfde to 55e54fd are reflected below:
- `interrupt_cx` is renamed `interrupt_trade` and now also covers CL16/17.
- `record_interruption` is new.
- The refusal "order tag already used; not sent" is new.
- `submit()` now uses `known_received_ns` for the clock, `ts_init`, `OrderSubmitted` and a new `submitted_ns` field.
- At trade-day end, interrupted CL trades now get an administrative close.

The item 28 and 30 status text I quote is from the tip. It now sits at wishlist lines 187-197.

DISCLOSURE. Two commands I ran go beyond reading. `python3 - "$f" <<'EOF'` started the interpreter on an empty script, and `pip show nautilus_trader` ran pip; it printed nothing. The grounding tool (`tools.kgraph.grounding`) was not run, because the branch rule is that nothing is run.

COMMON FACTS. These apply to every row and are not repeated in the table.
- (a) `recorded_ns` is the host wall clock, `time.time_ns()` (session.py:160). `sequence` is `self.events` (session.py:158).
- (b) Every row that has a `rule` key gets `rule_commit` and `finding` (session.py:163-165). `rule_commit` is the last commit that changed `paper_platform/rules/<rule>.json` (session.py:70-72). `finding` is that JSON's `evidence` URL.
- (c) The platform `code_commit` is on no journal row. It is only in start.json (session.py:129) and receipt.json (session.py:422). Finding 1.
- (d) Signal rows come from `Engine.event` (engine.py:47-48) and `quote()` (engine.py:15-16).
  - `received` is `ts_recv`, the tape receive time of the source message (inputs.py:59,85).
  - `exchange` is `ts_event` (inputs.py:86). `position` is the tape position.
  - `reference` is (`source_sha256`, `record_index`) (inputs.py:70).
- (e) What a reference points at depends on the feed:
  - Purchased replay: SHA-256 of the whole UTC-day DBN file, plus the record's index inside that file. The index counts the vendor-snapshot records (feed.py:150,163).
  - Capture: SHA-256 of the single frame body, plus its tape position (capture.py:278).

======================================================================
1. THE TABLE
Columns:
- T: time in ns, and which clock.
- RC: rule_commit.
- PC: platform commit (always "no on row", from (c)).
- REF: the feed reference and what it points at.
- XREF: extra references.
- LINK: order_id, fill-to-order, order-to-signal, finding.

n/a means no rule or message made the row. no means the row lacks something it could carry.

STATUS
S1. status / started (session.py:152)
- T: recorded_ns only.
- RC: n/a (no rule). PC: no.
- REF: n/a (no message yet).

S2. status / <stop reason> (session.py:380)
- T: recorded_ns, plus last_source.tape_received_ns (ts_recv of session.last) and host_received_ns. No exchange time.
- RC: n/a. PC: no.
- REF: last_source.reference, which is session.last. That is the last DELIVERED message of any period, including the vendor snapshot or out-of-session messages (session.py:336-341).
- Reasons that reach a live Session.stop:
  - "flattened at the 5.75-hour stop" (run_clock.py CLOCK_STOP)
  - "budget reached"; "failure"; "end of capture"; "end of purchased input"
  - "capture: " + status, an open set. Seen: closed, end of purchased input, message budget reached, capture stopped, capture failure, interrupted, CaptureFailure texts, "recorder exited without a terminal record", "capture journal unreadable". A "clock limit" status maps to CLOCK_STOP.
  - the replayed `recorded_stop`, an open set (it is the original run's reason)
  - "run stopped"; "markets-data snapshot failed" (run.py:294); "markets-data publication failed" (journal_publication.py:142); "session stopped" (api.py:49)
  - run.py's `why` text on an exception (run.py:376)

SIGNALS
G1. signal / open, CL01-CL15 (engine.py:326 -> open_trade 50-67)
- T: yes, ts_recv and ts_event of the confirming F_LAST message.
- RC: yes.
- REF: the confirming message.
- XREF: arm_reference = None (engine.py:64) -> NO. The arming message survives only as tape positions in trigger/conditions. Finding 3.

G2. signal / open, CL16/CL17 (unsided_print_rules.py:44,57)
- T yes, RC yes.
- REF: the unsided print that armed and opened it, the same message. Nothing further needed.

G3. signal / open, CX entry (engine.py:344)
- T yes, RC yes. REF = q, the print. XREF arm_reference = p, yes.

G4. signal / close, CL, normal (engine.py:321)
- T yes, RC yes. REF = the closing message.
- XREF: third_step_reference for CL01, yes.

G5. signal / close, CL released after settlement (engine.py:277-280)
- REF = the release message.
- The message at which the close condition was met (stored at engine.py:277) is never emitted -> NO. Finding 4.

G6. signal / close, CX entry management exit (engine.py:290 -> 321)
- REF = t. entry.reference = q.
- p's reference is missing -> NO. Finding 5.

G7. signal / close, CL07/08 timer (engine.py:178-211)
- T: received = expiry, a computed tape-clock time (earliest trade ts_recv + LINE_NS), not a message's time. exchange = None, position = None.
- RC yes. REF = sources[0], the earliest trade that left the span.
- XREF: expiry_references (all of them), expiry_quote_reference = engine.last. yes.

G8. signal / close at trade-day end, CL open trade (engine.py:362-369, admin False)
- T: engine.last ts_recv/ts_event, plus known_received_ns.
- REF: engine.last, the last in-session tick.
- XREF: known_at = the first message with ts_event >= end_of_day (engine.py:236-237). yes.

G9. signal / close at trade-day end, interrupted CL (engine.py:370-374, administrative=True)
- As G8, with trade_data False. yes.

G10. signal / close at session stop (engine.stop admin=True, via session.py:348)
- T: engine.last's time, not the stop time. The stop time is only in recorded_ns.
- REF: engine.last.
- The stop itself has no feed message. The matching flatten order references session.last instead (P5).

G11. signal / hold, suspend additions (manager first confirmation; engine.py:113-117, 126-139)
- REF = t (this is q). arm_reference = self.p. yes.

G12. signal / exit, release warning, not scored (manager, after confirmation)
- REF = t. arm_reference = state p.
- The confirmation row q (state["q"]) is not referenced -> NO. Finding 6.

G13. signal / not scored, CX entry confirmation with missing fields (engine.py:346-354)
- trade_id None. REF = t.
- p is not referenced -> NO. Finding 7.

G14. signal / not scored and observation interrupted, open trades (interrupt_trade, engine.py:156-169)
- Called at engine.py:270 (CL16/17 missing quote), 286 (settlement or F_MAYBE_BAD_BOOK), 292 (CX missing) and 365 (trade-day end, CX).
- REF = t. entry.reference = q.
- For CX, p's reference is missing -> NO. Finding 5.

G15. signal / held into settlement (engine.py:284)
- REF = the first settlement tick. yes.

G16. signal / quote followed (engine.py:307-317)
- REF = t. q_reference. yes.

G17. signal / print observed (cx_observations.py:65-75)
- rule = the response's rule. REF = the print. q_reference. yes.

G18. signal / price response unresolved (cx_observations.py:83-91)
- Raised at engine.py:254, 142, 356 and 360-361. REF = that tick. q_reference. yes.
- Timer variant (engine.py:210): REF = sources[0], and bid/ask come from engine.last with no reference to that message -> NO. Finding 8.

PAPER ORDERS (kind "paper order")
P1. No execution plan (session.py:182-184)
- order_id = run-seq. signal_sequence yes. T/REF copied from the signal. RC yes.

P2. Native open, entry rule (paper_execution.py:161-163)
- All signal fields, plus order_id, signal_sequence, submitted_ns (= known_received_ns).
- RC and finding are the entry rule's. yes.

P3. Native close (strategy close; manager "exit" routed as close with signal_action exit, paper_execution.py:259; follower close on parent close)
- yes.

P4. Native follow-open, manager (paper_execution.py:270-272; tag run-seq-MANAGER at session.py:190)
- rule = manager. entry_rule = parent. signal_sequence = the PARENT's signal. RC/finding = the MANAGER's. yes, see Finding 18.

P5. Administrative flatten WITH a close signal (paper_execution.py:313-317)
- signal_sequence yes.
- received and reference = session.last. bid/ask = session.last.
- exchange, position and entry still come from the stop signal (engine.last). So one row mixes two messages -> NO (consistency). Finding 12.

P6. Administrative flatten WITHOUT a close signal
- No signal_sequence -> NO. No exchange, no position -> NO. Findings 11, 12.

P7. Trade-day-end close order
- REF = engine.last. known_at and known_received_ns are present. submitted_ns = known_received_ns. yes.

ORDER STATUS (kind "order status")
O1. Nautilus events through on_event (paper_execution.py:75-78, 90)
- execution_event is the event class name. The pinned Nautilus 1.231.0 source (local clone, backtest/engine.pyx) generates Rejected, Accepted, ModifyRejected, Updated, CancelRejected, Canceled, Triggered, Expired and Filled.
- Read but not exercised: Accepted, Rejected (post-only that would cross), Canceled (IOC remainder, cancel_order) and CancelRejected can be reached from the three shapes (MarketOrder IOC, LimitOrder IOC, LimitOrder post-only GTC).
- T: `received` is the decision's if the event arose inside submit(), or the market() message's if it arose inside market(). exchange: NO. Finding 9.
- RC yes. order_id yes. Status-to-order by order_id: yes. signal_sequence: no (reachable through the paper order).

O2. OrderCanceled for a working order cancelled by a later close (paper_execution.py:108-110)
- REF = the close decision.
- No link to the close's signal or to the close order -> NO. Finding 10.

O3. "order tag already used; not sent" (paper_execution.py:96-97)
- **event, so signal_sequence when the event has one. RC yes. No paper-order row, by design.

O4. "liquidation unavailable after feed interruption" (paper_execution.py:122-124)
- yes. signal_sequence as in P5/P6.

O5. "no filled contracts to close" (paper_execution.py:128-129)
- Emitted only when working orders existed. With nothing working, no row at all -> NO. Finding 14.

O6. "No {bid|ask} for {post|cross_limit} order" (paper_execution.py:144-145), four variants
- signal_sequence yes.
- No execution_event, no order_status -> NO. Finding 16.

O7. "unfilled administrative remainder" (paper_execution.py:170-171)
- signal_sequence as in P5/P6.

O8. "observation ended with paper exposure" (record_interruption, paper_execution.py:274-292, called at session.py:175-177)
- signal_sequence yes. working_order_ids. RC is the parent's or the manager's. yes.

FILLS (kind "fill", paper_execution.py:84-88)
Every fill carries order_id (so fill-to-order holds), rule_commit, finding, bid/ask, quote_reference, quote_received_ns and fill_received_ns. Every fill lacks exchange time -> NO (Finding 9) and signal_sequence (reachable through the order).

F1. Resting post filled on a later message (inside market())
- reference, received and fill_received_ns = the filling message. quote_reference = the same message.

F2. Immediate fill inside submit()
- reference and received = the decision row's. fill_received_ns = known_received_ns. quote_reference = the last market() message.

F3. Timer decision
- reference = sources[0]. received = fill_received_ns = expiry (computed).
- The book and quote_reference depend on where the timer fired:
  - session.step:278-279, before market(M): message M-1.
  - engine.py:218, inside tick, after market(M): message M.
  - run.py pace_to_record:166: the last message.

F4. Trade-day-end close
- reference = engine.last. fill_received_ns and quote_reference = the first post-halt message (market() ran on it at session.py:294).
- known_at is not copied onto the fill.

F5. Flatten
- reference = session.last.
- quote_reference = the last NON-snapshot message market() saw (market() returns early on vendor snapshots, paper_execution.py:205-206).

ROWS NEVER WRITTEN
- R1: instructions skipped at the budget or deadline break (session.py:187-189). Finding 13.
- R2: a close with nothing held and nothing working (paper_execution.py:126-130). Finding 14.
- R3: batches rolled back (session.py:203-211).
- R4: decisions on warm-up messages, discarded (session.py:302-307). Finding 15.

======================================================================
2. NUMBERED FINDINGS
"Lines" are proposals. None was executed. Lines marked [DIGEST] add keys to decision dicts. That changes the causal-gate and preflight decisions_sha256 (capture.py record(), causal_gate) and decision parity across commits in replay_comparison.

1 [28] Platform commit not on any row.
- session.py:155-162. Item 28 asks for "the rule version (git commit) that made it" on each event. For CL rules that is the code (Finding 2).
- In hand: self.revision (session.py:58). Add to the dict at session.py:160: `code_commit=self.revision,`
- Certain from the code.

2 [28] rule_commit covers only the JSON file.
- session.py:70-72. CL01-15 behaviour lives in claude_rules.py, unsided_print_rules.py, engine.py, inputs.py, rulebook.py and cx_observations.py. The CL JSON holds a prose specification (rules/CL07.json).
- Mechanism: 95400eb changed engine.py and unsided_print_rules.py while CL01-15's rule_commit stayed 902d6e8. That diff reads as behaviour-preserving for CL01-15, so it is the mechanism only, not an observed drift.
- receipt calculation_files (session.py:137-139) lists inputs.py and root/crypto_ng files. It does not list claude_rules.py, unsided_print_rules.py, engine.py, rulebook.py or cx_observations.py.
- Lines: extend that tuple with "paper_platform/claude_rules.py", "paper_platform/unsided_print_rules.py", "paper_platform/engine.py", "paper_platform/rulebook.py", "paper_platform/cx_observations.py". With Finding 1 the per-row code_commit covers them as well.
- Certain from the code.

3 [28] CL open has no arming-message reference.
- engine.py:64 gives None for CL. claude_rules.arm (32-41) has no tick. t["reference"] is in scope in at() (66) but not inside arm().
- Lines [DIGEST]:
  - claude_rules.py after line 67: `self.arm_reference = t["reference"]`
  - in arm()'s dict: `arm_reference=self.arm_reference,`
  - engine.py:64: `arm_reference=p["reference"] if p else signal.get("arm_reference"),`
- Certain from the code.

4 [28] The message of a settlement-deferred close is dropped.
- engine.py:277 stores it in idea["deferred_close"][1]. close_trade (engine.py:81-85) copies only four keys.
- Line [DIGEST], in close_trade's details: `**({"deferred_reference": idea["deferred_close"][1]} if "deferred_close" in idea and not administrative else {}),`
- Certain from the code.

5 [28] CX close and interrupt rows lack p.
- close_trade (engine.py:69-86) and interrupt_trade (156-169).
- In hand: idea["p"], set at engine.py:54; None for CL.
- Line [DIGEST], in both event() calls: `arm_reference=idea["p"]["reference"] if idea.get("p") else None,`
- Certain from the code.

6 [28] Manager rows after confirmation lack q.
- engine.py:126-139. management() reads state["q"] (engine.py:105).
- Line [DIGEST]: `q_reference=(state["q"] if state else t)["reference"],`
- Certain from the code.

7 [28] CX entry "not scored" lacks p.
- engine.py:346-354. self.p is set in that branch (engine.py:333).
- Line [DIGEST]: `arm_reference=self.p["reference"],`
- Certain from the code.

8 [28] Timer "price response unresolved" carries bid/ask (engine.py:194-195) without a reference.
- In hand: self.last["reference"] (already used at engine.py:203).
- Replace engine.py:210 [DIGEST] with:
  ended = self.end_orphaned_responses(tick)
  for e in ended: e["expiry_quote_reference"] = self.last["reference"]
  events.extend(ended)
- Certain from the code.

9 [28] No exchange time on order-status or fill rows (paper_execution.py:75-78).
- In hand in market() as `stamp` (paper_execution.py:211), and in submit() as event.get("exchange"). Neither is stored on the venue.
- Lines:
  - RuleVenue.__init__: `self.exchange = None`
  - market() loop after 245: `venue.exchange = stamp`
  - submit() after 102: `self.exchange = event.get("exchange")`
  - on_event data: `exchange=self.exchange,`
- Related: market() gates only vendor snapshots (paper_execution.py:205). A working post can fill on messages in the settle window or after the 17:00 ET halt. That includes next-trade-day messages after 18:00 ET within the last UTC file, and nothing cancels an interrupted CX trade's working entry post before the stop. Committed plans post the open legs of CL02, CL09, CL12, CX01, CX09 and CX10.
- Certain from the code. Whether such a fill occurs depends on the tape.

10 [28/30] Cancels caused by a later close are not linked to that close (paper_execution.py:108-110 -> on_event).
- Lines:
  - __init__: `self.cause = None`
  - submit() after 103: `self.cause = dict(cause_signal_sequence=event.get("signal_sequence"), cause_order_id=order_id)`
  - market() loop: `venue.cause = None`
  - on_event data: `**(self.cause or {}),`
- Certain from the code.

11 [30] A flatten without a close signal has no signal_sequence (paper_execution.py:313-317).
- When this happens:
  - a manager with on_parent_close "hold" (skipped at paper_execution.py:266). No committed plan uses it (both plans say "exit"); plans from workflow input can.
  - residual inventory after an engine close, e.g. a partially filled IOC close
  - _record_stop_signals raising (session.py:363-366)
- Not in hand inside flatten(). It is in hand in RuleVenue.submit as event.get("signal_sequence").
- Lines:
  - __init__: `self.prior_signal = {}`
  - submit() after 101: `if event.get("signal_sequence") is not None: self.prior_signal[key] = event["signal_sequence"]`
  - flatten: `event.setdefault("prior_signal_sequence", venue.prior_signal.get(key))`
  - This is the prior signal on that trade, not the one that caused the flatten.
- Certain from the code.

12 [28] Flatten rows mix messages, and the stop signal and its order reference different messages.
- The stop signal (session.py:348) is engine.last.
- The flatten order's received and reference are session.last (paper_execution.py:315-316). exchange and position come from the merged signal (313).
- Lines, in the flatten dict:
  - `exchange=last["raw"]["ts_event"], position=last.get("position_on_tape"),`
  - `signal_reference=(close_signals or {}).get((rule, key), {}).get("reference"),`
- Certain from the code.

13 [28] Skipped instructions leave no trace (session.py:187-189).
- `needed` (session.py:203) counts one order per decision. It does not count follower orders, statuses or fills, so a follower order can hit the break.
- In hand: instruction, tag, sequence.
- Lines:
  - __init__: `self.skipped_instructions = []`
  - replace `break` so that it records each remaining instruction: `self.skipped_instructions.append(dict(signal_sequence=sequence, rule=instruction["rule"], order_id=tag)); continue`. The tag would be computed first.
  - stop's update (session.py:379): `skipped_instructions=self.skipped_instructions`
- Certain from the code.

14 [28] A close with nothing held and nothing working returns silently.
- paper_execution.py:126-130. The tag has already been consumed (94).
- Line: drop `if working:` so the "no filled contracts to close" row is always written.
- Certain from the code.

15 [28, check 3: warm-up suppression] Two sets of rows are never written.
- Warm-up decisions are computed and discarded (session.py:302-307), by design: "carry no historical position".
- Refused batches roll back (session.py:203-211).
- Neither is counted anywhere.
- Line: `self.warm_decisions += len(self.engine.tick(message))` (init 0), with the count in the receipt.
- Certain from the code.

16 [28] The no-quote refusal has no execution_event.
- paper_execution.py:144-145.
- Line: `execution_event=f"No {field} for {style} order",`
- Certain from the code.

17 [30] `finding` points at a whole family document, not a per-rule finding.
- CL01-15 share EVIDENCE.md@46199c5. Locally it has per-rule sections; the headers are at lines 24-368.
- CL16/17 point at VERSIONS.md@af2a0ef. EVIDENCE.md at that commit has no CL16/CL17 text; VERSIONS.md has their sections at lines 270 and 290.
- CX01-15 share strategy-20261123-codex/EVIDENCE.md@ad10921. That commit and folder are absent from every ref in the local markets-data clone, so it was not readable.
- A per-rule anchor is not in hand in the platform.
- Certain for the URLs. The CX content depends on material not readable here.

18 [30] On a manager follow-open, rule_commit and finding on the order and fill are the manager's (session.py:163-165, rule = manager per paper_execution.py:270).
- The parent's commit and finding are only on the parent signal row, reached through signal_sequence.
- No reader uses signal_sequence: trades.py joins on (rule, trade_id) (trades.py:90) and source_trade_id (trades.py:8).
- Not in hand in instructions(). In hand in write().
- Line: `if event.get("entry_rule"): event.update(entry_rule_commit=self.rule_commits[event["entry_rule"]], entry_finding=self.rules[event["entry_rule"]]["evidence"])`
- Certain from the code.

19 [28] Fill `reference` means different things depending on the path (F2-F5).
- The filling book is identified by quote_reference and quote_received_ns.
- On timer fills, fill_received_ns is a computed expiry, not a message receive time.
- Certain from the code.

20 [28] Rule commits are not guarded against a shallow clone.
- session.py:70-72 has no shallow guard and no empty-result check.
- The paper workflows fetch full history (live_ng_paper.yml:49, purchased_mbo_paper.yml:59 have no --depth). agent_run, record and compare use --depth=1 but do not start a Session.
- Lines:
  - `if git(code, "rev-parse", "--is-shallow-repository") == "true": raise ValueError(...)`
  - `if not all(self.rule_commits.values()): raise ValueError(...)`
- Certain from the code.

21 [28] Receipt replay checks only code_commit (session.py:62). It does not compare rule_commits or rule_files with the receipt.
- Line, after session.py:72: `if replay_receipt is not None and replay_receipt.get("rule_commits") != self.rule_commits: raise ValueError(...)`
- Certain from the code.

======================================================================
3. ITEM 30 CHAINS
(i) Entry rule's opening order fill
- fill.order_id -> paper order row: same order_id, tag run-seq, session.py:190.
- order -> signal: signal_sequence (session.py:186, copied by **event at paper_execution.py:161).
- rule_commit and finding are on the signal, order and fill rows.
- No link fails.

(ii) Manager follow-open fill
- fill.order_id -> paper order (tag run-seq-MANAGER).
- order -> signal: signal_sequence = the PARENT's signal row.
- rule_commit on the order and fill: resolved, and it is the MANAGER's file. finding is the MANAGER's own evidence.
- The parent's commit and evidence are reachable only through signal_sequence, which no reader follows (Finding 18).

(iii) Administrative close at the run stop
- fill.order_id -> paper order (run-flatten-RULE-KEY).
- order -> signal: signal_sequence only when close_signals had (rule, key).
- The first failing link is order -> signal in the P6 cases (Finding 11).
- rule_commit and finding are present, for the venue's rule.

======================================================================
4. APPEND-ONLY
- events.jsonl is opened once, with "x" (session.py:123).
- Every other open reads:
  - run.py:97 and 270
  - api.py:79
  - journal_publication.py:84 reads "rb" and appends to a temporary mirror blob
  - restore_view.py and replay_comparison.py
- Nothing truncates or rewrites the file. Publication pushes fast-forward commits of growing prefixes.
- sequence = self.events, incremented only after write and flush (session.py:166-168). json.dumps runs before write, so a serialization error leaves no gap. A partial OS write is not guarded; that depends on the OS.
- write() takes no lock itself. Every caller holds the session RLock:
  - step, advance_clock and stop (with stop_capture)
  - venue emits from market, submit and flatten, which run inside those
  - the guard thread (run.py:294-306), the api watchdog and the GitJournal worker reach write only through stop
  - the notice worker only reads
- Interleaving therefore rests on Nautilus delivering matcher events synchronously inside process_*. I did not find MessageBus.send's source in the local clone; that point depends on it.

5. RESTING POST FILLED LATER
It carries the FILLING message's reference, received, fill_received_ns and quote_reference, because market() sets them at paper_execution.py:242-245 before matching. It does not carry the decision row's reference (that is reached through order_id) or the filling message's exchange time (Finding 9).

6. RULE VERSION HONESTY
- `git status --porcelain -- paper_platform root crypto_ng` refuses on modified or untracked files (session.py:60). rules/*.json is not gitignored, so a rule file that differs from HEAD stops the start.
- rule_commits use `git log -1 <HEAD> -- file`.
- Receipt replay requires the same code_commit (session.py:62), so the original commit is what the replay records. The replay start.json also records original_run (session.py:112) and plan_source "receipt for <run>". Finding 21 applies.

OTHER HOUSE RULES, read only
- No mid price in paper_platform (grep).
- Trade cost: paper_execution.py:52 builds FillModel() and MakerTakerFeeModel(). Nautilus 1.231.0's defaults are prob_fill_on_limit 1.0 and prob_slippage 0.0 (fill.pyx:59-64). Both plans set maker_fee "0" and taker_fee "0" (lines 12, 25). Commission is not journaled. Fills carry a maker/taker `liquidity` label (paper_execution.py:88).
- The trade day is 6 pm ET the evening before to 5 pm ET (root/calendar.py:35-39). It is used for eligibility and for the engine's end.

READ AND FOUND COMPLETE
- The order_id join from fill to order on every native order row that has a paper-order row.
- rule_commit and finding resolved for every row with a rule, managers included.
- signal_sequence on every paper order made through record().
- References on G2-G4, G7-G11 and G15-G17.
- The full set of expiry references on timer closes.
- known_at on trade-day-end closes.
- record_interruption rows carry signal_sequence.
- The journal file is created exclusively and only appended.

Files: /home/user/paper-trading-platform/paper_platform/session.py, engine.py, paper_execution.py, claude_rules.py, cx_observations.py, unsided_print_rules.py, inputs.py, feed.py, capture.py, journal_publication.py, trades.py, rulebook.py, run.py, api.py, run_clock.py, paper_platform/rules/*.json, paper_platform/execution_plans/ngx3-*.json, /home/user/paper-trading-platform/docs/platform/OWN_PLATFORM_WISHLIST_20261123.md, /home/user/markets-data/tasks/family-research-20261022/research-union-current/strategy-20261123-claude/
