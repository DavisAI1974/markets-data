# Run 55: items 24 and 25, the real-time phone view and git publication: every way an event could fail to reach the phone or the git record

The agent's own report, word for word, as it came back to the session (session_017eY1WPw7p6f6Tyx49EyYD4, 2026-11-24). It is a reading of code and documents. Nothing was run. What was done with each finding is in README.md beside this file and under the item's number in the platform checklist.

---

Review of wishlist items 24 and 25, done by reading only. Repository: /home/user/paper-trading-platform, branch codex/strategy-trades-and-mbo-capture.

**How this was done**
- The branch tip moved while I was reading, from e12bfde to de048e0 (three new commits). I re-read the diffs for run.py, session.py, views.py, paper_execution.py, run_live.py, restore_view.py, the action and the two runner workflows. All line numbers below are at de048e0.
- I broke the no-run rule once: one `python3 -c` that printed the fields of paper_platform/markets/nymex-ng.json. It ran no platform code. Nothing else was run: no tests, no network, and not the grounding tool.
- Everything below comes from reading the code.

## Findings that would stop item 25 from publishing at all (they depend on git and on the remote, not readable here)

**1. [25] The first commit sits on top of a pinned commit in a shallow, blob-less checkout.**
- Where: journal_publication.py:115-118 and 121-126, push at :103.
- What the code does: the run branch's first commit has `46199c5f…` as its parent. Both runner workflows fetch that commit with `--depth=1 --filter=blob:none` plus a sparse cone. Its whole tree is read into a fresh index (no skip-worktree bits), and the result is pushed by URL to a new `paper-runs/<run>` ref.
- Risk at `write-tree` (:121): it has no `--missing-ok`. In a repo with a promisor remote, git verifies or prefetches every blob in that index outside the sparse cone (in the live workflow, everything except data/nymex_mbo/ng_v0_oct2023). That has to finish inside the 25 s limit at run.py:80.
- Risk at the first push (:103): if `46199c5f` is not the tip of any branch markets-data advertises at run time, git cannot exclude it. The pack must then hold that commit's whole tree, and its blobs are not on the runner.
- Either failure costs 3 tries at up to 25 s each. The worker then fails on the "start" cut and the run stops as "markets-data publication failed" before the first tick.
- Contrast: capture_backup.py:37-43 and 98-104 commit from a sparse checkout of the fetched tip using `git add`/`commit`.
- verify_paper_platform.yml:77 uses `push --dry-run`, which as I understand git does not build or send a pack, so it would not catch this.
- Fix (smallest): make the run branch an orphan holding only the run folder. In `_publish`:
  ```python
          if self.commit is None:
              self.git("read-tree", "--empty")
              self.commit = ""
  ```
  and at :124-126:
  ```python
              parent = ("-p", self.commit) if self.commit else ()
              self.commit = self.git("-c", "user.name=NG Paper Recorder", "-c",
                                     "user.email=paper@users.noreply.github.com", "commit-tree",
                                     tree, *parent, "-m", message, read_output=True)
  ```
  start.json already records `data_commit`, so the data lineage is kept. The replay and restore workflows read only `paper-trading/<run>` from that branch.
- Status: depends on git's `write-tree` and `push` behaviour in a partial clone, on the git version, and on whether `46199c5f` is a branch tip in markets-data. None of that is readable here.

## Item 25 findings, certain from the code

**2. [25] In live capture mode, orders and fills made by a timer are not pushed before the next tick is admitted.**
- Where: session.py:278-281.
- What the code does: inside `step()`, due timers run `advance_clock` (signals, paper orders, fills, each queued as a cut). The same `step()` then admits the message, with no `wait_for_orders` in between. run.py:336-340 calls `deliver()` only between steps.
- The replay path (`pace_to_record`, run.py:166-169) does call `deliver()` after each timer.
- Fix: hold the message and return after one timer.
  - Add `self.held = None` in `__init__`.
  - At :251:
    ```python
                    message = self.held if self.held is not None else next(self.stream, None)
                    self.held = None
    ```
  - Replace :278-281:
    ```python
                        if (expiry := self.engine.next_expiry_ns) is not None and expiry < received:
                            self.advance_clock(expiry)
                            if self.state == "active":
                                self.held = message
                                return {"timer": expiry}
                            return None
    ```
  - run.py:338 is unchanged; a non-None return skips the 0.1 s wait.
- Receipt replay should be checked against this change. I could not run it.

