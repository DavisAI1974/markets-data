# What every agent of the ticket build is held to (2026-11-24, twenty-sixth session)

A brief points here instead of repeating it. PAPER is this folder; SUB is the session's folder of live transcripts,
`/root/.claude/projects/-home-user/3e104f60-b369-56be-82d1-295b070262b0/subagents` (it is gone when the session ends:
the kept copies are in `PAPER/transcripts/`).

## Every agent
- Your limits are in your plan, `PAPER/run-plans/run-NNNN.json`, written before you started. Count your own tool calls,
  every one, by name, the hand-back apart, and report the true count. On reaching a limit: stop and return what is
  done, what is open and why.
- Bundle: several commands in one Bash call, several tool calls in one reply. You do not search for what your brief
  gives you by file and line.
- Report what you read and measured, each figure with the command it came from. No verdict words, no pass or fail.
  Speculation in its own section, labelled.
- Nothing is written into `/home/user/markets-data` or `/home/user/paper-trading-platform`, and nothing into the real
  graph, by anyone but the main session. `python3 -m tools.kgraph.extract coverage`, `ingest_*`, `defend register`
  and `defend challenge` write: on a scratch copy only.
- Checks: `MARKETS_DATA=/home/user/markets-data python3 -m pytest <files> -q -rs -p no:cacheprovider
  --basetemp=/home/user/tmp-pytest/<your run>`. The scratch folder stays OUTSIDE every git repository and is deleted
  after every run. Slow files (about five minutes): test_defend.py with test_outcome.py; test_ingest_artifacts.py
  (about four); select with `-k` while working. A check that needs an earlier machine's live transcripts is skipped
  here: name it, with its reason.
- No made-up data: a check reads real records at a named commit; a case the real record does not hold goes in the
  one separated section of its check file, as a real record with exactly the named thing changed and a `# change:`
  comment that names everything changed. Never loosen a check.

## A builder
- THE BRIEF IS THE GO. The failing check first, then only enough code; one point at a time.
- The checks run clean in a tool call BEFORE the call that commits. One commit for each point, subject beginning
  "PROPOSED, NOT YET READ BY THE REVIEWER: " and ending " [skip ci]", no emojis. Then
  `git push origin <your branch>:ccr-144315dd-pta2ze`; if refused: `git fetch origin ccr-144315dd-pta2ze &&
  git merge --no-edit FETCH_HEAD`, push again. Never force, never rebase. Push each point as it stands: a run can be
  stopped at any moment and what is not pushed is lost.
- If the same check fails a second time after one fix, stop and hand back the output, the diff and what you tried.
- Report: first line "# Builder run N (Sonnet): <tickets>, <what>"; point by point the check's name, the lines changed,
  the commit; the counts of each check file; what is open; what code cannot hold; your tool calls by name.

## A reviewer
- Read-only. Put one line back to see whether a check notices; `git checkout -- .` after each, and say so.
- Report: first line "# Reviewer run N (Opus): <tickets>, <which read>"; file:line, what the code does, what the ticket
  or the rule says, the concrete case; a last section "Open after this read": for the builder (each with file:line),
  for the main session, what code cannot hold. If nothing is left for the builder, say so in those words.

## The performance auditor
- Inspection commands only (`git status/log/show/diff`, `rg`, `ls`, `stat`, `head`, `tail`, `wc`, `cat`, `jq`, `awk`).
- THE FIRST LINE OF YOUR REPORT IS EXACTLY `# Performance auditor run N`; each audited run's block starts at column 0
  with `## Run NNN`; no other heading begins with "## Run". Nothing is averaged or totalled across runs. The whole
  report is inside your hand-back.
- A run's transcript: SUB/agent-<id>.jsonl (never print it). A model reply carries `message.id`, `message.model`,
  `message.usage` (input_tokens, cache_creation_input_tokens, cache_read_input_tokens, output_tokens); lines sharing
  a `message.id` count once for usage (`jq -s`, group by `.message.id`, last usage of each); `tool_use` items are
  counted over every assistant line by `name`; the hand-back is a tool call named `SubagentHandback` that the run's
  line does not count. Its line: the NEWEST line for the run in PAPER/agent-runs.jsonl. Its plan:
  PAPER/run-plans/run-NNNN.json; `git -C /home/user/markets-data log --diff-filter=A --format='%h %cI' -- <file>`
  against the transcript's first timestamp.
- Under each run's heading: (1) each of the eight limits against the figure reached (for a stopped run: at the stop):
  the harness total on the line where there is one, and the transcript's four token figures separately; tool calls;
  model replies; wall clock; sub-agents; and whether the plan was in git before the first timestamp. (2) the line
  against the transcript, any difference exactly; whether the transcript holds a hand-back; each count the run's own
  report states against the transcript's count by name. (3) where the spend went: replies; cache-read share and
  cache-read per reply; tool calls per reply and by kind; the largest tool result (tool, target, characters); for a
  stopped run, what its last reply was doing; for a builder, whether the checks ran in a call before the call that
  committed, and how many commits it made.
