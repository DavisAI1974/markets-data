# The agents' build: the list, marked off as each step is shown done (2026-11-24, twenty-fourth session)

Greg, 2026-11-24: "Before you start coding i want you to come up with a step by step list that you will mark off
when they are accomplished steps of how we are going to fully implement our build plan. I don't want any excuses
or handwaving saying that things are done when they aren't. This is our last building session for the agents".

The plan: Markets `research/kalshi/frankie_boss/CLAUDE_ARCH_PLAN_GRAPH_ENGINEERING_ADOPTION_20261123.md` and the
paper it rests on ("Graph Engineering", 11 pages). The paper's own test for the whole build: "Every important
output can be traced to an objective, a plan, an artifact, a source, a graph path, an evaluator decision, and a
bounded execution record."

How a box is marked. `[x]` only with the evidence written beside it: a commit, or a command and what it printed,
seen in this session. `[ ]` not done. `[GO]` built as far as it can be and waiting for Greg's go, with its budget.
`[HIS]` a decision that is Greg's and is not made. A step that was built in an earlier session and not seen
working in this one is `[ ]` until it is seen.

## A. The ground under the build

- [x] 1. The platform checkout holds its whole history and its libraries. Evidence: `git rev-parse
  --is-shallow-repository` prints `false`, 167 commits; `import nautilus_trader, databento, numpy` prints 1.231.0,
  0.81.0, 2.3.5.
- [x] 2. The plan a trial changes exists: `paper_platform/execution_plans/loop-trial.json`, a byte copy of the
  give-back plan (the hold rule in force). Evidence: platform `47fa1c5`; `cmp` of the two files is silent.
- [x] 3. The last run of the night ended as set. Evidence: receipt of `0f33fec4`, status "stopped 30 minutes after
  the first paced record, as set at the start", 4,033 journal rows, flat, no shutdown error. Not scored.
- [x] 4. That run is in the graph and the experiment record. Evidence: markets-data `8c6d0ec`; 1,710 orders,
  1,684 fills, 25 rule versions, trial `exp-2633f97cb6b9`; `kgraph check` prints "no breach".
- [ ] 5. Markets and markets-data checkouts hold enough history that a graph write names each file's own commit.
  HALF DONE. markets-data: `--is-shallow-repository` prints `false`, 571 commits. Markets: STILL SHALLOW (builders
  are writing in it); until it is whole, no graph command that names a Markets file's commit is run, and the
  `coverage` refresh waits on it.

## B. The graph as the memory (the plan's "largest expected saving", stages 4b and 5a)

State today, read from the graph: 1,147 claims from 8 documents. Handoffs U, V, W, X are in it. Handoffs Y, Z, AA
and the decisions file after line 6152 are NOT. Sessions still start from the handoff pile. The saving has never
been measured.

- [x] 6. The two lines of run 47 are settled so the agent-run record reads again. Greg: "do all 4 like you
  recommeded". Both lines stay; a line marked `corrects` is the run's next revision. Evidence: Markets `d712e0d`;
  `ingest_agent_runs` ran without refusing; the graph's AgentRun count went 35 -> 75 (every run in the file then);
  run 47's node shows the correcting line's figures; markets-data `d6b42ea`, `7877d9b`.
- [x] 7. Handoffs Y, Z and AA and the decisions file from line 6153 are read into claims by seven readers on Haiku
  (runs 70 to 76). Evidence: each reader's last line with a claim equals its piece's last line and no top-level
  bullet is without a claim (checked by code); 1,416 claims taken, 15 refused because the quote did not stand
  word for word (kept as Task lines); Claims 1,147 -> 2,563; `kgraph check`: no breach; the JSON under
  `graph/reads/run-0070..0076-*`; tokens by the harness: 139,521 / 131,291 / 157,673 / 216,270 / 219,900 /
  211,376 / 206,466 = 1,282,497 of the 1.5 million approved. NOT COVERED: the decisions file is read to line
  7070; this session's later entries are read at the close (step 32). `extract coverage` has not been run again
  (it waits on step 5), so the graph's own count of documents read is stale.
- [x] 8. The size is measured; it is NOT yet a saving. Evidence: the graph's session-start text plus the text for
  this task is 36,029 characters, about 9,000 tokens at 4 characters a token, against 78,868 characters, about
  19,700 tokens, for the pile. What the smaller text does not carry is step 9's result.
- [ ] 9. A fresh agent given ONLY the graph's context answers what a new session needs. FIRST TEST DONE, AND IT
  DOES NOT YET HOLD (agent run 83, Sonnet, one tool call: the read of the text; 109,515 tokens by the harness).
  Of 15 questions: 7 answered with claim ids; 3 in part (the one file a trial changes, how run 47 was settled,
  what comes next); 4 not in the text (what a trade day is, where the keys are named, never deploy the phone
  page during a run, who decides at the tick); 1 WRONG (the platform branch, from an old claim). The context
  builder is being changed for it (Markets, agent run 80). The box is marked only when a fresh agent, after the
  change, answers all 15 from the text or each miss is named here.
