# Performance auditor run 153 (Sonnet): runs 131, 136, 138 and 140 to 145, each its own block

Kept word for word as the agent returned it, 2026-11-24 (twenty-fifth session). Nothing below this line is the main session's.

---

# Performance auditor run 153

Scope: the nine finished runs 131, 136, 138, 140, 141, 142, 143, 144 and 145. Read-only. Nothing written, no sub-agent, no application script run. PAPER below = /home/user/markets-data/tasks/family-research-20261022/research-union-current/paper-trading-20261123.

How each figure was taken:
- Limits come from `jq -c . PAPER/run-plans/run-NNNN.json`.
- Plan-in-git times come from `git -C /home/user/markets-data log --diff-filter=A --format='%h %cI' -- <plan file>`.
- Run-record figures come from the newest line of each run in PAPER/agent-runs.jsonl (`jq -c 'select((.run|tostring)=="N")' | tail -1`).
- Transcript figures come from one `jq -s` pass per transcript in /root/.claude/projects/-home-user/3356516d-d71a-5e13-907d-ff8d8ffcb6d4/subagents/agent-<id>.jsonl. It groups assistant lines by `message.id`, sums `message.usage`, and counts `tool_use` blocks by name. The largest `tool_result` is by characters, matched to its `tool_use` id.
- Wall clock is the last minus the first transcript timestamp.
- Tool calls exclude `SubagentHandback`.
- Cache-read share = cache-read ÷ (fresh + cache-written + cache-read + output).
- All nine runs: no `advisor` call in any transcript, so the line counts none. No Agent/Task call, so 0 sub-agents. No Grep or Glob call (every run used Bash, plus Read in 140, 141 and 144). I did not count `rg` or `grep` typed inside Bash commands.
- For every run the line's four token figures, reply count, tool-call count and wall clock equal the transcript's. The exceptions are named under each run.

## Run 131
Builder, Sonnet 5.5, ticket 03b. Transcript agent-af6449e8ff5d6869d. Plan: PAPER/run-plans/run-0131.json.

1. Limits against figures

| Limit | Written | Reached | Result |
|---|---|---|---|
| max_model_calls | 40 | 31 replies | kept |
| max_tool_calls | 45 | 29 (all Bash) | kept |
| max_sub_agents | 0 | 0 | kept |
| max_tokens | 300,000 (the harness total, input and output together) | the line holds 136,782, "the harness's total at its third hand-back (none was given at its fourth)" | no harness total for the whole run. It cannot be shown kept on the plan's measure for the whole run. At the third hand-back it was 136,782. |
| max_wall_clock_s | 1800 | 1997.274 s | passed by 197.3 s |
| max_retries | 1 | 4 hand-backs in the transcript, so three after the first | the line says "sent back three times" |
| max_concurrent_workers | 1 | not measurable from the transcript | not shown |
| max_graph_writes | 0 | only Bash calls; I did not inspect their content for graph writes | not shown |

- Transcript four figures: fresh 66; cache-written 455,668; cache-read 2,765,266; output 60,969. Sum 3,281,969.
- The harness total (136,782) and the transcript sum are different measures. I could not reconcile them.
- Plan file added to git 2026-11-24T13:42:53+00:00. First transcript timestamp 13:45:44.393Z. The plan was in git before the run.

2. Line against transcript
- The newest line holds all four parts: replies 31 = 31; tool_calls 29 = 29 Bash (the 4 `SubagentHandback` calls not counted); the four figures are equal; wall 1,997,274 ms = 13:45:44.393 to 14:19:01.667.
- The only figure that is not for the whole transcript is `tokens_reported` (third hand-back).

3. Where the spend went
- 31 replies. Cache-read share 84.26%. Cache-read per reply 89,202. Tool calls per reply 0.935.
- Largest result: Bash `cat -n tests/agent_program/test_auditor_called.py`, 13,562 characters.

