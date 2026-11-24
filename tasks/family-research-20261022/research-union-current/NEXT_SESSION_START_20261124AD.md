# Start page AD, 2026-11-24 (written at the close of the twenty-sixth session). The page before this one: `NEXT_SESSION_START_20261124AC.md`.

Greg, 2026-11-24, his last instructions of the twenty-sixth session: "So why no auditor for every ticket?"; "And
when these agents get done, start new session"; "Don't start any new ones"; "Just restart the ones i stopped and
let them finish".

## JOB 1, BEFORE ANYTHING ELSE: FIX THE AUDITOR (his word)

Greg, 2026-11-24, at the close of the twenty-sixth session: "Then stop.running aditor for tje rest of this session.
Make fixing him.jon 1 in next chst". So the auditor was not run again in that session, neither the agent nor the
check at the close, and fixing it is the first job of this one. WHAT "FIXING" COVERS, as Claude reads it, his to
correct: (1) the rows owed, listed below; (2) the way the auditor is called, so that no run is ever again left
without its row: each group's suite is sent out WITH its auditor, and a group's box is not looked at before that
auditor is back.

His rule: the auditor covers EVERY run, and a group's suite is all four kinds of agent. In the twenty-sixth session
the main session wrote "one auditor run at the close" into the record without his word. That is taken back (the
decisions file, twenty-sixth session; the standing page `paper-trading-20261123/BRIEF_STANDING_20261124.md`, its
auditor section). He then said no new agent was to be started, so the session closed with these runs owing a row:
OWED, by group (each group's runs by that group's own auditor run):
- G03, ticket 04: runs 191, 210.
- G05, ticket 25: runs 196, 211, 214.
- G07, ticket 38: runs 203, 204, 207, 208, 212.
- G08, tickets 18 and 19: run 194.
- G11, ticket 46: runs 202, 209, 213.
- Scout run 206 (his earlier answers; it names tickets 15, 16, 22, 29, 36, 38, 42).
`python3 -m tools.kgraph.auditor_called --data <data>` EXITS 1 until they have their rows (it did when last run: 12 runs listed, before runs 210, 212 and 213 were recorded; with them 15 runs owe a row). No ticket's box is
marked before that. Send the auditor group by group (each run its own `## Run NNN` block; the kept transcripts are
in `paper-trading-20261123/transcripts/`), limits written and pushed and told to him first.

## READ FIRST, EVERY SESSION (his word)

