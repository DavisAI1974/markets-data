# Handoff, sixth session of 2026-11-16 (the 13 pinned, four trade days stored; next: short sheet file, delete list, Step 1 and 2)

Branch: `ccr-349e2ffe-07p8od` in `DavisAI1974/markets-data` for data and documents. This file replaces
`NEXT_SESSION_HANDOFF_20261116E.md` as the starting point.

The sixth session was started in the chat app by mistake and stopped by Greg partway ("I meant to be in code").
Items 1 and 2 of handoff E are done. Item 3 is measured but its file is not stored. Items 4 and 5 are not started.

## Read these, in this order

1. `root-redesign-20261116/ROOT_GAMEPLAN_DECISIONS.md`: every decision in Greg's words. The section "Sixth session"
   is new.
2. `root-redesign-20261116/SPEC-root.md` and `SPEC-outside.md`: both approved. The decisions file governs where
   anything differs.
3. Markets `CLAUDE.md`, "The trading rules".

## Where the ROOT code is (read this before building)

**All ROOT code is on Markets branch `claude/root-session6-017eY1`** (tip `b39e10a`; not on the trunk). It already
holds everything from `claude/plugin-company-customization-z50yb3`. A new session gets a new, empty branch. Bring
the code in first: `git fetch origin claude/root-session6-017eY1 && git merge --no-edit FETCH_HEAD`. If the merge
refuses with "unrelated histories" (a shallow clone), start the session's branch at that tip instead:
`git checkout -B <session branch> FETCH_HEAD`.
Fresh container: `pip install databento pyarrow xlrd openpyxl pytest`. Set `MARKETS_DATA` to the markets-data
checkout.
ROOT code goes to Markets on the session's own branch; data, outputs and documents go to markets-data. Never push
data to Markets. Nothing goes to the Markets trunk without Greg's word.

## FIRST THING: confirm the four stored trade days carry the "no orders" fix

The four trade days were stored, complete and checked, on markets-data branches `root-rows-20231002`,
`root-rows-20231003`, `root-rows-20231017` and `root-rows-20231018` (first commits `d51e0b3`, `b5501b2`, `b540ada`,
`1309ff2`). A second commit on each, with one small fix (an emptied price line is the words "no orders" instead of
a blank text cell), was being pushed by a background job when the session ended. Check each branch:

`git ls-remote origin 'refs/heads/root-rows-*'` then `git log -1 --format=%s origin/root-rows-<day>`

- If the newest commit says "rebuilt - an emptied line is the words 'no orders'", that trade day is finished.
- If it still says "ROOT stored rows, book pictures and receipt", rebuild that trade day and push it as a second
  commit on the same branch: `python3 -m root.run build <day> --out <folder>` (about 2 minutes, one trade day at a
  time: three at once ran out of memory), copy the `.parquet` files and `RECEIPT.json` over the branch's files, keep
  its `playback-<day>.json`, rewrite `FILES.md`, commit, push.
- The state at the end of the session is written at the bottom of this file under "State of the push".

Either version is complete and passed every check. The only difference is that one text cell.

## What is built (all on the real tape, nothing made up)

| Part | File | State |
|---|---|---|
| calendar | `root/calendar.py` | done |
| outside tables | `root/outside.py` | done: all 13 as tables; now hold every value known before 6 pm Eastern Oct 18; new table of routine hourly city readings |
| tape | `root/tape.py` | done; the calculation gate `for_calculations()` |
| book | `root/book.py` | done |
| rows | `root/rows.py` | done: one row per tick, 217 fields (sections A to E, and G) |
| pin | `root/pin.py` | done: section G, the 13 outside points on every row (132 fields) |
| store | `root/store.py` | done: rows and book pictures as Parquet parts, restatement table, receipt |
| checks | `root/checks.py` | done: row checks, records accounted for, trade counts, the pinning check, playback |
| sheet | `root/sheet.py` | written and run on a short stretch; the full workbook is not written |
| run | `root/run.py` | commands: check-week, check-book, build, playback |

Stored rows, per trade day: Oct 2: 820,670 rows; Oct 3: 879,497; Oct 17: 846,158; Oct 18: 771,468. Each 217 fields.
About 160 to 200 MB per trade day with the book pictures. A build takes about 2 minutes in the session. **No pods
are needed for the foundation.**

Calls Claude made in the pinning, stated to Greg in the session, his to correct (full list in the decisions file):
the once-per-trade-day figures (forecast, disagreement, expiry count) are empty on rows of no trade day; everything
else is the latest value known at the row's received time, with its known-from time on the row; the Sunday start-up
rows are pinned by the time as stamped; each forecast figure carries its cities in one cell; city temperatures are
the latest routine hourly reading with its own time beside it.

## What to do next, in this order

1. **Confirm the four stored trade days** (above).
2. **The short stretch of the sheet: store the file and tell Greg its size.** Already measured: 20,000 rows of trade
   day Oct 2 from 9:00 am Eastern (9:00:00 to 9:06:38 am) = 19.8 MB, about 990 bytes a row, 18 seconds to write,
   read back equal to the stored rows. That implies about 810 MB for trade day Oct 2 and about 3.3 GB for the four.
   Greg has not been given these numbers in a finished report yet. To write the file again from the stored rows:
   `python3 -m root.sheet 20231002 --rows <root-rows-20231002 checkout> --out <markets-data folder>/ROOT_short_stretch_20231002_0900.xlsx --readme <...>/WORKBOOK_README_PAGE.md --from-eastern 09:00 --count 20000`
   Two things for Greg to decide before the full workbook is written: GitHub refuses a file over 100 MB, so a trade
   day's workbook cannot go into git as one file; and 820,000 rows by 217 columns is heavy for Excel to open. The
   full workbook is written ONCE, after the calculation columns exist (Greg: "Do your plan").
