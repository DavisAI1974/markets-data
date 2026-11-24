# ROOT: every fixed window, cap and collapse found (2026-11-16)

Greg, 2026-11-16: no fixed windows; ROOT runs on the full depth of the data; the cutoffs and truncations were not his
choice; windows must come from the data, because many ticks fall between fixed sample points and some events live
outside the windows. This is the list of what has to come out. Nothing has been changed yet.

Code read:
- `A/` = Markets pin `2ebb8ce8`, `research/kalshi/frankie_raw_mbo_benchmark/` (the pinned producer package).
- `V4` = Markets `7f34afa`, `research/ng_exhaustion_mbo_v4_state_adapter_20260820.py` (the book adapter).
- `BOSS` = Markets `7f34afa`, `deploy/aws/box/frankie_box_boss_session.py`; `BED` = `deploy/aws/box/frankie_box_bedrock.py`.

Every line below was read in the code by the audit. The constants marked (checked) were read a second time.

## 1. Fixed time windows

| Where | Name | Value | What it limits |
|---|---|---|---|
| A/native_roll20.py:40, 201-202 | DEFAULT_WINDOW (checked) | 20 s trailing | roll20, which feeds the detector, the flow substrate and the per-second roll |
| A/native_replay_driver.py:914-916 | flow window | 20 s | signed flow size and side, which feed episodes, dipole stages, exhaustion and the response flow channel |
| A/native_flow_substrate.py:256 | window_share | 20 s | window-direction shares |
| A/native_candidate.py:72, 219 | LOCAL_RADIUS (checked) | 5 s | local-maximum test; a candidate is known 5 s late |
| A/native_candidate.py:73, 220, 486 | REFRACTORY (checked) | 45 s | spacing between candidates; peaks inside it are dropped |
| A/native_candidate.py:74-76, 421 | BASELINE_LAG / BASELINE_START (checked) | t-30 to t-10 s | prominence baseline for choosing candidates |
| A/native_candidate_adapter.py:69, 442 | PERSIST_SECONDS (checked) | 3 s | when a reversal or episode end is declared |
| A/native_response.py:146-166; A/native_a_arm_launch.py:494-495; BED:523-524 | HORIZON_SETS (checked) | 1, 10, 100 ms; 1, 10, 60 s | response readings |
| A/native_a_arm_launch.py:486; A/native_replenishment.py:520-524 | replenishment horizon | 60 s | restoration outcome; anything later is cut off |
| A/native_absorption.py:49, 367 | DEFAULT_REPLACEMENT_HORIZON_NS (checked) | 60 s | replacement ratio |
| A/native_calculation_runner.py:89, 336; A/native_mirror.py:442 | DEFAULT_MIRROR_DISTANCE_BOUND_NS (checked) | 60 s | mirror pairing; a pair further apart is unmatched |
| V4:51, 281, 702-706 | ACTIVITY_WINDOWS_S | 1, 5, 20, 60, 300 s | frame activity, copied into the ROOT frames at BOSS:869 |

Exchange calendar times in A/native_session.py:84-94 (close, reopen, settlement) are not modelling choices and stay.

## 2. Fixed count windows

| Where | Name | Value | What it limits |
|---|---|---|---|
| A/native_candidate.py:98, 221, 344-345 | threshold observations (checked) | last 86,400 seconds | the 85th-percentile bar for candidates |
| A/native_candidate.py:348-350 | flow buffer | 41 s | detector working memory |
| A/native_a_arm_launch.py:404, 562 | cadence_groups | 250,000 groups | when the principal is invoked |
| A/native_replay_driver.py:199-220 | every_groups | set by caller, not found | candidate event cadence |

## 3. Depth and detail caps

| Where | Name | Value | What it limits |
|---|---|---|---|
| V4:648-659, 730 | frame book (checked) | top 10 levels, no per-order queue | frame book and the top-10 depth imbalance (BOSS:856) |
| V4:777-781 | legacy rows | top 10 levels | rows behind roll20 and the legacy ledger |
| A/native_full_capture_adapter.py:633-634 | book_full | top-10 list kept; full lists beside it | frame book |
| A/native_roll20.py:38-39, 132-146 | bid_px_00 / ask_px_00 | top of book only | which side a trade is assigned to in roll20 |
| A/native_candidate_adapter.py:715 | touch depth | best level only | the queue-response channel |
| A/native_candidate_adapter.py:72, 136-168 | DEPTH_LEVELS | 10 | fallback when the full book is absent |
| A/native_replenishment_adapter.py:201 | NEIGHBOURHOOD_TICKS (checked) | 1 tick either side | which refills are credited to an episode |
| V4:619-631 | per-level summaries | front order, median and 90th-percentile queue age, largest share | per-order detail is left out of the frame book |
| A/native_full_capture_adapter.py:659 | activity level split | top of book versus everything else | activity since last group |
| A/native_stratum.py:26, 188-197 | EXACT_QUANTILE_CAP (checked) | 50,000 values | above it, quantiles come from a sample, not every value |
| V4:745 | checkpoint book | 20 levels | checkpoints (not in the ROOT path) |

## 4. History that is dropped

