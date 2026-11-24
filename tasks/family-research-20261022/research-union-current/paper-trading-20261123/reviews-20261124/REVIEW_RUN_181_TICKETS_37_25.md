# Reviewer run 181 (Opus): ticket 37, the showing; ticket 25, the second part

Everything below this line is the agent's own report, word for word; nothing below it is the main session's.

## Hand-back 1 of 1

# Reviewer run 181 (Opus): ticket 37, the showing; ticket 25, the second part

Working copy: /home/user/wt/r163 at 74006f2, clean at the end. Data checkout: /home/user/markets-data. I wrote nothing into the real graph or the real record. Every ingest ran against scratch copies in /tmp/claude-0/-home-user/3e104f60-b369-56be-82d1-295b070262b0/scratchpad/ (gnew, gold, old), and those are now removed. I did not run `tools.kgraph.extract coverage` or the grounding check.

## Part 2: ticket 37

**Experiment record.** `grep -c '"rule-version:' experiments/trials.jsonl` gives **5** (lines 4 to 8). The five are produced by `tools/kgraph/rule_versions.py:52-59`, one per commit that edited a rule file:
- exp-dec6b66218cb, afcf107c
- exp-08a4a2a139e6, 4142f97e
- exp-fdb915300b3a, 7e506e59
- exp-2e7fdf8d547f, 0d6226e0
- exp-ed15eea4fc7a, 13ddfa96

**Graph.** I loaded graph/nodes/Entity.jsonl in Python and filtered on `attrs.entity_kind == "rule version"`. There are **60** such nodes, one per (strategy, commit), covering **4** distinct commits:
- 74b1f223: 13 nodes, `rulever:CLxx@74b1f22345`
- 562b6f30: 17 nodes
- 1757145f: 28 nodes, `rulever:platform:...@1757145fa7`
- 95400eba: 2 nodes, CL16 and CL17

**Commits on one side only.** The two sides share no commit.
- In the record only: afcf107c, 4142f97e, 7e506e59, 0d6226e0, 13ddfa96.
- In the graph only: 74b1f223, 562b6f30, 1757145f, 95400eba.

**How the two sides relate.**
- The two sides count different things. A graph node is a strategy at a run's commit. A record node is a commit that edited a rule file.
- 74b1f223 and 562b6f30 do appear in the record, but as the change of paper-run trials (exp-1c51cc953e8b `paper-run:orders-20261124T010517Z` and exp-8124c70783d8 `paper-run:feed-only-...`), not as rule-version trials. 1757145f and 95400eba appear nowhere in the record.
- All nine commits have Commit nodes in the graph (`commit:paper-trading-platform:<10>`).
- DERIVED_FROM edges whose src starts with `rulever:` number 120. Their distinct dst are commits 13ddfa9666, 1757145fa7, 562b6f3041, 74b1f22345, 95400eba11 and three `src:link:` EVIDENCE/VERSIONS files. The edge I sampled was written by `code:tools.kgraph.ingest_paper@c47845e2c6+uncommitted`.
- Of the record's five commits, only 13ddfa96 is reached by an edge from a graph rule-version node. The literal key `"rule version in force"` (rule_versions.py ~line 68) matches 0 lines in graph/edges.
- The ticket's done-test reads "each platform rule version is a node of the experiment record as well as of the graph". On these counts, no rule-version commit is a node on both sides.

## Part 1: ticket 25, builder run 130 second part (b245ee3..6de2e47)

### How the checks ran
- **First run** (the given command): 1 passed, 26 skipped, all for "no paper-trading-platform checkout beside Markets". At that time /home/user/paper-trading-platform did not exist.
- **At 17:54 a symlink appeared**: /home/user/paper-trading-platform pointing to /home/user/davisai1974/paper-trading-platform, at HEAD 28d4dbb. It was made by something outside this run.
- **Later runs** (`-v`, then `-x --tb=line`): 1 passed and **26 ERROR at setup**: `tools.kgraph.schema.Refused: AgentRun run:0179: missing model`.

**Root cause of the setup errors.**
- The fixture at test_ingest_artifacts.py:48 calls `ingest_agent_runs.agent_runs(store)` (ingest_agent_runs.py:69, which calls store.write). That reaches schema.py:132, then `_need` at :96.
- In agent-runs.jsonl, line 214 (run 179, agent_type builder) has `"model": ""`. It is the only line of 217 with an empty model.
- This is drift in the record, not in the code. None of the 26 checks can run on this machine until that line is corrected or superseded.

**The only check that ran:** test_main_prints_the_counts_by_basis_and_the_listing. It has no fixture and runs without a platform checkout.

