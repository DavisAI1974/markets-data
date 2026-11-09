# Priority reanalysis — 2026-11-09

The requested top ten additions are complete: 628,672 source records across all four dates, selected for decision relevance and missing evidence, not favorable returns. All new cells were compared against their frozen source projections. Original master data sheets remain byte-identical. The main workbook holds P02–P10; the complete P01 flow table is in Priority_native_flow.xlsx to keep each file below GitHub’s file limit.

The existing three research branches were searched. Current reviewed heads: Desktop `3d0b06aa29781d5e39cc3eb45c6d09e174f195a2`, CCode `6152e284fef144c5f614ee26b949136d986fd66f`, Codex `418462afeaf0f14aa8129f6f4d02c3867d772fd0`. Branches share original artifacts; origin means research authorship, not exclusive branch residence. Immutable source URLs and blob hashes are recorded in priority_selection.json. CCode’s new reanalysis was not read.

The previous shared brief was retained: explicit clocks, counts and denominators; individual and combined evidence; weak/inverse/flat/missing states; price feedback; deterministic rules; future labels excluded from online inputs. This is a priority pass over every newly added row plus the existing workbook coverage/timing cells, not a claim to have newly recomputed every old research layer. Exhaustive reconciliation is deferred at the user’s request.

## The ten additions

| Priority | Addition | Rows | Research origin | Why now |
|---|---|---:|---|---|
| 1 | P01 Fresh versus expiring flow | 316,800 | Codex | Distinguish new aggression from rolling-window expiry before a flow trigger. |
| 2 | P02 Flow depth and refill | 3,215 | Desktop | Add full-depth, touch counts, fills, adds and removals to each family context. |
| 3 | P03 Four arm entry candidates | 41,866 | CCode | Compare flow and book agreement and disagreement across all recorded candidates. |
| 4 | P04 Order identity lifecycle | 21,326 | Codex | Tie aggression to later resting display and actual order actions without inferring intent. |
| 5 | P05 Observable resting state | 17,284 | Codex | Separate state known at decision time from later fills and removal. |
| 6 | P06 Matched prebirth controls | 116,798 | Codex | Retain controls, missing matches and adverse precursor differences. |
| 7 | P07 One lot order origins | 101,066 | CCode | Expose order age, repeated onsets and later fate of thin-touch orders. |
| 8 | P08 Event order and lean | 3,965 | Desktop | Compare aggression, size change, price relocation and recognition; preserve control curves. |
| 9 | P09 Recognition boundary | 3,176 | CCode | Separate observed birth-to-recognition movement from subsequent movement. |
| 10 | P10 Price flow book context | 3,176 | Codex | Add price path, fresh flow, display changes and explicit empty states at the decision clock. |

## Findings and implications

Dates in all four-value sequences are 2023-10-02, 2023-10-03, 2023-10-17, 2023-10-18.

### P01 — Fresh versus expiring flow

24,679/59,758 ratio changes (41.3%) had no fresh classified buy/sell volume. Four final seconds have no completion clock.

Arm only on newly observed aggression. Use completed-known-by clocks; P01 is in Priority_native_flow.xlsx.

### P02 — Flow, full depth and refill

Five-second flow/full-depth: 1,382 aligned, 1,220 opposed, 87 neutral, 526 missing. Full depth is not touch imbalance.

Keep full-depth, near-depth and touch signs distinct; no missing-to-zero conversion.

### P03 — Agreement and disagreement

Aligned 60s oriented mean ticks by date: 0.350, 0.128, 0.099, 0.006. Opposed: 0.046, 0.131, -0.274, 0.123.

Agreement does not dominate on every date. R1 is an untested composite hypothesis, not an established edge.

### P04 — Order identity and lifecycle

4,321 aggression-to-rest episodes; median duration by date 5.65ms, 6.01ms, 11.29ms, 8.46ms. Remaining P04 rows are actions.

An order-ID sequence is not trader intent. Final fate cannot enter a trigger.

### P05 — Resting state known by decision

1,558/4,321 episodes (36.1%) remain eligible at scheduled +25ms. No future-action cutoff violations in these rows.

Scheduled survival is not latency or our fill probability. Require current surviving state and measured arrival.

### P06 — Matched controls and gaps

Matched case flags: 9,190; unmatched: 6,518. Complete pair-feature and case records retained.

Future-excluded controls are retrospective. Do not use cohort/control membership online or count pair-feature rows as independent trades.

### P07 — One-lot order origin

101,066 onsets: 48,133 retreated, 52,060 recovered size, 871 improved. Repeated order onsets remain visible.

Thin touch alone is not an entry. Preserve order age, onset history and contrary fates.

### P08 — Event order and lean

2,474 aggression-first, 607 price-first, 75 same-bin, 1 censored/missing among 3,157 retrospective tapes.

Price can precede measured aggression. Birth alignment and bin order do not establish warning lead or causality.

### P09 — Recognition boundary

Median birth-to-recognition elapsed time by date: 52.12s, 52.16s, 52.27s, 51.67s. Undefined flow at emission: 1,355/3,176.

Recognition is late relative to retrospective birth; no verified 0.5s warning. Later price response is a different measure.

### P10 — Price, flow and book context

