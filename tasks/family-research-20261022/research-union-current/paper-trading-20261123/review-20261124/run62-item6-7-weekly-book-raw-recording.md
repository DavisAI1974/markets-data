# Run 62: items 6 and 7, the weekly order book and the raw recording: what each book does at the UTC file boundary, how a mid-week start is seated, what is stored and what can be lost

The agent's own report, word for word, as it came back to the session (session_017eY1WPw7p6f6Tyx49EyYD4, 2026-11-24). It is a reading of code and documents. Nothing was run. What was done with each finding is in README.md beside this file and under the item's number in the platform checklist.

---

I reviewed checklist items 6 and 7 at 37c5e91 (branch codex/strategy-trades-and-mbo-capture) by reading only. I ran nothing and changed no file in the repository.

Two sources are not on disk, so some answers depend on them:
- The NautilusTrader Rust orderbook crate (BookLevel add/update/delete). The partial copy has the matching engine's .pyx but not the level code.
- The databento Python client (how it dispatches records to `add_stream` and callbacks, whether it re-encodes, heartbeats, how far back intraday replay reaches).

Every finding was appended as I went to /tmp/claude-0/-home-user/f6fc58bd-1d38-5c78-9832-91292fa09200/scratchpad/review2/items-6-7.md. The section "Corrections after advisor review" at the end of that file replaces notes D, H, M and O above it.

## Findings

**1. [6] An exchange clear after the week's start-up restarts all three books, and nothing stops the run.**
- **What the code does:**
  - Archive: `root/tape.py:92-100` (classify) refuses only FLAGGED records after a file's opening block. An UNFLAGGED `R` later in a file is passed through as an ordinary tick.
  - Captured and live: `capture.py:274-277` checks only the instrument, the position and the next week. No check looks at action `R` or `F_SNAPSHOT` after position 0.
  - Such an `R` empties ROOT's book (`root/book.py:149-151`), clears the native mirror (`nautilus_book.py:28-29`) and sends `BookAction.CLEAR` to every rule venue (`paper_execution.py:224-225`).
  - In the matcher, a CLEAR also sets every resting paper order's queue-ahead to 0 (Nautilus `backtest/engine.pyx:4321-4326`, `7061-7067`).
- **What the rule says:** the only restart is the exchange's own on Sunday. `root/book.py:14` says the same ("clear: ... the exchange's Sunday start-up only").
- **Answer to the brief's question:** an `R` that is not part of a vendor snapshot reaches `market()` in these cases:
  - (a) record 0 of the week's first file (the Sunday clear);
  - (b) an unflagged `R` anywhere later in an archive file;
  - (c) any `R` at all in a captured or live stream. The live path never marks a snapshot (`record_mbo.py:76` passes `snapshot=False` unless the source is purchased), so `period` is never "vendor snapshot" there.
- **Fix, captured path.** Initialise `seated = False` beside `position = 0` at `capture.py:215`, then after line 277 add:
  ```
  flagged = fields["flags"] & tape.flag_bits()["F_SNAPSHOT"]
  if position and fields["action"] == tape.CLEAR:
      raise ValueError(f"a clear after the week's start-up at position {position}")
  if flagged and seated:
      raise ValueError(f"a flagged record after the Sunday start-up block at position {position}")
  seated = seated or (position > 0 and not flagged)
  ```
  The Sunday block is an unflagged `R` followed by flagged re-listed adds (`tape.py:8-10`), so a guard on flagged records alone would stop every week at position 1.
- **Fix, archive path.** This goes in `paper_platform/feed.py`, not `root/tape.py`, so ROOT stays aligned upstream. After line 154 add:
  ```
  if not snapshot and fields["action"] == tape.CLEAR and not (file is self.week[0] and index == 0):
      raise ValueError(f"{file.name}: a clear after the week's start-up at record {index}")
  ```
- **Effect of the fix:** changes no stored data. A run stops at that point, and in a live run a stop leads to the flattening orders.
- **Certainty:** the code paths are certain from the code. Whether CME or Databento ever sends an `R` mid-week (a channel reset or a gateway recovery) depends on behaviour not readable here.

