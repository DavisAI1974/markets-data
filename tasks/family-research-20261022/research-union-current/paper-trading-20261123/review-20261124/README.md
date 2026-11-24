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
