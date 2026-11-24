# Scout run 155 (Haiku): where things are for ticket 47

Kept word for word as the agent returned it, 2026-11-24 (twenty-fifth session). Nothing below this line is the main session's.

---

Scout run 155, ticket 47. Full report below. Sections 1 to 6 are complete. Section 3 is partly NOT IN THE CHECKOUT (see that section). Tool calls used: 24 of 30. No writes, no sub-agents.

## 1. April engine interface (/home/user/Markets-od-apr5)

Defs (no classes in either file):
- od_engine.py:24 def vec(rho):
- od_engine.py:29 def unvec(v, n=N_SITES):
- od_engine.py:34 def _discover_matrix_log(rho_traj, times):
- od_engine.py:115 def _discover_least_squares(rho_traj, times):
- od_engine.py:157 def recover(t, x):  (entry point)
- od_engine.py:246 def _recover_single(rho_traj, times):
- od_engine.py:282 def _recover_piecewise(rho_traj, times, n_segments):
- od_engine.py:359 def _trajectory_error(L, rho_traj, times):
- benchmark.py:21 def load_dataset(path):
- benchmark.py:53 def compute_r_squared_trajectory(x_true, x_pred):
- benchmark.py:79 def compute_holdout_r_squared(x_true, x_pred, split_frac=0.8):
- benchmark.py:86 def run_benchmark(dataset_path):
- benchmark.py:139 def print_results(metrics):
- benchmark.py:155 def main():

Entry input (od_engine.py:161-176 docstring, quoted):
- "t : np.ndarray" / "Time points, shape (n_t,)"
- "x : np.ndarray" / "Density matrix trajectory, shape (n_t, 5) where col 0 = time, cols 1-4 = rho elements. OR shape (n_t, 2, 2) if already parsed."
- Column indexing (od_engine.py:183-187): rho_traj[:,0,0]=x[:,1]; rho_traj[:,0,1]=x[:,2]; rho_traj[:,1,0]=x[:,3]; rho_traj[:,1,1]=x[:,4]. Other shapes raise at od_engine.py:191.
- Dataset format (benchmark.py:39-40): "Raw spin-boson format: (n_t, 5) complex array"; line 40 is `if data.ndim == 2 and data.shape[1] == 5:`.

Return keys:
- Single fit (od_engine.py:230-242): operator, coefficients, x_predicted, L, metadata.
- Piecewise (od_engine.py:337-355): same five keys; L is a list of per-segment matrices.
- coefficients keys: single (od_engine.py:222-228) eigenvalues_real, eigenvalues_imag, primary_decoherence_rate, method, L_norm; piecewise (od_engine.py:339-346) eigenvalues_real, eigenvalues_imag, primary_decoherence_rate, method, n_segments, L_norms.

Piecewise cut and fit:
- od_engine.py:194 n_segments = getattr(cfg, 'n_segments', 1)
- od_engine.py:196-197 if n_segments > 1: return _recover_piecewise(rho_traj, times, n_segments)
- od_engine.py:288 seg_size = n_t // n_segments
- od_engine.py:289 overlap = getattr(cfg, 'segment_overlap', 0)
- od_engine.py:294-297 fit range: start = max(0, seg * seg_size - overlap); end = min(n_t, (seg + 1) * seg_size + overlap) if seg < n_segments - 1 else n_t
- od_engine.py:299-303: seg_rho = rho_traj[start:end]; seg_times = times[start:end] - times[start]; L_seg, _ = _recover_single(seg_rho, seg_times)
- od_engine.py:304-306: on exception, falls back to the previous segment's L.
- od_engine.py:314-328: reconstruction over non-overlapping ranges (lines 315-316: start = seg * seg_size; end = (seg + 1) * seg_size if seg < n_segments - 1 else n_t), propagating with expm(L_seg * dt) @ v_start.
- od_engine.py:331: coefficients taken from L_list[0].

Holdout (the full-trajectory fit):
- benchmark.py:91 x = np.asarray(dataset["x"])  (full array)
- benchmark.py:98 result = od_engine.recover(t, x)  (whole trajectory in)
- benchmark.py:106 x_pred = np.asarray(result["x_predicted"])
- benchmark.py:110 x_compare = x
- benchmark.py:116 r_squared_holdout = compute_holdout_r_squared(x_compare, x_pred)
- benchmark.py:81-83 n = len(x_true); split = int(n * split_frac); return compute_r_squared_trajectory(x_true[split:], x_pred[split:])
- od_engine.py:200 L_best, best_method = _recover_single(rho_traj, times)  (non-piecewise path, full rho_traj)
- od_engine.py:145 V = vecs[margin:-margin].T  (full trajectory minus edge margin)
- Note: with od_config n_segments = 8 (see below), od_engine.py:197 returns the piecewise path before line 200 is reached.

