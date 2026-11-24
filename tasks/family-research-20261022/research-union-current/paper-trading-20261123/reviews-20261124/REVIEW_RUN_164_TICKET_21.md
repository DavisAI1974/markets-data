# Reviewer run 164 (Opus): ticket 21, the record's first users

Everything below this line is the agent's own report, word for word; nothing below it is the main session's.

## Hand-back 1 of 1

# Reviewer run 164 (Opus): ticket 21, the record's first users

Working copy: /home/user/wt/r165 at `74006f2` (from `git log --oneline -1`). MARKETS_DATA=/home/user/markets-data. Every `exp_dag` command below was run from /home/user/wt/r165 as `python3 -m tools.exp_dag <verb>`. I ran only the reading verbs: `--help`, `log`, `leaves`, `fetch`, `children`, `lineage` and `diff`. I ran no `push`, `rebuild` or `set-status`.

## What I read
- The scout report, all 70 lines: /home/user/markets-data/tasks/family-research-20261022/research-union-current/paper-trading-20261123/scout-20261124/SCOUT_RUN_150_TICKET_21.md
- /home/user/Markets/research/kalshi/frankie_boss/CLAUDE_ARCH_PLAN_GRAPH_ENGINEERING_ADOPTION_20261123.md lines 63-73. Line 66 lists the statuses "kept, reverted, crash". Line 70 lists the verbs `push, fetch, log, children, leaves, lineage, diff`. Lines 72-73 say: "First users: the Experiment Arms sheet of the build plan workbook (backfill its arms as nodes), the experiment orchestrator's series and survivors steps, the dipole teacher arms D0-D5."
- /home/user/markets-data/experiments/MANIFEST.json (19 lines, from `wc -l` and `cat -n`) and /home/user/markets-data/experiments/trials.jsonl (15 lines, parsed with `json.loads`, one per line).

## What the record holds: every node, counted by kind of key
I took the key prefix before the first `:` of each line in trials.jsonl (`collections.Counter(r['key'].split(':')[0])`). There are 15 lines and 15 distinct ids.

| key kind | count | written_by |
|---|---|---|
| `platform-run` | 6 | `code:tools.kgraph.ingest_platform@8ddd12c1d4` |
| `rule-version` | 5 | `code:tools.kgraph.rule_versions@3104192618` |
| `paper-run` | 3 | `code:tools.kgraph.ingest_agent_runs@d6331d0d41` |
| `measure` | 1 | `code:tools.kgraph.context@3104192618+uncommitted` |

The nodes, by trials.jsonl line, id and key:
1. `exp-1c51cc953e8b` `paper-run:orders-20261124T010517Z`
2. `exp-b13ec15d010b` `paper-run:closeout-20261124T011335Z`
3. `exp-8124c70783d8` `paper-run:feed-only-20261124T011440Z`
4. `exp-dec6b66218cb` `rule-version:afcf107c4c1024d9e4965bfb1ac788cd21f2881a`
5. `exp-08a4a2a139e6` `rule-version:4142f97e51cc86b12aa89876cf00f8347e1ca51e`
6. `exp-fdb915300b3a` `rule-version:7e506e59ef43b9940587b0e277b0892026ff7c30`
7. `exp-2e7fdf8d547f` `rule-version:0d6226e0a7dcc7314eacc8ca9a77a1b72b9bd973`
8. `exp-ed15eea4fc7a` `rule-version:13ddfa9666c2147f66718d5659f030ebc6120a83`
9. `exp-f76195cc9730` `measure:session-start-vs-handoff-pile:twenty-first-session`
10. `exp-877705156a72` `platform-run:036ed57524584afdaeb0bc60be6aaa71`
11. `exp-def66b8f3866` `platform-run:06ce6b90c0384057997e17a22d7a4624`
12. `exp-6b6413dffc70` `platform-run:064df1c2b58f46999f0276304c10d49e`
13. `exp-6b4be9413106` `platform-run:058313bbf2304bb0bb14aaed3315ab0e`
14. `exp-4b6ad8b89a35` `platform-run:ea4c1d2e7e0c43168c150c8b2aef3960`
15. `exp-2633f97cb6b9` `platform-run:0f33fec49f8c4905b6c212912077d439`

The verbs show the same set:
- `log` printed 15 headers (`grep -c '^exp-'`).
- `leaves` printed 10 headers (`grep -c '^exp-'`).
- `lineage exp-ed15eea4fc7a` gave the chain of five rule versions back to `exp-dec6b66218cb` (parent `-`).
- `children exp-1c51cc953e8b` gave `exp-b13ec15d010b` and `exp-8124c70783d8`.
- `fetch exp-ed15eea4fc7a` shows `links: ["exp-1c51cc953e8b","exp-8124c70783d8"]`.

