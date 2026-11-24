# Handoff Q, end of the fourteenth session (2026-11-18)

Branch: `ccr-349e2ffe-07p8od` in `DavisAI1974/markets-data` for data and documents. This file replaces handoff P as
the starting point. Every decision of this session, with Greg's words, is in
`root-redesign-20261116/ROOT_GAMEPLAN_DECISIONS.md`, section "Fourteenth session" and the entries after it (the
last entries are the newest). Desktop writes to the same branch: fetch before every push.

**Read first, in this order:**
1. This file, in full.
2. `root-redesign-20261116/peak-research-20261117/TRADE_LIFECYCLE_NOTES.md`: the running notes. ADD to it; never
   start another. Its sections dated 2026-11-18 govern where they differ from what is above them.
3. The decisions file, from "Fourteenth session" to the end of the session entries.

**Do NOT open last week's strategy material** (the handoff and review of 2026-11-13, the fifteen candidates, the
selected cases). Nothing of it is used.

## Where it stopped, in Greg's words

"w`need to get the individual trade renders. we decided tjhat the full day doesn't really tell us much when done on
one render"; then "save the data out of the pods in git and we'll continue later".

THE NEXT THING IS THE INDIVIDUAL TRADE RENDERS. One thing was put to him and NOT answered: what one picture is a
picture of. Do not draw them until he says.
- Every single print: 143,979 pictures over the four trade days, most of them near copies of each other.
- Every trade leg (the trade price curve cut into its own moves): 5,660 on trade day Oct 17, about 24,000 in all.
- Every trade of the program: 1,794; 1,895; 1,672; 1,682 (7,043).
Claude's call, stated to him, his to correct: one picture per TRADE LEG, each the four graphs on one clock, its
start and end from the data; trade day Oct 17 first on one pod, then the other three on his go; tell him the
stored size before the other three (about 24,000 pictures is large for git).

## What he decided this session (do not re-ask)

- THE UNIT IS THE EVENT, NOT THE TRADE DAY. "I feel like dipole and exhaustion are single trade event outputs and
  do a great job explaining those events"; "Or maybe a few trades in a row but not entire days". No render of a
  whole trade day.
- THE MEASURE of any output: does it give a better understanding of the PRICE / TRADE CURVE.
- NOTHING IS TYPED, LABELLED OR PUT IN THE EXCEL SHEETS until it is decided with him. This covers the thirteenth
  session's tick renders and everything made this session.
- NO HARD CODED BEGINNING OR END TIME. "We need the data to be telling us what those times are". No number of
  seconds, typed clock time or count of trades sets where a picture or an output starts or ends.
- NO TIME GRID, and no mention of one as a time: code and data made on one are deleted. In the record pages the
  old figure is written "[the old time step]".
- NO MADE-UP NUMBERS in a session, not even to check code. A new calculation is checked on real tape, on a pod.
- WHEN NEW DATA REPLACES OLD: delete the old while the run is going, confirm it is gone, and only then touch the
  new.
- EXHAUSTION RENDERS MADE ON OLD OR BAD DATA ARE DELETED.
- The order of work he set at the start: the exhaustion rerun on the pods first; renders pulled while it runs.

## What exists now

