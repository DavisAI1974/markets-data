# Handoff, eighth session of 2026-11-16 (Step 2 pieces C, the quote's runs, A and B built and stored; the pods used; next: the chain link models)

Branch: `ccr-349e2ffe-07p8od` in `DavisAI1974/markets-data` for data and documents. This file replaces
`NEXT_SESSION_HANDOFF_20261116G.md` as the starting point. Written while the session was still going, because it
had grown long; the chain link models were about to be built.

## Read these, in this order

1. `root-redesign-20261116/ROOT_GAMEPLAN_DECISIONS.md`: every decision in Greg's words. "Eighth session" is the
   newest section of this code session. The Desktop session also writes to this file (the two Codex pieces, the
   result of the two checks): fetch before every push.
2. `root-redesign-20261116/STEP1_STEP2_LAYOUTS.md`: the layouts, with "as built" for Step 1 pieces 1 and 2 and
   now "Step 2 as built" for C, the quote's runs, A and B. The chain link models' approved layout is piece 4.
3. `root-redesign-20261116/STEP2_PLAN.md`: the Step 2 plan, pieces A through K approved.
4. `root-redesign-20261116/SPEC-root.md` and `SPEC-outside.md`.
5. Markets `CLAUDE.md`, "The trading rules".

## Where everything is

- **ROOT code:** Markets branch `ccr-30cca01c-bgs4az`, tip `8f9a971`. Not on the trunk. A new session gets a new
  branch: `git fetch origin ccr-30cca01c-bgs4az && git merge --no-edit FETCH_HEAD`.
  Fresh container: `pip install databento pyarrow xlrd openpyxl pytest`; set `MARKETS_DATA` to the markets-data
  checkout and `ROOT_ROWS` to the folder that holds `rows-<trade day>/`.
- **Stored rows and outputs:** markets-data branches `root-rows-20231002` (`ac9fb25`), `-20231003` (`32664ba`),
  `-20231017` (`8e1da23`), `-20231018` (`9108441`). Each lists its files in `FILES.md`.
  **Clone each as its own shallow copy** (`git clone --depth 1 --single-branch --branch root-rows-<day>`). Do NOT
  fetch other old branches whole: one background search did and filled the session's disk (about 16 GB).
- **The agent skills** (`using-agent-skills`, `git-workflow-and-versioning`): the plugin does not install in the
  cloud container and is not in the Markets repository. Read them from the pinned public source:
  `git clone --depth 1 --branch 0.6.8 https://github.com/addyosmani/agent-skills`. Greg: "Use the git workflow
  skill": one logical thing per commit, the reason in the message.

## What is built in part 2 (all on the real tape, each with its one check passed on all four trade days)

| Calculation | File | What it writes |
|---|---|---|
| `flow_peak` (Step 1, piece 1) | `root/calcs/flow_peak.py` | The flow on every row; each peak on the row it becomes known. 36,688 peaks. |
| `peak_story` (Step 1, piece 2) | `root/calcs/peak_story.py` | Facts beside the rows: build-up, new low, reached zero, came back, beaten. 226,077 facts. |
| `book_totals` (Step 2, C) | `root/calcs/book_totals.py` | 24 columns: added, pulled, filled, moved per side, whole side and at the best price; refilled; filled with no side. |
| `quote_runs` (Step 2, I first part) | `root/calcs/quote_runs.py` | Facts: run started, new furthest price, first step back, best bid and best ask separately; the run in progress on every row. 260,968 facts. |
| `peak_links` (Step 2, A) | `root/calcs/peak_links.py` | Facts: at the tick a peak is known, its links back on each side and the peak before; at the tick a story ends, the later peaks inside it. 73,371 facts. |
| `open_stories` (Step 2, B) | `root/calcs/open_stories.py` | 10 columns: open stories on each side, those past zero, the oldest, newest and largest open peak. |

- Two gates in `root/tape.py`, same ticks through both: `for_calculations()` (raw tape records) and
  `rows_for_calculations()` (stored rows). A calculation that names `READS` gets the rows. The runner proves the
  two pass the same positions on every run.
