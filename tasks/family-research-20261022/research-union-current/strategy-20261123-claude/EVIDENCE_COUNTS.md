# Every stored count of the research tables, all four trade days side by side

Copied by script from the receipt `research-threads/RESEARCH-THREADS-<trade day>.json` of each daily
branch (its `the_counts`), unchanged. Each is a count of lines of that trade day alone. Nothing is added
across trade days, nothing is divided, no test of chance was made: each is a lead, not a result.
"none" means that trade day's receipt has no such row (no line was counted there).

| Receipt | SHA256 |
|---|---|
| `root-rows-20231002` `RESEARCH-THREADS-20231002.json` | `8d93a2aa9ec5ff76bf0e10e52fcae5fe6899388d52875fe7ee4e2ce375e31465` |
| `root-rows-20231003` `RESEARCH-THREADS-20231003.json` | `74eff53aab390a82f4df54bc680cf57131bc2bded678086b58b1ca8e08c896bf` |
| `root-rows-20231017` `RESEARCH-THREADS-20231017.json` | `eda66ff9434efe3563b6ecacaf44de748cc2dcfc45f02e452e9413ffbb817a68` |
| `root-rows-20231018` `RESEARCH-THREADS-20231018.json` | `620aadd64aeb689da28cef1293b7ff87715fbfca1a500f1af3906e4f7c83dcb3` |

## how a hump began | buy

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| a trade was received; trades inside: one or more | 1,197 | 1,211 | 1,152 | 1,156 |
| trades left the span at a moment with no tick; trades inside: none | 695 | 664 | 521 | 558 |
| trades left the span at a moment with no tick; trades inside: one or more | 415 | 446 | 384 | 368 |

## how a hump began | sell

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| a trade was received; trades inside: one or more | 1,129 | 1,205 | 1,040 | 1,076 |
| trades left the span at a moment with no tick; trades inside: none | 629 | 626 | 627 | 635 |
| trades left the span at a moment with no tick; trades inside: one or more | 394 | 427 | 379 | 370 |

## how much of a move was left at its first step | run of the best ask down

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| 1 steps in all | 5,361 | 6,013 | 5,258 | 5,017 |
| 2 steps in all | 1,024 | 1,006 | 1,177 | 1,132 |
| 3 steps in all | 312 | 258 | 331 | 323 |
| 4 steps in all | 92 | 78 | 106 | 109 |
| 5 steps in all | 34 | 19 | 38 | 29 |
| 6 steps in all | 9 | 7 | 11 | 16 |
| 7 steps in all | 4 | 1 | 6 | 4 |
| 8 steps in all | 4 | 1 | 4 | none |
| 9 steps in all | none | none | 1 | 3 |
| 10 steps in all | none | none | none | 1 |

## how much of a move was left at its first step | run of the best ask up

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| 1 steps in all | 5,462 | 5,961 | 5,411 | 5,180 |
| 2 steps in all | 872 | 976 | 964 | 880 |
| 3 steps in all | 341 | 302 | 337 | 336 |
| 4 steps in all | 94 | 95 | 116 | 136 |
| 5 steps in all | 42 | 30 | 69 | 57 |
| 6 steps in all | 21 | 11 | 25 | 26 |
| 7 steps in all | 4 | 6 | 5 | 10 |
| 8 steps in all | 2 | 1 | 2 | 6 |
| 9 steps in all | 1 | none | 1 | 2 |
| 12 steps in all | none | none | 1 | none |
| 14 steps in all | none | 1 | none | none |

## how much of a move was left at its first step | run of the best bid down

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| 1 steps in all | 5,298 | 6,054 | 5,717 | 5,321 |
| 2 steps in all | 882 | 902 | 1,104 | 1,050 |
| 3 steps in all | 297 | 272 | 377 | 361 |
| 4 steps in all | 114 | 105 | 123 | 120 |
| 5 steps in all | 47 | 37 | 55 | 46 |
| 6 steps in all | 10 | 14 | 17 | 19 |
| 7 steps in all | 8 | 4 | 7 | 12 |
| 8 steps in all | 8 | 1 | 3 | 5 |
| 9 steps in all | 1 | none | 2 | 4 |
| 10 steps in all | none | none | 1 | none |
| 12 steps in all | 1 | 1 | none | none |

