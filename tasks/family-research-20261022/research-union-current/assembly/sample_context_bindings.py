from acquire import ROOT
import json,csv,gzip
O=ROOT/'current';S=json.loads((ROOT/'expanded_sources.json').read_text());by={s['id']:s for s in S}
s=by['S13083'];rs=list(csv.DictReader((ROOT/'objects'/s['sha']).open()));assert len({r['sample_id'] for r in rs})==len(rs)
with (O/'original_sample_context_bindings.csv').open('w',newline='',encoding='utf8') as f:
 heads=['source_id','session_day','sample_id','family_id','phase','cutoff_ns_exact','cursor_cap','clock_meaning','source_url'];w=csv.writer(f);w.writerow(heads)
 for r in rs:w.writerow([s['id'],'20231018',r['sample_id'],r['family_id'],r['phase'],r['cutoff_ns'],r['cursor_cap'],'Sample context cutoff; individual source observations retain their own clocks',s['url']])
print('Original sample cutoff bindings',len(rs))
