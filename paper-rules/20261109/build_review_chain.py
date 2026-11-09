import json, gzip, hashlib, subprocess, itertools
from pathlib import Path

OUT=Path('C:/Users/A/markets-paper-rules-20261109')
BASE=Path('C:/Users/A/markets-carry-forward-20261109')
CACHE=Path('E:/Markets/outputs/research-union-20261109/objects')
catalog=json.load(gzip.open(BASE/'delivery/SOURCE_REGISTER.json.gz','rt'))
sources={}
def source(alias, prefix):
    rows=[r for r in catalog if r['git_blob_sha'].startswith(prefix) and 'reanalysis/claude' not in r['path']]
    r=next((r for r in rows if 'canonical-sources' in r['path']),rows[0])
    sha=r['git_blob_sha']; p=CACHE/sha
    if not p.exists(): p=BASE/'documents'/f'{sha}.md'
    b=p.read_bytes(); actual=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
    assert actual==sha,(alias,actual,sha)
    sources[alias]={'git_blob_sha':sha,'verified_git_blob_sha':actual,'source_path':r['path'],'local_path':str(p),'url':r['source_url'],'bytes':len(b)}
    return b.decode('utf-8')
texts={}
for a,p in [('index','f2e4d5517b52'),('v4','d91202800047'),('canonical','834247542933'),('ssos_producer','d323aab34ba77'),('lineage','aee92e84e562'),('recurrence_producer','a5412ce2d09f'),('novelty','fd510cfeace5'),('postexit','76181c241deb'),('timing','b7f70cc83c02'),('phase2','0fcb24e77a1a'),('pox_branches','78968bb102ee'),('pox_correction','9ece0900e2c5'),('recovery','06d083ca94b7'),('watch','62a12bd59484'),('entry_extension','697bcc48dd09'),('focused_pox','8fe24304a9e4'),('continuous','bf450aa8aa40'),('contract','eca142a055c9')]:
    texts[a]=source(a,p)
commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd='E:/Markets',text=True).strip()
for a,p in [('shape_helper','research/ng_dipole_native_shape_audit.py'),('ssos_freeze','research/NG_EXHAUSTION_CHAIN_PHASE2_PAPER_PLAY_FREEZE_20260817.json'),('management_proxy','research/NG_EXHAUSTION_CHAIN_PHASE2_EXECUTE_RESET_REENTER_CONTRACT_20260818.json'),('d1_rawpath','research/ng_exhaustion_exact_d1_rawpath_20260818.py'),('d1_all_rawpath','research/ng_exhaustion_d1_all_rawpath_entry_20260818.py'),('d1_agents','research/ng_exhaustion_exact_d1_agents_20260818.py'),('entry_protocol','research/NG_EXHAUSTION_ENTRY_TIMING_REVIVAL_PROTOCOL_20260818.md')]:
    sha=subprocess.check_output(['git','rev-parse',f'{commit}:{p}'],cwd='E:/Markets',text=True).strip()
    b=subprocess.check_output(['git','cat-file','blob',sha],cwd='E:/Markets')
    actual=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(); assert sha==actual
    dest=OUT/'review_chain_sources'/sha; dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes(b)
    sources[a]={'git_blob_sha':sha,'verified_git_blob_sha':actual,'source_path':p,'local_path':str(dest),'url':f'https://github.com/DavisAI1974/Markets/blob/{commit}/{p}','bytes':len(b),'source_origin':'original source recovered from local git object, not new analyst reanalysis'}
    texts[a]=b.decode('utf-8')
def cite(a, start, end=None):
    return {'source':a,'git_blob_sha':sources[a]['git_blob_sha'],'line_start':start,'line_end':end or start,'url':sources[a]['url']+f'#L{start}'+(f'-L{end}' if end else '')}
def findcite(a, term):
    for i,l in enumerate(texts[a].splitlines(),1):
        if term in l:return cite(a,i)
    raise ValueError((a,term))
findings=[]
def finding(id,severity,affected,problem,correction,refs):
    findings.append(dict(id=id,severity=severity,affected=affected,problem=problem,proposed_correction=correction,sources=refs))

