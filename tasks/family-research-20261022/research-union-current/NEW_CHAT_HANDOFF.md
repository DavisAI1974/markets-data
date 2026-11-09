# Reanalysis complete; finish analysis before platform work

Updated 2026-11-09T20:45:23.577442+00:00. This is a file/status clock, not a market-event clock.

## Latest user instructions

Finish the Excel reanalysis first. New discoveries must be pinned for the next analysis. Every defined strategy goes into platform paper trading; weak or conflicting historical evidence does not create an observation-only category. The platform must execute and record the paper trades automatically. The user cannot respond in milliseconds. Delayed or older playback data is acceptable. Do not substitute our own standalone historical strategy backtest for those platform paper trades. Session scheduling and platform setup are deferred. Henry Hub NG, December contract (upcoming December 2026 assumed), Tradovate demo was selected; NinjaTrader and CME options were researched, but no platform was installed, connected or activated. No orders were submitted.

## Completed analysis and current artifacts

- [Current Excel](Frankie_four_day_research_current.xlsx): 89,473,585 bytes; SHA256 `70b57f3d4843997b970d8a78df1fb1d3ce8a897c0ac318a21d62e242f49d6be4`. Opens with Reanalysis findings, Paper hypotheses, Reanalysis comparisons and Reanalysis cases. 13,326 new result cells read back; 88 pre-existing worksheet payloads are byte-identical. Raw source data unchanged. Three derived reader views were updated to remove stale observation-only policy and clarify the flow definition.
- [Pinned report](reanalysis-20261109/REPORT.md) and [next-analysis pins](reanalysis-20261109/PINNED_FINDINGS.json): five new findings D09-D13 extend D01-D08. 127,274 source cells directly rechecked; 3,176 information-operator contexts reproduced; 3,215 family rows retained; 864 comparison rows and 41 source-linked cases. Five focused calculation tests and independent confirmation recount pass.
- [Machine rule specification](reanalysis-20261109/TRADE_RULES.json): structured conditions/parameters and frozen coefficients only, with all 11 arms included. This is a custom schema, NOT a native Tradovate/NinjaTrader import or a running strategy. Platform implementation/verification remains work for later. R2's impossible stay-at-best-plus-price-move condition is corrected: at touch when armed, then original support may remain behind the improved best.
- [Native flow companion](Priority_native_flow.xlsx) is unchanged. All prior priority populations and historical discovery comparisons remain available.

D09: native/proxy quantities agree in 3,159/3,176 five-second windows; nonzero signs agree in 777/778. D10: 965/1,818 defined windows have activity in at most two bins; 631 zero-MI windows also have very large logged C. D11: adding the tested information features worsens MAE on all three later-date evaluations. D12: the already-consumed confirmation move changes remaining opportunity; touch-confirmed 20s remaining means are negative on three dates. D13: cancellation/flow agreement is not uniformly superior. These are conditional research findings, not platform paper-trade results or claimed net profitability.

## Next analysis

Use the pinned report, cases and complete comparison tables before generating new hypotheses. Preserve adverse, flat, missing, failed-confirmation and no-fill cases. Separate survival, subsequent price, executable fills, costs and net PnL. All four dates are already studied discovery data. Keep native and midpoint-classified flow distinct, and native cancellations separate from aggregate size changes. Do not repeat completed analysis merely to obtain more positive results.

When the user resumes paper execution, test all defined arms in actual platform paper accounts; replay may supply the data. Read current platform documentation and verify required inputs. NinjaTrader supports automated strategies and local Sim101 accounts; its documented OnMarketDepth interface lacks exchange resting-order IDs, while CME MBO includes them. CME's free practice simulator uses 10-minute delayed data; no documented custom JSON strategy loader was found. Tradovate API requirements are $1,000 funded account balance plus $25/month API add-on, with API market data separate. No purchases or account changes are authorized by this handoff.

## Preserved constraints

Do not restart completed workers. Do not read the other analyst's new reanalysis under agent-pass/reanalysis/claude or its new report. Preserve source clocks as exact integers/text, keep scheduled and known-by times distinct, and retain all contrary cases. No AWS, new remote compute, live trading, merge, deployment or messages to others. Root E:/Markets contains unrelated dirty work; use the isolated publication checkout. The frozen source-data and original discovery workbook remain in their earlier directories and Git commits. Broader reconciliation remains deferred.

## Durable deferred work — inspect before launching anything

Local workroot: E:/Markets/outputs/research-union-20261109. Isolated publication checkout: git-publication. Current priority work: priority-now. Original sources are Git-blob-hash-verified in objects/; active_sources.json, workflow_sources.json and expanded_sources.json preserve source inventories.

All workers observed in this turn finished; check actual processes and logs before resuming later:

- Original/base/trade-layer companion verification completed: 108 files, 10,788,537 rows including 143,270 trade-layer rows. Earlier extra export completed 5,569,627 rows across 68 books. Those deferred bulk files are not newly published in this priority commit.
- Workflow processing completed 18,168,382 retained rows: 17,665,501 clock pins plus 502,881 attachments. workflow_source_catalog.json and workflow_coverage.json are durable. workflow-progress.log.
- Only workflow Oct2 Excel export was started: 4,340,150 rows in 255 books completed (workflow-excel-20231002.log). Verify full payloads before publishing; do not rerun its completed export. Other dates remain unexported.
- Remaining-source resume completed: Oct2 798,156; Oct3 867,816; Oct17 824,841; Oct18 583,688; crossday10. remaining_source_catalog.json; remaining-resume.log. Resume fix commits source boundaries before checkpoints; CSV large fields supported.
- Source-sample reconciliation completed all 34,825,917 original records. 28,423,631 parent-bound records; 25,000,795 newly parent-bound; 6,402,286 still unbound, including 5,848,259 without sample_id and 554,027 without established source lineage. Counts overlap with original-clock coverage, so do not sum them. current/sample_reconciliation.json and current/sample-packets/ are durable; sample-reconciliation.log. Do not rerun. Parent joins require verified lineage and matching family/phase/instrument; never promote arbitrary sample_id alone to time.



## Local work

Workroot E:/Markets/outputs/research-union-20261109. Final analysis in reanalysis_followup; current workbook in current. Earlier discovery in discovery-depth, original projections in priority-now, verified blobs in objects. Four existing raw parquet inputs were downloaded and Git-blob verified while exploring historical tests, but no historical trading simulation was implemented or run. Do not restart that task unless requested. The interrupted R2 unit-test draft is preserved outside the publication tree in paper-setup-paused and is not passing/implemented code.
