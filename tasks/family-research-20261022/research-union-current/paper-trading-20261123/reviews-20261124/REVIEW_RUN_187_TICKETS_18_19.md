# Reviewer run 187 (Opus): tickets 18 and 19, the read of builder run 166's ten points

Everything below this line is the agent's own report, word for word; nothing below it is the main session's.

## Hand-back 1 of 1

# Reviewer run 187 (Opus): tickets 18 and 19, the read of builder run 166's ten points

Working copy /home/user/wt/r187 at 20c13a1. `git diff --stat d7a44f7 HEAD` on the four files is empty, so what I read here is the change. MARKETS_DATA=/home/user/markets-data, which is a shallow clone (`rev-parse --is-shallow-repository` = true, 7 boundary commits in .git/shallow).

## 1. The checks (full run, then `-v` on test_run_record.py)

- tests/agent_program/test_run_plan.py: 32 collected, 32 run, 0 skipped, 0 failing.
- tests/agent_program/test_run_record.py: 40 collected, 25 run, 15 skipped, 0 failing.
- All 15 skips are in test_run_record.py. Each says the live transcript or live folder (/root/.claude/projects/-home-user/3356516d-.../subagents/...) "is not on this machine". The ones skipped at :33 are a374a5827c8bc7cc6 x7, a7418ae8600f3ea3d x3, adb1142ab9df65719, a90a42cc900cc13e5 and a961b9f58c36234ce. Two more are skipped at :40 (the live folder). By name: test_a_brief_that_names_a_later_run_is_still_its_own_run, test_report_keeps_both_hand_backs_of_run_121, test_report_adds_the_message_run_124_hand_back_points_at, test_report_of_a_stopped_run_with_no_hand_back_and_no_text_says_so, test_missing_names_a_live_transcript_that_names_no_run_and_two_that_name_one, test_a_brief_that_names_no_run_is_tied_by_the_agent_id_alone, test_one_transcript_is_one_runs_not_two, test_a_transcript_that_is_run_108s_own_agrees_with_its_line_and_run_107s_does_not, test_outside_the_roster_the_agent_type_is_the_text_given, test_trap_a_sentence_naming_another_run_in_front_of_the_brief, test_trap_a_long_sentence_in_front_of_run_119s_brief_is_tied_only_by_the_agent_id, test_trap_a_run_whose_line_holds_another_agent_id_refuses_this_one, test_trap_a_line_already_on_record_is_compared_with_the_transcript, test_trap_the_pointed_at_message_is_the_last_one_not_the_longest, test_trap_a_short_text_inside_the_hand_backs_own_message_does_not_displace_the_real_one.
- Against the builder's account:
  - **test_missing_with_live_counts_on_the_record_as_it_was_at_7de89a4 (test_run_record.py:309) is NOT skipped. It runs here.** Builder run 180 said it was skipped and that it had not seen it hold. Of point 10's two checks, only the run 108 check (:421) is skipped.
  - Builder run 180's "before" count for test_run_record.py ("19 passed, 41 skipped") does not reconcile with 40 collected now minus 7 added.

## 2. Put-backs I repeated myself (one line each; `git checkout -- .` after each, `git status --porcelain` = 0 every time)