1,358/3,176 contexts have both flow halves empty. No future quote/flow-known-by violations in checked clocks.

Observe price feedback and empty states; availability alone does not prove predictive value.

## Per-date denominators

| Date | Flow seconds | Families | Four-arm candidates | Rest episodes | One-lot onsets | First-event tapes | Recognition rows |
|---|---:|---:|---:|---:|---:|---:|---:|
| 20231002 | 75,600 | 795 | 11,598 | 1,129 | 22,042 | 741 | 741 |
| 20231003 | 82,800 | 848 | 13,266 | 1,202 | 24,353 | 824 | 832 |
| 20231017 | 75,600 | 823 | 8,880 | 1,010 | 27,111 | 740 | 740 |
| 20231018 | 82,800 | 749 | 8,122 | 980 | 27,560 | 852 | 863 |

These are different source populations. They overlap and include repeated orders, actions, scheduled observations and pair-feature rows. Do not sum them as independent trades or join by row position. P08/P09 cohort counts differ on October 3 and 18; no cross-study identity was assumed.

## Timing, feedback and contrary evidence

| Date | Changes without fresh classified volume / all ratio changes | Eligible at +25ms / rest episodes | Recognition median seconds | After-recognition 60s mean ticks (N; + / − / flat) |
|---|---|---|---:|---|
| 20231002 | 6,138/14,957 | 369/1,129 | 52.121 | 0.137 (740; 287/263/190) |
| 20231003 | 6,710/16,638 | 377/1,202 | 52.156 | -0.060 (832; 260/312/260) |
| 20231017 | 6,002/14,495 | 417/1,010 | 52.272 | -0.157 (740; 264/275/201) |
| 20231018 | 5,829/13,668 | 395/980 | 51.673 | -0.073 (862; 339/335/188) |

Flow changes without fresh classified volume arise as classified volume leaves the rolling window; unknown-side events remain a separate category. No original completed-second clock precedes its second end; the final second of each session lacks a completion clock and remains unavailable. Completion can be delayed substantially in quiet markets.

The 60-second response table is an outcome diagnostic, not a warning lead, entry fill, net edge, or proposed exit time. Observations are overlapping, costs are excluded, and all four dates already informed discovery. Recognition-direction median response at 60 seconds is zero on every date. Flow/book agreement is not uniformly better than disagreement.

Full-depth sign is positive in 3,068 of 3,215 family rows, while touch depth can disagree. Full depth and touch are not interchangeable. Categorical `+`, `-`, `0`, `NA` were parsed explicitly; an event-order sentinel of -1 was excluded from observed-order comparisons and retained as censored. These checks changed the draft analysis before delivery.

Additional saved-cell feedback checks in price_feedback_cells.json compare prior 20-second price direction with current five-second flow and full-depth versus touch signs, followed by future price response. They preserve reverse-order and neutral/missing cases. They do not identify causal price impact, since family/cohort selection is retrospective and a complete intervening action-path causal analysis has not been performed.

## Case evidence and coverage

analysis_cases.json retains deterministic examples per date and state, including opposed, missing, adverse fate, expired and surviving orders. Each case names its sheet, actual Excel row, source ID, zero-based source row and complete cell values. It is an illustration index, not a filtered population used for metrics. cell_metrics.csv and Priority metrics contain all computed distributions; Priority counts retains population and clock-check counts.

The prior master coverage remains: 143,270 saved trades and 141 original layer fields via the existing companion layer workbooks. Existing companion research is not re-exported or silently replaced. Original corrected sources S00092/S00096/S00101/S00105 remain intact. The archived 193k dipole-stage table is context only, not admitted as newly verified event data. The claimed ~0.5-second warning remains unverified. The exact identities of the earlier “two workflows” remain unresolved; this report makes no new claim about their results.

## First paper rules

PAPER_STRATEGIES.md and PAPER_STRATEGIES.json freeze R1 fresh-flow/touch agreement with a strictly later quote confirmation, and R2 observed surviving-order absorption with later quote confirmation. Paper rules v1 contains the complete specification in the main Excel workbook. Both are prospective hypotheses; the selected studies do not test these composite rules as a strategy.

Shared provisional limits: one virtual standard NG contract total, four-tick stop trigger, twelve-tick session loss limit, 120-second holding cap, thirty-second cooldown and twenty entries per configured session. No averaging or automatic reversal. Marketable IOC fills require a subsequent executable quote and measured arrival; passive survival and scheduled offsets never stand in for our fills. Gross, fees, net and adverse-slippage stress are separate. Unknown fees produce unavailable net PnL.

PAPER_READINESS.md lists the remaining execution-adapter configuration and acceptance cases. No adapter was connected and no trades were submitted. The workbook/rules are ready for review and adapter implementation; execution readiness is conditional on that configuration and its checks.

## Deferred reconciliation

The previously running bulk jobs finished without duplicate launches. Workflow retained 18,168,382 rows; the Oct 2 workflow export finished 4,340,150 rows in 255 books. Remaining-source processing and source-sample reconciliation reached durable checkpoints. These bulk outputs are not claimed to be fully cell-verified or included in this priority delivery. Other workflow dates and exhaustive publication remain deferred for the next session.