**3. [25] Only "paper order" and "fill" get their own immediate commit.**
- Where: journal_publication.py:58.
- What the code does: "order status" events (cancel, reject, "No bid for post order", "order tag already used; not sent", "observation ended with paper exposure"), signals and the start/stop status ride on the next order, fill, minute or final commit.
- Whether order status counts as "order" in "at once on every order and fill" is Greg's reading.
- Fix if it counts: `if event["kind"] in ("paper order", "fill", "order status"):`

**4. [25] Minute snapshots: what the clock does.**
- The clock is the runner's monotonic clock: journal_publication.py:35, :63, :68. It is driven by the watchdog every 0.25 s (run.py:293), only while the session is active.
- A cut is queued every minute. But :122 makes no commit when the tree has not changed. So a minute with no new events.jsonl or receive-ns bytes (the 17:00-18:00 stretch, a feed gap, the recorder idle) pushes nothing and leaves no trace.
- Line 68 jumps `next_minute` over missed minutes with no record.
- Commit time is when the worker made the commit, not when the cut was taken. Under a push backlog, minute commits bunch together and the cut instant is recorded nowhere.
- Fix:
  - Add `cut_ns: int` to `JournalCut`.
  - At :48: `cut = JournalCut(trigger, s.events - 1, sizes, time.time_ns())`
  - At :123: `message = f"Paper {cut.trigger} through journal sequence {cut.sequence} at {cut.cut_ns} ns [skip ci]"`
  - At :122, if Greg wants a commit every minute even with no new bytes: `if tree != self.tree or cut.trigger == "minute":`
  - At :67, to name skipped minutes: `self._enqueue("minute" if now - self.next_minute < 60 else f"minute ({int((now - self.next_minute) // 60)} missed)")`

**5. [25] Race on the recorded stop reason.**
- Where: journal_publication.py:139-142.
- What the code does: the worker sets `error` and wakes waiters before it calls `session.stop(...)`. The main thread wakes in `wait_for_orders`, raises, and the finalizer (run.py:377) calls `s.stop(why)` with `why == "failure"`.
- Whichever thread gets `session.lock` first writes the status and the receipt. The journal can say "failure" instead of "markets-data publication failed".
- Fix: stop first, then publish the error.
  ```python
          except Exception as error:
              try:
                  self.session.stop("markets-data publication failed")
              finally:
                  with self.progress:
                      self.failed_cut, self.error = cut, error
                      self.progress.notify_all()
  ```

**6. [25] Failure reporting.**
- run.py:78 sends git's stderr to DEVNULL. A rejected or failed push surfaces only as "markets-data git push failed", with no cause.
- The receipt is written at session.py:400, before any final push, and has no publication field.
- If only the final push fails, the remote stops at the last "through journal sequence N" commit and holds no receipt. The runner's files are discarded with the job. The phone gets "failure during shutdown: git" with no sequence.
- Fix, run.py:78 and :82-83:
  ```python
              stderr=subprocess.PIPE,
  ...
          if proc.returncode:
              detail = (proc.stderr or "").strip().splitlines()[-1:]
              raise RuntimeError("markets-data git " + args[0] + " failed" + (": " + detail[0] if detail else ""))
  ```
  This is safe: the token travels in GIT_CONFIG_VALUE_0 as a header, not in the URL.
- Fix, run.py:396 and :399: report `f"git (markets-data holds journal through sequence {journal.published_sequence})"`.

**7. [25 and 24] `wait_for_orders` has no state check.**
- Where: journal_publication.py:70-77.
- What the code does: it waits only for the publish or an error, and each failing cut can take about 78 s (3 tries, 25 s each, plus 1 s and 2 s sleeps).
- Effect: a watchdog stop, or SIGTERM from run_live, during a slow push does not wake the main thread. The flatten orders, fills and terminal status reach Render only after that push resolves.
- Fix:
  ```python
          target = self.required_sequence
          with self.progress:
              while not self.progress.wait_for(
                      lambda: self.error is not None or self.published_sequence >= target, timeout=0.25):
                  if self.session.state != "active":
                      return
              if self.error is not None:
                  raise RuntimeError("markets-data publication failed") from self.error
  ```

## Item 24 findings

**8. [24] Times on the page do not name the trade day. Certain from the code.**
- At de048e0, trade-row times name it (views.py:31-42). The event cards and header do not:
  - views.py:191 prints the journal time as a bare Eastern clock date. That time is the runner's clock (`time.time_ns()`, session.py:160), which for an archive replay is today's date, not the tape's.
  - views.py:203-208 shows the tape receive time only as raw nanoseconds.
  - monitor.html:15 / views.py:320 and monitor.html:47 show the trade day as an unlabelled date.
  - views.py:252 does the same in the run history.
