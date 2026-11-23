# Independent strategy work for Codex

Prepared November 23, 2026, by Claude on Greg's word: "Update it so I can send it to codex so you two can have
parallel strategy sessions going on. No consulting with the other's work until everything is finished."

This is the handoff of November 13, 2026 ("Independent market research for Claude",
`main`: `tasks/family-research-20261022/claude-independent-research-20261113/HANDOFF.md`), brought up to date. Its
sections are kept. What changed is the data (rebuilt from the raw tape since November 16), the standing rules Greg
has set since, and the direction: this time it is addressed to Codex, and Claude runs the same step in parallel.
Where this file and the November 13 handoff differ, this file governs. That file is not changed.

## The user's instructions

Unchanged from November 13: Greg wants multiple useful strategies for different instances, conditions, and stages
of a trade. Useful information includes timing, participation, persistence, transitions, warnings, trade
management, and price response; it need not predict direction by itself.

Preserve every hypothesis you propose, including overlapping, opposing, weakly supported, and unresolved ideas.
Record limitations and contrary evidence without eliminating proposals, ranking down to one winner, or merging away
distinct ideas. A hypothesis with missing inputs stays, with an explicit statement that it cannot be evaluated. Do
not fabricate a signal or force an order when its conditions are not met.

TWO SESSIONS RUN IN PARALLEL, ONE BY CODEX AND ONE BY CLAUDE. NEITHER CONSULTS THE OTHER'S WORK UNTIL EVERYTHING IS
FINISHED. For Codex that means: do not read, list or search Claude's strategy outputs (they will be under
`tasks/family-research-20261022/research-union-current/strategy-20261123-claude/` on branch `ccr-349e2ffe-07p8od`);
do not ask to see them; do not compare against them. Claude is under the same rule for Codex's folder and for every
`codex/` branch. You may reach an overlapping idea; keep it on its own merits. When both are finished Greg says what
happens next; there is no step here to compare, filter, merge or pick winners.

DO NOT OPEN LAST WEEK'S STRATEGY MATERIAL (the fifteen candidates, the review and gap list of November 13, the
selected cases, the paper rules). It was made on data that was built wrong (cut on the wrong clock, two trade days
missing their first two hours, trades only). Nothing of it is carried: not a value, not a rate, not a rule. If you
have already read it, say so in your access record rather than claiming blindness, and do not use it.

Start in a fresh session.

## The task

1. FIRST MESSAGE: say how a strategy version is formed BLIND TO ITS OWN TRADE DAY. Only four trade days exist. A
   version that is to be tried on a trade day must be formed without that trade day's data and without anything
   learned from it. Greg, November 23: "we can have findings for previous days be known by later ones if need be":
   a later trade day may know what was found on an earlier one. Lay out exactly how you keep that (which trade days
   each version is formed on, which it is tried on, and what you had already seen of each trade day before you
   began, honestly).
2. THEN: 15 VERSIONS, laid out in one message. Each: the situation and the stage of a trade it is for; what must be
   observed, on which clock, known at which tick; the direction; how it arms, expires and resets; entry, management
   and what invalidates it; what it does when an input is missing; and what would show it to be wrong. Distinguish
   observations from proposed rules. Keep versions that overlap or oppose each other.
3. A version is a hypothesis. Nothing is "real" until it clears live. Report "works on X, not on Y", per cell,
   never "X failed".

The seven questions of November 13 stay as shared scope where they still apply: coverage and representativeness;
what each column means and when it was knowable; event order and what price movement is left after a decision
could actually be made; use during an active trade; conditions and mechanisms; reproducible specifications;
independent evaluation. Two changed: "the 141 original fields" are gone (see the data below), and COSTS ARE OUT
(see the rules).

## The standing rules (Greg's, all in force)

- A TRADE DAY runs 6 pm Eastern the evening before to 5 pm Eastern on the named date. Never a bare "day" or date.
  The hour from 5 pm to 6 pm belongs to neither trade day. The order book is carried through the week.
- ONLY THE FOUR TRADE DAYS (Oct 2, 3, 17, 18, 2023) enter any calculation.
- EVERY CALCULATION AT THE TICK, timed to the nanosecond. No time grid, and no mention of one as a time. A stored
  value is read at a tick BY ITS PLACE ON THE TAPE: several trades can share one nanosecond, and a read by time
  alone takes in trades that came after the tick (found and corrected on November 23).
- NO HARD CODED BEGINNING OR END TIME, and no window of our own choosing. The data says where an event starts and
  stops. The only spans allowed are the two of the crypto formulas below.
- DIPOLE AND EXHAUSTION ARE THE CRYPTO FORMULAS, MADE ON THE NATURAL GAS TAPE. Both are one figure: bought minus sold
  over bought plus sold, over the trades of the last 60 seconds (dipole) and the last 20 seconds (exhaustion), read
  at the nanosecond. They are stored; do not make your own line under those names. The natural gas lines ARE
  strategy inputs. CRYPTO DATA (anything measured on a crypto market) is in no analysis.
- NO MID PRICE. The best bid and the best offer are each their own column and are never combined.
- NO AVERAGING, POOLING, RANKING OR LABELS. Every trade and every event individually. No winner or loser label, no
  short or long label, no trade type made from what happened next.
- THE UNIT IS THE EVENT (one trade, a few trades in a row), not the trade day. The measure of any output: does it
  help us understand the price and trade curve.
- TRADE COST IS NOT A MARKET CONDITION. No fee, slippage, maker or taker offset, fill model or any other execution
  assumption enters any research calculation or output. Research numbers are gross. No rule from the crypto era is
  brought over.