Fields across all 15 nodes (Counter over trials.jsonl):
- `status`: `recorded` on all 15. No node is kept, reverted or crash, the three statuses plan line 66 names.
- `agent_run` and `loop` are null on all 15.
- `rev` is 1 on all 15.

All six platform runs name trade day 2023-10-02 and plan `ngx3-12be6ea6...`. Two of them, `exp-4b6ad8b89a35` and `exp-2633f97cb6b9`, use the `-giveback20` plan with exit `{"give_back_fraction": "0.2"}`.

## First user 1: the build plan workbook's Experiment Arms sheet
- **What the record holds for it:** no node. None of the 15 keys above has an arm-type prefix.
- **What the record does not hold, and what found nothing:**
  - The four kinds above are the only ones. There is no `arm`, `experiment-arm` or `workbook` kind.
  - `grep -o -i -w` over trials.jsonl found 0 matches each for `arm`, `arms`, `experiment arms`, `workbook`, `xlsx`, `build plan` and `Build_Plan`.
  - Grep of MANIFEST.json for `arms?|workbook|xlsx|...` found no hit.
  - `armed` matches 64 times, on lines 1 and 3 only. All 64 are rule counter names (`counts.engine.rules.CLnn.armed`, `CXnn.armed`).
  - A compound-token grep, `[A-Za-z0-9_.-]*(arm|teach|orchestr|surviv|workbook|series)[A-Za-z0-9_.-]*`, showed only `*.armed` counters in its top 20, each counted 2. I cut that output at 20 lines, so tokens below the top 20 were not displayed. The 64 `-w armed` matches equal 32 rules x 2, which fits all of them being counters, but the cut list does not show that directly.

## First user 2: the experiment orchestrator's series and survivors steps
- **What the record holds for it:** no node.
- **What the record does not hold, and what found nothing:**
  - No key kind for a step. `loop` is null on all 15 nodes.
  - `grep -o -i -w` found 0 matches each for `orchestrator`, `series`, `survivor`, `survivors`, `search`, `confirmation` and `classroom`.
  - MANIFEST.json gave no hit.
  - The compound-token grep showed no `orchestr`, `surviv` or `series` token in the displayed output.

## First user 3: the dipole teacher arms D0 to D5
- **What the record holds for it:** no node. `dipole` appears 4 times, on lines 1 and 3, always inside two counter names: `counts.engine.rules.CL07.missing.dipole line (60 s) before the trade` and the same for `CL08` (`grep -o -i -E '"[^"]*dipole[^"]*"' | sort | uniq -c`). Those are paper-run counters, not teacher arms.
- **What the record does not hold, and what found nothing:**
  - `grep -o -i -w` found 0 matches each for `teacher`, `D0`, `D1`, `D2`, `D3`, `D4`, `D5` and `D0-D5`.
  - I kept `-w` for D0-D5 because without it, hex commit ids and content_sha values would give false hits.
  - MANIFEST.json gave no hit.

## About `fetch`: it is not a lookup by key
Unpiped, with output to a scratch file:
- `fetch arm:D0` gave rc=0 and 0 bytes.
- `fetch paper-run:orders-20261124T010517Z`, a key that does exist, also gave rc=0 and 0 bytes.

So `fetch` matches by id only. On an unknown id it prints nothing and exits 0. That is why the absences above rest on the full list of 15 keys and the term search, not on `fetch`. My first round of fetch probes printed `rc=0` after a pipe into `head`, so that rc was `head`'s exit code, not the tool's. I do not use those probes as evidence.

