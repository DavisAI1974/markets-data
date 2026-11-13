# Evidence and availability map

All candidates remain retained. This map is not an execution runner. Fixed historical windows remain only in archived specifications; see [Horizon research](HORIZON_RESEARCH.md).

| Strategy | Required evidence | Context kept separately | Unresolved work |
|---|---|---|---|
| C1 Ask-side thinning continuation long | B01, B02, B03, B11, B12 | B04, B06 | D01, D02, D10, D11 |
| C2 Bid-side thinning continuation short | B01, B02, B03, B11, B12 | B04, B06 | D01, D02, D10, D11 |
| C3 Defended liquidity reversal | B02, B03, B05, B11, B12 | B01, B04, B08 | D01, D02, D04, D10, D11 |
| C4 Failed continuation reversal, both directions | B01, B02, B03, B11, B12 | B04, B05, B06 | D01, D02, D10, D11 |
| C5 Quiet-flow book release | B02, B03, B11, B11, B12 | B01, B04, B06 | D01, D02, D10, D11 |
| C6 Early flow-and-thinning entry | B01, B02, B03, B11, B12 | B04, B06 | D01, D02, D10, D11 |
| C7 Recognition plus one-second follow | B02, B07, B11, B12 | B01, B03, B04, B06 | D01, D06, D10, D11 |
| C8 Recognition plus one-second fade | B02, B07, B11, B12 | B01, B03, B04, B06 | D01, D06, D10, D11 |
| C9 Flow with cancellation support | B02, B03, B04, B11, B12 | B01, B06 | D01, D02, D03, D10, D11 |
| C10 Flow despite opposing cancellations | B02, B03, B04, B11, B12 | B01, B06 | D01, D02, D03, D10, D11 |
| C11 Expiry-driven flow transition | B02, B03, B11, B12 | B01, B04, B06 | D01, D02, D10, D11 |
| C12 Standing one-lot retreat | B02, B04, B05, B11, B12 | B01, B03 | D01, D03, D04, D10, D11 |
| C13 Observable dipole dive and rebound | B02, B03, B06, B11, B12 | B01, B04, B08, B10 | D01, D02, D05, D10, D11 |
| C14 Fresh flow handoff against the older trend | B02, B03, B11, B12 | B01, B04, B06, B10 | D01, D02, D10, D11 |
| C15 Pullback and renewed participation re-entry | B02, B03, B11, B12 | B01, B04, B06, B08, B10 | D01, D02, D10, D11 |

## Operand and clock contracts

### B01: Full depth and counts

**Fields:** L039 | full_bid_ask_depth, L040 | price_level_and_order_counts

**Operands:** before/during.bid_full_size; before/during.ask_full_size; before/during.bid_full_orders; before/during.ask_full_orders

**Source events:** groups-*.parquet

**Clock:** L029.values.before.known_by_ns for before; values.during_known_by_ns for during; source group known_by_ns for complete replay

**Availability:** Original per-trade joins exist; complete non-trade groups are located, not reconstructed in this pass.

### B02: Quotes and touch liquidity

**Fields:** L045 | spread_and_depth_imbalance, L052 | price_and_book_path, L054 | legacy_price, L040 | price_level_and_order_counts

**Operands:** bid_price_raw; ask_price_raw; bid_size; ask_size; bid_orders; ask_orders

**Source events:** groups-*.parquet

**Clock:** Complete group known_by_ns; use group_ordinal/cursor for strict later-group confirmation, including tied nanoseconds.

**Availability:** Original before/during values; L054 repeats L052 prices and L045 overlaps both.

### B03: Fresh, expired and rolling native flow

**Fields:** L048 | aggressor_and_native_signed_flow, L055 | legacy_native_signed_flow, L056 | legacy_per_second_roll20, L059 | derived_roll20_and_dipole_state

**Operands:** aggressor_side; size; trade_input_cursor; available_ns; incoming_buy/sell; expired_buy/sell; window_buy/sell

**Source events:** trades.parquet, actions-*.parquet, groups-*.parquet, native-flow-source-clocks.parquet

**Clock:** Trade available_ns/group known_by_ns governs admission; (t-W,t] membership uses explicitly registered source time axis; expiry timer processing gets its own decision clock.

**Availability:** L048 is individual trade operands only. L055/L056/L059 are missing in the grid. Native completed-second ratio/roll operands are separate contextual columns; they are not arbitrary fast/slow windows.

### B04: Cancellation attribution

**Fields:** L031 | order_lifecycle_cancels, L032 | order_lifecycle_modifies, L047 | mechanics_actions_by_side_and_level, L049 | depletion_and_replenishment

**Operands:** action; order_id; before_side; before_price; before_size; after_side; after_price; after_size; fill_linked_reduction; old/new_touch_effect_json

**Source events:** actions-*.parquet, groups-*.parquet

**Clock:** Action known_by_ns and group_close_cursor; classify touch against registered before/after quote context.

**Availability:** L047/L049 have aggregate touch effects; unlinked removal is not proof of cancellation. Raw action columns are located; action taxonomy and attribution still require verification.

