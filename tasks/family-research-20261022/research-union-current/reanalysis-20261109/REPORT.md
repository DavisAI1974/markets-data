# Reanalysis pinned for the next pass

The user’s instruction governs this report: every defined strategy goes into paper testing. Historical results explain the hypothesis and its weaknesses; they do not determine eligibility. Session scheduling and Tradovate integration are deferred. The intended instrument is standard Henry Hub NG, December 2026 (assumed upcoming December), on Tradovate demo. No trades were submitted.

This pass extends, rather than replaces, the eight earlier findings. It directly re-read 107,984 relevant cells from the current Excel, reproduced the information operator for all 3,176 recognition contexts, and compared all 3,215 retained family rows. All four October 2023 dates have already been used in discovery. The later-date model tests below use earlier dates for training, but are not untouched validation.

An additional 19,290 family-sheet cells were independently checked, bringing this pass to 127,274 directly checked source cells. The one-second confirmation result was separately recounted. Five focused calculation tests passed. These checks validate the analysis; they are not paper trades.

The next strategy evaluation must use automated trades in a platform paper account with platform-recorded fills and P&L. Delayed or older playback data is acceptable to the user. Standalone historical strategy backtests and platform setup are deferred until this analysis is delivered. No historical trading simulation was run in this pass; the additional raw inputs retrieved while exploring that route are preserved and unused.

TRADE_RULES.json contains only structured rules, parameters and frozen model coefficients. It is our custom configuration format, not a native Tradovate or NinjaTrader import. A compatible platform strategy/runner still has to implement and verify it. All 11 arms are included; the JSON is not evidence that they have run or that a platform accepts the file directly.

## D09 — Different flow definitions mostly agree in this cohort

P10’s original producer assigns each print by its price relative to the preceding complete-group midpoint. P01 retains native exchange-side classification. They are distinct measurements and must retain their names and provenance.

At identical recognition cutoffs, the 5-second buy/sell quantities match exactly in **3,159/3,176 contexts (99.46%)**. Of the 778 contexts where both measures give a nonzero direction, **777 agree and one disagrees**. At 20 seconds there is also one opposite-sign context. This source-definition distinction is real, but does not broadly overturn the earlier quiet-flow finding in this cohort: the proxy has 2,367 empty 5-second windows; native classification has 2,366.

Every compared native 5/20-second window has completion known-by times no later than the recognition decision. That was checked using integer nanoseconds, not inferred from calendar bin labels. The exact opposite-sign 5-second example is Oct 2 candidate `dip-19632-1696235372`, Excel row 327 in both P09 and P10: proxy imbalance −0.6667, native imbalance +0.1667. Native source rows are pinned in Reanalysis cases.

**Implication:** keep native and midpoint-classified paper variants identifiable. Their near-agreement is cohort-specific evidence, not permission to mix definitions globally.

## D10 — Large information ratios often describe sparse activity

The operator is defined in 1,818 of 3,176 contexts. Of those defined windows, **965 (53.1%) have activity in at most two of the twenty one-second bins**. In **631 (34.7%)**, estimated mutual information is zero; all 631 also have an absolute logged C ratio above 15 and nearly extreme entropy asymmetry. The remaining 1,358 contexts have no classified flow in the 20-second window and remain undefined.

The pinned operator defines C as signed mean marginal entropy divided by mutual information plus 1e−9. Consequently, a large C can arise from a near-zero denominator. It is not automatically strong directional conviction, hidden liquidity, or evidence of market influence. Zero MI here is an estimate from sparse binned observations, not proof of independence. The early-versus-late MI change is zero in 760 defined contexts.

**Implication:** paper-test the information features, while logging activity-bin counts, MI and the denominator condition. Keep both information-enhanced and simpler comparator rules.

## D11 — Information features do not yet show consistent incremental forecasting value

A fixed ridge model (penalty 10, no tuning) used price context, touch quantities/order counts and raw early/late/fresh flow quantities. We then added entropy asymmetry, MI change, logged C and imbalance change. Each later date was predicted using strictly earlier dates for fitting, imputation and scaling. Every available outcome remained in the test population.

| Test date | Baseline MAE, ticks | With information MAE, ticks | Test rows |
|---|---:|---:|---:|
| Oct 3 | 0.6817 | 0.7042 | 832 |
| Oct 17 | 0.8102 | 0.8188 | 740 |
| Oct 18 | 0.8408 | 0.8425 | 862 |

Mean absolute error worsened on all three dates and in all three 60-second-separated subsets. Squared error improved slightly on Oct 18, and directional summaries are mixed; all results are retained. Adding display-change features is also inconsistent. This tests one declared linear model and feature set, not whether all information-theoretic or nonlinear models are useless.

