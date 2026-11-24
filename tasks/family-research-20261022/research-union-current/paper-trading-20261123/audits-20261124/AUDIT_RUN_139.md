# Performance auditor run 139 (Sonnet): runs 122, 130, 132, 134 and 135, each its own block

Kept word for word as the agent returned it, 2026-11-24 (twenty-fifth session). Nothing below this line is the main session's.

---

## Run 122

Builder, claude-sonnet-5-5, transcript agent-ad16023331334520b.jsonl. Figures from the run's line in agent-runs.jsonl, run-plans/run-0122.json, and a jq -s pass over the transcript grouped by message.id.

1. Limits in the plan against figures reached
- max_model_calls 60: 16 replies, kept.
- max_tool_calls 70: 17 (transcript has 18 tool uses; the extra is SubagentHandback), kept.
- max_wall_clock_s 2400: 758.4 s (line 758,422 ms; transcript timestamps 13:37:55.859 to 13:50:34.281 agree), kept.
- max_sub_agents 0: 0 (no Task/Agent tool use), kept.
- max_concurrent_workers 1: no worker spawned, kept on the run's own side; other builders running at the same time not measured.
- max_tokens 500,000 ("the harness's total"): the line has tokens_reported null, so the limit cannot be shown kept on the measure its plan names. The transcript's own sum is 1,881,413 input + 44,250 output = 1,925,663; that is not the harness total and I cannot say how they relate.
- max_retries 1: not measured. No tool result flagged as error. Call 14 holds a push loop of up to 4 tries; the transcript does not show whether it looped.
- max_graph_writes 0: not measured (I did not scan its commands for graph writes).
- No advisor call; the line does not count one.
- Plan file entered git as 9bfef60 at 2026-11-24T13:36:21+00:00; first transcript timestamp 13:37:55.859, so it was in git before the run. Command: git -C /home/user/markets-data log --diff-filter=A --format='%h %cI' -- .../run-plans/run-0122.json.

2. Line against transcript: no difference. Fresh 34, cache-written 130,528, cache-read 1,750,851, output 44,250; fresh+written+read = 1,881,413 = line input_tokens; replies 16; tool calls 17; budget_tokens 500,000 = plan.

3. Where the spend went
- 16 replies. Cache-read 1,750,851 of the four figures' 1,925,663 = 90.9%. Cache-read per reply 109,428.
- Tool calls per reply 17/16 = 1.06 (15 Bash, 2 Read).
- Largest tool result: Read of /home/user/Markets-b456/tools/kgraph/defend.py, 44,668 characters. Second: Read of tests/agent_program/test_defend.py, 34,736. Third: Bash grep -n "    def write" -A60 tools/kgraph/store.py | head -120, 7,649. (jq over tool_result blocks matched to tool_use ids.)

4. Produced
- c832307 (git show --stat): 3 files, 201 insertions, 33 deletions (defend.py 105 lines changed, test_defend.py 128, BUILD_NOTES_DEFEND.md 1). dc44b3a: 2 files, 110 insertions, 1 deletion (defend.py 42, test_defend.py 69).
- BUILDER_RUN_122.md is 9,990 bytes. It says: "I read the whole of defend.py and the whole test file", and "greps and reads outside your list": sources.py (link, edge_id), store.py (write), schema.py (Artifact and REVISES), rule_versions.py:68, BUILD_NOTES_DEFEND.md, the real roles of every AgentRun via the store, the role list in agent-runs.jsonl.
- Transcript: the two whole-file Reads returned 44,668 and 34,736 characters (together 79,404). Call 1 was wc -l on defend.py, test_defend.py and BUILD_NOTES_DEFEND.md plus grep -n "def test_". Call 4 (2,823 chars) read BUILD_NOTES_DEFEND.md, sources.py, rule_versions.py lines 60-72, schema.py and the role list. The store.py grep returned 7,649 characters.

## Run 130

Builder, claude-sonnet-5-5, transcript agent-aee0e00f5187acfa1.jsonl.

1. Limits
- max_model_calls 50: 18, kept.
- max_tool_calls 60: 21 (22 tool uses less SubagentHandback), kept.
- max_wall_clock_s 2400: 650.8 s (line 650,813 ms; transcript 13:45:44.379 to 13:56:35.192), kept.
- max_sub_agents 0: 0, kept.
- max_concurrent_workers 1: no worker spawned, kept on the run's own side; the plan note says several builders worked at once, not measured.
- max_tokens 450,000: harness total on the line 103,873, kept on the plan's measure. Transcript sum 1,366,081 + 29,338 = 1,395,419, far above the harness total. Two sums tried against 103,873 do not match: fresh+output 29,376; fresh+written+output 123,137.
- max_retries 1: not measured. One tool result flagged error: call 17, a Monitor call, followed by a Bash poll in call 18.
- max_graph_writes 0: not measured; the line's outcome says its checks ran on a scratch copy of the real graph.
- No advisor call; the line does not count one.
- Plan entered git as b51ed27 at 13:42:20; first timestamp 13:45:44, so in git before the run.

