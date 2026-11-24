"""Fetch the published source files that sit under the outside data points, exactly as served. Nothing is parsed into
values, nothing is calculated, nothing is filtered: this only downloads, checks that each file is what it claims to be,
and writes MANIFEST.json (address requested, retrieval time, status, bytes and SHA256 as served, where it is stored).

Scope: the four trade days Mon Oct 2, Tue Oct 3, Tue Oct 17 and Wed Oct 18, 2023 (a trade day runs 6 pm Eastern the
evening before to 5 pm Eastern on the named date). The spans fetched are wider than the trade days so that every window
a later step may declare is covered; the spans are stated in SPANS below and in the manifest.

Every file is the source's CURRENT revision on the retrieval date. A source that keeps only revised figures cannot give
the figure as first published; the manifest says so per family.

    python3 fetch_sources.py --out <this folder>            # fetch everything not already in the manifest
    python3 fetch_sources.py --out <this folder> --only cot  # one family
"""
from __future__ import annotations

import argparse
import datetime as dt
import gzip
import hashlib
import io
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

USER_AGENT = 'Mozilla/5.0 (compatible; research-data-fetch/1.0)'
RETRIEVED_NOTE = 'current revision of the source on the retrieval date'

# The 16 stations of the gas-weighted temperature (the station list of the weather feed; weights are not used here).
STATIONS = ['NYC', 'BOS', 'PHL', 'DCA', 'ORD', 'DTW', 'MSP', 'STL', 'IAH', 'DFW', 'ATL', 'DEN', 'PHX', 'LAX', 'SFO',
            'SEA']
# Two more cities whose hourly temperatures the original files carried beside each row (they have no weight).
EXTRA_STATIONS = ['AUS', 'SAT']
MOS_MODELS = ['GFS', 'NAM', 'MEX']           # the three forecast-statistics products behind X02 and X09
SPANS = {
    'weather_obs': ('2023-09-01T00:00:00Z', '2023-11-01T00:00:00Z'),   # every reading, all report types
    'mos': ('2023-09-20T00:00Z', '2023-10-19T00:00Z'),                 # every model run made in this span
    'cot_years': [2020, 2021, 2022, 2023],                             # covers a 3-year window ending Oct 2023
    'eia930': 'EIA930_BALANCE_2023_Jul_Dec.csv',                       # hourly, every balancing authority
}
IEM = 'https://mesonet.agron.iastate.edu/cgi-bin/request'
IEM_PAUSE_S = 3.0                             # the archive asks for no more than one request a second


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def get(url: str, tries: int = 4) -> tuple[int, str, bytes]:
    last = None
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
            with urllib.request.urlopen(req, timeout=300) as resp:
                return resp.status, resp.headers.get('Content-Type', ''), resp.read()
        except urllib.error.HTTPError as err:
            last = f'HTTP {err.code}'
            if err.code in (400, 403, 404, 422):
                return err.code, err.headers.get('Content-Type', ''), err.read()
        except Exception as err:                                   # network trouble: wait and try again
            last = repr(err)
        time.sleep(5 * (attempt + 1))
    raise RuntimeError(f'could not fetch {url}: {last}')


def gz(raw: bytes) -> bytes:
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode='wb', mtime=0, compresslevel=9) as fh:   # mtime=0: same bytes every time
        fh.write(raw)
    return buf.getvalue()


# ---- checks: is the file what it claims to be? Each returns a short statement of what was seen, or raises. ----------
def check_zip(raw: bytes) -> str:
    with zipfile.ZipFile(io.BytesIO(raw)) as zf:
        bad = zf.testzip()
        if bad:
            raise ValueError(f'zip member {bad} is damaged')
        return 'zip opens; members: ' + ', '.join(f'{i.filename} ({i.file_size} bytes)' for i in zf.infolist())


def check_text_table(first_field: str, sep: str):
    def check(raw: bytes) -> str:
        head = raw[:4000].decode('utf-8', 'replace')
        line = next((ln for ln in head.splitlines() if ln and not ln.startswith('#')), '')
        if not line.split(sep)[0].strip().strip('"').lower().startswith(first_field.lower()):
            raise ValueError(f'first line does not start with {first_field!r}: {line[:120]!r}')
        return f'table header starts with {first_field!r}; {raw.count(b"\n")} lines'
    return check


def check_xls(raw: bytes) -> str:
    if raw[:8] != b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1':
        raise ValueError('not an Excel 97 workbook (wrong first bytes)')
    return 'Excel 97 workbook signature present'


def check_html(marker: str):
    def check(raw: bytes) -> str:
        if marker.lower().encode() not in raw.lower():
            raise ValueError(f'page does not contain {marker!r}')
        return f'page contains {marker!r}'
    return check


