# markets-data

Pinned data inputs for DavisAI1974/Markets: Databento NG MBO UTC-day members, standalone group exports,
sealed touch-print decisions and the October 18 candidate inputs and ledgers. Every file is listed in MANIFEST.json
with its sha256; loaders verify on read (see Markets: tasks/family-research-20261022/claude-code/data_locator.py).
ROOT frame spools are not here; MANIFEST.json lists them with their S3 targets and part hashes.
No code lives here. No file is ever rewritten in place; a corrected file gets a new path and a new manifest entry.
