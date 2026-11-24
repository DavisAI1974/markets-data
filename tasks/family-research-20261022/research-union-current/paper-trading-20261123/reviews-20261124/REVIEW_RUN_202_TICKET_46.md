# Reviewer run 202 (Opus): ticket 46, the first read of the consolidation step

Everything below this line is the agent's own report, word for word; nothing below it is the main session's.

## Hand-back 1 of 1

# Reviewer run 202 (Opus): ticket 46, the first read of the consolidation step

Working copy /home/user/wt/r202, detached at cd386b5. It was clean at the start and is clean at the end (`git status --porcelain` printed nothing). markets-data was at 84439dbd. Nothing was written to the real graph. Every graph run used a scratch copy under the scratchpad, made the same way the check's fixture makes it, and that copy is now deleted along with /home/user/tmp-pytest/r202.

Files: /home/user/wt/r202/tools/kgraph/consolidate.py, /home/user/wt/r202/tools/kgraph/resolve.py, /home/user/wt/r202/tests/agent_program/test_consolidate.py, /home/user/wt/r202/tests/agent_program/test_stage4b_resolve.py, /home/user/wt/r202/tools/kgraph/extract.py, /home/user/wt/r202/tools/README_AGENT_PROGRAM.md.

## 1. The checks
- `test_consolidate.py`, whole, once, with MARKETS_DATA set: **7 passed in 123.57s**.
- `test_stage4b_resolve.py`, whole, once: **1 failed, 2 passed, 1 skipped in 5.20s**.
  - Skip, in its own words: `test_stage4b_resolve.py:135: no surface form of the real graph has two standing merges; the case is not made up`. My own count agrees: 82 standing RESOLVED_TO links, and no source has more than one.
  - The failure is `test_the_resolvers_real_merges_are_checked_held_under_the_cutoff_and_can_be_undone`, raised at test_stage4b_resolve.py:76 (`extract.load_result`) -> extract.py:386 -> sources.py:81 `p.read_bytes()`: `FileNotFoundError: ... '/home/user/wt/paper-trading-platform/tasty/RUNNING_LIST.md'`.
  - Root cause: extract.py:59 `repo_dirs` takes the platform folder from the sibling `here.parent / "paper-trading-platform"`. Both /home/user/wt/paper-trading-platform and /home/user/paper-trading-platform sit at 28d4dbb. Neither working tree holds `tasty/RUNNING_LIST.md`, and the graph's source_commit e077b2e for that file is not an ancestor of 28d4dbb (`git merge-base --is-ancestor` says no). The loader reads the working tree, not the file as it stood at source_commit, so this is a platform checkout on the wrong tip. It is not code from this change.
  - The builder's `agent-runs.jsonl has uncommitted changes` RuntimeError did not appear. markets-data now shows only one untracked scout file. Whether the builder's first failure had this same cause is not established.

## 2. Put-backs (one line each, which check notices)
Method, which differs from the standing brief:
- I ran nine put-backs in parallel, each in its own copy of the working copy under the scratchpad (without .git), rather than in /home/user/wt/r202 with `git checkout -- .`. The working copy was never touched.
- The kernel killed one process for lack of memory during that call. M4b ran 316 s against about 550 s for the others.
- Artifact: test_consolidate.py:233 failed in M1, M2, M3, M4, M4b, M5 and M6 with the same words (`'claim:2689fd7e52d1' == 'claim:61549a6d6869'`). It comes from where the copies sat, not from the put-backs. The copies had no sibling `paper-trading-platform`, so `repo_dirs` dropped that repo. `_when` then gave claim:2689fd7e52d1 `('2026-11-24', 0)` against claim:61549a6d6869 `('2026-11-24', 1795478819)`. With the dirs resolved it gives `('2026-11-24', 1795486719)`. So `supersede` refused the true hand pair and accepted the turned one.

