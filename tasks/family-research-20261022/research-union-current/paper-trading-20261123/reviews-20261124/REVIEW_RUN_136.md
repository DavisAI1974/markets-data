# Reviewer run 136 (Opus): the fourth read of tickets 02 and 03, Markets c832307 and dc44b3a

Kept word for word as the agent returned it, 2026-11-24 (twenty-fifth session). Nothing below this line is the main session's.

---

REVIEW, agent run 136. Fourth read of tools/kgraph/defend.py for tickets 02 and 03. Read-only. Commits read: c832307 (the 11 points) and dc44b3a (the REVISES link), in /home/user/Markets-r136, detached at dc44b3a. All writes went to copies of the graph under /tmp/run136, and that folder is now deleted.

## 1. The checks

- At dc44b3a: `MARKETS_DATA=/home/user/markets-data python3 -m pytest tests/agent_program/test_defend.py -q`. **69 passed in 75.49s.** No error text. This is the first run after the builder's rebases.
- Old code put back: a scratch clone at dc44b3a with defend.py from 3a98333. **18 failed, 51 passed in 66.99s.** These checks did not run clean:
  - test_the_agent_must_be_a_reviewer_by_type_or_by_the_first_word_of_its_role
  - test_a_revision_that_changes_the_falsifiers_says_so_everywhere
  - test_the_said_by_flag_needs_every_word_as_a_whole_word
  - test_a_data_hash_commit_is_stored_resolved_to_its_full_sha
  - test_a_brief_path_that_is_not_a_file_is_named
  - test_verdict_labels_are_refused_with_hyphens_or_wider_gaps, 7 cases
  - test_a_proposer_never_writes_a_line_of_another_runs_link
  - test_the_graphs_source_hash_is_said_when_it_differs_from_the_bytes_read
  - test_a_first_registration_leaves_one_artifact_for_its_claim_file_and_no_revises_link
  - test_the_repository_of_a_claim_file_is_the_checkout_it_sits_under
  - test_a_revision_is_a_revises_link_between_claim_files_and_the_chain_reads_3_2_1
  - test_the_same_claim_file_again_writes_no_artifact_and_no_link
- A first old-code run showed about 40 failures. That was my setup: repo_dirs in tools/kgraph/extract.py:56-62 looks for the platform checkout beside the Markets checkout, and my clone had none. I added a symlink and re-ran, giving the 18/51 above.
- The builder says one existing check failed at its head because CLAUDE.md gained lines. `git diff df7e88c~1 df7e88c -- CLAUDE.md` shows 2 lines added at line 20. The check now finds the line by its words (`_claude_md_line`, test diff around line 260).

## 2. The 11 points

My cases for points 1-3, 5, 6 and 9 were rebuilt from the summary in my task, not copied from the cases in REVIEW_RUN_118.md. Only point 8 was rebuilt as run 118 stated it (its open item 10).

**Point 1, said-by flag**
- Code: `_named_in`, defend.py:277-280. Each `\w+` word of said_by must appear as a whole word, letter case ignored.
- Measured: "G" against "Greg wrote" gives False. "Greg" against "Gregory said" gives False. "Greg Davis" against "Greg said" gives False. "Greg Davis" against "Greg said, then Davis" gives True; the words can be anywhere in the lines, in any order. "G. Davis" against "G Davis" gives True. An empty name gives False.
- On the scratch graph, a cited CLAUDE.md ground with said_by "G" stored `said_by_named_in_lines: False`.
- The check, test_the_said_by_flag_needs_every_word_as_a_whole_word, expects [("e",False),("Greg",True),("Greg 2026-09-16",True),("Greg Nobody",False)] on a real line. That expectation is written out by hand, not taken from the code.

**Point 2, falsifier-change mark**
- Code: defend.py:480-488 carries `falsifiers_changed_at_revisions`; `_falsifiers_line` is at :557-564.
- Measured on a real claim (condition-3): r2 changed the falsifiers, r3 and r4 changed scope only. At r4 the attrs held `falsifiers_changed_at_revisions == [2]` and `falsifiers_changed_from_revision` was absent. `show` printed "the falsifiers differed from the revision before at revision 2". The brief printed "Note: the falsifiers differed from the revision before at revision 2 (what they say is not in this brief)."
- The check asserts [2] and then [2, 4] at rev 4, in the brief, `show` and `undefended`.

**Point 3, data-hash commit**
- Code: defend.py:352 stores the resolved commit.
- Measured: a manifest item typed with commit "HEAD" was stored as dc44b3a7760eb42f2683ca021d7db8bdd74ace0f. `claim_file` kept "HEAD" as typed.
- The check asserts a 40-character sha and the typed prefix kept.

