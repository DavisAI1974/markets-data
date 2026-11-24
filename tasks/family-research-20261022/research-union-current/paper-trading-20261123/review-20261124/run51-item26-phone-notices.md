# Run 51: every stop and failure path traced to the phone; every Pushover and Render name

The agent's own report, word for word, as it came back to the session (session_017eY1WPw7p6f6Tyx49EyYD4, 2026-11-24). It is a reading of code and documents. Nothing was run. What was done with each finding is under the item's number in the platform checklist and in agent-runs.jsonl.

---

Everything below is from reading files only. Nothing was run, parsed, tested or sent, and no file was changed.

Path abbreviations (all absolute):
- W = /home/user/paper-trading-platform/.github/workflows
- P = /home/user/paper-trading-platform/paper_platform
- D = /home/user/paper-trading-platform/docs/platform

Not determinable from the repository, flagged where used:
- GitHub's value set for `conclusion`, and whether an all-jobs-skipped run concludes `skipped`.
- How GitHub delivers a cancel signal and how long it waits.
- Which branch is the default. The clone holds only `codex/strategy-trades-and-mbo-capture`.
- Whether Render reads a blueprint outside the repository root, its default Python version, and its free-plan idle behaviour.
- Whether any secret or variable exists. D/OWN_PLATFORM_WISHLIST_20261123.md:131 says "The repository has the two Pushover secret names configured"; that is a statement in a document.

## 1. run_end_notice.yml

**Trigger** (W/run_end_notice.yml:2-9): `workflow_run`, `types: [completed]`, no branch filter. The four listed names are character-for-character identical to the `name:` lines:

| List line | Entry | `name:` line |
| --- | --- | --- |
| :5 | `Live NG MBO paper session` | W/live_ng_paper.yml:1 |
| :6 | `Purchased NG MBO paper replay` | W/purchased_mbo_paper.yml:1 |
| :7 | `Record NG MBO and persist checkpoints` | W/record_ng_mbo.yml:1 |
| :8 | `Budgeted agent run` | W/agent_run.yml:1 |

A trailing-whitespace search of the workflows folder found one hit, W/verify_paper_platform.yml:70 (`path: `), and none on a name or list line.

**Conclusions acted on** (:14): `if: ${{ github.event.workflow_run.conclusion != 'success' && github.event.workflow_run.conclusion != 'skipped' }}`. Every conclusion other than those two sends a notice.

**Permissions** (:10): `permissions: {}`. There is no checkout and no token use.

**Secrets** (:19-20): `PUSHOVER_APP_TOKEN` and `PUSHOVER_USER_KEY`. The workflow name, run number and conclusion pass through `env` (:21-23), not into the script text.

**Request** (:25-29): a multipart POST to `https://api.pushover.net/1/messages.json` with three fields:
- `token`
- `user`
- `message=NG Actions run $WORKFLOW #$RUN_NUMBER ended: $CONCLUSION`

There is no title, priority, url or device. The runner's sender (P/run.py:29-37) posts the same three fields form-encoded.

**curl flags**:
- `--fail` gives a non-zero exit on HTTP 400 and above, so an HTTP error is not hidden.
- `--silent --show-error` with `> /dev/null` discards Pushover's JSON reason, so the log would show the status code only.
- `--max-time 5` is the only time limit, and there is no `--retry`.

**Parsing**: I found nothing in indentation, the `${{ }}` expression, the quoting or the `#` inside double quotes that would stop it reading as a workflow. No parser was run.

**Run-time conditions**:
- There is no guard for an unset secret, so an empty `token=` or `user=` field is sent. If Pushover answers 4xx (not determinable here), curl exits 22, the job fails and no notice arrives. Nothing watches this workflow.
- It uses the same two secrets and the same endpoint as the runner, so one missing secret silences both senders.
- D/OWN_PLATFORM_WISHLIST_20261123.md:133: "GitHub starts it only from the default branch, so it takes effect after merge."
- All four listed workflows have one job gated by `inputs.greg_go && … && github.run_attempt == 1` (live:32, purchased:46, record:28, agent:37). Per the comment at :13 such a run is skipped, so a re-run or a run without the go sends nothing.
- W/live_ng_paper.yml:27-29 and W/record_ng_mbo.yml:23-25 share the group `ng-capture-live` when the source is live. A queued run that GitHub cancels would produce "ended: cancelled" without having started.

