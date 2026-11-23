# The evidence behind each version (Claude, 2026-11-23, eighteenth session)

## How to read it

- EVERY FIGURE IS A COUNT OF LINES OF ONE TRADE DAY, in the order Oct 2; Oct 3; Oct 17; Oct 18 (2023). Nothing is
  added across trade days, nothing is averaged, and no share is written. Where a sentence says "more often, set
  against their number", the two pairs of counts in the table beside it were compared by hand and the sentence
  is that comparison; the counts are there to check it. No test of chance has been made: each count is a lead,
  not a result.
- EVERY FIGURE WAS COPIED BY SCRIPT from a stored receipt or count file, not typed: the receipts
  `research-threads/RESEARCH-THREADS-<trade day>.json` and `CALC-<name>-<trade day>.json` and
  `crypto-ng-tick/CRYPTO-NG-TICK-<trade day>.json` on the four daily branches (`root-rows-20231002` `360fdaa`,
  `-20231003` `c8a0b75`, `-20231017` `733442a`, `-20231018` `1bd670e`), and two count files of the peak research of
  2026-11-17 beside the running notes (`HOW_A_LEVEL_EMPTIED.json`, `ATTRIBUTES_BY_PILE.json`: the peak with no
  window only). All 36 count tables of the research receipts are whole in `EVIDENCE_COUNTS.md`.
- NO STORED TABLE OF MARKET DATA WAS OPENED AND NOTHING WAS CALCULATED for this file. The single lines are in the
  stored tables named under each rule.
- THE RULES ARE NOW v2 (paper-trading rules). Where v2 changed a rule the heading says so. Paper trading is the
  test (Greg, 2026-11-23).
- THE VERSIONS WERE FORMED ON THESE SAME FOUR TRADE DAYS. A count below is where an idea came from. It is not a
  test of it.
- "none" means that trade day's receipt has no such row.

## CL01. The eaten level: with the run. CL02. The abandoned level: not followed

Source: the paper's finding 4; receipts, table "how the first level emptied by the second step".

**Runs of the quote that took a second step, by what became of the orders at the first level, and whether a third
step followed**

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| Best offer up, every order filled: took a third step | 53 | 39 | 91 | 83 |
| Best offer up, every order filled: two steps only | 70 | 111 | 137 | 79 |
| Best offer up, some filled, some pulled: took a third step | 362 | 368 | 419 | 438 |
| Best offer up, some filled, some pulled: two steps only | 597 | 731 | 678 | 597 |
| Best offer up, every order pulled: took a third step | 63 | 20 | 24 | 26 |
| Best offer up, every order pulled: two steps only | 149 | 81 | 111 | 151 |
| Best bid down, every order filled: took a third step | 60 | 51 | 60 | 74 |
| Best bid down, every order filled: two steps only | 75 | 98 | 113 | 80 |
| Best bid down, some filled, some pulled: took a third step | 383 | 321 | 461 | 422 |
| Best bid down, some filled, some pulled: two steps only | 677 | 626 | 784 | 708 |
| Best bid down, every order pulled: took a third step | 37 | 26 | 43 | 50 |
| Best bid down, every order pulled: two steps only | 107 | 100 | 153 | 195 |

The same runs from the count file of 2026-11-17, which also holds a FIFTH step:

