# Market data — start here

This repository is the single home for market data, tables, workbooks, renders, and provenance. Start here rather than a local E: folder or an old handoff. Application code remains in [DavisAI1974/Markets](https://github.com/DavisAI1974/Markets); data navigation belongs here.

## Current four-day analysis

Canonical research branch: `codex/research-union-four-days-20261109`. Completed analysis checkpoint: `27bad4ef402ade3c5f02a1d7e255d3790aed1888`.

- [Current Excel](https://github.com/DavisAI1974/markets-data/blob/codex/research-union-four-days-20261109/tasks/family-research-20261022/research-union-current/Frankie_four_day_research_current.xlsx)
- [Native-flow companion](https://github.com/DavisAI1974/markets-data/blob/codex/research-union-four-days-20261109/tasks/family-research-20261022/research-union-current/Priority_native_flow.xlsx)
- [New findings D09–D13](https://github.com/DavisAI1974/markets-data/blob/codex/research-union-four-days-20261109/tasks/family-research-20261022/research-union-current/reanalysis-20261109/REPORT.md)
- [Next-analysis pins](https://github.com/DavisAI1974/markets-data/blob/codex/research-union-four-days-20261109/tasks/family-research-20261022/research-union-current/reanalysis-20261109/PINNED_FINDINGS.json)
- [All 11 paper-strategy arms: JSON specification](https://github.com/DavisAI1974/markets-data/blob/codex/research-union-four-days-20261109/tasks/family-research-20261022/research-union-current/reanalysis-20261109/TRADE_RULES.json)
- [Continuation handoff and deferred reconciliation](https://github.com/DavisAI1974/markets-data/blob/codex/research-union-four-days-20261109/tasks/family-research-20261022/research-union-current/NEW_CHAT_HANDOFF.md)

Every defined strategy is included for platform paper testing. The JSON is a specification; no platform runner is connected and this work has recorded no platform paper fills. Old observation-only labels are superseded.

## E-drive consolidation — in progress

Requested November 9, 2026. The inventory found 64,571 non-dependency files, approximately 54.8 GB, across 18 Markets/research folders. These totals include duplicates and already-published files, not just missing research.

Bulk preservation archives are being uploaded to this repository's `market-data-consolidation-20261109` release. File manifests include original paths, byte sizes, and SHA-256 checksums. GitHub server digests verify uploaded archives. Preservation does not certify unfinished scientific work as complete.

Local deletion requires verified remote preservation. Migration is not complete. Credentials, machine configuration, and private agent histories are excluded from public publication and must not be silently deleted. Remaining exceptions will be recorded here.

## Continuing-work rules

1. Publish substantive data and results here and update this index or its linked manifests in the same session.
2. Preserve exact source identities, clocks, checksums, immutable references, adverse cases, and missing cases.
3. Distinguish current, historical, unfinished, and superseded artifacts. Do not restart completed workers.
4. Local storage is temporary workspace. Remove copies only after remote verification; never leave unique research only on E:.
5. Platform paper testing remains the proving ground. Do not replace it with a standalone historical backtest. Platform setup and scheduling remain deferred.
