# Run 61: items 2 and 17, the wiring review: each of the 32 strategies from its rule to its order under its own plan entry

The agent's own report, word for word, as it came back to the session (session_017eY1WPw7p6f6Tyx49EyYD4, 2026-11-24). It is a reading of code and documents. Nothing was run. What was done with each finding is in README.md beside this file and under the item's number in the platform checklist.

---

Review of items 2 and 17 on branch codex/strategy-trades-and-mbo-capture at head 37c5e91. This came from reading only. I changed no file in the repository. No code, test, workflow, network call or Python interpreter ran. One early shell command had a stray `python3 -c 1` in it; the permission layer refused it and it did not run. The running notes are in /tmp/claude-0/-home-user/f6fc58bd-1d38-5c78-9832-91292fa09200/scratchpad/review2/items-2-17.md.

## Which plan a run uses
- **ngx3-12be6ea6...json (commit 95400eb):** has all 32 rules. Each has contracts 1, offset_ticks 0 and a `cross` close. The six managers each list 22 parents with `on_parent_close: exit`.
- **ngx3-599eb8c0...json (commit a58ef5b):** this is the earlier plan built from 30 decisions. It has no CL16 or CL17 entry, and each manager lists 20 parents (no CL16 or CL17). Nothing else differs.
- **How a run picks one:**
  - The purchased-tape workflow (`purchased_mbo_paper.yml`) has no default, so the operator must name a plan.
  - The live workflow (`live_ng_paper.yml:12`) defaults to 12be.
  - A receipt replay uses the plan recorded in the receipt (`run.py:252`).
- **What 599e would do if picked:** `PaperExecution` accepts it, because it only checks that the planned rules are a subset of the catalogue (`paper_execution.py:179`). CL16 and CL17 would then write signals only, with no orders, and no manager would follow them (finding 10).
- **Market rules list:** `markets/nymex-ng.json` lists all 32 rules. `Session` builds `self.rules` from that list (`session.py:70`), so the engine evaluates all 32.

## 1. Table (one row per rule)
Every row: contracts 1, offset 0, close `cross`. Managers: 22 parents, on_parent_close `exit`.