finding('CHAIN-01','critical',['CH01','CH02','CH03','CM01-CM09'],
 'The prose says structural onset+5/+30 or +60, but the original producer anchors post_endpoint_price at causal confirmation. Characterizer subtracts horizon fields without correcting the anchor. Historical reported means cannot be assigned to the onset implementation without reconstruction.',
 'Keep separate documented-onset and producer-confirmation paper variants; use each variant consistently for entry, exit, +30/+60 classification and +120/+300 recovery. Both receive identical reporting and admission. Preserve historical means as producer-derived evidence; do not silently relabel them. The producer confirmation is onset+2 under three-consecutive-second endpoints, so both holds have equal length but differ in prices.',
 [cite('canonical',255,266),cite('canonical',277,305),cite('canonical',390),cite('ssos_producer',84,114),findcite('ssos_freeze','entry_clock')])
finding('CHAIN-02','critical',['CH01-CH06','CM01-CM09','CT01-CT05'],
 'Canonical identity is retrospective. The detector uses a full UTC-day 85th percentile, a +5 local window, and prominence-ranked nonmaximum suppression over the candidate set. Endpoint confirmation is not proof canonical identity was known. A successor-before-confirmation link is future-derived unless its detector identity was lawfully available then.',
 'Carry event_known_by independently of endpoint confirmation and seed/full-history availability. Canonical-frozen paper variants must record unavailable/late/no-fill when identity arrives after an entry clock, with no backdated order. A separately named streaming discovery rule may be designed but must not impersonate frozen detection. Preserve canonical overlap label for scoring only until knowable. UTC-day closure is a necessary identity wall, not sufficient proof that global refractory selection is settled.',
 [cite('canonical',194,199),cite('canonical',220,251),cite('postexit',11,19),findcite('v4','The remaining hard timing measurement'),findcite('v4','Retrospective canonical `t0`')])
finding('CHAIN-03','high',['CH01','CH02','CH03','CM01-CM09'],
 'Missing precise P/O/S/X math, history completeness and equality boundary. S is a collapsed same-flow seed, not a same-polarity relation. D4 in SSOS is four predecessor states and is not exact Phase-1 D4 membership.',
 'Use the explicit state and causal-history maps below. Require all needed predecessor confirmations+60 <= current t0 in the frozen research history wall, plus feature availability timestamps; do not weaken this to predecessor t0+60. Keep seed maturity and after-endpoint price-history maturity distinct.',
 [cite('canonical',89,103),cite('canonical',315,357),cite('ssos_producer',20,32),cite('ssos_producer',53,81),cite('lineage',120,155)])
finding('CHAIN-04','high',['CM05','CM06','CM07','CM08'],
 'Direction placeholders are unnecessary: the original novelty source explicitly maps OSP->SAME, OSP->FLIP, PSOS->FLIP, SXOO->FLIP to WITH_CURRENT.',
 'Replace direction placeholders with +current_polarity. Label converting the descriptive orientation into a submitted paper order as a present paper-design decision; the source described candidates, not frozen execution rules.',
 [findcite('novelty','### `OSP -> SAME`'),findcite('novelty','### `OSP -> FLIP`'),findcite('novelty','### `PSOS -> FLIP`'),findcite('novelty','### `SXOO -> FLIP`')])
finding('CHAIN-05','high',['CM01-CM09','CT05'],
 'Nine listed motifs omit the source recurrence atlas, extension families, failed-fold contexts, and the underlying exact-sequence search family. A generic dimensions-to-preserve phrase does not instantiate those candidates.',
 'Expand the motif/extension/context map below and preserve the exact D2-D4 sequence x relation x 30/60-exit search as a deterministic rule generator. Do not retain only patterns passing the old producer minimum-support/top-N/positive-sign presentation filters. Record overlap with trusted SSOS/POX; do not remove overlaps from the common paper ledger. Keep unique-screen results as a historical analytical view.',
 [findcite('postexit','### Reused pairs'),findcite('postexit','### Reused triplets'),findcite('postexit','## 5. D2'),findcite('postexit','## 6. Causal'),findcite('postexit','## 7. Failed'),findcite('phase2','The executable search'),cite('recurrence_producer',45,85),cite('recurrence_producer',100,116)])