Unchanged from page AC, its section of the same name: read ALL EIGHT files of `frankie_handoff_20261123_2/` whole
(beside this page), the verifier plan, then `READ_FIRST_UNTIL_THE_AGENTS_PART_IS_DONE.md`. THERE ARE FOUR KINDS OF
AGENT (scout, builder, reviewer, performance auditor). No general agents. Then read the decisions file
(`root-redesign-20261116/ROOT_GAMEPLAN_DECISIONS.md`) from "## Twenty-sixth session" to its end, and
`paper-trading-20261123/BRIEF_STANDING_20261124.md` (what every agent's brief points at).

THE POCOCK SKILLS: he added the plugin "Skills For Real Engineers" (mattpocock/skills) to his own library during
the twenty-sixth session; a session's library is read when it starts, so that session could not call them. SAY IN
YOUR FIRST MESSAGE whether `ask-matt`, `implement-spec`, `tdd`, `code-review`, `retro`, `to-questionnaire` are in
your list, and call them by name if they are. They are NOT registered in Markets (his word: "Don't").

paper-trading-platform: say in your first message whether it was selected WITH PUSH ACCESS. In the twenty-sixth
session it could be read (it is public) and not pushed to. Tickets 41, 42, 43 and the 30 minute test need the push.

## ANSWERED BY HIM ALREADY: DO NOT ASK AGAIN (his words: "I answered all of these questions in a session earlier today")

Each with its place in the decisions file (DEC). The sheet `paper-trading-20261123/to-questionnaire-what-only-greg-can-say.md`
holds the same list and the nine gos that are still his.

1. THE ORDER: the rest of the build list; then the 30 minute test of the agents WITHOUT the operator coefficients
   (his go, told with its limits); then ticket 47 LAST; then the same test WITH the coefficients, laid beside the
   first decision by decision.
2. THE 30 MINUTE TEST is 30 minutes of one of the four trade days on the stored tape, a short test (DEC:6697,
   6921, 7341). Only his go for the run itself remains.
3. THE AGENTS ARE THE DECIDERS (DEC:7086, 7138).
4. EVERY DATA LAYER goes to a decider; layers may be graphed to save room, none is dropped; everything stays in at
   first (DEC:7186, 7196, 7230). AFTER-THE-FACT DATA is a layer: kept, joined to every decision, read by the agents
   that write the next decider; out only of the packet a decider reads at the instant (DEC:7236). Native's
   later-written columns, ROOT's after-the-fact columns and the peaks go in that afterwards layer (DEC:7245).
   THE DAILY SHEETS ARE THE FOUR `root-rows` BRANCHES; the stored-rows sheet's own COLUMNS page marks all 408
   columns "Shown to Frankie: yes". All of this is laid out at the foot of
   `paper-trading-20261123/tickets-44-20261124/PLAN_38_EVERY_LAYER_20261124.md`: read it before ticket 38.
5. NO RUN WITHOUT HIS GO (DEC:7004). NO VERDICT WORDS (DEC:7480). A RECORD IS ONLY ADDED TO (DEC:7005). FOUR
   AGENTS, NO GENERAL AGENTS (DEC:7414). Data in markets-data carries MANIFEST entries (DEC:5583).
6. THE AUDITOR COVERS EVERY RUN (above).
7. A RESTART OR A SEND-BACK IS A NEW RUN NUMBER with its own limits, pushed and told to him before it starts.

## AGAINST READ AFTER READ (his word; the retro is `paper-trading-20261123/RETRO_20261124_SESSION26.md`)

ONE reviewer read for a ticket, measured only against the ticket's own "shown done by" line and the standing rules
by name, 500 words at most; then ONE builder pass; then the main session runs the named checks. A ticket is marked
when its done-line is met AND `auditor_called --ticket NN` exits 0. What a read finds beyond the line is one line
at the foot of the ticket, not another round.

## Set up before anything else

- Put the session's Markets and markets-data branches on top of `ccr-144315dd-pta2ze` (heads in the table below).
  markets-data must hold its WHOLE history (`git fetch --unshallow` of that branch only; never fetch every branch
  of Markets: it is over 32 GB).
- `pip install pyarrow numpy` (the packet's checks need them; the environment's setup script does not install them).
- The stored planes of trade day 2023-10-02 for the packet's checks: a bare git folder holding markets-data branch
  `root-rows-20231002` (about 434 MB), given to the checks as `MARKETS_PLANES_GIT=<that folder>`.
- The platform checkout beside Markets (`paper-trading-platform`, detached at `origin/ccr-0ac78691-8zapbb`,
  `28d4dbb`): the environment's setup script clones it; check it is there. Without it 79 checks skip.
- Checks: `MARKETS_DATA=<data> python3 -m pytest tests/agent_program/<file> -q -rs -p no:cacheprovider
  --basetemp=<a folder OUTSIDE every git repository>`; delete the folder after every run. markets-data must be
  CLEAN (committed) while any check runs: the checks refuse a copy with uncommitted changes.
- A builder's working copy: `git worktree add`, sparse: tools tests .claude research/kalshi/frankie_boss odcore
  root crypto_ng. It pushes `<its branch>:<the session's branch>`, fetches and merges when refused, never forces.
- Recording a run: the commands on page AC ("The tools built this session"). Use a QUOTED heredoc for any text
  with backticks. Commit the record at once after each recording.

## Where things are (check each with git before trusting it)

| Repository | Branch | Head |
| --- | --- | --- |
| Markets (code) | `ccr-144315dd-pta2ze` | `793c5af` |
| markets-data (records, graph, tickets) | `ccr-144315dd-pta2ze` | the commit that holds this page |
| paper-trading-platform, the change of the twenty-fourth session | `ccr-0ac78691-8zapbb` (NOT Codex's branch) | `28d4dbb` (read only; no push access in the twenty-sixth session) |
| markets-data, the stored planes of the four trade days (the daily sheets) | `root-rows-20231002`, `-20231003`, `-20231017`, `-20231018` | `360fdaa`, `c8a0b75`, `733442a`, `1bd670e` |
| Markets, Codex's discovery pipeline (ticket 47, LAST) | `od-refrag/markets-handoff` | `93ac56f` (only its README is read) |
| Markets, the April operator search (ticket 47) | `od-autoresearch/apr5-handoff` | `e65441a` |

Agent runs are recorded through 214. The next run is 215.

## Where the work stopped

NOTHING IS IN FLIGHT. At the close he said "Close it" and the last three builders (runs 210, 212, 213) were stopped
by the main session before they handed back; every run of the session is recorded (157 to 214): its report word
for word where it handed back, its line, its kept transcript. What the stopped builders had pushed is on the
Markets branch; what two of them left uncommitted is kept as patch files in
`paper-trading-20261123/builder-20261124/LEFT_UNCOMMITTED_RUN_212_ON_793c5af.patch` and
`LEFT_UNCOMMITTED_RUN_213_ON_4f0757c.patch`. The working copies themselves are lost with the session.

THE SESSION BRANCH OF MARKETS HOLDS FAILING CHECKS. What is shown, no more: (1) test_defend.py printed "11 failed,
68 passed" for stopped run 210; the one failure whose text is kept is a `defend.show` with no run named (ticket
04's own point 1); the names of the 11 are not kept (`04.md`). (2) One check of test_ingest_artifacts.py fails
because of the record (`25.md`, `19.md`). (3) Stopped run 213 saw 2 failing in a run of test_consolidate.py,
test_stage5a_context.py and test_stage4c_grounding.py together; names not kept; one was a file missing in the
platform checkout (`46.md`). Run each file whole before building on it.

NOTHING WENT THROUGH THE ENGINE OR THE TAPE. NOTHING WAS CALCULATED. NOTHING WAS WRITTEN INTO THE REAL GRAPH. No
paper run, no Frankie, no pod, no AWS, nothing to the trunk. THREE TICKETS ARE MARKED DONE: 03b, 21, 31.

Each worked ticket's own file (`paper-trading-20261123/tickets-44-20261124/NN.md`) ends with "State at the close of
the twenty-sixth session"; `GROUPS.md` in that folder ends with a table of where each group stands and what comes
next. Start each suite from those, not from memory.

DO, in this order:

0. The auditor rows owed (the top of this page).
1. G08, ticket 19: a builder fixes the recorder, the failing check first: a correcting line takes its session and
   every field it does not restate from the line it corrects (`tools/kgraph/run_record.py`, about line 271); then
   one more correcting line for run 119 puts `data_commits` back (that clears ticket 25's one failing check), and
   run 179's line goes back as written with the loader taking its correcting line. Then tickets 18 and 19 are
   marked.
2. G07, ticket 38, the one he has said again and again: every data layer to the decider. Read the plan and its
   foot and `38.md`. FIRST points 6 and 7 of parts C and D (point 6 from the kept patch: the after-the-fact file
   out of the folder a decider reads). Write the known-at table (each group of columns of each of the 63 layers: packet at its tick, packet at
   its known time, or the afterwards layer) from the plan's foot; ONE builder for parts A, B and E; ONE reviewer
   read with the stored planes present. The reviewer is also given the possible fault in `root/dipole_peaks.py`.
3. G05, ticket 25 points 3 and 4 (after item 1), then ticket 37 from scout 197's places.
4. G03, ticket 04: a builder runs test_defend.py whole and clears the failing checks its point 1 left (`04.md`); then one reviewer read
   against its done-line; then G04 (05, 06, 09), the same chain of files.
5. G11, ticket 46: point 4 from the kept patch (`46.md`); then the box.
6. G01: the three small points of reviewer run 190; the proposer's commit on eight grounds; ticket 01.
7. G09: ticket 14's nine points and the read of the platform change `28d4dbb`; the write-ups of 12 and 13; 15 is
   answered and is marked once scout 206 has its row.
8. Builder jobs not started: the manifest for the paper-trading folder (142 files named by ticket 31's command,
   none with an entry); the lock in code so no paper run starts without his written go; `pip install pyarrow`
   and the planes fetch in the environment's setup script.
9. THEN, on his go, told with its limits: the 30 minute test without the operator coefficients (G12). THEN ticket
   47. THEN the same test with the coefficients. Ticket 45 (two readers who built none of it) at the end.

## Faults of the twenty-sixth session that are still open (the main session's own)

- RUN 179'S LINE was changed in place (model "" to the plan's model). His rule is "only add". It goes back as it was
  written once the loader takes the correcting line (a builder's job; `tools/kgraph/ingest_agent_runs.py`).
- THE RECORDER takes a correcting line's session from the transcript's own harness id when the run has no plan
  (`tools/kgraph/run_record.py` line 271); it should take the session of the line it corrects. Seven such lines
  (runs 107 to 113) broke the loader; he allowed them to be put right in place, once ("Fix the 7 lines"). A
  builder fixes the recorder, the failing check first.
- NOTHING STOPS A RUN AT ITS LIMIT: scouts 206, 207 and 208 each went past their token limit and were only seen
  afterwards. Code cannot hold it; the auditor's row says so for each.

## Still his (none holds a builder; the sheet has each as one yes or no)

Tickets 07 and 08 (the reads), 28, 10, 16, 22 and its figure, 29, 36, 42; whether the auditor's row for each run is
made by a command with the auditor agent called on the rows that differ (the retro, item 2: NOT adopted; his
rule stands until he says). On ticket 38: the 20 columns of the crypto and ng program's own trades are kept out of
both the packet and the afterwards layer on his "observation and verification only"; that is Claude's reading, his
to correct. On the four daily branches: three `trade-legs-6pm-to-8pm` tables are on 10-02 and 10-17 only and one
test index on 10-02 only; whether they are made for the other trade days is his.

REMIND HIM: the repositories go private when the build is done. That step is his.
