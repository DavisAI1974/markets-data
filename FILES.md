# ROOT stored rows: trade day Tue Oct 17, 2023 (6 pm Eastern the evening before to 5 pm Eastern)

Built by the new ROOT (Markets branch `claude/root-session6-017eY1`, commit `b39e10a`) from the raw order tape
and the made outside tables in markets-data branch `ccr-349e2ffe-07p8od`. Nothing here comes from an old run.

- Rows: 846,158 (one per tick), 217 fields each. Sections A to E from the tape and the book, section G the 13 outside data points.
- Rows by label: 5 pm to 6 pm stretch 912, trade day 845,246.
- Book pictures: one at each of 33,703 trade messages, one at the first written row and one at the last (42,506,828 order lines).
- Only rows labelled "trade day" enter a calculation. The stretch and start-up rows are kept and marked; nothing is calculated on them.
- An empty field is stored as empty (null): never 0, never blank text. A line that a tick emptied is the words "no orders".
- Checks in `RECEIPT.json`, all passed: every record accounted for; the trade day cut; the book equals the vendor restatement; the book adds up at every trade; one history per order; the trade count; the outside points pinned right on every row and every section G column.
- `playback-*.json` is the playback record (four cuts, all identical). It was made on the first build of this session (Markets `fca77bb`), before the emptied line was changed from a blank cell to the words "no orders". That change touches one text cell and was not run through playback again (one check per changed part).
- Part 2, Step 1, laid out and approved by Greg 2026-11-16 (`STEP1_STEP2_LAYOUTS.md`; Markets `6a468af`). The rows files are untouched; each calculation's output is its own files.
  - `flow_peak` (piece 1, the flow and the exhaustion peak): `calc-flow_peak-20231017-part*.parquet`, one file beside each rows file, in the same row order, with the position on the tape and 12 columns. 8,619 peaks became known in the trade day.
  - `peak_story` (piece 2, what each peak did before and after; no fixed marks, no names for kinds of peak): `calc-peak_story-facts-20231017-part*.parquet`, one line per fact, each with the tick at which it became known and the peak it is about: 53,106 facts (8,619 build-up, 30,453 new low, 5,416 reached zero, 5,415 came back, 3,203 beaten); `calc-peak_story-20231017-part*.parquet`, the number of facts known on each row; `calc-peak_story-open-at-the-end-20231017-part000.parquet`, the 1 peaks whose story had not ended at the last tick.
  - Checks, in `CALC-flow_peak-20231017.json` and `CALC-peak_story-20231017.json`, all passed: every column and every fact worked out again from the stored rows by a different method and equal; playback equal at two cuts each. Rows of no trade day hold empty cells.
