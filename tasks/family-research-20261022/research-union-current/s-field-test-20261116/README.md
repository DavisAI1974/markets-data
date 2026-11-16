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

## Oct 18 test: does S add information beyond the fields already filled?

Scripts: `flatten_oct18.py`, `s_test_oct18.py`, `s_test_incremental.py`. Population: all 30,739 Oct 18 trades.

- Context (known strictly before each trade): S at `last_completed_group_before_trade` (PRESENT only), the
  pre-trade book, and the 64-group flow anchor. Leakage gate: 40 checks, 0 fails.
- Outcome (strictly after, event-driven): which comes first, the mid moving k ticks with the anchoring flow
  (continuation) or k ticks against it (reversal), k = 1, 2, 4. Settle window 14:28-14:30 ET excluded; outcomes
  never run through it. No trade cost.
- Cells: far side (bid/ask) x day part (overnight to 08:00, 08:00-11:00, 11:00 to settle, post settle) = 8 cells.

Results (`results/*.csv`):

- Existing top-of-book fields sort the outcome in 8 of 8 cells at k=1 and k=2 (aligned top imbalance, top sizes
  and order counts, the trade's own side).
- S04 `far_front_age_log` is the only S field that is consistent on its own: 7 of 8 cells at k=1, 3 of 8 at k=2.
  Inside strata of the existing top-of-book fields its sign reverses in most strata, so the stand-alone effect is
  largely the same information as the book fields.
- S08 `far_priority_loss_rate_64`: 5 of 8 cells at k=1, 1 of 8 at k=2. Every other S field: 0-3 of 8.
- S15-S18 are present on too few trades to test (2,050 and 175 of 30,739).
- Out of sample in time, per cell, adding 14 dense S fields to the existing fields raised AUC in 1 of 8 cells
  (linear) and 5 of 8 (boosted) at k=1; 2 and 4 of 8 at k=2; 4 and 4 of 8 at k=4. Log loss improved in at most
  3 of 8 cells at any k. S alone reaches AUC about 0.57 at k=1 against about 0.80 for the existing fields.

Reading: on this one day, for short-move direction at trade times, S adds little beyond the book fields already
in the sheet. This is one day and one use of the fields. It does not test S as a lifecycle or exhaustion read at
the dipole level, and k=4 outcomes follow the day's trend, so they cannot separate S from that trend.