- P1, run_plan.py:278 `raise Refused(... does not exist)` replaced with `pass`: test_a_plan_file_given_with_plan_that_does_not_exist_is_refused_with_its_name (test_run_plan.py:449) fails.
- P2, run_plan.py:256 `min(rows` replaced with `max(rows`: test_two_commits_that_add_the_plan_the_earliest_is_the_add (:459) fails.
- P3, run_plan.py:359 sentence set back to the old "tracked, and the commit that added it could not be found": test_a_plan_staged_and_never_committed_is_tracked_without_an_add (:481) fails.
- P4, graft branch only removed (the `refs/replace or info/grafts` condition in `_history_cut`, :263ff, set to `if False:`): the grafted test (:520) fails and the shallow test (:502) still holds.
- P4, shallow branch only removed (`== "true"` changed to `== "never"`): the shallow test fails and the grafted test still holds. So the two branches are told apart.
- P4/P5, run_plan.py:386 `return 3 if order_unmeasured else 0` replaced with `return 0`: the shallow, grafted and date-only tests all fail.
- P5, run_plan.py:373 `elif no_time:` replaced with `elif False:`: the date-only test (:531) fails. The regex at :402 set to `if False:`: the same test fails.
- P7, run_record.py:364 (the branch inside `_differences` at :356; the same text appears twice in the file) set to `elif False:`: test_trap_a_line_whose_model_replies_differs_from_its_kept_transcript_is_named (test_run_record.py:729) fails.
- P8, sha refusal (run_record.py:198) set to `if False:`: only test_trap_the_same_bytes_under_another_run_are_refused_on_the_sha_alone (:693) fails.
- P8, sidecar agent-id refusal (:196) set to `if False:`: only test_the_same_agent_id_under_another_run_is_refused_on_its_kept_sidecar_alone (:707) fails.
- P8, line agent-id refusal (:187) set to `if False:`: only test_trap_the_same_agent_id_under_another_run_is_refused_on_its_line_alone (:717) fails.
- P9, run_record.py:235 (both options given) set to `if False:`: test_agent_type_and_outside_roster_together_are_refused_whatever_their_values (:463) fails.
- P9, run_record.py:237 (empty value) set to `if False:`: test_an_empty_outside_roster_is_refused_with_what_it_needs (:473) fails.
- P9, accept side: both options are argparse defaults None (run_record.py:490), so the `is not None` tests read as intended. The check that `--outside-roster X` alone is still accepted (test_outside_the_roster_the_agent_type_is_the_text_given) is among the skipped ones, so the accept side is not run here.
- P10, the refusal in the 108 check (`run {run}'s line holds model` raise replaced with `pass`): test_run_108s_kept_transcript_is_accepted_and_run_107s_offered_as_108_is_refused (:448) fails.
- P10, the live-counts zeros: I put literal `0` into the code's counts line in place of `{len(unnamed)}` and `{len(live_not_kept)}` (run_record.py:476-477). **test_missing_with_live_counts... (:309) still holds.** See item 4.

## 3. Can exit 3 hide a real exit 1? (scratch repositories built from run 117's real plan, line and transcript; each case changes one named thing)

- Plan of run 117 committed at 14:00, AFTER the run began at 13:10:23.61; then one more commit at 14:30.
  - Full history: "git order: committed 2026-11-24T14:00:00+00:00 AFTER the run began 2026-11-24T13:10:23.610000+00:00", rc=1.
  - Shallow clone at `--depth 1`, history shows only the 14:30 commit: "git order: not measured: the history of ... is shallow ...", rc=3. Here the add time really is unknown.
  - **Shallow clone at `--depth 3`, history 14:30 / 14:00 plan / 13:00 base (the base is the boundary): "not measured ... is shallow", rc=3.** The add commit is visible with its real parent, so the late plan could be measured, and it reads as exit 3 instead of exit 1. Cause: run_plan.py:351 `cut = _history_cut(root)` is decided for the whole repository, and :369 `if cut:` comes before any comparison. Nothing checks whether the add commit is itself a boundary commit.
- **The same holds on the real record.**
  - Run 185's plan was added at ec7af4b, 2026-11-24T17:46:24, parent 27502f5. Run 166's was added at e60eeaa, 17:33:37, parent d70527a.
  - Neither parent is in /home/user/markets-data/.git/shallow, so both adds sit inside the visible history.
  - Their lines' started_at are 17:48:19.363Z (185) and 17:36:20.097Z (166), so both orders can be measured. Both runs print "not measured ... shallow", rc=3.
  - The test helper `_real_rc()` (test_run_plan.py:27) accepts that 3. As a result the "before the run began" sentence on the real record is never run on this machine.
- Date-only start ("2026-11-24"), plan committed at 13:08:54, then the plan file edited (max_tool_calls 999) and not committed: "plan in git: the plan was changed after it was written ...", the date-only "not measured" sentence, rc=1. Exit 1 wins.
- Grafted history, then plan edited the same way: "changed after it was written", "not measured ... is grafted", rc=1. Exit 1 wins. The grafted test (:520) does not check this. Builder run 180 said "Both also check that an edited plan gives exit 1"; only the shallow test does (:515-517).
- **Date-only start "2026-11-24" with the plan committed 2026-11-25T09:00 (a later date, so after any time on 2026-11-24): "not measured: ... a date with no time of day (2026-11-24) ...", rc=3.** A plan that is certainly late reads as exit 3. Cause: run_plan.py:373 `elif no_time:` decides "not measured" without comparing the add time with the end of the named date.

