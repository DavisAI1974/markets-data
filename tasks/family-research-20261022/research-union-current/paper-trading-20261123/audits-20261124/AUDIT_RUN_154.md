# Performance auditor run 154 (Sonnet): runs 128, 129, 130, 137 and 146 to 152, each its own block

Kept word for word as the agent returned it, 2026-11-24 (twenty-fifth session). Nothing below this line is the main session's.

---

# Performance auditor run 154

Eleven runs, each in its own block. Nothing is averaged or totalled across runs.

## Commands behind every figure

- **Transcript figures.** One `jq -s` per transcript file, `/root/.claude/projects/-home-user/3356516d-d71a-5e13-907d-ff8d8ffcb6d4/subagents/agent-<id>.jsonl`. It groups assistant lines by `message.id`, takes the last usage record of each id, and sums the four usage figures. Tool calls are `tool_use` items by `name`. The largest result is the longest `tool_result` text, matched back to its `tool_use` id.
- **Hand-back lines.** The `SubagentHandback` lines, and the timestamp of the line after each.
- **Time between lines.** A second `jq -s` printed every gap of 100 s or more between consecutive lines. For a run in several parts, a further `jq -s` printed the hand-back line, the line after it, and the line after that.
- **Line and plan figures.** `jq -c 'select(.run==N)' agent-runs.jsonl | tail -1` for the newest line. `jq` on `run-plans/run-0NNN.json` for the plan. `git -C /home/user/markets-data log --diff-filter=A --format='%h %cI' -- <plan>` for when the plan entered git.
- **Commits and reports.** `git -C /home/user/Markets show --stat --format=%s <sha> | grep -E "\||changed"`, and `wc -c` on the reports.
- **Counts that exclude the hand-back.** Every tool-call count below leaves out `SubagentHandback`.
- **Advisor calls.** None of the eleven transcripts has a `tool_use` named `advisor`. The advisor shows as a content item of type `server_tool_use`, name `advisor`. A `jq` select on `"name":"advisor"` found one in 137, one in 148, one in 149 and none in the other eight. No line counts the advisor in `tool_calls`.
- **Sub-agents.** No transcript has a Task or Agent tool call, so none was spawned.
- **Graph writes.** There is no line field and no transcript measure for the real-graph writes limit.
- **Working span.** For a run in several parts, the sum of (hand-back timestamp minus first line of that part). A later part starts at the line "The coordinator sent a message while you were working". The hand-back's own result line is stamped 0.1 to 0.2 s after the hand-back. The wait is the gap before the resume line.
- **Model and token figures.** In every run the line's model equals the transcript's model. Every line's four token figures, reply count, tool-call count and wall clock equal the transcript. Fresh plus cache-written plus cache-read equals the line's `input_tokens` in all eleven. Output equals the line in all eleven. Wall clock equals last minus first timestamp to the millisecond in all eleven.
- **Whole-transcript audit.** All eleven runs are audited whole here.

## Run 128

Builder, `claude-sonnet-5-5`, ticket 18, `agent-a5a037fef78998397`. An earlier block exists in an audit made after its FIRST part only. I found no `## Run 128` heading in `AUDIT_RUN_133.md` or `AUDIT_RUN_139.md`. I did not search further. This block audits the whole transcript, three parts.

**1. Limits** (plan `run-plans/run-0128.json`, added in b51ed27 at 13:42:20Z; first transcript line 13:45:44Z, so the plan was in git before the run began).

| Limit | Plan | Reached | Result |
|---|---|---|---|
| model calls | 40 | 32 | kept |
| sub-agents | 0 | 0 | kept |
| concurrent workers | 1 | not measurable beyond no Task call | no evidence against |
| tool calls | 50 | 29 (Bash 24, Read 5); 32 with the 3 hand-backs | kept |
| tokens | 350,000 (harness total) | 110,617 at the third hand-back (52,854 at the first, 81,129 at the second) | kept |
| wall clock | 1,800 s | whole span 2,314.475 s; working spans 116.376 + 259.580 + 569.026 = 944.982 s | whole span passed; working sum kept |
| retries | 1 | sent back twice (three parts) | 2 against 1; whether a send-back counts as a retry is not defined in the plan |
| graph writes | 0 | not measured | not shown |

