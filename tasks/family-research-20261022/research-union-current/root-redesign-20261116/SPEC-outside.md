# Spec: the `outside` part of ROOT (the 13 outside data points)

Status: DRAFT, 2026-11-16. Not ready for approval until the questions at the end are answered. No code is written
until Greg approves it.
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

`data/outside/ng_oct2023/` in markets-data: the source files exactly as served, with `MANIFEST.json`. The part checks
every file's fingerprint against the manifest before reading it and stops, naming the file, if one differs.

## What it produces

1. **One table for each point:** every value, with the time it became known and the source file it came from. These
   tables need the trade-day cut but not the tick rows, so they are the first thing built.
2. **The 13 on every row of the timeline** (section G of the row), once the rows are built: at each tick, the latest
   value that had become known by that tick's received time. A value holds until the next one replaces it.
3. A receipt: inputs with fingerprints, counts, every empty value with its reason, and the result of every check.

## What the original put beside a row

The original carried 13 points as 30 figures plus one hourly temperature per city. The new part carries the same:

| Point | Figures beside a row, as in the original |
|---|---|
| X01, X03, X04 | the NYMEX gas contract's managed-money net position: its standing among the last year of reports, its change on the week, its standing among the last three years |
| X08 | the ICE Henry Hub contract's standing among the last year |
| X02 | four forecast figures (gas-weighted heating degree days): GFS for the trade day's date, NAM for the same date, GFS for the day after, extended GFS for three days after. Each updates with every new model run. |
| X09 | the largest gap between GFS and NAM over the 8 days forecast, per shared run |
| X05, X07 | US48 wind generation in the hour; the gas-burn estimate for the hour |
| X06 | trading sessions since the front contract last expired |
| X10 | the observed gas-weighted heating degree days; and the latest hourly temperature of each of 18 cities (the 16 weighted ones, plus Austin and San Antonio, which carry no weight) |
| X11 | storage level, change on the week, comparison with the five-year average |
| X12 | the street estimate, the printed actual, actual minus estimate |
| X13 | the curve's shape, twice: from settlement prices (front, slope to the next month, slope to the far month, curvature, front minus next) and from last trades (the same, plus the next month's price) |

## How each point is made

Times are when a value becomes known. They are the original's, declared by name in the code.

| Point | How it is made (as in the original) | Known from | What the fixes change |
|---|---|---|---|
| X01, X03, X04 | Net = long minus short for managed money, CFTC code 023651. Standing = where this week's net falls among the reports of the trailing window: 1 year (at least 45 of about 52 reports, else empty) and 3 years (at least 140 of about 156). Change = this report minus the one before. | Friday 3:30 pm Eastern after the report date, a business day later in a holiday week. This is a rule, as in the original, not a record. | Fix 4: long, short, net and the number of reports in each window on the row. |
| X08 | The same 1-year standing for CFTC code 023391. The three other ICE gas codes stay in its table. | as X01 | Fix 4, as above. |
| X02 | For each model run and each city: the forecast temperatures for a target date give that date's high and low; their mean gives degree days, base 65 F; the cities are combined with the 16 original weights, spread over the cities present. Target dates: the trade day's date and the 7 after. | the run's start time plus 4.5 hours | Fix 4: each city's forecast temperatures underneath. See questions 1 and 2. |
| X09 | GFS minus NAM in gas-weighted heating degree days on the cities both have, per shared run; the largest gap over the 8 target dates and which one it is at. | as X02 | none, unless question 2 changes the day |
| X10 | Observed gas-weighted heating and cooling degree days and precipitation per gas day, 16 cities with the original weights; every station reading underneath. | each reading 10 minutes after its time; the gas-day figure 10 minutes after that gas day ends | **Fix 3.** The gas day ends 10 am Eastern (it was midnight Central). The temperature comes from the hourly readings (it was the high and low averaged). Wind and carry-over are their own columns. The routine hourly reading of each hour is taken from the routine-only files, so the source identifies it. See question 3. |
| X05, X07 | US48 wind generation by hour (X05). Gas burned for power, estimated as US48 gas generation in the hour x 24 x 7,900 / 1.035e9 (X07). Both from the EIA's own US48 rows (`raw/eia930/api/`), as in the original. The hourly rows of the six regions stay underneath. | the hour plus 2 hours | none |
| X06 | Trading sessions since the front contract last expired, with that contract's symbol and expiry date. | see call 1 | none |
| X11 | Level, change on the week, comparison with the five-year average. The original took all of them from the printed report where a saved copy was held, and otherwise from the EIA's series. | Thursday 10:30 am Eastern after the week | **Fix 1.** Level: the EIA's original estimate before any revision (`revisions.xls`). Change: the difference of two such levels. See call 2 for the five-year comparison. |
| X12 | The street estimate of the weekly change, the printed actual, actual minus estimate; one row per weekly report, and a report whose estimate was not found keeps its row empty with the reason. | the report's release time | **Fix 2.** Filled in. Waits on the saved pages. |
| X13 | The contract list, every exchange statistic and every trade of every month. The shape is worked out over the 12 nearest contract months that have a price, once from settlement prices and once from last trades, again at each change. | each record's own received time | none. Trades are read from the vendor's trades files; the original read the same trades out of the full order tape. |