**Workflows not covered**:
- W/compare_recorded_replay.yml:1 `Compare live and replay strategy journals`
- W/verify_paper_platform.yml:1 `Verify paper platform on purchased MBO`
- W/restore_phone_dashboard.yml:1 `Restore phone dashboard from a published run`
- W/run_end_notice.yml:1 `Phone notice for a run that ended without success` (itself)

## 2. The runner's own notices

**Sender**: `notify(reason, run, *, activity="paper run")` at P/run.py:28-39.
- Message: `f"NG {activity} {run}: {reason}"`.
- `timeout=5`, no retry.
- A non-OK reply raises `RuntimeError("phone notice delivery failed")`; the status code and body are dropped.
- Callers: run.py:299, :372, :391; run_live.py:55; record_mbo.py:227; agent_launcher.py:106.

**Mechanism in run.py**: `Session.stop` sets `self.stopping` (P/session.py:350) for whatever reason it is given. The worker (run.py:296-302) waits on it and sends `notify(s.stop_notice(), s.run)`. So every `Session.stop` inside `paper_platform.run` gives one notice, normal ends included.

**Notice text** (session.py:318-325): the state string, with two changes.
- `"flattened at the 5.75-hour stop"` becomes `"5.75-hour stop reached"`.
- When `capture_end` is set, `. Last recorded MBO X. Last processed Y.` is appended.

**Reasons passed to `Session.stop`**:

| Reason | Where |
| --- | --- |
| `"flattened at the 5.75-hour stop"` (P/run_clock.py:8) | session.py:199, :250, :276; via `due()` :188 at :215, :225, :241; run.py:293; run.py:319 then :362 |
| `"budget reached"` | session.py:203, :210, :287; via `due()` :190 at the same call sites |
| `"failure"` | session.py:230, :303; run.py:228 then :362 |
| `"end of capture"` / `"end of purchased input"` | session.py:253 |
| the original receipt's status (`message["recorded_stop"]`) | session.py:265 |
| `"markets-data snapshot failed"` | run.py:281 |
| `"markets-data publication failed"` | journal_publication.py:142 |
| `"run stopped"` | run.py:316 then :362 |
| `"session stopped"` and `due()` reasons | api.py:39, :49 |
| `"end of offline verification"` | test_ledger.py:117 |

- On a receipt-based replay (session.py:265) the notice repeats the original run's reason.
- `application` in api.py has no caller and no `notify`, so those two stops send nothing.

**`stop_capture`** is called at session.py:247, :263 and run.py:290. The reason is the clock stop when the status is `"clock limit"`, otherwise `"capture: " + status` (session.py:314-315). Status values:
- From record_mbo.py:221: `"end of purchased input"`, `"message budget reached"`, `"clock limit"`, `"capture stopped"`.
- `"interrupted"` (capture.py:102, :107).
- `"recorder exited without a terminal record"` (capture.py:149).
- `"capture journal unreadable"` (run.py:288).
- `CaptureFailure` texts:
  - `"live feed disconnected"`
  - `"live feed heartbeat timed out"`
  - `"Databento feed error N"`
  - `"live DBN write failed"`
  - `"live feed closed with an error"`
  - `"capture checkpoint publication failed"`
  - `"replayed MBO differs at position N"`
  - `"source ended before the stored prefix at position N"`

