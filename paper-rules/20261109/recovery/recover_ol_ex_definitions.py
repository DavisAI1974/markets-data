"""Bounded source extraction; never executes producers or reads market data."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OBJECTS = Path('E:/Markets/outputs/research-union-20261109/objects')
CATALOG = Path('C:/Users/A/markets-carry-forward-20261109/source_catalog.json')
IDS = ['S00008','S00279','S00280','S00281','S00283','S00735','S00736','S01693','S01725','S01727','S01734','S01763','S01769','S01772']
catalog = {r['id']: r for r in json.loads(CATALOG.read_text(encoding='utf-8'))}
sources = {}
for ident in IDS:
    r = catalog[ident]
    data = (OBJECTS / r['sha']).read_bytes()
    actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    assert actual == r['sha'], (ident, actual, r['sha'])
    sources[ident] = dict(source_id=ident, path=r['path'], url=r['url'], git_blob_sha1=actual,
                         sha256=hashlib.sha256(data).hexdigest(), bytes=len(data), local_path=str(OBJECTS / actual))

definitions = {
 'schema':'OL-EX-SOURCE-RECOVERY-v1',
 'scope':'Read-only definition recovery; no producer import/run, market-data replay, refit, backtest, service operation or migration.',
 'sources': sources,
 'register_predicates': {
   'OL01':'onset==NEW_BEST and flow==no_reduction',
   'OL02':'onset==STANDING_BEST_SHRANK and flow==fill_linked',
   'OL03':'onset==STANDING_BEST_SHRANK and flow==unlinked_reduction',
   'OL04':'onset==STANDING_BEST_SHRANK and prior_orders>2',
   'OL05':'onset==STANDING_BEST_SHRANK and prior_orders<=2',
   'OL06':'onset==NEW_BEST and observed_next_level and next_lots<10',
   'OL07':'onset==NEW_BEST and observed_next_level and next_lots>=10',
   'OL08':'flow==fill_linked and observed_next_level and next_lots<10; both onset types retained',
   'OL09':'Retain all causal order origins, age bins, prior-onset bins; subsequent fate/replenishment remains separately clocked event history.',
   'EX03':'Two source populations, ten response targets (next change plus nine fixed horizons), spread and touch strata.',
   'EX05':'Same-order T-to-A identity; four timer delays crossed with four observation horizons, plus separate five-horizon start/end inventory.',
   'missing_contract':'Every predicate has unavailable state if any required evidence absent; absence of next level in a complete book is no_next, not next_ge10 or next_lt10.'},
 'causal_contract': {
   'identity':'Preserve session, instrument, source version, group ordinal, first/close cursors, side/order/event ID. Cursor sequence breaks equal-clock ties; no cross-session order identity inference.',
   'availability':'Use completed group with recorded receive/known-by clock and actual delivery. Historical receive is not proof of earlier deployment availability.',
   'missing':'Missing book, order lineage, group close, tape join, endpoint or clock remains unavailable. An observed empty next level differs from missing book.',
   'retention':'All source populations and censored/ended-before-entry/missing observations remain in outer ledger. Source filters are documented, not promoted to outcome-conditioned entry filters.',
   'trade_mapping':'Recovered source observations and hypothetical entry quote conventions are not fills. Actual fill/execution mapping remains a separately identified adapter.'},
 'OL_onset': {
   'source':['S00280:32-80','S00736:13-43'],
   'predicate':'At completed close current side touch size == 1, and either current price != preceding retained close price or unchanged price with prior size > 1.',
   'labels':{'changed_price':'NEW_BEST, whether improved or worsened','unchanged_price_prior_size_gt1':'STANDING_BEST_SHRANK','same_price_prior_size_1':'no new onset'},
   'prior_touch':'Previous close on same side: [price_raw,lots,order_count]. Opposite touch is current close.',
   'direction':{'B':-1,'A':1},
   'group_filter_source':'S00280 retains only groups with nonempty bid/ask and non-null prices; previous means previous retained group. No initial-row onset. This is not S01763 valid-segment filtering.',
   'unsafe_gap_policy':'A source-skipped missing group must not silently establish live adjacency or uninterrupted episode survival; report unavailable continuity until verified.',
   'recorded_t':'S00736 requires exact onset transition group/cursor/known_by equality and each linked trade available_ns <= signal known_by_ns, matching group close cursor and transition line. Boolean means observed linked T, not fill-linked reduction.'},
 'OL_first_end': {
   'source':['S00280:55-80','S01693:42-75','S00736:33-42'],
   'event':'First strictly later retained group at which touch price differs from onset price or size != 1. Cannot be known before that close.',
   'labels':'Same price => SIZE_RECOVERED_AT_SAME_PRICE (source tests !=1, not >1); B lower/A higher => RETREATED; other changed price => IMPROVED; no observed end => CENSORED (S00280) or WINDOW_CENSORED (S01693).',
   'source_entry':'First completed quote >= onset known_by/receive + 1,000,000ns; S01693 also searches strictly after onset index. Not an actual order fill.',
   'end_vs_entry':'Observed end cursor/group <= observed entry cursor/group => BY_ENTRY including equality, else AFTER_ENTRY. S00736 explicitly emits NO_OBSERVED_END / NO_OBSERVED_ENTRY.',
   'source_bug_to_preserve_not_infer':'S00280 emits AFTER_ENTRY if end exists but no entry exists. Store that source label separately; normalized actionable status is NO_OBSERVED_ENTRY, never assume a fill.',
   'extra_original_wrapper':'S01693 horizons [1,5,30] seconds from hypothetical entry, first quote >= entry+h; entry/exit censoring explicit. Distinct source variant from first-end target; not a replacement.',
   'known_at_onset':['side','onset type','prior touch','current touch','completed onset mutations'],
   'forbidden_onset_inputs':['first end','end_vs_entry','lifetime','later order fate','retreat outcome']},
 'OL_history': {
   'source':['S00735:10-35'],
   'population':'STANDING_BEST_SHRANK only; preserve onset line and exact source coordinates.',
   'window':'Exactly three immediately preceding book closes, excludes onset close.',
   'validation':'For each prior row signal.group-prior.group == signal_index-prior_index, prior.cursor < signal.cursor, prior.known_by_ns <= signal.known_by_ns. Failure is invalid evidence, not a state label.',
   'ordered_classification':['fewer than 3: INSUFFICIENT_PRIOR_BOOKS','any prior touch price != onset new_best_raw: PRIOR_BEST_PRICE_CHANGED','all three sizes equal: FLAT','s0>=s1>=s2: FALLING','s0<=s1<=s2: BUILDING','otherwise: MIXED'],
   'boundary':'FALLING/BUILDING are weak monotonicity with at least one strict change because FLAT checked first; onset size is not included.'},
 'OL_tape_and_identity': {
   'source':['S00008:90-127','S00283:73-135','S00279:65-77','S00281:42-124'],
   'flow':'Capture mutations only within onset first_cursor through close_cursor. Count reductions at original price: nonzero linked_display_reduction => linked reduction; otherwise unlinked; reprices out are separate. fill_linked if linked count>0 else unlinked_reduction if unlinked count>0 else no_reduction.',
   'fill_link':'Book F accumulates same order/current price pending fills; C/M at same price or remove links min(reduction,pending). Clear pending at F_LAST. T is not F.',
   'next_level':'Sort nonempty same-side prices descending B / ascending A at onset close. Second price and sum displayed lots. Observed absent => no_next; size<10 => next_lt10; >=10 => next_ge10.',
   'prior_orders':'Previous touch order_count <=2 => prior_orders_le2, else prior_orders_gt2; missing prior count unavailable.',
   'order_origin':'Require exactly one touch order. Start older_resting. Process onset captured mutations in cursor order for that ID with after at side/onset price: A => fresh_add; M from another price => repriced_in; same-price M reducing size => size_cut_in_place; C => partial_cancel_in_place. Last qualifying assignment wins, not simply last arbitrary mutation.',
   'age':'First observed A timestamp for ID through reset; age_ms=round((onset close receive-first A receive)/1e6,3). Missing first A => none. Bins: <10 under_10ms; <1000 10ms_to_1s; <60000 1s_to_60s; else over_60s. Boundaries use rounded age.',
   'prior_onsets':'Read counter before incrementing for current onset; bins min(counter,3). Original first_seen and open_fates clear on R but onsets_by_order does NOT clear on R: retain source semantics and separate reset-aware deployment choice.',
   'later_fate':'First post-onset-close C/M/F for ID only. M_away if price differs; M_size_up if same price and size>before size; otherwise M_same_price. Future fate and repeat-ID share over whole population cannot gate onset.',
   'source_filters':'S00279 drops missing tape and CENSORED rows, zip joins by list position; causal integration must verify (session,onset_group,side,onset_cursor), retaining excluded observations separately.'},
 'EX03': {
   'source':['S01769:8-46','S01734','S01763:160-169'],
   'populations':{'aggression_to_rest':'event_id, source=start_group, decision=start_known_by_ns (initial completed group recognition)', 'family_prebirth':'instance, source=saved pre_group, decision=anchor_ns-1; retrospective diagnostic, never a post-recognition trade entry'},
   'fixed_horizons_ns':[1000000,5000000,25000000,100000000,250000000,500000000,1000000000,5000000000,20000000000],
   'endpoint':'For fixed target decision+h choose LAST completed group timestamp <= target, including equality (searchsorted right-1). May equal source group and yield valid flat. Target must be <= last retained timestamp; source/end valid and same segment.',
   'next_change':'First strictly later index with different bid_raw+ask_raw along contiguous valid same-segment groups; endpoint receive must be > decision. Invalid row/segment break stops search. No later change => boundary_or_no_later_change, not flat.',
   'spread':'ask_raw-bid_raw: ==1,000,000 one_tick; >1,000,000 wider; otherwise locked_or_other.',
   'touch':'(bid_lots-ask_lots)/(bid_lots+ask_lots). >0 bid_heavy, <0 ask_heavy, exact zero balanced. Original NaN falls through to balanced; preserve source label separately, normalized undefined denominator stays unavailable.',
   'change':'((endpoint_bid+endpoint_ask)-(source_bid+source_ask))/(2*1e9) price units; in ticks divide the same numerator by 2*1e6. No source directional trade fill is implied.',
   'valid_segment':'S01763 good = OPEN<=receive<CLOSE, both sides exist, 0<bid<ask, and none reset_member/snapshot_member/bad_receive_clock_member. Increment segment on each invalid group. Original October18 OPEN=1697580000*1e9 and CLOSE=1697662800*1e9; other sessions require their own source scope, never reuse these calendar constants.',
   'guard':'A family birth group can be first midpoint change one ns after prebirth cutoff. Outcome retained in diagnostic; cannot become a fill after recognition.'},
 'EX05_identity': {
   'source':['S01763:35-80,183-271','S01725'],
   'event':'Within a valid completed group, one or more T records with same nonzero order ID and wire side precede positive-size A matching ID/side. Trade price need not equal add price. pending keyed ID, first T side retained, sums T lots/distinct prices; clear pending at group boundary.',
   'event_id':'rest-{add_cursor}-{order_id}; identity is order event, not participant.',
   'direction':{'B':1,'A':-1},
   'known_by':'Initial completed group close timestamp and cursor. An order that clears within this group is retained with size_at_start_close=0 and visible_at_start_close=false.',
   'F':'Only matching tracked side and price increases cumulative fills and pending; F does not itself reduce display.',
   'C':'after=max(0,displayed-size); partial C is not automatic termination. Match min(pending,display reduction), decrement matched pending.',
   'M':'Changed side or price terminates reprice; same-price M sets displayed=size, matches pending reductions, implied_additions += max(0,after-before+pending), then pending=0.',
   'clear':'At after==0: fill_linked_clear if reduction>0 and matched==reduction; mixed_clear if matched>0; else unmatched_clear. Unmatched clear is not proof of voluntary cancellation.',
   'other_ends':'Duplicate A while tracked => duplicate_add_unresolved; R => reset_censored; retained EOF => session_end_censored. Group boundary accumulates unmatched pending and clears pending.',
   'no_lookahead':'Terminal kind and total lifetime/fills are outcomes. Live survival requires observed completed state and complete continuity, not retrospective end_known_by_ns field.'},
 'EX05_observation': {
   'source':['S01772:16-49','S01727'],
   'delays_ms':[0,5,25,100], 'horizons_s':[0.1,1,5,20],
   'decision':'start_known_by_ns + delay*1e6; quote is LAST completed group <= timer, not next group after timer.',
   'state':'Use only event actions group_known_by_ns<=timer sorted by raw cursor; last provides displayed_after,cumulative_passive_fills. Initial fallback size_at_start_close,fills=0.',
   'eligible_source':'end_known_by_ns > decision strict. Equal end clock means ended already. All decisions retained; source emits outcomes only for eligible decisions.',
   'eligible_causal':'No observed terminating action at completed group <=timer, positive known tracked display at original identity/price, complete source coverage. Unknown lineage/coverage => unavailable. Never consume future end_known_by_ns as timer input.',
   'features':'at_touch = original resting price equals side best on decision quote; fill_fraction=fills_known/initial_display; fill_state=some_passive_fills if fills_known>0 else no_passive_fills_yet. At-touch alone does not establish survival.',
   'outcomes':'Target=decision+h; LAST completed group <=target; target<=last retained time and source/end good and same segment. Direction-oriented midpoint change from decision quote. Missing endpoint=censored_or_boundary, not flat.'},
 'EX05_inventory_outcomes': {
   'source':['S01763:253-271'], 'horizons_s':[1,5,20,60,300],
   'anchors':['start_close','end_close unless end_kind endswith censored'],
   'clock':'Each anchor has own completed close timestamp. Latest completed quote <= anchor+h; same validity/segment endpoint checks.',
   'separation':'This is a distinct outcome grid from observation [0.1,1,5,20]. End-close outcome never becomes onset input; preserve both grids and original populations.'},
 'residual_limits':['No actual platform order/fill adapter supplied by these producers.','No production replay was run; synthetic fixtures check clocks and boundaries only.','Original source quirks are explicitly retained; corrected normalized missingness is not claimed as original research behavior.']
}
(ROOT/'ol_ex_source_bound_definitions.json').write_text(json.dumps(definitions,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'sources_verified':len(sources),'output':str(ROOT/'ol_ex_source_bound_definitions.json')}))
