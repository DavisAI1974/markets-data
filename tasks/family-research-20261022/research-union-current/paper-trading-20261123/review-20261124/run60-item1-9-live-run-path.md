# Run 60: items 1 and 9, the live run path: everything that would stop or stall the first live run, and whether live calculations are ROOT's

The agent's own report, word for word, as it came back to the session (session_017eY1WPw7p6f6Tyx49EyYD4, 2026-11-24). It is a reading of code and documents. Nothing was run. What was done with each finding is in README.md beside this file and under the item's number in the platform checklist.

---

Review of checklist items 1 and 9: paper-trading-platform, branch codex/strategy-trades-and-mbo-capture

**How this was done.** I only read code: sed, grep, git log/show/diff and cmp. Nothing ran. I tried one command that contained `python3 -c 1`; the permission layer blocked it, so no interpreter started. The grounding check (`tools.kgraph.grounding`) was not run, because of the no-run rule.

**The branch moved during the review.** It went from 37c5e91 to 34797ef: commits 2de679a, d01b70a and 34797ef. Line numbers below are at 37c5e91 unless marked. The newer commits change these files I read:
- `capture_backup.py`: a checkpoint push now has a 55 s timeout, and a slow push ends the process.
- `feed.py`: the book mirror is now checked at every UTC date change.
- `paper_execution.py`: a size increase now reaches the matcher as a delete and an add.
- `record_mbo.py`: the delivery that crosses the clock limit is now stored before the stop.

Running notes are in `/tmp/claude-0/-home-user/f6fc58bd-1d38-5c78-9832-91292fa09200/scratchpad/review2/items-1-9.md`.

## A. Findings that would stop or stall the first live run

**1. [item 1] The replay always starts at Sunday 00:00 UTC.**
- **Where:** `paper_platform/record_mbo.py:158-159`
- **What it does:** it subscribes to MBO with `stype_in="continuous"` and `start=datetime.combine(sunday, wall_time(), timezone.utc)`. In late November that is Saturday 7 pm EST. It does this on every connection, including one that has restored a checkpoint, because `capture.py:50-56` compares the replay byte for byte with the stored prefix.
- **What else requires it:** `capture.py:269-271` requires the first stored MBO record to be Sunday's unflagged clear, so the snapshot option cannot stand in.
- **Consequence:** if the gateway's intraday replay is limited to the last 24 hours, every start after Monday 00:00 UTC (Sunday 7 pm EST) is refused or truncated.
  - Refused: an ErrorMsg leads to `CaptureFailure`, and the recorder sends a phone notice.
  - Truncated: Session init raises "capture must start at Sunday's unflagged exchange clear", and the phone gets "preflight: failure".
- **Usable start window, if the limit is 24 h:** from the first MBO record of the week (the Sunday pre-open) to 7 pm EST Sunday, less the setup time. The named trade day is then Monday. A mid-week first run, or a second run later in the week, is not possible.
- **Smallest fix:** a guard that refuses loudly before anything is spent. Allowing mid-week starts (snapshot seating) changes item 6 and is Greg's decision. Insert in `run_live.py` after line 53:
```python
from datetime import datetime, time as wall_time, timedelta, timezone
if datetime.now(timezone.utc) >= datetime.combine(week_sunday(args.trade_day), wall_time(), timezone.utc) + timedelta(hours=24):
    from .run import notify
    notify("the Sunday start-up is outside the live replay window", "preflight")
    return 1
```
- **Certainty:** depends on Databento's live replay window, which cannot be read here.

**2. [item 1] Starting before any MBO record exists kills the run in its first minute.**
- **Where:** `live_contract.py:32-35`, `record_mbo.py:143-148`
- **What it does:** `publish()` runs when the replays complete. If no MBO record has arrived by then, `instrument_id` is None and it raises "weekly replay did not supply a definition". The recorder ends, then `run_live.py:88-89` raises RuntimeError.
- **Smallest fix:**
  - In `record_mbo.py:147-148` use:
```python
if contract and contract.instrument_id is not None and not contract.path.exists():
    contract.publish()
```
  - At the end of `LiveContract.observe` add:
```python
if self.instrument_id is not None and self.instrument_id in self.definitions and not self.path.exists():
    self.publish()
```
- **Certainty:** certain from the code for a start with zero MBO records. Whether the gateway sends MBO before the open depends on Databento and CME.