## 4. Point 10, read and measured

- The test computes none_n (:333) from each sidecar's `tie_note` at 7de89a4. `tie_note` is the code's own output, written at keep time: `_tie` returns NO_RUN_NOTE (run_record.py:158, :200) when its brief reading finds no run, and `keep` stores it (:345-346). That is the code's own brief reading under another name.
- Measured: the 18 sidecars at 7de89a4 (runs 109 to 135) all have tie_note false, so none_n = 0.
- not_kept (:334) hashes each kept .gz and looks the hash up among the sidecar `sha256` values. That route differs from the code's (run_record.py:462 compares run numbers with kept file names). But the check's live folder is made only of copies of the kept files, so not_kept = 0 by construction.
- Measured: with literal zeros written into the code's counts line, the check still holds. The two figures are still zeros that no route in this setup can make other than zero.
- Speculation, not measured: the two routes would diverge only for an unnamed live file that is not kept. The code's live_not_kept counts named runs only.
- The run 108 check (:421) now asserts the refusing side (:426-428), but it is skipped here. I read it and did not run it. The new unskipped :448 holds the refusal at the model check (I saw it fail on a put-back).

## 5. Both tools on the real record (read-only; `git status --porcelain` in markets-data = 0 before and after)

- `run_plan check --run 185`:
  - Limits: model_calls 9/50, tool_calls 11/45, tokens 91671/350000, wall 165.9/1800, sub_agents 0/0, graph_writes 0/0. Two of 8 limits cannot be measured.
  - "plan in git: unchanged since it was added (sha256 a9d74627...)"
  - "git order: not measured: the history of /home/user/markets-data is shallow ...", rc=3. Item 3 shows that this order is measurable.
- `--run 166`:
  - Limits: model_calls 17/60, tool_calls 19/60, wall 460.1/2400.
  - max_tokens "cannot be measured here (no harness total on the run's line: this limit cannot be shown kept)". Three of 8 cannot be measured.
  - Plan unchanged; same shallow "not measured", rc=3.
  - The run was stopped by the user's stop. Its single line's outcome reads "stopped by his stop before it handed back; it had committed ... 344e3e6 ... d7a44f7 ...; no report; started again as a new run (run 180)".
  - `missing` lists "run 166 | lacks: nothing | kept transcript exists".
  - Nothing in either output calls the stopped run anything other than what its line says.
- `run_record missing | tail -3`, rc=0:
  - "DIFFERS run 120 | model_replies: the line holds none, transcript 5"
  - "DIFFERS run 121 | model_replies: the line holds none, transcript 16"
  - COUNTS: runs 181; with a kept transcript 75; lacking something 107; complete and agreeing 59; a figure differs 15; plan or kept transcript with no line 8; live transcripts 0; figures that differ 15.
  - The NO LINE lines include 181, 183, 184, 187 (this run), 190, 191, 192.
  - I saw no verdict words in any of these outputs.

## 6. Standing rules in the new checks

- test_run_plan.py:449 (missing --plan) has no `# change:` comment. Its case is a path that does not exist, not a changed real line.
- test_run_plan.py:502 (shallow): the `# change:` comment names only the shallow clone. The later edit (max_tool_calls = 999, :515) has only an inline comment.
- test_run_record.py:729 (model_replies) says "nothing else is touched". The real record holds 2 lines for run 154. The rewrite drops every run-154 line and writes back only the edited newest one, so the older run-154 line is also removed.
- test_run_record.py:717 (run 116): the record holds 2 run-116 lines. The older one is kept and the edited newest is moved to the end. That matches its comment as far as content goes.
- test_run_record.py:463 and :473 change command-line arguments only and have no `# change:` comment.
- Point 6 header (test_run_plan.py:233ff): it now names other.txt, main.txt, the run-0128.json copy and the scratch repositories. Read only.
- run_plan.py docstring :19-21 still says "whenever `check` is given `--plan` ... the exit code is 3". The new paragraph at :32-33 says a `--plan` file that does not exist is exit 2. The two sentences sit side by side.
- The `info/grafts` half of the graft condition in `_history_cut` (:263ff) is not reached by any check. The grafted test uses `git replace --graft`, which goes through refs/replace.
- Nothing written into markets-data. A stray `sed -i ... /dev/null` in one of my commands errored ("not a regular file") and changed nothing. Scratch scripts are in /tmp/claude-0/-home-user/3e104f60-b369-56be-82d1-295b070262b0/scratchpad/pb/. My /home/user/tmp-pytest/r187 was deleted after every run. /home/user/tmp-pytest still holds b184 and r183, which are other runs' folders and were left alone.

