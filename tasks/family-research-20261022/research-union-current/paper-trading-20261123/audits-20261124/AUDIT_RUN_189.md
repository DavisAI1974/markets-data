# Performance auditor run 189 (Sonnet): runs 166 and 180, each its own block

Everything below this line is the agent's own report, word for word; nothing below it is the main session's.

## Hand-back 1 of 1

# Performance auditor run 189

## Run 166
Measured with `jq -s` over SUB/agent-a73e8f2570037bdb4.jsonl (replies grouped by `message.id`, last usage of each; tool_use counted over every assistant line), the run-0166.json plan, the newest agent-runs.jsonl line, and `git log --diff-filter=A` / `git show --stat`.

1. Limits against figures (run stopped by Greg's stop, no hand-back):
- max_model_calls 60: 17 replies, kept.
- max_tool_calls 60: 19 (all Bash), kept.
- max_sub_agents 0: 0, kept.
- max_concurrent_workers 1: not measurable from the transcript.
- max_retries 0: not measurable.
- max_graph_writes 0: not measurable. The transcript shows commits and pushes in the Markets worktree, and no graph write was checked.
- max_wall_clock_s 2400: 460 s (17:36:20.097 to 17:44:00.160), kept.
- max_tokens 450,000: the line has `tokens_reported: null`, so there is no harness total. The transcript's four figures are fresh input 34, cache written 84,446, cache read 1,088,821 and output 22,213. Input of 1,173,301 plus output 22,213 is 1,195,514. That is above 450,000. The plan defines the limit by the harness total, which is absent, so the limit is not measurable against the harness.
- The plan file was added to git at e60eeaa, 17:33:37. The transcript's first timestamp is 17:36:20, so the plan was in git first.

2. Line against transcript: no difference. The line shows 17 replies, 19 tool calls, 1,173,301 input (34, 84,446 and 1,088,821), 22,213 output, 460,063 ms, 0 hand-backs and 0 sub-agent calls. The transcript holds no `SubagentHandback`.

3. Where the spend went:
- 17 replies. Cache read is 1,088,821 of 1,195,514 (input plus output), which is 91.1% of that sum. That is about 64,048 per reply.
- 19 tool calls over 17 replies, 1.12 per reply. All 19 are Bash.
- Five of the 19 Bash calls ran pytest. Two ran `git commit`.
- Largest tool result: Bash, 26,011 characters (`git log`, `git status`, then `cat` of the scout report and related files in the first call). Next are 13,860 (`sed` of test_run_plan.py) and 11,398 (`sed` of run_plan.py).
- Where it was when stopped: its last reply was `git merge FETCH_HEAD` and `git push` of branch wt-b166, after the ticket 19 commit.
- Checks before each commit, by output order:
  - Before 344e3e6 (17:40:49, ticket 18), the last plan-check output reads "44 passed, 15 skipped". An earlier run in the same stretch read "3 failed, 47 passed, 15 skipped".
  - Before d7a44f7 (17:43:55, ticket 19), the last output reads "57 passed, 15 skipped". The run before it read "1 failed, 24 passed, 15 skipped" (the new model_replies-differs test).
  - The pairing of outputs to commits is by output order only.
- It had not begun a report. There is no hand-back, and its commit messages are the only prose it left.
- Commit stats: 344e3e6 changed 2 files (+169/-16); d7a44f7 changed 2 files (+114/-4).

## Run 180
Measured with `jq -s` over SUB/agent-af2091862612a53de.jsonl, the run-0180.json plan, the newest line, and `grep` in BUILDER_RUN_180_TICKETS_18_19.md (6,287 bytes by `wc -c`).

1. Limits against figures:
- max_model_calls 45: 10 replies, kept.
- max_tool_calls 40: 9 Bash plus the hand-back, kept.
- max_sub_agents 0: 0, kept.
- max_concurrent_workers 1, max_retries 0 and max_graph_writes 0: not measurable from the transcript. The report says 0 graph writes.
- max_wall_clock_s 1800: 217.6 s (17:48:19.256 to 17:51:56.872), kept.
- max_tokens 300,000: the harness total on the line is 55,480, kept. The transcript's four figures are fresh input 22, cache written 45,901, cache read 392,901 and output 10,033. Input of 438,824 plus output 10,033 is 448,857, which is above 300,000 as a sum. The plan defines the limit by the harness total. I cannot say how the harness arrives at 55,480.
- The plan file was added to git at ec7af4b, 17:46:24, and the transcript starts at 17:48:19, so the plan was in git first.

2. Line against transcript: no difference. The line shows 10 replies, 9 tool calls, 438,824 input, 10,033 output, 217,616 ms and 1 hand-back. The transcript holds one `SubagentHandback` (6,081 characters in its message). The report says "Tool calls: 8 of 40". By name the transcript has 9 Bash plus the hand-back, so the report's 8 is one lower than the line's 9, and I did not find a count of 8 in the transcript.

3. Where the spend went:
- 10 replies. Cache read is 392,901 of 448,857 (input plus output), which is 87.5%. That is about 39,290 per reply.
- 9 tool calls over 10 replies, 0.9 per reply, all Bash. Three of them ran pytest.
- Largest tool result: Bash, 17,832 characters (`git diff 60f8086..HEAD` of the two test files). Next are 6,991 (the same diff on the two source files) and 3,293 (`sed` of run_record.py).
- Put-backs: the transcript has no `Edit` or `Write` and no direct `git checkout --` call. The put-backs ran from a script, pb.py, written in the scratchpad. It holds 12 cases: points 1, 2, 3, 4, 4b, 5, 7, 8a, 8b, 8c, 9a and 9b. Each case replaces one code line, runs pytest with `-k`, runs `git checkout -- <file>`, then runs `rm -rf` on the pytest base temp folder.
  - In the first run of the script, 11 cases each printed "1 failed". Case 7 printed "OLD COUNT 2", meaning it did not run.
  - Later calls edited pb.py (`sed`, then a Python edit). I did not read their output, so case 7's rerun is not shown here.
  - The report names ten points. The script's twelve cases include sub-cases (4b, 8a to 8c, 9a, 9b).
  - Point 10 has no case in the script. The report says its two named checks are among the 15 skipped on this machine.
- Final pytest run: test_run_plan.py 32 ran clean, test_run_record.py 25 ran clean and 15 skipped. These match the line's outcome text.
- The skips are transcripts "not on this machine" under another session's folder.
- Git status was run after the script, and the report says it was empty.

## The same work twice
Run 180 was started to recover the report that run 166's stop lost. Its figures:
- 10 replies and 9 tool calls (plus the hand-back).
- Harness total 55,480.
- Transcript sum 448,857 (input 438,824, output 10,033).
- 217.6 s of wall clock.

Run 166's figures at its stop were 17 replies, 19 tool calls and 460 s, with no harness total and a transcript sum of 1,195,514. Both runs read the same four files and diffs and both ran the same check files.

The figures cannot show these things:
- How much of run 180's reading would have been avoided had run 166 reported.
- Any cost of the stop itself.
- How the harness total of 55,480 relates to the transcript sum.
- Whether run 166 would have run put-backs.

Tool calls besides the hand-back, my own run: 4 (the first call ran the `jq` over both transcripts, the second read the plans, lines and git, the third read sizes and commands, the fourth read put-back detail and the report check).
