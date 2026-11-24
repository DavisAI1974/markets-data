# Reviewer run 182 (Opus): ticket 38, the first read of the packet (builder run 102)

Everything below this line is the agent's own report, word for word; nothing below it is the main session's.

## Hand-back 1 of 1

# Reviewer run 182 (Opus): ticket 38, the first read of the packet (builder run 102)

## What was read and run
- Ticket 38 (whole), run plan run-0182.json, scout 162 report (whole, it is short).
- `git diff --stat e55da89^..2ac873f`: the six expected files (+831/-38). I read every hunk of all six.
- Between 2ac873f and 74006f2, `signal_packet.py`, `serve.py`, `test_decider.py` and `test_live_platform.py` have no changes. Line numbers below are therefore the same at both commits.
- Checks run in /home/user/wt/r162 with MARKETS_DATA=/home/user/markets-data, using the given command: **2 passed, 36 skipped, 0 failing.**
  - The 2 that ran: `test_live_platform.py:221` (the four trade days carry the same columns on each kind of sheet) and `:235` (every 2023-10-02 column placed in one of three places).
  - Skipped (reason as printed): 29 in test_decider.py, "no paper-trading-platform checkout at /home/user/paper-trading-platform". This covers every test in that file, including the four plane checks at 614, 646, 674 and 736 and the afterwards check at 538. Those five skip in the `world` fixture before the `planes` fixture is reached.
  - 6 skipped in test_live_platform.py on the same reason. 1 more (`:40`) skipped with "no ref for run 0f33fec4…".
  - markets-data/.git holds 16 refs, all `paper-runs/*`. There is no `root-rows-20231002` and no `paper-runs/0f33fec4…`.
- Measured by the Excel check (printed, not asserted): a 27, b 13, c 418. By sheet: dipoles 17/8/0, peaks 0/5/0, crypto and ng 0/0/20, rows 10/0/398. This matches the ticket.
- Read, not run (all skipped here): `PlaneSource`, `PlaneLayer`, `plane_state`, `plane_lines`, `plane_id_ok`, `plane_since`, `plane_afterwards`, `plane_leak`, `plane_since_check`, the planes branch of `build`, and the serve.py writers and id validation.

## Lines put back (each restored with `git checkout -- .`; `git status --short` was empty after each)
1. `signal_packet.py:590` `placed_mask` changed to `return (self.known >= 0)`, so the moment is ignored and every row is placed. Result: 2 passed, 36 skipped. No running check sees it.
2. `signal_packet.py:746`: a line added so `plane_id_ok` accepts any id starting `afterwards:`. Result: 2 passed, 36 skipped. No running check sees it.
3. `signal_packet.py:519`: `"flags"` removed from `PLANE_PROJECT["rows"]`. Result: the daily_sheets check passed. The counts moved to a 26 / c 419 (rows 9/0/399) and nothing failed.
- From reading only (these checks skip here): mutation 1 would be seen by `plane_leak`'s recount (`signal_packet.py:1227-1229`) in `test_decider.py:614`/`646`. Mutation 2 would be seen by `test_decider.py:727` and the earlier refusal at `:563`.

## Findings by rule

### R1: no data layer dropped silently; no cap, clip, sample, average or smoothing
- **The rows plane is read through 10 of its 408 columns** (`signal_packet.py:518-519`, read at 642-643).
  - The other 398 are listed in `not_read`. Their names go into the afterwards file as `columns_not_copied` (about line 789). The foot gives only a count per layer (1037-1047).
  - The whole file is still pulled into memory by `src.blob` (637) and `io.BytesIO` (640). Only the column set is cut; it is not read by part.
- **calc-research_columns is not placed.** Per the test comment at `test_decider.py:629`, 784,130 of its 820,670 rows hold no instant; the no-time rule is at `signal_packet.py:667-673`.
  - By `planes_named` (479-480), `exhaustion_20s` and `dipole_60s` are columns of this layer. So the per-tick dipole and exhaustion calculation does not reach a decider.
  - The dipole reaching a decider is the state's `flow_lines` at the tick plus the dipoles section's SHOWN cells. This bears on "the dipole above all".
- **The graph's CalcOutput and READS entries are filtered when a planes source is given.** `build` at `signal_packet.py:943-944` keeps only `planes_named` entries ending `.parquet`.
  - The `calc-<calc>` names from graph CalcOutput nodes (448-456) and the READS-derived names (463-482) are dropped from the foot on this path. `reads_unmatched` (691-708) re-adds READS names that are not branch layers.
  - Failing case: a CalcOutput node of the trade day whose `calc-<name>` has no file key on the branch leaves the foot with nothing written. No check compares CalcOutput names against placed ∪ named.
