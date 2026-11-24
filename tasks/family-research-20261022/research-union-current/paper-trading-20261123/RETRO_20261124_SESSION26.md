# Retro of the twenty-sixth session: read after read after read (2026-11-24)

Greg: "That's our token probelem. We keep moving around creating read after read after read"; "#run a
mattpocock-skills to combat this drift".

Made with the Pocock skill `retro`, run from his repository (`mattpocock/skills`, `skills/engineering/retro/SKILL.md`):
read the session's own records, look for what in the agents' ENVIRONMENT would stop the fault, and put the
candidates in order of how much they cost. Every figure below is counted from `agent-runs.jsonl` (the newest line
of each run from 157 on that had handed back or been stopped when this was written: 45 runs).

## What the record shows

| Kind of agent | Runs | Tokens by the harness (where given) | Tokens in the transcripts | Of those, the run's own context read again | Stopped by his stop |
|---|---|---|---|---|---|
| scout | 7 | 500,004 | 3,695,590 | 2,910,868 | 2 |
| reviewer | 14 | 846,761 | 11,089,681 | 9,643,663 | 5 |
| builder | 11 | 542,917 | 8,401,029 | 7,577,064 | 4 |
| performance auditor | 13 | 609,409 | 2,315,433 | 1,685,450 | 0 |
| all | 45 | 2,499,091 | 25,501,733 | 21,817,045 | 11 |

- Of every 100 tokens in the transcripts, 86 are an agent reading its own context again on its next reply. A
  reviewer or a builder makes about one tool call a reply (the auditor's reports say so run by run), so a run of
  20 replies reads its context 20 times.
- TICKET 31, a tool of about 250 lines, took 13 runs to close: 5 builder runs, 3 reviewer reads, 5 auditor runs.
- Tickets 18 and 19 are on their fifth reviewer read; tickets 02 and 03 on their fifth.
- 11 of the 45 runs were stopped part way and their work done again by a new run.
- 13 of the 45 runs are the auditor, and what it writes is a count set beside a limit.

## The candidates, the most costly first

1. THE REVIEW HAS NO END. (The skill's heading: coding standards; implementation and review.) A reviewer was sent
   again after every builder pass, each time free to find anything, and a ticket stayed open while it found
   more. The agents' own file says the reviewer is "called rarely and on purpose"; the Pocock flow builds every
   ticket test-first and holds ONE review at the end, each report under 400 words, then ONE pass of fixes. "Round
   again until the reviewer leaves nothing" was the main session's reading in the twenty-fifth session, not his
   word. THE CHANGE (made now, in the page every brief points at): one reviewer read for a ticket, measured
   against the ticket's own "shown done by" line and the standing rules by name, 500 words at most; one builder
   pass on what it finds; the main session then runs the named checks and marks the box. What a reviewer sees
   beyond the ticket's line is one line each at the foot of the ticket. A second read only where the same check
   has failed twice (the reviewer's own file).

2. THE AUDIT IS A COUNT, AND A MODEL IS DOING IT. (The skill: a mechanical thing gets a deterministic check, not
   an agent.) Each auditor block sets eight limits beside figures read from a transcript and compares a line
   with its transcript: `run_plan check` and `run_record missing` already do most of it with no model. 13 runs
   and about 600,000 tokens went on it this session. PUT TO HIM, because the rule is his ("the auditor is called
   on every run"): the row for every run is made by one command, kept in git as now; the auditor agent is called
   once at a session's close and reads only the rows where a limit was passed or a line and its transcript
   differ. Until he says, the change made now is smaller: one auditor run at the close for all the runs still
   owing a row, not one for each group as they finish.

3. ONE TOOL CALL A REPLY. (The skill: tool economy.) Briefs ask for bundled commands and the transcripts show
   about one call a reply all the same. THE CHANGE: a builder and a reviewer are handed ONE command that does the
   standing things in one call (show the change, run the named checks, print the counts), and the brief names a
   number of replies to stay under. To be built as a small script by a builder (a ticket of its own; not started).

4. A STOP THROWS AWAY EVERY RUN THAT IS OUT. 11 runs were ended part way; a reviewer or a scout that is stopped
   leaves nothing a new run can take up. THE CHANGE made in the briefs since the second stop: push each piece as
   it stands; hand back early. What code cannot hold: a message to the main session redirects it without ending
   the agents; a stop ends them all.

5. THE MAIN SESSION ASKED WHAT THE RECORD ANSWERS, three times. (The skill: navigation.) The decisions file is
   7,900 lines; the page a session starts from names where things are, not what he has already decided, topic by
   topic. THE CHANGE: the start page for the next session carries a list "ANSWERED BY HIM, do not ask again",
   each line with its place in the decisions file, made from scout run 206's report; it is kept up at each close.

6. THE MACHINE WAS MISSING WHAT THE CHECKS NEED, and each lack was found by a failing run. (The skill:
   information access.) No platform checkout (three groups held for an hour); no pyarrow (the packet's checks
   could not run in any session on this environment); no stored planes; a data checkout made shallow by the
   checks themselves. THE CHANGE: the environment's setup script brings the platform checkout (done) and is to
   install pyarrow and fetch the planes; one command at a session's start prints what is missing before any
   agent is sent (to be built).

7. THE MAIN SESSION'S OWN CONTEXT. Every agent's report came back whole into the main session (about 60 reports,
   several thousand words each), and it wrote long briefs by hand. THE CHANGE made part way: one page every brief
   points at (`BRIEF_STANDING_20261124.md`), short briefs, a word limit on hand-backs from now.

## What is not proposed

Dropping the reviewer, the auditor or the record. His rules stand: every claim defended, every run measured,
zero outside git. The changes above cut how many times the same thing is read, not what is checked.
