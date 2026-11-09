# Paper readiness — 2026-11-09

The two rules are specified and frozen for a prospective paper trial. They are not running, have not been strategy-backtested, and have no demonstrated net edge. This delivery performs research and workbook preparation, not execution deployment.

Ready: source-linked top-ten additions; four-session cell readback; contrary/flat/missing cases; exact source clocks; deterministic triggers, confirmations, order handling and exits; explicit provisional parameters; shared exposure/loss limits; required logs.

Before activation, the execution adapter must supply the exact NG expiry, paper account, session start/end in UTC, fees, source-to-local clock mapping and measured arrival timestamps. Unknown fees permit gross-only signal analysis, never a net-PnL claim. Missing timing/adapter configuration permits observation only. Confirm tick size/value against the configured instrument rather than substituting a micro contract.

Execution checks: feed a future-dated feature (reject); remove flow warmup (reject); change flow by expiry only (do not arm); confirm in the same group (reject); expire an R2 order before confirmation (reject); trigger both rules (one R1 position); force IOC no-fill (no position); trigger a stop during a gap (exit pending, never pretend flat); hit session loss (no automatic restart). These are acceptance cases for the adapter, not tests claimed to have run here.

The 0.5-second dipole warning remains unverified. The 0/5/25/100ms resting-state samples are schedules, not execution latency. All four historical days have already informed discovery. The next untouched paper session is the first prospective evaluation of these rules.

Deferred by the user's latest instruction: exhaustive branch reconciliation and remaining bulk workbook exports. Existing workers were allowed to finish; none was restarted for this priority pass. Their durable source/packet checkpoints remain available for the next session.