- The waits between parts were 543.472 s (13:47:40.838 to 13:56:44.310) and 825.653 s (14:01:03.985 to 14:14:49.638), a total of 1,369.125 s.
- Transcript figures: fresh 66, cache-written 214,681, cache-read 2,286,961, output 54,194. The four-figure total is 2,555,902.

**2. Line against transcript.** No difference in any figure. The outcome says "three parts", and the transcript has 3 hand-backs. It names 4 commits, and the line's `commits` lists the same 4. The outcome states no tool-call count. The reviewer's run 149 text says "24 by its own count": the transcript has 24 Bash calls, 29 in all.

**3. Where the spend went.**
- Replies: 32.
- Cache-read share of the four figures: 0.8948.
- Cache-read per reply: 71,468.
- Tool calls per reply: 0.906.
- Largest tool result: 7,995 characters, Bash, a command reading `reviews-20261124/REVIEW_RUN_134_TICKET_18.md`.

**4. What it produced.**
- dfb5879: `run_plan.py` 288 lines and `test_run_plan.py` 143, 431 insertions.
- 313c7da: 289 insertions, 30 deletions.
- d7962d0: a test file, 9 insertions, 2 deletions.
- 643ca97: 162 insertions, 32 deletions.
- Report `BUILDER_RUN_128.md`: 20,840 bytes.
- Read calls with no offset or limit: 1 (a 41-line background-task output file), so 0 on a file longer than 300 lines.
- Grep or Glob calls: 0.

## Run 129

Builder, `claude-sonnet-5-5`, ticket 19, `agent-a1e36d84b29f4ab5b`. `AUDIT_RUN_133.md` holds a block made after its FIRST part only (7 replies, 6 tool calls, 256,628 cache-read). This block audits the whole transcript, four parts.

**1. Limits** (plan added b51ed27 13:42:20Z; first line 13:45:44Z; in git before the run).

| Limit | Plan | Reached | Result |
|---|---|---|---|
| model calls | 40 | 33 | kept |
| sub-agents | 0 | 0 | kept |
| concurrent workers | 1 | no Task call | no evidence against |
| tool calls | 50 | 29 (all Bash); 33 with the hand-backs | kept |
| tokens | 350,000 (harness total) | 151,565 | kept |
| wall clock | 1,800 s | whole span 2,229.429 s; working spans 101.278 + 191.446 + 175.870 + 158.279 = 626.873 s | whole span passed; working sum kept |
| retries | 1 | sent back three times (four parts) | 3 against 1; the plan does not say whether a send-back counts |
| graph writes | 0 | not measured | not shown |

- The waits between parts were 558.634 s, 414.608 s and 628.852 s, from the hand-back's following line to the resume line. A hand-back at 13:47:25.737 resumed at 13:56:44.371, and so on; the three gaps measured 559, 415 and 629 s.
- Transcript figures: fresh 70, cache-written 381,055, cache-read 2,735,541, output 85,023. The four-figure total is 3,201,689.

**2. Line against transcript.** No difference. The outcome says "four parts", and the transcript has 4 hand-backs. It names 4 commits, and git shows the same 4.

**3. Where the spend went.**
- Replies: 33.
- Cache-read share: 0.8544.
- Cache-read per reply: 82,895.
- Tool calls per reply: 0.879.
- Largest tool result: 10,798 characters, Bash, `git fetch` and merge in `Markets-b19`, then `sed -n 84,125p tools/kgraph/r…`.

**4. What it produced.**
- 5c5ceb8: 3 files, 444 insertions, 2 deletions.
- 35bad34: 386 + 57 lines in 2 files.
- 29a5123: 253 insertions, 55 deletions.
- bdf4c01: 203 insertions, 29 deletions.
- Report `BUILDER_RUN_129.md`: 24,619 bytes.
- Read calls: 0 in all. Grep or Glob calls: 0.

## Run 130

Builder, `claude-sonnet-5-5`, ticket 25, `agent-aee0e00f5187acfa1`. `AUDIT_RUN_139.md` holds a block made after its FIRST part only; `AUDIT_RUN_153.md` quotes 18 replies and 21 tool calls from that earlier line. This block audits the whole transcript, two parts.

**1. Limits** (plan `run-0130.json`, added b51ed27 13:42:20Z; first line 13:45:44Z; in git before the run).

