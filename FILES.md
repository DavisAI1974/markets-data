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
- Part 2, the calculation `flow_peak` (the flow and the exhaustion peak; laid out and approved by Greg 2026-11-16, `STEP1_STEP2_LAYOUTS.md` piece 1; Markets `5aff999`): `calc-flow_peak-*.parquet`, one file beside each rows file, in the same row order, with the position on the tape and 12 new columns. 8,894 peaks became known in the trade day. Rows of no trade day hold empty cells. Check in `CALC-flow_peak-20231002.json`, passed: every column recounted from the stored rows by a different method and equal on all 820,670 rows; playback equal at two cuts.

| File | Bytes | SHA256 |
|---|---:|---|
| `CALC-flow_peak-20231002.json` | 4,433 | `00f6312124c74386b0191dac3e63a00601fb412e75e16fafcd205ac3c25ac372` |
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
| `calc-flow_peak-20231002-part000.parquet` | 842,257 | `f5d68b1b4b3aa54c1b489255f7e97ee42dc24949b283d7565d9945239009fe81` |
| `calc-flow_peak-20231002-part001.parquet` | 922,730 | `96f90cb8ffbe07af9d12845ab04381d0043d3bd815000f014ec66eb137e05fee` |
| `calc-flow_peak-20231002-part002.parquet` | 889,431 | `960a81d9ea90c7ad6fcc3c90193f41e380bc38d4340e4f811f429024d724ee77` |
| `calc-flow_peak-20231002-part003.parquet` | 133,752 | `c957b9b0f3f148d3ca015d94ee11c99b2dd9c1113d44b86d27ab61db069f241e` |
| `playback-20231002.json` | 666 | `1271155b67fc7f95d72f8720e29b79908f34e38d3b71a4a850568aa818dd5f05` |
| `rows-20231002-part000.parquet` | 19,837,787 | `5baee395161f79476c82a0f91035f48226782f5e8db4f55d81746ab8bf571c1b` |
| `rows-20231002-part001.parquet` | 20,111,686 | `eec0368236f487b8624d49aeb3c9ad8cbaf174a0398a2fa2d68908392d149db9` |
| `rows-20231002-part002.parquet` | 20,462,051 | `8e8f0e8ea3e24f80700f5db54d876b3330326bb2c0e57fed73c69271272e5ca2` |
| `rows-20231002-part003.parquet` | 2,876,301 | `4fd041156d86ce815ba967537bba6c4853a09aea16a2d9400cb63a007f6963e4` |
| `vendor-restatements-20231002.parquet` | 15,331 | `bfe15b673dce5d374c1c2e61cfdae19b07c27afaca128e364307b6921792ff6a` |
