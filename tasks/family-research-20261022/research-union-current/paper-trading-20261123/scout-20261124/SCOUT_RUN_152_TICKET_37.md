# Scout run 152 (Haiku): where things are for ticket 37

Kept word for word as the agent returned it, 2026-11-24 (twenty-fifth session). Nothing below this line is the main session's.

---

SCOUT RUN 152 REPORT (ticket 37). Tool calls used: 24 of 28. Stopped on my own accord with 4 calls unused; nothing exhausted. Quotes are exact.

## 1. Rule-version-as-experiment-node wording (adoption plan and paper-trading-20261123 *.md)

Adoption plan: /tmp/claude-0/-home-user/3356516d-d71a-5e13-907d-ff8d8ffcb6d4/scratchpad/frankie_handoff_20261123_2/CLAUDE_ARCH_PLAN_GRAPH_ENGINEERING_ADOPTION_20261123.md
- :160 `graph that the rule rests on. Each edit is a commit; each version is a node in the stage-2 DAG.`
- (Grep for the literal "rule version|rule edit|version a node|RuleVersion|rule_version" returned NO MATCHES in this file. The match above came from the looser pattern `rule.{0,40}(node|commit|version)`.)

/home/user/markets-data/tasks/family-research-20261022/research-union-current/paper-trading-20261123/ (*.md at top level), matches for `rule version|rule edit|version a node|RuleVersion|rule_version`:
- MISSING_PIECES_20261124.md:36 `so every paper order traces to registered claims and their checks. Today: 60 rule versions, all 60 ask for`
- MISSING_PIECES_20261124.md:107 `37. Rule versions are not nodes of the experiment record for the own platform (the plan: each rule edit a`
- MISSING_PIECES_20261124.md:108 `    commit, each version a node there); they are in the graph only.`
- AGENT_BUILD_CHECKLIST_20261124.md:29 `1,684 fills, 25 rule versions, trial \`exp-2633f97cb6b9\`; \`kgraph check\` prints "no breach".`
- AGENT_BUILD_CHECKLIST_20261124.md:96 `State today: 60 rule versions in the graph (30 of the own platform, 30 of the old runner); the grounding check`
- AGENT_BUILD_CHECKLIST_20261124.md:99 `- [ ] 20. The grounding check is seen running on the platform's 30 rule versions and its result is kept.`
- AGENT_BUILD_CHECKLIST_20261124.md:100 `  Shown by: \`rule_versions check --record\` after step 5, 30 Evaluation lines for the platform's rule versions.`
- AGENT_BUILD_CHECKLIST_20261124.md:104 `- [ ] 22. A rule version is tied to the claims read from the lines its \`finding\` link points at, by fixed code,`
- OWN_PLATFORM_WISHLIST_20261123.md:66 `28. Append-only: every signal, order, fill and status change, each with its time in nanoseconds, the rule version`
- OWN_PLATFORM_WISHLIST_20261123.md:69 `30. Every order is traceable back: fill to order to rule version to the finding the rule rests on. DECIDED (plan 7d)`
- Ticket 37 text (tickets-44-20261124/37.md:3, same wording as MISSING_PIECES:107-108): `Rule versions are not nodes of the experiment record for the own platform (the plan: each rule edit a commit, each version a node there); they are in the graph only.`
- tickets-44-20261124/37.md:9 `- [ ] Shown done by: each platform rule version is a node of the experiment record as well as of the graph`
- tickets-44-20261124/README.md:54 (ticket 37 row, status ready)
- Other hits in that folder (not top-level *.md, listed for completeness, not requested): audits-20261124/AUDIT_RUN_120.md:161; review-20261124/run57-item28-30-event-history-trace.md:225 and :409; scout-20261124/SCOUT_RUN_117_TICKETS_07_08_09.md:35-42, :77, :95, :104; tickets-20261124/02-grounds-read-into-the-graph.md:11-12; tickets-44-20261124/07.md:3, :9.

## 2. How a platform rule version is stored in the GRAPH

Node files in /home/user/markets-data/graph/nodes (14): AgentRun, Claim, CalcOutput, Commit, DipoleEvent, Evaluation, Entity, Fill, Order, Render, Peak, TradeDay, Source, Task (.jsonl each).