**The same runs: how many, how many took a third step, how many took a fifth step**

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| Best offer up, every order filled: moves | 123 | 150 | 228 | 162 |
| Best offer up, every order filled: took a third step | 53 | 39 | 91 | 83 |
| Best offer up, every order filled: took a fifth step | 10 | 3 | 17 | 18 |
| Best offer up, some filled, some pulled: moves | 959 | 1,099 | 1,097 | 1,035 |
| Best offer up, some filled, some pulled: took a third step | 362 | 368 | 419 | 438 |
| Best offer up, some filled, some pulled: took a fifth step | 45 | 42 | 81 | 74 |
| Best offer up, every order pulled: moves | 212 | 101 | 135 | 177 |
| Best offer up, every order pulled: took a third step | 63 | 20 | 24 | 26 |
| Best offer up, every order pulled: took a fifth step | 12 | 3 | 2 | 2 |
| Best bid down, every order filled: moves | 135 | 149 | 173 | 154 |
| Best bid down, every order filled: took a third step | 60 | 51 | 60 | 74 |
| Best bid down, every order filled: took a fifth step | 8 | 10 | 8 | 14 |
| Best bid down, some filled, some pulled: moves | 1,060 | 947 | 1,245 | 1,130 |
| Best bid down, some filled, some pulled: took a third step | 383 | 321 | 461 | 422 |
| Best bid down, some filled, some pulled: took a fifth step | 61 | 42 | 68 | 58 |
| Best bid down, every order pulled: moves | 144 | 126 | 196 | 245 |
| Best bid down, every order pulled: took a third step | 37 | 26 | 43 | 50 |
| Best bid down, every order pulled: took a fifth step | 6 | 0 | 9 | 11 |

- BEHIND CL01 AND CL02: in every one of the eight rows (four trade days, best offer up and best bid down) the
  third step came more often after "every order filled" than after "every order pulled", set against the number
  of runs in each.
- AGAINST CL01: the "every order filled" rows are small (the first table), and in seven of the eight more runs
  ended at two steps than took a third (the exception: best offer up on trade day Oct 18). By the FIFTH step the
  lead is not there in every row: on trade day Oct 3, best offer up, the eaten runs reached a fifth step least
  often of the three ways, set against their number (second table).
- AGAINST CL02 as a rule to act on: the pulled-only rows are small too, and by the fifth step the pulled-only runs
  are no longer the ones that went on least in every row (second table: trade day Oct 2, best offer up).
- UNRESOLVED: (1) how many of those third steps lie in the SAME exchange event as the second step (one order
  trading through several levels). Until that is counted, part of "an eaten level leads on" may be built in.
  (2) The largest way, "some filled, some pulled", is in neither version. (3) Only the first level of a run is
  stored this way.
- THE OTHER TWO DIRECTIONS (a better quote stepping in front), counted apart, no stance taken:

**Best offer down and best bid up: the same read**

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| Best offer down, every order filled: took a third step | 84 | 70 | 82 | 69 |
| Best offer down, every order filled: two steps only | 222 | 193 | 210 | 189 |
| Best offer down, some filled, some pulled: took a third step | none | none | none | none |
| Best offer down, some filled, some pulled: two steps only | none | none | none | none |
| Best offer down, every order pulled: took a third step | 59 | 43 | 74 | 66 |
| Best offer down, every order pulled: two steps only | 146 | 164 | 179 | 169 |
| Best bid up, every order filled: took a third step | 76 | 89 | 84 | 60 |
| Best bid up, every order filled: two steps only | 187 | 229 | 177 | 141 |
| Best bid up, some filled, some pulled: took a third step | none | none | none | none |
| Best bid up, some filled, some pulled: two steps only | none | none | none | none |
| Best bid up, every order pulled: took a third step | 65 | 53 | 73 | 63 |
| Best bid up, every order pulled: two steps only | 139 | 136 | 161 | 157 |

## CL03. The first step made by a fill. CL04. A level that has only been eaten, before it gives. CL09 (v2). The first step made by a cancel

Source: the paper's finding 1; receipts, table "how much of a move was left at its first step".

**Runs of the best offer up and of the best bid down, by how many steps they made in all**

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| Best offer up: 1 step in all | 5,462 | 5,961 | 5,411 | 5,180 |
| Best offer up: 2 steps in all | 872 | 976 | 964 | 880 |
| Best offer up: 3 steps in all | 341 | 302 | 337 | 336 |
| Best offer up: 4 steps in all | 94 | 95 | 116 | 136 |
| Best offer up: 5 steps in all | 42 | 30 | 69 | 57 |
| Best bid down: 1 step in all | 5,298 | 6,054 | 5,717 | 5,321 |
| Best bid down: 2 steps in all | 882 | 902 | 1,104 | 1,050 |
| Best bid down: 3 steps in all | 297 | 272 | 377 | 361 |
| Best bid down: 4 steps in all | 114 | 105 | 123 | 120 |
| Best bid down: 5 steps in all | 47 | 37 | 55 | 46 |