| Limit | Plan | Reached | Result |
|---|---|---|---|
| model calls | 50 | 32 | kept |
| sub-agents | 0 | 0 | kept |
| concurrent workers | 1 | no Task call | no evidence against |
| tool calls | 60 | 35 (Bash 27, Write 4, Edit 3, Monitor 1); 37 with the hand-backs | kept |
| tokens | 450,000 (harness total) | 183,526 | kept |
| wall clock | 2,400 s | whole span 4,180.951 s; working spans 650.585 + 2,292.619 = 2,943.204 s | passed on both measures; the working sum is 543 s over |
| retries | 1 | sent back once | 1 against 1; a send-back is not defined as a retry in the plan |
| graph writes | 0 | not measured; the outcome states nothing was written to the real graph | not shown |

- The single wait was 1,237.372 s (13:56:35.192 to 14:17:12.564).
- Inside the second part, tool results came after gaps of 576 s three times (line 104, line 109 and a 578 s gap before an attachment at line 106). The preceding Bash call in each case was `for i in $(seq 1 115); do grep -q DONE /tmp/run130/mut.out && break; s…`. A further gap of 361 s followed the same loop command. The first-part gap of 120 s followed a command in `Markets-b25`.
- Transcript figures: fresh 68, cache-written 760,667, cache-read 2,774,475, output 73,962. The four-figure total is 3,609,172.

**2. Line against transcript.** No difference. The outcome says "two parts", and the transcript has 2 hand-backs. It names 2 commits, and git shows the same 2.

**3. Where the spend went.**
- Replies: 32.
- Cache-read share: 0.7687.
- Cache-read per reply: 86,702.
- Tool calls per reply: 1.094.
- Largest tool result: 10,840 characters, Bash, a python heredoc in `Markets-b25` that imports shutil and tempfile.

**4. What it produced.**
- b245ee3: 435 insertions in 3 files.
- 6de2e47: 486 insertions, 186 deletions in 2 files.
- Report `BUILDER_RUN_130.md`: 17,676 bytes.
- Read calls: 0 in all. Grep or Glob calls: 0.

## Run 137

Builder, `claude-sonnet-5-5`, ticket 04, `agent-ab6b1507f1c36837e`. One part.

**1. Limits** (plan `run-0137.json`, added a7f647e 13:51:22Z; first line 13:53:13Z; in git before the run).

| Limit | Plan | Reached | Result |
|---|---|---|---|
| model calls | 60 | 37 | kept |
| sub-agents | 0 | 0 | kept |
| concurrent workers | 1 | no Task call | no evidence against |
| tool calls | 60 | 38 (all Bash); 40 with one advisor call and the hand-back | kept |
| tokens | 450,000 (harness total) | no harness total: the line's `tokens_reported` is null | cannot be shown kept on the measure the plan names; the transcript's fresh input plus output is 45,036 |
| wall clock | 2,400 s | whole span 1,625.238 s; to the hand-back 1,625.186 s | kept |
| retries | 1 | 0 | kept |
| graph writes | 0 | not measured | not shown |

- The advisor call was at 13:54:20 (line 30).
- Transcript figures: fresh 76, cache-written 106,399, cache-read 3,350,491, output 44,960. The four-figure total is 3,501,926.

**2. Line against transcript.** No difference. The outcome says "it may have run slightly past its 40 minutes". The transcript's span is 1,625 s, which is 27.1 minutes, and the plan limit is 2,400 s (40 minutes). The outcome names 3 commits, and git shows the same 3.

**3. Where the spend went.**
- Replies: 37.
- Cache-read share: 0.9568.
- Cache-read per reply: 90,554.
- Tool calls per reply: 1.027.
- Largest tool result: 23,855 characters, Bash, `sed -n 440,835p tools/kgraph/defend.py` in `Markets-b456`.
- Gaps of 100 s or more occurred at lines 30, 86, 92, 104, 107, 109, 111 and 114, each after a command.

**4. What it produced.**
- eb66c37: `outcome.py` 220 lines and its test 153, 373 insertions.
- 82e32cd: 81 insertions, 8 deletions.
- 821c2a0: 5 files, 141 insertions, 9 deletions.
- Report `BUILDER_RUN_137.md`: 7,756 bytes.
- Read calls: 0 in all. Grep or Glob calls: 0.