2. Line against transcript: no difference. Fresh 38, written 93,761, read 1,272,282, output 29,338, input total 1,366,081, replies 18, tool calls 21.

3. Spend
- 18 replies. Cache-read 1,272,282 of 1,395,419 = 91.2%. Per reply 70,682.
- Tool calls per reply 21/18 = 1.17 (15 Bash, 3 Edit, 2 Write, 1 Monitor).
- Largest tool result: Bash, 10,111 characters (git log, git branch, then sed -n ranges of schema.py, sources.py, ingest_agent_runs.py). Next: Bash sed reads of context.py, test_stage5a_context.py, store.py, 7,796; and 6,807.

4. Produced
- b245ee3: 3 files, 435 insertions (test_ingest_artifacts.py 203, ingest_artifacts.py 228, context.py 4).
- BUILDER_RUN_130.md is 7,748 bytes. It says: "Search by the builder. I ran one git probe and one python probe to find a real authoring-run case, which was not located for me. Nothing else was searched."
- Transcript: reads were sed -n ranges in Bash calls 1, 2, 3, 6; calls 4 and 5 were a tickets directory listing and a python probe. No whole-file Read.

## Run 132

Reviewer, claude-opus-5-5, transcript agent-aba376a58f48ae0e0.jsonl.

1. Limits
- max_model_calls 25: 10, kept.
- max_tool_calls 20: 9 (10 tool uses less SubagentHandback), kept.
- max_wall_clock_s 1200: 342.3 s (line 342,266 ms; transcript 13:49:28.841 to 13:55:11.107), kept.
- max_sub_agents 0: 0, kept.
- max_concurrent_workers 1: no worker spawned, kept on the run's own side.
- max_tokens 200,000: harness total 79,795, kept on the plan's measure. Transcript sum 591,192 + 23,063 = 614,255. Fresh+written+output = 96,258, does not match the harness total.
- max_retries 1: not measured; no tool result flagged error.
- max_graph_writes 0: not measured.
- No advisor call; the line does not count one.
- Plan entered git as 9d5294d at 13:47:52; first timestamp 13:49:28, so before the run.

2. Line against transcript: no difference. Fresh 22, written 73,173, read 517,997, output 23,063, input 591,192, replies 10, tool calls 9.

3. Spend
- 10 replies. Cache-read 517,997 of 614,255 = 84.3%. Per reply 51,800.
- Tool calls per reply 9/10 = 0.90 (8 Bash, 1 Read).
- Largest tool result: Read of /root/.claude/projects/-home-user/3356516d-d71a-5e13-907d-ff8d8ffcb6d4/tool-results/bo6ffz5e8.txt, 33,358 characters (a saved tool output, not a repository file). Next two: Bash, 4,803 and 4,485.

4. Produced: REVIEW_RUN_132_TICKET_19.md, 13,141 bytes. The line's outcome says 9 checks ran clean.

## Run 134

Reviewer, claude-opus-5-5, transcript agent-a475bb0023c0e5965.jsonl.

1. Limits
- max_model_calls 25: 12, kept.
- max_tool_calls 20: 11 (12 tool uses less SubagentHandback), kept.
- max_wall_clock_s 1200: 323.7 s (line 323,675 ms; transcript 13:49:28.863 to 13:54:52.538), kept.
- max_sub_agents 0: 0, kept.
- max_concurrent_workers 1: no worker spawned, kept on the run's own side; the plan note says one of two reviewers reading at once, not measured.
- max_tokens 200,000: harness total 75,155, kept on the plan's measure. Transcript sum 718,411 + 18,561 = 736,972. Fresh+written+output = 88,522, does not match.
- max_retries 1: not measured; no tool result flagged error.
- max_graph_writes 0: not measured.
- No advisor call; the line does not count one.
- Plan entered git as 76723de at 13:48:12; first timestamp 13:49:28, so before the run.

2. Line against transcript: no difference. Fresh 26, written 69,935, read 648,450, output 18,561, input 718,411, replies 12, tool calls 11.

3. Spend
- 12 replies. Cache-read 648,450 of 736,972 = 88.0%. Per reply 54,038.
- Tool calls per reply 11/12 = 0.92 (all Bash).
- Largest tool result: Bash, 28,037 characters (git log, git show --stat dfb5879, cat -n run_plan.py, cat -n test_run_plan.py, a further cat of a markets-data file). Next: Bash 7,780 (pytest run and a command on the record); Bash 6,277 (run_plan check loop).