**Point 4, missing --brief file**
- Code: defend.py:695-698.
- Measured: "brief: the file named /tmp/run136/nobrief.md is not there (--brief)". With no `--brief` at all: "brief: the brief file the reviewer was given is required (--brief)".
- The check asserts the path, "is not there", and no "required".

**Point 5, reviewer role**
- Code: defend.py:656-660, `agent_type` when present, else the first word of the role.
- Measured: all ten real "reviewer (read-only)" runs (run:0054 to run:0063) were admitted by `_independent`, and so were ten runs whose role is exactly "reviewer". run:0001 (role "scout") was refused: "...whose agent type, or else the first word of whose role, is 'reviewer'".
- Of the 92 real AgentRuns, 0 have `agent_type`, so the type branch has no real record to check against. The builder says the same.

**Point 6, verdict labels**
- Code: defend.py:103, `[_\s\-]+` between the words of a label, case ignored.
- Refused: "SUPPORTED-WITHIN-SCOPE", "SUPPORTED  WITHIN   SCOPE", "Supported_within-scope".
- Accepted: "the test passed on 3 days", "pass / fail", "Pass/Fail." ("Pass/Fail." with a trailing period is not a whole-value match).
- Refused, as plain prose: "the rule is supported within scope of CL06", "needs more evidence before trial", "it is inconclusive whether". The label words written in lower case inside a sentence count as the label. `\s` now also matches a line break between the words.
- The plan settles only that a sentence holding "passed" or "failed" stays accepted. It does not speak to label words in prose. For Greg to read.

**Point 7, the `written_by == run` clause**
- Code: defend.py:534.
- I removed the clause in the scratch clone and ran the three link checks with `-k`. test_a_proposer_never_writes_a_line_of_another_runs_link did not run clean. The other two, including the older "leaves standing" check, still ran clean. So only the new check holds the clause.

**Point 8, a proposer's ground as its own edge**
- Code: `_own_edge`, defend.py:401-406. It writes a keyed edge when `history[0].written_by != run`.
- Run 118's case. run:0003 wrote the plain SUPPORTS from src:Markets:CLAUDE.md to condition-3. The proposer run:0002 then added that cited ground, and the code wrote a keyed edge beside it. When the proposer dropped the ground, `withdrawn` listed only the keyed edge. run:0003's edge kept one line, its note and no withdrawn mark, and it stays live although the claim no longer rests on that Source. That is what the plan asked ("never rewritten or withdrawn by the proposer").
- A new case, not run 118's. run:0002 registered first and wrote the plain SUPPORTS from the CL06 Source. run:0003 then wrote a second line of that same edge, with attr note="reviewer wrote this". run:0002 then revised with the same ground. The edge's lines are now [run:0002, run:0003 (note), run:0002]. The proposer's revision wrote a new line over the other run's line, and that line's note is not on the current line. Cause: defend.py:405 looks only at `h[0]`, the first writer. No check covers this case.

**Point 9, the Source node's hash**
- Code: `_node_sha`/`_src_note`, defend.py:283-294. `source_commit` and `source_sha256` are set at :505.
- On the scratch graph I wrote a revision of src:Markets:CLAUDE.md holding sha256 of 64 zeros. The real drift there before that: the node held 8d85dc..., the committed bytes hash to 875fc4.... After my doctoring, `show` and the brief each printed one sentence naming both hashes and commit df7e88c.
- From probe 2 on, the CL06 Source in that scratch graph held whatever I wrote. The real CL06 node matched its bytes (f391e6...).
- The seven real claims registered in section 4 produce 0 such sentences in their briefs. None of them cites CLAUDE.md; the three that do were refused.
- The check depends on the real drift of src:Markets:.claude/agents/scout.md. Its own comment says it goes red if the graph is re-read.

**Point 10, docstring**
- c832307: the "cannot see" paragraph gained outcome_seen, who said a line, an artifact carrying reasoning, and data not in git. The stale REVISES / CONTRADICTS line became the CONTRADICTS sentence.
- dc44b3a: added the REVISES paragraph (defend.py:69-72). No check reads the docstring.

**Point 11, BUILD_NOTES**
- tools/kgraph/BUILD_NOTES_DEFEND.md gained one dated line (run 122) correcting line 3's DEPENDS_ON. Nothing was rewritten.
- The run-114 line still ends "Not built yet: a REVISES link on a revision and a CONTRADICTS link". dc44b3a touched only defend.py and the test file and added no dated line saying the REVISES link is now built.

