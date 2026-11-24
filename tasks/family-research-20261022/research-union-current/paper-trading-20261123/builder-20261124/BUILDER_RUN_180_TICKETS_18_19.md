# Builder run 180 (Sonnet): tickets 18 and 19, the reviewer's ten points

Everything below this line is the agent's own report, word for word; nothing below it is the main session's.

## Hand-back 1 of 1

# Builder run 180 (Sonnet): tickets 18 and 19, the reviewer's ten points

I made no edits and no commits. Run 166's two commits already hold nine of the ten points. Point 10 is only half held, because its two named checks are skipped here. `git status --porcelain` is empty. 344e3e6 and d7a44f7 are both on `origin/ccr-144315dd-pta2ze`. My working copy (/home/user/wt/b166) is one commit behind that branch (the other side of the merge), and none of my work is missing from it.

For each point I changed the one line of code, ran the check, saw it fail, then ran `git checkout -- <file>`. The checks are in /home/user/wt/b166/tests/agent_program/test_run_plan.py and test_run_record.py.

**Ticket 18** (all from commit 344e3e6, tools/kgraph/run_plan.py)
1. `test_a_plan_file_given_with_plan_that_does_not_exist_is_refused_with_its_name` holds the `raise Refused(f"the plan file {a.plan} does not exist")` line in `_check`. It asserts exit 2, the file name and "does not exist" in stderr, and no "limits were not written" sentence anywhere. Replacing the raise with `pass` made it fail. The docstring now says so.
2. `test_two_commits_that_add_the_plan_the_earliest_is_the_add` holds `h, when = min(rows, ...)` in `_git_state`. It uses a real side-branch repository plus a `--no-ff` merge, and asserts git lists two adds. Changing `min` to `max` made it fail. This line was not in run 166's diff, so the check is new and the code was already right.
3. `test_a_plan_staged_and_never_committed_is_tracked_without_an_add` holds the sentence "the file is in the index and no commit has added it", exit 1. Restoring the old sentence made it fail.
4. `test_a_shallow_clone_says_the_add_time_is_not_measured_and_is_exit_3` and `test_a_grafted_history_says_the_add_time_is_not_measured_and_is_exit_3` hold `_history_cut`, the `if cut:` branch, and `return 3 if order_unmeasured else 0`. The shallow case is a real `git clone --depth 1`. Both also check that an edited plan gives exit 1 instead. Putting back `if cut:` as `if False:` made the first fail. Putting back `return 0` made the shallow, grafted and date-only checks fail. I did not isolate the shallow and grafted branches inside `_history_cut` from each other.
5. `test_a_started_at_that_is_a_date_with_no_time_is_not_measured_and_is_exit_3` holds the `elif no_time:` branch and the date regex in `_start`. Putting back `elif False:` made it fail.
6. The header of the separated section in test_run_plan.py now names other.txt, main.txt, the scratch copy of run-0128.json, and the scratch repositories. I read this one. Code cannot hold a comment.

**Ticket 19** (commit d7a44f7, tools/kgraph/run_record.py)
7. `test_trap_a_line_whose_model_replies_differs_from_its_kept_transcript_is_named` holds the `elif mine != theirs:` branch in `_differences`, which produces "model_replies: line 11, transcript 10". The case is run 154's real line with model_replies raised from 10 to 11, and it first asserts the unchanged line names no difference. Replacing the branch with `elif False:` made it fail. There is a second place with the same text; I changed only the one in `_differences`.
8. Three checks, each failing alone:
   - `test_trap_the_same_bytes_under_another_run_are_refused_on_the_sha_alone` holds the sha refusal `d.get("sha256") == f["_sha256"]`. The sha refusal is reachable only with a sidecar `keep` itself would never write. `_tie` always takes an agent id and `keep` writes it into the sidecar. The same bytes carry the same agent id, so the sidecar agent-id refusal at run_record.py:196-197 fires first. The check therefore removes agent_id from the real run 157 sidecar, and its comment says so.
   - `test_the_same_agent_id_under_another_run_is_refused_on_its_kept_sidecar_alone` holds `if d.get("agent_id") == agent_id:` (lines 196-197).
   - `test_trap_the_same_agent_id_under_another_run_is_refused_on_its_line_alone` holds `line.get("agent_id") == agent_id` (lines 187-188).
   Putting back each of the three lines made its own check fail.
9. `test_agent_type_and_outside_roster_together_are_refused_whatever_their_values` holds `if a.outside_roster is not None and a.agent_type is not None:`. It tries equal values, differing values and a made-up word. `test_an_empty_outside_roster_is_refused_with_what_it_needs` holds the `not a.outside_roster.strip()` line, with "" and "  ". Putting back each line made its check fail.
10. Half held.
    - `test_missing_with_live_counts_on_the_record_as_it_was_at_7de89a4` no longer has the written-in zeros. It computes the run-naming count from each kept sidecar's `tie_note` and the not-kept count by hashing the files, in the test and not through the code.
    - It is among the 15 skipped checks because the earlier machine's live transcripts are not here. I could not run it, so I did not see it hold.
    - The refusing side was added to the run 108 check, which is also skipped here. I could not run that edit either.
    - The new, un-skipped `test_run_108s_kept_transcript_is_accepted_and_run_107s_offered_as_108_is_refused` holds the refusing side at the `run {run}'s line holds model` refusal, run_record.py:214. Replacing the raise with `pass` made it fail.

**Counts**
- Before run 166: test_run_plan.py 26 passed; test_run_record.py 19 passed, 41 skipped.
- First thing now: 57 passed, 15 skipped across both files.
- After my last change (none made): test_run_plan.py 32 passed; test_run_record.py 25 passed, 15 skipped.
- All 15 skips are "live transcript or folder is not on this machine".

**Open**
- Point 10's two skipped checks have not run on this machine. Someone should run them where the live transcripts are.
- Checks that depend on the real markets-data checkout accept exit 3 if it is itself shallow. I did not test that case.

**What code cannot hold:** the header text of point 6, and the fact that the sha refusal is unreachable for sidecars `keep` writes (point 8).

**Tool calls:** 8 of 40. Sub-agents: 0. Writes into the real graph: 0. Nothing was written into /home/user/markets-data, and the scratch folder was deleted after every run.