## Run 147

Builder, `claude-sonnet-5-5`, tickets 02, 03 and 01, `agent-aee83b12ed3f09c8c`. Two parts. The first wrote nothing and asked for a go.

**1. Limits** (plan `run-0147.json`, added 603268b 14:21:00Z; first line 14:22:11Z; in git before the run).

| Limit | Plan | Reached | Result |
|---|---|---|---|
| model calls | 50 | 14 | kept |
| sub-agents | 0 | 0 | kept |
| concurrent workers | 1 | no Task call | no evidence against |
| tool calls | 50 | 13 (all Bash); 15 with the 2 hand-backs | kept |
| tokens | 400,000 (harness total) | 120,113 | kept |
| wall clock | 2,100 s | whole span 960.509 s; working spans 66.413 + 681.210 = 747.623 s | kept |
| retries | 1 | sent back once | 1 against 1; a send-back is not defined as a retry |
| graph writes | 0 | not measured | not shown |

- The wait was 212.583 s (14:23:18.311 to 14:26:50.894).
- Transcript figures: fresh 28, cache-written 219,658, cache-read 1,104,768, output 24,369. The four-figure total is 1,348,823.

**2. Line against transcript.** No difference in figures. The outcome says "14 tool calls of 50 by its count". The transcript has 13 tool calls besides hand-backs, and 15 with the 2 hand-backs. The number 14 equals 13 plus one hand-back. The line holds 13.

**3. Where the spend went.**
- Replies: 14.
- Cache-read share: 0.8191.
- Cache-read per reply: 78,912.
- Tool calls per reply: 0.929.
- Largest tool result: 13,405 characters, Bash, `sed -n '215,285p' tools/kgraph/defend.py && sed -n '395,545p' tools/kgraph/defend.py`.

**4. What it produced.**
- 7e27239: 189 insertions, 29 deletions in 2 files.
- de1b3e0: `BUILD_NOTES_DEFEND.md`, 1 insertion.
- Report `BUILDER_RUN_147.md`: 14,896 bytes.
- Read calls: 0 in all. Grep or Glob calls: 0.

## Run 146

Reviewer, `claude-opus-5-5`, ticket 04, `agent-a30559c4f941d94f4`. One part.

**1. Limits** (plan `run-0146.json`, added 603268b 14:21:00Z; first line 14:22:11Z; in git before the run).

| Limit | Plan | Reached | Result |
|---|---|---|---|
| model calls | 28 | 13 | kept |
| sub-agents | 0 | 0 | kept |
| concurrent workers | 1 | no Task call | no evidence against |
| tool calls | 22 | 12 (Bash 11, Read 1); 13 with the hand-back | kept |
| tokens | 250,000 (harness total) | 92,014 | kept |
| wall clock | 1,500 s | whole span 1,161.292 s; to the hand-back 1,161.185 s | kept |
| retries | 1 | 0 | kept |
| graph writes | 0 | not measured | not shown |

- The transcript has gaps of 600 s (line 26), 350 s (line 36) and 171 s (line 39).
- The first two were after Bash commands, in `/tmp/run146` and `Markets-r146` with `MARKETS_DATA` set.
- Transcript figures: fresh 26, cache-written 207,530, cache-read 627,391, output 20,409. The four-figure total is 855,356.

**2. Line against transcript.** No difference. The outcome says "12 tool calls and the hand-back against 22", which is 12 plus the hand-back and matches. It says "1,161 seconds". Its own report said it went past 25 minutes, and the transcript does not show that (1,161 s is 19.4 minutes).

**3. Where the spend went.**
- Replies: 13.
- Cache-read share: 0.7335.
- Cache-read per reply: 48,261.
- Tool calls per reply: 0.923.
- Largest tool result: 29,798 characters, Read, a saved tool-result file `tool-results/b1c1xcxey.txt` with `offset` 28.

**4. What it produced.**
- No commit. The line names `read_commit` Markets:931b2b3.
- Report `REVIEW_RUN_146_TICKET_04.md`: 15,383 bytes.
- Read calls with no offset or limit: 0. Grep or Glob calls: 0.

## Run 148

Reviewer, `claude-opus-5-5`, ticket 19, `agent-a487de1f39a5561f6`. One part.

