# Handoff K, end of the tenth session (2026-11-17, about 05:40 UTC)

Branch: `ccr-349e2ffe-07p8od` in `DavisAI1974/markets-data` for data and documents. This file replaces
`NEXT_SESSION_HANDOFF_20261116J.md` as the starting point. Every decision of this session, with Greg's words, is in
`root-redesign-20261116/ROOT_GAMEPLAN_DECISIONS.md`, section "Tenth session" (its last entries are the newest). Desktop
writes to the same branch: fetch before every push.

## FIRST: four pods are running (Greg's go). Fetch, prove, store, then delete them

- General Purpose `cpu3g`, 8 CPUs, 32 GB, $0.32 an hour each ($1.28 for the four), started 05:34 UTC, running Markets
  `e083757` job `rebuild`: the rows built again with the outside tables as they now stand (hourly, no averages, no
  windows, no ranks), then `flow_peak` (its ranked column removed) and `outside_changes` beside the new rows.
- Pods: Oct 2 `oh6ne2gwlcildy`, Oct 3 `k021jyj7mk7hxf`, Oct 17 `e7iourinnnbz79`, Oct 18 `xjrhxh3z3o0wg9`. Progress is
  `https://<pod id>-8000.proxy.runpod.net/STATUS`: wait for `build passed`, `flow_peak passed`, `outside_changes passed`
  and `finished rebuild`. A `FAILED` line: read `build.log` / `flow_peak.log` / `outside_changes.log` there.
- Fetch and prove each trade day into its own shallow clone of `root-rows-<trade day>`:
  `python3 -m root.pod_fetch https://<pod>-8000.proxy.runpod.net <trade day> e0837576c466967fc4387dcb1de7ed6544f5b8ac --into <rows clone> build flow_peak outside_changes`
  (Markets branch `claude/loving-hawking-pwxr2c`). It replaces the rows, book pictures, vendor restatements,
  `RECEIPT.json`, the `calc-flow_peak-*` and `calc-outside_changes-*` files and their receipts. Update `FILES.md`
  (the rows now carry 323 outside columns; `peak_standing_so_far` is gone; the other calculations' outputs stand,
  made beside the earlier rows, whose tape, book and trade columns are unchanged), commit, push, confirm, THEN delete
  the pods with the Runpod MCP (load `runpod:runpod-mcp` first) and check the account shows none.
- **Greg's rule for the peaks (2026-11-17): "Of the peaks come out differently, then we keep old values and just
  delete column from stored avalues".** Before storing the new `calc-flow_peak-*` files, compare every one of their
  columns, row by row, with the stored ones (all columns except `peak_standing_so_far`). If all are equal, store the
  new files. If ANY value differs: do not store the new `flow_peak` output; keep the old stored files and only delete
  the `peak_standing_so_far` column from them (rewrite each part without that column, everything else byte-for-value
  the same), and say so in `FILES.md`. Either way tell Greg which happened.
- `playback-<trade day>.json` on each branch was made on the first build; not run again (no tests except on changed
  pieces). Say so in `FILES.md`.
- Then write the short-stretch workbook again from the rebuilt rows (`python3 -m root.sheet 20231002 --rows ... --out
  ... --from-eastern 09:00 --count 20000`; the stored `root-redesign-20261116/ROOT_short_stretch_20231002_0900.xlsx`
  carries the old averaged and ranked outside columns and is replaced). Tell Greg before running it in the session.

## Done this session (stored and pushed)

- The ROOT branch merged into Markets `claude/loving-hawking-pwxr2c` (code only; nothing on the trunk).
- `quote_peaks`, `together` stored on all four `root-rows` branches, checks passed. (`outside_changes` is being made
  again by the pods above.)
- The trade legs of 6 pm to 8 pm on trade days Oct 2 and Oct 17, by the old rule from 6 pm (`root/trade_legs.py`);
  every old trade and every old leg after the first came out again; stored on those two branches.
- Averages out (Greg: the cardinal rule): the averaged chain-model results and read-out deleted; `chain_models.py`
  removed. Outside figures made again hour by hour (`data/outside/ng_oct2023/made`, markets-data `5eab71f`): hourly
  observed temperature, wind and rain per city as reported, the cities' latest readings weighted at every new
  reading with degrees from 65 F, every forecast run hour by hour with GFS minus NAM; out: fund standings (1 and 3
  year windows), gas-day figures, the forecast high-low midpoint; storage five-year comparison kept in its table as
  information only, never on a row or in a calculation.
- Ranks out: `peak_standing_so_far` (a percentile) removed from `flow_peak`.
- The chain matching ("closest peak") STOPPED by Greg: our system deciding what is alike. Nothing of it was stored.

