# ROOT stored rows: trade day Tue Oct 17, 2023 (6 pm Eastern the evening before to 5 pm Eastern)

Built by the new ROOT (Markets branch `claude/root-session6-017eY1`, commit `b39e10a`) from the raw order tape
and the made outside tables in markets-data branch `ccr-349e2ffe-07p8od`. Nothing here comes from an old run.

- Rows: 846,158 (one per tick), 408 fields each. Sections A to E from the tape and the book (85 fields), section G the outside data (323 fields; before the rebuild of 2026-11-17 the rows held 217 fields, 132 of them outside).
- Rows by label: 5 pm to 6 pm stretch 912, trade day 845,246.
- Book pictures: one at each of 33,703 trade messages, one at the first written row and one at the last (42,506,828 order lines).
- Only rows labelled "trade day" enter a calculation. The stretch and start-up rows are kept and marked; nothing is calculated on them.
- An empty field is stored as empty (null): never 0, never blank text. A line that a tick emptied is the words "no orders".
- Checks in `RECEIPT.json`, all passed: every record accounted for; the trade day cut; the book equals the vendor restatement; the book adds up at every trade; one history per order; the trade count; the outside points pinned right on every row and every section G column.
- `playback-*.json` is the playback record (four cuts, all identical). It was made on the first build of this session (Markets `fca77bb`), before the emptied line was changed from a blank cell to the words "no orders". That change touches one text cell and was not run through playback again (one check per changed part).
- Part 2, Step 1, laid out and approved by Greg 2026-11-16 (`STEP1_STEP2_LAYOUTS.md`; Markets `6a468af`). The rows files are untouched; each calculation's output is its own files.
  - `flow_peak` (piece 1, the flow and the exhaustion peak): `calc-flow_peak-20231017-part*.parquet`, one file beside each rows file, in the same row order, with the position on the tape and 11 columns (12 until 2026-11-17, when the ranked column `peak_standing_so_far` was taken out). 8,619 peaks became known in the trade day.
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
- Part 2, the three calculations written in the ninth session and first run in the tenth (Markets `02ffde6`, on a pod; Greg's go 2026-11-17):
  - `quote_peaks` (the rest of piece I: the peaks in play at every turn of a run of the quote): `calc-quote_peaks-20231017-part*.parquet` beside the rows; `calc-quote_peaks-facts-20231017-part*.parquet`, 67,295 facts, one at every turn.
  - `outside_changes` (addition O: what was in play when an outside figure changed): `calc-outside_changes-20231017-part*.parquet`; `calc-outside_changes-facts-20231017-part*.parquet`, 77,306 facts over 108 outside columns followed (14,686 ticks with a change) (these were the figures of the first run; made again on 2026-11-17, see the rebuild below).
  - `together` (addition N: orders that entered or left at the same exchange time): `calc-together-20231017-part*.parquet`; `calc-together-facts-20231017-part*.parquet`, 2 lines in 1 sets that entered together and 32,234 lines in 9,023 sets that left together; `calc-together-open-at-the-end-20231017-part000.parquet`.
  - Checks, in `CALC-quote_peaks-20231017.json`, `CALC-outside_changes-20231017.json` and `CALC-together-20231017.json`, all passed on the first run (a recount by a second method, the playback cuts, the rows gate).
- The missing two hours of the trade legs, 6 pm to 8 pm Eastern (Greg 2026-11-17: "build the missing hrs exactly how we built the current data"; "Then change it ... Finish the data"; Markets `02ffde6` `root/trade_legs.py`, on a pod). The old rule (Markets `0408df44` `price_stretches`, `print_legs`, loaded byte for byte) run over the trade day's trades from 6 pm; only the start changed. The old legs (markets-data `main`, run 42571551209) stay as they are.
  - `trade-legs-6pm-to-8pm-trades-20231017.parquet` (252 trades before 8 pm), `trade-legs-6pm-to-8pm-stretches-20231017.parquet` (113 price stretches holding a trade before 8 pm), `trade-legs-6pm-to-8pm-legs-20231017.parquet` (69 legs holding a trade before 8 pm; the two touching 8 pm are marked, and the one that is the whole of the old cut leg 0 names it). Numbered from 6 pm; the old record numbers from 8 pm.
  - Check, in `TRADE-LEGS-20231017.json`, passed: every one of the 33,451 old trades is the tape's trade at the same place from 8 pm (clocks, price, size, order, side, the time its exchange event was complete) and every one of the 5,591 old legs after the first comes out again with the same trades, direction and price change.
- THE REBUILD of 2026-11-17 (Greg's go; Markets `e083757`, job `rebuild`, one General Purpose 8-CPU pod per trade day; every file fetched and compared with the fingerprint in its receipt before it was stored):
  - The rows were built again with the outside tables as they now stand (markets-data `5eab71f`: hour by hour, no averages, no windows, no ranks). They now carry 323 outside columns (229 new, 38 taken out: the fund standings over 1 and 3 years, the gas-day degree days, the forecast high-low midpoint and the others made from averages). Proved before storing: every one of the 179 columns the old and new rows share (all 85 tape, book and trade columns and the 94 outside columns kept) is equal on every one of the 846,158 rows. The book pictures and the vendor restatement came back byte for byte the same. The build's own checks in `RECEIPT.json` all passed.
  - `flow_peak` was run again only to drop the ranked column `peak_standing_so_far` (a percentile; Greg: "take any ranking system for any data out"). His rule: if the peaks came out differently, keep the old values and only delete the column. Compared before storing: every other column equal to the stored one on every row, so the new files are stored. No peak changed.
  - `outside_changes` was made again beside the rebuilt rows (the one calculation that reads the outside columns): 78,616 facts (14,689 ticks with a change); 319 outside columns followed, 249 of them changed in the trade day. Its checks passed. It replaces the earlier output, which followed the averaged and windowed columns that no longer exist.
  - Every other calculation's output stands as stored. Each was made beside the earlier rows, whose tape, book and trade columns are unchanged (proved above), and none reads an outside column. None was run again (Greg: "No tests except on changed pieces").
  - `playback-20231017.json` was made on the first build and was not run again.

| File | Bytes | SHA256 |
|---|---:|---|
| `CALC-book_totals-20231017.json` | 8,276 | `ad21e7706edd35de0feabba1f5cc6d27b83e09d90db7404be85eb61218a0dd6c` |
| `CALC-chain_peaks-20231017.json` | 5,587 | `08534c70cfbe5ce838b77673b89e8f21ae361d34ca98a20926a6d494c3253d94` |
| `CALC-flow_peak-20231017.json` | 4,281 | `0dfc5cc0b48b36050588884970c403b1d91999c4fbc5c7cd7ca31cdf7cb8ebde` |
| `CALC-open_stories-20231017.json` | 4,168 | `7aacee61855532684c2655b2f028b86708d45d5816f72b9dc1a22b1ef1b5ca04` |
| `CALC-outside_changes-20231017.json` | 20,092 | `d0b500982037f7d96389aa49d3684f6fd2010cb4780aed9cb5bdce848d9160b5` |
| `CALC-peak_links-20231017.json` | 4,354 | `364eb62a531bc7793d9c74272be88f3fbf41b8b8ff9a4fffcee559f6716e77c9` |
| `CALC-peak_story-20231017.json` | 4,199 | `69d5d54919061c4b4177cb3f1b1d2db6fa5872b3e95c172cb802877dffed3801` |
| `CALC-quote_peaks-20231017.json` | 3,959 | `90c9f28cdce9078c98994dadbd899a461ff9e135a0b82d1fd7a433aa17398d1b` |
| `CALC-quote_runs-20231017.json` | 6,407 | `6c9109c7e6d80593b24064d2c5ce1d127d3dfe01458753bd0289834f7c3346a3` |
| `CALC-refills-20231017.json` | 4,659 | `d2788f91c2edad0da0445984505f3f47a8c75d8cf54a404ec38ac14531480a5d` |
| `CALC-sweeps-20231017.json` | 5,356 | `d82d9040f1b9a87db7d5a672eeddc1ff2ff183c43050c91ff9df752b40ea6e1c` |
| `CALC-together-20231017.json` | 4,860 | `1ade81307d0bf62fc84416273ae46ff6d347afb21f8f9551260fe43131d540df` |
| `RECEIPT.json` | 8,291 | `e30e549451de54e20aaf74eb405373bd5d8a476e8fb5b23e22502b46a4dbbe73` |
| `TRADE-LEGS-20231017.json` | 2,246 | `adbfd3d514235f02d93aa580932384c3d328b08aa62318d17ec17243f18df689` |
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
| `calc-flow_peak-20231017-part000.parquet` | 776,718 | `8fdaaa2d234a562defd497b67e7927eca39c631cde96fe9d7a76587d7e257da0` |
| `calc-flow_peak-20231017-part001.parquet` | 800,571 | `3a3bcbdec2fee972280e80d70655212aff54f9a17490a79176bc0a2c4ec49024` |
| `calc-flow_peak-20231017-part002.parquet` | 826,381 | `6ee4c2a82af8e326eb984487a9d3af4c22867ad23e71519204396f1e35f9afd2` |
| `calc-flow_peak-20231017-part003.parquet` | 242,906 | `049fa5730f89f8f0c263778c1db41ce3be7b5b406ebe03990642533b0b97441d` |
| `calc-open_stories-20231017-part000.parquet` | 615,807 | `4f35684f6a1615ab2cb716463120e64396720e789a04752974228d54cc0e6f3e` |
| `calc-open_stories-20231017-part001.parquet` | 599,461 | `4d216c6eeef0e1a7046dc1603a1de426c7c2804748b9e9f80904224c5ebac935` |
| `calc-open_stories-20231017-part002.parquet` | 604,288 | `e45ef3aebf07ab27d5428b3694bb8f239379f80cf3b72b5434f14194dd166eb8` |
| `calc-open_stories-20231017-part003.parquet` | 199,436 | `35668c6254d37fe939b7c047dbff27435d093d03ea46ed531c8ed36f68d669e5` |
| `calc-outside_changes-20231017-part000.parquet` | 539,815 | `2959bef096c5c1a3b7e0b1e032774ef7b6516282a00b5b6652145a4e6f03556c` |
| `calc-outside_changes-20231017-part001.parquet` | 538,145 | `05e997eb8a1b2a8aeecc5c55cec535e5149e96b70785451a34a531036a397d66` |
| `calc-outside_changes-20231017-part002.parquet` | 538,078 | `5f40d1095e05bca130fb98704ee7a42cbad36567d5f51d8892261451de478d97` |
| `calc-outside_changes-20231017-part003.parquet` | 177,379 | `9bbe0e9f1552217549e5a42a29ca6d3590ceabbb1bfc8519159e7ea6c59a17d8` |
| `calc-outside_changes-facts-20231017-part000.parquet` | 1,699,127 | `b3266448f39085de5e8e926019dbc211848b14d737a9141b2a6b5b8c96b83c49` |
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
| `calc-quote_peaks-20231017-part000.parquet` | 547,088 | `ce8fc668ec69d2495c16880fdbdc50e583adc2cc40057fd485fa15baa979df78` |
| `calc-quote_peaks-20231017-part001.parquet` | 543,636 | `4682b39ff7d7885d10e5e9cca1de6cd4e908073bda25cae6a2e077865805d965` |
| `calc-quote_peaks-20231017-part002.parquet` | 544,286 | `2298415ba5cbff6726bff4276a64d598791d683d5f836bf47589e17e42d91b5e` |
| `calc-quote_peaks-20231017-part003.parquet` | 178,548 | `be45dca6c2b3f54bb07d5bbd7aa8155da74ee2edd296ea034417937599aec60b` |
| `calc-quote_peaks-facts-20231017-part000.parquet` | 1,453,053 | `8283d2d92b9706cc0a9033cffb8f8f7353fc7d9ab973a9ef57731ad8c9f0cad2` |
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
| `calc-together-20231017-part000.parquet` | 534,345 | `10ad2cc6f5a9b46243a5bf74be54325e52303abeafa7b2017e7d1fc192f33cf0` |
| `calc-together-20231017-part001.parquet` | 536,387 | `3ce3f607305171c05a066641ff5ad903f2ed680a7a14cde68af910265f54b426` |
| `calc-together-20231017-part002.parquet` | 537,171 | `29d1a89e7ebca6410b28730c4ca6a30cf0529197d671a236f959802cdf2a19d3` |
| `calc-together-20231017-part003.parquet` | 176,842 | `4aa833da60f03f0a4ab86c4bac39c93b4e009ea2fc17932de2e0e117220044f9` |
| `calc-together-facts-20231017-part000.parquet` | 795,028 | `d4d95a27d1d6f49d7d3f557f3ff0ddd6ef8f9f0499cd1b1644772646d557e639` |
| `calc-together-open-at-the-end-20231017-part000.parquet` | 909 | `dbcf236a733ec98b017da71b00ce46f057e8562e197ab6f62d9c7d4dadc6012a` |
| `playback-20231017.json` | 665 | `730534ef97f7ba68f7b3ca9e381ae0723fc360e787b16956ac03927e5aa4177d` |
| `rows-20231017-part000.parquet` | 19,973,753 | `129af2a47cbce9921f21ca5051c75435f7961eb2138ed76865d7f25bd2b0718a` |
| `rows-20231017-part001.parquet` | 20,463,874 | `e605e5ca15822068c2c0863adb7c21ff3cf2fc60ef0163a6231f6fcb3bea1803` |
| `rows-20231017-part002.parquet` | 20,456,125 | `88daf42ead9133913a71c643751e75e400e6acf638f8ec2c4b8a541761e38a29` |
| `rows-20231017-part003.parquet` | 4,899,564 | `1c5b5ec098d3da4043473fabed84b29647095b7204c1657a4fca8d533b69813b` |
| `trade-legs-6pm-to-8pm-legs-20231017.parquet` | 14,740 | `576a1e698538f064fe16fa1cff1e0188f1ea052abd96e72e316094b1baae8be7` |
| `trade-legs-6pm-to-8pm-stretches-20231017.parquet` | 4,561 | `9333247b507b59ec381b28a8a1121c81b19723a241f211c52f655673595befcd` |
| `trade-legs-6pm-to-8pm-trades-20231017.parquet` | 12,914 | `c1353119145c28deb27d1ba4d98ad8f950bd2da77bc3266714f69d130c39fb54` |
| `vendor-restatements-20231017.parquet` | 25,152 | `839562be094b57fb8d241d5df378fa377727cfc6bd72906d080805aafb7840bd` |
