# Discovery update to paper readiness

Version: priority-paper-v1.1-discovery-20261109. The original v1 specification remains frozen in the preceding commit. This version changes readiness and required diagnostic logging, not historical prices or the original entry/exit hypotheses. No adapter was connected and no order was submitted.

- **R1: paper execution check required.** Keep the exact v1 trigger and risk controls. Cross-window agreement has conditional support, but the complete price-confirmed rule has no demonstrated net execution edge. Existing instrument/session/fee/arrival-clock configuration and acceptance checks still apply. `paper_enabled=false` until those checks are performed.
- **R2: observation-only.** Preserve and log every trigger, suppression and subsequent outcome. Do not submit paper orders from this rule yet. Known fills improve survival for one-lot replenished residuals and worsen it for larger residuals, while later price advantage remains unproved. Require a direct test of the whole price-confirmed rule by these states before enabling it. `paper_enabled=false`.
- Log initial display, current residual, fills known, source-accounted implied added display, unmatched-fill accounting, onset mechanism and flow-change provenance. Never infer hidden reserve or participant intent from these fields.

The timing correction replaces the earlier P08 ordering interpretation. Birth-aligned lean is retrospective context. Neither permits a 0.5-second warning claim. Keep missing/quiet-flow observations and opposite-signal cases even when the rule abstains.

The current data cannot price fills or fees for the user's unspecified paper platform. Written rules and observation schedules remain separate from deployment and measured latency.
