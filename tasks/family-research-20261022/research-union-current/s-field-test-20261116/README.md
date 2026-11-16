# S-field test on October 18 and empty-cell census (2026-11-16)

Working notes for the eight-trade workbook fill. Base: `codex/evidence-availability-20261113` at `1dd7d93`.
Nothing here changes the workbook or any existing field value.

## Empty-cell census of the R2 workbook (5,513 ticks)

Source: release asset `Claude-Eight-Trade-Types-Rebuilt.xlsx`, SHA256 `49dd87cc...8257` (verified on download).
Every cell holds content; "empty" cells carry `NO_MATCHING_VALUE_IN_RETAINED_INPUT`. Per-field, per-day status
counts are in `results/census.json` (`scripts/census2.py`).

- Empty on all four days: L024, L026, L060-L063, L067-L071, L077-L080, L083-L089, L091-L092, L094-L098.
- Empty on Oct 2, 3, 17 only: S01-S19 (Oct 18 filled on all 1,447 ticks).
- Nothing else is empty.

## Where the S fields come from

- S01-S19 are the 19 C15 raw components of the Dipole teacher (`research/kalshi/frankie_boss/c15_teacher.py`,
  `c15_teacher_r3.py`, `c15_dstate.py`). The "far side" is the side being hit: over the last 64 completed groups,
  buy volume > sell volume by more than 5% of the total selects the ask, the reverse selects the bid, otherwise the
  far-side columns are MISSING. Reconstructing that rule from the trade list reproduces S presence on 99.97% of
  Oct 18 trades.
- The Nov 9 replay is `research/kalshi/frankie_boss/four_day_pins/recover_second_set.py` on Markets branch
  `codex/frankie-brain-four-day-pins-20261109` (commit `7f34afa`). It is written for Oct 2. Inputs are the
  `native-messages-*` shards on `codex/frankie-book-recovery-<day>-42617700678` in this repository.
- No second-set output for Oct 2, 3 or 17 was found on any branch.
- `scripts/run_second_set.py` runs that code unchanged from local git objects. Speed here: about 35-50 messages
  per second on one core, so roughly 4-6 hours for Oct 2 (808,453 messages).
- Not yet validated: the Oct 18 archive starts with 841,601 warm-up messages before the session and its receipt
  has a different shape, so the Oct 2 script does not run on it as written.

## Calculation audit: are IDs or clocks used as values?

Read from `c15_teacher.py`, `c15_teacher_r3.py`, `c15_dstate.py`, `teacher_changes.py` at Markets `7f34afa`.

- Trade IDs and trade cursors are not in the calculation. The replay uses the trade list to cross-check trade
  messages and to label output rows.
- Order ID, instrument/publisher ID, cursor, receive clock, session identifiers and hashes are used as keys, ordering
  guards and provenance only.
- Two duration-type quantities are values: order age in seconds (S04, S09) and counts of elapsed groups (S17, S19).
- With `teacher_changes` applied (Greg, 2026-09-28): the "1024" fields are running totals over the whole day so far,
  the cohort is every level of the far side, and the short window is the last 64 groups or all groups while fewer
  exist.

## Oct 18, every trade individually

The earlier within-cell rate tables, correlations and model scores were withdrawn (they averaged over trades) and
are no longer in this folder. Scripts: `flatten_oct18.py`, `build_trade_frame_oct18.py`, `s_individual_oct18.py`.

- `results/oct18_trade_ledger.csv.gz`: one row per trade, all 30,739. Designation (trade id, ordinal, cursor,
  group, three clocks), the trade, the book just before it, the far side from the prior 64 groups of flow, all 19
  S values with their states, and what happened to that trade next (first 1-, 2- and 4-tick move with or against
  the flow, and seconds to it). Leakage gate on the context: 40 checks, 0 fails. Settle window 14:28-14:30 ET is
  marked excluded and no outcome runs through it. No trade cost.
- `results/oct18_twin_pairs.csv.gz`: pairs of individual trades with identical existing-field context (far side,
  day part, spread, far-touch size and order count, near-touch size, trade side relative to flow), at least 60 s
  apart, where one continued and the other reversed. 3,154 pairs at 1 tick, 5,027 at 2, 5,469 at 4. Both trades'
  S values are listed side by side for all 19 fields.
- `results/oct18_twin_field_counts*.csv`, `results/oct18_twin_clock_check.csv`: counts over those listed pairs.

Per-field facts (counts of individual trades or pairs, 1-tick pairs unless stated):

| Field | Fact |
|---|---|
| S05, S13 (whole-day identity survival, size retention) | Higher on the earlier trade in 2,047 of 2,047 and 2,050 of 2,050 pairs that differ. Equal to each other on 26,468 of 26,701 trades. |
| S09 (far queue age p90, all levels) | Higher on the later trade in 3,109 of 3,154 pairs. |
| S02, S07, S10 (whole-day absorption, priority loss, replenish) | Follow time order in 2,728, 2,657 and 2,569 of 3,154 pairs. |
| S04 (far front-order age) | Higher on the continued trade in 1,759 pairs, on the reversed in 1,394; same direction whichever trade is earlier. Matches the front-order age already in the sheet's FIFO fields within 0.05 on 1,211 of 1,317 selected Oct 18 ticks. |
| S12 (far size concentration) | 1,720 / 1,434 at 1 tick, 2,544 / 2,482 at 2 ticks; direction depends on which trade is earlier. |
| S03, S06, S08, S11, S14, S19 (64-group fields, unresolved age) | Near even between continued and reversed: 1,536/1,605, 1,481/1,671, 842/842, 1,473/1,678, 1,481/1,671, 1,460/1,645. S14 equals S06 on 21,318 of 26,701 trades. |
| S01 (extension count) | Zero on 24,651 of 26,701 trades; same on both trades in 2,668 of 3,154 pairs. |
| S15-S18 | Present on 2,050 (S15, S17) and 175 (S16, S18) trades; 26 and 0 pairs. |

The whole-day fields move with elapsed session time, so within a pair they mostly record which trade came later.
These counts describe the next 1-4 tick move at trade times only; S as a dipole lifecycle read is not examined.
