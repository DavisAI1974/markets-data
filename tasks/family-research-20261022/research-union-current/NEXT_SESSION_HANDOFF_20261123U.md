# Handoff U, end of the eighteenth session (2026-11-23)

Branch: `ccr-349e2ffe-07p8od` in `DavisAI1974/markets-data` for data and documents. This file replaces handoff T as
the starting point. Every decision of this session, with Greg's words, is in
`root-redesign-20261116/ROOT_GAMEPLAN_DECISIONS.md`, section "Eighteenth session" and the entries after it (the last
entries are the newest). Desktop writes to the same branch: fetch before every push.

**Read first, in this order:**
1. This file, in full.
2. `CLAUDE_ARCH_PLAN_GRAPH_ENGINEERING_ADOPTION_20261123.md` and `README_HANDOFF_20261123.md` (Markets, trunk and
   session branch, `research/kalshi/frankie_boss/`): Greg's adopted plan. Stage 7 is the current work.
3. The decisions file, from "Eighteenth session" to the end.
4. `strategy-20261123-claude/VERSIONS.md` (beside this file): Claude's 15 strategies as paper-trading rules (v2 on
   top, the first proposals below).
5. Markets `strategies/tasty_7e_check.py` (session branch): the 7e check program, its docstring and `--help`.

## WHERE THINGS STAND, IN ONE LINE EACH

- STRATEGIES: Claude's 15 (CL01 to CL15) and Codex's 15 (CX01 to CX15) are all different and ALL 30 GO INTO PAPER
  TRADING, each on its own (Greg). No winner. Paper trading is the test. Do not change Claude's because of Codex's.
