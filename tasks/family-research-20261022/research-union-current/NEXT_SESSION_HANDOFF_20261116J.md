# Handoff J, end of the ninth session (2026-11-16 late evening Eastern)

Branch: `ccr-349e2ffe-07p8od` in `DavisAI1974/markets-data` for data and documents. This file replaces
`NEXT_SESSION_HANDOFF_20261116I.md` as the starting point (I is still right about everything it covers: how a pod
launch goes, where the stored outputs are, the facts found). Desktop writes to the same branch: fetch before every
push.

Greg has news to share ("we may have figured out something huge"). He said he will share it after the build and
run below are done. Ask for nothing; he will bring it.

## THE ORDER FOR THE NEXT CHAT (Greg's last words of the ninth session; they govern the list under "What to do next")

"I have usage to finish what we started properly in the next chat. I don't want to have partially built firlds or
stop short of an experiment outpit." And: "Once all of these calcs are done, we are going to do the strategy
creation like we did last week ... I want to have some sort of barometer to see where our knowledge works or
doesn't in a parer trade atmosphere".

1. **Finish what was started, properly, all the way to its output.** No field left partly built; no experiment
   stopped short of its result.
   - The three calculations that are written and not run (the peaks in play at every turn of the quote; what was
     in play when an outside figure changed; orders that act together): run on the pods, checked, stored.
   - The chain link models taken as far as they will go, in the six ways: built, run, stored, and read out (what
     the results say), each way kept beside the others.
