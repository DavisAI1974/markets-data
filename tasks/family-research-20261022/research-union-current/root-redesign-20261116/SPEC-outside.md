# Spec: the `outside` part of ROOT (the 13 outside data points)

Status: DRAFT for Greg's approval, 2026-11-16. No code is written until he approves it.
It is one part of ROOT part 1 (`SPEC-root.md`, section G). Decisions behind it: `ROOT_GAMEPLAN_DECISIONS.md`.

## Objective

Make the 13 outside data points for the four trade days from the published source files held in git, and pin them
onto every row of the timeline, each value from the moment it became known.

Greg's rule for this part: **"Keep everything as it was in the original 13 dp files", with four fixes on top and
nothing else.**

1. Storage (X11): the figure as first printed on Thursday morning, not the later revised one.
2. Storage estimate against actual (X12): filled in.
3. Temperature (X10): worked out from the hourly readings, on the gas day ending 10 am Eastern, with wind and
   carry-over from earlier days as their own columns.
4. The published figures underneath each point are kept and go on the row as well.

"As it was" is defined by the original builder and the feeds it called, read at Markets `7f34afa`:
`frankie_day_external.py`, `cot_feed.py`, `nws_temp_feed.py`, `forward_curve.py`, `flow_calendar.py`,
`fetch_day_history.py`. Each formula is carried into the new part unchanged unless one of the four fixes changes it.
The new part does not import those files.

## Inputs

`data/outside/ng_oct2023/` in markets-data: 107 source files exactly as served, with `MANIFEST.json`. The part checks
every file's fingerprint against the manifest before reading it and stops, naming the file, if one differs.

## What it produces

1. **One table for each point:** every value, with the time it became known and the source file it came from. These
   tables exist as soon as the part is built; they do not need the tick rows.
2. **The 13 on every row of the timeline** (section G of the row), once the rows are built: at each tick, the latest
   value that had become known by that tick's received time. A value holds until the next one replaces it.
3. A receipt: inputs with fingerprints, counts, every empty value with its reason, and the result of every check.

## The 13, point by point

Times are when a value becomes known. They are the original's, declared by name in the code.

| Point | What it is (as in the original) | Known from | What the fixes change |
|---|---|---|---|
| X01, X03, X04 | Managed-money net position (long minus short) in the NYMEX gas contract, CFTC code 023651: where it stands among the last 1 year of weekly reports (X01, needs at least 45 of about 52), the change from the week before (X03), where it stands among the last 3 years (X04, needs at least 140 of about 156). | Friday 3:30 pm Eastern after the report date; a business day later in a holiday week. | Fix 4: long, short, net and the number of reports in each window on the row. |
| X08 | The same 1-year standing for the ICE Henry Hub contract, CFTC code 023391. The three other ICE gas codes are kept in its table as before. | as X01 | Fix 4, as above. |
| X02 | Forecast gas-weighted heating degree days, from the forecast model output (GFS, NAM, extended GFS), 16 cities with the original weights, for the trade day's date and the 7 days after. Every model run is kept. | the run's start time plus 4.5 hours | Fix 4: each city's forecast temperatures underneath. See call 2 and call 3. |
| X09 | Disagreement between models: GFS minus NAM in gas-weighted heating degree days on the cities both have, per shared run; the largest gap over the 8 days and which day it is at. | as X02 | none |
| X10 | Observed gas-weighted heating and cooling degree days and precipitation, 16 cities, with every station reading underneath. | each reading 10 minutes after its time; the gas-day figure 10 minutes after that gas day ends | **Fix 3.** The gas day ends 10 am Eastern (it was midnight Central). The day's temperature is the mean of the hourly readings (it was the high and low averaged). Wind and carry-over become their own columns. See call 4. |
| X05, X07 | US48 wind generation by hour (X05); gas burned for power, estimated as gas generation in the hour x 24 x 7,900 / 1.035e9 (X07). The hourly rows of the six regions are kept underneath. | the hour plus 2 hours | none. **Waits on the EIA's own US48 figure** (see "What is still missing"). |
| X06 | Trading sessions since the front contract last expired, with that contract's symbol and expiry date. | see call 1 | none |
| X11 | Weekly storage: level, change on the week, and the comparison with the five-year average. | Thursday 10:30 am Eastern after the week | **Fix 1.** The level is the EIA's original estimate before any revision (`revisions.xls`). The change is the difference of two such levels. The five-year comparison is the original's fallback rule: the level minus the mean of the same week in the five years before, all five listed beside it. |
| X12 | The street estimate of the weekly change, the printed actual, and actual minus estimate, one row per weekly report. | the report's own release time | **Fix 2.** Filled in. **Waits on the saved pages** (see "What is still missing"). |
| X13 | The futures curve: the contract list, every exchange statistic, every trade of every month; and the curve's shape over the 12 nearest contract months (front, next, the far month, the two slopes, the curvature, front minus next, backwardation or contango), once from settlement prices and once from last trades, recomputed at each change. | each record's own received time | none. Trades are read from the vendor's trades files; the original read the same trades out of the full order tape. |