## Greg's standing rules sharpened this session (all in the decisions file)

- No averaging, blending, pooling or grouping of cases, ever, unless he asks for it by name; anything that would
  combine cases is named to him as averaging, in that word, before anything is written.
- ZERO predetermined windows. No ranking of any data (no place in line, percentile, standing).
- "We let the data group data together, not our systems." No labels, groups or identifiers until all four trade days
  have run all their calcs; grouping is done with him.
- "No tests except on changed pieces." Unchanged calculations are not run again.
- "It's wasteful to be rerunning these": a plain removal (a column) is deleted from the stored values, never made
  by running the calculation again. A rerun is only for a piece whose values change.
- Temperatures hour by hour; the gas day only as a label.
- Unchanged: trade day 6 pm to 5 pm Eastern; only the four trade days enter a calculation; outside data seats the
  book only; rows are ticks; empty is never zero; every trade individually; never invent data; gross; AWS off
  limits; Markets is code only; nothing to the trunk without his word; no pod without his go with the price.

## Open, in order (Greg's order: finish the data, then strategy)

1. The pods above: fetch, store, delete; the short-stretch workbook again.
2. Remove the stopped chain matching code (`root/chain_ways.py`, `root/chain_common.py`, the `ways` pod job and
   their constants). Greg: "Don't worry about it now! Just run the data!" - do it quietly as clean-up; nothing runs.
3. **Native's missing two hours (DECIDED: made as its other hours; revisit its windows later, see below).** Traced
   this session: the stored record was made by the Frankie box (Markets `7f34afa`
   `deploy/aws/box/frankie_box_bedrock.py` `run()` driving Native's pinned replay driver, Markets `2ebb8ce8`), in
   recovery mode (the box's emission stamp `frankie_emission` is on every ledger row). Oct 2 was fed only the Oct 2
   UTC file (808,453 records to the 21:00 UTC halt, no opening book). Oct 3 (which covers 6 pm) was fed: the opening
   book warmed from the previous UTC file up to its halt (book only, not counted), then that file's tail after the
   halt plus the trade day's file to its halt (the box's `opening_scope: PREVIOUS_UTC_TAIL`). Make Oct 2 and Oct 17
   the same way (Greg: the earlier file seats the book only). A short test run on the Oct 2 file alone must match the
   stored record (markets-data `codex/frankie-lifecycle-recovery-20231002-42621496819`, fetched by single file only)
   line for line before anything else. The stored receipts: that branch's `RECOVERY_RECEIPT.json`,
   `source-binding.json`. Greg's go for the Native test pod was given this session; a full run needs the price put
   to him again.
4. Still with Greg (put once each, when the work reaches it): replacing the 16 typed city weights with measured gas
   use (EIA residential and commercial deliveries by state, split by Census population; a new outside input);
   `peak_highest_for_ns` (how long since the flow was last larger - not a rank, but "bigger than"); `chain_peaks`
   writes six steps of before lines (the chain follows by rule at any depth from the peak lines); the 20-second flow
   is his standing exception. His remark: "we already have clearly defined family chain rules that were derived
   from runs months ago" - the old Step 1 families and Step 2 chain groupings are the base for the grouping stage
   (decisions file, fourth and seventh sessions; `STEP2_PLAN.md` "Step 2's own grouping"); he said not to worry about
   it now.
5. Then the strategy versions as a paper-trade barometer (handoff J item 2; Codex's handoff of 2026-11-13 on
   markets-data `main`, `claude-independent-research-20261113/HANDOFF.md` and
   `research-union-current/codex-review-and-gaps-20261113/REVIEW_AND_GAPS.md`; both read this session). Where they
   differ from tonight's rules, tonight's win, and he is told where: the handoff's 32 selected cases, eight realized
   trade types (labels), the 141 old fields and its cost and fill handling all conflict with the rules above.

## TO REVISIT (Greg: carry into every handoff until done)

Native's record is built on predetermined windows (a 20-second roll, a level set from 85 in 100 seconds, 60-second
horizons), which his "no predetermined windows" rule does not allow for our own work. He chose to keep Native as it
was made for now.

## Where everything is

- Code: Markets `claude/loving-hawking-pwxr2c`, tip `e083757` or later.
- Stored rows and outputs: `root-rows-20231002` (`d9fc971` or later), `-20231003` (`4cbfd75`), `-20231017`
  (`70ac9d4`), `-20231018` (`e4d0f02`). Clone each shallow. Never fetch old branches whole.
- Agent skills: read from `addyosmani/agent-skills` tag 0.6.8 (git workflow skill). Runpod: the MCP and its skills.
