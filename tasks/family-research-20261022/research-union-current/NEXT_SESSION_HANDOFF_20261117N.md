# Handoff N, end of the eleventh session (2026-11-17, about 10:50 UTC)

Branch: `ccr-349e2ffe-07p8od` in `DavisAI1974/markets-data` for data and documents. This file replaces handoffs K,
L and M as the starting point. Every decision of this session, with Greg's words, is in
`root-redesign-20261116/ROOT_GAMEPLAN_DECISIONS.md`, section "Eleventh session" (its last entries are the newest).
Desktop writes to the same branch: fetch before every push.

**Read these two first, in this order:**
1. `root-redesign-20261116/peak-research-20261117/TRADE_LIFECYCLE_NOTES.md`: the running notes. A generic price
   move stage by stage, what each piece of data tells at each stage, the guesses that turned out wrong, the open
   questions, and what Greg saved for this session. Greg: the notes are written down as we go. ADD to that file;
   do not start another.
2. The decisions file, section "Eleventh session".

**Do NOT open last week's strategy material** (Greg: "Don't use any of your finding from last week ... That
handoff was just to remind you of the job"; "start at the beginning"): the handoff and review of 2026-11-13, the
fifteen candidates, the selected cases and their results. Handoffs K and L point at them: ignore those pointers.

## Where things stand

- **NOT FINAL YET (10:38 UTC): four pods are still drawing the renders** (Oct 2 `v77rqljqv0s9hb`, Oct 3
  `vmczelc3kybrzv`, Oct 17 `f3g6yj2owboz01`, Oct 18 `g5cpkm35bkwrst`; $1.28 an hour for the four; Markets `f4385cd`, job
  `calc:renders`). Their output is fetched with `python3 -m root.pod_fetch <pod address> <trade day>
  f4385cda0fc070906ad93f6ea301f141fe401200 --into <rows clone>/renders renders`, stored, then the pods deleted. This
  line is replaced when that is done. Until then the `renders/` folders and `ROOT_dipoles_pinned.xlsx` named below
  do not exist yet, and the rows branches are at the tips given here.
- Code: Markets branch `ccr-3096f7d6-fst7al`, tip `f4385cd` (nothing on the trunk).
- Stored rows and outputs: `root-rows-20231002` `6037f23`, `-20231003` `33b3652`, `-20231017` `a76923a`, `-20231018`
  `8a6175f`. Each branch's `FILES.md` lists and explains every file. Clone each shallow; never fetch old branches
  whole. The renders are in each branch's `renders/` folder (about 100 MB a trade day).
- Every Step 1 and Step 2 calculation that was laid out is run and stored for all four trade days.

## Made this session (all stored, every check passed, all four trade days)

1. The rebuild (rows with the hourly outside figures, 408 columns; peaks unchanged, the ranked column gone).
2. `leg_peaks`, `resting`, `dipole_peaks`, `turn_peaks` (the peak with no window), `move_steps`.
3. **The pin and the renders** (`renders/` on each `root-rows` branch): Native's dipoles pinned to their birth
   seconds on our tape (`dipoles-pinned-<trade day>.parquet`, and all four as `ROOT_dipoles_pinned.xlsx` in
   `root-redesign-20261116/`), one picture per dipole, and every exhaustion peak drawn as its own small panel on
   pages, with an index naming each peak's page and panel.
4. The peak research folder (`peak-research-20261117/`): every peak placed in the move under way, and the reads.

## What the research showed, in short (each trade day on its own; details and counts in the notes file)

- A peak tells who was hitting, on which side, how much, and when it stopped. It holds no price.
- Peaks in the middle or at the beginning of a move of the quote are tall and push with it. Peaks at the end are
  short and on the other side about three times in four.
- A quarter or more of the 20-second peaks have their high on a tick with no trade (made by the window). More
  than half of the peaks with no window have no 20-second peak at their high.
- The standing orders mostly get out of the way. A level that was only abandoned leads nowhere; a level that was
  eaten leads on. The peak reads the same either way.
- **Native's dipole, reverse engineered:** the level it must clear is exactly 1 on every dipole, so it selects
  nothing; our flow is fully one-sided in about 19,000 to 20,000 seconds a trade day and Native marks 741 to 863 of
  them; no two births are closer than 45 seconds and that is the most common gap; most are known exactly 50
  seconds after the birth. Greg judged the 50-second line an artifact and the evidence agrees: the 45 and the 50
  are constants of the detector. BUT the dipoles born WITH a trade in their birth second (about four in ten) read
  as real events: they agree with our tape, mark the second the flow became one-sided, and about nine in ten are
  the same event as an exhaustion peak. More than half of those are a single lot.
- Not yet looked at: the pictures themselves. Nobody has gone through the dipole renders or the exhaustion pages
  to see whether the shapes repeat (Greg: last week's exhaustion renders showed near-identical shapes within a
  kind of trade and distinct shapes from trade to trade; those were on the thin, wrongly run data).