Config (od_config.py):
- od_config.py:11 recovery_method = "least_squares"
- od_config.py:50 n_segments = 8
- od_config.py:53 segment_overlap = 0

Imports:
- od_engine.py:15-17: import numpy as np; from scipy.linalg import expm, logm, norm; import od_config as cfg
- benchmark.py:11-18: import os; import sys; import time; import traceback; import numpy as np; import tracemalloc; import od_engine
- od_config.py: no import lines found.

## 2. Trunk operator tools (/home/user/Markets/odcore)

symbolic.py
- Docstring lines 1-6 (quoted): "odcore/symbolic.py — PySR (Julia backend) symbolic regression: DISCOVER the" / "dipole / coupling / MI-vs-H equation from raw crypto operator data." / "" / "RECONSTRUCTED-FROM-CLAUDE.md (the per-session research workflow; would-be port of" / "s12_consolidate_per_domain.py). Cites:" / "  - PySR (Brunton/Cao/Liu/Tegmark/Cranmer family) with the extended operator set"
- Defs/classes: symbolic.py:30 def pysr_available() -> bool; :39 class DiscoveredEquation (dataclass); :49 def _regressor(niterations, maxsize, seed) (private); :68-69 def discover(M: np.ndarray, target: str, features: list[str], niterations: int = 40, maxsize: int = 12, seed: int = 0) -> DiscoveredEquation
- Input (symbolic.py:71-73): M = np.asarray(M, dtype=float); y = M[:, COL[target]]; X = np.column_stack([M[:, COL[f]] for f in features]). COL comes from operators.py (symbolic.py:24).
- Requirement and fallback: docstring lines 14-15 "Fallback: when Julia/PySR is unavailable (l.2057), callers fall back to the reconstructed numpy forms (dipole_predictor.fit_algebraic_dipole)." Lazy import of pysr at symbolic.py:32 (in pysr_available) and symbolic.py:50 (in _regressor). Only availability check is pysr_available() (symbolic.py:30-35). No Julia check in the file. No fallback code in symbolic.py; discover() raises if pysr is missing. I did not verify dipole_predictor.py or that function exists.

null_extract.py
- Docstring lines 1-7: "odcore/null_extract.py — centered-SVD null extraction + coupling decomposition." / "" / "RECONSTRUCTED-FROM-CLAUDE.md (would-be port of s12_coupling_decomposition.py /" / "s13_chemistry_residual.py). Cites (CLAUDE (5).md):" / "  - Center the 6 columns (NOT z-score: scale is a units choice, MI is the invariant," / "    INFO-051 l.1051), SVD, smallest right-singular vector = null[0] (INFO-012 l.597;"
- Public: :45 class NullResult; :51 def extract_null(M: np.ndarray) -> NullResult; :66 class CouplingDecomp; :74 def decompose_coupling(null0, mi_threshold: float = 0.5, ...); :98 class StrengthReadout; :104 def coupling_strength(M) -> StrengthReadout; :128 class CouplingVerdict; :141 def analyze_coupling(M, mi_threshold: float = 0.4, ...). Private: :31 _unit.

coupling_scanner.py
- Docstring lines 1-7: "odcore/coupling_scanner.py — rank channel pairs by structured coupling; emit decoupling events." / "" / "RECONSTRUCTED-FROM-CLAUDE.md. Cites:" / "  - Coupling discriminator + INFO-041 control (structured vs mere correlation): null_extract." / "  - Tautology-killing circular-shift null (INFO-066 l.913): a coupling claim is only real if" / "    its excess survives circular-shifting one channel (kills the instantaneous pairing while"
- Public: :28 class PairScore; :55 def tautology_structure_null(a, b, window, stride, ...); :78 def score_pair(a, b, name, pair_kind, ...); :108 class DecouplingEvent; :115 def rolling_coupling(a, b, win: int = 600, step: int = 60) -> np.ndarray; :126 def detect_decoupling(cc_series, lookback: int = 20, ...). Private: :47 _structure_metric.