- A calculation that needs pieces 1 and 2 holds a `PeakStory` and works them out again in the same pass
  (`peak_links.Peaks` reads piece 2's facts as they become known). It does not read stored files.
- Run one: `python3 -m root.run calc <name> <trade day> --rows <rows folder> --out <folder>`.

## The pods (Greg: "Run the pods"; the step runs go on pods, all four trade days at the same time)

- Used once this session, for A and B: four Runpod General Purpose CPU pods (`cpu3g`, 8 CPUs, 32 GB, $0.32 an
  hour each, 10 GB disk), image `python:3.12`, port `8000/http`, about seven minutes, then deleted.
- `root/pod_run.sh <trade day> <Markets branch> <calculation> ...` is the launcher. The pod fetches the code, the
  tape and its rows from the two PUBLIC repositories (no key on the pod), runs the calculations, and serves its
  output folder on port 8000. The session fetches each file from
  `https://<pod id>-8000.proxy.runpod.net/`, compares it with the fingerprint in its receipt, checks the code
  commit and the rows commit, and stores it. The pod writes nothing to git.
- The session can only reach a pod after its address is added to the "Markets" cloud environment's allowed hosts
  (`update_environment`, one approval from Greg). Four dead addresses from this session are still on that list;
  remove them in the same call that adds the next four.
- **Helpers pinned (Greg: "Make sure the helpers are pinned to cpus so it isn't just one running by itself").**
  The launcher now starts every helper at once, each bound to its own CPU with `taskset`. Not yet run on a pod.
- Each `exec-pod` call asks Greg for permission and he had to re-open the prompts. Better next time: put the
  launch in the pod's container command at create, start the file server even when a run fails, and read
  progress and logs over the pod's address.
- **A new launch needs his go at the time, with the price.**

## What to do next, in this order

1. **The chain link models** (Step 1 piece 4; layout APPROVED: "Do it"; `STEP1_STEP2_LAYOUTS.md`). Decided so far
   in this session (Claude's calls, to state to Greg when built; none is built):
   - Two parts. (a) A normal per-trade-day calculation: one line per peak at the tick its story ends, holding what
     the peak did (its size, the time from the low to the high, how it ended, how long that took, how far it
     faded, the number of steps down, the price move from the high to the end, the best and worst price on the
     way, same side as the peak before or not) and the six peaks before it whose stories had ended when it became
     known. Usual recount and playback. (b) A models runner: each trade day's peaks scored by models taught on the
     other three; it rebuilds the teaching tables through the tape gate.
   - Carried from the original (`research/ng_exhaustion_chain_phase1_discovery_20260817.py` and
     `..._phase1_causal_20260817.py` on Markets branch `chatgpt/ng-exhaustion-chain-phase2-20260817`): the inputs
     are the figures of the d peaks before, the target is the peak's own figures; figures standardised on the
     teaching days; depth 0 is the teaching mean; ridge (0.1, 1, 10, 100, 1000), nearest neighbours (10, 20, 40,
     80, 160, weighted by distance), extra trees (leaf 10, 20, 40, 80; seed 20260817); the setting chosen by
     leaving one teaching block out in turn; the gain at a step back is the error without that peak minus the
     error with it. Steps back 1 to 6 first, shown to Greg before going further. The old programs disagree on the
     number of trees (180/60, 140/50, 100/40, 80/30); the three-week "known at the time" pilot (140, and 50 while
     choosing) is the nearest precedent.
   - Not carried: "all models positive", the depth candidate, the Fisher tables (labels, a depth, pooled results).
   - Under his averaging rule: each figure's own squared error per peak, model and depth is written; the mean over
     the figures sits beside it.
   - To say when the six steps are shown: some gain is true by definition (a peak "beaten" means the next peak on
     that side is larger).
   - Peaks with an empty figure are counted on all four trade days before a rule is chosen; never filled with zero.
   - The check: every input peak's story ended at or before the target became known; ridge worked out again in
     closed form. Extra trees and nearest neighbours have no independent recount; the receipt says so.
   - Helpers pinned one per CPU, one thread each (`OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, `MKL_NUM_THREADS`
     set to 1, `n_jobs=1`); each helper writes its CPU into the receipt. Library versions pinned in `pod_run.sh`.
   - **scikit-learn is a new dependency. The spec says ask first: name it to Greg with the launch request.**
2. **D and the print legs of I wait on Greg's answer to the two checks** (decisions file, "Result of the two
   checks"): Native's record and the old print legs miss the first two hours of trade days Oct 2 and Oct 17.
   Claude's recommendation there: make the print legs again from the stored rows for all four trade days; place
   Native's record for Oct 3 and 18, and his choice for Oct 2 and 17.
3. The rest of I (the lines that name peaks: read the run in progress off the row a fact names), K, H (every
   instance), then the grouping with Greg.
4. **Before K:** the finding on place in line (decisions file, eighth session). A filled order had another order
   ahead of it in our line on about 2,000 to 3,300 rows a trade day; about half is only the order of messages in
   a sweep; some front orders were cancelled untraded by the exchange in the same event; the rest is not
   explained. Anything about the foundation goes to Greg first.

## Rules (all recorded in the decisions file). New or sharpened this session:

- **The whole `tests/root` folder is never run.** One check per new part, run once, on that part only.
- **A corrected step is checked on the corrected part only.** The whole run is not made again for it.
- **The step runs go on pods**, all four trade days at once, helpers pinned to CPUs. Anything run in the session
  is said to him before it is run, not after.
- Unchanged: a TRADE DAY is 6 pm Eastern the evening before to 5 pm Eastern; only the four trade days enter a
  calculation; rows are ticks; empty is never zero; every trade individually and any averaging is an addition; no
  fixed marks; no caps; no labels or groups until all four trade days have run everything; never invent data; no
  trade cost; bad or unused data is not saved; AWS is off limits; Markets is code only and nothing goes to its
  trunk without his word; do not re-ask what he has decided.

## Waiting on Greg

- His answer to the two checks (Native's record and the print legs on trade days Oct 2 and Oct 17).
- His go, at the time, for the chain link models' pods, and his word on scikit-learn.
- Any correction to Claude's calls under "Step 2 as built", above all the fill call (a fill the book shows no
  change for counts as filled and as added).
- Still open from before: the four old `trade-day-book-2023...` branches to delete; the Markets trunk does not
  have the session branches' `CLAUDE.md` changes; the Markets repository is near its size quota.

## Facts from this session (for whoever builds next)

- Both repositories are public: a pod, or any clone, needs no key to read them.
- The session's writable disk is about 16 GB. `markets-data` branch `ccr-349e2ffe-07p8od` fetched with full
  history is 2.2 GB; fetch with `--depth 1`.
- The Markets working tree holds `artifacts/` (4.6 GB). A pod takes the code with
  `git clone --depth 1 --filter=blob:none --sparse` and `sparse-checkout set root` (1.6 MB).
- On every trade day: no clear, no unapplied message, no empty best price, no fill without its order's row in
  the same exchange event, no move of a best price on the first tick.
- The fill messages always come before their order's own row inside an exchange event.
- How he wants the work: plain words, read on a phone, a whole plan in one go, his question answered first,
  decisions recorded in git as they are made, and no test or check beyond the one per part.