**1. Limits** (plan `run-0148.json`, added 0e58f82 14:23:30Z; first line 14:26:50Z; in git before the run).

| Limit | Plan | Reached | Result |
|---|---|---|---|
| model calls | 18 | 11 | kept |
| sub-agents | 0 | 0 | kept |
| concurrent workers | 1 | no Task call | no evidence against |
| tool calls | 12 | 10 (Bash 9, Read 1) on the line; with one advisor call and the hand-back, 12 | kept on the line's count; exactly at the limit if the advisor and the hand-back are counted |
| tokens | 140,000 (harness total) | 84,923 | kept |
| wall clock | 1,200 s | whole span 367.421 s; to the hand-back 367.255 s | kept |
| retries | 1 | 0 | kept |
| graph writes | 0 | not measured | not shown |

- The advisor call was at 14:30:01 (line 42).
- Transcript figures: fresh 24, cache-written 70,938, cache-read 629,529, output 24,344. The four-figure total is 724,835.

**2. Line against transcript.** No difference. The outcome says "12 tool calls of 12 counting its hand-back, one of them the advisor". That equals 10 plus advisor plus hand-back, and matches.

**3. Where the spend went.**
- Replies: 11.
- Cache-read share: 0.8685.
- Cache-read per reply: 57,230.
- Tool calls per reply: 0.909.
- Largest tool result: 31,869 characters, Read, the saved file `tool-results/ba36way7l.txt` with no offset or limit. That file has 434 lines.

**4. What it produced.**
- No commit. The line names `read_commit` Markets:bdf4c01.
- Report `REVIEW_RUN_148_TICKET_19_FOURTH.md`: 16,931 bytes.
- Read calls with no offset or limit on a file longer than 300 lines: 1 (the 434-line file). Grep or Glob calls: 0.

## Run 149

Reviewer, `claude-opus-5-5`, ticket 18, `agent-a9f6541796ac17edb`. One part.

**1. Limits** (plan `run-0149.json`, added 737a14c 14:27:15Z; first line 14:27:37Z; in git before the run).

| Limit | Plan | Reached | Result |
|---|---|---|---|
| model calls | 18 | 8 | kept |
| sub-agents | 0 | 0 | kept |
| concurrent workers | 1 | no Task call | no evidence against |
| tool calls | 12 | 7 (all Bash); 9 with one advisor call and the hand-back | kept |
| tokens | 140,000 (harness total) | 91,824 | kept |
| wall clock | 1,200 s | whole span 942.910 s; to the hand-back 942.783 s | kept |
| retries | 1 | 0 | kept |
| graph writes | 0 | not measured | not shown |

- The advisor call was at 14:40:26 (line 34).
- There was a 566 s gap before a result at line 28 (after `cat > /tmp/run149/mut.py <<'EOF'`).
- Transcript figures: fresh 18, cache-written 142,853, cache-read 438,265, output 27,817. The four-figure total is 608,953.

**2. Line against transcript.** No difference. The outcome says "8 tool calls and the hand-back of 12, one of them the advisor". That is 7 plus the advisor equals 8, plus the hand-back. The line holds 7. It says "942.9 seconds", which matches.

**3. Where the spend went.**
- Replies: 8.
- Cache-read share: 0.7197.
- Cache-read per reply: 54,783.
- Tool calls per reply: 0.875.
- Largest tool result: 25,823 characters, Bash, `git log --oneline -1 && git diff d7962d0 643ca97 -- tools/kgraph/run_plan.py tests/agent_program/test_run_plan.py; P=…`.

**4. What it produced.**
- No commit. The line names `read_commit` Markets:643ca97.
- Report `REVIEW_RUN_149_TICKET_18_THIRD.md`: 17,726 bytes.
- Read calls: 0. Grep or Glob calls: 0.

## Run 150

Scout, `claude-haiku-5-5`, ticket 21, `agent-adb363a9d3c341a49`. One part.

**1. Limits** (plan `run-0150.json`, added bb236e6 14:28:21Z; first line 14:29:07Z; in git before the run).

