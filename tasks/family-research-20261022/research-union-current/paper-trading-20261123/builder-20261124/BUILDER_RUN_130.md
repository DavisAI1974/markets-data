# Builder run 130 (Sonnet): ticket 25, ingest_artifacts

Kept word for word as the agent returned it, 2026-11-24 (twenty-fifth session). Nothing below this line is the main session's.

---

Ticket 25 is built and pushed, with parts A and B done and all checks passing. I did not re-run the tests after the final merge, so the merged tip is untested.

COMMITS
- My commit is b245ee3.
- Branch ccr-659edd86-di9udt was rejected on the first push. I merged FETCH_HEAD (merge commit b848096) and pushed again, dc44b3a..b848096.
- Files outside my three are not mine; the merge only brought in other builders' work (for example `tools/kgraph/run_plan.py` and `run_record.py`).

git diff --stat 3a98333 HEAD for my three files, taken before the merge:
- tests/agent_program/test_ingest_artifacts.py: 203 lines new
- tools/kgraph/context.py: 4 lines
- tools/kgraph/ingest_artifacts.py: 228 lines new
- Total: 435 insertions.

PYTEST (the last run was on the pre-merge tree, before the final push)
- tests/agent_program/test_ingest_artifacts.py: 16 passed.
- tests/agent_program/test_stage5a_context.py: 18 passed, 2 xfailed, in 134 s. No check pins the head's exact lines, so none changed. I did not check whether the 2 xfails were already there before my change.
- I never ran the new tests before the module existed, so there was no red run. I wrote the test file first, then the module, and the first run went red only on two test-side facts.

WHAT THE INGEST PRINTED ON THE SCRATCH COPY
- Artifacts by set: control files 4, decider programs 5, rule files 32, execution plans 7, run plans 24, plan files 2.
- Branch artifacts: 4 (Markets, markets-data, platform working branch, platform codex branch).
- Metrics written: 407 figures.
- Runs skipped for no AgentRun node: none.
- Files skipped: 0.
- Store wrote 591 new, 1 revised, 1 unchanged. I did not trace the revised line.
- No run on record: 77 artifacts. That is all of them, because no committed file or head is named by any run's newest line. The list includes decider_v1.py (commit 04f4378), all four control files, and the platform and codex heads.
- Run plans: 24 exist now (18 when the scout looked) because other builders keep adding them.

CURRENT VERSIONS BLOCK, as the session text shows it at 6,000 tokens on the scratch copy
```
CURRENT VERSIONS (as last read into the graph):
- Markets: branch wt-b25, head 3a98333 (2026-11-24), as read at 2026-11-24T13:55:35Z
- markets-data: branch ccr-659edd86-di9udt, head f652a24 (2026-11-24), as read at 2026-11-24T13:55:35Z
- paper-trading-platform codex: branch origin/codex/strategy-trades-and-mbo-capture, head 47fa1c5 (2026-11-24), as read at ...
- paper-trading-platform: branch ccr-0ac78691-8zapbb, head 28d4dbb (2026-11-24), as read at ...
- tools/decider/programs/README.md: version 2ac873f, authoring run not recorded
- tools/decider/programs/decider_v1.md: version 073f43d, authoring run not recorded
- tools/decider/programs/decider_v1.py: version 04f4378, authoring run not recorded
- tools/decider/programs/loop_decider.py: version 131a9dc, authoring run not recorded
- tools/decider/programs/skip_all.py: version 1d0a6dc, authoring run not recorded
- tools/ratchet/programs/packet_graph_v1.md: version 92a0cf4, authoring run not recorded
- tools/ratchet/programs/paper_rules.md: version 3104192, authoring run not recorded
- tools/ratchet/programs/platform_decider.md: version 131a9dc, authoring run not recorded
- tools/ratchet/programs/platform_exit.md: version 35d1537, authoring run not recorded
- 32 rule files, 7 execution plans, 24 run plans, 2 plan files
These are the versions as last read into the graph; check each with git before trusting it.
```
The whole text was 23,882 characters against 24,000 allowed.

