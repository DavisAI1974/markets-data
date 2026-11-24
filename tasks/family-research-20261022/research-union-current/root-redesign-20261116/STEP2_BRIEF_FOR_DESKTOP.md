# Step 2 brief for the Desktop session (written 2026-11-16, seventh session)

Greg asked for this so that the Step 2 plan can be worked on in Desktop while the code session builds and runs
Step 1. Read it top to bottom. It says what the system is, what Step 2 was, what has changed since, what to
prepare for Greg, and how to work without colliding with the code session.

## 1. Your job, and what not to do

**Do:** prepare the Step 2 plan with Greg. Step 2 is to be gone through with him result by result before any of it
is built: what each result is, whether it is pooled, what individual values lie underneath, and what changes under
his rules. Write it in plain words; he reads on a phone, one piece at a time.

**Do not:**
- build or run anything, write no code, start no pod, and do not touch AWS (it is off limits until Greg says);
- edit `ROOT_GAMEPLAN_DECISIONS.md` or `STEP1_STEP2_LAYOUTS.md` (the code session writes to them all the time);
- push to the Markets repository or to any `root-rows-*` branch.

**Write only to one new file:** `STEP2_PLAN.md` in this folder, on markets-data branch `ccr-349e2ffe-07p8od`.
Fetch and merge before every push (the code session pushes to the same branch, to other files). Put anything Greg
decides with you under a heading "Decisions (Greg's words)" in that file, with his words in quotation marks; the
code session copies them into the decisions file.

## 2. What the system is

**The goal.** Find out which pieces of market data dictate what happens next in front-month NYMEX natural gas, and
teach it to Frankie (the trading agent) by showing him historical trade days one tick at a time with everything
already worked out on the rows.

**ROOT** is the first set of calculations made from the tape, done once, in one place, that everything later reads.
- Part 1, the foundation, is built: for each of four trade days (Mon Oct 2, Tue Oct 3, Tue Oct 17, Wed Oct 18,
  2023) one row per tick of the full order tape, 217 fields: the message as the exchange sent it, what it did to
  the order book, the book at that tick, and 13 outside data points (positioning, weather, storage, the curve).
  About 770,000 to 880,000 rows a trade day. Stored on markets-data branches `root-rows-20231002`, `-20231003`,
  `-20231017`, `-20231018`.
- Part 2 is calculations added on top, one at a time. Each adds columns or facts and passes its own check. "Step 1"
  and "Step 2" are the first of these. They come from research done in August 2026 on 55 weeks of 2025-26 data
  (the "exhaustion chain" study), rewritten to read the tick rows with their caps and limits off.

**Where things are.**
- Decisions, every one in Greg's words: `ROOT_GAMEPLAN_DECISIONS.md` (this folder). The section "Seventh session"
  is the newest and governs.
- The Step 1 layouts and what is built: `STEP1_STEP2_LAYOUTS.md` (this folder).
- The approved foundation specs: `SPEC-root.md`, `SPEC-outside.md` (this folder).
- ROOT code: Markets branch `ccr-ebe7e38d-wwccru`, folder `root/` (calculations in `root/calcs/`).
- The newest handoff: `../NEXT_SESSION_HANDOFF_20261116F.md`.

**Where Step 1 stands today.**
- Piece 1, built and run on all four trade days: the signed trade flow over the last 20 seconds at every tick, and
  every peak of it. 34,278 peaks over the four trade days (about one every 9 or 10 seconds).
- Piece 2, being built now: what each peak did before and after. Recorded as facts at the tick each becomes known:
  the low the rise started from, each new low of the fade, the flow reaching zero, coming back (how long it stayed
  away), or being beaten by a larger peak, each with the price at that tick.
- The chain link, decided by Greg as "B": three models are taught on the four trade days and their full values are
  written per peak. To be laid out in detail once piece 2 exists. No chain depth is written.
- The family (A, B, C): not assigned inside the calculations. It is the base of the grouping afterwards.

## 3. Greg's rules that bear on Step 2 (all recorded in the decisions file)

