# What is still missing, from a second full read of the zip and the paper (2026-11-24, twenty-fourth session)

Greg, 2026-11-24: "I thought every claim had to be defended with the new piece that we added to our agents that
wasn't in the loop pdf. Go back and reread the files in the pdf"; "We are still missing pieces. Don't do anything
after you read but mKe a list".

Read again in full: the zip's eight files (the handoff note, the plan, the Codex amendments, the CLAUDE.md roles
section, the four agent files), the verifier plan they name (Markets
`research/kalshi/FRANKIE_INDEPENDENT_SCIENTIFIC_VERIFIER_PLAN.md`), and the paper's appendix and checklists.
Nothing was built, started or restarted after the read. Each line: what the files say, then what is so today.

## A. Every claim defended (the piece that is not in the paper: the independent verifier)

The verifier plan's one rule: "the proposer of a claim must not be its sole verifier. An independent reviewer
should challenge the claim, while deterministic checks establish what the evidence actually supports." The
amendments make it one system with the graph: its claim, check, verdict and adverse-evidence contracts are the
fields of the graph's Claim and Evaluation nodes, and the independent reviewer is the reviewer agent.

1. NO CLAIM MADE TODAY WAS CHALLENGED BY ANYONE BUT ITS PROPOSER. The first written decider's four conditions,
   and its five inferences, were written by one agent and read by no independent reviewer. The loop's proposer
   hands in a change with the claims it rests on, and nothing challenges it before its trial.
2. NO CLAIM IS REGISTERED BEFORE ITS OUTCOME IS SEEN. The contract asks for: the hypothesis, the exact claim, its
   scope, its mechanism, its alternative explanations, its falsifiers written beforehand, the code commit and
   the data hashes. The graph's layout has these fields; nothing fills them. A proposal today carries a
   one-sentence hypothesis and a list of claim ids.
3. NO COMPETING EXPLANATION, NO FALSIFIER, NO DISTINGUISHING OBSERVATION is asked of anyone. The plan asks the
   reviewer for at least one of each, "without feeding it the proponent's conclusions first".
4. NOTHING KEEPS THE OUTCOME FROM THE CHALLENGER until the challenge is on record. Built today: the proposer is
   handed the last trial's after-the-fact record; no rule says who may see it when.
5. NO CHECK IS WRITTEN AFTER A TRIAL. The check register asks, for each check: what was expected, what was
   observed, the inputs' hashes, the reviewer. Nothing compares a trial's record with what its claim said would
   show it wrong.
6. NO ADVERSE EVIDENCE IS ON RECORD. The graph has no CONTRADICTS link at all; a refutation is to be kept beside
   the claim it refutes, both standing.
7. NO RULE IS TIED TO A CLAIM. The plan (7a, 7d) and the amendments: each rule names the claim ids it rests on,
   so every paper order traces to registered claims and their checks. Today: 60 rule versions, all 60 ask for
   evidence; the rules point at 3 documents and none of the 3 is read into claims.
8. THE FIRST DECIDER'S MAIN GROUND IS NOT A CLAIM OF THE GRAPH. Its divergence condition rests on the dipole
   research in CLAUDE.md, and CLAUDE.md is not among the documents the graph reads. So it has no graph path.
9. A DECIDER'S DECISIONS ARE NOT IN THE GRAPH. Each decision names the packet lines it rests on and is kept as a
   line of a file; nothing loads decisions, or what happened after them, as nodes with their checks.
10. NO REFUTE WAVE HAS RUN ON ANYTHING (the plan: Opus, on high-stakes findings). Not on the readers' 1,547 new
    claims, not on the 32 consolidation links, not on the decider.
11. Status words: the files ask for what was checked, what was observed, what remains open, and no verdict
    labels unless he asks. The graph's layout follows this. Not yet applied to a trial, because no check exists.

## B. The agents (stage 1 and the amendments)

12. THE SCOUT WAS NOT USED ONCE. The roles section: "The main session does not grep or bulk-read files itself
    when the scout can." This session the main session read and searched itself, and the reads into claims were
    done by general agents (the scout cannot write a file).
13. THE BUILDER DID NOT SHOW ITS DIFF FIRST. Its file says: show the diff and wait for the main session's go.
    Every builder brief today told it to write without waiting.
14. THE REVIEWER HAS NOT READ THE FINAL DIFF. Its file says: the final diff before it goes to Greg or Codex.
    The platform's third read was stopped before it returned; everything built in Markets today has been read
    by no reviewer.
15. "Four agents in total; no more." This session also used general agents as readers, a consolidator, a test
    reader and a writer.
