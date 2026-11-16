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
- **Foundation first.** "The calcs come from the initial foundation."
- **Old material is discarded, not archived.** The delete list is written and waits for Greg's "delete".

## Waiting on Greg

1. Approval of `SPEC-root.md` part 1.
2. The word "delete" for `OLD_MATERIAL_REMOVAL_LIST.md` (four groups; group 4 was added after he first saw the list).
3. `web.archive.org` allowed on the "Markets" cloud environment, if X12 is wanted before the later update. Greg adds
   it by hand; the service rejected the request when it was in a list with other sites.
4. Permission for Markets branches other than the session's, when old ROOT code is deleted there.

## What to do next

- **Switch to Opus with the Fable advisor (`/model opus`).** The gameplan for part 1 is finished.
- First build: the `outside` part's point tables and their small workbook (approved). It needs the trade-day cut but
  not the tick rows.
- Then, once `SPEC-root.md` is approved: `calendar`, `tape`, `book`, `rows`, `store` and `checks`, then pinning the
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
