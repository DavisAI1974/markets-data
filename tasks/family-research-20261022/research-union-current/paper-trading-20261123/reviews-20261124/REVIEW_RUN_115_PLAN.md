# Reviewer run 115 (Opus): the plan for tickets 03b, 04, 05 and 06, read before the builder starts

Kept word for word as the reviewer returned it, 2026-11-24 (twenty-fifth session). Nothing below this line is the main session's. What the main session changed for each of its 22 points is in `../tickets-44-20261124/PLAN_03b_04_05_06_v2.md`.

---

REVIEW, AGENT RUN 115: the plan for tickets 03b, 04, 05 and 06, read before the builder starts

Plan read: /home/user/markets-data/tasks/family-research-20261022/research-union-current/paper-trading-20261123/tickets-44-20261124/PLAN_03b_04_05_06.md. Line numbers below are from that file (P:n). Where the changed section (P:116-158) differs from the lines above it, the changed section is the one I read as standing.
Code read at Markets 2ac873f (`git log --oneline -1`): tools/kgraph/schema.py, store.py, defend.py, context.py and grounding.py, read in parts.
What I ran against the real records (read-only):
- markets-data `paper-trading-20261123/agent-runs.jsonl`: 119 lines, highest run 117, 22 distinct free-text `role` strings. It has one auditor line, run 111, with `audits` [1..109].
- markets-data `graph/`: 0 Claim lines carry `registration`. There is no CONTRADICTS edge file and no REVISES edge file.
I did not run `python3 -m tools.kgraph.grounding`. AGENTS.md: my grep for rank/label/average/pool/made-up returned only line 31 (HOLD; "rank" matched inside "Frankie"), so I cite no AGENTS.md line for ranking or labels.

---------------------------------------------------------------
TICKET 03b (the auditor is called on every run)

1. What "Shown done by" asks (03b.md:16), and what in the plan meets it
- "the rule in the three places named": P:33-34 (CLAUDE.md Agent roles, the auditor's file, the read-first page marked "(done)").
- "the check command run on the real agent-runs.jsonl, printing no unaudited run of the scout, the builder or the reviewer from run 107 on": P:26-32, P:35. The plan does not say the command is run on the real file at its current state as the shown-done evidence. Measured: run 111 audits only 1..109, and the file reaches run 117, so as it stands today the command would list runs 110 and up.
- "naming truthfully the runs before 107 that only run 111's audit of the whole record covers": nothing in the plan meets this. P:31 prints only the runs that no auditor line names. Runs 1-106 are named by run 111, so they would print nothing at all, and nothing marks them as covered only by the whole-record audit.
- "a check on the real record that a run line added with no auditor run naming it is listed and fails the command": P:36 does something different. It cuts the real file off before the first auditor line; it does not add a run line. Close, but not the ticket's case.
- "the auditor's reports in git": nothing in the plan. The ticket's body (03b.md:8) also asks for "the auditor's report for each of its runs kept in git word for word".
- Not in "Shown done by" but in the ticket body (03b.md:7): "The check runs before any ticket's box is marked and at the close of every session; a box is not marked while a run that worked on that ticket is unaudited." Nothing in the plan ties a ticket's box to the runs that worked on it.

2. What the plan builds that the ticket does not ask for
- P:29-30 ("Every other run is one that needs an audit, whatever its role") goes wider than the ticket's "every run of the other three". The real file has roles 'main session', 'web-fetch' and 'claude-code-guide'. The token plan (adoption plan:47-48, "Every agent run is recorded") supports measuring every run; the ticket's words name only the three.
- P:151-153 (changed point 3) adds an "outside the roster" listing that no ticket asks for.

3. Rules (item d: an auditor line that only names run numbers)
- The case: P:28-29 makes `audits`, a bare list of run numbers, the only thing the check reads. An auditor line that names run numbers clears those runs whether or not the auditor read anything. Run 111's line is exactly that shape: a range 1..109 with nothing tying each number to a row.
- What the rules say: the ticket asks for "each run its own row, against the limits told to Greg before it started" (03b.md:6, 10). The amendments (Integration rule 3, CODEX_PROMPT_AMENDMENTS:28-29) say "Auditor findings are source-tagged claims".
- What would hold it (a suggestion, not in any source): the auditor line also names its report as repo:path@commit, and the check confirms that each audited run number has its own row in that file at that commit. Or the rows become AgentRun/Metric entries, per rule 3, and the check reads those.
- `corrects` (P:27-28): with "the newest stands", a correcting line for an auditor run that carries a shorter `audits` list silently un-audits runs. That follows from the rule as written; the plan has no check for it.

4. Ambiguities the builder would have to decide
- P:152-153: is a run "outside the roster" counted in the failing exit code or listed apart? And how is "outside the roster" read from 22 free-text role strings? Examples: 'builder (as the reader)', 'scout (general agent on Haiku with the scout's brief)', 'reviewer (read-only)'. Options: match a prefix of `role`; read `agent_type`, which exists in the file; or a fixed table of the 22 strings.
- Where do "the limit told" and "the figure reached" (P:31-32) come from? Options: the line's `budget_tokens` / `tool_calls`; `run-plans/run-NNNN.json` (P:154-158, from run 114 on); or both. Before 114 there is no run-plan JSON.
- Are auditor runs themselves audited? P:29 leaves them out.

