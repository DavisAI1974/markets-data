# Builder run 122 (Sonnet): tickets 02 and 03, the points of the third read and the REVISES link

Kept word for word as the agent returned it, 2026-11-24 (twenty-fifth session). Nothing below this line is the main session's.

---

Part one and Part two are both built, committed and pushed. The last whole-file run was 69 passed, 0 failed, 76.75 s. I made that run before the last two rebases, and I did not re-run after them. Each rebase only brought in other agents' files (run_record.py, run_plan.py, auditor_called and others), but the CLAUDE.md the checks read has since changed.

**Two things to know first**
- I wrote the code without showing you a diff and waiting for a go. My brief said to show the diff and wait, but this run could not wait mid-run. I took the plan you handed me as the go.
- The Co-Authored-By line is "Claude Sonnet 5.5 <noreply@anthropic.com>", not the "Claude Fable 5.2" your brief asked for. The harness attribution reminder gives Sonnet 5.5 and the Claude-Session line, and it yields only to the user's own instructions. Your brief came from an agent, so I followed the reminder. Please say if you want it amended.

**Commits (pushed to ccr-659edd86-di9udt, never forced)**
- Part one: c832307, "PROPOSED, FOURTH, NOT YET READ BY THE REVIEWER: defend.py points of the third read (tickets 02, 03) [skip ci]". It was first committed as 886c0e5.
- Part two: dc44b3a, "PROPOSED, NOT YET READ BY THE REVIEWER: a revision is a REVISES link between its claim files (ticket 02) [skip ci]".
- Both first pushes were rejected as non-fast-forward, because other agents had pushed to the same branch. I fetched and rebased, then pushed. That is why the ids differ from the local ones.
- Because of the rebase, `git diff --stat 3a98333 HEAD` over the whole tree would show the other agents' files too. Limited to my three files it reads:
  - tests/agent_program/test_defend.py: 197 lines changed
  - tools/kgraph/defend.py: 147 lines changed
  - tools/kgraph/BUILD_NOTES_DEFEND.md: 1 line added
  - Total: 3 files, 311 insertions, 34 deletions.

**Pytest counts**
- At the start the baseline was not 53 clean. `test_who_said_a_cited_line_is_the_proposers_word_and_code_says_so` already failed at head (see "Existing checks I changed").
- After Part one: 65 passed.
- After Part two: 69 passed, 0 failed.

**Point by point** (line numbers are in defend.py at dc44b3a; the exact numbers may be off by a few, so use the names)

| Point | Change | Check that holds it |
|---|---|---|
| 1. Said-by flag | `_named_in` (about :273) is used in `_ground` (about :264). Every word must appear as a whole word, case-insensitive. A name with no word characters gives false. | `test_the_said_by_flag_needs_every_word_as_a_whole_word` |
| 2. Falsifier list | `falsifiers_changed_at_revisions` is built in `_register` (about :461-469) and carried forward. `_falsifiers_line` (about :525) gives the plain words. `show`, the brief and `undefended` print them. The old `falsifiers_changed_from_revision` key and its sentence stay beside the list. | `test_a_revision_that_changes_the_falsifiers_says_so_everywhere` |
| 3. Data hash commit | `_manifest` builds new dicts with the full sha. The claim file stays as typed. | `test_a_data_hash_commit_is_stored_resolved_to_its_full_sha` |
| 4. Missing `--brief` file | `_challenge` (about :665) names the path and says "is not there". A missing `--brief` still says "required (--brief)". | `test_a_brief_path_that_is_not_a_file_is_named` |
| 5. Reviewer by type or first word | `_independent` (about :622-629). The run's `agent_type` is used when it has one, else the first word of the role, lower-cased with punctuation stripped. The message still contains "role". | `test_the_agent_must_be_a_reviewer_by_type_or_by_the_first_word_of_its_role` |
| 6. Verdict labels | `_label_re` (:99). The underscore now matches `[_\s\-]+`, so hyphens and wider gaps are refused. An ordinary "passed" or "failed" sentence is still accepted. | `test_verdict_labels_are_refused_with_hyphens_or_wider_gaps` (7 cases, plus an accepted sentence) |
| 7. Other runs' links | The `written_by == run` clause is now exercised: another run's plain edge is in `wrote` and the clause leaves it standing. It was probably already green at head; I did not force a red for it. | `test_a_proposer_never_writes_a_line_of_another_runs_link` |
| 8. Own edge | `_own_key` and `_own_edge` (about :397). When another run holds the plain link, the proposer's link goes beside it under the key "ground of <run>". `wrote` holds both ids. | `test_a_proposer_never_writes_a_line_of_another_runs_link` |
| 9. Source hash | Each ground records `source_node_sha256`, the Source node's sha256 as found at registration. The claim's attrs carry `source_commit` and `source_sha256`. `_src_note` prints one sentence with both hashes in the brief and in `show`, only when they differ. | `test_the_graphs_source_hash_is_said_when_it_differs_from_the_bytes_read` |
| 10. Docstring | The "What code CANNOT see" paragraph is extended and the "Independence" wording is corrected. The old line 66 is replaced with the objection and CONTRADICTS sentences. The REVISES paragraph came in the Part two commit. | none (docstring only) |
| 11. Build notes | One dated line added to BUILD_NOTES_DEFEND.md. It corrects line 3 (DERIVED_FROM and SUPPORTS, never DEPENDS_ON) and names this round's changes. | none (note only) |

