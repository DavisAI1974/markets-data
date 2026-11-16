# Handoff for the next session (written 2026-11-16)

Branch: `ccr-349e2ffe-07p8od` in `DavisAI1974/markets-data`, started from `codex/evidence-availability-20261113` at
`1dd7d93`. It contains Codex's work plus this session's two folders:
`s-field-test-20261116/` and `trade-day-rebuild-20261116/`. Read both READMEs/receipts before doing anything.

## Standing rules from Greg (this session)

- **Trade day only.** A trade day is the CME session: 17:00 ET the evening before (the halt; trading resumes
  18:00 ET) to 17:00 ET on the named date. Never write a bare "day" or bare date: say "trade day" or "UTC clock
  day". The UTC clock day exists only because the vendor cuts raw tape files that way. Download whichever UTC
  clock-day files cover a trade day; build, label and analyze on the trade day; shelve (do not delete, do not use)
  the hours that belong to another trade day. Any exception needs a specific stated reason.
- **Every trade individually.** No rates, correlations, averages or model scores as a readout, and no market rule
  derived from an average. Recurring explanations may be noted only after the individual trades are laid out, with
  the trades where they hold and where they do not.
- **IDs and clocks designate; they are not inputs.** Keep every ID and clock with each trade. They must not be
  values in a calculation. Durations (order age) and counts of elapsed groups are the two time-derived values in
  the S calculation; whether they count as market conditions is Greg's call.
- **Never invent data.** Unavailable stays empty with an explicit status.
- **Frankie output fields stay blank** (L077-L079, L091-L092, L094-L098). Launch is HOLD.
- **AWS**: the connector needed a new sign-in; one attempt only, do not spend time on it. Pods may be used if needed.
- **Earlier Claude analysis** (`main` / `codex/claude-independent-research-20261113`) is not to be read or allowed
  to shape new strategies. An informal side-by-side comes after the new work is done.
- Save to git only. Nothing on local drives is durable.

## What is done

1. **Empty-cell census of the R2 workbook** (5,513 ticks): `s-field-test-20261116/results/census.json`.
   Empty on all four trade days: L024, L026, L060-L063, L067-L071, L077-L080, L083-L089, L091-L092, L094-L098.
   Empty on trade days Oct 2, 3, 17: S01-S19. Nothing else.
2. **S-field source found.** `recover_second_set.py` on Markets `codex/frankie-brain-four-day-pins-20261109`
   (`7f34afa`); GitHub run 42640458600 holds checkpoint 9 for trade day Oct 2 (never finished, not restarted).
   It runs unchanged in a cloud container via `s-field-test-20261116/scripts/run_second_set.py`, about 35-50
   messages per second per core.
3. **Oct 18 per-trade ledger** (30,739 trades) and **twin pairs**: `s-field-test-20261116/results/`. Field-by-field
   facts are in that README. Six S fields (S02, S05, S07, S09, S10, S13) track elapsed session time.
4. **Trade-day replay built and verified for all four trade days**: `trade-day-rebuild-20261116/`.

## Trade-day rebuild results (`trade-day-rebuild-20261116/results/*_RECEIPT.json`)

| Trade day | Session messages | Trades | New trades (18:00-20:00 ET) | Position shift vs old archive |
|---|---:|---:|---:|---|
| Oct 2 | 820,642 | 38,127 | 457 | cursor +12,189, group +9,320 |
| Oct 3 | 879,830 | 41,410 | 0 | none |
| Oct 17 | 846,406 | 33,703 | 252 | cursor +4,805, group +3,154 |
| Oct 18 | 771,787 | 30,739 | 0 | none |

- Every message equals the archived message at the mapped position, on all four.
- Every existing trade (143,270) is found identical at the mapped cursor and group. New total: 143,979.
- `*_trades.parquet` lists every trade of the trade day with its new cursor, its old cursor
  (`prior_archive_trade_cursor`) and `in_prior_trade_list`.
- **Midnight UTC carry is exact.** On all four evenings the book carried through the prior file equals the
  exchange's 00:00 UTC snapshot: same orders, sides, prices, sizes, and identical queue order on every price level.