5. Schema: none needed for 03b.

---------------------------------------------------------------
TICKET 04 (nothing keeps the outcome from the challenger)

1. What "Shown done by" asks (04.md:9), and what in the plan meets it
- "the code hands the after-the-fact record to a challenger only once the challenge is on record": P:42-53 builds a new door, `defend outcome`.
- The ticket's own "What is missing" (04.md:3) names the code that hands it today: "the proposer is handed the last trial's after-the-fact record". P:61-66 leaves exactly that code outside the door: `tools/ratchet/file_proposer.py` `kept_records` (lines 103-121; scout 112 reports that brief lines 138-144 also list each earlier trial's status, hypothesis and figures) and the afterwards brief.
- So, built as written, the code that hands the record today still hands it, and the door covers a path no existing code goes through. The plan's stated limit leaves the ticket's own named case unmet.
- "and a check proves it": P:57-60.

2. What the plan builds that the ticket does not ask for
- `outcome_records` on the claim file (P:54-56), with registration refusing a claim whose artifact or ground is one of them. The ticket asks only about who is handed the record and when.
- Release Task nodes and `defend show` listing releases (P:50-53). These serve the "a check proves it" record; they go a little wider than the ticket.

3. Rules (item a: can a challenger still reach an outcome?)
- (i) The brief. `defend.py:422-424` and `440-442` put the proposer's free-text `outcome_visibility.what` into the brief whenever `outcome_seen` is true. The plan keeps only `outcome_records` out of the brief. The `what` text can state the outcome itself, and the ticket-04 door does not touch it.
- (ii) `defend show` (`defend.py:548-590`) is not gated by run. It is "the proposer's side: never given to the reviewer" only by docstring (`defend.py:12`). The plan adds releases to it (P:53), each with every record's repo, path, commit and sha256 (P:51-52). A reviewer run that types `defend show` gets the paths of every released outcome record.
- (iii) The graph files. `outcome_records`, if stored on the Claim node, is in markets-data `graph/nodes/Claim.jsonl`, which any agent can read. The release Task nodes are there too.
- (iv) What tickets 05 and 06 add is not gated by 04's door: the Evaluation's `what_was_observed`, `falsifier_observation_seen`, the counter Claim (its text is `what_was_observed`, P:93), the OPEN CONFLICTS section of the session text (P:97-101), the "checked, with how many falsifiers were seen" place-in-process line (P:144-146), the checker's stated confidence (P:139-140), and grounding's "N claim(s) contradict this one" (`grounding.py:209-212`).
  - The concrete case is the plan's own second reviewer (P:59-60). A second reviewer run with no challenge of its own is refused by the door. But the session text it starts from (`tools.kgraph.context`, the CLAUDE.md "agent program" section) shows the open conflict, the counter claim's words and "checked, N falsifiers seen", all of which carry the outcome.
