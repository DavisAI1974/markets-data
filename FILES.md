# ROOT stored rows: trade day Wed Oct 18, 2023 (6 pm Eastern the evening before to 5 pm Eastern)

Built by the new ROOT (Markets branch `claude/root-session6-017eY1`, commit `b39e10a`) from the raw order tape
and the made outside tables in markets-data branch `ccr-349e2ffe-07p8od`. Nothing here comes from an old run.

- Rows: 771,468 (one per tick), 217 fields each. Sections A to E from the tape and the book, section G the 13 outside data points.
- Rows by label: 5 pm to 6 pm stretch 889, trade day 770,579.
- Book pictures: one at each of 30,739 trade messages, one at the first written row and one at the last (35,735,000 order lines).
- Only rows labelled "trade day" enter a calculation. The stretch and start-up rows are kept and marked; nothing is calculated on them.
- An empty field is stored as empty (null): never 0, never blank text. A line that a tick emptied is the words "no orders".
- Checks in `RECEIPT.json`, all passed: every record accounted for; the trade day cut; the book equals the vendor restatement; the book adds up at every trade; one history per order; the trade count; the outside points pinned right on every row and every section G column.
- `playback-*.json` is the playback record (four cuts, all identical). It was made on the first build of this session (Markets `fca77bb`), before the emptied line was changed from a blank cell to the words "no orders". That change touches one text cell and was not run through playback again (one check per changed part).
- Part 2, Step 1, laid out and approved by Greg 2026-11-16 (`STEP1_STEP2_LAYOUTS.md`; Markets `6a468af`). The rows files are untouched; each calculation's output is its own files.
  - `flow_peak` (piece 1, the flow and the exhaustion peak): `calc-flow_peak-20231018-part*.parquet`, one file beside each rows file, in the same row order, with the position on the tape and 12 columns. 7,967 peaks became known in the trade day.
  - `peak_story` (piece 2, what each peak did before and after; no fixed marks, no names for kinds of peak): `calc-peak_story-facts-20231018-part*.parquet`, one line per fact, each with the tick at which it became known and the peak it is about: 45,958 facts (7,967 build-up, 24,758 new low, 5,268 reached zero, 5,267 came back, 2,698 beaten); `calc-peak_story-20231018-part*.parquet`, the number of facts known on each row; `calc-peak_story-open-at-the-end-20231018-part000.parquet`, the 2 peaks whose story had not ended at the last tick.
  - Checks, in `CALC-flow_peak-20231018.json` and `CALC-peak_story-20231018.json`, all passed: every column and every fact worked out again from the stored rows by a different method and equal; playback equal at two cuts each. Rows of no trade day hold empty cells.