### B05: Tracked order survival and refill

**Fields:** L030 | order_lifecycle_adds, L031 | order_lifecycle_cancels, L032 | order_lifecycle_modifies, L033 | order_lifecycle_replaces, L034 | order_lifecycle_trades, L035 | order_lifecycle_fills, L036 | order_lifecycle_clears, L037 | order_identity_transitions, L041 | fifo_queues, L042 | queue_age_and_survival, L043 | queue_concentration, L044 | orders_and_volume_ahead, L049 | depletion_and_replenishment

**Operands:** order_id; action; before/after side/price/size; fill_linked_reduction; fill_unchanged_display; first_cursor; close_cursor

**Source events:** actions-*.parquet, groups-*.parquet, source-receipt.json

**Clock:** Only order state available at current completed group; never join future survival or final fate into setup.

**Availability:** Grid aggregates cannot establish exact order identity, FIFO or seed lineage. Source action ledger exists; bootstrap/reset-aware order replay is unresolved.

### B06: Native morphology and its publication clock

**Fields:** L056 | legacy_per_second_roll20, L058 | legacy_structure_observables, L059 | derived_roll20_and_dipole_state, L064 | derived_price_flow_book_paths, L066 | derived_feature_availability_timestamps

**Operands:** context.Native dipole ratio at latest completed second; context.Native roll buy/sell; second_rows.native_buy/native_sell; completed_second_known_by_ns; completion_group; completion_cursor

**Source events:** native-flow-source-clocks.parquet, sample-clock-pins.npz

**Clock:** completed_second_known_by_ns, not label_ns or sample_cut_ns; repeated tick attachments are not new ratio updates.

**Availability:** Contextual native series preserved. Named L layers are unavailable; alternative learned-window constructions must get separate version IDs and must not rewrite the archived native ratio.

### B07: Causal recognition

**Fields:** L076 | clock_prospective_discovery_confirmation, L029 | raw_source_identity_provenance_clocks_integrity, L075 | clock_feature_availability

**Operands:** life.recognition_ns; life.recognition_clocks.group; life.recognition_clocks.close_cursor; life.recognition_clocks.known_by_ns

**Source events:** whole-lifecycles.parquet, a-dipole-clocks.parquet

**Clock:** Actual recognition_ns; birth label is retrospective; final end cannot arm or time a live entry.

**Availability:** Exact case recognition clocks exist although L076 cells are missing; prior result places recognition after leg end in 25/32 cases.

### B08: State-masked S measurements

**Fields:** S01 | extension_count_log, S02 | far_absorption_share_1024, S03 | far_absorption_share_64, S04 | far_front_age_log, S05 | far_identity_survival_1024, S06 | far_identity_survival_64, S07 | far_priority_loss_rate_1024, S08 | far_priority_loss_rate_64, S09 | far_queue_age_p90_log, S10 | far_replenish_log1p_1024, S11 | far_replenish_log1p_64, S12 | far_size_hhi, S13 | far_size_retention_1024, S14 | far_size_retention_64, S15 | pullback_ticks_last_log, S16 | pullback_ticks_prev_log, S17 | step_duration_groups_log, S18 | step_ratio_log, S19 | unresolved_age_groups_log

**Operands:** previous_input; at_trade_input; at_emission_group_close; last_completed_group_before_trade; raw_float64; state_code; state

**Source events:** joined-inputs-*.parquet, compact feature projection (upstream source still to bind)

**Clock:** Map emission close to L029.during.known_by_ns and last-completed to L029.before.known_by_ns; previous_input needs its precise input cursor/clock. State and producer semantics must also be verified.

**Availability:** Only Oct18 has these payloads; at_trade_input is missing throughout. PRESENT/state_code=0 is necessary but does not by itself prove live availability.

### B09: External context and publication state

**Fields:** X01 | cot.managed_money_net_pctile_1y, X02 | weather_forecast.forecast_gw_hdd, X03 | cot.managed_money_net_chg_wow, X04 | cot.managed_money_net_pctile_3y, X05 | grid_stack.bas.US48.wind_mwh, X06 | squeeze_watch.sessions_since_prompt_expiry, X07 | grid_stack.bas.US48.est_gas_burn_bcfd, X08 | cot.ice.ld1.managed_money_net_pctile_1y, X09 | model_disagreement.summary.max_abs_spread_gw_hdd, X10 | weather.gw_hdd (observed), X11 | EIA weekly storage (level, weekly change, vs 5-year), X12 | storage estimate vs actual, X13 | the futures curve shape

**Operands:** series[].original.state; series[].original.value; series[].original.published_ns; series[].original.row.event_time_ns; asof_receive_ns; publication_confidence

**Source events:** joined-inputs-*.parquet, external publication stores referenced by original payload

**Clock:** Declared published_ns <= asof_receive_ns; keep release time, underlying observation time and actual receiver delivery separately.

**Availability:** Mixture of published, static and missing values. Some publication timestamps are derived; X13 includes price-derived curve operands. Not independent directional confirmation.

### B10: Information-model inputs and frozen legacy models