## how much of a move was left at its first step | run of the best bid up

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| 1 steps in all | 5,299 | 5,915 | 5,713 | 5,306 |
| 2 steps in all | 938 | 1,066 | 1,187 | 1,109 |
| 3 steps in all | 305 | 302 | 346 | 359 |
| 4 steps in all | 77 | 79 | 107 | 99 |
| 5 steps in all | 31 | 21 | 34 | 37 |
| 6 steps in all | 9 | 4 | 13 | 24 |
| 7 steps in all | 2 | none | 6 | 4 |
| 8 steps in all | 2 | 1 | none | none |
| 9 steps in all | 1 | none | none | none |
| 11 steps in all | 1 | none | none | none |
| 12 steps in all | none | 1 | none | none |

## how much of a move was left at its first step | trade leg down

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| 1 steps in all | 1,914 | 2,315 | 1,652 | 1,455 |
| 2 steps in all | 706 | 756 | 677 | 627 |
| 3 steps in all | 255 | 229 | 271 | 262 |
| 4 steps in all | 100 | 89 | 116 | 123 |
| 5 steps in all | 43 | 35 | 59 | 43 |
| 6 steps in all | 19 | 21 | 28 | 30 |
| 7 steps in all | 13 | 6 | 16 | 10 |
| 8 steps in all | 4 | 2 | 3 | 6 |
| 9 steps in all | 1 | none | 1 | 2 |
| 10 steps in all | 2 | none | 3 | 1 |
| 11 steps in all | none | none | 1 | 1 |
| 12 steps in all | 1 | none | 1 | none |
| 14 steps in all | none | none | 1 | none |
| 15 steps in all | 1 | none | none | none |
| 19 steps in all | none | none | 1 | none |

## how much of a move was left at its first step | trade leg up

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| 1 steps in all | 1,964 | 2,265 | 1,629 | 1,465 |
| 2 steps in all | 693 | 762 | 713 | 623 |
| 3 steps in all | 248 | 269 | 258 | 230 |
| 4 steps in all | 76 | 92 | 136 | 123 |
| 5 steps in all | 46 | 34 | 55 | 65 |
| 6 steps in all | 19 | 18 | 28 | 33 |
| 7 steps in all | 5 | 7 | 4 | 11 |
| 8 steps in all | 5 | 5 | 5 | 6 |
| 9 steps in all | 2 | 1 | none | 3 |
| 10 steps in all | 1 | none | 1 | none |

## how the first level emptied by the second step | run of the best ask down

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| every order filled: took a third step | 84 | 70 | 82 | 69 |
| every order filled: two steps only | 222 | 193 | 210 | 189 |
| every order pulled: took a third step | 59 | 43 | 74 | 66 |
| every order pulled: two steps only | 146 | 164 | 179 | 169 |
| other (an order still rested or changed price): took a third step | 312 | 251 | 341 | 350 |
| other (an order still rested or changed price): two steps only | 656 | 649 | 788 | 774 |

## how the first level emptied by the second step | run of the best ask up

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| every order filled: took a third step | 53 | 39 | 91 | 83 |
| every order filled: two steps only | 70 | 111 | 137 | 79 |
| every order pulled: took a third step | 63 | 20 | 24 | 26 |
| every order pulled: two steps only | 149 | 81 | 111 | 151 |
| other (an order still rested or changed price): took a third step | 27 | 19 | 22 | 26 |
| other (an order still rested or changed price): two steps only | 56 | 53 | 38 | 53 |
| some filled, some pulled: took a third step | 362 | 368 | 419 | 438 |
| some filled, some pulled: two steps only | 597 | 731 | 678 | 597 |

## how the first level emptied by the second step | run of the best bid down

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| every order filled: took a third step | 60 | 51 | 60 | 74 |
| every order filled: two steps only | 75 | 98 | 113 | 80 |
| every order pulled: took a third step | 37 | 26 | 43 | 50 |
| every order pulled: two steps only | 107 | 100 | 153 | 195 |
| other (an order still rested or changed price): took a third step | 6 | 36 | 21 | 21 |
| other (an order still rested or changed price): two steps only | 23 | 78 | 54 | 67 |
| some filled, some pulled: took a third step | 383 | 321 | 461 | 422 |
| some filled, some pulled: two steps only | 677 | 626 | 784 | 708 |

## how the first level emptied by the second step | run of the best bid up

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| every order filled: took a third step | 76 | 89 | 84 | 60 |
| every order filled: two steps only | 187 | 229 | 177 | 141 |
| every order pulled: took a third step | 65 | 53 | 73 | 63 |
| every order pulled: two steps only | 139 | 136 | 161 | 157 |
| other (an order still rested or changed price): took a third step | 287 | 266 | 349 | 400 |
| other (an order still rested or changed price): two steps only | 612 | 701 | 849 | 811 |

