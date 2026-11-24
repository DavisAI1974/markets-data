# Handoff, fourth session of 2026-11-16 (ROOT part 1 settled; ready to build)

Branch: `ccr-349e2ffe-07p8od` in `DavisAI1974/markets-data`. This file replaces `NEXT_SESSION_HANDOFF_20261116C.md`
as the starting point; C lists as open several things that are now closed.

## Read these, in this order

1. `root-redesign-20261116/ROOT_GAMEPLAN_DECISIONS.md`: every decision, in Greg's words. The section "Answers to the
   open questions of `SPEC-root.md`" holds everything decided in this session.
2. `root-redesign-20261116/SPEC-root.md`: ROOT part 1, the foundation. All five open questions are answered and the
   text is in line with them. **It waits only for Greg's approval.**
3. `root-redesign-20261116/SPEC-outside.md`: the 13 outside data points. **Approved by Greg.**
4. `data/outside/ng_oct2023/README.md` (in the repository root, not the research folder): the source files held.
5. `root-audit-20261116/OLD_MATERIAL_REMOVAL_LIST.md`: what is deleted when Greg says "delete".

## What closed in this session

- **Which ticks get rows:** the four trade days, the 5 pm to 6 pm stretch on each side, the Sunday start-up before
  trade day Oct 2. The extra ticks only complete the book; nothing is calculated on them and anything ever made from
  them is kept completely apart. A row whose order entered before the written record carries a mark.
- **The 13 outside data points do not wait on AWS.** Their source files were fetched from the original public
  sources and Databento and are in git: `data/outside/ng_oct2023/`, 142 files, with a manifest. 12 of the 13 have
  their sources; only the street estimate of storage (X12) has none (it needs `web.archive.org`).
- **The 13 are as in the original files, with four fixes, kept simple for this first ROOT part** (one forecast per
  trade day; the Thursday storage figure). `SPEC-outside.md` is approved.
- **Excel questions:** already settled by Greg in earlier sessions; see the decisions file. The longest line of
  orders at one price on the held tape is 49, so a full line always fits in one cell.
- **Part 2 shape confirmed,** with three rules: nothing is stated twice; every calculation is looked at before it is
  run; columns may be eliminated later on Greg's decision, everything is kept for now.
- **Step 1 stays and is built on top of.** Its columns stay in the workbook; the 2021 definitions and data are the
  base; the new data expands it once the hard-coded cutoffs are listed for Greg and removed. Base and growth go in
  separate columns. It is handled with the calculations of part 2, not the foundation.
- **The raw data collected on 2026-11-16 stays** and was double-checked (see the README beside it).
- **Foundation first.** "The calcs come from the initial foundation."
- **Old material is discarded, not archived.** The delete list is written and waits for Greg's "delete".

## Waiting on Greg

(Part 1 was APPROVED and the old material DELETED later the same session; see the decisions file.)

3. `web.archive.org` allowed on the "Markets" cloud environment, if X12 is wanted before the later update. Greg adds
   it by hand; the service rejected the request when it was in a list with other sites.
4. Permission for Markets branches other than the session's, when old ROOT code is deleted there.

## Done later in the session (on Opus)

- `SPEC-root.md` APPROVED ("Foundation is good"). The old material DELETED (672 files, one commit `ee4da3f`).
- First piece BUILT: the `outside` tables. Markets `ccr-ddc0ebeb-do2y3o` at `6208460` (`root/calendar.py`,
  `root/outside.py`, `root/DECLARED_CONSTANTS.md`, `tests/root/`, 21 tests passing); tables, receipt and a small
  workbook in markets-data `data/outside/ng_oct2023/made/`. Storage (X11, X12) not made: waits on Greg's word on
  `xlrd`. Step 1 search recorded in the decisions file.

## Decided at the end of the session (back on Fable)

- **Step 1.** No correct Step 1 exists for the four trade days; the old Step 1 outputs are on other dates (2021 and
  2025-26) and carry assumed trade costs, so their values are not carried. The rerun reads everything we hold (full
  order tape, full book, the 13). Depth is judged by outputs laid side by side, after the foundation. Two columns:
  the first is Step 1 as originally defined, made on the four trade days; the second is the growth, its inputs
  decided when it is laid out. The list of hard-coded boundaries is owed to Greg first. Detail and the paths of the
  files Codex found are in the decisions file.