- [ ] 10. This session's handoff is the graph's start command and a short page of what the graph does not hold,
  not another long handoff. Shown by: the page in git and the command's output for the next session's task.
- [GO] 11. The other 97 documents in the reader's scope (the older handoffs, the research notes). Not read. About
  97 reads, about 16 million tokens on Haiku by the harness's count. Waits for Greg's go.

## C. The loop with an agent proposing each change (stages 3 and 7f on the own platform)

- [ ] 12. The proposer: the loop hands each trial's history and the graph's context to an agent and takes one
  change to `loop-trial.json` back; the tokens come from the harness's own report. Shown by: the code in Markets
  and its checks green on real records with a command that only prints (no engine).
- [ ] 13. Each proposal names the claims it rests on, or is marked an inference; each named claim is checked
  against the graph and the check is kept in the trial's record (the paper's "evaluator decision"). A missing
  path is reported, never a gate. Shown by: a check that reads the `proposal` out of the experiment record.
- [ ] 14. The ready check: one command that starts nothing and says whether the loop can start. Shown by: its
  output on `platform_exit.md`, every entry ready, and a check proving it never runs the control file's command.
- [ ] 15. The control file is right: the data path resolves from the loop's worktree, and the budget declares
  model calls, agents and tokens (the paper: every run declares its limits before it starts). Shown by: step 14.
