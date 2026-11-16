# Bitcoin-era trade rules: removed from Markets (2026-11-16)

Greg, 2026-11-16: "remove any bitcoin era rules and the associated code that factors them in. And make a note that
we should start fresh with kalshi rules for kalshi only."

**The note, as it now stands in Markets `CLAUDE.md`:** no bitcoin-era rules. Kalshi rules start fresh, for Kalshi
only. None is written yet, so none is assumed. Do not reintroduce a fee floor, a net-of-cost gate, a maker or taker
fill assumption, slippage, a bps cost threshold or a crypto-venue strategy rule, and do not copy one out of old
code, an old handoff or the archive. Kept from the crypto era: measurement tools only (the dipole read, the
pre-entry look-ahead window, the leakage gate).

Commits: Markets trunk `claude/kalshi-s79-kickoff-ij8t9o` `4f6172f`; research branch
`research/markets-adaptive-wavepacket-migration-20261108` and session branch `ccr-5317ce1c-hpqa9c` `a60cbda`.
Each: 85 files changed, 56 removed, 28 edited, 1 added, 10,389 lines out.

## Removed whole (56 files)

The rule was the file's purpose, and nothing that is kept imports it. Checked by searching every code file on both
branches for imports, script calls and workflow references.

| Group | Files |
|---|---|
| Repo root | `_info_dipole_fee_floor`, `_info_dipole_harness`, `_info_dipole_regime_gate`, `_info_dipole_gated_swing`, `_info_dipole_netcost_backtest`, `_info_dipole_trailing_backtest`, `_info_dipole_swing_backtest`, `_netcost_stack`, `_netcost_stack_balanced`, `_balanced_rerun`, `_regenerate_audit_oracle`, `_regenerate_audit_summary`, `_liquidity_dive`, `backtester`, `adaptive_backtester`, `news_dipole_replay` (16) |
| `executor/` | the crypto paper executor, all 7 files (simulated fee, stop and target in bps) |
| `scripts/` | `od_backtest`, `od_xvenue_backtest`, `od_trade_dipole_run` |
| `odcore/` | `platform` (Kraken cell configurations with maker and taker fees), `swing_maker` |
| `research/shape_s71/` | 15 Kraken and Coinbase fill, ramp, exit and deploy models. `leg_imbalance` and `whole_legs` had no cost line of their own but could only run through the removed executor |
| `research/shape_s77/` | all 3 files (gate scored at fees of 0, 5 and 10 bps, with its findings and results) |
| `research/od_book/` | all 10 files. Its pre-registered kill gate was the 22 bps fee floor |

## Stripped in place (the file does something else too)

| File | Removed | Kept |
|---|---|---|
| `research/kalshi/lag_join.py` | fee functions, slippage, maker offset, maker-fill and minimum-wave rule, their options | the lag join; each trade reports the gross move to the stop and to the extreme |
| `research/kalshi/coach_replay.py` | the round-trip fee term | the playbook replay, gross |
| `odcore/validation.py` | cost-charging backtest, random-versus-walk-forward gap, net-return null | the walk-forward splitter |
| `odcore/flip_detector.py` | fee-charging swing P&L | lean series, flip detection, retiming |
| `odcore/generators.py` | bridge to the removed adaptive backtester | the signal functions |
| `backend/api_server.py` | 50 bps round-trip fee on realized outcomes | everything else; outcomes are the gross move |
| `research/shape_s71/early_signal.py` | the cost result in the notes; trailing-stop and maximum-hold constants | the book imbalance read used by `release_book_signal.py` |
| `research/shape_s71/lookahead_sweep.py` | import from a removed file | carries its own 1 s book reader |
| `_canary_leakage.py`, `_canary_incremental.py`, `_info_dipole_timing_test.py` | import from the removed swing backtest | now import `_series_tools.py` (new: loader, zigzag, trailing imbalance, moved unchanged) |
| `odcore/dipole_predictor.py`, `odcore/info_dipole.py`, three Kalshi collectors | cost wording in comments | code unchanged |

Documents edited: `CLAUDE.md`, the `kalshi-backtest` skill, `FORECASTER_RUNBOOK_S93.md`,
`FORECAST_AGENT_DIRECTIVE_S88.md`, `FORECAST_AGENT_DESIGN_S87.md`, the coach brain's risk gate
(`knowledge/ng_brain.json` and its README), `KALSHI_BUILD_SCOPE.md`, `KALSHI_TRADING.md`,
`KALSHI_PRODUCT_RANKING_S91.md`. The product ranking lost its fee axis, fee table and maker-order guidance; the
order of the ranking was set with that axis in it and has not been redone.

## Checked

Every remaining Python file compiles on both branches. The kept modules import. `lag_join.py --selftest` and
`coach_replay.py --selftest` pass. No program was run on market data: none of the Kalshi or crypto tape is in the
cloud container, and no made-up data was used.

## Left in place, for Greg to decide

- **Old findings and handoffs** that describe cost-based results (`LAG_EXPLOIT_FINDINGS_S81.md`,
  `LEVEL_HIT_FINDINGS_S82.md`, `S36_NETCOST_BACKTEST_FINDINGS.md`, the session handoffs, `CLAUDE_ARCHIVE_OD.md`).
  They state results, not rules, and the new rule says not to copy from them. Delete them too?
- **Five crypto pipeline files that read a stored label already net of a fee** (`_build_episode_onsets`,
  `_build_onset_coeff_lists`, `vendored_build_kit/_build_sameperiod_cand`, `_eligible_cross_section`,
  `_run_clean_rerun`). They do no fee arithmetic themselves.
- **`odcore/sizing.py`**: crypto-era position sizing with no cost term. Its only user was the removed executor.
- **`backend/api_server.py`**: still a crypto signal service with a 30-minute hold and a 120-minute abandon rule.
- **Crypto collectors and their runner scripts** (`phase1_progressive_run.sh`, `kraken_checkpoint_watcher.sh`,
  the crypto pull in `scripts/session_start.sh`): no rule in them.
- **Other Markets branches** (the Frankie branch, the Codex branches) were not touched.