- A TRADE DAY runs 6 pm Eastern the evening before to 5 pm Eastern on the named date. The 5 pm to 6 pm hour is its
  own marked stretch. Never a bare "day" or a bare date.
- ONLY THE FOUR TRADE DAYS enter any calculation. Data from outside them seats the order book and nothing else.
- Rows are ticks, columns are fields. Nothing collapsed, nothing dropped. A row holds only what was known at its
  tick; nothing is written back onto an earlier row.
- Every trade individually. No rates, averages or model scores as a readout. Two exceptions he has made: the
  20-second roll of the flow, and the chain link models. **Any averaging is an addition to the individual
  outputs, never a replacement of them.**
- **Caps and limits come off the Step 1 and Step 2 outputs.** No master list is wanted; name a limit only where it
  changes what comes out.
- **No fixed marks.** "Let the data be what it is and then we group after we see how they separate." Nothing is
  measured against a level, a length of time or a set of moments picked in advance.
- **No labels, groups or identifiers in advance.** "We hold off on labels and groups and identifiers until all 4
  days have run all their calcs and we'll see how they define themselves. We don't want to do that for them and
  that goes for all outputs in st1 and 2."
- **The old families are the base** of the grouping once the runs are done. "We'll see if they still group like
  that or differently or the same but with additions." And: "we will probably find they group themselves more
  ways than one with different pieces in different groups."
- **Step 2 gets a closer look before it is run.** Told that nearly every Step 2 result is pooled: "We'll have to
  look at step 2 closer before it's run. That might be intentional." So do not assume a pooled result is a fault.
- Every calculation is laid out for him (what we want, what it did, what changes) and approved BEFORE it is built.
- The old programs are rewritten, not patched. The old files stay untouched on their branches.
- Trade cost is not a market condition: no fee, slippage or fill assumption in anything.
- Bad or incomplete data that will not be used is not saved.
- He wants the step runs on pods, all four trade days at the same time. No pod starts until he has seen the pod
  type and the price.

## 4. What Step 1 was, in the old work (so Step 2 makes sense)

- **Events.** One reading a second of the 20-second signed trade flow. An "exhaustion event" was a peak of that
  flow that passed three gates (above the 0.85 level of its UTC clock day, the largest within 5 seconds either
  side, the strongest within 45 seconds). 235,170 events over 55 weeks.
- **The ending and the state after.** An event ended when its flow had been at or through zero for 3 seconds in a
  row. Sixty seconds after the peak each event was given one of four state names, which Step 2 uses as letters:
  **P** = persistent (the flow never reached zero in 60 seconds); **S** = collapsed, and the late flow reloaded on
  the same side; **O** = collapsed, and the late flow was on the opposite side; **X** = collapsed, late flow too
  thin to say.
- **Price after.** The move in ticks at 5, 10, 20, 30, 60, 120 and 300 seconds after the ending.
- **Family.** A, B or C from the shape of the 60 seconds before the peak (nearest of three frozen centres; A held
  94 in 100).
- **Chain depth.** Three models (ridge, nearest neighbours, extra trees), taught on blocks of 18 to 48 weeks,
  predicted what an event would do from the events before it. An event's depth (D1, D2, ...) was how many earlier
  events, counted back one at a time, improved the prediction in all three models. Out of 156,422 scored events:
  20,562 reached D1, 1,725 D2, 133 D3, 9 D4, 1 D5.

## 5. What Step 2 was ("Phase 2 characterization", 2026-08-17 and 18)

Step 2 took the frozen 55-week event table and the Step 1 chain depths and described the chains. It did not find
new events. Its results, one by one, with the kind of number each is:

