# Performance auditor run 120 (Sonnet): runs 114, 115 and 117, each its own block

Kept word for word as the auditor returned it, 2026-11-24 (twenty-fifth session). Nothing below this line is the main session's.

---

Audit of runs 114, 115 and 117 (run 120). Each run is its own block. Nothing is averaged or totalled across them. Read-only; nothing was written.

Method, commands run on the files named in the task:
- Run lines: `jq -c 'select(.run==...)' agent-runs.jsonl`.
- Plan files: `cat run-plans/run-0114.json`, `run-0115.json`, `run-0117.json`.
- Plan in git: `git -C /home/user/markets-data log --format='%h %cI' -- <plan file>`.
- Transcripts, `jq -s`:
  - Replies = assistant lines grouped by `.message.id`, one line taken per id.
  - Usage = the four figures summed over those replies.
  - Tool calls = unique `tool_use` ids, excluding SubagentHandback.
  - Result sizes = `tool_result` content length in characters.
- Production: `git -C /home/user/Markets diff --stat 2ac873f 68d65a6` and `wc -c` on the two reports.
- A "limit passed" below means the figure went above the limit.
- The harness total is the figure on the run line (`tokens_reported`). The transcript figures are the four usage fields.
- For all three plan files, `git log` gives commit 16b14f6, 2026-11-24T13:08:54+00:00. The first transcript timestamps are 13:10:23.559Z (run 114), 13:10:23.578Z (run 115) and 13:10:23.610Z (run 117). In all three cases the plan file was in git about 1 minute 29 seconds before the run's first timestamp.

## Run 114 (builder, claude-sonnet-5-5, transcript agent-a7b300c42b5b933f8.jsonl)

1. Limits (run-plans/run-0114.json) against the figures reached:
   - max_model_calls 60: 22 replies. Not passed.
   - max_sub_agents 0: 0. No Agent tool call in the tool-name list (Bash 19, Edit 3, Read 4, plus the hand-back). Not passed.
   - max_concurrent_workers 1: not measured.
   - max_tool_calls 80: 26. Not passed.
   - max_tokens 600,000:
     - Harness total on the line: 119,607. Not passed.
     - Transcript, the four figures: fresh input 46; cache-written 110,043; cache-read 1,962,598; output 20,871. These add to 2,093,558.
     - The harness total is not the same measure. I tried fresh+output (20,917) and cache-written+output (130,914). Neither gives 119,607. I did not find what the harness counts.
   - max_wall_clock_s 2400: 499.709 s from first to last transcript line (13:10:23.559 to 13:18:43.268). The line says 499,733 ms. Not passed.
   - max_retries 1: not measured. 1 tool result carries is_error true. I did not read what it was or whether it was repeated.
   - max_graph_writes 0: not measured from the transcript. The plan's note says writes go to a scratch copy. I did not inspect where the Bash commands wrote the graph. The pytest commands set `MARKETS_DATA=/home/user/markets-data`.

2. The line against the transcript:
   - input_tokens 2,072,687 equals 46 + 110,043 + 1,962,598 exactly. cache_written, cache_read and output match the line exactly.
   - tool_calls 26 matches.
   - wall_clock_ms 499,733 against 499,709 from timestamps, a difference of 24 ms.
   - No other difference found.

3. Where the spend went:
   - 22 model replies.
   - Cache-read share of the four figures: 1,962,598 / 2,093,558 = 93.74%. That is about 89,200 cache-read tokens per reply.
   - 26 tool calls over 22 replies = 1.18 per reply.
   - 27 tool results, 113,102 characters in all.
   - Three largest results:
     - Read of /home/user/Markets-b456/tests/agent_program/test_defend.py, 28,265 characters.
     - Read of /home/user/Markets-b456/tools/kgraph/defend.py, 19,465 characters.
     - Read of .../reviews-20261124/REVIEW_RUN_107.md, 17,209 characters.

4. Produced: `git diff --stat 2ac873f 68d65a6` shows 3 files changed, 396 insertions, 73 deletions.
   - tests/agent_program/test_defend.py: 235 lines changed.
   - tools/kgraph/defend.py: 233 lines changed.
   - tools/kgraph/BUILD_NOTES_DEFEND.md: 1 line.
   - Per the line, 53 checks ran clean by the run's own report. That was not checked by me.