For the four trade days, read from the files: no positioning report and no storage report comes out inside any of
them, so trade days Oct 2 and Oct 3 carry the report of Sep 28 for storage (week ending Sep 22) and the positioning
report dated Sep 26; trade days Oct 17 and Oct 18 carry the storage report of Oct 12 (week ending Oct 6) and the
positioning report dated Oct 10.

## Claude's calls. Correct any that are wrong.

1. **X06, when it is known.** The original stamped it at the open of the trade day and then an old reader rule moved
   any value with no time of its own to 2 pm Eastern. On a row-by-row timeline that would leave the first 20 hours of
   each trade day showing the previous trade day's count. Call: the count for a trade day is on every row of that
   trade day, known from its open.
2. **X02, how many forecasts.** The original files keep every model run. Earlier on 2026-11-16 Greg said to use one
   forecast per trade day for the ROOT stage. "Keep everything as it was" came later. Call: as the original; every
   run is kept and a row carries the latest run known at its tick.
3. **X02 and X09, which day they describe.** Fix 3 moves the observed temperature to the gas day ending 10 am
   Eastern. Call: the forecast degree days use the same gas day and the same mean-of-readings rule, on the forecast
   temperatures the model gives inside that day (every 3 hours for GFS and NAM, every 12 for extended GFS), so the
   forecast and the observed figure describe the same day.
4. **X10, the details of fix 3.** Call: one reading per hour and station, the routine hourly report; degree days
   from the mean of those readings, base 65 degrees F as before; wind is the gas-weighted mean wind speed over the
   same gas day; carry-over is the gas-weighted heating degree days of each of the two gas days before, as two
   columns. The number of hours with a reading is on the row; a station with none that gas day is named, and the
   weights are spread over the stations present, as before.
5. **Curve files.** Every curve file held is read in time order, so the settlement shape known at the open of trade
   day Mon Oct 2 is Friday's. The original read only the two clock-day files of each trade day.
6. **Where the tables are kept.** In markets-data beside the source files, `data/outside/ng_oct2023/made/`, one
   plain table per point, with the receipt.
7. **A workbook of the tables now.** Proposed, for Greg's yes or no: a small workbook with one sheet per point, so
   the 13 can be seen before the tick rows exist. It is separate from the four trade-day sheets.

## What is still missing

| Point | What | What it waits on |
|---|---|---|
| X05, X07 | the EIA's own US48 figure | `api.eia.gov` allowed on the cloud environment and a free EIA key. The file held has 62 regions and no national row; adding them up ourselves is not "as it was". |
| X12 | the street estimate | `web.archive.org` allowed on the cloud environment. The estimates were read from saved copies of two web pages. |
| X01, X03, X04, X08 | a record of when each October 2023 report came out | The original worked the time out by rule; that rule is kept and marked as a rule, not a record. |

A point that is waiting is built with everything else in place and its values empty, each with the stated reason.
Nothing is estimated or filled in.

## Success criteria

1. Every source file read matches its fingerprint in the manifest.
2. Each of the 13 is either filled on every row or empty with a stated reason. No value is invented.
3. On every row, each outside value became known at or before the row's received time, and is the latest such value.
4. Every number written into the code is on the declared list with its reason: the availability times, the window
   lengths and minimum counts, the 16 weights, base 65, the gas-burn conversion, the 12 contract months.
5. Two runs on the same inputs give byte-identical tables.
6. Tests use the real source files only.
7. When AWS can be reached again: the points the fixes do not touch (X01, X03, X04, X08, X09, X13) are compared with
   the original made files, value by value, and every difference is listed with its cause.

## Where the code goes

Markets repository, `root/outside.py` with tests in `tests/root/`, on the building session's own branch. No new
dependency beyond `databento` (to read the curve files) and a reader for the EIA's `.xls` files, which is asked for
before it is added.

## Boundaries

- **Always:** keep every source row; declare every constant; leave a missing value empty with its reason; write the
  receipt.
- **Ask first:** any paid download; any new source; any change to a formula of the original beyond the four fixes.
- **Never:** use the old workbook or an old made file as a source; fill a value from a different report or a
  different day; put a cost or fee into anything.