- **Receipts and pictures are counted, not named.** Paths ending .json, .log, .md or .png, and the dipole/leg renders, go into `other` (`signal_packet.py:617-619`). They are counted as `ps["receipts"]` (687). That count does not appear in the foot or the afterwards file. A data `.json` on the branch would fall here.
- **One reason text is misapplied.** `signal_packet.py:665` gives every non-parquet layer the reason "Native's own episode lines". `native-episodes` is already caught by PLANE_NOT_PLACED (505, prefix match at 659), so the text only ever lands on other layers.
- **Plane lines in the text are cut to 110 characters** (`PLANE_ROW_CHARS`, 495), with the cut at 718-719. The line points to planes_since.json and the row is written whole there (`plane_since`, 770). A cut with a pointer, not a drop.
- **No average or smoothing in the planes code.** `known` is the row-wise `np.fmax` of instant columns (581). That is a max across a row's own instants, not a pool across rows.

### R2: after-the-fact data kept out of the packet; each row placed by its own time; afterwards ids refused
- **Placement.** A row is placed when the latest of its epoch-ns instants is ≤ moment (`placed_mask`, 589-590). Instants are chosen by magnitude [1e18, 2.5e18) on int64/double columns (575-581).
- **Times are compared in float64.** `astype("float64")` is at 577. At about 1.7e18 the spacing is 256 ns.
  - Arithmetic, not a measurement on rows: `float(1696206036000000100) == float(1696206036000000000)` is True.
  - A row known up to about 128 ns after the moment can be placed. `known_at_ns` (685, 738) is rounded the same way, so `plane_leak` (1229-1233), which compares the same floats, cannot see it.
- **Placement uses the row's latest instant, not the time the row became known.** PLANE_FILE_REASONS (435-440) and the legs entry (512-513) keep peaks and legs out for exactly that reason.
  - Layers with peaks/open-at-the-end/humps in their names have no PLANE_NOT_PLACED entry: `peak-lives` on the branch, `dipole-peaks`, `calc-*_peaks*`, `calc-*-open-at-the-end`, `research-humps`, `crypto-ng-tick-humps`.
  - `test_decider.py:627-628` asserts `research-humps` and `calc-leg_peaks-facts` are placed.
  - Required evidence: the 28 placed layers, each with the column `known` takes for it and whether that column is the time the row was known.
- **The whole-day row count reaches the decider.** `info["of"]` is the stored file's row count for the full trade day. It goes to:
  - the zero-row plane line, "({of} later…)" (732);
  - the foot, "k count of of" (1039);
  - `layers[...]["of_in_the_stored_file"]` (1184), written to layers.json by `serve.py:322-324`;
  - `pk["planes"]` (1185), handed to programs (`serve.py:331` removes only `plane_ids` and `plane_source`; README documents `{count, of}`).
  - Concrete case: a line "calc-sweeps-facts 12 of 340" tells the decider how many rows the layer will reach by the end of the day. `plane_leak` does not look at `of`.
- **afterwards_layers.json sits in the question folder before the decision.** It is written at `serve.py:318-321`, beside brief.md, state.json and planes_since.json. It now carries `stored_planes` with `rows_after`, `row_range` and `first_known_at_ns` (the time of the next row after the moment; about line 788).
  - The id refusal stops a decision from naming it; nothing in the change stops an agent that reads the folder from reading it.
  - `test_decider.py:691-692` checks only that the brief does not name it.
- **The afterwards-id refusal.** `PacketIds.__contains__` (`signal_packet.py:418-419`) accepts only layer_of ids, `state.` paths and `plane:<key>:<n>` below the count (`plane_id_ok`, 745-753). Anything starting `afterwards:` is not in it, and `validate_decision` (`serve.py:176`) rejects with "not in the packet". The settle path passes `plane_ids` as well (about `serve.py:350`). Read, not run here.
- **The door checks only each layer's head row.** `plane_since_check` (1247) and `afterwards_check` (835) have callers only in tests (`test_decider.py:552, 569, 640, 667, 687, 695`). At serve time, `leakage_check` → `plane_leak` (`serve.py:267`) checks each layer's single head line and its count. The rows written into planes_since.json (`serve.py:310-315`) are not checked by the door.
- **`earlier_planes_file`** (`serve.py:284-294`) picks the latest earlier `moment_ns` across all question folders of the mailbox. It does not check that trade_day, run or source commit match.
- **Programs are not handed plane rows** (`serve.py:331`). Programs get counts and heads only, as the README says.

### R3: trade days
- The plane path has no `root/tape.py` gate. `signal_packet.py` has no `root.tape` import (grep). The day comes from `trade_day_of` (133-138), which gives 17:00 ET and later to the next date: the halt hour goes to the next trade day, written as an exception in its docstring and not part of this diff.
- `PlaneSource.commit(day)` (541-547) reads any day for which a `root-rows-<ymd>` branch exists. Plane rows are placed by instant ≤ moment with no lower bound at 18:00 ET of the evening before.
- Only the existence of the branch limits which trade days are read. It is not the four-day gate.