Results:
- **M1**, later side taken from every read (consolidate.py:104 `for cid in added` -> `for cid in sorted(day)`): noticed at test_consolidate.py:105, `'claim:002233702f5f' in {...}` is false.
- **M2**, a linked pair listed again (consolidate.py:111 -> `if False:`): noticed at test_consolidate.py:107, the pair `('claim:119062a27485','claim:1cb677d86be0')` is in the standing set.
- **M3**, the Task drops the refused pair from its count (consolidate.py:177 `"pairs_refused": 0, "refused": []`): not shown by measurement. Its only failure was the 233 artifact, which stops that test before line 235. By reading, line 235 `(pairs_applied, pairs_refused) == (1, 1)` would notice it.
- **M3b**, the refused pair never appended (so it is dropped from both the Task and the printed result): noticed at test_consolidate.py:232, `assert (1 == 1 and 0 == 1)`.
- **M4**, a read counted through with no Task of its own (consolidate.py:189 `ok = bool(done)`): noticed at test_consolidate.py:163, :179 and :253 (`(1, 'through the step') == (1, 'not yet')`).
- **M4b**, `ok = True`: noticed at test_consolidate.py:134, :179 and :253.
- **M5**, `undo` deleting the link's lines instead of withdrawing: noticed at test_consolidate.py:192, `KeyError: 'e:a742a86c2d02'`.
- **M6**, `undo` accepting MENTIONS (resolve.py:269 tuple plus `"MENTIONS"`): noticed at test_consolidate.py:199, `DID NOT RAISE Refused`.
- **M7**, the date fault (resolve.py:282 `re.search(..., src)` over the whole path instead of the file name): noticed at test_consolidate.py:211, `'2026-10-22' == '2026-11-24'`.

## 3. On a scratch copy of the real graph
- `consolidate status`: `COUNTS claims=2694 through_the_step=0 not_yet=2694 reads=15 reads_not_yet=15`
- `brief --read run:0092`: 1345 lines; `claims_added=131 claims_with_a_candidate=35 pairs=262 (earlier_date=3 same_date=9 undated=250)`
- `brief --read run:0022`: 17915 lines; `claims_added=256 claims_with_a_candidate=232 pairs=3576 (earlier_date=675 same_date=2551 undated=350)`

**Reach of the 32 hand pairs**, measured another way. I read graph/reads/run-0096-consolidate-pairs.json against the raw MENTIONS edges, both raw and through my own closure over the standing RESOLVED_TO links (not `resolve._standing_merges`). The brief's rule also skips a pair where the earlier claim is dated later; that rule removed none of the 32.
- **22 of 32 are reachable.** Raw and through merges give the same intersections.
- **run:0022: 3 of 9**, which confirms the builder's figure.
- Per read (reachable / hand pairs): run:0018 3/3, run:0022 3/9, run:0023 1/1, run:0032 3/3, run:0072 3/5, run:0073 2/3, run:0074 4/4, run:0075 2/3, run:0092 1/1.
- All 10 unreached pairs have mentions on both sides (1 to 6 each) and share none. The gap is the shared-Entity rule, not missing MENTIONS. For example, claim:e33dc2451acd (5 mentions) against claim:170a98938fbb, claim:45cfc0b14822 and claim:92968610fe89 shares 0 with each.
- 727 of 2,694 claims have no MENTIONS edge at all (consolidate.py:78 builds pairs from MENTIONS only). None of them can appear in any brief.

## 4. Same-date and no-date pairs; cuts and ranking
- `supersede` checks, at resolve.py:305-306: `a, b = _when(...)`; `if a[0] and b[0] and a < b: Refused`.
  - With one date missing, nothing is checked and either direction is accepted.
  - With equal dates, the order is the tuple's second item: the commit time of `source_commit` (resolve.py:284-289), compared across repositories. It is 0 when the repo is missing from dirs, and `apply` from Python defaults to `dirs=None`, which makes it 0 as well.
  - Nothing checks the handoff letter or the decisions-file line that the brief tells the reader to use.
- Concrete case: same file, same commit. claim:01bf69899b10 (ROOT_GAMEPLAN_DECISIONS.md:6143) and claim:a33d8b40772c (:6048), both dated 2026-11-24, both at source_commit 9d2dc38f. Through `consolidate apply --read run:0022` on the scratch copy, both directions were applied (`applied 3 refused []`), and two SUPERSEDES links now stand against each other. One of them puts line 6048 over line 6143, against the brief's own rule.
- Concrete case: a repo missing from dirs. The true pair 2689fd7e52d1 over 61549a6d6869 is refused and its reverse accepted (the section 2 artifact).
- The briefs list pairs both ways: **579** pairs in run:0022's brief and **29** in run:0092's have their reverse in the same brief (claims of the same read, same or missing date). `candidates` at consolidate.py:111 excludes only links already standing, and `apply` (consolidate.py:169) does not check either direction.
- The same probe put a run:0092 pair (claim:e381befd151f over claim:6c0b6129f869) through `--read run:0022`. It was applied and counted in run:0022's Task. `apply` does not limit pairs to the read's claims.
- Cuts, caps and scores: none found in `brief`, `candidates` or `apply`.
  - The only ordering is consolidate.py:110 `sorted(shared, key=lambda o: (day[o] or "~", o))`, by date then id, which is not a score.
  - The only drop is consolidate.py:114, the earlier claim dated after the later one, which follows the plan.
  - Pairs without a date are listed at consolidate.py:118, not cut.
  - The check at test_consolidate.py:115-126 rebuilds the full set separately and asserts equality.

