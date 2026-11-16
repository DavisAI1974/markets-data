"""Run the unchanged Nov-9 second-set replay (recover_second_set.py) with inputs read from the local
markets-data git objects instead of raw.githubusercontent (same repo, same pinned revisions, same bytes)."""
import hashlib, subprocess, sys
sys.path.insert(0, '/home/user/work/pins')
# The package __init__ imports the torch trunk (model code, unused by the teacher equations). Register the
# package without executing __init__ so only the teacher/adapter modules load; no calculation code is altered.
import types, importlib
import research, research.kalshi
sys.path.insert(0, '/home/user/work/pins/research/kalshi/frankie_boss')   # the teacher modules import siblings by bare name
sys.path.insert(0, '/home/user/work/pins/research')
# torch is only used by the teachers' attach()/_target() (tensor packing for the model), never by iter_raw, which is
# the only path this replay runs. A fail-closed stand-in satisfies the import; ANY use raises instead of diverging.
class _NoTorch(types.ModuleType):
    def __getattr__(self, name):
        if name.startswith('__'): raise AttributeError(name)
        raise RuntimeError('torch.%s was used: the raw-component replay must not touch torch' % name)
sys.modules['torch'] = _NoTorch('torch')
_pkg = types.ModuleType('research.kalshi.frankie_boss'); _pkg.__path__ = ['/home/user/work/pins/research/kalshi/frankie_boss']
sys.modules['research.kalshi.frankie_boss'] = _pkg
from research.kalshi.frankie_boss.four_day_pins import recover_book_layers as RBL
REPOS = {RBL.D: '/home/user/markets-data', RBL.M: '/home/user/Markets'}
def fetch(repo, revision, path):
    data = subprocess.check_output(['git', '-C', REPOS[repo], 'show', f'{revision}:{path}'])
    if path.endswith('/RECOVERY_RECEIPT.json'):
        # The Oct 3/17/18 archive receipts omit three keys the Oct 2 one carries. Fill them from the same archive:
        # trade count and scope from the receipt's own top level, last receive clock from the final message shard.
        import json, gzip, io
        r = json.loads(data); o = r['original_replay_receipt']
        if 'trades' not in o: o['trades'] = r['expected_trades']
        if 'scope' not in o: o['scope'] = r['scope']
        if 'last_ts_recv_ns' not in o:
            base = path.rsplit('/', 1)[0]
            man = json.loads(subprocess.check_output(['git', '-C', REPOS[repo], 'show', f'{revision}:{base}/MANIFEST.json']))
            last = [f['path'] for f in man['files'] if f['path'].startswith('native-messages-')][-1]
            blob = subprocess.check_output(['git', '-C', REPOS[repo], 'show', f'{revision}:{base}/{last}'])
            lines = gzip.GzipFile(fileobj=io.BytesIO(blob)).read().splitlines()
            o['last_ts_recv_ns'] = json.loads(lines[-1])['original_message']['ts_recv_ns']
        return json.dumps(r).encode()
    RBL.READS.append(dict(repository=repo, revision=revision, path=path, bytes=len(data),
                          sha256=hashlib.sha256(data).hexdigest()))
    return data
RBL.fetch = fetch
from research.kalshi.frankie_boss.four_day_pins import recover_second_set as RSS
RSS.fetch = fetch
import argparse
p = argparse.ArgumentParser(); p.add_argument('output'); p.add_argument('--limit', type=int)
p.add_argument('--max-seconds', type=float); p.add_argument('--resume-from'); p.add_argument('--resume-sha256')
p.add_argument('--day'); p.add_argument('--revision'); p.add_argument('--manifest-sha256')
a = p.parse_args()
if a.day:   # same code, another day's pinned archive (module constants are read at call time)
    RSS.DAY = a.day; RSS.REVISION = a.revision; RSS.MANIFEST_SHA256 = a.manifest_sha256
    RSS.SOURCE = f'tasks/family-research-20261022/frankie-four-day-pins/book-recovery-42617700678-1/{a.day}'
RSS.main(a.output, a.limit, a.max_seconds, a.resume_from, a.resume_sha256)