- Fix:
  - Move the body of `time_at` (views.py:31-42) to a module function `eastern_time(ns)`, and let `time_at` return `eastern_time(event.get("fill_received_ns", event["received"]))`.
  - views.py:189-191: `fields.append(f"<small>Journal (runner clock) · {eastern_time(event['recorded_ns'])}</small>")`
  - After the loop at :206-211: `if event.get("received") is not None: fields.append(f"<small>{time_label.removesuffix(' (ns)')} · {eastern_time(event['received'])}</small>")`
  - views.py:320: `trade_day=e(f"trade day {state['trade_day']}" if state.get("trade_day") else "")`
  - monitor.html:47: `document.getElementById('trade-day').textContent=row.trade_day ? 'trade day '+row.trade_day : '';`
  - views.py:252: `+ (e("trade day " + day) + " · " if day else "")`

**9. [24] Render posts have no retry. Depends on Render's free plan, not readable here.**
- What the code does: every post uses an 8 s timeout and no retry (run.py:88, 118, 147). Any timeout or a 5xx raises and stops the run as "failure".
- render.yaml sets `plan: free`, and the store is `/tmp/ng-paper-events.sqlite` (relay.py:39).
- If Render sleeps the free service after idle time, the next event after a quiet stretch (for example the 17:00-18:00 stretch with no phone open) meets a cold start longer than 8 s. The restart also empties the store.
- Fix (code): reuse restore_view.py:49-63 as `Publication.post`, with timeout (10, 30) and up to 4 tries on ConnectionError, Timeout, 429 and 502-504, and use it at the three post sites. A repeat is safe because relay.py:100-103 accepts an identical body for an existing sequence.
- Fix (hosting, Greg's call because it costs money): `plan: starter` with a persistent disk, and `PAPER_RELAY_DB` on that disk.

**10. [24] The 409 refill sends one HTTP request per event on the main thread. Certain from the code.**
- Where: run.py:97-101.
- What the code does: after an empty-store restart, the whole run so far is re-posted one event at a time, each with up to 8 s, while no tick is admitted. A run with thousands of events stalls for minutes.
- Fix: replace :97-102 with
  ```python
                  with (self.s.folder / "events.jsonl").open(encoding="utf8") as f:
                      missing = [row for row in map(json.loads, f) if target["next"] <= row["sequence"] <= event["sequence"]]
                  for start in range(0, len(missing), 128):
                      chunk = missing[start:start + 128]
                      response = self.http.post(self.url + "/ingest/batch", json={"packets": [self.packet(row) for row in chunk]},
                                                timeout=8, allow_redirects=False)
                      if response.status_code != 200 or response.json().get("next") != chunk[-1]["sequence"] + 1:
                          raise RuntimeError("Render journal recovery failed")
                  return
  ```

**11. [24] Stop events reach the page after the phone notice. Certain from the code.**
- What the code does: run.py:107 stops main-loop delivery once the session is not active. The stop's events are posted only at run.py:392, after `watcher.join()` (:373), `notice_worker.join()` (:384) and the retry `notify` (:387). Each Pushover call has a 5 s timeout.
- Fix: submit the final relay delivery right after the `s.stop(why)` block (after :382), before `notice_worker.join()`. Collect its result where :401 does now. The notice is not delayed by this.

**12. [24] Smaller page items.**
- A paper order with no execution plan (`pricing="open"`, session.py:181-182) shows no side or quantity, because views.py:171 requires `placement`. Fix: add `elif event["kind"] == "paper order": fields.append(f"<small>{e(event.get('side', ''))} · no execution plan</small>")`. This applies only to receipt replay of a run that had no plan.
- `p`, `strong` and `b` have no `overflow-wrap` (monitor.html:7). Long reason text or order tags in `<p>` (views.py stop_details, card) could force sideways scrolling. Fix: add `p,strong,b{overflow-wrap:anywhere}` to the style block. Whether it actually overflows depends on rendering, which I could not do.
- The dead path at run.py:164 calls `publication.push()`, which no longer exists. No caller passes `publication`, so it is unreachable. Fix: delete :163-164 and the `publication=None` parameter.
- A pinned run that is lost from an emptied store loops with no message (relay.py:139, 191). The page keeps showing its old cards and never says the run is gone.

## Labelled speculation (not settled from the code)
- run_live.py:116 gives the paper process 480 s after the recorder stops, then SIGTERM, then 90 s, then SIGKILL. If the worker already failed, `finish()` re-tries the failed cut and each queued cut, each up to about 78 s. A long backlog could pass the window, and a killed process sends no "failure during shutdown" notice.
- GitHub may rate-limit a burst of many fill pushes (one push per fill) and refuse some.
- Whether an iOS Safari EventSource sends the cached Basic credentials, and whether Render's proxy streams SSE without buffering, can only be shown on the hosted page.
- The relay has no limit on password attempts.

## Read and found doing what the items require
- **Relay before git:** in `deliver()` the Render post comes before the git wait (run.py:325-327), and `deliver()` runs before the pacing sleep (run.py:336 before :351).
- **One commit per order or fill, exact prefix:** the cut sizes are taken under the session lock after `journal.flush()` (session.py:167) and the receive-ns flush (journal_publication.py:42-47). Each order or fill cut is exactly the journal through that event (sequence = `s.events - 1` after the increment). `_stage_prefix` only appends and refuses a boundary that moves backwards (:84-94). Distinct sizes give distinct trees, so one commit and one push per order or fill (:121-128). `published_sequence` advances only after the push (:128-131).
- **Ambiguous push:** the same commit is re-pushed before anything later is staged (:114), and each commit's parent is the one before, so every push is a fast-forward. Three tries, then the run stops (:101-109, :142).
- **Commit form:** message "Paper {trigger} through journal sequence {n} [skip ci]". Identity "NG Paper Recorder", paper@users.noreply.github.com. Ref `refs/heads/paper-runs/<run>`. Only `paper-trading/<run>/<file>` paths are staged (:96, :25).
- **Shutdown:** the final cut includes receipt.json (:45-46). A failed worker's cut and all queued cuts are re-published in order (:154-157).
- **Destination checks, all pointing at DavisAI1974/markets-data:**
  - fetch origin: session.py:45-51
  - exactly one push URL, either form; HTTPS needs a token: run.py:42-52
  - the push goes to that validated URL: journal_publication.py:103
  - action.yml:28 and :51 set the URLs
  - action.yml:47-49 pins the host key with StrictHostKeyChecking
  - the HTTPS header is scoped to the push URL (run.py:65-71)
  - SSH_AUTH_SOCK is passed only to the paper and backup processes (run_live.py:22-27)
  - Not enforced: a runner-level `insteadOf` or `pushInsteadOf` git setting could rewrite the URL after the check.
- **Relay ordering:** the relay accepts only the next contiguous sequence (relay.py:104-107) and accepts an identical re-post without change (:100-103). A batch is one transaction of up to 128, which matches run.py:110 and restore_view.py:17.
- **No drops or repeats on the page:** SSE ids are `run/sequence`; reconnect resumes from Last-Event-ID (relay.py:292-297); a run change resets the cursor and clears the page (relay.py:192-195, monitor.html:37-51). A strategy filter keeps status events and sends a cursor event to move the position past other rules (relay.py:232, 246-248). A pinned run closes after "finished" (relay.py:256, monitor.html:74). The first page load and the stream meet at the same max sequence (relay.py:338-340, views.py:299-305 at the old tip). The vendored htmx fires `htmx:beforeCleanupElement` on swapped elements, so the old stream is closed on a filter change.
- **Fields shown:**
  - fill: side, quantity, fill price, liquidity, order id, fill id, and the bid and ask at the fill message (paper_execution.py:84-88; views.py card)
  - order: rule, action, side, quantity, placement, limit, reason, decision bid and ask
  - status: reason; the stop details are in the header
  - Every field name the page reads matches a field the runner emits. No key collides with `Session.write`'s fixed keys.
- **House rules on the page:** prices are shown only as separate bid and ask; there is no mid, no average and no summary figure in views.py or trades.py (open contracts are a count). The fee model's maker and taker fees are "0" in both plans and no commission is journaled or shown. Viewport meta is present (monitor.html:2).
- **Passwords and tokens:** every event route requires the viewer password (relay.py:141-328); only /health and /static are open. Ingest requires the bearer token (relay.py:79-81, 115, 121). Neither secret is printed, rendered or put in a URL. Git stderr is discarded, and a timeout message shows only the URL.

Files: /home/user/paper-trading-platform/paper_platform/journal_publication.py, /home/user/paper-trading-platform/paper_platform/run.py, /home/user/paper-trading-platform/paper_platform/session.py, /home/user/paper-trading-platform/paper_platform/relay.py, /home/user/paper-trading-platform/paper_platform/views.py, /home/user/paper-trading-platform/paper_platform/monitor.html, /home/user/paper-trading-platform/paper_platform/render.yaml, /home/user/paper-trading-platform/paper_platform/run_live.py, /home/user/paper-trading-platform/.github/actions/markets-data/action.yml, /home/user/paper-trading-platform/.github/workflows/live_ng_paper.yml, /home/user/paper-trading-platform/.github/workflows/purchased_mbo_paper.yml, /home/user/paper-trading-platform/.github/workflows/verify_paper_platform.yml
