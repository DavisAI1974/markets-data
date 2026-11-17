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
- Part 2, Step 2, pieces A and B, approved by Greg 2026-11-16 (`STEP2_PLAN.md`; Markets `899f1b8`). Run on a Runpod pod, one trade day per pod, the four at the same time, on his go; every file here was fetched from the pod and compared with the fingerprint in its receipt. The rows files are untouched.
  - `peak_links` (piece A, the links between peaks, as facts, with no letters and no depth): `calc-peak_links-facts-20231017-part*.parquet`, one line per fact, each with the tick at which it became known and the peak it is about: 17,237 facts. At the tick a peak becomes known: the last peak before it on its own side and on the other side (the tick of its high, the time between the two highs, the price at its high, whether its story was still open) and the peak before, same side or not. At the tick a story ends: how many later peaks became known while it was open, and the first of them. Of 8,619 peaks, the peak before was on the same side for 6,176 and on the other side for 2,442; 5,343 became known while the peak before was still open; the most later peaks inside one story was 55. `calc-peak_links-20231017-part*.parquet`, the number of facts known on each row; `calc-peak_links-open-at-the-end-20231017-part000.parquet`, the 1 peaks whose story had not ended at the last tick.
  - `open_stories` (piece B, the state at each tick): `calc-open_stories-20231017-part*.parquet`, one file beside each rows file, in the same row order, with the position on the tape and 10 columns: for buy peaks and for sell peaks, how many stories are open, how many of those have reached zero and not come back, and the tick of the high of the oldest, the newest and the largest open one. The most open at one tick: 20 buy, 19 sell.
  - Checks, in `CALC-peak_links-20231017.json` and `CALC-open_stories-20231017.json`, all passed: every link and every column worked out again from the stored outputs of pieces 1 and 2 as whole tables and equal; playback equal at two cuts each. Rows of no trade day hold empty cells.
- Part 2, additions L and M and the first part of the chain link models, approved by Greg 2026-11-16 ("Try them all"; "Do it"; `STEP1_STEP2_LAYOUTS.md`). Run on a Runpod pod 2026-11-16 evening Eastern, one trade day per pod, the four at the same time, each calculation its own helper pinned to its own CPU, on his go ("Approve"); every file here was fetched from the pod and compared with the fingerprint in its receipt before it was stored. The rows files are untouched.
  - `refills` (addition L, orders traded against with size put back; Markets `b8b720c`): `calc-refills-facts-20231017-part*.parquet`, one line per fact at the tick of the order's own row: 1,522 facts, 1,440 with size put back, 1,262 of them leaving the order the same size or larger; 357 orders, at most 99 times on one order. Size put back: bid 1,801, ask 1,406, equal to the `refilled` totals of the stored book totals. `calc-refills-20231017-part*.parquet` holds the count of facts known on each row.
  - `sweeps` (addition M, every trade event and the quote touching or crossing; Markets `5f49e4d`): `calc-sweeps-facts-20231017-part*.parquet`, one line per fact: 32,728 trade events (1,398 with no fill message, 24 with more than one trade side, at most 6 price levels filled in one event); the quote touched or crossed 553 times (1,886 ticks), none standing at the last tick. It was run twice: the first run's receipt counted the touch facts 33 times over (the facts themselves were right); only the corrected run is stored.
  - `chain_peaks` (the chain link models, first part: what each peak did, and the ended peaks before it; Markets `b8b720c`): `calc-chain_peaks-facts-20231017-part*.parquet`, one line per peak at the tick its story ended: 8,618 peak lines (5,415 came back, 3,203 beaten; 1 still open at the last tick, listed in `calc-chain_peaks-open-at-the-end-*`). `calc-chain_peaks-before-20231017-part*.parquet`, one line per step back at the tick a peak became known: 51,687 lines, six steps written out (7 peak lines had fewer than six ended peaks before them). Empty cells: no low for the rise on 32 lines, no trade between the high and the end on 148, no peak before on 1. It holds no model.
  - Checks, in `CALC-refills-20231017.json`, `CALC-sweeps-20231017.json` and `CALC-chain_peaks-20231017.json`, all passed on the first run of each: every fact and line worked out again by a different method and equal; playback equal at two cuts (three for sweeps), each cut where something was still unfolding. Rows of no trade day hold empty cells.
