# Action plan going forward (written 2026-11-16, end of the second session)

Branch: `ccr-349e2ffe-07p8od` in `DavisAI1974/markets-data`. This is the document to read first in the next session.
It says why we are doing this, what is already true, what happens next and in what order, what gets deleted, and
what is waiting on Greg. The two handoffs (`NEXT_SESSION_HANDOFF_20261116.md` and `...20261116B.md`) hold the detail
behind each statement here.

---

## 1. Purpose: why the plan changed

We started this work to fill empty cells in the trade workbook for four trade days (Oct 2, 3, 17 and 18, 2023).
While doing that we found that the foundation the cells rest on is not sound, in three layers:

1. **The order book was being restarted in the middle of every trade day.** The old replay applied the vendor's
   00:00 UTC snapshot, which is 20:00 ET, two hours into the trade day. Every resting order's age started again from
   that moment. That was fixed: the book is now seated at the Sunday open of the trade week and carried straight
   through.
2. **Two of the four trade days were missing their first two hours** (18:00 to 20:00 ET) in the old archives: 457
   trades on trade day Oct 2 and 252 on trade day Oct 17.
3. **The calculation that everything else is built on, called ROOT, throws data away before anyone looks at it.** It
   steps through the tape one whole second at a time although the tape is in nanoseconds; it uses fixed windows (20,
   45, 60, 300 seconds and others); it looks at only the top 10 price levels in many places; it has thresholds that
   stop events from being recorded at all (no candidate in the first 15 minutes, only the top 15 percent of seconds,
   nothing within 45 seconds of another); and it restarts order ages the same way the old replay did.

Greg did not choose those cutoffs and would have stopped them. His statement of what we are doing:

> "This is what we're trying to figure out, what pieces of data are dictating things and when we decide ahead of
> time, we're killing our own research silently."

So the purpose of the plan is no longer "fill the empty cells". It is:

**Rebuild the foundation so that it is a complete record of what the tape says, at the tape's own resolution and
full depth, with nothing decided ahead of time. Then find out from that record, trade by trade, which pieces of data
dictate things. Then refill the sheet from it. Everything built on the old foundation is traced, removed and rerun,
so that no old value or old code can slip into a new run.**

---

## 2. The rules that govern every step

Greg's standing rules, old and new. If a step would break one, the step is wrong.

- **Trade day only.** A trade day is the CME session: 17:00 ET the evening before (the halt; trading resumes 18:00
  ET) to 17:00 ET on the named date. Never write a bare "day" or bare date; say "trade day" or "UTC clock day".
- **Every trade individually.** No rates, averages, correlations or model scores as a readout, and no market rule
  derived from an average.
- **IDs and clocks designate; they are not inputs to calculations.**
- **Never invent data.** Unavailable stays empty with a stated status. Tests use real tape only.
- **No trade cost in any research calculation.**
- **Frankie output fields stay blank** (L077-L079, L091-L092, L094-L098). Launch is on hold.
- **ROOT decides nothing ahead of time.** It records; it does not select, threshold, summarize, sample, rank or drop.
  Where a choice cannot be avoided it is written down by name next to what it affects, with the alternative kept.
- **Nanosecond resolution**, each message, in tape order: whatever the MBO tape uses and the live feed will use.
- **No fixed windows.** The data defines the spans. All kinds of span are formed; the data decides which apply.
- **Full depth**: every price level and every order. No top-10, top-3 or top-of-book views.
- **Everything we hold gets run.**
- **No bad version is kept.** Use the correct build, replace, and delete what it replaces. Old code and files sneak
  into new runs, so whatever is replaced is removed in the same change that replaces it. The old build is never a
  pass/fail test for the new one.
- **Everything is saved to git.** Temporary storage elsewhere is allowed only on the way to git.
- **Earlier Claude analysis** (markets-data `main` and `codex/claude-independent-research-20261113`; Markets
  `agent-pass/reanalysis/claude`) is not to be read or allowed to shape new work.

