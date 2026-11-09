# November 9 market-data consolidation

Start from [the central index](../../MARKET_DATA_INDEX.md). This directory records preservation and cleanup, not a new scientific analysis.

## Research-union workroot

[MANIFEST.json](MANIFEST.json) preserves all 2,437 substantive files from the former `E:/Markets/outputs/research-union-20261109` working tree, excluding its Git checkout, original-source blob cache, and regenerable Python bytecode. The original files total 16,505,143,923 bytes. They are stored in 28 ZIP archives totaling 7,947,799,272 bytes attached to [the repository release](https://github.com/DavisAI1974/markets-data/releases/tag/market-data-consolidation-20261109).

Each manifest file entry identifies its original relative path, byte length, SHA-256, and containing archive. Archive entries contain the download URL, byte length, and SHA-256. Some uploads may still be in progress: [REMOTE_VERIFICATION_COMBINED.json](REMOTE_VERIFICATION_COMBINED.json) lists the uploads whose GitHub server digest has been verified. Only those archives qualify for local cleanup.

[ARCHIVE_CONTENT_VERIFICATION.json](ARCHIVE_CONTENT_VERIFICATION.json) records a complete restore check: every member was decompressed and its hash and byte length matched the original file manifest. This is byte-preservation verification, not a claim that every deferred workbook or draft is scientifically complete.

## Finding or restoring a file

1. Find its original relative path in `MANIFEST.json`.
2. Download the named ZIP from the release and compare its SHA-256 with the manifest.
3. Extract the named member and compare its SHA-256 and length with the file entry.
4. Treat the restored copy as temporary work; publish substantive changes and update the central index before cleanup.

The archives preserve historical versions, current analysis, deferred bulk reconciliation, and interrupted drafts. Use the central index's current workbook and pinned findings for ongoing interpretation. Do not execute an old draft merely because it was archived. All defined strategy arms remain included for platform paper trading; preservation does not activate a platform runner.

## Wider inventory

The inventory covers 18 Markets/research directories. Older working-tree copies, original remote blobs, unpublished files, and excluded credentials are being reconciled into a separate catalog. Do not assume that preservation of the research-union workroot means every folder on E: has been removed. Deletion receipts and outstanding exceptions will be linked here as reconciliation completes.
