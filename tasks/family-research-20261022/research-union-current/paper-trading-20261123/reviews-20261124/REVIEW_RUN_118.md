# Reviewer run 118 (Opus): the third read of tickets 02 and 03, Markets `68d65a6`

Kept word for word as the reviewer returned it, 2026-11-24 (twenty-fifth session). Nothing below this line is the main session's. What the main session did with each open point is in `../tickets-44-20261124/02.md` and `03.md`.

---

REVIEWER RUN 118: third read of tools/kgraph/defend.py, tickets 02 and 03

Read: Markets branch ccr-659edd86-di9udt, head 68d65a6. `git log --oneline -3` gives 68d65a6, ef55c31, 9ca6a48 on top of 2ac873f. I read the diff `git diff 2ac873f 68d65a6` of defend.py, test_defend.py and BUILD_NOTES_DEFEND.md, the "Open after this read" list of REVIEW_RUN_107.md (lines 186-202), and BUILDER_RUN_114.md. Line numbers below are for defend.py at 68d65a6 unless another file is named.

## Checks run

- At 68d65a6, in /home/user/Markets: `53 passed in 60.69s`. No failures, no skips, no error text.
- Reverting the fix:
  - Setup: a `git clone --shared` into /tmp/run118, checked out at 68d65a6, with defend.py put back to its 2ac873f text and the test file left at 68d65a6. I symlinked the sibling checkouts in.
  - Result: `16 failed, 37 passed`. The 16 that went red are every new or changed check:
    - the_brief_holds_the_claim...
    - who_said_a_cited_line...
    - verdict_labels...
    - reviewer_who_made_a_ground_of_a_ground
    - the_role_must_be_exactly_reviewer
    - the_brief_is_sealed
    - artifact_listed_among_the_reasoning_files
    - revision_that_changes_the_falsifiers
    - revision_leaves_standing_a_link_another_run_wrote
    - data_manifest_item_is_checked
    - refused_challenge_leaves_a_task
    - refused_challenge_brief_leaves_a_task
    - refusal_that_cannot_be_written...exits_3
    - registration_never_writes_a_new_revision_of_an_existing_source
    - inference_that_names_nothing
    - claim_carries_no_dead_unlinked_grounds_field
  - Limits: this reverts the whole file at once, not each fix singly, and I did not read why each check went red.
  - The same clone with the 68d65a6 code: 53 passed.
  - Two earlier runs of that clone without the sibling symlinks gave 40 failed. That was my harness: "artifact_repo ... with a local checkout" was refused. It was not the code, and those counts are not used here.

## The 15 points of run 107

Tried means tried on a scratch copy of the real graph at /tmp/run118/graph, through `defend.main` with `--data /home/user/markets-data --graph-dir /tmp/run118/graph`.

**1. said_by**
- What the code does now:
  - :470-474 `_saidline` prints "said by X as the proposer states; code does not check who said it", the commit and the sha256, and "The said_by name appears in the cited lines: true|false".
  - :258 computes that flag as a plain substring: `said.lower() in "\n".join(lines).lower()`.
- Tried: a cited ground with `said_by: "e"` on .claude/agents/scout.md line 8 stored `said_by_named_in_lines: true`. Any one letter that occurs in the line gives true.
- The check, test_who_said_a_cited_line_is_the_proposers_word_and_code_says_so, went red on the old code.
- Open:
  - Who said the line (what code cannot hold).
  - The substring test, which says true for a single letter (for the builder).

**2. outcome_seen and falsifiers**
- What the code does now:
  - :418-424 sets `falsifiers_changed_from_revision` by comparing only with revision n-1.
  - It carries the flag over only when the same file is registered again.
- Tried:
  - rev1 F1, rev2 F2, rev3 F2 with only the scope changed.
  - After rev3 the attribute is absent.
  - `undefended` prints `claim:reg-e217699b2597  revision 3  E about rule CL01` with no mark.
  - brief and show read the same attribute (:503, :661), so neither says it either.
  - show still lists every revision's falsifiers.
  - test_a_revision_that_changes_the_falsifiers_says_so_everywhere asserts this disappearance (its last line).
- outcome_seen is still the proposer's declaration. The "What code CANNOT see" paragraph (:56-57) does not name it; the builder says it did not add that.
- Open:
  - Whether a later revision's brief should still say that the falsifiers were changed after revision 1 (Greg's to settle).
  - outcome_seen being self-declared (what code cannot hold, to be said in the ticket).

**3. Data manifest**
- What the code does now: :296-320 resolves the commit in the named checkout and hashes the file at that commit. Bad sha, commit, path and repo are all refused, and the check went red on the old code.
- Tried: an item with `"commit": "HEAD"` registered, and was stored as `'commit': 'HEAD'` (:320 returns the items as given). The registration pins nothing; `code_commit` by contrast is stored resolved to the full sha.
- As read from the diff, an item must be a file committed in a local checkout. Data kept only in S3 (MANIFEST.json for data) can only enter as `{"none": ...}`, and its bytes are not checked.
- Open:
  - Storing the resolved commit (for the builder).
  - S3 bytes with AWS unavailable (what code cannot hold, to be said in the ticket).