---

## 3. What is already true (all pushed unless stated)

**The tape.** Seven UTC clock-day files of front-month natural gas, order by order, in
`data/nymex_mbo/ng_v0_oct2023/`: Oct 1, 2, 3, 15, 16, 17, 18. The Oct 1 and Oct 15 files are the Sunday files that
open the two trade weeks.

**The trade-day replay** (`trade-day-rebuild-20261116/`). `scripts/trade_day_stream.py` yields every message of a
trade day on a book warmed from the Sunday file and carried through every 00:00 UTC. At each 00:00 UTC crossed, the
carried book equals the exchange's own snapshot: same orders, sides, prices, sizes and queue order on every level.
Session messages: 820,642 / 879,830 / 846,406 / 771,787. Trades: 38,127 / 41,410 / 33,703 / 30,739, total 143,979
(143,270 from the old archives found identical, plus 709 never held before). Its README is the recipe for building
any new trade day and lists what is still written in by hand for October 2023.

**Resting-order age** (`resting-order-age-20261116/`). On 2,926 orders the snapshot's event time is exactly the time
of the message that last set the order's queue priority, so the book rule and the exchange agree. The exchange
re-lists every weekend carry-over order in one block on Sunday morning with one stamp; for those orders no earlier
time exists on the tape, and their ages are marked as lower bounds (182 to 319 such orders resting at each 00:00
UTC).

**The book record at every trade.** 143,979 records, one per trade: the full book when the trade arrives, every
level, every order, with lower-bound ages marked. Stored on four branches of markets-data,
`trade-day-book-20231002`, `-20231003`, `-20231017`, `-20231018`, 100 trades per file with a file list. All four
were verified complete after upload: 382, 415, 338 and 308 files, each branch matching what was sent. The records for
the 5,513 workbook ticks are also on the working branch in `trade-day-rebuild-20261116/book_records/`. The old
selected-tick records were deleted.

**The ROOT audit** (`root-audit-20261116/ROOT_WINDOWS_AND_CAPS.md`). Every fixed window, cap, threshold, tick collapse
and repeated pass found in the old ROOT, with file and line, read at Markets pin `2ebb8ce8` (the producer package)
and Markets `7f34afa`.

**The ROOT redesign** (`root-redesign-20261116/`). `CAPABILITY_MAP.md` (draft 2) is the shape Greg told us to
proceed with. `SPEC-tape-stream.md` is the first module spec, with three questions for Greg.

**Runpod.** The 4,096 GB scratch volume that held old ROOT outputs for trade days Oct 2, 3 and 17 was deleted on
Greg's instruction; it was costing $0.796 an hour. The account has no pods and no volumes, one idle endpoint
(`frankie-reading-granite42`), and about $38. The Runpod plugin is enabled on the account, so its tools load in a new
session. Four small CPU pods created in data center US-CA-2 never started; with the volume gone there is no reason
to use that data center.

**Not done.** The workbook cells still hold old values. The four old archive branches
`codex/frankie-book-recovery-*` still exist. The trade-day rule is on the Markets trunk (`b827fbe`), the Markets research branch (`96ff7f3`) and branch
`ccr-5317ce1c-hpqa9c`.

---

## 4. The plan, in order

### Step 1. Finish the two read-throughs that were running when this was written

Purpose: we cannot delete or rerun safely until we know exactly what the old ROOT touched.

- **The file-by-file list of old ROOT code**: each file marked keep, lift a part, replace and delete, or not ROOT,
  plus every script or setting that would pull old ROOT code into a new run. Save as
  `root-audit-20261116/OLD_ROOT_FILE_LIST.md`.
- **The lineage trace**: what "our two new workflow steps" are and what ran between ROOT and them; for every sheet
  field, where its values come from; every file and folder in this research folder that rests on an old ROOT output.
  Save as `root-audit-20261116/OLD_ROOT_LINEAGE.md`.