- The chain link models, second part (Step 1 piece 4; approved by Greg 2026-11-16: "Let it produce full values", "Do it"; Markets `1a0e073`, `root/chain_models.py`). Run on the same pod, on helpers pinned one to a CPU, one thread each. **These values are NOT known at any tick:** this trade day's peaks were scored by ridge, nearest neighbours and extra trees taught on the OTHER three trade days (2023-10-02, 2023-10-03, 2023-10-18), some of them later. They are kept in their own table and are never put on a tick row. It is a model score by his decision, kept per peak.
  - `chain-models-20231017-part*.parquet`: one line per peak, model and step back (1 to 6), 155,142 lines: each of the ten figures' own squared error without and with the ended peak at that step, the mean over the ten beside them, and the gain. Peaks scored at steps 1 to 6: 8,542, 8,510, 8,478, 8,441, 8,414, 8,381. A line that is not scored has empty values and the reason (fewer ended peaks before it than the step; an empty figure on the peak or on one of the peaks before it; story still open at the last tick).
  - Checks, in `CHAIN-MODELS-20231017.json`, passed: every peak given to a model had a story that ended at or before the tick its target became known (215,974 inputs looked at, over all four trade days); ridge worked out again in closed form agrees with the library. Nearest neighbours and extra trees have no independent recount. Libraries: scikit-learn 1.9.1, numpy 2.5.5, Python 3.12.16.