**4. Inference with empty rests_on**
- What the code does now: :403 refuses it.
- The check test_an_inference_that_names_nothing_it_rests_on_is_refused went red on the old code.
- Nothing further found.

**5. Refusals kept**
- What the code does now:
  - :349-361 `_retain` no longer swallows a failed write. It raises `NotRetained` with both reasons, and `main` returns 3 (:726).
  - The `challenge` and `challenge_brief` wrappers are at :574 and :589.
- Tried:
  - A `--brief` path that does not exist gives rc 2 and a Task is kept. The message read "the brief file the reviewer was given is required (--brief)" although a path was given.
  - A non-JSON challenge file gives rc 2 and a Task is kept.
  - `challenge-brief` on `claim:nope` with no `--run` gives rc 2 and a Task written_by `code:tools.kgraph.defend@68d65a694a` with attr `run` = str(None).
- The monkeypatch check:
  - It replaces `GraphStore.write` with a function that raises only when a Task node is in the batch.
  - It writes no data and makes up no record; only the write path is faked.
  - It asserts exit 3, both reasons in stderr, and no Task added. It went red on the old code (which exited 2).
- Open:
  - (b) and (c): any typed id, with or without a run, leaves a Task node in the graph (Greg's to settle).
  - The misleading message when the brief file is missing (for the builder).

**6. Independence**
- What the code does now:
  - :555-571 walks DERIVED_FROM over grounds of grounds.
  - :570 requires the role to be exactly "reviewer" after trim and lower-case.
- Read in the scratch graph: ten real reviewer runs, run:0054 to run:0063, hold the role `'reviewer (read-only)'`. They are now refused as challengers. test_the_role_must_be_exactly_reviewer uses the first of them as its refused case.
- The walk follows DERIVED_FROM only. Who wrote a cited file or a rule (the SUPPORTS side) is not walked.
- The grounds-of-grounds check went red on the old code.
- Open:
  - Whether "reviewer (read-only)" may challenge (Greg's to settle).
  - Authorship of cited files, and the same agent under two run numbers (what code cannot hold).

**7. Sealed brief**
- What the code does now:
  - :606-612 builds the brief and compares sha256.
  - :392 refuses the artifact listed among the reasoning files.
  - The brief labels the artifact "printed in full as the thing claimed about".
- Both checks went red on the old code. The forged and padded briefs would have passed the old header test.
- Open: an artifact that itself holds reasoning (what code cannot hold).

**8. Hypothesis in the brief**: settled by Greg; not read further.

**9. Dead code**
- unlinked_grounds and "NO LINK" are gone from the diff.
- The check asserts that they are absent, and went red on the old code.

**10. REVISES and CONTRADICTS**
- Settled for the next round.
- The docstring at :66 still says "Not settled here ... goes to Greg", which is stale wording (for the builder).

**11. Verdict words**
- What the code does now:
  - :89-93 and :157: the six labels are refused anywhere, with "_" read as "[_ ]".
  - The plain forms are refused only as a whole value.
- Tried with `_labels` directly:
  - Accepted: 'supported-within-scope', 'Supported  within scope' (two spaces), 'the check passed', 'the canary failed', ' Passed. ', 'PASS: yes'.
  - Refused: 'the tape is inconclusive at 1-sec'.
- The brief itself tells the reviewer "no pass or fail framing". The check asserts that "the check passed" and "it failed" are accepted.
- Open: which side of this line holds (Greg's to settle). The hyphen and double-space variants (for the builder).

**12. Missing checks**
- Checks now exist for points 4, 5 (challenge side and the failed write), 7 and A, and all went red on the old code.
- Their reach:
  - The others-link check uses an edge id that was never a ground. It does not exercise the `written_by == run` clause at :454.
  - The exact-role check depends on near-miss roles being present in the real graph; it skips otherwise.
  - The Source check depends on the real drift between the graph's scout.md Source and the committed file. It asserts that drift as a precondition, so it fails if the graph catches up.

**13. New A, links of other runs (builder's reading (a))**
- What the code does now: :447-456.
- Tried:
  1. run:0003 wrote SUPPORTS scout.md -> claim.
  2. The proposer's rev2 added scout.md as a ground. That rewrote run:0003's edge: its history shows rev 1 by run:0003 with `{}`, then rev 2 by run:0002 with commit b134dc4... and sha256 0620db6....
  3. The proposer's rev3 dropped that ground. The edge stands live, carrying the proposer's commit and sha256, although rests_on no longer names scout.md (`history[0].written_by` is run:0003).
- Open (for the builder; whether a proposer may write a revision of another run's link is Greg's to settle).

**14. New B, Source nodes (builder's reading (e))**
- What the code does now: :184-191 never revises an existing Source.
- Tried, registering a cited ground on scout.md:
  - The Source node keeps sha256 c83b3a53... at commit a494363....
  - The ground and the SUPPORTS edge (:434) carry sha256 0620db6c... at commit b134dc4....
  - So the Source the ground points at holds the hash of other bytes than the quote was checked against.
- Where the difference is and is not said:
  - The claim's top-level attrs (:440) carry source and lines but no commit and no sha256.
  - No line of `show` says that the two hashes differ; show prints only the ground's hash.
  - grounding._quote_now (grounding.py:90-126) reads the checkout's current file, not either hash.
- Open (for the builder).

**15. BUILD_NOTES**
- A line was added that names DERIVED_FROM and SUPPORTS.
- The earlier line 3 still says DEPENDS_ON, contradicted by the new line (residual; for the builder).

## Against the two tickets

**Ticket 02**
- Observed:
  - A claim node with hypothesis, exact claim, scope, mechanism, alternatives, falsifiers, the resolved code commit, artifact sha256, data-manifest hashes and outcome_visibility, written before any challenge.
  - One command shows it: `python3 -m tools.kgraph.defend show --claim claim:reg-5f683ef0eb03 --data /home/user/markets-data --graph-dir /tmp/run118/graph` gave rc 0 and printed the fields, every revision's falsifiers and the grounds.
- Not met as written:
  - "outcome not yet seen" is the proposer's declaration.
  - "falsifiers written beforehand" is shown per revision, but the change mark is lost at the next revision (point 2).
  - The manifest commit can be stored as "HEAD" (point 3).
- Not checked: data held outside git.

**Ticket 03**
- Observed:
  - The brief from `challenge-brief` (run:0003) held the hypothesis, and none of the strings MECH-XYZ, ALT-XYZ, FALS-XYZ.
  - The challenge by run:0003 gave rc 0. It wrote Evaluation eval:614cb2adc5eb, with rubric "independent challenge v1: a reviewer who was not given the proposer's reasoning gives at least one competing explanation, one falsifier and the observation that distinguishes them", and an EVALUATES edge to the claim.
- Not met as written:
  - The exact-role refusal of real "reviewer (read-only)" runs (point 6).
- Not checked: whether a reviewer actually opened the reasoning files; that is the reviewer's own statement.

## Speculation (labelled)

The precondition of test_registration_never_writes_a_new_revision_of_an_existing_source may stop holding after any later graph extraction that revises the scout.md Source. The check would then go red for a reason unrelated to the code.

## Exact counts and commits

- At 68d65a6: 53 passed, 0 failed, 0 skipped (60.69s).
- With defend.py at 2ac873f: 16 failed, 37 passed.
- Commits read: 9ca6a48, ef55c31, 68d65a6 (as a diff from 2ac873f).

## Open after this read

1. Point 1: who said a cited line (what code cannot hold, to be said in the ticket). The substring flag that is true for a single letter (for the builder).
2. Point 2: the falsifier-change mark lost at a later revision (Greg's to settle). outcome_seen self-declared and not named in the docstring's "cannot see" list (what code cannot hold, to be said in the ticket).
3. Point 3: the manifest commit stored unresolved, e.g. "HEAD" (for the builder). S3-held data bytes are not checkable with AWS unavailable (what code cannot hold, to be said in the ticket).
4. Point 5: Tasks written for any id and with no run, i.e. (b) and (c) (Greg's to settle). The "required (--brief)" message when the file is given but missing (for the builder).
5. Point 6: real runs run:0054 to run:0063 with role "reviewer (read-only)" are refused (Greg's to settle). Authorship of cited files, and one agent under two run numbers (what code cannot hold, to be said in the ticket).
6. Point 7: an artifact that itself carries reasoning (what code cannot hold, to be said in the ticket).
7. Point 10: the stale docstring wording at :66 (for the builder).
8. Point 11: "the check passed" and "it failed" are accepted (Greg's to settle). The hyphen and double-space label variants are accepted (for the builder).
9. Point 12: the others-link check does not exercise :454's `written_by == run` clause (for the builder).
10. Point 13 / reading (a): another run's link stands live, with the proposer's attrs, after the proposer dropped that ground; the proposer's registration revised another run's edge (for the builder; Greg's to settle whether a proposer may revise another run's link).
11. Point 14 / reading (e): the Source sha256 differs from the ground's and the edge's, the claim's top-level source carries no commit or sha256, and no output says they differ (for the builder).
12. Point 15: BUILD_NOTES line 3 still says DEPENDS_ON (for the builder).

## Housekeeping

- /tmp/run118 and /tmp/pytest-of-root are deleted. My two scratch scripts in the session scratchpad (try118.py, t03.py) are deleted.
- `git -C /home/user/markets-data status --short` and `git -C /home/user/Markets status --short` both printed nothing.
- Nothing was written to markets-data `graph/`. No engine, tape or AWS was touched.

Tool calls: 15 Bash, 1 advisor, and this SubagentHandback, 17 in all.