Grep "RuleVersion|rule_version|rule version|paper-rules|VERSIONS.md" (case-insensitive), count per file, total 759 occurrences across 8 files:
- Claim.jsonl 27
- Commit.jsonl 1
- Entity.jsonl 66
- Evaluation.jsonl 30
- Fill.jsonl 72
- Order.jsonl 560
- Source.jsonl 2
- Task.jsonl 1
(Fill and Order hits are rule_version attrs on order/fill records, not counted as rule-version nodes here.)

Node kind that holds a rule version: **Entity**, with attrs `entity_kind` = `"rule version"`. First three lines of Entity.jsonl with that value (matched text, from -o):
- Entity.jsonl:93 `"attrs": {"commit": "74b1f223451343ec5e15a3cb8b5e8c4dfbc0b3cb", "entity_kind": "rule version", "name": "CL05 at 74b1f22345", "repo": "DavisAI1974/paper-trading-platform", "run": "orders-20261124T010517Z", "strategy": "CL05", "trial": "exp-1c51cc953e8b"}`
- Entity.jsonl:94 `"attrs": {"commit": "74b1f223451343ec5e15a3cb8b5e8c4dfbc0b3cb", "entity_kind": "rule version", "name": "CL06 at 74b1f22345", ... "strategy": "CL06", "trial": "exp-1c51cc953e8b"}`
- Entity.jsonl:95 `"attrs": {"commit": "74b1f223451343ec5e15a3cb8b5e8c4dfbc0b3cb", "entity_kind": "rule version", "name": "CL07 at 74b1f22345", ...}`
- Entity attrs seen on rule-version nodes: commit, entity_kind, name, repo, run, strategy, trial. The rule file's PATH, COMMIT and SHA256 are NOT on the Entity attrs in these lines (the commit is there; path and sha256 are not). The rule file path and sha256 are not found on any rule-version node.
- Rule-version commit node: Commit.jsonl:22 (`written_by: "code:tools.kgraph.rule_versions@3104192618"`).
- Source.jsonl and Task.jsonl matches are VERSIONS.md of markets-data `tasks/family-research-20261022/research-union-current/strategy-20261123-claude/VERSIONS.md`: Source.jsonl:437 (`"sha256": "d838b3d2575055ec089d15b4edc58ee1093cbe6e...`), Source.jsonl:543, Task.jsonl:49 (state not_extracted). That file is not a platform rule file as far as this match shows.
- Graph manifest /home/user/markets-data/graph/MANIFEST.json: not searched (out of my call budget).

## 3. tools/exp_dag.py (the experiment record)

Storage (docstring 3-16): experiments/trials.jsonl (record, append-only), experiments/frankie_exp_dag.sqlite (index, rebuilt), experiments/MANIFEST.json. Verbs (docstring :15): push, fetch <id>, log, children <id>, leaves, lineage <id>, diff <a> <b>; also set-status <id> <status>, rebuild.