- BEHIND: nothing counted at the first step or before it. Both versions carry finding 4 earlier in the move. The
  table shows what is at stake there: most runs make one step only.
- AGAINST: the paper, in its own words: "Nothing yet warns BEFORE a move's first step: only the lines AT the first
  step and at the end were read."
- CL09 (v2) stands on the same two things read the other way: a level that was only pulled led on least often
  (the table under CL01 and CL02), and most runs end at one step (this table).
- UNRESOLVED: how many first steps are made by a fill and how many by a cancel; what follows each. For CL04, how
  often a level is traded into with nothing pulled or added since the quote took that price.

## CL05. A first step with the exhaustion line on its side (v2: trade legs only)

Source: the paper's findings 2 and 3; receipts, tables "the exhaustion_20s line at the first step" and "the print
against the quote".

**Moves by where the exhaustion line stood at their first step, and whether they took a second step**

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| Best offer up, line on its side: took a second step | 716 | 681 | 893 | 800 |
| Best offer up, line on its side: one step only | 2,551 | 3,006 | 2,889 | 2,648 |
| Best offer up, line against it: took a second step | 598 | 682 | 571 | 580 |
| Best offer up, line against it: one step only | 2,731 | 2,788 | 2,338 | 2,256 |
| Best offer down, line on its side: took a second step | 712 | 687 | 751 | 747 |
| Best offer down, line on its side: one step only | 2,674 | 2,884 | 2,195 | 2,185 |
| Best offer down, line against it: took a second step | 651 | 619 | 814 | 747 |
| Best offer down, line against it: one step only | 2,464 | 2,899 | 2,783 | 2,509 |
| Best bid up, line on its side: took a second step | 657 | 686 | 932 | 808 |
| Best bid up, line on its side: one step only | 2,514 | 2,814 | 2,908 | 2,535 |
| Best bid up, line against it: took a second step | 629 | 709 | 659 | 702 |
| Best bid up, line against it: one step only | 2,559 | 2,865 | 2,535 | 2,453 |
| Best bid down, line on its side: took a second step | 708 | 724 | 794 | 849 |
| Best bid down, line on its side: one step only | 2,631 | 3,022 | 2,510 | 2,468 |
| Best bid down, line against it: took a second step | 595 | 566 | 808 | 689 |
| Best bid down, line against it: one step only | 2,485 | 2,826 | 2,992 | 2,569 |
| Trade leg up, line on its side: took a second step | 546 | 607 | 695 | 569 |
| Trade leg up, line on its side: one step only | 876 | 1,184 | 833 | 670 |
| Trade leg up, line against it: took a second step | 507 | 542 | 470 | 470 |
| Trade leg up, line against it: one step only | 1,029 | 1,003 | 738 | 738 |
| Trade leg down, line on its side: took a second step | 598 | 580 | 512 | 530 |
| Trade leg down, line on its side: one step only | 899 | 993 | 658 | 679 |
| Trade leg down, line against it: took a second step | 508 | 523 | 620 | 516 |
| Trade leg down, line against it: one step only | 943 | 1,244 | 928 | 701 |

**Trade legs: where both quotes stood at the leg's END against the leg's first trade**

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| Trade leg up, 1 step: both quotes where they were | 1,202 | 1,313 | 856 | 744 |
| Trade leg up, 1 step: not both where they were | 762 | 952 | 773 | 721 |
| Trade leg up, 2 steps: both quotes where they were | 54 | 67 | 83 | 54 |
| Trade leg up, 2 steps: not both where they were | 639 | 695 | 630 | 569 |
| Trade leg down, 1 step: both quotes where they were | 1,121 | 1,466 | 834 | 769 |
| Trade leg down, 1 step: not both where they were | 793 | 849 | 818 | 686 |
| Trade leg down, 2 steps: both quotes where they were | 60 | 79 | 78 | 55 |
| Trade leg down, 2 steps: not both where they were | 646 | 677 | 599 | 572 |

