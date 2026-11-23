# Handoff S, end of the sixteenth session (2026-11-23)

Branch: `ccr-349e2ffe-07p8od` in `DavisAI1974/markets-data` for data and documents. This file replaces handoff R as
the starting point. Every decision of this session, with Greg's words, is in
`root-redesign-20261116/ROOT_GAMEPLAN_DECISIONS.md`, section "Sixteenth session" and the entries after it (the last
entries are the newest). Desktop writes to the same branch: fetch before every push.

**Read first, in this order:**
1. This file, in full.
2. `root-redesign-20261116/peak-research-20261117/TRADE_LIFECYCLE_NOTES.md`: the running notes. ADD to it; never
   start another. Its sections dated 2026-11-23 govern where they differ from what is above them.
3. The decisions file, from "Sixteenth session" to the end of the session entries.
4. Markets `CLAUDE.md` on `ccr-26ff219b-72monm`: the rules "DIPOLE AND EXHAUSTION MEAN THE CRYPTO FORMULAS" and
   "THE NATURAL GAS DIPOLE AND EXHAUSTION ARE USED FOR STRATEGY. CRYPTO DATA IS NOT".

**Do NOT open last week's strategy material** (the fifteen candidates, the review and handoff of 2026-11-13, the
selected cases). Claude opened Codex's review once this session, on Greg's word, for the research questions only;
nothing of it is used. The research QUESTIONS are in `root-audit-20261116/RESEARCH_INTENTIONS.md` (no results).

## FIRST: THE RESEARCH THREADS RUN (his word: "let's start new session starting with these")

- BUILT, NOT RUN: Markets `ccr-26ff219b-72monm` `2df4f14`, `root/research_threads.py`. It reads the earlier
  research QUESTIONS again on the rebuilt data. Nothing new is calculated on the tape: the stored move steps, the
  stored resting lines, the stored natural gas exhaustion and dipole lines and the rows are laid side by side.
- IT MAKES, for each trade day: `research-moves-<trade day>.parquet` (one line per move in price: a trade leg, a
  run of the best bid, a run of the best ask; 37 columns), `research-humps-<trade day>.parquet` (one line per
  hump of the 20-second exhaustion line; 59 columns) and `RESEARCH-THREADS-<trade day>.json` with the counts.
- THE RUN: one pod, all four trade days side by side. About 36,000 moves and 4,100 to 4,600 humps a trade day
  (17,304 humps in all). Estimate, never run: about five minutes, two to three cents at $0.32 an hour. HE HAS NOT
  GIVEN THE GO IN THE NEW SESSION: show the price, wait for the word "go".
- Launch: `DAYS` left as the four; `bash code/root/pod_leg_renders.sh <full commit> research_threads`. Fetch with
  `python3 -m root.pod_fetch <address>/d<trade day> <trade day> <commit> --into <folder> research_threads` into a
  new folder `research-threads/` on each daily branch.
- TWO CHECKS BEFORE ANYTHING IS SAID FROM IT: (1) the job's count "how the first level emptied by the second
  step" for the best ask up and the best bid down must equal `peak-research-20261117/HOW_A_LEVEL_EMPTIED.json`;
  (2) read the job's count of first steps where the stored exhaustion line equals the step line's own 20-second
  flow, and where it does not.
- THEN: read the counts for him, each trade day on its own, as leads (no test of chance is made). Then the Excel
  columns for these two tables: put the column list to him first (his rule: nothing in a sheet until decided).
