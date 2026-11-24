# Where the old ROOT outputs went (lineage trace, 2026-11-16)

Provenance only: which files rest on which old inputs. No findings were read or judged. Produced by a read-through of
this research folder (catalogs, registries, handoffs, scripts) plus the pinned assembly code at Markets `7f34afa`.
"Read" means the statement was read in a file; "inferred" means it was not. Nothing has been deleted on the strength
of this list; Greg signs it off first.

## A. "Our two new workflow steps": the files do not say which two they are

- The workbook's "Workflow calculations" sheet names two families only in general terms (read:
  `assembly/update_master.py:41`, `assembly/prepare_workbook_specs.py:22`): "Original SQLite clock and family
  calculations" and "Julia model and full-depth calculation(s) suite".
- Its status reads "exact two user-requested runs not yet conclusively identified" (read, same lines). `README.md:17`
  says they "still require exact run/output reconciliation".
- `assembly/stamp_handoff.py:75` records three guesses Greg rejected ("Four-date combined event studies", "Codex
  trade environment application", "Recover October 2 Frankie second set") and his own description: "original Oct18
  SQLite/Julia work weeks ago, three dates a few days ago and four-day runs this morning".
- Gap-queue items G02 and G04 refer to "both new workflow outputs" without naming them.

**Greg has to name the two.** Candidate run families listed in `assembly/workflow_sources.json` (448 files):

| Family | Run id(s) |
|---|---|
| four-day-extensions | 42563528655 |
| family-replication | 42564821790 (preflight), 42566535537 |
| combined-events | 42569937357 (groups, actions, trades), 42571551209 (studies a/b/c) |
| whole-lifecycles | 42573465249 |
| lifecycle-data-links | 42583801329 |
| replay-comparison | no run id; Markets `3d0b06aa` |

The inputs to "Original SQLite/Julia" are Desktop's family research files, Markets
`artifacts/sqlite-triage/20261022/families/` (read: `assembly/expand_sources.py:16-18`).

## B. The chain from ROOT onward, as far as the files show it (order inferred from run ids)

1. ROOT and native outputs: `replay-artifacts/<trade day>/root-native-remaining` and the native-dipole cache.
2. replay-comparison: research atlas, flow-book discovery, candidate inputs.
3. four-day-extensions (continuous pre-birth), then family-replication (family starts, pre-birth controls).
4. combined-events: per-group book with the top 10, actions, trades; then family occurrences, dipole clocks, signals.
5. whole-lifecycles (includes the per-second native flow table), then lifecycle-data-links (trade and signal links,
   external points).
6. The joined-inputs grid of 141 fields (`four_day_pins/assemble.py`, run 42608467894).
7. The per-trade book archive (book-recovery 42617700678) and the native lifecycle copy (42621496819; copied from
   ROOT, not rerun).
8. The S-field run 42640458600, unfinished.

## C. Where each sheet field's values come from

| Fields | Source |
|---|---|
| day, trade id, event / receive / known-by clocks | the tape (all 143,270 trades found identical in the rebuild) |
| trade ordinal, trade cursor, source trade fields, coverage | old archive numbering (shifts on trade days Oct 2 and 17) |
| L001-L023, L025, L081-L082 | static documents and controls |
| L024, L026, L080, L083-L089 | the 2021 package; empty |
| L027, L028, L030-L037, L047 | tape content, delivered through the old book archive |
| L029, L038, L046, L053 | old book archive receipts and integrity fields |
| L039-L045, L052, L054, L057 | old book archive (the original grid used the top-10 group book; its producer is not identified) |
| L048 | trade operands plus old ROOT flow |
| L055, L056 | old ROOT per-second flow |
| L049, L050, L051, L058, L059, L076 | old ROOT sections: queue, replenishment, absorption, candidates, episodes |
| L064, L066, L090 | old ROOT plus old book archive |
| L065 | old book archive, with the fixed activity windows |
| L093 | old ROOT candidate discoveries |
| L099 | hashes of old ROOT and old book states; model part pending |
| L060-L063, L067-L071 | empty (old ROOT planes existed for trade day Oct 18) |
| L072-L075 | trade clocks from the tape; L075 also uses old group clocks |
| L077-L079, L091-L092, L094-L098 | Frankie output; blank |
| X01-X13 | outside published data (X13 includes price-derived curve operands) |
| S01-S19 | the S-field code, trade day Oct 18 only; S04 and S09 use restarted ages |

## D. Files and folders in this research folder that rest on old inputs

**On old ROOT sections and lifecycle ledgers**
- `field-rebuild-20261113/`: `native_records`, `native_joins`, `flow_inputs`, remaining-field recovery.
- `oct18-native-recovery-20261115/`, all of it.
- Workbook releases R1 and R2.

**On old per-second flow and the 20-second roll**
- The whole-lifecycles native flow table (the population called P01).
- `priority-ten-20261109/`, `Priority_native_flow.xlsx` (inferred), `discovery-depth-20261109/`,
  `reanalysis-20261109/`.
- `case-case-series.csv`, `case-case-per-second.csv`.

**On old dipole candidates, episodes and lifecycles**
- `dipole_trade_gaps.csv`, `dipole_gap_summary.json`, `dipole_map_source_verification.json`.
- `corrected_price_response.json`.
- All `case-case-*.csv` and `ccode_render_review.csv` (inferred).
- `evidence/` (inferred).

**Built on the above**
- `paper-validation-20261109/` (inferred), `fifteen-strategies-20261113/`.

**Mixed**
- `Frankie_four_day_research_current.xlsx`, `research-pins/*.xlsx` (inferred), `trade-layers/*.xlsx` (all 141
  fields).
- `evidence-availability-20261113/`: `raw/`, the field and tick audits.
- `field-rebuild-20261113/original_full_population/`, `Claude-Eight-Trade-Types-Original.xlsx`.
- `s-field-test-20261116/results/census.json` (a census of the R2 workbook).

**On the old per-trade book archive (not ROOT)**
- `field-rebuild-20261113/`: the book shard lists, `event_records`.
- `s-field-test-20261116/`: `scripts/run_second_set.py`, the trade day Oct 18 ledger and twin pairs.

## E. What does not rest on old inputs

- `trade-day-rebuild-20261116/` (from the raw tape; its trade lists still carry the old cursor beside each trade).
- `resting-order-age-20261116/`, `root-audit-20261116/`, `root-redesign-20261116/`.
- `historical-shape-attachments/`, `historical_shape_sources.json`, `dipole_dive_chat_evidence.json`.
- The static content under `field-rebuild-20261113/`.
- The outside published values (X fields).
- Handoff and policy documents; the `assembly/` code.

## F. Not determined

- Which two runs are "our two new workflow steps".
- Whether the combined-events top-10 group book came from ROOT itself or from a separate replay.
- The contents of `research-pins/*.xlsx` file by file.
- Whether the trade day Oct 18 flow, queue and replenishment sources came from the same ROOT build as the other three
  trade days.
- Anything on the stopped AWS boxes or in Desktop's own folders.

## G. Greg's answer on the two workflow steps (2026-11-16)

1. **The original trade day Oct 18 SQLite and Julia work**: confirmed by Greg. This is Desktop's family research,
   Markets `artifacts/sqlite-triage/20261022/families/` (its handoffs record 5,275,928 resolved observations and
   5,803,712 measurement rows read from ROOT and native contexts).
2. **"A replacement for the hundreds of trillions of calcs that were wrong with like 5+ million"**, described in a
   handoff from the week of Nov 8. **Not located yet.** Searched without a match for "trillion": this branch of
   markets-data, the Markets session branch, GitHub code search on both default branches, and the Oct 22 grouping
   session. Leads, unconfirmed:
   - The Nov 8 notes in Markets `research/kalshi/adaptive_wavepacket_20261108/` name the problem as an "ID/name-driven
     group count explosion" to be replaced, and say it was not yet connected at that time.
   - This folder's `README.md` records 5,075,640 timestamp-indexed research rows and 5,569,627 clock-indexed rows
     from the four-day workflow processing of Nov 9, which may be the "5+ million".
   Greg to confirm which run this is, or point to the handoff (it may be a Desktop handoff that is not in git, or on
   a branch that was not searched).

**Greg, later on 2026-11-16:** the second step is "probably" the four-day workflow processing of Nov 9, run by
Codex: the run families listed in section A (four-day extensions, family replication, combined events, whole
lifecycles, lifecycle data links, replay comparison; 448 files in `assembly/workflow_sources.json`), whose verified
companion batch is the 5,075,640 timestamp-indexed research rows recorded in this folder's `README.md`. Treat that
as the second workflow step unless the handoff describing the "hundreds of trillions" replacement turns up and says
otherwise. Both steps sit downstream of old ROOT outputs and are rerun on the new record.

**Greg, closing this out:** the older version with "hundreds of trillions" of calculations was scrapped completely
and the work restarted. There is nothing of it to find or retrieve; he mentioned it only as a pointer to the Nov 9
run. Do not search for it again.
