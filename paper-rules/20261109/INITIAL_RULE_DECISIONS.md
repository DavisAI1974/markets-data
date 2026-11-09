# Initial 11-rule runtime clarifications

These are new paper-protocol definitions for ambiguities in the November rule specification. They are not new empirical results, optimal parameters or changes to the original measurements. The parent JSON is preserved by immutable Git blob.

- Fresh trade means a classified arrival in the arming group. Quote confirmation compares both quotes with the frozen arming quote, in a strictly later completed group. A partial move remains pending until both requirements hold or the timer expires.
- For the existing invalidation fields, any neutral/opposed sign starts the timer. Both the one-second duration and two-group count must hold. Full agreement resets it. Missing data is not neutral and is handled separately.
- A change of direction starts a new direction episode; a persistent true condition after a completed trade does not automatically produce repeated entries.
- The original R2 `cancel_invalidates=true` is interpreted as any cancellation action, including a partial cut. Partial fills with positive residual remain valid. The order may be behind the best quote at confirmation, consistent with the corrected geometry.
- R4/R5 compare the first eligible delayed quote with the original recognition midpoint. They cannot enter at or after their fixed anchor+20-second exit deadline.
- R7/R8 retain the original P10 midpoint-classified feature source and frozen coefficient arrays. Native flow is not silently substituted. Observed-undefined operator values use the stored imputation/missing flags; feed failures or future inputs do not.
- Common default holding time starts at actual entry fill; fixed anchor exits remain fixed where explicitly specified. Gross loss-limit accounting uses platform fills. Unknown fees are not fabricated as net results.
- The narrowed R10 per-order cap remains in that particular version. It does not remove the separate repeat-survivor/source-history hypotheses recovered by reconciliation.
- Midpoints are doubled integer price ticks. The one-tick confirmation threshold is therefore 2, not 1; a half-tick move does not confirm.
- Process platform fill reports first, then data validity, order/signal invalidation, exit deadlines and risk latches, pending expiry, confirmation and entry gates. Simultaneous invalidation wins over confirmation. Confirmation at its deadline remains eligible, but entry at an exit deadline is expired.
- Cooldown starts on a final rejected/no-fill entry attempt or the last position-closing fill, per rule. The gross loss cap latches at or below minus the specified tick limit for that rule/session, blocks new entries, cancels pending entries and requests any remaining exit. A new explicit platform session ID resets it.
- MODEL_FREEZE preserves coefficient evidence, but exact ordered feature-definition and artifact-availability bindings remain incomplete. Model inference cannot run until MODEL_BINDING_REQUIREMENTS is satisfied. Training cutoff and artifact availability are separate clocks; replay wall-clock availability must be mapped explicitly, never backdated.

This file clarifies the specification. It does not claim that all corresponding engines or platform adapters have been implemented or run. All new candidates use the same paper-inclusion/reporting policy; source-specific conditions remain distinct.
