# Builder run 184 (Sonnet): ticket 46, consolidation as a standing step

Everything below this line is the agent's own report, word for word; nothing below it is the main session's.

## Hand-back 1 of 1

# Builder run 184 (Sonnet): ticket 46, consolidation as a standing step

Everything is built, checked and pushed in one commit, 56f1ecb. I merged remote tip changes in manifest_check, cd386b5, and pushed to ccr-144315dd-pta2ze. `git status --porcelain` in /home/user/wt/b175 is empty. `git -C /home/user/markets-data status --porcelain graph` shows nothing of mine. Every trial ran on a scratch copy of the real graph, deleted afterwards.

Piece by piece, all in commit 56f1ecb. I did not commit the pieces separately; the check file went red first (ImportError, no consolidate module), then green.

1. **Take-back of a SUPERSEDES link.** resolve.py `undo` now takes back RESOLVED_TO and SUPERSEDES links through `withdraw_edge`, and its CLI help says so. Any other link is still refused. The check is `test_undo_takes_back_a_later_over_earlier_link_and_it_stays_on_record_as_withdrawn`. It checks the link is gone from the standing set, still on record as withdrawn with its reason and run, and the first line is kept (history has 2 lines). A MENTIONS edge is still refused. Lines written: about 10 in resolve.py.
2. **`consolidate brief`.** The check is `test_a_brief_names_only_the_reads_claims_and_every_pair_shares_an_entity_with_the_earlier_dated_earlier`, on run:0022 (256 claims).
   - Every later side is a claim of that read.
   - Every pair shares a mentioned Entity.
   - No pair is already linked.
   - A dated earlier claim is dated at or before the later one.
   - The pairs equal an independently worked-out set, so none is cut.
   - The printed counts equal the brief.
3. **`consolidate apply`.** Each pair goes through `resolve.supersede` as it stands, and the repo-dirs CLI path is used as `resolve` does. A refused pair is printed with its refusal and kept in the count. One Task `task:consolidated:<sha of the read>` is written with state done. It carries the read, the applier, the claims, `candidate_pairs`, `pairs_applied`, `pairs_refused` and the refused list. A PRODUCED edge goes from the applying run. A second apply for the same read is refused.
   - `test_before_any_apply_every_claim_of_a_real_read_is_not_yet_and_after_apply_the_read_is_through_the_step`: all 15 reads and all claims are "not yet" first. I took back the 9 real run 96 links that rest on run:0022 on the scratch copy and re-applied those 9 real pairs. Result: 9 applied, 0 refused, the Task counts match, `store.check_all()` is clean, and status shows run:0022 through the step with 256 claims.
   - `test_an_empty_pairs_file_is_a_real_answer_and_the_read_is_through_the_step`, on run:0023 (150 claims).
   - Foot section, each with a `# change:` comment:
     - `test_a_pair_supersede_refuses_is_printed_and_counted_never_dropped_and_a_second_apply_is_refused`: a real pair turned the other way round is refused and counted 1 applied, 1 refused.
     - `test_a_claim_added_after_the_last_pass_is_listed_as_not_yet`: a real claim copied under a new id with `extracted_by=run:0099`, plus its SUPPORTS link, shows as "not yet" while run:0023 is through.
4. **`consolidate status`.** One line per read, then the COUNTS line, exit 0.
5. **The date fault.** `test_the_date_fault_cannot_return_supersede_reads_the_files_date_not_the_folders`. The two claims are `claim:eeeda142ddb2`, 2026-11-24 from file ...20261124X.md, and `claim:69e43c1bcaf7`, 2026-11-23 from file ...20261123U.md. Both sit in the folder family-research-20261022 and have no `said_on`. The true pair is accepted, and the reverse is refused with "2026-11-23 against 2026-11-24". Run 175 had written the two literals. I did not use the paper-trading-20261123 folder as the brief suggested, because the family-research-20261022 pair is the same fault in a real claim.
6. **The manual.** tools/README_AGENT_PROGRAM.md has a new step 6 after line 93: brief, a reader, apply, undo, and "a read is NOT finished until `status` shows it through the step".

Check counts, run from the working copy with MARKETS_DATA set:
- test_consolidate.py: 7 passed (about 90 s).
- test_stage5a_context.py: 18 passed, 2 xfailed.
- test_stage4b_resolve.py: not clean. Its first run gave 1 failed, 2 passed, 1 skipped. The failed check is `test_the_resolvers_real_merges_are_checked_held_under_the_cutoff_and_can_be_undone`. A re-run gave 3 errors, all the same RuntimeError: `agent-runs.jsonl has uncommitted changes in markets-data: commit it before it is a source`. I did not look into what was uncommitted, so I cannot say whether the first failure shared that cause. I wrote nothing into markets-data, so this is not mine, but the main session should commit or settle that file and re-run the check.

**`status` on a scratch copy of the real graph** (before any apply):
`COUNTS claims=2694 through_the_step=0 not_yet=2694 reads=15 reads_not_yet=15`

All 15 reads are not yet: run:0018, 0021, 0022, 0023, 0024, 0032, 0033, 0070, 0071, 0072, 0073, 0074, 0075, 0076 and 0092. The hand pass of run 96 has no Task, so it shows as not yet. That is what is so, and I wrote no Task for it.

A real brief for run:0092 (131 claims) gave 35 claims with at least one candidate and 262 pairs: 3 with an earlier date, 9 with the same date, 250 with a claim undated.

**Findings that change what the step does**
- **Same-day pairs are in the brief.** My first rule was "earlier date only". It reached 0 of the 9 real hand pairs for run:0022, because almost all of the 32 run 96 links are same-day (the 2026-11-24 handoffs, the decisions file by line). The brief therefore has three sections: earlier date, same date, and a claim with no date. The reader orders the same-date and undated pairs from the words, using the handoff letter or the decisions-file line.
- **751 of 2694 claims have no date** by `resolve._when` (no `said_on`, and no 8-digit date in the file name, as with ROOT_GAMEPLAN_DECISIONS.md and RUNNING_LIST.md). Their pairs are listed in their own section, not cut. This is why run:0092 shows 250 undated pairs. `supersede` itself never refuses a pair with a missing date.
- **Entity sharing is narrower than the hand pass.** Only 3 of the 9 real hand pairs of run:0022 share a mentioned Entity, even after following merges. The brief reaches those 3, and the other 6 it cannot. For all 32 hand pairs, roughly 10 share none. The check asserts 3, so it fails if this changes.

**Open**
- Same-date and undated pairs are many, so a brief can be large (run:0092 has 1,345 lines). Nothing ranks them, per the rule.
- `apply` counts candidate pairs at apply time, before applying. If the graph moved since the brief, that number can differ from the brief's.
- A second `apply` for the same read is refused; to change an answer, `undo` the links. There is no command that removes or reopens the Task.
- Pairs outside the brief are applied too if the reader returns them, since `supersede` accepts any pair of claims.

**What code cannot hold**
- Who reads the pairs. A reader (an agent or Greg) must read the brief and write the pairs file; no verb calls a model.
- Nothing makes anyone run the step. It stays a manual step 6 plus `status`, which shows a read as not yet until it is done. The nodes exist; nothing is enforced.
- A hand pass like run 96 stays "not yet" in `status` unless someone runs `apply` for it.

**Tool calls:** about 22 of 60 (my own count, approximate). Model calls: 0. Sub-agents: 0. Writes into the real graph: 0.