## Open, in order

1. **The three-tier picture, and a tick-level ("nano") line beside the 20-second one (Greg, 2026-11-17: "Do a 3
   tier ... Price, dipole and exhaustion in 3 different graphs. You can keep the 20 sec but we need to add nano if
   we're going to be pinning and comparing to nano timed things").** His words and the three things to settle with
   him first are in the notes file, last section. KEEP the 20-second flow and everything made on it; ADD the version
   made at the tick beside it. One picture, three separate graphs on one time axis of real timestamps: price, dipole,
   exhaustion. The first renders (stored in each `root-rows` branch's `renders/`) were too crowded for him to read.
   What stands on the 20-second window is listed in the decisions file (twelve of seventeen calculations).
2. **Greg's saved idea: the stacked pair of graphs** (his words are in the notes file, "SAVED FOR THE NEXT
   SESSION"). For each dipole and the trade that goes with it: price on top, the dipole line below, one time axis
   of real timestamps. The question is whether the two MOVE at the same moments, whatever the direction. Three
   things to settle with him first are listed there.
3. **The strategies: 15 versions, from the beginning, as a paper-trade barometer.** TELL GREG BEFORE STARTING: he
   raises the effort setting ("I'll put you on extra high"). Rules: only the four trade days; every trade
   individually; no averaging, no predetermined windows (the 20-second flow is the one exception), no ranks, no
   labels, no caps or limits; gross; the leakage gate first; the settle window left out; each trade day traded by
   versions formed on the other three, blind to it. Lay all 15 out to him in one message before writing any; name
   in that word anything that averages. Nothing of last week's findings.
4. Greg's answer on deleting last week's two folders from `main` (put to him once; nothing is pushed to `main`
   without his yes): `tasks/family-research-20261022/claude-independent-research-20261113/` and
   `research-union-current/codex-review-and-gaps-20261113/`. Told: deleting leaves them in git history; the first
   holds the earlier trade-leg record he ruled valid (the leg checks were proved against it at `15fbf2a`): keep it
   apart or delete it too; only `main` and the working branch were checked.
5. The five-step process (`DavisAI1974/Basic_equations`, `level2_four_sciences.py` lines 10 to 20). Which two
   streams; it uses windows and an ensemble as written: his calls before anything is run.
6. The open questions in the notes file (how old the level was that a peak hit; what the price did after each
   pile; the eaten-or-abandoned read at every level; the outside figures; refills and orders moving together).
7. **Bedrock.** The Bedrock stage makes three layers and three ledgers (Markets `7f34afa`). Stored: one ledger
   (the lifecycle ledger) for trade days Oct 2, 3 and 17. Not found: the three layers and the other two ledgers on
   any trade day; anything but the episode lines for Oct 18. Greg: it runs without AWS. His call on what is made.
8. Native's missing two hours (6 pm to 8 pm, trade days Oct 2 and Oct 17): a short test run on the Oct 2 file alone
   must match the stored record line for line first; the full run needs the price put to Greg.
9. Remove the stopped chain matching code (`root/chain_ways.py`, `root/chain_common.py`, the `ways` pod job).
10. Greg's open calls, each put once when reached: measured gas use for the 16 city weights;
    `peak_highest_for_ns`; `chain_peaks` writing six steps of before lines.
11. The full workbooks, all at once, at a slow time, in parts of about 45,000 rows.
12. The grouping stage, with Greg (Desktop is looking at family and chain groups from the same branches).

## Standing rules Greg sharpened this session

- **One launch carries every piece that is ready, all started together.** Pods are not started and stopped piece
  by piece. A pod needs his go at the time, with the price (General Purpose 8 CPUs: $0.32 an hour each, $1.28 for
  four). To fetch, the pods' four addresses must be allowed on the "Markets" cloud environment (an approval card).
- **We don't pick winners. We want the story:** which part each kind of data tells.
- **Write the notes down as we go**, in the notes file.
- Each trade day's stored files are kept up to date as each calculation lands; the workbook is written later.
- Nothing of last week's findings enters the strategies. He is told before the strategy work starts.
- A read of stored files in the session is told to him first; a run goes on pods.
- The pod runner pins each job to ONE CPU. A job that wants every CPU must widen its own affinity
  (`root/dipole_renders.py` shows how).
- Do not list a `codex/frankie-lifecycle-recovery-*` branch with file sizes through a partial clone: it downloads
  every file. Fetch single files by raw address.

## TO REVISIT (Greg: carry into every handoff until done)

Native's record is built on predetermined windows (a 20-second roll, a level set from 85 in 100 seconds, 60-second
horizons, and, found this session, a 45-second spacing and a 50-second wait before a dipole is made known), which
his "no predetermined windows" rule does not allow for our own work. He chose to keep Native as it was made for now.