| Rule | Role | Side | What opens it (code) | What closes it (code) | Open style | Wired |
|---|---|---|---|---|---|---|
| CL01 | entry | with run (offer up = buy) | end of the event holding the run's 2nd step, and every first-level order left by fill (`claude_rules.py:208-218`) | that run's step-back fact (`313-323`) | cross_limit | yes; 11 (live feed only) |
| CL02 | entry | against run | 2nd step, every first-level order pulled, none hit (`219-227`) | run ends or 3rd step (`active`, max_steps 2) | post | yes |
| CL03 | entry | with step | first outward step on removal by fill, with a print of that side in the event (`188-197`, 300) | run start changes (`active`) | cross_limit | yes |
| CL04 | entry | with the eaten quote | level hit, not disturbed, still standing (`124-135`) | level disturbed, better quote, or first step back after the level gives (`324-338`) | cross_limit | yes |
| CL05 | entry | with leg | leg's first step, a quote has changed, exhaustion on the leg's side (`159-171`) | leg changes (`active`) | cross | 14 |
| CL06 | entry | with both quotes | both quotes stepped the same way and ask > bid (`257-263`) | pair resets: either quote steps the other way | cross_limit | yes |
| CL07 | entry | hump side | hump starts on a sided print with the dipole before it on its side (`150-158`) | hump ends, at a record (`at`) or by timer (`engine.advance_clock` 178-211) | cross | yes |
| CL08 | entry | hump side | later outward step of the quote in another event, hump opposite the dipole (`242-256`) | hump ends or run changes | cross_limit | yes |
| CL09 | entry | against step | first outward step by a cancel, no print in the event (`198-207`) | run ends or 2nd step | post | yes |
| CL10 | entry | with run | 2nd step with the dipole opposite (`228-229`) | run ends | cross | yes |
| CL11 | entry | against run | same moment as CL10 (`230-237`) | run ends or 3rd step | cross | yes |
| CL12 | entry | against push | first same-size-or-larger reload of an order at the best (`102-114`) | order leaves, quote steps away, or quote goes through the level (`339-351`) | post | yes |
| CL13 | entry | aggressor side | one aggressor side filled more than one price in the event (`283-291`) | swept quote steps back (`352-360`) | cross | yes |
| CL14 | entry | against run | first opposing sided print at the latest step's price (`265-279`) | run ends or takes its next step | cross_limit | yes |
| CL15 | entry | original direction | return step after a run of 2+ and a 1-step run back (`238-241`) | run changes | cross | yes |
| CL16 | entry | with step | unsided print whose quote stepped since the previous print; not the first run; run not already entered (`unsided_print_rules.py:37-46`) | tracked run's step back, seen at a print (`62-80`) | cross | 7 |
| CL17 | entry | buy at offer / sell at bid | first unsided print at that quote since its last step (`47-59`) | tracked quote moves against the side, seen at a print | cross_limit | 7 |
| CX01 | entry | buy | `confirm_all` at q = the current print (`engine.py:329-344`) | `close_any` via `management` (`engine.py:290`) | post | 1, 2, 3, 4 |
| CX02 | entry | sell | as CX01 | as CX01 | cross_limit | 1, 2, 3, 6 |
| CX03 | entry | buy | as CX01 | as CX01 | cross_limit | 1, 2, 3 |
| CX04 | entry | sell | as CX01 | as CX01 | cross_limit | 1, 2, 3 |
| CX05 | manager | buy | own position opens at each buy parent's open (`paper_execution.py:262-272`) | own exit at confirmation (`when_confirmed: exit`), or the parent's close | cross | 3, 12 |
| CX06 | manager | sell | as CX05 | as CX05 | cross | 3, 12 |
| CX07 | entry | buy | as CX01 | as CX01 | cross_limit | 2, 3 |
| CX08 | entry | sell | as CX01 | as CX01 | cross_limit | 2, 3 |
| CX09 | entry | sell | as CX01 | as CX01 | post | 2, 3, 4 |
| CX10 | entry | buy | as CX01 | as CX01 | post | 2, 3, 4 |
| CX11 | manager | buy | opens at parent open; "hold" when confirmed | exit on `t.bid<q.bid` or `t.dipole<=0`, or the parent's close | cross | 1, 3, 12 |
| CX12 | manager | sell | as CX11 | exit on `t.ask>q.ask` or `t.dipole>=0`, or the parent's close | cross | 1, 3, 12 |
| CX13 | manager | buy | opens at parent open; "suspend additions" when confirmed | exit on `t.price<q.price`; release on its list; or the parent's close | cross | 1, 3, 12 |
| CX14 | manager | sell | as CX13 | exit on `t.price>q.price`, or the parent's close | cross | 1, 3, 12 |
| CX15 | entry | aggressor side | `confirm_all` plus `directional_confirm` | `directional_close` | cross_limit | 1, 2, 3, 6 |

## 2. Open styles in the matcher (`paper_execution.py:137-157`; NautilusTrader 1.231.0 `backtest/engine.pyx`)
- **Which quote it prices from:** the decision event's `bid`/`ask`, which is the feed's book at the decision record (`feed.py:101-102` via `inputs.py:74`).
- **Price arithmetic, checked for both sides:**
  - post buy = bid − offset; post sell = ask + offset.
  - cross_limit buy = ask + offset; cross_limit sell = bid − offset.
  - So `offset_ticks` moves a post away from the other side, and lets a crossing limit reach further through the book. Every offset in the plan is 0.
- **post** (LimitOrder, `post_only=True`, GTC, at the same-side quote):
  - A buy at the best bid is not marketable while ask > bid. NautilusTrader accepts it and it rests (`engine.pyx:5440-5462`).
  - Its queue position is the size already resting on its own side at that price (`7010-7047`). It fills later from prints and queue changes.
  - If that side of the feed book is empty, no order is sent; the journal gets "No bid for post order" (`paper_execution.py:143-146`).
  - It is cancelled by the trade's close (`105-118`), which then crosses only the contracts actually filled. If nothing filled, nothing more is sent.
  - It is NOT cancelled by an interruption (finding 4).
