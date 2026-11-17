# Handoff, ninth session (2026-11-16 evening Eastern): L, M and the chain link models built, run on pods and stored; the six steps put to Greg

Branch: `ccr-349e2ffe-07p8od` in `DavisAI1974/markets-data` for data and documents. This file replaces
`NEXT_SESSION_HANDOFF_20261116H.md` as the starting point. Desktop writes to the same branch: fetch before every
push.

## Read these, in this order

1. `root-redesign-20261116/ROOT_GAMEPLAN_DECISIONS.md`: "Ninth session" is the newest section and holds every call
   made in this session and Greg's words. "Seventh session" and "Eighth session" still govern what they cover.
2. `root-redesign-20261116/STEP1_STEP2_LAYOUTS.md`: now with "Built in the ninth session" and "Run in the ninth
   session" (the counts for L, M and the per-peak chain lines).
3. `root-redesign-20261116/CHAIN_LINK_FIRST_SIX_STEPS.md`: the read-out of the chain link models put to Greg.
4. `root-redesign-20261116/STEP2_PLAN.md`, `SPEC-root.md`, `SPEC-outside.md`, and Markets `CLAUDE.md`, "The trading
   rules".

## Where everything is

- **ROOT code:** Markets branch `ccr-d9ae98a9-65go6q`, tip `459f733` or later. Not on the trunk. A new session gets
  a new branch: `git fetch origin ccr-d9ae98a9-65go6q && git merge --no-edit FETCH_HEAD` (it fast-forwards).
- **Stored rows and outputs:** markets-data branches `root-rows-20231002` (`4a1e4c4`), `-20231003` (`ea5b8b8`),
  `-20231017` (`2725dc2`), `-20231018` (`cf5a0f6`). Clone each as its own shallow copy. Never fetch old branches
  whole.
- **The agent skills:** read from `git clone --depth 1 --branch 0.6.8 https://github.com/addyosmani/agent-skills`
  (the router and `git-workflow-and-versioning`). The Markets repository's own `repo-conventions` skill loads.
- **Runpod:** use the Runpod MCP and load the Runpod skills (`runpod:runpod-mcp`, `runpod:runpod`) first.

## What is built in part 2 now (each with its one check passed on all four trade days)

`flow_peak`, `peak_story`, `book_totals`, `quote_runs`, `peak_links`, `open_stories` (before this session), and:

| Calculation | File | What it writes |
|---|---|---|
| `refills` (addition L) | `root/calcs/refills.py` | A fact at an order's own row whenever a fill is followed by size put back, or by a change of price. 1,860, 1,727, 1,522 and 1,608 facts. |
| `sweeps` (addition M) | `root/calcs/sweeps.py` | One fact per exchange event with a trade; facts when the quote touches or crosses and when it parts. 38,412, 41,789, 33,834 and 30,911 facts. |
| `chain_peaks` (chain link models, first part) | `root/calcs/chain_peaks.py` | One line per peak at the tick its story ends (what it did); one line per step back at the tick it becomes known (the ended peaks before it). |
| the chain link models (second part) | `root/chain_models.py` | Not a tick calculation. One line per peak, model and step: each figure's squared error without and with the peak at that step, the mean, the gain. Taught on the other three trade days; not known at a tick. |

## The pods (how a launch goes now)

- `root/pod.py` runs on the pod; `root/pod_fetch.py` runs in the session. `pod_run.sh` is gone.
- Create one pod per trade day with the Runpod MCP: image `python:3.12`, CPU `cpu3g` with 8 CPUs ($0.32 an hour
  each, read the price again at the time), disk 10 GB, port `8000/http`, an env `POD_WORD` (a random word made in
  the session), entrypoint `bash -c`, and a command that clones `root/` of the Markets branch and runs
  `python3 /root/work/code/root/pod.py <trade day> <branch> <commit> calc:<names>` (the exact command is in the
  decisions file's commit history, Markets `b8b720c`, and in this session's launch).
- The file server is up first. Progress is the pod's `STATUS` file at `https://<pod id>-8000.proxy.runpod.net/`.
- A further run, or a corrected part, on the same pod: `.../run?word=<word>&commit=<40 hex>&job=calc:<names>` or
  `job=models`. No `exec-pod` call is needed.
- The session can reach a pod only after its address is added to the "Markets" environment's allowed hosts (one
  approval), and the addresses come off again when the pods are deleted (one approval).
- Store first, push, confirm the push, THEN delete the pods. Greg: "You'll have to migrate the data to the data
  repo."
- **A new launch needs his go at the time, with the price.**

## What to do next, in this order

1. **The chain link models: WAIT for Greg.** He asked to see the first six steps before going further. They were
   put to him. How far back to go, and whether the settings lists are widened (ridge and nearest neighbours chose
   the last setting of their lists), are his.
2. **D and the print legs of I wait on his answer to the two checks** (Native's record and the old print legs miss
   the first two hours of trade days Oct 2 and Oct 17). Recommendation unchanged: make the print legs again from
   the stored rows for all four trade days; place Native's record for Oct 3 and 18; his choice for Oct 2 and 17.
3. The rest of I (the lines that name peaks), K with N, O, H (every instance), then the grouping with him.
4. **Before K:** bring him the finding on the place-in-line figures (decisions file, eighth session).

## Rules (all in the decisions file). New or sharpened in this session

- "And we are going to be very light on the tests. Only on pieces that change and only once."
- "Nothing is run in the session without telling me first." In this session nothing was calculated in the session;
  it fetched, proved and stored, and read the stored models table to count (said to him first).
- The Runpod MCP and the Runpod skills are used for every launch.
- Everything a pod makes goes to markets-data before the pod is deleted.
- Unchanged: a TRADE DAY is 6 pm Eastern the evening before to 5 pm Eastern; only the four trade days enter a
  calculation; rows are ticks; empty is never zero; every trade individually and any averaging is an addition; no
  fixed marks; no caps; no labels or groups until all four trade days have run everything; never invent data; no
  trade cost; bad or unused data is not saved; AWS is off limits; Markets is code only and nothing goes to its trunk
  without his word; do not re-ask what he has decided.

## Questions for Greg, each put once at the point the work reaches it

Carried from handoff H and still open: 1 (Native's record and the print legs on Oct 2 and 17), 2 (the fill call in
C), 3 and 4 (C, the quote's runs, A and B stand as run), 7 (the place-in-line finding, before K), 8 (the other
calls under "Step 2 as built"), 9 (a setup script that fetches the pinned skills), 10, 11.
- Closed in this session: 5 (scikit-learn and the launch: "Approve").
- 6 (L, what gets a fact) was put to him with L's counts in this session's report; his answer is awaited. As built:
  every row with size put back gets a fact, with a yes/no for "same size or larger".
New from this session, his to correct (all in the decisions file): the size put back never more than the fill; a
touch already standing at the first tick marked and counted from the first tick; the ten figures and how each
enters a model; the rule for empty figures; six steps written out as lines, not a cap.

## Facts from this session (for whoever builds next)

- The quote is already touching or crossed at the first tick of trade days Oct 2 and Oct 3, and not on Oct 17 or 18.
- No trade or fill row carries the tape's "no price" value on any of the four trade days.
- Piece 2 has no low for the rise on 32 to 42 peaks a trade day.
- The pods' web front refuses Python's own client name; `pod_fetch.py` names itself plainly.
- The session's clock and Runpod's agree to the minute; Runpod's billing posts late.
- Library versions on the pods: Python 3.12.16, numpy 2.5.5, pyarrow 26.0.1, databento 0.90.0, scikit-learn 1.9.1,
  scipy 1.18.1.
