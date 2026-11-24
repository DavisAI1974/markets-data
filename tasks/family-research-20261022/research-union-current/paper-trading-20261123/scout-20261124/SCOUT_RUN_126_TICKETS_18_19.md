# Scout run 126 (Haiku): where things are for tickets 18 and 19

Kept word for word as the agent returned it, 2026-11-24 (twenty-fifth session). Nothing below this line is the main session's.

---

AGENT RUN 126 REPORT (scout). My true count: 20 tool calls, the limit. I stopped there. Parts (a)-(j) are NOT all covered; gaps are listed at the end.

TICKET TEXT (copied)
- /home/user/markets-data/tasks/family-research-20261022/research-union-current/paper-trading-20261123/tickets-44-20261124/18.md:3 "What is missing ... NO RUN HAD ITS BUDGET WRITTEN IN A PLAN BEFORE IT STARTED. The plan: max model calls, sub-agents, concurrent workers, tool calls, tokens, wall clock, retries and graph writes, in the run's plan JSON, and on running out the run returns what is done, what is open and why it stopped."
- same folder, 18.md:9 "- [ ] Shown done by: before each run a plan holds the eight limits; a run that reaches one stops and returns what is done, what is open and why"
- .../tickets-44-20261124/19.md:3 "...It asks for the model, input tokens, output tokens, wall clock and outcome. Recorded: the harness's one total, the model by its short name; ten stopped runs have no figure; runs 99, 100 and 101 are not recorded yet."
- 19.md:9 "- [ ] Shown done by: each run's record has the exact model, input tokens, output tokens, wall clock and outcome; today's runs filled in from their own transcripts, the stopped ones too"

(a) /home/user/Markets/tools/swarm/plan.py: 113 lines (under 150), read in full.
- :24-25 BUDGET_KEYS = ("max_model_calls", "max_sub_agents", "max_concurrent_workers", "max_tool_calls", "max_tokens", "max_wall_clock_s", "max_retries", "max_graph_writes")
- :32 class PlanRefused(ValueError) - docstring: "The plan is over its own budget, or is not complete. The message names the figure."
- :36 class RunPlan (dataclass; fields name, workload, models, efforts, max_output_tokens, cutoff, events, budget, estimate_per_event, estimate_total_input_tokens, estimate_note, not_estimated, graph_dir, greg_go)
- :53 RunPlan.to_json; :56 RunPlan.from_json; :60 RunPlan.load; :64 RunPlan.write (no docstrings)
- :68 def estimates(store, event_ids) (no docstring)
- :76 def make_plan(...) (no docstring)
- :89 def check(plan: RunPlan) -> None - docstring: "Refuse a plan that is incomplete or whose estimate is over its budget; the message names the figure." Checks at :91 (all 8 BUDGET_KEYS present, non-negative numbers), :94 no events, :96 estimate order, :98 estimate total, :100 model ids in M.MODELS, :104 max_concurrent_workers >= 1, :106 estimate vs max_tokens, :109 events vs max_model_calls, :111 events vs max_sub_agents.
- Module docstring lines 1-11: the estimate covers worker INPUT only (chars/4); the workers' output, reducer, refute wave and retries are bounded by the budget as the run goes.

(b) /home/user/Markets/tools/swarm/run.py. Grep `max_|budget|exhaust|stopped|reason`, 60-line head limit (hit cap reached; 60 lines shown).
- 4, 8, 12-16: docstring (run plan, budget; "on exhaustion it stops and returns the completed events, the unresolved events and the reason")
- 43 section comment "the budget, enforced as it goes"; 45 class Budget; 48 Budget.__init__; 53 elapsed; 56 def reason_exhausted (checks at 58 wall clock, 60 graph writes, 62 model calls, 64 tokens); 68 def reserve(tokens, new_agent) (71 reason_exhausted; 72 max_tokens; 75-76 max_sub_agents); 84 def settle (budget counted per call); 89 def take_retry (91 max_retries); 96 def count_writes; 100 def snapshot; 108 _tokens_of
- 115 _counting; 118-121 graph writes counted; 128 _call_job (131 need = est_in + max_out; 136 caller.call; 138-149 settle; 139-140 retry); 159-164 stop_reason outcome text; 188 _fan_out (docstring 189-190 "Returns (the jobs never started, the reason launching stopped or None)"; 197 reserve; 208-209 "a budget used up with nothing left to do is not a stop")
- 215 def run_plan(plan, caller, store): 216 P.check(plan); 217-218 refuses if greg_go empty; 219 Budget(plan.budget); 254-258 workers stop reason; 256 "not started: " + reason; 288-292 refute wave stop reason
- 303 _store, 307 cmd_plan, 355 cmd_go, 383 main.
- RETURN SHAPE (run.py:296-298): {"plan", "completed_events", "unresolved" (dict event -> reason), "stopped_because" (string or None), "refute_wave_events", "agent_runs" ({"workers": [...], "refuters": [...], "reports"}), "budget_used" (budget.snapshot()), "synthesis"}.