## the dipole_60s line at the first step | run of the best ask down

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| the line stood at zero: one step only | 107 | 83 | 105 | 92 |
| the line stood at zero: took a second step | 35 | 23 | 45 | 35 |
| the line was against the move: one step only | 2,487 | 2,862 | 2,995 | 2,694 |
| the line was against the move: took a second step | 694 | 617 | 916 | 828 |
| the line was empty: one step only | 24 | 29 | 54 | 74 |
| the line was empty: took a second step | 28 | 7 | 20 | 18 |
| the line was on the move's side: one step only | 2,743 | 3,039 | 2,104 | 2,157 |
| the line was on the move's side: took a second step | 722 | 723 | 693 | 736 |

## the dipole_60s line at the first step | run of the best ask up

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| the line stood at zero: one step only | 110 | 97 | 110 | 112 |
| the line stood at zero: took a second step | 39 | 39 | 30 | 38 |
| the line was against the move: one step only | 2,838 | 2,969 | 2,220 | 2,271 |
| the line was against the move: took a second step | 621 | 730 | 584 | 607 |
| the line was empty: one step only | 6 | 3 | 18 | 55 |
| the line was empty: took a second step | 2 | 2 | 3 | 9 |
| the line was on the move's side: one step only | 2,508 | 2,892 | 3,063 | 2,742 |
| the line was on the move's side: took a second step | 715 | 651 | 903 | 799 |

## the dipole_60s line at the first step | run of the best bid down

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| the line stood at zero: one step only | 99 | 121 | 85 | 130 |
| the line stood at zero: took a second step | 39 | 24 | 44 | 38 |
| the line was against the move: one step only | 2,554 | 2,886 | 3,303 | 2,758 |
| the line was against the move: took a second step | 634 | 571 | 911 | 781 |
| the line was empty: one step only | 9 | 9 | 30 | 28 |
| the line was empty: took a second step | 5 | 3 | 4 | 5 |
| the line was on the move's side: one step only | 2,636 | 3,038 | 2,299 | 2,405 |
| the line was on the move's side: took a second step | 690 | 738 | 730 | 793 |

## the dipole_60s line at the first step | run of the best bid up

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| the line stood at zero: one step only | 94 | 121 | 84 | 121 |
| the line stood at zero: took a second step | 36 | 33 | 38 | 46 |
| the line was against the move: one step only | 2,623 | 2,943 | 2,339 | 2,413 |
| the line was against the move: took a second step | 639 | 771 | 665 | 732 |
| the line was empty: one step only | 13 | 19 | 40 | 44 |
| the line was empty: took a second step | 11 | 9 | 15 | 27 |
| the line was on the move's side: one step only | 2,569 | 2,832 | 3,250 | 2,728 |
| the line was on the move's side: took a second step | 680 | 661 | 975 | 827 |

## the dipole_60s line at the first step | trade leg down

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| the line stood at zero: one step only | 45 | 56 | 38 | 33 |
| the line stood at zero: took a second step | 31 | 21 | 33 | 34 |
| the line was against the move: one step only | 937 | 1,214 | 975 | 742 |
| the line was against the move: took a second step | 547 | 519 | 665 | 558 |
| the line was empty: one step only | none | 1 | 1 | 1 |
| the line was empty: took a second step | 3 | none | none | 3 |
| the line was on the move's side: one step only | 932 | 1,044 | 638 | 679 |
| the line was on the move's side: took a second step | 564 | 598 | 480 | 510 |

## the dipole_60s line at the first step | trade leg up

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| the line stood at zero: one step only | 33 | 62 | 26 | 37 |
| the line stood at zero: took a second step | 25 | 29 | 24 | 34 |
| the line was against the move: one step only | 1,041 | 1,089 | 713 | 708 |
| the line was against the move: took a second step | 520 | 573 | 473 | 493 |
| the line was empty: one step only | none | 1 | 1 | 1 |
| the line was empty: took a second step | 1 | none | 1 | 4 |
| the line was on the move's side: one step only | 890 | 1,113 | 889 | 719 |
| the line was on the move's side: took a second step | 549 | 586 | 702 | 563 |

## the exhaustion_20s line at the first step | run of the best ask down

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| the line stood at zero: one step only | 131 | 138 | 147 | 157 |
| the line stood at zero: took a second step | 44 | 42 | 50 | 60 |
| the line was against the move: one step only | 2,464 | 2,899 | 2,783 | 2,509 |
| the line was against the move: took a second step | 651 | 619 | 814 | 747 |
| the line was empty: one step only | 92 | 92 | 133 | 166 |
| the line was empty: took a second step | 72 | 22 | 59 | 63 |
| the line was on the move's side: one step only | 2,674 | 2,884 | 2,195 | 2,185 |
| the line was on the move's side: took a second step | 712 | 687 | 751 | 747 |

