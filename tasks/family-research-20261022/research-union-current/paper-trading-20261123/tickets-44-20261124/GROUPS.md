# Which ticket is in which group (2026-11-24, twenty-fifth session)

Greg, 2026-11-24: "You said that these tickets were grouped together before. Let's get a full suite of 4 types of
agents on each ticket group. We can start new sess first though".

The groups are the fourteen of `../tickets-20261124/` (that folder is not changed). The 47 numbered tickets of this
folder stay the tracker: a box is still marked ticket by ticket, with its evidence. The group is what a suite of
agents is given. A suite is the four kinds: scout, builder, reviewer, performance auditor.

HOW THIS TABLE WAS MADE. Each group file ends with "Missing pieces covered" (for example `A1, A2, A3, A11`); the
number in each code is the ticket's number. Where a ticket is named by two group files it is put in ONE, the first,
and the other is noted. Ten tickets are named by no group file: 03b, 16, 17, 21, 23, 37, 43, 44, 45 and 46. Each is
PLACED BY CLAUDE below and marked "(placed)"; these placements are his to correct. Seven more are named in the old
README only as "held and not ticketed": they are in the last row.

| Group (file in `../tickets-20261124/`) | Its tickets here | Can a builder work on it without his go? | State at the close of the twenty-fifth session |
|---|---|---|---|
| G01 One claim defended, end to end | 01, 02, 03, 11 | Yes for 01, 02, 03. 11 waits on 05. | 02, 03: built, read four times; the fourth read's points built by run 147 and NOT READ. 01: ten claim files written; none registered or challenged. |
| G02 The grounds read into the graph | 07, 08 | NO: the reads need his go (budget told then). | Located only (scout run 117). |
| G03 The loop takes only defended claims | 04 (its other items, 01 to 03, are in G01) | Yes | 04: built (run 137), read once (run 146); its points are open for the builder. |
| G04 The check after a trial, and adverse evidence | 05, 06, 09 | Yes to build; shown on tape only with his go | Planned (`PLAN_03b_04_05_06_v2.md`); not built. Same file chain as G01 and G03. |
| G05 Artifact and metric nodes | 25, 26, 37 (placed) | Yes for 25 and 37. 26 waits on 06. | 25: built in two parts (run 130); the second part not read. 37: located (scout run 152). |
| G06 The hybrid session start | 20 (the session half), 32 | 32 waits on 25. 20 waits on 32. | Not started. |
| G07 Every data layer to the decider | 38, 39 | Yes for 38. 39 waits on 38, 02 and 03. | 38 partly built and OPEN (418 of 458 columns not given to a decider). |
| G08 A budget and a full record for every agent run | 18, 19 | Yes | Both built; 18 read three times (run 149), 19 read four times (run 148). |
| G09 The agents used as their files say | 12, 13, 14, 15, 03b (placed), 16 (placed) | Yes for 12, 13, 14, 03b. 15 and 16 are his decision. | 03b: DONE, marked with its evidence (the check exits 0 at markets-data `9a8f404`). 12, 13, 14: shown by how the runs are made, not written up. |
| G10 Refute wave | 10 | NO: his go, budget told then. Waits on 01. | Not started. |
| G11 The real graph put in order | 27, 30, 31, 21 (placed), 44 (placed), 46 (placed) | Yes for 31, 21, 44, 46. 27 is a model run: its budget is told first. 30 waits on 44. | 21 and 31: located (scout runs 150, 151). 46: its ticket says it is worked at its place in the order or when he says sooner. |
| G12 First pass on tape | 40, 41, 43 (placed) | NO: his go, told with its budget. 43 can be built; it starts with a run. | Not started. The platform cannot be pushed to from a session: push access was refused. |
| G13 The loop's first start | 22, 23 (placed) | NO: his go and his figure. | Not started. |
| G14 Frankie's own events as the trigger | 36 | NO: his decision. | Not started. |
| G15 An operator for the natural gas market (added on his word, 2026-11-24; no file in the old folder) | 47 | WORKED LAST, on his word of the twenty-sixth session: after the rest of the list and after the 30 minute test without the operator coefficients (G12). Then locating and planning: yes. Any calculation: NO, his word on the state and the target and his go with the budget first. | Located in part (scout run 155). Codex brought the discovery pipeline to Markets `od-refrag/markets-handoff` (`93ac56f`); only its README is read. |
| Outside the groups | 45 (placed): the independent review at the end, two readers who built none of it. | After every worked ticket. | Not started. |
| Held, no suite until he says | 17 (placed), 24, 28, 29, 33, 34, 35, 42 | NO: each needs his go or decision; most need a model key that does not exist or receipts that are on AWS. | Not started. |

