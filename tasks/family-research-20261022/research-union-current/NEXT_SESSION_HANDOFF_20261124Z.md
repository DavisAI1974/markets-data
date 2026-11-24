# Handoff Z, 2026-11-24, end of the twenty-second session

## The answer first

- All the session's work was in `DavisAI1974/paper-trading-platform`, branch `codex/strategy-trades-and-mbo-capture`
  (draft PR #5), head `be4d244`. Everything there is DRAFT: never run, never parsed, no check, no test, no paper run.
- Job 1 of handoff Y (the agent program in Markets: `kgraph check`, `extract recheck`, `platform_scope mark`, the
  link between a stale claim and the claim that says otherwise, the manual) was NOT touched. It waits on Greg's word.
- Nothing is on the trunk of any repository. Nothing sits unpushed.

## Where things are

| Repository | Branch | Head |
| --- | --- | --- |
| paper-trading-platform | `codex/strategy-trades-and-mbo-capture` | `be4d244` |
| markets-data | `ccr-39e0401c-g5omlm` (handoff branch `ccr-349e2ffe-07p8od` is merged in; fetch it before every push) | the commit that adds this file |
| Markets | `ccr-39e0401c-g5omlm` | `537749a` (unchanged this session) |

- The checklist: platform `docs/platform/OWN_PLATFORM_WISHLIST_20261123.md`, 35 numbers. Codex has 1 to 19, Claude has
  20 to 35. Item 17 and its two decider agents are Codex's: do not start them. A box is checked only when on main.
- Greg's decisions, word for word, and Claude's slips: `root-redesign-20261116/ROOT_GAMEPLAN_DECISIONS.md`, section
  "Twenty-second session".
- Agent runs, model and tokens: `paper-trading-20261123/agent-runs.jsonl` (runs 43 to 64; the next is 65).
- Reviewer reports word for word and what was done with every finding: `paper-trading-20261123/review-20261124/`.
- Keys, names and places only: `paper-trading-20261123/KEYS_WHERE_THEY_ARE.md`. Read it; do not ask Greg for a key.

## Greg's decisions this session (all in the decisions file)

1. A live run whose 5.75 hours would land in the 5 pm to 6 pm hour flattens before 5 and ends at 5. Built (item 20).
2. A live run whose 5.75 hours land after 6 pm is NOT cut short: it carries into the next trade day.
3. The paper runs use the STORED TAPE FED LIKE LIVE (workflow `purchased_mbo_paper.yml`, tape `purchased-archive`).
4. Retain the books through a reset. On the stored tape they already are (counted: one clear per file, always the
   first record). For a live feed the way is written under item 6, not built.
5. A speed bar for the stored tape. Started, not wired (below).
6. Agent budgets are to go up; the figures and the measure are still his to give.
7. Keys go in the cloud environment by his hand; a note of names and places is kept (done).

## What the next session does first

1. THE SPEED BAR (item 12). `paper_platform/playback.py` holds the steps and the pace arithmetic; nothing calls it.
   Left to build, in this order, each said under item 12:
   - Runner: `--speed` on `paper_platform/run.py` and a `speed` box on `purchased_mbo_paper.yml` (pass it only when
     `original_run` is empty: a receipt replay runs the earlier commit's code). `pace_to_record` waits by the pace;
     keep its positional arguments (`test_ledger.py` passes `base` as a number). A change is journaled as its own kind
     `playback speed` under `s.lock`, never `status`. The speed goes in the receipt constants and in the status
     packet (`Publication.packet`).
   - Phone: a table and two routes on `paper_platform/relay.py` (the page stores the wanted speed with the viewer
     sign-in; the runner asks for it with the writer token); a thread in `run.py` asks every two seconds; a failed
     ask keeps the speed. The bar itself in `views.py` and `monitor.html` (the template is a `string.Template`: a `$`
     in script must be doubled or kept out). Let the new kind through the strategy filter in `stream_rows`.
   - Read `paper_platform/test_*.py` against every change before pushing (two slips this session came from not
     doing that).
2. THE HELD ITEMS on 20 to 35, each under its number: cancels at the stop journaled as trade data (20); timer orders
   not pushed before the next tick in live (25); journal rows with no source message, the code commit on rows (28);
   the flatten order with no signal link (30).
3. Job 1 in Markets, when Greg says.

## Waiting on Greg (do not re-ask what is decided; these are not decided)

- Which "API function" he means for the list (the 35 items have none).
- The new agent budget figures and the measure (on record: scout 300,000, builder 600,000, reviewer 250,000 by the
  harness total; the true spend of a reviewer was 3 to 5 million tokens by all calls).
- His word to switch on the agent budget hook (`paper_platform/agent_budget_hook.py`, registered nowhere).
- A parse-only pass over the edited files (it is a check, so it needs his go).
- Whether the platform's `Flow` windows, which call `crypto_ng.tick.line` and not `reads`, stand as the crypto
  formula.
- The Pushover names entered in the Markets environment and in the GitHub Actions secrets.
- The first paper run: his go, with its budgets told first. The message budget needs sizing again for a faster run.

## The four explanations he asked for (given in chat, kept here)

- RETAINING THE BOOKS. On the stored tape the only clear records are each file's first: the two Sunday ones are the
  exchange's start-up and seat the week; the five others are the vendor's UTC-file opening, compared with the carried
  book and never applied. So the book is carried all week. Record: `review-20261124/item6-clear-records-counted.md`.
- THE STORAGE DECISION AND THE GAP (item 7). It is where a LIVE recording is kept so it outlives the loss of the
  GitHub runner. Checkpoints go to markets-data every 60 seconds plus the time of one publish. A runner lost in that
  span loses our receive times for those deliveries (the records can be bought again, our times cannot). On the
  stored tape there is no recorder, so this gap does not exist.
- QUEUE POSITION. Only six rules post their opens (CL02, CL09, CL12, CX01, CX09, CX10); every close crosses.
  NautilusTrader takes the whole size at the price as "ahead" when the paper order rests, lowers it only on trades at
  that price, and sets it to nothing on ANY full cancel at that price. So a posted paper order can fill later than a
  real one (partial cancels ahead are not counted) or sooner (one cancel at the price puts it at the front). It is an
  estimate. An exact queue could be kept from ROOT's own book; not built.
- THE STORED TAPE FED LIKE LIVE. Built already. At live pace one run covers about 6 pm to 11:45 pm Eastern of the
  named trade day. The speed bar is what lets one run cover the whole trade day (4x fits 23 hours in 5.75).

## Rules that bit this session

- Tell Greg before anything runs, even a git-only measurement.
- An interrupt kills background agents: tell each to write findings to a file as it goes.
- Read the tests against every engine or matcher change before pushing.
- Never type a key value into a file, a command or a reply.