- BEHIND: in most cells more moves took a second step, set against their number, when the line stood on their
  side at the first step.
- AGAINST: it reads the other way in three cells, all on trade day Oct 3 and all upward: best offer up, best bid
  up, trade leg up. In several other cells the two are close. The paper's own heading: it "says little" for a run
  of the quote.
- BUILT IN: a trade leg's first step is a print and that print is in the line.
- UNRESOLVED: the second table is read at a leg's END. Whether the quotes had moved AT the first step (the
  condition CL05 uses) is not counted.

## CL06. Both quotes have stepped the same way

Source: the paper's finding 2 (the table above), by analogy; the receipts of `quote_runs` and `sweeps`.

**How often the quote was touched or crossed (no stance is taken then)**

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| Ticks with the book crossed | 1,858 | 2,084 | 1,886 | 1,910 |
| Times the quote touched or crossed | 587 | 636 | 553 | 557 |
| Runs of the best bid started | 13,332 | 14,780 | 14,813 | 13,877 |
| Runs of the best offer started | 13,680 | 14,767 | 13,864 | 13,268 |

- BEHIND: nothing counted on the state itself. The analogy: a trade leg of two steps has nearly always moved a
  quote, a one-step leg mostly has not.
- AGAINST: none counted. By eye on one trade (running notes, sixteenth session): the offer moved back and forth a
  tick several times while the bid stood.
- UNRESOLVED: how often the state begins, and what the next step of either quote is.

## CL07. Fresh trading on the dipole's side. CL08. Fresh trading against the dipole. Rule 6 of all fifteen (v1's CL09): a change of side made by the span

Source: the paper's findings 5 and 6; receipts, tables "how a hump began" and "what came first after a hump
began"; the crypto and ng receipt.

**Humps of the exhaustion line, by how they began**

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| Humps in all | 4,459 | 4,579 | 4,103 | 4,163 |
| Buy hump, began on a trade | 1,197 | 1,211 | 1,152 | 1,156 |
| Sell hump, began on a trade | 1,129 | 1,205 | 1,040 | 1,076 |
| Buy hump, began as old trades left, no trade inside | 695 | 664 | 521 | 558 |
| Sell hump, began as old trades left, no trade inside | 629 | 626 | 627 | 635 |
| Buy hump, began as old trades left, trades came later | 415 | 446 | 384 | 368 |
| Sell hump, began as old trades left, trades came later | 394 | 427 | 379 | 370 |
| Humps holding one trade | 881 | 928 | 827 | 840 |

**What came first after a hump that began ON A TRADE (CL07 and CL08 together: not yet split by the dipole)**

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| buy hump: a step of the best offer (the quote it hits) | 534 | 452 | 509 | 535 |
| buy hump: a trade on its side | 438 | 496 | 403 | 384 |
| buy hump: a step of the best bid (the other quote) | 145 | 154 | 155 | 174 |
| buy hump: a trade on the other side | 80 | 109 | 85 | 63 |
| sell hump: a step of the best bid (the quote it hits) | 521 | 537 | 551 | 578 |
| sell hump: a trade on its side | 442 | 490 | 357 | 367 |
| sell hump: a step of the best offer (the other quote) | 70 | 81 | 81 | 82 |
| sell hump: a trade on the other side | 96 | 97 | 51 | 49 |

