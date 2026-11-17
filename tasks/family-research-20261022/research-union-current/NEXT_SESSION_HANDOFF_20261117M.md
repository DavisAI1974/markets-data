# Handoff M, the eleventh session (2026-11-17, about 09:45 UTC)

Branch: `ccr-349e2ffe-07p8od` in `DavisAI1974/markets-data` for data and documents. This file replaces handoffs K
and L as the starting point. Every decision of this session, with Greg's words, is in
`root-redesign-20261116/ROOT_GAMEPLAN_DECISIONS.md`, section "Eleventh session" (its last entries are the newest).
Desktop writes to the same branch: fetch before every push.

**Do NOT open last week's strategy material** (Greg, 2026-11-17: "Don't use any of your finding from last week ...
That handoff was just to remind you of the job"; "start at the beginning"). That means the handoff and review of
2026-11-13, the fifteen candidates, the selected cases and their results. Handoffs K and L point at them: ignore
those pointers. The session that wrote this file did read them, so the strategies are best formed in a fresh chat.

## Where things stand

- **No pod exists. Nothing is running. Nothing is billing.** Everything made is stored and pushed.
- Code: Markets branch `ccr-3096f7d6-fst7al`, tip `b9fd00a` (nothing on the trunk).
- Stored rows and outputs: `root-rows-20231002` `6037f23`, `-20231003` `33b3652`, `-20231017` `a76923a`,
  `-20231018` `8a6175f`. Each branch's `FILES.md` lists and explains every file. Clone each shallow; never fetch old
  branches whole.

## Done this session (all stored, all checks passed, all four trade days)

1. The rebuild from the morning pods (rows with the hourly outside figures, 408 columns; the peaks unchanged, the
   ranked column gone; `outside_changes` made again).