4. Produced (`git show --stat`)
- df7e88c: 4 files, 184 insertions, 57 deletions. auditor_called.py +35/-; test_auditor_called.py 202 lines changed; CLAUDE.md 2; frankie-performance-auditor.md 2.
- 120579e: 2 files, 174 insertions, 18 deletions.
- 781f0ac: 2 files, 141 insertions, 42 deletions.
- d8ecd10: 4 files, 71 insertions, 26 deletions.
- Report PAPER/builder-20261124/BUILDER_RUN_131.md: 19,194 bytes (`wc -c`).

## Run 136
Reviewer, Opus 5.5, tickets 02 and 03. Transcript agent-a6a1b50f5d51a6c71.

1. Limits against figures

| Limit | Written | Reached | Result |
|---|---|---|---|
| max_model_calls | 30 | 18 | kept |
| max_tool_calls | 22 | 19 (Bash), 20 with the hand-back | kept |
| max_sub_agents | 0 | 0 | kept |
| max_tokens | 250,000 | line `tokens_reported` null | cannot be shown kept on the plan's measure |
| max_wall_clock_s | 1500 | 669.5 s | kept |
| max_retries | 1 | one hand-back | kept |
| max_concurrent_workers | 1 | not measurable | not shown |
| max_graph_writes | 0 | not measurable | not shown |

- Transcript four figures: 38; 96,927; 1,312,161; 36,737 (sum 1,445,863).
- Plan added 13:51:22+00:00. First transcript timestamp 13:53:13Z. The plan was in git before the run.

2. Line against transcript
- All figures equal.
- The line's outcome text says "finished at its limit of 22 tool calls". Its own `tool_calls` and the transcript both give 19.

3. Where the spend went
- 18 replies. Cache-read share 90.75%. Cache-read per reply 72,898. Tool calls per reply 1.056.
- Largest result: Bash `cd /home/user/Markets-r136 && git show --stat c832307 dc44b3a | head -40; git show c832307 -- tools/kgraph/defend.py ...`, 22,251 characters.

4. Produced and reading
- Review PAPER/reviews-20261124/REVIEW_RUN_136.md: 18,003 bytes.
- Read calls with no offset or limit on a file over 300 lines: 0 (no Read calls at all). Grep or Glob calls: 0.

## Run 138
Reviewer, ticket 25. Transcript agent-a5e497a66f23d0103.

1. Limits against figures

| Limit | Written | Reached | Result |
|---|---|---|---|
| max_model_calls | 25 | 12 | kept |
| max_tool_calls | 20 | 11 | kept |
| max_sub_agents | 0 | 0 | kept |
| max_tokens | 220,000 | no harness total on the line | cannot be shown kept |
| max_wall_clock_s | 1500 | 1070.0 s | kept |
| max_retries | 1 | one hand-back | kept |
| max_concurrent_workers | 1 | not measurable | not shown |
| max_graph_writes | 0 | not measurable | not shown |

- Transcript four figures: 24; 121,553; 539,274; 21,045 (sum 681,896).
- Plan added 13:57:10+00:00. First transcript timestamp 13:58:07Z. The plan was in git before the run.

2. Line against transcript: all equal.

3. Where the spend went
- 12 replies. Cache-read share 79.08%. Cache-read per reply 44,940. Tool calls per reply 0.917.
- Largest result: Bash `git log --oneline -3 && git show --stat b245ee3 | head -20 && cat -n tools/kgraph/ingest_artifacts.py && git show b245ee3 -- tools/kgraph/context.py`, 19,812 characters.

4. Produced and reading
- Review PAPER/reviews-20261124/REVIEW_RUN_138_TICKET_25.md: 13,587 bytes.
- Whole-file Reads over 300 lines: 0 (no Read calls). Grep or Glob: 0.

## Run 140
Reviewer, ticket 03b, third read. Transcript agent-afe3deec2d38e24e1.

1. Limits against figures