## the exhaustion_20s line at the first step | run of the best ask up

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| the line stood at zero: one step only | 145 | 140 | 131 | 172 |
| the line stood at zero: took a second step | 54 | 56 | 46 | 44 |
| the line was against the move: one step only | 2,731 | 2,788 | 2,338 | 2,256 |
| the line was against the move: took a second step | 598 | 682 | 571 | 580 |
| the line was empty: one step only | 35 | 27 | 53 | 104 |
| the line was empty: took a second step | 9 | 3 | 10 | 29 |
| the line was on the move's side: one step only | 2,551 | 3,006 | 2,889 | 2,648 |
| the line was on the move's side: took a second step | 716 | 681 | 893 | 800 |

## the exhaustion_20s line at the first step | run of the best bid down

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| the line stood at zero: one step only | 152 | 178 | 144 | 185 |
| the line stood at zero: took a second step | 49 | 37 | 71 | 64 |
| the line was against the move: one step only | 2,485 | 2,826 | 2,992 | 2,569 |
| the line was against the move: took a second step | 595 | 566 | 808 | 689 |
| the line was empty: one step only | 30 | 28 | 71 | 99 |
| the line was empty: took a second step | 16 | 9 | 16 | 15 |
| the line was on the move's side: one step only | 2,631 | 3,022 | 2,510 | 2,468 |
| the line was on the move's side: took a second step | 708 | 724 | 794 | 849 |

## the exhaustion_20s line at the first step | run of the best bid up

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| the line stood at zero: one step only | 158 | 149 | 158 | 174 |
| the line stood at zero: took a second step | 39 | 45 | 48 | 46 |
| the line was against the move: one step only | 2,559 | 2,865 | 2,535 | 2,453 |
| the line was against the move: took a second step | 629 | 709 | 659 | 702 |
| the line was empty: one step only | 68 | 87 | 112 | 144 |
| the line was empty: took a second step | 41 | 34 | 54 | 76 |
| the line was on the move's side: one step only | 2,514 | 2,814 | 2,908 | 2,535 |
| the line was on the move's side: took a second step | 657 | 686 | 932 | 808 |

## the exhaustion_20s line at the first step | trade leg down

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| the line stood at zero: one step only | 69 | 77 | 63 | 69 |
| the line stood at zero: took a second step | 36 | 33 | 44 | 49 |
| the line was against the move: one step only | 943 | 1,244 | 928 | 701 |
| the line was against the move: took a second step | 508 | 523 | 620 | 516 |
| the line was empty: one step only | 3 | 1 | 3 | 6 |
| the line was empty: took a second step | 3 | 2 | 2 | 10 |
| the line was on the move's side: one step only | 899 | 993 | 658 | 679 |
| the line was on the move's side: took a second step | 598 | 580 | 512 | 530 |

## the exhaustion_20s line at the first step | trade leg up

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| the line stood at zero: one step only | 58 | 75 | 54 | 50 |
| the line stood at zero: took a second step | 41 | 36 | 29 | 48 |
| the line was against the move: one step only | 1,029 | 1,003 | 738 | 738 |
| the line was against the move: took a second step | 507 | 542 | 470 | 470 |
| the line was empty: one step only | 1 | 3 | 4 | 7 |
| the line was empty: took a second step | 1 | 3 | 6 | 7 |
| the line was on the move's side: one step only | 876 | 1,184 | 833 | 670 |
| the line was on the move's side: took a second step | 546 | 607 | 695 | 569 |

## the print against the quote | trade leg down

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| 1 steps in all: the best bid and the best offer both stood where they were | 1,121 | 1,466 | 834 | 769 |
| 1 steps in all: the best bid and the best offer were not both where they were | 793 | 849 | 818 | 686 |
| 2 steps in all: the best bid and the best offer both stood where they were | 60 | 79 | 78 | 55 |
| 2 steps in all: the best bid and the best offer were not both where they were | 646 | 677 | 599 | 572 |
| 3 steps in all: the best bid and the best offer both stood where they were | 2 | 2 | 1 | 3 |
| 3 steps in all: the best bid and the best offer were not both where they were | 253 | 227 | 270 | 259 |
| 4 steps in all: the best bid and the best offer were not both where they were | 100 | 89 | 116 | 123 |
| 5 steps in all: the best bid and the best offer were not both where they were | 43 | 35 | 59 | 43 |
| 6 steps in all: the best bid and the best offer were not both where they were | 19 | 21 | 28 | 30 |
| 7 steps in all: the best bid and the best offer were not both where they were | 13 | 6 | 16 | 10 |
| 8 steps in all: the best bid and the best offer were not both where they were | 4 | 2 | 3 | 6 |
| 9 steps in all: the best bid and the best offer were not both where they were | 1 | none | 1 | 2 |
| 10 steps in all: the best bid and the best offer were not both where they were | 2 | none | 3 | 1 |
| 11 steps in all: the best bid and the best offer were not both where they were | none | none | 1 | 1 |
| 12 steps in all: the best bid and the best offer were not both where they were | 1 | none | 1 | none |
| 14 steps in all: the best bid and the best offer were not both where they were | none | none | 1 | none |
| 15 steps in all: the best bid and the best offer were not both where they were | 1 | none | none | none |
| 19 steps in all: the best bid and the best offer were not both where they were | none | none | 1 | none |

