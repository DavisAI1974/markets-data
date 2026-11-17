# ROOT stored rows: trade day Mon Oct 2, 2023 (6 pm Eastern the evening before to 5 pm Eastern)

Built by the new ROOT (Markets branch `claude/root-session6-017eY1`, commit `b39e10a`) from the raw order tape
and the made outside tables in markets-data branch `ccr-349e2ffe-07p8od`. Nothing here comes from an old run.

- Rows: 820,670 (one per tick), 217 fields each. Sections A to E from the tape and the book, section G the 13 outside data points.
- Rows by label: 5 pm to 6 pm stretch 544, Sunday start-up 343, trade day 819,783.
- Book pictures: one at each of 38,127 trade messages, one at the first written row and one at the last (47,069,561 order lines).
- Only rows labelled "trade day" enter a calculation. The stretch and start-up rows are kept and marked; nothing is calculated on them.
- An empty field is stored as empty (null): never 0, never blank text. A line that a tick emptied is the words "no orders".
- Checks in `RECEIPT.json`, all passed: every record accounted for; the trade day cut; the book equals the vendor restatement; the book adds up at every trade; one history per order; the trade count; the outside points pinned right on every row and every section G column.
- `playback-*.json` is the playback record (four cuts, all identical). It was made on the first build of this session (Markets `fca77bb`), before the emptied line was changed from a blank cell to the words "no orders". That change touches one text cell and was not run through playback again (one check per changed part).
- Part 2, Step 1, laid out and approved by Greg 2026-11-16 (`STEP1_STEP2_LAYOUTS.md`; Markets `6a468af`). The rows files are untouched; each calculation's output is its own files.
  - `flow_peak` (piece 1, the flow and the exhaustion peak): `calc-flow_peak-20231002-part*.parquet`, one file beside each rows file, in the same row order, with the position on the tape and 12 columns. 9,525 peaks became known in the trade day.
  - `peak_story` (piece 2, what each peak did before and after; no fixed marks, no names for kinds of peak): `calc-peak_story-facts-20231002-part*.parquet`, one line per fact, each with the tick at which it became known and the peak it is about: 58,828 facts (9,525 build-up, 33,833 new low, 5,946 reached zero, 5,945 came back, 3,579 beaten); `calc-peak_story-20231002-part*.parquet`, the number of facts known on each row; `calc-peak_story-open-at-the-end-20231002-part000.parquet`, the 1 peaks whose story had not ended at the last tick.
  - Checks, in `CALC-flow_peak-20231002.json` and `CALC-peak_story-20231002.json`, all passed: every column and every fact worked out again from the stored rows by a different method and equal; playback equal at two cuts each. Rows of no trade day hold empty cells.
