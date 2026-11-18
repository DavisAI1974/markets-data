# Handoff O, end of the twelfth session (2026-11-18)

Branch: `ccr-349e2ffe-07p8od` in `DavisAI1974/markets-data` for data and documents. This file replaces handoff N as
the starting point (N stays as the record of what is built). Every decision of this session, with Greg's words, is
in `root-redesign-20261116/ROOT_GAMEPLAN_DECISIONS.md`, section "Twelfth session" (its last entries are the newest).
Desktop writes to the same branch: fetch before every push.

**Read first, in this order:**
1. This file, in full.
2. `root-redesign-20261116/peak-research-20261117/TRADE_LIFECYCLE_NOTES.md`: the running notes. ADD to it; never
   start another. Its sections dated 2026-11-18 govern where they differ from what is above them.
3. The decisions file, sections "Eleventh session" and "Twelfth session".
4. `root-redesign-20261116/three-renders-samples-20261118/README.md` and its pictures (what he has already seen).

**Do NOT open last week's strategy material** (the handoff and review of 2026-11-13, the fifteen candidates, the
selected cases). Nothing of it is used.

## THE JOB, in Greg's words (2026-11-18, at the close)

"Wait. I also asked for the exhaustion render too. Whatever crypto did to generate those renders do that. If one of
the calcs was a 20 sec. Use it just like crypto did. Look at if the crypto data was altered to be different that
what we have in any way. I want everything in our new exhaustion calc to be exactly like the old calc. Agaim,
desktop has already gotten a great start on this."

"The only difference between the two should be that was crypto and we're doing ng".

What that means, plainly:
- He wants the natural gas exhaustion render to come out of the SAME calculation that made the crypto exhaustion
  graphs of July 7, 2026 (the four-panel picture "Kraken onset->exhaustion arcs REGROUPED BY TYPE"). He judged
  those graphs "basically good enough on their own to trade from". The point is how much they tell.
- Nothing in that calculation is to be improved, swapped or left out. If it used a 20-second roll, the 20-second
  roll is used, the same way. The only difference allowed is the market.
- Before building, find every way the crypto data or its handling differs from what we hold, and either remove
  the difference or put it to him. He asked for this check by name.
- Desktop already started down this road on the earlier (bad) data. Start from what it has; do it on the rebuilt
  data.

## Where things stand

- **No pod was started this session.** The account was read again at the close (the pod list): it shows none.
- Code: Markets branch `claude/wizardly-fermi-0s9nlb` = `ccr-3096f7d6-fst7al` = `b1ed5bf` (brought in by
  fast-forward; no code was changed this session; nothing on the trunk).