- Part 2, Step 2, pieces C and I (the quote's own runs), approved by Greg 2026-11-16 (`STEP2_PLAN.md`; Markets `9612f87`). They read the stored rows through the rows gate, which passed exactly the ticks of the tape gate. The rows files are untouched.
  - `book_totals` (piece C, the book running totals): `calc-book_totals-20231017-part*.parquet`, one file beside each rows file, in the same row order, with the position on the tape and 24 columns: for the bid side and the ask side, size added, pulled, filled and moved since the first tick of the trade day, each for the whole side and at the best price, the size put back on orders as they traded (`refilled`), and the filled size whose fill message the tape gives no side for. At the last tick: bid added 466,967, pulled 431,411, filled 34,830, moved 83,280; ask added 387,389, pulled 348,961, filled 37,952, moved 28,451.
  - `quote_runs` (piece I, first part: the runs of the best bid and of the best ask, followed separately; no minimum length or size): `calc-quote_runs-facts-20231017-part*.parquet`, one line per fact, each with the tick at which it became known and the run it is about: 67,295 facts (14,813 runs of the best bid, 13,864 of the best ask; run started, new furthest price, first step back); `calc-quote_runs-20231017-part*.parquet`, the run in progress on each side on every row and the number of facts known there; `calc-quote_runs-open-at-the-end-20231017-part000.parquet`, the 2 runs still going at the last tick.
  - Checks, in `CALC-book_totals-20231017.json` and `CALC-quote_runs-20231017.json`, all passed. Book totals: every column worked out again from whole columns by a different method and equal; on every row each side's total size equals its size at the open plus added minus pulled minus filled; the size filled equals the size of the tape's fill messages (72,782); playback equal at two cuts, one inside an exchange event between a fill message and the row where the book shows it. Quote runs: every fact found again from the foundation's marks of a best price moving (the calculation reads only the best-price columns) and equal; playback equal at two cuts, one on a tick that ends one run and starts the next. Rows of no trade day hold empty cells.

| File | Bytes | SHA256 |
|---|---:|---|
| `CALC-book_totals-20231017.json` | 8,276 | `ad21e7706edd35de0feabba1f5cc6d27b83e09d90db7404be85eb61218a0dd6c` |
| `CALC-flow_peak-20231017.json` | 4,489 | `41d09932c74f8dcb940eb3dddc31e11e395ff604a65f14843bf0adaf2abdb83b` |
| `CALC-peak_story-20231017.json` | 4,199 | `69d5d54919061c4b4177cb3f1b1d2db6fa5872b3e95c172cb802877dffed3801` |
| `CALC-quote_runs-20231017.json` | 6,407 | `6c9109c7e6d80593b24064d2c5ce1d127d3dfe01458753bd0289834f7c3346a3` |
| `RECEIPT.json` | 8,902 | `4ec88893c09030330ff0e7a9f9b9bd2032e074e251286115af324acd1f8031b0` |
| `book-pictures-20231017-part000.parquet` | 11,957,324 | `b029cda92bb6d4d90b1c2d1538205f16dd2aba00111e3d956dd594b07b8e9cf1` |
| `book-pictures-20231017-part001.parquet` | 12,710,758 | `96a4d6c711cb2ec4c0a17df8411aa928e80cb488e127d90509356588bb008070` |
| `book-pictures-20231017-part002.parquet` | 12,933,911 | `c1a33bfc8819448e998bac25abb5cb5fcc4272ed0984cd0310d603da8862b64e` |
| `book-pictures-20231017-part003.parquet` | 12,353,609 | `9d662bea92b1be4caa65c2f039f1b486bcb03dd30c708143202540e632bd55ee` |
| `book-pictures-20231017-part004.parquet` | 12,683,155 | `e4350b21485cca996059e5853fb9e2d392c66a1078cdc04cd48c3fdd4b523928` |
| `book-pictures-20231017-part005.parquet` | 12,732,973 | `de30b4b8c5b59b46175fbfef782e521f61335ca74198d04da5f6f790bc2641ea` |
| `book-pictures-20231017-part006.parquet` | 11,635,603 | `50b0ce1867b9bd8e0920a48d5f1322d2a22c54f2abd8faef01d58b667bfdc187` |
| `book-pictures-20231017-part007.parquet` | 12,600,363 | `917bd7aa6dcef7bb8788879cc6067ea8689cfb6697a6f4b68533fc27198dda3d` |
| `book-pictures-20231017-part008.parquet` | 11,899,351 | `dd7e83b147f82bde0e90070a45c93ade780f6e4d120b808858d65e929b8da80f` |
| `book-pictures-20231017-part009.parquet` | 12,275,903 | `426b05a05e76c813e859eb49a081b86a43abe2d78f1a897da675d733c11b58a8` |
| `book-pictures-20231017-part010.parquet` | 1,335,158 | `ab39063c15ae0de108b36a1667483902fcea0a3a8f4257ba395be70e05bb6d73` |
| `calc-book_totals-20231017-part000.parquet` | 2,070,817 | `efec8fa67265c32615eadcde1666ab674c0eba4a543fd5cf8c6cafbe2a78cfae` |
| `calc-book_totals-20231017-part001.parquet` | 2,257,574 | `ddc5f541e7381d120af8c49d42db4aa54ba7827de905081ab3e549ba2f3d3218` |
| `calc-book_totals-20231017-part002.parquet` | 2,257,307 | `b1f01f0749c7400fabe8e49bfd79b57a92b2360df7ee0a5cd4617e1cfda5943c` |
| `calc-book_totals-20231017-part003.parquet` | 534,907 | `6d25142e4f9c4471dac0504ccea0bc7b7a8b44cd972f58a796285c2c76348404` |
| `calc-flow_peak-20231017-part000.parquet` | 813,379 | `4de40f4e7e6856ed4af46a11bb4ca3f8e7aa3d26db73ba25fa66917c9ae1627f` |
| `calc-flow_peak-20231017-part001.parquet` | 835,113 | `bffa6bb47e4c3abcb30c3ccc399a2ecd7e6e529fcc530860aa79b73dec720d65` |
| `calc-flow_peak-20231017-part002.parquet` | 863,914 | `be9ce16a972a43daffe3759e5ec3f0125580c0d13b2c2a9bc98d07efcbb8701b` |
| `calc-flow_peak-20231017-part003.parquet` | 252,366 | `885ad4fe4806847aadd93664b550ee82cbf4dff933d402eec663f76ae521e808` |
| `calc-peak_story-20231017-part000.parquet` | 541,475 | `b714419ae72d3e6c4efaa542dab1f40c110638295572270bac6f152a062a4049` |
| `calc-peak_story-20231017-part001.parquet` | 542,945 | `11df9b06ae9b664bad7e06a12d5ef76b44dc32c0927caf3e14d37d8f4811959c` |
| `calc-peak_story-20231017-part002.parquet` | 544,446 | `3357e08dbc030f7b105bf98a605ca46ba0acf50f8e67daf9514e1e6615767595` |
| `calc-peak_story-20231017-part003.parquet` | 178,194 | `52576e840f333ce9a98f96979e969cda31652299b4f9200090474ff73b8f065a` |
| `calc-peak_story-facts-20231017-part000.parquet` | 1,474,998 | `064f007725b82161aaecd46db29161fa148860ff919742785ea8cdd576822ad8` |
| `calc-peak_story-open-at-the-end-20231017-part000.parquet` | 1,110 | `c1f2082ec94a9a7575aa30d1e0c72f5f76a4e153bad64aa9ab24468c794071f0` |
| `calc-quote_runs-20231017-part000.parquet` | 2,952,347 | `c45306a7bdee6e3007fe16850ea5355c0fd4346e1cfff9165291f8897d5e39d2` |
| `calc-quote_runs-20231017-part001.parquet` | 2,854,193 | `743d9c7347d16eb2f370d730806eb3be96ef7f2d3a7de5ce1a11637bdd97caf1` |
| `calc-quote_runs-20231017-part002.parquet` | 2,854,428 | `612b6b7b45221a4545e801a34a716cd2f678c0b6d34a9cb8e5ac9407dbb77606` |
| `calc-quote_runs-20231017-part003.parquet` | 787,230 | `f7fd36d370ef3cdc7d367752272cb5735bc3338baf81a87815efb37d21e7e344` |
| `calc-quote_runs-facts-20231017-part000.parquet` | 1,544,974 | `8afeaf21a2d6350c431b52fd397d26307fa0c2a6dd74f79bd3da70bb028e3e28` |
| `calc-quote_runs-open-at-the-end-20231017-part000.parquet` | 2,027 | `f8583bd9f5a0d54e11a334af66f6fd576346bea2afb5864a6cfa49967e2e6c84` |
| `playback-20231017.json` | 665 | `730534ef97f7ba68f7b3ca9e381ae0723fc360e787b16956ac03927e5aa4177d` |
| `rows-20231017-part000.parquet` | 19,729,598 | `7c1559d5056070a4b91ffd4f7cf2928d1034a54fde3cb3a4e518438372416595` |
| `rows-20231017-part001.parquet` | 20,226,095 | `a30f8b597209bd74a81ec426f678699e61a341099a1b66a9fa6e35299a7057f0` |
| `rows-20231017-part002.parquet` | 20,215,925 | `b1c9b234966d8874d4fec39567dbd483f47da3205209d03ccf57ca065722a36a` |
| `rows-20231017-part003.parquet` | 4,808,580 | `efb7d6338879f8ad53224a307a882f4562cc5aafa797faf3a4ef07ef80c32313` |
| `vendor-restatements-20231017.parquet` | 25,152 | `839562be094b57fb8d241d5df378fa377727cfc6bd72906d080805aafb7840bd` |