**Paths in run.py**:
- **Before the `try`** (run.py:191-224): no notice. This covers every `p.error`, including `"Render must use an HTTPS URL"` (:216-217, reached when `vars.PAPER_RELAY_URL` is empty) and `"required run credential missing: "` (:218-220), plus a git error in `writer_remote`.
- **Inside the `try`, before the Session exists** (:230-253): the clock check, the `/health` GET at :232, the receipt and plan read, and `Session.__init__` with its preflight. The finalizer sends `notify(why, "preflight")` at :372.
  - `why` is `"failure"` by default.
  - It is the deadline text for `PreflightDeadline` (:344-345).
  - It is `"capture: <status> (connection N, last MBO M)"` for `CaptureEnded` under `--capture` (:348-352).
  - A `/health` failure reads only "NG paper run preflight: failure".
- **Signal handlers** are installed at :268-269, after the Session and preflight. Before that, SIGTERM has its default action and no handler runs.
- **Session exists, worker not yet started** (:254-303): `s.stop("failure")` at :362, then a synchronous notice at :371-372.
- **Worker started but not sent**: the finalizer joins it at :368-369. If the process is killed, nothing is sent by the runner.
- **Relay delivery failure mid-run** (:104, :124, or a `requests` exception with `timeout=8`): `why` stays `"failure"`, so the notice is "NG paper run <run>: failure" with no cause. The final delivery is retried at :376-377. If that also fails, `"relay"` is added and a second notice is sent.
- **Journal publisher failure**:
  - The worker stops the session (journal_publication.py:142), giving the notice "markets-data publication failed".
  - The finalizer then adds `"git"` (:381) or `"live Git delivery (final journal recovered)"` (:383-384).
  - That gives a second notice and a `RuntimeError`.
  - A minute-snapshot `OSError` gives "markets-data snapshot failed" (:281) and follows the same finalizer branch.

**A failed notice request is handled four ways**:
- **run.py**:
  - The worker swallows it with `pass` (:301-302), unlogged.
  - The finalizer tries once more (:370-374).
  - On a second failure `"phone"` is added and a third send with different text is tried and swallowed (:389-393).
  - `raise RuntimeError("shutdown failed: …")` at :394 is inside `finally`. It replaces any in-flight exception and turns an otherwise exit-0 stop into a failed job.
- **record_mbo.py:226-227**: a bare `notify` in `finally`, with no catch and no retry. A failure replaces the `CaptureFailure`. On a clean stop it makes the recorder exit non-zero, which makes run_live.py:106 return 1.
- **run_live.py:55**: bare.
- **agent_launcher.py:105-108**: caught and appended to the errors, no retry; then `SystemExit` at :186-187.

**Recorder (record_mbo.py)**:
- No notice before :203: `parser.error` at :189-190, :195, :201-202.
- From :203 the `finally` at :227 sends "NG MBO capture nymex-ng/<sunday>/<source>: <outcome>" at every end, clean ones included.
- `outcome` is `"capture failure"` for any exception that is not a `CaptureFailure`, for example a missing `DATABENTO_API_KEY` (:130-131).
- Its handlers are installed at :210-212, inside the writer.

**Checkpoint publisher (capture_backup.py)**:
- It has no `notify`, and run_live.py:69-70 passes it only `PAPER_CAPTURE_KEY`.
- In the live workflow its death sends SIGUSR1 (run_live.py:91). The recorder notice reads "capture checkpoint publication failed" and the runner notice "capture: capture checkpoint publication failed. …".
- In the record-only workflow its death leads to `kill -TERM` (W/record_ng_mbo.yml:76), so the recorder notice reads "capture stopped".
- The steps "Restore the last published capture checkpoint" and "Persist the final committed deliveries" send nothing themselves.

**run_live.py** notifies only at :55. It sends nothing of its own on:
- `parser.error` at :48-49;
- `return 1` at :75 and :80;
- `RuntimeError("capture stopped before opening a new connection")` at :77;
- the 120-second paper wait expiring at :102-105.

## 3. Names