**3. [item 1] The contract file waits for two "replay completed" messages.**
- **Where:** `record_mbo.py:137, 143-146`
- **What it does:** `replays_remaining = 2` assumes one REPLAY_COMPLETED per subscription.
- **Consequence:** if the gateway sends one per session, or none for the `start=0` definition subscription, the contract file is never written. `run_live.py:85-87` then waits the full 5.75 h and returns 1 with no notice of its own. The `live_starts` row is never written either, so `live_eligible` stays False.
- **Smallest fix:** the change in finding 2 removes the contract's dependence on the count. The `live_starts` count still depends.
- **Certainty:** depends on Databento live behaviour. Whether two replay subscriptions are allowed in one session also depends.

**4. [item 1] The definition header may not build.**
- **Where:** `live_contract.py:38-39`
- **What it does:** it builds `databento_dbn.Metadata` without `symbols`, `partial`, `not_found` or `mappings`.
- **Consequence:** if the 0.62 constructor requires those arguments, a TypeError is raised inside the callback. That leads to `sink.failed`, "live DBN write failed", and RuntimeError at `run_live.py:89`, all in the first minutes.
- **Smallest fix:**
```python
header = Metadata(dataset=self.dataset, start=record.ts_event, stype_out=SType.INSTRUMENT_ID,
                  symbols=[], partial=[], not_found=[], mappings=[],
                  schema=Schema.DEFINITION, stype_in=SType.INSTRUMENT_ID)
```
- **Certainty:** depends on the databento_dbn 0.62 signature, which is not on disk. The DBN version of the header against the record bytes also depends.

**5. [item 1] The definition file is written uncompressed.**
- **Where:** `live_contract.py:41`, `live_contract.py:50-51`
- **What it does:** it writes uncompressed DBN, which `DatabentoDataLoader().from_dbn_file` then reads.
- **Smallest fix:**
```python
pending.write_bytes(zstandard.ZstdCompressor().compress(bytes(header) + bytes(record)))
```
  with `import zstandard` at the top of the file.
- **Certainty:** depends on whether the adapter accepts a file that is not zstd. The adapters crate is not on disk.

**6. [item 1] Publishing needs the deploy key, which is not checked anywhere.**
- **Where:** `live_ng_paper.yml:51-61`, `action.yml:35,51`, `capture_backup.py:69-71`, `run.py:42-52`
- **What it does:** the push URL `git@github.com:...` is set only when `secrets.MARKETS_DATA_DEPLOY_KEY` is non-empty.
- **Consequence if the secret is absent:**
  - The capture backup follower raises at its first publish, about 60 s in, and the run ends.
  - `run.py` refuses with "HTTPS publication requires MARKETS_DATA_TOKEN"; the workflow never sets that variable.
- Item 1's status lists four missing settings but does not mention this secret.
- **Smallest fix:** a step before line 51:
```yaml
- name: Require the markets-data deploy key
  env: {KEY: "${{ secrets.MARKETS_DATA_DEPLOY_KEY }}"}
  run: test -n "$KEY"
```
- **Certainty:** certain from the code. Whether the secret exists is not readable here.

**7. [item 1] Nothing checks that the named trade day matches the run.**
- **Where:** `run_live.py:47, 68`
- **Consequence:**
  - A date whose trade day does not overlap the run leaves every message with `in_session` False (`feed.py:46`). Then `capture_preflight` (`capture.py:320`) never reaches its threshold, and the run stalls to 5.75 h. Example: today's date typed after 6 pm ET.
  - A Sunday date raises ValueError at `run_live.py:68`.
- **Smallest fix:** after `run_live.py:53`:
```python
from root.calendar import trade_day_bounds
opens, halts = trade_day_bounds(args.trade_day)
if not time.time_ns() < halts or time.time_ns() + int(LIMIT_SECONDS * 1e9) <= opens:
    parser.error("the named trade day does not overlap this run")
```
- **Certainty:** certain from the code.

**8. [item 1] The paper session waits for the preflight before it exists.**
- **Where:** `session.py:107`, `capture.py:289-323`
- **What it does:** no session, journal, matcher or phone view exists until the preflight engine has seen 4,096 in-session messages and at least one `open`.
- **Consequence:** on a Sunday start this cannot begin before 6 pm EST.
- **Fix:** none proposed; this is item 11's gate. The dispatch time must allow for it.
- **Certainty:** certain from the code. How long it takes depends on the market.

