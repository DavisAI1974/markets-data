# Handoff V, end of the nineteenth session (2026-11-23, about 7 pm Eastern)

Branch: `ccr-349e2ffe-07p8od` in `DavisAI1974/markets-data` for data and documents. This file replaces handoff U as
the starting point. Every decision of this session, with Greg's words, is in
`root-redesign-20261116/ROOT_GAMEPLAN_DECISIONS.md`, section "Nineteenth session" (the last entries are the newest).
Desktop and Codex write to this branch too: fetch before every push.

**Read first, in this order:**
1. This file, in full.
2. `paper-trading-20261123/RUNNER_PLAN_20261123.md` (the build plan; its section "CHANGES AFTER THE REVIEW" wins)
   and `paper-trading-20261123/RULES_ON_TASTY_FEED_20261123.md` (the 30 rules against the feed).
3. The decisions file, section "Nineteenth session", to the end.
4. `paper-trading-20261123/OWN_PLATFORM_WISHLIST_20261123.md` (what Greg wants in our own platform; pasted to Codex).
5. In `DavisAI1974/paper-trading-platform`, branch `claude/tasty-runner`: `tasty/` (our code) and `AGENTS.md`.

## WHERE THINGS STAND, IN ONE LINE EACH

- STAGE 7e, THE SANDBOX HALF, IS DONE (not tested: the production stream, and any OPTION order). The tastytrade SANDBOX signs in, lists natural gas futures and options, and FILLS a natural gas
  future, buy and sell (orders 2207792 and 2207911, 1 lot /NGF7, both at 3.534). Records: `paper-trading-20261123/7e/`.
- THE SANDBOX'S OWN STREAM WORKS WITHOUT PRODUCTION KEYS. It is exactly 900 SECONDS BEHIND the market. It carries
  trade prints with price, size, the buy/sell side (missing on 9 of 107 prints in one recording, 141 of 440 in the
  longer one), a time in MILLISECONDS, and the bid and offer at the print; quote messages in about half-second steps
  with no time. It carries NO single orders, NO exchange end-of-event mark, NO nanoseconds, and not every trade.
- PRODUCTION KEYS: not needed until live trading (Greg). `prod-stream` has never been run.
- THE 30 ON THIS FEED, UNGRADED (Greg: "Let's see if our strategies sell even with thin data. We won't give it a
  bad mark if it doesn't but maybe it will"): 6 cannot run (CL01, CL02, CL03, CL04, CL09, CL12: they need single
  orders); 24 run with named stand-ins. Nothing from this feed is ever scored.