| # | Result | What it did | Kind of result |
|---|---|---|---|
| 1 | The causal region | Checked that the model gains at depths 2 to 4 stayed positive in every block of weeks when only information known 30 or 60 seconds after an ending was used. | Model scores: a mean gain per model, per block. |
| 2 | Short and long chains | Counted how many chains reached each depth and the median time a chain took (65 s at D1, 143 s at D2, 216.5 s at D3, 279 s at D4). | Counts; medians and quartiles. |
| 3 | One origin, or rolling | Tested whether a deep chain is one ancestor carried along or a state refreshed from the last few events. Read as a rolling state machine: the last four states matter, not one old origin. | Odds ratios and test values, pooled per week. |
| 4 | The play search | Looked at exact strings of the predecessors' state letters (for example S,S,O,S or P,O,X) and the price move after the next event's ending, entered 5 seconds after the ending and left at 30 or 60 seconds. | Mean move in ticks per string per block; the share of weeks positive; p-values from a shuffle test. |
| 5 | The frozen paper play | `NG_CHAIN_D4_SSOS_CONTINUATION_V1`: the four events before must read S,S,O,S; enter with the current event's side 5 s after its ending, leave at 30 s. 1,242 cases in the base, mean +0.256 ticks, stated gross. | A rule with fixed entry and exit times; mean per block. |
| 6 | After the exit | For P,O,X parents: exit, reset, and wait for a later full setup. How long until the next one (median about 4 hours), how many events in between. | Counts, shares, medians. |
| 7 | Opposite and same side branches | Split P,O,X cases by whether the current event is on the opposite or the same side as the last X event; a "shallow" and a "deep" adverse group defined by fixed tick marks at +30 and +60 seconds. | Means, shares, Fisher test values. |
| 8 | Reusable pieces | Counted pairs and triplets of state letters that recur inside different chains (PP|S, PO|S, PPP|SS ...). | Counts per block. |
| 9 | Which pieces extend | For each pair, the share of chains that went on to the next depth, against the block's baseline. | A rate and a lift ratio (for example 1.27x). |
| 10 | Timing families | Fitted a mixture model to the log of the time chains took: three groups at D2 (about 126 s, 215 s, 798 s), two at D3. | Model-fitted groups and their centres. |
| 11 | Failed folds | Policy: a pattern that fails in one block is flagged and taken apart, never deleted. Example OOO followed by a flip, split by the event before. | A policy; per-context means. |
| 12 | The novelty screen | Removed every case already covered by the two known plays and listed other recurring strings that kept their sign across blocks. | A queue of candidates; means per block. |
| 13 | Aftermath checks | Earlier programs (2026-08-17) that gave, per state, the share of next events on the same side and the share of moves that continued, reversed or chopped. | Pooled rates with confidence bands. |

Read from the Step 2 programs themselves (not run): the main program takes exactly the 4 events before, one fixed
pattern, never across a week boundary; drops events whose predecessor ended, or whose next event began, within 60
seconds; cuts the weeks into fixed blocks (first 18 to learn, then two test blocks, then a confirmation block);
needs minimum counts of 3, 20 or 30 before a result is shown; and shows only the top 50 or top 80 patterns. No
assumed cost appears anywhere in the Step 2 programs.

## 6. What has changed since, that Step 2 has to be re-thought against

These are facts of the rebuild, not proposals. Each one touches most rows of the table above.

1. **The state letters do not exist as labels.** S, O, P and X were made from fixed marks (60 seconds, seconds 41
   to 60, a 3-second ending). Greg has ruled no fixed marks and no labels in advance. What exists instead per peak
   is what it did: each new low, reaching zero, coming back, beaten, with times and prices. So every Step 2 result
   written in letters needs to be re-expressed from those facts, or wait for the grouping.
2. **Chain depth is not written.** The chain link is three models taught on the four trade days, and their full
   values are kept per peak. D1, D2 ... as labels are not assigned in advance.
3. **About ten times as many peaks.** The gates are off. The old events are the largest of them.
4. **Four trade days, not 55 weeks.** There are no blocks of weeks, no "eras", no held-back week. Anything that
   rested on a result holding across blocks has nothing to hold across yet. Too rare to appear in four trade days
   is "not seen yet", not a contradiction (the old work counted chains 4 deep 9 times and 5 deep once).
