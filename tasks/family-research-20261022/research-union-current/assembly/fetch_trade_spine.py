from acquire import *
import pyarrow.parquet as pq, collections
a=json.loads((ROOT/'source_inventory.json').read_text())
rows=[r for r in a if '/frankie-four-day-pins/run-42608467894-1/' in r['path'] and r['path'].endswith('.parquet')]
def one(r):
    f=download(r['repo'],r['ref'],r['path'],ROOT/'objects'/r['sha'])
    data=f.read_bytes();assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==r['sha']
    return r['id']
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
    done=list(pool.map(one,rows))
print('trade shards fetched',len(done))
r=rows[0];t=pq.read_table(ROOT/'objects'/r['sha']);print('columns',t.schema.names);print('sample',str(t.slice(0,1).to_pylist())[:3000])
