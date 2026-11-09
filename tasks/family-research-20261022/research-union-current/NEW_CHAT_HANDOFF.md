# Continue after the discovery-focused reanalysis

Updated **2026-11-09T19:43:28.439837+00:00 UTC**. File/status clock, separate from market-event clocks.

## Latest instructions and completion

The user clarified that reanalysis must seek new discoveries from the depth of the data and new additions, not merely summarize/check known relationships. Finish the prior delivery first. This was done: priority-ten publication 1c234d511e26a0d1d054a39dbafc8a436232e7bb was remotely verified before starting this extension. Exhaustive branch reconciliation remains deferred for a day or two. Do not restart completed workers or read the other analyst's new report.

The discovery extension is complete for the selected priority populations, with explicit remaining interpretation gaps. All 628,672 original priority records remain accounted for, plus 38,736 already-existing original order-outcome rows used as later evaluation evidence. There are 3,176 exact candidate/time joins, 17,284 verified order-state prefixes, 137 family numeric fields screened across four dates, 10,643 retained group/target comparison rows and 215 source-linked illustrative cases covering all eight claims. Do not call this exhaustive interpretation of all historical sources or proof of a profitable strategy.

## Current deliverables and authority

- [Main Excel](Frankie_four_day_research_current.xlsx) opens with Discovery findings, Discovery evidence, Paper discovery update, comparisons and field coverage. 131,374 new summary cells were read back; 83 pre-existing worksheet payloads remain identical. Three derived reader views were explicitly corrected/annotated. All raw source-data sheets are unchanged.
- [Native flow companion](Priority_native_flow.xlsx) is unchanged.
- [Discovery report](discovery-depth-20261109/REPORT.md), [claims](discovery-depth-20261109/CLAIMS.csv), [cases](discovery-depth-20261109/CASES.csv), [coverage](discovery-depth-20261109/COVERAGE.csv), [open questions](discovery-depth-20261109/OPEN_QUESTIONS.md), [receipt](discovery-depth-20261109/RECEIPT.json).
- [Current paper readiness](discovery-depth-20261109/PAPER_READINESS.md) and [version 1.1 specification](discovery-depth-20261109/PAPER_STRATEGIES_v1_1.json) supersede the prior readiness classification. R1: execution check required; R2: observation-only. Both paper_enabled flags are false. No adapter connected and no trade submitted.

New findings distinguish one-lot replenishment from larger-order depletion, survival from later price direction, flow expiry from arrivals, missing recent flow from absent book/price information, and onset mechanism from the one-lot label. Cross-window flow agreement has a horizon-dependent association. Mechanically related fills/aggressor quantities are highly redundant, not independent confirmation.

**Correction:** prior P08 smaller-index ordering is superseded. Aggressor index a is interval (a,a+1]; quote index q is sampled boundary with transition in (q-1,q]. Corrected totals: 1,139 aggression intervals before quote intervals, 682 quote intervals before aggression intervals, 1,335 overlapping/unresolved and one censored. This is sampled-interval correspondence, not proof of native event order or a 0.5-second warning. Raw source values never changed. The main workbook's active Priority findings and Priority counts views are corrected; the preceding version remains only as historical provenance in Git and the prior-version directory.

The rule version was revised because all 76 one-lot filled survivors at +5ms had prefix-accounted replenishment, but improved survival did not establish consistent subsequent price advantage. R2 now logs signals only until a direct complete-rule execution test. Original v1 remains frozen for audit; risk limits were not optimized. Empty classified-flow windows are ordinary signal invalidation states, distinct from feed corruption.

Local discovery work: E:/Markets/outputs/research-union-20261109/discovery-depth. Source bytes and verified projections remain at the parent workroot. New scripts and complete comparison tables are published under discovery-depth-20261109. Six focused tests and independent Excel/loop recounts passed. See WORKBOOK_VERIFICATION.json and INDEPENDENT_CHECKS.json.

## Preserved constraints

Original research from CCode/Desktop/Codex is authorized. Do not read CCode's new reanalysis under agent-pass/reanalysis/claude or its new report. Preserve contrary, flat, missing and adverse cases. Keep exact ns as text; scheduled time is separate from observed known-by time. Do not admit archived 193k dipole-stage data as newly verified calculations. Do not overwrite corrected sources S00092/S00096/S00101/S00105 with older copies. The exact identities of the earlier two workflows remain unresolved. No AWS, new remote compute, live trading, merge, deployment or messages to others. Data destination remains DavisAI1974/markets-data on codex/research-union-four-days-20261109. Preserve unrelated dirty files in E:/Markets.

## Durable deferred work — inspect before launching anything

Local workroot: E:/Markets/outputs/research-union-20261109. Isolated publication checkout: git-publication. Current priority work: priority-now. Original sources are Git-blob-hash-verified in objects/; active_sources.json, workflow_sources.json and expanded_sources.json preserve source inventories.

All workers observed in this turn finished; check actual processes and logs before resuming later:

- Original/base/trade-layer companion verification completed: 108 files, 10,788,537 rows including 143,270 trade-layer rows. Earlier extra export completed 5,569,627 rows across 68 books. Those deferred bulk files are not newly published in this priority commit.
- Workflow processing completed 18,168,382 retained rows: 17,665,501 clock pins plus 502,881 attachments. workflow_source_catalog.json and workflow_coverage.json are durable. workflow-progress.log.
- Only workflow Oct2 Excel export was started: 4,340,150 rows in 255 books completed (workflow-excel-20231002.log). Verify full payloads before publishing; do not rerun its completed export. Other dates remain unexported.
- Remaining-source resume completed: Oct2 798,156; Oct3 867,816; Oct17 824,841; Oct18 583,688; crossday10. remaining_source_catalog.json; remaining-resume.log. Resume fix commits source boundaries before checkpoints; CSV large fields supported.
- Source-sample reconciliation completed all 34,825,917 original records. 28,423,631 parent-bound records; 25,000,795 newly parent-bound; 6,402,286 still unbound, including 5,848,259 without sample_id and 554,027 without established source lineage. Counts overlap with original-clock coverage, so do not sum them. current/sample_reconciliation.json and current/sample-packets/ are durable; sample-reconciliation.log. Do not rerun. Parent joins require verified lineage and matching family/phase/instrument; never promote arbitrary sample_id alone to time.

## Next session

If continuing paper setup, use discovery readiness version 1.1: R1 requires execution checks and R2 is observation-only. Both paper_enabled flags are false. Configure the actual adapter; do not silently change thresholds. If resuming reconciliation, inventory live workers first, inspect completed manifests and checkpoints, verify Oct2 workflow Excel, then complete other dates and unbound-source disposition. Publish only explicitly verified artifacts. Do not use the older bulk publisher blindly; it has a different scope. The next untouched paper session supplies the first prospective evidence for these rule combinations.

The pre-priority handoff remains in Git history at ef5466792f6eecc0fe32879e42bacc450cf4e75b. That older running-worker status is superseded here.