- **cross** (MarketOrder, IOC):
  - A buy needs an initialized ask; otherwise it is rejected "no market" (`5342-5347`).
  - It fills against displayed depth, adjusted for liquidity this venue already consumed (`6225-6300`). The unfilled rest is cancelled (`7432`). With no fills it is rejected "no market with no fills" (`7319-7320`).
  - The same style is used for every close.
- **cross_limit** (LimitOrder, IOC, at the opposite quote):
  - If the feed quote is None, no order is sent.
  - If marketable on the venue's own best bid and ask (`_core`), it fills through `fill_limit_order` (`6625-6760`). The rest is cancelled (`6685`, `6745`, `7432`).
  - If not marketable, it is cancelled at once (`5461`). See finding 6.
  - For a crossing order, the queue check gives 0 ahead and no trade-size cap, so it fills. This is because `_last_trade_size` is None outside `process_trade_tick` (`4694-4707`, `6791-6845`).

## 3. CL16 and CL17 at an unsided print
- **Open:**
  1. `UnsidedPrintRules.at(t)` emits the signal.
  2. `engine.py:322-323` empties only the CL01–CL15 `signals`; `print_signals` pass through.
  3. `open_trade` journals the event with `t`'s bid and ask, i.e. the feed's book at the trade record.
  4. `Session.record` routes it: the rule's own venue, plus the managers of that side (CX05, CX11, CX13 for a buy; CX06, CX12, CX14 for a sell). Each sends a cross.
  5. CL16 sends a market IOC priced off the venue's book. CL17 sends an IOC limit at the touched quote: ask for a buy, bid for a sell.
- **Close:** the step back is seen at a later print, sided or not. `engine.py:272` uses `unsided_print_rules.close` and is not suppressed. The close is a market IOC.
- **A quote missing at a print:** the trade gets "not scored: the feed lacks bid/ask" (`engine.py:266-271`) and goes to the unmonitored set. Its own and its managers' contracts are journaled, then flattened at the end of the trade day as administrative (`engine.py:370-374`).
- **What is missing at that print (finding 7):**
  - The unsided print itself is never given to the matcher. `paper_execution.py:233` passes only A/B sides.
  - The paper order is decided at the trade record, before the vendor's fill and cancel records remove the contracts that print traded. So it is priced from the book before the print's own fills, and can take those same contracts.
  - The print's consumption is not seeded. NautilusTrader seeds trade consumption only for a sided tick, and only when the venue holds resting orders (`engine.pyx` `_seed_trade_consumption`).

## 4. Managers
- **Parents:** every listed parent is a catalogue entry rule able to open on the manager's side.
  - Buy managers (CX05, CX11, CX13): CL01–CL17 (each can buy), CX01, CX03, CX07, CX10, CX15.
  - Sell managers (CX06, CX12, CX14): CL01–CL17, CX02, CX04, CX08, CX09, CX15.
  - No CX entry of the wrong side is listed, and none of the right side is left out.
- **Opening:** the manager's own position opens at the parent's open through `instructions()` (filtered on `side == direction`). This happens even when the parent's own order is not sent or not filled; the README says so.
- **Own exit:** the engine emits it with `trade_id = <parent>/<manager>` (`engine.py:132`). That is the same key the venue used at the open (`paper_execution.py:271`), so it closes that position (`256-259`).
- **Parent close:** sends a manager close (`266-272`).
- **Parent interruption:**
  - `record_interruption` (`paper_execution.py:274-292`, called at `session.py:185-187`) journals the parent's and each same-side manager's held contracts and working orders as "observation ended with paper exposure". It sends no order.
  - The engine drops the manager states (`engine.py:159`), so no later exit can come.
  - The contracts stay until `Session.stop`: `engine.stop(administrative=True)` closes the unmonitored trades (`375-378`), then `flatten` crosses each venue key, marked not trade data.
  - Exception: an interrupted CL16 or CL17 parent is flattened at the end of the trade day.