| File | Bytes | SHA256 |
|---|---:|---|
| `CALC-book_totals-20231017.json` | 8,276 | `ad21e7706edd35de0feabba1f5cc6d27b83e09d90db7404be85eb61218a0dd6c` |
| `CALC-chain_peaks-20231017.json` | 5,587 | `08534c70cfbe5ce838b77673b89e8f21ae361d34ca98a20926a6d494c3253d94` |
| `CALC-flow_peak-20231017.json` | 4,489 | `41d09932c74f8dcb940eb3dddc31e11e395ff604a65f14843bf0adaf2abdb83b` |
| `CALC-open_stories-20231017.json` | 4,168 | `7aacee61855532684c2655b2f028b86708d45d5816f72b9dc1a22b1ef1b5ca04` |
| `CALC-peak_links-20231017.json` | 4,354 | `364eb62a531bc7793d9c74272be88f3fbf41b8b8ff9a4fffcee559f6716e77c9` |
| `CALC-peak_story-20231017.json` | 4,199 | `69d5d54919061c4b4177cb3f1b1d2db6fa5872b3e95c172cb802877dffed3801` |
| `CALC-quote_runs-20231017.json` | 6,407 | `6c9109c7e6d80593b24064d2c5ce1d127d3dfe01458753bd0289834f7c3346a3` |
| `CALC-refills-20231017.json` | 4,659 | `d2788f91c2edad0da0445984505f3f47a8c75d8cf54a404ec38ac14531480a5d` |
| `CALC-sweeps-20231017.json` | 5,356 | `d82d9040f1b9a87db7d5a672eeddc1ff2ff183c43050c91ff9df752b40ea6e1c` |
| `CHAIN-MODELS-20231017.json` | 41,720 | `95ccbfb438d8f6a558699513f84f6aeed3643e0568fd717ba6b2840c6d4f1bf4` |
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
| `calc-chain_peaks-20231017-part000.parquet` | 540,444 | `ee3caa7e6a689809ca052a7b1f16d9364500bceb79d09d6a78b8cf28644372d4` |
| `calc-chain_peaks-20231017-part001.parquet` | 539,700 | `ef29589643969f8dda5f041aa2a0e5bae3a1c5570e233db0d2cdb0809c9bbca0` |
| `calc-chain_peaks-20231017-part002.parquet` | 540,459 | `ec7956718ac08d7cde4aaf64d3e38f385ab5cf12035e63bc251ae82cacc58464` |
| `calc-chain_peaks-20231017-part003.parquet` | 178,205 | `137c295261543b0dd47f5d713b858c88a8c81b0580b978a8a7170b56f80a06a2` |
| `calc-chain_peaks-before-20231017-part000.parquet` | 413,043 | `f94db93e54581861ae05cf94d045a8e031d136ab247c2495c5cc81c9d89b843f` |
| `calc-chain_peaks-facts-20231017-part000.parquet` | 550,551 | `ccf04bd95b3362fc7394b9f7e21bb2edd19031ee91fd92031b81ae610d6cad48` |
| `calc-chain_peaks-open-at-the-end-20231017-part000.parquet` | 885 | `3c240692c5d20ef50059dc7d960cf8f907b57dc66f1a333863555076c4467803` |
| `calc-flow_peak-20231017-part000.parquet` | 813,379 | `4de40f4e7e6856ed4af46a11bb4ca3f8e7aa3d26db73ba25fa66917c9ae1627f` |
| `calc-flow_peak-20231017-part001.parquet` | 835,113 | `bffa6bb47e4c3abcb30c3ccc399a2ecd7e6e529fcc530860aa79b73dec720d65` |
| `calc-flow_peak-20231017-part002.parquet` | 863,914 | `be9ce16a972a43daffe3759e5ec3f0125580c0d13b2c2a9bc98d07efcbb8701b` |
| `calc-flow_peak-20231017-part003.parquet` | 252,366 | `885ad4fe4806847aadd93664b550ee82cbf4dff933d402eec663f76ae521e808` |
| `calc-open_stories-20231017-part000.parquet` | 615,807 | `4f35684f6a1615ab2cb716463120e64396720e789a04752974228d54cc0e6f3e` |
| `calc-open_stories-20231017-part001.parquet` | 599,461 | `4d216c6eeef0e1a7046dc1603a1de426c7c2804748b9e9f80904224c5ebac935` |
| `calc-open_stories-20231017-part002.parquet` | 604,288 | `e45ef3aebf07ab27d5428b3694bb8f239379f80cf3b72b5434f14194dd166eb8` |
| `calc-open_stories-20231017-part003.parquet` | 199,436 | `35668c6254d37fe939b7c047dbff27435d093d03ea46ed531c8ed36f68d669e5` |
| `calc-peak_links-20231017-part000.parquet` | 537,361 | `149b39edeb2d29458384d84986a1cc2d74b1e22a893fd651872f6c26802efb96` |
| `calc-peak_links-20231017-part001.parquet` | 536,926 | `31bf9dbdc9fcb8520343d53b3f005ccdf12770d192a6cf41cf3a4f529c6dec80` |
| `calc-peak_links-20231017-part002.parquet` | 537,485 | `b73c288161b1a165d94555a30ffae97b3788ed10bb3e0100ac98f3708491f200` |
| `calc-peak_links-20231017-part003.parquet` | 177,173 | `70cfdf30a0af25974dde29735210467c4a01764d29ab83ba47d4a1117efc22a3` |
| `calc-peak_links-facts-20231017-part000.parquet` | 475,863 | `61ff6772dbfd361fa930819ad8d455636853fbf3ab96e114d70b9e3afbd3fcff` |
| `calc-peak_links-open-at-the-end-20231017-part000.parquet` | 1,148 | `3ef15b002297b096925c738447e3f5835ffe466f1ceb5c54efa12737cbee91b6` |
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
| `calc-refills-20231017-part000.parquet` | 528,518 | `1be7f81ebe5843a06af5ac5f4c66bf9091760af3395542a8ce8b72a093404805` |
| `calc-refills-20231017-part001.parquet` | 529,099 | `a4d72fa01fb0f498c08edea6a5ecca24c72c893b0c92f81a51ab17564ed028b3` |
| `calc-refills-20231017-part002.parquet` | 529,169 | `c1c19a18f1bb2b9af92ba4f93fa5f9962e86655319c682d8ef0bad9fd6dc8a20` |
| `calc-refills-20231017-part003.parquet` | 175,199 | `c9eb2f114c98038961d2677110a35ca51a515523eda459729e16069ee79f54b5` |
| `calc-refills-facts-20231017-part000.parquet` | 38,723 | `6c6e6c89f3bb80719ce45ac2fe09e892518a23577910825e20ae4cd5b6903e7e` |
| `calc-sweeps-20231017-part000.parquet` | 540,735 | `a4fb6dfe701716a1e0e652718219542cb7b12816a1bd3985c7427dae3f03fe6d` |
| `calc-sweeps-20231017-part001.parquet` | 542,246 | `2f70980fb4ea655718c4eff03d8892b8bec28395cb049994a8c971ef80afcdfd` |
| `calc-sweeps-20231017-part002.parquet` | 543,209 | `4e95f10bafd7162fb5568968b85d7839c903b5eb2ec79e9520440727a7d421bd` |
| `calc-sweeps-20231017-part003.parquet` | 178,278 | `e9260983388287b20888a530c32b9ace930ca1f34068886e59f6eefe14446f30` |
| `calc-sweeps-facts-20231017-part000.parquet` | 1,174,208 | `fb37cae11e510badcee746c7d7891a5494045cee5097f9290f52313c11eb58dd` |
| `calc-sweeps-open-at-the-end-20231017-part000.parquet` | 734 | `686f3712d423508eaf008134ba74805b62b07249acf3c63d533a38374b048ab2` |
| `chain-models-20231017-part000.parquet` | 27,593,519 | `c1f08e341c7e2751a54f64e43806e24cf5e6f4e886ebf9df38ae9e83568ed0cc` |
| `playback-20231017.json` | 665 | `730534ef97f7ba68f7b3ca9e381ae0723fc360e787b16956ac03927e5aa4177d` |
| `rows-20231017-part000.parquet` | 19,729,598 | `7c1559d5056070a4b91ffd4f7cf2928d1034a54fde3cb3a4e518438372416595` |
| `rows-20231017-part001.parquet` | 20,226,095 | `a30f8b597209bd74a81ec426f678699e61a341099a1b66a9fa6e35299a7057f0` |
| `rows-20231017-part002.parquet` | 20,215,925 | `b1c9b234966d8874d4fec39567dbd483f47da3205209d03ccf57ca065722a36a` |
| `rows-20231017-part003.parquet` | 4,808,580 | `efb7d6338879f8ad53224a307a882f4562cc5aafa797faf3a4ef07ef80c32313` |
| `vendor-restatements-20231017.parquet` | 25,152 | `839562be094b57fb8d241d5df378fa377727cfc6bd72906d080805aafb7840bd` |
