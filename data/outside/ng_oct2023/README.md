# Outside data for the four trade days: the published source files

Fetched 2026-11-16 from the original public sources, for trade days Mon Oct 2, Tue Oct 3, Tue Oct 17 and Wed Oct 18,
2023 (a trade day runs 6 pm Eastern the evening before to 5 pm Eastern on the named date).

**These are source files exactly as served. No value in this folder is calculated.** The 13 outside data points are
made from them in a later step (the `outside` part of ROOT), which has its own short specification and is not built
yet.

- `MANIFEST.json`: for every file, the address requested, when it was retrieved, the bytes and SHA256 as served, the
  check it passed, and where it is stored. Large text files are stored as a gzip of the bytes as served (written with
  no time stamp inside, so the same bytes give the same file).
- `fetch_sources.py`: the program that fetched them. It downloads and checks; it does not parse or calculate.
- `pull_curve.py`: the program that pulled the futures-curve files from Databento (it quotes first, refuses above a
  ceiling, and never buys a file twice). The key is not in it.
- `fetch_eia_api.py`: the program that fetched from the EIA data service. The key is read from the environment and is
  never stored; a response containing it would be refused.
- `raw/`: the files, 142 in all, about 48 MB.

Every file is the source's revision as of the retrieval date. Where a source keeps only revised figures, the figure as
first published cannot come from it; that is said below.

## What is held, by outside data point

| Points | What | Files held | Read and confirmed |
|---|---|---|---|
| X01, X03, X04, X08 | positioning | `raw/cot/`: the CFTC yearly files 2020 to 2023 | The NYMEX gas contract (023651) and four ICE gas contracts (023391, 023392, 0233AG, 0233AH) are present every week, including the reports dated Sep 19 to Oct 24, 2023. |
| X02, X09 | forecast temperature; disagreement between models | `raw/mos/`: three forecast products (GFS, NAM, extended GFS) for 16 stations, every run made Sep 20 to Oct 19, 2023 | Every station has every run on the clock days checked: GFS four a day, NAM two, extended GFS two. |
| X10 | observed weather | `raw/weather_obs/`: every reading for 18 stations (the 16 weighted cities, plus Austin and San Antonio, whose hourly temperatures the original files also carried), Sep 1 to Oct 31, 2023, all report types and all fields, the raw station message included. Beside each, a second file with the routine hourly reports only, so the routine reading of each hour is identified by the source. | Each of the 16 first fetched has at least 23 readings with a temperature on each clock day checked. Each routine-only file has about one row per hour (1,464 hours in the span). NYC (Central Park) reports hourly only; the others also have 5-minute reports, which carry no parsed temperature. |
| X05, X07 | wind; gas burned for power | `raw/eia930/api/`: from the EIA data service, hourly generation by fuel and hourly demand for US48 and six regions (ERCO, CISO, MISO, PJM, SWPP, SOCO), every hour from Sep 23 to Oct 19, 2023 (UTC). This is the EIA's own US48 figure, as the original files used. Also `raw/eia930/EIA930_BALANCE_2023_Jul_Dec.csv.gz`, the EIA's bulk file with all 62 balancing authorities. | US48 has all 24 hours with a wind and a gas figure on each of the six UTC clock days that touch the four trade days. |
| X11 | weekly storage | `raw/storage/`: the EIA history, the EIA's own file of original estimates (`revisions.xls`), and the weekly series from the EIA data service since Sep 2017 (`raw/storage/api/`, the current revised history) | The weeks ending Sep 22 to Oct 27, 2023 are present in both. `revisions.xls` holds the storage LEVEL of each week as estimated before any revision, with the EIA's note where a week was later changed (checked on the week ending Jan 20, 2023: 2,729 there, 2,734 in the history). The weekly change and the five-year comparison exactly as printed in each report are not in it (see below). |
| X13 | the futures curve | `raw/curve/`: from Databento, every natural gas contract month (`NG.FUT`), one native file per UTC clock day: contract definitions, exchange statistics, and every trade of every month. UTC clock days Sep 29, Oct 1 to 3 and Oct 16 to 18, 2023 (Sep 30, a Saturday, was requested for definitions and statistics and holds no records). Cost $0.80. | Each definitions file lists 146 outright contract months plus the calendar spreads. Each statistics file holds settlement-price records (2,066 to 4,064 a clock day) and open interest. The trades files hold 897 (Sunday evening) to 128,776 trades a clock day. The full order tape of the other contract months was quoted at $4.83 and not bought (Greg: "if we decide we need it we can buy it later"). |
| X06 | sessions since the front contract expired | nothing to fetch | It comes from the exchange calendar. |

## Not held yet, and why

| Points | What is missing | Reason |
|---|---|---|
| X12 | the street estimate of each storage figure before it was released | It was read from saved copies of two web pages on the Internet Archive (`web.archive.org`). That site is not allowed from the cloud environment. |
| X11 | the weekly change and the five-year comparison exactly as printed in each report | The EIA's files give the level before revision, region by region. The change and the five-year figures as printed were on the report page of that week, which the EIA does not keep; saved copies are on the Internet Archive. Whether they are taken from there or worked out from the levels is decided in the `outside` specification. |
| X01, X03, X04, X08 | the time each October 2023 report was published | The CFTC's release schedule page as served today lists 2026 only (`raw/cot/cftc_release_schedule.html`). The published time for the 2023 reports needs another source. On the usual weekly timetable (Friday 3:30 pm Eastern, a business day later in a holiday week) no positioning report, and no Thursday storage report, comes out inside any of the four trade days, so this affects the time written beside a value, not which value a row holds. |
| X05, X07 | the grid figures as first published | The EIA keeps the current revision only. |