- (v) Revisions. The door checks only for a challenge of the CURRENT revision. Suppose a reviewer run is released the outcome after challenging revision 1, and the proposer then registers revision 2. `challenge()` (`defend.py:503-541`) does not look at earlier releases, so that same run can challenge revision 2 having seen the outcome. Nothing in the plan refuses that or marks it.
- (vi) `outcome_records` is declared by the proposer. A claim file that omits the key gets no brief-side protection. The plan has no check of it against the trial folders.
- (vii) Who counts as a reviewer. "a run whose role is the reviewer's" (P:46) rests on the open run-107 point: "a reviewer is any run whose role holds the word" (`defend.py:499-500`). A run whose free-text role does not contain "reviewer" takes the "any other run" branch (P:48) and is released once any challenge exists.
- Verifier plan line 90 conditions the blinding: "when the research design requires a blind comparison". The plan applies it to every claim. That is stricter than line 90 and does not break it; I note it only.

4. Ambiguities
- Are the gated readers in (iv) behind the door, or shown to everyone? Options: gate the session text's conflict section and the place-in-process line by run (context.py has no run argument today); accept them as ungated and say so in the ticket next to P:61-66; or show "a check is on record" without what was observed.
- Does `defend show` print the release's record paths, or only who and when? P:53 says "who was handed the outcome, when"; P:51-52 says the Task node holds paths and hashes.
- Ticket 05's checker needs the outcome records. Must it get them through `defend outcome`? P:70-87 never connects the two, so a check can name any repo file as an input with no release on record.

5. Schema: `outcome_records` is a new claim-file key. `defend.py:90-94` (`CLAIM_KEYS`) refuses unknown keys, so `defend.py` changes; `schema.py` does not, because `check_node` (`schema.py:99-136`) has no attribute allowlist. P:21 says "no new ... field". The key is a new field of the Claim contract even if `schema.py` is untouched.

---------------------------------------------------------------
TICKET 05 (a check is written after a trial)

1. What "Shown done by" asks (05.md:9), and what in the plan meets it
- "for each registered falsifier a check line": P:72-73, one entry for EACH falsifier, refused if one is missing (P:76).
- "what was looked at, what was observed, what stays open": P:74, `what_was_checked`, `what_was_observed`, `what_remains_open`.
- "with the inputs' hashes": P:71, P:81-82.
- "and the reviewer": P:82, `reviewer` = the run.
- "built and checked without the engine": P:86-87.
- "shown on a real trial at the first pass on tape": P:87, deferred to Greg's go (ticket 40). That matches 05.md:5.

2. What the plan builds that the ticket does not ask for
- `falsifier_observation_seen` (P:75).
- Per-step confidence (P:137-141).
- `defend unchecked` (P:84). This is small; it is the twin of `undefended`.

3. Rules (item b)
- Is `falsifier_observation_seen: yes / no / not determined` a verdict label?
  - The banned list in `defend.py:86-88` does not hold yes, no or "not determined".
  - Amendments Task 2 item 4 (CODEX_PROMPT_AMENDMENTS:68-71): "Flag where `SUPPORTED_WITHIN_SCOPE` / `REFUTED_WITH_EVIDENCE` style labels appear and propose descriptive status fields (what was checked, what was observed, what remains open)".
  - The field is a three-way categorical summary of `what_was_observed` against the registered `expected_observation`, per falsifier. "yes" carries the same information as a per-falsifier REFUTED_WITH_EVIDENCE, and it is the trigger for code to write a CONTRADICTS link (P:91-96).
  - Whether that counts as "style" is Greg's reading. The rule's own example ("descriptive status fields ... what was observed") is already met by the three plain fields without it.
  - For a model-assisted check, the "yes" is a model's judgement that causes a graph write. Verifier plan line 101: "deterministic evidence adjudicates, and unresolved interpretation goes to human review".