finding('CHAIN-06','high',['CH02','CH03','CH04','CH05','CH06'],
 'POX parent, postexit observations, prefixes and focused3429 are separate hypotheses. Source includes absolute-polarity splits and bank-positive +10/+30 management proxy candidates omitted from the register. Prefix watch role is not a complete executable order rule.',
 'Preserve broad canonical POX, same and opposite branches, UP and DOWN strata, both bank-positive proxies, all shallow/deep/mixed states, every prefix, and the separate focused3429 lineage. Source-frozen parent exits +60. Additional prefix/dynamic management trades are separately named paper-design variants, never retrospective edits to the original parent ledger.',
 [findcite('pox_branches','## Additional hypothesis'),findcite('management_proxy','rule_plus10'),findcite('management_proxy','rule_plus30'),findcite('recovery','## Population'),findcite('watch','global_causal_watch_ladder'),findcite('focused_pox','FIXED_3429_DO_NOT_REOPEN')])
finding('CHAIN-07','critical',['CT01','CT02','CT03','CT04','CT05'],
 'Exact-D1..D5 are retrospective all-model-positive lineage labels. CHOP_ROTATION, elapsed-time GMM family, and eventual chain termination are also revealed-path labels, not causal entry triggers. The historical D1 path code additionally calls endpoint confirmation detector_confirm_idx and uses a future descendant t0 as its exit boundary.',
 'Retain exact labels for outcome and cohort reporting; use a separately versioned causal predictor/state with feature availability for trading. No exact depth, realized shape, final duration, or natural historical boundary may enter an earlier order decision. Do not sell at last trade before an unknown descendant event as though that were executable. Explicitly separate endpoint confirmation and detector-mark clocks.',
 [cite('lineage',120,155),findcite('d1_rawpath','def fit_shape_model'),findcite('d1_rawpath','no claim that realized'),findcite('d1_all_rawpath','detector_confirm_idx'),findcite('d1_all_rawpath','STRUCTURAL_EXIT_PRICE_RULE') if 'STRUCTURAL_EXIT_PRICE_RULE' in texts['d1_all_rawpath'] else findcite('d1_all_rawpath','structural_exit_price_rule'),findcite('continuous','These are research characterizations')])
finding('CHAIN-08','critical',['CT03','CT04'],
 'The register stops at the August18/19 fixed-horizon hierarchy; the authoritative August20 continuous-instance correction and V4 clean source explicitly supersede fixed PRIOR/T0/H scanning as the current architecture. Earliest correct / durable correct are hindsight scores, not permissible lock rules.',
 'Preserve old grids and all outputs as comparison/history variants, without claiming them current V4 discovery. Current paper timing evaluates immutable causal snapshots every second, seals the first causal lock, and later annotates PRIOR/T0/H. Retain early and fallback lanes with the same evaluation protocol; absence of early causal inputs permits later availability, while poor historical performance must not exclude a candidate. Frozen first-lock thresholds/model artifacts still need binding or declared new paper-design rules.',
 [cite('continuous',3,20),findcite('continuous','first_durable_correct'),findcite('continuous','No 2-of-3 vote'),findcite('continuous','audit/comparison evidence only'),findcite('v4','## 10. Immutable'),findcite('v4','## 11. Sealed')])
finding('CHAIN-09','high',['CH02','CH03','CT01-CT05'],
 'Focused POX fixed3429 has future FLIP/SAME labels and cannot be rebuilt from 679 canonical adjacent POX observations. V4 labels the fixed POX branch oracle-conditioned/posthoc; candidate/control identity and label-reveal clocks remain necessary.',
 'Maintain both source populations with separate namespace, IDs and provenance. Test initial continuation before later branch selection; reveal FLIP/SAME only at its proper clock. Include oracle-conditioned rows in the common report but do not present their oracle labels as an online signal. Missing master-ledger joins stay explicit implementation limitations with retained case rows.',
 [findcite('focused_pox','total'),findcite('focused_pox','Do not treat the older 679'),findcite('focused_pox','FLIP/SAME is a future label'),findcite('v4','The fixed POX branch')])