- PAPER-TRADING ROUTE (Greg): free on the platforms first, starting with the TASTYTRADE SANDBOX; then the others
  (NinjaTrader: he can sign up; CME practice; Tradovate); then our own open source one changed to fit
  (NautilusTrader is Claude's candidate: it reads Databento order-by-order data and has a paper sandbox).
- THE PLAN (Greg's graph engineering adoption, from his chat with Claude as architect): NOW stage 7, paper trading
  on the tastytrade sandbox. Signals from TASTYTRADE'S PRODUCTION QUOTE STREAM on a read-only login; orders ONLY to
  the sandbox. Frankie does not change. Stages 2 to 6 and 8 are filed. Stage 1 (four agents) is committed.
- STAGE 7e, THE FIRST STEP: built, reviewed three times, committed, NOT RUN. It waits on two logins (below).
- AWS is not available. The S3 bucket is undecided: leave it, its data and the S3 code exactly as they are.

## THE AGENTS (stage 1, Greg: "the full sonnet, haiku and opus plan")

All four run on Anthropic models, in Claude Code sessions (Greg: "I'm fine with them running in code sess"):
scout on Haiku (reads and locates), builder on Sonnet (writes code from a settled plan), reviewer on Opus (checks
plans and final changes), frankie-performance-auditor on Sonnet (Codex wrote its first version; Codex runs none of
them). Files: `.claude/agents/` on the Markets trunk (`beb3836`) and on the session branch. The CLAUDE.md roles
section says how the main session routes work. Every agent run gets a declared budget first; each run's model and
tokens are recorded (`paper-trading-20261123/agent-runs.jsonl`, seven runs of stage 7e, about 1.24 million tokens).

Codex's read-only auditor and verifier tasks run with these agents, in a Claude Code session, by
`CODEX_PROMPT_AMENDMENTS_20261123.md`. NOT STARTED: each begins on Greg's word.

## THE 7e CHECK: WHAT IT IS AND WHAT IT NEEDS

Markets `ccr-fffbc766-a1gxpl`, `strategies/tasty_7e_check.py` (`2ca5096`; `pip install -r
strategies/requirements-7e.txt`). Three sub-commands, each run on Greg's say:
1. `sandbox-lookup`: signs in to the sandbox, lists the account, natural gas futures and the option chain.
2. `sandbox-order`: dry-runs one natural gas order; ONLY with `--submit` places it, polls it, cancels if asked, and
   records positions. Every number (symbol, side, type, time in force, quantity, polls, pages) comes from the
   operator; none is chosen by the code. Use a DAY order: the sandbox page says an immediate-or-cancel order with no
   stock leg is cancelled, which is the likely reason Codex's futures orders were turned away on 2026-11-09.
3. `prod-stream`: signs in to production READ-ONLY (scope read, a guard allows only GETs and refuses any order path),
   gets the natural gas streamer symbols, then (with `--streamer-symbol`) records everything the DXLink stream sends,
   whole, with our receive time in nanoseconds, and a plain summary (event types, field names, time fields, any
   buy/sell side, any order id).
Guarantees: an order is never re-sent; every key and token is scrubbed from every write and print; a receipt is
always written; output only to a markets-data folder (it refuses Markets). Output goes to
`paper-trading-20261123/7e/` beside this file.

THE KEYS:
- SANDBOX (test keys, no money): in `paper-trading-20261123/tasty-sandbox.env` beside this file, on Greg's word
  ("Put in there they are only test keys"). THIS REPOSITORY IS PUBLIC: that file is readable by anyone; he chose
  it knowingly. Load with `set -a; . <that file>; set +a`. It holds the client ID and secret; THE REFRESH TOKEN IS
  STILL MISSING ("Create Grant" on the sandbox application): when he gives it, add it to that file's last line,
  commit and push, so he never gives it again. SUPERSEDED, Greg: "Or cloud is fine too anywhere I'm not posting them
  every sess": the sandbox REFRESH TOKEN goes in the cloud environment's settings (below), not in that file.
- PRODUCTION, read-only, data only (client ID, client secret, refresh token from his real account): NEVER in any
  file in git. He enters them once in the cloud environment "Markets" settings (Edit, Environment variables) as
  `TASTY_PROD_CLIENT_ID`, `TASTY_PROD_CLIENT_SECRET`, `TASTY_PROD_REFRESH_TOKEN`, and with them the sandbox's
  `TASTY_SANDBOX_REFRESH_TOKEN`; every later session reads them from there. FIRST THING IN A SESSION: check those four
  names are set (names only, never print a value); if one is missing, tell him which. The stream needs a fully onboarded customer; natural gas quotes may need a data entitlement.
- NETWORK: `developer.tastytrade.com` and `api.cert.tastyworks.com` are allowed on environment "Markets". Production
  needs `api.tastyworks.com` and the DXLink host the quote token names: an approval card for each, when used.

WHAT 7e MUST ANSWER: does a natural gas future fill in the sandbox at all (tastytrade's own page says only stock fills
have been seen); does the stream carry every trade with its buy/sell side (the two lines need it); does it carry
single orders with numbers (six of Claude's rules need it: CL01, CL02, CL03, CL04, CL09, CL12); at what timestamp
resolution. The answers decide which of the 30 rules can run on tastytrade.

## THE RUNNER (7b), RULES GREG SET, NOT BUILT

- On GitHub Actions. A job STOPS ITSELF AT 5.75 HOURS. At the stop it FLATTENS EVERY POSITION; each closing order is
  marked "flattened at the 5.75-hour stop" and is NOT trade data. EACH RUN STARTS OVER NEW; nothing carries over.
  First runs are single jobs started on his go; a hand-over between jobs comes later if wanted.
- A BUDGET: the moment any budget is reached, everything stops and he is notified on his phone at once. Holds for
  agent runs too.
- REAL TIME: he must see what is created, produced and learned at any moment. Claude's call: every signal, order,
  fill and status goes the moment it happens to a live store shown on one page for his phone, and is appended to the
  git record in markets-data, pushed every minute and at once on every order and fill. The live store and the phone
  notice are outside services: NAME THEM TO HIM BEFORE ANYTHING IS SET UP.
- Credentials for the runner live in GitHub secrets, set by Greg. Starting the runner needs his go.
- Live signals read today's market, outside the four trade days: Claude's reading is that his word to run stage 7
  covers it, kept in its own folder apart from ROOT.

## OPEN WITH GREG, EACH PUT ONCE

1. THE DELETE LIST, waiting for his word "delete" (or "delete rules" for the first group). markets-data `main`:
   `paper-rules/20261109/` (128 files), `carry-forward/20261109/` (27), their lines in `MARKET_DATA_INDEX.md`; and the
   old research he already said to discard: `claude-independent-research-20261113/` (246; it holds the earlier
   trade-leg record of 8 files he kept on 2026-11-17), `claude-code-cases/` (70), `replay-artifacts/` (22),
   `claude-code-pins/` (11), `claude-code-derived/` (4), `research-union-current/codex-review-and-gaps-20261113/
   REVIEW_AND_GAPS.md` (1). Not in it: the 13 `codex/` branches and old paper files on Markets branches (each by name).
2. The live store and the phone notice for the runner (outside services).
3. The open items of the plan: the metric of each keep-if-better loop; Granite as the grounding checker or replaced
   after the stage 8 test; when the filed stages go ahead; the S3 bucket.
4. Carried from handoff T: `root/research_excel.py` still holds the removed sheet writer; the Excel workbook in parts
   at his word; rewriting git history only on his word; `DavisAI1974/Basic_equations` not attached.

## WHAT EXISTS NOW

- Markets trunk `claude/kalshi-s79-kickoff-ij8t9o` `beb3836`: the stage 1 set (four agents, the CLAUDE.md roles
  section, the plan, its index, the amendments) on top of Codex's `79517f6`.
- Markets session branch `ccr-fffbc766-a1gxpl` `ec2e86f`: the ROOT code (`a556589`) plus the stage 1 set, the plan
  documents, Codex's verifier plan, and `strategies/` (the 7e check). Not on the trunk: ROOT and `strategies/`.
- markets-data `ccr-349e2ffe-07p8od` (this branch): `strategy-20261123-claude/` (VERSIONS, EVIDENCE, EVIDENCE_COUNTS,
  ACCESS_RECORD, BLIND_FORMATION, OPEN_QUESTIONS), `paper-trading-20261123/` (README, agent-runs.jsonl), the
  decisions, the notes (eighteenth session sections) and the further research list (items 18 to 20 added).
- The four daily branches: unchanged this session.
- Codex's strategies: markets-data `codex/ng-blind-20261123` `ad10921`, `strategy-20261123-codex/` (read after
  Claude's rules were pushed; nothing of Claude's was changed by them).
- Runpod: no pod exists; balance $31.30 at the start of the session.

## SLIPS OF THIS SESSION, SO THEY ARE NOT MADE AGAIN

- Claude began building its own paper engine (a replay of the stored tape) before reading the earlier chats on
  paper trading. Greg had said months before: "Do not substitute our own standalone historical strategy backtest
  for those platform paper trades." Read the chats when he points to them; the written record is not enough.
- The first 15 held a version that never opened a trade and warnings with no side. A strategy is a rule that opens
  and closes a trade.
- A full checkout of the Markets trunk (4 GB) was started for a three-file change and stopped. Use a shallow clone
  with only the needed paths.
- A push to the trunk was tried before Greg's explicit word; the session's safety check refused it. He then gave it.
- Long answers. He reads on a phone: the answer in the first lines.

## TO REVISIT (Greg: carry into every handoff until done)

Native's record is built on predetermined windows (a 20-second roll, a level set from 85 in 100 seconds, 60-second
horizons, a 45-second spacing and a 50-second wait before a dipole is made known), which his "no predetermined
windows" rule does not allow for our own work. He chose to keep Native as it was made for now.
