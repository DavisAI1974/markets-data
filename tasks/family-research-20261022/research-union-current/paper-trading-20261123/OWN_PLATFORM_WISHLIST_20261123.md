# Our own paper trading platform: what we want (2026-11-23)

Asked by Greg for pasting into a chat session. Source: Greg's decisions in ROOT_GAMEPLAN_DECISIONS.md (eighteenth
and nineteenth sessions), handoff U, and the 7e records in `7e/` beside this file. Items marked DECIDED are Greg's
words. Items marked OPEN wait on his word. Items marked SUGGESTED are Claude's and are his to strike.

OUR OWN PAPER TRADING PLATFORM: WHAT WE WANT

WHAT IT IS
1. Paper trades natural gas futures (and their options later) on a live feed. No real money, no real orders.
2. All 30 strategies run (Claude's CL01 to CL15, Codex's CX01 to CX15), each on its own, never mixed. DECIDED
3. A strategy is a rule that opens and closes a trade. Each rule is a file in git; each change is a commit. DECIDED
4. Our own, open source, changed to fit. NautilusTrader is the candidate (reads Databento order-by-order data and
   has a paper sandbox). SUGGESTED

THE DATA
5. Order-by-order feed: every single order with its id, every trade with its buy/sell side, nanosecond times. The
   tastytrade sandbox feed gave best bid/ask and last trade only so far, which is why we build our own.
6. The exact order book kept for the whole week, seated at the exchange's Sunday start-up, carried straight through.
   Never restarted at midnight UTC. DECIDED
7. Everything the feed sends is recorded whole, as it arrives, with our receive time in nanoseconds. Raw, nothing
   dropped. DECIDED
8. Real data only. No made-up numbers, not even to test code. DECIDED

THE CALCULATIONS
9. A SECOND VERSION OF ROOT does the live calculations. It sits beside ROOT, never replaces it, and uses ROOT's own
   calculation code so live and historical numbers come from the same math. DECIDED
10. Dipole and exhaustion are the crypto formulas on the natural gas tape (60 and 20 seconds), read at the
    nanosecond. DECIDED
11. Every rule sees only what is known at that tick. Check built in: the trades opened on a tape cut at a tick
    equal the trades opened on the whole tape up to that tick. DECIDED
12. Replay mode: the same platform runs a stored trade day's tape, tick by tick, with the same code as live.
    SUGGESTED

THE RULES OF THE HOUSE
13. A TRADE DAY is 6 pm Eastern the evening before to 5 pm Eastern on the named date. The 5 to 6 pm hour is its own
    marked stretch: no trades, messages kept. Never a bare "day" or date. DECIDED
14. NO MID PRICE anywhere. DECIDED
15. NO TRADE COST in any research figure: no fee, slippage, or fill assumption. DECIDED
16. NO AVERAGING, pooling, ranking or labels. Each trade is its own line. DECIDED
17. How a paper fill is priced: OPEN, Greg's word. Until then each paper trade carries both quotes (bid and ask) at
    its entry and its exit, and no result figure.
18. If the feed lacks what a rule needs, that rule's trades are marked "not scored: the feed lacks <what>" and stay
    out of all scoring. DECIDED

THE RUN
19. Runs on GitHub Actions. No AWS. DECIDED
20. A run STOPS ITSELF AT 5.75 HOURS, flattens every position, and marks each closing order "flattened at the
    5.75-hour stop": not trade data. DECIDED
21. Each run starts over new. Nothing carries over. DECIDED
22. Nothing starts without Greg's go. DECIDED
23. A BUDGET: the moment any budget is reached everything stops and Greg is notified on his phone at once. Holds for
    agent runs too. DECIDED

WHAT GREG SEES
24. REAL TIME: every signal, order, fill and status the moment it happens, on one page that reads well on a phone.
    DECIDED
25. The same events appended to the git record in markets-data, pushed every minute and at once on every order and
    fill. DECIDED
26. A phone notice for: a budget stop, a run stop, a failure. The live store and the notice service are named to
    Greg before anything is set up. OPEN
27. Per strategy, a plain list of its trades: time in, time out, both quotes at each end, why it opened, why it
    closed. No summary number until Greg sets one. SUGGESTED

THE RECORD
28. Append-only: every signal, order, fill and status change, each with its time in nanoseconds, the rule version
    (git commit) that made it, and the feed messages it was made from. DECIDED
29. A receipt for every run: code commit, inputs, constants used, files written with their fingerprints. DECIDED
30. Every order is traceable back: fill to order to rule version to the finding the rule rests on. DECIDED (plan 7d)
31. An order is never sent twice. Each carries its own unique tag. DECIDED
32. Keys and tokens never in any file, print or commit. DECIDED
33. Output goes only to markets-data, never to the Markets code repository. DECIDED

ONLY ADD
34. Replace no existing file or layout. ROOT, its four-trade-day gate and its tests stay as they are. DECIDED

WHO BUILDS
35. Codex does the first build. Claude checks it after and makes the adjustments needed. DECIDED