**What came first after a hump that began AS OLD TRADES LEFT (rule 6; v1's CL09)**

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| buy hump: a step of the best offer (the quote it hits) | 146 | 110 | 131 | 132 |
| buy hump: a trade on its side | 433 | 424 | 317 | 318 |
| buy hump: a step of the best bid (the other quote) | 127 | 172 | 128 | 147 |
| buy hump: a trade on the other side | 404 | 404 | 328 | 329 |
| sell hump: a step of the best bid (the quote it hits) | 115 | 149 | 150 | 163 |
| sell hump: a trade on its side | 412 | 386 | 367 | 348 |
| sell hump: a step of the best offer (the other quote) | 114 | 108 | 171 | 172 |
| sell hump: a trade on the other side | 382 | 410 | 318 | 322 |

- BEHIND CL07 AND CL08: after a hump that began on a trade, the quote it was hitting stepped, or more trading came
  on its side, far more often than a trade on the other side came, in every cell. The other quote stepping first
  lies in between, and which way it stepped is not in the count.
- BEHIND RULE 6 (v1's CL09): after a hump made by the span, a trade on its side and a trade on the other side came in close
  numbers in every cell: a little more often on its side in five of the eight cells, on the other side in three.
- BUILT IN: a buy that takes out the best offer steps it in the same exchange event. The column that says so is
  stored (`next_..._same_event`) and has not been counted. A hump holding one trade ends when that trade leaves
  the 20 seconds.
- AGAINST CL08: by eye on five pictures (running notes, fifteenth session) the two lines turned after the price,
  never before.
- UNRESOLVED: the split of the first table's trade-begun humps by where the dipole line stood just before the
  trade. It is the whole difference between CL07 and CL08 and it has not been counted.

## CL10 and CL11. The price runs against the dipole (with the price; against the price)

Source: receipts, table "the dipole_60s line at the first step". One case by eye (running notes, fifteenth
session): trade day Oct 18, trade leg 2990, a fall of six steps with the dipole on the buying side throughout.

**Runs of the quote by where the dipole line stood at their FIRST step, and whether they took a second step**

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| Best offer up, line on its side: took a second step | 715 | 651 | 903 | 799 |
| Best offer up, line on its side: one step only | 2,508 | 2,892 | 3,063 | 2,742 |
| Best offer up, line against it: took a second step | 621 | 730 | 584 | 607 |
| Best offer up, line against it: one step only | 2,838 | 2,969 | 2,220 | 2,271 |
| Best offer down, line on its side: took a second step | 722 | 723 | 693 | 736 |
| Best offer down, line on its side: one step only | 2,743 | 3,039 | 2,104 | 2,157 |
| Best offer down, line against it: took a second step | 694 | 617 | 916 | 828 |
| Best offer down, line against it: one step only | 2,487 | 2,862 | 2,995 | 2,694 |
| Best bid up, line on its side: took a second step | 680 | 661 | 975 | 827 |
| Best bid up, line on its side: one step only | 2,569 | 2,832 | 3,250 | 2,728 |
| Best bid up, line against it: took a second step | 639 | 771 | 665 | 732 |
| Best bid up, line against it: one step only | 2,623 | 2,943 | 2,339 | 2,413 |
| Best bid down, line on its side: took a second step | 690 | 738 | 730 | 793 |
| Best bid down, line on its side: one step only | 2,636 | 3,038 | 2,299 | 2,405 |
| Best bid down, line against it: took a second step | 634 | 571 | 911 | 781 |
| Best bid down, line against it: one step only | 2,554 | 2,886 | 3,303 | 2,758 |

- BEHIND CL11 (against the price): in twelve of the sixteen cells runs with the dipole against them at the first
  step took a second step somewhat less often, set against their number, than runs with it behind them. It reads
  the other way in four: best offer up on trade day Oct 3, best offer down on Oct 2, best bid up on Oct 3 and, by
  a hair, best bid up on Oct 18.
- BEHIND CL10 (with the price): the one case seen by eye. No count.
- AGAINST BOTH: the two groups are close in every cell. And the versions read the dipole at the SECOND step,
  which has not been counted at all.
- UNRESOLVED: the same table at the second step (third step or not), which settles one against the other cell by
  cell.

## CL12. The reloaded level

Source: the receipt of `refills`.

**Filled orders with size put back, by what the order's row says happened**

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| Stayed (same place in line) | 1,232 | 1,195 | 976 | 1,079 |
| Lost its place: size raised | 321 | 223 | 270 | 267 |
| Lost its place: price changed | 126 | 116 | 107 | 111 |
| Shrank by fill | 60 | 60 | 47 | 47 |
| Left by fill | 121 | 133 | 122 | 104 |
| Orders with size put back | 383 | 404 | 357 | 379 |
| Most times on one order | 70 | 66 | 99 | 76 |

- BEHIND: nothing counted against the moves. The table says only that the event is there to be read, and that a
  few hundred orders a trade day do it, some of them many times.
- AGAINST: none counted.
- UNRESOLVED: how many of these are at the best price on the side being hit, and whether the level then holds.

## CL13. Paying up through more than one level

Source: the receipt of `sweeps`.

**Trade events**

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| Exchange events holding a trade | 37,238 | 40,517 | 32,728 | 29,797 |
| Most price levels filled in one event | 13 | 7 | 6 | 5 |

- BEHIND: nothing counted. How many events filled more than one level is in the stored table, not in the receipt.
- AGAINST: none counted; the opposite reading (the book fills in behind and the quote comes back) is as likely on
  its face.
- UNRESOLVED: the number of such events, and the next step of the swept quote in a later exchange event.

## CL14. The other side arrives at the top step of a run

Source: the running notes of 2026-11-17, stage (4), and their count file `ATTRIBUTES_BY_PILE.json` (the peak with
no window: a run of trades on one side, read at its last trade, laid against the runs of the quote).

**Runs of trades on one side, by where their last trade sat in a move of the quote**

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| At the END of a move: how many | 1,837 | 1,876 | 1,900 | 1,721 |
| At the END: pushing with the move | 506 | 522 | 556 | 437 |
| At the END: the side pushed into was the thinner at the best price | 1,345 | 1,361 | 1,338 | 1,219 |
| IN BETWEEN: how many | 1,339 | 1,241 | 1,310 | 1,156 |
| IN BETWEEN: pushing with the move | 854 | 825 | 912 | 842 |
| IN BETWEEN: the side pushed into was the thinner | 846 | 782 | 835 | 747 |
| At the BEGINNING: how many | 2,599 | 2,869 | 2,429 | 2,161 |
| At the BEGINNING: pushing with the move | 1,681 | 1,889 | 1,656 | 1,517 |
| At the BEGINNING: the side pushed into was the thinner | 1,707 | 1,829 | 1,543 | 1,368 |
| A ONE-STEP move: how many | 5,792 | 6,698 | 4,762 | 4,508 |
| A ONE-STEP move: pushing with the move | 1,252 | 1,422 | 891 | 852 |
| A ONE-STEP move: the side pushed into was the thinner | 4,614 | 5,340 | 3,755 | 3,521 |

- BEHIND: at the end of a move the run of trades in play pushed WITH the move far less often than at its
  beginning or in between, and most often hit the thinner of the two best levels.
- BUILT IN: selling into the bid is what stops the bid's rise. The one-step rows read the same way as the end
  rows, as they must: a one-step move is its own end.
- AGAINST: the notes call the reading "to test, not shown". These counts are of a run of trades read at its LAST
  trade, which is known only at the first trade on the other side; CL14 acts on a single print, earlier. That
  form is not counted.
- UNRESOLVED: whether the print was the first on the other side since the run's latest step; whether the level
  still stood after it.

## CL15. The step back and the return

Source: receipts, table "what a move gave back".

**Runs of two and of three steps: what the first step back was**

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| Best offer up, 2 steps: gave back one tick | 854 | 946 | 951 | 872 |
| Best offer up, 2 steps in all | 872 | 976 | 964 | 880 |
| Best offer up, 3 steps: gave back one tick | 333 | 294 | 335 | 328 |
| Best offer up, 3 steps in all | 341 | 302 | 337 | 336 |
| Best bid down, 2 steps: gave back one tick | 861 | 882 | 1,074 | 1,014 |
| Best bid down, 2 steps in all | 882 | 902 | 1,104 | 1,050 |
| Best bid down, 3 steps: gave back one tick | 292 | 267 | 372 | 349 |
| Best bid down, 3 steps in all | 297 | 272 | 377 | 361 |

- BEHIND: the first step back is one tick nearly every time. So the step back is small.
- AGAINST: that says nothing about what comes next. The paper: "Do large moves come back" is not answered.
- UNRESOLVED: the whole version. It needs the moves that follow a move, which Greg has saved for later
  (`FURTHER_RESEARCH_LIST.md`, item 4).