finding('CHAIN-10','high',['all reviewed CH/CM/CT'],
 'paper_included=true and definition_or_source_binding_pending are inventories, not platform paper rules. No concrete per-candidate clocks, order lifecycle, risk/rejection/missing-data outcomes, version-bound inputs or common report protocol exist in these entries.',
 'Attach executable declarative contracts for every exact rule or paper-design variant, and retain a row for every match/nonmatch/unknown/late/no-fill/rejection/censoring outcome. Use identical costs/reporting across candidates. Keep source rules and new operational choices separate. Do not claim these become operational merely by naming them in JSON.',
 [findcite('ssos_freeze','order_semantics'),findcite('v4','Execution is downstream'),findcite('v4','No chain/case is removed')])
finding('CHAIN-11','high',['CT05'],
 'D2/D3 fitted elapsed-time centers are not thresholds, and their mixture component assignments require frozen weights, variances and means. Deriving live short/middle/long from nearest center invents a different classifier.',
 'Carry exact trained GaussianMixture artifacts or mark component assignment unresolved; preserve continuous elapsed age causally. Posthoc timing-family labels may stratify all outcomes, and causal predictions of those families are distinct candidates.',
 [cite('recurrence_producer',88,98),findcite('timing','These are characterization families'),findcite('timing','D4/D5 remain too sparse')])
finding('CHAIN-12','critical',['CT01','CT02','CT03'],
 'Original D1 raw-path loaders truncate timestamps to integer seconds and sort by (second, price), reordering trades within a second. This can make the first/last trade marks the minimum/maximum price of that second rather than actual tape order.',
 'Preserve historical producer results with their source revision and this defect. The platform paper adapter must retain event/receive timestamps and authoritative sequence order; use the first actually observable eligible trade/quote after decision. Do not silently attribute original sorted-price fills to a causal execution simulation. Apply the same corrected adapter to all candidates; retain missing sequence/ordering as an explicit input-integrity outcome.',
 [findcite('d1_rawpath','pts.sort();return pts'),findcite('d1_all_rawpath','pts.sort(key=lambda z: (z[0], z[1]))')])

states={
 'input':'Per-second classified aggressor buy/sell volume; roll20=(sum_buy-sum_sell)/(sum_buy+sum_sell) over trailing inclusive seconds t-19..t. Undefined if denominator zero. Original source classifies trade price above/below concurrent BBO midpoint; midpoint ties unclassified. Do not silently substitute native aggressor flow.',
 'polarity':'p=+1 if roll20(t0)>0 else -1; zero/undefined t0 is invalid-data status retained in ledger.',
 'post_curve':'p*roll20(t0+j), j=0..60; original fill_curve forward fills then backward fills leading missing values. State availability includes all contributors; a causal implementation must not backfill from later observations into earlier state.',
 'zero_onset':'first j in 1..58 with three consecutive finite oriented values <=0 at j,j+1,j+2; None if absent through +60.',
 'late_pressure':'For seconds t0+41..t0+60 inclusive, A=volume aligned with event polarity, B=opposite volume; L=(A-B)/(A+B) if positive denominator, otherwise None.',
 'P':'zero_onset is None -> persistent_exhaustion',
 'X':'zero_onset exists AND (L is None OR abs(L)<1e-12) -> collapsed_sparse_indeterminate',
 'S':'zero_onset exists AND L>0 (after X test) -> collapsed_same_flow_reload',
 'O':'zero_onset exists AND L<0 (after X test) -> collapsed_opposite_flow_reversal',
 'structural_endpoint':'Starting t0+1, carry last finite raw roll20 forward; first run of 3 p*value<=0 gives e=first second and c=e+2 confirmation. No endpoint if no such run before actual weekly last trade.',
 'seed_available_at':'At least t0+60 and latest input availability and event_known_by. A seed computed from the full +60 curve cannot be used at t0.',
 'history_h60':'For each immediate predecessor: c exists, c+60<=current t0; displacement/MFE/MAE finite and uncensored at c+[5,10,20,30,60]; next_same_polarity non-null in original producer. Online version must reconstruct that relation only after successor identity is known.',
 'relative_polarity':'SAME iff p_current==p_latest_predecessor, FLIP otherwise. This is distinct from seed-state S.',
 'sources':[cite('canonical',89,103),cite('canonical',147,198),cite('canonical',255,266),cite('canonical',315,357),cite('shape_helper',137,168),cite('ssos_producer',53,81)]
}

