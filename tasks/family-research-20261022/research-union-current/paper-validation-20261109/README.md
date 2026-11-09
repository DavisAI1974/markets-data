# Offline paper preparation — 2026-11-09

**22 synthetic contract tests pass. No paper session has started.** R1 remains execution-check-required and R2 remains observation-only; both flags in the authoritative version 1.1 specification are still false. This package is a small reference for timing and quote eligibility, not an executable trading system or historical strategy backtest.

The priority-ten Excel and discovery analysis were already finalized in commit `25a2b996444ea566c425af2d6498ce6da3093b92`. They are unchanged by this preparation. No existing workers were restarted.

## What was checked

- Exact integer nanosecond clocks; `(t-window,t]` flow boundaries; exclusion of future received/known observations; unknown aggressor quantity separate from classified flow; empty versus balanced flow.
- R1 fresh-arrival arming, both-quote confirmation in a later complete group, long/short symmetry, five-second expiry, sign rejection, consumed arms and a new transition before rearming.
- Warmup, continuity, quote-age/silence, spread/size and ordering guards; failure pauses without automatic resume.
- Persistent invalidation across distinct groups, reset on renewed agreement, empty flow as a signal condition, and immediate invalidation on feed failure.
- Quote eligibility after measured arrival and after the confirmation group, correct bid/ask side, and rejection of invalid or future-known quotes.
- Separate gross, adverse-slippage scenario and fee-adjusted results; unknown fees remain missing. R2 activation remains blocked.

Run from this directory: `python -m unittest -v test_contract_checks`.

`Group` assumes already normalized, complete groups and a verified common clock domain. Its index is a local complete-group ordinal, not a raw exchange sequence. Prices are integer standard-NG ticks. The reference functions do not reconstruct a book, validate real source groups, measure latency, deduplicate a feed, or send an order. Quote eligibility does not implement the IOC lifecycle: a future controller must select the first eligible observation exactly once and retain unresolved exposure on failed exits.

## Adapter inspection

The local `executor/exchanges/paper.py` uses cryptocurrency chart closes, a manufactured spread and immediate simulated fractional fills. It is unsuitable for this NG experiment.

The local `research/ng_exhaustion_mbo_v4_state_adapter_20260820.py` is a research book/event-group adapter, not a configured paper execution adapter. Its rolling activity removes timestamps strictly before the cutoff, retaining the left boundary. Version 1.1 requires an exclusive left boundary. Its exported activity totals therefore must not be reused unchanged for R1. No legacy adapter was edited, and this finding does not invalidate its original research definition.

These are read-only local-source observations, not certifications of either adapter. Source hashes are in `CHECK_RECEIPT.json`.

## Still required before execution

The pending user configuration is the **paper platform, exact standard-NG contract/expiry, and session hours/timezone**. Fees and a measured send/arrival clock mapping must then come from that configured environment. `SESSION_TEMPLATE.json` intentionally leaves these values unset.

The full runner still needs implementation/integration and end-to-end acceptance for: one-contract portfolio capacity; first-eligible-quote IOC cancellation and retries; no fictitious flattening during outages; hard stop and overshoot; 120-second hold; 30-second cooldown; 20-entry cap; gross/net session loss; last-120-second entry rejection; session/contract boundaries; fresh-snapshot recovery and explicit resume; and immutable signal/order/fill logs. Passing these reference tests does not satisfy those checks.

After configuration, connect only the paper environment, freeze a prospective version, verify feed/clock continuity, complete those runner checks and record the activation decision. R2 requires its additional full-sequence study before any order capability. The four historical discovery sessions are not unseen validation data.

## Interpretation

The test results establish behavior of these reference functions on synthetic inputs. They do not measure signal counts, fill rates, latency, drawdown, profitability, or a live platform's behavior. No new PnL or historical trading performance has been inferred.