| Where | What | Value |
|---|---|---|
| V4:550-552 | activity history | dropped after 300 s |
| V4:236-243, 705 | each activity window | expires at its own length |
| A/native_candidate.py:344-345, 349-350 | detector bar and buffer | 86,400 observations; 41 s |
| A/native_candidate.py:489-500 | pending peaks inside a winner's 45 s | dropped |
| A/native_absorption.py:404-418 | pending runway | leaves at 60 s |
| A/native_replenishment_adapter.py:994-1005 | touch-restoration watches | pruned with the 60 s pending set |

## 5. Thresholds that decide whether anything is recorded

| Where | Name | Value | Effect |
|---|---|---|---|
| A/native_replay_driver.py:405; A/native_candidate.py:222, 387 | candidate_warmup_seconds (checked) | 900 s per segment | no candidate in the first 15 minutes of a segment |
| A/native_replay_driver.py:406; A/native_candidate.py:223, 388 | candidate_min_observations (checked) | 600 seconds with flow | no candidate before then |
| A/native_candidate.py:71, 407 | PEAK_QUANTILE (checked) | 0.85 | seconds below the bar are rejected |
| A/native_candidate.py:450-454 | refractory | 45 s | later peaks rejected |
| A/native_roll20.py:127-146 | trade filters | price and size above zero, a valid quote, price not at the midpoint | trades at the midpoint or without a quote are left out of flow |
| A/native_candidate.py:86, 395, 415 | zero-flow and local-maximum tolerances | 1e-12 | rejected seconds |

## 6. Where ticks are collapsed

| Where | What happens |
|---|---|
| A/native_replay_driver.py:1034; A/native_roll20.py:107-118 | every message group is put into one receive-time second |
| A/native_replay_driver.py:735-769 | the detector, episodes, responses and flow shares advance once per completed second |
| A/native_replay_driver.py:750-757; A/native_response.py:294-296 | horizons are read on whole seconds, so the sub-second horizons can be up to 1 s late |
| A/native_replay_driver.py:765, 811-826; A/native_candidate_adapter.py:743-749 | change points are checked once per second, and queue changes never trigger one |
| A/native_candidate_adapter.py:456-471 | one dipole stage per second, using the book at the last group close |
| A/native_replay_driver.py:1111-1126; V4:596-598 | book state is taken only when a message group closes, not at each message |
| V4:593-607 | legacy rows are written on trades, plus once per group only if the top 10 changed |
| A/native_roll20.py:122-123 | roll20 uses trades only |
| A/native_dipole.py:49, 85 | dipole stage index is binned by doubling (0, 1, 2-3, 4-7, ...) |
| A/native_causal_stream.py:233, 237 | availability is placed on a whole second |

## 7. Fixed "what happened next" horizons

Response +1, 10, 100 ms and +1, 10, 60 s; restoration +60 s; replacement +60 s; reversal after 3 opposite seconds;
mirror pairing within 60 s. (Same lines as section 1.)

## Redundant passes and builds noticed while reading

- The tape is replayed twice: once through the V4 adapter (BOSS:833-880) and again through the full-capture adapter
  in the bedrock traversal (BOSS:702-704, BED:580).
- roll20 is binned two ways that can disagree: per row (BOSS:846) and per group (A/native_replay_driver.py:1032), and
  the flow substrate keeps a third binner of the same rows (driver:447-453, 1057).
- The fixed-window activity is built on every group (V4:731), then discarded and recomputed by the full-capture
  adapter (A/native_full_capture_adapter.py:639).
- The book snapshot is taken twice per group, at 10 levels and at full depth (full_capture:633; BOSS:863).
- The same 20 seconds are summed twice each second (driver:915-916 and roll20:201-202).
- Up to 86,400 values are fully sorted on each judged second (A/native_candidate.py:400).
- Three order books are kept per instrument: the adapter's, the queue adapter's and the replenishment observer's
  (driver:505-516).
- Depth imbalance is computed in two sections (comment at A/native_response.py:99-101).

## Not found or not determined

- `hold3`: no such name in the package; the nearest thing is PERSIST_SECONDS = 3.
- `HARDCODED_WINDOWS` is cited in notes in A/native_layer_crosswalk.py but no such symbol exists.
- The caller's value for `every_groups`.
- Whether the redundancy list is complete: it is only what was noticed while listing windows, not a full audit.

## Greg's decision on the time step (2026-11-16)

ROOT runs at the tape's own resolution: nanoseconds, the same clocks the MBO tape carries and the live feed will
deliver. Whole seconds are out, because they lose most of the data depth.

What that means for the rewrite:
- The step is the tape's own unit, in tape order: each message, with its nanosecond receive time (when it could be
  known) and its nanosecond event time kept beside it. Nothing is binned to a second.
- The trade-day tape has 771,787 to 879,830 messages and 583,688 to 653,912 completed message groups per trade day,
  against 82,800 seconds. Every one of them becomes a step.
- Historical and live must compute the same way: the live MBO feed carries the same fields (event time, receive
  time, sequence, the end-of-group flag), so one code path serves both.
- Point to settle with Greg in the spec: the exchange publishes one event as a group of messages ending with an
  end-of-group flag. Orders, fills and flow can be stepped message by message. The book between two messages of the
  same group is a half-applied update that never existed as a public book, so book readings belong at each group
  close. That is the tape's own unit, not a truncation, but it is his call.
- Everything in sections 1, 2 and 4 to 7 above that is expressed in seconds has to be re-stated from the data.
