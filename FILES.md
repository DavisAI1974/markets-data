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

| File | Bytes | SHA256 |
|---|---:|---|
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
| `playback-20231017.json` | 665 | `730534ef97f7ba68f7b3ca9e381ae0723fc360e787b16956ac03927e5aa4177d` |
| `rows-20231017-part000.parquet` | 19,729,598 | `7c1559d5056070a4b91ffd4f7cf2928d1034a54fde3cb3a4e518438372416595` |
| `rows-20231017-part001.parquet` | 20,226,095 | `a30f8b597209bd74a81ec426f678699e61a341099a1b66a9fa6e35299a7057f0` |
| `rows-20231017-part002.parquet` | 20,215,925 | `b1c9b234966d8874d4fec39567dbd483f47da3205209d03ccf57ca065722a36a` |
| `rows-20231017-part003.parquet` | 4,808,580 | `efb7d6338879f8ad53224a307a882f4562cc5aafa797faf3a4ef07ef80c32313` |
| `vendor-restatements-20231017.parquet` | 25,152 | `839562be094b57fb8d241d5df378fa377727cfc6bd72906d080805aafb7840bd` |