## the print against the quote | trade leg up

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| 1 steps in all: the best bid and the best offer both stood where they were | 1,202 | 1,313 | 856 | 744 |
| 1 steps in all: the best bid and the best offer were not both where they were | 762 | 952 | 773 | 721 |
| 2 steps in all: the best bid and the best offer both stood where they were | 54 | 67 | 83 | 54 |
| 2 steps in all: the best bid and the best offer were not both where they were | 639 | 695 | 630 | 569 |
| 3 steps in all: the best bid and the best offer both stood where they were | 2 | 2 | none | 3 |
| 3 steps in all: the best bid and the best offer were not both where they were | 246 | 267 | 258 | 227 |
| 4 steps in all: the best bid and the best offer were not both where they were | 76 | 92 | 136 | 123 |
| 5 steps in all: the best bid and the best offer were not both where they were | 46 | 34 | 55 | 65 |
| 6 steps in all: the best bid and the best offer were not both where they were | 19 | 18 | 28 | 33 |
| 7 steps in all: the best bid and the best offer were not both where they were | 5 | 7 | 4 | 11 |
| 8 steps in all: the best bid and the best offer were not both where they were | 5 | 5 | 5 | 6 |
| 9 steps in all: the best bid and the best offer were not both where they were | 2 | 1 | none | 3 |
| 10 steps in all: the best bid and the best offer were not both where they were | 1 | none | 1 | none |

## what a move gave back | run of the best ask down

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| 1 steps in all, gave back +0.001 | 5,317 | 5,966 | 5,224 | 4,990 |
| 1 steps in all, gave back +0.002 | 38 | 43 | 32 | 25 |
| 1 steps in all, gave back +0.003 | 4 | 4 | 2 | 2 |
| 1 steps in all, gave back +0.004 | 2 | none | none | none |
| 2 steps in all, gave back +0.001 | 1,007 | 996 | 1,168 | 1,120 |
| 2 steps in all, gave back +0.002 | 14 | 10 | 9 | 12 |
| 2 steps in all, gave back +0.003 | 1 | none | none | none |
| 2 steps in all, gave back +0.005 | 1 | none | none | none |
| 2 steps in all, gave back +0.008 | 1 | none | none | none |
| 3 steps in all, gave back +0.001 | 310 | 257 | 327 | 319 |
| 3 steps in all, gave back +0.002 | 2 | 1 | 3 | 4 |
| 3 steps in all, gave back +0.004 | none | none | 1 | none |
| 4 steps in all, gave back +0.001 | 88 | 77 | 106 | 107 |
| 4 steps in all, gave back +0.002 | 4 | 1 | none | 2 |
| 5 steps in all, gave back +0.001 | 34 | 19 | 36 | 27 |
| 5 steps in all, gave back +0.002 | none | none | 2 | 2 |
| 6 steps in all, gave back +0.001 | 8 | 7 | 11 | 16 |
| 6 steps in all, gave back +0.002 | 1 | none | none | none |
| 7 steps in all, gave back +0.001 | 3 | 1 | 6 | 4 |
| 7 steps in all, gave back +0.003 | 1 | none | none | none |
| 8 steps in all, gave back +0.001 | 4 | 1 | 4 | none |
| 9 steps in all, gave back +0.001 | none | none | 1 | 3 |
| 10 steps in all, gave back +0.001 | none | none | none | 1 |

