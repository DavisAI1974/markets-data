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

| File | Bytes | SHA256 |
|---|---:|---|
| `CALC-flow_peak-20231002.json` | 4,359 | `3799b95fd8f25e4b27574c71247ce8a3fcf4bdcfe6de3d2a8d137b47cc914ca2` |
| `CALC-peak_story-20231002.json` | 4,069 | `33041b1c4f2b039c1aa3eb9a027f1ba1a5349016901a5957d7cdbde4a8870635` |
| `RECEIPT.json` | 8,555 | `70c2ce013a4885070229206c0e7311629eb65b0a3028dfc828c9e43dbc30b2b2` |
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
| `calc-flow_peak-20231002-part000.parquet` | 853,746 | `3ebc4a5e655f33958130db6f9fba0c701ae7291cdfa989c6b76081fa93016fb9` |
| `calc-flow_peak-20231002-part001.parquet` | 931,679 | `cb606e2c2186e41407e585a9336f9ea345032d3b99a3ecccc2db55ace3c928c2` |
| `calc-flow_peak-20231002-part002.parquet` | 899,088 | `a740131113368130a378859dc9b5363cbdf118cb0faa1187493604fe0c6dace0` |
| `calc-flow_peak-20231002-part003.parquet` | 134,805 | `3e1eaf9255a55d60d1e253be48ca7c4fff6e3992a09d3dbc01597e155a42738a` |
| `calc-peak_story-20231002-part000.parquet` | 543,206 | `2c38f89b9a7ab92f3da3c156a9d1b411913e355547f29a23ed8323c813262aaf` |
| `calc-peak_story-20231002-part001.parquet` | 546,367 | `4e55915f2a81f7a40db1542c01df3138cdcf7b56b9bf050768d1861ddeae5f43` |
| `calc-peak_story-20231002-part002.parquet` | 544,696 | `7332a16466558670f1b3e926213d3ecde2008f27aecf9fa141c8b46ca026f164` |
| `calc-peak_story-20231002-part003.parquet` | 101,171 | `a32bcc04475561e4bf8e709fe21e5fe27935398b16d20e06344df187ebc6fbf2` |
| `calc-peak_story-facts-20231002-part000.parquet` | 1,642,296 | `136aef8bff3ffc24f565f696b2dacf983ab26456a3f5ff3fbc327996f6f154a6` |
| `calc-peak_story-open-at-the-end-20231002-part000.parquet` | 1,110 | `bb9abe39d68b721d747d2da3b9ff9510481d9e2cb1684a5e26645a6ecc587976` |
| `playback-20231002.json` | 666 | `1271155b67fc7f95d72f8720e29b79908f34e38d3b71a4a850568aa818dd5f05` |
| `rows-20231002-part000.parquet` | 19,837,787 | `5baee395161f79476c82a0f91035f48226782f5e8db4f55d81746ab8bf571c1b` |
| `rows-20231002-part001.parquet` | 20,111,686 | `eec0368236f487b8624d49aeb3c9ad8cbaf174a0398a2fa2d68908392d149db9` |
| `rows-20231002-part002.parquet` | 20,462,051 | `8e8f0e8ea3e24f80700f5db54d876b3330326bb2c0e57fed73c69271272e5ca2` |
| `rows-20231002-part003.parquet` | 2,876,301 | `4fd041156d86ce815ba967537bba6c4853a09aea16a2d9400cb63a007f6963e4` |
| `vendor-restatements-20231002.parquet` | 15,331 | `bfe15b673dce5d374c1c2e61cfdae19b07c27afaca128e364307b6921792ff6a` |