If either is missing from the folder, it did not finish and must be run again before anything is deleted. Two places
cannot be reached from a cloud session and must be checked separately: the stopped AWS boxes and Desktop's own
working folders.

### Step 2. Greg's sign-offs (section 6 lists them)

Purpose: nothing is deleted and no code is written on a guess.

### Step 2b. The calculation inventory (Greg, 2026-11-16)

Greg: "We really need to inspect all of our calcs from root through the 2 new workflow pieces and adding in the
research projects we did to figure out what we want to figure out, is currently being calc, and how we make new
calcs to meet our needs."

Purpose: before any new calculation is designed, lay every existing one out next to the question it was meant to
answer, so that we can see three things side by side: what we want to find out, what is actually being calculated
today, and what new calculation the full record makes possible. Without this, the new research layer would either
repeat the old calculations with their limits, or drop a question nobody remembered was being asked.

Scope, in the order the data flows (see `root-audit-20261116/OLD_ROOT_LINEAGE.md` section B):
ROOT and its sections; replay comparison; four-day extensions; family replication; combined events; whole
lifecycles; lifecycle data links; the 141-field grid; the per-trade book archive; the S fields; the 2021 Step 1
census; Desktop's SQLite and Julia family research; and the research projects in this folder (priority-ten,
discovery-depth, reanalysis, fifteen-strategies, paper-validation, the case tables, the dipole maps).

The deliverable is one table, `root-audit-20261116/CALCULATION_INVENTORY.md`, one row per calculation:

| Column | What goes in it |
|---|---|
| Where | stage, file and line |
| What it was meant to find out | the question, in plain words, from the code's own notes and the handoffs |
| What it actually calculates | inputs, the formula in words, the step size, every window, cap and threshold |
| What data it uses and what it leaves out | depth, resolution, which messages, which contract |
| What it feeds | the later calculations and sheet fields that take it in |
| What the full record allows | how the same question would be asked with every message, full depth, no fixed window |
| Keep the question? | Greg's column |

Method: read the code and definitions only, not results or findings. One reader per stage, each returning rows for
this table; then one pass to join them and to list questions that no calculation answers and calculations that
answer no stated question.

The first column of questions is drafted from the records for Greg to correct. Already on record as things he wants
to find out: which pieces of data dictate what happens next; the shapes of a family across its life (the approach
before birth, the turn, the tail and exhaustion), by direction; the dipole dive; the roughly half-second lead on
natural gas; the exhaustion canary and the entry hypothesis; flow authority, its collapse and recovery; where a
turning point comes from; and what each S field was trying to measure.

**The Claude and Codex research projects (Greg, 2026-11-16):** "let's list the intended results and research
angles. I don't think we want to keep the results. They probably aren't calc correctly." So for every research
project by either of us, the inventory records what it set out to find and the angle it took, and nothing else. The
results themselves are not carried forward and are removed with the rest of the old-ROOT material once the list is
signed off. This lifts the "do not read the earlier Claude analysis" wall for one purpose only: reading what each
project intended and how it approached it. Result numbers, findings and conclusions are still not read into new
work. Saved as `root-audit-20261116/RESEARCH_INTENTIONS.md`.

This step can run while the new ROOT record is being built (step 3), because the record keeps everything
regardless. It must be finished and signed off before any research-layer spec is written (step 4).

### Step 3. Build the new ROOT, one piece at a time

ROOT becomes only the complete record. Each piece follows the same cycle: a short written spec; Greg approves; build
in small slices; test on real tape only; a trial on a short stretch of one trade day; then all four trade days; a
receipt with counts; and, in the same change, delete the old piece it replaces.

1. **`tape-stream`** (spec written). Make the existing trade-day stream work for any trade day: cut by exchange time
   so winter is right; warm-up files worked out from the calendar; the contract taken from the tape; refusal when a
   file is missing or a carried book differs from the exchange snapshot; the same interface for a live feed. It must
   reproduce the four verified trade days to the exact counts above.