- Per cell. One yes/no per falsifier has no per-cell or per-event slot. CLAUDE.md ("Per-cell always, never pool ... Report 'works on {X}, not {Y}'") and verifier line 17 ("No averaging ... pooled headline obscures event/cell distinctions"). A falsifier seen on 2 of 40 events becomes one "yes" unless `scope`/`exceptions` carry it. The plan does not say which.
- "the proposer does not write its own check" (P:77) matches verifier line 62 ("an independent reviewer identity" per check) and line 48. The plan does not require the checker to be the reviewer.
  - Amendments rule 2 (CODEX:20-25): "independent review goes to the reviewer ... any deterministic checks it later needs are built by the builder".
  - So under P:77 a builder or scout run may write a model-assisted check. Whether that is allowed is not settled in the plan (see 4).
- "an independent challenge first" (P:78) matches the verifier's flow (lines 37-44: registration, then a reviewer isolated from the proposer's rationale, then the counterexample plan, then checks) and line 90.
- Revision binding. P:72-73 and P:81 take the falsifiers and `claim_revision` from the CURRENT revision at check time. If the proposer registers a new revision after the trial and before the check, `expected_observation` is copied from falsifiers written after the outcome existed. Nothing binds the check to the revision that was current when the trial ran, and P:78's ordering is not enforced against revision. Verifier line 56 ("immutable revision ... preregistered falsifiers") is the rule this touches.
- The label refusal (P:79, `_label_re` at `defend.py:89`) applied to the whole check file would refuse a verbatim quote in `observed_at` (P:91-92) whose source text contains "failed", "rejected" or "passed". A real log line is the concrete case. The quote is evidence, not the checker's framing.
- Confidence: see the changed point 2 below.

4. Ambiguities
- Who may write a check: any run that did not register the claim (P:77), or only a reviewer-role run (verifier 62, amendments rule 2)?
- Which revision's falsifiers does a check answer: the current one at check time, or the one current at the trial? The trial is not tied to a claim yet (P:64-65), so there is no stored link to say which.
- How does a check say "seen on some events, not others": one entry per falsifier with a per-event list in `exceptions`, or more than one entry per falsifier?
- What makes a check's inputs real records here? The real graph holds 0 registered claims and no challenge, so the scratch checks must register a claim and write a challenge themselves. Which real file is the claim's artifact, and which run writes the challenge?

5. Schema: `falsifier_observation_seen`, `observed_at` and confidence are new Evaluation attributes. `schema.py` accepts them (no attribute allowlist). P:21's "no field" is not what is built.

---------------------------------------------------------------
TICKET 06 (adverse evidence on record) and TICKET 26

1. What "Shown done by" asks, and what in the plan meets it
- 06.md:9, "evidence against a claim is a CONTRADICTS link in the graph": P:91-96 (from a check) and P:129-133 (from a sourced objection).
- "both standing": P:96. `context.py:202-205` already keeps a contradicted claim unmoved.
- "the session text shows open conflicts": P:97-101.
- 26.md:9, "a section of open conflicts that shows a CONTRADICTS link when one exists": P:97-101.

2. What the plan builds that the ticket does not ask for
- Writing CONTRADICTS from a reviewer's objection (P:129-133).
- Showing each claim's place in the process (P:144-146). That comes from Greg's decisions log (decisions:7453-7465), not from ticket 06.