## 3. The REVISES link (dc44b3a, defend.py:409-421 and 506-520, show at :756-762)

**Real claim condition-3, registered by run:0002**
- r1 from markets-data. Revisions r2 (falsifiers changed) and r3 (scope) from copies under /tmp. r4 by a relative path.
- Graph read back: one Claim node. Artifact nodes `artifact:claim-file:reg-323056d84ffe:r1` to `r4`. Each has `repo`, `path`, `version` (an int: 1, 2, 3, 4), `authoring_run` run:0002, `sha256`, `claim` and `claim_file`.
- Links: PRODUCED run to each Artifact, MENTIONS each Artifact to the Claim, REVISES r2 to r1, r3 to r2, r4 to r3. `show` printed the chain.
- `repo`: r1 is "markets-data" with its path inside the checkout. r2 and r3 are "none: read from outside a repository" with the absolute /tmp path. **r4 stored path "c3r4.json", the relative path as typed, with no working folder recorded.**

**The same file again**
- The same file a second time gave unchanged 3 and no new Artifact.
- **A file with the same JSON but other bytes** (re-serialised) gave unchanged 3 and no Artifact. The skip compares the Claim node's content hash (:509), not the file bytes, so a sha256 of those bytes is recorded nowhere.
- **The same file after the graph changed:** after I doctored the Source node (point 9), registering the identical c3r6.json again wrote claim rev 7, Artifact r7 with the same sha256 as r6 (d53da1a8f094...), and a REVISES r7 to r6. Cause: `source_node_sha256` is stored inside `rests_on` in the Claim attrs, so a change elsewhere in the graph makes a new revision. The plan says "the same file again writes nothing".

**check_all**
- On the real graph (a read): 0 messages.
- On a fresh copy: 26 messages, all "MANIFEST.json does not list <path>". The manifest names the real graph's files, so this comes from copying.
- After the scratch writes: [] on every scratch graph.

**A claim registered by the older code, then revised**
- condition-1 was registered with 3a98333 code, then revised with the dc44b3a code. Claim rev 2, one Artifact r2 (version 2), no REVISES, and no Artifact r1.
- **`show` prints "revises nothing (the first claim file)" for r2** (defend.py:761), although it is revision 2.

**Readers of the graph**
- tools/kgraph/store.py:255-262, `_rested_on`: for REVISES it returns `dst`, so the Artifact of N "rests on" the Artifact of N-1. It is used at store.py:176 and :384.
- tools/kgraph/context.py:154 and :239 iterate MENTIONS but keep only `e["src"] in claims`. The new Artifact-to-Claim MENTIONS have an Artifact as src.
- grounding.py: no use of REVISES, MENTIONS or Artifact found.
- Speculation (labelled): if a claim file's Artifact becomes a member of a closed scope, store.py:176/384 would refuse the next revision through REVISES. I did not try it.

**Ticket 25**
- The claim-file ids (`artifact:claim-file:...`) do not share a prefix with `artifact:<repo>:<path>`.
- No other Artifact nodes are in the graph today (0 before my writes).
- Speculation (labelled): if ticket 25 writes `artifact:markets-data:<path of a claim file>` with `version` = a commit sha, the same file would be two Artifact nodes with `version` of two kinds (int revision vs sha string). Any reader sorting by `version`, as `show` does at :757, would meet mixed types if a claim's Artifacts ever mixed. I did not try it.

## 4. The ten real claim files of ticket 01 (scratch graph, proposer run:0002)

**Registered (7):** condition-1, condition-2, condition-3, inference-1, inference-2, inference-3, inference-4c.

**Refused (3), each word for word:** condition-4.json, inference-4a.json, inference-4b.json: "rests_on[0]: the quote is not on those lines word for word (whole words, in a row)".

**Root cause**
- These grounds cite Markets CLAUDE.md lines 381-382 (condition-4, inference-4b) and 187-188 (inference-4a).
- A cited ground is read at the last commit of the path (defend.py:263, `git log -1 -- path`), now df7e88c. The claim file names no commit for a cited ground.
- With whitespace normalised, the quotes now stand starting at lines 386-388 and 192-194.
- After I moved rests_on[0] to those lines, all three were refused at rests_on[1] with the same words. I did not inspect rests_on[1].
- The 3a98333 code refuses condition-4 the same way. The builder's check finds its own CLAUDE.md line by its words, while the real files carry fixed line numbers. The check runs clean and three real files are refused.