## what a move gave back | run of the best ask up

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| 1 steps in all, gave back -0.001 | 5,388 | 5,877 | 5,351 | 5,121 |
| 1 steps in all, gave back -0.002 | 61 | 75 | 58 | 52 |
| 1 steps in all, gave back -0.003 | 6 | 7 | 2 | 5 |
| 1 steps in all, gave back -0.004 | 6 | 1 | none | 2 |
| 1 steps in all, gave back -0.005 | 1 | none | none | none |
| 1 steps in all, gave back -0.007 | none | 1 | none | none |
| 2 steps in all, gave back -0.001 | 854 | 946 | 951 | 872 |
| 2 steps in all, gave back -0.002 | 15 | 29 | 13 | 8 |
| 2 steps in all, gave back -0.003 | 1 | 1 | none | none |
| 2 steps in all, gave back -0.004 | 1 | none | none | none |
| 2 steps in all, gave back -0.009 | 1 | none | none | none |
| 3 steps in all, gave back -0.001 | 333 | 294 | 335 | 328 |
| 3 steps in all, gave back -0.002 | 7 | 3 | none | 8 |
| 3 steps in all, gave back -0.003 | none | 5 | 2 | none |
| 3 steps in all, gave back -0.007 | 1 | none | none | none |
| 4 steps in all, gave back -0.001 | 89 | 90 | 113 | 134 |
| 4 steps in all, gave back -0.002 | 5 | 5 | 2 | 2 |
| 4 steps in all, gave back -0.004 | none | none | 1 | none |
| 5 steps in all, gave back -0.001 | 41 | 27 | 67 | 54 |
| 5 steps in all, gave back -0.002 | 1 | 3 | 2 | 3 |
| 6 steps in all, gave back -0.001 | 21 | 11 | 23 | 23 |
| 6 steps in all, gave back -0.002 | none | none | 2 | 1 |
| 6 steps in all, gave back -0.003 | none | none | none | 2 |
| 7 steps in all, gave back -0.001 | 4 | 4 | 5 | 10 |
| 7 steps in all, gave back -0.002 | none | 1 | none | none |
| 7 steps in all, gave back -0.003 | none | 1 | none | none |
| 8 steps in all, gave back -0.001 | 1 | none | 2 | 6 |
| 8 steps in all, gave back -0.002 | 1 | 1 | none | none |
| 9 steps in all, gave back -0.001 | 1 | none | 1 | 2 |
| 12 steps in all, gave back -0.001 | none | none | 1 | none |
| 14 steps in all, gave back -0.001 | none | 1 | none | none |

## what a move gave back | run of the best bid down

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| 1 steps in all, gave back +0.001 | 5,242 | 5,996 | 5,641 | 5,244 |
| 1 steps in all, gave back +0.002 | 51 | 55 | 69 | 69 |
| 1 steps in all, gave back +0.003 | 4 | 3 | 6 | 7 |
| 1 steps in all, gave back +0.004 | none | none | none | 1 |
| 1 steps in all, gave back +0.005 | none | none | 1 | none |
| 1 steps in all, gave back +0.006 | 1 | none | none | none |
| 2 steps in all, gave back +0.001 | 861 | 882 | 1,074 | 1,014 |
| 2 steps in all, gave back +0.002 | 17 | 17 | 29 | 29 |
| 2 steps in all, gave back +0.003 | 3 | 3 | 1 | 5 |
| 2 steps in all, gave back +0.005 | 1 | none | none | 2 |
| 3 steps in all, gave back +0.001 | 292 | 267 | 372 | 349 |
| 3 steps in all, gave back +0.002 | 3 | 4 | 5 | 8 |
| 3 steps in all, gave back +0.003 | 1 | 1 | none | 3 |
| 3 steps in all, gave back +0.004 | 1 | none | none | 1 |
| 4 steps in all, gave back +0.001 | 108 | 99 | 117 | 117 |
| 4 steps in all, gave back +0.002 | 5 | 5 | 6 | 2 |
| 4 steps in all, gave back +0.003 | 1 | none | none | 1 |
| 4 steps in all, gave back +0.004 | none | 1 | none | none |
| 5 steps in all, gave back +0.001 | 42 | 35 | 53 | 45 |
| 5 steps in all, gave back +0.002 | 3 | 2 | 2 | 1 |
| 5 steps in all, gave back +0.003 | 1 | none | none | none |
| 5 steps in all, gave back +0.004 | 1 | none | none | none |
| 6 steps in all, gave back +0.001 | 10 | 14 | 17 | 18 |
| 6 steps in all, gave back +0.002 | none | none | none | 1 |
| 7 steps in all, gave back +0.001 | 5 | 2 | 7 | 10 |
| 7 steps in all, gave back +0.002 | 3 | 2 | none | 2 |
| 8 steps in all, gave back +0.001 | 7 | none | 3 | 5 |
| 8 steps in all, gave back +0.002 | none | 1 | none | none |
| 8 steps in all, gave back +0.003 | 1 | none | none | none |
| 9 steps in all, gave back +0.001 | 1 | none | 2 | 3 |
| 9 steps in all, gave back +0.002 | none | none | none | 1 |
| 10 steps in all, gave back +0.001 | none | none | 1 | none |
| 12 steps in all, gave back +0.001 | 1 | 1 | none | none |