- **Per-parent inventory:** yes. `venue.inventory` and `active_orders` are keyed by `<parent trade id>/<manager>`.
- **Shared venue:** each manager has one matching engine for all its parent trades (finding 12).

## 5. Rules that cannot fire, and the item 18 mark
- **Can every rule fire?** No rule is impossible on the purchased tape as the code stands. All 32 are in the market list and evaluated.
- **CL16 and CL17 on the purchased tape:** they need Databento MBO trade records with side N. I found no count for the purchased NGX3 tape in the repository. The docs give counts for the tastytrade sandbox only (RUNNER_PLAN line 112). So I cannot say from reading how often they fire there.
- **Where the "not scored: the feed lacks …" mark is written:**
  - CX entry confirmation with a missing operand (`engine.py:345-354`, trade_id None).
  - CX entry management (`290-294`).
  - Manager management and arming (`120-122`).
  - CL16 and CL17 with a missing bid or ask (`266-271`).
  - Never for CL01–CL15 (finding 11).
- **The mark is also written when the feed lacks nothing:** whenever a line is empty (finding 1).

## 6. Never mixed
- **Separate per rule:** the venue, `OrderTags`, inventory, active orders and trade IDs. The ID is uuid5 of run, rule, position and identity. Manager tags append the manager.
- **Shared CL state that no rule's trade writes to another's:** `runs`, `levels`, `hump`, `leg`, `together`/`pair_start`. Each arm makes its own `conditions` dict. Only CL04 (`c["run"]`) and CL01 (`third_step_reference`) mutate anything at close, and each mutates its own trade.
- **Other shared state:** `runs[...]["tested"]` is read only by CL14. The manager state is keyed by parent trade and then by manager name (`engine.py:90`). `Responses` is keyed by trade or `trade/manager`.
- **Within one rule:** CX entries allow one open trade per rule (`engine.py:331`). CL rules can hold several of their own trades at once. Each has its own inventory key, but they share one matching engine (finding 12).

## 7. Sizes
- The open quantity is `policy["contracts"]` (1), at `paper_execution.py:300`.
- Close and flatten send `abs(inventory[key])` for that one trade key (`119-131`).
- Nothing sums or multiplies across rules or across trades.

## Findings

**1. [2] An empty line ends CX trades as "not scored".**
- **Code:** `inputs.py:19-21` sets a line to None when its span (20 s or 60 s) holds no sided print. `rulebook.py:77-80` evaluates close and release lists with `require_complete=True`. `engine.py:290-294` then interrupts the trade as "not scored: the feed lacks t.exhaustion" (or t.dipole).
- **Rules reached:** CX01–CX04 and CX15 (close lists read the lines), CX11 and CX12 (t.dipole), CX13 and CX14 (release reads t.exhaustion). For CX13 and CX14, a missing release operand overrides an exit whose condition is met, so the exit is never sent.
- **What item 18 requires:** the mark is for when the feed lacks a field. Here the feed lacks nothing.
- **Fix option (b), hold the trade while a line is empty, without marking it:** change `engine.py:290-291` to
  ```
  close, missing = management(rule, idea["side"], idea["p"], idea["q"], t)
  if missing and not all(term.split(".")[1] in ("dipole", "exhaustion") for term in missing):
  ```
  and apply the same test at `engine.py:105` and `111` for managers.
- **Fix option (a):** read an empty line as 0, as `crypto_ng.tick.line` writes it. That would close CX01 at once.
- **Choosing between (a) and (b) is for the rule's author.**
- **Changes an order sent:** yes.
- **Certainty:** certain from the code. How often it happens depends on 20 s gaps without a sided print on the tape.

