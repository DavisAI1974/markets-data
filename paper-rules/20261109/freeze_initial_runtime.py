"""Clarify the initial rule specification without fitting or evaluating returns."""
import json,pathlib
ROOT=pathlib.Path(__file__).parent
OLD=ROOT.parent/'markets-carry-forward-20261109/delivery/prior/reanalysis-20261109/TRADE_RULES.json'
OUT=ROOT/'machine';OUT.mkdir(exist_ok=True)
r=json.loads(OLD.read_text(encoding='utf-8'))
r['version']='priority-paper-v2-runtime-20261109'
r['parent_git_blob']='e17c21d77f219de143d308031b3bda88bba2c55a'
r['execution_enabled']=False
r['execution'].update({'fill_authority':'platform_execution_report','position_ownership':'isolated_per_rule','duplicate_signal_policy':'one_entry_attempt_per_signal_id','input_unavailable_policy':'record_no_entry','reject_missing_account':True,'reject_non_simulation_account':True})
r['data'].update({'nanosecond_input_types':['integer','decimal_integer_string'],'float_nanosecond_clocks_allowed':False,'known_by_relation':'less_than_or_equal_to_decision','group_tie_break':'original_complete_group_cursor','missing_is_zero':False,'model_feature_classification':'P10_previous_completed_group_midpoint','native_feature_classification':'exchange_aggressor_side','model_imputation_allowed_statuses':['observed_undefined'],'model_imputation_disallowed_statuses':['feed_missing','unknown_availability','future_known_by','definition_mismatch'],'model_freeze_source':'MODEL_FREEZE.json'})
r['risk']['max_hold_origin']='actual_entry_fill'
r['risk']['stop_origin']='actual_entry_fill_price'
r['risk']['stop_mark']='executable_exit_quote'
r['risk']['session_loss_origin']='realized_gross_ticks_from_platform_fills'
r['risk']['rejected_or_no_fill_is_zero_return']=False
r['risk']['cooldown_origin']='entry_attempt_final_reject_or_no_fill_or_last_position_closing_fill'
r['risk']['cooldown_scope']='per_rule'
r['risk']['cooldown_reset_on']='new_final_attempt_disposition_or_position_close'
r['risk']['loss_cap']={'scope':'per_rule_per_session','threshold':'realized_gross_ticks<=-session_loss_ticks','action':'latch_block_new_entries_cancel_pending_entries_request_exit_open_position','latch_reset':'next_explicit_platform_session_id','rejections_and_no_fills_count_as_returns':False}
r['runtime_semantics']={
 'evaluation':{'opportunities':'every_declared_complete_event_or_timer','clock':'feed_event_time_with_actual_known_by_and_delivery','backdate_orders':False,'repeat_same_event_id':'ignore_for_state_mutation_record_duplicate','out_of_order_event':'record_error_no_entry','snapshot_reset':'invalidate_pending_signals_request_platform_exit_rewarm'},
 'arm':{'edge':'false_to_true_per_direction_episode','initial_state':False,'direction_change':'close_old_episode_open_new_episode','unknown_state':'does_not_establish_false_or_true','rearm_after_fill':'requires_new_false_to_true_episode','pending_timeout_origin':'arm_decision_ns','confirm_deadline_relation':'less_than_or_equal'},
 'fresh_trade':{'scope':'arming_complete_group','minimum_classified_lots':1,'unknown_side_is_classified':False},
 'flow_expiry':{'timer_events':True,'left_boundary':'exclusive','right_boundary':'inclusive','expiry_only_requires_classified_arrival_lots':0,'expiry_only_requires_expired_classified_lots_greater_than':0,'flip_old_and_new_sign_nonzero':True,'flip_old_and_new_sign_different':True},
 'quote_confirmation':{'baseline':'frozen_arming_bid_and_ask','long_bid':'current_bid_ticks>=arm_bid_ticks+confirm_bid_ticks','long_ask':'current_ask_ticks>=arm_ask_ticks+confirm_ask_ticks','short_bid':'current_bid_ticks<=arm_bid_ticks-confirm_bid_ticks','short_ask':'current_ask_ticks<=arm_ask_ticks-confirm_ask_ticks','all_quote_conditions_required':True,'later_group_required':True,'partial_quote_confirmation':'remain_pending_until_both_or_expiry'},
 'signal_invalidation':{'adverse_field':'defined_sign_not_equal_to_armed_direction','neutral_is_adverse':True,'field_combination':'any','duration_condition':'continuous_bad_elapsed_ns>=1000000000','group_condition':'consecutive_bad_complete_groups>=2','duration_and_group_combination':'all','reset_counter':'all_listed_fields_defined_and_aligned','unknown_field':'data_failure_not_neutral_or_good','while_pending':'invalidate_no_entry','after_entry':'request_platform_exit'},
 'R2_order':{'seed_group_actions':['T','A'],'seed_identity_fields':['order_id','side','complete_group_cursor'],'arm':'first_later_F_with_positive_residual_at_touch','arm_flow_side':'native_flow5_and_touch_sign_equal_resting_side_direction','resting_side_direction':{'bid':1,'ask':-1},'confirm_price':'original_order_price','confirm_at_touch_required':False,'any_C_including_partial_size_cut_invalidates':True,'reprice_invalidates':True,'zero_residual_invalidates':True,'partial_F_positive_residual_keeps_order_valid':True,'cancel_order_of_processing':'original_message_sequence_before_group_close'},
 'event_priority':['apply_platform_execution_reports','validate_data_continuity','apply_order_identity_invalidators','apply_signal_invalidators','apply_exit_deadline_and_risk_latch','expire_pending_past_confirmation_deadline','evaluate_confirmation','check_entry_deadline_strictly_before_exit','check_risk_and_cooldown','submit_entry'],
 'boundary_priority':{'simultaneous_invalidation_and_confirmation':'invalidate_no_entry','confirmation_at_confirmation_deadline':'eligible_if_no_other_invalidator','confirmation_at_exit_deadline':'expired_no_entry'},
 'delayed_touch':{'anchor_quote':'last_valid_complete_quote_at_actual_recognition','anchor_direction':'nonzero_touch_imbalance_sign','comparison_quote':'first_available_complete_quote_at_or_after_anchor_plus_delay','maximum_lateness_ns':'1000000000','confirmation':'anchor_direction*(current_mid_twice_ticks-anchor_mid_twice_ticks)>=2','midpoint_representation':'twice_price_ticks_integer','half_tick_change_confirms':False,'one_tick_change_confirms':True,'no_second_attempt_after_failed_confirmation':True,'exit_clock':'anchor_ns+20000000000','entry_at_or_after_exit_clock':'record_expired_no_entry'},
 'frozen_linear':{'models':['M0','M1'],'predictor':'paper_rules.models.predict_frozen_linear','direction':'sign_prediction','zero_prediction':'record_zero_direction_no_order','training_or_refitting_at_runtime':False,'feature_order':'model_features','missing_flag_order':'append_in_feature_order','undefined_observed_value':'frozen_training_imputation_with_flag','feed_missing_value':'unavailable_no_imputation'},
 'one_lot':{'anchor':'first_complete_group_where_same_best_price_falls_from_more_than_one_to_one','direction_by_resting_side':{'bid':-1,'ask':1},'origin':'source_order_history_size_cut','future_episode_fate_is_input':False,'prior_R10_one_entry_per_order_cap':'preserved_only_in_R10;separate_repeat_survivor_variants_not_capped_by_R10'},
 'orders':{'marketable_limit_buy':'ask_at_send','marketable_limit_sell':'bid_at_send','time_in_force':'IOC','entry_timeout':'platform_IOC_final_status','partial_fill':'record_actual_filled_quantity_only','entry_no_fill':'record_no_fill_no_position','entry_rejected':'record_rejected_no_position','position_created_on':'platform_execution_report','exit_quantity':'actual_remaining_position','exit_unfilled':'retry_next_valid_complete_group','exit_complete_on':'platform_execution_report','order_ids':'adapter_generated_unique_per_rule_signal_attempt','opposing_rule_orders':'never_net_for_rule_attribution'},
 'report_states':['condition_false','condition_unknown','input_unavailable','zero_direction','armed','confirmation_failed','invalidated','expired','risk_capped','submitted','rejected','no_fill','partial_fill','filled','exit_pending','closed','censored','data_failure'],
 'uniform_admission':{'performance_filter':False,'historical_sign_filter':False,'minimum_support_filter':False,'paper_included_all_registered_candidates':True}
}
r['runtime_semantics']['frozen_linear']['binding_manifest']='MODEL_BINDING_REQUIREMENTS.json'
r['runtime_semantics']['frozen_linear']['missing_binding_action']='MODEL_BINDING_UNAVAILABLE'
(OUT/'INITIAL_RULES_V2.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8')
(ROOT/'INITIAL_RULE_DECISIONS.md').write_text('''# Initial 11-rule runtime clarifications

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
''',encoding='utf-8')
print('Preserved and clarified',len(r['strategies']),'initial strategies; no execution enabled.')