| Limit | Plan | Reached | Result |
|---|---|---|---|
| model calls | 30 | 6 | kept |
| sub-agents | 0 | 0 | kept |
| concurrent workers | 1 | no Task call | no evidence against |
| tool calls | 28 | 26 (Grep 17, Glob 6, Read 3); 27 with the hand-back | kept |
| tokens | 120,000 (harness total) | 66,461 | kept |
| wall clock | 600 s | whole span 83.515 s; to the hand-back 83.331 s | kept |
| retries | 1 | 0 | kept |
| graph writes | 0 | not measured | not shown |

- No advisor call.
- Transcript figures: fresh 12, cache-written 56,506, cache-read 212,124, output 19,264. The four-figure total is 287,906.

**2. Line against transcript.** No difference. The outcome says "26 tool calls of 28", and the transcript has 26.

**3. Where the spend went.**
- Replies: 6.
- Cache-read share: 0.7368.
- Cache-read per reply: 35,354.
- Tool calls per reply: 4.333.
- Largest tool result: 9,304 characters, Grep, pattern `^\s*def test_|^class Test` over `tests/agent_program`.

**4. What it produced.**
- No commit; report `SCOUT_RUN_150_TICKET_21.md`: 13,054 bytes.
- Tool calls by kind: Read 3, Grep 17, Glob 6.
- The 3 Reads had `offset`/`limit` unset on two files: `experiments/MANIFEST.json` (19 lines) and `experiment-orchestrator/SKILL.md` (106 lines). Neither is over 300 lines.

## Run 151

Scout, `claude-haiku-5-5`, ticket 31, `agent-a25d63e73afd44a16`. One part.

**1. Limits** (plan `run-0151.json`, added bb236e6 14:28:21Z; first line 14:29:07Z; in git before the run).

| Limit | Plan | Reached | Result |
|---|---|---|---|
| model calls | 30 | 7 | kept |
| sub-agents | 0 | 0 | kept |
| concurrent workers | 1 | no Task call | no evidence against |
| tool calls | 28 | 26 (Grep 18, Read 5, Glob 3); 27 with the hand-back | kept |
| tokens | 120,000 (harness total) | 67,185 | kept |
| wall clock | 600 s | whole span 89.623 s; to the hand-back 89.510 s | kept |
| retries | 1 | 0 | kept |
| graph writes | 0 | not measured | not shown |

- No advisor call.
- Transcript figures: fresh 14, cache-written 56,347, cache-read 251,380, output 21,245. The four-figure total is 328,986.

**2. Line against transcript.** No difference. The outcome says "26 tool calls of 28", and the transcript has 26.

**3. Where the spend went.**
- Replies: 7.
- Cache-read share: 0.7641.
- Cache-read per reply: 35,911.
- Tool calls per reply: 3.714.
- Largest tool result: 6,598 characters, Read, `MARKET_DATA_INDEX.md` with offset 0, limit 50, `allow_large` true.

**4. What it produced.**
- No commit; report `SCOUT_RUN_151_TICKET_31.md`: 12,000 bytes.
- Tool calls by kind: Read 5, Grep 18, Glob 3.

## Run 152

Scout, `claude-haiku-5-5`, ticket 37, `agent-aee46bc9389bd728c`. One part.

**1. Limits** (plan `run-0152.json`, added bb236e6 14:28:21Z; first line 14:29:07Z; in git before the run).

| Limit | Plan | Reached | Result |
|---|---|---|---|
| model calls | 30 | 5 | kept |
| sub-agents | 0 | 0 | kept |
| concurrent workers | 1 | no Task call | no evidence against |
| tool calls | 28 | 24 (Grep 16, Read 5, Glob 3); 25 with the hand-back | kept |
| tokens | 120,000 (harness total) | 68,874 | kept |
| wall clock | 600 s | whole span 64.873 s; to the hand-back 64.775 s | kept |
| retries | 1 | 0 | kept |
| graph writes | 0 | not measured | not shown |

- No advisor call.
- Transcript figures: fresh 10, cache-written 61,969, cache-read 184,556, output 15,351. The four-figure total is 261,886.

**2. Line against transcript.** No difference. The outcome says "24 tool calls of 28", and the transcript has 24.

**3. Where the spend went.**
- Replies: 5.
- Cache-read share: 0.7047.
- Cache-read per reply: 36,911.
- Tool calls per reply: 4.800.
- Largest tool result: 9,336 characters, Grep, pattern `rule version|rule edit|version a node|RuleVersion|rule_version`.

