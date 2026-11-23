# What could not be settled (Claude, strategy step, 2026-11-23)

Each item: what is open, and the exact data or the decision of Greg's it needs. Claude's call is stated where one
was made, so the work does not wait on an answer.

## Needs a run (a pod, on Greg's "go" after the price)

1. THE TRY ITSELF. No version has been tried. One run would write, for every version and each trade day on its
   own, ONE LINE FOR EACH STANCE (the tick it was taken at and let go at; the best bid and the best offer at each,
   each on its own; the steps and prints between; the state it stood on; whether anything lay in the same exchange
   event), and the counts by cell. It would cover every tick of the four trade days (819,783; 878,671; 845,246;
   770,579), the 136,187 moves, the 17,304 humps and the trades on the tape (38,127; 41,410; 33,703; 30,739). The
   leakage gate comes first. NOT BUILT, NOT PRICED: it is put to him with the price when he wants it. Because the
   versions were formed on these trade days it would be a record, not a test.
2. THE BUILT-IN UNDER THE PAPER'S FINDING 4. How many of a run's third steps lie in the same exchange event as its
   second step (one order trading through several levels)? Until that is counted, part of "a level that was eaten
   leads on" (the paper's finding 4, versions CL01 and CL02) may be made by the event. Data: `calc-quote_runs-facts`
   and the rows' `exchange_event`. Added to `FURTHER_RESEARCH_LIST.md`.
3. THE COUNTS THAT ARE STORED BUT NOT MADE, one for each version marked "not counted yet" in `VERSIONS.md`: how a
   first step was made (CL03); a level only eaten since the quote took its price (CL04); the quotes at a trade
   leg's first step (CL05); both quotes stepped (CL06); the dipole just before a hump's first trade (CL07, CL08);
   the dipole at a run's second step (CL10, CL11); a reload at the best price being hit (CL12); an event through
   more than one level (CL13); a print on the other side at the top of a run (CL14). All read stored values; none
   needs a new line.

## Needs a decision of Greg's

4. A BLIND TEST needs a trade day beyond the four: its raw order tape, built the same way. Which trade day, and
   when, is his. Until then nothing here is more than a hypothesis.
5. TWO READS THAT CLAUDE TREATS AS READS OF STORED VALUES, NOT AS NEW LINES, his to strike:
   - CL04: one stored running total of `book_totals` subtracted from itself between two ticks the data sets (the
     tick the quote last moved, and now).
   - CL07 and CL08: the stored dipole line as it stood JUST BEFORE a trade (the read before the trade's own read,
     by place), so that the trade is not inside the value it is compared with.
6. THE VERSIONS WITH TWO USES (CL02, CL08, CL12, CL14): each is a warning with no direction and also a proposed
   stance against the move. Claude's call: both uses are written and both would be recorded. Which he wants is his.
7. NUMBERS LEFT OPEN AS HIS: how the largest way a level empties ("some filled, some pulled") would be split
   (CL01, CL02); how much more often counts as "much more often" (CL09).
8. CL15 CANNOT BE EVALUATED until he opens item 4 of the further research list ("do large moves come back").
9. HOW A REAL ORDER GETS IN AND OUT is in no version, on purpose: no fill, no cost, no size. The record of a
   stance is the best bid and the best offer, each on its own. On the followed quote alone, a move let go at its
   first step back stands one tick behind unless it took a third step. Whether that is enough to trade on is a
   question for after the try, and his.
10. WHAT WAS LEFT OUT ON CLAUDE'S OWN CALL, his to correct: the crypto and ng program's TURNS table (its turn
    amount was set on crypto results), with the program's trades. Still not for strategy: the information measure.
11. TWO COUNT FILES OF THE PEAK RESEARCH OF 2026-11-17 ARE CITED (Claude's own, of last week, made on the rebuilt
    rows and kept beside the running notes). `ATTRIBUTES_BY_PILE.json`, the peak with no window only: the whole
    evidence of CL14. `HOW_A_LEVEL_EMPTIED.json`: the FIFTH-step table under CL01 and CL02, the two "against"
    sentences drawn from it, and the "3 of 150" line added to the running notes. (Its third-step figures are the
    paper's own: the research run of 2026-11-23 was checked equal to this file.) They were read in the session
    without being named to him first: owned. Claude's call: they may be cited, marked as what they are, because
    they stand on the rebuilt data. If he rules that last week's research is out whole, those two tables, those
    sentences and that line come out and CL14 stands with no count behind it.
12. CODEX'S HANDOFF still asks for blind formation; this session formed on all four on his word. Not changed.

## Not supplied

- Any trade day beyond the four.
- `DavisAI1974/Basic_equations` (the original dipole equations): not attached; not needed for these versions.
