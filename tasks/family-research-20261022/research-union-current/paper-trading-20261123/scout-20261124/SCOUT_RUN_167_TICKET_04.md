# Scout run 167 (Haiku): where things are for ticket 04

Everything below this line is the agent's own report, word for word; nothing below it is the main session's.

## Hand-back 1 of 1

Scout run 167, ticket 04.

Tool calls: 27 of 30 (Read 9, Grep 16... counted as 27 total, all listed in the work above). Model calls: 0 advisor calls. Wall clock well under 600 s. Writes: 0.

Scope note: working tree /home/user/Markets, .git/HEAD = ref: refs/heads/ccr-144315dd-pta2ze. I did not read a commit sha for the tree. Line numbers below are as the working tree stands when I read it. They match the reviewer's cited lines (outcome.py:82-83, 110-111, 162-176, 167, 172; file_proposer.py:142-148; loop.py:390, 411; test_outcome.py:185-186, 226-253, 256-276).

=== POINT 1: `defend show` with no --run prints the proposer's whole side ===
Behaviour:
- tools/kgraph/outcome.py:107-116 `def check_show(store, claim_id, run)`. Line 110-111: `if run is None:` / `return`. Line 114: `if _agent_is_reviewer(node) and not own_current_challenge(...)`. Line 115-116 raises the refusal.
- tools/kgraph/defend.py:777-801 `def show(store, claim_id, run=None)`. Line 780 calls `outcome.check_show`. Line 789: `+ (f"  (shown to {run})" if run else "  (no run was named)")`. Lines 790-795 print mechanism, alternatives, falsifiers, outcome_visibility and so on.
- tools/kgraph/defend.py:858-883 `def main`. Line 861 has `--run` added as a plain optional argument, not required. Line 873-874 `elif a.verb == "show": print(show(store, a.claim, a.run))`.
Checks touching it:
- tests/agent_program/test_outcome.py:177 `def test_show_refuses_a_reviewer_without_its_own_challenge`. Line 185 `assert dmain(w, "show", cid) == 0`. Line 186 `assert "no run was named" in ...`.
- tests/agent_program/test_outcome.py:161 `def test_the_brief_says_only_that_an_outcome_was_or_was_not_seen`. Line 174 calls `defend.show(s, seen)` with no run.
- tests/agent_program/test_outcome.py:193 `def test_a_challenge_records_whether...`. Line 203 `dmain(w, "show", cid, "--run", REVIEWER)`.
Status: ALREADY IN THE CODE? NO for "needs --run". Line 110-111 in outcome.py reads: `    if run is None:` / `        return`. The test at line 185-186 asserts the no-run read succeeds.

=== POINT 2: a trial's folder is matched to its trial by order ===
Behaviour:
- tools/ratchet/file_proposer.py:127-152 `def kept_records(self, history=())`. Line 131 says "a guess by modification time, as the line says". Line 142 `runs = sorted((p for p in keep.iterdir() if p.is_dir()), key=lambda p: (p.stat().st_mtime_ns, p.name))`. Line 144 `for i, r in enumerate(runs):`. Line 145-147 holds folder i if `held.get(i)`. Line 150-151 names folder i with its path.
- tools/ratchet/file_proposer.py:155-205 `def brief`. Line 160 `folder = self.mailbox / f"trial-{n}"`. Line 173-175 prints held rows without folder path.
- tools/ratchet/file_proposer.py:208-210 `def __call__`. Line 209 `folder = self.mailbox / f"trial-{trial_no}"`, line 210 mkdir. Line 214 writes brief.md.
- tools/ratchet/loop.py:369-371 ProposalFailed branch (proposal not kept). Line 390 `push(n, hyp, "crash", parent, anchor["commit"], {}, None, f"crash: {failed}", agent_run)` (no folder, no proposal). Line 397-398 "crash: the proposer made no change". Line 411-412 "touched" branch.
- loop.py:252-281 `def execute(n)`: retries write one `attempts` list per trial; the folder is not tied to any trial id.
Status: NOT IN THE CODE. The trial's own id is not written with the folder (no grep hit for id in folder naming; folder is named by n, but kept_records matches by sorted mtime index, file_proposer.py:142-147).
Checks touching it:
- tests/agent_program/test_outcome.py:226 `def test_the_file_proposer_holds_a_trial_that_rests_on_an_unchallenged_claim`. Lines 230-232 make three folders r0, r1, r2 in order. Line 245-247 check `kept_records`, `kept[0]`, `str(keep / "r0") not in kept[0]`, and `all(str(keep / f"r{i}") in kept[i] for i in (1, 2))`. Line 252 repeats after the challenge.
- No other test calls kept_records. Grep for kept_records / --keep / held in test_stage3_proposer.py, test_decider_loop.py, test_defend.py, test_stage3_ratchet.py: only tests/agent_program/test_decider_loop.py:126 `"--keep", str(keep)` (test_decider_loop.py:105 `piece 2: trial_with_decider --dry`). No crash-folder test.

