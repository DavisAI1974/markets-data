# Scout run 197 (Haiku): where things are for ticket 37

Everything below this line is the agent's own report, word for word; nothing below it is the main session's.

## Hand-back 1 of 1

Scout run 197, ticket 37.

Tool calls used: 19 of 30, all Read/Grep/Glob, no Bash, no writes. By name: Read 12, Grep 6, Glob 1. No model-call count was given with the run plan, so I have not reported one.

Note: the ratchet control file and the grounding module are outside the named set; I cite them only where a hit touched rule versions.

A. tools/kgraph/rule_versions.py (137 lines). Functions:
- L1-17 module docstring. L19-34 imports, RULE_FILES, REPO, LOOP_PROGRAM.
  L32: RULE_FILES = ("tasty/paper/rules_cl.py", "tasty/paper/rules_cx.py")
  L33: REPO = "paper-trading-platform"
- L37 `def load(dag: ExpDag, store: GraphStore, platform_dir) -> dict:`
  L39: commits = git(platform_dir, "log", "--reverse", "--format=%H", "--", *RULE_FILES).split()
  L40: runs = [t for t in dag.log() if (t.get("key") or "").startswith("paper-run:") and t.get("change")]
  L45: in_force[c] = git(platform_dir, "log", "-1", "--format=%H", c, "--", *RULE_FILES) or None   (inside try; RuntimeError -> None, L46-47)
  L50: files = git(platform_dir, "show", "--format=", "--name-only", c).split()
  L53: hypothesis=git(platform_dir, "log", "-1", "--format=%s", c)
  L61: nodes = {n["id"]: n for n in (commit_node(REPO, platform_dir, c) for c in commits)}
  L63-70: loop over store.nodes("Entity") with entity_kind "rule version"; version = in_force.get(rv["attrs"]["commit"]); edges.append(link("DERIVED_FROM", rv["id"], f"commit:{REPO}:{version[:10]}", key="rule version in force", what="the commit that last changed the rule files before the run's own code commit", found_by="git log -1 <run commit> -- " + " ".join(RULE_FILES)))
  L72-81: unplaced runs -> Task node `task:run-commit-not-in-checkout:<sha>`
  L82: graph = store.write(...)
- L90 `def check(store, dirs, reviewer, run, record=True)`: L91 selects rule-version Entities; L95 grounding.check_node; L100 grounding.record. (Grounding check, not a git read.)
- L106 `def main(argv=None) -> int`: L112 subparsers `load` and `check`; L113 sub.add_parser("load"); L114-115 check with `--record` (store_true) and `--reviewer`.
- Platform checkout reads: only the git commands at L39, L45, L50, L53, and commit_node at L61 (sources.py).

Graph node + edge for one rule edit: the rule_versions.py `load` writes no graph node per rule edit; it writes only the 5 experiment-record trials (L52-59) and the commit nodes (L61) plus DERIVED_FROM edges (L68) and Task nodes (L78-81). The graph rule-version Entities come from ingest_paper.py and ingest_platform.py (see B). The graph Entity `rule version` nodes are read (L63-70) and linked; they are not created here.

The record push, L52-59, verbatim:
  parent = dag.push(
      hypothesis=git(platform_dir, "log", "-1", "--format=%s", c), status="recorded", parent=parent,
      change={"repo": REPOS[REPO], "commit": c}, metrics=[], links=under,
      environment={"what": "one edit of the paper runner's rules", "rule_files_changed": [f for f in files if f in RULE_FILES],
                   "files_changed": len(files)},
      note="A rule version. It carries no figure: nothing from the sandbox feed is scored. "
           "Linked: the paper runs that ran under it.",
      key=f"rule-version:{c}", written_by=by)
  Key = `rule-version:<commit>`; parent = previous rule commit (None for the first); status = "recorded"; links = `under` (L51: sorted ids of paper runs whose in_force commit == c); L60 ids[c] = parent.

