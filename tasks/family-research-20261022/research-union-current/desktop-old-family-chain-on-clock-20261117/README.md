# Old family and chain states on the clock of the four trade days (Desktop session, 2026-11-17)

Made in a Claude chat session ("Desktop") on Greg's word, 2026-11-17 about 04:18 to 04:40 Eastern.
New files only. Nothing existing was changed. Nothing is in the daily stores or the workbook yet:
**this folder is the hand-over to Code so the daily sheets and the workbook can be updated from it.**

Read from: the four `root-rows-<trade day>` branches (`daac81d`, `e4ffcc9`, `74f4225`, `d2c34be`): `rows`,
`calc-flow_peak`, `calc-chain_peaks-facts`, `calc-peak_links-facts`. Old definitions read from Markets branch
`chatgpt/ng-exhaustion-post-phase2-20260818` (`59c03e8`): the frozen family classifier
(`research/FRANKIE_NG_PRE_FAMILY_CLASSIFIER_FROZEN_OPERATIONAL_20260817.json`, fingerprint
`583f6a121788b3d962f2ec849a270f96b1786d714ac930d2b0069c6261eda6f7`, equal to the one the old code expects),
`research/ng_exhaustion_live_clock.py` (`family_feature`, copied unchanged),
`research/ng_exhaustion_chain_canonical_table_20260817.py` (the +60 s state, the endpoint, the three gates),
`research/ng_exhaustion_chain_phase2_parallel_agents_20260818.py` (chain strings, the "known before" rule).

## Greg's words in this session (for the decisions file)

- "Do you want to start looking at new family and chain data to see what it's showing us? New structures? New
  groupijgs? But we want the data to guide us"
- "Use the old famiky definitions of families and chain examples to build the things using same timestamps as the
  renders you sent me."
- "And if they don't add anything try something else and if they do add, keep pulling on that string"
- "And we don't associate peaks with anything other than the data but they really should be pinned to the timestanp
  like price curve and dipole. They happen at certain times and for certain reasons. I don't think groupling applies
  at all to them"
- "If calculations happen over a time period the sensible thing is to pin them to timestamps rignt?" Answered: yes.
  A calculation over a stretch of time carries three stamps: the tick it is about, the stretch it read, and the tick
  its answer became known.
- "Have you been updating the appropriate excel sheets with the findings you've made? I don't want to spend so much
  time and effort running these clacs if they just get for gotten about" Answered: no, nothing of this session was
  stored until this folder.
- "Push data to markets data repo and print here so we can discuss"
- "We have to tell code so he can update excel sheets." "List output files and renders for code to use to.ipdate
  excel sheets"

Standing from this: the peaks are their own layer on the clock, like price and the dipole. No peak is put in a group.
The old families and chain states are a separate layer, each stamped where it is about and where it became known.

## Files

| File | What it is |
|---|---|
| `old-defs-on-peaks-<trade day>.parquet` (4) | One line per peak of the trade day, on the tick of its high (9,525 / 10,577 / 8,619 / 7,967 = 36,688, equal to the stored `flow_peak` counts). Columns below. |
| `flow-60s-before-and-after-<trade day>.parquet` (4) | For every peak, the 121 readings of the 20-second flow the old definitions read: one second apart from 60 s before the tick of its high to 60 s after, with the peak's side (positive is the peak's own side). Empty where nothing with a side traded in the 20 seconds. |
| `pinned_layers_<trade day>.png` (4) | Render, one per trade day, ten panels each holding about the same number of peaks. Price (every trade), every peak at its high, the old detector's events at their own tick with their old family, and each event's old state drawn at the tick it became known (60 s later), joined to its event. Counts on the image equal the table rows (checked in the script). |
| `build_old_defs.py`, `render_pinned.py`, `load.py` | The programs. |
| `MANIFEST.json` | Path, bytes, sha256 and source of every file here. |

## Calls made (Greg's to correct)

- t0 is the peak's own tick (the tick of its high). The old programs worked on whole seconds of the UTC clock day;
  here the 61 readings before and the 60 after are one second apart counted from that tick.
- The flow is the stored `flow_20s` (bought minus sold over bought plus sold, last 20 seconds, the tape's own trade
  side). The old programs took the side from the trade price against the mid. The stored flow was made again from
  the rows of trade day Oct 2 and is equal on all 819,783 ticks (tick order, the received clock, side B is bought).
- The old definitions carry their fixed windows (20 s, 60 s before, 60 s after, the 45 s spacing, the 85-in-100
  level). They are built here as written, as the base to look at. They are not new ROOT calculations.
- The old detector's three gates are written as facts about each peak. No peak is removed. The 85-in-100 level is
  taken over the trade day (the old programs took it over the UTC clock day). An "old-detector event" here is a
  peak that passes all three.
- Chains stay inside one trade day.

## Columns of `old-defs-on-peaks-<trade day>.parquet`

- The peak: `trade_day`, `peak_high_position`, `peak_high_received_time_ns`, `et` (Eastern), `peak_known_position`,
  `side`, `size`, `bought_at_high`, `sold_at_high`, `no_side_at_high`, `contracts_at_high`, `price_at_high_all`.
