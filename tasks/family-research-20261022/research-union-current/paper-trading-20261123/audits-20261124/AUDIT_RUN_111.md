# Performance auditor run 111 (Sonnet): the agent runs' token spend against the token plan, every line of the run record

Kept word for word as the auditor returned it, 2026-11-24 (twenty-fifth session). Nothing below this line is the main session's. This is the auditor's first run of the build (ticket 03b); it names every run from 1 to 109.

---

AUDIT OF MODEL-TOKEN SPEND AGAINST THE TOKEN PLAN (run 111, read-only; nothing written, nothing run through the engine or tape, no AWS, no sub-agent)

Sources read
- Plan: /home/user/Markets/research/kalshi/frankie_boss/CLAUDE_ARCH_PLAN_GRAPH_ENGINEERING_ADOPTION_20261123.md, "Token plan", items 1-4 (lines 38-52).
- Record: /home/user/markets-data/tasks/family-research-20261022/research-union-current/paper-trading-20261123/agent-runs.jsonl (115 lines, runs 1 to 109 all present, no gaps; 6 lines carry `corrects`: L50 for run 47, L51 for 48, L52 for 49, L86 for 83, L96 for 92, L111 for 104).
- Tickets: tickets-44-20261124/18.md, 19.md, 20.md (same directory). Also tickets-20261124/08-budget-and-record-for-every-agent-run.md.
- Loader: /home/user/Markets/tools/kgraph/ingest_agent_runs.py.
- Transcripts: /root/.claude/projects/-home-user/3356516d-d71a-5e13-907d-ff8d8ffcb6d4/subagents/ holds 6 transcripts (this session only): runs 107 (agent-a374a5827c8bc7cc6), 108 (agent-ae63f020e27f3aa06), 109 (agent-afe6c2a52ec45b6fb), 110 (agent-a961b9f58c36234ce), 111 (mine, agent-a7dbeba5559521347), 112 (agent-aea464eed0a1e704f). Transcripts of runs 1 to 106 and of the main session are NOT on this machine, so no figure on any line for runs 1-106 could be checked against its transcript. Lines for runs 47-67 carry figures that the line itself says were read from transcripts; I could not re-check them.

How I read the plan's item 3 (model, input tokens, output tokens, wall clock, outcome). Columns below: E = exact model id (a `claude-...` string); In / Out = separate input and output token figures; W = wall_clock_ms; Oc = outcome text; T = `tokens_reported` (the harness's single total, input and output together, per its own tokens_note: "the last step of its last model call"); A = `all_calls_tokens` (sum of every step of every call, from transcript; also not split into input/output). Y = line holds it, - = absent or null. T and A are not what item 3 asks for (it asks for input and output separately); I show them because they are the only token figures on most lines.