## what a move gave back | run of the best bid up

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| 1 steps in all, gave back -0.001 | 5,267 | 5,882 | 5,682 | 5,270 |
| 1 steps in all, gave back -0.002 | 28 | 33 | 31 | 33 |
| 1 steps in all, gave back -0.003 | 2 | none | none | 3 |
| 1 steps in all, gave back -0.004 | 1 | none | none | none |
| 1 steps in all, gave back -0.005 | 1 | none | none | none |
| 2 steps in all, gave back -0.001 | 930 | 1,058 | 1,172 | 1,104 |
| 2 steps in all, gave back -0.002 | 7 | 7 | 15 | 4 |
| 2 steps in all, gave back -0.003 | 1 | none | none | 1 |
| 2 steps in all, gave back -0.005 | none | 1 | none | none |
| 3 steps in all, gave back -0.001 | 301 | 300 | 344 | 355 |
| 3 steps in all, gave back -0.002 | 2 | 2 | 2 | 3 |
| 3 steps in all, gave back -0.003 | 1 | none | none | 1 |
| 3 steps in all, gave back -0.004 | 1 | none | none | none |
| 4 steps in all, gave back -0.001 | 76 | 79 | 107 | 98 |
| 4 steps in all, gave back -0.002 | 1 | none | none | 1 |
| 5 steps in all, gave back -0.001 | 31 | 21 | 34 | 37 |
| 6 steps in all, gave back -0.001 | 7 | 4 | 13 | 24 |
| 6 steps in all, gave back -0.002 | 1 | none | none | none |
| 6 steps in all, gave back -0.003 | 1 | none | none | none |
| 7 steps in all, gave back -0.001 | 2 | none | 6 | 4 |
| 8 steps in all, gave back -0.001 | 2 | 1 | none | none |
| 9 steps in all, gave back -0.001 | 1 | none | none | none |
| 11 steps in all, gave back -0.001 | 1 | none | none | none |
| 12 steps in all, gave back -0.001 | none | 1 | none | none |

## what a move gave back | trade leg down

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| 1 steps in all, gave back +0.001 | 1,816 | 2,207 | 1,540 | 1,384 |
| 1 steps in all, gave back +0.002 | 95 | 106 | 109 | 66 |
| 1 steps in all, gave back +0.003 | 2 | 2 | 2 | 5 |
| 1 steps in all, gave back +0.005 | none | none | 1 | none |
| 1 steps in all, gave back +0.024 | 1 | none | none | none |
| 2 steps in all, gave back +0.001 | 645 | 712 | 628 | 593 |
| 2 steps in all, gave back +0.002 | 56 | 44 | 48 | 34 |
| 2 steps in all, gave back +0.003 | 4 | none | 1 | none |
| 2 steps in all, gave back +0.005 | 1 | none | none | none |
| 3 steps in all, gave back +0.001 | 231 | 213 | 251 | 245 |
| 3 steps in all, gave back +0.002 | 23 | 15 | 19 | 11 |
| 3 steps in all, gave back +0.003 | 1 | 1 | 1 | 6 |
| 4 steps in all, gave back +0.001 | 86 | 83 | 103 | 115 |
| 4 steps in all, gave back +0.002 | 7 | 5 | 12 | 7 |
| 4 steps in all, gave back +0.003 | 6 | 1 | 1 | none |
| 4 steps in all, gave back +0.004 | 1 | none | none | 1 |
| 5 steps in all, gave back +0.001 | 40 | 30 | 53 | 41 |
| 5 steps in all, gave back +0.002 | 2 | 4 | 5 | 2 |
| 5 steps in all, gave back +0.003 | 1 | 1 | 1 | none |
| 6 steps in all, gave back +0.001 | 16 | 20 | 27 | 30 |
| 6 steps in all, gave back +0.002 | 3 | 1 | none | none |
| 6 steps in all, gave back +0.004 | none | none | 1 | none |
| 7 steps in all, gave back +0.001 | 11 | 5 | 15 | 8 |
| 7 steps in all, gave back +0.002 | 1 | 1 | none | 2 |
| 7 steps in all, gave back +0.003 | 1 | none | 1 | none |
| 8 steps in all, gave back +0.001 | 4 | 2 | 2 | 6 |
| 8 steps in all, gave back +0.002 | none | none | 1 | none |
| 9 steps in all, gave back +0.001 | 1 | none | 1 | 1 |
| 9 steps in all, gave back +0.002 | none | none | none | 1 |
| 10 steps in all, gave back +0.001 | 2 | none | 1 | 1 |
| 10 steps in all, gave back +0.002 | none | none | 1 | none |
| 10 steps in all, gave back +0.003 | none | none | 1 | none |
| 11 steps in all, gave back +0.001 | none | none | 1 | 1 |
| 12 steps in all, gave back +0.001 | 1 | none | 1 | none |
| 14 steps in all, gave back +0.001 | none | none | 1 | none |
| 15 steps in all, gave back +0.001 | 1 | none | none | none |
| 19 steps in all, gave back +0.001 | none | none | 1 | none |

