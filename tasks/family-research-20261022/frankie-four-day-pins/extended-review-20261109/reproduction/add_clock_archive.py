"""Build a complete file and table index of the late-session clock archive."""

import json
import re

from add_workflow_review import DAYS, PREFIX, REPO, REV, ROOT, url


OMIT = re.compile(r'(?:b-delayed-outcomes|cross-study-condition-outcomes)\.parquet(?:$|/)')
ARCHIVED = '/whole-lifecycles/'
CLOCK_ROOT = 'all-row-clock-pins/run-42584823565-1'


def read(name):
    return json.loads((ROOT / name).read_bytes())


def main():
    tables = []
    excluded = set()
    prior = set()
    for day in (*DAYS, 'cross'):
        for item in read(f'clock-catalog-{day}.json'):
            source = item['source']
            path = source['path']
            table_id = item['table_id']
            if OMIT.search(path):
                excluded.add((day, table_id))
                continue
            if ARCHIVED in path:
                prior.add((day, table_id))
                continue
            counts = item['counts']
            tables.append([
                day, source['collection'], table_id, path, counts.get('rows', 0),
                counts.get('clocks', 0), counts.get('corrections', 0),
                len(item['parts']), source['git_blob'],
                f"https://github.com/{source['repository']}/blob/{source['revision']}/{path}",
                url(f'{CLOCK_ROOT}/{day}/rows/{table_id}/TABLE.json'),
            ])
    files = []
    for directory, role in (
        ('all-row-clock-pins', 'Clock archive. Use the table-level clock roles.'),
        ('claude-code-pins', 'Corrected exact Tier 1 nanosecond pins.'),
        ('timestamp-pins', 'Timestamp inventory and verification.'),
        ('codex-trade-environment', 'Trade environment field inventory.'),
        ('layer-wiring-repair', 'Layer wiring and payload schema audit.'),
    ):
        tree = read(f'tree-{directory}.json')
        assert not tree['truncated'], directory
        for entry in tree['tree']:
            if entry['type'] != 'blob':
                continue
            part = entry['path'].split('/')
            if len(part) > 3 and part[2] == 'rows' and (part[1], part[3]) in excluded | prior:
                continue
            path = directory + '/' + entry['path']
            use = role
            if directory == 'all-row-clock-pins' and not any(p == 'rows' for p in part):
                use = 'Archive catalog for provenance. Apply the exclusions in this workbook before use.'
            day = next((d for d in DAYS if d in path or f'oct{d[-2:]}' in path), None)
            files.append([day, path, entry['size'], entry['sha'], REV, use, url(path)])
    main = read('tree-main-late.json')
    assert not main['truncated']
    commit = 'c01caaf4f327e8fdff21e4e8b9c5153aba8604a8'
    for entry in main['tree']:
        path = entry['path']
        if entry['type'] != 'blob' or not path.startswith(PREFIX + '/claude-code-'):
            continue
        day = next((d for d in DAYS if d in path or f'oct{d[-2:]}' in path), None)
        role = ('Earlier ledger for provenance. Use the corrected pins where present.'
                if '/claude-code-pins/' in path else 'Original case research and reference draws.')
        files.append([day, path.removeprefix(PREFIX + '/'), entry['size'], entry['sha'], commit, role,
                      f'https://github.com/{REPO}/blob/{commit}/{path}'])
    assert len(tables) + len(excluded) + len(prior) == 553
    output = {
        'Late-session clock tables': {
            'headers': ['Date or cross-day shard', 'Source collection', 'Table ID', 'Original Git path',
                        'Source rows', 'Clock entries', 'Clock corrections', 'Clock parts', 'Source Git blob',
                        'Original immutable source', 'Immutable table clock metadata'],
            'rows': tables,
        },
        'Late-session clock files': {
            'headers': ['Trading date', 'Git file', 'Bytes', 'Git blob ID', 'Commit', 'Use boundary',
                        'Immutable URL'],
            'rows': files,
        },
    }
    (ROOT / 'LATE_CLOCK_TABLES.json').write_text(json.dumps(output), encoding='utf-8')
    print({k: len(v['rows']) for k, v in output.items()})
    print(f'{len(excluded)} delayed outcome tables and {len(prior)} prior second-workflow tables excluded')


if __name__ == '__main__':
    main()