operators.py
- Docstring lines 1-7: "odcore/operators.py — the windowed Operator-Discovery basis." / "" / "RECONSTRUCTED-FROM-CLAUDE.md. Parts list cites (CLAUDE (5).md):" / "  - Basis [H_a, H_b, H_a^2, H_b^2, H_a*H_b, MI], window=40 (INFO-012 l.597; basis l.265)." / "  - Estimator robustness: Vasicek / KDE / kNN(KSG) families all agree on the structural" / "    core (INFO-022 l.609; INFO-034 KSG holds l.1972). We use Vasicek m-spacing for the"
- Public: :30 def vasicek_entropy(x, m=None) -> float; :61 def ksg_mi(a, b, k: int = 4, base: float = np.e, ...); :117 def operator_row(a_win, b_win, k: int = 4, ...); :126 def windowed_operator_matrix(a, b, window: int = 40, ...); :145 def anti_frac(a, b, window: int) -> float. No classes.

validation.py
- Docstring lines 1-7: "odcore/validation.py: walk-forward splits with an embargo." / "" / "Random k-fold overstates out-of-sample results on correlated time series, so splits are expanding-window" / "walk-forward with an embargo gap. The cost-charging backtest, the random-vs-walk-forward gap and the" / "net-return null that used to live here were removed on 2026-11-16 (Greg): trade cost is not a market" / "condition, and no bitcoin-era trade rule is carried forward."
- Public: :13 def walk_forward_splits(n: int, n_folds: int = 5, embargo: int = 50). No classes.

leakage.py
- Docstring lines 1-6: "odcore/leakage.py — pre-entry leakage check: a signal computed AT t must be invariant to data AFTER t." / "" / "The Architect's mandatory discipline (S36b): every new signal gets this BEFORE it touches a backtest. The" / "algebraic-dipole 0.993 OOF / FN=0 is "exactly the shape leakage takes" — it does not enter the falsification" / "harness until it survives this. The test is model-agnostic: a leakage-free signal's value at index i cannot" / "change when you corrupt every data point AFTER i. If it does, the signal peeks at the future."
- Gate: leakage.py:23 def assert_no_leakage(signal_at, ts, p, bv, sv, idxs, reps=3, seed=0). Private :13 _eq. No classes. signal_at(i, ts, p, bv, sv) (leakage.py:24). Corrupts p, bv, sv after i by permutation (leakage.py:35-39).
- Returns (leakage.py:26 docstring, :45 code): return (len(fails) == 0, fails), i.e. (passed: bool, fails: list of (i, v_clean, v_corrupt)). Empty fails = no look-ahead.

generators.py
- Docstring lines 1-5: "odcore/generators.py — OD signal functions (real-bin -> per-bar signal)." / "" / "Signals are computed from REAL BinSeries (no synthetic). Each returns a per-bar array in" / "{-1, 0, +1} aligned to the bars (signal[t] is acted on returns[t+1])."
- Public: :23 def ofi_signal(s: BinSeries, thresh: float = 0.05); :30 def ofi_fade(s, thresh=0.05); :35 def momentum(s, k: int = 5); :42 def dipole_direction(s, window: int = 40). Private :16 _sign. Input type BinSeries (generators.py:12, from .io).

## 3. Natural gas data for the four trade days