## Where the scout's report and the record differ, line by line
- **Scout line 30, "MANIFEST.json ... 20 lines":** `wc -l` gives 19, and `cat -n` numbers lines 1-19. The keys at lines 2, 3, 4 and 5-18 match the scout.
- **Scout line 26 and line 67, "no node-kind enum" / "Table names and node kinds in exp_dag.py: none":** that is about the file. The record has four key kinds, written by four loaders in `tools.kgraph.*` (`written_by`), not by `exp_dag.py`. The scout did not name them.
- **Scout line 35:** the scout searched arm, workbook, orchestrator, D0-D5 and teacher, but not `dipole`. `dipole` has 4 hits (CL07/CL08 counter names, lines 1 and 3). The scout said line 3's text was omitted. I confirm line 3 holds `armed` counters as well.
- **Scout line 31 and lines 32 and 34:** these agree with the record. The trials.jsonl sha256 `7f2d17c7...b838b4` and the sqlite sha256 `b71df641...a52dd` match what I measured, and there are 15 lines.
- **Scout line 68, "frankie_exp_dag.sqlite not read":** I did not open it directly either. I have not read which file `log`, `leaves` and `fetch` read from (sqlite or jsonl). Their output agrees with trials.jsonl on all 15 ids.
- **Scout lines 17-24 (the verbs):** `--help` from /home/user/wt/r165 lists the same nine: push, fetch, children, lineage, log, leaves, rebuild, diff, set-status. The scout read /home/user/Markets/tools/exp_dag.py, not the r165 copy.
- **Plan against the record:** plan line 70 and MANIFEST line 4 name 7 verbs. The tool has 9, the extra two being `rebuild` and `set-status`.
- **Scout lines 11-13:** the plan's "first users" lines are 72-73, which agrees with my read of lines 63-73.

## The record is unchanged
- sha256 before and after, identical:
  - MANIFEST.json `c03ebe7d2111db489431d6791fda893b1c95885cc6b8198063307946b9f78348`
  - frankie_exp_dag.sqlite `b71df6419d51d85fc0833442e75a08b694c4b2ced935f03851d438d5887a52dd`
  - trials.jsonl `7f2d17c7587b4e2056c9f1eb400a4c1ee31670e5907cd40a680662b7d9b838b4`
- Sizes and mtimes are the same (792 / 102400 / 75679 bytes, Nov 24 17:08).
- All three files are tracked (`git -C /home/user/markets-data ls-files experiments`).
- `git -C /home/user/markets-data status --porcelain experiments` printed nothing (empty output, rc=0), both before and after.

## Data-integrity and rule notes from what I read
- `exp-f76195cc9730` (the measure node) has `written_by` ending `+uncommitted`. Its loader ran from a working tree with uncommitted changes, so the commit it names does not fully identify the code that wrote it.
- The 15 nodes carry no AWS dependency or execution assumption that I could see. The platform-run notes say "Not scored: the figures of this trial are counts of what was written" (Greg, 2026-11-24).

## Speculation (labelled; not measured)
- Speculation: the two `-giveback20` platform runs and the four base-plan runs are the closest thing in the record to arms, because they share one trade day and one plan and differ in an exit setting. They are not keyed or linked as arms, and the record does not call them arms.
- Speculation: the four loaders that wrote the record are all graph ingesters (`tools.kgraph.*`). If so, the record's users so far are the paper-trading platform and the rules history, not the three users plan lines 72-73 name.

## Open after this read
**For the builder**
- `exp_dag fetch` on an id that does not exist prints nothing and exits 0. A test or reader cannot tell "not there" from success.
- There is no lookup by key. `fetch <key>` returns nothing even for a key that exists.
- The `+uncommitted` `written_by` on `exp-f76195cc9730`.
- Plan line 70 and MANIFEST line 4 list 7 verbs; the tool has 9.

**For the main session**
- None of the three first users in plan lines 72-73 has a node. There is no arm, step or teacher-arm key kind, and no line carries `loop` or `agent_run`.
- No node has status kept, reverted or crash (plan line 66). All 15 are `recorded`.
- I did not run the grounding check (`python3 -m tools.kgraph.grounding text "..."`) on plan lines 72-73. The scout cites graph mentions at Entity.jsonl:350 and Claim.jsonl:435; I did not open them.

**What code cannot hold**
- The scout reports (scout line 47) that the workbook `Frankie_BOSS_Build_Plan_R4_20260921.xlsx` is not on disk in either checkout and has no text export. Backfilling its Experiment Arms sheet needs that file from Greg.
- The scout reports (scout line 38) that D0 to D5 are not defined anywhere it searched. Teacher-arm nodes need a definition of the six arms that exists only outside the code.
- The orchestrator's series and survivors steps are marked "NOT built" in the scout's reading of the skill (scout line 41). I did not read the skill myself.

Tool calls: 8 of 14 (6 Bash, 1 advisor, 1 SubagentHandback). No sub-agents, no writes to the record or the graph. Scratch files written, each holding one fetch probe's output (both were 0 bytes): /tmp/claude-0/-home-user/3e104f60-b369-56be-82d1-295b070262b0/scratchpad/f1.txt and /tmp/claude-0/-home-user/3e104f60-b369-56be-82d1-295b070262b0/scratchpad/f2.txt.