- [ ] 16. The manual says how the main session runs one trial's handshake, step by step.
- [ ] 17. Two readers on the whole diff (the Pocock review: one for the house rules, one for the plan and the
  handoff's list), the reviewer on Opus. Shown by: their findings, each fixed with its commit or listed as open.
- [GO] 18. The loop's first start. Trial 0 and three trials: four passes of 30 minutes of stored tape through the
  engine (the one pass made on his go took 4 seconds), three proposing agents on Sonnet, at most 300,000 tokens.
  Waits for Greg's go.
- [HIS] 19. The figure the loop keeps or reverts by. Until he chooses, every trial is recorded and none is kept
  or reverted.

## D. Rules tied to claims (stages 4c, 7d, 7f)

State today: 60 rule versions in the graph (30 of the own platform, 30 of the old runner); the grounding check
asks for evidence on all 60. The platform's rules point at 3 documents; none of the 3 is read into claims.

- [ ] 20. The grounding check is seen running on the platform's 30 rule versions and its result is kept.
  Shown by: `rule_versions check --record` after step 5, 30 Evaluation lines for the platform's rule versions.
- [GO] 21. The documents the rules rest on are read into claims: `strategy-20261123-claude/EVIDENCE.md` (388
  lines), `VERSIONS.md` (785 lines) and Codex's `EVIDENCE.md`. About 7 reads, about 1.2 million tokens on Haiku.
  Waits for Greg's go.
- [ ] 22. A rule version is tied to the claims read from the lines its `finding` link points at, by fixed code,
  every tie its own line that can be taken back. Shown by: the check of step 20 run again, and the count of rule
  versions that now have a path beside the count that still ask for evidence. Needs step 21 to show anything.

## E. Everything built in the twenty-first session, seen working or said not to be

- [ ] 23. The agent program's checks on the data as it stands. Last seen: 30 failed, 62 passed, 21 skipped, 52
  errors. Shown by: the run after steps 5 and 6, and every check still failing named with its cause.
- [ ] 24. The real graph through the fixed code (handoff Y): `kgraph check`, `extract recheck`,
  `platform_scope mark`, `check` again. Shown by: what each printed.
- [ ] 25. Stage 5b (Frankie's packet from the graph), stage 6 (the swarm) and stage 8 (the token test): each one's
  `plan` command, which calls no model and sends nothing, runs and prints its count. Shown by: the three outputs.
- [ ] 26. Every agent run of this session is a line of `agent-runs.jsonl` with its model and tokens, the stopped
  ones too.

## F. Held, and not to be called done

- [GO] 27. A run of the swarm (stage 6). Needs Greg's go and a model key; none is in a session or in GitHub.
- [GO] 28. A run of the token test (stage 8). Needs Greg's go, a model key, and Granite's receipts of a whole
  trade day, which are on the Linux box (AWS, off limits).
- [GO] 29. Switching Frankie's input to the graph's packet (stage 5b). Launch is HOLD.
- [HIS] 30. Whether Frankie or an agent decides at the tick (stage 8d). Not built; his to say first.
- [HIS] 31. The plan's stage 1 says to retire the three `aws-*` agent files and the `aws-mcp` entry. They are
  still in Markets. Removing files goes to Greg first; not done.

## H. The graph live in a run, and applied to the strategies (Greg's word, 2026-11-24, added after the list)

Greg: "it's not just building the old stuff, there's supposed to have been code that should have been reading and
building the graphs pretty much in real time and applying to the strategies."

State today, read from the platform's code and the last run's receipt: NONE OF THIS EXISTS. Nothing in a run
reads the graph, writes the graph or calls an agent. A run's orders and fills reach the graph only when a session
loads the finished run by hand. The 32 written rules decide alone at the tick. The plan's own text has this only
as stage 7d (the links, with no word on when) and one paragraph of stage 8d.

- [x] 34. The graph is written WHILE a run goes: `tools/kgraph/live.py` follows a run's record branch push by push.
  Evidence (Markets `9637393`, `6644da0`; checks on real records, 7 passed in `test_live_platform.py`): followed
  over all 90 pushes of run `0f33fec4` (25.3 s) and all 143 of `ea4c1d2e` (39.8 s), each ends with the same
  (id, content) of every node and edge as one load of the finished run; a second follow writes nothing. NOT
  DONE, said so: nothing starts the follower by itself when a run starts; a session starts it.
- [x] 35. For every opening signal the graph's packet for that moment is built: `tools/kgraph/signal_packet.py`.
  Evidence (Markets `7b85a49`): on run `0f33fec4` all 217 opening signals, 0 breaches of the leak check; a packet
  built at an early push equals the one built at the tip; 612 to 5,998 tokens a packet at a 6,000 budget. WHAT
  THE CHECK CANNOT SEE: whether a stored value was itself made from later ticks; and the rule texts were written
  with these four trade days already seen. On the 2023 tape every claim of the graph is out of every packet
  (2,563 of 2,563): each was written after that tape. A packet today is the rule, the run's own earlier rows and
  the dipole events known by then.
- [GO] 36. A place in the run where an answer is applied to the strategy, built switched off. BUILT, READ BY THE
  REVIEWER, NOT RUN (platform branch `ccr-0ac78691-8zapbb`, `d2403b1`..`6f7c54f`; NOT on Codex's branch). The
  reviewer (run 82, Opus) walked every added line with nothing plugged in and found no path where a row, order,
  fill, timer or budget differs. It found faults with answers or a decider ON: a malformed answer can stop a run;
  a close by answer also ends the rule's own research idea; the wait for a decider counts against the run's
  clock; two smaller ones. Being fixed (run 84), then read again. ITS PROOF, that a run with nothing plugged in
  is the same row for row, is one pass of the tape through the engine: waits for Greg's go.
- [x] 37. WHO ANSWERS AT THE TICK: DECIDED BY GREG, 2026-11-24: "We are supposed to be testing our new agents
  setup to see if they could be the decders. Again, that's the intent behind all of the work we've done on them
  and it's stated in the zip files". The agents decide. Evidence: his words, in the decisions file.
- [ ] 37a. The gate: when a rule's opening signal fires, the decider is asked and the order goes only on "take";
  a missing or broken answer opens no trade. Built for the trial (not paced). Shown by: the code, its checks
  that need no tape, and the reviewer's read. Its proof on tape is step 38.
- [ ] 37b. The decider's side in Markets: for each question the graph's packet is built, the brief is handed to
  an agent, the answer goes back, and every decision is its own line (the packet, its tokens, the answer, who
  answered, how long it took). Shown by: checks on a real run's journal with no engine.
- [ ] 37d. ALL OF THE DATA DEPTH REACHES THE DECIDER (Greg: "We have to get all of data depth back.in"): the
  dipole and exhaustion lines, every other value the engine's inputs hold at the signal's tick, and the order
  book's depth level by level. Shown by: the platform's question carrying it (code and no-tape checks), the
  packet passing it through, and, on tape (step 38), one question's `state` beside the book as the journal has
  it at that tick.
- [ ] 37e. The loop on the decider program: one file an agent changes (`loop_decider.py`), one trial to try it,
  every trial recorded; and a first version written by an agent (`decider_v1.py`, in git for Greg to read:
  Markets `04f4378`). Shown by: the control file loading, the ready check, and checks with a command that only
  prints.
- [ ] 37c. NOT BUILT, said so: the gate in a paced or live run (the order would have to wait while the tape moves
  on), and answers reaching a run on a GitHub runner from a session. A decider at the scale of a whole trade day
  needs a model key; none exists in GitHub or a session.
- [GO] 38. THE FIRST DECIDER TEST: a trial of a stretch of stored tape with the agents deciding each opening
  signal from the graph's packet. It puts the tape through the engine: waits for Greg's go, put to him with its
  budget (how many signals, which model, how many tokens).

ROOT in a run (his question the same hour): YES for the calculations the rules read. Every run works out, at
every tape message and on the tape's own nanosecond times, `root/calcs/quote_runs.py`, `root/calcs/leg_peaks.py`,
`root/book.py`, `root/calendar.py` and the dipole (60 s) and exhaustion (20 s) lines of `crypto_ng/tick.py`; the
receipt of each run lists them with their hashes, and its causal check passed. NOT SHOWN SINCE 2026-11-23: that
those lines equal ROOT's stored ones at every sided print (the platform branch's own checks have not run since).

- [GO] 39. The platform's own checks run again (`verify_paper_platform.yml`, his to start or to give the go
  for): they hold the check that the run's lines equal ROOT's.

## G. The close

- [ ] 32. Greg's decisions of the session are in the decisions file as they were made.
- [ ] 33. Everything is pushed in the three repositories; this list's boxes match what the evidence shows; what
  is not done is said in the first lines of the last reply.