5. Against run 110 (same task, ended by Greg's stop; transcript agent-a961b9f58c36234ce, matched by cache-read 2,032,035):

   | | Run 114 | Run 110 |
   |---|---|---|
   | Replies | 22 | 21 |
   | Tool calls | 26 | 24 |
   | Tool calls per reply | 1.18 | 1.14 |
   | Cache-read tokens | 1,962,598 | 2,032,035 |
   | Cache-written | 110,043 | 118,945 |
   | Output | 20,871 | 28,296 |

   Run 110 has no harness total on its line.

6. Candidates for less spend (not demonstrated):
   - Batch independent commands into one reply. Mechanism: cache-read tokens grow roughly with replies times accumulated context. Measure: the cache-read tokens per reply, and which of the 22 replies carried one call that could have gone with another.
   - Hand the builder only the needed line ranges of the 28,265-character test file and the 17,209-character review. Mechanism: each large result stays in context for every later reply. Measure: the context length at each reply, with and without the full reads.
   - The test file was read in full once and the defend.py in two ranges. Whether either was re-read after an edit was not checked.

## Run 115 (reviewer, claude-opus-5-5, transcript agent-a90c4998f99c38289.jsonl)

1. Limits (run-plans/run-0115.json) against the figures reached:
   - max_model_calls 30: 19 replies. Not passed.
   - max_sub_agents 0: 0 (tool names are Bash 12, Read 14, plus the hand-back). Not passed.
   - max_concurrent_workers 1: not measured.
   - max_tool_calls 30: 26. Not passed.
   - max_tokens 250,000:
     - Harness total: 125,374. Not passed.
     - Transcript: fresh 42; cache-written 112,678; cache-read 1,504,731; output 27,296. These add to 1,644,747.
     - The harness total is not the same measure. fresh+output is 27,338 and cache-written+output is 139,974. Neither gives 125,374.
   - max_wall_clock_s 1200: 529.960 s (13:10:23.578 to 13:19:13.538). The line says 529,997 ms. Not passed.
   - max_retries 1: 0 tool results with is_error.
   - max_graph_writes 0: no Edit or Write tool call. The Bash commands, 110 characters of each seen, are grep, sed, wc and git log. Not measured beyond that.

2. The line against the transcript:
   - input_tokens 1,617,451 equals 42 + 112,678 + 1,504,731 exactly. Output and tool_calls (26) match.
   - wall_clock_ms 529,997 against 529,960, a difference of 37 ms.
   - No other difference found.

3. Where the spend went:
   - 19 replies.
   - Cache-read share of the four figures: 1,504,731 / 1,644,747 = 91.49%. That is about 79,200 per reply.
   - 26 tool calls over 19 replies = 1.37 per reply.
   - 27 tool results, 121,222 characters in all.
   - Three largest results:
     - Bash on root-redesign-20261116/ROOT_GAMEPLAN_DECISIONS.md (the grep and extract from "THE TWENTY-FIFTH SESSION STARTS"), 13,888 characters.
     - Read of tickets-44-20261124/PLAN_03b_04_05_06.md, 13,596 characters.
     - Bash `grep -n ... defend.py | head -120` in /home/user/Markets/tools/kgraph, 10,053 characters.

4. Produced: reviews-20261124/REVIEW_RUN_115_PLAN.md, 34,134 bytes (`wc -c`). Per the line, 22 points to change in the plan and 4 things the sources do not answer. The v2 plan was written by the main session, not by this run.

5. Against runs 113 and 107 (reviewer, same kind of read; transcripts a41c466a54fb81282 and a374a5827c8bc7cc6, matched by cache-read):

   | | Run 115 | Run 113 | Run 107 |
   |---|---|---|---|
   | Replies | 19 | 21 | 14 |
   | Tool calls | 26 | 21 | 14 |
   | Tool calls per reply | 1.37 | 1.00 | 1.00 |
   | Cache-read tokens | 1,504,731 | 1,633,669 | 1,599,935 |
   | Harness total | 125,374 | none (ended by stop) | 149,733 |

   Run 107 was a re-read of code, not a plan read. Its task differs from run 115's.

6. Candidates for less spend (not demonstrated):
   - Give the reviewer the part of ROOT_GAMEPLAN_DECISIONS.md it needs, not a 13,888-character grep and extract. Mechanism: the result stays in context. Measure: how much of that result the report cites.
   - Read independent files in one reply. Run 115 already batched slightly more than 113 and 107 (1.37 against 1.00). Measure: which of its 19 replies had only one call that could have been grouped.
   - The 34,134-byte report took 27,296 output tokens. A shorter hand-back format is a candidate, but it changes what the reader receives. That is Greg's choice.

## Run 117 (scout, claude-haiku-5-5, transcript agent-a182da9fd43370b82.jsonl)

1. Limits (run-plans/run-0117.json) against the figures reached:
   - max_model_calls 20: 10 replies. Not passed.
   - max_sub_agents 0: 0 (tool names are Glob 5, Grep 14, Read 11, plus the hand-back). Not passed.
   - max_concurrent_workers 1: not measured. The run issued several tool calls in one reply, which is not the same thing as concurrent workers.
   - max_tool_calls 30: 30 besides the hand-back. AT the limit, not passed. The line says it stopped at the limit and returned what was found and what was not.
   - max_tokens 150,000:
     - Harness total: 91,604. Not passed.
     - Transcript: fresh 20; cache-written 85,089; cache-read 501,509; output 18,234. These add to 604,852.
     - The harness total is not the same measure. fresh+output is 18,254 and cache-written+output is 103,323. Neither gives 91,604.
   - max_wall_clock_s 900: 80.761 s (13:10:23.610 to 13:11:44.371). The line says 80,794 ms. Not passed.
   - max_retries 1: 1 tool result with is_error true. It was not read, so whether it was retried is not known.
   - max_graph_writes 0: no Edit or Write tool call. Not passed.

2. The line against the transcript:
   - input_tokens 586,618 equals 20 + 85,089 + 501,509 exactly. Output matches.
   - tool_calls 30 matches.
   - wall_clock_ms 80,794 against 80,761, a difference of 33 ms.
   - No other difference found.

3. Where the spend went:
   - 10 replies.
   - Cache-read share of the four figures: 501,509 / 604,852 = 82.91%. That is about 50,150 per reply.
   - 30 tool calls over 10 replies = 3.00 per reply.
   - 31 tool results, 58,320 characters in all.
   - Three largest results:
     - Grep with pattern `"(id|source|repo|repository|path|commit|lines|doc|document|file|src|origin|from)"\s*:`, 11,056 characters.
     - Grep with pattern `VERSIONS\.md|CLAUDE\.md|strategy-20261123`, 8,010 characters.
     - Grep with pattern `decisions\.jsonl|^\s*def |"[a-z_]+"\s*:|\bjson\.dumps|write|open\(`, 5,309 characters.
   - Other searches in the run: Glob `**/*` and Glob `**/decisions.jsonl`.

4. Produced: scout-20261124/SCOUT_RUN_117_TICKETS_07_08_09.md, 14,611 bytes. Per the line:
   - 32 rule files found, pointing at three documents.
   - No code ties a rule version to a claim.
   - CLAUDE.md is not in the graph reader's document list.
   - No decisions.jsonl exists.
   - File sizes were not found; the main session filled them in with git.

5. Against runs 112 and 109 (scout; transcripts aea464eed0a1e704f and afe6c2a52ec45b6fb, matched by cache-read):

   | | Run 117 | Run 112 | Run 109 |
   |---|---|---|---|
   | Replies | 10 | 6 | 10 |
   | Tool calls | 30 | 20 | 41 |
   | Tool calls per reply | 3.00 | 3.33 | 4.10 |
   | Cache-read tokens | 501,509 | 356,619 | 655,995 |
   | Harness total | 91,604 | 111,756 | 118,766 |

   The three tasks differ (tickets 07 to 09 against tickets 04 to 06).

6. Candidates for less spend (not demonstrated):
   - Run Glob `**/*` and the broad-alternation Greps with `head_limit` or a narrower path. Mechanism: the three Greps returned 24,375 characters, 42% of the 58,320 characters of results. Measure: how much of each result the report uses.
   - Give the scout the file paths it will need (the rule files, ingest modules and kgraph module list). Mechanism: it ran 5 Globs to find them. Measure: how many of the 30 calls only located files.
   - The run stopped at its tool-call limit and left file sizes and the Codex document unfound. If the next plan gives the scout a size-capable tool (for example `wc -c`), that would remove a gap rather than save spend. This is a question for the plan, not a saving.

Tool calls made by this audit, besides the hand-back: 4 (Bash). The advisor tool was not called.
