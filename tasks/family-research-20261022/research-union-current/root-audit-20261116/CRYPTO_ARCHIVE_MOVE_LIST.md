# Crypto files: proposed move to the `archive/crypto` branch (2026-11-16)

For Greg's sign-off. **Nothing has been deleted from the trunk.** The branch `archive/crypto` exists and is a full
snapshot of the trunk at `676322d` (taken after the fee and fill rules were stripped), so every file below is
already safe there.

How the list was made: every Python file on the trunk was parsed for its imports, and every workflow, deploy
file, shell script and Claude skill was searched for file names. 107 Python files are reached from the live
code (`research/kalshi`, `tasks`, `desk`, `deploy`, the workflows); 81 are not. A file is on this list only if
nothing live reaches it and it is crypto-era work.

**Total: 173 files.**

## Root: exchange collectors and canaries (15)

`binance_btcusdt_canary.py`, `binance_btcusdt_canary_phone.py`, `bybit_perp_collector.py`, `bybit_public_tickers.py`, `coinbase_btcusd_4hr_trajectory.py`, `coinbase_btcusd_book_collector.py`, `coinbase_btcusd_canary.py`, `coinbase_btcusd_canary_v2.py`, `coinbase_collector.py`, `coinbase_eth_collector.py`, `collect_bybit_perp_history.py`, `kraken_book_collector.py`, `kraken_btcusd_collector.py`, `kraken_collector.py`, `kraken_eth_collector.py`

## Root: crypto research scripts (22)

`_birth_probe.py`, `_build_episode_onsets.py`, `_build_fingerprint_dataset.py`, `_build_onset_coeff_lists.py`, `_build_test_bars.py`, `_canary_fingerprint.py`, `_canary_fingerprint_v2.py`, `_canary_incremental.py`, `_canary_leakage.py`, `_diag_lookahead.py`, `_info_dipole_flow_detrend.py`, `_info_dipole_flow_probe.py`, `_info_dipole_flow_robustness.py`, `_info_dipole_timing_test.py`, `_info_dipole_trend_flip.py`, `_micro_attribution.py`, `_run_onset_coeffs.py`, `_series_tools.py`, `_test_coeff_lightweight.py`, `autoresearch_lite.py`, `operator_drift_alarm.py`, `operator_registry.py`

## Root: result files of crypto backtests (10)

`_info_dipole_flow_probe_results.json`, `_info_dipole_gated_swing_results.json`, `_info_dipole_harness_results.json`, `_info_dipole_netcost_backtest_results.json`, `_info_dipole_regime_gate_results.json`, `_info_dipole_swing_backtest_results.json`, `_info_dipole_swing_backtest_results_realbins.json`, `_info_dipole_timing_test_results.json`, `_info_dipole_trailing_backtest_results.json`, `_regenerate_audit_oracle_results.json`

## Root: crypto runner scripts (4)

`_run_onset_detached.bat`, `kraken_checkpoint_watcher.sh`, `phase1_ny_scheduler.sh`, `phase1_progressive_run.sh`

## Root: crypto-era documents (17)

`BUILD_PLAN.md`, `BUILD_QUESTIONS.md`, `CLAUDE_ARCHIVE_OD.md`, `CLEANUP_RUNBOOK.md`, `DEPLOY.md`, `FINGERPRINT_PROVENANCE_FINDINGS_S35.md`, `HANDOFF_DESKTOP.md`, `HANDOFF_PHASE1_5.md`, `HANDOFF_TO_CODE.md`, `HANDOFF_TO_CODE_PHASE2.md`, `HUMMINGBOT_PAPER_RUNBOOK.md`, `MARKETS_BRIEF_FOR_FRIENDS.md`, `MISSION.md`, `OPTION_E_PRODUCT_SPEC.md`, `S36_NETCOST_BACKTEST_FINDINGS.md`, `S77_REVIEW_FOR_CHATGPT.md`, `TODO.md`

## Root: crypto-era kickoffs and handoffs (S20 to S38) (30)

