# Item 6: book-clear records on the seven stored tape files, counted (2026-11-24)

Greg asked whether the books need to be retained when a clear arrives mid-week. Before any design, the stored tape
was counted. The seven files of `data/nymex_mbo/ng_v0_oct2023/` were read record by record with a short script
(the DBN header skipped, then each record's action and flags read from its bytes). No platform code ran and nothing
was written. Every file's record count matched its manifest. Every record on all seven files is an MBO record.

| Tape file | Records | Clear records | Where | Snapshot flag on the clear | Snapshot-flagged records in the file |
| --- | --- | --- | --- | --- | --- |
| `NG_v0_mbo_20231001.dbn.zst` (Sunday) | 12,532 | 1 | the first record | no | 342 |
| `NG_v0_mbo_20231002.dbn.zst` | 813,342 | 1 | the first record | yes | 733 |
| `NG_v0_mbo_20231003.dbn.zst` | 879,077 | 1 | the first record | yes | 741 |
| `NG_v0_mbo_20231015.dbn.zst` (Sunday) | 29,063 | 1 | the first record | no | 350 |
| `NG_v0_mbo_20231016.dbn.zst` | 925,662 | 1 | the first record | yes | 697 |
| `NG_v0_mbo_20231017.dbn.zst` | 858,976 | 1 | the first record | yes | 738 |
| `NG_v0_mbo_20231018.dbn.zst` | 760,803 | 1 | the first record | yes | 718 |

What it shows. The two Sunday files open with a clear that carries no snapshot flag: the exchange's own start-up,
which seats the week's book. The five other files open with a clear that carries the vendor's snapshot flag: the
opening of the vendor's UTC file, which the platform compares with the carried book and never applies. No clear
record comes after a file's first record on any of the seven files. So on the stored tape the book is carried
through every boundary it meets and the silent emptying described in run 62's finding 1 cannot occur. It can on a
true live feed, where nothing marks a restatement; the way to hold the book through such a reset is written under
item 6 of the platform checklist and is not built.