THE CHECKS (16 in the file, all on one scratch copy of the real graph)
- decider_v1.py version: expects 04f437861201ba5b8be0b411346a91eafdc531c6 and all four required attrs.
- Rule and control files: 32 rule files, 4 control files and 5 decider programs each have an Artifact.
- Working branch: for each of the three repositories (3 cases), the stored branch, head and subject equal what git gave in the test straight after the ingest. A first version compared against git at assertion time and failed once because another builder moved the markets-data head in between.
- Codex branch: the stored head equals `git rev-parse origin/codex/strategy-trades-and-mbo-capture`.
- Authoring run:
  - Run 119's newest line lists data_commits 11fe552 and 9079b22 (markets-data), so commit 11fe552 resolves to run:0119.
  - Run 114's code_commit is 68d65a6, so that commit resolves to run:0114. Only 114's newest line names it. My first test said 114, 118 and 123 all name it, which was wrong, because they only mention it in other fields.
  - decider_v1.py carries the "not recorded" text and is in the printed list.
- PRODUCED link: the only PRODUCED link into decider_v1.py comes from commit:Markets:04f4378612.
- Metrics:
  - `metric:run:0114:tool_calls` is 26, with unit "calls", and `of` is run:0114.
  - `output_tokens` for run 114 is 20871.
  - Every Metric's `of` is exactly one AgentRun.
  - A null figure writes no Metric.
- Idempotence: the second run printed `'new': 0, 'revised': 0`, and `check_all` after the ingest reports nothing that was not there before.
- Session text: it holds the Markets branch and head's first 7 characters, plus the closing sentence. The same copy before the ingest holds the "none on record" sentence. It is within budget at 6,000 and 3,000 tokens.
- Block cut: at 1,500, 2,000, 2,500 and 3,000 tokens the file lines are cut and a "not shown for want of budget" line says how many. At 400,000 tokens nothing is cut.

DEPARTURES AND OPEN POINTS
1. **Edge type.** I used PRODUCED from the commit to the Artifact, not PINNED_AT. PINNED_AT's wording in schema.py is "a trade day, a time, a place on the tape", and PRODUCED's wording is "a run, a commit made dst". A PRODUCED link from the run is also written when a run is named and is a node.
2. **as_read_at is carried over.** A fresh time on every read would make the second run write new revisions. So the node keeps the first-read time while nothing else about it changed, and the session text's "as read at" is the time that state was first read, not the last read. If you want the last read, the "writes nothing new" rule has to give.
3. **model_replies unit.** I gave it "replies", since your list was tokens, calls or ms.
4. **No real file has an authoring run.** No commit that last changed any file in the six sets is named by any run's line, so no Artifact of a file carries a run on the real record. The positive path is tested only through `authoring_run()` with real shas. The several-runs wording ("not recorded: N runs name commit ...") has no real case, since no commit is named by two runs, so it is untested. I did not invent runs.
5. **Circular import.** context.py imports `current_versions_lines` from `tools/kgraph/ingest_artifacts.py`, which imports `CHARS_PER_TOKEN` from context lazily inside the function.
6. **Block cap.** The 10 per cent cap applies only to the cut-able file lines. The branch lines, count line and closing sentence always stay, so at very small budgets the block exceeds 10 per cent.
7. **Search by the builder.** I ran one git probe and one python probe to find a real authoring-run case, which was not located for me. Nothing else was searched.

TIDY-UP AND CALL COUNT
- /tmp/run130 and /tmp/pytest-of-root are deleted. `git -C /home/user/markets-data status --short` is empty.
- Tool calls: 17.
- Hard-limit status is not recorded: I did not time the run or total the tokens. The 60-call limit was not reached, and the wall-clock (40 minutes) and token limits were not checked.