- Constants: :34-37 (EXP_DIR, RECORD, SQLITE, SCHEMA_VERSION). STATUSES :41 `("kept", "reverted", "crash", "recorded")`. FIELDS :43-44 `("parent", "agent_run", "hypothesis", "change", "metrics", "runtime_s", "environment", "status", "links", "loop", "note")`.
- Node/table kinds: the record is trial lines (no node kinds in exp_dag). SQLite tables, created in rebuild(): `create table trial` (:199-202), `create table metric` (:203-204), `create table link` (:205).
- Class ExpDag :51; __init__ :52-57; lines :60; latest :68; _append :75; _check :82 (change must be {repo, commit}, see :93-94); push :100-120; set_status :122; fetch :136; log :140; children :148; leaves :151; lineage :155; diff :164-190 (git diff --stat of two commits, :185); rebuild :191-233; write_manifest :235; main :264-310.
- ADD a node: `ExpDag.push(self, *, hypothesis, status, parent=None, agent_run=None, change=None, metrics=None, runtime_s=None, environment=None, links=None, loop=None, note=None, key=None, written_by) -> str` at :100-104. Key rule: `key` is a natural key, same key = same entry (:105-106); id = "exp-" + sha(["key", key]) (:113); returns the tid (:120).
- Link a node to a parent: `parent=` argument of push (:100, stored in body at :107). There is no separate link function. Verb: `--parent` (main :271).
- Commit id on a node: `change={"repo": ..., "commit": ...}` (:93-94 validated; :107 stored); CLI `--repo`/`--commit` (:273-274, combined to change at :310). Shown in _show :259.
- Verb to add: CLI `push` (main :268-281; --hypothesis :269, --status :270 choices STATUSES, --parent :271, --commit :274, --key :281, --by required :282).
- Read-only verbs: fetch (:136), log (:140), children (:148), leaves (:151), lineage (:155), diff (:164). Note `rebuild` (:191) writes the sqlite, and `set-status` (:122) appends a new rev line.
- Line ranges a builder must read (about 134 lines): :1-60 (docstring, constants, class head); :100-121 (push); :191-205 (rebuild head); :264-300 (main head). Also :93-94 (_check change rule).
- Note: rule_versions.py load pushes rule versions into THIS record already: rule_versions.py:52-59 `parent = dag.push(... status="recorded", parent=parent, change={"repo": REPOS[REPO], "commit": c}, ... key=f"rule-version:{c}", written_by=by)`. Rule version edits are therefore written to trials.jsonl under key `rule-version:<commit>` by code (see section 6).

## 4. Tests of exp_dag (tests/)

Grep "exp_dag" in /home/user/Markets/tests returned 8 files (import lines only for most):
- tests/agent_program/test_decider_loop.py:20
- tests/agent_program/test_live_platform.py:13
- tests/agent_program/test_stage2_exp_dag.py:8 (import ExpDag, Refused)
- tests/agent_program/test_stage3_proposer.py:67
- tests/agent_program/test_stage3_ratchet.py:23
- tests/agent_program/test_stage4a_graph_store.py:114 (fixture data text containing "tools/exp_dag.py")
- tests/agent_program/test_stage7d_platform.py:10
- tests/agent_program/test_stage7f_rule_versions.py:10

Scratch-record fixtures (exp_dir= a tmp folder, so markets-data is not written):
- test_stage2_exp_dag.py: fixture `loaded(tmp_path)` :15-19 (`ExpDag(root, exp_dir=tmp_path / "experiments")`, plus GraphStore at :19). Tests: :24 test_one_trial_for_each_run_folder_and_each_figure_is_the_receipts; :43 test_loading_twice_adds_nothing; :50 test_the_verbs; :62 test_a_reverted_and_a_crashed_trial_stay_in_the_record; :77 test_what_is_refused.
- test_stage7f_rule_versions.py: module fixture `made(tmp_path_factory)` :22-30 (`tmp = tmp_path_factory.mktemp("g")`, `dag = ExpDag(root, exp_dir=tmp / "experiments")` at :30). Tests: :38 test_each_edit_of_the_rules_is_a_trial_in_the_order_it_was_made; :52 test_each_paper_run_is_tied_to_the_rule_version_it_ran_under; :72 test_a_rule_version_rests_on_no_finding_yet_and_the_check_says_so; :85 test_the_rules_loop_has_its_control_file_guards_the_right_files_and_waits_for_no_figure.
- Not read: test_stage7d_platform.py, test_stage4a, others (import lines only).

## 5. Rule files: /home/user/markets-data/paper-rules/