CLI verbs (L3-4): `python3 -m tools.kgraph.rule_versions load [--data] [--markets] [--platform] [--graph-dir]` and `python3 -m tools.kgraph.rule_versions check [--record] [--reviewer run:00NN]`.

B. Graph rule-version Entities (grep `rulever:` / `rule version`; hits quoted by file:line).
- tools/kgraph/ingest_paper.py:
  L55-56: `def rulever_id(strategy, commit): return f"rulever:{strategy}@{commit[:10]}"`  (id form CL01@74b1f22345)
  L213: a["rule_version"] = rulever_id(it["strategy"], rule_commit)   (in _build_orders, def L160)
  L326: versions = {o["attrs"]["rule_version"]: o["attrs"]["strategy"] for o in orders.values() if o["attrs"].get("rule_version")}
  L327-331: nodes.append({"id": rv, "type": "Entity", "attrs": {"name": f"{strat} at {commit[:10]}", "entity_kind": "rule version", "strategy": strat, "commit": commit, "repo": REPOS[PLATFORM_REPO], "run": name, "trial": trial_id(name)}}) ; L331: edges.append(link("DERIVED_FROM", rv, cnode["id"]))
  L339-340: PLACED_BY edge from order to rv.
  Where the commit comes from: L310-311 `commit = json.loads((folder / "receipt.json").read_text(...))["code_commit"]` = the RUN's code commit, not a rule file's last edit. Node is written inside `paper(store, platform_dir)` (def L277). `_build_orders` def L160, `rulever_id` L55.
  Lines 213 derive rule_commit from the run's own rows (passed in as `rule_commit`, = commit when cnode, L322).
- tools/kgraph/ingest_platform.py:
  L69-70: `def rulever_id(rule, commit): return f"rulever:platform:{rule}@{commit[:10]}"`
  L211-213: `if row.get("rule") and row.get("rule_commit"): rv = rulever_id(row["rule"], row["rule_commit"]); edges.append(link("PLACED_BY", nid, rv))`
  L216-219: versions.setdefault((row["rule"], row["rule_commit"]), set()) ; findings collected.
  L220-221: `for (rule, commit), findings in sorted(versions.items()): rv = rulever_id(rule, commit)`
  L235-237: node {"id": rv, "type": "Entity", "attrs": {"name": f"{rule} at {commit[:10]}", "entity_kind": "rule version", "rule": rule, "commit": commit, "repo": ..., "platform": "own paper platform"}}
  L238: edges.append(link("DERIVED_FROM", rv, cnode["id"]))   -> the Commit node of `commit` (rule_commit from the journal row, from L224 commit_node or L231 fallback id `commit:paper-trading-platform:<10>`).
  L242-243: DERIVED_FROM rv -> src:link finding node, key "finding".
  Function containing L196-243: load_run, def L177. Commit source: the journal row's `rule_commit` (L211, L216), not a git log.
- The "rulever:" hits outside writers: tools/kgraph/rule_versions.py L63-70 (reads); tests/agent_program/test_stage4b_resolve.py:118 (asserts no rulever: in brief); tools/README_AGENT_PROGRAM.md:104-106 (doc).
- The 60 nodes: I did not open graph/nodes/Entity.jsonl; per reviewer, `rulever:CLxx@74b1f22345` form comes from ingest_paper (L56) keyed on the run's code commit.
- DERIVED_FROM edge for ingest_paper rulever nodes: dst = the run's Commit node `commit:paper-trading-platform:<10>` (L331). For ingest_platform rulever nodes: dst = the Commit node of the journal row's rule_commit (L238). The rule_versions.py DERIVED_FROM (L68, key "rule version in force") has dst = `commit:paper-trading-platform:<10 of in-force commit>`; grep found that key string only at rule_versions.py:68.

