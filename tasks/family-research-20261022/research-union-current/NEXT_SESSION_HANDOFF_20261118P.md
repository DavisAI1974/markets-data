# Handoff P, end of the thirteenth session (2026-11-18)

Branch: `ccr-349e2ffe-07p8od` in `DavisAI1974/markets-data` for data and documents. This file replaces handoff O as
the starting point. Every decision of this session, with Greg's words, is in
`root-redesign-20261116/ROOT_GAMEPLAN_DECISIONS.md`, section "Thirteenth session" (its last entries are the newest).
Desktop writes to the same branch: fetch before every push.

**Read first, in this order:**
1. This file, in full.
2. `root-redesign-20261116/peak-research-20261117/TRADE_LIFECYCLE_NOTES.md`: the running notes. ADD to it; never
   start another. Its sections dated 2026-11-18 govern where they differ from what is above them.
3. The decisions file, sections "Twelfth session" and "Thirteenth session".

**Do NOT open last week's strategy material** (the handoff and review of 2026-11-13, the fifteen candidates, the
selected cases). Nothing of it is used.

## THE JOB, in Greg's words (2026-11-18, at the close)

"And we should probably have the ticks to be nano since our data is nano"; "Definitely run it on nano ticks. .1 is
losing too much data"; "Delete .1 outputs and renders. We don't keep wring dayta"; "We've gone over numerois times";
"And the pod ran the exhaustion calcs for 30k+ trades each day.for 4 days in a matter of minues earlier? Something
doesn't sound rigjt"; "We're going to have to rerun days with the new tick time anyway right?"; "let's make new
handoff, commit and push and print drop in for new chat and save rerun for new session."

What that means, plainly:
- THE EXHAUSTION CALCULATION IS RUN AGAIN AT THE TICK, on all four trade days. Every trade at its own nanosecond.
  No grid of tenths of a second, no grid of any size. This is decided; do not put it to him again.
- The first run of this session is WRONG DATA by his word. Its outputs and renders are deleted and none is stored.
- He expects an exhaustion line for each of the 30,000 and more trades of a trade day. The first run did not do
  that (see below). This is the first thing to settle with him.

## What happened in this session, plainly

1. The crypto exhaustion calculation was read whole and the list of differences finished (the notes file).
2. He decided: "Bring back the program and just designate it crypto and ng so we know what it is at a later date.
   And it's crypto iutpots if are any will now go into our excel sheet. They would be for observation or
   vaelrification purpose only". The crypto trading program is back, byte for byte, as `crypto_ng/` in Markets.