2. **Then the first strategy versions, as a paper-trade barometer,** the way the strategy creation was done last
   week (ask him where last week's strategy work is kept if the handoffs do not say; do not guess a method).
   Gross (no trade cost), every trade individually, the leakage gate first, only the four trade days, each trade
   day paper traded by versions formed on the other three.
3. Do not begin a further piece (the resting orders; the missing two hours of the trade legs and Native) unless it
   can be carried through to its stored output in that chat. They follow.

What tonight's calculations already say, to start the strategy step from: the peaks before a peak say a good deal
about the next peak's flow and nothing measurable about the price moves after it; a few hundred orders are traded
against and reloaded at the best price; nine lots in ten added to the book are pulled, not traded; the quote mostly
flickers.

## Read these, in this order

1. `root-redesign-20261116/ROOT_GAMEPLAN_DECISIONS.md`, section "Ninth session" (long; its last entries are the
   newest decisions). "Seventh session" and "Eighth session" still govern what they cover.
2. `NEXT_SESSION_HANDOFF_20261116I.md` (the pods, the stored outputs, the rules).
3. `root-redesign-20261116/STEP1_STEP2_LAYOUTS.md` and `CHAIN_LINK_FIRST_SIX_STEPS.md`.
4. `STEP2_PLAN.md`, `SPEC-root.md`, `SPEC-outside.md`; Markets `CLAUDE.md`, "The trading rules".

## Where everything is

- **ROOT code:** Markets branch `ccr-d9ae98a9-65go6q`, tip `a6a7861`. A new session gets a new branch:
  `git fetch origin ccr-d9ae98a9-65go6q && git merge --no-edit FETCH_HEAD` (it fast-forwards).
- **Stored rows and outputs:** `root-rows-20231002` (`4a1e4c4`), `-20231003` (`ea5b8b8`), `-20231017` (`2725dc2`),
  `-20231018` (`cf5a0f6`). Clone each as its own shallow copy.
- **Runpod:** no pods, nothing billing. Use the Runpod MCP and load the Runpod skills first. Price read this
  session: General Purpose `cpu3g` $0.04 a CPU an hour (8 CPUs $0.32); Compute-Optimized `cpu3c` $0.03 a CPU an
  hour (32 CPUs, 64 GB, $0.96). Read it again at the time.

## State of the build

**Run on pods, checked, stored (this session):** L (`refills`), M (`sweeps`), `chain_peaks`, and the chain link
models at six steps. Counts in the layouts file; the six-step read-out in `CHAIN_LINK_FIRST_SIX_STEPS.md`.

**WRITTEN, each with its one check, wired into the runner and into `root/pod.py`. NOT RUN, not even once:**

| Calculation | File | What it writes |
|---|---|---|
| `quote_peaks` (the rest of piece I) | `root/calcs/quote_peaks.py` | One fact at every turn of a run of the quote: the buy peak and sell peak most lately known (the tick of its high, time since, where its story stands) and the rise under way. |
| `outside_changes` (addition O) | `root/calcs/outside_changes.py` | One fact for every outside column whose value differs from the row before in the trade day, with what was in play (peaks and the run of the quote in progress). |
| `together` (addition N) | `root/calcs/together.py` | One line per order of every set of two or more orders that entered, or left, at the same exchange time. |

`root/calcs/in_play.py` is their shared helper (it follows the peaks and the quote's runs from the stored rows by
their own code). The checks are `checks.quote_peaks`, `checks.outside_changes`, `checks.together`, with
`checks._in_play_as_stored`. These three use the default playback cut. Their constants are NOT yet in
`root/DECLARED_CONSTANTS.md` (add: `in_play` READS, OPEN/PAST_ZERO/ENDED, HIGH_SIDE/HIGH_POSITION/HIGH_AT;
`together` SET_FROM = 2 and its words; `outside_changes` GROUPS, OUTSIDE, KIND, KNOWN_FROM, TIME, FIRST_OUTSIDE).
Run them on the pods with his go: `job=calc:quote_peaks,outside_changes,together`. Expect the first run to find
faults (this session's first runs found two); fix the part and run that part again on the same pods.
`outside_changes` reads 108 outside columns of every row: give it memory (it was sized for a 32 GB pod).

## What to do next, in this order (all decided by Greg; see the decisions file for his words)

1. **Run `quote_peaks`, `outside_changes` and `together` on the pods** (his go at the time, with the price).
2. **The chain link models, taken as far as they will go and tried in different ways. Every way's result is kept
   beside the others; the six-step result stays as stored.** Not built. Six ways were named to him (Claude's
   calls): (1) as built, out to 24 steps back; (2) each earlier peak alone, out to 48; (3) what a peak does AFTER
   it becomes known (how it ended, how long, how far it faded, the steps down, the three price moves), given its
   own size and side and then the chain, out to 24; (4) the same with each earlier peak alone, to 48; (5) only the
   peaks before on its own side, to 24; (6) only those on the other side, to 24. Wider lists of settings (ridge
   and nearest neighbours chose the last entry of the original lists). The step counts are how far each is run
   now, not caps: where the gain has not gone by the last step, run that way further.
   Design notes from this session, not built and not all stated to him yet (state them when built):
   - A new runner beside `root/chain_models.py` (which stays, so the stored six steps can be made again). It
     works out each peak's earlier peaks itself, to any depth, from the peak lines (the tick a peak became known,
     the tick its story ended, its side): the stored before lines stop at six steps by design.
   - One fixed set of peaks per way (those with every step of that way available), so the model given d-1 peaks is
     fitted once and "without" at step d is "with" at step d-1. Lines are then per peak, model and number of peaks
     given; gains are differences of neighbouring lines. This halves the work and the storage.
   - Inputs: the nine figures that are never empty (not the time from the low to the high, which is empty on 32
     to 42 peaks a trade day and would empty out a tenth of the peaks at 24 steps). A target with an empty figure
     is scored on the figures it has. Nothing is filled in.
   - Size: 24 steps of every figure for three models is large. Store the per-figure errors as 4-byte numbers and
     the mean as 8-byte, declared; keep parts under GitHub's 100 MB a file.
   - Pods: 32 CPUs each for these (extra trees at 24 steps is the cost). All helpers pinned, one thread each.
   - Read each way's result the way the six steps were read: counts of peaks that gained and lost first, the mean
     beside them, the four trade days apart, flow figures apart from price figures. Then tell him what they say.
3. **K (the resting orders through a peak and a run), with the "another order ahead" facts.** Not built. Greg:
   where a filled order had another order ahead of it in our line, show it as a fact (how many orders and how much
   size were ahead, and which orders), in case it tells us something new; show nothing where there was none. The
   foundation is not changed for it. This session's design for K, not built: anchors are a peak's high and the
   start of a run of the quote; a line at every later turn of that peak's story or run; for each side, for the
   whole side and for the orders at the best price at the anchor: of the orders resting at the anchor, the size
   and number since filled, pulled, moved, the size added to them, and what is still resting. An order belongs to
   an anchor when it entered at or before it; no place-in-line figure is used.
4. **The trade legs and Native's dipole (this unparks D and the print legs of I).** Valid values are NEVER
   discarded: place Native's record and the trade legs as they are for trade days Oct 3 and Oct 18, and what
   exists from 8 pm Eastern on for Oct 2 and Oct 17 (marked as starting there). **Make only the missing 6 pm to
   8 pm Eastern of trade days Oct 2 and Oct 17, exactly the way the existing data was made**: the same programs
   and rule (trade legs: Markets `0408df44`, `continue_trade_chronology.py`; Native: Markets `2ebb8ce8`,
   `research/kalshi/frankie_raw_mbo_benchmark/native_session.py`). Read each first; if one cannot be run as it
   stands on those hours, bring that to him before doing anything else. Where the records are kept is in the
   decisions file, "Result of the two checks" (seventh session). Fetch those old branches by single file or
   shallow, never whole.
5. Then D (the dipole beside the peaks), H (every instance rendered), and the grouping with him.

## Rules (all in the decisions file); the ones sharpened tonight

- "Take the chains as far as they will go. And try the calcs in different ways. Keep the different results and see
  what the results are telling you."
- The goal of every calculation: to explain or predict a trade, its lifecycle or any piece of it, from any angle.
- "We are going to be very light on the tests. Only on pieces that change and only once."
- L shows what the data shows; nothing is filtered.
- Valid data is never discarded; where an old value and a new one both exist, both are kept.
- Everything a pod makes goes to markets-data before the pod is deleted.
- Say plain names, not letters: he asked what "inok" was (it was I, N, O, K).
- Unchanged: trade day 6 pm Eastern to 5 pm Eastern; only the four trade days enter a calculation; rows are ticks;
  empty is never zero; every trade individually; no fixed marks, caps, labels or groups; never invent data; no
  trade cost; AWS off limits; Markets is code only; nothing to the Markets trunk without his word; no pod without
  his go at the time, with the price; nothing run in the session without telling him first; do not re-ask.

## Still open with Greg (each put once, when the work reaches it)

From handoff H: 2 (the fill call in C), 3 and 4 (C, the quote's runs, A and B stand as run), 8 (the other calls
under "Step 2 as built"), 9 (a setup script that fetches the pinned skills), 10, 11. Closed tonight: 1, 5, 6, 7.
