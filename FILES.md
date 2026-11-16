# ROOT stored rows: trade day Tue Oct 3, 2023 (6 pm Eastern the evening before to 5 pm Eastern)

Built by the new ROOT (Markets branch `claude/root-session6-017eY1`, commit `b39e10a`) from the raw order tape
and the made outside tables in markets-data branch `ccr-349e2ffe-07p8od`. Nothing here comes from an old run.

- Rows: 879,497 (one per tick), 217 fields each. Sections A to E from the tape and the book, section G the 13 outside data points.
- Rows by label: 5 pm to 6 pm stretch 826, trade day 878,671.
- Book pictures: one at each of 41,410 trade messages, one at the first written row and one at the last (51,053,273 order lines).
- Only rows labelled "trade day" enter a calculation. The stretch and start-up rows are kept and marked; nothing is calculated on them.
- An empty field is stored as empty (null): never 0, never blank text. A line that a tick emptied is the words "no orders".
- Checks in `RECEIPT.json`, all passed: every record accounted for; the trade day cut; the book equals the vendor restatement; the book adds up at every trade; one history per order; the trade count; the outside points pinned right on every row and every section G column.
- `playback-*.json` is the playback record (four cuts, all identical). It was made on the first build of this session (Markets `fca77bb`), before the emptied line was changed from a blank cell to the words "no orders". That change touches one text cell and was not run through playback again (one check per changed part).
- Part 2, Step 1, laid out and approved by Greg 2026-11-16 (`STEP1_STEP2_LAYOUTS.md`; Markets `6a468af`). The rows files are untouched; each calculation's output is its own files.
  - `flow_peak` (piece 1, the flow and the exhaustion peak): `calc-flow_peak-20231003-part*.parquet`, one file beside each rows file, in the same row order, with the position on the tape and 12 columns. 10,577 peaks became known in the trade day.
  - `peak_story` (piece 2, what each peak did before and after; no fixed marks, no names for kinds of peak): `calc-peak_story-facts-20231003-part*.parquet`, one line per fact, each with the tick at which it became known and the peak it is about: 68,185 facts (10,577 build-up, 40,754 new low, 6,278 reached zero, 6,277 came back, 4,299 beaten); `calc-peak_story-20231003-part*.parquet`, the number of facts known on each row; `calc-peak_story-open-at-the-end-20231003-part000.parquet`, the 1 peaks whose story had not ended at the last tick.
  - Checks, in `CALC-flow_peak-20231003.json` and `CALC-peak_story-20231003.json`, all passed: every column and every fact worked out again from the stored rows by a different method and equal; playback equal at two cuts each. Rows of no trade day hold empty cells.

