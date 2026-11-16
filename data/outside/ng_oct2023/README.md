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
- `raw/`: the files, 84 in all, about 30 MB.

Every file is the source's revision as of the retrieval date. Where a source keeps only revised figures, the figure as
first published cannot come from it; that is said below.

## What is held, by outside data point

| Points | What | Files held | Read and confirmed |
|---|---|---|---|
| X01, X03, X04, X08 | positioning | `raw/cot/`: the CFTC yearly files 2020 to 2023 | The NYMEX gas contract (023651) and four ICE gas contracts (023391, 023392, 0233AG, 0233AH) are present every week, including the reports dated Sep 19 to Oct 24, 2023. |
| X02, X09 | forecast temperature; disagreement between models | `raw/mos/`: three forecast products (GFS, NAM, extended GFS) for 16 stations, every run made Sep 20 to Oct 19, 2023 | Every station has every run on the clock days checked: GFS four a day, NAM two, extended GFS two. |
| X10 | observed weather | `raw/weather_obs/`: every reading for the same 16 stations, Sep 1 to Oct 31, 2023, all report types and all fields, the raw station message included | Every station has at least 23 readings with a temperature on each clock day checked. NYC (Central Park) reports hourly only; the others also have 5-minute reports. |
| X05, X07 | wind; gas burned for power | `raw/eia930/`: the EIA hourly grid file for Jul to Dec 2023, 62 balancing authorities | ERCO, CISO, MISO, PJM, SWPP and SOCO are present for every October hour. **There is no US48 row in this file** (see below). |
| X11 | weekly storage | `raw/storage/`: the EIA history, and the EIA's own file of original estimates (`revisions.xls`) | The weeks ending Sep 22 to Oct 27, 2023 are present in both. `revisions.xls` holds the estimate of each week as first released, with a note where a week was later changed. |
| X06 | sessions since the front contract expired | nothing to fetch | It comes from the exchange calendar. |

## Not held yet, and why

| Points | What is missing | Reason |
|---|---|---|
| X12 | the street estimate of each storage figure before it was released | It was read from saved copies of two web pages on the Internet Archive (`web.archive.org`). That site is not allowed from the cloud environment. |
| X13 | the futures curve, every contract month | It comes from Databento (a paid pull). The Databento key saved on the cloud environment has a line break and a date after it, so Databento rejects it. |
| X01, X03, X04, X08 | the time each October 2023 report was published | The CFTC's release schedule page as served today lists 2026 only (`raw/cot/cftc_release_schedule.html`). The published time for the 2023 reports needs another source. |
| X05, X07 | a US48 total | The file holds the 62 balancing authorities, not the national total. The EIA publishes US48 through its data service (`api.eia.gov`, free key). Adding the authorities up ourselves would be a choice, and it is not made here. |
| X05, X07 | the grid figures as first published | The EIA keeps the current revision only. |
