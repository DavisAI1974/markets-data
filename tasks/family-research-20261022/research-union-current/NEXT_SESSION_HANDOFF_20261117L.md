# Handoff L, end of the eleventh session (2026-11-17, about 06:10 UTC)

Branch: `ccr-349e2ffe-07p8od` in `DavisAI1974/markets-data` for data and documents. This file replaces
`NEXT_SESSION_HANDOFF_20261117K.md` as the starting point. Every decision of this session, with Greg's words, is in
`root-redesign-20261116/ROOT_GAMEPLAN_DECISIONS.md`, section "Eleventh session" (its last entries are the newest).
Desktop writes to the same branch: fetch before every push.

## Where we stopped (Greg: "let's stop for the night ... kill the pods. We'll pick up from here later")

- **No pod exists. Nothing is running. Nothing is billing.** The account was checked at the stop and shows none.
- **Everything made is stored and pushed.** Nothing is half done.
- **We stopped while reading inputs for the three remaining Step 2 calculations. No code was written for them and
  nothing was run.** Greg had given the go ("Run the 3 calcs on the pods. Let's gwt this done"), then stopped for
  the night. A pod needs his go again at the time, with the price.

## Done this session

1. **The rebuild fetched, proved, stored; the four pods deleted.**
   - **The peaks came out the same** on all four trade days (every column equal on every row; only the ranked
     column `peak_standing_so_far` is gone). So the new peak files are stored, by his rule.
   - The rebuilt rows: 408 columns (85 tape, book and trade; 323 outside). Every column shared with the old rows
     is equal on every row. Book pictures and vendor restatements came back byte for byte the same.
   - `outside_changes` made again beside the rebuilt rows; checks passed.
   - Stored: `root-rows-20231002` `daac81d`, `-20231003` `e4ffcc9`, `-20231017` `74f4225`, `-20231018` `d2c34be`,
     each with `FILES.md` rewritten.
2. **The short-stretch workbook written again** from the rebuilt rows (`ROOT_short_stretch_20231002_0900.xlsx`,
   20,000 rows, 408 columns, 37.1 MB, read back equal to the stored rows).
3. **Greg's decisions recorded** (all in the decisions file):
   - "Just keep the daily sheets updated and we'll do the workbook all at once at a slow time": each trade day's
     stored files are kept up to date as each calculation lands; the Excel workbook is written all at once later,
     broken into parts to stay under GitHub's limit. At 408 columns a part must be about 45,000 rows (80,000 rows
     would be about 149 MB).
   - "When all of the calcs are done and the excel sheets have been updated I'll show you the earlier discovery."

## Where each trade day stands (all four the same, all pushed)

- The rows, rebuilt (raw tape on every row: 16 fields; the place in line, first in first out, on every row).
- Twelve calculations stored: `flow_peak`, `peak_story`, `book_totals`, `quote_runs`, `quote_peaks`, `peak_links`,
  `open_stories`, `refills`, `sweeps`, `chain_peaks`, `together`, `outside_changes`.
- The 6 pm to 8 pm trade legs (trade days Oct 2 and Oct 17).
- NOT in them, because never run: the three calculations below, and Native's missing two hours.

## Open, in order

