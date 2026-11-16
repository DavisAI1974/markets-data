"""Fetch from the EIA data service what the original outside-data files took from it, exactly as served:

  eia930   hourly generation by fuel (fuel-type-data) and hourly demand and generation (region-data) for the seven
           respondents the original used, US48 first: this is the EIA's own US48 figure.
  storage  the weekly Lower-48 working gas series (the current, revised history; the figures as first printed come
           from raw/storage/revisions.xls, not from here).

Every response page is stored as served and listed in MANIFEST.json. The key is read from the environment variable
EIA_API_KEY and is never written anywhere: the recorded address leaves it out, and a page that contained it would be
refused, not stored. Nothing is parsed into values or calculated; pages are opened only to count rows and follow paging.

    EIA_API_KEY=... python3 fetch_eia_api.py --out <this folder>
"""
from __future__ import annotations

import argparse
import datetime as dt
import gzip
import hashlib
import io
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

API = 'https://api.eia.gov/v2'
USER_AGENT = 'Mozilla/5.0 (compatible; research-data-fetch/1.0)'
RESPONDENTS = ['US48', 'ERCO', 'CISO', 'MISO', 'PJM', 'SWPP', 'SOCO']      # the original's seven
# Hourly span, UTC hours: from 8 days before trade day Oct 2 opens (the original's lead) to past the Oct 18 halt.
HOURLY_START, HOURLY_END = '2023-09-23T00', '2023-10-19T00'
STORAGE_SERIES = 'NW2_EPG0_SWO_R48_BCF'
STORAGE_START = '2017-09-01'                 # the five-year comparison needs five earlier years
PAGE = 5000


def gz(raw: bytes) -> bytes:
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode='wb', mtime=0, compresslevel=9) as fh:
        fh.write(raw)
    return buf.getvalue()


def get(route: str, params: list[tuple[str, str]], key: str) -> bytes:
    url = f'{API}/{route}/data/?' + urllib.parse.urlencode(params + [('api_key', key)])
    last = None
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
            with urllib.request.urlopen(req, timeout=180) as resp:
                return resp.read()
        except Exception as err:
            last = type(err).__name__                       # never the address: it carries the key
        time.sleep(5 * (attempt + 1))
    raise RuntimeError(f'EIA {route}: request failed ({last})')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    key = os.environ.get('EIA_API_KEY', '')
    if not key:
        sys.exit('EIA_API_KEY is not set')
    out = Path(args.out)
    manifest_path = out / 'MANIFEST.json'
    manifest = json.loads(manifest_path.read_text())
    have = {f['stored'] for f in manifest['files']}

    jobs = []
    for route in ('fuel-type-data', 'region-data'):
        for ba in RESPONDENTS:
            jobs.append(('eia930', f'electricity/rto/{route}', f'eia930_{route}_{ba}',
                         [('frequency', 'hourly'), ('data[]', 'value'), ('facets[respondent][]', ba),
                          ('start', HOURLY_START), ('end', HOURLY_END),
                          ('sort[0][column]', 'period'), ('sort[0][direction]', 'asc')]))
    jobs.append(('storage', 'natural-gas/stor/wkly', f'eia_weekly_{STORAGE_SERIES}',
                 [('frequency', 'weekly'), ('data[0]', 'value'), ('facets[series][]', STORAGE_SERIES),
                  ('start', STORAGE_START), ('sort[0][column]', 'period'), ('sort[0][direction]', 'asc')]))

    for family, route, stem, params in jobs:
        offset, page, total = 0, 0, None
        while total is None or offset < total:
            stored = f'raw/{family}/api/{stem}_page{page:02d}.json.gz'
            paged = params + [('length', str(PAGE)), ('offset', str(offset))]
            address = f'{API}/{route}/data/?' + urllib.parse.urlencode(paged)          # recorded without the key
            if stored in have:
                entry = next(f for f in manifest['files'] if f['stored'] == stored)
                rows, total = entry['rows'], entry['total_rows']
            else:
                when = dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
                raw = get(route, paged, key)
                if key.encode() in raw:
                    sys.exit(f'refused: the response for {stem} contains the key; nothing stored')
                resp = json.loads(raw)['response']
                rows, total = len(resp['data']), int(resp['total'])
                body = gz(raw)
                path = out / stored
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(body)
                manifest['files'].append(dict(
                    family=family, address=address + '  (the key is left out of this record)', retrieved_utc=when,
                    http_status=200, bytes_as_served=len(raw), sha256_as_served=hashlib.sha256(raw).hexdigest(),
                    check=f'JSON response opens; {rows} rows on this page, {total} rows in all', rows=rows,
                    total_rows=total, stored=stored, stored_as='gzip of the bytes as served', stored_bytes=len(body),
                    stored_sha256=hashlib.sha256(body).hexdigest()))
                manifest_path.write_text(json.dumps(manifest, indent=1) + '\n')
                print(f'ok {stored}  {rows} rows of {total}', flush=True)
                time.sleep(1.0)
            if rows == 0:
                break
            offset += rows
            page += 1
    print(f'done: {len(manifest["files"])} files held')


if __name__ == '__main__':
    main()