- Part 2, Step 2, pieces C and I (the quote's own runs), approved by Greg 2026-11-16 (`STEP2_PLAN.md`; Markets `9612f87`). They read the stored rows through the rows gate, which passed exactly the ticks of the tape gate. The rows files are untouched.
  - `book_totals` (piece C, the book running totals): `calc-book_totals-20231018-part*.parquet`, one file beside each rows file, in the same row order, with the position on the tape and 24 columns: for the bid side and the ask side, size added, pulled, filled and moved since the first tick of the trade day, each for the whole side and at the best price, the size put back on orders as they traded (`refilled`), and the filled size whose fill message the tape gives no side for. At the last tick: bid added 392,063, pulled 361,298, filled 30,249, moved 39,891; ask added 367,409, pulled 334,662, filled 32,424, moved 36,589.
  - `quote_runs` (piece I, first part: the runs of the best bid and of the best ask, followed separately; no minimum length or size): `calc-quote_runs-facts-20231018-part*.parquet`, one line per fact, each with the tick at which it became known and the run it is about: 64,050 facts (13,877 runs of the best bid, 13,268 of the best ask; run started, new furthest price, first step back); `calc-quote_runs-20231018-part*.parquet`, the run in progress on each side on every row and the number of facts known there; `calc-quote_runs-open-at-the-end-20231018-part000.parquet`, the 2 runs still going at the last tick.
  - Checks, in `CALC-book_totals-20231018.json` and `CALC-quote_runs-20231018.json`, all passed. Book totals: every column worked out again from whole columns by a different method and equal; on every row each side's total size equals its size at the open plus added minus pulled minus filled; the size filled equals the size of the tape's fill messages (62,673); playback equal at two cuts, one inside an exchange event between a fill message and the row where the book shows it. Quote runs: every fact found again from the foundation's marks of a best price moving (the calculation reads only the best-price columns) and equal; playback equal at two cuts, one on a tick that ends one run and starts the next. Rows of no trade day hold empty cells.
- Part 2, Step 2, pieces A and B, approved by Greg 2026-11-16 (`STEP2_PLAN.md`; Markets `899f1b8`). Run on a Runpod pod, one trade day per pod, the four at the same time, on his go; every file here was fetched from the pod and compared with the fingerprint in its receipt. The rows files are untouched.
  - `peak_links` (piece A, the links between peaks, as facts, with no letters and no depth): `calc-peak_links-facts-20231018-part*.parquet`, one line per fact, each with the tick at which it became known and the peak it is about: 15,932 facts. At the tick a peak becomes known: the last peak before it on its own side and on the other side (the tick of its high, the time between the two highs, the price at its high, whether its story was still open) and the peak before, same side or not. At the tick a story ends: how many later peaks became known while it was open, and the first of them. Of 7,967 peaks, the peak before was on the same side for 5,540 and on the other side for 2,426; 5,030 became known while the peak before was still open; the most later peaks inside one story was 68. `calc-peak_links-20231018-part*.parquet`, the number of facts known on each row; `calc-peak_links-open-at-the-end-20231018-part000.parquet`, the 2 peaks whose story had not ended at the last tick.
  - `open_stories` (piece B, the state at each tick): `calc-open_stories-20231018-part*.parquet`, one file beside each rows file, in the same row order, with the position on the tape and 10 columns: for buy peaks and for sell peaks, how many stories are open, how many of those have reached zero and not come back, and the tick of the high of the oldest, the newest and the largest open one. The most open at one tick: 14 buy, 19 sell.
  - Checks, in `CALC-peak_links-20231018.json` and `CALC-open_stories-20231018.json`, all passed: every link and every column worked out again from the stored outputs of pieces 1 and 2 as whole tables and equal; playback equal at two cuts each. Rows of no trade day hold empty cells.
- Part 2, additions L and M and the first part of the chain link models, approved by Greg 2026-11-16 ("Try them all"; "Do it"; `STEP1_STEP2_LAYOUTS.md`). Run on a Runpod pod 2026-11-16 evening Eastern, one trade day per pod, the four at the same time, each calculation its own helper pinned to its own CPU, on his go ("Approve"); every file here was fetched from the pod and compared with the fingerprint in its receipt before it was stored. The rows files are untouched.
  - `refills` (addition L, orders traded against with size put back; Markets `b8b720c`): `calc-refills-facts-20231018-part*.parquet`, one line per fact at the tick of the order's own row: 1,608 facts, 1,527 with size put back, 1,370 of them leaving the order the same size or larger; 379 orders, at most 76 times on one order. Size put back: bid 2,223, ask 1,273, equal to the `refilled` totals of the stored book totals. `calc-refills-20231018-part*.parquet` holds the count of facts known on each row.
  - `sweeps` (addition M, every trade event and the quote touching or crossing; Markets `5f49e4d`): `calc-sweeps-facts-20231018-part*.parquet`, one line per fact: 29,797 trade events (1,357 with no fill message, 24 with more than one trade side, at most 5 price levels filled in one event); the quote touched or crossed 557 times (1,910 ticks), none standing at the last tick. It was run twice: the first run's receipt counted the touch facts 33 times over (the facts themselves were right); only the corrected run is stored.
  - `chain_peaks` (the chain link models, first part: what each peak did, and the ended peaks before it; Markets `b8b720c`): `calc-chain_peaks-facts-20231018-part*.parquet`, one line per peak at the tick its story ended: 7,965 peak lines (5,267 came back, 2,698 beaten; 2 still open at the last tick, listed in `calc-chain_peaks-open-at-the-end-*`). `calc-chain_peaks-before-20231018-part*.parquet`, one line per step back at the tick a peak became known: 47,755 lines, six steps written out (8 peak lines had fewer than six ended peaks before them). Empty cells: no low for the rise on 35 lines, no trade between the high and the end on 118, no peak before on 1. It holds no model.
  - Checks, in `CALC-refills-20231018.json`, `CALC-sweeps-20231018.json` and `CALC-chain_peaks-20231018.json`, all passed on the first run of each: every fact and line worked out again by a different method and equal; playback equal at two cuts (three for sweeps), each cut where something was still unfolding. Rows of no trade day hold empty cells.
- Part 2, the three calculations written in the ninth session and first run in the tenth (Markets `02ffde6`, on a pod; Greg's go 2026-11-17):
  - `quote_peaks` (the rest of piece I: the peaks in play at every turn of a run of the quote): `calc-quote_peaks-20231018-part*.parquet` beside the rows; `calc-quote_peaks-facts-20231018-part*.parquet`, 64,050 facts, one at every turn.
  - `outside_changes` (addition O: what was in play when an outside figure changed): `calc-outside_changes-20231018-part*.parquet`; `calc-outside_changes-facts-20231018-part*.parquet`, 72,736 facts over 108 outside columns followed (13,926 ticks with a change).
  - `together` (addition N: orders that entered or left at the same exchange time): `calc-together-20231018-part*.parquet`; `calc-together-facts-20231018-part*.parquet`, 15 lines in 5 sets that entered together and 27,060 lines in 7,795 sets that left together; `calc-together-open-at-the-end-20231018-part000.parquet`.
  - Checks, in `CALC-quote_peaks-20231018.json`, `CALC-outside_changes-20231018.json` and `CALC-together-20231018.json`, all passed on the first run (a recount by a second method, the playback cuts, the rows gate).

| File | Bytes | SHA256 |
|---|---:|---|
| `CALC-book_totals-20231018.json` | 8,090 | `bacda48896dcb6beb2aeccccd69d60faebb453d53fec6df1ea0820ab31caf21c` |
| `CALC-chain_peaks-20231018.json` | 5,400 | `8c7fefead7a27e658c1a44f31487791ee8f29bd4a55e46c9515add25db2be56e` |
| `CALC-flow_peak-20231018.json` | 4,305 | `01ad68bb58b45faeeb1cc265d3a484f3621c670d71eba70c6ea95f1ae5ce76cc` |
| `CALC-open_stories-20231018.json` | 3,980 | `d1db6acf3332b150e082f7b118b32d7ad54cec0e74a1c44428e35c246238c60b` |
| `CALC-outside_changes-20231018.json` | 8,384 | `69874bbe0ff6b0571354eb6f4fe20d365163e67e87134898038635f3f0193c4f` |
| `CALC-peak_links-20231018.json` | 4,168 | `c63d8fcf3d11ea883cb2cc10c21a50c9bdf89bb010eb4e711915e1863b381c70` |
| `CALC-peak_story-20231018.json` | 4,013 | `c27dc48a20d5bf9db1f8d1d7eed23c0c29a4374f3ba69fac20317d1484563c54` |
| `CALC-quote_peaks-20231018.json` | 3,772 | `9081b18c7e065e0889139c5a3d1a11b545149493da7064421a08e3f102b6c8c8` |
| `CALC-quote_runs-20231018.json` | 6,221 | `c9fad90f9babc52b853517fc50caa8ef47a3eacbef8abf3af71406e7bfa373fa` |
| `CALC-refills-20231018.json` | 4,478 | `d94d50ccfadb5f0bd3ffeb49789f70cf20bd136e9a4a5a7d120be9681bb05776` |
| `CALC-sweeps-20231018.json` | 5,174 | `b4a4a5936a2ddc931a37c72df502af117ed427f41426864cd753953f89fc59c6` |
| `CALC-together-20231018.json` | 4,679 | `6c255d20dc9b052286ce760b2b35cb9950075d2409d615fff739b7e3f05369fa` |
| `RECEIPT.json` | 8,849 | `ab9b100236fc09124313410653ad6f49a1139661f6c66adc70209febb6f9436b` |
| `book-pictures-20231018-part000.parquet` | 12,044,565 | `825dae26433b637002707b830852ad544c22ad171b816427d82c6d5ffd18707b` |
| `book-pictures-20231018-part001.parquet` | 12,391,163 | `b77cce7fcdc43d67ae8818a23f65bd07ff39df6428f02ea0f00900d1ad5be7d4` |
| `book-pictures-20231018-part002.parquet` | 12,182,897 | `6d3447de145a9723aba9499e3c480ae527b7e53fefa939e3c40e7fc7a64ff5b6` |
| `book-pictures-20231018-part003.parquet` | 12,892,234 | `19b6af4349fce663bb3281c8588a7b23bc40be49dc58b470c92ff17ec5ee5d9d` |
| `book-pictures-20231018-part004.parquet` | 12,947,908 | `3dbb250bc6c53c10bd5f8417da7a2da91f13166af5fa04edf8234e053d5a6f8d` |
| `book-pictures-20231018-part005.parquet` | 11,388,728 | `6998b53fff63dcd3882b63a2e57f76288a43f91d6d1d567a0d5806f126798c20` |
| `book-pictures-20231018-part006.parquet` | 11,918,275 | `77ab656c3b2828527201b6cac260ff8086199e000fc4e93654ac71cdaf5b145b` |
| `book-pictures-20231018-part007.parquet` | 12,122,094 | `702ebad0ad0c2a67e4d5520ede4c1c6a132b357697ce3bd4a42d57e1e2e881f7` |
| `book-pictures-20231018-part008.parquet` | 6,550,590 | `28a058da1a92473626f33b6a5d9bb0e69fe94e78c34671a9a1b123181a315983` |
| `calc-book_totals-20231018-part000.parquet` | 2,181,068 | `b65d3fec8799c953e0c0dcb63f09aaba66cdc6a2a52c4ea3fff534377b338726` |
| `calc-book_totals-20231018-part001.parquet` | 2,236,724 | `552849f6666cad06cb0afb6f462562256df1cd19d2ce40db88470ccb407ea396` |
| `calc-book_totals-20231018-part002.parquet` | 2,089,368 | `9e0e4b8de93fdd9c8318b85c0671c6fb244e59563d0c069aed3ab420f5e05aee` |
| `calc-chain_peaks-20231018-part000.parquet` | 540,125 | `16d2da77ffcf9297c619094baf284f791eef334f18585144fbfb1d6316b8d7d3` |
| `calc-chain_peaks-20231018-part001.parquet` | 540,293 | `7fd3e92f8d2ffc06f8a8d2032cc5ff1169c9648c7c4bf37a52395b21bab4edf0` |
| `calc-chain_peaks-20231018-part002.parquet` | 524,727 | `95d3d6333a7c05ceb70ca0cd7565b9de92b680b75e38170332479f17312198a2` |
| `calc-chain_peaks-before-20231018-part000.parquet` | 380,082 | `2bd458e2f393abeccb3395deaa0f14e8749dd88f109a190c54e0a44f9d9b3816` |
| `calc-chain_peaks-facts-20231018-part000.parquet` | 503,376 | `728b707f6c16d213e87a3aa49b428929e79015c14ca8b6d68e8f973b70458f0f` |
| `calc-chain_peaks-open-at-the-end-20231018-part000.parquet` | 901 | `dac642e5a00562bc74b714536693229c7e51a0740d03f71da401a697b749885c` |
| `calc-flow_peak-20231018-part000.parquet` | 806,993 | `40b208450b7106d70c7ab984a9c918bc61e24eb23b94b233486129c6d2b96a7f` |
| `calc-flow_peak-20231018-part001.parquet` | 860,997 | `40708987669d0a28f0740ffa15b1f56efbcf7551cad8e3602fed6f08ba85a1fc` |
| `calc-flow_peak-20231018-part002.parquet` | 818,036 | `a338ddf196f90fadfbe19bcb40844c860478910ccef2884d03f9309ee466ed8d` |
| `calc-open_stories-20231018-part000.parquet` | 619,366 | `29220e4fd44f3c4b57c737411551fa521a84b913dfad9fbae762c78fccd211c1` |
| `calc-open_stories-20231018-part001.parquet` | 603,709 | `a178301cc7c836d33d1eb7608581d410cb357b6a3d12e3440b2fede95d30b265` |
| `calc-open_stories-20231018-part002.parquet` | 591,256 | `3418eec110bead9b055144676aad5231f85003f9bcd3bcc3fc1a033ff8668050` |
| `calc-outside_changes-20231018-part000.parquet` | 539,845 | `8aedb8fb537b3dd296b09bbb5898f2e7d149fa4f8955c5ae81034f90f71b382a` |
| `calc-outside_changes-20231018-part001.parquet` | 538,459 | `23d17d664d7142b4fd5c80c7dce5ce93e897fecd1cb8356a4a20cba2de00afc2` |
| `calc-outside_changes-20231018-part002.parquet` | 522,673 | `b3e004490969b5fb7c9b042aaa6260117f49e5d12afe28ad4f9a05b4cc987626` |
| `calc-outside_changes-facts-20231018-part000.parquet` | 1,601,909 | `63808863841e15bfdf1618ed5a59d3c45e2846e7192faa23b8f8143fc596009a` |
| `calc-peak_links-20231018-part000.parquet` | 537,351 | `1f6357c87cef64d03117835c1b2539f797661949e13fb93045c4e51fc39a53f9` |
| `calc-peak_links-20231018-part001.parquet` | 537,322 | `2017d3efb5fa5430c74e0bdfcf280c92d989d666658fdadfcfc28249cc8cf10e` |
| `calc-peak_links-20231018-part002.parquet` | 521,739 | `19bb50350ad871e175c2714c664ba8b4f0a3b9183c4d73c91ea06f5509dccd79` |
| `calc-peak_links-facts-20231018-part000.parquet` | 440,243 | `8c6fe1e4911ab4a561b970ccaa90086dee4881e5fb17133de5457130604af095` |
| `calc-peak_links-open-at-the-end-20231018-part000.parquet` | 1,252 | `06141584c08aad2e2f0ce81b1e70152944ac572d68e2c90e479639cce54afc48` |
| `calc-peak_story-20231018-part000.parquet` | 541,088 | `90cca4a659ca9ffe1aa158ee909d15d701564738442139a2c8961ab0e4ceccc0` |
| `calc-peak_story-20231018-part001.parquet` | 543,461 | `fd7dbccf128339644900ee73e1240ae1de70c4c739161476089adf3d4fee7636` |
| `calc-peak_story-20231018-part002.parquet` | 527,795 | `b0bdb49e559c472790e719a1aca597bfc67e830b49c5ec99df5e282cba70382b` |
| `calc-peak_story-facts-20231018-part000.parquet` | 1,267,791 | `338352a0c4d686f9b5afcf8f2aa17f27e1e91a4359b0929933e76ccf332513f9` |
| `calc-peak_story-open-at-the-end-20231018-part000.parquet` | 1,126 | `e793ae68151a914e0b5df371bb1ae3e1f540cfc42096cfa09ef34958b9a35db0` |
| `calc-quote_peaks-20231018-part000.parquet` | 547,563 | `0f95550f6794fa4beb6d9e3c9769446fa6af330ed982558468354ef4c6918fdf` |
| `calc-quote_peaks-20231018-part001.parquet` | 544,768 | `a4c81af023379168bcd0401f0be3303b805ef5c8fe2a627dcd4da20f22d34cf0` |
| `calc-quote_peaks-20231018-part002.parquet` | 528,173 | `6ee10bdd91a681c2fd2a867b29ff62bb36df9cb333af96c2c1bf4f9c13d8425f` |
| `calc-quote_peaks-facts-20231018-part000.parquet` | 1,385,686 | `0c40c27777ff9041259605e9aa96a69f89f50e96a0eca66d3332e6290d0ea54e` |
| `calc-quote_runs-20231018-part000.parquet` | 2,958,414 | `1f0a2a182412dec9d39459da2fdaa9a2bc0e1d3ec4e9eb7ad6cb1f0fd16984f8` |
| `calc-quote_runs-20231018-part001.parquet` | 2,867,305 | `d8f52d36ebd5265ff2e697b082844158970c9cd88c2ccbce8f187b5637884139` |
| `calc-quote_runs-20231018-part002.parquet` | 2,766,047 | `65934821804695dc507cd67da3fb9dc441cf08c34270bcf23580fff04003d974` |
| `calc-quote_runs-facts-20231018-part000.parquet` | 1,473,430 | `eb33ba31604c99e23a7a1ff4b24a297c18d54a13e6ab6eb067064c3a89d1a266` |
| `calc-quote_runs-open-at-the-end-20231018-part000.parquet` | 2,048 | `ab3388b72386de986b15500ae387354384c67f8775beaede87e2f0630128b752` |
| `calc-refills-20231018-part000.parquet` | 528,706 | `e24f741e1a8540c39db96edc2a632af0ac7a67730f75ce036dbfe36f03324b99` |
| `calc-refills-20231018-part001.parquet` | 529,329 | `6d63e3ddfb399414cd855d5e285257ba9331870802048d961670416a81dca570` |
| `calc-refills-20231018-part002.parquet` | 513,959 | `445c054f7c8936a127567fa3891b129814a3a6b0da63e2c26f105bfe13c32f7a` |
| `calc-refills-facts-20231018-part000.parquet` | 40,586 | `98fee353e92e47039afbf3d30b36814087ed230f153e68bea732776e3509524b` |
| `calc-sweeps-20231018-part000.parquet` | 541,057 | `db6a5a1d7c74546d8234ed66471f3356d8a55989c3e5eae62d28b2f9d8fe8e29` |
| `calc-sweeps-20231018-part001.parquet` | 542,342 | `8fdebb73fbceea7d935c9300e028d9ca37b11f154d584713f9070b3e8fc85fca` |
| `calc-sweeps-20231018-part002.parquet` | 527,085 | `efbbbdfecdb85cb302b2bf83921b0b7dab366ad465d2c7d0ae4deed813e87861` |
| `calc-sweeps-facts-20231018-part000.parquet` | 1,088,842 | `f1f09a7788b6c4f2dcf199b81b152c9a1716671c7b6bbafcf2e6d31902e24dff` |
| `calc-sweeps-open-at-the-end-20231018-part000.parquet` | 734 | `686f3712d423508eaf008134ba74805b62b07249acf3c63d533a38374b048ab2` |
| `calc-together-20231018-part000.parquet` | 534,156 | `38231314fcd48ad3db35dd73487bb5d8a8d3388c69d1cbe64864020e5810c8df` |
| `calc-together-20231018-part001.parquet` | 536,266 | `847816e2703a3318bc3edd840fd5888cdbc020bf910e233b89e8656b7e573af0` |
| `calc-together-20231018-part002.parquet` | 520,497 | `e271481fc4e463f2bd622ae1c45c315f25d38b1a6e55d3a770755e44d0971183` |
| `calc-together-facts-20231018-part000.parquet` | 681,187 | `741bead91e201a9f9fe01f705a53b42bf02ce0452ccb5d26ba3c457ef75a8376` |
| `calc-together-open-at-the-end-20231018-part000.parquet` | 909 | `dbcf236a733ec98b017da71b00ce46f057e8562e197ab6f62d9c7d4dadc6012a` |
| `playback-20231018.json` | 666 | `dff963b8f017297e3be9ddd21c68c5ed3d1d7afe470aa63cb0bc13c67c4c8439` |
| `rows-20231018-part000.parquet` | 19,918,917 | `553218f493ba6420dfc957f9adce322ddf8e477ab150f60fc88f97fba635df47` |
| `rows-20231018-part001.parquet` | 20,110,859 | `7cd439efe8f94e71d4612e7d8effe88994ae96b653d724c73749797bd1479975` |
| `rows-20231018-part002.parquet` | 18,971,027 | `4a74d42f71f754bd55db61a627e92cdebe9812faf248b649310462a05703023f` |
| `vendor-restatements-20231018.parquet` | 34,368 | `ceacfad36514edf43a7ba367914f00a6f79eab37a3276fc07fa0dff223eb43b7` |