`CLAUDE_session_note_2026-06-08_S23.md`, `CLAUDE_session_note_2026-06-08_S24.md`, `CLAUDE_session_note_2026-06-08_S25.md`, `KICKOFF_2026-06-03_S21.md`, `KICKOFF_2026-06-05_S22.md`, `KICKOFF_2026-06-07_S23.md`, `KICKOFF_2026-06-08_S24.md`, `KICKOFF_2026-06-09_S25.md`, `KICKOFF_2026-06-09_S26.md`, `KICKOFF_2026-06-09_S27.md`, `KICKOFF_2026-06-13_S31.md`, `KICKOFF_2026-06-21_DATAFIX.md`, `KICKOFF_2026-06-21_S32.md`, `KICKOFF_2026-06-21_S35.md`, `KICKOFF_2026-06-22_S36.md`, `KICKOFF_2026-06-23_S38.md`, `SESSION_HANDOFF_2026-06-03_S20.md`, `SESSION_HANDOFF_2026-06-05_S21.md`, `SESSION_HANDOFF_2026-06-07_S22.md`, `SESSION_HANDOFF_2026-06-08_S23.md`, `SESSION_HANDOFF_2026-06-08_S24.md`, `SESSION_HANDOFF_2026-06-08_S25.md`, `SESSION_HANDOFF_2026-06-13_S30.md`, `SESSION_HANDOFF_2026-06-21_S32.md`, `SESSION_HANDOFF_2026-06-21_S33.md`, `SESSION_HANDOFF_2026-06-21_S34.md`, `SESSION_HANDOFF_2026-06-21_S35.md`, `SESSION_HANDOFF_2026-06-22_S36.md`, `SESSION_HANDOFF_2026-06-22_S36b.md`, `SESSION_HANDOFF_2026-06-22_S37.md`

## backend/ (crypto signal API) (5)

The whole folder.

## frontend/ (crypto signal web app) (29)

The whole folder.

## discord_bot/ (2)

The whole folder.

## fingerprint_dataset/ (crypto fingerprint data) (22)

The whole folder.

## vendored_build_kit/ (crypto dipole build scripts) (14)

The whole folder.

## research/ (crypto leftovers) (3)

`research/shape_s71/fit_shapes.py`, `research/shape_s71/lookahead_sweep.py`, `research/strategy_evolution/live_mock_replay/HINDSIGHT_AUDIT_ORACLE_FIX_2026-06-21.md`

## Stays on the trunk, and why

| What | Why |
|---|---|
| `odcore/` (19 files), `tests/` (3), `scripts/` (5) | The toolkit `CLAUDE.md` calls live. Live code imports six of its modules today: `leakage`, `leadlag`, `info_dipole`, `io`, `operators`, `symbolic`. The other twelve modules, the tests and the runner scripts are reached by nothing live. Default: keep the package whole. |
| `research/shape_s71/early_signal.py` | `release_book_signal.py` imports its book imbalance read. |
| `news_ingest_rss.py`, `news_coupling_research.py`, `build_news_policy_from_coupling.py`, `build_daily_news_context.py`, `daily_news_context.py`, `news_events.example.jsonl`, `NEWS_EVENTS_SCHEMA.md` | The news pipeline, repointed at Kalshi contracts in S78 and named in the Kalshi build scope and the backtest skill. |
| `regime_classifier.py`, `phase1_5_evaluator.py`, `markets_adapter.py` | Imported by `news_coupling_research.py`. |
| `desk/`, `deploy/`, `data/`, `artifacts/`, `tasks/`, `.github/`, `.claude/` | Live: the natural-gas desk service, the AWS units, the workflows. `desk/app.py` does not use `backend/` or `frontend/`. |
| Kalshi-era kickoffs and handoffs (S78 on) | Not crypto. |

## Edits that go with the delete

- `CLAUDE.md`: the pointers to `CLAUDE_ARCHIVE_OD.md`, `S36_NETCOST_BACKTEST_FINDINGS.md` and the S36 handoffs say "on branch `archive/crypto`".
- `KALSHI_TRADING.md`: the same pointer, one line.
- Nothing else needs to change. The remaining mentions of moved files are comments naming where a function was ported from. `odcore/fingerprint.py` tries to import a constant from `backend/api_server.py` that does not exist there, so that import already fails today and the move changes nothing.

## Questions

1. `odcore/`: keep the whole package on the trunk (default), or move the twelve modules nothing live imports, with `tests/` and `scripts/`?
2. The same delete on the research branch `research/markets-adaptive-wavepacket-migration-20261108` and the session branch (default: yes, same list).
