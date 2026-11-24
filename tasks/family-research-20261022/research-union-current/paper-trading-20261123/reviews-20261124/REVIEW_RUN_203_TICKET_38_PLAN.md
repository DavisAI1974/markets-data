# Reviewer run 203 (Opus): ticket 38, the read of the plan for every data layer

Everything below this line is the agent's own report, word for word; nothing below it is the main session's.

## Hand-back 1 of 1

# Reviewer run 203 (Opus): ticket 38, the read of the plan for every data layer

## What was read and measured
- Read in full: BRIEF_STANDING_20261124.md, run-0203.json, PLAN_38_EVERY_LAYER_20261124.md, 38.md, REVIEW_RUN_182_TICKET_38.md, SCOUT_RUN_162_TICKET_38.md.
- Working copy /home/user/wt/r162 is at `f9b1920`. I made no edits and put no lines back, so no `git checkout` was needed.
- **The branch.** `git --git-dir=/home/user/planes.git ls-tree -r --name-only root-rows-20231002` gives 937 paths.
- **No pyarrow.** None of the Pythons on this machine has pyarrow (checked: /usr/bin/python3, 3.11, 3.12, 3.13 and /usr/local/bin/python3). So I read each parquet file's footer myself (the parquet metadata block at the end of the file, decoded with a short reader I wrote) from `git show` output. That gives schema and row counts only; no row values were read.
  - The script is /tmp/claude-0/-home-user/3e104f60-b369-56be-82d1-295b070262b0/scratchpad/pf.py and its output is .../scratchpad/layers.txt.
  - Column lists are in .../scratchpad/cols_rows.txt (408 columns) and .../scratchpad/cols_calc-research_columns.txt (328 columns).
- **Layer count.** Grouping files by name (date and `-partN` stripped) gives 62 parquet layers. With `native-episodes-20231002.jsonl.gz` that makes the plan's 63.
- **Grounding check: not run.** It would have needed calls beyond my limit.

## Item 1, part B: the layers, what tells when a row became known, and causality

### The main finding: calc-research_columns mixes per-tick reads with move and hump outcomes
This layer has 820,670 rows and 328 columns.
- **The per-tick columns** are `dipole_60s`, `exhaustion_20s`, the `info_*` measure and the division flag. They come from `standing()` at `root/research_columns.py` about lines 104-114.
- `standing` (`root/research_threads.py:157-169`) takes the last stored read made before the tick's nanosecond, or at that nanosecond and at or before the tick's tape position. Its docstring (161-163) says that reads made at the same nanosecond after the tick are excluded on purpose. **From this code, the per-tick columns at tick p use reads up to p only.**
- **The `tick` module that computes the reads was not located.** `crypto_ng_tick.py:408` calls `tick.reads(...)`. Neither `root/crypto_ng/tick.py` nor `crypto_ng/tick.py` exists in /home/user/wt/r162, and a search for `^LEAN_NS` found nothing. So the line itself rests only on the docstring at `root/crypto_ng_tick.py:9`: "Every trade enters each line at the nanosecond it was received and leaves it exactly 20 (or 60) seconds later."
- **The block columns carry outcomes, placed early.** The same file writes 316 block columns: `leg__`, `bid_run__` and `ask_run__` (50 each), `hump__` (83) and `hump_between_ticks__` (83).
  - Moves are written onto the tick of their FIRST step: `put(prefix, ..., place[stored['first_step_position'][line]])`, research_columns.py about line 144.
  - Humps are written onto the tick they began: about line 165.
  - Humps that began with no tick of their own are written on the last tick BEFORE they began: `searchsorted(received_at, began_received_ns) - 1`, about lines 169-174.
- **Which outcome columns they are** (from the footer): `leg__end_position`, `leg__end_received_ns`, `leg__end_price`, `leg__dipole_60s_at_end`, `leg__exhaustion_20s_at_end`, `leg__best_bid_at_end`, and the same for `bid_run__` and `ask_run__`. For humps: `hump__ended_received_ns`, `hump__how_it_ended`, `hump__ended_on`, `hump__furthest_flow`, `hump__furthest_received_ns`, `hump__last_trade_price` and others.
- **Concrete failing case:** a move whose first step is at tick p and whose end is minutes later. Its end price sits on row p.
- **What part B would do with it.** Part B places a row by the received time of its `position_on_tape`. Applied to this layer it would hand a decider, at tick p, how the move or hump ended. The plan's "one entry per layer" cannot hold this layer; it needs one entry per column group.
- **Today it is not placed.** signal_packet treats it as having no time.
- Arithmetic only, not checked on the rows: 820,670 − 784,130 = 36,540 rows hold an instant. That is near research-moves (33,131) plus humps (4,459). This suggests the rows that do hold a time are exactly the block rows.

