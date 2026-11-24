# decider_v1: the nine claim files (ticket 01), PROPOSED, NOT YET REGISTERED

Written by builder run 119 (proposer). Page: `tools/decider/programs/decider_v1.md` (Markets); program `tools/decider/programs/decider_v1.py`.
Each file is a claim file for `python3 -m tools.kgraph.defend register`. Every quote in `rests_on` was cut by script from the file itself
(rule files at platform commit 28d4dbb080ff462e1318bd825f0fd858838b91ef, CLAUDE.md and packet.py in Markets) and checked with the tool's own
quote check before the file was written. Each file was tried on a scratch copy of the graph with run:0002 and registered without a refusal.

| file | page lines | what it is |
| --- | --- | --- |
| condition-1.json | 11-14 | suspended additions (CX13, CX14) |
| condition-2.json | 15-17 | same run again (CL16, CL03, CL09) |
| condition-3.json | 18-19 | crossed quote (CL06) |
| condition-4.json | 20-24 | strong divergence on an entry with the move (CLAUDE.md lines 381-382; SIDE lines of CL01, CL03, CL06, CL10, CL13, CL15, CL16) |
| inference-1.json | 29-30 | a CX13/CX14 warning applied to any rule's signal on that side |
| inference-2.json | (none: the page lists no inference for condition 2) | the inference the program makes: the same-run skip applied to any rule; written as a tenth file by the coordinator's word |
| inference-3.json | 31 | CL06's sentence applied to every rule |
| inference-4a.json | 32-36 (item 4) | the flow on the newest known dipole event stands for the line now |
| inference-4b.json | 32-36 (item 4) | -0.20 is on the scale of ours |
| inference-4c.json | 32-36 (item 4) | the rule list is the "with the move" rules (with the CL10 sentence) |

(The page line numbers are for the page as read; the page's inference list starts at the line after "Inferences (for Greg)".)

## Where the page holds something other than the main session's count
The page numbers its inferences 1, 3 and 4 only (there is no 2 and no 5). Item 4 holds three statements separated by semicolons, so it is split
into 4a, 4b and 4c as the ticket counts them: five inference files. That is a reading of the page, not something it says.

## Where the page and the files differ (the files were followed)
- CX13/CX14: the page writes q's with a straight apostrophe; the files have q’ (U+2019). Page: "an exit"; file: "issue an exit".
- The page's "unresolved" end of a warning is in no rule file. It stays in the claim's exact_claim (as the page's words) and is named in boundaries as ungrounded.
- CL06: the file holds "Not while the best offer\n  is at or below the best bid." (JSON escape and two spaces inside one raw line); the quote is the file's raw text.
- CL10: the page drops the word "line" ("the dipole stands on the OTHER side"); the file reads "while the dipole line stands on the\n  OTHER side."
- CLAUDE.md lines 381-382: the page uses plain characters; the file has an em dash, a multiplication sign, a less-than-or-equal sign, a minus sign and an arrow, and "~65% reversal" begins line 382. The quote is the file's, joined across the two lines with a space.
- The page places the trade days only as "these trade days"; no dates are in the page or in these files.

## Grounds added that the page does not name
- condition-4 also rests on CLAUDE.md line 386 (the "Discipline" bullet: the signed flow is NOT a direct direction predictor), because the page says "not the flow as a direction call".
- inference-4a and 4b rest on CLAUDE.md lines 187-191 (the bought-minus-sold formula; EXHAUSTION line 20 seconds, DIPOLE line 60 seconds) and line 383 ("toward 0.5"), and 4a on packet.py line 81 (the 20-second fields are read at the end of the birth second). These bear on the claims in ways the page itself points at; the reviewer is given them as grounds, not as the proposer's reading.
- Condition 2: the page names no inference for the program's use of the same-run skip on every rule; it is written into the boundaries.

## Not in a file
Nothing in the claims was left without a file ground, with these exceptions: the page's "unresolved" end (above); how the decider reads "newest row of that trade"
(a program matter, not a rule text); the origin of the choice of 20 seconds for the divergence field (CLAUDE.md gives 20 seconds for the EXHAUSTION line only).
No MANIFEST.json entry was written: the writes were confined to this folder.

reasoning_files listed in each claim: the page, this README, and ticket 01 (the program is the artifact and is printed in the brief).