## what a move gave back | trade leg up

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| 1 steps in all, gave back -0.001 | 1,851 | 2,172 | 1,539 | 1,388 |
| 1 steps in all, gave back -0.002 | 105 | 90 | 84 | 72 |
| 1 steps in all, gave back -0.003 | 5 | 3 | 5 | 4 |
| 1 steps in all, gave back -0.004 | 2 | none | 1 | 1 |
| 1 steps in all, gave back -0.006 | 1 | none | none | none |
| 2 steps in all, gave back -0.001 | 642 | 713 | 663 | 594 |
| 2 steps in all, gave back -0.002 | 45 | 47 | 50 | 28 |
| 2 steps in all, gave back -0.003 | 4 | 1 | none | 1 |
| 2 steps in all, gave back -0.004 | 2 | 1 | none | none |
| 3 steps in all, gave back -0.001 | 235 | 251 | 236 | 216 |
| 3 steps in all, gave back -0.002 | 10 | 17 | 21 | 12 |
| 3 steps in all, gave back -0.003 | 2 | 1 | 1 | 2 |
| 3 steps in all, gave back -0.005 | 1 | none | none | none |
| 4 steps in all, gave back -0.001 | 73 | 82 | 124 | 109 |
| 4 steps in all, gave back -0.002 | 3 | 9 | 11 | 13 |
| 4 steps in all, gave back -0.003 | none | 1 | 1 | 1 |
| 5 steps in all, gave back -0.001 | 41 | 31 | 54 | 56 |
| 5 steps in all, gave back -0.002 | 5 | 3 | 1 | 7 |
| 5 steps in all, gave back -0.003 | none | none | none | 2 |
| 6 steps in all, gave back -0.001 | 17 | 15 | 27 | 29 |
| 6 steps in all, gave back -0.002 | 1 | 1 | none | 4 |
| 6 steps in all, gave back -0.003 | 1 | 1 | none | none |
| 6 steps in all, gave back -0.004 | none | 1 | none | none |
| 6 steps in all, gave back -0.005 | none | none | 1 | none |
| 7 steps in all, gave back -0.001 | 5 | 4 | 4 | 9 |
| 7 steps in all, gave back -0.002 | none | 3 | none | 2 |
| 8 steps in all, gave back -0.001 | 4 | 5 | 5 | 6 |
| 8 steps in all, gave back -0.002 | 1 | none | none | none |
| 9 steps in all, gave back -0.001 | 2 | 1 | none | 2 |
| 9 steps in all, gave back -0.003 | none | none | none | 1 |
| 10 steps in all, gave back -0.001 | 1 | none | 1 | none |

## what came first after a hump began | buy, began on: a trade was received

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| a step of the best bid | 145 | 154 | 155 | 174 |
| a step of the best offer | 534 | 452 | 509 | 535 |
| a trade on the hump's side | 438 | 496 | 403 | 384 |
| a trade on the other side | 80 | 109 | 85 | 63 |

## what came first after a hump began | buy, began on: trades left the span at a moment with no tick

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| a step of the best bid | 127 | 172 | 128 | 147 |
| a step of the best offer | 146 | 110 | 131 | 132 |
| a trade on the hump's side | 433 | 424 | 317 | 318 |
| a trade on the other side | 404 | 404 | 328 | 329 |

## what came first after a hump began | sell, began on: a trade was received

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| a step of the best bid | 521 | 537 | 551 | 578 |
| a step of the best offer | 70 | 81 | 81 | 82 |
| a trade on the hump's side | 442 | 490 | 357 | 367 |
| a trade on the other side | 96 | 97 | 51 | 49 |

## what came first after a hump began | sell, began on: trades left the span at a moment with no tick

| | Oct 2 | Oct 3 | Oct 17 | Oct 18 |
|---|---:|---:|---:|---:|
| a step of the best bid | 115 | 149 | 150 | 163 |
| a step of the best offer | 114 | 108 | 171 | 172 |
| a trade on the hump's side | 412 | 386 | 367 | 348 |
| a trade on the other side | 382 | 410 | 318 | 322 |
