# Handoff W, end of the twentieth session (2026-11-23, about 9 pm Eastern; trade day Tue Nov 24, 2026)

Branch: `ccr-349e2ffe-07p8od` in `DavisAI1974/markets-data` for data and documents. This file replaces handoff V as
the starting point. Every decision of this session, with Greg's words, is in
`root-redesign-20261116/ROOT_GAMEPLAN_DECISIONS.md`, section "Twentieth session" (the last entries are the newest).
Desktop and Codex write to this branch too: fetch before every push.

**Read first, in this order:**
1. This file, in full.
2. `tasty/RUNNING_LIST.md` in `DavisAI1974/paper-trading-platform`, branch `claude/tasty-runner`: the list of gaps
   and misses to take care of. Greg asked for it; every run adds to it. Line C22 says what is parked.
3. The decisions file, section "Twentieth session", to the end.
4. `paper-trading-20261123/RUNNER_PLAN_20261123.md`, its last section "CHANGES OF 2026-11-24" (what the rules are
   given now), and `strategy-20261123-claude/VERSIONS.md` (CL16 and CL17 are new, after CL15).
5. In the code repository: `tasty/paper/` (the runner) and `AGENTS.md`.

## WHERE THINGS STAND, IN ONE LINE EACH

- THE PAPER RUNNER IS BUILT AND HAS RUN LIVE. All of it is in `DavisAI1974/paper-trading-platform`, branch
  `claude/tasty-runner` (`0772834`), folder `tasty/`. 26 checks pass, all on real recordings and real order records.
- THERE ARE 32 STRATEGIES: Claude's CL01 to CL17 and Codex's CX01 to CX15. CL16 and CL17 were added this session for
  the print with no side (Greg: "The 30 is a jumping off point, not the limit"). 26 run on the tastytrade feed; six
  cannot (CL01, CL02, CL03, CL04, CL09, CL12: they need single orders).
- FROM NOW, RUNS ARE LEDGER-ONLY (Greg: "We can just observe on ledger"). The runner without `--orders` reads the
  live feed, runs all 32 and writes every paper trade with both quotes at each end; nothing is sent. NO ORDER GOES TO
  THE SANDBOX.
- ONE RUN WITH ORDERS WAS MADE (8:05 to 8:12 pm Eastern). It showed that sandbox orders say nothing about the rules:
  the sandbox fills at the market as it is now while its own stream is 900 seconds old, and it refused every buy.