| Name | Read at | Declared at |
| --- | --- | --- |
| `PUSHOVER_APP_TOKEN` | run.py:32, :218; record_mbo.py:201; agent_launcher.py:130; filter at run_live.py:20-21, :64 | Actions secret in live_ng_paper.yml:75, purchased_mbo_paper.yml:131, record_ng_mbo.yml:64, agent_run.yml:65, run_end_notice.yml:19 |
| `PUSHOVER_USER_KEY` | run.py:33 and the same check sites | :76, :132, :65, :66, :20 of the same files |
| `PAPER_RELAY_URL` | run.py:215; restore_view.py:79 | Actions **variable** `vars.PAPER_RELAY_URL` in live_ng_paper.yml:72, purchased_mbo_paper.yml:129, restore_phone_dashboard.yml:40 |
| `PAPER_RELAY_TOKEN` | run.py:63, :218; restore_view.py:84; relay.py:35; filter at run_live.py:20, :84 | Actions secret in live:73, purchased:130, restore:41; P/render.yaml:12-13 (`sync: false`) |
| `PAPER_VIEW_PASSWORD` | relay.py:34 | P/render.yaml:10-11 (`sync: false`) |
| `PAPER_RELAY_DB` | relay.py:39, default `/tmp/ng-paper-events.sqlite` | nowhere except test_viewer.py:27 |
| `PORT` | P/render.yaml:7 | supplied by Render; not read in code |

- No name is spelled differently in two places.
- `PAPER_RELAY_DB` is the only name read but declared nowhere. No name is declared but never read.
- P/README.md:37 lists the four runner names and says "Set values in the service secret stores". The workflows read `PAPER_RELAY_URL` from `vars`, not `secrets`; D/OWN_PLATFORM_WISHLIST_20261123.md:135 says "the variable". Stored as a secret it would arrive empty and end at run.py:216-217.
- The dashboard user name `greg` is fixed in relay.py:38.
- relay.py:36-37 refuses to start if the two Render values are empty or equal.
- Other names read, outside Pushover and Render:
  - `PAPER_CAPTURE_KEY`
  - `DATABENTO_API_KEY`
  - `MARKETS_DATA_TOKEN`
  - `MARKETS_DATA_DEPLOY_KEY`
  - `ANTHROPIC_API_KEY`
  - `PAPER_RUN_STARTED_NS`
  - `EXECUTION_PLAN`

## 4. render.yaml

**The blueprint** (P/render.yaml:1-13):
- `type: web`, `name: ng-paper-viewer`, `runtime: python`, `plan: free`.
- `buildCommand: pip install -r paper_platform/requirements-viewer.txt`.
- `startCommand: python -m uvicorn paper_platform.relay:relay --factory --host 0.0.0.0 --port $PORT`.
- `healthCheckPath: /health`.
- Two `envVars`, both `sync: false`.

**Absent**: `rootDir`, `region`, `disk`, `branch`, any Python version. There is no `.python-version` or `runtime.txt` in the repository; the workflows pin Python 3.13.

**Against the code**:
- `relay` is a factory function (relay.py:33) returning the app (:346), which matches `--factory`.
- Both commands use paths from the repository root, consistent with no `rootDir`.
- `/health` exists unauthenticated (relay.py:75-77) and is the route the runner calls (run.py:232).
- The port is taken by uvicorn only.
- Events go to a SQLite file at `PAPER_RELAY_DB`, default `/tmp/…` (relay.py:39), with tables created at start (:44-65). No disk is declared; P/README.md:37 says "Render's SQLite cache is ephemeral."
- P/requirements-viewer.txt holds `fastapi==0.115.0` and `uvicorn==0.41.0`. The modules relay.py imports (rulebook, market, trades, views) import only the standard library.
- views.py:31 and :161 use `ZoneInfo("America/New_York")`; no `tzdata` is listed.

**Differences found**:
- The file is at `paper_platform/render.yaml`, not the repository root.
- No Python version is given, while relay.py uses `str | None` annotations (for example :142).
- `PAPER_RELAY_DB` is not declared.

## 5. Runner to Render