1. **The three remaining Step 2 calculations, on four pods** (layouts approved: `STEP2_PLAN.md` pieces D, I and K).
   None has code yet. Write them first (code only), then ask Greg's go with the price (last quoted: four General
   Purpose 8-CPU pods, $0.32 an hour each, $1.28 for the four; check the live price).
   - **The trade legs beside the peaks** (the rest of I). Inputs: the old legs for all four trade days (markets-data
     `main` commit `15fbf2a`, `.../combined-events/run-42571551209-1/events-<trade day>/a-print-legs.parquet` and
     `a-trades.parquet`; `root/trade_legs.py` shows how they are fetched and pinned) and the new 6 pm to 8 pm legs on
     the `root-rows` branches. The peaks in play come from `root/calcs/in_play.py`, as `quote_peaks` uses it.
   - **The resting orders through a peak and a leg** (K). From the stored rows. Greg's earlier call: where a filled
     order had another order ahead of it in our line, that is shown as a fact (how many orders, how much size, which
     orders); it is built with this piece.
   - **Native's dipole beside the peaks** (D). Native's stored record is placed as it is (valid data is kept); on
     trade days Oct 2 and Oct 17 it starts at 8 pm and is marked so. What was learned about the record this
     session, to save finding it again:
     - Trade days Oct 2, 3 and 17: markets-data branches `codex/frankie-lifecycle-recovery-<date>-42621496819`,
       folder `tasks/family-research-20261022/frankie-four-day-pins/native-lifecycle-42621496819-1/<date>/`:
       225 `lifecycle-NNNN.jsonl.gz` files and 225 `lifecycle-index-NNNN.parquet` files (four digits), with
       `MANIFEST.json` (every file's size and fingerprint), `SECTION_FIELDS.json`, `RECOVERY_RECEIPT.json`.
     - On Oct 2: 5,289,814 lines in 12 sections; 741 `candidate` lines and 1,482 `episode` lines. An `episode` line
       carries `candidate_id`, `birth_recv_ns`, `precursor_recv_ns`, `recognized_recv_ns`, `recognition_outcome`,
       `terminal_phase`. Each index file says, line by line, which section a line is and the time it was known by
       (`known_by_ns`), so the candidate and episode lines can be found without reading everything.
     - Fetch single files only (`raw.githubusercontent.com/.../<branch>/<path>`). Do NOT list that branch with file
       sizes through a partial clone: it downloads every file one at a time (done by mistake this session, stopped,
       the copy deleted; nothing was changed anywhere).
     - Trade day Oct 18's record is elsewhere and from an older run: Markets commit `3d0b06aa`,
       `artifacts/sqlite-triage/20261022/families/trade-lifecycle-targeted-v1/source-episode.jsonl.gz`.
2. Remove the stopped chain matching code (`root/chain_ways.py`, `root/chain_common.py`, the `ways` pod job and
   their constants). Clean-up; nothing runs.
3. **Native's missing two hours** (6 pm to 8 pm, trade days Oct 2 and Oct 17), made the same way as its other
   hours. Unchanged from handoff K item 3: a short test run on the Oct 2 file alone must match the stored record
   line for line first; the full run needs the price put to Greg.
4. Greg's open calls, each put once when the work reaches it (unchanged from handoff K item 4): measured gas use
   for the 16 city weights; `peak_highest_for_ns`; `chain_peaks` writing six steps of before lines.
5. The full workbooks, all at once, at a slow time, in parts.
6. Greg shows the earlier discovery (after the calculations are done and the workbooks written).
7. The strategy versions as a paper-trade barometer (handoff K item 5).

## TO REVISIT (Greg: carry into every handoff until done)

Native's record is built on predetermined windows (a 20-second roll, a level set from 85 in 100 seconds, 60-second
horizons), which his "no predetermined windows" rule does not allow for our own work. He chose to keep Native as it
was made for now.

## Where everything is

- Code: Markets branch `ccr-3096f7d6-fst7al` (this session's own), tip `e083757`, the same commit as
  `claude/loving-hawking-pwxr2c`. No code was changed this session. Nothing is on the trunk.
- Stored rows and outputs: `root-rows-20231002` (`daac81d`), `-20231003` (`e4ffcc9`), `-20231017` (`74f4225`),
  `-20231018` (`d2c34be`). Clone each shallow. Never fetch old branches whole.
- The "Markets" cloud environment still lists the four dead pod addresses of this session (and earlier ones); they
  can come off the list. A new set of pods needs its own four addresses allowed (an approval card for Greg).
- Agent skills: read from `addyosmani/agent-skills` tag 0.6.8 (git workflow skill). Runpod: the MCP and its skills.
- Standing rules: unchanged from handoff K ("Greg's standing rules sharpened this session") and the decisions file.