| Limit | Written | Reached | Result |
|---|---|---|---|
| max_model_calls | 22 | 11 | kept |
| max_tool_calls | 15 | 10 (9 Bash, 1 Read) | kept |
| max_sub_agents | 0 | 0 | kept |
| max_tokens | 160,000 | harness total on the line 89,117 | kept on the plan's measure |
| max_wall_clock_s | 1200 | 323.6 s | kept |
| max_retries | 1 | one hand-back | kept |
| max_concurrent_workers | 1 | not measurable | not shown |
| max_graph_writes | 0 | not measurable | not shown |

- Transcript four figures: 24; 76,515; 669,934; 23,106 (sum 769,579). The harness total and the transcript sum could not be reconciled.
- Plan added 13:58:42+00:00. First transcript timestamp 13:59:08Z. The plan was in git before the run.

2. Line against transcript: all equal.

3. Where the spend went
- 11 replies. Cache-read share 87.05%. Cache-read per reply 60,903. Tool calls per reply 0.909.
- Largest result: Read of /root/.claude/projects/-home-user/3356516d-d71a-5e13-907d-ff8d8ffcb6d4/tool-results/bn59qgw32.txt, 34,983 characters.

4. Produced and reading
- Review PAPER/reviews-20261124/REVIEW_RUN_140_TICKET_03b_THIRD.md: 15,902 bytes.
- Read with no offset or limit on a file over 300 lines: 1. It is the 582-line saved tool-result file above, not a source file. Grep or Glob: 0.

## Run 141
Reviewer, ticket 19, second read. Transcript agent-a40a803cb420c4bb9.

1. Limits against figures

| Limit | Written | Reached | Result |
|---|---|---|---|
| max_model_calls | 22 | 10 | kept |
| max_tool_calls | 15 | 9 (8 Bash, 1 Read) | kept |
| max_sub_agents | 0 | 0 | kept |
| max_tokens | 160,000 | no harness total on the line | cannot be shown kept |
| max_wall_clock_s | 1200 | 290.2 s | kept |
| max_retries | 1 | one hand-back | kept |
| max_concurrent_workers | 1 | not measurable | not shown |
| max_graph_writes | 0 | not measurable | not shown |

- Transcript four figures: 24; 83,539; 671,664; 20,739 (sum 775,966).
- Plan added 14:00:44+00:00. First transcript timestamp 14:01:14Z. The plan was in git before the run.

2. Line against transcript: all equal.

3. Where the spend went
- 10 replies. Cache-read share 86.56%. Cache-read per reply 67,166. Tool calls per reply 0.900.
- Largest result: Read of /home/user/Markets-r141/tools/kgraph/run_record.py, 21,485 characters.

4. Produced and reading
- Review PAPER/reviews-20261124/REVIEW_RUN_141_TICKET_19_SECOND.md: 15,684 bytes.
- Read with no offset or limit on a file over 300 lines: 1 (run_record.py, 400 lines). Grep or Glob: 0.

## Run 142
Reviewer, ticket 18, second read. Transcript agent-a6b0f4d47c4dcf205.

1. Limits against figures

| Limit | Written | Reached | Result |
|---|---|---|---|
| max_model_calls | 22 | 11 | kept |
| max_tool_calls | 15 | 10 (Bash) | kept |
| max_sub_agents | 0 | 0 | kept |
| max_tokens | 160,000 | no harness total on the line | cannot be shown kept |
| max_wall_clock_s | 1200 | 723.2 s | kept |
| max_retries | 1 | one hand-back | kept |
| max_concurrent_workers | 1 | not measurable | not shown |
| max_graph_writes | 0 | not measurable | not shown |

- Transcript four figures: 24; 75,531; 646,645; 26,646 (sum 748,846).
- Plan added 14:01:35+00:00. First transcript timestamp 14:02:04Z. The plan was in git before the run.

2. Line against transcript: all equal.

3. Where the spend went
- 11 replies. Cache-read share 86.35%. Cache-read per reply 58,786. Tool calls per reply 0.909.
- Largest result: Bash `sed -n '126,400p' .../reviews-20261124/REVIEW...`, 20,883 characters.

4. Produced and reading
- Review PAPER/reviews-20261124/REVIEW_RUN_142_TICKET_18_SECOND.md: 16,376 bytes.
- Whole-file Reads over 300 lines: 0 (no Read calls). Grep or Glob: 0.