C. Code that finds the commit that last edited a rule file for a run's commit. Grep for `log`, `-1`, `--format` in ingest_paper.py, ingest_platform.py, rule_versions.py, sources.py:
- tools/kgraph/rule_versions.py:45  in_force[c] = git(platform_dir, "log", "-1", "--format=%H", c, "--", *RULE_FILES) or None   <- the only one that finds a rule file's last edit at a run commit.
- tools/kgraph/rule_versions.py:39  git log --reverse --format=%H -- RULE_FILES (all rule commits).
- tools/kgraph/rule_versions.py:50  git show --format= --name-only c (files of a commit).
- tools/kgraph/rule_versions.py:53  git log -1 --format=%s c (subject).
- tools/kgraph/rule_versions.py:70  found_by string "git log -1 <run commit> -- ...".
- tools/kgraph/sources.py:49  out = git(repo_dir, "log", "-1", "--format=%H", "--", rel_path)   (last commit touching a path; caller not checked in this run; this is the generic helper, not a rule-version lookup).
- tools/kgraph/sources.py:103  git(repo_dir, "log", "-1", "--format=%s%x00%cI", full)   (commit subject/date, via commit_node).
- tools/kgraph/ingest_paper.py: no `log`, `-1` or `--format` hit. (Grep showed only `receipt`, L311 and L355.)
- tools/kgraph/ingest_platform.py: no `log -1` or `--format` hit; `_git` def L77; `rev-parse` L89; `fetch` L91; `show` L101.

D. tools/exp_dag.py.
- L100-120 `def push(self, *, hypothesis, status, parent=None, agent_run=None, change=None, metrics=None, runtime_s=None, environment=None, links=None, loop=None, note=None, key=None, written_by) -> str`. Docstring L105-106: "`key` is a natural key (a run folder, a commit) so that loading the same thing twice makes one entry; without it every push is a new entry."
- Refusal: `self._check(body, known)` at L111 raises Refused for: hypothesis missing (L84), status not in STATUSES (L85-86), parent not in record (L87-88: `if body.get("parent") and body["parent"] not in known: raise Refused(f"parent {body['parent']} is not in the record")`), each link not in record (L89-91: `linked trial {other} is not in the record`), change not {repo, commit} (L92-94), metric shape (L95-97).
- Duplicate key: NOT refused. tid = "exp-" + sha(["key", key]) (L113); if the latest revision has the same content_sha it returns tid unchanged (L116-117); if content differs it appends rev+1 (L118-119).
- Links: `links` is a list of trial ids that must already be in the record (L89-91). `parent` is one trial id that must already be in the record (L87-88). `set_status` at L122-134 is the other writer.
- CLI push: exp_dag.py L271 `--parent`, L281 `--key`, L311-313 print(dag.push(hypothesis=a.hypothesis, status=a.status, parent=a.parent, agent_run=a.agent_run, ..., links=a.link, loop=a.loop, note=a.note, key=a.key, written_by=a.by)). L18 usage line `python3 -m tools.exp_dag push --hypothesis "..." --status recorded --key paper-run:orders-...`.