FOUND IN THE CHECKOUT: nothing.
- /home/user/markets-data/MARKET_DATA_INDEX.md, grep "crypto-ng-tick|root-rows|rows-2023|20231002": no matches.
- Glob /home/user/markets-data **/crypto-ng-tick-lean-60s-*.parquet: no files.
- Glob **/crypto-ng-tick-line-20s-*.parquet: no files.
- Glob **/*root-rows*: no files.

Branch that holds them (code, not index):
- root/pod.py:99 '--branch', f'root-rows-{day}'
- root/pod_leg_renders.sh:30 --branch "root-rows-$d" "$GITHUB/markets-data" "$WORK/rows/$d"
- root/pod_fetch.py:6 and :94: "the local folder of that trade day's root-rows branch"
- root/crypto_ng_excel.py:46 LINK = 'https://github.com/DavisAI1974/markets-data/blob/root-rows-{day}/{folder}/{name}'
- root/pinned_excel.py:14 same pattern with renders/{name}
- Files in that branch (root/pod_leg_renders.sh:32-34): /crypto-ng-tick/crypto-ng-tick-tape-trades-*, /crypto-ng-tick/crypto-ng-tick-line-20s-*, /crypto-ng-tick/crypto-ng-tick-lean-60s-*, /crypto-ng-tick/crypto-ng-tick-program-trades-*, /crypto-ng-tick/crypto-ng-tick-humps-*, /calc-move_steps-facts-*, /calc-resting-facts-*

Names in code:
- Stored rows: root/tape.py:217 STORED_ROWS = 'rows-{day}-part*.parquet'; declared at root/DECLARED_CONSTANTS.md:138.
- Line files: root/crypto_ng_tick.py:431 save(out, f'crypto-ng-tick-line-20s-{day}.parquet', line_table(r20, ...)); :432 save(out, f'crypto-ng-tick-lean-60s-{day}.parquet', line_table(r60, ...)). Same line_table and LINE_COLUMNS for both.
- root/leg_renders.py:73 LINES = dict(dipole=('crypto-ng-tick-lean-60s', 60), exhaustion=('crypto-ng-tick-line-20s', 20)); root/research_columns.py:44 same pair as dipole_60s / exhaustion_20s.
- root/DECLARED_CONSTANTS.md:281: spans 60 and 20 from _dipole_price_overlay.py W = 60 and regroup2.py SMOOTH_SEC = 20.
- root/crypto_ng_tick.py:31-35 lists the stored files.

Column names (root/crypto_ng_tick.py:94-106, LINE_COLUMNS):
- read :95; moment_received_ns :96; what :97; position_on_tape :98; trades_left :99; flow :103 ("THE LINE: bought minus sold over bought plus sold ..."); nothing_traded :105.
- Lines 100-102 NOT READ: names there (bought and sold counts, per root/crypto_ng_tick.py:312-313 r['bought'], r['sold'], r['left']) are not confirmed.
- Row builder: root/crypto_ng_tick.py:308-313 line_table, dict(zip(names_of(LINE_COLUMNS), [...])).
- Reader columns: root/crypto_ng_tick.py:687 and :739: columns=['moment_received_ns', 'flow'].

Other:
- root/store.py: no line matched the pattern.
- root/info_measure.py:63 LINE_FILE = 'crypto-ng-tick-line-20s'; :123 rows_folder / 'crypto-ng-tick' / f'{LINE_FILE}-{day}.parquet'.
- ROOT design docs (root-redesign-20261116/, count of matches for "root-rows-20231002|crypto-ng-tick", content not read): ROOT_GAMEPLAN_DECISIONS.md 40; STEP2_BRIEF_FOR_DESKTOP.md 1; peak-research-20261117/TRADE_LIFECYCLE_NOTES.md 3. Total 44 in 3 files.

## 4. Where a new calculation lives and how it gets ticks

root/tape.py
- :201 def calculation_eligible(exchange_ns: int, built=BUILT_TRADE_DAYS) -> bool. Docstring: "True only for a tick inside one of the four built trade days (6 pm to 5 pm Eastern). ... The 5 pm to 6 pm stretches and the Sunday start-up keep their marked rows but are never calculated on; warm-up and shelved ticks only build the book."
- :198 BUILT_TRADE_DAYS = frozenset(dt.date(2023, 10, d) for d in (2, 3, 17, 18))
- :209 def for_calculations(week: list[WeekFile], built=BUILT_TRADE_DAYS). Docstring: "The ONE gate through which any calculation receives ticks. Yields (file index, record index, record) for calculation-eligible ticks only. A calculation must never iterate `ticks()` or the raw files itself."
- :229 def rows_for_calculations(rows_folder: Path, trade_day: dt.date, columns, built=BUILT_TRADE_DAYS). Docstring: "The ONE gate through which a calculation receives STORED ROWS (what each tick did to the book is on the row, not on the raw tape record). Yields (position on the tape, the row's values in `columns` order) ... decided by the same `calculation_eligible` on the row's exchange time as `for_calculations()`: so it passes exactly the same ticks. ... A calculation must never open a stored file itself."
- Related: :221 stored_row_files; :133 ticks; :114 read_week.

root/calcs/__init__.py
- Lines 1-3 (quoted): "ROOT part 2: the calculations added on top of the foundation, one file each. A calculation receives ticks / only through `tape.for_calculations()` and never reads the tape itself (tests/root/test_tape.py)."
- No registration code. The file is a docstring only; nothing registers a calculation.

Pattern: root/calcs/turn_peaks.py
- Docstring :1-3 (quoted): "ROOT part 2, calculation `turn_peaks`: the peak worked out with no window, and every peak laid against the turns / of the price (Greg, 2026-11-17: ...". Line 24-25: "The rows reach this only through `tape.rows_for_calculations()`."
- Imports :29-32: from root.calcs import flow_peak, in_play; leg_peaks as LP; peak_story as P; quote_runs as Q.
- Entry function NOT FOUND in lines 1-80 read. Not searched further.

Test: tests/root/test_tape.py
- :100 test_only_the_four_trade_days_reach_a_calculation
- :120 test_calculation_code_cannot_read_the_tape_itself (the forbidden-name test; docstring :121). Forbidden tokens :124-125 include 'parquet', 'pyarrow', 'read_table', 'stored_row_files', 'glob', 'Path', 'read_text', 'read_bytes'. :126 opens_a_file regex for open(. :127 scans (REPO / 'root' / 'calcs').glob('**/*.py'). :133 asserts both gate defs exist.
- :137 test_the_rows_gate_passes_exactly_the_ticks_the_tape_gate_passes