=== POINT 3: a refused proposal's rests_on is dropped from its row ===
Behaviour:
- tools/ratchet/loop.py:233-249 `def push(...)`. Line 246: `"rests_on": list((proposal or {}).get("rests_on") or [])`. Line 237-238 keeps `env["proposal"]` only when proposal is given.
- tools/ratchet/loop.py:369-371: `except ProposalFailed as e:` then `prop = {"hypothesis": ..., "agent_run": None, "usage": None}`. No proposal key, so `proposal = prop.get("proposal")` at loop.py:385 is None.
- tools/ratchet/loop.py:390: `push(n, hyp, "crash", parent, anchor["commit"], {}, None, f"crash: {failed}", agent_run)`. No `proposal=` argument. Row gets `rests_on: []`.
- tools/ratchet/file_proposer.py:252-262 refusals (no source; unregistered claim: `raise ProposalFailed(f"{cid} is not a claim of the graph", hyp)`).
Status: NOT IN THE CODE.
Checks touching it:
- tests/agent_program/test_stage3_proposer.py:206 `def test_a_proposal_that_breaks_a_rule_is_refused_with_its_reason` (parametrized; takes `rests_on`, `inference`, `reason`). Checks the refusal text only, not the row.
- tests/agent_program/test_stage3_ratchet.py:320 `def test_a_proposer_that_raises_is_a_recorded_crash_and_the_loop_goes_on`. Checks the crash, not rests_on on the row.
- tests/agent_program/test_stage3_ratchet.py:218 `def test_a_missing_usage_file_is_a_recorded_crash_and_the_loop_goes_on` (in test_stage3_proposer.py per the grep: line 218).
No check reads `rests_on` on a crash row.

=== POINT 4: `--out` is not checked against the data checkouts; a second release to a new --out writes a second release Task; a release Task lists the challenges of every revision ===
Behaviour:
- tools/kgraph/outcome.py:129-137 `def release`. 139-178 `def _release`. Line 146 `dirs = dirs or repo_dirs(store.data_root, None, None)`. Line 162 `targets = [Path(out) / r["repo"] / r["path"] for r in recs]`. Line 163-165 is the ONLY out check: `if t.exists(): raise schema.Refused(f"out: {t} already exists; a handed-over file is never rewritten")`. Line 167 `chs = sorted(e["id"] for e in defend.challenges_of(store, claim_id))` (all revisions). Line 168 tid from claim, rev, run, recs, chs, stamp. Line 172-173 store.write of the Task. Line 174-176 copy after the Task.
- tools/kgraph/extract.py:56-62 `def repo_dirs`: fixed candidates (`here.parent / "paper-trading-platform"`, markets-data = data_root). No check of --out.
Status: NOT IN THE CODE. No check of --out against checkouts; a new --out makes a new Task (line 172).
Checks touching it:
- tests/agent_program/test_outcome.py:92-93 (out0; `not out.exists()` after refusal), 104-106 (out1, copy bytes), 123 and 125 (out2, out3), 137 (out4). `def test_releases_lists_everyone...` line 144 does not use --out.
- test_outcome.py:114 `assert ... a["challenges"] == [S["ev1"]]`: covers revision 1 only; does not catch the all-revisions list.
- No test releases twice to one --out, or to a new --out, or checks --out against the data checkout.

