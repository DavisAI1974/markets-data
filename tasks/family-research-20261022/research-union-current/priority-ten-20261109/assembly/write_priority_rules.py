"""Freeze auditable prospective paper hypotheses; no execution or backtest claim."""
import json
from pathlib import Path
P=Path(__file__).parent/'priority-now'
rules={
 'version':'priority-paper-v1-20261109',
 'status':'Specification complete; prospective paper hypotheses; not connected or running',
 'scope':'Standard NG futures only; one explicitly configured contract. No continuous-contract roll or MNG substitution.',
 'evidence':'All four October 2023 sessions are discovery data. Rules below have not been backtested as a strategy or validated on unseen sessions.',
 'parameters':{'paper_contracts':1,'max_total_open_contracts':1,'max_entries_per_session':20,'stop_ticks':4,'session_loss_ticks':12,'max_hold_seconds':120,'cooldown_seconds':30,'max_spread_ticks':2,'max_quote_age_ms':1000,'max_group_silence_ms':1000,'flow_windows_seconds':[5,60],'confirmation_timeout_seconds':5,'invalidation_persistence_ms':1000,'assumed_tick_size':'0.001','tick_value_usd':10,'fees_round_turn_usd':None,'execution_adapter':None,'contract_id':None,'session_start_utc':None,'session_end_utc':None},
 'parameter_status':'All thresholds, lookbacks, ordering, sizing and risk caps are provisional operational choices, not estimated optima. Freeze before the first prospective session; changes require a new version.',
 'clock_and_input_contract':[
  'Process one complete exchange message group at a time, deduplicated by session, instrument, source cursor and record ordinal. Decision t is the local receive time at which that entire group is available. Preserve receive ns, event ns, source cursor, group and local monotonic times independently as exact integers/text.',
  'Use only events received and completed by t. Any source feature with known_by_ns > t is unavailable. A calendar label or scheduled sample time never grants availability. Never use the final birth/cohort, recognition outcome, end_kind, fate, future return or matched-control selection in an entry.',
  'Reconstruct the current displayed bid/ask and order-ID ledger from an initial snapshot plus uninterrupted ordered messages. Unknown trade direction is counted separately and never inferred from a later quote. Only explicit source aggressor classification contributes to flow.',
  'B_w and S_w are classified buy/sell aggressor quantities in complete groups with receive times in (t-w seconds,t], for w=5 and 60. F_w=(B_w-S_w)/(B_w+S_w); zero denominator is MISSING, not balanced. Require a complete 60-second warmup. Recompute from admitted native events; do not use scheduled historical bucket values early.',
  'I_touch=(displayed bid lots at current best bid - displayed ask lots at current best ask)/(their sum). Both quotes and both sizes must be positive and known by t. I_touch is separate from full-depth imbalance and from a price move.',
  'Reject entries on missing/reset/gap/out-of-order input, crossed or locked quotes, nonpositive sizes, quote age >1000ms, group silence >1000ms, spread >2 ticks, or any unknown instrument/session mapping. These provisional age/spread limits are not estimated from the selected studies.'
 ],
 'strategies':[
  {'id':'R1','name':'Fresh flow with touch-book agreement','mode':'paper candidate',
   'sources':['P01 Fresh versus expiring flow','P02 Flow depth and refill','P03 Four arm entry candidates','P10 Price flow book context'],
   'trigger':'At complete group g, require a newly observed classified aggressor trade in g. Let d=sign(F_5). Require d !=0, sign(F_60)=d and sign(I_touch)=d, with all three defined. Arm only on false-to-true transition of this combined condition; store g, t, best bid and best ask. An expiry-only flow change cannot arm.',
   'confirmation':'In a strictly later complete group within 5 seconds of arming, require both best bid and best ask to be >= one tick above the armed quotes if d=+1, or <= one tick below if d=-1. Re-evaluate all three signs and input gates at this group. If any sign/gate fails, or 5 seconds elapse, disarm. Same-group price movement does not confirm. Consume the arm on first confirmation.',
   'entry':'Buy one paper contract for d=+1, sell one for d=-1, using the shared marketable IOC model. Never fill at the armed quote or midprice.',
   'invalidation':'Exit if sign(F_5) or sign(I_touch) differs from entry d, including balanced or missing, in at least two complete groups spanning >=1000ms continuously. Any intervening valid agreement resets the timer. Missing/gap data also invokes the immediate data-failure rule.',
   'interpretation':'Tests whether fresh agreement plus subsequent price confirmation is useful. Four-arm fixed-horizon responses do not prove this composite rule profitable.'},
  {'id':'R2','name':'Observed absorption with price confirmation','mode':'paper candidate',
   'sources':['P04 Order identity lifecycle','P05 Observable resting state','P07 One lot order origins'],
   'trigger':'Track an order only if a trade T followed by add A with the same source order ID and side occurs in one complete group and the residual is visible at that group close. Define d=+1 for a resting bid and d=-1 for a resting ask. After that group, require an explicitly linked passive fill F for the same order; at the close of the fill group it must still have positive displayed residual at the best quote. Record the current bid/ask and arm. Do not infer hidden reserve, trader identity or intent.',
   'confirmation':'In a strictly later complete group within 5 seconds, require both quotes to move at least one tick in d relative to the armed quotes. At confirmation the same tracked order must still be displayed at its resting-side best quote with positive residual; sign(I_touch)=d and F_5 defined with sign(F_5)=d. Any cancellation, reprice, reset, zero residual, loss of touch, opposite/missing sign, or gate failure disarms. Consume the order arm on first confirmation; no second entry from that order in the session.',
   'entry':'Buy one paper contract for resting bid support; sell one for resting ask resistance. Use shared marketable IOC; observing another order fill is never our own fill.',
   'invalidation':'Exit immediately at the first subsequent executable observation if the tracked order is gone, repriced, no longer at touch, or has zero displayed residual. Also apply R1 persistent flow/book invalidation and the shared stop/time/data rules.',
   'interpretation':'Tests an observable surviving-order mechanism. Final order fate is excluded. The source survival fractions are not entry fill probabilities.'}
 ],
 'fill_and_exit_model':[
  'No passive queue-fill assumption. Submit a one-contract marketable IOC to the paper adapter only after confirmation and capacity checks. Store decision, send, arrival, acknowledgement and fill times. Missing arrival/latency evidence means signal-only, not a fabricated fill.',
  'If using an instrumented quote simulator, the first complete, valid group strictly after confirmation and at/after measured order arrival supplies the executable quote: ask for buys, bid for sells. Require displayed executable size >=1. Fill exactly one or zero; zero fill cancels IOC and consumes the arm. Unknown quote state or size means no fill. Record the quote cursor and actual latency; never assume a 0/5/25/100ms schedule is latency.',
  'Adverse slippage sensitivity: alongside executable-quote gross PnL record a separate scenario adding one tick against every entry and every exit. This is a declared stress scenario, not a measured fill. Net PnL is unavailable until configured broker/exchange fees are supplied; never default them to zero.',
  'Mark long positions to current executable bid and shorts to current executable ask. Request exit on the first of: adverse marked move >=4 ticks from entry fill; strategy invalidation; elapsed time >=120 seconds from actual entry fill; session-end boundary; session loss limit; input failure. No profit target and no automatic reversal. Hard-stop trigger is not a guaranteed fill price.',
  'Exit with an opposite one-contract marketable IOC using the same next-observed-arrival quote rule. If unfilled, remain open and retry on the next valid complete group until flat; permit no new entries. If data are unavailable, mark exit pending/unresolved and do not invent a price or claim flat. Record any loss-limit overshoot.',
  'On input failure, cancel pending entries and request flattening through the paper adapter. Pause new entries until a fresh snapshot, ordered continuity, 60-second flow warmup and explicit operator resume are recorded. There is no automatic resume after a loss-limit stop.'
 ],
 'portfolio_and_session':[
  'At most one contract total across R1 and R2; no scaling or averaging. If both confirm in the same group while flat, R1 wins and R2 is logged as suppressed. Signals while open are logged but cannot add or reverse.',
  'After any filled exit, wait 30 seconds before a new arm. IOC entry failure does not reopen the consumed arm; require a new false-to-true R1 condition or a different R2 order. Stop after 20 filled entries in the configured session.',
  'Disable new entries and request exit when realized plus executable-marked unrealized gross PnL <= -12 ticks, or fee-adjusted PnL <= -12 ticks if fees are configured. Track gross and net distinctly. Never reset this limit intraday. Restart only at the explicitly configured next session with an operator record.',
  'Exact session UTC start/end, instrument expiry, paper adapter, fees and measured arrival clock mapping are required before activation. Reject entries in the last 120 seconds of the configured session. A session or contract roll closes the old paper exposure; it is never stitched across prices.'
 ],
 'observation_only':['Expiry-only flow changes','Retrospective dipole birth or prebirth-control labels','Unverified 0.5-second warning claim','Final order fate or future outcomes','Disagreement/neutral/missing-flow arms: retain signals and subsequent outcomes for comparison; do not silently delete them'],
 'logging':{'keys':['rule_version','session_id','instrument_id','strategy_id','signal_id','source_group','source_cursor','source_receive_ns','decision_receive_ns','feature_known_by_ns','local_send_ns','local_arrival_ns','ack_ns','fill_ns','latency_ns','side','quantity','bid','ask','bid_size','ask_size','F5','F60','I_touch','native_buy5','native_sell5','native_unknown5','order_id_if_R2','arm_reason','gate_results','rejection_or_suppression_reason','fill_quote_cursor','entry_price','exit_reason','exit_price','gross_ticks','fee_usd','net_ticks','stress_ticks','data_quality_state'],
 'review':'After the first prospective session compare signal-to-fill attrition, latency, missed/expired arms, every adverse/flat case, stop overshoot, gross/net/stress outcomes and price-before-flow versus flow-before-price. Report denominators per rule/side/session; do not retune on individual wins. Keep the frozen first version and publish any revision separately.'}
}
(P/'PAPER_STRATEGIES.json').write_text(json.dumps(rules,indent=2),encoding='utf8')
md=['# First paper-trade rules — v1, 2026-11-09','',rules['status'], '',rules['evidence'],'', '## Shared parameters','', '| Parameter | Value |','|---|---|']
md += [f'| {k} | {v if v is not None else "UNCONFIGURED"} |' for k,v in rules['parameters'].items()]
md += ['',rules['parameter_status'],'','Standard NG tick: 0.001 USD/MMBtu and $10 per contract. [CME specification FAQ](https://www.cmegroup.com/articles/faqs/micro-henry-hub-natural-gas-futures-and-options-frequently-asked-questions.html). Historical October 2023 evidence is not MNG evidence.','']
for title,key in [('Clock and input contract','clock_and_input_contract')]:
 md+=['## '+title,'']+[f'{i}. {v}' for i,v in enumerate(rules[key],1)]+['']