### The table, layer by layer
Rows and time or position columns are from the footers.

**Per-tick calculation layers.** 18 layers, each 820,670 rows, keyed by `position_on_tape`, with no time column:
- calc-book_totals, calc-chain_peaks, calc-flow_peak, calc-leg_peaks, calc-move_steps, calc-open_stories, calc-outside_changes, calc-peak_links, calc-peak_story, calc-quote_peaks, calc-quote_runs, calc-refills, calc-research_columns (above), calc-resting, calc-sweeps, calc-together, calc-turn_peaks, dipole-peaks.
- Known-at for these can only come from a position look-up. Causality was read for calc-research_columns only.
- For calc-leg_peaks, only the column text at `root/calcs/leg_peaks.py:49` was read: `leg_facts_known` is "How many facts ... became known at this tick". The calculation bodies of the other 16 were not read.
- calc-flow_peak carries `peak_high_received_time_ns` and `peak_highest_for_ns`. calc-open_stories carries `*_open_high_position`. Whether these hold values from after p is not read.

**Facts tables.** 16 layers, each with `known_position` and `known_received_time_ns`:
- chain_peaks-before (57,114 rows), chain_peaks-facts (9,524), leg_peaks-facts (15,963), move_steps-facts (78,468), outside_changes-facts (73,236), peak_links-facts (19,049), peak_story-facts (58,828), quote_peaks-facts (62,505), quote_runs-facts (62,505), refills-facts (1,860), resting-ahead (2,909), resting-facts (110,284), sweeps-facts (38,412), together-facts (33,609), turn_peaks-facts (84,368), dipole-peaks-facts (11,007).
- The known-at column exists. But several of these also carry what look like end values:
  - turn_peaks-facts: `move_ended_received_ns`, `move_end_price`
  - chain_peaks-facts: `high_to_end_ns`, `price_at_end`, `ended_by`
  - peak_links-facts: `first_later_high_position`, `ended_by`
  - sweeps-facts: `lasted_ns`, `ticks_lasted`, `last_trade_price`
- Whether `known_*` is at or after those ends is not shown by the footer. The calculation code was not read.
- Today's fmax placement is at or after `known_received_time_ns`. Placing these by `known_received_time_ns` alone would be early for any column later than it.

**Open at the end.** 8 layers, no known column:
- chain_peaks (1 row), leg_peaks (1), peak_links (1), peak_story (1), quote_runs (2), sweeps (0), together (0), turn_peaks (0).
- They are written from what is still open when the tape ends: `root/calcs/leg_peaks.py:159` `tables['open-at-the-end'] = legs.still_going()`, and `root/chain_common.py:92` `still_open=`.
- So they are known only at the end of the trade day. together-open-at-the-end carries `set_exchange_time_ns`; under today's rule it would be placed by that time if it held rows.

**The crypto and ng lines.**
- crypto-ng-tick-lean-60s (71,204 rows), crypto-ng-tick-line-20s (71,220), info-measure (71,220): each has `moment_received_ns` and `position_on_tape`, one row per read.
- A read made at the same nanosecond after a tick stands on trades later on the tape (`research_threads.py:161-163`). Placing these by `moment_received_ns <= moment` alone lets those in. The position tie-break is needed.

**Humps.**
- crypto-ng-tick-humps (4,459 rows) and research-humps (4,459) have `began_received_ns`, `ended_received_ns`, `furthest_received_ns` and `how_it_ended`. Neither has a known column. research-humps also carries `dipole_60s_at_ended` and `best_*_at_ended`.
- The earliest a whole row can be known is at its end. Code not read.

**Turns.** crypto-ng-tick-turns (4,342): `marked_received_ns`, `furthest_received_ns`, `lean_at_furthest`. "Furthest" is after the mark. It is not placed today (`signal_packet.py:509`).