4. Produced: REVIEW_RUN_134_TICKET_18.md, 13,293 bytes. The line's outcome says 7 checks ran clean.

## Run 135

Reviewer, claude-opus-5-5, transcript agent-adb1142ab9df65719.jsonl.

1. Limits
- max_model_calls 25: 15, kept.
- max_tool_calls 18: 14 (15 tool uses less SubagentHandback), kept.
- max_wall_clock_s 1200: 235.6 s (line 235,635 ms; transcript 13:50:17.738 to 13:54:13.373), kept.
- max_sub_agents 0: 0, kept.
- max_concurrent_workers 1: no worker spawned, kept on the run's own side; the plan note says one of three reviewers reading at once, not measured.
- max_tokens 180,000 (harness total): the line has tokens_reported null, so the limit cannot be shown kept on the measure its plan names. Transcript sum 906,013 + 21,865 = 927,878; not the harness total.
- max_retries 1: not measured; no tool result flagged error.
- max_graph_writes 0: not measured.
- No advisor call; the line does not count one.
- Plan entered git as fe43fdb at 13:49:49; first timestamp 13:50:17, so before the run.

2. Line against transcript: no difference. Fresh 30, written 68,818, read 837,165, output 21,865, input 906,013, replies 15, tool calls 14.

3. Spend
- 15 replies. Cache-read 837,165 of 927,878 = 90.2%. Per reply 55,811.
- Tool calls per reply 14/15 = 0.93 (all Bash).
- Largest tool result: Bash, 26,763 characters (git diff 3a98333 df7e88c -- auditor_called.py CLAUDE.md .claude/agents/frankie-performance-auditor.md, then cat -n tests/agent_program/test_auditor_called.py). Next: Bash 13,072 (pytest in /home/user/Markets-r135); Bash 12,277 (python3 -m tools.kgraph.auditor_called on the real record).

4. Produced: REVIEW_RUN_135_TICKET_03b_SECOND.md, 15,899 bytes. The line's outcome says 24 checks ran clean.

## Set beside the earlier runs

Earlier figures are copied from the last section of AUDIT_RUN_133.md, not re-measured. Per-reply figures are divisions of the figures shown.

Builders: 122 and 130 beside 129, 121, 114, 110

| | 122 | 130 | 129 | 121 | 114 | 110 |
|---|---|---|---|---|---|---|
| Replies | 16 | 18 | 7 | 16 | 22 | 21 |
| Tool calls | 17 | 21 | 6 | 14 | 26 | 24 |
| Tool calls per reply | 1.06 | 1.17 | 0.86 | 0.875 | 1.18 | 1.14 |
| Cache-read tokens | 1,750,851 | 1,272,282 | 256,628 | 840,239 | 1,962,598 | 2,032,035 |
| Cache-read per reply | 109,428 | 70,682 | 36,661 | 52,515 | 89,209 | 96,764 |

Reviewers: 132, 134 and 135 beside 123, 118, 115, 107

| | 132 | 134 | 135 | 123 | 118 | 115 | 107 |
|---|---|---|---|---|---|---|---|
| Replies | 10 | 12 | 15 | 14 | 17 | 19 | 14 |
| Tool calls | 9 | 11 | 14 | 13 | 16 | 26 | 14 |
| Tool calls per reply | 0.90 | 0.92 | 0.93 | 0.93 | 0.94 | 1.37 | 1.00 |
| Cache-read tokens | 517,997 | 648,450 | 837,165 | 825,377 | 1,053,514 | 1,504,731 | 1,599,935 |
| Cache-read per reply | 51,800 | 54,038 | 55,811 | 58,955 | 61,971 | 79,196 | 114,281 |

What the figures can show
- Counts and divisions of those counts.
- Run 122's cache-read per reply (109,428) is its 1,750,851 divided by 16 replies. It had two whole-file Reads of 44,668 and 34,736 characters in its first three tool calls. Runs 114, 110, 115 and 107 lie in the same range of cache-read per reply (89,209 to 114,281).
- Run 130 read only by sed -n ranges in Bash, with no whole-file Read.

What they cannot show
- The tasks differ. Run 122 changed eleven places of one 835-line file and was told to read ranges, and it read the whole file. Run 130 wrote two new files of 228 and 203 lines. Reviewers 132, 134 and 135 each read a different change.
- Each cell is one run, no repeat.
- Cache-read depends on how long the context grows, which depends on the task. Fewer replies means fewer cache reads by arithmetic.
- The briefing method of each run is not isolated from its task.
- Harness totals (runs 130, 132, 134) and transcript sums are different measures and I could not reconcile them.
- Nothing here says anything about the quality of any run's output.

Tool calls I made besides the hand-back: 4, all Bash.
