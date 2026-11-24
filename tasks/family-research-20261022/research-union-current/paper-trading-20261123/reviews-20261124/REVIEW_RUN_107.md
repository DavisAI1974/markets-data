# Reviewer run 107 (Opus, claude-opus-5-5): the second read of tickets 02 and 03, Markets `3a6ac09` as it stands at `2ac873f`

Kept word for word as the reviewer returned it, 2026-11-24 (twenty-fifth session). Nothing below this line is the main session's. Run 107 was a general agent handed `.claude/agents/reviewer.md` as its instructions (the `reviewer` type had not loaded by name yet). What the main session did with each open point is in `../tickets-44-20261124/02.md` and `03.md`.

---

Reviewer run 107: second read of tickets 02 and 03 (tools/kgraph/defend.py, tests/agent_program/test_defend.py, tools/kgraph/BUILD_NOTES_DEFEND.md), checking the fix 3a6ac09 against the 15 findings of run 105.

Commits read: Markets HEAD 2ac873f (branch ccr-659edd86-di9udt); the fix is 071777f..3a6ac09. `git log 3a6ac09..HEAD` shows no change to defend.py or test_defend.py after the fix, so HEAD is the code that was read. markets-data HEAD is dc51ed2. All experiments ran on a scratch copy of graph/ at /tmp/run107-scratch/graph, which is now deleted.

## Test run

