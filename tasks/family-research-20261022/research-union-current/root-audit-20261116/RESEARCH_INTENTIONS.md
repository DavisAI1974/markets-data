# What the Claude and Codex research set out to find, and the angle each took (2026-11-16)

Greg, 2026-11-16: "let's list the intended results and research angles. I don't think we want to keep the results.
They probably aren't calc correctly."

This file holds intentions and approaches only. No result, number, rate, verdict or conclusion from any of the
research is recorded here, and none is to be carried into new work. It is the first column of the calculation
inventory: what we want to figure out. For Greg to correct and sign off; the results themselves are removed after
that.

## Codex, in this research folder

| Project | What it intended to find out | Angle taken | Leaned on |
|---|---|---|---|
| `reanalysis-20261109` | Do two definitions of flow (midpoint-based and exchange-reported aggressor side) agree at the same decision time? Are large information ratios real or caused by sparse activity? Do information or display-change features add forecasting value beyond count, price and book? Is any move left after a one-tick confirmation? Do actual cancellations and additions that agree with traded flow matter? | Compare the two flow definitions in 5 s and 20 s windows at the same recognition clock. Rebuild the information measure over 20 one-second bins. Fit one fixed model date by date on earlier dates only, with and without the added features. Confirmation at +1 s and +5 s, outcome to +20 s and +60 s. Group cancellations as aligned, opposed, neutral or missing, by trade day. | per-second native flow, recognition contexts, the workbook |
| `discovery-depth-20261109` | Do recent price and book state add anything to flow at recognition time? Does full, near or touch depth change how flow agreement, adds, fills and withdrawals read? Once an order has survived to an observation clock, do fills or remaining display say anything about further survival? Do one-lot origin, age and onset history separate retreat, recovery and improvement? What do matched pre-birth controls and event order add? Is a flow change fresh volume or expiring volume? | Questions written before looking. Exact joins on date, candidate and nanosecond clock. Sign-combination cells against single components, per trade day and direction. Survival from 5 ms to 25 ms and 25 ms to 100 ms. Later moves at 1, 5, 20, 60 and 300 s. | the ten priority tables |
| `priority-ten-20261109` | Which ten missing evidence tables matter most for decisions, and what does each show across all four trade days? | Tables chosen for decision relevance, clock safety and coverage, not profitability. Every row kept. | per-second native flow, family flags, candidates, order lifecycles, matched pre-birth controls, one-lot origins |
| `fifteen-strategies-20261113` | Which different strategies fit different situations and trade stages: continuation, defended-liquidity reversal, failed continuation, quiet-flow release, follow or fade after recognition, cancellation-supported flow, expiry flips, one-lot retreat, dipole dive and rebound, fresh-flow handoff, pullback re-entry? | Specification only: one paper ledger per strategy, no voting between them; rules of the form setup, arm, later quote confirmation, exit. | the eleven earlier rule arms, earlier findings, the case views, Greg's V-shape idea |
| `paper-validation-20261109` | Do the rule contracts behave as specified: clock boundaries, arming, confirmation, guards, quote eligibility? | Unit tests on made-up inputs, and a read of the existing adapters. Note: made-up market inputs are against the standing rule. | the rule files |
| `evidence-availability-20261113` | For each of the 141 fields: what does it measure and when was it knowable? Which evidence does each strategy need? New questions: the delay from flow to quote response; displayed size against order count; time from withdrawal to return; movement in trade prints against movement in quotes; age, survival and information state; the vintage of outside data. Which horizons should be learned instead of inherited? | Audit of every field, case and tick against source groups and known-by clocks. Proposed: learn horizons per strategy and stage on time, exchange-event, trade-count and volume clocks. | the 32-case grid, the S fields, the outside values |
| Gap list G01-G08 | What does the dipole map look like for every trade from before birth to the end? Can the 19 S fields be reused? Can broken clocks be repaired? Can both workflow outputs be bound in? What order and queue context exists at each decision? When was each outside input first available? Can the 99 layers be bound per trade? | Gap closure trade by trade. | the trade list, workflow outputs, full-book sources |
| Gap list G09-G12 and the shape notes | Does natural gas show direction-specific shapes before birth, at the turn and in the tail and exhaustion, as the older crypto pictures did in concept? Is there a sub-second warning lead? How do exhaustion and strengthening contrast? How does flow authority weaken, collapse and recover? | Signed flow, the dive (rate of change of lean) and elapsed-time rates by phase and direction, on native clocks. | natural-gas paths, native shape forms |

## Desktop's family research (trade day Oct 18)