**4. What it produced.**
- No commit; report `SCOUT_RUN_152_TICKET_37.md`: 14,300 bytes.
- Tool calls by kind: Read 5, Grep 16, Glob 3.

## Set beside the earlier runs

Earlier figures are taken from `AUDIT_RUN_153.md` and `AUDIT_RUN_133.md`, last sections. I did not re-measure them. Cache-read per reply is a division of the figures shown. In the builder table, 130 and 129 are the whole-transcript figures from this report, not the first-part figures in the earlier audits.

**Builders**

| | 128 | 129 | 130 | 137 | 147 | 131 | 122 | 121 |
|---|---|---|---|---|---|---|---|---|
| Replies | 32 | 33 | 32 | 37 | 14 | 31 | 16 | 16 |
| Tool calls | 29 | 29 | 35 | 38 | 13 | 29 | 17 | 14 |
| Tool calls per reply | 0.906 | 0.879 | 1.094 | 1.027 | 0.929 | 0.935 | 1.06 | 0.875 |
| Cache-read tokens | 2,286,961 | 2,735,541 | 2,774,475 | 3,350,491 | 1,104,768 | 2,765,266 | 1,750,851 | 840,239 |
| Cache-read per reply | 71,468 | 82,895 | 86,702 | 90,554 | 78,912 | 89,202 | 109,428 | 52,515 |

**Reviewers**

| | 146 | 148 | 149 | 140 | 141 | 142 | 143 | 144 | 145 |
|---|---|---|---|---|---|---|---|---|---|
| Replies | 13 | 11 | 8 | 11 | 10 | 11 | 9 | 13 | 8 |
| Tool calls | 12 | 10 | 7 | 10 | 9 | 10 | 8 | 12 | 7 |
| Tool calls per reply | 0.923 | 0.909 | 0.875 | 0.909 | 0.900 | 0.909 | 0.889 | 0.923 | 0.875 |
| Cache-read tokens | 627,391 | 629,529 | 438,265 | 669,934 | 671,664 | 646,645 | 482,587 | 789,099 | 303,265 |
| Cache-read per reply | 48,261 | 57,230 | 54,783 | 60,903 | 67,166 | 58,786 | 53,621 | 60,700 | 37,908 |

**Scouts**

| | 150 | 151 | 152 | 125 | 126 | 127 |
|---|---|---|---|---|---|---|
| Replies | 6 | 7 | 5 | 6 | 3 | 2 |
| Tool calls | 26 | 26 | 24 | 17 | 20 | 20 |
| Tool calls per reply | 4.333 | 3.714 | 4.800 | 2.83 | 6.67 | 10.00 |
| Cache-read tokens | 212,124 | 251,380 | 184,556 | 323,831 | 103,478 | 27,571 |
| Cache-read per reply | 35,354 | 35,911 | 36,911 | 53,972 | 34,493 | 13,786 |

**What the figures can show**
- Counts and divisions of those counts.
- The seven whole-file Reads and Grep or Glob counts are in each run's block.
  - Among the reviewers, 148 has 1 whole-file Read over 300 lines, and 146 and 149 have 0. Earlier, 140, 141 and 144 had 1 each, and 136, 138, 142, 143 and 145 had 0.
  - Grep or Glob calls were 0 in all seven briefed runs here. They were 0 in the nine earlier reviewer runs.
  - I did not count `grep` or `rg` run inside Bash.
- Builders 128, 129 and 130 each have a first-part-only block in an earlier audit (129 and 130 as quoted in 153; 128 has none). The whole-transcript replies and cache-read are well above those first-part figures. The earlier tables are not comparable with these figures.

**What they cannot show**
- The tasks differ: each builder changed different files and brought different checks, and each reviewer read a different change.
- Each cell is one run with no repeat.
- Cache-read depends on how far the context grew, which depends on the task and the number of replies. Fewer replies means fewer cache reads by arithmetic.
- The briefing method is not isolated from the task.
- Harness totals and transcript sums are different measures. Run 137 has no harness total, so its token limit cannot be compared on the plan's measure.
- Nothing here measures the quality of any run's output. No percentage is given and no run is ranked.

Tool calls I made besides the hand-back: 9, all Bash.