3. **Delete the old** (Greg: "After we get new data filled in let's delete the old"): show Greg the list and wait
   for his "delete". Delete nothing before it. The list as understood:
   - `trade-day-rebuild-20261116/scripts/` in this folder;
   - the four `trade-day-book-*` branches of markets-data (143,979 book pictures made with the stand-in scripts, cut
     at the wrong hour); all four were on the remote on 2026-11-16;
   - `root-redesign-20261116/CAPABILITY_MAP.md` and `SPEC-tape-stream.md`, which `SPEC-root.md` says go once it is
     approved. They are still in the folder: put them on the list for his word.
4. **Step 1 and Step 2 calculations** (gameplan work): first the list of hard-coded limits in the Step 1 programs,
   owed to Greg, sent to him alone before anything else. Build it from the code itself (the
   `chatgpt/ng-exhaustion-*` branches of Markets, read-only), every limit with its file and line, and say which
   programs the list covers; the "seen so far" list in the decisions file is partial. Then each calculation laid
   out his way (what we want, what it did, what changes) and approved BEFORE it is built or run. Nothing is run and
   no code goes into `root/calcs/` until he says yes. Calculation code receives ticks only through
   `tape.for_calculations()`. Carry into the layouts: the 0.85 level taken over a whole UTC clock day (it looks
   ahead); the candidates for the averaging exception (to confirm with Greg); whether any calculation reads another
   contract month's order book (the definite answer on the full tape of the other months); the definitions built on
   a fixed window, which cannot simply drop it.

## Rules (all recorded in the decisions file)

- A TRADE DAY runs 6 pm Eastern the evening before to 5 pm Eastern on the named date. The 5 pm to 6 pm hour is its
  own marked stretch. Never a bare "day" or a bare date.
- ONLY THE FOUR TRADE DAYS (Oct 2, 3, 17, 18, 2023) enter any calculation. Data from outside them seats the order
  book and nothing else. Any other use of outside data goes to Greg FIRST. Nothing is commingled.
- Rows are ticks, columns are fields. One row per tick, nothing collapsed. Nothing is dropped.
- Empty cells are never counted in a calculation and never stored as zero or as blank text.
- Every trade individually. No rates, averages or model scores (one Step 1 exception, to confirm with Greg when it
  is laid out).
- Every calculation is laid out for Greg and approved BEFORE it is built or run, Step 1 and 2 included.
- Checks: one per new part, run once, on that part only. Do not re-run everything. Keep moving.
- Never invent data. Real tape only. Trade cost is not a market condition.
- AWS is off limits until Greg says. No pod starts until he has seen the pod type and the price.
- Do not re-ask what he has decided. Where a point is a detail, make the call, state it, let him correct it.
- Markets is code only; the trunk gets nothing without his word.

## Waiting on Greg

- His "delete" for the old material, once he has seen the list.
- The two workbook questions above (the 100 MB limit; the size for Excel).
- `artifacts/recovered-c-drive/` (4.7 GB) is still in Markets; it waits on AWS.
- `web.archive.org` on the cloud environment, if the street estimate (X12) is wanted.

## Facts from this session (for whoever builds next)

- The received time never goes backwards on the written rows of the four trade days, and no row is received before
  its exchange time. The 343 Sunday start-up rows of Oct 1 carry the unreliable-received-time flag; their stamps
  equal their exchange times (7:05 to 8:00 am Eastern).
- The session's memory limit is about 3 GB: build one trade day at a time, and read stored rows part by part.
- The compressed outside tables have different bytes on this machine (a different zlib build) with equal contents.
  The fingerprints in `data/outside/ng_oct2023/made/RECEIPT.json` are of the files as stored now.
- The handoff E file was changed after the sixth session cloned (its "Check results" were filled in); nothing in it
  conflicts with the work done.
- `using-agent-skills` (the Markets router) is not available in the chat app; it is in a code session.

## How Greg wants the work done

- Plain words, one piece at a time. He reads on a phone. Answer his question first, then return to the open item
  once.
- Do not re-ask what he has decided. Record decisions in git as they are made.
- Keep moving: build, one check on the new part, report what passed and what did not, next part.
- Keep foreground commands short. He stopped two long ones in this session; run a long build in the background with
  a log and report from the log.

## State of the push

DONE. All four trade days were rebuilt with the "no orders" fix, every check passed again, and the second commit
is on the remote for each: `root-rows-20231002` `806ee43`, `root-rows-20231003` `7b0f5d7`, `root-rows-20231017`
`cdcc525`, `root-rows-20231018` `aa226d1`. Nothing is left to rebuild; step 1 of "What to do next" is a look only.
Markets `claude/root-session6-017eY1` is at `b39e10a`. Playback was not run again after the one-cell change; the
playback records on the branches are from the first build of the session.