3. Rules (item c)
- Write rule 1 for the counter Claim.
  - Code: `schema.check_node` (`schema.py:117-119`) needs `source`, `line_start`, `line_end` and `quote` when `inference` is false. `store.write` (`store.py:186-190`) needs `source` to be a NODE ID of the graph. `store.py:193-197` (and `check_all` at 373-374) needs a SUPPORTS link from that source to the claim.
  - The plan (P:94) says "its source the input file with those lines and quote". It names no Source node and no SUPPORTS link. Built as written, the write is refused. Built with a Source node made as `defend._source_at` does (`defend.py:177`) and a SUPPORTS link, it is accepted.
  - The text of the counter claim is the checker's `what_was_observed` (P:93), marked `inference: false`. The quote is the source's words; the text is the checker's reading of them. For a model-assisted check, that text is a reading tied to a quote, not the quote. Write rule 1 (adoption plan:95) separates "has a source" from "marked inference". The plan marks it "not an inference" whatever the check type.
- Taking a link back. P:100 says "A link taken back (`resolve undo`, with its reason)". `resolve.undo` (`resolve.py:264-269`) refuses any edge that is not RESOLVED_TO: "{edge} is not a merge of the graph". Built as written, a CONTRADICTS link cannot be taken back by that command, and the plan names no other command and no rule for who may take one back.
- Can the section crowd out the budgeted sections?
  - Code: `SECTION_SHARES` (`context.py:73-81`) holds the shares; `room = max(0, budget_chars - fixed - ...)` (`context.py:451-453`). The trim loop (`context.py:501-508`) only removes lines from the budgeted sections.
  - The plan: OPEN CONFLICTS is "shown ahead of the budgeted sections and counted in the budget" (P:98-99), with no share and no cap. That makes it part of `fixed`.
  - The case: enough live CONTRADICTS links (a refute wave, `tools/swarm/refute.py:150-165`, also writes them) leave `room` at 0, every other section empty, and the text still over budget, because the trim loop cannot shorten the conflict section.
  - The adoption plan, 5a (line 134-135): "include ... open conflicts, serialize within the declared token budget".
- "both stand": the CONTRADICTS link the plan describes carries the check id and falsifier number (P:95-96) but not the claim revision it was written against. After a later revision, the link still points at the stable id, and nothing says it was against an earlier wording.

4. Ambiguities
- Who may take a CONTRADICTS link back, with what command? Options: a new verb in `defend`; widen `resolve undo` (that changes its contract); or none, so the link stays.
- What is the counter claim's `inference` value for a model-assisted check: false, as P:94 says, or true with the quote as its ground?
- How large is the OPEN CONFLICTS section allowed to be? Options: a share added to `SECTION_SHARES`; one line per link with a cap and a "N more" foot like the existing footer (`context.py:405-413`); or uncapped and not counted.

---------------------------------------------------------------
THE CHANGED SECTION, POINT 1 (item e): the frozen wording and the REVISES link

- Is every superseded object addressable today? Every earlier revision is already addressable: `store.history(id)` returns every line ever written, "Nothing is ever lost" (`store.py:114-117`), and `defend show` prints each revision's falsifiers with time and writer (`defend.py:561-564`). Adoption plan:97: "every superseded object stays addressable". The plan's frozen node copies what is already addressable.
- The frozen node is not the wording as it was. Its store line carries the copier's `written_by` and a new `written_at` (`store.py:219-220`), not the original revision's. "as they were" holds for the attrs only if the attrs copy the original line's time and writer by hand.
- Which write rule it breaks.
  - The rule: `store.write`, `store.py:193-197` ("Claim {id}: no SUPPORTS link from its source").
  - The case: a frozen copy of a not-inference registered claim has `inference: false` and a `source`. The write is refused unless a SUPPORTS link into `<id>#r<N-1>` is written in the same batch. The plan writes only REVISES (P:125-126).
  - Adding SUPPORTS links duplicates the grounds of every revision on a second node. `grounding.check_claim` then finds paths on it too.
  - For an inference claim, the copy has no DERIVED_FROM, so `grounding.py:197-201` returns "revise" for the frozen node.