**2. [2] An interrupted CX entry rule never opens again in that session.**
- **Code:** `engine.py:332` adds unmonitored trades to `active_names`. Unmonitored trades come from settlement, `F_MAYBE_BAD_BOOK`, a missing field, or finding 1.
- **What the plan requires:** each CX entry opens on its confirmation.
- **Fix:** delete `engine.py:332`. A second trade gets its own uuid5 key and inventory key.
- **Changes an order sent:** yes, later opens are sent.
- **Certainty:** certain from the code.

**3. [2] An interruption sends no order, so contracts are held to the run stop.**
- **Code:** `session.py:185-188`. The parent's and its managers' contracts are held until `Session.stop`. Every CX entry still open at 5 pm Eastern takes this path (`engine.py:366-367`).
- **When the flatten lands:**
  - The feed continues through the UTC file that holds 6 pm Eastern (`root/calendar.py:86-92`), i.e. to 00:00 UTC, which is 8 pm Eastern.
  - Unless a budget or the clock stops the run sooner, the flatten lands at the end of input, in the next trade day.
- **What the plan requires:** close `cross` and `on_parent_close: exit`.
- **Fix, if the authors want a close at the interruption:** after `session.py:187` add
  ```
  e = dict(e, action="close", signal_action=e["action"])
  ```
  The existing path then cancels working orders and crosses the parent and its managers. These are marked not trade data (`paper_execution.py:298-299`).
- **Changes an order sent:** yes.
- **Certainty:** certain from the code.

**4. [2, 17] An interruption leaves a working post order working.**
- **Code:** `paper_execution.py:274-292` does not cancel working orders.
- **Rules reached:** a post open for CX01, CX09 or CX10 keeps resting after the interruption. It can fill later, including after 5 pm Eastern. Nothing closes those contracts until the stop.
- **Fix:** before line 292 insert
  ```
  for identifier in working:
      venue.engine.cancel_order(venue.orders[identifier][0])
  ```
  Finding 3's fix also covers this.
- **Changes an order sent:** yes, a cancel is sent.
- **Certainty:** certain that the order is not cancelled. Whether it fills depends on the tape.

**5. [17] CL closes at the trade day's end are sent at the first record at or after 5 pm Eastern.**
- **Code:** `engine.py:228-238` sends them at the first record with `ts_event` at or after 5 pm Eastern, which falls in the halt.
- **The matcher's behaviour:** it has no halt state. A market IOC fills against whatever book that record leaves.
- **Fix:** no small line fix. When to act is a decision for Greg.
- **Certainty:** depends on the book at that record.

**6. [17] A cross_limit at a print that went through the quote can be cancelled unfilled.**
- **What NautilusTrader does:** `process_trade_tick` moves `_core` ask to the print price for a buyer through the ask, or `_core` bid for a seller through the bid (`engine.pyx:4657-4667`). It restores only the other side (`4720-4727`).
- **What the paper order does:** it is priced from the feed book's quote. It can then be judged not marketable and cancelled (`5461`).
- **Rules reached:** CX02 (`q.price < q.bid` is possible) and CX15. CX03, CX04, CX07 and CX08 need the price equal to the quote, so they are not reached.
- **Fix:** no small fix offered.
- **Changes an order sent:** it changes whether a fill happens.
- **Certainty:** depends on `OrderMatchingCore.is_limit_marketable`, which is not in the partial copy.

**7. [17] Orders decided at a trade record price from the book before that print's own fills.**
- **Code:** CX entries, managers that follow them, CL16 and CL17 decide at the trade record. Their orders price from the book as it stood before the print's own fill and cancel records. The unsided print is never sent to the matcher (`paper_execution.py:233`), so a resting post of another rule at that price gets no trade tick from it.
- **Partial fix, for the unsided print only:** at line 233 accept side `"N"` with `AggressorSide.NO_AGGRESSOR`.
- **Changes an order sent:** it changes fills.
- **Certainty:** depends on Databento sending the trade record before the fill and cancel records, which is not readable here.

