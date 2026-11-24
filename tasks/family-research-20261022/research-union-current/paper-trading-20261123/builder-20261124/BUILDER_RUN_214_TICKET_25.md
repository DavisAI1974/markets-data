# Builder run 214 (Sonnet): ticket 25, run 196 carried on; stopped after point 2

Everything below this line is the agent's own report, word for word; nothing below it is the main session's.

## Hand-back 1 of 1

# Builder run 214 (Sonnet): ticket 25, the points of the second read (run 196 carried on)

Stopped after point 2 because of a check that fails for a reason in the record. Points 3 and 4 are not started.

**Counts**
- First run, with point 2's edits in the working copy: 27 passed, 1 failed (28 checks, 308 s).
- The failure is not the one run 196 was given. The main-session check now passes. The one failing is `test_authoring_run_from_a_field_in_the_real_record`, at `tests/agent_program/test_ingest_artifacts.py:158`.
- Its words: `assert got["authoring_run"] == "run:0119" and got["authoring_basis"].startswith("field")` gives run 0119 correctly, but the basis is "outcome text of a builder: read from the run's outcome text, not from a field".
- After my last change: I did not re-run the file after committing, so the counts are still 27 and 1. Point 2 added no new check names; it only changed the two existing checks.

**Why that check fails (the record, not my files)**
- The check's comment says run 119's newest line lists data_commits 11fe552 and 9079b22. That is no longer true.
- agent-runs.jsonl line 125 is run 119's old line and does carry `data_commits ['11fe552','9079b22']`.
- Line 261 is a correcting line for run 119 (`corrects`, started 2026-11-24T13:23:23Z). It was added by markets-data 090116cc, "correcting lines for runs 107 to 121". It has no `data_commits`, and its outcome text names 11fe552 and 9079b22.
- The newest line of a run stands, so authorship falls to step (b), the builder's outcome text. The answer, run 0119, is the same. Only the basis differs.
- At b0c1f81 run 119 had one line with the field. At 65baee9c and HEAD it has two, and the newest has none.
- I did not loosen or change the check. A fix needs a decision from you or the main session. Either pick another run whose newest line still carries the field, or have the check expect the outcome-text basis for run 119 and use a different run for the field case.

**Points**
1. Run 196's commit is 3f03d0e, already on GitHub. The whole file runs with it at 27 clean and 1 failing. The failing one is the check above, not the main-session check.
   - Check: `test_the_main_sessions_commits_and_those_outside_the_runs_hold_against_git`, which now passes.
2. Check: `test_current_versions_block_is_held_to_a_tenth_and_says_what_it_cut`.
   - Lines changed: `tools/kgraph/ingest_artifacts.py` +6. Where the lines that are never cut exceed a tenth of the budget, the block adds one line saying the branch lines are kept whole and take more than their share, with the two figures: characters taken and characters allowed.
   - `tests/agent_program/test_ingest_artifacts.py` +19 −2: the new helper `_held_to_a_tenth_or_says_it_is_not`, used by the 1,000-token check and by the held-to-a-tenth check, which now runs budgets 1,000, 1,500, 1,800, 2,000, 2,300, 2,500 and 3,000.
   - Both checks passed in the full run.
   - Commit: 11cc642, merged and pushed to ccr-144315dd-pta2ze as 09bcffe. The merge brought in 13 files from others, and I did not re-run after it.
3. The line that counts the block (context.py:456): not started.
4. The checks for put-backs (c) and (f): not started.

**Open**
- The failing check above, which needs your word.
- Points 3 and 4.
- The check file has not been re-run since the merge at 09bcffe.

**Tool calls:** 7 of 50 (including the Read of the brief). No sub-agents. The scratch folder /home/user/tmp-pytest/b214 is deleted. markets-data is unchanged.
