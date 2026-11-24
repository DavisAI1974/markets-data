# Reviewer run 183 (Opus): ticket 14, the first read of what was built in Markets in the twenty-fourth session

Everything below this line is the agent's own report, word for word; nothing below it is the main session's.

## Hand-back 1 of 1

# Reviewer run 183 (Opus): ticket 14, the first read of what was built in Markets in the twenty-fourth session

Working copy /home/user/wt/r157 (detached at 74006f2, clean). This machine has no paper-trading-platform checkout, so I could not read the platform's own change. The packet change e55da89..2ac873f is not covered here; run 182 has it.

Read status. I read pieces 1 to 5 in full. In piece 6 I read 6fdd4e1, ad57e2b, 131a9dc, the serve.py and _run_program.py parts of 547e59b, and the later changes to file_proposer.py. Not read: the signal_packet.py part of 547e59b past its first ~230 diff lines (474 lines changed), the tests of 78d1f92 and 1e9a7c5 (test_decider_loop.py), and the test file of 53d46c9 (test_stage5a_context.py). I stopped there because of the tool-call limit.

## The checks
I ran the command once, as given, with `timeout 900` and output piped to `tail -40`. It wrote no pytest output: no dots, no summary line. The process (pid 8993) was still alive about 17 minutes after it started, so the most likely reading is that the 900 s timeout killed it before it printed anything (speculation: the output may have been buffered behind the pipe). I have no measured counts of checks run, skipped or failing for any file. I did not run it a second time, per "one run is enough". `/home/user/tmp-pytest/r183` was deleted; `/home/user/tmp-pytest/b184` belongs to another run and was left alone.

From reading the code only, not from running it:
- test_decider_v1.py skips its whole module when there is no `/home/user/paper-trading-platform` (fixture, test file line 21 and 27-28). On this machine that is all 4 of its checks. So piece 2 was read and not run.
- 53d46c9's commit message says two checks in test_stage5a_context.py are marked as expected failures with the reason. I did not read them.

## Piece 1: 7672c8d afterwards.py
- afterwards.py:109 (now :85) and :191 (now :167) keep only the first decision row and the first journal answer for each sequence (`setdefault`). If a sequence has a second decision line, for example after a restart, the afterwards line silently leaves it out; only the source file still holds it. The code comment says "none dropped from the file", but the join drops it.
- `market_after` (commit :167, now :143) scans for the highest and lowest bid and ask from the signal to the end of the quotes series. It stops at neither the trade day's 17:00 ET end, nor the 17:00-18:00 halt, nor the trade's close. A series that crosses a trade-day boundary would put the next trade day's extremes on the line. No quotes file exists yet (BUILD_NOTES), so this has not happened.
- Leakage: the file carries `known_only_afterwards: true` on every line plus a header. Nothing in this commit hands it to a decider. Its brief (`make_brief`) is labelled "for writing the next decider". At 74006f2 the brief command needs `--claim` (gated by outcome.may_see_outcome) or `--rests-on-none`. The path from here to a program run on the same trade day is under piece 6.
- The brief's budget cut (commit :292, now :270) drops the newest lines. The foot says "Shown: k of N" and points to the file, so what is cut stays on record.
- Fees, mid price: none. The test looks for `"mid` and `spread` in the output and finds neither (test :131).
- The test fixture (test :34-39) builds quotes.jsonl from the bid and ask carried on the real journal rows. These are real values, but the series is assembled by the test and not stored by any collector; its docstring says so.
- Importing it or running its checks starts nothing: no engine, no tape.

## Piece 2: 04f4378 decider_v1
Unchanged since this commit. Line numbers are the same at 74006f2 relative to the file.