- Glob paper-rules/** and paper-rules/* both returned the same 100 paths (truncated by the tool at 100, "more than 100 matches"). Every path seen is under paper-rules/20261109/ (the only top-level folder shown). Count: 100 listed, total not known (truncated). Files include README.md, RESTART_HANDOFF.md, NEXT_CHAT_HANDOFF.md, machine/*.json, platform/CME_CAPABILITIES.json, paper_rules/*.py, reconciliation/*.gz.
- /home/user/markets-data/MARKET_DATA_INDEX.md:17 (`[Omitted long matching line]`, mentions paper-rules); :19 `[latest recovery/runtime update](paper-rules/20261109/RECOVERY_RUNTIME_UPDATE.md) adds 22 exact median states`; :21 `Latest continuation: [restart handoff and section-level reconciliation findings](paper-rules/20261109/RESTART_HANDOFF.md)`.
- /home/user/Markets/tools/README_AGENT_PROGRAM.md:39 (`4b. Filling it, no model | ... rule_versions.py`); :49 `| 7f. Rule versions | \`rule_versions.py\` | \`load\`, \`check [--record]\` |`; :55 (`a rule version, a merge taken back ...`); :104 `(\`porder:<order id>\`) and each \`fill\` row ... with the rule version`; :106 (run with a receipt.json as one trial).
- Note: the rule files RULE_FILES constant and the platform repo are in /home/user/Markets/tools/kgraph/rule_versions.py (not read); the platform repo is DavisAI1974/paper-trading-platform.

## 6. Programs in /home/user/Markets/tools that turn rule versions into graph nodes

- tools/kgraph/rule_versions.py (the program):
  - :3-4 usage: `load [--data] [--platform]`, `check [--record] [--reviewer run:00NN]`
  - :37 `def load(dag: ExpDag, store: GraphStore, platform_dir) -> dict:` (lines 37-86 per earlier scout, not all re-read)
  - :39 `commits = git(platform_dir, "log", "--reverse", "--format=%H", "--", *RULE_FILES).split()`
  - :52-59 `dag.push(...)` with `key=f"rule-version:{c}"` (the experiment record write, one per rule commit)
  - :63-68 Entity lookup: `for rv in store.nodes("Entity")`, `if rv["attrs"].get("entity_kind") != "rule version"`, `link("DERIVED_FROM", rv["id"], f"commit:{REPO}:{version[:10]}", ...)` at :68
  - :78-80 Task nodes for run commits not in checkout
  - :90 `def check(store, dirs, reviewer, run, record=True)`; :91 `rvs = [e for e in store.nodes("Entity") if e["attrs"].get("entity_kind") == "rule version"]`
  - :106 `def main(argv=None)`; :127 reviewer default; :131 print per rule version
  - Also :38 `by = code_stamp("tools.kgraph.rule_versions")`
- tools/kgraph/ingest_paper.py: :213 `a["rule_version"] = rulever_id(it["strategy"], rule_commit)`; :303, :326, :332 (`rep["rule_versions"] = len(versions)`), :339-340 `edges.append(link("PLACED_BY", oid, a["rule_version"]))`.
- tools/kgraph/ingest_platform.py:268 `"rule_versions": len(versions)`.
- tools/kgraph/live.py:153, :156 rule_versions counts.
- tools/kgraph/grounding.py:399 and :430 (`rule_versions_checked`).
- tools/kgraph/context.py:406 and ingest_artifacts.py:170-176 are "CURRENT VERSIONS" (Artifact), not rule versions.
- tools/ratchet/programs/paper_rules.md:4, :73 (`python3 -m tools.kgraph.rule_versions check`).
- NOT FOUND in tools/: a function named rulever_id definition (only the call at ingest_paper.py:213 was seen); `VERSIONS` string not found in any tools/ file in the grep (VERSIONS only matched CURRENT VERSIONS above).

## NOT FOUND
- Rule file PATH, COMMIT and SHA256 as attributes of a rule-version node: searched graph/nodes (all 14 files with the Entity lines above); not on Entity attrs (attrs keys seen: commit, entity_kind, name, repo, run, strategy, trial). The commit is there; path and sha256 are not seen.
- Literal "RuleVersion" class or table: not found in tools/ or tests/ (grep of the whole tools/ tree for RuleVersion returned no match, only rule_version/rule version lines above).
- Literal phrases "each rule edit a commit" and "each version a node" in the plan: not found as written; closest is plan :160 quoted above.
- graph/MANIFEST.json and experiments/MANIFEST.json, experiments/trials.jsonl: not searched (budget). experiments/frankie_exp_dag.sqlite: not opened (binary, per instructions).
- paper-rules/ total file count: not determinable (Glob truncated at 100; only folder 20261109 seen in the listing).

Tool calls: 24 (9 + 8 + 6 + 1). No writes.