- THE RUNNER: PART A IS BUILT; ITS PLUMBING IS CHECKED, ITS RULES ARE NOT YET READ AGAINST THEIR TEXT (feed reader, the two lines, quote runs, trade legs, Claude's 9 runnable
  rules, the ledger, a replay that sends nothing). PART B IS NOT STARTED (Codex's 15 rules and the order path).
  No strategy has sent an order yet.
- THE CODE MOVED. All paper trade code is in `DavisAI1974/paper-trading-platform`, branch `claude/tasty-runner`
  (`afcf107`), folder `tasty/`. It was removed from Markets (`ccr-532eaea6-vgz20z`, `65f71a9`).
- OUR OWN PLATFORM: Codex is doing the first build in the same repository (`main`, `paper_platform/`). Claude checks
  it and adjusts it ONLY when Greg says Codex is done. Claude does not touch Codex's files or `main` before that.
- A SECOND VERSION OF ROOT for live and other data is decided (beside ROOT, never replacing it). Not started.
- AWS is off limits. The S3 bucket is undecided: leave it. No pod exists; none was started.

## REPOSITORIES AND BRANCHES FOR THE NEXT SESSION

- markets-data: `ccr-349e2ffe-07p8od` (records, documents, decisions).
- paper-trading-platform: `claude/tasty-runner` (our code). It is NOT on the "Markets" environment's repository
  list: the session must attach it with push access (an approval card). First step there: fetch Codex's `main` and
  confirm `crypto_ng/tick.py`, `root/calcs/quote_runs.py` and `root/calcs/leg_peaks.py` are still byte-identical to
  Markets.
- Markets: `ccr-532eaea6-vgz20z` (`65f71a9`), brought in first on the session's own branch. It holds no paper trade
  code any more. The trunk is untouched this session.
- In `RULES_ON_TASTY_FEED_20261123.md`, stand-in S3 (the quote between prints from the Quote messages) is
  SUPERSEDED by G1 of the plan: the rules read the quote from the prints' own bid and offer only.

## THE KEYS

- SANDBOX client ID and secret: `paper-trading-20261123/tasty-sandbox.env` (public repository, his choice). Load
  with `set -a; . <that file>; set +a`.
- SANDBOX REFRESH TOKEN: in the same file, as `TASTY_SANDBOX_REFRESH_TOKEN` (Greg, 2026-11-23: "Put it in file").
  Loading the file sets all three sandbox values; nothing has to be pasted. If a sign-in is refused, the token was
  revoked or replaced: "Create grant" on the sandbox tool page gives a new one (the long string starting `eyJ`,
  shown ONCE in the yellow box; the short code starting `G` is the grant's id and does not sign in), and it replaces
  the line in the file. The cloud environment "Markets" has no environment variables saved.
- PRODUCTION (three `TASTY_PROD_*`): not set, not needed yet.
- Network: `api.cert.tastyworks.com`, `developer.tastytrade.com` and `tasty-demo-dxlink-md-ws.dxfeed.com` (the
  sandbox stream, approved by Greg this session) are allowed on environment "Markets".
- GitHub: the Claude GitHub App is installed on `paper-trading-platform` (Greg, this session).

## WHAT 7e FOUND, FOR ANYONE BUILDING ON IT

- The sandbox refuses futures orders in the daily halt hour (5 to 6 pm Eastern): HTTP 422
  `tif.futures_session_not_active` (`7e/sandbox-order-20261123T223131*`).
- The sandbox says its accounts are "not approved for futures" and fills them anyway.
- tastytrade's own page: the simulator fills at the MIDDLE of its quote rounded to the tick (up for a buy, down for
  a sell). The BUY fits (compared with the stream's quote 30 seconds later); the SELL was not compared with a quote
  (it fell between two recordings). Greg's rule is NO MID PRICE: a sandbox fill price is recorded as what the sandbox
  said, beside both quotes, and is never a result.
- Order 2207911 had its fill recorded and the position went flat, but its STATUS stayed "Live" through ten polls.
  The program then asked to cancel it ("Cancel Requested"); its final status was NOT read after that: unverified.
  A new run begins by confirming no position and no live order.
  Read fills and positions, never status alone.
- The dry run returned two server errors (HTTP 500) before it passed; the program's retry handled it.
- The access token lasts 15 minutes; an order path must sign in fresh before each submit.
- Whether the sandbox's fill quote is the same 15-minute-old market as the stream is NOT proven (two fills only).

## THE RUNNER: WHAT IS BUILT, WHAT IS NEXT

Built (part A, `tasty/paper/` on `claude/tasty-runner`; 3 tests pass on the real recording, rerun by the main
session. WHAT THE TESTS PROVE: nothing sees a later message (cut equals whole), the lines equal ROOT's functions,
and a rule's quote never comes from a Quote message. WHAT THEY DO NOT PROVE: that any rule's trigger matches its
text. `rules_cl.py` (423 lines) has not been read by the main session or the reviewer): `events.py`, `feed_tasty.py`, `lines.py` (calls `crypto_ng.tick.reads` and `tick.line` as they are; Greg's
word for that is in `CLAUDE.md` on Markets branch `ccr-532eaea6-vgz20z` only, NOT on the trunk), `quotes_live.py` (ROOT's `QuoteRuns` and `Legs` as they are), `rule_base.py`,
`rules_cl.py`, `ledger.py`, `replay.py`. Run the checks with
`python3 -m pytest -q -p no:cacheprovider tests/tasty_runner` (it needs a markets-data checkout; `TASTY_7E_RECORDINGS`
names the folder of recordings).

On the 10-minute recording (run 5), ungraded, no orders: CL06 opened 17, CL14 14, CL15 10, CL07 5, CL10 4, CL11 4,
CL05 3, CL08 2, CL13 0; the six that need single orders 0. These counts show the rules FIRE; they do not show the
rules are RIGHT (see step 0).

NEXT, in order:
0. BEFORE RUN B BUILDS ON THE SAME INTERFACE: for each rule that opened, trace one ledger line by hand against
   the recording and the rule's text in `strategy-20261123-claude/VERSIONS.md`. Fix or hand back what does not match.
1. PUT TO GREG, the builder's hand-back points that are his (not yet put to him):
   a. Rules 3 and 4 of "what holds for all fifteen" (the settlement window 2:28 to 2:30 pm Eastern; the close at
      the end of the trade day) are NOT in the code yet. Rule 3 needs the boundary said (is 2:30:00 in or out).
   b. Where a rule says "first" of two things and both show at one print, the verdict is written "undecided: both
      happened at one print" (CL06, CL07, CL08).
   c. A print with no side is never shown to a rule; what it does to the quote or a leg reaches the rule at the
      next print that has a side, so it can close a trade late and never open one.
   d. A gap is counted when the feed's day volume grows by more than the prints seen. That definition is the
      builder's.
   Calls already in the code, his to strike: the G3 start is counted from the first print of ANY side; a trade
   still open when a recording ends stays open on the ledger (`closed: null`), the flatten of S6 is not in part A.
   Smaller ones, Claude's to settle: a trade print that is not "NEW" or not a valid tick stops the reader (none
   seen yet); prints out of order stop the reader (none seen yet).
2. Rerun the replay and the checks on the 25-minute recording (`7e/sandbox-stream-20261123T233543*`; a third of its
   prints have no side).
3. BUILDER RUN B (Sonnet, 300,000 tokens, budget already declared to Greg): Codex's 15 rules (`rules_cx.py`, from
   `strategy-20261123-codex/VERSIONS.md` on markets-data branch `codex/ng-blind-20261123`), the order path
   (`broker_tasty.py`) and the runner loop (`runner.py`), all as the plan says. It writes straight into
   `paper-trading-platform` on `claude/tasty-runner`.
4. REVIEWER (Opus, 250,000 tokens) on the finished code.
5. THE CANARY: 30 minutes from the session, on Greg's go, with an order-count budget said to him first. Record the
   stream through each order and 15 minutes past it, to see what quote the sandbox fills from.
6. Not yet testable on real data: the 4:44 pm stop, the halt hour, the settlement window (the recordings cover
   6:00 to 6:10 pm and about 6:20 to 6:45 pm on the feed; the second one starts mid-session, a real case for the
   G3 start rule). A recording across those hours is needed first.
7. Later, each on Greg's word: GitHub Actions for the runner (he sets the sandbox keys as GitHub secrets); the live
   page and the phone notice (outside services, named to him first); the other platforms; the second ROOT.

## THE AGENTS: BUDGETS AND WHAT WAS SPENT (`paper-trading-20261123/agent-runs.jsonl`, runs 8 to 10)

Declared to Greg: scout 150,000; reviewer on the plan 200,000; builder 600,000 (split by Claude into two runs of
300,000); reviewer on the code 250,000; 1,200,000 in all. Spent: scout 122,420; reviewer 101,431; builder run A
156,983. Left: builder run B 300,000; reviewer 250,000. A run's tokens can only be read when it returns.

## OPEN WITH GREG, EACH PUT ONCE

1. The builder's points a to d above.
2. The copy of the 7e check on the earlier session's Markets branch `ccr-fffbc766-a1gxpl`: deleted only on his word
   for that branch by name.
3. (Settled: the sandbox refresh token is in the sandbox key file.)
4. How a paper fill is priced (his word; until then both quotes at each end and no result figure).
5. Where an order-by-order live feed for our own platform comes from (a price is shown to him first).
6. Carried from handoff U, unchanged: the delete list waiting for his word "delete"; the live store and the phone
   notice; the open items of the plan; `root/research_excel.py`; the Excel workbook; git history; `Basic_equations`.

## SLIPS OF THIS SESSION, SO THEY ARE NOT MADE AGAIN

- Claude told Greg the sandbox feed had no trades and no sides after looking at it during the halt hour through a
  15-minute delay. Measure the delay before saying what a feed lacks.
- Claude said "23 of 30 can run" before checking what each rule reads. The table came after; the count was 24, with
  stand-ins Claude had not yet named.
- Claude deleted the 7e program's file while a 25-minute recording was still running; the program could not write
  its receipt. The receipt was written by hand and says so. Do not remove a program that is running.
- Claude asked Greg three times for a "refresh token" when the page in front of him showed a grant id. Ask what the
  page's label says, once.
- The agent-skills plugin (`using-agent-skills`) did not load in this session; only Superpowers did.

## TO REVISIT (Greg: carry into every handoff until done)

Native's record is built on predetermined windows (a 20-second roll, a level set from 85 in 100 seconds, 60-second
horizons, a 45-second spacing and a 50-second wait before a dipole is made known), which his "no predetermined
windows" rule does not allow for our own work. He chose to keep Native as it was made for now.