## Run 143
Reviewer, ticket 03b, fourth read. Transcript agent-a9815c3c53b26ec96.

1. Limits against figures

| Limit | Written | Reached | Result |
|---|---|---|---|
| max_model_calls | 20 | 9 | kept |
| max_tool_calls | 14 | 8 (Bash) | kept |
| max_sub_agents | 0 | 0 | kept |
| max_tokens | 150,000 | harness total on the line 81,346 | kept on the plan's measure |
| max_wall_clock_s | 1200 | 471.0 s | kept |
| max_retries | 1 | one hand-back | kept |
| max_concurrent_workers | 1 | not measurable | not shown |
| max_graph_writes | 0 | not measurable | not shown |

- Transcript four figures: 20; 63,451; 482,587; 23,981 (sum 570,039).
- Plan added 14:08:46+00:00. First transcript timestamp 14:09:12Z. The plan was in git before the run.

2. Line against transcript: all equal.

3. Where the spend went
- 9 replies. Cache-read share 84.66%. Cache-read per reply 53,621. Tool calls per reply 0.889.
- Largest result: Bash `git log --oneline -1 && git diff 120579e 781f0ac -- tools/kgraph/auditor_called.py tests/agent_program/test_auditor_called.py; ...`, 26,678 characters.

4. Produced and reading
- Review PAPER/reviews-20261124/REVIEW_RUN_143_TICKET_03b_FOURTH.md: 20,398 bytes.
- Whole-file Reads over 300 lines: 0 (no Read calls). Grep or Glob: 0.

## Run 144
Reviewer, ticket 19, third read. Transcript agent-a1268354ddf538d47.

1. Limits against figures

| Limit | Written | Reached | Result |
|---|---|---|---|
| max_model_calls | 20 | 13 | kept |
| max_tool_calls | 14 | 12 (10 Bash, 2 Read) | kept |
| max_sub_agents | 0 | 0 | kept |
| max_tokens | 150,000 | harness total on the line 100,944 | kept on the plan's measure |
| max_wall_clock_s | 1200 | 505.3 s | kept |
| max_retries | 1 | one hand-back | kept |
| max_concurrent_workers | 1 | not measurable | not shown |
| max_graph_writes | 0 | not measurable | not shown |

- Transcript four figures: 30; 88,056; 789,099; 20,507 (sum 897,692).
- Plan added 14:10:05+00:00. First transcript timestamp 14:10:36Z. The plan was in git before the run.

2. Line against transcript: all equal.

3. Where the spend went
- 13 replies. Cache-read share 87.90%. Cache-read per reply 60,700. Tool calls per reply 0.923.
- Largest result: Read of /root/.claude/projects/-home-user/3356516d-d71a-5e13-907d-ff8d8ffcb6d4/tool-results/bavx0ulo8.txt, 32,470 characters.

4. Produced and reading
- Review PAPER/reviews-20261124/REVIEW_RUN_144_TICKET_19_THIRD.md: 15,626 bytes.
- Read with no offset or limit on a file over 300 lines: 1. It is the 502-line saved tool-result file above. The run's other Read call carried an offset or limit. Grep or Glob: 0.

## Run 145
Reviewer, ticket 03b, fifth read. Transcript agent-af7242959a08a7b00.

1. Limits against figures

| Limit | Written | Reached | Result |
|---|---|---|---|
| max_model_calls | 16 | 8 | kept |
| max_tool_calls | 10 | 7 (Bash), 8 with the hand-back | kept |
| max_sub_agents | 0 | 0 | kept |
| max_tokens | 120,000 | no harness total on the line | cannot be shown kept |
| max_wall_clock_s | 900 | 169.7 s | kept |
| max_retries | 1 | one hand-back | kept |
| max_concurrent_workers | 1 | not measurable | not shown |
| max_graph_writes | 0 | not measurable | not shown |

