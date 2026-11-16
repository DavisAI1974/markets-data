# Handoff, third session of 2026-11-16 (the ROOT gameplan)

Branch: `ccr-349e2ffe-07p8od` in `DavisAI1974/markets-data`. Pushes to it work from a cloud session.

## Read these, in this order

1. `root-redesign-20261116/ROOT_GAMEPLAN_DECISIONS.md`: every decision Greg made in this session, in his words where
   he gave them. This is the governing record.
2. `root-redesign-20261116/SPEC-root.md`: the draft specification of ROOT part 1, the foundation. Awaiting Greg's
   approval. Its "Open questions for Greg" are the first thing to put in front of him.
3. `root-redesign-20261116/WORKBOOK_README_PAGE.md`: the wording of the README page of the rebuilt workbook.
4. `ACTION_PLAN_20261116.md`: the earlier plan. Where it differs from the three files above, they win.

`CAPABILITY_MAP.md` and `SPEC-tape-stream.md` are superseded by `SPEC-root.md` and are deleted when Greg approves it.

## Where things stand

- **ROOT keeps its purpose**, the first calculations from the tape that every later stage reads, with one addition:
  it first pins everything together on one timeline. It is rebuilt from the ground up. Old ROOT outputs and old ROOT
  calculations are both discarded.
- **Part 1, the foundation, is gameplanned and specified** (draft): one timeline for the week, the book for the week,
  the native tape one row per tick, the book and order facts on each row, the 13 outside data points pinned, the
  checks including the playback check. Four trade days: Mon Oct 2, Tue Oct 3, Tue Oct 17, Wed Oct 18, 2023, each
  6 pm to 5 pm Eastern, with the 5 pm to 6 pm hour as its own marked stretch.
- **Part 2, the ROOT calculations, is not designed.** Greg's idea, late in the session: work out every calculation we
  want (the old ROOT sections, the SQL step, the other workflow step, the dipoles, the S fields, anything else) and
  do them all in ROOT, so that the later steps are only analysis, pattern matching and logic. Greg restated it:
  "So everything is calc and pinned correctly for the next steps and we eliminate some separate processes and do
  them all at once instead of split up." Claude proposed the shape (foundation plus calculations added one at a
  time, each named, pinned and checked; a calculation may only add columns); Greg has not said yes to that shape in
  so many words. Confirm it. His last word on it: "We'll still do that ahead of time. Frankie will just have to learn why
  and how dipole works and apply what he's learned when he sees it." So definitions are worked out by us ahead of
  time and calculated in ROOT; Frankie learns and recognizes, he does not calculate.
- **Working out those calculations is the calculation inventory**, laid out Greg's way for every one: what we want it
  to calculate, what is calculated today, and what changes. It has not been started beyond reading.
- **Why all of this:** the calculated data for a trade day is filled in beforehand and shown to Frankie one tick at
  a time, so he learns to recognize things as they unfold and sees what else is changing at the same moment.

## What was done to files in this session

- New: `ROOT_GAMEPLAN_DECISIONS.md`, `SPEC-root.md`, `WORKBOOK_README_PAGE.md`, `root-redesign-20261116/tools/`.
- A first sheet "READ ME FIRST" was added to `Frankie_four_day_research_current.xlsx` and
  `Priority_native_flow.xlsx` (fingerprints before and after are in the decisions file). The 500 MB R2 release
  workbook was not changed: a cloud session has no tool that replaces a release file.
- No ROOT code was written. Nothing was deleted.

## Waiting on Greg

1. The open questions in `SPEC-root.md` (which ticks outside the trade day get rows; the order of work while the
   outside data files cannot be reached; a trial sheet before the full workbook; where the stored rows live; the
   column list) and then his approval or corrections of part 1.
2. His yes on the shape of part 2.
3. His AWS sign-in (claude.ai connector settings). The 13 outside data files and their inputs are on S3; one attempt
   was made and it asked for a new sign-in.
4. Sign-offs of the old ROOT file list, the lineage delete list and the research intentions. Still not given.
5. Which comes first next: the calculation inventory for part 2, or building the foundation.
6. **`CLAUDE.md` in Markets still defines the trade day as 5 pm to 5 pm.** Greg decided in this session that a trade
   day is 6 pm to 5 pm with the 5 pm to 6 pm hour as its own stretch. `CLAUDE.md` loads in every session and has not
   been changed. It needs Greg's word before the trunk is edited.

## How Greg wants the work done (learned in this session)

- Slow down and gameplan. One piece at a time. Do not jump ahead, and do not write code or specs while a piece is
  being talked through.
- Plain words. Say what a thing is before using its name. He reads on a phone.
- Lay each piece out as: what we want it to calculate, what it calculates today, what changes.
- Do not carry the old ROOT forward in edited form, and do not write up old work that is being replaced. If
  something is wrong it gets fixed and we move on.
- Record his decisions in git as they are made.
- When he asks a question, answer it first, then return to the open item once, briefly.

## Model setup

- `/advisor fable` works when typed alone on its own line (it failed when the whole drop-in was pasted after it).
- Gameplan, inventory and specs: run on Fable. Building an approved part: switch to Opus (`/model opus`) with the
  Fable advisor. Claude cannot switch models; it tells Greg when it is time.
- The Superpowers plugin is installed and its start-up message pushes itself as a router. `CLAUDE.md` says one router
  only (agent-skills). Its brainstorming piece was used once on its own, at Greg's request.

## Practical notes

- **Environment.** This session ran in the "Default" cloud environment: Databento is refused there and no pull was
  needed. A pull needs the "Markets" environment, and the key saved there still has to be corrected (see the action
  plan, section 8).
- **Old code, for reading only.** It is not on the tips of the Markets trunk or the research branch. It is at
  Markets `7f34afa` (`git fetch --depth 1 origin codex/frankie-brain-four-day-pins-20261109`) and the producer
  package at pin `2ebb8ce8ef4834545ad99a4ecdff50c18c5b3134` (`git fetch --depth 1 origin <that sha>`).
- **Read in full in this session:** the book adapter, `native_rt_book.py`, `native_full_capture_adapter.py`,
  `native_replay_driver.py`, `native_roll20.py`, `native_session.py` (to line 310), `derive()` in
  `frankie_box_boss_session.py`, the head of `a_memory_member_first_recalculation_20260828.py`, `c15_observer.py`,
  and the builder of the 13 outside points, `frankie_day_external.py`.
- **Not read yet (needed for the inventory):** the section calculators of the producer package (queue,
  replenishment, absorption, response, mirror, ladder, lineage, recurrence, recognition, exhaustion, dipole,
  discovery, book regime, clocks, candidate and its adapter, flow substrate, detector coverage, group adapters), the
  SQLite and Julia family research (`artifacts/sqlite-triage/20261022/families/` in Markets), Codex's four-day
  workflow processing, the S-field code, and the Step 1 programs.
- **Where new ROOT code goes:** the Markets repository, folder `root/` with tests in `tests/root/`, on the session's
  own Markets branch.
- `pip install databento pyarrow` is needed in a fresh container; the seven raw MBO files read cleanly.
- **To verify on the tape before the `tape` part is planned:** whether the exchange's Sunday block of re-listed
  orders carries the vendor's snapshot flag (it decides whether those records are rows or snapshot records).
- **"No trades between 5 pm and 6 pm"** was counted on two evenings only (Mon Oct 2 and Tue Oct 17). The build's
  own counts will show the other evenings.
- **The "READ ME FIRST" sheets** added to the two workbooks were read back by program. They were not opened in Excel.