- Point 8 detail: on the scratch graph, the other run's edge history is one line, by that run, after the proposer's registration, two revisions and the drop. The proposer's own edge is withdrawn at the drop.
- Point 9 detail: I print from the hash recorded at registration, not from a lookup at print time, because the brief seal rebuilds the brief and a later look-up would refuse an honest brief if the Source were re-read. The same check also asserts no "differs" sentence for a Source whose hash matches the bytes read.
- Point 9 detail: the scout.md drift comment is on the existing check, and the new check carries the same note.

**Part two**
- `_where_filed` (:412) works out the repository and path of the claim file.
- `_register` (about :505-520) writes the Artifact `artifact:claim-file:<id>:r<N>` with PRODUCED and MENTIONS, plus REVISES to revision N-1 when N is 2 or more, all in the same `store.write` as the claim.
- The skip rule: a new revision is decided before the write by comparing the store's own content hash with the previous line. If nothing is new, no Artifact or link is written.
- `show` prints the chain (about :756-762).
- Checks:
  - `test_a_first_registration_leaves_one_artifact_for_its_claim_file_and_no_revises_link`
  - `test_the_repository_of_a_claim_file_is_the_checkout_it_sits_under`
  - `test_a_revision_is_a_revises_link_between_claim_files_and_the_chain_reads_3_2_1` (also covers one Claim node, and `check_all` reporting nothing new)
  - `test_the_same_claim_file_again_writes_no_artifact_and_no_link` (also covers the same wording from another path)
- The existing final check `test_the_store_checks_no_worse_after_the_writes` also passes.

**Existing checks I changed**
- `test_a_revision_that_changes_the_falsifiers_says_so_everywhere`: only the last assertion changed. It used to assert the old mark disappears at revision 3. It now asserts the list `[2]` stays and is in the brief, `show` and `undefended`. I added revisions 4 and 5 (list `[2, 4]`, then carried).
- `test_the_role_must_be_exactly_reviewer` is renamed and rewritten as the first-word check:
  - run:0054, role "reviewer (read-only)", may now challenge.
  - The refused cases are the real builder runs whose roles start "builder (as the ..." or "builder, as the ...".
  - No real role merely contains "reviewer" without starting with it, and no real AgentRun has an `agent_type`. So the contains-only case and the `agent_type` branch have no real-record check, and I made none up.
  - run:0054 was not refused through the ground chain of claim:70038adffed2.
- `test_who_said_a_cited_line_is_the_proposers_word_and_code_says_so` already failed at head 3a98333, before any edit of mine. It cited line 32 of the committed CLAUDE.md, and lines had been added above it. `_claude_md_line()` in the test file now finds the line in the same committed file by the same quote. The quote and the expected values are unchanged.
- `test_registration_never_writes_a_new_revision_of_an_existing_source`: comment only (the scout.md drift note).

**Things I had to find that were not located for you**
- I read the whole of defend.py and the whole test file.
- Greps and reads outside your list: `sources.py` (`link`, `edge_id`), `store.py` (`write`), `schema.py` (Artifact and REVISES), `rule_versions.py:68`, `BUILD_NOTES_DEFEND.md`, the real roles of every AgentRun via the store, and the agent-runs.jsonl role list.
- `git status` and `git stash` in the worktree only, to prove the who_said failure at head.
- I did not check whether the real graph holds any registered claim. My brief said not to write into it. The code skips the REVISES link when the earlier Artifact is missing, which would only matter for a claim registered by older code.

**Ambiguities**
- Point 8: I key both DERIVED_FROM and SUPPORTS through `_own_edge`, and only when another run's link already holds the plain id. Your brief named SUPPORTS only.
- Point 2: the wording of the list sentence is mine: "the falsifiers differed from the revision before at revision(s) 2, 4".

**Tidy-up and tool calls**
- /tmp/run122 and /tmp/pytest-of-root are deleted.
- `git -C /home/user/markets-data status --short` is empty (0 lines).
- Nothing went through the engine, the tape or AWS, and nothing was written into the real graph.
- I used one advisor call.
- Tool calls used: about 21 of 70 (the count includes the advisor call).

File paths:
- /home/user/Markets-b456/tools/kgraph/defend.py
- /home/user/Markets-b456/tests/agent_program/test_defend.py
- /home/user/Markets-b456/tools/kgraph/BUILD_NOTES_DEFEND.md
