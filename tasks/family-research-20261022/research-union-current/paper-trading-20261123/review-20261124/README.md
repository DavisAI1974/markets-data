# Reviews of the paper platform draft by Claude's agents (2026-11-24)

Each file here is one agent's report, word for word, as it came back to the session. Every report is a reading of
code and documents on paper-trading-platform, branch `codex/strategy-trades-and-mbo-capture`. Nothing was run on
that branch. The run numbers are those of `../agent-runs.jsonl`, which holds each run's model and tokens.

What was done with each finding is listed below. "Fixed" means changed in draft on that branch, not run.

## Run 50, item 23: the agent launcher (`run50-item23-agent-launcher.md`)

| Finding | What was done |
| --- | --- |
| 1. A clock stop reported as a connection failure | Fixed by the other Claude session before this report came back (`bf1d039`: the two stops are BaseException). The recorded-reason list the report also offers was not added. |
| 2. The phone notice waits behind git steps with no time limit | Fixed, `e0da2fa`: the notice goes first, each git step has 25 seconds, the commit carries `[skip ci]`. The file fingerprints it offers were not added. |
| 3. A call that was sent and did not finish is recorded as zero tokens | Fixed in part, `e0da2fa`: the record says the call was sent and gives the most it can have used. Reading usage from the stream's events was not added: the report marks those field names unconfirmed. |
| 4. Reported usage is never compared with the budget | Fixed, `e0da2fa`: an overrun is reported as a budget stop and the answer is kept. |
| 5. A refusal to start sends no notice | Fixed, `e0da2fa`. |
| 6. Only the fetch address is checked, not the push destination | Fixed, `e0da2fa`: the runner's own check of the push destination, and a dry-run push before any request that costs tokens. |
| 7. The brief and attachments can be any path on the runner | Fixed, `e0da2fa`: only files committed in the platform repository; the workflow no longer expands wildcards. |
| 8. No job time limit; the launcher is a child of the shell | Fixed: 355 minutes (`e0da2fa`), `exec` (`a5818fc`). |
| 9. The record has no times and no call identifier | Fixed, `e0da2fa`. |
| 10. The brief and the answer are published in full | Not changed. Said under item 23. |
| 11. The SDK pin is not confirmed | Looked up on PyPI: `anthropic` 2.13.0 exists. Whether it installs beside the platform's other pins was not tried. |
| 12. Both new workflows act only from the default branch | Not changed. Said under items 23 and 26. |

## Run 51, item 26: the phone notices (`run51-item26-phone-notices.md`)

| "What is not wired" | What was done |
| --- | --- |
| 1. The run-end notice is not active on this branch | A setting (merge). Not changed. |
| 2. Whether the secrets and the variable exist | Settings only Greg can supply. Listed under item 26. |
| 3. Three workflows outside the notice list | Fixed, `a5818fc`. |
| 4. No guard for an unset secret, no retry | Fixed, `a5818fc`. |
| 5. `PAPER_RELAY_DB` and a Python version are not in the Render blueprint | Not changed: Render's rules could not be read (run 53). Said under item 26. |
| 6. A dead publisher in the record-only workflow is reported as "capture stopped" | Fixed, `a5818fc`. It also changes the end status stored in that capture; no replay reads it (said under item 26, `262218c`). |
| 7. The worker's failed notice attempt leaves no trace | Fixed, `a5818fc`. |
| 8. The recorder's notice failure replaces the capture error | Not changed: the capture error stays in the traceback, and a failed notice failing the job is kept. |
| 9. A cancel signal is not forwarded in three workflows | Fixed, `a5818fc` (`exec`). GitHub's cancel behaviour was not exercised. |
| 10. `run_live.py` exits without a notice of its own | Not changed: at those ends the recorder or the runner it started sends its own notice. |
| 11. The first failure notice carries no cause | Left to Codex: the word is also the receipt's status, which receipt replay reuses. Said under item 26. |
| 12. Relay posts have no retry | Not changed. Said under item 26. |

Also from run 51, fixed in `a5818fc`: a start the runner refuses before its session exists now sends a notice.

## Run 52, item 23: Claude Code's documented hook behaviour (`run52-item23-claude-code-hooks.md`)

Used for `paper_platform/agent_budget_hook.py` (`8ac675b`, `ad12472`, `262218c`). What the documentation does not
say (the usage figures in a subagent's transcript, what a refused call does to the subagent) is marked in the
report; the usage figures were then read on this session's own runs and are said under item 23.

## Run 53, item 26: Render's documentation (`run53-item26-render-docs.md`)

No answer: render.com does not resolve from the session.

# The independent review of Codex's draft (checklist item 35), runs 54 to 59

Greg, 2026-11-24: items 20, 24, 25, 27, 28, 30, 31, 32 and 35 are Claude's to fix and finish. Six reviewers (the
reviewer agent, `claude-opus-5-5`) each read one group of numbers on the branch, reading only. The rule kept when
acting on a report: a fix was made only where the finding is certain from the code and the fix changes no order
sent and no journal field's meaning. Everything else is written under its number for Codex or for Greg.
NautilusTrader's own source at release 1.231.0 was read to settle what the reports marked as depending on it.