(c) /home/user/markets-data/tasks/family-research-20261022/research-union-current/paper-trading-20261123/run-plans/run-0122.json, read in full (21 lines). Keys: run 122, session, agent "builder", model "claude-sonnet-5-5", task, written_before_the_run_started true, max_model_calls 60, max_sub_agents 0, max_concurrent_workers 1, max_tool_calls 70, max_tokens 500000, max_wall_clock_s 2400, max_retries 1, max_graph_writes 0, max_graph_writes_is, max_tokens_is, on_reaching_a_limit "the run stops and returns what is done, what is open and why it stopped", note. Note: this plan has no max_trials and no greg_go field; it is not the swarm's plan.py shape.

(d) /home/user/Markets/tools/ratchet/:
- budget declared in program.py: BUDGET_KEYS at :16-17 (max_trials, max_wall_clock_s, max_model_calls, max_sub_agents, max_concurrent_workers, max_tool_calls, max_tokens, max_retries, max_graph_writes); Program.budget :48; parse() :90 reads budget :149-151 (_count per key), :168 budget={k: bud[k] ...}.
- enforcement: loop.py USAGE_BUDGET :48-49; run_loop at loop.py:201 (budget = program.budget at :218; max_retries :256); the stop check at loop.py:341-362 (max_trials :350, max_wall_clock_s :352, max_graph_writes :354; "stopped = f'budget exhausted: {over}'" :361). Return includes "budget_used" at :445.
- ready.py:204-212 checks every budget key is declared before a run.

(e) /home/user/Markets/research/kalshi/frankie_boss/CLAUDE_ARCH_PLAN_GRAPH_ENGINEERING_ADOPTION_20261123.md lines 38-52 (copied):
38 ## Token plan (applies to every stage)
39 (blank)
40 1. Model routing. Haiku: search, reading docs, extraction, per-event fan-out workers. Sonnet:
41    building, tests, entity resolution, graph queries, reducers. Opus: plans touching core
42    Frankie paths, repeated failures, final review, refute waves on high-stakes findings only.
43 2. Declared budget per run (paper section VIII.B), written in the run's plan JSON before it
44    starts: max model calls, max sub-agents, max concurrent workers, max tool calls, max tokens,
45    max wall clock, max retries, max graph writes. On exhaustion the run returns completed work,
46    unresolved items and the reason it stopped.
47 3. Every agent run is recorded as an AgentRun entry in the graph with model, input tokens,
48    output tokens, wall clock and outcome, so token use is measured per run, not estimated.
49 4. Graph-built context replaces handoff replay (stage 5). This is the largest expected saving.
50    Speculative until measured: the saving is not known until stage 5 runs side by side with the
51    current session start and the current Frankie packet (proven packet: 92,427 input tokens at
52    3,262 rows, stacked_v1).

(f) /home/user/Markets/tools/kgraph/ingest_agent_runs.py: 135 lines (over 150? no, under 150: full file read). Defs: run_id :29; agent_runs(store) :33 (no docstring; reads RUNS_FILE line by line, :41 json.loads, :42-50 attrs incl. tokens_reported, tokens_note, input_tokens, output_tokens, tool_calls, wall_clock_ms, budget_tokens; :52-53 keeps every other key; :55-63 duplicate run numbers raise ValueError unless "corrects" and same session; :67 write); _figures :70; paper_runs(dag, store, platform_dir) :79; main(argv) :121. Module docstring :1-12: "The harness reports one token figure for a run (input and output together). It is stored as `tokens_reported`; `input_tokens` and `output_tokens` stay empty because they were never given."

(g) /home/user/markets-data/tasks/family-research-20261022/research-union-current/paper-trading-20261123/agent-runs.jsonl (line numbers from Grep):
- RUN 1 (line 1): keys in order: run, session, stage, role, model, task, tokens_reported, tokens_note, tool_calls, wall_clock_ms, outcome. model "haiku"; tokens_reported 180587; tokens_note "total tokens the harness reports for the run (input and output together; not split)".
- RUN 64 (line 67): keys in order: run, role, model, stage, task, tokens_reported, model_calls, last_call_tokens, all_calls_tokens, advisor_tokens, tool_calls, wall_clock_ms, outcome, tokens_note, session, budget_tokens, budget_note. model "claude-fable-5-2"; tokens_reported 303912; tokens_note "tokens_reported is the total the harness reports when a run ends: the last step of its last model call. last_call_tokens and all_calls_tokens are read from the run's own transcript; all_calls_tokens adds every step of every call, the advisor's included".
- RUN 114 (line 122): keys in order: run, session, stage, role, model, task, plan, tokens_reported, tokens_note, input_tokens, input_tokens_fresh, input_tokens_cache_written, input_tokens_cache_read, output_tokens, token_split_note, tool_calls, wall_clock_ms, budget_tokens, budget_note, outcome, agent_type, code_commit, tickets. model "claude-sonnet-5-5"; tokens_reported 119607; tokens_note "the harness's total for the run when it ended (input and output together)".
- Note: the file has two lines with run 104 and two with run 83 (the "corrects" revisions) and no run 99-101 line is excluded by the reader's duplicate check; run 114 appears once at line 122.