**2. [6] On a modify that raises size at the same price, the matcher keeps the order's place; ROOT sends it to the back.**
- **What the code does:**
  - `paper_execution.py:227` reads `replaced = old and new and (old[0] != new[0] or old[2:] != new[2:])`. Here `old[2:]` is (side, `entered_pos`), and `entered_pos` never changes on a modify (`root/book.py:137` updates `placed_*` only).
  - So a same-price size increase becomes `BookAction.UPDATE` (line 231).
  - ROOT, and the native mirror through leave and join (`nautilus_book.py:44-50`), move that order to the back of its line (`root/book.py:134-138`).
- **What the rule says:** "a rise in size sends it to the back of its own line" (`root/book.py:9-10`), and item 6 asks for the exact book.
- **Fix, `paper_execution.py:227`:**
  ```
  replaced = old and new and (old[0] != new[0] or old[2:] != new[2:] or new[1] > old[1])
  ```
- **Side effect of the fix:** the added DELETE also zeroes queue-ahead for every paper order at that price (`engine.pyx:4337-4338`, `7049-7059`).
- **Effect of the fix:** changes the matcher's book order, and so possibly paper fills (orders). No stored data changes.
- **Certainty:** certain that an UPDATE is sent. That Nautilus's L3 UPDATE keeps the order in place depends on the Rust orderbook crate, which is not on disk.

**3. [6] A paper order's queue position in the matcher is an estimate, not its place in the L3 line.**
- **What the code does:**
  - `paper_execution.py:54` sets `queue_position=True`.
  - Nautilus records queue-ahead as the whole size at the level when the paper order rests (`engine.pyx:7010-7047`, `8134`).
  - It reduces that only on trades at that price (`7069-7096`). Partial cancels ahead of the paper order do not reduce it.
  - Any DELETE at that price and side sets it to 0 (`7049-7059`). Every full cancel and every price-moving modify of any exchange order at that price sends a DELETE (`paper_execution.py:228-229`).
  - Any CLEAR or `F_SNAPSHOT`-flagged delta sets it to 0 (`4321-4326`). Flags are passed through raw at `paper_execution.py:223`.
- **At midnight UTC:** nothing reaches the matcher, because the vendor snapshot returns early at `paper_execution.py:205-206`. The boundary itself leaves queue-ahead unchanged.
- **What the item requires:** an exact book with queue position kept.
- **Fix:** no small fix inside this repository. It is upstream Nautilus's queue model.
- **Certainty:** certain from the code (the Nautilus .pyx is on disk).

**4. [6] Nothing compares the matcher's book with anything; the ROOT-to-native comparison runs only on the archive path.**
- **What the code does:**
  - `feed.py:145-149` compares ROOT's book with the restatement and checks the native mirror (`verify_queues`) at each later ARCHIVE file. A difference raises (the run stops).
  - Each rule venue's `engine._book` is never compared with ROOT, the mirror or the restatement.
  - The captured feed (`capture.py:211-286`) makes no comparison at all.
  - Captured purchased replay skips the restatement entirely. Its snapshot frames are stored with `position` NULL (`record_mbo.py:111,124-125` to `capture.py:50,57`), and `messages()` reads only rows with a position (`capture.py:229-232`). The live stream contains no restatement.
  - Strategy inputs read best bid and ask from the native mirror (`inputs.py:74` from `feed.py:101-102` from `nautilus_book.py:56-58`), not from ROOT's own book.
- **Where the books can differ on the same message:**
  - finding 2 (size-raising modify);
  - finding 3 (queue estimate);
  - a trade print with side other than A or B, which sends no `TradeTick` (`paper_execution.py:233`). No book changes in any of the three, but the matcher sees no trade.
  - On an L3 book, a `TradeTick` never changes the matcher's book (`engine.pyx:4620-4631` mutate only L1).
- **Fix for the live path:** run `stream.book.verify_queues(...)` at each `weekly_book_boundary`. In `feed.py` after line 54 add:
  ```
  if boundary is not None and boundary["position"]:
      self.book.verify_queues(f"UTC {boundary['utc_date']}")
  ```
  This covers ROOT against the native mirror only. Comparing the venues' books would need one more read: `venue.engine.get_book()` per venue against `self.book.native` at the same point.