Crypto-era figures:
- `STRONG_DIVERGENCE = -0.20` at decider_v1.py:21 is the live threshold. It is used at :118: `aligned = (bought - sold)/(bought + sold) * sign(side)`; skip if `<= -0.20`, for the rules CL01/03/06/10/13/15/16 (:18).
- "~65% reversal" appears only in the comment and in decider_v1.md:41-42. No number in the code uses it.
- The input is the dipole event's `our_flow_bought_20s_after` / `our_flow_sold_20s_after` (:115), not `imb_level`. The page itself says the scale is not established (md:50-51). CLAUDE.md's exhaustion read speaks of collapse "toward 0.5", which suggests a 0..1 scale. Under that scale -0.20 would not be comparable to a figure on a -1..1 scale.

Leakage: the flow columns are documented as known at the end of the birth second (packet.py:80-81, :89). The newest dipole is chosen by `known_at_ns` (:113). I found no read-ahead in the program; it reads only the packet.

Default answer: take (TAKE_WHY, :11). The door's brief for live agents says the opposite: "Say skip when the packet gives no ground to take" (serve.py:135 at 74006f2). See piece 3.

Test test_decider_v1.py:73-97 puts a real dipole node into a real packet at a moment that is not its own. The docstring says "The pairing is not a real moment". This is a constructed packet in a check. That node's `known_at_ns` may be later than the packet's moment, and the test does not check.

Importing it or running its checks starts nothing.

## Piece 3: 9054a00 serve / answer / next
Two cases are left with nothing on record:
- serve.py:268 at the commit (:261 now): a question.json that is unreadable or malformed is "left alone" on every pass. No refused.json, no answer, no decisions.jsonl line. One that never becomes valid stays unrecorded indefinitely while the platform waits.
- serve.py:288 (:347 now): the same holds for a decision.json that is permanently not JSON.

`brief()` catches only OSError/ValueError/KeyError (:270 now). Any other exception from the packet build ends the serve process.

The brief tells a live agent to default to skip (:135 now). decider_v1 and file_proposer RULES ("When the packet gives no ground ... the answer is take") default to take. The same door gives the two kinds of decider opposite defaults.

Importing does nothing. `serve` only answers a mailbox and starts no trial.

## Piece 4: 1d0a6dc the program door
Records:
- An invalid answer from a live agent is kept as decision.rejected.json (settle).
- An invalid answer from a program is not kept. `by_program` (now ~:326-340) writes only the reason, and the program's raw output `d` is dropped. A program that raises keeps only the last stderr line, cut to 300 characters.
- On the program path, packet.json and brief.md are not written. At 74006f2 state.json/layers.json are written (`write_layers`).

Fence: `-I`, env={}, empty folder. The README says plainly that this is not a sandbox. `_run_program.py` imports the program file by path, so importing the door starts nothing. A program runs only when `serve --program` answers a question.

## Piece 5: 53d46c9 context.py
- `SECTION_SHARES` (:74) and `COMMON_SHARE` (:83) are stated as engineering choices.
- Rules are ordered by how many documents restate them (:381), and the budget then cuts from the end. In effect that ordering decides which rules are cut; the comment says "an order for a reader, not a ranking".
- What is cut stays on record. The result returns `cut`, `cut_by_kind`, `not_reached`, `by_words`, and the foot counts them.
- The fill looks at only the first 60 cut claims of each section (:548) and stops after 40 misses (:520). The rest remains in `cut`.
- Which task words were left out by COMMON_SHARE is not recorded in the result.
- Since the commit, 4 lines were added to the file; I did not read them.

## Piece 6: 6fdd4e1..1e9a7c5
**trial_with_decider.py (6fdd4e1)**
- Without `--dry`, it starts the door and `paper_platform.trial` (:144, :146): an engine run on the stored tape. No check in the code requires Greg's go. Only the docstring and platform_decider.md say so. Importing it starts nothing.
- :182 `rmtree(mailbox)` deletes every per-question file: refused.json, decision.rejected.json, answer.json, state.json, layers.json. Only decisions.jsonl is copied, at :180, and only when the trial reports `kept`. Without `--keep`, decisions.jsonl is deleted too, and only the counts survive.
- :148 waits at most 15 s for decisions.jsonl to catch up with the answer.json files, then terminates the door. Lines not yet written are lost, and `decider_asked` undercounts with no message.