**The 26 checks that did not run** (skipped in the first run, setup error in the later ones):
- test_decider_v1_has_its_last_commit_and_the_four_required_attrs
- test_a_builders_outcome_text_names_the_author
- test_a_reviewers_task_text_is_not_authorship
- test_platform_rule_files_were_made_outside_the_agent_runs
- test_every_listed_file_has_an_artifact_and_a_missing_one_is_named
- test_working_branch_artifact_holds_the_branch_and_head_git_gives, three parametrisations
- test_codex_branch_artifact_from_the_remote_ref
- test_authoring_run_from_a_field_in_the_real_record
- test_the_main_sessions_commits_and_those_outside_the_runs_hold_against_git
- test_metric_of_run_0114_tool_calls
- test_every_metric_is_of_one_run_and_none_is_a_sum
- test_a_null_figure_writes_no_metric
- test_the_same_snapshot_ingested_twice_writes_nothing_new
- test_an_existing_commit_node_is_left_as_it_is
- test_session_text_shows_the_markets_branch_and_head
- test_the_block_says_which_repository_holds_what_and_ours_first
- test_session_text_without_artifacts_says_none_on_record
- test_session_text_is_within_its_budget_with_the_block_counted
- test_at_a_small_budget_the_branch_lines_stay_and_the_file_lines_go
- test_current_versions_block_is_held_to_a_tenth_and_says_what_it_cut
- test_case_two_runs_name_one_commit_in_a_field
- test_case_two_builders_name_one_commit_in_their_outcome
- test_case_the_commits_field_in_both_forms_and_the_repo_it_names
- test_case_a_builders_task_text_is_not_authorship

**Probe used in place of the checks** (scratchpad probe.py, now deleted). Conditions for every probe figure below:
- No platform checkout: the probe ran before the symlink appeared, and `repo_dirs(..., None)` found none.
- `agent_runs` refused run 179 and the probe caught it, so no new AgentRun nodes and no PRODUCED edges from new runs.
- Markets tree at 74006f2.

Results:
- First ingest: `{'new': 439, 'revised': 0}`. By basis: field 1, builder outcome text 10, main session 63, outside 19, two runs 0.
- Rule files and execution plans were skipped (no platform checkout).
- Second ingest of the same snapshot: new 0, revised 0, unchanged 393. A third with `read_at` set to 2099: the same.

**Put-backs.** Each ran against the one runnable check, and I restored with `git checkout -- .` after each; `git status --short` showed clean each time.
- (a) `-- rel` changed to `HEAD`: test_main_prints... failed.
- (f) step (b) also reads the task text: 1 passed, not noticed.
- (c) `== 1` changed to `>= 1` (first occurrence, field step): 1 passed, not noticed.
- The checks written for (c) and (f) (test_case_two_runs..., test_case_a_builders_task_text...) are among the 26 that did not run.

### Each point of the first read's list (REVIEW_RUN_138_TICKET_25.md:151-164)

1. **Moving markets-data head.**
   - Code: read_snapshot (ingest_artifacts.py:181) reads once; ingest (:275) writes from the snapshot. The branch test now takes the stored head to be either the head git gave before the snapshot or the one after.
   - Measured: the probe's second and third ingests wrote nothing new. The branch test itself did not run (setup error).
2. **Mutants (c) and (d).** (c) is covered by test_case_two_runs..., which did not run here; my (c) put-back went unnoticed by the one runnable check. (d) is under the builder's open items below.
3. **Block over a tenth below about 1,800 tokens.** current_versions_lines is at :317. The branch lines are never cut, and the size loop cuts file lines only.
   - Probe with two branch lines (block chars against the 10 per cent limit):

     | Budget (tokens) | Block chars | Limit |
     |---|---|---|
     | 1000 | 572 | 400 |
     | 1500 | 572 | 600 |
     | 1800 | 674 | 720 |
     | 2000 | 674 | 800 |
     | 2500 | 886 | 1000 |
     | 3000 | 1098 | 1200 |
     | 6000 | 1451 | 2400 |

   - The two platform lines in the builder's printed block are 349 characters. That is arithmetic on the builder's text, not a run. With all file lines cut, the block would be about 921 characters, which is over the tenth for budgets below about 2,300 tokens.
   - test_current_versions_block_is_held_to_a_tenth... (test file :277-284) checks the size only `if files:`, so once every file line is cut it checks no size. The 1,000-token check (:269-274) checks no size at all.
4. **Order and wording.** LABELS at :82 holds the four labels in the order Markets, markets-data, platform (ours), Codex's (his). The order check did not run.
5. **`as_read_at` showing the first read.** `_node` at :265 keeps the standing line while nothing else changed and writes `first_read_at`. The block prints "first read at". The probe's third ingest (later read time) wrote 0 new.
6. **PRODUCED from a Commit** (settled by the plans). ingest writes PRODUCED from `commit:{repo}:{sha[:10]}` for every artifact. It writes PRODUCED from a run only for the bases "field" and "outcome text of a builder", and only when that run's node exists.
7. **"Not recorded".** Replaced by the four bases in `authorship` (:140), plus "not settled" when two runs name a commit.
8. **True authoring runs.** Still held by inference: see "the main session" under the builder's open items.
9. **Stale head in the text.** No change. The block's last line says to check each version with git.
10. **Which Commit node the first ingest revised.** I ran the old b245ee3 code from a git archive on a fresh scratch copy (Markets = r163, no platform): `{'new': 415, 'revised': 0}`. This does not reproduce the builder's first ingest, so it stays open.
11. **Plan-file set covers one folder.** SETS (:52) now has three sources for "plan files" and a new "agent files" set. LISTED (:68) names a listed file that is missing.