## 5. Rules in /home/user/Markets/CLAUDE.md (first two lines each)

- :133-134 "- **ONLY THE FOUR TRADE DAYS ENTER A CALCULATION (Greg, 2026-11-16, said several times).** Scope: the ROOT rebuild," / "  trade days Oct 2, 3, 17 and 18, 2023. Only ticks inside those four trade days (18:00 ET to 17:00 ET) are used in"
- :150-151 "- **EVERY CALCULATION IS MADE AT THE TICK, TIMED TO THE NANOSECOND (Greg, 2026-11-18: "Definitely run it on nano" / "  ticks"; "We've gone over numerous times").** Rows are ticks; nothing is put on a time grid of any size before it"
- :234-235 "- **EACH TRADE INDIVIDUALLY, never average.** No pooled hit-rate, no mean signed-bps, no averaged" / "  coefficient — every aggregate blurs away the per-trade fingerprint that IS the predictive content."
- :237-238 "- **Per-cell always, never pool.** Cells = moneyness × side × velocity/lag-class × release (for" / "  level-hits); regime × city × season × bucket × swing-dir (for weather). A signal that survives on a"
- :250-251 "- **Leakage gate before ANY backtest** (`odcore/leakage.py`) — pre-entry context must be invariant to" / "  future trades. This is mandatory and non-negotiable."
- :252 "- **Zero synthetic trading data.** Ever."
- :219-220 "- **THE NATURAL GAS DIPOLE AND EXHAUSTION ARE USED FOR STRATEGY. CRYPTO DATA IS NOT IN OUR ANALYSIS OR ON THE EXCEL" / "  SHEETS (Greg, 2026-11-23: "The crypto data is not to be in our analysis or on excel sheets. The ng version of"

## 6. Stage 3 loop control file (tools/ratchet/PROGRAM_TEMPLATE.md)

Field keys (line):
- loop :7; repo :8; mutable :11; protected :14
- metric :19; name :20; direction :21 (null = Greg has not chosen the figure; every trial run and recorded, status "recorded"); unit :23
- figures :25 (a list; "EVERY figure listed is read after each run and written as its own line"); name :26; unit :27; parse :28; kind :29; pattern :30; group :31
- run :35; command :36; cwd :38; timeout_s :39; env :40
- budget :43; max_trials :44; max_wall_clock_s :45; max_model_calls :46; max_sub_agents :47; max_concurrent_workers :48; max_tool_calls :49; max_tokens :50; max_retries :51; max_graph_writes :53
- crash :55; max_consecutive_crashes :56
- keep :59
- stop :62; after_trials :63; after_trials_without_a_keep :64
- escalate :66; escalate_file :70
- record :72; data_root :73

The five words (case-insensitive grep over tools/ratchet, covering PROGRAM_TEMPLATE.md, loop.py, program.py):
- canary: NOT FOUND.
- target: NOT FOUND. Stop fields are after_trials (:63) and after_trials_without_a_keep (:64); no target-stop key.
- holdout: NOT FOUND.
- secondary: NOT FOUND. The figures list (:25) allows more than one figure, each on its own line.
- summary: FOUND only at tools/ratchet/loop.py:447 "summary": [{k: h[k] for k in ("n", "id", "commit", "status", "figures", "parent", "note")}. Not in PROGRAM_TEMPLATE.md or program.py.
- phase: NOT FOUND.

## NOT FOUND (what was searched)
- Ratchet words: whole tools/ratchet folder.
- holdout in April code: none in od_engine.py; only benchmark.py:79, :116.
- Stored ROOT rows and line files: not in /home/user/markets-data checkout (globs and index grep above). root/store.py: no match.
- turn_peaks.py entry function: not in lines 1-80; not searched further.
- dipole_predictor.fit_algebraic_dipole: named in a docstring only; not checked.
- Not read: April README.md, SUMMARY.md, od_autoresearch.md, results.tsv; od_config.py beyond the lines quoted.

## Tool-call count
24 of 30 used. No sub-agents, no writes.