=== POINT 5: the `--rests-on-none` reason is kept only in the brief's own head ===
Behaviour:
- tools/decider/afterwards.py:277-309 `def main`, the `brief` branch. Line 287 `ap.add_argument("--rests-on-none", ...)`. Line 291 `why = (a.rests_on_none or "").strip()`. Line 292-294 refuses unless exactly one of --claim or --rests-on-none (message to stderr, `return 2`). Line 304-305 the claim note. Line 307 `note = f"Bears on no registered claim: {why}"`. Line 308 `Path(a.out).write_text(make_brief(a.afterwards, a.budget, note), encoding="utf-8")`.
- tools/decider/afterwards.py:258 `def make_brief(path, budget, note=None)`.
- No Task written, no graph write, refusals printed to stderr (lines 293, 302), not kept.
Status: NOT IN THE CODE (reason only in brief head, afterwards.py:307-308).
Checks touching it:
- tests/agent_program/test_outcome.py:256 `def test_afterwards_brief_goes_through_the_rule`. Line 265-266 (--claim unchallenged: exit 2, no file, cid in stderr). Line 268-269 (challenged: file written, cid on first line). Line 272-273 (`--rests-on-none` reason on first line of out2). Line 275-276 (neither flag / both: exit 2).
- tests/agent_program/test_decider_afterwards.py:148 `def test_brief_one_line_a_decision_and_nothing_added`. Line 150 passes `--rests-on-none`.

=== POINT 6: the checks of test_outcome.py depend on each other ===
Status: DESIGN STATED IN CODE at tests/agent_program/test_outcome.py:8-9: "The checks run in file order: each builds on the graph the one before left (a claim is challenged, then released, then revised)."
Shared module-level / fixture names (test_outcome.py):
- line 30-45 `@pytest.fixture(scope="module") def world(tmp_path_factory)`: one scratch graph copy `w["graph"]`, `w["n"]` counter (line 41), `w["raw"]`, `w["commit"]`, `w["spec"]`. Mutated by every write.
- line 23-27: PROPOSER, REVIEWER, REVIEWER2, R0, JOURNAL, CLAIMS (module constants).
- line 48 `fresh(w)`, line 52 `reg(w,...)` (increments w["n"], line 57), line 63 `chal(w,...)` (increments w["n"], line 65), line 78 `rel(w,...)`.
- line 83 `S = {}` module-level dict. Keys and readers:
  - S["cid"]: SET line 88 (test_refused_before_any_challenge..., line 86). READ at 101, 122, 131, 145, 173, 194.
  - S["ev1"]: SET line 102 (test_released_after..., line 100). READ at 114 and 197.
  - S["ev2"]: SET line 139 (test_a_new_revision..., line 130). READ at 198 and 202.
  - S["cid2"]: SET line 163 (test_the_brief..., line 161). READ at 178 (test_show_refuses..., line 177).
  - S["cid3"]: SET line 228 (test_the_file_proposer..., line 226). READ at 223 (helper `_rows`, line 216), 235, 239-252.