**9. [item 1] The checkpoint publisher ends the run on any one failed push.**
- **Where:** `capture_backup.py:125-130` (34797ef)
- **What it does:** one failed push, or one longer than 55 s, ends the follower. `run_live.py:102-105` then sends SIGUSR1, the recorder stops with "capture checkpoint publication failed", and the run ends. There is no retry.
- **Smallest fix:** replace the loop body with:
```python
time.sleep(60)
try:
    store.publish(push_seconds=55)
    failures = 0
except subprocess.SubprocessError:
    failures += 1
    if failures >= 3:
        raise
```
  with `failures = 0` before the loop. The 34797ef comment chose to end on the first failure, so this is Greg's call.
- **Certainty:** certain from the code.

**10. [item 1] The checkpoint branch starts from a shallow, blob-less markets-data HEAD.**
- **Where:** `capture_backup.py:43`
- **What it does:** `git switch -c` creates the capture branch on that HEAD.
- **Consequence:** if that commit is no longer an advertised tip at the first push, the push may have to fetch and send every blob. That is the problem 37c5e91 fixed for the run branch, and the 55 s limit would then end the run.
- **Smallest fix:** `git(self.root, "switch", "--orphan", self.branch)`
- **Certainty:** depends on git push behaviour from a shallow clone and on markets-data activity.

**11. [item 1] Each order waits for its own push before the next tick.**
- **Where:** `run.py:325-327`, `journal_publication.py:69-75, 100-107`
- **What it does:** every paper order and fill makes the tick loop wait for that order's markets-data push (25 s timeout, 3 tries).
- **Consequence:** the decision clock falls behind the live feed. The deliveries stay in SQLite.
- **Fix:** no small fix; this is under item 25.
- **Certainty:** certain from the code. The size of the lag depends on GitHub.

**12. [item 1] The new mirror check can end a Sunday run after about an hour.**
- **Where:** `feed.py` (34797ef) runs `verify_queues` at every UTC date change.
- **Consequence:** on a Sunday-evening run the first check is at Monday 00:00 UTC (Sunday 7 pm EST). Any mismatch between the native book and ROOT's book raises, and the session ends with "failure".
- **Certainty:** certain that a mismatch stops the run. Whether a mismatch occurs depends on the data.

**13. [item 1] The cutoff copy opens the live database with a URI that may not be honoured.**
- **Where:** `capture.py:327-328`
- **What it does:** it ATTACHes `file:...?mode=ro` on a connection opened without `uri=True`.
- **Smallest fix:**
```python
with sqlite3.connect(f"file:{short}", uri=True) as db:
```
- **Certainty:** depends on the runner's SQLite being built with `SQLITE_USE_URI`. As far as I know Ubuntu's build sets it.

**14. [item 1] One budget figure is counted two ways.**
- **Where:** `record_mbo.py:77-80` against `session.py:206`
- **What it does:** the recorder counts every delivery, including the replay from Sunday, control records and heartbeats. The session counts MBO positions from 0. The same `--message-budget` goes to both, so the recorder reaches it first.
- **Consequence:** a budget below the week's deliveries so far ends the run during replay or warm-up.
- **Certainty:** certain from the code.

**15. [item 1] Heartbeats may not reset the silence timer.**
- **Where:** `record_mbo.py:65, 170`
- **What it does:** the time of the last delivery is updated only in `Sink.write`.
- **Consequence:** if the client does not pass gateway heartbeats to the stream, 40 s of silence raises "heartbeat timed out". A quiet pre-open or the 5 to 6 pm hour would do it.
- **Certainty:** depends on databento 0.81 stream dispatch.

**16. [item 1] Settings that depend on the account:**
- **Visibility:** `live_ng_paper.yml:48-49` fetches the platform repository anonymously. This depends on the repository being public.
- **Job time:** the clock allows 345 min, then 45 s, up to 480 s, 15 s and the final publish step. The hosted job limit is 360 min; `timeout-minutes: 365` is above it. This depends on how long each part takes.
- **Contract roll:**
  - Where it bites: if `NG.v.0` maps to another contract mid-week, `live_contract.py:22-23` raises CaptureFailure. On a restart, `capture.py:274` raises ValueError. NGZ6 is near expiry this week.
  - Certainty: depends on the roll date and the gateway's mapping.