**Code:** Markets branch `ccr-92cbec22-u0cbuj`, `e8cd626` (the session's own branch; nothing on the trunk). It holds
everything of `claude/magical-allen-kncdpa` (`7c98593`) plus:
- `crypto_ng/tick.py`: the rules and numbers of the July 2026 crypto exhaustion calculation, written at the
  nanosecond and standing on their own (the 20-second line; the turn finder's 60-second lean and turn amount; in
  at the first trade on the other side after a turn; the 30-second wait). The July program's own files were
  removed from the branch on his word (code made for a time grid); the originals stay on Markets `75b15fa`.
- `root/crypto_ng_tick.py`: the data run and the single-event pictures (`--trade`, `--moment`, `--tape`,
  `--stretch`). `whole_humps` sets a picture's two edges from the line.
- `root/continuing.py`: the search for runs of trades and dipole stretches that continue over more than one trade.
- `root/four_graphs.py`: one event as four separate graphs on one clock.
- `CLAUDE.md` carries the new rules (no time grid or mention of one; no made-up numbers; what `crypto_ng/` holds).

**Stored, each file fetched and proved against its receipt, `FILES.md` up to date on every branch:**
`root-rows-20231002` `36be8d2`, `-20231003` `fe6a8a8`, `-20231017` `b2af4e2`, `-20231018` `6abd6c0`.
- `crypto-ng-tick/` (all four): the 20-second exhaustion line for the whole trade day at every moment it changes;
  the 60-second lean; every turn; every trade of the program; EVERY TRADE ON THE TAPE on its own line (38,127;
  41,410; 33,703; 30,739); and every HUMP of the 20-second line on its own line. Trade day Oct 17 also holds 64
  single-event pictures (the stretch of the twelfth session, and the program's trades 1051 to 1080).
- `continuing/` (all four): every run of trades on one side and every stretch the dipole at the tick stays on one
  side, each on its own line with its trades, what the trade price did across it and the trade legs under way.
- `four-graphs/` (Oct 17 only): his stretch as four graphs on one clock, two pictures.
- REMOVED this session: the eleventh session's 920 exhaustion sheets and their index tables (`renders/`), and the
  first run of this session, replaced by the second.

**The counts (each trade day on its own; leads, not results; nothing filtered):**

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| Humps of the 20-second line | 4,459 | 4,579 | 4,103 | 4,163 |
| ... holding more than one trade | 2,254 | 2,361 | 2,128 | 2,130 |
| ... more than one trade leg under way | 1,380 | 1,438 | 1,280 | 1,245 |
| ... holding no trade | 1,324 | 1,290 | 1,148 | 1,193 |
| Runs of trades on one side | 11,568 | 12,685 | 10,402 | 9,550 |
| ... more than one trade | 7,417 | 7,993 | 6,477 | 5,850 |
| ... more than one trade leg under way | 1,270 | 1,421 | 1,358 | 1,249 |
| Stretches of the dipole on one side | 6,880 | 7,541 | 6,056 | 5,566 |
| ... more than one trade | 5,094 | 5,604 | 4,513 | 4,139 |
| ... more than one trade leg under way | 2,300 | 2,612 | 2,203 | 1,986 |

## Open with him, each put once

1. What one picture is a picture of (above). Blocks the individual trade renders.
2. Whether a brief dip through zero should end a hump. As built it does, so a picture's lead-in can be short (the
   program's trade 1051: 2.9 seconds). He has the pictures.
3. Steps or curve for a single event's exhaustion line. Both are printed for every picture stored.
4. The dipole at the tick was stored by the thirteenth session on Claude's call, without his yes as a calculation.
   The dipole search of this session stands on it.
5. The 920 exhaustion sheets removed were made on the REBUILT rows, not on the earlier bad data. Told to him; they
   come back from git in one step if he wants them (each `FILES.md` names the commit).
6. Carried from handoffs O and P, in their order: his stacked-pair question counted with no window; TELL HIM
   before the strategies start (he raises the effort setting): 15 versions laid out in one message, and first how
   a version is formed blind to its own trade day; his open calls (deleting last week's two folders from `main`;
   the five-step process and its two streams; Bedrock; Native's missing two hours); removing the stopped chain
   matching code; the full workbooks; the Excel sheets for the stored pictures (nothing goes in until decided).

## NOT PROVED, said to him

That the trades of the program equal what the July files would have made. The July files worked on a time grid and
are not run. Every other check passed on the real tape (both lines counted a second way at every read; the 20
seconds equal to the stored flow on every tick; the humps and the stretches hold every trade once).

## How a launch goes now (as done this session)

- The session REFUSES to run a calculation on market data in the session; small reads of stored tables went
  through, a script that walked a stretch did not. Do not plan on it: the look goes on a pod.
- This session's cloud environment is "Markets" with LIMITED network. Every new pod address needs an approval
  card (`update_environment`, add `<pod id>-8000.proxy.runpod.net`; take the dead ones off in the same card).
- ONE POD CAN RUN ALL FOUR TRADE DAYS: four helpers, each pinned to its own CPU, all at the same time (the search
  ran this way and passed first time in ninety seconds for about 2 cents). General Purpose `cpu3g`, 8 CPUs, $0.32
  an hour; read the price again at the time. Pass `dataCenterIds` with United States centres.
- The pod's command clones the code branch (`root` and `crypto_ng` only) and each trade day's `root-rows` branch,
  serves `/root/work/out` on port 8000 and writes `STATUS`, `CODE_COMMIT` and `ROWS_COMMIT` beside each trade day's
  output, so `python3 -m root.pod_fetch <address>/d<trade day> <trade day> <commit> --into <folder> <job>` proves
  every file before it is stored. The commands used are in the decisions file's entries for this session.
- KEPT SO IT IS NOT DONE AGAIN: two of four pods sat at "container is starting" and never came up, and the session's
  worker restarted twice while pods were up; a run quoted at 40 cents cost about $2.40. A pod that is not up in a
  few minutes is deleted and its trade day run elsewhere. After ANY restart, read the account first.
- Store, push, confirm each push on the remote, THEN delete the pods and read the account.

## Slips of this session, so they are not made again

- A made-up list of numbers on a time grid was used in the session to check new code, and told to him only after.
  Against two of his rules. Deleted; now a written rule in `CLAUDE.md`.
- Pictures were cut at edges set by Claude (typed clock times; 45 and 60 seconds; neighbouring trades). The data
  sets the edges now.
- He was told 4,053 runs of trade day Oct 17 are a single trade. That was a count of runs with no length in time.
  By trades: 3,925 single, 6,477 with more than one.
- A whole trade day of a line made from single prints tells him nothing. Draw events.
- Questions put to him as a form are dismissed. Say the call, make it, let him correct it from the picture. The
  one exception this session: a choice whose size differs a hundredfold (what one picture is a picture of).
- The agent-skills plugin does not load in the container; the router and the git workflow skill were read from
  the pinned public source (tag 0.6.8). Superpowers loads by itself; his rule is one router only. Not used.

## TO REVISIT (Greg: carry into every handoff until done)

Native's record is built on predetermined windows (a 20-second roll, a level set from 85 in 100 seconds, 60-second
horizons, a 45-second spacing and a 50-second wait before a dipole is made known), which his "no predetermined
windows" rule does not allow for our own work. He chose to keep Native as it was made for now. In this session it
was not used.
