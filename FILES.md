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

| File | Bytes | SHA256 |
|---|---:|---|
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
| `playback-20231018.json` | 666 | `dff963b8f017297e3be9ddd21c68c5ed3d1d7afe470aa63cb0bc13c67c4c8439` |
| `rows-20231018-part000.parquet` | 19,918,917 | `553218f493ba6420dfc957f9adce322ddf8e477ab150f60fc88f97fba635df47` |
| `rows-20231018-part001.parquet` | 20,110,859 | `7cd439efe8f94e71d4612e7d8effe88994ae96b653d724c73749797bd1479975` |
| `rows-20231018-part002.parquet` | 18,971,027 | `4a74d42f71f754bd55db61a627e92cdebe9812faf248b649310462a05703023f` |
| `vendor-restatements-20231018.parquet` | 34,368 | `ceacfad36514edf43a7ba367914f00a6f79eab37a3276fc07fa0dff223eb43b7` |