**17. [item 1] When Greg hears of a failure on his phone.**
- **Notices sent:**
  - The recorder notifies on every exit (`record_mbo.py:243`).
  - `run.py` notifies on refusal and on every stop.
- **No notice of its own:**
  - `run_live.py` sends none on its failure paths:
    - a missing setting (61-65)
    - the contract wait timing out (85-87)
    - a `bind_live_plan` error (93)
  - The restore step's KeyError on a missing `PAPER_CAPTURE_KEY` (workflow lines 66-70).
  - These reach the phone only as a generic "ended: failure", through `run_end_notice.yml`. That only fires if the file is on the default branch, and only when the job ends, so a contract wait that times out is heard after 5.75 h.
- **Silent:** a job skipped because `greg_go` is unticked, the actor differs or `run_attempt` is above 1 (`live_ng_paper.yml:33`), because `run_end_notice.yml:17` excludes `skipped`.
- **Smallest fix:** in `run_live.py:86-87`:
```python
if stopping.wait(0.1) or time.monotonic() >= deadline:
    from .run import notify
    notify("no live NG contract definition before the stop", "preflight")
    return 1
```

## B. Findings on item 9 and the house rules

**18. [item 9] The 60 s and 20 s windows are paper_platform code.**
- **Where:** `inputs.py:12-41`
- **What it does:** `Flow` keeps the span of trades itself and calls only `crypto_ng.tick.line`.
- **What the rule says:** CLAUDE.md amendment G2 permits calling `crypto_ng.tick.reads` and `line` exactly as they are, and copying nothing.
- **What I read:** the semantics match `reads`:
  - The window runs from t−W (excluded) to t (included).
  - Trades leaving at the same nanosecond as an arrival leave first.
  - Only trades with a side are counted.
  - It starts empty at the trade-day open.
- **Windows:** `LEAN_NS` is 60 s and `LINE_NS` is 20 s, imported from `crypto_ng/tick.py:42-43`. The clock is each tick's `ts_recv`, with no time grid. Expiry reads happen through `engine.advance_clock` at the expiry nanosecond.
- **Fix:** either Greg accepts `Flow` as the same formula, or `Flow` is replaced by calls to `reads()` over the trades so far. That is O(n²) per trade day; this is speculation about cost.
- **Certainty:** certain from the code.

**19. [item 9] A one-sided book silently resets the quote runs.**
- **Where:** `inputs.py:77-80`, `unsided_print_rules.py:19-25`
- **What it does:** when one side has no best price, it replaces `QuoteRuns()` and drops all run state, with no record.
- **What ROOT does:** `root/calcs/quote_runs.py:116-118` raises in that case, so live and historical behaviour differ on such a tick.
- **Smallest fix:** keep the state and mark the tick. Replace line 80 with `one_sided = True` (and `one_sided = False` above), and add `one_sided=one_sided` to the returned dict. Whether a rule should reset is Greg's call.
- **Certainty:** certain from the code.

**20. [item 9] Best bid and ask come from Nautilus's book, not ROOT's.**
- **Where:** `nautilus_book.py:56-58`
- **What it does:** the best bid and ask that feed every calculation are read from the native Nautilus book, not from `root/book.py:161-165`. The two books are kept in step through `_join`, `_leave` and `_resize`.
- **Checks:** at 37c5e91 they were compared only at purchased-tape restatements. 34797ef adds a check at each UTC date change.
- **Certainty:** certain from the code.

**21. [item 9] The trade-day gate is re-derived, not called.**
- **Where:** `feed.py:46`
- **What it does:** `in_session = not snapshot and opens <= ts_event < halts` repeats `root.tape.calculation_eligible` (`tape.py:201-206`) for the one named trade day. By reading it is equivalent; the gate function is not called.

**22. [item 1] The trade-day close can fill in the 5 to 6 pm hour.**
- **Where:** `engine.py:225-235`, `paper_execution.py:204-206`
- **What it does:** the trade-day close is decided at the first message with `ts_event` at or after 5 pm ET, which is in the 5 to 6 pm hour. The crossing order goes to the matcher at that message, and the matcher is fed the halted book.
- **Consequence:** a run that spans 5 pm without the clock-stop flatten fills a paper trade in an hour that has no trades. d01b70a records that a run crossing the whole hour is not cut short.
- **Fix:** Greg's call. One option: in `Session.record`, do not submit when `self.last["period"] == STRETCH`, and flatten at the first trade-day message after 6 pm.
- **Certainty:** certain from the code.

