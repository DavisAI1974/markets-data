# The reviewer's reads of 2026-11-24, runs 103 and 105 (findings as returned, shortened; status beside each)

## Run 103 (Opus, 128,459 tokens): the platform change `47fa1c5..27f7261`, third read

What it read and found nothing in: with nothing plugged in, no line changes a journal row, an order, a fill, a
timer, a budget count, the stop point or the receipt beyond the `answers` key (`_late`, the `needed` count, the
branches of `record`, the lines of `step`, the class attributes, `start.json`, the receipt, `feed.py:146`,
`trial.py`, `run.py` each walked); no trade can open without a valid `take`; building the question is wrapped
and reads only; the MBO window's last message is the signal's own; no mid price in the changed code. None of
the new `Session` lines has run on tape.

Findings, each being closed by agent run 106 unless said:
1. State left out without being named: `engine.rules` and `engine.cx` beyond their ids; each venue's closed
   orders, `book_quote`, `reference`, `received`, `known_received_ns`; `execution.policies`, `followers`; each
   active order's type, filled quantity and timestamps. OPEN, run 106 fix 1.
2. Outside the diff, Codex's code: `paper_execution.py:53` builds a fill model and a maker-taker fee model.
   OPEN: run 106 reports what they are set to; whether a fee can be non-zero goes to Greg.
3. `conditions.instrument` passes the plan's definition time through unchecked. OPEN, fix 3.
4. `received_by_replay_ns` (wall time) inside the MBO window makes `state_sha256` differ between runs. OPEN, fix 4.
5. For a trade print the book's guard reduces to best prices plus a sequence number that repeats within an
   exchange event. OPEN, fix 5.
6. `CLOSE_NOT_BUILT` says the give-back exit is in force; untrue for a plan with no exit. OPEN, fix 6.
7. The README says the decider's wait is out of the clock; building the question is not. OPEN, fix 7.
8. A `BaseException` from a decider escapes `step`. OPEN, fix 8 (left so on purpose; said in the README).
9. The market series starts on a different clock than deciding; no count or hash of its files in any record; a
   failure writing it ends the trial without a journal. OPEN, fix 9.
10. An `answer` row count can exceed taken plus asked. OPEN, fix 10.
11. The first causal trace's book now stays in memory until the session's first step. NOTED: memory, not a row.
12. `question["journal"]` points into the scratch checkout that also holds the stored week of tape: keeping the
    future from a decider rests on the decider's side. NOTED: the packet's own leak check is that side.

What a first pass on tape must show, in its order: (1) nothing plugged in, row for row against `47fa1c5` on the
same stretch, after setting aside the run id, trade ids, order ids and the wall-clock fields; (2) an
always-take decider: the same signals, orders and fills, plus one question and one answer row for each gated
open; (3) an always-skip decider: the same signal rows, no opening orders, closes that send nothing; (4) for
each question: the window's last message is the signal's own, the book is there or its reason, the book's last
sequence is the signal's; (5) the size of each question, the seconds to build it, the time waited; (6) the
market series' print count against the tape's prints in the stretch and its first and last times against the
stretch.

## Run 105 (Opus, 104,454 tokens): Markets `071777f`, tickets 02 and 03 (`tools/kgraph/defend.py`)

Its one run of the tests gave 24 errors before any test body ran (the scratch folder's parent did not exist).

Findings, each sent to builder run 104 to fix before it goes on:
1. Any file could be cited as Greg's words on a substring match; no file hash or commit kept.
2. The code commit and the artifact's hash were checked for format only.
3. Outcome visibility was a free sentence; falsifiers could be rewritten later unseen.
4. The data hashes were optional; unknown keys were dropped.
5. An inference with no grounds registered.
6. A refused registration left no record (the verifier plan: never silent exclusion).
7. Any run could revise another's claim.
8. The reviewer's independence was only "a different run number".
9. The brief was not sealed: it pointed at a file that holds the proposer's reasoning; its hash was not kept.
10. The hypothesis was left out of the brief, further than the plan asks.
11. Grounds were written as DEPENDS_ON, which the grounding check does not count as holding a claim up.
12. A ground with no node got no link and nothing said so.
13. A dropped ground's link was never withdrawn; no REVISES or CONTRADICTS edge (the last two: Greg's to settle).
14. The verdict-word check covered keys that are never stored, and refused ordinary words.
15. The store check in the tests was weak; one refusal case tested the wrong thing.
For ticket 01 it read the first decider: conditions 1 to 3 rest on rule texts; condition 4's quote of CLAUDE.md
does not stand word for word (the page writes ASCII where the file has other characters); the -0.20 and ~65%
are crypto-era measurements, which is a point for the challenge.
