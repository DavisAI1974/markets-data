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

## Second pass, same day: the dead and old Kalshi rules

Greg, 2026-11-16: "And remove the dead and old kalshi rules." Commits: trunk `676322d`; research and session
branches `b20ab9c`. Each: 15 files edited, 3 removed.

Rules removed: net-of-fee at maker and taker, the size-vs-fee wall, the spread toll, pooled hit-rate evaluation.

- **Removed whole** (built on a removed rule): `LAG_EXPLOIT_FINDINGS_S81.md`, `LEVEL_HIT_FINDINGS_S82.md`,
  `NYMEX_PRODUCTS_SURVEY_S91.md` (ranked and planned on the fee floor with maker and taker gates).
- **`release_signal_history.py`**: the pooled hit rate, the release-versus-placebo rate and the fade rate are
  gone. It writes one record per read. Loader, settle guard and leakage gate are unchanged.
- **Findings stripped**: weather baseline (fee out of the worked example), event move, path forecast research,
  gold and silver (its toll-net table is not kept), event surprise, weather regime, depth run-length.
- **Handoffs a new session reads**: the S93 handoff, the S94 kickoff and the blind-forecaster handoff lost the
  "net-of-fee maker AND taker" line and the cost-model requirements.
- **`CLAUDE.md`**: the S86 priorities block is gone; the standing rule names the Kalshi rules that were removed.

Checked: `research/kalshi` compiles; the edited module and its three importers import; both self-tests pass.

## Left in place, for Greg to decide

- **Older Kalshi-era handoffs and kickoffs** (S78 to S92, about 30 files): dated records that still carry the
  old rule text. `CLAUDE.md` says not to copy from them. Delete the superseded ones whole? (The crypto-era
  ones, S20 to S38, went to branch `archive/crypto` with the other crypto files; see
  `CRYPTO_ARCHIVE_MOVE_LIST.md`.)
- **Old Kalshi study scripts** in `research/kalshi/hist/` (7 scripts and their result files), listed in the
  file index as old and off the live path. Studies, not rules, so left.
- **Fixed numbers inside the Kalshi programs** (60 s bins, a 20-bin window, a 1,800 s settle guard, a 120 s
  pause, the $350 and $500 play thresholds in the coach brain). These are the same kind of ahead-of-time
  decision the ROOT redesign removes, but they are the programs' working parts, not leftovers.
- **`odcore/sizing.py`**: crypto-era position sizing with no cost term. It stays with the rest of `odcore/`,
  which Greg kept whole on the trunk.
- **Other Markets branches** (the Frankie branch, the Codex branches) were not touched.