**23. [house rule: no trade cost] The fee model is a non-zero model with its fees taken from the contract.**
- **Where:** `paper_execution.py:52`
- **What it does:** `MakerTakerFeeModel()` takes its fees from the instrument. The live values come from the Nautilus Databento decoder, which is not on disk. The NGX3 plan shows "0". Fill events do not emit a commission (`paper_execution.py:84-88`).
- **Smallest fix:** in `bind_live_plan`, `if Decimal(definition["maker_fee"]) or Decimal(definition["taker_fee"]): raise ValueError("fees must be zero")`.
- **Certainty:** depends on the decoder's fee values.

**24. AWS.** No boto3, S3, Bedrock or SageMaker on the path (grep).

## C. Walk of question 1, from the first workflow step to the first decision

1. **Dispatch.** Job condition (line 33): `greg_go`, actor DavisAI1974, attempt 1. Otherwise the job is skipped and no notice goes out.
2. **Start the clock.** Step 1 writes `PAPER_RUN_STARTED_NS`. Everything after it, setup included, counts against the 5.75 h.
3. **Fetch the platform code.** Step 2 does `git init`, then an anonymous fetch of `GITHUB_SHA` (depends on visibility).
4. **Check out markets-data twice.**
   - The `checkpoint` checkout is at HEAD, sparse to `paper-trading/capture-backup`.
   - The `purchased-inputs` checkout is pinned to 46199c5 and sparse to `data/nymex_mbo/ng_v0_oct2023`. It downloads the whole October 2023 archive although the live path reads none of it; it only serves as the data root.
   - Both need `MARKETS_DATA_DEPLOY_KEY` (finding 6).
5. **Install.** Python 3.13, then `requirements.txt`: databento 0.81.0, databento-dbn 0.62.0, nautilus_trader 1.231.0, cryptography.
6. **Restore.** Needs `PAPER_CAPTURE_KEY`, otherwise KeyError. If `ls-remote` finds no branch, it creates `mbo-captures/nymex-ng/<sunday>/live`. On a first run there is no manifest, so nothing is restored.
7. **Start `run_live`.**
   - It checks the budgets are above 0 and that the clock is under 345 min.
   - It requires six variables: `DATABENTO_API_KEY`, `PAPER_CAPTURE_KEY`, `PAPER_RELAY_URL`, `PAPER_RELAY_TOKEN`, `PUSHOVER_APP_TOKEN`, `PUSHOVER_USER_KEY`.
   - It requires `EXECUTION_PLAN`; the default is `ngx3-12be6ea6...json`.
   - The database path is `purchased-inputs/paper-trading/captures/nymex-ng/<sunday>/live.sqlite`.
8. **Start the capture backup follower.** It publishes every 60 s (finding 9).
9. **Start the recorder.**
   - It checks the remote and the Pushover keys.
   - `capture_writer` takes the lock and opens WAL.
   - It writes the ready file with the connection ID, then calls `live()`: `Live(heartbeat 30 s, no reconnect)`, an MBO subscription from Sunday 00:00 UTC and a definition subscription with `start=0`.
   - Silence of more than 40 s raises (finding 15).
10. **Wait for the contract.** `run_live` waits for `definition.dbn` with no limit other than the deadline (findings 1–3).
11. **Bind the plan.** `bind_live_plan` (findings 4, 5) writes `live-ng-plan.json`.
12. **Start `run.py`.**
    - It receives `--data --trade-day --market nymex-ng --message-budget --event-budget --execution-plan <bound> --capture <db> --capture-connection <id> --greg-go`.
    - It checks the relay URL is HTTPS, the credentials, and that the push URL is `git@`.
    - `GET /health` (90 s timeout).
13. **Build the Session.**
    - `clock_stop` sets the stop.
    - It checks the markets-data remote and that the code is committed (`__pycache__` is gitignored).
    - It builds `PaperExecution`.
    - `capture_preflight` (findings 8, 13) runs.
    - `warm_through` is read, then `start.json` is written.
14. **Run the loop.** `GitJournal` and the Render relay start, then the step loop: warm-through, then the first eligible tick, which sets `first_live_decision_cursor`.

