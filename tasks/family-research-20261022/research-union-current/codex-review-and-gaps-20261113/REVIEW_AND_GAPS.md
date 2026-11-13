# Codex strategy review and research gaps

November 13, 2026. This record preserves the review and gap discussion from the current session. It is outside Claude's independent evidence package. Claude should not read this document during the independent exercise.

## User direction

The fifteen saved candidates are a starting set, not a ceiling or the full historical research universe. Preserve all earlier hypotheses and all future additions, including overlapping, opposite, weakly supported, and unresolved ideas. There is no single-winner objective, strategy-set comparison, selection, or elimination exercise. Record evidence strength and missing inputs without removing hypotheses from the research program.

Claude's parallel work must be completely independent of Codex's strategies, findings, suggested additions, and gap answers. His research is additive. The independent handoff supplies neutral questions and source observations, not this review or our candidate list. Use a fresh Claude session and preserve any exposure disclosure.

All substantive data and results belong in DavisAI1974/markets-data. Local folders are migration sources or temporary Git staging, not authoritative delivery. Commit, push, verify, and return repository links in the same session.

## Saved specification and verification

The existing fifteen-candidate package is pinned at commit `fe45d2eff9b389e00c80807b6e2240003ba4885d`:

- [Complete specification](https://github.com/DavisAI1974/markets-data/blob/fe45d2eff9b389e00c80807b6e2240003ba4885d/tasks/family-research-20261022/research-union-current/fifteen-strategies-20261113/STRATEGIES_15.json)
- [Original five](https://github.com/DavisAI1974/markets-data/blob/fe45d2eff9b389e00c80807b6e2240003ba4885d/tasks/family-research-20261022/research-union-current/fifteen-strategies-20261113/ORIGINAL_FIVE.json)
- [Saved verification](https://github.com/DavisAI1974/markets-data/blob/fe45d2eff9b389e00c80807b6e2240003ba4885d/tasks/family-research-20261022/research-union-current/fifteen-strategies-20261113/VERIFICATION.json)

The review checked the saved file hashes, fifteen unique included candidates, mappings to the eleven recovered encoded legacy arms, and the selected-case package's 32 files, 5,513 tick appearances, 141 original fields and 167 total columns. These are integrity checks, not strategy-performance validation. No new strategy runner or platform paper execution was started. Prior connectivity probes and historical replay diagnostics are separate activities.

## Five strengthened candidates

Potential fits below are conditions to test, not demonstrated net profitability of these complete rules.

| Candidate | Evidence and potential fit | Failure possibilities and trade-management use |
| --- | --- | --- |
| C1 Ask-side thinning continuation long | Ask full size and order count declined in all four selected large-up-lasting legs. Requires fresh buying, positive defined 5s/60s flow and later upward quote confirmation; bid buildup stays optional. | Refilling asks, buying without quote progress, or late confirmation can defeat continuation. Track executions, cancellations, replenishment and expiry separately. |
| C2 Bid-side thinning continuation short | Bid full size and order count declined in all four large-down-lasting legs. Requires fresh selling, negative defined flow and later downward quote confirmation. | Brief downward legs had different book signatures. Bid refill or ineffective selling may interrupt continuation. |
| C3 Defended liquidity reversal | Source-linked passive fill, surviving residual, then fresh aggression and quotes moving away from defense. The order may remain behind the improved best quote. | Survival is not reversal probability. Cancellation, repricing, depletion or adverse quote movement invalidate the support; track the exact order and price. |
| C4 Failed continuation reversal | Prior quote progress, a failed same-direction attempt, opposing liquidity growth, then opposite aggression and quote confirmation. Upward failure has exploratory support; retain the downward mirror as a hypothesis. | Temporary stalls can resume. An exit warning for a continuation position is distinct from a qualified reversal entry. |
| C5 Quiet-flow book release | Known healthy feed, exactly zero recent classified quantity and nonzero touch-lot direction. Restores immediate timing as a distinct version. | Missing is not known-empty; touch imbalance can vanish and small movement may not cover costs. Track whether fresh participation joins while preserving its own ledger. |

## Ten additions

| Candidate | Evidence and potential fit | Failure possibilities and trade-management use |
| --- | --- | --- |
| C6 Early flow-and-thinning entry | C1/C2 setups without waiting for quote relocation; timing experiment motivated by movement consumed during confirmation. | Accepts unconfirmed setups; does not prove millisecond opportunities can be captured. Preserve early-only, confirmed-only and common events. |
| C7 Recognition plus one-second follow | Continuation after causal recognition and midpoint confirmation. | Motivating D12 diagnostic had negative mean remaining movement on three dates. Do not credit the already-completed confirmation move to entry. |
| C8 Recognition plus one-second fade | Opposite position on the same eligible recognition events as C7; exhaustion/reversion hypothesis. | Sustained continuation defeats fading. Shared events do not imply shared fills or net profitability. |
| C9 Flow with cancellation support | Native touch cancellations support flow; D13 aligned comparison exceeded opposed on three dates. | Liquidity may return; aggregate depth reduction does not uniquely identify cancellations. Track cancellation scope and refill. |
| C10 Flow despite opposing cancellations | Trades with flow despite contrary cancellation direction; opposed comparison exceeded aligned on October 17. | Adverse book changes can overwhelm aggression. Preserve disagreement rather than vetoing eligibility. |
| C11 Expiry-driven flow transition | Expiry-caused sign flip with longer flow/touch agreement and subsequent quote confirmation. | Arithmetic changes may lack price opportunity. Older R9 diagnostic had 116 arms and no confirmations. Separate expiry from fresh arrivals. |
| C12 Standing one-lot retreat | An existing best quote is explicitly reduced to one lot. Earlier source-origin evidence motivates tracking how it became thin. | Residual may hold or refill; retreat need not yield executable profit. A newly exposed one-lot best is a different state. |
| C13 Observable dipole dive and rebound | Local already-observed ratio valley/crest recovery, with direction from native flow and later quote movement. | Sparse updates, oscillation or expiry can produce shape without useful response. Preserve both price directions and driver tags. |
| C14 Fresh flow handoff against older trend | New aggression changes 5s direction while 60s stays old. Fresh-driven flow flips had greater short-term flow-state persistence in earlier evidence. | Flow-state persistence is not price continuation; a counter-move may fail. Track whether the longer window follows or resists. |
| C15 Pullback and renewed-participation re-entry | Prior quote move, contained pullback, renewed aggression and later resumption. | Pullback can become reversal; apparent recovery can be expiry-driven. Preserve sparse/missing information features and frozen earlier models. |

## Eight trade-type observations retained

All observations below describe the selected examples, not general market incidence or proven forward signals. Dates are October 2, 3, 17 and 18, 2023.

| Type | Retained observation |
| --- | --- |
| Large up lasting | Ask full size/count declined on all four dates; bid buildup was not universal. |
| Large up brief | Endpoint book changes were mixed and selected legs extremely short. |
| Large down lasting | Bid full size/count declined on all four dates. |
| Large down brief | Ask full size/count declined while bid size/count were flat or rose, unlike lasting-down depletion. |
| Small up lasting | Book-change signs reversed between October 2/3 and October 17/18. |
| Small up brief | Bid full size/count declined on all four dates despite the upward print leg. |
| Small down lasting | October 3 opposed the other three dates' bid-size/count pattern. |
| Small down brief | Ask full size/count declined on all four dates; native ratio remained unchanged during each millisecond leg. |

All sixteen small legs ended at the preceding trade's price, making print bounce versus quote relocation important to inspect. All sixteen brief legs lasted 0.300–19.162 milliseconds. Recognition followed the selected leg in 25/32 cases. These observations do not authorize retrospective entries, identify every case as pure bounce, or make realized trade type an entry selector.

## Seven gaps and how to address them

1. **Coverage beyond selected examples.** Preserve the full selected-case grid and examine every eligible occurrence in additional continuous sessions. Record failed, flat, unconfirmed and unfilled cases. Keep eight realized types as reporting cohorts, never entry conditions.
2. **Meaning and availability of all fields.** Maintain an individual record for each original field: semantics, source, availability clock, valid/missing states, duplicated operands and event-path behavior. Recover missing source inputs when possible; otherwise preserve explicit unavailability. Retention does not establish interpretive completeness.
3. **Exact sequence and timing.** Reconstruct complete-group paths from state change through observable signal, quote response, decision, order arrival and fill/no-fill. Measure remaining movement after actual entry. Keep arrivals, expiry, cancellations, executions and refill separate.
4. **Trade management.** Retain explicit original and additional management variants on source-linked entry events. Study structural invalidation, continuation/exhaustion warnings, time exits and re-entry with actual exit availability. A useful management observation need not be a useful entry predictor.
5. **Conditions distinguishing outcomes.** Examine individual driver, book, order-origin, replenishment, spread, activity, prior-path and session conditions. Predeclare questions before inspecting outcomes. Preserve sparse and disagreeing cases; do not create a composite confidence score or universal eligibility veto.
6. **Runnable unambiguous rules.** Specify states, reference updates, arming/rearming, expiration, reset, missing-data treatment, simultaneous decisions and order lifecycle. Use source-linked acceptance examples and version all interpretations without replacing originals.
7. **Faithful execution and independent evaluation.** Verify feed capability and platform semantics, account for latency/costs, and reconcile all decisions with platform order and fill records. Preserve strategy attribution even when opposing positions could net. Freeze versions before fresh evaluation and log opportunities during pauses/caps.

These steps improve evidence and implementation without eliminating candidates. A setup that cannot be evaluated is recorded as such; no signal or fill is invented.

## Additional ideas proposed in this discussion

These are retained suggestions for future explicit specifications, not implemented rules or validated results. They have not been supplied to Claude.

- Defended liquidity finally breaks: distinguish execution-driven depletion from withdrawal and test movement through failed defense.
- Aggression exhaustion without opposite aggression: investigate an independent management warning and separately define any entry variant.
- Cancellation-led movement before fresh flow: examine withdrawal and quote change before new aggression, preserving source identity and timing.
- Failed reversal and original-trend resumption: a reversal attempt fails and the original direction regains control; do not require an earlier strategy to have filled.
- Observable range rejection: prior-observation boundaries, repeated tests and response, without hindsight-defined highs/lows.
- Price relocation followed by participant response: trace later independent additions, cancellations or aggression and subsequent price; preserve both continuation and reversal possibilities.

There is no cap on additions, no requirement to manufacture a count, and no later filtering step.

## Execution evidence and limits

The saved October 16 legacy replay is known development evidence for new designs. All diagnostic arms that traded lost after one-extra-tick-per-fill stress; strict R6A's single trade was zero after stress. Fees remained unknown. These results are not results for the new fifteen and do not remove hypotheses.

Historical tastytrade sandbox probes rejected the specified futures IOC orders and did not establish the native order IDs and complete CME event-group access needed for some rules. Those are historical probe results, not current capability verification. A Day order plus cancellation must not silently replace IOC semantics. A prior routed-and-cancelled zero-fill connectivity test is not strategy paper execution.

## Source records

- [Discovery D01–D08](https://github.com/DavisAI1974/markets-data/blob/fe45d2eff9b389e00c80807b6e2240003ba4885d/tasks/family-research-20261022/research-union-current/discovery-depth-20261109/REPORT.md)
- [Reanalysis D09–D13](https://github.com/DavisAI1974/markets-data/blob/fe45d2eff9b389e00c80807b6e2240003ba4885d/tasks/family-research-20261022/research-union-current/reanalysis-20261109/REPORT.md)
- [October 16 legacy replay](https://github.com/DavisAI1974/markets-data/blob/fe45d2eff9b389e00c80807b6e2240003ba4885d/tasks/family-research-20261022/research-union-current/paper-validation-20261109/NG_HOLDOUT_20231016.md)
- [Historical platform preflight](https://github.com/DavisAI1974/markets-data/blob/fe45d2eff9b389e00c80807b6e2240003ba4885d/tasks/family-research-20261022/research-union-current/paper-validation-20261109/TASTYTRADE_NG_PREFLIGHT.md)

The full original case rows, source dependencies and renderings are now preserved separately in the independent source package in this repository. Their inclusion there is evidence preservation, not new validation.