base_rule={
 'scope':'canonical seed-chain namespace; ordered immediate predecessors in continuous trading week; no midnight/date/file reset',
 'match':'exact predecessor seed string and optional SAME/FLIP current-versus-latest relation',
 'availability':'all match fields lawful at decision; original h60 historical wall checked separately from actual online event_known_by; no current +60 seed input',
 'clocks':{'documented':'entry=e+5; default exit=e+60; SSOS frozen exit=e+30','producer_comparison':'entry=c+5; default exit=c+60; SSOS exit=c+30'},
 'endpoint_gate':'c<=e+5. Successor-before-confirmation condition <=c follows original producer, but only causal observations may block a prospective order; uncertain retrospective identity is unknown-input, not guessed.',
 'side':'orientation*p_current; +1 WITH_CURRENT, -1 AGAINST_CURRENT',
 'fills':'Original source marks carried last-trade prices and gross ticks, not executable spread/queue fills. Concrete platform fill/latency/cost/risk/duplicate rules are required paper-design decisions shared across all candidates.',
 'exit_reset':'Exit at variant clock; reset trade ownership after flat; any later reentry is a new signal/trade ID; no automatic reversal',
 'retention':'Keep all observations and all outcomes, including unknown identity, missing price, censored endpoint, late signal, no fill, rejection and overlap. No performance admission gates.',
 'design_disclosure':'The source atlas did not freeze reversal orders; executing oriented descriptive motifs as paper orders is a present design decision.'
}
orientation={
 'OOSS->FLIP':-1,'SOOS->SAME':1,'OOO->SAME':-1,'XSX->FLIP':-1,
 'OSP->SAME':1,'OSP->FLIP':1,'PSOS->FLIP':1,'SXOO->FLIP':1,
 'S->SAME':1,'X->FLIP':1,'PS->SAME':1,'OOS->SAME':1,'SOS->FLIP':1,'OSX->FLIP':1,'OOX->FLIP':1,'POO->SAME':1,'XOO->FLIP':1,'POX->FLIP':1,'SOX->SAME':-1,
 'OOO->FLIP':1,'POX->SAME':1,'O->FLIP':1,'P->FLIP':1,'SS->SAME':1
}
contexts={'OOO->FLIP':['XOOO','POOO','OOOO','SOOO'],'O->FLIP':['PO','OO','SO','XO'],'P->FLIP':['OP','PP','SP','XP'],'SS->SAME':['OSS','SSS','PSS','XSS'],'POX->SAME':['PPOX','OPOX']}
module_map={
 'causal_predecessor_motifs': [{'motif':m,'source_orientation':o,'paper_side':('p_current' if o==1 else '-p_current'),'interpretation':'source observed orientation, not an admission/performance rank'} for m,o in orientation.items()],
 'all_contrary_orientation_variants':'If the common paper design tests both directions, opposite orientations must be marked design additions rather than source sign changes; preserve historical original sign and all regimes.',
 'pair_modules':['PP|S','PO|S','OO|F','OP|F','XP|F','SS|S','PP|F'],
 'triplet_modules':['PPP|SS','PPX|SS','OOO|FF','PPS|SS','POP|SF','XPP|FS','OPO|FS','PXP|SS'],
 'timing_context_pairs':['XS|F','SX|S','XX|F','XO|F','PP|F','XP|S','PX|F','XP|F','PP|S','OO|S','OS|S','OX|F','SO|S','SO|F','SS|F'],
 'extension_hypotheses':{'D1_to_D2':['PP|S','XP|F','PP|F','OP|F'],'D2_to_D3':['OPO|FS','XPP|FS','PXP|SS']},
 'longer_context_variants':contexts,
 'module_semantics':'P/O/S/X characters are consecutive seed states oldest to newest; right of | each S/F is relative polarity of each later module member to the prior. Module membership cannot be known before all its seed states and event identities are known. Extension target is later event/lineage continuation, not the future label as input.',
 'source_search_generator':{'predecessor_depths':[2,3,4],'alphabet':['P','O','S','X'],'relations':['UNSPLIT','SAME','FLIP'],'exit_offsets_seconds':[30,60],'entry_offset_seconds':5,'orientation':'source-selected direction preserved where present; both-direction exploration is a labelled paper-design expansion','admission':'none by count, p-value, sign, held result or overlap'},
 'additional_exploratory_atlas_generator':{'predecessor_depths':[1,2,3,4],'alphabet':['P','O','S','X'],'relations':['SAME','FLIP'],'exit_offsets_seconds':[60],'note':'The producer only printed sufficiently supported cells. Do not turn its presentation filter into paper membership.'},
 'complete_pair_triplet_generator':{'seed_lengths':[2,3],'seed_alphabet':['P','O','S','X'],'order':'oldest_to_newest; all Cartesian products, never permutation normalized','relative_polarity_alphabet':['S','F'],'relative_polarity_length':'seed_length-1','dimensions':['source lineage context','extension stage','posthoc exact-depth cohort','posthoc timing-family','absolute first polarity UP/DOWN'],'pair_count':32,'triplet_count':256,'current_seed':'Only included when final member seed is actually known; module uses full member seed sequence. It is incompatible with entry at that member t0 before +60 maturity.','direction':'Module recurrence/extension source itself does not define trade side. Two explicit paper-design arms +latest_known_member_polarity and -latest_known_member_polarity preserve symmetry; do not call either source-frozen.','exit':'Paper-design 25s and55s holds from causal delayed entry mirror source trade holding durations; declare these additions.'},
 'reveal_safe_paper_variants':{'original_fixed_clock':'Preserve source fixed entry/exit clock exactly. If ANY required label/input is unavailable at entry, emit INPUT_UNAVAILABLE/NO_ENTRY; do not backfill.','delayed_causal_entry':'New paper-design variant: enter at first platform decision tick >= max(original_entry_clock, all required actual input/identity/label known_by times). Do not require future success/remaining-life forecasts.','delayed_exit':'New paper-design variant exits 25s (source +30 vs+5 family) or55s (source +60 vs+5 family) after its own fill; source original exit remains a distinct row. Missing fill yields NO_FILL.','current_seed_clock':'max(current t0+60, every contributing input availability, current event_known_by), never current t0.','current_relation_clock':'max(current event_known_by,current polarity_available_at,latest predecessor identity/polarity available_at); SAME/FLIP here means contemporary relation, not focusedPOX future label.','focused_future_branch_clock':'Authoritative branch_label_revealed_at plus all inputs; currently unbound. Unknown reveal clock yields INPUT_UNAVAILABLE; do not replace it by current event polarity or a guessed +60.','final_depth_or_duration_clock':'Final-depth/duration outcome availability requires all gains/outcomes establishing terminal label. Such conditioned versions are labelled posthoc-conditioned delayed designs, not live early prediction; independently predicted-depth variants need causal model output.','direction':'For every source orientation retain it; where no source side exists instantiate both WITH and AGAINST latest causally known polarity with paper-design labels.','state_reset':'Separate signal and position ledger per variant; one fill per signal+variant; after exit reset position ownership; later matched setup creates new ID. Same common execution and reporting for every arm.'},
 'sources':[findcite('phase2','The executable search'),cite('recurrence_producer',100,116),findcite('postexit','## 3. Phase'),findcite('postexit','## 6. Causal'),findcite('timing','## 4.'),findcite('novelty','## Higher-magnitude')]
}

