# markets-data

Current user instruction (2026-11-08): data, derived tables, renders, workbooks and provenance are published here. Code and findings belong in DavisAI1974/Markets. The local-only storage rule is removed. Preserve immutable artifact versions and hashes; no AWS/S3.

Completed native dipole snapshot: [figures, tables, workbook, caches and supplied images](tasks/family-research-20261022/native-dipole/20261108-33693e180/README.md). Every transferred file is hashed in its snapshot MANIFEST.json.

Pinned data inputs for DavisAI1974/Markets: Databento NG MBO UTC-day members, standalone group exports,
sealed touch-print decisions and the October 18 candidate inputs and ledgers. Every file is listed in MANIFEST.json
with its sha256; loaders verify on read (see Markets: tasks/family-research-20261022/claude-code/data_locator.py).
ROOT frame spools are not here. Legacy S3 targets in the original manifest are historical references, not an authorized transfer route or evidence of uploaded files.
No code lives here. No file is ever rewritten in place; a corrected file gets a new path and a new manifest entry.