Which reports the four trade days carry (report dates read from the files; release times by the rules above): trade
days Oct 2 and Oct 3 carry the storage report for the week ending Sep 22 and the positioning report dated Sep 26;
trade days Oct 17 and Oct 18 carry the storage report for the week ending Oct 6 and the positioning report dated
Oct 10. By those rules no storage or positioning report comes out inside any of the four trade days.

## Claude's calls. Correct any that are wrong.

1. **X06, when it is known.** The original stamped it at the open of the trade day, and then an old reader rule moved
   any value with no time of its own to 2 pm Eastern. On a row-by-row timeline that would leave the first 20 hours of
   each trade day showing the previous trade day's count. Call: the count for a trade day is on every row of that
   trade day, known from its open.
2. **X11, the five-year comparison.** The figure as printed (the five-year average and the year-ago level) was on the
   report page, which the EIA does not keep; it waits on the Internet Archive. Until then the original's own fallback
   is used: the level minus the mean of the same week in the five years before, the five levels listed beside it,
   taken from the EIA history file `ngshistory.xls`. Each row names which rule made it.
3. **Curve files.** Every curve file held is read in time order, so the settlement shape known at the open of trade
   day Mon Oct 2 is Friday's. The original read only the two clock-day files of each trade day.
4. **Where the tables are kept.** In markets-data beside the source files, `data/outside/ng_oct2023/made/`, one
   plain table per point, with the receipt.

## What is still missing

| Point | What | What it waits on |
|---|---|---|
| X12 | the street estimate | `web.archive.org` allowed on the cloud environment. The estimates were read from saved copies of two web pages. |
| X11 | the five-year average and year-ago level exactly as printed | `web.archive.org`, the saved report pages. |

A point that is waiting is built with everything else in place and its values empty, each with the stated reason.
Nothing is estimated or filled in.

## Success criteria

1. Every source file read matches its fingerprint in the manifest.
2. Each figure is either filled on every row or empty with a stated reason. No value is invented.
3. On every row, each outside value became known at or before the row's received time, and is the latest such value.
4. Every number written into the code is on the declared list with its reason: the availability times, the window
   lengths and minimum counts, the 16 weights, base 65, the gas-burn conversion, the 12 contract months.
5. Two runs on the same inputs give byte-identical tables.
6. Tests use the real source files only.
7. When AWS can be reached again: the figures the fixes do not touch are compared with the original made files,
   value by value, and every difference is listed with its cause.

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

## Questions for Greg (these are his decisions, not calls)

1. **The forecast on a row (X02).** The original showed four forecast figures, each updating with every new model
   run. Earlier on 2026-11-16 Greg ruled one forecast per trade day for the ROOT stage, the last made before the
   trade day opens (`SPEC-root.md`, section G). "Keep everything as it was" came after. Which is it: every run as it
   arrives, or the one forecast made before the open?
2. **Which day the forecast describes (X02, X09).** Fix 3 moves the observed temperature to the gas day ending
   10 am Eastern. The forecast in the original describes the calendar date. Left as it was, forecast and observed
   describe different days. Is the forecast moved to the same gas day, or left as it was?
3. **The details of fix 3 (X10).** Three things were not said: whether degree days come from the mean of the day's
   hourly readings or are counted hour by hour; what the wind column is; and how many earlier gas days the carry-over
   covers.
4. **A workbook of the point tables now.** Yes or no: a small workbook with one sheet per point, so the 13 can be
   seen before the tick rows exist, separate from the four trade-day sheets.
