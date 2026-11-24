# Scout run 125 (Haiku): where things are for ticket 04

Kept word for word as the agent returned it, 2026-11-24 (twenty-fifth session). Nothing below this line is the main session's.

---

SCOUT REPORT, run 0125, ticket 04 locate. Checkout 3a98333 (as given; not verified, no git here). Tool calls used: 17 of 20. No writes, no sub-agents.

FILES OPENED
- /home/user/Markets/tools/ratchet/file_proposer.py (full)
- /home/user/Markets/tools/ratchet/proposer.py (full, 277 lines)
- /home/user/Markets/tools/decider/afterwards.py (read 0-231; the tool numbers the first line 0)
- /home/user/Markets/tools/kgraph/defend.py lines 463-724
- /home/user/Markets/tests/agent_program/test_stage3_proposer.py lines 1-60 and 82-101
- /home/user/Markets/tools/ratchet/loop.py lines 201-250, 296-325, 362-383, 383-396, 440-457
PATTERNS SEARCHED
- Glob tools/ratchet/* : 8 files (BUILD_NOTES_PROPOSER.md, __init__.py, loop.py, PROGRAM_TEMPLATE.md, file_proposer.py, program.py, proposer.py, ready.py). No ratchet.py exists.
- Grep defend.py `^def (show|undefended|challenges_of|_registered|challenge)\b`: 5 hits (463, 574, 643, 648, 694)
- Grep test_stage3_proposer.py `^def test_`: 13 hits (29,42,154,161,206,218,231,245,259,268,284,291,300)
- Grep loop.py `^\s*def |history|rests_on|push\(|\.append\(`: 80 hits, read via lines above
- Grep exp_dag.py `def push`: 1 hit (line 100)
- Grep tests/agent_program `def (graph|clone)\b|fixture`: 30 hits (shown capped at 30)
NOT FOUND
- No `rests_on` key stored per trial in loop.py history, and no per-trial claim list in the exp_dag push body.
- No code in tools/ratchet or tools/kgraph that checks "every registered claim of a trial has a challenge". Closest: defend.undefended (defend.py:694).
- No ratchet.py. Not opened: tests/agent_program/realrecords.py (PAPER, data_root), the PLATFORM/PLAN constants of test_stage3_proposer.py, the test bodies beyond the names in the grep.

1. FILE_PROPOSER.PY
- No `__init__` in MailboxFileProposer; it inherits MailboxProposer.__init__ (proposer.py:70-81). Its own override is file_proposer.py:97-100:
```
97	    def __init__(self, *a, **k):
98	        super().__init__(*a, **k)
99	        self.task = k.get("task") or TASK
100	        self.file_rel = self.plan_rel                      # the one mutable file, here a program
```
  Attributes set by the base (proposer.py:72-82): self.mailbox (resolved Path), self.program (Program, the control file), self.plan_rel (= program.mutable[0]), self.data_root, self.graph_dir, self.context_budget, self.timeout_s, self.poll_s, self.task, self.dirs, self._store. Subclass adds self.task and self.file_rel.
- kept_records 103-121: skipped per instruction.
- brief, file_proposer.py:124-170 (full):
```
124	    def brief(self, present: str, history: list, n: int, worktree) -> tuple[str, list]:
125	        p = self.program
126	        ctx = kcontext.build(self.store(), self.task, self.context_budget, dirs=self._dirs())
127	        contract = Path(worktree) / CONTRACT_FILE
128	        contract_text = contract.read_text(encoding="utf-8") if contract.is_file() else "(the contract file is not in the worktree)"
129	        folder = self.mailbox / f"trial-{n}"
130	        L = [f"# Brief for trial {n} of the loop {p.loop}", "",
131	             f"Task: write the whole of one program, {self.task}.",
132	             "You do not run anything: the loop runs a trial on the platform's stored tape after your file is applied.",
133	             "", "## The one file that may change", "",
134	             f"Only `{self.file_rel}`. A change anywhere else is refused. Its present content, in full:", "",
135	             "```python", present.rstrip("\n"), "```", "",
136	             "## The contract of decide(packet), from " + CONTRACT_FILE, "", contract_text.rstrip("\n"), "",
137	             "## The rules a decider program obeys", "", RULES, "",
138	             "## Earlier trials, each its own line", ""]
139	        if not history:
140	            L.append("(none yet)")
141	        for h in history:
142	            figs = ", ".join(f"{k}={v}" for k, v in h["figures"].items()) or "no figures"
143	            L.append(f"- trial {h['n']}: status {h['status']}; hypothesis: {h['hypothesis']}; figures: {figs}; "
144	                     f"note: {h['note'] or 'none'}")
145	        L += ["", "The figures are counts of what each trial wrote, not results. Nothing is totalled, averaged, "
146	              "ranked or called good or bad here."]
147	        if p.metric_direction is None:
148	            L.append("No figure is chosen for keeping or reverting: every trial is recorded and none is kept or reverted.")
149	        else:
150	            L.append(f"The loop keeps or reverts by `{p.metric_name}` ({p.metric_direction}).")
151	        L.append(f"The runs of 2026-11-24 are not scored ({WORKING_NOTE}).")
152	        kept = self.kept_records()
153	        if kept:
154	            L += ["", "## Records the earlier trials kept (paths to read; each trade is its own line in trades.jsonl)", ""] + kept
155	        L += ["", f"## Session context from the graph (about {ctx['tokens_estimated']} tokens of {self.context_budget})", "",
156	              ctx["text"], "Claim ids in the text above: " + (", ".join(ctx["included"]) or "none"), "",
157	              "## How to answer", "",
158	              f"1. Write the whole new file to `{folder / 'proposed.py'}` FIRST.",
159	              f"2. Then write `{folder / 'answer.json'}`, nothing else in it:", "",
160	              '{"hypothesis": "<one sentence>",',
161	              ' "rests_on": ["claim:<id>", "..."],',
162	              ' "inference": null}', "",
163	              "`rests_on` lists the claim ids the change stands on; if no claim supports it, leave it empty and "
164	              'give `"inference"`: one sentence on why none does. A proposal with neither is refused. '
165	              "A claim id that is not in the graph is refused. A file that does not compile, defines no `decide`, "
166	              "is identical to the present one, imports outside the standard library, or names open, os, pathlib, "
167	              "subprocess, socket, importlib, __import__, eval or exec is refused.",
168	              'To end the loop instead: {"stop": true, "reason": "..."}.',
169	              "The usage file is written by the main session from the harness's report; do not write it."]
170	        return "\n".join(L) + "\n", ctx["included"]
```
  Note: history lines in the brief (141-144) show only n, status, hypothesis, figures, note. No rests_on.
- __call__, file_proposer.py:173-196 (full):
```
173	    def __call__(self, worktree, trial_no, history):
174	        folder = self.mailbox / f"trial-{trial_no}"
175	        folder.mkdir(parents=True, exist_ok=True)
176	        path = Path(worktree) / self.file_rel
177	        present = path.read_text(encoding="utf-8")
178	        text, _ = self.brief(present, history, trial_no, worktree)
179	        with (folder / "brief.md").open("x", encoding="utf-8") as f:
180	            f.write(text)
181	        deadline = time.monotonic() + self.timeout_s
182	        answer = self._wait(folder / "answer.json", deadline)
183	        if isinstance(answer, dict) and answer.get("stop") is True:
184	            return None
185	        usage_doc = self._wait(folder / "usage.json", deadline)
186	        hyp = answer.get("hypothesis") if isinstance(answer, dict) else None
187	        hyp = hyp if isinstance(hyp, str) and hyp.strip() else None
188	        usage, agent_run = self._usage(usage_doc, hyp)
189	        proposed = folder / "proposed.py"
190	        while not proposed.exists():
191	            if time.monotonic() >= deadline:
192	                raise ProposalFailed(f"timed out after {self.timeout_s}s: proposed.py is missing in {folder}", hyp)
193	            time.sleep(self.poll_s)
194	        applied = self._apply_file(present, path, proposed, answer, hyp)
195	        (folder / "applied.json").write_text(json.dumps(applied, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
196	        return {"hypothesis": hyp, "agent_run": agent_run, "usage": usage, "proposal": applied}
```
- _wait: NOT overridden in file_proposer; it is proposer.py:138-150 (see section 3).
- _apply_file, file_proposer.py:198-240 (full):
```
198	    def _apply_file(self, present: str, path: Path, proposed: Path, answer, hyp):
199	        if not isinstance(answer, dict):
200	            raise ProposalFailed("answer.json is not a JSON object")
201	        if hyp is None:
202	            raise ProposalFailed("answer.json: `hypothesis` is missing or empty")
203	        try:
204	            raw = proposed.read_bytes()
205	            new = raw.decode("utf-8")
206	        except (OSError, UnicodeDecodeError) as e:
207	            raise ProposalFailed(f"proposed.py cannot be read as UTF-8 text: {e}", hyp)
208	        rests_on, inference = answer.get("rests_on"), answer.get("inference")
209	        if rests_on is None:
210	            rests_on = []
211	        if not isinstance(rests_on, list) or not all(isinstance(c, str) for c in rests_on):
212	            raise ProposalFailed("`rests_on` must be a list of claim ids", hyp)
213	        if inference is not None and not isinstance(inference, str):
214	            raise ProposalFailed("`inference` must be null or a sentence", hyp)
215	        if isinstance(inference, str) and not inference.strip():
216	            inference = None
217	        if not rests_on and not inference:
218	            raise ProposalFailed("no source: `rests_on` is empty and `inference` is empty (every proposal has a "
219	                                 "source or is marked an inference)", hyp)
220	        problem = source_problem(new, present)
221	        if problem:
222	            raise ProposalFailed(problem, hyp)
223	        store = self.store()
224	        for cid in rests_on:
225	            node = store.node(cid)
226	            if node is None or node["type"] != "Claim":
227	                raise ProposalFailed(f"{cid} is not a claim of the graph", hyp)
228	        path.write_bytes(raw)
229	        grounded = []
230	        for cid in rests_on:
231	            try:
232	                r = grounding.check_claim(store, cid, self._dirs())
233	                grounded.append({"claim": cid, "decision": r["decision"], "reason": r["reason"]})
234	            except Exception as e:                         # a check that cannot run is said, never a refusal
235	                grounded.append({"claim": cid, "decision": "unchecked",
236	                                 "reason": f"the grounding check could not run: {type(e).__name__}: {e}"})
237	        diff = "".join(difflib.unified_diff(present.splitlines(keepends=True), new.splitlines(keepends=True),
238	                                            f"a/{self.file_rel}", f"b/{self.file_rel}"))
239	        return {"path": self.file_rel, "old_sha256": sha(present.encode("utf-8")), "new_sha256": sha(raw),
240	                "diff": diff, "rests_on": rests_on, "inference": inference, "grounding": grounded}
```
  The answer key is `rests_on` (line 208), with `inference` (208) and `hypothesis` (186). `stop` at 183. The returned dict (240) holds rests_on as a list of claim-id strings, plus grounding entries {claim, decision, reason}. Only the claim id is checked to be a Claim node (225-227); registration is NOT checked here. applied.json is written at 195 and the same dict is returned as "proposal" at 196.

2. THE LOOP (tools/ratchet/loop.py; there is no ratchet.py)
- Trial runner: `run_loop(program_path, proposer, *, scratch, data_root=None, exp_dir=None) -> dict` at loop.py:201. Inner `push` at 233-249; `settle` at 296-319; proposer call at 368: `prop = proposer(wt, n, [dict(h) for h in history])`; proposal taken at 384: `proposal = prop.get("proposal")`; settle receives it as `proposal` (parameter at 296, used at 311).
- history entry, loop.py:244-246 (full):
```
244	        row = {"n": n, "id": tid, "commit": commit, "status": status, "figures": dict(figs),
245	               "note": note, "hypothesis": hypothesis, "parent": parent, "runtime_s": runtime}
246	        history.append(row)
```
  Keys: n, id, commit, status, figures, note, hypothesis, parent, runtime_s. NO rests_on, claims or proposal key in the history row.
- Trial pushed to the experiment record: loop.py:239-242 (full):
```
239	        tid = dag.push(hypothesis=hypothesis, status=status, parent=parent, agent_run=agent_run,
240	                       change={"repo": repo.name, "commit": commit}, metrics=metrics, runtime_s=runtime,
241	                       environment=env, loop=program.loop, note=note,
242	                       written_by=stamp)
```
  And at 236-238 the proposal is carried INSIDE the environment, not as its own field:
```
236	        env = dict(env_base, attempts=list(attempts))
237	        if proposal is not None:                        # only a proposer that states one (replay states none)
238	            env["proposal"] = proposal
```
  So the rests_on list of each trial is kept only at exp_dag environment["proposal"]["rests_on"] (and grounding). No links= is passed.
- exp_dag push: /home/user/Markets/tools/exp_dag.py:100-120, signature `def push(self, *, hypothesis: str, status: str, parent: str | None = None, agent_run: str | None = None, change: dict | None = None, metrics: list | None = None, runtime_s: float | None = None, environment=None, links: list | None = None, loop: str | None = None, note: str | None = None, key: str | None = None, written_by: str) -> str`. Body fields stored: parent, agent_run, hypothesis, change, metrics, runtime_s, environment, status, links, loop, note; plus id, key, rev, content_sha, written_by, written_at. No docstring beyond the one at 105-106.
- Final report, loop.py:440-447: keys loop, branch, worktree, logs, trials, kept, reverted, crashed, recorded, best, stopped_because, unresolved, escalations, declared_escalation_conditions, budget_used, summary (summary keys n, id, commit, status, figures, parent, note).

3. PROPOSER.PY (277 lines, so defs with line numbers)
- 1-19 module docstring (answer.json contract: {"hypothesis", "change": {...}, "rests_on": ["claim:<id>", ...], "inference": null | "<why>"}).
- 21-37 imports and constants (USAGE_FIELDS 34, DEFAULT_TASK 35, WORKING_NOTE 37).
- 40 `def dump_plan(doc) -> str`; 45 `_leaves`; 56 `_kind`; 61 `_compact`; 65 `_read_json`.
- 69 `class MailboxProposer:`
- 70-71 `def __init__(self, mailbox, program: Program, *, data_root=None, graph_dir=None, context_budget=6000, timeout_s=3600.0, poll_s=2.0, task=None, dirs=None)`
- 85 `def store(self) -> GraphStore` (read-only graph)
- 90 `def _dirs(self)`
- 94 `def brief(self, plan: dict, history: list, n: int) -> tuple[str, list]`
- 138 `def _wait(self, path: Path, deadline: float)` (138-150, copied):
```
138	    def _wait(self, path: Path, deadline: float):
139	        err = None
140	        while True:
141	            if path.exists():
142	                try:
143	                    return _read_json(path)
144	                except (json.JSONDecodeError, OSError) as e:       # still being written, or not JSON
145	                    err = e
146	            if time.monotonic() >= deadline:
147	                if err:
148	                    raise ProposalFailed(f"{path.name} in {path.parent} is not valid JSON: {err}")
149	                raise ProposalFailed(f"timed out after {self.timeout_s}s: {path.name} is missing in {path.parent}")
150	            time.sleep(self.poll_s)
```
- 152 `def __call__(self, worktree, trial_no, history)`
- 177-178 `@staticmethod` ; 178 `def _usage(doc, hyp)`
- 195 `def _apply(self, plan: dict, plan_path: Path, answer, hyp)`
- Base class has no method docstrings; its module docstring is the only one. Base `_apply` is for the exit/rules plan, not the file.

4. AFTERWARDS.PY (tools/decider/afterwards.py)
- Module docstring: lines 1-20 (the Read tool numbered the first line 0; the docstring closes on the line numbered 20). Key text: "What happened after each decision: the after-the-fact layer..."; "Nothing in the file may be given to a decider at the instant it decides; it is for learning after the fact (Greg, 2026-11-24)."
- 218-222 write_lines (copied):
```
218	def write_lines(path, header, lines):
219	    with Path(path).open("w", encoding="utf-8", newline="\n") as f:
220	        f.write(json.dumps(header, sort_keys=True) + "\n")
221	        for l in lines:
222	            f.write(json.dumps(l, sort_keys=True) + "\n")
```
- 225 section comment "# ---- the brief section ----"
- 227-228 _ext:
```
227	def _ext(x):
228	    return "none" if not x else f"{x['price']} at {x['first_reached_ns']}"
```
- 231-232 `def _q(x):` (the body is at line 232 and was not shown; the read stopped at 231 by my limit).

5. DEFEND.PY (tools/kgraph/defend.py)
- 463-467 _registered (copied):
```
463	def _registered(store: GraphStore, claim_id: str) -> dict:
464	    c = store.node(claim_id)
465	    if not c or c["type"] != "Claim" or c["attrs"].get("registration") != REGISTRATION:
466	        raise schema.Refused(f"claim: {claim_id!r} is not a claim registered with `defend register`")
467	    return c
```
- challenge 574-586 (wrapper), _challenge 601-640. Evaluation attrs, defend.py:627-636 (copied):
```
627	    attrs = {
628	        "rubric": RUBRIC, "what_was_checked": checked, "what_was_observed": observed, "what_remains_open": open_,
629	        "check_type": "independent challenge", "method": "tools.kgraph.defend challenge",
630	        "method_version": code_stamp("tools.kgraph.defend"), "claim_revision": c["rev"],
631	        "input_hash": c["content_sha"], "location": "tools/kgraph/defend.py", "scope": c["attrs"]["scope"],
632	        "expected_observation": dist, "reproducibility": f"the challenge file, sha256 {fh}; the brief, sha256 {bh}",
633	        "exceptions": d["objections"], "reviewer": run, "alternatives": alts, "falsifiers": fals,
634	        "distinguishing_observation": dist, "objections": d["objections"], "brief_sha256": bh,
635	        "saw_proposer_reasoning": d["saw_proposer_reasoning"], "what_i_opened": opened, "challenge_file": d,
636	    }
```
  Edges at 637: `edges = [link("EVALUATES", eid, claim_id), link("PRODUCED", run, eid)]`; written at 638 with type "Evaluation".
- challenges_of 643-645 (copied):
```
643	def challenges_of(store: GraphStore, claim_id: str) -> list[dict]:
644	    return [e for e in (store.node(x["src"]) for x in store.edges("EVALUATES") if x["dst"] == claim_id)
645	            if e and e["attrs"].get("rubric") == RUBRIC]
```
- show 648-691 (copied in full):
```
648	def show(store: GraphStore, claim_id: str) -> str:
649	    c = _registered(store, claim_id)
650	    a = c["attrs"]
651	    out = [f"{claim_id}  revision {c['rev']}  (registered by {a['proposer_run']})"]
652	    for k in ("proposer", "hypothesis", "exact_claim", "scope", "boundaries", "mechanism", "alternatives", "falsifiers",
653	              "artifact_repo", "artifact_path", "code_commit", "artifact_sha256", "data_manifest_hashes",
654	              "outcome_visibility", "inference", "inference_reason", "source_event_ids", "event_time", "knowledge_time",
655	              "reasoning_files"):
656	        if k in a:
657	            out.append(f"{k}: {a[k] if isinstance(a[k], str) else json.dumps(a[k], ensure_ascii=False)}")
658	    ol = _outcome_line(a)
659	    if ol:
660	        out.append(ol)
661	    if _falsifiers_line(a):
662	        out.append(f"falsifiers_changed_from_revision: {a['falsifiers_changed_from_revision']}  ({_falsifiers_line(a)})")
663	    out.append("every revision's falsifiers, with the time each was written:")
664	    for l in store.history(claim_id):
665	        out.append(f"  revision {l['rev']}, written {l['written_at']} by {l['written_by']}: "
666	                   f"{json.dumps(l['attrs']['falsifiers'], ensure_ascii=False)}")
667	    out.append("rests on:")
668	    out += [f"  {json.dumps(g, ensure_ascii=False)}" for g in a["rests_on"]] or ["  nothing"]
669	    out += [f"  {_saidline(g)}" for g in a["rests_on"] if g["kind"] == "cited"]
670	    ch = challenges_of(store, claim_id)
671	    out.append("challenges on record:")
672	    for e in ch:
673	        ea = e["attrs"]
674	        out += [f"  {e['id']}  by {ea['reviewer']}  at claim revision {ea['claim_revision']}  (brief sha256 {ea['brief_sha256']}; "
675	                f"saw the proposer's reasoning: {ea['saw_proposer_reasoning']}; opened: {json.dumps(ea['what_i_opened'])})",
676	                f"    alternatives: {json.dumps(ea['alternatives'], ensure_ascii=False)}",
677	                f"    falsifiers: {json.dumps(ea['falsifiers'], ensure_ascii=False)}",
678	                f"    distinguishing observation: {ea['distinguishing_observation']}",
679	                f"    what was checked: {json.dumps(ea['what_was_checked'], ensure_ascii=False)}",
680	                f"    what was observed: {json.dumps(ea['what_was_observed'], ensure_ascii=False)}",
681	                f"    objections: {json.dumps(ea['objections'], ensure_ascii=False)}"]
682	    if not ch:
683	        out.append("  none")
684	    out.append("what remains open:")
685	    if not ch:
686	        out.append("  no independent challenge is on record")
687	    for e in ch:
688	        out += [f"  ({e['id']}) {x}" for x in e["attrs"]["what_remains_open"]]
689	        if e["attrs"]["claim_revision"] != c["rev"]:
690	            out.append(f"  ({e['id']}) it was made at revision {e['attrs']['claim_revision']}, not the current {c['rev']}")
691	    return "\n".join(out)
```
- undefended 694-702 (copied):
```
694	def undefended(store: GraphStore) -> list[str]:
695	    out = []
696	    for c in sorted(store.nodes("Claim"), key=lambda n: n["id"]):
697	        if c["attrs"].get("registration") != REGISTRATION:
698	            continue
699	        if not any(e["attrs"]["claim_revision"] == c["rev"] for e in challenges_of(store, c["id"])):
700	            fl = _falsifiers_line(c["attrs"])
701	            out.append(f"{c['id']}  revision {c['rev']}  {c['attrs']['exact_claim'][:100]}" + (f"  [{fl}]" if fl else ""))
702	    return "\n".join(out)
```
  Note: undefended counts a challenge only if its claim_revision equals the claim's current rev; it works per claim, not per trial, and it does not link to any trial.
- Also: independence rule `_independent` at defend.py:551-571 refuses a run that registered the claim, or that made a ground claim, or whose role is not exactly "reviewer".

6. TEST_STAGE3_PROPOSER.PY
- Test functions (13): 29 test_run_47_two_lines_load_as_two_revisions(root, tmp_path); 42 test_same_run_number_without_corrects_or_across_sessions_is_still_refused(root, tmp_path); 154 test_the_plan_file_round_trips_byte_for_byte(); 161 test_one_value_is_applied_and_every_earlier_trial_is_in_the_next_brief(tmp_path, root, graph, clone); 206 test_a_proposal_that_breaks_a_rule_is_refused_with_its_reason(...); 218 test_a_missing_usage_file_is_a_recorded_crash_and_the_loop_goes_on(tmp_path, root, graph, clone); 231 test_usage_reaches_the_report_and_stops_the_loop_at_max_tokens(...); 245 test_replay_still_works_and_states_no_proposal(tmp_path, root, clone); 259 test_exactly_one_of_replay_and_mailbox_is_required(tmp_path, clone); 268 test_ready_check_on_a_good_control_file_and_it_never_runs_the_command(...); 284 test_ready_check_reports_a_shallow_repository(tmp_path, clone); 291 test_ready_check_reports_a_missing_mutable_file_and_an_unset_variable(...); 300 test_ready_check_reads_the_manifest_of_the_stored_tape_by_name_and_size(tmp_path, root, clone).
- Fixtures, lines 1-60 read: 1-13 imports (json, shutil, subprocess, Path, pytest, iar, GraphStore, `from .realrecords import PAPER, data_root`); 16-18 `@pytest.fixture(scope="module") def root(): return data_root()`; 21-25 helper `scratch_store(root, tmp_path)` (copies root/graph into tmp_path/graph, returns GraphStore and path, not a fixture). Lines 83-88 `graph` fixture: copies root/graph into a module tmp dir. Lines 90-96 `clone` fixture: skips unless the PLATFORM checkout holds PLAN (loop-trial.json) at HEAD, then git-clones it into tmp_path/platform. PLATFORM and PLAN constants are defined above line 82 and were not read.
- Real records used: root = data_root() from tests/agent_program/realrecords.py (not opened); root/graph (the real graph); root/iar.RUNS_FILE (agent runs file, real run 46 and 47 lines); the paper-trading-platform checkout's loop-trial.json via clone. Test 29 skips if no corrected run 47 exists.
- These tests exercise MailboxProposer (proposer.py) and the plan file, not MailboxFileProposer. I did not grep tests for MailboxFileProposer or file_proposer; none is shown in the 60+20 lines read.

PATHS CITED: tools/ratchet/file_proposer.py, tools/ratchet/proposer.py, tools/ratchet/loop.py, tools/exp_dag.py, tools/decider/afterwards.py, tools/kgraph/defend.py, tests/agent_program/test_stage3_proposer.py, tests/agent_program/realrecords.py (not opened), all under /home/user/Markets.