5. **The trade day, not the UTC clock day or the week.** A chain cannot run across 5 pm.
6. **No fixed entry and exit times, no fixed tick marks.** The paper play's +5 s and +30 s, the "shallow" and
   "deep" groups at -1 and -2 ticks, the 60-second gaps: all are marks picked in advance.
7. **Pooled results.** Rows 2, 4, 5, 6, 7, 9 and 13 report a mean, a median, a rate or a lift with no individual
   values beside it. Greg's rule: an averaged figure is an addition, the individual values are always kept. His
   caution: the pooling in Step 2 may be intentional, so each one is looked at with him, not removed.
8. **Model-fitted groups** (row 10) are a grouping. Under his rule groups come after all four trade days have run,
   from how the values separate, with the old groups as the base.

## 7. What to prepare for Greg

For each of the 13 results (or however they are better split), in his three-part form:

- **What we want** it to tell us, in one or two plain sentences.
- **What it did**, including the kind of number and what it was pooled over.
- **What changes** under the rules above, and what individual values would be written per peak or per chain.

And for each, a plain answer to: is the pooling there on purpose (does the question only make sense over many
cases, such as "how often does this piece recur"), or was it only how the result was reported? Bring him the ones
where you are unsure as questions, one at a time. Keep a short list of what cannot be made on four trade days at
all, with the reason.

Do not decide for him. Where a point is a detail, make the call, state it, and let him correct it.

## 8. The historical Step 2 material in git (read-only)

All on the Markets repository, branch `chatgpt/ng-exhaustion-chain-phase2-20260817` (tip `1bec694`). Start with the
first two.