3. He decided the rest: no winner or loser; no average ("we took the average of the trade types to get a
   simplified version ... We will want to do our trades individually and see how they separate organically. Like
   the reversal of that crypto process"); no short or long label before a run ("We will want to see how the long
   and short prints behave but not give them that label prior to run"); "Each trade should have its own
   exhaustion graph. No more than one graph per render"; "We also want to be measuring exhaustion prior to trade
   start and after trade ends"; "Part of exhaustion research is to see if there are prebirth signals".
4. Built and run on four pods on his go ("Then go as long as it runs exactly like crypto"): the exhaustion job and
   a second job for his three renders and the stacked pairs. Both passed their checks on all four trade days.
5. He looked at the first exhaustion render and ruled the run wrong: nano ticks, not tenths of a second.

### What the first exhaustion run did, and the two ways it was wrong

- IT PUT THE TRADES ON A GRID OF TENTHS OF A SECOND, because the Kraken collector did and the July program walks
  cells. Claude stated that as a call ("our trades are summed into tenths of a second, the way the Kraken
  collector did it") and it is against a rule he has given many times: rows are ticks, nothing collapsed, timed
  to the nanosecond.
- IT DID NOT MAKE A LINE FOR EVERY TRADE OF THE TAPE. It read every tape trade (30,739 to 41,410 a trade day) only
  as a total inside its tenth of a second, and made an exhaustion arc for each trade OF THE PROGRAM: the program
  makes its own trades. Counts of that run, given once so the mismatch is plain; they are from deleted data and
  are NOT to be used: 1,332; 1,441; 1,251 and 1,270 program trades on the four trade days. That is why four trade
  days took seconds. Claude never put that count in front of him before the run, against his "There should be a
  lot more than 600 trades per day". Before any run from here: say how many trades the run will make a line for.

## Where things stand

- **No pod exists.** Four were made at 04:18 UTC and deleted at 04:41 UTC (about 23 minutes at $1.28 an hour for
  the four). The account was read after the delete: none.
- **Code:** Markets branch `claude/magical-allen-kncdpa`, `7c98593` (the session's own branch; nothing on the
  trunk). Its `CLAUDE.md` carries the new rule (every calculation at the tick, timed to the nanosecond) and the
  one exception for `crypto_ng/`. It holds everything of `claude/wizardly-fermi-0s9nlb` (`b1ed5bf`) plus:
  - `crypto_ng/`: the July program (`flip_detector.py`, `swing_maker.py`, `info_dipole.py` byte for byte;
    `platform.py` with three import lines changed), `PROVENANCE.md`, `ng.py` (the natural gas row: sol's row).
    `tests/crypto_ng/test_provenance.py` proves the fingerprints. `CLAUDE.md` carries the one exception under "no
    bitcoin-era rules".
  - `root/crypto_ng_exhaustion.py`: the REFUSED tenth-of-a-second job. It stops at once (`REFUSED`). Kept as the
    record of the July steps and of the checks worth keeping (the inputs check, the recount, the comparison with
    the stored flow). It is to be written again at the tick.
  - `root/tick_renders.py`: the three renders at the tick and the stacked pairs. Run and stored (below).
  - `root/pod.py`, `root/pod_fetch.py`: the two jobs wired in (`calc:crypto_ng,ticks`, and `moment:`, `trade:`,
    `curve:` to print one trade).
- **Stored this session** (the made-at-the-tick outputs only), in a folder `tick-renders/` on each daily branch,
  each `FILES.md` brought up to date: `root-rows-20231002` `8ea723a`, `-20231003` `f1a7684`, `-20231017` `12e7890`,
  `-20231018` `1988900`.
  - `tick-dipole-<trade day>.parquet`: the dipole and the exhaustion at the tick on every tick of the trade day.
  - `three-renders-<trade day>-NNN.png` (64, 70, 57, 52 pictures): his three renders for the whole trade day. 600
    trades to a picture is a SIZE OF PICTURE ONLY; every trade is in a picture. He read "600" as a cap on the
    trades: say it this way.
  - `dipole-leg-pair-<trade day>-<dipole>.png` (99, 118, 90, 97) and the table of all dipoles born with a trade.
  - Check passed on every tick of all four trade days: the run of trades equals the stored `turn_peaks`.
- **THE DIPOLE AT THE TICK WAS STORED ON CLAUDE'S CALL, WITHOUT HIS YES AS A CALCULATION.** Handoff O said it needed
  his yes first. It was stated to him as a call in the go message (with the three renders) and he did not speak
  to it. It is the figure of the samples he looked at in the twelfth session (the run under way against the run
  before it). Say so when the renders are shown; if he changes what the dipole at the tick is, the table and the
  pictures are made again and the old ones go in the same change.
- **HE HAS NOT LOOKED AT THE STORED THREE RENDERS OR THE STACKED PAIRS.** Show him. His "No more than one graph per
  render" was read as being about the exhaustion pictures; the three renders are three graphs in one picture and
  the pair is two, as he first asked. He did not answer that reading. If he wants single pictures it is a change
  of drawing only.
- **NOT stored, deleted on his word:** everything of the tenth-of-a-second exhaustion run (the grid, the program's
  trades, the arcs, the printed graphs of two trades). Nothing of it reached git.
- **The counts the stacked pairs gave** (stored, in each `TICK-RENDERS-<trade day>.json`; counts only, no test of
  chance): of the recorded dipoles born with a trade, those with the first trade of a trade leg in the birth
  second: 99 of 288, 118 of 335, 90 of 267, 97 of 315. Of ALL seconds of the trade day that hold a trade, those
  holding the first trade of a trade leg: 4,088 of 10,330; 4,595 of 11,482; 3,803 of 9,963; 3,532 of 9,405. About a
  third either way: by this count a dipole born with a trade does not pick out the start of a trade leg more
  often than any second with a trade does.

## FIRST in the next session: two things that need his word, put once and together

No recommendation is made for him on the first; both sides are his own words.
1. **WHICH TRADES GET AN EXHAUSTION LINE.** The trades of the crypto and ng program (it makes its own, on the order
   of a thousand or two a trade day; the count at the tick will be its own and is told to him before the run), OR
   every trade on the tape, each as its own start (30,739 to 41,410 a trade day). He said "Bring back the
   program", and he also believed the run had covered "30k+ trades each day". If every tape trade: say what
   starts and ends a single print's line, since a print has no length (the stored candidates: the run of trades
   on one side it belongs to, its trade leg). Said with it, so its size is plain: the 20-second line at every
   trade's own tick is ALREADY STORED (`flow_20s`, `flow_bought_20s`, `flow_sold_20s` in `calc-flow_peak-*`, on
   every tick of all four trade days, this tick included, the received clock). A line for every tape trade is
   then mostly a read of stored columns around each trade, plus the moments a trade leaves the 20 seconds with no
   tick. No program is needed for that.
2. **"EXACTLY LIKE CRYPTO" AT THE TICK.** The July program exists only on a grid of cells. At the tick its rules
   have to be written again on the clock. Lay it out his way (what we want, what crypto did, what changes) and
   get his yes before any code:
   - What stays: every rule and every number. The 20-second line. The turn finder's lean over 60 seconds (its
     600 cells). The turn amount 0.10. In at the next trade on the other side. The wait of 30 seconds (its 300
     cells). 45 seconds before and 60 after as the least a picture shows.
   - What changes: no cells. Every trade enters each line at the nanosecond it was received and leaves it at the
     nanosecond exactly 20 (or 60) seconds later. The lines are written as every moment they change, each with
     its own time. The turn finder is walked over those moments, not over tenths of a second.
   - Said plainly to him: this is no longer the July code run byte for byte; it is the July rules on our clock.
     The byte-for-byte program stays in `crypto_ng/program/` as the record.