2. **`book-core`**. One full-depth order book, in one pass. Lift the order-book rule from the old adapter (it matched
   the exchange on every order checked) and leave behind its top-10 views, fixed activity windows and legacy rows.
   Every order, its queue position and its times, available after every message.
3. **`event-ledger`**. One record per message with nothing left out: what the message was, what it did to which
   order, every change it caused in the book, and the end-of-event flag where it occurs, so a reader can take the
   book after any message or only at event ends. The spec must settle the record layout and the storage size: a
   trade day has about 770,000 to 880,000 messages.
4. **`change-points`**. Every change of state the tape shows, of every kind, each with the message that caused it: a
   level appears or empties, the best price moves, an order joins, shrinks, grows, moves or leaves, a queue's front
   changes, the trading side flips, an eaten level refills. ROOT does not pair these into chosen spans.
5. **`checks`**, built alongside each piece: snapshot equality at every 00:00 UTC; queue sums; every message
   accounted for; the same bytes when run twice; and a guard that fails the build if ROOT code contains a window
   length, threshold, top-N or sample that is not on a short declared list with its reason.
6. **Running it.** After a trial stretch passes in the session, run all four trade days on Runpod CPU pods. Bring
   Greg the pod type, hourly price and expected total before starting anything.

### Step 4. The research layer on top of the record

Purpose: this is where "which pieces of data dictate things" is answered. Every definition here is visible, named
and changeable, and none can remove anything from the record.

- **`spans`**: spans formed by pairing change points: an order's life, a level's time at the front, a one-sided run,
  a drain and refill, a structure's own life, and any other pairing the record supports. All are formed.
- **`structures`**: candidates, episodes, dipoles, families and lineage as named definitions, with no percentile
  bar, warm-up or spacing rule. The 2021 Step 1 family definitions are the base. First list every hard-coded
  boundary in the Step 1 programs (Markets `7f34afa`, `research/ng_exhaustion_mbo_5y_step1_census_20260822.py` and
  two others; seen so far: lineage depth 5, 52 and 26 week blocks, the frozen family classifier), show Greg the
  list, then remove them and let the new data expand the families. Families stay trade-agnostic.
- **`trade-join`**: for every trade individually, every span and structure it sits inside, where in its life, and
  the values at that moment. This is what feeds the sheet.

### Step 5. Remove everything built on the old ROOT, and rerun what depended on it

Purpose: Greg's rule that no bad version is kept, and that old outputs must not be merged into anything new.

Using the lineage from step 1: delete each file and folder that rests on an old ROOT output, and rerun the steps
that consumed them on the new record, including the two workflow steps and whatever ran between ROOT and them.
Greg expects this may be small, because some steps right after ROOT were redone completely; the trace decides.

### Step 6. Refill the sheet from the new record

- The 709 new trades (457 on trade day Oct 2, 252 on trade day Oct 17): all per-trade fields.
- The 13 external points (sheet fields X01-X13): they were built on the trading day from the start and should not
  change for existing trades; attach them to the 709 new trades. Where the four October 2023 day files live has not
  been checked.
- Book, queue and age fields from the new book records.
- The S fields (S01-S19): the old calculation uses fixed 64- and 1,024-group windows and the top 3 levels
  (`c15_teacher_r3.py` line 205), so it is not run as it stands. What each S field was trying to measure is re-asked
  of the full record. Greg agreed to this on 2026-11-16.
- The Step 1 fields (L080, L083-L089) from the expanded families; the family and pre-birth fields (L060-L063,
  L067-L071) from the new structures. L024 and L026 are the 2021 raw objects themselves and stay as they are.
- Write the new workbook release and apply the same to the four-day research workbook.
- Then delete the four old archive branches and list exactly what was removed.

### Step 7. Housekeeping that needs Greg