- SANDBOX-ONLY ISSUES ARE PARKED (Greg: "The sandbox specific issues won't be a problem soon so don't spend time on
  them"). RICHER DATA IS COMING (Greg: "we don't need to make system around thin data"). Nothing more is built to
  fit this feed or this sandbox.
- THE SANDBOX ACCOUNT 5WY79188 IS SHORT 13 LOTS OF /NGF7 and is LEFT AS IT IS, on his word. Six sell orders there
  read "Cancel Requested" (five of the run's, and 2207911 of 2026-11-23).
- THE RULES WILL BE REWRITTEN LATER, with the agent program highlighting what to look at (Greg: "I'm not shooting
  for perfection right now, jist feedback on how it's working so far"). Section A of the list is the input.
- NOTHING IS SCORED from this feed. AWS is off limits. No pod exists; none was started. The Markets trunk is
  untouched.

## REPOSITORIES AND BRANCHES FOR THE NEXT SESSION

- markets-data: `ccr-349e2ffe-07p8od` (records, documents, decisions).
- paper-trading-platform: `claude/tasty-runner` (`0772834`), our code in `tasty/` and `tests/tasty_runner/`. It is
  not on the "Markets" environment's repository list: the session attaches it with push access (an approval card).
  Codex works on `main` there (`a7a3cc5` when last fetched): none of his files is touched until Greg says he is
  done. Checked at the end of this session: no file outside `tasty/` and `tests/tasty_runner/` differs from where
  the branch started, and `crypto_ng/tick.py`, `root/calcs/quote_runs.py` and `root/calcs/leg_peaks.py` are
  byte-identical on his `main`, on our branch and on Markets.
- Markets: `ccr-532eaea6-vgz20z` (`65f71a9`); this session's own branch `ccr-d613618f-v7t9jy` is the same commit.
  It holds no paper trade code. Bringing it in first makes the four agents (scout, builder, reviewer,
  frankie-performance-auditor) available to the session.

## THE KEYS

Unchanged from handoff V. The three SANDBOX values are in `paper-trading-20261123/tasty-sandbox.env` (a public
repository, test keys, Greg's choice); load with `set -a; . <that file>; set +a`; check by name only. PRODUCTION keys
are not set and not needed. Checked at the end of this session by exact match: none of the three values is in any
file of `live-runs/` or `step0-20261124/`. The stream library is `websockets==15.0.1`
(`pip install -r tasty/requirements-7e.txt`; a new container does not have it).

## WHAT WAS DECIDED THIS SESSION (Greg's words are in the decisions file)

- Two things at one print: both are written, each as its own event, and no "first" is claimed.
- A gap is only a real break (the stream dropping, a sequence step other than 1 or 2, a print out of order).
- The print with no side gets strategies of its own: CL16 and CL17. The fifteen stay as written.
- Not perfection now; feedback on how it works. Do not build around thin data. Sandbox-only issues are parked.
- Start paper trading; then, after the run with orders: observe on the ledger.
- A list of gaps and misses, kept in the paper trade repository and added to.

Claude's calls, said to him, his to strike: the fix to CL14 (the print whose own quote shows the step can be the
first sell or buy since it); the settlement window bounded as ROOT marks it; the reviewer aimed at the order path
only; the start of a run counted from the first print of any side; a trade open at the end stays open on the ledger.

## THE RUNNER: WHAT IS BUILT

`tasty/paper/`: `events.py`, `feed_tasty.py` (reader), `lines.py` (the two lines, by calling `crypto_ng.tick.reads`
and `tick.line` as they are), `quotes_live.py` (ROOT's quote runs and trade legs as they are), `clock.py` (the
settlement window), `rule_base.py`, `rules_cl.py` (CL01 to CL17), `rules_cx.py` (CX01 to CX15, written by the
builder agent from Codex's text), `ledger.py`, `replay.py` (the engine and a replay of a recording),
`broker_tasty.py` (the order path, sandbox host only), `stream_tasty.py` (the live socket), `runner.py` (the loop),
`close_out.py` (a hand tool for the sandbox account). `tasty/checks/`: six small readers of the raw messages that
import nothing of the runner. `tasty/tasty_7e_check.py` is the 7e check, not edited.

Run the checks: `python3 -m pytest -q -p no:cacheprovider tests/tasty_runner` (26; they need this data branch
checked out; `TASTY_7E_RECORDINGS` names the folder of recordings if it is elsewhere).

WHAT THE CHECKS PROVE: nothing sees a later message (cut equals whole, all 32 rules); the lines equal one pass of
`tick.reads`, at sided prints and at prints with no side; a rule's quote never comes from a Quote message; CL14,
CL16, CL17 and Codex's entry rules open where the raw messages say; a close names the print that showed it; the
fifteen never act at a print with no side; the runner's replay equals the engine's; the fill and position readers
read the real order records. WHAT THEY DO NOT PROVE: that every rule matches its text (one ledger line of each rule
that opened was traced by hand: `paper-trading-20261123/step0-20261124/STEP0_TRACE_20261124.md`; `rules_cx.py` was
read once by the main session and traced by the builder, not by the reviewer); the settlement window, the 4:44 pm
stop and the halt hour (no recording crosses them).

## THE RUNS OF THIS SESSION (records in `paper-trading-20261123/live-runs/`, none scored)

1. `orders-20261124T010517Z/`: the run with orders. 7 minutes, stopped at its order budget. 62 paper trades from 13
   strategies. 19 submits, all sells; 13 filled; 6 answered with a server error and never became orders; 101
   intended orders not sent (43 buys refused by the sandbox, 34 closes held back because their open had not
   filled, 23 cut off by the budget stop, the flatten refused).
2. `closeout-20261124T011335Z/`: the close-out by hand. Six cancels sent (five accepted); the buy of 13 not sent,
   its dry run refused; a dry run of "Buy to Close" refused too.
3. `feed-only-20261124T011440Z/`: 16 minutes, no orders. 183 paper trades. Its file
   `fills-beside-the-market.json` sets each of the 13 fills beside the feed's own prints at the market time it
   filled: each is at the market's bid or offer then, up to 12 ticks from the quote the rule acted on.

## NEXT, IN ORDER

1. LEDGER-ONLY RUNS, each on Greg's go (a paper run needs his explicit go). From `paper-trading-platform`, with the
   keys loaded:
   `python3 -m tasty.paper.runner --out <a new folder under paper-trading-20261123/live-runs/> --account 5WY79188
   --symbol /NGF7 --streamer-symbol /NGF27:XNYM --seconds <N> --max-orders 1`
   NO `--orders`. It signs in, reads the stream and sends nothing; each intended order is written `sent: false`.
   Commit the run's folder when it ends and add the run to section D of the list. The symbol is the January 2027
   contract: check it is still the one to follow.
2. THE RUNNER'S OWN GAPS, the ones that hold on any feed and any broker (list C22 names them): the order budget
   ends the whole run instead of only the orders (C17); the receipt does not show what was left in the account
   (C21); the two lines are worked out again from all the trades at every print, twice (C2); orders go one at a
   time behind a queue (C16); the reviewer's findings not fixed (C12); the stops and windows not yet seen on real
   data (C3); no check of the hump code over a whole recording (C4).
3. THE RULES, for the rewrite: section A of the list. Greg's agent program is to highlight what to look at; ask him
   which program and when.
4. WHEN THE RICHER FEED ARRIVES: the rules and the engine carry over (a rule takes plain events and knows nothing
   of tastytrade); the stand-ins S1 to S7 and the thin-feed handling are dropped or redone (list C7).
5. Later, each on Greg's word: GitHub Actions for the runner (a run stops itself at 5.75 hours); the live page and
   the phone notice; checking Codex's platform when Greg says he is done; the second ROOT.

## THE AGENTS: BUDGETS AND WHAT WAS SPENT (`paper-trading-20261123/agent-runs.jsonl`, runs 11 to 13)

Declared by Greg for this session: builder 300,000, reviewer 250,000. Spent: builder run B1 (Codex's rules) 89,470;
builder run B2 (the order path and the loop) 108,305; reviewer on the order path 62,449. LEFT: builder 102,225;
reviewer 187,551. A run's tokens are read from the notice the harness sends when it returns. The agent types
`builder`, `reviewer` and `scout` were not available at the start of the session; they appeared after the Markets
branch was brought in. The builder's own definition says to show a diff and wait and never to run against market
data: a brief has to say which of those are lifted and why.

## OPEN WITH GREG, EACH PUT ONCE (none holds the work up; he said so)

1. Whether an exit indication of CX05, CX06, CX11 to CX14 closes the position another of Codex's rules opened (as
   built, one switch in `replay.py`) or is only written beside it.
2. Whether Codex writes a strategy of his own for the print with no side.
3. Whether the fifteen should also read the quote a no-side print carries (on the 25-minute recording CL05 passed
   over 70 triggers and opened 42).
4. Codex's wording the runner does not carry yet (list A9).
5. Carried from handoff V, unchanged: the copy of the 7e check on Markets branch `ccr-fffbc766-a1gxpl` (deleted only
   on his word for that branch by name); how a paper fill is priced; where an order-by-order live feed for our own
   platform comes from; and handoff U's list (the delete list, the live store and the phone notice, the open items
   of the plan, `root/research_excel.py`, the Excel workbook, git history, `Basic_equations`).

## SLIPS OF THIS SESSION, SO THEY ARE NOT MADE AGAIN

- Claude wrote two of Greg's answers into the decisions file as decided and began to build on them before he had
  decided: one answer had been sent unfinished and belonged to the other question. Read an answer back in one line
  before recording it as decided when it does not match an option offered.
- Claude read "a strategy for that" as a rule about how the 30 read the feed. He meant a trading strategy of its
  own. When he says strategy, he means a trading strategy.
- Claude changed the start check before the run so that an order already filled did not count, and so let the run
  begin with order 2207911 standing as "Cancel Requested", which handoff V had down as unverified. An open item of
  a handoff is checked before a run that depends on it.
- The order budget stopped the whole run after seven minutes, so the feed was not recorded past the fills; a second
  recording had to be started in a hurry. Say what a stop ends before the run starts.
- Claude wrote a folder name into the list and the decisions file that no output had shown (off by two seconds).
  A path is copied from output, never typed from memory.
- "#run mattpocock-skills" in the kickoff: no skill or plugin of that name was installed; only Superpowers loaded
  again and the agent-skills plugin did not.

## TO REVISIT (Greg: carry into every handoff until done)

Native's record is built on predetermined windows (a 20-second roll, a level set from 85 in 100 seconds, 60-second
horizons, a 45-second spacing and a 50-second wait before a dipole is made known), which his "no predetermined
windows" rule does not allow for our own work. He chose to keep Native as it was made for now.