for s in rules['strategies']:
 md+=['## '+s['id']+' — '+s['name'],'',f"Sources: {', '.join(s['sources'])}.",'']
 for k in ['trigger','confirmation','entry','invalidation','interpretation']:md += ['**'+k.capitalize()+'.** '+s[k],'']
for title,key in [('Execution and exits','fill_and_exit_model'),('Portfolio and session','portfolio_and_session'),('Observation only','observation_only')]:md+=['## '+title,'']+[f'{i}. {v}' for i,v in enumerate(rules[key],1)]+['']
md+=['## Required log','',', '.join(rules['logging']['keys']), '',rules['logging']['review']]
(P/'PAPER_STRATEGIES.md').write_text('\n'.join(md)+'\n',encoding='utf8')
(P/'PAPER_READINESS.md').write_text('''# Paper readiness — 2026-11-09

The two rules are specified and frozen for a prospective paper trial. They are not running, have not been strategy-backtested, and have no demonstrated net edge. This delivery performs research and workbook preparation, not execution deployment.

Ready: source-linked top-ten additions; four-session cell readback; contrary/flat/missing cases; exact source clocks; deterministic triggers, confirmations, order handling and exits; explicit provisional parameters; shared exposure/loss limits; required logs.

Before activation, the execution adapter must supply the exact NG expiry, paper account, session start/end in UTC, fees, source-to-local clock mapping and measured arrival timestamps. Unknown fees permit gross-only signal analysis, never a net-PnL claim. Missing timing/adapter configuration permits observation only. Confirm tick size/value against the configured instrument rather than substituting a micro contract.

Execution checks: feed a future-dated feature (reject); remove flow warmup (reject); change flow by expiry only (do not arm); confirm in the same group (reject); expire an R2 order before confirmation (reject); trigger both rules (one R1 position); force IOC no-fill (no position); trigger a stop during a gap (exit pending, never pretend flat); hit session loss (no automatic restart). These are acceptance cases for the adapter, not tests claimed to have run here.

The 0.5-second dipole warning remains unverified. The 0/5/25/100ms resting-state samples are schedules, not execution latency. All four historical days have already informed discovery. The next untouched paper session is the first prospective evaluation of these rules.

Deferred by the user's latest instruction: exhaustive branch reconciliation and remaining bulk workbook exports. Existing workers were allowed to finish; none was restarted for this priority pass. Their durable source/packet checkpoints remain available for the next session.
''',encoding='utf8')
print('PAPER RULES WRITTEN',rules['version'])
