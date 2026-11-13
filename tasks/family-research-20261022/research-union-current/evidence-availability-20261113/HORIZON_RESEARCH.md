# Let the data determine the horizons

The user's latest instruction supersedes fixed 5s and 60s requirements for new strategies. Those constants remain verbatim only in archived specifications and historical baselines. No horizon has been learned or selected in this availability pass.

## What becomes data-dependent

| Quantity | Data to examine | Separate research variants |
|---|---|---|
| Fast/slow participation memory | Each native buy, sell and unknown-side arrival; exact admission clock; expired lots | Elapsed-time windows; complete-group windows; classified-event or volume clocks |
| Book-change reference | Every completed quote/depth/count update, with resets retained | Elapsed time; quote-change count; order-action count |
| Quiet-state duration | Healthy-feed intervals, classified and unclassified activity, group cadence | Time since last classified trade; consecutive complete groups; activity-conditioned duration |
| Confirmation delay/expiry | Setup, first quote response, opposing response, no-response and censoring clocks | Immediate and delayed variants; elapsed-time and event-count deadlines |
| Recognition follow/fade observation | Exact recognition and subsequent quotes | Empirical response-delay grid, including immediate observation; no inherited +1s obligation |
| Morphology scale | Each distinct native update and its source arrivals/expiry; all tick attachments retained | Pattern step count, elapsed-time persistence and separately versioned native-window variants |
| Management horizon | Quote response, fresh participation, refill and failures after decision | Event-triggered management; learned persistence duration; execution/risk limits documented separately |
| Re-entry reference | Observed impulse/pullback/recovery, all with known-by timestamps | Data-derived reference depth and return interval; no inherited 20s obligation |

The first pass preserves `observed_trade_intervals.csv` with every consecutive selected-case interval and `case_manifest.json` with exact leg durations. These are inspection data, not sufficient training data. The selected examples deliberately span price shapes; their leg durations cannot be used as live window lengths. The 60-second padding is a historical display/extraction choice and remains intact, not a proposed signal horizon. If learned histories require more context, extend source retrieval while preserving every original row.

## Development protocol

1. Reconstruct complete continuous streams with contract/session/reset identities, exact source order, native side classification and feature availability. Never infer quiet flow from absent trade rows. All days, eight descriptive cohorts and individual fields stay visible; realized cohort names are not online inputs.
2. Build empirical distributions of event spacing, quote-response latency, participation persistence, cancel-to-return delay and observable morphology intervals. Preserve individual event histories and unresolved/right-censored episodes. Do not discard flat, adverse, missing, sparse or late observations to create cleaner distributions.
3. Form candidate horizons from development-data support and event boundaries. Register the candidate-generation rule before measuring strategy outcomes. Keep time, complete-group, trade-count and volume clocks as distinct variants; do not substitute one for another. Candidate resolution is constrained by observed timestamp precision and feature update cadence, not by aesthetically round seconds. Restrict supported estimation ranges transparently; retain unsupported horizons as unresolved rather than silently excluding their hypotheses.
4. For each strategy and useful role (timing, continuation, stall, reversal, in-trade management), inspect a horizon-response surface. Keep each raw operand separate. Examine response and censoring rates, coverage, sensitivity, hypothetical execution delay and costs, not only maximum profit or correlation. More than one horizon may be useful in different observable states; no universal winner is required.
5. Split time before learning. Candidate generation, preprocessing, horizon fitting and any observable-state partitioning must happen inside the development portion of each temporal fold. Purge overlapping lookback/outcome intervals across fold boundaries using the largest candidate exposure; do not hard-code another arbitrary purge duration. Keep entire coupled event/order episodes together. Report every strategy and all variants, including insufficient coverage and no-fill cases.
6. Lock the resulting per-strategy/per-stage horizon definitions, candidate-generation code, source hashes and training cutoff before evaluating untouched sessions. The four selected dates and the already-read October16 replay are development evidence; none is an untouched test for these choices. Obtain independent additional sessions for confirmation. Test stability across multiple temporal folds and retain uncertainty when sample support is inadequate.
7. A proposed adaptive online horizon may depend only on past admitted observations. Log the chosen horizon, its input event IDs, known-by clocks, model/version and any update rule at every decision. Do not retroactively revise prior decisions after observing the price path. If insufficient history exists, log an unresolved decision; keep the tick and opportunity.

## Exact clock definition required before implementation

`W_fast` and `W_slow` are unset research parameters, not aliases for 5 and 60. For a time-window experiment, define both the source clock used for `(t-W,t]` membership and the processing/admission clock. A late source event cannot enter an earlier historical decision. Expiry itself is an event: log when the decision process could observe it. Decide and version timer-driven versus next-complete-group processing; evaluate both as separate hypotheses where appropriate.

For event-count windows, retain exact event identity and distinguish complete groups, individual native prints, order actions and quote changes. A zero-time gap is a legitimate separate event if cursor order proves it; a repeated attachment of one completed native second is not a new native update.

The existing native ratio is an archived measurement with a fixed historical construction. Preserve its values and label/availability clocks. Any recalculation using learned windows creates a new named measurement and lineage alongside it; it does not overwrite the original 141 fields or contextual series.

## Deliverables before paper evaluation

- A versioned candidate-horizon registry with derivation data, clock axis, support, uncertainty and fold membership.
- A per-event, per-strategy ledger with every setup, no-setup, unavailable, censored, pause and no-fill disposition, plus all original tick references.
- Per-strategy and observable-stage horizon-response surfaces; day/type views remain separate and complete.
- Locked validation recipes and fresh-session results, including unfavorable results and alternative horizons.

Current state: planning and availability audit only. No learned horizon, strategy replay, backtest, execution adapter or paper order has been produced here.