- What the peak did, copied from the stored `chain_peaks` facts: `ended_by`, `high_to_end_ns`, `lowest_share`,
  `steps_down`, `price_at_high`, `price_at_end`, `price_move_with_side`, `furthest_price_with_side`,
  `furthest_price_against_side`, `low_to_high_ns`, and the same three price moves in ticks (`ticks_...`).
  Empty for the 5 peaks whose story had not ended at the last tick.
- The old gates, as facts: `old_gate_size_at_or_over_85_in_100`, `old_gate_highest_within_5s`,
  `old_gate_kept_after_45s_spacing`, `old_gates_all_three`, `old_gate_size_level`, `old_prominence`.
- The old family, from the 60 s before (known at the high): `old_family`, `dist_A`, `dist_B`, `dist_C` (the full
  distance to each old centre), and the shape figures `pre_...`. `pre_samples_empty` counts readings that were empty
  and filled the old way; `pre_reaches_before_first_tick` marks the 42 peaks in the first minute of a trade day.
- The old state, read over the 60 s after. **It is about the high but is known only 60 s later** (stamp it at
  `peak_high_received_time_ns` + 60 s): `old_state_at_60s` (S same-flow reload, O opposite-flow reversal,
  P persistent, X sparse; empty for the 16 peaks in the last minute of a trade day), `zero_within_60s_at_s`,
  `below_half_at_s`, `below_quarter_at_s`, `below_tenth_at_s`, `flow_at_60s_with_side`.
- The old endpoint, with no horizon: `endpoint_onset_s`, `endpoint_confirmed_s` (seconds after the high; the answer
  is known at the confirmation second). Empty for 1 peak (Oct 18) that never reached it.
- Chain strings. `gated_...` are among the old-detector events only, `all_...` among all peaks:
  `..._before_states` (the states of up to four just before, oldest first), `..._before_sides` (S same side or
  F flip between them), `..._to_last_before` (this one's side against the last one), `..._known_before` (how many
  of those just before had passed their endpoint confirmation plus 60 s by this high: the old rule),
  `..._pair`, `..._triplet` (the old module strings; these include the peak's own state, so they are known late),
  and the old named examples `..._SSOS`, `..._POX_opposite`, `..._POX_same`, each also with `_known`.
- `kn_states`, `kn_rel`, `kn_last_age_s`: the states of the latest peaks at least 60 s old at this high (so already
  known), this peak's side against the latest of them, and how old that one was.

## What was measured

1. **The old detector's events on these four trade days.** The 85-in-100 size level comes out at 1.0 on all four
   trade days, so every old-detector event is a fully one-sided 20 seconds. 5,458 peaks have size 1.0; 15,260 are the
   highest within 5 s; 3,258 pass all three gates: 812 (Oct 2), 807 (Oct 3), 789 (Oct 17), 850 (Oct 18).
   Of the 3,258, 1,677 have one contract in the 20 seconds and 483 have two.
   On the Oct 17 render they sit mostly where the tape is thin: 355 from 18:00 to 04:15, 165 from 04:15 to 08:07,
   between 7 and 38 in each of the seven daytime panels, 111 from 14:28 to 17:00.
2. **Old family of the old-detector events:** A 3,083, B 72, C 103 (by trade day: A 771 / 767 / 756 / 789,
   B 15 / 14 / 13 / 30, C 26 / 26 / 20 / 31). The frozen 2026 population was A 3,235, B 72, C 122 of 3,429.
3. **Old state of the old-detector events:** S 743, O 898, P 922, X 695.
4. **Old named chain examples among the old-detector events:** S,S,O,S before: 34 (18 with all four known by the old
   rule). P,O,X before with this one on the opposite side: 26 (8 known); on the same side: 15 (12 known).
5. **Where a result is stamped changes what it seems to say.** With the +60 s state stamped at the high (the state
   of the peak just before, same side, state P), the peak's price move with its side from its high to the end of
   its story was: with 1+ ticks 922, flat 1,142, against 1+ ticks 512 (2,576 peaks). With only a state already
   known at the high (the latest peak at least 60 s old, same side, state P): with 835, flat 1,065, against 834
   (2,734 peaks).
6. **How far the peaks sit from the old family centres.** Of the 3,258 old-detector events, 1,569 are within 5 of
   the centre of A. Of the other 33,430 peaks, 1,324 are. No peak nearest to B is closer than 40.1 to it, and none
   nearest to C is closer than 26.3.
7. **Set aside on Greg's word (peaks are not grouped), kept for the record:** every peak's old family and its price
   move with its side to the end of its story. A: 31,861 ended peaks, with 8,919, flat 12,942, against 10,000.
   B: 1,740, with 494, flat 726, against 520. C: 3,082, with 814, flat 1,271, against 997.

Not measured, labelled as a reading: item 1 suggests the old detector, run on these days, mostly marks thin tape.
Whether that holds outside these four trade days is not known from this.

## Not done

- The daily sheets and the workbook are not updated from this. That is the hand-over to Code.
- No Excel file was written here.
- The renders and counts of the earlier chat session of 2026-11-16 evening ("ST1 and ST2 findings": the price curve
  with every peak, the price curve with the peak line, Oct 17 against random points) were made on sandbox copies
  and are not in this folder; that session's workspace is gone. They can be drawn again from the stored files.
