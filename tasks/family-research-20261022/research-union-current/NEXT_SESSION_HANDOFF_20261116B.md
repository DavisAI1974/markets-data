# Handoff, second session of 2026-11-16

Branch: `ccr-349e2ffe-07p8od` in `DavisAI1974/markets-data` (Greg approved committing straight to it). Read
`NEXT_SESSION_HANDOFF_20261116.md` first for the standing rules; this file is what changed after it.

## Greg's calls this session

- **No bad version is kept.** Use the correct build, replace, and remove the old one. No old-versus-new comparison
  lists, no old cursor numbering carried along. The old build is not a pass/fail test for the new one.
- **Resting-order age:** the adapter rule is left alone. The warm-up starts at the Sunday file of the trade week.
- **Storage:** put things in git however is best. The 8.9 GB of per-trade book records are rebuilt on demand, not stored.
- **S replay:** run it in Runpod pods, all four trade days at once.
- **Step 1 populations (L080, L083-L089):** not "not applicable". They are the 2021 base, to be expanded by the new
  trade days after the hard-coded boundaries are listed and removed. Families stay trade-agnostic; each trade gets
  its own record of the families it sits in (Greg undecided on going further).
- **Runpod volume:** option 2: see what is on it, move what is worth keeping to a right-sized volume, then delete it.
  Greg expects a good part of the stored ROOT data to be reusable even if some ROOT work is redone.

## Done and pushed

1. **Age checks** (`resting-order-age-20261116/`): on 2,926 orders at four 00:00 UTC boundaries the snapshot's event
   time is exactly the event time of the message that last set the order's queue priority. The Sunday file re-lists
   every weekend carry-over order in one block with one stamp; no older entry time exists on the tape.
2. **Tape:** `NG_v0_mbo_20231015.dbn.zst` added (29,063 records, $0.0027).
3. **Trade-day replay** (`trade-day-rebuild-20261116/scripts/trade_day_stream.py`): warm-up from the Sunday file
   (Oct 1 for trade days Oct 2-3, Oct 15 for Oct 17-18); live `floor` list of orders whose age is only a lower bound.
   All four trade days re-verified. README there is the recipe for building a new trade day.
4. **Book record at every trade** (`scripts/build_book_records.py`): 143,979 records built, every row check passed.
   In git: receipts, shard manifests, and the full records for the 5,513 workbook ticks (`book_records/`). The old
   selected-tick records under `field-rebuild-20261113/book_records/` were removed.

## Not done

- **Workbook cells** still hold old values; they change when the R3 workbook is written.
- **Old archive branches** `codex/frankie-book-recovery-*` still exist (to be removed last; may need Greg, since this
  session's permission system refuses pushes to other branches).
- **The two hours:** fields for the 457 new trades (trade day Oct 2) and 252 (trade day Oct 17). Includes attaching
  the 13 external points (sheet fields X01-X13); where the four October 2023 day files live is not yet checked.
- **S replay:** `recover_second_set.py` (Markets `7f34afa`) must be pointed at `trade_day_stream.py` and matched on a
  first stretch of trade day Oct 18 before any pod run. Stored trade day Oct 18 S04/S09 are built on restarted ages.
- **Step 1 programs** (Markets `7f34afa`, `research/ng_exhaustion_mbo_5y_step1_census_20260822.py` and two others):
  located, not read through. Hard-coded so far seen: `MAX_DEPTH = 5` (lineage depth), `INITIAL_TRAIN_WEEKS = 52`,
  `TEST_BLOCK_WEEKS = 26`, and the frozen family classifier.
- **Family fields:** Desktop's family research is in Markets `artifacts/sqlite-triage/20261022/families/`. For trade
  day Oct 18 the Frankie ROOT run saved planes for L062, L063, L067-L071; L060 and L061 are not among its 18 planes.
- **Trade-day rule in Markets `CLAUDE.md`:** on branch `ccr-5317ce1c-hpqa9c` only. Pushes to the trunk and to
  `research/markets-adaptive-wavepacket-migration-20261108` were refused by the permission system.

## Runpod

- Signed in by email code as the account owner; key `runpod-cli-agent` is saved only in that session's container.
  The Runpod plugin was enabled on the account mid-session and its tools connected.
- Account: balance $38.99 at 08:30 UTC Nov 16; no pods; endpoint `frankie-reading-granite42` idle;
  volume `qu5lhaqqbx` (`ng-replay-20231002-03-17-scratch`, 4,096 GB, US-CA-2, high-performance).
- Billing records show spend only on UTC clock days Nov 8 ($33.43) and Nov 9 ($16.76); the account's
  "current spend per hour" field reads $0.284. Whether the volume is charging now was not settled.
- Codex's saved notes say the volume holds the ROOT and native outputs for trade days Oct 2, 3 and 17 (journals,
  book frames, structures, signed flow, order ledgers, lifecycle records, dipole candidates and episodes, archives),
  built on the old cut, with the S-field calculations excluded. No file listing has been made.
- **Blocked:** four CPU pods created in US-CA-2 (cpu3c and cpu3g, with and without the volume) all showed status
  RUNNING but never started a container in 8 to 13 minutes: no runtime, no system log, exec answered "Pod not
  found". All four were terminated. The control without the volume failed the same way, so the volume is not the
  cause. CPU price read: cpu3c $0.03 and cpu3g $0.04 per vCPU-hour.

## Container notes

- Network: session moved to the "Markets" environment; allowed hosts now include hist.databento.com,
  agents.runpod.io, api.runpod.io, api.runpod.ai, mcp.runpod.io, hapi.runpod.net.
- The Runpod command-line tool ignores the session proxy; run it through a wrapper that sets aiohttp `trust_env`.
- Pinned code worktree: Markets `7f34afa` at `/home/user/work/pins`. `pip install databento pyarrow pandas runpod`.