### R4: no made-up data in a check
- All four plane checks build their packets on the hand-made STAND-IN state (`test_decider.py:288-289` "not market data", 312, used at 576, 619, 648, 676, 737). The planes and signals are real.
- Assertions that cannot fail: `test_decider.py:634` (`... or True`), `:694` (`... or True`), and `:698` (`rr["rows_after"] == rr["source"].get("rows_after", rr["rows_after"])`, which compares a value with itself because `source` has no `rows_after`).
- **The Excel check reads real workbooks but cannot fail for the rows and crypto sheets.** Every header lands in a, b or c through an else branch (`test_live_platform.py:269-270`, 279-282), so `set(placed) == day_columns` (288) always holds there. The 27/13/418 is printed, not asserted (294-295).
  - "a" comes from membership in `PLANE_PROJECT` or `dp.SHOWN`, not from a built packet. Mutation 3 shows this.
  - The 20 crypto and ng columns all get one reason (program trades). They include `onset_read_20s` and `exhaustion_20s_at_start` (header read from the workbook).

## Grounding check (`python3 -m tools.kgraph.grounding text`, run from /home/user/Markets)
- "the stored-rows day is about 1 GB in memory" returned `{"decision":"revise","claim":{"id":"text:3c95aed52ba1",...},"reason":"no claim in the graph carries the sentence's numbers together with its words","required_evidence":["a source line that states 1 together, about: stored-rows, memory"]}`.
- "...for each of 217 questions would be about 3.4 GB" returned `{"decision":"revise","claim":{"id":"text:8cf7080b9486",...},"reason":"no claim in the graph carries the sentence's numbers together with its words","required_evidence":["a source line that states the figure 3.4 (no claim in the graph carries it at all)"]}`.
- BUILD_NOTES.md:24 gives 15.5 MB at the last real signal and 1.12 GB at end of day. 217 × 15.5 MB ≈ 3.36 GB (arithmetic).

## Ticket open points 1 to 4 against the code today (74006f2)
1. **Still as described.** `PLANE_PROJECT` (518-519); whole blob read to memory (637-643); no reading by part or row group.
2. **Still as described.** PLANE_NOT_PLACED (496-514); the no-time rule (667-673); `planes_named` calc reasons (448-456). No function turns a tape position into its time (scout C: not found; I did not search further).
3. **Still as described.** The delta file chain is in `serve.py:284-315`; the afterwards references are in `plane_afterwards` (774-795). It is Greg's to accept or change.
4. **Not touched by this change.** `state_layer_list` (339-349) and `_leaves` (352-365) split a long `mbo_window` value into positional rows, which `resolve_state_id` (379-400) accepts as `state.mbo_window/[i]`. That is a position in the list, not the message's own id. The message fields were not located (scout D).

## Speculation (labelled; not measured)
- A plane column of Arrow type `timestamp[...]`, int32 or uint64 is not seen as an instant (575). `row()` turns datetimes into strings (657-658), so the late-instant scans at 1236-1237 and 1260-1261 would also miss it.
- A column holding a 0 or -1 sentinel fails `v.min() >= EPOCH_LO` (579) and stops counting as an instant for every row.
- Parts are sorted as text (621), so `-part10` comes before `-part2`. Row ids would then not follow stored order (placement is by mask, so it is not a leak).
- If the trade-day branch is missing, the `use_planes = False` before the raise at 939-940 does nothing.

## Open after this read

### For the builder (file:line)
- `signal_packet.py:577`: compare instants as int64, not float64.
- `signal_packet.py:732, 1039, 1184, 1185`: `of` (the whole-day row count) reaches the decider.
- `signal_packet.py:943-944`: the `.parquet` filter drops CalcOutput and READS names with nothing written.
- `signal_packet.py:617, 687`: receipts are counted, not named.
- `signal_packet.py:665`: the reason text is misapplied.
- `signal_packet.py:496-514`: the peak, open-at-the-end and humps layers are placed by their latest instant. Give the known-at column for each of the 28 placed layers.
- `serve.py:296-324`: run `plane_since_check` (1247) and `afterwards_check` (835) at the door, not only in tests.
- `serve.py:284-294`: match trade_day and source commit when choosing the earlier file.
- `test_decider.py:634, 694, 698`: assertions that cannot fail.
- `test_live_platform.py:269-270, 279-295`: assert the counts, and build a real packet for the "a" places.

### For the main session
- Get a run of the 36 skipped checks with a paper-trading-platform checkout and `MARKETS_PLANES_GIT` set (or `root-rows-20231002` fetched into markets-data/.git), then repeat mutations 1 and 2.
- Decide whether `afterwards_layers.json` may sit in the folder an agent decider reads (`serve.py:318`).
- Decide whether calc-research_columns (the per-tick dipole and exhaustion) being out of the packet is accepted under "the dipole above all".
- The two size sentences have no grounding path; required evidence is above.

### What code cannot hold
- Greg's call on open point 3: the delta chain versus the whole day per question.
- Whether peaks, humps and open-at-the-end rows may be placed by their latest instant: it depends on what each column means.
- The real shape of the MBO window: unknown until one pass of the tape (open point 4).

Limits: tool calls 11 of 22 (including this hand-back and one advisor call); 0 sub-agents; 0 writes to the graph or markets-data; the scratch folder /home/user/tmp-pytest/r182 was deleted after each run; the worktree is clean. I cannot measure the token total from inside the run.