### The builder's four open items (BUILDER_RUN_130.md:91-183)

1. **(d), and whether the line is needed.** context.py:406-407 adds the block to `head`, and :456 counts `head` in `fixed`. I put back `fixed` computed from head without the block, measured with context.build on the scratch copy, and restored:

   | Budget (tokens) | Original: chars / claim lines | Put-back (d): chars / claim lines | Limit (chars) |
   |---|---|---|---|
   | 1500 | 5970 / 17 | 5989 / 17 | 6000 |
   | 2500 | 9965 / 35 | 9971 / 36 | 10000 |
   | 3000 | 11891 / 45 | 11935 / 45 | 12000 |
   | 4000 | 15951 / 66 | 15996 / 65 | 16000 |
   | 6000 | 23906 / 114 | 23943 / 116 | 24000 |

   - Each figure is one run, with two branch lines in the block.
   - Both versions stay within the budget. The trim loop (context.py:504-511) and the fill loop that follows hold the bound, but only while a claim line remains to trim.
   - The line is not what holds the bound. It changes which claims are chosen, and no check holds that choice.
2. **"Main session" over-claims.**
   - Code: authorship :140, step (c). read_snapshot takes the session span from `started_at` whenever any line of the session has it. Otherwise it uses the commit times of the session's markets-data commits.
   - The builder wrote that no run line has started_at. Today, session_017eY1WSS3Qut93aDb3jnVG6 has started_at on 25 of 25 newest lines; the other eight sessions have none.
   - The span ends at the latest started_at, not at ended_at.
   - The probe printed both span methods. 13 markets-data run plans came out as "outside the agent runs": run-0157 to 0161 and run-0180 to 0185, including this run's own plan, run-0181.json.
   - The builder's account of 44 "main session" artifacts still holds as a mechanism: any builder commit that carries the session line is counted as the main session's.
3. **Which node the first ingest revised.** Open (point 10 above).
4. **Checks not run after the merge.** `git diff --stat 6de2e47 74006f2 -- tools/kgraph tests/agent_program` lists 11 files. None is ingest_artifacts.py, context.py, store.py, schema.py, extract.py or test_ingest_artifacts.py. The checks cannot run now because of run 179's line (above), not because of the merge.

### A count that does not reconcile
BUILDER_RUN_130.md:118 says "102 artifacts in all". Its basis rows sum to 103 (1+10+44+48+0). Its sets sum to 99, plus 4 branch artifacts, also 103.

### Lines read beyond those handed to me
- context.py:395-410 and :440-545
- extract.py:56-71
- test_ingest_artifacts.py:20-70 and :255-290
- BUILDER_RUN_130.md:91-183, REVIEW_RUN_138:151-164, SCOUT_RUN_152:31-69
- rule_versions.py:40-70

## Speculation (labelled)
- The revision by the first ingest may have been a platform Commit node that rule_versions.py or ingest_paper had written with different attrs before ingest_artifacts rewrote it. My probes had no platform checkout, so they could not show this.
- The 13 run plans tagged "outside" may be main-session commits made after the session's latest started_at. I did not check this per file.

## Open after this read

**For the builder**
- The held-to-a-tenth check checks no size once every file line is cut. With four branch lines, the block is over the tenth below about 2,300 tokens (arithmetic).
- Put-back (d): the counted-block line changes which claims are chosen, not the bound; no check holds either.
- The session span ends at the latest started_at rather than ended_at, so later main-session commits fall to "outside".
- The 102 against 103 count at BUILDER_RUN_130.md:118.
- Which node the first ingest revised.
- The (c) and (f) checks were not observed here.

**For the main session**
- agent-runs.jsonl line 214 (run 179, `"model": ""`) makes the ticket-25 fixture error at setup. Until a later line for run 179 carries a model, none of the 26 checks runs.
- A platform checkout appeared at /home/user/paper-trading-platform at 17:54 during this run. This run's brief described it as absent.
- Ticket 37: the record holds 5 rule-file-edit commits and the graph holds 60 (strategy, commit) nodes over 4 commits, with no commit in common. Which unit "a rule version" means is a question about the plan.

**What code cannot hold**
- True authoring runs for commits that a run names only in prose, or not at all.
- A head shown in the text goes stale on the next push.

## Counts
- Check runs:
  - First given command: 1 passed, 26 skipped, 0 failing.
  - `-v` run: 1 passed, 26 errors at setup.
  - `-x` run: 1 error, then stopped.
  - Put-backs: (a) 1 failed and 26 skipped; (f) and (c) 1 passed and 26 skipped each.
- Final state:
  - `git -C /home/user/markets-data status --porcelain graph experiments`: empty (0 lines).
  - 62 files under graph and experiments are tracked, and `git check-ignore` returned exit 1, so neither file is ignored.
  - r163 is clean.
  - My basetemp is removed. Folders b184 and r183 in /home/user/tmp-pytest belong to other runs.
- Tool calls: 17 of 22. That is 15 Bash/Read calls, 1 advisor call and this hand-back.