- Stored rows and outputs: `root-rows-20231002` `07ff47c`, `-20231003` `261bf0a`, `-20231017` `9dc46c9`,
  `-20231018` `03946e5`. Each now holds a `desktop/` folder (Desktop's peak lives) with its own section in
  `FILES.md`: keep both when `FILES.md` is written again. Clone each shallow. **Never list one with file sizes
  through a partial clone (`git ls-tree -l`): it downloads every file.** Add the files you need by name
  (`git sparse-checkout add /<file>`).
- Stored this session: only documents and the sample pictures (`three-renders-samples-20261118/`). No calculation
  was built or run. No daily store changed except the Desktop addition above.

## THE CRYPTO EXHAUSTION CALCULATION, as its script has it (steps 1, 2 and 4 to 7 read whole; step 3 read in part)

Where it is: Markets branch `claude/davisai-s71-counterparty-capacity-sf1168`, commit `75b15fa` (2026-07-07):
`research/shape_s71/regroup2.py` (drew his picture), `arc_gate.py` and `shape_arc.py` (the pieces it uses),
`two_shapes.py`, `SESSION_HANDOFF_2026-07-07_S71.md`, `SIGNAL_SHAPE_DIRECTION_S71.md` (his own words of that day).
The helpers it calls on the same branch: `_birth_probe.py` (`to_grid`, `_depthK`), `_liquidity_dive.py`
(`build_channels`), `odcore/platform.py` (`run_kraken_cell`, `KRAKEN`), `odcore/flip_detector.py`,
`kraken_book_collector.py`. Fetch that branch shallow and read these files whole before building.

Step by step:
1. THE DATA: the Kraken order book stream for one coin, one record after another (`<coin>_book.jsonl`): the time,
   the mid price, the spread, the size bought and the size sold by takers since the record before, and the resting
   bids and asks. Five coins (btc, eth, sol, xrp, doge), each one recent window of about 40 hours.
2. THE GRID: everything is put on a regular grid of TENTHS OF A SECOND (`to_grid(…, 0.1)`): book figures take the
   last value in each cell and are carried forward; bought and sold are summed in each cell.
3. THE TRADES: made by the platform's own executor, `run_kraken_cell(cfg, mid, buy, sell, best bid size, best ask
   size, half the median spread)` (`odcore/platform.py` on that branch). READ IN PART: `run_kraken_cell`,
   `kraken_flips` and the head of `run_stream` were read; `run_stream`'s body, `swing_maker`, `retime_flips` and
   `detect_flips` were NOT. Read them whole before building. What was read:
   - The turns come from a zigzag on a lean of trades over 600 cells (`WFLIP = 600`) with a reversal level set per
     coin (`rev`: 0.10 for eth, btc and sol; 0.30 for doge; 0.13 for xrp), moved earlier ("early-arm",
     `retime_flips`) where the coin has an `eps` (eth 10, btc 5). `lean_series` is written for one reading a
     second; this work fed it tenths of a second.
   - Each turn becomes a SIMULATED trade ("leg") with an entry (`open_idx`, the ONSET, t = 0), an exit
     (`close_idx`), a side, and a result in bps (`net_bps`). The simulation carries a maker fee and a taker fee
     (the Kraken cells: maker 0), a front-of-the-line fill, a grace of 300 or 600, a price stop per coin (`bail`:
     eth 100, btc 80) and a close improved by 0.5 bps. So `net_bps` is NOT a plain price move: fees, fills and a
     stop are inside it. There is also an entry gate in that file (`_entry_gate`, the divergence read); whether
     this path used it was not established.
   - **`odcore/platform.py` is NOT in the current code.** It went with the crypto-era rules.
4. THE FLOW LINE: `rolling_imb(buy, sell, 20)`: at every cell, bought minus sold over bought plus sold, over the
   last 200 cells (20 SECONDS, `SMOOTH_SEC = 20`). Where nothing traded in those 20 seconds the value is 0.
   Its own comment on the 20: trades were sparse; "a shorter window makes per-leg |imb| a saturated 0/1 square
   wave; 20s recovers a readable per-leg arc without over-blurring the turn".
5. THE ARC of one trade: that line from 45 seconds before its onset to 60 seconds after (`PRE_SEC, POST_SEC =
   45, 60`; 1,051 cells), multiplied by the trade's side so that "with the trade" is up. A trade is left out if
   the 105 seconds do not fit inside the data or its exit is not after its entry.
6. THE FOUR KINDS: short or long by whether the trade lasted at most the MEDIAN length of that coin's trades;
   winner or loser by whether `net_bps` is above 0. Short-loser, long-winner, short-winner, long-loser.
7. THE PICTURE: for each kind, the MEAN of the arcs of that kind (only if there are at least 8), one line per
   coin, four panels, x = seconds from the onset, y = "mean flow". Saved also as `quad_means.npz`.

What that session found with it (its handoff): the arc repeats from trade to trade; the part BEFORE the onset told
the kind of trade out of sample on all five coins (the taller the peak at the onset, the longer and the more often
a winner); how long a trade lasted set where the collapse landed. Four days later
(`S77_REVIEW_FOR_CHATGPT.md` on `archive/crypto`, 2d): matching the entry shape to the winner shapes did not lift
the result; a winner and its losing twin shared the entry shape.

## Crypto against what we hold: a FIRST READ of the differences (code read only; NOT finished)

He asked for this check by name. Finish it first. Each line below is to be confirmed in the code, then either
removed (make ours the same) or put to him once, plainly.

| | Crypto, July 7 | What we hold for the four trade days |
|---|---|---|
| The tape | A collector's stream of book records with bought and sold size per record | Every single exchange message, one row per tick |
| The clock | A grid of tenths of a second | Every tick, to the nanosecond |
| The 20-second flow | Over the last 200 grid cells; 0 where nothing traded | Stored `flow_20s` in `calc-flow_peak-*`: over the last 20 seconds on the received clock, at every tick; EMPTY where nothing traded |
| The side of a trade | As the collector recorded it (check `kraken_book_collector.py`) | The tape's own aggressor side; a trade with no side is counted apart |
| The trades followed | SIMULATED trades of the platform's executor (zigzag on a 600-cell lean, reversal 0.10, maker fills) | No such trades exist for natural gas. We hold the trade legs (print by print), the runs of the quote, the peaks. `run_kraken_cell` has never been run on this tape |
| Winner or loser | `net_bps` of the simulated trade (check what costs are inside it) | Nothing. His standing rule: trade cost is not a market condition; research is gross |
| Short or long | Against the median length | His standing rules: no ranks, no labels put on by us |
| The line drawn | The mean over many trades | His standing rule: any method that combines cases is named to him as averaging before it is written |
| How much data | Five coins, about 40 hours each | One contract, four trade days |
| The session | Round the clock, one unbroken window per coin, all its trades taken together | Cut by trade day (6 pm to 5 pm Eastern), the 5 pm halt and the settlement window marked; each trade day on its own |

THREE THINGS THAT NEED HIS WORD before anything is built. Put them together, once, plainly, with no recommendation
made for him: both sides of each are his own rules.
1. THE TRADES. The crypto arcs follow simulated trades made by the crypto executor. To be exactly like crypto the
   same executor has to be run on the natural gas tape. It is not in the current code, and his rule of 2026-11-16
   says: "NO BITCOIN-ERA RULES ... do not reintroduce any of them, and do not copy one out of old code, an old
   handoff or the archive" (fee floors, maker and taker fill assumptions, crypto-venue strategy rules). Bringing
   the executor back is his explicit word, or he names what the onset is on this tape in its place.
2. WINNER OR LOSER. In crypto it is the simulated trade's `net_bps`, which has fees, fills and a stop inside it.
   His rules: trade cost is not a market condition; research is gross. His word on what a winner is here.
3. THE MEAN AND THE MEDIAN. Each crypto line is the mean over many trades, and short or long is against the
   median. His rules name both (averaging; a rank; a label put on by us). "Exactly like the old calc" asks for
   them. Name the averaging to him in that word; whichever he says, every single trade's own arc can be drawn
   beside it.

## What Desktop has (the "great start")

On this branch, under `research-union-current/`:
- `desktop-peak-lives-on-clock-20261117/`: the life of every peak on the clock, both kinds (also in each daily
  store's `desktop/` folder).
- `desktop-old-family-chain-on-clock-20261117/`: the old family and chain definitions laid on the four trade days,
  kept as reference for how the 55-week run defined and grouped (never an input).
- Its earlier pictures, made on the earlier data and pasted by Greg this session (described in the notes file):
  "Flow lean and midpoint around the birth" (the 20-second lean and the midpoint from 40 seconds before a birth
  to 60 after, against matched controls), the share of births above and below their level, and the first-event
  curves. They are the same kind of picture as the crypto arcs, anchored on a dipole's birth. **They and their
  programs were NOT found on this branch** (searched by file name). Where they are is not known to this session:
  ask Greg, or Desktop through him. If they sit only in last week's folders, that meets "do not open last week's
  strategy material" and is his call.

## What was drawn this session (he has seen all of it)

`root-redesign-20261116/three-renders-samples-20261118/` (README inside). One stretch of trade day Oct 17.
- THE THREE RENDERS HE ASKED FOR, three separate graphs on one axis of real timestamps: (1) the trade price curve,
  drawn smooth through every trade ("smooth" is drawing only); (2) the dipole at the tick; (3) the exhaustion at
  the tick. He looked at the samples: "I am seeing spikes and dips at the same timestamps so thats promising ...
  I wanted to see if the big movements happened in all 3 at the same time and they do".
- The stacked pair for two recorded dipoles born on a trade leg's first trade (trade day Oct 17: 90 of the 267
  dipoles born with a trade sit on the first trade of a trade leg; not yet set beside any second with a trade;
  the other three trade days not counted).
- Claude's calls in those pictures, his to correct: the exhaustion at the tick is the run of trades on one side
  (the peak with no window, stored in `turn_peaks`); the dipole at the tick is the latest run of buying against
  the latest run of selling (a new figure, not a stored calculation; it adds a run's trades together, named to him
  as averaging).

## Open, in order

1. **The crypto-exact exhaustion calculation and its render** (the job above). Finish the difference list; put
   the three rows to him; then lay the calculation out his way (what we want, what it did, what changes: the
   answer to "what changes" should be "the market, and nothing else") for his yes; then build, check, run on
   pods, store, render.
2. **The three renders for all four trade days** (trade price curve, dipole at the tick, exhaustion at the tick),
   with the crypto-exact exhaustion render as its own graph. The dipole at the tick needs his yes as a calculation
   first. The stretch one picture covers is still open (the samples used a count of trades).
3. **The dipoles that line up with trade legs**: all of them, all four trade days, as the stacked pair; the same
   count for any second with a trade, so the 90 of 267 means something.
4. His stacked-pair question, counted with no window (each move of one line, the distance to the nearest move of
   the others, every case listed). By eye he has his answer; it is not measured.
5. Then, carried from handoff N in its order: TELL HIM before the strategies start (he raises the effort
   setting): 15 versions, laid out in one message first, and first how a version is formed blind to its own trade
   day; then his open calls, each put once (deleting last week's two folders from `main`; the five-step process
   and its two streams; Bedrock; Native's missing two hours); removing the stopped chain matching code; the full
   workbooks (with a sheet of the peak lives).
6. Finish reading `STEP1_STEP2_LAYOUTS.md` and `STEP2_PLAN.md` line by line (read by section this session) before
   the strategy lay-out.
7. The layout "Exhaustion with no window" at the end of `STEP1_STEP2_LAYOUTS.md` was put to him and never
   approved. It is overtaken by item 1. Do not build it; mark it so when item 1 is laid out.

## Standing rules as they stand after this session

- THE EXHAUSTION CALCULATION IS THE CRYPTO ONE, EXACTLY. The only difference: that was crypto, this is natural gas.
- "No exceptions! That window gives us nothing but a visual to confirm from" (the 20 seconds), said earlier the
  same session, was not withdrawn. Do not argue one against the other and do not re-ask. Build the crypto-exact
  exhaustion render (20 seconds as crypto used it) AND the tick versions beside it; what counts as a signal is his
  word when they are in front of him.
- THE THREE RENDERS are the trade price curve, the dipole, and the exhaustion. Other lines (the resting orders'
  lean, a running total of lots, the quote) are additions for later, beside them, never in place of them.
- Three separate graphs on one axis of real timestamps. No lines laid over each other at first.
- Everything else in handoff N's standing rules holds (the trade day; only the four trade days in a calculation;
  no averaging without naming it; every trade individually; no ranks, labels, caps or limits; gross; the leakage
  gate; runs on pods in one launch with his go and the price; a read of stored files is told to him first; notes
  written as we go; valid data never discarded; nothing to the Markets trunk without his word; AWS off limits).

## Slips of this session, so they are not made again

- He asked for three named renders and was sent other lines twice ("those aren't the 3 renders I asked for").
  Draw exactly what he names, with his names on it. Offer additions afterwards, separately.
- He was told the crypto exhaustion had no 20-second window. Wrong: it was read off the later files on
  `archive/crypto` instead of the script that made the picture. The July sessions' own branches still exist
  (`claude/davisai-s71-…`, `claude/entry-curve-shape-classifier-b5neon`, `claude/curve-shape-gate-s75-06m1vf`,
  `claude/book-swing-s77-kraken-meomsh`). When he says "like we did months ago", find the script on its own
  session's branch before answering.
- Questions put to him as a form were dismissed. He reads on a phone and answers in his own words: say the call
  you are making, make it, and let him correct it from the picture.
- A listing with file sizes on a `root-rows` branch pulled every file. Do not do it.
- The agent-skills plugin does not load in the container; the router and the git workflow skill were read from
  the pinned public source (tag 0.6.8). A second skill system (Superpowers) loads by itself in this environment;
  his rule is one router only. It was not used.

## TO REVISIT (Greg: carry into every handoff until done)

Native's record is built on predetermined windows (a 20-second roll, a level set from 85 in 100 seconds, 60-second
horizons, a 45-second spacing and a 50-second wait before a dipole is made known), which his "no predetermined
windows" rule does not allow for our own work. He chose to keep Native as it was made for now. In this session it
was used only as a mark saying where to look.
