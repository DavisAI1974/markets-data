# Research on the rebuilt data: the research threads read again (Claude, 2026-11-23)

Written on Greg's word so that both strategy sessions have it to look at if needed. It replaces every earlier
research report: THE OLD RESEARCH AND STRATEGY DOCUMENTS OF EARLIER SESSIONS ARE NOT TO BE USED (they stand on data
that was built wrong).

## How to read it

- The questions are the earlier research's (`root-audit-20261116/RESEARCH_INTENTIONS.md`). None of its values is
  carried. Everything here was read from the tape rebuilt since 2026-11-16.
- Every figure is a COUNT of lines, each trade day on its own, in the order Oct 2; Oct 3; Oct 17; Oct 18 (2023).
  Nothing is averaged or pooled. No test of chance has been made: each is a lead, not a result.
- THE COUNTS WERE READ FROM ALL FOUR TRADE DAYS. A strategy version must be formed blind to the trade day it is
  tried on. Say how you use this paper before you form a version, or leave it shut.
- A move is one of three stored things: a trade leg (a move in the trade prints), a run of the best bid, a run of
  the best offer. Its first step is the first tick at which it could be known. A hump is the time the 20-second
  exhaustion line stays on one side of zero.
- Exhaustion and dipole are the crypto formulas made on the natural gas tape: bought minus sold over bought plus
  sold over the trades of the last 20 seconds (exhaustion) and 60 seconds (dipole), read at the tick by place on
  the tape.

## What was found

1. MOST MOVES ARE OVER AT THE MOMENT THEY CAN FIRST BE KNOWN.

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| Runs of the quote that ended | 27,010 | 29,545 | 28,675 | 27,143 |
| ... one step only | 21,420 | 23,943 | 22,099 | 20,824 |
| ... two steps | 3,716 | 3,950 | 4,432 | 4,171 |
| ... three or more | 1,874 | 1,652 | 2,144 | 2,148 |
| Trade legs that ended | 6,118 | 6,906 | 5,659 | 5,119 |
| ... one step only | 3,878 | 4,580 | 3,281 | 2,920 |
| ... two steps | 1,399 | 1,518 | 1,390 | 1,250 |
| ... three or more | 841 | 808 | 988 | 949 |

2. A ONE-STEP TRADE LEG IS MOSTLY THE PRINT BOUNCING BETWEEN BID AND OFFER. Trade legs at whose end the best bid and
   the best offer both stood where they were at the leg's first trade:

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| One-step legs | 2,323 of 3,878 | 2,779 of 4,580 | 1,690 of 3,281 | 1,513 of 2,920 |
| Two-step legs | 114 of 1,399 | 146 of 1,518 | 161 of 1,390 | 109 of 1,250 |
| Three or more | 4 of 841 | 4 of 808 | 1 of 988 | 6 of 949 |

3. WHERE THE EXHAUSTION LINE STANDS AT A MOVE'S FIRST STEP SAYS LITTLE ABOUT WHETHER A RUN OF THE QUOTE GOES ON, AND
   SOMEWHAT MORE FOR A TRADE LEG. Moves that took a second step, the line on the move's side ("with") against the
   line against it:

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| Best offer up, with | 716 of 3,267 | 681 of 3,687 | 893 of 3,782 | 800 of 3,448 |
| Best offer up, against | 598 of 3,329 | 682 of 3,470 | 571 of 2,909 | 580 of 2,836 |
| Best offer down, with | 712 of 3,386 | 687 of 3,571 | 751 of 2,946 | 747 of 2,932 |
| Best offer down, against | 651 of 3,115 | 619 of 3,518 | 814 of 3,597 | 747 of 3,256 |
| Best bid up, with | 657 of 3,171 | 686 of 3,500 | 932 of 3,840 | 808 of 3,343 |
| Best bid up, against | 629 of 3,188 | 709 of 3,574 | 659 of 3,194 | 702 of 3,155 |
| Best bid down, with | 708 of 3,339 | 724 of 3,746 | 794 of 3,304 | 849 of 3,317 |
| Best bid down, against | 595 of 3,080 | 566 of 3,392 | 808 of 3,800 | 689 of 3,258 |
| Trade leg up, with | 546 of 1,422 | 607 of 1,791 | 695 of 1,528 | 569 of 1,239 |
| Trade leg up, against | 507 of 1,536 | 542 of 1,545 | 470 of 1,208 | 470 of 1,208 |
| Trade leg down, with | 598 of 1,497 | 580 of 1,573 | 512 of 1,170 | 530 of 1,209 |
| Trade leg down, against | 508 of 1,451 | 523 of 1,767 | 620 of 1,548 | 516 of 1,217 |

   PARTLY BUILT IN for a trade leg: its first step is a print, and that print is in the line. The same rows for the
   dipole line are in each receipt.

