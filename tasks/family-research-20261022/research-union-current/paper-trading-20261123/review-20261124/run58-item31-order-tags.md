# Run 58: item 31, order tags: every way an order could be sent twice or two orders share a tag

The agent's own report, word for word, as it came back to the session (session_017eY1WPw7p6f6Tyx49EyYD4, 2026-11-24). It is a reading of code and documents. Nothing was run. What was done with each finding is in README.md beside this file and under the item's number in the platform checklist.

---

Review of checklist item 31 on branch codex/strategy-trades-and-mbo-capture (tip e12bfde). This review comes from reading the code only. I did not run any tests, workflows or network calls, and I changed no file. Two Bash calls did start an interpreter by mistake, `python3 -c ""` and `python3 -I -` with empty input. Neither executed any code or imported anything, but you should know they happened. Nautilus source is not on this machine (searched the whole filesystem; `requirements.txt:6` pins `nautilus_trader==1.231.0`), so anything that turns on Nautilus behaviour is marked as depending on it.

**Item 31 wording** (`docs/platform/OWN_PLATFORM_WISHLIST_20261123.md:173-175`): "An order is never sent twice. Each carries its own unique tag." The status text says one session-long tag registry is shared by all venues. The first submission claims its tag before cancellation, journaling or matching, and entries, strategy and manager exits and administrative closes all go through the same guard. The code matches that description: `paper_execution.py:94` is the first statement of `RuleVenue.submit`, every order path reaches it, and one `OrderTags` object is made at `:182` and handed to every venue at `:196`.

## Findings

**1. A normal close does not check that its cancellations took effect before sending a fresh close.**
- **Where:** `paper_platform/paper_execution.py:102-117`.
- **What the code does:** It calls `cancel_order` on each working order for the trade, then sizes the new close as `abs(self.inventory[key])`. The "still awaiting cancellation" check at `:114` runs only when `administrative_flatten` is set.
- **What item 31 requires:** no second order for the same contracts.
- **Failing case:** The current plan `ngx3-599eb8c0...json` has six `"post"` open legs, which become GTC resting orders (`:152`). Managers on `on_parent_close: "exit"` can receive a second close for the same key: their own `exit` (trade id `key/name`, `engine.py:107/132`) and the parent's close (trade id `f"{trade_id}/{manager}"`, `paper_execution.py:265`). If a cancel does not take effect synchronously (no `OrderCanceled` back through `on_event` before `:116`), the old order stays active. That can be a resting close, or a resting open that later fills, while a new close for the full held quantity is sent.
- **Status:** depends on behaviour not readable here, namely whether Nautilus 1.231 `OrderMatchingEngine.cancel_order` emits `OrderCanceled` synchronously through the `ExecEngine.process` endpoint registered at `:57`. The missing check is certain from the code.
- **Smallest fix** (at `:114-115`):
```
            if self.active_orders.get(key):
                raise RuntimeError("working paper order still awaiting cancellation")
```
- **Effect of the fix:** In the normal path the raise reaches `session.step`'s `except` (`session.py:302-304`), which runs `stop("failure")` and the administrative flatten.

**2. A refused repeat tag leaves no journal row.**
- **Where:** `paper_platform/paper_execution.py:94-95`.
- **What the code does:** When `claim` returns False, `submit` returns without emitting anything.
- **What item 31 requires:** a repeat is never sent. Refusing does that, but the refusal itself is not recorded.
- **Reachability:** From the callers I read, nothing resubmits a tag (see the proof below), so this branch is a backstop that leaves no trace if it is ever reached. Certain from the code.
- **Smallest fix:**
```
        if not self.tags.claim(order_id):
            self.emit("order status", **event, order_id=order_id, pricing="native L3", submitted=False,
                      execution_event="order tag already used; not sent")
            return
```

**3. Tag uniqueness depends on rule ids containing no "-", and nothing enforces that.**
- **Where:** `paper_platform/paper_execution.py:286` (`f"{run}-flatten-{rule}-{key}"`) and `session.py:183` (`f"{order_id}-{rule}"`). Rule ids are file stems (`rulebook.py:22`); the plan keys are only checked to be a subset of the catalogue (`paper_execution.py:176`).
- **What the code does:** The tag is cut apart at "-", so splitting it back into rule and key is only unambiguous while rule ids contain no "-".
- **Present catalogue:** CL01..CL17 and CX01..CX15, four characters with no "-". Two different (rule, key) pairs cannot produce the same flatten identifier today. Certain from the code.
- **Speculation, not observed:** a future rule id such as `A-B` with key `x` would collide with rule `A` and key `B-x`.
- **Smallest fix** (after `paper_execution.py:178`):
```
        if any(not rule.isalnum() for rule in planned):
            raise ValueError("strategy IDs used in order tags must be letters and digits only")
```