**platform_decider.md (131a9dc)**
- The run command uses trade day 2023-10-02 with `--from-minute 30 --minutes 30`: a 30-minute window of the trade day.
- `direction: null`, so nothing is kept or reverted.
- The file says NOT RUN, but `tools.ratchet.loop` with this file starts engine runs. Nothing in the code holds it.

**loop_decider.py**: takes every signal. Importing it does nothing.

**file_proposer.py (ad57e2b), static check**
- `source_problem` (now ~:76) admits any standard-library module that is not in FORBIDDEN. That gives concrete ways round it: `import linecache; linecache.getline("<abs path>/events.jsonl", n)` reads a file without `open`; `import urllib.request; urllib.request.urlopen(...)` names no forbidden word; `io.FileIO(path)` too. The docstring admits run-time-built names, but these cases need none.
- So a program could read a finished journal or the afterwards file at decision time: a leakage path through the program.

**Brief and outcomes**
- The proposer's brief lists earlier trials' figures and the paths of their kept events/trades/decisions (:127-150, :189 now). The next program then runs on the same trade day. Outcomes of that tape reach the author of the decider that decides on that tape.
- Since the commit, `held()` blocks a trial's records only when a REGISTERED claim it rested on fails outcome.may_see_outcome. A trial that rested on `inference` alone, or on unregistered claims, still has its paths and figures shown.
- The folder-to-trial mapping is a guess by modification time, which the code itself says.

**547e59b serve.py and signal_packet.py (part read)**
- Every `state:` line gets `known_at_ns = moment` with basis "the signal's own tick" (signal_packet.py:307, :1095). This is asserted, not derived from the data, so a check that compares times passes it by construction.
- `state:tick` includes `settlement` (:313).
- STATE_SHARE 0.5 (:112). LEFT_OUT_NAMES_SHOWN 20 (:115); I did not read what happens to the rest. Rows over 400 characters are cut, and the line says the whole is in state.json.

## Speculation (labelled)
- What `settlement` means in the platform's tick cannot be read here. If it is the named trade day's settlement, it is after-the-fact for a signal earlier in that trade day.
- The trial wrapper reads the door's stderr through a PIPE and never drains it while the trial runs. A chatty door could block once the pipe fills.
- In decider_v1, the "newest row of the trade" test for a standing suspension (:79-80 area) could read a released warning as still standing if the packet budget cut the release row.

## Open after this read
**For the builder**
- afterwards.py:85, :167: decisions left out by setdefault are not marked on the line.
- afterwards.py:143: the market_after scan is not bounded by the trade day.
- serve.py:261, :347: questions and decisions with no record.
- serve.py:135 against file_proposer RULES: opposite defaults.
- serve.py by_program (~:326-340): rejected program output not kept.
- trial_with_decider.py:148, :180, :182: lost decision lines and deleted per-question files.
- file_proposer.py:50/:76: linecache, urllib.request and io.FileIO pass the check.
- file_proposer.py:127-150: outcome paths shown for inference-only trials.
- signal_packet.py:307: state known_at asserted, not derived.

**For the main session**
- Rerun the checks with a longer wall clock, or per file, to get counts.
- Have the rest of 547e59b signal_packet.py, test_decider_loop.py and test_stage5a_context.py read.
- The platform change needs a machine that has the checkout.

**What code cannot hold**
- Nothing in the code gates trial_with_decider.py without `--dry`, or the ratchet loop with platform_decider.md, behind Greg's go.
- A program fenced by syntax-tree reading is not a sandbox.
- Programs are written by agents who have seen the same trade days they are tried on.
- The 0.20 threshold's scale; the 30-minute window.

Tool calls: 19 of 28.
