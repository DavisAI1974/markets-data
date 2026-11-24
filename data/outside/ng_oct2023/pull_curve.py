"""Pull the futures-curve source files from Databento: every natural gas contract month (NG.FUT, the parent symbol),
one native file per UTC clock day per schema, kept byte for byte as delivered. Nothing is converted, parsed into
values, sampled or dropped; the only reading done here is opening each file to count its records for the manifest.

Schemas: definition (which contract months exist and when each expires), statistics (settlement prices, open interest
and the exchange's other statistics, each with its own time), trades (every trade of every month).

The whole request is quoted first and refused above CEILING_USD. A file already in the manifest is never bought again.
The key is not in this program: the cloud environment's network supplies it, so the client is given a placeholder.

    python3 pull_curve.py --out <this folder> --quote-only
    python3 pull_curve.py --out <this folder>
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import sys
from pathlib import Path

import databento as db

DATASET, SYMBOL, STYPE = 'GLBX.MDP3', 'NG.FUT', 'parent'
CEILING_USD = 1.00                       # Greg approved "about $0.80" on 2026-11-16
# UTC clock days. The four trade days are covered by Oct 1 to 3 and Oct 16 to 18. Sep 29 is the Friday before trade
# day Mon Oct 2 (its settlement is the last one known when that trade day opens); Sep 30 is taken for definitions
# and statistics in case a Friday settlement message is stamped after midnight UTC.
DAYS = {
    'definition': ['20230929', '20230930', '20231001', '20231002', '20231003', '20231016', '20231017', '20231018'],
    'statistics': ['20230929', '20230930', '20231001', '20231002', '20231003', '20231016', '20231017', '20231018'],
    'trades': ['20230929', '20231001', '20231002', '20231003', '20231016', '20231017', '20231018'],
}


def span(day: str) -> tuple[str, str]:
    start = dt.date(int(day[:4]), int(day[4:6]), int(day[6:]))
    return start.isoformat(), (start + dt.timedelta(days=1)).isoformat()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    ap.add_argument('--quote-only', action='store_true')
    args = ap.parse_args()
    out = Path(args.out)
    manifest_path = out / 'MANIFEST.json'
    manifest = json.loads(manifest_path.read_text())
    have = {f['stored'] for f in manifest['files']}
    client = db.Historical('db-' + 'x' * 29)          # placeholder; the network supplies the real key

    todo, total = [], 0.0
    for schema, days in DAYS.items():
        for day in days:
            stored = f'raw/curve/NG_FUT_{schema}_{day}.dbn.zst'
            if stored in have:
                continue
            start, end = span(day)
            cost = client.metadata.get_cost(dataset=DATASET, symbols=[SYMBOL], stype_in=STYPE, schema=schema,
                                            start=start, end=end)
            total += cost
            todo.append((schema, day, start, end, stored, cost))
            print(f'quote {schema} {day}: ${cost:.4f}', flush=True)
    print(f'quoted total for {len(todo)} files: ${total:.4f} (ceiling ${CEILING_USD:.2f})', flush=True)
    if total > CEILING_USD:
        sys.exit('refused: the quote is above the ceiling')
    if args.quote_only:
        return

    for schema, day, start, end, stored, cost in todo:
        path = out / stored
        path.parent.mkdir(parents=True, exist_ok=True)
        when = dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        store = client.timeseries.get_range(dataset=DATASET, symbols=[SYMBOL], stype_in=STYPE, schema=schema,
                                            start=start, end=end, path=str(path))
        raw = path.read_bytes()
        records, first, last = 0, None, None
        for rec in store:
            records += 1
            first = rec.ts_event if first is None else first
            last = rec.ts_event
        entry = dict(family='curve', address=f'Databento {DATASET} {SYMBOL} (stype {STYPE}) schema={schema} '
                                             f'start={start} end={end}, native DBN, zstd',
                     retrieved_utc=when, quoted_usd=round(cost, 6), bytes_as_served=len(raw),
                     sha256_as_served=hashlib.sha256(raw).hexdigest(),
                     check=f'file opens as {store.schema} with {records} records'
                           + (f'; exchange times {first} to {last} (UTC ns)' if records else
                              '; no records (the market was closed for the whole clock day)'),
                     stored=stored, stored_as='the bytes as served', stored_bytes=len(raw),
                     stored_sha256=hashlib.sha256(raw).hexdigest())
        manifest['files'].append(entry)
        manifest_path.write_text(json.dumps(manifest, indent=1) + '\n')
        print(f'ok {stored}  {len(raw)} bytes  {records} records', flush=True)
    print(f'done: {len(manifest["files"])} files held')


if __name__ == '__main__':
    main()