**4. A cross_limit or post close refused for "No bid"/"No ask" is not retried before stop.**
- **Where:** `paper_platform/paper_execution.py:139-143`.
- **What the code does:** It journals `order status` with `submitted=False` and returns. The tag is used up, working orders for the trade were already cancelled at `:104-107`, and the inventory stays held.
- **This is not a repeat refusal.** `engine.close_trade` pops the trade (`engine.py:70`), so the engine never signals a second close for it. Two things can close it later:
  - the stop path's administrative flatten: style `cross`, market IOC, tag `f"{run}-flatten-{rule}-{key}"` (`paper_execution.py:286-293`);
  - for a manager key only, a later parent close under `on_parent_close: "exit"`, tag `f"{run}-{seq}-{manager}"`.
- A "close after a posted close was cancelled" always carries a new sequence and so a new tag; it is never refused as a repeat. Certain from the code.
- **Item 31 asks for nothing here.** Whether a refused close should be retried is a plan decision, so I propose no replacement lines.

**5. A zero-quantity close with no working orders returns without a journal row.**
- **Where:** `paper_platform/paper_execution.py:123-127`.
- **What the code does:** The tag is consumed silently. Example: a manager's `exit` followed by its parent's close on the same tick. `manage` runs before `close_trade` (`engine.py:313-315`), so the exit sends first and the parent close finds zero inventory.
- **No duplicate order results.** This touches traceability (item 30), not item 31. Certain from the code.
- **Optional fix:** drop the `if working:` guard at `:124` so the "no filled contracts to close" row is always emitted.

**6. The Nautilus `ClientOrderId` validity of the tags cannot be checked here.**
- **Where:** `paper_platform/paper_execution.py:132` (`ClientOrderId(order_id)`).
- **Tag sizes:** up to about 87 ASCII characters (32 hex for the run, `-flatten-`, 4-character rule, `-`, 36-character uuid5, and `/CXnn` for manager keys), including "-" and "/".
- **If an id is rejected,** the raise comes after the claim and, for closes, after cancellation (`:102-115`). In the normal path it propagates to `stop("failure")`. For a manager key the flatten identifier also contains "/", so the flatten would raise as well. That error is caught at `:294-298` and the inventory stays in the receipt. Nothing is sent twice in that sequence.
- **Status:** depends on behaviour not readable here, namely Nautilus 1.231's identifier validation (character set and length). No fix proposed without that source.

**7. Fill ids may repeat across venues.** This is adjacent to item 31 (item 30, traceability).
- **Where:** `paper_platform/paper_execution.py:85` (`fill_id=str(event.trade_id)`). Each rule has its own `OrderMatchingEngine` (`:51`).
- **Failing case:** If the matcher generates trade ids from a per-engine counter, two rules' fills can carry the same `fill_id`.
- **Status:** depends on Nautilus's trade-id format, not readable here.
- **Smallest fix:**
```
                      fill_id=f"{self.rule}-{event.trade_id}",
```

## Tag forms and the proof for question 1

- `run` is `uuid4().hex` (`session.py:55`): 32 lowercase hex characters, no "-".
- `seq` is the journal sequence of the signal row (`session.py:170,173`). `Session.events` increments once per written row (`:164`), so `seq` is unique per signal within a session.

The forms, in the order the question lists them:
- **A. Strategy open, close or exit sent to its own rule, including a manager's own `exit`:** `f"{run}-{seq}"` (`session.py:174,183`), when the instruction's rule equals the signal's rule.
- **B. A manager's order driven by its parent's open or close:** `f"{run}-{seq}-{manager}"` (`session.py:183`).
- **C. A manager's own exit:** form A under its own signal's sequence.
- **D. Administrative flatten:** `f"{run}-flatten-{rule}-{key}"` (`paper_execution.py:286`). The key is a uuid5 string (`engine.py:53`) or `f"{uuid5}/{manager}"` (`paper_execution.py:265`, `engine.py:107/132`).
- **Stop-path signals** written by `_record_stop_signals` (`session.py:339-342`) only fill `close_signals`; they never produce a form A or B tag.

Why no two different orders can share a tag:
- **Between forms:** after `run-`, form A continues with digits only, form B with digits then "-" then a rule id, and form D with the literal `flatten`. The three sets do not overlap.
- **Within form A:** one `seq` per signal, and `instructions` yields the parent instruction at most once (`paper_execution.py:249-255`).
- **Within form B:**
  - For one `seq`, each manager appears at most once in `followers[parent]`: one entry per planned rule (`:183-195`), and duplicate parents are refused (`:187-188`).
  - A manager is never the parent, because parents must not be managers (`:193`). So a parent and a manager under the same `seq` cannot both take form A.
  - The same manager following two parents that signal on the same row gets two signal rows with two different `seq`, so the tags differ.
  - A manager's exit and its parent's close on one tick are two signal rows: tags `run-sA` and `run-sB-CXnn`.