def targets():
    """(family, stored name, address, check, store gzipped?)"""
    out = []
    for year in SPANS['cot_years']:
        out.append(('cot', f'fut_disagg_txt_{year}.zip',
                    f'https://www.cftc.gov/files/dea/history/fut_disagg_txt_{year}.zip', check_zip, False))
    out.append(('cot', 'cftc_release_schedule.html',
                'https://www.cftc.gov/MarketReports/CommitmentsofTraders/ReleaseSchedule/index.htm',
                check_html('Release Schedule'), False))
    for name, check in [('ngshistory.xls', check_xls), ('ngsstats.xls', check_xls), ('cvhistory.xls', check_xls),
                        ('archngshistory.xls', check_xls), ('archngsstats.xls', check_xls),
                        ('archrevisions.xls', check_xls), ('archmthdiff_history.xls', check_xls),
                        ('revisions.xls', check_xls),          # the original estimates of every week later revised
                        ('revisions.html', check_html('revision')), ('schedule.html', check_html('schedule')),
                        ('notes.html', check_html('storage')), ('methodology.html', check_html('methodology')),
                        ('mthdiff.html', check_html('storage'))]:
        out.append(('storage', name, f'https://ir.eia.gov/ngs/{name}', check, False))
    out.append(('storage', 'NW2_EPG0_SWO_R48_BCFw.xls',
                'https://www.eia.gov/dnav/ng/hist_xls/NW2_EPG0_SWO_R48_BCFw.xls', check_xls, False))
    out.append(('eia930', SPANS['eia930'] + '.gz',
                'https://www.eia.gov/electricity/gridmonitor/sixMonthFiles/' + SPANS['eia930'],
                check_text_table('Balancing Authority', ','), True))
    sts, ets = SPANS['weather_obs']
    for st in STATIONS + EXTRA_STATIONS:
        q = urllib.parse.urlencode(dict(station=st, data='all', sts=sts, ets=ets, tz='Etc/UTC', format='tdf',
                                        missing='M', trace='T', latlon='yes', elev='yes'))
        out.append(('weather_obs', f'asos_{st}_20230901_20231101.tsv.gz', f'{IEM}/asos.py?{q}',
                    check_text_table('station', '\t'), True))
    # The same span again with the routine hourly reports only (report type 3), so the routine reading of each hour
    # is identified by the source itself and not by a rule of ours. The all-types files above stay the full record.
    for st in STATIONS + EXTRA_STATIONS:
        q = urllib.parse.urlencode(dict(station=st, data='all', sts=sts, ets=ets, tz='Etc/UTC', format='tdf',
                                        missing='M', trace='T', latlon='yes', elev='yes', report_type='3'))
        out.append(('weather_obs', f'asos_{st}_routine_20230901_20231101.tsv.gz', f'{IEM}/asos.py?{q}',
                    check_text_table('station', '\t'), True))
    sts, ets = SPANS['mos']
    for model in MOS_MODELS:
        for st in STATIONS:
            q = urllib.parse.urlencode(dict(station='K' + st, model=model, sts=sts, ets=ets, format='csv'))
            out.append(('mos', f'mos_{model}_K{st}_20230920_20231019.csv.gz', f'{IEM}/mos.py?{q}',
                        check_text_table('runtime', ','), True))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    ap.add_argument('--only', help='one family: cot, storage, eia930, weather_obs, mos')
    args = ap.parse_args()
    out = Path(args.out)
    manifest_path = out / 'MANIFEST.json'
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {
        'what': 'Published source files under the outside data points, as served. No value here is calculated.',
        'trade_days': ['2023-10-02', '2023-10-03', '2023-10-17', '2023-10-18'],
        'vintage': RETRIEVED_NOTE, 'spans': SPANS, 'files': [], 'refused': []}
    have = {f['stored'] for f in manifest['files']}
    failures = 0
    for family, name, url, check, zipped in targets():
        stored = f'raw/{family}/{name}'
        if (args.only and family != args.only) or stored in have:
            continue
        if 'mesonet.agron.iastate.edu' in url:
            time.sleep(IEM_PAUSE_S)
        when = dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        status, ctype, raw = get(url)
        entry = dict(family=family, address=url, retrieved_utc=when, http_status=status, content_type=ctype,
                     bytes_as_served=len(raw), sha256_as_served=sha256(raw))
        try:
            if status != 200:
                raise ValueError(f'HTTP status {status}')
            entry['check'] = check(raw)
        except Exception as err:
            failures += 1
            entry['reason'] = str(err)
            manifest['refused'] = [r for r in manifest['refused'] if r['address'] != url] + [entry]
            print(f'REFUSED {stored}: {err}', flush=True)
        else:
            body = gz(raw) if zipped else raw
            path = out / stored
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(body)
            entry.update(stored=stored, stored_as='gzip of the bytes as served' if zipped else 'the bytes as served',
                         stored_bytes=len(body), stored_sha256=sha256(body))
            manifest['files'].append(entry)
            manifest['refused'] = [r for r in manifest['refused'] if r['address'] != url]
            print(f'ok {stored}  {len(raw)} bytes  {entry["check"][:90]}', flush=True)
        manifest_path.write_text(json.dumps(manifest, indent=1) + '\n')
    print(f'done: {len(manifest["files"])} files held, {len(manifest["refused"])} refused')
    sys.exit(1 if failures else 0)


if __name__ == '__main__':
    main()