**Brief of condition-1** (challenge-brief, then a challenge by run:0054)
- The proposer's mechanism, alternatives and falsifiers do not appear. My test was a prefix match of each.
- In it: the hypothesis, the exact claim, the scope, the boundaries, and the reasoning_files names under "Do NOT open".
- **The proposer's `outcome_visibility.what` is printed in full**, as "registered after an outcome was seen: The page says of the decider: ...". The next ticket takes that out.

**The challenge**
- Gave Evaluation eval:182c363cf310, one EVALUATES link to the claim.
- Rubric: "independent challenge v1: a reviewer who was not given the proposer's reasoning gives at least one competing explanation, one falsifier and the observation that distinguishes them".

**CLI**
- `python3 -m tools.kgraph.defend show --claim claim:reg-70bed7b1dcb9 --data ... --graph-dir <scratch>` printed the claim with all its fields.

## 5. Against the "shown done by" lines

**Ticket 02**
- Observed:
  - A Claim node holding hypothesis, exact claim, scope, mechanism, alternatives, falsifiers, the code commit, the artifact and manifest hashes, and outcome_visibility.
  - One command (`show`) shows it.
  - One Claim node across revisions, with the REVISES chain.
- Does not meet:
  - 3 of the 10 real ticket-01 files do not register today (section 4).
  - "Outcome not yet seen": the real files declare `outcome_seen: true` and register. The code stores the declaration; it does not require false.
  - Same-file and stale-graph cases: section 3.
- Not checked: "before any trial". The code has no trial to order against.

**Ticket 03**
- Observed:
  - The brief holds the claim and the admitted grounds, without mechanism, alternatives or falsifiers.
  - A challenge by a real reviewer run is an Evaluation naming its rubric, linked EVALUATES.
- Does not meet:
  - The brief prints `outcome_visibility.what` in full, which is the proposer's own prose.
  - The brief prints the said-by prose as given.
- Not checked: whether a real reviewer reads only the brief.

## Exact counts and commits

- Tests at dc44b3a: 69 passed (75.49s).
- dc44b3a tests with 3a98333 defend.py: 18 failed, 51 passed (66.99s).
- Clause-removed mutation, `-k` subset: 1 failed, 2 passed, 66 deselected.
- Commits read: c832307, dc44b3a (old code at 3a98333; CLAUDE.md change df7e88c).

## Open after this read

For the builder:
1. `_own_edge` (defend.py:405) decides by the first writer only. A proposer's revision writes a new line over another run's later line of the proposer's plain link, and that line's attrs drop off the current line.
2. The same claim file again writes a new claim revision, Artifact and REVISES when a Source node changed elsewhere, because `source_node_sha256` is inside `rests_on`.
3. A re-serialised file with the same content writes no Artifact, so its bytes' sha256 is recorded nowhere.
4. A relative claim-file path is stored as typed, with no working folder (defend.py:421).
5. `show` says "revises nothing (the first claim file)" for an Artifact of revision >= 2 whose earlier revision was written by the older code (defend.py:761).
6. BUILD_NOTES still says "Not built yet: a REVISES link"; dc44b3a added no dated line.
7. Three real ticket-01 files are refused: the cited CLAUDE.md lines moved, and defend.py:263 reads the last commit of the path, not a commit named in the claim file.

Settled by the plans:
8. A refusal is kept for any id typed, with or without a run.
9. A sentence holding "passed" or "failed" is not a label.
10. A run whose first role word is "reviewer" is admitted.

For Greg:
11. Lower-case label words inside ordinary prose ("supported within scope", "inconclusive whether") are refused.
12. The brief prints `outcome_visibility.what` and the said-by prose in full (the next ticket takes the first out).

What code cannot hold:
13. outcome_seen is the proposer's word.
14. Who said a cited line.
15. Whether the artifact itself carries reasoning.
16. Data not in git.
17. One agent under two run numbers.
18. The `agent_type` branch has no real record (0 of 92 AgentRuns).
19. The point-9 check rests on the real drift of src:Markets:.claude/agents/scout.md.

## Housekeeping

- /tmp/run136 (with its scripts and the platform symlink) and /tmp/pytest-of-root are deleted. /home/user/paper-trading-platform is intact.
- `git -C /home/user/markets-data status --short` and `git -C /home/user/Markets-r136 status --short` both printed nothing. Markets-r136 is still at dc44b3a.
- Nothing was written to markets-data graph/. No engine, tape or AWS was touched.
- One search was made: the grep for `def repo_dirs`, used to fix my old-code clone setup.

Tool calls: 20 Bash, of which one failed on an import error and was re-run; 1 advisor; and this SubagentHandback. 22 in all. The 22-call limit is reached.