**8. [17] A close that does not fill is not retried.**
- **Code:** a close rejected for an empty side leaves contracts held. The engine has already removed the trade (`engine.py:70`), so the next attempt is the stop's flatten.
- **Fix:** no small fix.
- **Certainty:** depends on a book side being empty.

**9. [2] The budget break in `Session.record` can skip a close.**
- **Code:** `session.py:196-199` breaks out before any instruction, closes included. The close signal is already journaled as trade data, but its order is then left to the administrative flatten. Also, `needed` at `session.py:213` does not count follower fan-out or fills.
- **Fix:**
  ```
  if self.state == "active" and instruction["action"] == "open" and (self.events >= self.output_budget
                                 or time.monotonic() >= self.deadline):
      continue
  ```
- **Changes an order sent:** yes.
- **Certainty:** certain from the code.

**10. [2, 17] The superseded 599e plan is still selectable.**
- **What it does:** it lacks CL16 and CL17, and is accepted by `PaperExecution`.
- **Fix:** remove the file (put the deletion to Greg first), or name it superseded in `execution_plans/README.md`.
- **Changes an order sent:** only if that plan is selected.
- **Certainty:** certain from the code.

**11. [2, 18] CL01–CL15 get no "not scored" mark when a quote side is empty.**
- **Code:** `inputs.py:79-80` resets the quote runs. CL01's close (`claude_rules.py:313-323`) then never fires before the trade day's end. The other CL rules close at the next fact.
- **Fix:** change `engine.py:266` to
  ```
  if t["trade"] or not reads_unsided:
  ```
- **Changes an order sent:** yes.
- **Certainty:** depends on the feed. The `quote_runs` docstring says no empty side occurs on the four trade days, so this reaches the live feed only.

**12. [6] One matching engine per manager serves all its parent trades, and per CL rule all its own trades.**
- **Code:** with `liquidity_consumption=True`, two opens of the same rule at one record take from the same displayed level. One trade's order can then move another trade's fill price within that rule.
- **Inventory:** stays per trade.
- **Fix:** no small fix.
- **Certainty:** depends on when NautilusTrader resets consumption (`4329-4335`).

**13. [3] A CL01–CL15 confirmation can be lost.**
- **Code:** `claude_rules.py:302` marks the confirmation emitted before `engine.py:322-323` drops it.
- **Certainty:** depends on whether an unsided trade record can carry `F_LAST`, which is not readable here.

**14. [3] CL05 and unsided prints.**
- **Code:** the leg calculation takes every print (`inputs.py:81-82`), and CL05's arm has no side check (`claude_rules.py:159-171`). So a leg step shown by an unsided print can open CL05 at the event's end.
- **Close timing:** a leg end shown by an unsided print closes at the next record of any kind. RUNNER_PLAN stand-in S7 says "the next print that has a side", and asks that both prints be named.
- **Certainty:** depends on whether S7 applies to the purchased tape.

## What I read and found wired
- **Files read in full:** all 32 rule files, both plans, `assemble_execution_plan.py`, `execution_policy.py`, `paper_execution.py`, `engine.py`, `claude_rules.py`, `unsided_print_rules.py`, `rulebook.py`, `cx_observations.py`, `session.py`, `trades.py`, `inputs.py`, `feed.py` and `nymex-ng.json`.
- **Read in part:** `root/calcs/quote_runs.py`, `run.py`, `run_live.py`, `live_contract.py`, the workflow plan inputs, and NautilusTrader `engine.pyx` (order processing, fills, trade tick, deltas, queue position).
- **Found wired:**
  - Each planned rule gets its own venue, tags, inventory and journal rows.
  - Opens follow the planned style, and every close crosses.
  - Manager follow, own exit and parent close all use matching trade keys.
  - The six managers' parent lists are correct and complete.
  - The post, cross and cross_limit prices and the offset signs are correct for both sides.
  - Every rule sends contracts 1, and nothing is summed across rules.
  - `trades.py` builds one row per rule and trade_id, manager rows included.

Everything above comes from reading. No pass or fail is given.