## Run 58, item 31: order tags (`run58-item31-order-tags.md`). Platform commit `55e54fd`.

| Finding | What was done |
| --- | --- |
| 1. A normal close does not check its cancellations took effect | Not changed; left for Codex. Read in NautilusTrader 1.231.0 (`backtest/engine.pyx`, `cancel_order`): the cancel event is sent before the call returns, so no second order results. |
| 2. A refused repeat tag leaves no journal row | Fixed: the refusal is journaled. |
| 3. Tag uniqueness rests on rule IDs holding no "-" | Fixed: a plan with such a rule ID is refused. |
| 4. A close refused for a missing quote is not retried | Not changed: a plan decision. Said under item 31. |
| 5. A close with no contracts and no working orders writes no row | Not changed; left for Codex (it adds journal rows and so moves the event budget). |
| 6. Whether NautilusTrader accepts the tags as client order IDs | Settled by reading its source (`identifiers/client_order_id.rs`, `core/correctness.rs`): any non-empty ASCII string, no length limit. |
| 7. Fill IDs may repeat between rules | Not changed; left for Codex. Confirmed in the source (`_generate_trade_id_str`): the ID is made from the venue, the instrument, the time and that engine's own count. |

## Run 59, item 32: credentials (`run59-item32-credentials.md`). Platform commit `fee5336`.

| Finding | What was done |
| --- | --- |
| 1. Pushover values in curl's argument list | Fixed. |
| 2. The deploy key reaches ssh-add through a here-string | Fixed: a pipe. |
| 3. The capture key is set for every step of the job | Fixed: the three steps that use it, in both workflows. |
| 4. The agent socket reaches `pip install` | Fixed in the agent workflow. Left for Codex in the live, record-only and replay workflows (a reordering of his steps). |
| 5. The record-only workflow's two processes inherit every credential | Fixed. |
| 6. A Render address with a password and no user name passes | Fixed in the runner and the dashboard restore. |
| 7. The live launcher's list of withheld names is incomplete | Fixed. |
| 8. `MARKETS_DATA_TOKEN` in the replay workflow | Not changed: it is the fallback when the deploy key is absent. |
| 9. Git children inherit the whole environment | Not changed; left for Codex. |
| 10. SDK errors reach the Actions log as tracebacks | Not changed; nothing found that puts a key in a message. |
| 11. Checkpoint block names are hashes of their unencrypted content | Not changed: a format change. Said under item 32. |
| 12. The relay | Nothing to change. |

## Run 54, item 20: the 5.75-hour stop (`run54-item20-clock-stop.md`). Platform commit `8019fca`.

| Finding | What was done |
| --- | --- |
| 1. The live paper process can be killed before its final journal is pushed | Fixed: 480 seconds, not 120. |
| 2. The replay job has ten minutes after the clock | Fixed: 365 minutes, as the other two. |
| 3. The record-only workflow never starts the shared clock | Fixed: its first step starts it. |
| 4. The flattening order is sent when the market is shut | Not changed. Put to Greg under item 20: the stop can fall in the 5 pm to 6 pm Eastern hour, and which rule gives way is not on record. |
| 5. A failed cancel stops that trade's close | Not changed; left for Codex. With NautilusTrader 1.231.0 the cancel of an accepted order is immediate. |
| 6. Orders the stop cancels are journaled as trade data | Not changed; left for Codex (it changes a journal field). |
| 7. The flattening order mixes fields from two records | Not changed; left for Codex (it changes journal fields). |
| 8. Fill lines on the page carry no administrative mark | Fixed on the page. Taking the trade's time out from an administrative fill is left for Codex. |
| 9. The watchdog waits for the session lock in replay | Not changed; no small fix. |

## Run 56, items 27 and 16: the trade list (`run56-item27-trade-list.md`). Platform commit `de048e0`.

| Finding | What was done |
| --- | --- |
| F1. A trade time shows a bare date, not the trade day | Fixed on the page: every trade row time names its trade day or the 5 pm to 6 pm stretch. |
| F2. A close at the end of the trade day reads as an ordinary close | The row now names the stretch (F1). The order itself is the matter put to Greg under item 20. |
| F3. A timer close shows the timer's time with an earlier message's quotes | Fixed on the page: it says when the quotes were seen. |
| F4, F5, F11. Signals whose orders the event budget cut off | Not changed; left for Codex (`session.py`, where the batch is cut). |
| F6. An unsent administrative close is not labelled | Fixed on the page. |
| F7. A rejected open shows "No order sent" only in the details | Not changed; left for Codex. |
| F8. A manager row borrows its parent's entry | Not changed; left for Codex. |
| F9. The trades API returns bare nanosecond integers | Not changed; left for Codex. |
| F10. An "Earlier events" page lists trades past its cut-off | Not changed: Greg's or Codex's call. |
| F12. Every manager close is labelled "Manager exit" | Fixed on the page. |