Every one of the 48 is in exactly one row (47 was added at the close): 01 02 03 03b 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24
25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47.

## What limits how many suites work at once

- ONE BUILDER FOR ONE CHAIN OF FILES. G01, G03 and G04 all change `tools/kgraph/defend.py` and
  `tools/kgraph/outcome.py`: their builders work one after another, not side by side. G05, G08, G09 and G11 touch
  other files and can be built beside them.
- ONE WRITER INTO THE REAL GRAPH AT A TIME, from a clean copy that holds its whole history.
- Run numbers are given out by the main session only. A run's limits are in git before it starts, and he is told
  the limits first, with the total across the suites.
- A group that waits on his go or his decision gets a scout at most, and no build.

## The order from the twenty-sixth session (Greg, 2026-11-24)

"Is everything else on the build list done? Of not, finish that first. ... let's save the od part for the very last
after we do a 30 min test without it". So: (1) every group a builder may work on without his go; (2) G12, the 30
minute test of the agents without the operator coefficients, on his go, told with its limits; (3) G15, ticket 47;
(4) the same test with the coefficients, set beside the first. A send-back is a new run with its own plan (the
decisions file, twenty-sixth session).

## Where each group stood at the close of the twenty-sixth session (2026-11-24)

Each worked ticket's own file ends with its state at this close. No box was marked after tickets 21 and 31: the
auditor's rows for the last runs are owed (start page AD, its first job), and he said no more agents were to be
started in the session.

| Group | Where it stands | Next |
|---|---|---|
| G01 (01, 02, 03, 11) | 02 and 03 read a fifth time: 79 checks run clean; three small points for the builder. 01 not started. | The three points; the proposer names commit `b134dc4` on eight grounds of three claim files; then ticket 01's four steps (they write into the real graph). |
| G03 (04) | The six points of reviewer run 146 are on GitHub (Markets `17869d4`, `e9e052f`). See `04.md` for the last run. | One reviewer read against the done-line. Then G04 (05, 06, 09), the same chain of files. |
| G05 (25, 26, 37) | 25: points 1 and 2 on GitHub; one check fails because of the record; points 3 and 4 not started. 37: the done-line is not met; needs a builder. | Ticket 19's recorder fix first (it clears 25's failing check); then 25's points 3 and 4; then 37 from scout 197. |
| G06 (20, 32) | Not started (waits on 25). | |
| G07 (38, 39) | Plan written, read by the reviewer, laid against his words and the daily sheets; the code of the layers read by two scouts; parts C and D with a builder (see `38.md`). Parts A, B and E not started. | The known-at table from the plan's foot; ONE builder for A, B and E; one reviewer read with the stored planes present. |
| G08 (18, 19) | Both built and read. Two faults found in the main session's own correcting lines (see `19.md`). | A builder for the recorder (a correcting line takes its session and its unstated fields from the line it corrects); the auditor's row for run 194; then both boxes. |
| G09 (12, 13, 14, 15, 03b, 16) | 15 answered by him. 14 read: nine points for the builder; the platform change `28d4dbb` not yet read. 12 and 13 shown, not written up. | 14's builder and its second read; the write-ups of 12 and 13. |
| G11 (27, 30, 31, 21, 44, 46) | 21 and 31 DONE. 46: built and read once; the one builder pass was under way (see `46.md`). 44: one piece built. | Mark 46 when its pass is in and audited. |
| G12, G13, G14, G10, G02, held | Not started: each needs his go or his decision. | The sheet `../to-questionnaire-what-only-greg-can-say.md`. |
| G15 (47) | LAST, on his word. Only the README of Codex's branch is read. | After the 30 minute test without the coefficients. |