| Project | What it intended to find out | Angle taken | Leaned on |
|---|---|---|---|
| Pre-birth scope | Was anything observable before each family's recorded start? | From 120 s before the start up to the start; last known state plus every update; a row counts only if available strictly before the start. | 749 families, ROOT planes, the 13 outside points |
| Clock research scope | What did the market look like around families when everything is lined up on one clock? | A combined walk with event, receive and availability times kept separate, from 120 s before. | the outside tables, the 99 planes, the S fields, trade prices |
| Descriptive plan | Direction, momentum, exhaustion, pre-birth: what differs before, at and after a start, against nearby ordinary periods? | Before, onset and later kept separate; several elapsed-time horizons; nearby controls. | the aligned database, lifecycle rows |
| Model comparison | Taken together, how do the layers relate to later price moves and to how often families occur? Which layer combinations interact? | The same joined table fed to several kinds of model; forward folds with a 10-minute gap; drop-one-source-group comparisons. | fields at the moment, plus changes over 120, 300 and 600 s |
| Full-depth rerun | Do the comparisons change once every book level and corrected durations are added? | Refit with targets and folds unchanged. | all book levels, volume ahead |
| Full-context coverage | Was the full depth behind the 99 planes, queues and dipoles actually used, and what changes if it is? | A coverage gate before any rerun; dipole checks against written definitions. | the 99-entry registry, the S fields |
| Instance analysis | Two particular trades side by side: what differed in queues, replenishment and price before the moves, and could it have been seen in real time? Then every one of the 30,739 trades and its lifecycle. | Individual reconstruction on a common 120 s window, an availability timeline, and a ledger of what would disprove each idea. | saved quote and level exports |

## Claude

| Project | What it intended to find out | Angle taken | Leaned on |
|---|---|---|---|
| Reanalysis (Markets `agent-pass/reanalysis/claude/`) | What remains of a dipole lifecycle at the earliest clock it can be known? What separates continuation, failed start and reversal? Do large moves come back? How do thin one-lot touches end? Do pressure signals carry direction over 1 to 30 s? Does the book react to price changes, and is that a response or a shared cause? Is the dipole an exit cue? Which layers together sort the outcome? | Distributions at a decision clock over whole lifecycles, per trade day and never pooled. The tape replayed by order into end-of-second state. A look-ahead clock at +5 s. Matched controls as the general-market sample. Same-second and later-second effects separated. | the raw tape, whole-lifecycle tables, per-second paths, the 99 layers |
| Open questions | The join between the two detectors. Can weakening onsets warn earlier with a direction? Other lifecycle endpoints. A bid-heavy full book: a property of the session or a signal? Per-order lifetimes. | Each a small targeted test. | same |
| Paper strategies | Large-move fade; dipole logging; thin-touch nowcast; touch imbalance and refill nowcast; weakening-onset warning; dipole exit overlay; touch-queue read at the look-ahead clock. | Paper rules with each parameter marked as evidenced or provisional. | same |
| Independent research (markets-data `main`) | Where are the gaps in understanding, strategy design and faithful testing, and what hypotheses follow? | One case at a time, at tick level. | 32 cases chosen afterwards by realized moves, 141 fields |
| Cases, pins, derived | Ten illustrative cases; how each detector output maps to the 99-layer registry; what cross-day rank relationships look like when nothing is there. | Typical or extreme events picked by a stated rule; a field-to-layer map; shifted draws. | detector outputs, per-second tables |

## Questions that come up in more than one project

- Is a change in flow fresh aggression, or old volume dropping out of a window?
- How much of a move is left at the earliest moment a decision could actually be made?
- Is anything observable before a family's or dipole's birth?
- Do replenishment, survival or cancellation separate continuation from failure?
- What are exhaustion, the flip and the tail, and can they warn early?
- Do the layers add anything together that they do not add alone?
- When was each field or outside value knowable?

## Angles that depended on the old limits

Every project below was shaped by a fixed window, a fixed horizon, whole-second resolution or a top-N view. This is
the list of where an idea was limited by the foundation, as distinct from being a wrong idea.

- Codex reanalysis: 5 s and 20 s flow windows; 20 one-second bins; +1 s and +5 s confirmation; +20 s and +60 s
  outcomes; 60 s spacing.
- Discovery depth: observation clocks at +5, +25 and +100 ms; outcomes at 1, 5, 20, 60 and 300 s; per-second flow.
- Priority ten: the whole-second native flow table.
- Fifteen strategies and the rule files: 5 s and 60 s flow windows; confirmation within 5 s; recognition at +1 to
  2 s; 20 s exits; 120 s maximum hold.
- Evidence availability: case windows padded by 60 s; 32 cases chosen by trade prints.
- Desktop: the fixed 120 s pre-birth window; changes over 120, 300 and 600 s; horizons from 1 s to 3,600 s; a 600 s
  gap between folds; summarized queues in the first versions.
- Claude reanalysis: end-of-second book state; a +5 s look-ahead clock; outcomes at 60 s and 300 s; a 20 s dipole
  window; an endpoint at the third opposite second; a 3 s grid; a top-5 size layer; per-date thirds.
- Claude cases: chosen on moves at +60 s and +300 s; the eight trade types are labels made from what happened next.