## Points, each

1. Exit 2 with the file named: held by test_run_plan.py:449 (seen failing on put-back). The docstring is still open by reading (:19-21 against :32-33).
2. Held by :459 (seen failing on put-back).
3. Held by :481 (seen failing on put-back). The sentence matches the staged state.
4. Shallow and graft are each held separately (:502, :520; seen failing with each branch removed alone). "Unless something else is already exit 1" is held for shallow only (:515-517). Open: a late plan whose add commit is visible in a shallow clone reads exit 3 (run_plan.py:351/:369). On this machine that is every real run.
5. Held by :531 (seen failing on put-back). Open: a plan committed on a later date than a date-only start reads exit 3 instead of exit 1 (:373). No check holds date-only plus exit 1.
6. Closed by reading (header :233ff).
7. Held by test_run_record.py:729 (seen failing on put-back). Its `# change:` comment misstates what is dropped.
8. Each refusal is held alone by :693, :707 and :717 (each seen failing alone). The sha refusal is reached only with a sidecar whose agent_id was removed by hand. `keep` never writes such a sidecar (run_record.py:196 is checked before :198 for the same file). The comment at :694-695 says so.
9. Held by :463 and :473 (seen failing on put-back). The accept side is held only by a skipped check.
10. Not closed. The live-counts check runs here and still holds with zeros written into the code. The 108 refusal is held by :448 (seen failing); the edit to :421 is read only (skipped).

## Speculation (labelled; not measured)

- `_history_cut` reports "grafted" for any refs/replace ref, including a plain object replace that is not a graft. I did not try one.
- A shallow repository could be measured per plan by checking whether the add commit is listed in .git/shallow. Only when it is would the add time be truly unknown. This is a reading of git, not something I tried in code.

## Open after this read

**For the builder**
- Ticket 18:
  - run_plan.py:351/:369: shallow or grafted is decided for the whole repository. A late plan whose add commit is visible (depth 3) reads exit 3 instead of exit 1. On the real record, runs 185 and 166 have visible add commits and still read "not measured". Needs a check with a real shallow clone at a depth past the add.
  - run_plan.py:373: a date-only start with the plan committed on a later date reads exit 3. No check holds date-only plus edited plan giving exit 1, or a later-date add.
  - test_run_plan.py:520: the grafted test lacks the "already exit 1" half the builder says it has.
  - The `info/grafts` path in `_history_cut` is held by no check.
  - run_plan.py:19-21: the docstring still says every `--plan` exits 3.
  - test_run_plan.py:449 has no `# change:` comment. :502's comment does not name the 999 edit.
- Ticket 19:
  - test_run_record.py:309/:333-337: the two figures are still zero by construction (the check holds with literal zeros in the code). none_n comes from the code's own tie_note.
  - test_run_record.py:729-731: the comment says nothing else is touched, but the older run-154 line is dropped.

**For the main session**
- Builder run 180's account says the live-counts check is skipped. It runs on this machine.
- 15 checks, including the run 108 refusal side and the `--outside-roster` accept side, can only run where the earlier machine's live transcripts are.
- The real markets-data checkout is shallow. With `_real_rc()` the real-record order assertions are not exercised here, and every real `check` now exits 3.

**What code cannot hold**
- The header text of point 6.
- That the sha refusal cannot be reached for sidecars `keep` writes (point 8).
- A shallow clone whose boundary is the add commit itself (depth 1): there the add time is truly unknown.

Tool calls: 13 of 20 (11 Bash, 1 Read, 1 advisor, plus this hand-back). Model calls are within 26. Sub-agents 0. Writes into the real graph 0.