**Implication:** test the baseline and information-enhanced versions side by side in paper. No feature earns extra confidence merely because its definition is more elaborate.

## D12 — Confirmation can consume the apparent advantage

Take the touch-imbalance direction at recognition, wait one second, and select cases whose midpoint has moved at least one tick in that direction. The table separates movement from recognition from the movement remaining **after** confirmation, both ending at recognition +20 seconds.

| Date | Confirmed cases | From recognition, ticks | Remaining after confirmation, ticks |
|---|---:|---:|---:|
| Oct 2 | 39 | +0.974 | −0.449 |
| Oct 3 | 39 | +1.962 | +0.474 |
| Oct 17 | 30 | +1.067 | −0.033 |
| Oct 18 | 54 | +0.852 | −0.519 |

The apparent advantage reverses on three dates once the already-consumed move is removed. At five-second confirmation, the 60-second-separated subset likewise has negative remaining 20-second movement on three dates. Results at 60 seconds are mixed. Native-flow confirmation has very small separated samples: 2–7 cases/day at one second, so it cannot support a stable conclusion.

This is a delayed midpoint diagnostic, not the exact R1/R2 sequence, a bid/ask fill, or net PnL. All opposite, flat, subtick and unavailable states are retained. The one-second value is used only at the later decision; using it to select an entry at recognition would be look-ahead.

**Implication:** paper-test immediate, delayed-follow and delayed-fade versions separately. Measure actual entry prices and subsequent moves; never credit the confirmation move to the later entry.

## D13 — More book confirmation is not uniformly better

P02 distinguishes native touch additions and cancellation-derived removals. Define cancellation support as ask cancellations minus bid cancellations. Comparing subsequent movement in the **flow direction**, its agreement with 5-second flow improves the 20-second mean on three dates, but not Oct 17:

| Date | Cancellation support agrees with flow | Cancellation support opposes flow |
|---|---:|---:|
| Oct 2 | +0.432 (n=338) | −0.058 (n=231) |
| Oct 3 | +0.119 (n=306) | +0.071 (n=274) |
| Oct 17 | +0.124 (n=384) | +0.311 (n=235) |
| Oct 18 | +0.624 (n=287) | +0.397 (n=195) |

Addition agreement and net add/cancel agreement also fail to dominate on all dates. In contrast, P10’s display additions/removals are derived from changes in same-price aggregate sizes; those fields do not uniquely identify order cancellations, executions or individual additions. The two representations must not be treated as equivalent mechanisms.

These are family-conditioned comparisons using the retained pre-start reference and source event selection. They do not establish executable incremental returns. Neutral, missing and zero-direction populations remain in the comparison table; a missing directional outcome is not a flat return.

**Implication:** include aligned and opposed book/flow paper arms, and compare them on identical horizons. Do not require every apparent confirmation to agree before allowing a strategy to be tested.

## Rule correction retained for paper implementation

The original R2 wording required the same unre-priced support order to remain at the best quote while both quotes moved one tick away in the support direction. Those conditions cannot hold together. The corrected hypothesis requires the order to be at touch when its linked fill arms the signal, then remain displayed at its original price as price moves away. It can be behind the new best quote. Removal, cancellation/reprice and zero residual still invalidate the tracked support. This is a logical correction, not an empirically fitted improvement, and the exact corrected sequence is still to be implemented and tested.

## What is pinned for the next analysis

- Keep all thirteen findings and contrary evidence. Distinguish order survival, price movement, executed trade results and net results.
- Reproduce the 631 zero-MI/large-C windows and test activity-aware normalization without using future prices to choose thresholds.
- Track remaining movement after actual paper entry. Compare immediate, follow and fade arms; retain no-fill and failed-confirmation cases.
- Preserve native-versus-proxy flow provenance, exact decision/known-by clocks, and native-versus-aggregate book-change definitions.
- Test every defined paper hypothesis listed in PAPER_HYPOTHESES.json. No observation-only category based on weak historical evidence. Unspecified future variants need explicit rules; future labels remain outcomes, never entry inputs.
- Next evaluation should report each rule, side, day and market state, including spread, fee, latency and loss-limit effects. Do not call these already-used four dates out-of-sample proof.
- Broader branch reconciliation, whole-parent ancestry/lifespan and static/external-information layers remain deferred. Existing completed workers must not be restarted.

The evidence tables, source-linked cases, test results and workbook receipt accompany this report. The workbook’s earlier observation-only recommendations are superseded by the user’s all-paper instruction.