- Which readers would count it as a second live claim. "holding that revision's fields as they were" includes `registration`, `proposer_run` and `exact_claim`.
  - `defend._registered` (`defend.py:408-412`) accepts any Claim whose `registration` matches. So `challenge-brief`, `challenge`, `show`, and the planned `outcome` and `check` all accept `<id>#r1` as a registered claim; a challenge, release or check could be written against a frozen wording.
  - `defend.undefended` (`defend.py:593-600`) lists every registered Claim with no challenge at its own id. `<id>#r1` has none, so it is listed. The plan names `undefended` as one that will skip it (P:124-125).
  - `context.build` (`context.py:186-187`) takes every Claim node as `live`. The frozen copy lands in its statement-kind section beside the live claim and counts in the footer's "N claims not shown". The plan names the session text (P:124).
  - `grounding.check_text` (`grounding.py:289`, `332`) and `grounding.check_all` (`grounding.py:389`) iterate every Claim. They are NOT named in P:124-125.
  - `store.check_all` (`store.py:357-392`) checks every Claim against write rule 1 (the SUPPORTS case above).
  - The plan says "marked so that it is never listed" but names no marker field and no reader beyond three.
- `_rested_on` (`store.py:255-262`) treats REVISES as "rests on" its dst. A REVISES link into a frozen node that someone later puts in a closed scope would be refused (`store.py:170-185`). This is speculation about a future case only.
- Revisions under confidence. If the confidence lines (point 2) are stored on the Claim node, each new line is a new store revision (`store.py:207-221`). Each one:
  - makes every challenge "not at the current revision" (`defend.py:598`, `588-589`);
  - makes the brief header no longer match a brief already handed out (`defend.py:511-512`);
  - fires point 1's "on registering revision N write `#r<N-1>`" if the trigger is a store revision rather than a registration;
  - is refused at `defend.py:364-366` if the reviewer or checker is the writer ("only {proposer_run} may revise it").
  The plan does not say where the confidence lines are stored.
- Is "an objection that states evidence with its source is a refutation" what the sources say? 4a-bis (adoption plan:105-107) says "a refutation a CONTRADICTS edge"; it does not say what is a refutation. Verifier line 78 lists "adverse cases" and "unresolved objections" as separate things a verdict links, and does not say which one a sourced objection is. Verifier line 101: "deterministic evidence adjudicates, and unresolved interpretation goes to human review". Line 48 says the independent reviewer "owns critiques, alternative explanations and falsifiers", not adjudication. Nothing I read says that a reviewer's objection with a source, made before any trial, is a refutation. Three further points:
  - `CHALLENGE_KEYS` (`defend.py:95-96`) has `objections` as text. A structured objection with file, lines and quote is a new challenge-file shape.
  - The plan does not say what node the CONTRADICTS link from an objection starts at (a counter Claim? the Evaluation?). `check_edge` has no type pairing (scout 112), so either is accepted.
  - The label refusal (`defend.py:89`) would refuse an objection whose quoted source text holds "failed" or "rejected".

---------------------------------------------------------------
THE CHANGED SECTION, POINT 2 (item f): CONFIDENCE

- What Greg said (ROOT_GAMEPLAN_DECISIONS.md:7480-7493): "Don't we have different strps that it has to pass like being contested and proving validation before it makes it through? And after that it's just scored confidence wise correct?" and "Wverything stays as a.possibility. it's a matter of 0 confidence or highly confident". His order is: steps first, then a confidence score. The plan has a confidence stated at registration by the proposer (P:139), before the claim is contested. That is not in his words.
- The proposer's registration confidence reaching the reviewer. Verifier line 98: "Give the reviewer claim/specification + sealed admissible evidence, without feeding it the proponent's conclusions first". If the proposer's confidence is in the brief or the session text (P:144-146 shows "the confidences stated for it" for every claim), the reviewer is handed the proponent's conclusion. The plan does not keep it out of the brief or the session text.
- Everything the zip and plans say about confidence (grep for confidence|score over all three files):
  - adoption plan:25, "Confidence cutoffs in fan-out reducers are allowed."
  - adoption plan:118, entity-resolution merges keep "confidence";
  - adoption plan:145 (stage 6, the swarm), "confidence cutoff on what goes to review, Opus or Sonnet refute wave on what passes";
  - verifier:43, "no agent vote or score averaging";
  - verifier:50, the verifier sits "after claim formation and before promotion of scientific confidence";
  - verifier:78, "No aggregate acceptance score, model majority vote or automatic promotion."
  - The amendments file has no hit.
  - Every zip use of a confidence cutoff is in a fan-out reducer deciding what goes TO review (before the refute wave). None is a cutoff "to a strategy" (P:147-148).
