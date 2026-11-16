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

| File | Bytes | SHA256 |
|---|---:|---|
| `CALC-book_totals-20231018.json` | 8,090 | `bacda48896dcb6beb2aeccccd69d60faebb453d53fec6df1ea0820ab31caf21c` |
| `CALC-flow_peak-20231018.json` | 4,305 | `01ad68bb58b45faeeb1cc265d3a484f3621c670d71eba70c6ea95f1ae5ce76cc` |
| `CALC-peak_story-20231018.json` | 4,013 | `c27dc48a20d5bf9db1f8d1d7eed23c0c29a4374f3ba69fac20317d1484563c54` |
| `CALC-quote_runs-20231018.json` | 6,221 | `c9fad90f9babc52b853517fc50caa8ef47a3eacbef8abf3af71406e7bfa373fa` |
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
| `calc-flow_peak-20231018-part000.parquet` | 806,993 | `40b208450b7106d70c7ab984a9c918bc61e24eb23b94b233486129c6d2b96a7f` |
| `calc-flow_peak-20231018-part001.parquet` | 860,997 | `40708987669d0a28f0740ffa15b1f56efbcf7551cad8e3602fed6f08ba85a1fc` |
| `calc-flow_peak-20231018-part002.parquet` | 818,036 | `a338ddf196f90fadfbe19bcb40844c860478910ccef2884d03f9309ee466ed8d` |
| `calc-peak_story-20231018-part000.parquet` | 541,088 | `90cca4a659ca9ffe1aa158ee909d15d701564738442139a2c8961ab0e4ceccc0` |
| `calc-peak_story-20231018-part001.parquet` | 543,461 | `fd7dbccf128339644900ee73e1240ae1de70c4c739161476089adf3d4fee7636` |
| `calc-peak_story-20231018-part002.parquet` | 527,795 | `b0bdb49e559c472790e719a1aca597bfc67e830b49c5ec99df5e282cba70382b` |
| `calc-peak_story-facts-20231018-part000.parquet` | 1,267,791 | `338352a0c4d686f9b5afcf8f2aa17f27e1e91a4359b0929933e76ccf332513f9` |
| `calc-peak_story-open-at-the-end-20231018-part000.parquet` | 1,126 | `e793ae68151a914e0b5df371bb1ae3e1f540cfc42096cfa09ef34958b9a35db0` |
| `calc-quote_runs-20231018-part000.parquet` | 2,958,414 | `1f0a2a182412dec9d39459da2fdaa9a2bc0e1d3ec4e9eb7ad6cb1f0fd16984f8` |
| `calc-quote_runs-20231018-part001.parquet` | 2,867,305 | `d8f52d36ebd5265ff2e697b082844158970c9cd88c2ccbce8f187b5637884139` |
| `calc-quote_runs-20231018-part002.parquet` | 2,766,047 | `65934821804695dc507cd67da3fb9dc441cf08c34270bcf23580fff04003d974` |
| `calc-quote_runs-facts-20231018-part000.parquet` | 1,473,430 | `eb33ba31604c99e23a7a1ff4b24a297c18d54a13e6ab6eb067064c3a89d1a266` |
| `calc-quote_runs-open-at-the-end-20231018-part000.parquet` | 2,048 | `ab3388b72386de986b15500ae387354384c67f8775beaede87e2f0630128b752` |
| `playback-20231018.json` | 666 | `dff963b8f017297e3be9ddd21c68c5ed3d1d7afe470aa63cb0bc13c67c4c8439` |
| `rows-20231018-part000.parquet` | 19,918,917 | `553218f493ba6420dfc957f9adce322ddf8e477ab150f60fc88f97fba635df47` |
| `rows-20231018-part001.parquet` | 20,110,859 | `7cd439efe8f94e71d4612e7d8effe88994ae96b653d724c73749797bd1479975` |
| `rows-20231018-part002.parquet` | 18,971,027 | `4a74d42f71f754bd55db61a627e92cdebe9812faf248b649310462a05703023f` |
| `vendor-restatements-20231018.parquet` | 34,368 | `ceacfad36514edf43a7ba367914f00a6f79eab37a3276fc07fa0dff223eb43b7` |