4. A LEVEL THAT WAS EATEN LEADS ON MORE OFTEN THAN A LEVEL THAT WAS ONLY PULLED. Runs of the quote that took a second
   step, by what became of the orders at the first level, and how many then took a third step:

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| Offer up, every order filled | 53 of 123 | 39 of 150 | 91 of 228 | 83 of 162 |
| Offer up, some filled, some pulled | 362 of 959 | 368 of 1,099 | 419 of 1,097 | 438 of 1,035 |
| Offer up, every order pulled | 63 of 212 | 20 of 101 | 24 of 135 | 26 of 177 |
| Bid down, every order filled | 60 of 135 | 51 of 149 | 60 of 173 | 74 of 154 |
| Bid down, some filled, some pulled | 383 of 1,060 | 321 of 947 | 461 of 1,245 | 422 of 1,130 |
| Bid down, every order pulled | 37 of 144 | 26 of 126 | 43 of 196 | 50 of 245 |

5. ABOUT THREE HUMPS IN TEN ARE MADE BY THE 20-SECOND SPAN, NOT BY THE MARKET.

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| Began on a trade | 2,326 | 2,416 | 2,192 | 2,232 |
| Began as old trades left, no trade inside at all | 1,324 | 1,290 | 1,148 | 1,193 |
| Began as old trades left, trades came later | 809 | 873 | 763 | 738 |

6. WHAT COMES FIRST AFTER A HUMP BEGINS.

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| Began on a trade: the quote it was hitting stepped | 1,055 | 989 | 1,060 | 1,113 |
| Began on a trade: another trade on its side | 880 | 986 | 760 | 751 |
| Began on a trade: the other quote stepped | 215 | 235 | 236 | 256 |
| Began on a trade: a trade on the other side | 176 | 206 | 136 | 112 |
| Began as old trades left: a trade on its side | 845 | 810 | 684 | 666 |
| Began as old trades left: a trade on the other side | 786 | 814 | 646 | 651 |

   A hump made by the span carries no direction. PARTLY BUILT IN for a hump that began on a trade: a buy that takes
   out the best offer steps it in the same exchange event (a stored column says so; not counted yet).

7. THE INFORMATION MEASURE (Codex's measure: the crypto information dipole operator on twenty one-second pieces
   counted back from each read of the exhaustion line). Its first figure equals the stored exhaustion line at every
   read. Where all the trading of the 20 seconds is on one side its ratio is made by the division.

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| Reads with figures | 70,393 | 77,645 | 60,608 | 55,168 |
| Nothing traded in the 20 seconds | 827 | 809 | 817 | 853 |
| All trading on one side (ratio made by the division) | 4,594 | 4,869 | 4,360 | 5,268 |
| Reads standing on one piece of twenty | 3,750 | 3,611 | 3,699 | 4,278 |
| Reads standing on two pieces | 5,068 | 4,856 | 4,627 | 5,873 |

   Not for strategy yet: it has not been compared with the original dipole equations.

## What was not found, and what is not answered

- Nothing yet warns BEFORE a move's first step: only the lines AT the first step and at the end were read.
- "Do large moves come back" is not answered: the stored figure is only the first step back, one tick nearly every
  time.
- Set aside by Greg for later: `root-redesign-20261116/FURTHER_RESEARCH_LIST.md` (seventeen items).

## One fault found and corrected

The first run read a stored line by time (the last read at or before a tick's nanosecond). Several trades can share
a nanosecond, so that read took in trades that came after the tick. Every value is now read by the tick's place on
the tape. The tables were made again; only the trade leg rows of finding 3 moved, by 2 to 13 lines each.

## Where it is stored

`DavisAI1974/markets-data`, branches `root-rows-20231002`, `-20231003`, `-20231017`, `-20231018`:
`research-threads/` (one line per move, one line per hump, the receipt with every count by direction),
`info-measure/`, `research-trace/` (the listing that found the fault), and `calc-research_columns-*` (the same
values beside the every-tick rows). Each branch's `FILES.md` explains every file. The decisions, with Greg's words:
`root-redesign-20261116/ROOT_GAMEPLAN_DECISIONS.md`, seventeenth session.
