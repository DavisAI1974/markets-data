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
- Part 2, the calculation `flow_peak` (the flow and the exhaustion peak; laid out and approved by Greg 2026-11-16, `STEP1_STEP2_LAYOUTS.md` piece 1; Markets `5aff999`): `calc-flow_peak-*.parquet`, one file beside each rows file, in the same row order, with the position on the tape and 12 new columns. 9,910 peaks became known in the trade day. Rows of no trade day hold empty cells. Check in `CALC-flow_peak-20231003.json`, passed: every column recounted from the stored rows by a different method and equal on all 879,497 rows; playback equal at two cuts.

| File | Bytes | SHA256 |
|---|---:|---|
| `CALC-flow_peak-20231003.json` | 4,563 | `0250a73be517a0b71baffd01393201c3128c28140b77db9f4c43fc4423661928` |
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
| `calc-flow_peak-20231003-part000.parquet` | 854,197 | `ce21690fa54721482b3b20eb2096f9e24d9dad41705ddd192fe579414326d791` |
| `calc-flow_peak-20231003-part001.parquet` | 896,017 | `45bb72f6d13d2c3f5af05c65fef3a8ea36ab8df596f17b5a85750120f2668631` |
| `calc-flow_peak-20231003-part002.parquet` | 941,884 | `b8dcb94122c193504ff01bf887f26a6e20236c6e7be02742d32520ad45e0f376` |
| `calc-flow_peak-20231003-part003.parquet` | 374,331 | `497d7d87e0ac425283440b2693942c8ed4fa4a14da58639eff361c128f0fb234` |
| `playback-20231003.json` | 665 | `3b3887a39333a6c9f413048ffe7bac1ceaada3984fd127b23870f17c896c9853` |
| `rows-20231003-part000.parquet` | 20,012,767 | `b966a6f7145eb70f50e444ca0dd7dcec20e479d77247cd087d9d4873e7aab995` |
| `rows-20231003-part001.parquet` | 20,119,090 | `17bddfe9a6d9640c5b0a8f0d1880b5c4c698a7c4fcd8b1f3f8cdd53b2cf76d98` |
| `rows-20231003-part002.parquet` | 20,331,880 | `3be73726c98238d760079b31eee002cd7a2c867acf7048b193e51295bc0ac7f3` |
| `rows-20231003-part003.parquet` | 7,711,059 | `bb39165ae86256f4dfd3fa20cbea8a29df82fd1adfb0783c38ddf5c4b5474cde` |
| `vendor-restatements-20231003.parquet` | 24,587 | `76762a2a2f0ad22ffed9fc2e4d67c8e6b8d3a451a53cd6c622a9ba3f1a6179cb` |