E. Check-file tests touching rule versions.
tests/agent_program/test_stage7f_rule_versions.py (97 lines):
- L38 def test_each_edit_of_the_rules_is_a_trial_in_the_order_it_was_made(made): L41 `assert len(commits) >= 5 and report["rule_versions"] == commits`; L43 `assert [t["change"]["commit"] for t in trials] == commits`; L45 `assert [t["parent"] for t in trials[1:]] == [t["id"] for t in trials[:-1]]          # each on the one before`; L47 `assert t["hypothesis"] == _git(plat, "log", "-1", "--format=%s", c) and t["status"] == "recorded"`; L48 `assert t["metrics"] == []`; L49 `assert store.node(f"commit:paper-trading-platform:{commits[-1][:10]}")["attrs"]["sha"] == commits[-1]`
- L52 def test_each_paper_run_is_tied_to_the_rule_version_it_ran_under(made): L59 `assert run["id"] in by_commit[in_force]["links"]`; L60 `assert report["in_force"][run["change"]["commit"]] == in_force`; L64 `assert mine`; L67 `assert f"commit:paper-trading-platform:{in_force[:10]}" in ends`; L69 `assert again["written"] == {"trials_new_or_revised": 0, ...}`
- L72 def test_a_rule_version_rests_on_no_finding_yet_and_the_check_says_so(made): L76 `assert out["checked"] == len(rvs) == 30 and out["need_evidence"] == 30`; L78 `assert len(evals) == 30 and {e["dst"] for e in store.edges("EVALUATES")} == {r["id"] for r in rvs}`; L81 `... ["evaluations_written"] == 0   # one line a check`
- L85 def test_the_rules_loop_has_its_control_file_guards_the_right_files_and_waits_for_no_figure(made): L91 `assert set(rules) >= set(_git(plat, "ls-files", *rule_versions.RULE_FILES).splitlines())`
tests/agent_program/test_stage7d_paper.py:
- L32 def test_counts_of_run_1_as_the_ledger_and_receipt_hold_them(made): L53 `assert r["rule_versions"] == len({t["strategy"] for t in ledger}) == 13`
- L88 def test_every_order_is_placed_or_reported(made): L94 `assert (o["id"] in placed) == bool(o["attrs"].get("rule_version"))`; L98 `assert rv["attrs"]["entity_kind"] == "rule version"`
tests/agent_program/test_stage7d_platform.py:
- L71 def test_each_fill_fills_one_order_and_each_order_has_a_rule_version(made): L84 `assert n["attrs"]["entity_kind"] == "rule version"`; L85 `assert rv == ipf.rulever_id(o["attrs"]["rule"], o["attrs"]["rule_commit"])`
- L93 def test_the_trial_counts_equal_counts_made_from_the_journal(made) (rule version counts not read in detail).
Outside the three named files (touch rule versions, for completeness): tests/agent_program/test_stage4c_grounding.py:169, :174; tests/agent_program/test_platform_scope.py:121-122; tests/agent_program/test_stage4b_resolve.py:118.

F. Platform rule files: /home/user/paper-trading-platform/paper_platform/rules/ holds 32 files (Glob, `**/*`): 17 CL (CL01 to CL17) and 15 CX (CX01 to CX15). Files: CL01 CL02 CL03 CL04 CL05 CL06 CL07 CL08 CL09 CL10 CL11 CL12 CL13 CL14 CL15 CL16 CL17; CX01 CX02 CX03 CX04 CX05 CX06 CX07 CX08 CX09 CX10 CX11 CX12 CX13 CX14 CX15.
CL01.json keys (/home/user/paper-trading-platform/paper_platform/rules/CL01.json, L1-8): "id" (CL01), "family" (CL), "role" (entry), "source" (a markets-data GitHub URL pinned to commit 46199c5f...), "evidence" (same, EVIDENCE.md), "specification" (text, "## CL01 (v2). The eaten level ...").
Note: RULE_FILES at rule_versions.py:32 names tasty/paper/rules_cl.py and tasty/paper/rules_cx.py, not these JSON files. I did not check whether those .py paths exist in the checkout.

NOT FOUND:
- A builder-side search for "the commit that last edited each rule file" inside ingest_paper.py or ingest_platform.py: none (patterns `log`, `-1`, `--format`, `rev-parse`, `show` searched in tools/kgraph/{ingest_paper,ingest_platform,rule_versions,sources}.py).
- Platform rule-file contents for the rule-version identity beyond CL01.json: not read (CX files and other CL files not opened).
- Graph Entity.jsonl counts (60 nodes, 4 commits) and experiments/trials.jsonl (5 records): not opened; figures are the reviewer's (REVIEW_RUN_181, L20-24 and L13-18).

Tool count: 19 of 30 (Read 12, Grep 6, Glob 1).