pox={
 'canonical_parent':{'sequence':'POX','side':'p_current','entry':'e+5 documented / c+5 producer','exit':'e+60 documented / c+60 producer','branches':['UNSPLIT','SAME','FLIP'],'absolute_polarities':['UP','DOWN'],'note':'No ranking/admission distinction between branches or polarities.'},
 'proxy_management_variants':[{'id':'POX_BANK_POSITIVE_10_ELSE_60','rule':'At anchor+10, if current oriented mark-to-entry return>0 exit; otherwise exit anchor+60.'},{'id':'POX_BANK_POSITIVE_30_ELSE_60','rule':'At anchor+30, if current oriented mark-to-entry return>0 exit; otherwise exit anchor+60.'}],
 'proxy_status':'Original exploratory proxies preserved as candidates; later settled parent doctrine does not silently replace their source history. New active paper registration explicitly declares these as separate variants.',
 'postexit_labels':{'population':'POX SAME parents with R60<0; retain all others in parent ledger','shallow30':'R30>=-1 tick','deep30':'R30<=-2 ticks','shallow60':'R60==-1 tick','deep60':'R60<=-2 ticks','cells':['shallow/shallow','shallow/deep','deep/shallow','deep/deep','other/undefined'],'recovered':'R120>=0 OR R300>=0','relapse':'R120>=0 AND R300<0','note':'R_h is return from anchor+5 entry. Labels +30/+60 knowable at exit only; recovery is later outcome, never earlier trigger.'},
 'prefixes':{'POX':['P','PO','POX'],'SSOS':['S','SS','SSO','SSOS']},
 'source_prefix_roles':{'P':'background_only','PO':'background_only','POX':'armed_watch','S':'background_only','SS':'background_watch','SSO':'early_watch','SSOS':'armed_watch'},
 'prefix_paper_design_needed':'The historical prefix rule only emits a watch state. To trade prefixes, choose and label a new causal entry/direction/exit contract; retain source watch-state completion outcomes under the same reporting. Do not pretend the source prescribes a trade at P or PO.',
 'trusted_reentry':'After flat/reset, first later fully causal SSOS or POX FLIP setup; separate signal/trade ledger. Clean-reset annotation asks whether each predecessor h60 became available after reset; raw predecessor t0 after reset is a distinct stricter annotation, not same condition.',
 'focused3429':{'fixed_total':3429,'future_flip':1546,'future_same':1883,'identity':'authoritative fixed ledger, never canonical adjacency reconstruction','sequence':'initial continuation first; later causally predicted/revealed branch management','unknowns':['master ledger exact rows/join binding','honest candidate/control universe for identity prediction','label reveal timestamps','frozen causal predictor and lock','specific management economics rule']},
 'sources':[findcite('pox_branches','## Additional hypothesis'),findcite('management_proxy','supporting_fixed_checkpoint_proxy'),findcite('recovery','## Population'),findcite('recovery','## Exit-known'),findcite('watch','global_causal_watch_ladder'),findcite('postexit','### Clean-reset'),findcite('focused_pox','population_contract')]
}