| File | Bytes | SHA256 |
|---|---:|---|
| `CALC-flow_peak-20231003.json` | 4,491 | `8f368bbb15da6beb3d4c5def44e9a5ad56e3a0d02820c7cb0f487d4e91872f82` |
| `CALC-peak_story-20231003.json` | 4,203 | `1cc7ff64545eb6fe28bf5146e9d8b50da79c450bc04e93769e73b3a4b750b3b0` |
| `RECEIPT.json` | 9,215 | `e073a3f90b7155943a6075543909f279b6a7cff68ea54e277d1993b97722534f` |
| `book-pictures-20231003-part000.parquet` | 11,063,412 | `e8540de6eee5c4607654dc8933d78aec236754e272a93b353aa1e2675191556c` |
| `book-pictures-20231003-part001.parquet` | 11,611,555 | `8468695df9b90caccf96f1cad87cd115201e577211aa1ef31777913f7bf3d070` |
| `book-pictures-20231003-part002.parquet` | 10,932,568 | `a5e146e665784c726c31bc6ef4a13a22eb23c3d1ab3463c0e94148390341cda3` |
| `book-pictures-20231003-part003.parquet` | 11,548,867 | `6f322a3c6d2bf4bd0d31ca6aa7a5f69b4e9196166ccf870e607f8b2865a7c234` |
| `book-pictures-20231003-part004.parquet` | 12,815,760 | `580d97d5a920adca07ccbcf4fe66aa311b8a0c1c1732c89dca1a72a689e729b4` |
| `book-pictures-20231003-part005.parquet` | 12,521,850 | `1730c34f1b071cc85e54053d27bc578daa19401e9f4c1efae9bc6b4d400efd26` |
| `book-pictures-20231003-part006.parquet` | 12,301,738 | `60bd49e24099e6b747db39004ffbe1a07683e2a08c985b0805f00c35e5ad164c` |
| `book-pictures-20231003-part007.parquet` | 11,244,139 | `4bf6f72e541263675e014fa9b8ea52c39ccb83ae5818476d1d37ed1f9a853e33` |
| `book-pictures-20231003-part008.parquet` | 11,618,127 | `8cbac7d164a8ebdb3e006b70a8894e5bcbdcb9e42c394eebeaaf53d4921269a0` |
| `book-pictures-20231003-part009.parquet` | 10,871,933 | `43a2ca2ef027647bb4a909ce5b5c6245bbc18bc6093d101cf4ba1b82cd75608a` |
| `book-pictures-20231003-part010.parquet` | 10,309,376 | `687f0522e2ac16d6c6cc6d717963eab651f17c3b63f0e0fc6f5bec4ca11d3dfb` |
| `book-pictures-20231003-part011.parquet` | 12,376,914 | `a65610a119d6c989b33167bd63ac2307b636251a881f6b8d42ba3c009f35b220` |
| `book-pictures-20231003-part012.parquet` | 2,103,777 | `2efbaf418f271dee1b2a58fe275eadf0de1a1a58a3492a2ad5371a588aa656a9` |
| `calc-flow_peak-20231003-part000.parquet` | 865,259 | `22c6021cfc7b6fc7717ed07805ed09dd0e6bcb0286e689445b14349c100585f2` |
| `calc-flow_peak-20231003-part001.parquet` | 905,209 | `d0c991aeb9f4e6132b0f899ed28348877af19c08fe27a6e03af9bdcc22d406c2` |
| `calc-flow_peak-20231003-part002.parquet` | 952,173 | `900985a9326ba349913acb4f8ba03259d7e09b378377f5111c9e355fea43bb88` |
| `calc-flow_peak-20231003-part003.parquet` | 378,209 | `2b8ce5a2a92e22ca4bafa4a259c20d71c134b4cd23027d987ff1d14113e92f50` |
| `calc-peak_story-20231003-part000.parquet` | 544,773 | `96c03b062293f9a9aed2bbbdcf600ab51c2658340eb157e685a0945ae0094199` |
| `calc-peak_story-20231003-part001.parquet` | 546,528 | `cd6ee3b9959670a610532ca3ef684714130c08e6709042c7dca121430b3f98bc` |
| `calc-peak_story-20231003-part002.parquet` | 547,481 | `1a4bc5a7b6382c8d0a25b25700b451d69224a8d96a0f5d28bfc03684234e66ff` |
| `calc-peak_story-20231003-part003.parquet` | 281,289 | `be27355072a51ddefe21c479886bca8f7d3a735d2ccc8e84f3fb88bfca26fceb` |
| `calc-peak_story-facts-20231003-part000.parquet` | 1,874,054 | `1b402027e954cffb905dee93e0ef8ee429b99cd535a53251b6bfadfb7b25e806` |
| `calc-peak_story-open-at-the-end-20231003-part000.parquet` | 1,110 | `f25e3b1e1912c14f029cb92b88e2d51e14c6886b39bf23010a0c6dcd9294d853` |
| `playback-20231003.json` | 665 | `3b3887a39333a6c9f413048ffe7bac1ceaada3984fd127b23870f17c896c9853` |
| `rows-20231003-part000.parquet` | 20,012,767 | `b966a6f7145eb70f50e444ca0dd7dcec20e479d77247cd087d9d4873e7aab995` |
| `rows-20231003-part001.parquet` | 20,119,090 | `17bddfe9a6d9640c5b0a8f0d1880b5c4c698a7c4fcd8b1f3f8cdd53b2cf76d98` |
| `rows-20231003-part002.parquet` | 20,331,880 | `3be73726c98238d760079b31eee002cd7a2c867acf7048b193e51295bc0ac7f3` |
| `rows-20231003-part003.parquet` | 7,711,059 | `bb39165ae86256f4dfd3fa20cbea8a29df82fd1adfb0783c38ddf5c4b5474cde` |
| `vendor-restatements-20231003.parquet` | 24,587 | `76762a2a2f0ad22ffed9fc2e4d67c8e6b8d3a451a53cd6c622a9ba3f1a6179cb` |
