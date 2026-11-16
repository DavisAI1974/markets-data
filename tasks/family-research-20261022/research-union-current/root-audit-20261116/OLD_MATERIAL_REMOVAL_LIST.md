# Old material in this research folder: what it is, how it was made, why it existed (2026-11-16)

Greg, 2026-11-16: "As long as we know how and why the old stuff exists we have the important part."

This is that record, and it is the list of what is removed from the research folder when Greg says "delete". **Nothing
has been removed yet.** It records what each thing is and where it came from. It records no result, number or finding.

Every item is on branch `ccr-349e2ffe-07p8od` up to and including the commit that adds this file, so it can be found
again there. Copies also sit on three older branches of markets-data (`codex/research-union-four-days-20261109`,
`codex/evidence-availability-20261113`, `codex/fifteen-strategy-synthesis-20261113`). The `main` branch does not hold
them. Detail behind the "how" column: `OLD_ROOT_LINEAGE.md` (sections B, C and D). What each research project set out
to find: `RESEARCH_INTENTIONS.md`.

"Basis" says how sure the "how it was made" is: **read** (stated in the folder's own files), **lineage** (traced in
`OLD_ROOT_LINEAGE.md`), or **inferred** (the lineage could only infer it).

## Group 1: the old workbooks

| Path | What it is | How it was made | Why it existed | Basis |
|---|---|---|---|---|
| `Frankie_four_day_research_current.xlsx` | The four-day research workbook: every saved trade of the four trade days with the 141 fields, plus review sheets. | Assembled by the `assembly/` scripts from the old trade archives, the old ROOT outputs, the old per-trade book archive and the outside data. Trades only, cut on the wrong clock (two trade days missing their first two hours). | To have every trade and every field in one place for review and for Frankie. | read (README.md) and lineage |
| `trade-layers/` (17 workbooks) | All 143,270 saved trades with their 141 fields, split by trade day. | The joined-inputs grid of 141 fields (`four_day_pins/assemble.py`), exported to Excel. | The full per-trade copy behind the workbook above. | read and lineage |
| `research-pins/` (23 workbooks) | 5,075,640 research rows indexed by timestamp, split by trade day. | Codex's four-day workflow processing of 2026-11-09, exported to Excel. Not determined file by file which old output each row rests on. | To pin the research tables to their clocks beside the trades. | read (README.md); contents not determined file by file |
| `Priority_native_flow.xlsx` | The priority flow workbook. | From the old whole-lifecycles per-second flow table. | The first of the ten priority evidence tables. | inferred |
| `field-rebuild-20261113/Claude-Eight-Trade-Types-Original.xlsx` | The eight-trade review workbook as first made. | An earlier selection of eight trades with the same 141 fields. | The first small sheet whose empty cells started this work. | inferred |

The 2021 Step 1 fields (L080, L083 to L089) and the 2021 objects (L024, L026) are **empty** in these workbooks
(`OLD_ROOT_LINEAGE.md`, section C), and the static-values file holds nothing for them. So no Step 1 value is lost when
the workbooks go; Greg's "don't wipe Step 1" is not touched by this list.

## Group 2: old calculated outputs

| Path | What it is | How it was made | Why it existed | Basis |
|---|---|---|---|---|
| `field-rebuild-20261113/` except the files kept below | Records, joins, flow inputs, book shard lists and the repair programs for refilling workbook fields. | From old ROOT sections, the old lifecycle ledgers and the old per-trade book archive. | To fill empty workbook cells from the old outputs. | lineage |
| `oct18-native-recovery-20261115/` | Per-trade "native" patches for trade day Oct 18. | Copied from the old ROOT native outputs. | To fill the trade day Oct 18 fields. | lineage |
| `case-case-*.csv` (10 files), `ccode_render_review.csv`, `case_table_inventory.json` | Tables behind the ten case pictures. | From old dipole candidates, episodes, per-second flow and the 20-second roll. | To let the case pictures be checked against tables. | lineage for two files, inferred for the rest |
| `dipole_trade_gaps.csv`, `dipole_gap_summary.json`, `dipole_map_source_verification.json`, `corrected_price_response.json` | Dipole map gap lists and the corrected price-response examples. | From old dipole candidates, episodes and lifecycles. | To list what the dipole map was missing per trade. | lineage |
| `evidence/` (4 files) | Saved evidence rows. | From the old dipole and lifecycle outputs. | Supporting rows for the case review. | inferred |