- **The book issue.** The old replay applied that snapshot, which restarted every resting order's priority time
  and last-update time at 00:00 UTC (20:00 ET). The new replay carries the book through. The only differences from
  the archive are those two time fields.
- Snapshot records carry each order's true event time. For 225-278 resting orders per trade day (Oct 3, 17, 18)
  that time is more than a second older than what the replay knows, i.e. orders resting from before the warm-up
  file. Their ages remain lower bounds unless the snapshot event time is adopted. Not yet decided.

## Next, in Greg's order

1. **Book issue.** Recompute the book/FIFO record at every trade on the carried book and compare, trade by trade,
   with what is in the sheet. Expected to differ after 20:00 ET on all four trade days: order-age and queue fields
   (L041-L043, and age parts of L065), S04, S09, anything following the same orders over time. List every changed
   cell; correct in place with source and method.
2. **Fill the two hours.** Trade day Oct 2: 457 new trades; trade day Oct 17: 252. Each needs its book snapshot
   and all per-trade fields, built the same way as existing trades. None of the 32 selected cases is in those
   hours, so this affects the full four-trade-day sheet, not the eight-trade sheet's tick rows.
3. **S fields on trade days Oct 2, 3, 17** — pending Greg's answers below. The replay must consume the trade-day
   stream (`trade_day_stream.py`), not the old archives, and must be validated against the stored Oct 18 values on
   a first stretch before any full run.
4. Then write the new workbook release (R3) and apply the same to `Frankie_four_day_research_current.xlsx`.

## Carried over at Greg's request: the resting-order age question

Raise this with Greg at the start of the next session, before the book issue is worked.

- What is known: after the midnight carry, an order placed during the warm-up file or the trade day has its true
  priority time. An order that was already resting when the warm-up file opens does not: the replay first sees it
  in that file's opening snapshot and stamps it with the snapshot's receive time (00:00 UTC of the warm-up file).
- Size of it: on trade days Oct 3, 17 and 18, 252, 225 and 278 resting orders at the 00:00 UTC check have a
  snapshot event time more than one second older than the priority time the replay holds. On trade day Oct 2 the
  count is 0 (the warm-up is Sunday's file).
- Why it matters: every order-age value built on those orders (front-order age, queue-age percentiles, S04, S09)
  is a lower bound, not the true age, for as long as the order rests.
- The question: adopt the exchange snapshot's own event time as the order's priority time, or keep the receive-time
  stamp and mark those ages as lower bounds. Adopting it changes the adapter's rule (it uses receive time), mixes
  event time with receive time for those orders, and has not been tested. Not yet checked: whether a snapshot
  event time is the order's original entry or its last priority-changing modification.

## Open decisions for Greg

- The six clock-like S fields: rebuild on a rolling window, keep and mark "tracks session time", or drop.
- Run the S replay for the other three trade days now, or first read the Oct 18 chain fields (S01, S19) against
  each dipole's life.
- L024, L026, L080, L083-L089 are defined as the sealed October 2021 package; proposal is to mark them "not
  applicable to 2023 trades".
- L060-L063, L067-L071: definitions are prose; no complete runnable producer was found in git.
- The resting-order age question above.
- Add the trade-day rule to the project `CLAUDE.md`.

## Practical notes for the container

- Disk allowance is tight (about 6 GB free). Never fetch the book-recovery or replay-archive branches whole: use
  `git fetch --depth 1 --filter=blob:none origin <branch>` and read single files with `git show`.
- `pip install databento pyarrow pandas scikit-learn scipy`. `torch` cannot be installed; the S replay never calls
  it and `run_second_set.py` installs a stand-in that raises if it is ever used.
- Code worktree used here: Markets `7f34afa` checked out at `/home/user/work/pins`; the scripts hard-code that path
  and `/home/user/markets-data`.
- Raw tape: `data/nymex_mbo/ng_v0_oct2023/` (UTC clock-day files Oct 1, 2, 3, 16, 17, 18).
- R2 workbook: release `eight-trade-types-repair-20261115-r2`, SHA256 `49dd87cc80b5bea8b0d7d6ab320c63f70432ea705f554807f5a3948f2dce8257`.