**Sender**: `Publication` in run.py.
- Header: `Authorization: Bearer <PAPER_RELAY_TOKEN>` (:62-63).
- One event: POST `{url}/ingest` (:87-89).
- Up to 128 events: POST `{url}/ingest/batch` (:110, :116-118).
- Both use `timeout=8` and `allow_redirects=False`.
- Body: `{"event": …, "status": …}` (:128-143).
- Called from `deliver()` (:310-312) in the main loop (:321), from `pace_to_record` (:167-168), and once more at shutdown (:376-377).

**Receiver**:
- relay.py:115-119 `/ingest` and :121-127 `/ingest/batch`.
- Both depend on `authorize_writer` (:79-81), which compares the whole header with `"Bearer " + writer` and otherwise returns 403.
- The batch limit of 128 (relay.py:30) matches the sender.
- restore_view.py:83-86 uses the same route and header.

**When Render is unreachable**:
- **At start**: one `requests.get(url + "/health", timeout=90).raise_for_status()` (run.py:232). On failure no Session is made, the notice is "preflight: failure", and the process ends with the exception.
- **Mid-run**: the first failed POST raises. There is no retry in run.py; restore_view.py:49-63 has four attempts with backoff. The run stops with state `"failure"` and goes through `Session.stop`. It does not wait and does not go on.
- **Render restarted with an empty database**: the relay answers 409 with `{"next": expected}` (relay.py:104-107). The runner re-posts the journal from that sequence (run.py:90-102, :119-122).
- **At shutdown**: relay delivery and git publication are attempted independently (run.py:376-388).
- No keep-alive request exists. POSTs happen only when events are pending.

## 6. Double and missed notices

Counts follow from the lines cited. The "Actions" column applies only once run_end_notice.yml is on the default branch.

| Scenario | Recorder | Runner | "failure during shutdown" | Actions |
| --- | --- | --- | --- | --- |
| Purchased replay ends (input end, budget, 5.75-hour stop), no shutdown errors | – | 1 | – | none (job success) |
| Purchased replay, exception mid-run | – | "failure" | 1 if any shutdown error | "ended: failure" |
| Any stop with shutdown errors or incomplete clock-stop liquidation (run.py:364) | – | 1 | 1 | "ended: failure" |
| Live, 5.75-hour stop | "clock limit" | "5.75-hour stop reached" | – | none (run_live.py:106 returns 0) |
| Live, event budget in runner | "capture stopped" | "budget reached" | – | none |
| Live, message budget in recorder | "message budget reached" | "capture: message budget reached. …" | – | none |
| Live, feed failure | failure text, non-zero exit | "capture: <text>. …" | – | "ended: failure" |
| Agent run completed | – | "NG agent run <run>: completed" | – | none |
| Agent budget stop, run stop or failure (agent_launcher.py:184-187) | – | 1 | – | "ended: failure" |
| Step fails before the runner, job timeout, lost runner | – | – | – | 1 |
| Cancelled by hand | see below | see below | – | "ended: cancelled" |

- **Runner reports a failure and the job fails**: Greg receives the runner's notice or notices plus the Actions notice. The runner's text carries the 32-hex run id (session.py:55); the Actions text carries the workflow name and `run_number`. There is no shared identifier.
- **Cancelled by hand**:
  - If SIGINT or SIGTERM reaches the Python process, run.py sends "run stopped" (:268-269, :316) and the recorder sends "capture stopped" (record_mbo.py:211).
  - run_live.py then waits up to 45 s (:95) and 120 s (:102).
  - Only W/record_ng_mbo.yml:71 has a `trap` that forwards the signal. In live_ng_paper.yml:77-79, purchased_mbo_paper.yml:143 and agent_run.yml:73, Python is a child of the step's shell with no `trap` or `exec`.
- **5.75-hour stop with job success**: a "run stop" notice is sent by the runner ("NG paper run <run>: 5.75-hour stop reached"), and in the live workflow also by the recorder. The Actions notice job does not send.
- **Missed entirely**:
  - any `p.error` exit when the cause is a missing Pushover secret (both senders share it);
  - a skipped run;
  - the three uncovered workflows;
  - a failure of run_end_notice.yml itself;
  - everything in the "Actions" column until merge.