## Group 3: old research results (Claude and Codex)

What each set out to find, and the angle it took, is kept in `RESEARCH_INTENTIONS.md`. The results go.

| Path | Rests on | Basis |
|---|---|---|
| `priority-ten-20261109/` | old per-second flow and the 20-second roll | lineage |
| `discovery-depth-20261109/` | the same | lineage |
| `reanalysis-20261109/` | the same | lineage |
| `fifteen-strategies-20261113/` | the three above | lineage |
| `paper-validation-20261109/` | the three above; its tests used made-up inputs | inferred |
| `evidence-availability-20261113/` | a mix: audits of the 141 fields and of the old tick selections | lineage |
| `s-field-test-20261116/` | the old per-trade book archive and the old S-field code | lineage |

## Group 4: the tools and lists that would rebuild or point at the old workbooks

These were not on the list first shown to Greg. They are how old material would creep back, so they are listed here
for his word with the rest.

| Path | What it is |
|---|---|
| `assembly/` (40 files) | The programs that fetched the old sources and built, merged and published the old workbooks. |
| `CHECKPOINT_MANIFEST.json`, `FILE_CLOCKS_AND_STATUS.json`, `PAPER_CURRENT.json`, `workbook_population.json`, `companion_verification.json`, `publication_verification.json`, `latest_publication.json`, `published_source_catalog.json`, `price_clock_verification.json`, `horizon_clock_corrections.json`, `extra_pin_session_audit.json`, `latest_screenshot_source.json`, `screenshot_source_map.csv`, `nineteen_field_reuse.csv`, `research_gap_queue.csv` | File lists, fingerprints and checks of the old workbooks and their sources. |
| `README.md`, `NEW_CHAT_HANDOFF.md`, `NEW_CHAT_HANDOFF.json`, `CCODE_GAP_FILLER_HANDOFF.md` | The old description of the folder and the old handoffs that tell a new session to continue the old workbook. |
| `root-redesign-20261116/tools/add_readme_page.py`, `page_four_day.txt`, `page_priority.txt` | The tool and wording that added a "READ ME FIRST" page to the two old workbooks. |

## Kept

- `data/nymex_mbo/ng_v0_oct2023/` (the raw order tape) and `data/outside/ng_oct2023/` (the outside source files).
- `root-redesign-20261116/` (decisions, specifications, README page wording, the workbook frame and its tool).
- `root-audit-20261116/` (the audit lists, this file).
- `resting-order-age-20261116/`, `historical-shape-attachments/`, `historical_shape_sources.json`,
  `dipole_dive_chat_evidence.json`: they do not rest on old inputs.
- From `field-rebuild-20261113/`: `LAYER_REGISTRY.json` (the names of the 141 fields, which the workbook frame tool
  reads), `STATIC_FIELD_VALUES.json`, `STATIC_CONTENT_MANIFEST.json` and `static_content/` (the reference documents
  behind fields L001 to L026, L081, L082; not old ROOT output).
- `ACTION_PLAN_20261116.md` and the `NEXT_SESSION_HANDOFF_*` files.

- **Step 1.** The Step 1 columns of the workbook, the 2021 family definitions and the Step 1 programs in the Markets
  repository all stay (Greg: "That stays ... It just gets built on top of"). Nothing on this list holds a Step 1 value.

## Not removed with this list

- `trade-day-rebuild-20261116/` and the four `trade-day-book-*` branches: yesterday's stand-in replay and book
  pictures. They go in the same change that brings in the new tape and book, once those pass their checks.
- Old ROOT code in the Markets repository: `OLD_ROOT_FILE_LIST.md`. It goes when its replacement lands, and needs
  Greg's permission for Markets branches other than the session's.
- Out of reach of a cloud session: the two workbook release files on GitHub, the old archive branches
  (`codex/frankie-book-recovery-*`, `codex/frankie-lifecycle-recovery-*`) and the three older branches named at the top,
  the stopped AWS boxes, Desktop's own folders.
