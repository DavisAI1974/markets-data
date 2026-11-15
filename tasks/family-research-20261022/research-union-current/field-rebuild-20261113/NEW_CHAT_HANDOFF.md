# Resume the Markets pre-run field recovery

## GitHub is the source of truth

Repository: DavisAI1974/markets-data
Branch: codex/evidence-availability-20261113
Task root: tasks/family-research-20261022/research-union-current/
Latest workbook release: https://github.com/DavisAI1974/markets-data/releases/tag/eight-trade-types-repair-20261115-r2
Workbook SHA256: 49dd87cc80b5bea8b0d7d6ab320c63f70432ea705f554807f5a3948f2dce8257
Workbook size: 500,539,823 bytes.
Read oct18-native-recovery-20261115/WORKBOOK_R2_PUBLICATION.json for the verified asset and publication receipt. Read field-rebuild-20261113/REMAINING_35_FIELD_STATUS.json and REMAINING_FIELDS.md for current field definitions and dependencies.

## User requirements

- Persist all NEW task code, data, results and workbooks directly to GitHub. No new task files, caches, clones, temporary data or workbook copies on C:, E: or other local drives. Process in memory. Existing files may be read.
- AWS is unavailable; do not try AWS.
- Never invent unavailable data. Leave actual values blank/null, with explicit availability status. Do not substitute unrelated outputs, zero vectors, guessed identities or missing discoveries as negative outcomes.
- Frankie has NOT run on these days. His outputs are expected to be unavailable; classify them as awaiting execution. Do not run Frankie merely to fill the workbook.
- Preserve all original ticks, hypotheses, eight types and four dates. The original full population is 143,270 trades; selected workbook population is 5,513 ticks across 32 cases.
- Preserve all existing S values and missing states. Never restart stopped S calculations.
- No new arbitrary 5/60-second horizons. Existing archived horizon definitions are provenance only.
- Do not consult Claude's new independent results or branch.
- User requested committing/saving this work and then moving to a new chat.

## Completed and verified

1. Prior six-field recovery: 33,078 cells across L025, L064, L065, L090, L093 and L099. L025 is exact metadata; the other five have explicitly limited source coverage.
2. Oct18 recovery commit: 87e5931b4927963f4b877c75956d1550f3c7d4ac.
   - Recovered 7,893 terminal queue records and 18,752 replenishment outcome records from old pinned GitHub archives.
   - Joined all 30,739 Oct18 trades by integer receive time AND cursor. Retained every eligible same-clock tie.
   - 41 trades have no eligible replenishment outcome and remain null.
   - Published 31 all-trade patch shards, complete source dictionaries, verification report and recovery code in oct18-native-recovery-20261115/.
3. Corrected field availability commit: ed9d3989bb8abadd348368ac2d1be60c7417abba.
4. Workbook R2 adds 2,894 supported L050/L051 cells across all 1,447 selected Oct18 ticks. These are original observed outcomes, not claims of complete active-state semantics.
   - 91 additional lossless payload chunks; all 128,082 earlier chunks preserved.
   - Every changed data cell and added chunk verified after ZIP/XML readback.
   - All unaffected cells byte-identical; 77 unaffected ZIP parts checked.
   - S values, formulas, layout, other days and all original selected ticks preserved.
   - GitHub asset downloaded through RAM and SHA256/length verified before publication receipt.
   - No task files written to local drives.
   - Native Excel and visual rendering were not checked; the bundled artifact editor previously failed with out-of-memory. The established OOXML fallback was used.
5. Source history is pinned before the independent Claude work: DavisAI1974/Markets at 3d0b06aa29781d5e39cc3eb45c6d09e174f195a2. The original population manifest is pinned in markets-data at fd72c6054947851581f55f2b2fd1ac6cdd869a7f.

## What remains

The 35-field inventory is NOT complete:
- 1 exact metadata field: L025.
- 5 fields with scoped content: L064, L065, L090, L093, L099. Model-run components of the last three await Frankie.
- 10 fields awaiting Frankie: L077-L079, L091-L092, L094-L098.
- 19 unresolved pre-run fields: L024, L026, L060-L063, L067-L071, L080, L083-L089.

The pre-run gaps need exact 2021 DBN/bootstrap evidence, binding D-family and predecessor/ancestry/risk-set outputs, and the original Step-1 ground-truth/population/crosswalk/label/reconciliation package. Pinned GitHub tree searches found protocols and source identities but did not locate the required produced packages. Preserve empty values until actual matching evidence is available.
The full 143,270-trade rebuild remains unfinished. The Oct18 patch covers its 30,739 trades; do not claim it completes all four days/all fields.

Do not confuse C15 D1-D6 with the binding scientific D-family geometry. Do not use selected-case native candidates as Step-1 membership or true target onset. Historical regression forecasts are not Frankie's reasoning/probability movie. Candidate recognition is not a first model lock.

## Storage and tooling continuity

Earlier cleanup removed 60 generated recovery/cache files (1,524,499,772 bytes) from the pre-existing E: publication worktree only after GitHub verification. Original archives, parent Markets checkout and Git history were preserved.
The old isolated worktree E:/Markets/outputs/codex-evidence-availability-publication intentionally contains deleted generated files. Do NOT commit those cleanup deletions, pull files back onto E:, or run disk-writing repair/cache scripts.
Current changes were committed directly via GitHub's Git API, so they are already remote; a local git push is unnecessary.
GitHub connector reads work. Connector writes previously returned 403; authenticated gh api was used for remote commits/releases, passing bodies through stdin. Networked memory-only Python commands required sandbox approval. Never print tokens.
Use the verified GitHub files as the next chat's starting point. The user is ready for a fresh chat; do not restart completed recovery or manufacture the outstanding data.