depth={
 'retrospective_definition':'For origin i, D=max consecutive d starting1 such that all ridge/extra_trees/knn full-view structural OOT incremental_gain(d,target=i+d)>0; first missing or nonpositive model gain ends the consecutive prefix. Exact-Dd means maximum consensus depth equals d, not merely d predecessors.',
 'counts':{'exact_D0':135860,'exact_D1':18837,'exact_D2':1592,'exact_D3':124,'exact_D4':8,'exact_D5':1},
 'birth_cohorts':{'D1':{'births':20562,'executable_stops':135823,'censored_stops':37},'D2':{'births':1725,'stops':18837},'D3':{'births':133,'stops':1592},'D4':{'births':9,'stops':124},'D5':{'births':1,'stops':8}},
 'causal_use':'Exact depth and full path class are reporting targets only. Every causally scored candidate remains, including incorrect/no-lock/late predictions. The original all-model rule defines the historical label; it is not a voting/admission rule for current V4.',
 'path_math':{'path_efficiency':'abs(P_end-P_start)/sum(abs(delta_P)); 0 if zero denominator','endpoint_to_excursion_efficiency':'abs(signed_endpoint_ticks)/max(abs(MFE),abs(MAE)); 0 if zero denominator','two_sidedness':'min(max(MFE,0),max(-MAE,0))/max(max(MFE,0),max(-MAE,0)); 0 if zero denominator','shape_fit':'clip each ratio into [1e-6,1-1e-6], logit, train-fitted StandardScaler, 2-component GMM random_state20260818 n_init30; CHOP_ROTATION component minimizes inverse-logit centroid path_efficiency+endpoint_to_excursion_efficiency-two_sidedness; other=DIRECTIONAL','versions':'Early rawpath uses origin confirmation+60 to descendant t0, later all_rawpath uses origin endpoint confirmation to descendant t0. Both are historical source versions; neither proves canonical identity at endpoint confirmation. Preserve frozen trained artifacts per version.'},
 'current_timing_contract':{'start':'latest lawful availability of required predecessor inputs; never derive a live start from future target t0','step_seconds':1,'features':'all lawful structural/price/flow/dipole/book/context snapshots; immutable as-of records','lock':'first crossing of a prospectively frozen causal lock rule; thresholds/model identifiers are required and not specified by these prose sources','first_correct_and_durable':'truth-dependent evaluation only, never lock criteria','coordinates':'After scoring, compare lock to canonical target t0 -> PRIOR lead / T0 / H+N; exactD0 uses candidate-relative reporting','fallback':'Do not delay an already emitted early signal; separately record late-availability and later-lock variants. Do not delete or rank by historical performance.','end':'Historical natural boundary used for scoring must not act as a future-known execution exit; execution exits require their own causal rule.'},
 'historical_grid_versions':{'entry_revival':[1,2,3,4,5,10,15,20,30,45,60,90,120,180,300,600,900,1800,3600],'chain_birth_prior':[1,2,3,4,5,10,15]+list(range(20,3601,5)),'chain_birth_rule_ready':'max(predecessor confirmation_idx+H), require <=target t0 for retrospective PRIOR eligibility; true live availability also requires event_known_by','status':'Preserved source comparison/history, not current V4 discovery architecture'},
 'sources':[cite('lineage',120,155),findcite('index','Frozen conditional birth cohorts'),findcite('v4','Current clean support'),cite('d1_rawpath',31,68),findcite('d1_all_rawpath','def fit_shape'),findcite('continuous','## Core rule'),findcite('continuous','## Per-instance outputs')]
}