I ran `MARKETS_DATA=/home/user/markets-data python3 -m pytest tests/agent_program/test_defend.py -q --basetemp=/tmp/run107-scratch/bt` from /home/user/Markets.
- Result: **40 passed in 22.03s**, with 0 errors and 0 skips.
- The error from run 105 (the scratch folder's parent did not exist) did not occur. /tmp/run107-scratch had been created first.

## The 15 findings, one by one

**1. Greg's words.**
- What changed: a cited ground (defend.py:234-252) now:
  - finds the latest commit that touched the path;
  - reads the file's bytes at that commit;
  - checks the quote is at least six whole words on the stated lines (`_check_quote`, which uses extract.check_claim);
  - stores the commit and the sha256, and makes or finds a Source node.
- So the substring match is gone, and the hash and commit are kept.
- Still occurs: who said the words is the free-text `said_by`. `_saidline` (defend.py:415-419) prints "Greg's words" whenever said_by is "greg" or "greg davis".
- Case tried on scratch: I cited Markets:KALSHI_TRADING.md line 3 with said_by "Greg". It registered (claim:reg-4e319c63b3da). The brief heading read "### 1. Greg's words, Markets:KALSHI_TRADING.md lines 3-3 (commit b69c879...)". Nothing checks that the file or line records Greg.
- Open: the attribution to Greg is self-declared.

**2. Code commit and artifact hash.**
- What changed: `_verify_artifact` (defend.py:262-275) runs `git rev-parse --verify <commit>^{commit}` in the artifact repo's checkout, hashes the file as it is at that commit, and refuses a mismatch naming both hashes.
- Covered by test_the_artifact_is_checked_not_only_its_format (test:202-208): wrong hash, missing commit, missing path. The failing case from run 105 no longer occurs.

**3. Outcome visibility and later rewrites of falsifiers.**
- What changed: `_outcome` (defend.py:278-283) requires the shape {"outcome_seen": bool, "what": text} and refuses extra keys. When true it is stated in the brief and in show (defend.py:422-424).
- What changed: `show` (defend.py:561-564) lists every revision's falsifiers with written_at and written_by. `undefended` lists the claim again after a revision.
- Still occurs: a revision may rewrite the falsifiers and keep outcome_seen false.
  - Case tried: revision 3 of claim:reg-751bbc009e4c replaced the falsifier and kept outcome_seen false. It registered.
  - show shows revisions 1-3 with their times, so the rewrite is visible.
- Open: outcome_seen is self-declared, and nothing ties "before any trial" to a trial record.

**4. Data hashes and unknown keys.**
- What changed: `_manifest` (defend.py:286-293) requires either a list of {"what","sha256"} with a 64-hex sha, or {"none": "<why>"}. `_unknown` (defend.py:141-144) refuses unknown keys by name.
- Still occurs: the manifest sha256 is checked for format only.
  - Case tried: data_manifest_hashes [{"what":"anything","sha256":"0"*64}] registered (claim:reg-c3d2cf4410d1).
- Open: data hashes are not tied to any file or manifest.

**5. An inference with no grounds.**
- defend.py:388-391 requires a source ground only when inference is false.
- Still occurs. Case tried: inference true, inference_reason "a reading", rests_on [] registered (claim:reg-6bc0ba365ada).
  - Running grounding.check_node on it afterwards returned decision "revise", with "nothing in the graph shows what it rests on".
- So the grounding check catches it after the fact, but registration admits it. No test covers this case.

**6. A refused registration left no record.**
- What changed: `register` (defend.py:297-302) calls `_retain` (defend.py:305-324), which writes a Task node with the file, reason, run and time. Case tried: a claim with no mechanism took the Task count from 161 to 162.
- Still occurs, part 1: `_retain` swallows every exception from store.write (`except Exception: pass`, defend.py:323-324).
  - When the run is not an AgentRun, the writer is `code_stamp(...)`.
  - store.write refuses code-stamped writes into the real graph when the code has uncommitted changes, and also refuses when a pending file is left over.
  - In those cases the refusal is recorded nowhere. This is from reading the code; I did not reproduce it on the real graph.
- Still occurs, part 2: refusals in `challenge` (defend.py:503-523) and `brief` leave no record.
  - Case tried: a challenge by the proposer run was refused, and the Task count stayed at 161.

**7. Any run could revise another's claim.**
- What changed: defend.py:364-366 refuses a revision from any run other than the first one's proposer_run. history is oldest first (store.py:114-117).
- Test at test:217 covers it. The failing case no longer occurs.

**8. Reviewer independence.**
- What changed: `_independent` (defend.py:488-500) requires all of the following:
  - the run is an AgentRun;
  - the run is not the proposer_run of any revision;
  - the run is not extracted_by, proposer_run or proposer of any DIRECT ground claim;
  - the role contains the substring "reviewer".
- Still open, from reading:
  - Grounds of grounds (transitive authorship) are not checked.
  - Role is free text on the AgentRun, so any role string containing "reviewer" qualifies.
  - The docstring (defend.py:52-55) states what code cannot see: the same agent under two run numbers, and one session writing both files.

**9. Sealing the brief.**
- What changed: the challenge requires --brief and stores its sha256 (defend.py:508-525). It checks only that the file CONTAINS the heading line "# Challenge brief for <id> (revision N)" (defend.py:511). The file is not compared with what `brief()` produces.
- Still occurs. Case tried: a "brief" file holding only that heading plus "mechanism: MECH proposer reasoning" was accepted. It wrote Evaluation eval:59ca7dd1b42e.
- So the stored brief hash proves which file was handed in, not that the file was the sealed brief or that it lacked the proposer's reasoning.
- Also from reading:
  - The brief prints the artifact in full (defend.py:431, 443-445). If artifact_path names a write-up that holds the mechanism, that reasoning goes into the brief. Nothing checks for this.
  - The brief prints the names of the reasoning_files.

**10. Hypothesis in the brief.**
- It is now in the brief (defend.py:436). The plan (line 56) lists "plain-language hypothesis" as a contract field, and Phase 3.1 (plan line 98) says "claim/specification + sealed admissible evidence, without ... the proponent's conclusions".
- Mechanism, alternatives, falsifiers and outcome text are left out. test:250-251 asserts their absence.
- Open: whether the hypothesis counts as the claim or as the proposer's reasoning. That reading is Greg's.

**11. Edge type of the grounds.**
- What changed: claim grounds get DERIVED_FROM (defend.py:382-383). Rule and cited grounds get SUPPORTS from their Source node (defend.py:386-387). These are the edges grounding.py:141 and 167-168 count.
- The grounding test (test:127-136) shows supporting paths for a non-inference claim and for an inference that rests on a claim.
- Stale document: BUILD_NOTES_DEFEND.md line 3 still says "tied to what it rests on (DEPENDS_ON, SUPPORTS)". The fix did not change that file (`git diff 071777f 3a6ac09 -- tools/kgraph/BUILD_NOTES_DEFEND.md` is empty).

**12. A ground with no node.**
- Every ground now either resolves to an edge or refuses the registration (defend.py:207-253), so the silent case does not occur.
- `unlinked_grounds` is always written as [] (defend.py:374) and is never filled. The "NO LINK" branch of show (defend.py:567-568) cannot be reached.

**13. Dropped grounds and the REVISES / CONTRADICTS question.**
- What changed: after a revision, defend.py:396-402 withdraws every live DERIVED_FROM out of the claim and every SUPPORTS into it that this revision did not write again. The withdrawn line keeps its old version and a reason. Test at test:225-235.
- What the code does today on REVISES / CONTRADICTS: no REVISES edge is written on a revision; revisions are store revisions of the same node id. No CONTRADICTS edge is written from an objection; objections are stored as attrs on the Evaluation.
- The docstring (defend.py:62) leaves both to Greg. Left open for Greg.

**14. Verdict-word check.**
- What changed: `_labels` (defend.py:147-160) now walks the claim file as given (all keys except claim_key; defend.py:360) and the whole challenge file (defend.py:523). It skips keys named "quote". "true", "false", "holds" and "ok" are accepted (test:331-332).
- Still occurs: ordinary English words in the list (passed, failed, rejected, approved, verdict) are refused anywhere, including file names. Cases tried:
  - falsifier "orders rejected by the exchange appear": refused.
  - scope "after the settle window passed": refused.
  - hypothesis "the runs that failed to start are logged": refused.
  - challenge what_i_opened ["out/verdict.json"]: refused ("what_i_opened[0] carries the word 'verdict'").
- test:329-330 asserts that the mechanism "the rule was rejected by the book" is refused, so the test fixes this behaviour in place.

**15. Tests.**
- The store-check test (test:335-337) now compares GraphStore.check_all() problems before and after all writes, and allows no new one.
- The refusal cases I read each match the field or ground they target.
- Not covered by any test:
  - an inference with no grounds (finding 5);
  - a brief whose content differs from brief() (finding 9);
  - a refused challenge leaving a record (finding 6);
  - a link written by another run being kept across a revision (new finding A).
- test:323-330 fixes the refusal of ordinary words (finding 14).

## New in the fix

**A. A revision withdraws links that other runs wrote into the claim.**
- Where: defend.py:398-402. The rule there is: any live SUPPORTS whose dst is the claim, or DERIVED_FROM whose src is the claim, and which this revision did not write, is withdrawn under the proposer's run. It does not check who wrote the link.
- Case tried on scratch:
  1. run:0003 wrote SUPPORTS from src:markets-data:.../paper-trading-20261123/agent-runs.jsonl to claim:reg-751bbc009e4c.
  2. run:0002 (the proposer) then registered a revision.
  3. The result reported withdrawn ['e:1469bed94842'].
- So a proposer's revision takes back evidence links another run attached to its claim. The verifier plan (line 48) says no one may rewrite source evidence; the withdrawn line keeps its old version.

**B. Registration may revise a shared Source node. Read only, not reproduced.**
- Where: `_source_at` (defend.py:182-188). When the graph's Source node for repo:path has a different sha256 from the bytes at the commit, but the checkout's current file has the same bytes, the function returns the checkout's freshly built node under the same id.
- Effect: registration writes a new revision of a Source node that other claims (extracted with their own lines) point at.
- I looked for such a Source in the current checkout: no Source node has a file that changed since the graph read it (0 found), so I could not show it happening.

**C. Refusals can still vanish.** `_retain` swallows write failures (defend.py:323-324). Challenge refusals are never retained. Both are covered under finding 6.

**D. BUILD_NOTES_DEFEND.md is stale.** It was not updated by the fix: it still says DEPENDS_ON, and does not mention Task retention, the brief file, or the role check.

## Ticket 02, against its "shown done by" line

Seen that meets it:
- One command writes a Claim node with all of these fields: hypothesis, exact claim, scope, mechanism, alternatives, falsifiers (each with observation and record), code commit (resolved and with the artifact hash checked), data manifest hashes, structured outcome visibility, the whole claim file, and proposer_run.
- One command shows it. On scratch:
  `python3 -m tools.kgraph.defend show --claim claim:reg-751bbc009e4c --data /home/user/markets-data --graph-dir /tmp/run107-scratch/graph`
  This printed exit 0 and every field above, the falsifiers of revisions 1-3 with their times, the grounds, and the challenge on record.

Seen that does not meet it:
- The data hashes are not verified against anything (finding 4).
- "Outcome not yet seen" is self-declared and not tied to a trial (finding 3).
- An inference with no grounds registers (finding 5).

Could not check: whether any real claim is registered before a real trial. No real claim or trial was involved; all writes went to the scratch graph.

## Ticket 03, against its "shown done by" line

Seen that meets it:
- `brief()` holds the exact claim, hypothesis, scope, the artifact at its commit, and the grounds in full. It leaves out the mechanism, alternatives, falsifiers and outcome text (test:238-251).
- The challenge is an Evaluation with rubric "independent challenge v1: ...", tied by EVALUATES to the claim. It needs at least one alternative, at least one falsifier and a distinguishing_observation, and stores the brief's sha256 and the reviewer run.

Seen that does not meet it:
- The brief actually handed in is not checked against the generated brief. A file that carried the proposer's mechanism was accepted (finding 9).
- The artifact is printed in full whatever it is.
- Independence rests on a free-text role and direct authorship only (finding 8).

Could not check:
- whether a real reviewer opened what it was told not to (self-reported in what_i_opened and saw_proposer_reasoning);
- whether two run numbers are the same agent.

## Checkouts after this read

- `git -C /home/user/markets-data status --short`: empty.
- `git -C /home/user/Markets status --short`: empty. HEAD is still 2ac873f.
- /tmp/run107-scratch and /tmp/pytest-of-root: deleted. Both are confirmed absent.
- Nothing was written into markets-data graph/. No engine, tape or AWS was used.

## Counts

- Tests: 40 passed, 0 failed, 0 errors, 0 skipped, in 22.03s.
- Commits read: 071777f, 3a6ac09, HEAD 2ac873f (Markets); dc51ed2 (markets-data, read only).
- Tool calls made: 13 including this handback. Well inside every limit.

## Open after this read

1. Finding 1: "Greg's words" rests on a self-declared said_by.
2. Finding 3: outcome_seen is self-declared; falsifiers can be rewritten in a revision with outcome_seen still false. The rewrite is visible in show.
3. Finding 4: data manifest sha256 is checked for format only.
4. Finding 5: an inference with empty rests_on registers.
5. Finding 6: `_retain` swallows write failures; refused challenges leave no record.
6. Finding 8: independence rests on the substring "reviewer" in a free-text role and on direct ground authorship only.
7. Finding 9: the brief handed in is not compared with the generated brief; the artifact is printed in full whatever it holds.
8. Finding 10: whether the hypothesis belongs in the brief (Greg's reading).
9. Finding 12: unlinked_grounds and the "NO LINK" output are dead code.
10. Finding 13: REVISES and CONTRADICTS edges are not written (Greg's to settle).
11. Finding 14: ordinary words (passed, failed, rejected, approved, verdict) are refused, including in file names, and a test fixes this.
12. Finding 15: no tests for findings 5, 6 (challenge side) and 9, or for new finding A.
13. New A: a proposer's revision withdraws SUPPORTS and DERIVED_FROM links written by other runs.
14. New B (read, not reproduced): registration can write a new revision of a shared Source node.
15. New D: BUILD_NOTES_DEFEND.md still says DEPENDS_ON and does not describe the fix.