- NOT IN THE RUN, said to him: the outside figures; where in the trade day; the orders at every level of a move
  and one order's life after a part fill (new calculations, to be laid out first); Codex's information measure
  (Claude's answer: not as it is; a tick version would be a new formula, his to say; Claude has not read
  Codex's code for it).

## SECOND: THE STRATEGY STEP (not started)

- He was told before it starts so he can raise the effort setting. He has not said start.
- Its first message: how a version is formed blind to its own trade day; then 15 versions in one message.
- NEW THIS SESSION: "we can have findings for previous days be known by later ones if need be".
- WHAT FEEDS IT, as Claude reads his rulings together (put to him, not corrected): IN: the rows; the calculations
  with no window (`quote_runs`, `book_totals`, `refills`, `sweeps`, `together`, the trade legs, the peaks with no
  window, `resting`, `move_steps`); the natural gas dipole line, exhaustion line and humps. OUT: the 20-second
  peak family; Native's dipole record; the crypto and ng program's own trades and prices; the mid price; crypto
  data; last week's strategy material.

## What he decided this session (do not re-ask)

- THE TRADE PRICE GRAPH IS TWO POINTS AND THE LINE JOINING THEM. NO MID PRICE. Two dotted lines for when it was
  bought and when it was sold. The scale names only the two prices. The other graphs stay.
- THE MID PRICE IS IN NO EXCEL SHEET, and nothing made from it goes in one.
- "We should not have originally picked a zero price movement to look at our best bid offer graphs." Read a
  trade's two prices before picking it for a look.
- THE NATURAL GAS DIPOLE AND EXHAUSTION ARE USED FOR STRATEGY and go into the Excel sheets. CRYPTO DATA (anything
  measured on a crypto market) is in no analysis and no sheet. The crypto work gives the formulas only.
- THE FOUR TRADE DAY SHEETS are the sheets of `ROOT_dipoles_pinned.xlsx`. His "Yes" to: a "crypto and ng" sheet
  per trade day; the program's mid-made price columns and fee mark left out; the dead page columns out of the
  peaks sheets.
- THE RESEARCH THREADS: the questions only, never the old values; only the threads that add value; a later trade
  day may know an earlier one's findings.
- Pictures are for him; they link nothing. No picture for every trade; any trade is drawn by number on request.

## What exists now

**Code:** Markets `ccr-26ff219b-72monm`, `2df4f14` (this session's own branch; nothing on the trunk). It holds
everything of `ccr-b66f34d5-h6ra1t` (`35d45df`) plus: the two-points price graph (`root/trade_renders.py`),
`root/crypto_ng_excel.py` (the Excel update), `root/research_threads.py` (built, not run), the new rule in
`CLAUDE.md`. No test suite was run; the no-hidden-numbers rule was applied by hand.

**Stored:** `root-rows-20231002` `bc213c9`, `-20231003` `85fd853`, `-20231017` `1eccc49`, `-20231018` `a4f2708`.
- `trade-renders-quotes-test/`: trade day Oct 2, trades 883 and 1672; trade day Oct 18, trade 982: the new
  price graph with the best bid and the best offer. Their index tables hold no mid-made end price.
- `trade-renders/` (all four): the 40 older pictures STILL DRAW THE MID PRICE LINE, and their index tables still
  hold the mid as the end price of a trade that ended at no tick. His to say.
- Everything else as handoff R lists it.
- `ROOT_dipoles_pinned.xlsx` (this branch, `4262074`): thirteen sheets: the read-me; and for each trade day
  "dipoles" (Native's, untouched), "peaks" (the 20-second peaks, page columns removed), "crypto and ng" (the
  program's trades: 1,794; 1,895; 1,672; 1,682).

**Checked this session, names, receipts and history only (no table opened, nothing proved byte for byte):** the
four daily branches hold the same sixteen calculations, every receipt's checks passed, every calculation stands
on the rows as last rebuilt. One stale thing: `renders/DIPOLE-RENDERS-<trade day>.json` still lists the
exhaustion pages deleted on 2026-11-18.

**The old Excel files** (the one workbook `Frankie_four_day_research_current.xlsx`, `trade-layers/`,
`research-pins/`) are on three older `codex/` branches only: old data, cut on the wrong clock, nothing carried.

## Open with him, each put once

1. The last graph of a trade's picture is still the mid price's change per tick. Claude's call: take it out.
2. The 40 pictures of `trade-renders/`: redraw without the mid line, on his word.
3. The crypto and ng program's own trades: Claude's reading is that they stay observation only (their starts and
   ends come from settings tuned on crypto results). Not confirmed by him.
4. Whether the two natural gas lines go into the Excel file read at every trade on the tape (Claude's call: yes,
   a sheet per trade day). Not put to him as a column list yet.
5. The full every-tick workbooks: still "at a slow time". About 6 gigabytes in some 74 files by one measurement.
6. A proof of every stored file against its receipt, byte for byte, on a pod. Offered, not asked for.
7. Desktop's research report: none is on any branch. If it exists elsewhere he has to say where.
8. The stale `DIPOLE-RENDERS` receipts; Native's 6 pm to 8 pm on trade days Oct 2 and Oct 17; Desktop's peak
   lives as a sheet ("Workbook later").
9. Carried from handoff R, items 1 to 7 there (what the shaded "trade" should be; every trade, not 40; the best
   bid and best offer graphs in every picture; the per-step count; whether the 60-second line is his "dipole";
   the read-me sentence is now fixed; the older carried items).

## How a launch goes now (three pods this session, every run passed first time)

- NO POD STARTS UNTIL HE HAS TYPED THE WORD "go" AFTER THE PRICE IS ON HIS SCREEN. "Proceed", "Yes", an
  instruction and "Nevermind you're doing it" were each NOT the go this session, and he then typed "Go".
- Environment "Markets", limited network: every new pod address needs his approval card (`update_environment`).
  THE LAST POD'S ADDRESS IS STILL ALLOWED AND MUST COME OFF IN THE NEXT CARD: `9ty1zttoaxd7cs-8000.proxy.runpod.net`.
- General Purpose `cpu3g`, 8 CPUs, $0.04 a CPU an hour, $0.32 an hour; read the price again at the time. Pass
  United States `dataCenterIds`. Image `python:3.12`, port `8000/http`, entrypoint `/bin/bash -c`, one command:
  make `/root/work/out`, start `python3 -m http.server 8000 --directory /root/work/out`, clone the code branch
  (`--depth 1 --filter=blob:none --no-checkout --single-branch --branch ccr-26ff219b-72monm`, then
  `sparse-checkout set root crypto_ng`, then `checkout`), then
  `DAYS='...' bash code/root/pod_leg_renders.sh <FULL 40-character commit> <module> [options]`, then
  `sleep infinity`. Check the commit in the command before sending it.
- The daily branches: one shallow clone each (`--depth 1 --filter=blob:none --no-checkout`), then
  `sparse-checkout set --no-cone` with the files needed by name. NEVER list one with file sizes.
- BEFORE `pod_fetch`: the local clone must hold the commit the pod read the rows at. After a local commit and a
  shallow fetch it may not: run `git fetch --depth 2` (or deeper) first, or the fetch program refuses.
- WHEN NEW DATA REPLACES OLD: start the pod, delete the old from the branch, confirm it is gone on the remote, and
  only then fetch the new. Store, push, confirm each push, THEN delete the pod and read the account.
- After ANY restart of the session, read the account first (it restarted once this session with no pod up).
- The session's container needs `pip install pyarrow==26.0.1` before it can read a stored table.

## Slips of this session, so they are not made again

- Claude did not recognise `ROOT_dipoles_pinned.xlsx` as his four trade day sheets, told him no such sheets
  existed, and then pointed him at the old files on the `codex/` branches. He had to say "look back in the past
  couple of sessions".
- Trade 883 was picked for the best bid and best offer test without looking at its two prices: it did not move.
- `onset_read_20s` was taken for the exhaustion value; it is the number of a read. Caught before storing.
- The first link check of the Excel update counted nothing and so proved nothing. Checked cell by cell after.
- A pod's run time was written into the record from a guess, not the clock. Corrected.
- Long answers. He reads on a phone: the answer in the first lines.

## TO REVISIT (Greg: carry into every handoff until done)

Native's record is built on predetermined windows (a 20-second roll, a level set from 85 in 100 seconds, 60-second
horizons, a 45-second spacing and a 50-second wait before a dipole is made known), which his "no predetermined
windows" rule does not allow for our own work. He chose to keep Native as it was made for now. In this session it
was not used.