- Part 2, Step 2, pieces C and I (the quote's own runs), approved by Greg 2026-11-16 (`STEP2_PLAN.md`; Markets `9612f87`). They read the stored rows through the rows gate, which passed exactly the ticks of the tape gate. The rows files are untouched.
  - `book_totals` (piece C, the book running totals): `calc-book_totals-20231002-part*.parquet`, one file beside each rows file, in the same row order, with the position on the tape and 24 columns: for the bid side and the ask side, size added, pulled, filled and moved since the first tick of the trade day, each for the whole side and at the best price, the size put back on orders as they traded (`refilled`), and the filled size whose fill message the tape gives no side for. At the last tick: bid added 406,585, pulled 363,428, filled 42,718, moved 42,000; ask added 422,692, pulled 379,439, filled 42,970, moved 44,240.
  - `quote_runs` (piece I, first part: the runs of the best bid and of the best ask, followed separately; no minimum length or size): `calc-quote_runs-facts-20231002-part*.parquet`, one line per fact, each with the tick at which it became known and the run it is about: 62,505 facts (13,332 runs of the best bid, 13,680 of the best ask; run started, new furthest price, first step back); `calc-quote_runs-20231002-part*.parquet`, the run in progress on each side on every row and the number of facts known there; `calc-quote_runs-open-at-the-end-20231002-part000.parquet`, the 2 runs still going at the last tick.
  - Checks, in `CALC-book_totals-20231002.json` and `CALC-quote_runs-20231002.json`, all passed. Book totals: every column worked out again from whole columns by a different method and equal; on every row each side's total size equals its size at the open plus added minus pulled minus filled; the size filled equals the size of the tape's fill messages (85,688); playback equal at two cuts, one inside an exchange event between a fill message and the row where the book shows it. Quote runs: every fact found again from the foundation's marks of a best price moving (the calculation reads only the best-price columns) and equal; playback equal at two cuts, one on a tick that ends one run and starts the next. Rows of no trade day hold empty cells.
- Part 2, Step 2, pieces A and B, approved by Greg 2026-11-16 (`STEP2_PLAN.md`; Markets `899f1b8`). Run on a Runpod pod, one trade day per pod, the four at the same time, on his go; every file here was fetched from the pod and compared with the fingerprint in its receipt. The rows files are untouched.
  - `peak_links` (piece A, the links between peaks, as facts, with no letters and no depth): `calc-peak_links-facts-20231002-part*.parquet`, one line per fact, each with the tick at which it became known and the peak it is about: 19,049 facts. At the tick a peak becomes known: the last peak before it on its own side and on the other side (the tick of its high, the time between the two highs, the price at its high, whether its story was still open) and the peak before, same side or not. At the tick a story ends: how many later peaks became known while it was open, and the first of them. Of 9,525 peaks, the peak before was on the same side for 6,862 and on the other side for 2,662; 6,002 became known while the peak before was still open; the most later peaks inside one story was 112. `calc-peak_links-20231002-part*.parquet`, the number of facts known on each row; `calc-peak_links-open-at-the-end-20231002-part000.parquet`, the 1 peaks whose story had not ended at the last tick.
  - `open_stories` (piece B, the state at each tick): `calc-open_stories-20231002-part*.parquet`, one file beside each rows file, in the same row order, with the position on the tape and 10 columns: for buy peaks and for sell peaks, how many stories are open, how many of those have reached zero and not come back, and the tick of the high of the oldest, the newest and the largest open one. The most open at one tick: 21 buy, 24 sell.
  - Checks, in `CALC-peak_links-20231002.json` and `CALC-open_stories-20231002.json`, all passed: every link and every column worked out again from the stored outputs of pieces 1 and 2 as whole tables and equal; playback equal at two cuts each. Rows of no trade day hold empty cells.
- Part 2, additions L and M and the first part of the chain link models, approved by Greg 2026-11-16 ("Try them all"; "Do it"; `STEP1_STEP2_LAYOUTS.md`). Run on a Runpod pod 2026-11-16 evening Eastern, one trade day per pod, the four at the same time, each calculation its own helper pinned to its own CPU, on his go ("Approve"); every file here was fetched from the pod and compared with the fingerprint in its receipt before it was stored. The rows files are untouched.
  - `refills` (addition L, orders traded against with size put back; Markets `b8b720c`): `calc-refills-facts-20231002-part*.parquet`, one line per fact at the tick of the order's own row: 1,860 facts, 1,763 with size put back, 1,575 of them leaving the order the same size or larger; 383 orders, at most 70 times on one order. Size put back: bid 3,053, ask 1,653, equal to the `refilled` totals of the stored book totals. `calc-refills-20231002-part*.parquet` holds the count of facts known on each row.
  - `sweeps` (addition M, every trade event and the quote touching or crossing; Markets `5f49e4d`): `calc-sweeps-facts-20231002-part*.parquet`, one line per fact: 37,238 trade events (1,052 with no fill message, 17 with more than one trade side, at most 13 price levels filled in one event); the quote touched or crossed 587 times (1,858 ticks), once already standing at the first tick of the trade day (marked on its two facts), none standing at the last tick. It was run twice: the first run's receipt counted the touch facts 33 times over (the facts themselves were right); only the corrected run is stored.
  - `chain_peaks` (the chain link models, first part: what each peak did, and the ended peaks before it; Markets `b8b720c`): `calc-chain_peaks-facts-20231002-part*.parquet`, one line per peak at the tick its story ended: 9,524 peak lines (5,945 came back, 3,579 beaten; 1 still open at the last tick, listed in `calc-chain_peaks-open-at-the-end-*`). `calc-chain_peaks-before-20231002-part*.parquet`, one line per step back at the tick a peak became known: 57,114 lines, six steps written out (9 peak lines had fewer than six ended peaks before them). Empty cells: no low for the rise on 42 lines, no trade between the high and the end on 171, no peak before on 1. It holds no model.
  - Checks, in `CALC-refills-20231002.json`, `CALC-sweeps-20231002.json` and `CALC-chain_peaks-20231002.json`, all passed on the first run of each: every fact and line worked out again by a different method and equal; playback equal at two cuts (three for sweeps), each cut where something was still unfolding. Rows of no trade day hold empty cells.
- The chain link models, second part (Step 1 piece 4; approved by Greg 2026-11-16: "Let it produce full values", "Do it"; Markets `1a0e073`, `root/chain_models.py`). Run on the same pod, on helpers pinned one to a CPU, one thread each. **These values are NOT known at any tick:** this trade day's peaks were scored by ridge, nearest neighbours and extra trees taught on the OTHER three trade days (2023-10-03, 2023-10-17, 2023-10-18), some of them later. They are kept in their own table and are never put on a tick row. It is a model score by his decision, kept per peak.
  - `chain-models-20231002-part*.parquet`: one line per peak, model and step back (1 to 6), 171,450 lines: each of the ten figures' own squared error without and with the ended peak at that step, the mean over the ten beside them, and the gain. Peaks scored at steps 1 to 6: 9,430, 9,390, 9,350, 9,314, 9,244, 9,207. A line that is not scored has empty values and the reason (fewer ended peaks before it than the step; an empty figure on the peak or on one of the peaks before it; story still open at the last tick).
  - Checks, in `CHAIN-MODELS-20231002.json`, passed: every peak given to a model had a story that ended at or before the tick its target became known (215,974 inputs looked at, over all four trade days); ridge worked out again in closed form agrees with the library. Nearest neighbours and extra trees have no independent recount. Libraries: scikit-learn 1.9.1, numpy 2.5.5, Python 3.12.16.
- Part 2, the three calculations written in the ninth session and first run in the tenth (Markets `02ffde6`, on a pod; Greg's go 2026-11-17):
  - `quote_peaks` (the rest of piece I: the peaks in play at every turn of a run of the quote): `calc-quote_peaks-20231002-part*.parquet` beside the rows; `calc-quote_peaks-facts-20231002-part*.parquet`, 62,505 facts, one at every turn.
  - `outside_changes` (addition O: what was in play when an outside figure changed): `calc-outside_changes-20231002-part*.parquet`; `calc-outside_changes-facts-20231002-part*.parquet`, 71,986 facts over 108 outside columns followed (13,270 ticks with a change).
  - `together` (addition N: orders that entered or left at the same exchange time): `calc-together-20231002-part*.parquet`; `calc-together-facts-20231002-part*.parquet`, 49 lines in 15 sets that entered together and 33,560 lines in 9,283 sets that left together; `calc-together-open-at-the-end-20231002-part000.parquet`.
  - Checks, in `CALC-quote_peaks-20231002.json`, `CALC-outside_changes-20231002.json` and `CALC-together-20231002.json`, all passed on the first run (a recount by a second method, the playback cuts, the rows gate).
- The missing two hours of the trade legs, 6 pm to 8 pm Eastern (Greg 2026-11-17: "build the missing hrs exactly how we built the current data"; "Then change it ... Finish the data"; Markets `02ffde6` `root/trade_legs.py`, on a pod). The old rule (Markets `0408df44` `price_stretches`, `print_legs`, loaded byte for byte) run over the trade day's trades from 6 pm; only the start changed. The old legs (markets-data `main`, run 42571551209) stay as they are.
  - `trade-legs-6pm-to-8pm-trades-20231002.parquet` (457 trades before 8 pm), `trade-legs-6pm-to-8pm-stretches-20231002.parquet` (278 price stretches holding a trade before 8 pm), `trade-legs-6pm-to-8pm-legs-20231002.parquet` (124 legs holding a trade before 8 pm; the two touching 8 pm are marked, and the one that is the whole of the old cut leg 0 names it). Numbered from 6 pm; the old record numbers from 8 pm.
  - Check, in `TRADE-LEGS-20231002.json`, passed: every one of the 37,670 old trades is the tape's trade at the same place from 8 pm (clocks, price, size, order, side, the time its exchange event was complete) and every one of the 5,995 old legs after the first comes out again with the same trades, direction and price change.

| File | Bytes | SHA256 |
|---|---:|---|
| `CALC-book_totals-20231002.json` | 8,071 | `66b40a2ca3017a57d145cda9209ac7bc5c1b7f8ffe60e9b78703eb34ef88ae0d` |
| `CALC-chain_peaks-20231002.json` | 5,457 | `4b72c65f8b550107bfcc635f4aae45fc5ee0d9f3522751aae3fe611910112c44` |
| `CALC-flow_peak-20231002.json` | 4,359 | `3799b95fd8f25e4b27574c71247ce8a3fcf4bdcfe6de3d2a8d137b47cc914ca2` |
| `CALC-open_stories-20231002.json` | 4,038 | `7530fee1bbc708343b76f5e1145e91816045932af1e64cb7bd187c3f5224ec3d` |
| `CALC-outside_changes-20231002.json` | 8,447 | `0fcb5b881c5f5663cd82e279c2ea464b6223b51b8f8d6cf272a663434b35d2df` |
| `CALC-peak_links-20231002.json` | 4,226 | `c95b23feb44df79d2097b4edb8a14b663ec119c2442fdc1a4f7234ac228f9e38` |
| `CALC-peak_story-20231002.json` | 4,069 | `33041b1c4f2b039c1aa3eb9a027f1ba1a5349016901a5957d7cdbde4a8870635` |
| `CALC-quote_peaks-20231002.json` | 3,828 | `d3d91662b9c8598b8a269ae97647fb44c77f8b67f12e4122c08522d22ed51cce` |
| `CALC-quote_runs-20231002.json` | 6,277 | `4920f30b142a5f22a05064ec02d0ce764545b1078333cbee6e91c37fb41672fb` |
| `CALC-refills-20231002.json` | 4,530 | `d9fedaf01aa4625d3c6adac0861797cda1d0b58fe2a6b4e611b7796bd771d619` |
| `CALC-sweeps-20231002.json` | 5,227 | `15f2bffefe04e3b5636eda6d57c8f3a29ac8fe82ce78d51aa27a1f468b407542` |
| `CALC-together-20231002.json` | 4,737 | `ae03f15e72bae4751ef2d1f06503dfae72716f7323c08508a39e03088b868701` |
| `CHAIN-MODELS-20231002.json` | 41,737 | `d7cdd61f0b044f21abae27d13b297f099a27e38e3fa531fa956dcf5da88b6060` |
| `RECEIPT.json` | 8,555 | `70c2ce013a4885070229206c0e7311629eb65b0a3028dfc828c9e43dbc30b2b2` |
| `TRADE-LEGS-20231002.json` | 2,248 | `6be3667105c5002b2d6b860deb4110e7ec0d063428f4e13c183f569bb3dc55a8` |
| `book-pictures-20231002-part000.parquet` | 10,629,137 | `3cd57f981710a2ba70922ba433876da798a7d696c1119dc2218282c07a771b8c` |
| `book-pictures-20231002-part001.parquet` | 11,792,993 | `62f3be457bd3f626264ce2bdff03a745498b976553c127344938cecaece133ba` |
| `book-pictures-20231002-part002.parquet` | 11,335,501 | `e225f15d191edb0379bcd2e568c6440dde08213cab4a61389de063e71e70fafa` |
| `book-pictures-20231002-part003.parquet` | 11,613,301 | `396be1885d941d9d45f5abd92356ba4bfc555247938c453a6ac6138dfa600c78` |
| `book-pictures-20231002-part004.parquet` | 10,599,636 | `a12d911f7730670fb34eb4b6b2368da661c526b39988cde0f8f6918f5c077a4a` |
| `book-pictures-20231002-part005.parquet` | 11,522,876 | `968f1af8034d5f65bea7852937fdd8c9426c21bb705a86fd5b7085c805047939` |
| `book-pictures-20231002-part006.parquet` | 12,168,538 | `0a5fd04400aa8067a4da46364b07b84b05cce5fea0d6b78d8e8e1c9ab90c806f` |
| `book-pictures-20231002-part007.parquet` | 11,937,325 | `a0ff95cafff76fdf8f4ab0e4492bb592d95d8aead705c089bbe3d9d9059c68ea` |
| `book-pictures-20231002-part008.parquet` | 10,920,955 | `8fd63bb57f5f994466b8b8c9be3dd6b735b0604bcb8040595da37cb45e179a11` |
| `book-pictures-20231002-part009.parquet` | 10,308,560 | `f77832783024829a7b033f7693149c650d3ff4500c24c0110dbeafcaeeee03b9` |
| `book-pictures-20231002-part010.parquet` | 11,857,180 | `79688805d6dbb7a84ce41f5164dd3a6ea59f9ed01afd26ae1a03234ccb6e72dc` |
| `book-pictures-20231002-part011.parquet` | 2,804,135 | `f9906e1187df39dc8e1cd6a47e0541d96345a10e9027d0cffb005639600f2ed6` |
| `calc-book_totals-20231002-part000.parquet` | 2,151,030 | `9d58bdc1f4fcfc119b154d4153a58180b7ac31718e4d277ffd57daa260e86fdb` |
| `calc-book_totals-20231002-part001.parquet` | 2,301,703 | `576445d730245c536a42523d063abe8c62a10e5af090bcb7de226e4fc22cb3cb` |
| `calc-book_totals-20231002-part002.parquet` | 2,255,182 | `4d8e44df7f69974c8266d73cc4073fcb7fbc37aa5ef0b4a40a47a83768fb7c9d` |
| `calc-book_totals-20231002-part003.parquet` | 302,100 | `31865b55280efd3356df869bf52ccb4ae4a4847a14882574c9b3bfef56b71a35` |
| `calc-chain_peaks-20231002-part000.parquet` | 541,630 | `f08eb0e98771bf932a72365f408d8b7d176529bf6d66188405357fc8335b9e78` |
| `calc-chain_peaks-20231002-part001.parquet` | 541,584 | `49523ae92a70504c7a545fbc6ce1b2681cefc407035e6fd6e54797592f81a68a` |
| `calc-chain_peaks-20231002-part002.parquet` | 541,254 | `b61f16d346a01f000153641639b12f29f01d8849e58347ba048fa96b21459345` |
| `calc-chain_peaks-20231002-part003.parquet` | 101,287 | `17a9faf75d264d11751a1a97b1167707f98746e7144134b39c81f02fc00056b9` |
| `calc-chain_peaks-before-20231002-part000.parquet` | 429,219 | `00316e275666d707684a0be0ff1dff4ac77356a4d0c15fba96c3c12c57a50d73` |
| `calc-chain_peaks-facts-20231002-part000.parquet` | 604,590 | `3cf502219a12e3ba3df41d3bab3773ffd6e968403303433895ff89e453908390` |
| `calc-chain_peaks-open-at-the-end-20231002-part000.parquet` | 885 | `f510cb77dedf45a1e24a3faf786c9af96e16b1f35be1bbf6fc0b5bd57eccfd46` |
| `calc-flow_peak-20231002-part000.parquet` | 853,746 | `3ebc4a5e655f33958130db6f9fba0c701ae7291cdfa989c6b76081fa93016fb9` |
| `calc-flow_peak-20231002-part001.parquet` | 931,679 | `cb606e2c2186e41407e585a9336f9ea345032d3b99a3ecccc2db55ace3c928c2` |
| `calc-flow_peak-20231002-part002.parquet` | 899,088 | `a740131113368130a378859dc9b5363cbdf118cb0faa1187493604fe0c6dace0` |
| `calc-flow_peak-20231002-part003.parquet` | 134,805 | `3e1eaf9255a55d60d1e253be48ca7c4fff6e3992a09d3dbc01597e155a42738a` |
| `calc-open_stories-20231002-part000.parquet` | 627,635 | `42db6adbb3e4d578fec0a195d837986d9214f4020848283587b8775104d0ca8f` |
| `calc-open_stories-20231002-part001.parquet` | 609,888 | `14bfbdc2c83bbb6345ffcd87b5d8d1f8afebeb4037c084cdee39d0e93a2e48c0` |
| `calc-open_stories-20231002-part002.parquet` | 611,139 | `b53c120588f9d2a28500635e6463afd4398c94973d6ba8f2127f584112cb2986` |
| `calc-open_stories-20231002-part003.parquet` | 112,289 | `046c0be1199f7b218624f4ad02eb4ba045a3a587f3fa63ffab8c370fab7ee6a5` |
| `calc-outside_changes-20231002-part000.parquet` | 538,401 | `a34b8307a0ca6303e85b8d472d9526e2a47d1ba1b69a129bc6a9f28ab4b1a31e` |
| `calc-outside_changes-20231002-part001.parquet` | 537,694 | `5150acb96c039973e8b2368ebd3d941dea9c067d7ed3bc843b8fba48f668c691` |
| `calc-outside_changes-20231002-part002.parquet` | 537,525 | `f365f30221dcc5f63e642f076ed7e80dd58a833c6825124a9bd27e79e71b05c7` |
| `calc-outside_changes-20231002-part003.parquet` | 100,578 | `366a11319f248884f46732fce71e865d62910ca06336e677ec7498a9950d441c` |
| `calc-outside_changes-facts-20231002-part000.parquet` | 1,533,605 | `844d1e2ee9cf06f676067902febba2c61fc3d4e2dc6c0526805a4b5fac6b6848` |
| `calc-peak_links-20231002-part000.parquet` | 538,343 | `95149772d8320af72d0d9a1dc450b76c1bd02f8874c3aab950ad3efb232922a3` |
| `calc-peak_links-20231002-part001.parquet` | 538,453 | `042948e3049ab20a5f37aeea4395e03b0b674e3639c9b42ddeb798afed42fb25` |
| `calc-peak_links-20231002-part002.parquet` | 537,876 | `45f666770fa1cd32ba4eeb5245c0ddbadc8bcaed407d056febeef205df2f9eea` |
| `calc-peak_links-20231002-part003.parquet` | 100,608 | `c39f9a31194c98e3f97eaead68d1e0de396ff4c55a7cdb4dab07e70a588d9408` |
| `calc-peak_links-facts-20231002-part000.parquet` | 520,135 | `0ee543366ad5a4b9756998b78b1ad2864da8305ea6df3991c7c90c92e46ae9c4` |
| `calc-peak_links-open-at-the-end-20231002-part000.parquet` | 1,148 | `280a2b32c7fd86eef728adcc3a5bb3e07b86522f4542bdd25b93f3ece630f626` |
| `calc-peak_story-20231002-part000.parquet` | 543,206 | `2c38f89b9a7ab92f3da3c156a9d1b411913e355547f29a23ed8323c813262aaf` |
| `calc-peak_story-20231002-part001.parquet` | 546,367 | `4e55915f2a81f7a40db1542c01df3138cdcf7b56b9bf050768d1861ddeae5f43` |
| `calc-peak_story-20231002-part002.parquet` | 544,696 | `7332a16466558670f1b3e926213d3ecde2008f27aecf9fa141c8b46ca026f164` |
| `calc-peak_story-20231002-part003.parquet` | 101,171 | `a32bcc04475561e4bf8e709fe21e5fe27935398b16d20e06344df187ebc6fbf2` |
| `calc-peak_story-facts-20231002-part000.parquet` | 1,642,296 | `136aef8bff3ffc24f565f696b2dacf983ab26456a3f5ff3fbc327996f6f154a6` |
| `calc-peak_story-open-at-the-end-20231002-part000.parquet` | 1,110 | `bb9abe39d68b721d747d2da3b9ff9510481d9e2cb1684a5e26645a6ecc587976` |
| `calc-quote_peaks-20231002-part000.parquet` | 547,415 | `2195538666a0f3d624bca1beefcab8587ae0b2061b6ce3fe33390d974f009faf` |
| `calc-quote_peaks-20231002-part001.parquet` | 543,085 | `eb204e6cfe404436ff260fcf904bcd47b84126479e758afeea28e65ca87d71e6` |
| `calc-quote_peaks-20231002-part002.parquet` | 541,338 | `8cce07089c71657eb304d87af4943e455e8264d9a635cbd8b6c1f3e8c26521c6` |
| `calc-quote_peaks-20231002-part003.parquet` | 101,347 | `8db3f87c581bc9cb07d18850a288f50fe3a15dcfcada8c888b5eeecd64412eb9` |
| `calc-quote_peaks-facts-20231002-part000.parquet` | 1,336,895 | `b1428b856362c28a63625a580c2853185c9c98b8b00bcd3c73df035d4dbadd94` |
| `calc-quote_runs-20231002-part000.parquet` | 2,924,217 | `e217ec8a3cdf5220a63498d5122cdfcfbf0d6f99c4842fc57dfaad347511d47a` |
| `calc-quote_runs-20231002-part001.parquet` | 2,841,038 | `c450676e3a5924a453ba8c59028c5d175606f0c85dbeae8505a222db05a2caf6` |
| `calc-quote_runs-20231002-part002.parquet` | 2,853,492 | `e2034a0bbb96780f4edefd2331bcb88b0a8d544ea8dc0e6a7c01bd7dbb769e35` |
| `calc-quote_runs-20231002-part003.parquet` | 460,532 | `5041cb8be4a4e9d383bb4a5cab0d2f0ea19c18d5ffb99df5f56f2fac6fd17d47` |
| `calc-quote_runs-facts-20231002-part000.parquet` | 1,418,846 | `0a7952fd722a472233eab7e5031bf8380a08b398e84416719d3191c035673aea` |
| `calc-quote_runs-open-at-the-end-20231002-part000.parquet` | 2,027 | `1f4012ba57299a3bd3d926ff969b8a5abea1adc8e1a2f8e09c875c994e8bcba3` |
| `calc-refills-20231002-part000.parquet` | 528,998 | `b1357dd847fc3bc43b6236f9436d7fb7ba174fd7cb1dffeebf73805ea9aa4ac8` |
| `calc-refills-20231002-part001.parquet` | 529,129 | `b3a7d86626d843cb48693fb5b49fbdfd04582661e2393f948812ed9b30301334` |
| `calc-refills-20231002-part002.parquet` | 529,418 | `7910e560030f8202f6c7a3200678ca0a9b08fa9f58286283515cd0ecbe2b50e4` |
| `calc-refills-20231002-part003.parquet` | 99,597 | `f473fae8f5abbe2f19eabea8a751a636d286d2e0ea374bb37ce968b62cce15ae` |
| `calc-refills-facts-20231002-part000.parquet` | 43,246 | `7fdf235bf5630e1222f6361d2c551c249080b4fbdea4bdfcd83692e71bce030a` |
| `calc-sweeps-20231002-part000.parquet` | 542,415 | `ddba3a0121f1b5349ad1d068c0335f23bcaa92c8db538caefc3d15f52c721f32` |
| `calc-sweeps-20231002-part001.parquet` | 544,788 | `88caff913b4b0ca50c827a2ce5d8393c22a0a62da00a2b8945e9598072f091ad` |
| `calc-sweeps-20231002-part002.parquet` | 544,077 | `537c22c680efbd469c00521b9733a0c8cda80b05c4d7fefd6ee34ae61b6a02d0` |
| `calc-sweeps-20231002-part003.parquet` | 101,073 | `c546b9afa0b7fe044ed48fc34cf28ff34e4c4edc94c6bd0354f891bd3dfa1a4c` |
| `calc-sweeps-facts-20231002-part000.parquet` | 1,306,990 | `28443be0ef78535527d9637ddea4a857191fb4d113f963ea72065910148d92c0` |
| `calc-sweeps-open-at-the-end-20231002-part000.parquet` | 734 | `686f3712d423508eaf008134ba74805b62b07249acf3c63d533a38374b048ab2` |
| `calc-together-20231002-part000.parquet` | 535,134 | `a74ab1fd9d30a06ca6bd183b7f5d6193c9bd7877a419f7e4514113e5c080a292` |
| `calc-together-20231002-part001.parquet` | 537,492 | `c40c1e8a762bb26a38f6d4880e79fbd2ceb06eea3d5a58d55624cdfdef45fca9` |
| `calc-together-20231002-part002.parquet` | 536,885 | `6d7ce03ca13df0b51caef93ea20935feb31512de7e126362c8ccfb914f672d2a` |
| `calc-together-20231002-part003.parquet` | 100,266 | `ee017ffb9cb317d41533b33c9d8e314d8ab89e4c8b39185cc21b175e2868b508` |
| `calc-together-facts-20231002-part000.parquet` | 847,537 | `32e579d4a30d70fad70185cf5eebb308787a8102f043fdd8aba3c966517a9412` |
| `calc-together-open-at-the-end-20231002-part000.parquet` | 909 | `dbcf236a733ec98b017da71b00ce46f057e8562e197ab6f62d9c7d4dadc6012a` |
| `chain-models-20231002-part000.parquet` | 29,898,720 | `479a1b2b912eb54ba0ad53662adc5fd5ed28faf4ec0b05513b167039f2ba8114` |
| `playback-20231002.json` | 666 | `1271155b67fc7f95d72f8720e29b79908f34e38d3b71a4a850568aa818dd5f05` |
| `rows-20231002-part000.parquet` | 19,837,787 | `5baee395161f79476c82a0f91035f48226782f5e8db4f55d81746ab8bf571c1b` |
| `rows-20231002-part001.parquet` | 20,111,686 | `eec0368236f487b8624d49aeb3c9ad8cbaf174a0398a2fa2d68908392d149db9` |
| `rows-20231002-part002.parquet` | 20,462,051 | `8e8f0e8ea3e24f80700f5db54d876b3330326bb2c0e57fed73c69271272e5ca2` |
| `rows-20231002-part003.parquet` | 2,876,301 | `4fd041156d86ce815ba967537bba6c4853a09aea16a2d9400cb63a007f6963e4` |
| `trade-legs-6pm-to-8pm-legs-20231002.parquet` | 18,924 | `f091da8df71f8d0606c89cc14733bffbfa7ea2e77db9432fcea0413396e27a6c` |
| `trade-legs-6pm-to-8pm-stretches-20231002.parquet` | 6,499 | `ffc54ed29acc1a7fb1035c3efab141fdcab08e0fe6d01659f9b359df1c7c481f` |
| `trade-legs-6pm-to-8pm-trades-20231002.parquet` | 19,258 | `962df2d7d631a7621a465903efea81cb53c3987324b6549a196f7bb28d85bb4c` |
| `vendor-restatements-20231002.parquet` | 15,331 | `bfe15b673dce5d374c1c2e61cfdae19b07c27afaca128e364307b6921792ff6a` |