## 5. The ticket's lines
- **One command writes the brief for that read's claims only.** Held by a named check: test_consolidate.py:88-128 (line 105, and M1 is noticed).
- **Pairs applied through the existing command, each with its reason and its run.** Held by a named check: test_consolidate.py:150-160 (the `why` and `made_by` of each of 9 real pairs). Two qualifiers:
  - `apply` takes pairs outside the read (section 4).
  - The Task-count half of the refusal check (M3) is held only by reading of line 235 in this run.
- **A count from the graph of claims not yet through the step, zero after the step runs.** Held by named checks: test_consolidate.py:131-165, 168-179 and 240-255. The count is per read, not per claim:
  - consolidate.py:189 `ok = read in done` counts every claim of a read with a Task as through. That includes the 96 of run:0092's 131 claims that had no candidate, and the 727 claims with no MENTIONS.
  - By reading: a claim added later under a read that already has its Task would count as through. No check covers that case.
- **The manual says a read is not finished until the step has run.** Held by reading: tools/README_AGENT_PROGRAM.md lines 95-102 (new step 6). No check.
- **A check on the real graph that a claim added after the last pass is listed as not yet.** Held by a named check, with a qualifier: test_consolidate.py:240-255 uses a copied real claim with a new id and `extracted_by=run:0099` from the foot section, not a claim that is really in the graph.
- **The date fault cannot return.** Held by a named check: test_consolidate.py:203-217 (M7 noticed at :211).

## Speculation (labelled)
- If the read numbers are the load order, three hand pairs reachable in the whole-graph count could not be reached when each read takes the step on load. They are claim:b46eb688903c over claim:94cdb179e465 and over claim:f24b268b39fe, and claim:f9da8f4a1db7 over claim:46c8da3b54ee. Each new claim is from run:0032 dated 2026-11-24, and each old claim is from run:0033 dated 2026-11-23.
  - At run:0032's step the old claims are not yet in the graph.
  - At run:0033's step the old claim is the read's own (the later side), and consolidate.py:114 drops the run:0032 claim because it is dated later.
  - More generally, a newly read claim older than an existing claim is never set under that existing claim. Not measured.

## Open after this read
For the builder:
- resolve.py:305-306 and consolidate.py:111/169: a pair and its reverse can both be applied when the dates are equal with equal stamps, or when a date is missing. A two-way SUPERSEDES pair results (shown above), and 579 and 29 pairs are listed both ways.
- resolve.py:284-289: the equal-date order comes from the commit time and from whether the repo resolves in dirs. The same true pair is accepted or refused depending on where the checkout sits.
- test_consolidate.py:222-233 depends on a sibling `paper-trading-platform` checkout through extract.py:59. Moved elsewhere, the check fails for that reason.
- consolidate.py:169: `apply` does not check that a pair's later claim belongs to `--read`.
- consolidate.py:189: `status` counts by the read's Task. No check covers a claim added later under a read that already has its Task.
- test_consolidate.py:235: the M3 put-back is not shown noticed by measurement. Re-run with the platform sibling present to confirm.

For the main session:
- test_stage4b_resolve.py fails because the platform checkout at 28d4dbb lacks tasty/RUNNING_LIST.md (e077b2e is not an ancestor). Either put the checkout on the right tip or decide how the loader should read a file that is no longer in the working tree.
- The shared-Entity rule reaches 22 of 32 hand pairs (3 of 9 for run:0022), and 727 claims have no MENTIONS. On the ticket's own aim, the brief's rule leaves 10 of the 32 hand-found pairs out of reach. Widening the rule is Greg's call.

What code cannot hold:
- Who reads the brief.
- That anyone runs the step.
- The reader's ordering of same-date and undated pairs. The only automatic check is the date and commit-time tuple described above.

## Limits
- Tool calls: Bash 17, advisor 1, total 18 of 22 (the hand-back not counted).
- Model calls: about 19 of 28.
- Sub-agents: 0.
- Writes into the real graph: 0.
- Wall clock: the put-back call alone ran about 9.5 minutes, so this run is very likely near or past the 1800 s limit. I did not measure the exact figure.