(h) NOT DONE. Glob of /root/.claude/projects/-home-user/3356516d-d71a-5e13-907d-ff8d8ffcb6d4/subagents/ returned 59 files: 21 *.jsonl, 21 *.meta.json, 17 *.prefix.json. Glob gives no sizes, so I could not pick the smallest transcript; I did not read any transcript's lines.

(i) Test file covering ingest_agent_runs: Grep `ingest_agent_runs` over /home/user/Markets/tests returned 10 files, all in tests/agent_program/: test_platform_scope.py, test_stage2_exp_dag.py, test_stage3_proposer.py, test_stage4a_graph_store.py, test_stage4b_extract.py, test_stage4b_resolve.py, test_stage4c_grounding.py, test_stage5a_context.py, test_stage6_swarm.py, test_stage7f_rule_versions.py. Not determined which one tests the ingest's own functions (no line hits returned). Test function names for the ingest: NOT FOUND in this pass; my def-grep of tests/agent_program was truncated at 100 lines and showed only test_auditor_called.py, test_decider*.py, test_defend.py, test_live_platform.py.

(j) /home/user/markets-data/tasks/family-research-20261022/research-union-current/paper-trading-20261123/audits-20261124/AUDIT_RUN_111.md, Grep "FINDINGS" -A 25 (line numbers as given):
233 E. FINDINGS
234 1. The record holds the exact model id on 25 of 115 lines and separate input and output on 3 of 115 (runs 107-109). Measured: field counts above (python over agent-runs.jsonl). Sure. Open: whether lines for runs 1-106 can be filled; their transcripts are not on this machine.
235 2. 80 lines hold the harness's one total and wall clock; 35 lines hold neither; 25 runs have no token figure on any line (list in A). Sure on the counts; the reason per run (stopped, interrupt, not yet recorded) I read only for some.
236 3. The 21 transcript-derived lines (runs 47 to 67) carry `all_calls_tokens` that exceed `tokens_reported` by a large factor (for example run 64: 303,912 reported against 25,873,032 over 105 calls; run 67: 160,941 against 9,177,121 over 77 calls). The two measure different things (the harness figure is the last call's total). Sure on the figures as written on the lines; I did not re-derive them (transcripts absent). No line states which one a limit is compared against.
237 4. For runs 107, 108, 109 the line figures equal my sums from the transcripts exactly (fresh, cache-written, cache-read, output, input, tool calls, wall clock). Sure.
238 5. Token limits were exceeded on L14, L86, L103, L114 by the harness total, and run 109's tool calls exceeded its limit by 1 (41 vs 40). ... Only L114 and L115 have an `over_budget` field; L14 and L103 are not marked. Sure on figures.
239 6. (cache-read share inference, runs 107-109)
240 7. (largest tool results; inference)
241 8. No plan JSON exists for any run in either tree; the eight limits are held as chat statements and as note text on 7 lines (runs 104-109). The code to check a plan against the eight limits exists at /home/user/Markets/tools/swarm/plan.py for the swarm; ...
242 9. Ticket 20 ...
Item 10: NOT SHOWN. The Grep for "FINDINGS" stopped at line 243 ("[Omitted long context line]"), so item 10 is probably that omitted line; I did not read it. Item 10 is not copied here.

PATTERNS SEARCHED (hit counts)
- Read/Grep on tickets 18, 19 (read, full).
- tools/swarm/run.py `max_|budget|exhaust|stopped|reason`: 60 hits shown (cap of 60; more may exist). Defs grep `^\s*(def|class) `: 15 hits.
- tools/ratchet/*.py `budget|max_`: 40 shown (cap 40; more may exist). Defs grep `^\s*def `: 59 hits shown in full, none capped.
- agent-runs.jsonl `"run": 1,` 1 hit; `"run": 64,` 1 hit (line 67); `"run": 114,` 1 hit (line 122).
- tests/ `ingest_agent_runs`: 10 files.
- tests/agent_program `ingest_agent_runs|^\s*def test_`: 100-line cap reached; no ingest-specific test found in the shown part.
- AUDIT_RUN_111.md `^  [0-9]+\. `: 0 hits (the list uses no leading indent); `FINDINGS` with -A 25: 1 hit block.

TOOL CALLS: 20 (the limit). The advisor tool was not called, to stay inside the tool budget.

NOT FOUND / NOT DONE: (h) sub-agent transcript first 3 lines; (i) ingest test function names and line numbers; (j) item 10 text. Hit caps reached on the run.py grep (60), ratchet grep (40), and the tests def-grep (100). Ratchet defs enforcing budget are loop.py:201 run_loop and :341-362 (not a single named function). No files were written or edited.