- **Merge, not scrap.** The new run's outputs are merged with the 55-week findings into a new Step 1 knowledge base;
  conflicts get a deeper dive. Claude's proposed way of doing it (statements with what each was measured on, never
  mixed rows) is in the decisions file, awaiting Greg's yes. The 5-year full order tape on S3 covers the 55 weeks and
  all of October 2023, so old and new can later be measured on the same events once AWS is back.

- **One run.** Step 1 and Step 2 calculations (the two Step 1 columns, and Step 1 with the Phase 2 calculations) are
  made in the same single pass wherever that can be done; each stays its own named calculation with its own checks.

- **One exception to "no averages".** Greg: a Step 1 calculation works the same data both averaged and not averaged,
  for different answers. Both are kept, each in its own column. Which calculation it is gets confirmed with him when
  the Step 1 calculations are laid out. The rule stands everywhere else.

## Where the ROOT code is (read this before building)

**The new ROOT code exists only on Markets branch `ccr-ddc0ebeb-do2y3o`** (commits `a1b3ad2` and `6208460`: `root/` and
`tests/root/`). A new session is given a new, empty branch. Start by bringing that work in:
`git fetch origin ccr-ddc0ebeb-do2y3o && git merge --no-edit FETCH_HEAD` (or cherry-pick the two commits), then run
`MARKETS_DATA=<markets-data checkout> python3 -m pytest tests/root -q` and see 21 pass before adding anything.

## What to do next (on Opus, with the Fable advisor; a fresh session is suggested)

- Storage tables (X11, X12 actual) with `xlrd`, unless Greg has said no.
- Then: `calendar`, `tape`, `book`, `rows`, `store` and `checks`, then pinning the
  13 onto the rows, then `sheet`. The first sheet written is a short stretch; its size is reported before the full
  workbook is written.
- New ROOT code goes in the Markets repository, `root/` with tests in `tests/root/`, on the session's own Markets
  branch. Real tape only in tests.
- After the foundation: the calculations, one at a time, each laid out Greg's way and approved before it runs.
- Before the `tape` part: check on the tape whether the Sunday block of re-listed orders carries the vendor's
  snapshot flag.

## How Greg wants the work done

- Slow, one piece at a time, plain words. He reads on a phone.
- Each piece: what we want it to calculate, what it calculates today, what changes.
- **Do not re-ask what he has already decided.** When he says something was covered, it was: read the earlier
  session's transcript (the session tools can list a past session's messages) before putting it to him again.
- Where a point is a detail and not his decision, make the call, state it, and let him correct it.
- Record his decisions in git as they are made. Answer his question first, then return to the open item once.
- Do not carry old ROOT forward, and do not write up old work that is replaced.

## Practical notes

- **Cloud environment "Markets".** Allowed now: `hist.databento.com`, `www.cftc.gov`, `www.eia.gov`, `ir.eia.gov`,
  `api.eia.gov`, `mesonet.agron.iastate.edu`. AWS is off limits on Greg's word ("Aws is unavailable so don't try it").
- **Databento key:** saved cleanly on the environment; the network supplies it. Give the client a placeholder,
  `db.Historical('db-' + 'x' * 29)`. Never write a key into either repository.
- **EIA key:** Greg gave one in chat for the fetch. It is in no file. `fetch_eia_api.py` reads it from the
  environment variable `EIA_API_KEY` if a re-fetch is ever needed.
- **Fresh container:** `pip install databento pyarrow xlrd openpyxl`.
- **Old code, for reading only:** Markets `7f34afa` (`git fetch --depth 1 origin
  codex/frankie-brain-four-day-pins-20261109`) and the producer package at pin
  `2ebb8ce8ef4834545ad99a4ecdff50c18c5b3134`. The original builder of the 13 is also on the Markets trunk at
  `artifacts/sqlite-triage/20261022/families/external-classroom-audit-v1/frankie_day_external.py`.
- **Skills:** `/advisor fable` works. `using-agent-skills` was not loaded in this session ("Unknown skill"). The
  Superpowers brainstorming skill was used on its own.