A. EVERY LINE OF agent-runs.jsonl (L = line, r = run; role abbreviated; model as recorded; roles/models with a long parenthesis cut at the parenthesis)
L1 r1 scout | haiku | E- In- Out- W Y Oc Y T Y A-
L2 r2 builder | sonnet | E- In- Out- W Y Oc Y T Y A-
L3 r3 reviewer | opus | E- In- Out- W Y Oc Y T Y A-
L4 r4 builder | sonnet | E- In- Out- W Y Oc Y T Y A-
L5 r5 reviewer | opus | E- In- Out- W Y Oc Y T Y A-
L6 r6 builder | sonnet | E- In- Out- W Y Oc Y T Y A-
L7 r7 reviewer | opus | E- In- Out- W Y Oc Y T Y A-
L8 r8 scout | haiku | E- In- Out- W Y Oc Y T Y A-
L9 r9 reviewer | opus | E- In- Out- W Y Oc Y T Y A-
L10 r10 builder | sonnet | E- In- Out- W Y Oc Y T Y A-
L11 r11 builder | sonnet | E- In- Out- W Y Oc Y T Y A-
L12 r12 builder | sonnet | E- In- Out- W Y Oc Y T Y A-
L13 r13 reviewer | opus | E- In- Out- W Y Oc Y T Y A-
L14 r14 scout | haiku | E- In- Out- W Y Oc Y T Y A-
L15 r15 builder | sonnet | E- In- Out- W- Oc Y T- A-
L16 r16 reviewer | opus | E- In- Out- W- Oc Y T- A-
L17 r17 scout | haiku | E- In- Out- W- Oc Y T- A-
L18 r18 main session | claude-fable-5-2 | E Y In- Out- W- Oc Y T- A-
L19 r20 builder | sonnet | E- In- Out- W Y Oc Y T Y A-
L20 r23 builder (as the reader) | sonnet | E- In- Out- W Y Oc Y T Y A-
L21 r21 builder (as the reader) | sonnet | E- In- Out- W Y Oc Y T Y A-
L22 r19 builder | sonnet | E- In- Out- W Y Oc Y T Y A-
L23 r24 builder (as the reader) | sonnet | E- In- Out- W Y Oc Y T Y A-
L24 r22 builder (as the reader) | sonnet | E- In- Out- W Y Oc Y T Y A-
L25 r25 builder (as the resolver) | sonnet | E- In- Out- W Y Oc Y T Y A-
L26 r26 builder | sonnet | E- In- Out- W- Oc Y T- A-
L27 r27 builder | sonnet | E- In- Out- W- Oc Y T- A-
L28 r28 reviewer | opus | E- In- Out- W- Oc Y T- A-
L29 r32 scout (general agent on Haiku) | haiku | E- In- Out- W Y Oc Y T Y A-
L30 r33 scout (general agent on Haiku) | haiku | E- In- Out- W Y Oc Y T Y A-
L31 r29 builder | sonnet | E- In- Out- W Y Oc Y T Y A-
L32 r30 builder | sonnet | E- In- Out- W Y Oc Y T Y A-
L33 r31 reviewer | opus | E- In- Out- W- Oc Y T- A-
L34 r34 reviewer | opus | E- In- Out- W- Oc Y T- A-
L35 r36 builder (as the evaluator) | sonnet | E- In- Out- W Y Oc Y T Y A-
L36 r35 reviewer | opus | E- In- Out- W- Oc Y T- A-
L37 r37 builder | sonnet | E- In- Out- W Y Oc Y T Y A-
L38 r38 builder | sonnet | E- In- Out- W Y Oc Y T Y A-
L39 r39 builder | sonnet | E- In- Out- W Y Oc Y T Y A-
L40 r40 builder | sonnet | E- In- Out- W Y Oc Y T Y A-
L41 r41 general agent (as a decider) | "the session's own model, not overridden" | E- In- Out- W- Oc Y T- A-
L42 r42 same as L41 | same | E- In- Out- W- Oc Y T- A-
L43 r43 same | same | E- In- Out- W- Oc Y T- A-
L44 r44 same | same | E- In- Out- W- Oc Y T- A-
L45 r45 general agent (read-only tracer) | "the session's own model, not overridden" | E- In- Out- W- Oc Y T- A-
L46 r46 same as L45 | same | E- In- Out- W- Oc Y T- A-
L47 r47 same as L45 | same | E- In- Out- W- Oc Y T- A- (outcome: "stopped by Greg's next message; returned nothing")
L48 r48 scout (read-only) | "the scout agent's own model as its definition sets it" | E- In- Out- W- Oc Y T- A-
L49 r49 scout (read-only) | same as L48 | E- In- Out- W- Oc Y T- A-
L50 r47 (corrects L47) general agent | claude-fable-5-2 | E Y In- Out- W- Oc Y T- A Y
L51 r48 (corrects L48) scout | claude-haiku-5-5 | E Y In- Out- W- Oc Y T- A Y
L52 r49 (corrects L49) scout | claude-haiku-5-5 | E Y In- Out- W- Oc Y T- A Y
L53 r50 general agent | claude-fable-5-2 | E Y In- Out- W Y Oc Y T Y A Y
L54 r51 general agent | claude-fable-5-2 | E Y In- Out- W Y Oc Y T Y A Y
L55 r52 claude-code-guide | claude-haiku-5-5 | E Y In- Out- W Y Oc Y T Y A Y
L56 r53 web-fetch | claude-haiku-5-5 | E Y In- Out- W Y Oc Y T Y A Y
L57 r54 reviewer | claude-opus-5-5 | E Y In- Out- W Y Oc Y T Y A Y
L58 r56 reviewer | claude-opus-5-5 | E Y In- Out- W Y Oc Y T Y A Y
L59 r58 reviewer | claude-opus-5-5 | E Y In- Out- W Y Oc Y T Y A Y
L60 r59 reviewer | claude-opus-5-5 | E Y In- Out- W Y Oc Y T Y A Y
L61 r55 reviewer | claude-opus-5-5 | E Y In- Out- W Y Oc Y T Y A Y
L62 r57 reviewer | claude-opus-5-5 | E Y In- Out- W Y Oc Y T Y A Y
L63 r60 reviewer | claude-opus-5-5 | E Y In- Out- W Y Oc Y T Y A Y
L64 r61 reviewer | claude-opus-5-5 | E Y In- Out- W Y Oc Y T Y A Y
L65 r62 reviewer | claude-opus-5-5 | E Y In- Out- W Y Oc Y T Y A Y
L66 r63 reviewer | claude-opus-5-5 | E Y In- Out- W Y Oc Y T Y A Y
L67 r64 general agent | claude-fable-5-2 | E Y In- Out- W Y Oc Y T Y A Y
L68 r65 builder (general agent briefed with builder.md) | claude-sonnet-5-5 | E Y In- Out- W- Oc Y T- A Y
L69 r66 builder | claude-sonnet-5-5 | E Y In- Out- W- Oc Y T- A Y
L70 r67 builder | claude-sonnet-5-5 | E Y In- Out- W Y Oc Y T Y A Y
L71 r68 builder (general agent briefed with builder.md) | sonnet | E- In- Out- W- Oc Y T- A-
L72 r70 reader (general agent, scout's extraction mode) | haiku | E- In- Out- W Y Oc Y T Y A-
L73 r71 reader | haiku | E- In- Out- W Y Oc Y T Y A-
L74 r72 reader | haiku | E- In- Out- W Y Oc Y T Y A-
L75 r74 reader | haiku | E- In- Out- W Y Oc Y T Y A-
L76 r75 reader | haiku | E- In- Out- W Y Oc Y T Y A-
L77 r76 reader | haiku | E- In- Out- W Y Oc Y T Y A-
L78 r73 reader | haiku | E- In- Out- W Y Oc Y T Y A-
L79 r69 builder | "sonnet (the builder agent's own model as its definition sets it)" | E- In- Out- W- Oc Y T- A-
L80 r77 builder | same wording as L79 | E- In- Out- W- Oc Y T- A-
L81 r78 builder | same wording | E- In- Out- W Y Oc Y T Y A-
L82 r79 reviewer | "opus (the reviewer agent's own model as its definition sets it)" | E- In- Out- W- Oc Y T- A-
L83 r83 general agent, fresh, given only the graph's text | sonnet | E- In- Out- W- Oc Y T- A-
L84 r81 builder | "sonnet (...own model as its definition sets it)" | E- In- Out- W Y Oc Y T Y A-
L85 r82 reviewer | "opus (...)" | E- In- Out- W Y Oc Y T Y A-
L86 r83 (corrects L83) general agent, fresh | sonnet | E- In- Out- W Y Oc Y T Y A-
L87 r84 builder | "sonnet (...)" | E- In- Out- W Y Oc Y T Y A-
L88 r85 builder | same | E- In- Out- W Y Oc Y T Y A-
L89 r86 reviewer | "opus (...)" | E- In- Out- W Y Oc Y T Y A-
L90 r87 builder, as the writer | "sonnet (...)" | E- In- Out- W Y Oc Y T Y A-
L91 r89 builder | same | E- In- Out- W Y Oc Y T Y A-
L92 r80 builder | same | E- In- Out- W Y Oc Y T Y A-
L93 r90 builder | same | E- In- Out- W Y Oc Y T Y A-
L94 r91 builder | same | E- In- Out- W Y Oc Y T Y A-
L95 r92 reader (general agent, extraction mode) | haiku | E- In- Out- W- Oc Y T- A-
L96 r92 (corrects L95) reader | haiku | E- In- Out- W Y Oc Y T Y A-
L97 r96 consolidator (general agent) | sonnet | E- In- Out- W Y Oc Y T Y A-
L98 r88 builder | "sonnet (...)" | E- In- Out- W- Oc Y T- A-
L99 r93 builder | same | E- In- Out- W- Oc Y T- A-
L100 r94 builder | same | E- In- Out- W Y Oc Y T Y A-
L101 r95 builder | same | E- In- Out- W- Oc Y T- A-
L102 r97 builder | same | E- In- Out- W Y Oc Y T Y A-
L103 r98 general agent, fresh, given only the graph's text | sonnet | E- In- Out- W Y Oc Y T Y A-
L104 r99 builder | "sonnet (...)" | E- In- Out- W Y Oc Y T Y A-
L105 r100 builder | same | E- In- Out- W- Oc Y T- A-
L106 r101 reviewer | "opus (...)" | E- In- Out- W- Oc Y T- A-
L107 r103 reviewer | "opus (...)" | E- In- Out- W Y Oc Y T Y A-
L108 r104 builder | "sonnet (...)" | E- In- Out- W Y Oc Y T Y A-
L109 r105 reviewer | "opus (...)" | E- In- Out- W Y Oc Y T Y A-
L110 r106 builder | "sonnet (...)" | E- In- Out- W Y Oc Y T Y A-
L111 r104 (corrects L108) builder | "sonnet (...)" | E- In- Out- W Y Oc Y T Y A-
L112 r102 builder | "sonnet (...)" | E- In- Out- W Y Oc Y T Y A-
L113 r107 reviewer | claude-opus-5-5 | E Y In Y Out Y W Y Oc Y T Y A-
L114 r108 scout | claude-haiku-5-5 | E Y In Y Out Y W Y Oc Y T Y A-
L115 r109 scout | claude-haiku-5-5 | E Y In Y Out Y W Y Oc Y T Y A-

Counts, over the 115 lines (null counted as absent; every field in the table was tested for non-null)
- Exact model id: held by 25 lines (L18, L50-L70, L113-L115); not held by 90 lines (the line gives "haiku", "sonnet", "opus", or a sentence such as "the session's own model, not overridden").
- Input tokens as its own figure: 3 lines (L113, L114, L115). Not held by 112.
- Output tokens as its own figure: the same 3 lines; not held by 112.
- Wall clock: held by 80 lines; not held by 35 (L15-18, L26-28, L33, L34, L36, L41-52, L68, L69, L71, L79, L80, L82, L83, L95, L98, L99, L101, L105, L106).
- Outcome: held by 115; not held by 0.
- Harness single total (`tokens_reported`, not split): 80 lines; none on 35 lines (the same 35 as wall clock).
- `all_calls_tokens` (transcript sum, not split; with `model_calls`, `last_call_tokens`, `advisor_tokens`): 21 lines (L50-L70), all of them run 47 to run 67.
- Lines holding none of the token figures (no `tokens_reported`, no `all_calls_tokens`, no input/output): 30 lines. Runs for which no line anywhere holds any token figure: 25 runs: 15, 16, 17, 18, 26, 27, 28, 31, 34, 35, 41, 42, 43, 44, 45, 46, 68, 69, 77, 79, 88, 93, 95, 100, 101. Runs 47, 48, 49 (first lines) and 83, 92 (first lines) hold none on their first line but their `corrects` line holds one, so they are not in the 25.
- Runs 15, 16, 17 and 41-46 are stopped or interrupted runs (L16 outcome "stopped by the interrupt; no report returned"; tokens_note "the harness reports no tokens for a stopped run"). I did not read the stopped-reason of each of the 25.
- Ticket 19 says "ten stopped runs have no figure; runs 99, 100 and 101 are not recorded yet." The file shows runs 99 and 100 and 101 recorded (L104, L105, L106), with 100 and 101 having no figure. So ticket 19's wording differs from the file; I do not know which was written later.
- The only lines that split input from output are runs 107, 108, 109, which are this session's three runs (plus the two later-line revisions at L50-L70 give one summed figure, not a split).

B. LIMITS TOLD BEFORE (`budget_tokens`, `budget_note`) AND WHAT THE RUN REACHED
Counts: `budget_tokens` non-null on 58 lines, `budget_note` on 95 lines; 49 lines carry the key `budget_tokens` with null (notes there quote Greg's "no limit for the build" / "No token limits on the build"). Figure reached = `tokens_reported` unless stated. Over = reached figure above the limit on the line.
Each line with a token limit (L = line, r = run: limit / reached / past?):
L8 r8: 150,000 / 122,420 / no
L9 r9: 200,000 / 101,431 / no
L10 r10: 300,000 / 156,983 / no
L11 r11: 150,000 / 89,470 / no
L12 r12: 150,000 / 108,305 / no
L13 r13: 100,000 / 62,449 / no
L14 r14: 80,000 / 125,570 / YES (line has no over_budget field; its note says the scout's session budget was 300,000, 174,430 left)
L15 r15: 130,000 / none recorded / unknown
L16 r16: 90,000 / none recorded (stopped) / unknown
L17 r17: 40,000 / none recorded (stopped) / unknown
L68 r65: 600,000 / `tokens_reported` none; all_calls_tokens 1,471,486 / unknown by the harness total; past by the transcript sum
L69 r66: 600,000 / none; all_calls_tokens 2,689,355 / unknown by the harness total; past by transcript sum
L70 r67: 600,000 / 160,941; all_calls_tokens 9,177,121 / no by harness total; past by transcript sum
L71 r68: 600,000 / none / unknown
L72 r70: 1,500,000 shared by seven reads / 139,521 / no (the line group: seven together 1,282,497 per L78's note)
L73 r71: 1,500,000 shared / 131,291 / no
L74 r72: 1,500,000 shared / 157,673 / no
L75 r74: 1,500,000 shared / 219,900 / no
L76 r75: 1,500,000 shared / 211,376 / no
L77 r76: 1,500,000 shared / 206,466 / no
L78 r73: 1,500,000 shared / 216,270 / no
L79 r69: 600,000 / none / unknown
L80 r77: 600,000 / none / unknown
L81 r78: 600,000 / 118,591 / no
L82 r79: 400,000 / none / unknown
L83 r83: 60,000 / none (first line) / unknown
L84 r81: 600,000 / 95,882 / no
L85 r82: 400,000 / 138,193 / no
L86 r83 (corrects L83): 60,000 / 109,515 / YES (note on the line: "the run passed it"; no over_budget field)
L87 r84: 600,000 / 91,401 / no
L88 r85: 600,000 / 72,760 / no
L89 r86: 400,000 / 107,355 / no
L90 r87: 600,000 / 110,334 / no
L91 r89: 600,000 / 88,218 / no
L92 r80: 600,000 / 172,629 / no
L93 r90: 600,000 / 85,396 / no
L94 r91: 600,000 / 49,190 / no
L95 r92: 1,500,000 shared / none / unknown
L96 r92: 1,500,000 shared / 199,776 / no
L97 r96: 300,000 / 235,977 / no
L98 r88: 600,000 / none / unknown
L99 r93: 600,000 / none / unknown
L100 r94: 600,000 / 99,336 / no
L101 r95: 600,000 / none / unknown
L102 r97: 600,000 / 99,233 / no
L103 r98: 110,000 / 115,078 / YES (no over_budget field; the note says only "told to Greg before it started")
L104 r99: 600,000 / 85,895 / no
L105 r100: 600,000 / none / unknown
L106 r101: 400,000 / none / unknown
L107 r103: 400,000 / 128,459 / no
L108 r104: 600,000 / 110,449 / no
L109 r105: 300,000 / 104,454 / no
L110 r106: 600,000 / 122,930 / no
L111 r104 (corrects L108): 600,000 / 162,364 / no
L112 r102: 600,000 / 296,108 / no
L113 r107: 300,000 / 149,733 / no
L114 r108: 150,000 / 174,551 / YES (line field over_budget: "tokens: 174,551 against 150,000")
L115 r109: 150,000 / 118,766 tokens, no; tool calls 41 against 40 / YES on tool calls (line field over_budget: "tool calls: 41 against 40")
Over-budget by the harness total: 4 lines carry a figure above the limit (L14, L86, L103, L114); only L114 and L115 carry an `over_budget` field; L86 says it in the note; L14 and L103 do not say it. On the lines 68-70 the transcript sum (21 lines carry it) is far above the limit while the harness total is below or absent; the two figures measure different things (harness total = last step of last call; transcript sum counts the whole conversation again at every call, cache reads included). Which of the two a "token limit" means is not written anywhere I read.
The 1,500,000 limit is shared by seven reads (L72-L78, run 73 notes "seven together 1,282,497 by the harness's totals"; my sum of the seven line figures is 139,521+131,291+157,673+219,900+211,376+206,466+216,270 = 1,282,497, which matches the note); the eighth read (run 92) used 199,776 more, giving 1,482,273 of 1,500,000 by the same totals (my arithmetic).
Other limits on lines, in prose: tool calls and wall clock appear in the notes of runs 104, 105, 106, 107, 108, 109 only (60/30 min; 40/20 min; 60/30; 60/30; 40/15; 40/15). Run 104 (L108/L111): 15 and 22 tool calls, 193,758 ms and 509,885 ms: within. Run 105: 17 vs 40, 133,585 ms vs 20 min: within. Run 106: 18 vs 60, 260,031 ms: within. Run 107: 14 vs 60, 227,619 ms: within. Run 108: 23 vs 40, 165,430 ms vs 15 min: within. Run 109: 41 vs 40: past by 1; 113,068 ms: within.

Runs 107, 108, 109: line figures against their transcripts (each reply counted once by message.id; many records share one message.id when a reply makes several parallel tool calls, so records are far more than replies)
- Run 107 (L113): line input_tokens_fresh 28, cache_written 143,580, cache_read 1,599,935, output 20,529, input_tokens 1,743,543. Transcript sums: 28, 143,580, 1,599,935, 20,529. No difference. 14 replies, model claude-opus-5-5 in all 14 (matches the line). Tool uses in transcript 15, one is the hand-back, so 14 besides it; the line says 14. Wall clock from first to last timestamp 12:45:16.631 to 12:49:04.099 = 227.5 s; line 227,619 ms. No difference.
- Run 108 (L114): line fresh 10, written 143,564, read 460,905, output 43,133, input 604,479. Transcript: same, no difference. 5 replies, model claude-haiku-5-5. Tool uses 24 including hand-back = 23; line 23. Wall 12:45:56.555 to 12:48:41.893 = 165.3 s; line 165,430 ms. No difference.
- Run 109 (L115): line fresh 20, written 102,151, read 655,995, output 27,293, input 758,166. Transcript: same, no difference. 10 replies, claude-haiku-5-5. Tool uses 42 including hand-back = 41; line 41. Wall 12:46:43.313 to 12:48:36.361 = 113.0 s; line 113,068 ms. No difference.
- Model: runs 108 and 109 lines say claude-haiku-5-5; the meta.json for run 108 says model "haiku" (the general-purpose type) and the replies say claude-haiku-5-5; consistent. The line for run 107 says claude-opus-5-5; replies say the same.
- Harness total (`tokens_reported`) against transcript figures: 107: 149,733 vs input+output with cache read 1,764,072 and without cache read 164,137; 108: 174,551 vs 647,612 and 186,707; 109: 118,766 vs 785,459 and 129,464. The harness total is not any of these sums (inference: it is the last model call's usage, as the line for runs 47-67 states for its own field; I did not compute last-call values for 107-109).

C. THE EIGHT LIMITS OF ITEM 2 (model calls, sub-agents, concurrent workers, tool calls, tokens, wall clock, retries, graph writes; in the run's plan JSON before it starts; on running out, return done/open/why)
- Lines recording a limit: tokens: 58 lines (`budget_tokens`). Tool calls and wall clock: in `budget_note` text only, runs 104, 105, 106, 107, 108, 109 (L108-L111, L113-L115... precisely L108, L109, L110, L111, L113, L114, L115 plus L112's line has none). Sub-agents: "no sub-agents" on runs 104, 107, 108, 109 (a prohibition in prose, not a number). Graph writes: "no write into the real graph" on runs 104 and 107, "nothing written" on 108 and 109 (a prohibition, not a number). Model calls: no line records a limit (21 lines record a count, `model_calls`, runs 47-67). Concurrent workers: none. Retries: none. No line records "what is done, what is open and why it stopped" as a rule; some outcomes say it after the fact.
- Plan JSON files: I searched /home/user/Markets and /home/user/markets-data (excluding .git) for file names matching *plan*.json, *budget*, *run-plan*, and for the eight key names (max_model_calls, max_sub_agents, max_concurrent, max_tool_calls, max_tokens, max_wall, max_retries, max_graph_writes) in *.json files. Found: no .json file holding any of the eight keys. Name matches found: /home/user/Markets/tasks/family-research-20261022/full-depth-rerun-plan.md (markdown), many /home/user/markets-data/graph/reads/run-00NN-*.json (names contain "plan"; not run plans, I did not open each), tickets-20261124/08-budget-and-record-for-every-agent-run.md.
- Code that does hold the eight keys: /home/user/Markets/tools/swarm/plan.py lines 24-25 define BUDGET_KEYS = max_model_calls, max_sub_agents, max_concurrent_workers, max_tool_calls, max_tokens, max_wall_clock_s, max_retries, max_graph_writes, and lines 104-111 refuse a plan over them. It is the model-API swarm's plan checker (also referenced in tools/swarm/run.py, model.py, tests/agent_program/test_stage6_swarm.py), not a file for these chat-launched agent runs. I did not open run.py to see how it is used. No instance plan file with these keys exists in the two trees.
- Ticket 18 states the same gap ("a token figure was told to Greg in chat; nothing held a run to it"); tickets 18 and 19 are Status ready, 20 is blocked.

D. WHERE THE SPEND GOES (transcript, runs 107, 108, 109; each reply counted once by message.id)
Run 107 (reviewer, claude-opus-5-5): fresh input 28; cache-written 143,580; cache-read 1,599,935; output 20,529; replies 14; tool uses 15 (14 + hand-back). Cache-read is 91.9% of all four figures summed (arithmetic: 1,599,935 / 1,764,072). Largest tool results: Bash, 25,273 characters (command begins "cd /home/user/Markets && wc -l tools/kgraph/defend.py tests/agent_program/tes..."); next Bash 21,351 characters ("cat -n tests/agent_program/test_defend.py"); next Bash 15,007 ("cat -n tools/kgraph/defend.py | sed -n 400,900p").
Run 108 (scout, claude-haiku-5-5): fresh 10; cache-written 143,564; cache-read 460,905; output 43,133; replies 5; tool uses 24 (23 + hand-back), so about 4.6 tool calls per reply (parallel calls). Largest results: Grep 8,409 characters (pattern of unicode escapes \x{2212}|\x{2264}|\x{00D7}|\x{2192}|\x{2014} under /home/user/Marke...); Read 7,961 (/home/user/Markets/tools/decider/programs/decider_v1.py); Read 4,775 (decider_v1.md). Its output is 43,133 tokens, the largest output of the three.
Run 109 (scout, claude-haiku-5-5): fresh 20; cache-written 102,151; cache-read 655,995; output 27,293; replies 10; tool uses 42 (41 + hand-back). Largest results: Grep 12,473 characters (pattern "afterwards|after_the_fact|after-the-fact" in /home/user/Markets); Read 9,821 (tools/decider/trial_with_decider.py); Read 8,614 (tools/kgraph/schema.py).
Sizes are characters of the tool_result text only (text blocks); I did not count image blocks (none seen) and did not convert to tokens. Result size alone does not give each run's cache-read, which grows with every later reply re-reading the whole context (cache-read per reply: 107 about 114,000, 108 about 92,000, 109 about 66,000, my arithmetic, 1,599,935/14 and so on).
For information, the other transcripts here (not in the three-run ask and not on any line of the file): run 110 (builder, claude-sonnet-5-5): fresh 14, written 95,628, read 318,815, output 8,767, 6 replies, largest result Read of /home/user/Markets-b456/tools/kgraph/defend.py 38,117 characters. Run 112 (scout, claude-haiku-5-5): fresh 10, written 90,641, read 265,978, output 6,655, 5 replies, largest Read of /home/user/paper-trading-platform/paper_platform/trial.py 22,010 characters. Runs 110 and 112 are not yet on lines in agent-runs.jsonl (it ends at run 109); run 111 is this run.

E. FINDINGS
1. The record holds the exact model id on 25 of 115 lines and separate input and output on 3 of 115 (runs 107-109). Measured: field counts above (python over agent-runs.jsonl). Sure. Open: whether lines for runs 1-106 can be filled; their transcripts are not on this machine.
2. 80 lines hold the harness's one total and wall clock; 35 lines hold neither; 25 runs have no token figure on any line (list in A). Sure on the counts; the reason per run (stopped, interrupt, not yet recorded) I read only for some.
3. The 21 transcript-derived lines (runs 47 to 67) carry `all_calls_tokens` that exceed `tokens_reported` by a large factor (for example run 64: 303,912 reported against 25,873,032 over 105 calls; run 67: 160,941 against 9,177,121 over 77 calls). The two measure different things (the harness figure is the last call's total). Sure on the figures as written on the lines; I did not re-derive them (transcripts absent). No line states which one a limit is compared against.
4. For runs 107, 108, 109 the line figures equal my sums from the transcripts exactly (fresh, cache-written, cache-read, output, input, tool calls, wall clock). Sure.
5. Token limits were exceeded on L14, L86, L103, L114 by the harness total, and run 109's tool calls exceeded its limit by 1 (41 vs 40). In none of these did anything stop the run (the lines for 108 and 109 say "nothing stopped it"). Only L114 and L115 have an `over_budget` field; L14 and L103 are not marked. Sure on figures.
6. For runs 107-109, cache-read input is the largest share of tokens (107: 91.9% of the four-figure sum; 108: 460,905 of 647,612 = 71.2%; 109: 655,995 of 785,459 = 83.5%; my arithmetic). Run 108's output (43,133) is 6.7% of its sum and higher than runs 109 (27,293) and 107 (20,529) in absolute tokens. Inference: reading cost scales with the number of replies times the size of context carried; run 107's 14 replies each re-read about 114,000 cached tokens. Not tested by any change.
7. The largest single tool results are 25,273 characters (run 107, a Bash that printed defend.py/test text), 8,409 (run 108, one Grep) and 12,473 (run 109, one Grep). Inference: file text printed whole into context is what a tighter brief or a line-ranged read would reduce; not tested.
8. No plan JSON exists for any run in either tree; the eight limits are held as chat statements and as note text on 7 lines (runs 104-109). The code to check a plan against the eight limits exists at /home/user/Markets/tools/swarm/plan.py for the swarm; I did not check whether anything feeds chat-launched runs into it.
9. Ticket 20 (the saving is not measured): I found no run line or file that holds a side-by-side figure of graph-built context against the session start or the 92,427-token Frankie packet; I did not search for one outside the paths named. Open: the measurement needs stage 5 to run, which ticket 20 marks blocked.
10. Loader: ingest_agent_runs.py lines 42-49 copy `model`, `tokens_reported`, `input_tokens`, `output_tokens`, `tool_calls`, `wall_clock_ms`, `budget_tokens` into AgentRun attributes and keep every other key (`setdefault`), so `budget_note`, `over_budget`, `model_calls`, `all_calls_tokens`, `input_tokens_cache_read` and the rest are carried into the graph as written. A `corrects` line from the same session is the run's next revision; a repeat without it raises an error (lines 51-62). The file's own docstring (lines 10-11) says `input_tokens` and `output_tokens` stay empty "because they were never given". Open: which of two lines for runs 47, 48, 49, 83, 92, 104 a consumer should take as current; the loader keeps one node id per run, so the later line's attributes win for the node (inference from `seen[nid]` and the node id `run:NNNN`; I did not run it).

What I did not do / limits reached: no transcripts for runs 1-106; did not read the stopped-reason of each of the 25 no-figure runs; did not open the swarm run.py; did not open the many graph/reads/run-*.json files. I stopped within the limits (no limit reached).

My own count of tool calls: 15 before this hand-back, 16 with it.