- **Within form D:**
  - `flatten` runs once per session. `stop` checks and sets `state` under the RLock before flatten (`session.py:345-349`), and every later `stop` call returns at `:346-347`. That covers the run.py finalizer `s.stop(why)` (`run.py:376`), the guard thread (`run.py:294,303,306`), the publication worker (`journal_publication.py:142`), `stop_capture` (`session.py:308`) and the API watchdog (`api.py:39,49`).
  - Each (rule, key) is visited once per call: `keys` is a dict built before the loop (`paper_execution.py:283-285`).
  - With 4-character rule ids that contain no "-", the rule/key split is unambiguous (finding 3). The "/" in a manager key comes after the rule id, so it cannot make one (rule, key) identifier equal another.
- **Across sessions:** `run` differs, and the registry is per `PaperExecution` (`:182`).

## What I read and found on questions 2-8

- **Q2:** A refusal journals nothing (finding 2). From the callers read, a refusal is never reached: every later order for the same trade carries a new sequence or the flatten form. The "No bid" walk is in finding 4.

- **Q3:** `_apply` (`session.py:193-216`) decides first and calls `record` (which submits) only after the deadline and budget checks at `:197-204`. Both rollback branches are followed at once by `stop()` in the same lock, so the state leaves "active" and `step`/`advance_clock` return early (`:220-221`, `:235-236`). No order exists for a rolled-back batch, and the decision cannot recur on a later tick. Certain from the code.
  - Adjacent observation: with execution on, `needed` at `:196` counts one row per order-bearing decision, but `record` also writes "paper order", fill and status rows. The mid-batch stop at `:209-211` (no rollback) and the instruction break at `:180-182` are therefore reachable. Neither sends a second order:
    - An unrecorded open has no venue order. `engine.stop` gives it an administrative close signal, and the venue has no key for it.
    - An unrecorded close leaves inventory that flatten closes once.
  - A journal-integrity effect follows: a stop close signal can name a trade whose open was never journaled, and `replay_comparison.py:46-47` raises "unknown opening trade" on it.

- **Q4:** In the stop path, close signals are only collected (`session.py:339-342`) and never submitted as normal closes. Flatten cancels working orders first and refuses to send while any is still active (`paper_execution.py:114`). An IOC close fills or cancels inside `process_order`, so the inventory flatten reads already reflects it. One trade therefore cannot get a normal close and an administrative close for the same inventory, provided Nautilus IOC orders do not rest (depends on Nautilus). `stop()` cannot run twice (see form D). Flatten cannot run after a failed first attempt, so the "tag has been consumed" comment at `:295` describes no reuse path.

- **Q5:** The tags are distinct in both same-row cases (see form B). Manager actions in the catalogue are `exit`, `hold` and `suspend additions` (`CX05/06/11-14.json`), and `record` routes only `open`/`close`/`exit` (`session.py:171`). A manager never produces an "open" of its own that could double its venue position.

- **Q6:** See finding 6.

- **Q7:** `replay_comparison.py:33-34` skips every non-signal row, and `:41-42` drops run, sequence and recorded_ns. Order tags, paper orders and fills are not compared between a live run and its replay; the tags would differ by `run` anyway. The `:37-38` check refuses a repeated opening trade id in signals.
  - `journal_publication.py:99-109`: a retried push resends the same commit, and no journal row is written.
  - `run.py:84-101`: a Render 409 re-posts earlier journal rows to the relay viewer. That re-sends events to the viewer, not orders to a venue.

- **Q8:** Every access to `orders`, `active_orders` and `inventory` runs under `Session.lock`:
  - the main loop: `step` at `session.py:234` and `advance_clock` at `:220`;
  - shutdown and status: `stop` at `:345`, `stop_capture` at `:307`, and `status` at `:397`, which the relay thread reaches through `Publication.packet` at `run.py:127`.
  - The other threads (guard, publication worker, API watchdog) reach venues only through `stop`. The `OrderTags` lock is redundant under that RLock and harmless.
  - Unlocked reads at `run.py:155` and `api.py:36-37` touch only `state`/`due()`, never venue state. Certain from the code.

## Files
- /home/user/paper-trading-platform/paper_platform/paper_execution.py
- /home/user/paper-trading-platform/paper_platform/session.py
- /home/user/paper-trading-platform/paper_platform/engine.py
- /home/user/paper-trading-platform/paper_platform/run.py
- /home/user/paper-trading-platform/paper_platform/capture.py
- /home/user/paper-trading-platform/paper_platform/journal_publication.py
- /home/user/paper-trading-platform/paper_platform/replay_comparison.py
- /home/user/paper-trading-platform/paper_platform/cx_observations.py
- /home/user/paper-trading-platform/paper_platform/rulebook.py
- /home/user/paper-trading-platform/paper_platform/execution_plans/ngx3-599eb8c0d48926292bbb4ef83fd518d5d2753daf.json
- /home/user/paper-trading-platform/docs/platform/OWN_PLATFORM_WISHLIST_20261123.md