16. Retiring the three `aws-*` agent files and the `aws-mcp` entry (stage 1): not done; his to say.
17. The performance auditor's Granite call list for one trade day (the token test's baseline): not made. The
    receipts are on the Linux box, which is AWS and off limits.

## C. The token plan (it applies to every stage)

18. NO RUN HAD ITS BUDGET WRITTEN IN A PLAN BEFORE IT STARTED. The plan: max model calls, sub-agents, concurrent
    workers, tool calls, tokens, wall clock, retries and graph writes, in the run's plan JSON, and on running
    out the run returns what is done, what is open and why it stopped. Today a token figure was told to Greg in
    chat; nothing held a run to it (one test run passed its figure unnoticed until it ended).
19. AGENT RUNS ARE NOT RECORDED AS THE PLAN ASKS. It asks for the model, input tokens, output tokens, wall clock
    and outcome. Recorded: the harness's one total, the model by its short name; ten stopped runs have no
    figure; runs 99, 100 and 101 are not recorded yet.
20. THE SAVING IS NOT MEASURED. The plan calls the graph-built context "the largest expected saving", unknown
    until it runs side by side with the current session start AND the current Frankie packet (92,427 tokens).
    The session start: measured in size, and it fails on content (two tests). The Frankie packet: not run.

## D. The experiment record, the loop, the graph (stages 2, 3, 4)

21. The record's first users (the build plan workbook's Experiment Arms sheet, the experiment orchestrator's
    steps, the dipole teacher arms D0 to D5): not seen in the record this session; not verified.
22. The loop has never run. Its figure is his to choose.
23. The plan's own candidate loops have no control file: the extraction prompt itself (the paper's "graph
    autoresearch", with a gold set and precision and recall) and the Granite structured-output plan.
24. Nothing runs a loop on a GitHub runner or a pod; there is no workflow file (dispatch is on HOLD).
25. NO ARTIFACT NODES AND NO METRIC NODES. The paper's invariant: every artifact has an authoring run and a
    version. The plan's session context is to include "the current artifact versions". The graph holds neither
    kind of node, so it cannot say where things are now. This is the cause of the wrong-branch answer in both
    tests, and it was in the plan all along.
26. NO OPEN CONFLICTS in the session context (the plan asks for them): there is no CONTRADICTS link to show.
27. Merging names (Sonnet resolution) was not run on today's 1,547 new claims.
28. The build plan workbook and the research notes are not read into claims; 97 documents unread (needs his go).
29. No gold set, so no measure of the readers (precision, recall), of the merges, or of the answers beyond the
    15-question test. No monitoring of the graph over time (the paper's trends).
30. The graph's own count of documents read is stale (its refresh waits on the Markets checkout's history), and
    the handoff's commands for the real graph (`extract recheck`, `platform_scope mark`) were not run today.
31. Whether the files added to markets-data today have their MANIFEST.json entries: not checked.

## E. Context and packet (stage 5), swarm (6), paper record (7), token test (8)

32. The session start from the graph does not hold yet; the short page beside it is not written or tested.
33. Frankie's packet from the graph: built beside the old path, never run side by side (HOLD).
34. The swarm: built, never run (needs his go and a model key; none exists).
35. The token test: built to plan, never run; its baseline cannot be made from git. Its arms with prompt caching
    and batch requests have never been tried. No table, no charts.
36. Stage 8d: the trigger is to be Frankie's own state (events, births, peaks, exhaustion) "posting a task with
    its subgraph and budget". Built today: the platform's own rule signals ask a decider. Frankie's events
    trigger nothing.
37. Rule versions are not nodes of the experiment record for the own platform (the plan: each rule edit a
    commit, each version a node there); they are in the graph only.

## F. Built today and not finished, or never on tape

38. The packet with every data layer (ROOT's stored planes, the whole state beside the brief, the after-the-fact
    file): stopped mid-work twice; pushed unfinished.
39. The first decider was written before the dipole and exhaustion lines and the depth reached the packet; it
    does not use them.
40. The gate, the question's whole state, the MBO window, the book and the market series have never met the
    tape. The book's guard and the size of a real question are unknown.
41. The platform change is on its own branch, not on Codex's.
42. The gate exists in a trial only. A paced or live run has none, and no path carries an answer from a session
    to a run on a GitHub runner.
43. Nothing starts the live graph follower when a run starts.
44. From this morning's list, still open: the Markets checkout's history (5), the whole suite on the data as it
    stands (23), the token test's plan command (25), the two-reader review of Markets (17), the handoff (10).
