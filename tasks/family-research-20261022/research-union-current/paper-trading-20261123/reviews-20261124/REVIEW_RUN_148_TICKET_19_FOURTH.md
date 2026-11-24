# Reviewer run 148 (Opus): ticket 19, the fourth read, Markets bdf4c01

Kept word for word as the agent returned it, 2026-11-24 (twenty-fifth session). Nothing below this line is the main session's.

---

# Reviewer run 148 (Opus): ticket 19, the fourth read, Markets bdf4c01

Commit read: bdf4c01, in the working copy /home/user/Markets-r148 (detached, `git log --oneline -1` = bdf4c01). Diff read: `git diff 29a5123 bdf4c01 -- tools/kgraph/run_record.py tests/agent_program/test_run_record.py`. I also read the last hand-back in BUILDER_RUN_129.md (line 196 on).

Run 144's open list: my first command looked for a "## " heading in REVIEW_RUN_144_TICKET_19_THIRD.md and found none (the file has only the "# Reviewer run 144" heading). I read its lines 15-45 and 170-200 instead, which include "OPEN AFTER THIS READ". The five points I checked are the ones in your brief, and they match that list.

## 1. The checks

`MARKETS_DATA=/home/user/markets-data python3 -m pytest tests/agent_program/test_run_record.py -q --basetemp=/tmp/run148/bt`: **33 passed, 0 failed, 0 skipped.**

## 2. Put-backs

Each was a one-line change (or the stated lines) in a copy of the tree taken with `git archive bdf4c01` under /tmp/run148. Line numbers are at bdf4c01.

| Put-back | Change | Checks that failed |
|---|---|---|
| B1 | `usage[mid]` made `usage[len(usage)]`, :101 | 4 (run 144 had 3): test_figures_run_117_match_the_auditors_measure, test_append_refuses_a_run_that_has_a_line_then_writes_a_correction, test_trap_a_line_whose_figures_differ_from_its_kept_transcript_is_named, test_trap_a_line_with_more_tokens_than_its_transcript_refuses_a_correction |
| B2 | `others.add(uid)` added in the hand-back branch | 3: test_figures_run_117..., test_figures_run_116, test_append_refuses_a_run_that_has_a_line_then_writes_a_correction |
| B3 | :167 and :169 made `if False:` | 2 (run 144 had 3 for its two-line version): test_append_refuses_another_runs_transcript_empty_outcome_and_bad_role, test_trap_a_sentence_naming_another_run_in_front_of_the_brief |
| B4 | `if kept != sha:` made `if False:`, :322 | 1: test_keep_never_writes_over_a_kept_gz_that_has_no_sidecar |
| N1 | :83 made the first number in the whole brief, and :87 `if own:` made `if False:` | 5 (run 144 had 4): test_missing_names_a_live_transcript_that_names_no_run_and_two_that_name_one, test_a_brief_that_names_no_run_is_tied_by_the_agent_id_alone, test_trap_a_sentence_naming_another_run..., test_trap_a_long_sentence_in_front_of_run_119s_brief..., test_trap_a_line_already_on_record_is_compared_with_the_transcript |
| N2 | `enumerate(hb[-1:], 1)`, :295 | 2: test_report_keeps_both_hand_backs_of_run_121, test_trap_a_real_hand_back_followed_by_a_short_one_drops_nothing |
| N3a | the model_replies `elif mine != theirs:` made `elif False:`, :362 | **0, all 33 clean**. No check holds the case where a line's model_replies differs from the transcript's. |
| N3b | the generic `elif mine != theirs:`, :369 | 2: test_missing_complete_line_that_differs_is_not_read_as_lacking_nothing, test_trap_a_line_whose_figures_differ... |
| N4 | `above = f["_text_before_last_hand_back"]` made the longest text, :297 | 1: test_trap_the_pointed_at_message_is_the_last_one_not_the_longest |
| Q1 | agent-id check :164 made `if False:` | 1: test_the_agent_id_must_be_the_transcripts_own |
| Q2 | :180 `if known and known != {agent_id}:` made `if False:` | 2: test_trap_a_long_sentence..., test_trap_a_run_whose_line_holds_another_agent_id_refuses_this_one |
| R1 | the another-run agent-id refusal dropped (line check and plan/sidecar check, 2 lines) | **0, 33 clean** |
| R1, line half only | | 0, 33 clean |
| R1, plan/sidecar half only | | 0, 33 clean |
| R2 | the same-bytes (sha256) refusal dropped, 1 line | **0, 33 clean** |
| R1+R2 | all three lines dropped together | 2: test_one_transcript_is_one_runs_not_two, test_trap_a_long_sentence_in_front_of_run_119s_brief... |
| R3 | model comparison in `_compare_with_line` made `and False:` | 1: test_trap_a_line_already_on_record_is_compared_with_the_transcript |
| R4 | the `len(t) > len(hand_backs[-1])` condition dropped, :325 | 1: test_trap_a_short_text_inside_the_hand_backs_own_message_does_not_displace_the_real_one |