Findings and freezes:
- [Final freeze and handoff, 2026-08-18](https://github.com/DavisAI1974/Markets/blob/chatgpt/ng-exhaustion-chain-phase2-20260817/research/NG_EXHAUSTION_CHAIN_PHASE2_FINAL_FREEZE_20260818.md): the whole of Step 2 in thirteen short sections.
- [First findings and the paper play, 2026-08-17](https://github.com/DavisAI1974/Markets/blob/chatgpt/ng-exhaustion-chain-phase2-20260817/research/NG_EXHAUSTION_CHAIN_PHASE2_FINDINGS_20260817.md)
- [All agent findings](https://github.com/DavisAI1974/Markets/blob/chatgpt/ng-exhaustion-chain-phase2-20260817/research/NG_EXHAUSTION_CHAIN_PHASE2_ALL_AGENT_FINDINGS_20260818.md)
- [Findings addendum, P-O-X](https://github.com/DavisAI1974/Markets/blob/chatgpt/ng-exhaustion-chain-phase2-20260817/research/NG_EXHAUSTION_CHAIN_PHASE2_FINDINGS_ADDENDUM_POX_20260818.md)
- [After the exit: recurrence](https://github.com/DavisAI1974/Markets/blob/chatgpt/ng-exhaustion-chain-phase2-20260817/research/NG_EXHAUSTION_CHAIN_PHASE2_POSTEXIT_RECURRENCE_FINDINGS_20260818.md)
- [Timing and context](https://github.com/DavisAI1974/Markets/blob/chatgpt/ng-exhaustion-chain-phase2-20260817/research/NG_EXHAUSTION_CHAIN_PHASE2_TIMING_CONTEXT_FINDINGS_20260818.md)
- [Module novelty](https://github.com/DavisAI1974/Markets/blob/chatgpt/ng-exhaustion-chain-phase2-20260817/research/NG_EXHAUSTION_CHAIN_PHASE2_MODULE_NOVELTY_FINDINGS_20260818.md)
- [P-O-X branch reconciliation](https://github.com/DavisAI1974/Markets/blob/chatgpt/ng-exhaustion-chain-phase2-20260817/research/NG_EXHAUSTION_CHAIN_PHASE2_POX_BRANCH_RECONCILIATION_V2_20260818.md)
- [P-O-X same side, re-expression](https://github.com/DavisAI1974/Markets/blob/chatgpt/ng-exhaustion-chain-phase2-20260817/research/NG_EXHAUSTION_CHAIN_PHASE2_POX_SAME_POSTEXIT_REEXPRESSION_20260818.md)
- [Parallel recurrence reconciliation](https://github.com/DavisAI1974/Markets/blob/chatgpt/ng-exhaustion-chain-phase2-20260817/research/NG_EXHAUSTION_CHAIN_PHASE2_PARALLEL_RECURRENCE_RECONCILIATION_20260818.md)

Contracts and gates:
- [The study contract](https://github.com/DavisAI1974/Markets/blob/chatgpt/ng-exhaustion-chain-phase2-20260817/research/NG_EXHAUSTION_CHAIN_STUDY_CONTRACT_20260817.json): how a chain link was defined.
- [The gate into Phase 2](https://github.com/DavisAI1974/Markets/blob/chatgpt/ng-exhaustion-chain-phase2-20260817/research/NG_EXHAUSTION_CHAIN_PHASE2_GATE_20260817.json) (the file Greg sent on 2026-11-16).
- [The paper play freeze](https://github.com/DavisAI1974/Markets/blob/chatgpt/ng-exhaustion-chain-phase2-20260817/research/NG_EXHAUSTION_CHAIN_PHASE2_PAPER_PLAY_FREEZE_20260817.json)
- [Execute, reset, re-enter contract](https://github.com/DavisAI1974/Markets/blob/chatgpt/ng-exhaustion-chain-phase2-20260817/research/NG_EXHAUSTION_CHAIN_PHASE2_EXECUTE_RESET_REENTER_CONTRACT_20260818.json)
- [Reappearance watch map](https://github.com/DavisAI1974/Markets/blob/chatgpt/ng-exhaustion-chain-phase2-20260817/research/NG_EXHAUSTION_CHAIN_PHASE2_REAPPEARANCE_WATCH_MAP_20260818.json)

Programs:
- [The main Step 2 program](https://github.com/DavisAI1974/Markets/blob/chatgpt/ng-exhaustion-chain-phase2-20260817/research/ng_exhaustion_chain_phase2_characterize_20260817.py)
- [The four parallel lanes](https://github.com/DavisAI1974/Markets/blob/chatgpt/ng-exhaustion-chain-phase2-20260817/research/ng_exhaustion_chain_phase2_parallel_agents_20260818.py): pairs and triplets, extension, timing, true and false contexts.
- [Chain memory depth](https://github.com/DavisAI1974/Markets/blob/chatgpt/ng-exhaustion-chain-phase2-20260817/research/ng_exhaustion_chain_memory_depth_20260817.py)
- [Aftermath validation, second version](https://github.com/DavisAI1974/Markets/blob/chatgpt/ng-exhaustion-chain-phase2-20260817/research/ng_exhaustion_aftermath_validate_v2_20260817.py)
- [The Step 1 detector](https://github.com/DavisAI1974/Markets/blob/chatgpt/ng-exhaustion-chain-phase2-20260817/research/ng_exhaustion_chain_canonical_table_20260817.py), for the state letters and the price moves Step 2 reads.

Later work that built on Step 2 (for reference; it carries assumed trade costs in places, which do not come over):
branch [`chatgpt/ng-exhaustion-post-phase2-20260818`](https://github.com/DavisAI1974/Markets/tree/chatgpt/ng-exhaustion-post-phase2-20260818/research),
and the [original Step 1 file map](https://github.com/DavisAI1974/Markets/blob/chatgpt/ng-exhaustion-entry-timing-revival-20260818/research/NG_EXHAUSTION_CHAIN_STEP1_ORIGINAL_FILE_MAP_20260820.md).

## 9. Two things to know about the old Step 2 outputs

- The event tables themselves are not in git. They were GitHub Actions artifacts, now expired. The findings
  documents and the programs are what survives.
- The old work shares no dates with the four trade days (it runs 2025-06-29 to 2026-07-12). No old row can be laid
  against a tick row. What carries over is the questions and the definitions.