- ZERO SYNTHETIC OR MADE-UP DATA, not even to check code. Real tape only.
- THE LEAKAGE GATE comes before any backtest: what a version knows at a tick must not change when later ticks
  change. The daily settlement window (2:28 to 2:30 pm Eastern) is marked on the tape; keep it out of a backtest.
- Wrong or incomplete data that will not be used is not saved. Valid data is never discarded.

## Data that must be used

All of it is the tape of the natural gas front-month future (NYMEX), order by order, rebuilt since November 16.
The eight trade types, the 32 selected cases and the 141 fields of November 13 are NOT used.

`DavisAI1974/markets-data`, one branch for each trade day: `root-rows-20231002`, `root-rows-20231003`,
`root-rows-20231017`, `root-rows-20231018`. On each, `FILES.md` explains every file and every receipt describes
every column and the checks it passed. Clone each as its own shallow copy and add the files you need by name. Do
not list a branch with file sizes: that downloads every file.

- `rows-<trade day>-part*.parquet`: EVERY TICK (819,783; 878,671; 845,246; 770,579 ticks of the trade day), 408
  columns: the message, the book at that tick (best bid, best offer, sizes, orders, both sides), the marks of what
  changed, and the outside figures with the moment each became known.
- `calc-<name>-<trade day>-part*.parquet`: a calculation's columns, one file beside each rows file, the same rows
  in the same order; and its tables of lines (`calc-<name>-facts-...`). The runs of the quote, the book totals,
  refills, sweeps, orders moving together, the trade legs, the peaks with no window, the resting orders through a
  move, the steps of a move.
- `crypto-ng-tick/`: the exhaustion line (`...line-20s...`), the dipole line (`...lean-60s...`), every trade on the
  tape (`...tape-trades...`), the humps of the exhaustion line (`...humps...`).
- `research-threads/`: one line for every move in price and one for every hump, with stored values laid beside
  each. `info-measure/`: the information measure at every read of the exhaustion line.
- `calc-research_columns-<trade day>-part*.parquet`: the exhaustion line, the dipole line and the information
  measure at every tick, and each move and hump on its own tick, beside the every-tick rows.

WHAT MAY FEED A VERSION, as Claude reads Greg's rulings together (put to him; his to correct):
- IN: the rows; the calculations with no window (`quote_runs`, `book_totals`, `refills`, `sweeps`, `together`, the
  trade legs, the peaks with no window, `resting`, `move_steps`); the natural gas dipole line, exhaustion line and
  humps.
- OUT: the 20-second peak family (`flow_peak`, `peak_story`, `peak_links`, `open_stories`, `chain_peaks`,
  `dipole_peaks`); Native's dipole record (built on fixed windows); the crypto and ng program's own trades and
  prices (its settings were tuned on crypto results); the mid price; any crypto data; last week's strategy
  material.
- NOT YET FOR STRATEGY: the information measure (`info_...`). It is the crypto information dipole operator on
  twenty one-second pieces. Where all the trading of the 20 seconds is on one side its ratio is made by the
  division (marked `info_ratio_made_by_division`), and it has not yet been compared with the original equations.

## Reading the shared record

The decisions and the notes are common ground for both sessions; they are not either session's strategy work.
Branch `ccr-349e2ffe-07p8od` of `DavisAI1974/markets-data`, under
`tasks/family-research-20261022/research-union-current/`:

- `root-redesign-20261116/ROOT_GAMEPLAN_DECISIONS.md`: every decision of Greg's, with his words.
- `root-audit-20261116/RESEARCH_INTENTIONS.md`: the earlier research questions, with no result.
- `root-redesign-20261116/FURTHER_RESEARCH_LIST.md`: research set aside for later. Not part of this task.
- `root-redesign-20261116/peak-research-20261117/TRADE_LIFECYCLE_NOTES.md`: the running notes. READ WITH CARE: its
  counts were read from ALL FOUR trade days. A version must be formed blind to the trade day it is tried on, so
  say in your first message how you use these notes, or leave them shut.
- Do not open `strategy-20261123-claude/` there.

Code, if you need to read how a stored column was made: `DavisAI1974/Markets`, branch `ccr-dd95052b-3vcrwq`,
folders `root/`, `crypto_ng/`, `odcore/`. Calculations receive ticks only through the two gates of `root/tape.py`.

## Access limits and missing information

Use your own authenticated GitHub access. Test a source through your own tools and distinguish
downloaded-and-verified from referenced-but-unavailable. Do not claim you read a source you could not open.

Not supplied: any trade day beyond the four; a working platform connection; credentials. If you need something
that is not stored, name it exactly (trade day, stream, columns, clock) and carry on with what does not depend on
it. This is research and specification work: do not submit orders, start execution, or change accounts. No pod,
box or paid run starts without Greg's word "go" after he has seen the price.

## Expected outputs

Save to `DavisAI1974/markets-data` on your own `codex/` branch, under
`tasks/family-research-20261022/research-union-current/strategy-20261123-codex/`. Commit, push, confirm the remote
commit, and give Greg the links in the same session. Change nothing that exists.

1. `ACCESS_RECORD.md`: what you opened and verified, what was missing, and whether anything of last week's strategy
   material or of Claude's strategy work was visible to you.
2. `BLIND_FORMATION.md`: your first message: how a version is formed blind to its own trade day.
3. `VERSIONS.md` (and a machine-readable copy if you want one): the 15 versions, each as the task above says, with
   ids such as `CX01`. Version any revision; keep every proposal.
4. `EVIDENCE.md`: for each version, the source-linked observations behind it and the contrary and unresolved ones,
   each trade day on its own, every case individually, nothing pooled.
5. `OPEN_QUESTIONS.md`: what you could not settle, the exact data or decision of Greg's each needs.

Greg reads on a phone: answer in the first lines, plain words, a whole plan in one go.