- The builder's "2 failed" for point 1 is the figure with all three lines dropped together. R1 dropped alone leaves 33 clean, and so does R2 alone; each part is covered only because the other refuses the same case.
- One of my sed attempts at R1+R2 changed 0 lines. I discarded it; only the run that changed 3 lines counts.
- I give the count changes against run 144 (B1, B3, N1) as numbers only. I have not traced their cause.

## 3. The five points

### Point 1: one transcript is one run's

Code: run_record.py `_tie`, the block after :180.
- The newest line of every other run is checked for the same agent_id ("its line").
- Every other run's plan and kept sidecar is checked for the same agent_id ("its plan" / "its kept sidecar").
- A kept sidecar's sha256 equal to the transcript's is refused ("already kept as run N").
- Both `append` and `keep` go through `_tie`.

Tried on a scratch copy of the record (`--data /tmp/run148/data`):

| Case | Result | Files written |
|---|---|---|
| Run 107's live transcript as run 108, with run 108's real line and no sidecar (the real record holds no agent_id on 107's or 108's line, and neither has a plan or sidecar) | `append --corrects` and `keep` both rc=2: "run 108's line holds model claude-haiku-5-5, the transcript's models are claude-opus-5-5". The point-2 model check refuses it, not the point-1 rule, and the message does not name run 107. | none |
| Run 107's correcting line written first (rc=0, so the line now holds a374...), then the same transcript as 108 | `append` and `keep` rc=2: "agent id a374a5827c8bc7cc6 is already on record for run 107 (its line), not run 108" | none |
| Run 107 kept (rc=0), its sidecar's agent_id removed by hand, then the same bytes kept as 108 | rc=2: "these bytes (sha256 d51d331e...) are already kept as run 107, not run 108" | none |
| Kept run 109's bytes offered as run 999 | rc=2: "the transcript's brief names agent run 109, not run 999". The brief rule refuses it first. None of the 18 kept sidecars has a tie_note, so I could not try a kept transcript whose brief names no run. | none |
| Run 109 kept again with the same bytes | rc=0: "run 109: the same bytes are already kept; nothing new". A no-op; a file hash snapshot showed nothing written. | none |
| **Open case.** On the real record, 10 runs have a line with model claude-opus-5-5 or none, no agent_id, tokens no higher than run 107's transcript, and no plan or sidecar: 54, 55, 56, 57, 58, 59, 60, 61 among them. | Run 107's live transcript (its brief names no run) given as run 54: `append --corrects x` rc=0, line written; `keep` rc=0, run-0054.jsonl.gz and its sidecar written | the line; run-0054.jsonl.gz and run-0054.json |

Reading of the code, not measured: same bytes always carry the same agentId. `keep` always writes `agent_id` into the sidecar, and the sidecar agent-id check comes before the sha check in the same loop. So the sha refusal fires only for a sidecar that has no agent_id, and `keep` never writes one like that.