missing=[
 {'item':'Actual frozen event_known_by / discovery mark','impact':'No canonical prospective order can truthfully use a historical t0 as event knowledge. Endpoint confirmation, source-day close, and event mark are distinct.','resolution':'Instrument or bind a proven first-known event stream; alternatively define separate replay detector, with new identity and changed population explicitly declared.'},
 {'item':'Causal first-lock model, frozen coefficients, thresholds and maturity/reveal rules','impact':'Continuous V4 contract specifies architecture and ledgers, not one exact trading signal.','resolution':'Bind exact existing model artifacts or declare new paper-design model and lock choices; keep every candidate without performance admission.'},
 {'item':'Exact GMM fitted weights, covariance, scaler and trained cohorts','impact':'Source code describes training; centers alone do not reproduce timing or shape assignments.','resolution':'Bind frozen trained model artifact hashes or leave historical labels as supplied; do not nearest-center substitute.'},
 {'item':'Prefix, range/fade/rotation, survival/hazard, extension-to-order rule math','impact':'Sources identify opportunity/state hypotheses but do not choose executable thresholds, side or exit.','resolution':'Declare concrete new paper-design contracts separately from source original semantics. All should receive common testing, including contrary branches.'},
 {'item':'Focused3429 master identities and reveal metadata','impact':'Canonical679 cannot substitute; future branch identity cannot enter first trade.','resolution':'Bind fixed ledger artifact and candidate control universe.'},
 {'item':'Source input manifests and platform adapter/fill semantics','impact':'Original gross last-trade marks do not establish actionable broker fills; byte-exact detector inputs, tick mapping, session, event/receive/source ordering need binding.','resolution':'Use shared platform paper adapter and retained no-fill/late/error statuses; label common operational choices.'}
]

report={'review_scope':'Read-only adversarial review of CH/CM/CT carry-forward register and original chain sources. No workers, research suites, migration or other agents started; no parent artifact edited.','artifact':str(BASE/'delivery/HYPOTHESIS_REGISTER.json'),'decision':'CH/CM/CT entries are not complete explicit platform PAPER contracts. Recoverable math and additional hypotheses are supplied here; genuine source-definition gaps remain explicit.','user_policy':'Every candidate and outcome retained under same paper testing/reporting; no historical-performance ranking or admission; preserve source versions, while authoritative corrections determine current interpretation.','findings':findings,'explicit_maps':{'seed_and_endpoint':states,'common_seed_motif_contract':base_rule,'recurrence':module_map,'pox':pox,'depth_and_timing':depth},'unresolved_definitions':missing,'sources':sources,'verification':'Every source byte payload used for citations has Git blob SHA1 verified. Additional original files read from pinned local git commit via cat-file, not working-tree assumptions.','local_original_commit':commit}
OUT.mkdir(parents=True,exist_ok=True)
(OUT/'review_chain.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'output':str(OUT/'review_chain.json'),'findings':len(findings),'verified_sources':len(sources),'bytes':(OUT/'review_chain.json').stat().st_size}))