## What is not wired

1. **run_end_notice.yml is not active on this branch.** A setting (merge to the default branch), no line.

2. **Whether the secrets and variable exist.** Settings, no line:
   - Actions secrets `PUSHOVER_APP_TOKEN`, `PUSHOVER_USER_KEY`, `PAPER_RELAY_TOKEN`.
   - Actions variable `PAPER_RELAY_URL`.
   - Render values `PAPER_VIEW_PASSWORD`, `PAPER_RELAY_TOKEN`.

3. **Three workflows are outside the notice list.** After W/run_end_notice.yml:8:
   ```
         - Compare live and replay strategy journals
         - Verify paper platform on purchased MBO
         - Restore phone dashboard from a published run
   ```

4. **No guard for an unset secret and no retry in the notice step.** Before W/run_end_notice.yml:25:
   ```
             : "${PUSHOVER_APP_TOKEN:?PUSHOVER_APP_TOKEN is not set}" "${PUSHOVER_USER_KEY:?PUSHOVER_USER_KEY is not set}"
   ```
   and on :25:
   ```
             curl --fail --silent --show-error --max-time 5 --retry 3 --retry-delay 2 \
   ```

5. **`PAPER_RELAY_DB` and a Python version are not in the blueprint.** Under `envVars` in P/render.yaml:
   ```
         - key: PAPER_RELAY_DB
           value: /tmp/ng-paper-events.sqlite
         - key: PYTHON_VERSION
           value: <a full 3.13 version string>
   ```
   The version value is a placeholder; the form Render accepts was not checked. The file location is either a move to the repository root or a path entered on Render, which is a setting.

6. **A publisher death in the record-only workflow is reported as "capture stopped".** Replacing W/record_ng_mbo.yml:76:
   ```
               if [[ "${finished:-}" == "$backup_pid" ]]; then kill -USR1 "$recorder_pid" 2>/dev/null; else kill -TERM "$recorder_pid" 2>/dev/null; fi
   ```
   record_mbo.py:212 already turns SIGUSR1 into "capture checkpoint publication failed".

7. **The worker's failed notice attempt leaves no trace.** Replacing P/run.py:301-302:
   ```
               except (requests.RequestException, RuntimeError) as error:
                   print("phone notice attempt failed: " + type(error).__name__, flush=True)
   ```

8. **The recorder's notice failure replaces the capture error and its exit status.** Replacing P/record_mbo.py:227:
   ```
           try:
               notify(outcome, f"{profile['id']}/{sunday}/{args.source}", activity="MBO capture")
           except (requests.RequestException, RuntimeError) as error:
               print("phone notice not delivered: " + type(error).__name__, flush=True)
   ```
   This needs `import requests` at the top of the file.

9. **A cancel signal has no forwarding in three workflows.** Prefix the Python command with `exec` at each of these lines:
   - W/live_ng_paper.yml:78 (`exec python -m paper_platform.run_live …`)
   - W/purchased_mbo_paper.yml:143
   - W/agent_run.yml:73

   Whether this is sufficient depends on GitHub's cancel behaviour, which was not checked.

10. **run_live.py exits without a notice of its own** at :48-49, :75, :77, :80 and :104-105. For the last one, before `return 1` at :105:
    ```
                    from .run import notify
                    notify("paper runner did not finish within 120 seconds", "live")
    ```

11. **The first failure notice carries no cause**, for example a Render outage. `why` is set only for `CaptureEnded` (run.py:347-352). `why` also becomes the receipt status (session.py:349, :378), which receipt replay reuses (session.py:265). So a line here changes recorded data; none is offered.

12. **Relay posts in run.py have no retry and no keep-alive.** The retry pattern in the repository is restore_view.py:49-63. Whether the run should stop, wait or go on when Render is unreachable is recorded nowhere in the files read; the code as written stops.
