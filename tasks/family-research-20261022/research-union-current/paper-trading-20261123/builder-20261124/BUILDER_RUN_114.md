# Builder run 114 (Sonnet): its hand-back on the fix for tickets 02 and 03, Markets `68d65a6`

Kept word for word as the builder returned it, 2026-11-24 (twenty-fifth session). Nothing below this line is the main session's. The change is marked PROPOSED and is not read by the reviewer yet.

---

DONE, pushed, stopped. Commit 68d65a6 on wt-b456, pushed to ccr-659edd86-di9udt (earlier UNFINISHED commit ef55c31 on top of run 110's 9ca6a48). Subject as ordered. No go beyond this was taken.

DIFF STAT (git diff --stat 2ac873f HEAD): test_defend.py 235 lines changed, BUILD_NOTES_DEFEND.md +1, defend.py 233 changed; 3 files, 396 insertions, 73 deletions. schema.py untouched.

LAST RUN: 53 passed in 60.70s (0 failed, 0 skipped). First run at the start (run 110's state): 47 passed, 1 failed (the others-link check).

THE 13 POINTS (D = run 110 had code and check, M = made by me; defend.py line numbers are for HEAD)
1. said_by / said_by_named_in_lines: D. defend.py:261 (store), :470 _saidline (brief, show). Checks: test_who_said_a_cited_line_is_the_proposers_word_and_code_says_so; also the brief check.
2. falsifiers_changed_from_revision: D. defend.py:422-424, _falsifiers_line, show, undefended. Check: test_a_revision_that_changes_the_falsifiers_says_so_everywhere. The docstring line saying outcome_seen is a declaration the code cannot see: I did NOT verify or add it; run 110's module docstring was left as it stood.
3. data_manifest_hashes items {what,sha256,repo,path,commit}: M. defend.py:296 _manifest(d, dirs), resolves the commit in that repo, hashes the file at it, refuses naming both hashes; {"none": why} kept. Check: test_a_data_manifest_item_is_checked_against_the_file_at_its_commit (real CL01 rule file and commit).
4. Empty rests_on on an inference refused: D. defend.py:404. Check: test_an_inference_that_names_nothing_it_rests_on_is_refused.
5. No refusal vanishes: M. defend.py:324 NotRetained, :349 _retain (no swallow; raises with both reasons), register/challenge/challenge_brief wrappers (:589 for challenge-brief), main returns 3 for NotRetained and 2 for a kept refusal. Task attrs now carry verb, and claim/challenge_file/brief_file(+sha) for challenge. Checks: test_a_refused_challenge_leaves_a_task_and_no_evaluation (library and CLI, exit 2), test_a_refused_challenge_brief_leaves_a_task, test_a_refusal_that_cannot_be_written_says_both_reasons_and_exits_3 (monkeypatches GraphStore.write to fail only for Task nodes; no data made up).
6. Exact role + transitive DERIVED_FROM walk: D. defend.py:551-570. Checks: test_the_role_must_be_exactly_reviewer, test_a_reviewer_who_made_a_ground_of_a_ground_is_refused, test_who_may_challenge. Real runs 3 and 5 hold role "reviewer" exactly (the checks pass with them as reviewers). Note test_the_role_must_be_exactly_reviewer SKIPS-silently only if no real run holds a near-miss role; it did not report skipped in the last run (53 passed, none skipped).
7. Sealed brief: D (challenge compares sha256 with brief it builds, stored; artifact-in-reasoning_files refused at :393; brief says printed in full as the thing claimed about). Checks: test_the_brief_is_sealed_to_what_the_code_builds, test_an_artifact_listed_among_the_reasoning_files_is_refused.
8. Dead unlinked_grounds and NO LINK branch removed: D. Check: test_a_claim_carries_no_dead_unlinked_grounds_field.
9. Verdict words: D (six labels anywhere, any case, underscore or space; plain forms only as whole value). Check: test_verdict_labels_are_refused_and_ordinary_words_are_not. The "rule was rejected by the book" assertion now asserts it is ACCEPTED; run 110 had already moved it into this test, so I changed nothing there.
10. Revision withdraws only its own earlier registration's links: M code (defend.py:447 onward: edge must match a ground of an earlier revision AND have first been written by the proposer's run), check was run 110's and was red; I also tightened its last assertion (history of the other run's edge has one line, not withdrawn). Check: test_a_revision_leaves_standing_a_link_another_run_wrote_into_the_claim.
11. Existing Source never rewritten: M. defend.py:184 _source_at returns the existing node unrevised whatever its sha256; commit and sha256 are stored on the ground (already) and now on the SUPPORTS edge (link attrs). Condition brought about on the scratch graph with a real file: the graph's Source src:Markets:.claude/agents/scout.md has a sha256 differing from the committed file; the check asserts that precondition, cites line 8 of it, and shows the Source history unchanged (it was red before: rev 2 was written). Check: test_registration_never_writes_a_new_revision_of_an_existing_source. A real consequence: the same fix covers CLAUDE.md, exp_dag.py and others whose graph Source is stale.
12. Checks for 4, 5 (challenge side and failed retention), 7, 10: all present as named above.
13. BUILD_NOTES_DEFEND.md: one dated line added (DERIVED_FROM and SUPPORTS, Task retention, sealed brief, exact role, etc.); earlier lines untouched; file now 5 lines.

EXISTING CHECKS CHANGED: none loosened. I changed run 110's own new others-link check (last assertion simplified). Check test_a_refused_registration_leaves_a_task_and_no_claim still passes unchanged (Task attrs keep claim_file and the fields it reads).

AMBIGUITIES / NOT DONE: (a) "written by the proposer's run through register" is read as: the edge matches a ground of an earlier revision and its first line was written by the proposer's run; a link the proposer wrote by other means to the same grounds would also count. (b) challenge-brief takes an optional --run so a refusal can be stamped; with none, the writer is code_stamp. (c) Refusals of challenge-brief and challenge are retained even when the claim id does not exist. (d) REVISES/CONTRADICTS not built, docstring line left. (e) The "outcome_seen is a declaration" docstring wording (point 2) not separately checked or added.

HOUSEKEEPING: /tmp/run114 and /tmp/pytest-of-root deleted after each run; `git -C /home/user/markets-data status --short` is empty; nothing written to markets-data graph/; no engine, tape or AWS. Tool calls: about 24 (Bash, Read, Edit, Write combined; the advisor tool was not used).