**Program trades.**
- crypto-ng-tick-program-trades (1,794): onset and end positions and times. Out by Greg's rule.
- crypto-ng-tick-tape-trades (38,127): `position_on_tape`, `received_time_ns`, `flow_20s_at`, `starts_program_trade`, `ends_program_trade`. The program columns are taken out by `PLANE_COLUMNS_OUT` (`signal_packet.py:520`).

**peak-lives** (21,092):
- It has `known_received_time_ns` and also `end_received_time_ns`, plus `high_to_known_ns` and `begin_to_end_ns`.
- Its positions are stored as double.
- `known_et` and `end_et` are timestamp type, which the int64/double test at `signal_packet.py:575` skips.

**leg-renders-index** (6,119): `known_received_ns`, `ended_known_received_ns`, `picture_first_ns`, `picture_last_ns` and a `render` blob. The picture runs to the leg's end.

**dipoles-pinned** (741): `native_birth_ns`, `native_known_second_ns`. Not placed today (`signal_packet.py:500`).

**research-moves** (33,131): `first_step_received_ns`, `end_received_ns`, `end_price`, no known column. It is an outcome table.

**research-trace-first-steps** (104): `first_step_received_ns`, `read_by_time`. Code not read.

**The 6 pm to 8 pm trade legs.**
- trade-legs-6pm-to-8pm-legs (124): `first_available_ns`, `last_available_ns`, `last_receive_ns`.
- trade-legs-6pm-to-8pm-trades (457): `available_ns`, `receive_ns`.
- trade-legs-6pm-to-8pm-stretches (278): ordinals only, no time.
- The legs layer is not placed today (`signal_packet.py:512`).

**trade-renders-index** (3,588): program-trade pictures. Out by rule.

**vendor-restatements** (733): `exchange_time_ns`, `received_time_ns`. It is not read whether `received_time_ns` is the time of the restatement or of the original message.

**book-pictures** (47,069,561): `took_place_received_time_ns`, `picture_position`. Not placed today.

**rows** (820,670 rows, 408 columns): `received_time_ns`, `position_on_tape`.

**native-episodes** (.jsonl.gz): not read.

### Layers not reached
- **Calculation code not read** (footer only): every per-tick calc except research_columns; all 16 facts tables; both humps tables; research-moves; research-trace-first-steps; leg-renders; dipoles-pinned; vendor-restatements; book-pictures; the 6 pm to 8 pm legs.
- **native-episodes:** nothing read.
- **The `tick` module** behind `tick.reads`: not located.

## Item 2, part A: is any of the 408 row columns not known at its own tick?
- Read from `root/rows.py`:
  - `ends_exchange_event` (rows.py:56): the tape's own end-of-event flag on this tick.
  - `row_label` (rows.py:66, section "B. Our labels"): trade day, 5 pm to 6 pm stretch, or Sunday start-up, decided by exchange time.
  - `in_settlement_window` (rows.py:74): a calendar label.
  - `order_size_after` (rows.py:81, section C): the order's size just after this tick.
  - All four are known at the tick.
- **Section G (the outside figures, pinned).** DECLARED_CONSTANTS.md:177-190 says `AS_OF` columns hold the "latest value known at or before the row's received time". `outside.py:111` says the pinning refuses a value known after the row.
- **PER_TRADE_DAY is open.** That list (`root/pin.py:146`, used at 162 and 217) is written "on every row of the trade day". I did not read which columns it holds (lines 146-161). If any of them becomes known during the trade day, it sits on earlier rows. This needs reading before part A ships the column.
- **Sections D, E and F** were not read column by column. Among the time-like and "after"-named names (cols_rows.txt) I found no label or outcome column. That is a name scan, not a reading.

## Item 3: which clock
- **The packet's moment today** is `moment, run, rule = sig["received"], ...` (`signal_packet.py` about line 890, inside `build` at 884). It is a nanosecond, not a tape position.
- **Not located:** where `sig["received"]` is filled and on which clock. `tools/decider/afterwards.py:98` uses `_row_time(row)`, which was not read.
- **The plan's look-up should be `received_time_ns`.** The plan says the time a tick was received; the stored lines and facts all use received times (`moment_received_ns`, `known_received_time_ns`).
- **Same-nanosecond ties.** Several ticks share a nanosecond (`research_threads.py:161-163`, traced by research_trace.py). With "received ≤ moment" alone, rows of ticks after the signal's tick at the same nanosecond are handed over. To exclude them the signal's own `position_on_tape` is needed, and the plan does not provide it.
- **Float comparison still in place.** Times are still compared in float64 (`signal_packet.py:577`, run 182). Part C fixes this, and it has to land before B relies on it.