Open:
- The rule holds only once the agent id is on record somewhere. Today it is on record for none of runs 107 on (run 144's list said the same).
- Until the main session writes the agent_id lines or keeps the transcripts, an unnamed brief (runs 107 and 108) can be put on an old run's line.

### Point 2: a line already on record is compared with the transcript

Code: `_compare_with_line`, called at the start of both `append` (after `_tie`) and `keep`. It takes the newest line for the run.
- If the line's model is a string starting with "claude-", every "+" part of it must be among the transcript's models.
- input_tokens and output_tokens each must be no lower than the line's.

Tried:
- Run 108's own live transcript as a correction: rc=0, line written.
- Run 107's transcript with every id changed to afresh0000000000, given as 108 on a fresh copy: rc=2, refused on the model.

Open:
- A line whose model does not start with "claude-" is not compared on the model (84 runs lack an exact model).
- test_a_transcript_that_is_run_108s_own_agrees_with_its_line_and_run_107s_does_not asserts only the accept side; `t107` is unused in it (the builder says so too).
- test_trap_a_line_already_on_record... asserts `"model" in err or "input_tokens" in err`. R3 is still caught, because run 107's tokens are higher than run 108's.

### Point 3: `--outside-roster`

Code: `cmd_append`, lines after `_compare_with_line`.
- `--outside-roster` with an `--agent-type` that differs is refused ("exactly one").
- `role` must be one of the four.
- With `--outside-roster`, agent_type is the text as given.

Tried:
- `--outside-roster general-purpose`: rc=0; agent_type "general-purpose", role "reviewer".
- `--agent-type wizard --outside-roster wizard`: rc=0, written. Both options were taken although the message says "exactly one", and "wizard" got past the agent-type check.
- `--outside-roster ""`: rc=0; agent_type fell back to "reviewer" with no refusal.

Run 144 asked for this as "a run by an agent that is not one of the four". Its words are above; I have not set the two accepted cases against any wording beyond that.

### Point 4: `report`, the pointed-at message

Code: :325. `text_before_hb` is the last text before the hand-back that is longer than the hand-back. `report` (:297-298) shows it when the last hand-back is under 600 characters and the text is longer than it.

- On run 124's kept transcript (transcripts/run-0124.jsonl.gz): last hand-back 149 characters; pointed-at text 11,210 characters, opening "## Run 118\n\nReviewer, claude-opus-5-5. Transcript `agent-acd...". It is the same text as the longest.
- Among the 18 kept transcripts and all live ones (de-duplicated by agent id), run 124's is the only one with a last hand-back under 600 characters. There is no other kept run to try it on.
- R4 and N4 are now each held by one check.

### Point 5: tests

- The live-count check (test file :308-331) takes `run` and `agent_id` from the kept sidecars at 7de89a4. It asserts each unzipped transcript's first agentId equals its sidecar's. It no longer reads briefs.
- Two figures are written-in zeros: ":329 ... and 0 name none" and ":331 live transcripts not kept 0;". In this check's set-up they hold by construction, since every live file there is a kept one.
- The counts line now reads "live transcripts N, of which M name one run and K name none" (run_record.py :473-474).
- The separated section starts at test :439. All 9 `def test_` in it open with a "# change:" comment (:454, 470, 493, 515, 547, 557, 572, 615, 627). I checked that each comment is there, not that each is exact. The one I read in the diff for the long-sentence trap now names both of its changes.

## 4. `missing` on the real record

The command wrote nothing; both git status checks were empty afterwards.

COUNTS line as printed:
`COUNTS: runs 145; lacking exact model 84; lacking input tokens 106; lacking output tokens 106; lacking wall clock 30; lacking outcome 0; with a kept transcript 18; lacking something 106, of which a kept transcript could fill 0 and none kept 106; complete and agreeing with a kept or live transcript: 23; complete, a figure differs: 14; complete, no transcript to compare: 2; plan or kept transcript with no line 7; live transcripts 43, of which 41 name one run and 2 name none, live transcripts with no line 4, live transcripts not kept 23; figures that differ 21`

Rows by kind:
- `run` 145
- `DIFFERS` 21
- `NOT KEPT` 23
- `NO LINE` 11 (equal to 7 + 4 in COUNTS; that is a sum, not checked row by row)
- `UNNAMED` 2 (agent-ae63f020e27f3aa06, agent-a374a5827c8bc7cc6)

Since the builder's run (144 runs, 41 live): 1 more run line and 2 more live files. Other sessions' runs have gone on since.

Three rows checked by hand against the record:
- "DIFFERS run 109 | model_replies: the line holds none, transcript 10": run 109's newest line has no model_replies, and its kept transcript gives model_replies 10. They agree.
- "NOT KEPT run 110 | live transcript agent-a961b9f58c36234ce.jsonl is not kept yet": the live file's brief names [110] and its agentId is a961b9f58c36234ce; there is no transcripts/run-0110.jsonl.gz. They agree.
- "NO LINE run 146 | has a plan and no line": run-plans/run-0146.json exists; agent-runs.jsonl has 0 lines for 146. They agree.

## 5. Against "Shown done by"

The ticket: "each run's record has the exact model, input tokens, output tokens, wall clock and outcome; today's runs filled in from their own transcripts, the stopped ones too".

| Part | Record now |
|---|---|
| exact model | 84 of 145 runs lack it |
| input tokens | 106 lack them |
| output tokens | 106 lack them |
| wall clock | 30 lack it |
| outcome | 0 lack it |

- The 106 runs that lack something have no kept transcript.
- Today's runs: 23 live transcripts are not kept, 7 runs have a plan or kept transcript with no line, and 21 figures differ (for example model_replies absent on runs 109 on).
- Filling these in is done with `keep` and `append` on the record. It is not in the code.

For the builder, as measured in this read:
- No check holds N3a (the model_replies value comparison, :362).
- No check holds R1 alone or R2 alone. The sha refusal is reachable only for a sidecar without agent_id, which is a reading of the code (above).
- `--agent-type X --outside-roster X` is accepted with any X, and `--outside-roster ""` falls back to the role.

Whether these go back to the builder is the main session's call.

Commands as at bdf4c01 (from Markets, `python3 -m tools.kgraph.run_record`):
- Keep one finished run's transcript:
  `keep --data <markets-data> --run <N> --transcript <subagents folder>/agent-<id>.jsonl --agent-id <id>`
- Correcting line for a run that was sent back. :249-251: without `--tokens-reported` the earlier line's tokens_reported and tokens_note carry over. `--agent-id` is required and must equal the id on record (:180).
  `append --data <markets-data> --run <N> --transcript <file> --agent-id <id> --role <builder|reviewer|scout|frankie-performance-auditor> --stage "<...>" --task "<...>" --outcome "<...>" --corrects "<what it corrects>" [--tickets <a,b>] [--code-commit <C>] [--agent-type <T> | --outside-roster "<what it was>"]`
  To set a new harness total instead of carrying the old one, add `--tokens-reported <K>`.
- Line of a run that has none yet: the same `append` without `--corrects`, with `--tokens-reported <harness total>` when one is known.

## 6. Clean-up

- /tmp/run148 and /tmp/pytest-of-root are deleted.
- `git -C /home/user/markets-data status --short` is empty.
- `git -C /home/user/Markets-r148 status --short` is empty.

## Speculation (labelled)

- The R1 and R2 parts likely each slipped past alone because every test that offers one transcript as two runs either records the id (caught by the id rule) or keeps the bytes (caught by both). This is not traced line by line.

## Test counts and commit

33 passed, 0 failed, 0 skipped at bdf4c01.

## Open after this read

- For the builder:
  - N3a (:362, model_replies value differs): no check holds it.
  - R1 alone and R2 alone: no check holds either. The sha refusal is unreachable for any sidecar `keep` writes (a reading of the code).
  - `--agent-type X --outside-roster X` is accepted with any X, and `--outside-roster ""` falls back to the role without a refusal.
  - test :329/:331 have the two written-in zeros; the 108 test asserts only the accept side.
- For the main session:
  - Point 1's rule cannot hold until agent ids are on record: run 107's live transcript was accepted as run 54 (line and kept file) on a scratch copy.
  - Write agent_id lines, or keep the transcripts, for runs 107 on.
  - Keep the 23 live transcripts not kept.
  - Write lines for the 7 runs with a plan or kept transcript and no line.
  - Write correcting lines for the 21 differing figures.
  - Decide whether the three builder items above go back to the builder.
- What code cannot hold:
  - Runs 1 to 106 have no transcript kept, and the 106 lacking runs are those.
  - Where nothing on record names an agent id and the brief names no run, the tie rests on the id the main session passes.

## Tool calls

12, counting this hand-back: 9 Bash, 1 Read, 1 advisor, 1 SubagentHandback. No sub-agents, no write into any repository or the real record, no engine, tape or AWS.

Files: /home/user/Markets-r148/tools/kgraph/run_record.py, /home/user/Markets-r148/tests/agent_program/test_run_record.py, /home/user/markets-data/tasks/family-research-20261022/research-union-current/paper-trading-20261123/agent-runs.jsonl, /home/user/markets-data/tasks/family-research-20261022/research-union-current/paper-trading-20261123/reviews-20261124/REVIEW_RUN_144_TICKET_19_THIRD.md