2. **Step 2's remaining pieces:** `leg_peaks` (the trade legs beside the peaks), `resting` (the resting orders
   through a peak, a run of the quote and a trade leg, with the fills that had an order ahead in our line),
   `dipole_peaks` (Native's stored dipole lines placed on the tape).
3. **The peak with no window** and every peak against the turns of the price (`turn_peaks`).
4. **`move_steps`** (Claude's pick on Greg's word): every step of every price move with what was in play.
5. The short-stretch workbook written again from the rebuilt rows.

So every Step 1 and Step 2 calculation that was laid out is now run, except the renders (one picture per
instance, piece H) and the grouping stage, which is done with Greg.

## What the peak work showed (each trade day on its own; the decisions file has all four)

- The peak with no window exists and is counted: 11,567; 12,684; 10,401; 9,549 on the four trade days.
- "Did the price move under way at the peak's high take any more steps?" was counted for every peak and, beside
  it, for ANY print. Against the runs of the best bid and best ask there is no difference between a peak and any
  print. Against the trade legs the peaks lean a little toward the ends (on every trade day).
- Most moves are one step long, so the count cannot tell a flicker from a long move. `move_steps` was made so the
  same question can be read by each move's own number of steps. That reading has NOT been done.
- Greg's aim stands: "if the peaks are peaking at the turns, then we have a huge problem solved". It is not shown
  yet. Desktop is looking at whether the peaks fall into groups (family and chain work) from the same branches.

## The peak research folder (made after the pods, from stored files only)

**Read `root-redesign-20261116/peak-research-20261117/TRADE_LIFECYCLE_NOTES.md` first.** It is the running notes:
a generic price move stage by stage, with what each piece of data tells at each stage, the guesses that turned out
wrong, and the open questions. Greg: the notes are written down as we go; add to that file, do not start another.

`root-redesign-20261116/peak-research-20261117/` (README, one file of peaks per trade day, five count files). Greg's
standing word: "we don't have to pick winners. We just want the story": which part of the story each kind of data
tells. The README's "The story" table is the map. In short, each trade day read on its own:
- A peak tells who was hitting, on which side, how much, and when it stopped. It holds no price.
- Peaks in the middle or at the beginning of a move of the quote are the tall ones and push with it; peaks at the
  end are short and on the other side about three times in four.
- A quarter or more of the 20-second peaks have their high on a tick with no trade (made by the window); more than
  half of the peaks with no window have no 20-second peak at their high.
- When the quote backs away and the level it left emptied only by orders pulling out, the move takes a third step
  least often; the pushing side is hitting either way.
- Where the price stood at the end of a 20-second peak's story is about even three ways in every pile.
- The five-step process Greg asked about is in `DavisAI1974/Basic_equations`, `level2_four_sciences.py` lines 10 to
  20 (observables built from information; treat them as state variables; an operator library; solve the rate of
  change; look for the opposing pair). Nothing of it was run; it uses windows and an ensemble, which are his calls.
All of this read all four trade days. It is not to be used to form a strategy version for the trade day it is
traded on.

## Open, in order

1. **Greg's answer on deleting last week's material from `main`** (put to him once, with the list): the folders
   `tasks/family-research-20261022/claude-independent-research-20261113/` and
   `research-union-current/codex-review-and-gaps-20261113/`. Told: deleting leaves them in git history; the first
   folder also holds the earlier trade-leg record he ruled valid (the checks of `trade_legs` and `leg_peaks` were
   proved against it at commit `15fbf2a`): keep it apart, or delete it too; only `main` and the working branch were
   checked, not the older branches. Nothing is pushed to `main` without his yes.
2. **The strategies: 15 versions, from the beginning, as a paper-trade barometer.** TELL GREG BEFORE STARTING (he
   raises the effort setting). Rules: only the four trade days; every trade individually; no averaging, no
   predetermined windows (the 20-second flow is the one exception), no ranks, no labels, no caps or limits; gross;
   the leakage gate first; the settle window left out; each trade day traded by versions formed on the other three,
   blind to it. Lay all 15 out to him in one message before writing any; name in that word anything that averages.
   The session that wrote this has seen counts from all four trade days, another reason for a fresh chat.
3. Read `move_steps` by each move's own number of steps against the peaks (the unfinished part of the peak work).
4. **Bedrock.** Read from the code (Markets `7f34afa`): the Bedrock stage makes three layers (derived_geometry,
   prebirth_opportunity, causal_clocks) and three ledgers. Stored: one ledger (the lifecycle ledger) for trade days
   Oct 2, 3 and 17, on branches `codex/frankie-lifecycle-recovery-<date>-42621496819`. Not found: the three layers
   and the other two ledgers on any of the four trade days; anything but the episode lines for Oct 18. Greg: it was
   run without AWS and AWS is not needed. His call on what is made and where.
5. **Native's missing two hours** (6 pm to 8 pm, trade days Oct 2 and Oct 17), made the same way as its other
   hours: a short test run on the Oct 2 file alone must match the stored record line for line first; the full run
   needs the price put to Greg. When made, `dipole_peaks` is run on it and stored beside what is there.
6. Remove the stopped chain matching code (`root/chain_ways.py`, `root/chain_common.py`, the `ways` pod job).
7. Greg's open calls, each put once when reached: measured gas use for the 16 city weights;
   `peak_highest_for_ns`; `chain_peaks` writing six steps of before lines.
8. The full workbooks, all at once, at a slow time, in parts of about 45,000 rows.
9. The renders (piece H), then the grouping stage with Greg.

## Standing rules Greg sharpened this session

- **One launch carries every piece that is ready, all started together, each on its own CPU.** Pods are not
  started and stopped piece by piece.
- Each trade day's stored files are kept up to date as each calculation lands; the workbook is written later.
- Nothing of last week's findings enters the strategies.
- A pod needs his go at the time, with the price (General Purpose 8 CPUs: $0.32 an hour each, $1.28 for four).
- To fetch from pods, their four addresses must be allowed on the "Markets" cloud environment (an approval card).
  The four of the last launch are dead and can come off the list.
- Do not list a `codex/frankie-lifecycle-recovery-*` branch with file sizes through a partial clone: it downloads
  every file. Fetch single files by raw address.

## TO REVISIT (Greg: carry into every handoff until done)

Native's record is built on predetermined windows (a 20-second roll, a level set from 85 in 100 seconds, 60-second
horizons), which his "no predetermined windows" rule does not allow for our own work. He chose to keep Native as it
was made for now.