## Item 4: parts C, D and E against the rules
- **C:** I read nothing in it that breaks a rule. It removes `of`, names receipts and stops dropping names.
- **D:** "beside the folder, no pointer" keeps the file out of the folder's listing. Whether an agent decider can read the parent directory is not said. If it can, the file is still in reach.
- **E covers none of the 63 layers.**
  - The 458 columns are dipoles 25 + peaks 5 + crypto and ng 20 + rows 408. None of the 63 branch layers (calc-research_columns with its 316 outcome columns, the facts tables, the humps) is in the 458.
  - So E can reach zero while part B leaks.
  - E is also the check where run 182 found the counts printed and not asserted (`test_live_platform.py:269-295`).
- **The gate.** Reading the stored planes through `git show` hands over rows already made. research_columns made its rows from ticks through `tape.rows_for_calculations` (research_columns.py about line 90), so the read is not a new calculation.
  - What is missing is a day limit. `PlaneSource.commit` reads any `root-rows-<ymd>` branch that exists (run 182 R3).
  - The rows have no lower bound at 18:00 ET the evening before. The per-tick calc files hold rows for the 5 pm to 6 pm stretch too (comment in `crypto_ng_tick.py`, `against_stored_flow`, and `row_label` values).
  - The plan says nothing about the halt-hour rows or the Sunday start-up rows.

## Item 5: what a builder would have to guess
1. The signal's tape position, for the tie at one nanosecond, and the clock of `sig["received"]`.
2. How to enter a layer whose columns differ in when they are known. "One entry per layer" cannot hold calc-research_columns; it needs entries per column group, or per column.
3. For facts tables: what proof shows that every column is at or before `known_position`, not only that the column exists.
4. Where the open-at-the-end layers, the humps and research-moves go. The plan says "settles" or "listed", but not whether that is the after-the-fact file or not placed.
5. Whether halt-hour rows (5 pm to 6 pm) and Sunday start-up rows are handed over, and what the lower time bound is.
6. Which days PlaneSource may read (the four-day list).
7. Timestamp-typed columns (peak-lives `known_et`): are they instants?
8. Whether `native-episodes` (jsonl.gz) gets an entry.
9. Where the known-at table lives in code and in what shape.
10. Whether part A's reading by part still builds `known` from all 408 columns' instants. With every column read, the x*_known_from_ns columns join the fmax; nulls on early rows; a sentinel 0 or -1 would drop a column from the instants (run 182 speculation).

## Speculation (labelled; not measured)
- The 36,540 rows of calc-research_columns that hold an instant are the block rows (arithmetic above).
- The facts tables' end-like columns may be written at a `known_position` equal to the end, which would make them causal. Only their code can say.

## Open after this read
**For the builder of A and B (file:line):**
- `root/research_columns.py` about 135-174: the leg, bid_run, ask_run, hump and hump_between_ticks blocks put outcomes on the first-step, began, or earlier tick. These columns cannot be placed by position. They go to the after-the-fact file, or stay not placed.
- `signal_packet.py` about line 890 (`moment = sig["received"]`): placement needs the signal's tape position for ties (`research_threads.py:157-169` is the existing tie rule).
- `root/pin.py:146-161`: read PER_TRADE_DAY's columns before shipping them in part A.
- `root/calcs/leg_peaks.py:159` and `root/chain_common.py:92`: the open-at-the-end rows are known only at the end of the trade day.

**For the main session:**
- Whether D's "beside the folder" is out of the decider's read scope.
- E's check does not cover the 63 branch layers.
- The four-day limit and the 18:00 ET lower bound for the plane reads.
- Locate the `tick` module (`tick.reads`).
- Run the grounding check on the plan's figures (not run here).

**What code cannot hold:** whether each of the 16 facts tables' end columns are known at `known_position`. That needs each calculation's code read, file by file.

Limits: 18 of 18 tool calls (Read 6, Bash 12), not counting this hand-back. No advisor call, 0 sub-agents, 0 graph writes. Nothing written outside the scratchpad, and the worktree is untouched. I cannot measure the token total from inside the run.