- The trade-day rule is on the Markets trunk as of 2026-11-16 (`claude/kalshi-s79-kickoff-ij8t9o` at `b827fbe`).
  It is also on `research/markets-adaptive-wavepacket-migration-20261108` (at `96ff7f3`), the branch the second
  session of 2026-11-16 was cut from. The trade-cost rule ("trade cost is not a market condition", Greg 2026-11-08) was
  added to the trunk's `CLAUDE.md` on 2026-11-16 (`9a28fcb`), so the two files now match. Only `CLAUDE.md` was
  brought over: the rest of the original rule commit `2e9af64` (two skill files, `KALSHI_TRADING.md` and six
  research programs that remove fee terms, including `lag_join.py`) is still only on the research branch. Greg to
  say whether those go to the trunk too.
- Deleting old code from Markets branches other than the session's own.

---

## 5. What gets deleted, and when

| What | When |
|---|---|
| Old selected-tick book records | Done |
| Runpod scratch volume with old ROOT outputs | Done |
| Each old ROOT code file marked "replace and delete" | In the same change that brings in its replacement |
| Every script or setting that stages old ROOT code into a run | When `tape-stream` and `book-core` land |
| Files and folders in this research folder that rest on old ROOT outputs | After Greg signs off the lineage list |
| Old archive branches `codex/frankie-book-recovery-*` | After the new workbook is written |
| Old cursor numbering columns in the trade lists | After the workbook rows are re-keyed |
| Results of the Claude and Codex research projects (reanalysis, discovery depth, priority ten, fifteen strategies, paper validation, the independent Claude research) | After `RESEARCH_INTENTIONS.md` is signed off |
| Old ROOT outputs on the stopped AWS boxes; Desktop's family research files | Greg's call, once listed |

---

## 6. Waiting on Greg

1. `SPEC-tape-stream.md`: where the new ROOT code lives (proposed: Markets repository, new folder `root/`); what to
   do in a week with an exchange holiday or a missing Sunday file (proposed: stop and name what is missing); a
   contract roll inside a trade week (proposed: carry both contracts' books).
2. Sign-off of the old ROOT file list and of the lineage delete list, once they exist.
3. (Settled 2026-11-16.) "Our two new workflow steps" are the original trade day Oct 18 SQLite and Julia family
   research, and, probably, Codex's four-day workflow processing of Nov 9 (5,075,640 research rows). Detail in
   `root-audit-20261116/OLD_ROOT_LINEAGE.md` sections A and G. The older version with "hundreds of trillions" of calculations was scrapped completely and restarted;
   Greg mentioned it only as a pointer. There is nothing of it to find or retrieve.
3b. Correct the draft list of what we want to find out (step 2b). (Settled 2026-11-16: the Claude and Codex
   research projects are listed by intended result and research angle only; their results are not kept.)
4. Permission, or his own hand, for pushes to Markets branches other than the session's.
5. Go and budget for pods when the first full run is ready.

---

## 7. What is not known yet

- How large the per-message ledger and change-point record are, and so how they are stored.
- How long a full four-trade-day run takes at one step per message.
- What each fixed window turns into once the data defines it. That is the research itself, not a detail.
- Whether other contract months are held for these trade days.
- What is on the stopped AWS boxes.

---

## 8. Starting the next session

1. Read this file, then `NEXT_SESSION_HANDOFF_20261116B.md`, then `root-redesign-20261116/CAPABILITY_MAP.md` and
   `SPEC-tape-stream.md`, then `root-audit-20261116/ROOT_WINDOWS_AND_CAPS.md`.
2. Work on branch `ccr-349e2ffe-07p8od` of markets-data. Do not fetch the `trade-day-book-*` branches whole.
3. `pip install databento pyarrow pandas`. Pinned old code, for reading only: Markets `7f34afa` (branch
   `codex/frankie-brain-four-day-pins-20261109`) and the producer package at Markets pin
   `2ebb8ce8ef4834545ad99a4ecdff50c18c5b3134` (`research/kalshi/frankie_raw_mbo_benchmark/`).
4. Use the "Markets" cloud environment; it allows the Databento and Runpod addresses.
5. Begin at section 4, step 1.