- Where a claim's confidence comes from after it has been contested and validated: nothing in the zip, the amendments or the verifier plan says. The verifier plan places the "promotion of scientific confidence" after the verifier, at "human-reviewed disposition / downstream use (separate approval)" (verifier:45, 50).
- Collisions:
  - (i) A cutoff that reads "each step's" confidence (P:149) passes a claim only if the proposer's, the reviewer's and the checker's model-stated figures each clear it. That is a unanimity rule over model judgements: verifier:78 "model majority vote or automatic promotion" and verifier:101 "Do not ask multiple LLMs to vote on correctness". A cutoff on "the newest stated" figure makes the last model's figure decide. A cutoff that moves a claim "to a strategy" by code is automatic promotion (verifier:78) under either reading.
  - (ii) "never computed or pooled" (P:140-141) keeps the no-averaging rule (CLAUDE.md "EACH TRADE INDIVIDUALLY, never average"; verifier:17).
  - (iii) Labels: the plan turns no confidence into a word. The banned list (`defend.py:86-88`) and `schema.py:7-8` cover words only.
  - (iv) A 0-to-1 figure stated by a model has no rubric for what a value means, and no method or input it was measured on. CLAUDE.md "No made-up numbers are used in a session" is written about calculations on tape; whether a model's stated confidence falls under it is not said. The plan does not ask for a rubric.
- "It does not stay as a strategy unless it's proven first" (decisions:7466-7479) against the plan's heading "NO 'PROVEN'" (P:134). The decisions log records the main session's correction, "a strategy's standing is his rule and the record carries it" (7470-7471), and "PUT TO HIM, NOT ANSWERED: who says 'proven' and on what" (7473-7474). The later entry (7498-7502) is the main session's reading of the zip ("nobody stamps it"), not his words. The tie "each strategy is tied to its claims and shows where each stands" (7477-7479) is not in the plan.

---------------------------------------------------------------
THE CHANGED SECTION, POINTS 3 AND 4

- Point 3: see 03b, items 2 and 4.
- Point 4: the eight keys at P:155-157 match `tools/swarm/plan.py:25` (it ends `max_wall_clock_s`, `max_retries`, `max_graph_writes`; I read that one line). This is process for the main session and builds nothing under the four tickets.
- The table at P:9-18 says "writes into the real graph: 0". The run-plan key is `max_graph_writes`, which `tools/swarm/run.py:60` counts as every write, scratch or real. Whether the builder's figure for that key is 0 or a count of scratch writes is not said.

---------------------------------------------------------------
ITEM 5: does anything need a schema change despite P:21-22?

`schema.py` itself need not be edited: `check_node` has no attribute allowlist, and P:121-133 adds no node or edge type. The plan does add new fields, though P:21 says "no new ... field": `outcome_records`, `revision_of`, the unnamed "never listed" marker, the confidence lines, `falsifier_observation_seen` and `observed_at`, plus a structured objection with a source. `defend.py`'s own allowlists (`CLAIM_KEYS` at 90-94, `CHALLENGE_KEYS` at 95-96) refuse unknown keys and must change. `schema.CLAIM_CONTRACT_FIELDS` and `EVALUATION_CONTRACT_FIELDS` (`schema.py:74-84`) would no longer list every contract field in use.

---------------------------------------------------------------
SPECULATION, labelled as such

