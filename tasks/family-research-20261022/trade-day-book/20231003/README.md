# Book record at every trade, trade day 20231003

One row per trade: the full book at the moment the trade arrives, on the trade-day book (warmed from the Sunday
open, carried through every 00:00 UTC). 100 trades per file, in trade order. MANIFEST.json lists every file with its
size and SHA256; BOOK_RECEIPT.json holds the counts and checks.

Built by tasks/family-research-20261022/research-union-current/trade-day-rebuild-20261116/scripts/build_book_records.py
on branch ccr-349e2ffe-07p8od. Fetch one file at a time; do not fetch this branch whole.