DECIDED, not to be asked again: nano ticks; no winner or loser; no average; no short or long label before a run
(each trade's length is a stored number); one picture per trade with one graph; the program is named "crypto and
ng" and its outputs are for observation and verification only; wrong data is deleted, not kept.

## What the rerun has to carry (Claude's layout to bring him; NOT approved, nothing built)

- THE LINE AT THE TICK. The stored `flow_20s` (`calc-flow_peak-*`) is already the 20-second line read at every
  tick on the received clock. It is EMPTY where nothing traded in the 20 seconds; crypto wrote 0 there. His
  standing rule keeps it empty. What the stored column does not hold: the moments a trade leaves the 20 seconds
  when no tick arrives. The rerun writes the line as a table of every moment it changes.
- BEFORE THE START AND AFTER THE END. "We also want to be measuring exhaustion prior to trade start and after
  trade ends"; "It looks lie we are truncating the exhaustion data in the render at the start and end". The line
  exists for the whole trade day, so nothing is lost; a picture has two edges. The crypto cut (45 before the
  start, 60 after the start) stops before a long trade ends. Tried and seen by him only as the first print: from
  the trade before to the trade after, never less than 45 before the start and 60 after the END. In a busy
  stretch the neighbours are close and the picture still looks cut. To settle with him from pictures.
- PREBIRTH. "Part of exhaustion research is to see if there are prebirth signals"; "Should we just run for the
  entire 23 hours to try to find additional findings?" Yes: the line is made for the whole trade day, so what it
  did before every trade's start is there for every trade, each read on its own.
- CURVE OR STEPS. "And we want the line to look like a curve and not like straight lines right or does it matter?
  Look at crypto render from july". Told: the July lines were smooth because each was an average of hundreds of
  trades; one trade's line moves in steps (it changes only when a trade enters or leaves the 20 seconds). A
  smooth curve through its own points is drawing only, as with the trade price curve, and makes a flat stretch
  and a jump look like a slide. The code can print either (`curve:`); the curve was never printed for him. Print
  one trade both ways and let him say.
- THE DATA CHECK. "It's one thing to matchnfile sizes but it's another check to make sure we have the data the
  files are calling". Every receipt lists each input the program is handed, where it comes from on our tape and
  how much of it was there, with the sizes proved equal to the tape's own totals. Keep it. (Read in the first
  run, tape totals not tied to the grid: trades with no side on the tape 2,230; 1,870; 2,647; 2,408, which go into
  neither bought nor sold. To be proved again by the rerun's receipts.)
- THE NINE BOOK LEVELS. He asked whether crypto used nine more levels of the book than we do. No: Kraken's records
  held ten levels, the July script loaded them and the exhaustion calculation never read levels 2 to 10. They
  were used by a different crypto calculation (the lean of the resting book, July 8 to 11). We hold every order,
  so they can be built on his word.
- THEN, when the rerun is stored: the exhaustion render for the one trade carried over from the twelfth session
  (trade day Oct 17, the stretch of the three renders from 11:58:32.200 Eastern), one trade, one graph; and the
  program's outputs into the Excel file as sheets named "crypto and ng <trade day>", every row linked to its
  picture, Desktop's sheets kept.

## How a launch goes (as done this session)

- The session REFUSES to run a job on market data in the session (its permission check stopped a dry run twice).
  The first run of new code is on the pods; a fault is fixed and that piece run again on the same pods.
- This session's cloud environment ("markets-data") had open network, so no approval card was needed for the pod
  addresses. Read the next session's own environment (`get_environment`) before counting on that.
- One pod per trade day, Runpod MCP `create-pod`: image `python:3.12`; `cpu` `cpu3g` with 8 vCPUs ($0.32 an hour
  each, read the price again at the time); `disk` 10; `ports` `8000/http`; `env` `POD_WORD` (a random word made in
  the session, never in git); `entrypoint` `bash -c`; `cmd`:
  `mkdir -p /root/work && cd /root/work && git clone -q --depth 1 --filter=blob:none --sparse --branch <branch>
  https://github.com/DavisAI1974/Markets code && git -C code sparse-checkout set root crypto_ng && python3
  /root/work/code/root/pod.py <trade day> <branch> <commit> calc:<jobs>`.
- Progress: `https://<pod id>-8000.proxy.runpod.net/STATUS` (send the agent name `curl/8`). A further run:
  `.../run?word=<word>&commit=<40 hex>&job=<job>`.
- Fetch and prove: `python3 -m root.pod_fetch https://<pod id>-8000.proxy.runpod.net <trade day> <commit the pod
  last ran> --into <folder in a clone of root-rows-<trade day>> <jobs>`. Clone each daily branch shallow and
  sparse (`--filter=blob:none --sparse`, then `git sparse-checkout set --no-cone /FILES.md`) and add new files with
  `git add --sparse`. NEVER list a daily branch with file sizes.
- Store, push, confirm each push, THEN delete the pods and read the account.

## Open, in order

1. The two things above; then the layout at the tick for his yes; then build, first run on the pods (one launch,
   his go at the time with the price, the count of trades said first), check, store, delete the pods.
2. The exhaustion render for the one trade carried over; steps and curve side by side for him to choose.
3. The program's outputs into the Excel sheets (observation and verification only).
4. Show him the stored three renders and stacked pairs; his word on one graph per render for them, and on the
   dipole at the tick as a stored calculation.
4b. The stored pictures have NO EXCEL SHEET yet. His standing rule: pictures are saved alongside the Excel sheets,
   each row linked to its picture. Add to `ROOT_dipoles_pinned.xlsx` (fetch first; keep Desktop's sheets) a sheet
   per trade day from `three-renders-index-<trade day>.parquet` and one from `dipole-leg-pairs-<trade day>.parquet`,
   every row linked to its picture in `tick-renders/` on that trade day's branch. A read of stored files: tell
   him first.
5. Carried from handoff O, in its order: his stacked-pair question counted with no window; TELL HIM before the
   strategies start (he raises the effort setting): 15 versions, laid out in one message first, and first how a
   version is formed blind to its own trade day; then his open calls, each put once (deleting last week's two
   folders from `main`; the five-step process and its two streams; Bedrock; Native's missing two hours); removing
   the stopped chain matching code; the full workbooks (with a sheet of the peak lives).
6. Finish reading `STEP1_STEP2_LAYOUTS.md` and `STEP2_PLAN.md` line by line before the strategy lay-out. The
   layout "Exhaustion with no window" at the end of the first is overtaken; do not build it.

## Standing rules as they stand after this session

- NANO TICKS. Every calculation is made at the tick, each trade at its own nanosecond. No grid of tenths of a
  second or of any size, and that includes anything copied from crypto.
- WRONG DATA IS DELETED, NOT KEPT ("We don't keep wrong data").
- THE CRYPTO AND NG PROGRAM is the one exception to "no bitcoin-era rules", on his word; observation and
  verification only; its outputs go into the Excel sheet under that name.
- NO WINNER OR LOSER. NO AVERAGE. NO SHORT OR LONG LABEL before a run; a trade's length is a number.
- EVERY TRADE INDIVIDUALLY: its own line, its own graph. No more than one graph per render (as read: the
  exhaustion pictures).
- EXHAUSTION IS MEASURED BEFORE A TRADE STARTS AND AFTER IT ENDS; prebirth signals are part of the research; a
  render must not cut the line off at the start and the end.
- BEFORE A RUN, SAY WHAT IT WILL COVER: how many trades get a line, and how long it should take.
- Everything else in handoffs N and O holds (the trade day; only the four trade days in a calculation; no
  averaging without naming it; no ranks, labels, caps or limits; gross; the leakage gate; runs on pods in one
  launch with his go and the price; a read of stored files is told to him first; notes written as we go; valid
  data never discarded; nothing to the Markets trunk without his word; AWS off limits; the 20-second window is
  used in the exhaustion calculation as crypto used it and is otherwise a picture to confirm from).

## Slips of this session, so they are not made again

- The trades were put on a tenth-of-a-second grid because the crypto collector did. "Exactly like crypto" never
  outranks "rows are ticks, timed to the nanosecond". When a crypto step would collapse ticks, say so to him and
  do it at the tick.
- The run's reach was not said before it ran. He was thinking of every trade on the tape; the run followed the
  program's own trades. Say the count first.
- Pages of 40 panels and pictures holding every trade at once were proposed. He wants one trade, one graph.
- He asked for the render of one trade and got a picture cut at fixed marks ("It looks like we are truncating").
- An in-session dry run was attempted after telling him; the session refused it. Do not plan on one.
- Questions put to him as a form are dismissed. Say the call, make it, let him correct it from the picture.
- The agent-skills plugin does not load in the container; the router and the git workflow skill were read from
  the pinned public source (tag 0.6.8). Superpowers loads by itself; his rule is one router only. Not used.

## TO REVISIT (Greg: carry into every handoff until done)

Native's record is built on predetermined windows (a 20-second roll, a level set from 85 in 100 seconds, 60-second
horizons, a 45-second spacing and a 50-second wait before a dipole is made known), which his "no predetermined
windows" rule does not allow for our own work. He chose to keep Native as it was made for now. In this session it
was used only as a mark saying where to look.