## D. Answers to questions 2 to 7

**Q2. The live subscription.**
- It asks for GLBX.MDP3 MBO, symbol `NG.v.0`, `stype_in="continuous"`, `start` Sunday 00:00 UTC. Whether the live gateway accepts continuous symbology depends on Databento.
- The week's book is seated only by replaying from Sunday; there is no seating from a mid-week snapshot (finding 1).
- The contract in the plan is ignored on a live run.
- The matcher's instrument ID is the definition's ID, which must equal the first MBO record's ID (`live_contract.py:33`). A different ID is refused first by `LiveContract.observe` (CaptureFailure) and then by `CapturedFeed` (`capture.py:274`), before `market()`'s own check at `paper_execution.py:208-209`.

**Q3. The contract on a live run.**
- It is built by NautilusTrader's own `DatabentoDataLoader` from the exchange definition record (`live_contract.py:50-58`); it is not typed by hand.
- 150611 and NGX3 are not used: only `plan["rules"]` is taken (line 59). The NGX3 file name survives only as `policy_source`.
- `NautilusMboBook` uses the live MBO ID (`feed.py:22`, `capture.py:272-273`).

**Q4. The calculations and where they come from.**
- **Dipole (60 s) and exhaustion (20 s):** `paper_platform/inputs.Flow`, plus `crypto_ng.tick.line`, `LEAN_NS` and `LINE_NS` (finding 18).
- **Humps:** `paper_platform/claude_rules.py:150-158`, which tracks sign changes. Markets' `root/crypto_ng_tick.whole_humps` is not in this repository.
- **Quote runs:** `root.calcs.quote_runs.QuoteRuns.tick`, called in `inputs.py:78` and `unsided_print_rules.py:28`, with the reset of finding 19.
- **Legs:** `root.calcs.leg_peaks.Legs.trade` and `now`, called on every trade print as ROOT does.
- **Calendar:** `root.calendar` (`trade_day_bounds`, `label`, the settlement constants).
- **Book:** `root.book.Book`, subclassed in `paper_platform/nautilus_book.py`; best prices are read from the native book (finding 20).
- **Mid price:** none is formed on the live path. `crypto_ng.half_spread_bps` uses one but is not called.
- **ROOT itself:**
  - Diff against main is not possible: the clone is shallow at 902d6e8 and has no main ref. No commit after 902d6e8 touches `root/` or `crypto_ng/`.
  - Byte comparison with `/home/user/Markets`, which is at 537749a (a Markets session checkout, not a confirmed trunk), shows these files identical: `crypto_ng/tick.py` and `__init__.py`; `root/calendar.py`, `book.py`, `tape.py`, `outside.py`; and `root/calcs/{quote_runs, leg_peaks, in_play, flow_peak, peak_links, peak_story}.py`.

**Q5. Ticks outside the trade day.**
- **Before 6 pm ET the evening before:** `in_session` is False and the engine makes no decision. The matcher still receives the tick.
- **5 to 6 pm hour:** the inputs ignore it; the first such message ends the trade day. The matcher receives it (finding 22).
- **Settlement window (2:28–2:30 pm ET):**
  - CL closes are deferred.
  - CX observations are interrupted, and their open trades become unmonitored (this is under item 2).
  - New CL arms are refused (`claude_rules.py:296`) and no CX entries are taken (`self.p = None`).
  - The matcher keeps matching, including resting post orders.
- **After the trade day:** `engine.ended` is set and no decisions are made. The matcher keeps receiving every message until the run stops.
- `market()` gates only vendor snapshots, so the matcher sees all of the above.

**Q6. "No real money, no real orders".** No order-entry client, broker or tastytrade code is on the path. The HTTP posts go only to Pushover and to the Render journal. The git pushes go to markets-data. Databento is subscribe-only. Matching is the in-process `OrderMatchingEngine`.

**Q7. The warm-up.**
- `execution.market(message)` runs at `session.py:303-304`, before the warm branch at 308, so the matcher receives every warm-up message.
- The warm-up decisions from `engine.tick` are discarded (line 312), and `open`, `unmonitored`, `managers` and `responses.pending` are cleared. No order is submitted, so no resting paper order can exist from the warm-up.
- The timer path at lines 288-291 finds nothing to close, because those collections are cleared after each warm tick.