**Fields:** L039 | full_bid_ask_depth, L040 | price_level_and_order_counts, L045 | spread_and_depth_imbalance, L048 | aggressor_and_native_signed_flow, L058 | legacy_structure_observables, L059 | derived_roll20_and_dipole_state, L064 | derived_price_flow_book_paths, L066 | derived_feature_availability_timestamps

**Operands:** prior price/range; early/late/fresh buy and sell; entropy; MI; C; flow-change; original M0/M1 coefficient/transform definitions

**Source events:** TRADE_RULES.json.models, prior model input generation and source event tapes

**Clock:** Each component must carry max(input known_by); preprocessing and model training cutoffs precede validation. Frozen R7/R8 remain archived; learned-window forks receive new model IDs.

**Availability:** Frozen models retained in prior rules; 141-field grid does not supply all original model features. No predictions generated here.

### B11: Integrity, source identity and session continuity

**Fields:** L024 | canonical_sep_nov_2021_dbn_mbo_objects, L025 | october_first_source_window, L026 | canonical_predecessor_bootstrap_objects, L027 | native_acmrtfn_messages, L028 | snapshot_bootstrap_reset_messages, L029 | raw_source_identity_provenance_clocks_integrity, L038 | contract_session_roll_state, L046 | complete_state_reset_bootstrap_receipts, L053 | missingness_and_integrity_flags, L072 | clock_event_time, L073 | clock_receive_time, L074 | clock_event_known_by, L075 | clock_feature_availability

**Operands:** day; trade_ordinal; trade_id; trade_cursor; event_ns; receive_ns; known_by_ns; source_trade_revision; source_trade_path; coverage; snapshot_member; reset_member; bad_receive_clock_member

**Source events:** joined-inputs-*.parquet, source-receipt.json, groups-*.parquet, actions-*.parquet

**Clock:** Exact integer nanoseconds plus cursor order. Decisions cannot precede any required operand known_by or complete-group close.

**Availability:** Metadata and before/during integrity flags exist; snapshot/continuity proof must cover all relevant events, not only trade attachments.

### B12: Order submission, fills and costs

**Fields:** Execution-report fields outside the original 141

**Operands:** decision_ns; submit_ns; ack_ns; fill_ns; fill_price; fill_size; no_fill_reason; fees; slippage; latency

**Source events:** future paper adapter execution reports

**Clock:** decision <= submission <= observed fill; receipt and source event clocks retained independently.

**Availability:** No new strategy execution reports exist. Instrument identity, fees and adapter remain unresolved. No simulated midpoint fills claimed.

## Every prior arm remains

Original C1–C5 are archived unchanged, alongside revised C1–C15 and the eleven legacy arms R1–R10 (R6A and R6B separately). The machine-readable map has distinct records for each. No family is replaced by a winner.

## Additive questions beyond fifteen

### H16: Flow-to-price response delay

Does fresh flow transmit to both quotes at different delays depending on refill/cancellation state?

Keep every arrival, no-response, delayed-response and adverse-response episode. Estimate elapsed-time and complete-group response distributions, censored at known observation end. Use as timing/management information without assuming direction.

Evidence: B02, B03, B04. Dependencies: D01, D02, D03, D11.

### H17: Displayed size versus order-count divergence

Do falling lots with rising order counts, or the converse, distinguish fragmentation, resistance and later quote movement?

Keep all four change-sign combinations and exact zero changes. Treat the ratio as optional derived context, with separate raw operands; resolve identities before attributing fragmentation to a mechanism.

Evidence: B01, B02, B05. Dependencies: D01, D04, D11.

### H18: Liquidity withdrawal and return

Does the time and event count from actual cancellation to same-price liquidity return distinguish continuation from failed release?

Track same-order versus replacement-order return and original versus new touch. Retain absent return and unresolved identity. Learn time scales; never use eventual refill to classify a live setup.

Evidence: B02, B04, B05. Dependencies: D01, D03, D04, D11.

### H19: Trade-print movement versus quote movement

Can print-side alternation explain small/brief moves while quote relocation marks a different state?

Preserve every print and bid/ask path. Record previous-price returns, same-side prints, spread changes and both-quote relocation separately across all types. This is an additional explanatory and management branch, never a rule for removing bounce-like cases.

Evidence: B02, B03. Dependencies: D01, D02, D11.

### H20: Information-state context and lifecycle age

Do separately observed age, survival, replenishment and information inputs distinguish stalls, renewed activity or management needs?

Keep all 19 S fields and each state slot; do not make available-on-Oct18 observations a four-day claim. Missing and zero-MI states remain visible. Source-clock and producer dependencies precede any live use.

Evidence: B06, B08, B10. Dependencies: D05, D07, D09, D11.

### H21: External vintage and market-state interaction

Do publication-vintage context and contract curve state change the interpretation of local flow/liquidity response?

Preserve all 13 X fields, revisions and original states. Four selected days cannot isolate a day-level external effect; expand independent sessions before fitting. Separate price-derived curve context from independent external observations.

Evidence: B01, B02, B03, B09. Dependencies: D01, D02, D08, D11.