- If the confidence lines are kept as separate Metric or Evaluation nodes rather than on the Claim node, the revision effects described under point 1 do not arise. I have not checked that against any reader.
- `tools/decider/afterwards.py` at 2ac873f: my grep for `def brief` and "next decider" found nothing in it. The "brief" P:63 names may live elsewhere or under another name; scout 109 (not read by me) may say where.

---------------------------------------------------------------
TO CHANGE IN THE PLAN BEFORE THE BUILDER STARTS

1. 03b: meet "naming truthfully the runs before 107 that only run 111's audit of the whole record covers" (a separate listing of runs covered only by a whole-record auditor line).
2. 03b: the check that a run line ADDED with no auditor naming it is listed and fails, as the ticket words it.
3. 03b: the auditor's reports kept in git, and something that ties each `audits` number to a row in a report at a commit.
4. 03b: the tie between a ticket's box and the runs that worked on it.
5. 03b: say how roles map to the roster, and whether "outside the roster" fails the exit code.
6. 04: say how the ticket's own named case (`file_proposer` `kept_records` / brief lines 138-144, and the afterwards hand-over) is met, or change the ticket's words to the limit the plan states. As written, the code that hands the record today is untouched.
7. 04: put behind the door, or say plainly they are not, these outcome-bearing channels: `outcome_visibility.what` in the brief; `defend show` with release paths; the graph JSONL; the counter claim; OPEN CONFLICTS; the place-in-process line; checker confidences; grounding's adverse count.
8. 04: refuse, or mark, a challenge of a later revision by a run that was already released the outcome.
9. 05: bind a check to the revision current at the trial, or refuse a revision registered after a trial's outcome exists.
10. 05: say who may write a check (reviewer role only, or any non-proposer run).
11. 05: say how a falsifier seen on some events and not others is written (per cell, not one yes/no).
12. 05/06: exempt verbatim quotes (`observed_at`, a sourced objection's quote) from the label refusal.
13. 06: name the Source node and SUPPORTS link for the counter claim, and its `inference` value for model-assisted checks.
14. 06: name a command that can take a CONTRADICTS link back. `resolve undo` refuses it (`resolve.py:267-268`).
15. 06: give OPEN CONFLICTS a share or a cap, so the text stays within its budget (adoption 5a).
16. 06: record on each CONTRADICTS link the claim revision it was written against.
17. Point 1: drop the frozen Claim node, or name its marker and every reader that must skip it (`defend._registered`, `undefended`, `context.build`, `grounding.check_text`, `grounding.check_all`, `store.check_all`), and the SUPPORTS links it needs to be written at all.
18. Point 1: either keep a sourced objection as an unresolved objection (verifier 78) or cite a line that makes it a refutation; none I read does.
19. Point 2: say where confidence lines are stored and who writes them, without making a new Claim revision.
20. Point 2: keep the proposer's confidence out of the reviewer's brief and session text (verifier 98).
21. Point 2: do not let code move a claim "to a strategy" on a cutoff (verifier 78).
22. P:21: strike "no new ... field", or list the new fields and the `defend.py` allowlist changes.

NOT ANSWERED BY THE ZIP, THE PLANS OR GREG'S WORDS

- Where a claim's confidence comes from after it has been contested and validated, who states it, and on what rubric. The zip's only cutoffs are in fan-out reducers before review (adoption 25, 145). The verifier plan puts confidence promotion at human-reviewed disposition (45, 50) without saying how.
- Which acts count as a refutation: whether a reviewer's objection with a source, before any trial, is one (4a-bis names the edge, not the act; verifier 78 names "adverse cases" and "unresolved objections" apart).
- Who says a strategy is "proven" and on what (decisions:7473-7474, recorded as put to him, not answered by him). Also whether that is the same as a confidence cutoff.
- Which confidence a cutoff reads (the newest, or each step's). The plan itself flags this at P:148-150.

TOOL CALLS: 27, counting this handback and the one advisor call (26 before this one). No file written, nothing committed, nothing run through the engine or the tape, no AWS.