- **Effect of the fix:** changes no stored data. It can stop a run.
- **Certainty:** certain from the code.

**5. [6] Mid-week start, live: the recorder asks for the week from Sunday 00:00 UTC on every connection.**
- **What the code does:**
  - `record_mbo.py:158-159` subscribes with `start=datetime.combine(sunday, 00:00, UTC)`.
  - `capture.py:269-271` refuses a capture whose first MBO is not an unflagged `R` dated Sunday in UTC.
  - On restart, `capture.py:51-55` and `69-71` require a byte-identical replay of the stored prefix.
  - Each recorder run lasts at most 5.75 h (`run_clock.py:10`, `record_mbo.py:41,66-67`), so a week needs repeated replays from Sunday.
- **If the gateway cannot replay that far:**
  - It may send an `ErrorMsg`, which becomes a CaptureFailure (`record_mbo.py:141-142`).
  - It may start later. On a restored database that raises "replayed MBO differs at position 0" (`capture.py:65`). On a fresh database the recorder stores it, and `CapturedFeed.messages` refuses to read it (`capture.py:270-271`).
  - No code path seats the book from a mid-week snapshot.
- **What the item requires:** the week seated from Sunday.
- **Fix:** none proposed.
- **Certainty:** the code paths are certain. Whether the live gateway can replay from Sunday 00:00 UTC on a Wednesday depends on behaviour not readable here (Databento's intraday-replay window; the client is not on disk).

**6. [6] The week fails to read if the start-up is not on the UTC Sunday, or if a message falls on Friday evening or Saturday.**
- **What the code does:**
  - "Sunday" comes from `week_sunday` (`calendar.py:79-83`), a date calculation from the trade day.
  - It is matched against the UTC date of the first file (`tape.py:118-120`, `87-90`) and of the first record (`capture.py:269`).
  - The "Sunday start-up" label is decided on the Eastern clock (`calendar.py:71`).
  - There is no holiday calendar for the week. The only holiday code is `root/outside.py:183-213`, for report dates.
  - A week whose exchange start-up is not on the UTC Sunday (a Monday-evening reopen) is refused, by `classify` or by `capture.py:271`.
  - `label()` raises for any record at or after Friday 6 pm Eastern, or on a Saturday (`calendar.py:73-75`). It is called from `feed.py:55`, so the whole stream stops.
- **What the item requires:** seated at the exchange's Sunday start-up.
- **Fix:** none proposed. Holiday handling is a rule question for Greg.
- **Effect of the fix:** none.
- **Certainty:** certain from the code.

**7. [7] The receive time is stamped from the wall clock after the client has decoded each record, and waits behind the previous record's disk write.**
- **What the code does:**
  - `record_mbo.py:64`: `received_ns = time.time_ns()`. That is the wall clock (CLOCK_REALTIME, which NTP can step). It is taken when `Sink.write` begins, after the databento client has read the socket and split the record out.
  - It is one stamp per record. `record_mbo.py:73-74` rejects a write that is not exactly one record. It is not a per-delivery or socket-read time.
  - `capture.py:58-62` with `synchronous=FULL` (`capture.py:84`) makes one fsynced commit per record. Each stamp is therefore taken only after the previous record's commit returns. During a burst, later stamps include the disk time of the records before them.
  - `ts_out=False` (`record_mbo.py:133`): the gateway's send time is not requested and not stored.
- **What the item requires:** our receive time in nanoseconds, as it arrives.
- **Fix (smallest):** add a monotonic stamp beside the wall stamp so clock steps can be seen. At `record_mbo.py:64` add `mono_ns = time.monotonic_ns()` and pass it through `append()` to a new `frames` column. The fsync-per-record wait is a design choice and has no one-line fix.
- **Effect of the fix:** changes stored data (a new column). No order.
- **Certainty:** the stamp point is certain. Whether the client re-encodes bytes, and how long it holds a socket read before calling `write`, depend on the databento client.

**8. [7] Deliveries that arrive after a stop are not stored, starting with the delivery that crosses the clock limit.**
- **What the code does:** `record_mbo.py:66-69`. The write that crosses the deadline sets stop and then returns without storing. Every write after `done` is set (the budget, a failure, a signal) is discarded without a row or a count, until the client closes (up to 10 s, line 188).
- **What the item requires:** nothing dropped.
- **Fix (smallest, stores only the deadline-crossing delivery):** replace lines 66-69 with:
  ```
  if self.done.is_set():
      return len(data)
  if self.last_delivery_at >= self.deadline:
      self.stop("clock limit")
  ```
  Removing the `done` check entirely would also overrun the message budget and keep appending after a failure, so it is not proposed.
- **What remains after the fix:** deliveries after stop are still dropped. On the next run they come back by replay as first copies with replay-time stamps (finding 10).
- **Effect of the fix:** changes stored data (one more row). No order.
- **Certainty:** certain from the code.

**9. [7] Parts of the session are never stored, depending on the client.**
- Stored as kind "control", with their bytes: every non-MBO record that reaches `Sink.write`. That covers SystemMsg (including REPLAY_COMPLETED), ErrorMsg, SymbolMappingMsg, and definition records from the second subscription (`record_mbo.py:75,161-163`). The DBN metadata header is stored as kind "metadata" (line 70-71).
- Never stored by this code: the text control protocol (greeting, authentication, session reply).
- **Fix:** none proposed.
- **Effect of the fix:** none.
- **Certainty:** whether heartbeats or any other record are consumed by the client without being dispatched to the stream, and whether the bytes written are the gateway's own or a re-encoding (DBN version upgrade of metadata, definition or mapping records), depend on the databento client. MBO's 56-byte layout matches `capture.py:21`.

**10. [7] A drop ends the recorder. The next run re-requests the gap from Sunday, and the gap's rows carry the replay time, marked only through `live_starts`.**
- **What the code does:**
  - `reconnect_policy="none"` (`record_mbo.py:133`): a disconnect raises CaptureFailure (line 167-168), and that process ends.
  - The next run restores the checkpoint and subscribes again from Sunday (finding 5).
  - Stored positions are re-stored as new rows with `replay_of=N` and their new `received_ns` (`capture.py:51-55,59-62`). The whole week's prefix is written again on each restart.
  - Records after the stored prefix (the gap) become first copies with the replay-time `received_ns`, not an original arrival time.
  - The marking is indirect: `live_starts` (`record_mbo.py:149-151`) puts them before that connection's live start, and `receive_time_coverage` (`capture.py:166-181`) labels them "gateway replay delivery". No column on the row says "original arrival not observed".
  - A re-delivery that differs is inserted with `position` and `replay_of` both NULL (`capture.py:53,59-62`) before the failure. It is named only in `connections.status` (`capture.py:112-118`). In a live capture no other MBO row has both NULL, so it can be found. In a purchased capture it looks like a snapshot frame.
- **What the item requires:** receive time as it arrives.
- **Fix:** none offered for the marking. The connection status already names the position.
- **Effect of the fix:** none.
- **Certainty:** certain from the code. Whether REPLAY_COMPLETED's callback runs after every earlier record's stream write, which decides the `live_starts` position, depends on the client's dispatch order.

**11. [7] Between checkpoints, the runner alone holds up to 60 s plus one full publish, and a hung push widens that without limit.**
- **What the code does:**
  - `capture_backup.py:125-127`: `follow` sleeps 60 s, then publishes. It runs in both workflows (`record_ng_mbo.yml:71`, `run_live.py:80-81`).
  - A publish backs up the whole SQLite file, hashes every 4 MiB block, encrypts the new blocks, commits and pushes (`capture_backup.py:74-104`). Its duration grows with the file and has no limit in the code. `git()` has no timeout (`session.py:24-25`).
  - "Last published boundary" is the last `frames.id` and `MAX(position)` in the backup copy (`capture_backup.py:81-82,92-93`).
  - A failed publish ends `follow`, and the recorder gets SIGUSR1 (`run_live.py:101-105`, `record_ng_mbo.yml:79-84`). A hanging push does not end it, and the recorder keeps recording.
- **What is lost if the runner dies inside that span:** the `frames` rows (MBO bodies can be fetched again from the vendor, without their original `received_ns`); the control frames (system, error, mapping, definition); the `connections` row's `ended_ns` and status; and the `live_starts` row.
- **What the item requires:** recorded whole.
- **Smaller code changes that would shrink the span:**
  - (a) Publish only rows with `id` above the last published id, as one encrypted append block per minute, instead of a full-file backup. Publish time then follows new rows, not the week's size.
  - (b) A timeout on the push at `capture_backup.py:104`:
    ```
    subprocess.run(["git", "-C", str(self.root), "push", "origin", "HEAD:refs/heads/" + self.branch], check=True, timeout=55)
    ```
    A timeout stops the recorder, and in a live run that leads to the flattening orders.
- **Effect of the fix:** neither changes stored data; (b) can lead to orders.
- **Certainty:** certain from the code. The push duration depends on GitHub.

**12. [7] Stored order is arrival order; replays are the only stored repeats.**
- **What the code does:** `frames.id` is the INTEGER PRIMARY KEY in insertion order (`capture.py:91-94`), one insert per `Sink.write` call. `position` goes up by 1 per first-copy MBO (`capture.py:56-57,66-67`) and is UNIQUE.
- The only records stored twice are the replays of finding 10, marked with `replay_of`. Readers use rows with a position only (`capture.py:229-232`), and `capture.py:274` refuses a gap.
- **What the item requires:** stored in arrival order.
- **Fix:** none.
- **Effect of the fix:** none.
- **Certainty:** certain from the code, given that the client calls `write` in socket order. That ordering depends on the client.

## What the code does that the items ask for (read, not run)

**Item 6, per book:**
- **ROOT's book, and its native mirror `NautilusMboBook` (`feed.py:22`):**
  - Seated from the week's first file, record 0: the unflagged `R` (`tape.py:87-90`, `capture.py:269-271`). The flagged re-listed adds that follow are applied as ticks.
  - At each later archive file, the vendor's opening restatement is compared, never applied (`feed.py:145-149`, `book.py:188-210`). A difference raises and stops the run.
- **Rule venues (`paper_execution.py`):**
  - Seated from the same stream: `session.py:303-304` sends every message to `market()` from Sunday.
  - The snapshot is skipped (`paper_execution.py:205-206`).
- **An order resting across midnight UTC:**
  - ROOT keeps `entered_*` and `placed_*` (event time, receive time, position). The comparison checks the place time against the restatement (`book.py:198,201`).
  - The native mirror and the matcher get `BookOrder` with no time (`nautilus_book.py:34-40`, `paper_execution.py:221-222`). They keep line order only.
  - Nothing is reset at the boundary in any of the three books. `weekly_book_boundary` (`feed.py:28-42`) records a hash of the queue before the first row of each new UTC receive date.
- **Archive mid-week start:** reads from Sunday every time (`feed.py:116`, `tape.py:114-120`) and warms through the original start.
- **The 5 pm to 6 pm hour and the settlement window:**
  - Every non-snapshot record is applied to ROOT and the mirror (`feed.py:53-75`); `eligible` only sets `in_session`.
  - Every non-snapshot record goes to the matcher (`paper_execution.py:205`).
  - Settlement affects strategy responses only (`engine.py:232-246`).

**Item 7:**
- MBO records are stored with their bytes as handed to `Sink.write` (`capture.py:59-62`), each with its own `received_ns`.
- Checkpoints are encrypted with Fernet. Restore writes a temporary file, checks each block's SHA-256, and publishes with `os.link`, which refuses to replace an existing database (`capture_backup.py:52-66`).

**Files read:**
- /home/user/paper-trading-platform/root/book.py, root/tape.py, root/calendar.py
- paper_platform/feed.py, nautilus_book.py, paper_execution.py, capture.py, record_mbo.py, capture_backup.py, run_live.py, run_clock.py
- paper_platform/session.py:24-25 and 260-305, engine.py:213-246, inputs.py
- .github/workflows/record_ng_mbo.yml and live_ng_paper.yml
- docs/platform/OWN_PLATFORM_WISHLIST_20261123.md:41-51
- /home/user/nautechsystems/nautilus_trader/nautilus_trader/backtest/engine.pyx:4274-4346, 4581-4710, 6800-6845 and 7010-7110