- Line 211 imports `clone`, `load`, `proposer`, `PRINT_CMD`, `REPO`, `LOOP_FILE` from test_decider_loop (clone is a fixture there). Line 213 `UNREGISTERED`.
Cross-check dependencies (a check reads what another wrote):
- 105/125 release -> 127 expects releases [REVIEWER, PROPOSER] and 147-153 expects them listed.
- 139 chal ev2 -> 140, 141, 198, 202. 187 chal (test_show, line 177) adds a second REVIEWER challenge that 188 and 190 read.
- 102 ev1 -> 103, 105 release, 114.
- 88 registration of condition-1 -> every later check (via S["cid"]).
- 89 asserts challenges_of == [] and depends on nothing earlier, but the graph is module-level, so it is first in file order.
- 204-205 counts 3 flags, which depends on ev1, ev2, ev3 from 199 and the show at 203.
- 201 `again = chal(...)` expects the same id as S["ev2"] (line 202).
If the world fixture is skipped (lines 36, 44) every check skips; if 88 fails, S["cid"] is unset and later checks raise KeyError (reviewer's S6).

=== CHECK FILES: separated "cases the real record does not hold" section ===
- tests/agent_program/test_outcome.py: no "# change:" comment and no section titled as such. The one non-real input is in test_a_new_revision_needs_a_new_challenge, line 130-132: `reg(w, "condition-1", lambda d: d.update(scope=d["scope"] + " (revision two of the file)"))`. Module docstring line 6 says it is "a COPY of a real claim file with its scope sentence lengthened". Part headers: line 156 "# ---- part B: ..." and line 208 "# ---- part C: ...". No "not held" section.
- tests/agent_program/test_defend.py: grep for "# change:" and "CASES THE REAL" found no hit. Only section header at line 742 "# ---- the points of the fourth read (run 147) ----". No separated not-held section found.

=== PLATFORM-CHECKOUT SKIPS AND REFUSALS ===
Skips in the six files:
- tests/agent_program/test_defend.py:36-39 fixture: `plat = root.parent / "paper-trading-platform"` ... `pytest.skip("no paper-trading-platform checkout")` (line 39). Also line 49 `pytest.skip(f"{need} is not in this graph")`.
- tests/agent_program/test_decider_loop.py:31 `PLATFORM = Path("/home/user/paper-trading-platform")`; line 108 `pytest.skip("no platform checkout")`; line 111 `pytest.skip("no loop-trial.json")`; line 51 `pytest.skip(f"no record branch for {R0} in {root}")`; line 157 `pytest.skip(f"{rel} is not committed here")`.
- tests/agent_program/test_stage3_proposer.py:33 `pytest.skip("this checkout has no corrected run 47")`; line 74 `PLATFORM = Path("/home/user/paper-trading-platform")`; line 93 `pytest.skip("no paper-trading-platform checkout holding loop-trial.json")`; line 157 `pytest.skip("no loop-trial.json in the platform checkout")`; line 248 `pytest.skip("the real commits of the replay check are not in this checkout")`.
- tests/agent_program/test_stage3_ratchet.py:29 `PLATFORM = Path("/home/user/paper-trading-platform")`; line 47 `pytest.skip("no local paper-trading-platform checkout")`.
- tests/agent_program/test_decider_afterwards.py:26 `pytest.skip(f"no markets-data checkout: {e}")`; line 30 `pytest.skip(f"no record branch for {R0} in {root}")`. (These are markets-data, not the platform; the reviewer's seven SKIPPED lines came from here.)
- tests/agent_program/test_outcome.py: no platform skip. Skips are at line 36 `pytest.skip(f"{JOURNAL} is not tracked in {root}")` and line 44 `pytest.skip(f"{run} is not in this graph")`. Its `clone` fixture is imported from test_decider_loop (line 211), so it inherits that file's platform skip (test_decider_loop.py:108) if it has one; I did not read the clone fixture body.
Refusals (code, not skips) that need a platform checkout:
- tools/kgraph/defend.py:246-248: `plat, rid, commit = dirs.get("paper-trading-platform"), ...` / `raise schema.Refused(f"{where}: a rule ground needs rule_id, a commit sha and a platform checkout")`. This is what the reviewer's registration hit in /tmp copies (S6).
- tools/kgraph/defend.py:255: `raise schema.Refused(f"{where}: rule {rid} has no text at commit {commit} in the platform checkout ({e})")`.
- tools/kgraph/defend.py:368: `repo {x['repo']!r} has no local checkout`.
- tools/kgraph/outcome.py:151: `record {spec}: repo {repo!r} has no local checkout`.
- tools/kgraph/extract.py:59: `cand = Path(platform) if platform else here.parent / "paper-trading-platform"` (here = /home/user/Markets, so /home/user/paper-trading-platform). Reviewer's /tmp copies fell outside this path, so registration failed there.

=== NOT FOUND ===
- No "# change:" section in test_outcome.py or test_defend.py (searched tests/agent_program/test_outcome.py and test_defend.py, patterns "# change:", "CASES THE REAL", "# ----", "# ====").
- No test calls kept_records or checks the crash-folder case (searched tests/agent_program for "kept_records", "--keep", "held", "trial-" in test_stage3_proposer.py, test_decider_loop.py, test_defend.py, test_stage3_ratchet.py).
- No test for --out against checkouts or for a second release to a new --out (searched test_outcome.py for "--out", "out", "already exists").
- No test reads rests_on on a crash row (searched test_stage3_ratchet.py, test_stage3_proposer.py for "rests_on").
- No test of the `--rests-on-none` reason beyond first-line presence (searched test_outcome.py, test_decider_afterwards.py).
- Not read: test_stage3_proposer.py and test_decider_loop.py check bodies (only names and skips, via grep); clone fixture body in test_decider_loop.py; test_defend.py check bodies (only names, via grep at 742 and skips). The loop's and proposer's checks were not run.
- Files searched: tools/kgraph/outcome.py, defend.py, extract.py; tools/ratchet/loop.py, file_proposer.py; tools/decider/afterwards.py; tests/agent_program/test_outcome.py, test_defend.py, test_stage3_ratchet.py, test_stage3_proposer.py, test_decider_loop.py, test_decider_afterwards.py, realrecords.py (not opened). Working tree /home/user/Markets on ccr-144315dd-pta2ze.