- Transcript four figures: 16; 49,200; 303,265; 13,290 (sum 365,771).
- Plan added 14:19:20+00:00 (`git log` printed 14:19:20 for this plan). First transcript timestamp 14:19:52Z. The plan was in git before the run.

2. Line against transcript
- Figures equal.
- The line's outcome text says "8 tool calls of 10". The `tool_calls` figure is 7, and the transcript has 7 Bash plus the hand-back.

3. Where the spend went
- 8 replies. Cache-read share 82.91%. Cache-read per reply 37,908. Tool calls per reply 0.875.
- Largest result: Bash `git log --oneline -1 && git diff 781f0ac d8ecd10 -- tools/kgraph/auditor_called.py tests/agent_program/test_auditor_called.py CLAUDE.md .claude/agen...`, 15,756 characters.

4. Produced and reading
- Review PAPER/reviews-20261124/REVIEW_RUN_145_TICKET_03b_FIFTH.md: 8,987 bytes.
- Whole-file Reads over 300 lines: 0 (no Read calls). Grep or Glob: 0.

## Set beside the earlier runs

Earlier figures for 122, 130, 132, 134 and 135 are from the newest lines in PAPER/agent-runs.jsonl. They agree with the table in AUDIT_RUN_139.md. Cache-read per reply is a division of the figures shown.

- Run 129: AUDIT_RUN_139.md holds 7 replies, 6 tool calls and 256,628 cache-read, from an earlier line of that run. The figures below are from its newest line.
- Run 121: its newest line holds model_replies null. The reply count 16 is from AUDIT_RUN_139.md.

Builders

| | 131 | 122 | 130 | 129 (newest line) | 121 |
|---|---|---|---|---|---|
| Replies | 31 | 16 | 18 | 33 | 16 |
| Tool calls | 29 | 17 | 21 | 29 | 14 |
| Tool calls per reply | 0.935 | 1.06 | 1.17 | 0.879 | 0.875 |
| Cache-read tokens | 2,765,266 | 1,750,851 | 1,272,282 | 2,735,541 | 840,239 |
| Cache-read per reply | 89,202 | 109,428 | 70,682 | 82,895 | 52,515 |

Reviewers briefed the old way, then with the diff, then earlier

| | 136 | 138 | 140 | 141 | 142 | 143 | 144 | 145 | 132 | 134 | 135 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Replies | 18 | 12 | 11 | 10 | 11 | 9 | 13 | 8 | 10 | 12 | 15 |
| Tool calls | 19 | 11 | 10 | 9 | 10 | 8 | 12 | 7 | 9 | 11 | 14 |
| Tool calls per reply | 1.056 | 0.917 | 0.909 | 0.900 | 0.909 | 0.889 | 0.923 | 0.875 | 0.900 | 0.917 | 0.933 |
| Cache-read tokens | 1,312,161 | 539,274 | 669,934 | 671,664 | 646,645 | 482,587 | 789,099 | 303,265 | 517,997 | 648,450 | 837,165 |
| Cache-read per reply | 72,898 | 44,940 | 60,903 | 67,166 | 58,786 | 53,621 | 60,700 | 37,908 | 51,800 | 54,038 | 55,811 |

What the figures can show
- Counts, and divisions of those counts.
- Whole-file Reads over 300 lines were 0 in 136, 138, 142, 143 and 145, and 1 each in 140, 141 and 144. Grep or Glob calls were 0 in all nine runs.

What they cannot show
- The tasks differ: a builder making four re-sent parts of one tool and its checks, against different reviewers each reading a different change.
- Each cell is one run, with no repeat.
- Cache-read depends on how far the context grew, which depends on the task and the number of replies. Fewer replies means fewer cache reads by arithmetic.
- The briefing method is not isolated from the task. Plans 136 and 138 and plans 140 to 145 differ in more than the briefing, so no effect of the briefing can be separated here.
- Harness totals (where a line holds one) and transcript sums are different measures. I could not reconcile them.
- Nothing here measures the quality of any run's output. No percentage is given and no run is ranked.

Tool calls I made besides the hand-back: 4, all Bash.
