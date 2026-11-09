from acquire import ROOT
import json,csv,pathlib,collections,bisect,heapq,hashlib
import pyarrow.parquet as pq
OUT=ROOT/'current';src=json.loads((ROOT/'active_sources.json').read_text())
base=pathlib.Path('E:/markets-data-frankie-audit-20261109/tasks/family-research-20261022/whole-lifecycles/run-42573465249-1')
summary=[];gaps=[];maps=[];candidate_rows=[]
trade_rows=list(csv.DictReader((OUT/'trade_spine.csv').open()))
for day in ['20231002','20231003','20231017','20231018']:
    d=base/f'audit-{day}'
    lif=pq.read_table(d/'whole-lifecycles.parquet').to_pylist()
    windows={r['parent_id']:r for r in pq.read_table(d/'component-windows.parquet').to_pylist()}
    candidates=[r for r in lif if r['kind']=='candidate']
    # An interval association is descriptive coverage, never proof the signal was known at the trade.
    intervals=[]
    for r in candidates:
        w=windows.get(r['parent_id']);start=w['first_cut_ns'] if w else r['anchor_label_ns']
        end=r['lifecycle_end_label_ns'];pre=bool(w and w['starts_before_lifecycle'])
        complete=bool(r['complete_original_second_sequence'] and pre and r['lifecycle_end_known_by_ns'] is not None)
        intervals.append((int(start),int(end),r['parent_id'],complete))
        candidate_rows.append([day,r['candidate_id'],str(start),str(r['anchor_label_ns']),str(end),str(r['recognition_ns'] or ''),str(r['lifecycle_end_known_by_ns'] or ''),pre,bool(r['complete_original_second_sequence']),complete,r['endpoint_definition']])
    intervals.sort();active={};ending=[];j=0;c=collections.Counter()
    for t in sorted([t for t in trade_rows if t['day']==day],key=lambda r:int(r['receive_ns'])):
        now=int(t['receive_ns'])
        while j<len(intervals) and intervals[j][0]<=now:
            start,end,pid,full=intervals[j];active[pid]=(end,full);heapq.heappush(ending,(end,pid));j+=1
        while ending and ending[0][0]<now:
            end,pid=heapq.heappop(ending)
            if active.get(pid,(None,))[0]==end:active.pop(pid,None)
        allids=sorted(active);fullids=[i for i in allids if active[i][1]]
        status='Covered by saved prebirth and complete observed lifecycle' if fullids else 'Mapped lifecycle has a missing segment' if allids else 'No saved candidate interval covers this trade'
        row=[day,t['trade_id'],t['receive_ns'],t['known_by_ns'],status,len(allids),';'.join(allids),';'.join(fullids)]
        maps.append(row);c[status]+=1
        if not fullids:gaps.append(row)
    summary.append({'day':day,'trades':sum(c.values()),'saved_candidate_lifecycles':len(candidates),**dict(c)})
head=['day','trade_id','trade_receive_ns_exact','trade_known_by_ns_exact','mapping_status','candidate_intervals','all_parent_ids','complete_parent_ids']
for name,rs in [('trade_dipole_map.csv',maps),('dipole_trade_gaps.csv',gaps)]:
    with (OUT/name).open('w',newline='',encoding='utf-8') as f:w=csv.writer(f);w.writerow(head);w.writerows(rs)
with (OUT/'dipole_lifecycle_index.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f);w.writerow(['day','candidate_id','prebirth_start_ns','birth_label_ns','end_label_ns','recognition_ns','end_known_by_ns','prebirth_saved','sequence_complete','prebirth_through_end_saved','endpoint_definition']);w.writerows(candidate_rows)
(OUT/'dipole_gap_summary.json').write_text(json.dumps(summary,indent=2))

states=json.loads((ROOT/'second_set_states.json').read_text())
schema=json.loads((ROOT/'table_schemas.json').read_text())
layer=[]
for r in states[1:]:
    if r[1]!='last_completed_group_before_trade':continue
    name=r[2].split(' | ')[1]
    hits=[t['id'] for t in schema if name in t['fields']]
    layer.append([r[2],r[0],r[1],r[3],r[4],';'.join(hits),'No exact named field found in 674 research-table schemas' if not hits else 'Exact name found; compare definition and clock', 'Existing Oct18 values can be joined where present; missing dates or states need source recovery before new calculation'])
with (OUT/'nineteen_field_reuse.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f);w.writerow(['field','saved_day','saved_phase','present','missing','exact_field_source_ids','reuse_evidence','next_action']);w.writerows(layer)

queue=[
 ['G01','Every-trade dipole map','All four days',len(gaps),'dipole_trade_gaps.csv','Recover prebirth, birth, recognition, continuation and terminal observations for each listed trade; preserve overlaps and no-dipole observations.','Every trade has an explicit result; source clocks and complete path or precise missing segment are recorded.'],
 ['G02','19-field reuse and bindings','All four days',19,'nineteen_field_reuse.csv','Inspect existing 19-field values, both new workflow outputs, original order queues and structural histories before launching replay. Reuse exact equivalent values; do not treat a related feature as equivalent.','Per field: definition, units, lookback, row/phase key, availability clock, existing coverage, missing operands and cheapest necessary calculation.'],
 ['G03','Clock and relative-offset repairs','All four days','See clock_gaps.csv','clock_gaps.csv','Resolve float/scientific-notation clocks by source cursor or record identity; verify session origins, duration offsets and second-boundary meanings. Replace incorrect current values.','Every corrected record enters the Excel pins; scheduled cutoffs and observed endpoints remain distinct; no stale alternatives.'],
 ['G04','Both new workflow outputs','Exact runs to be bound','Run inventory','source_catalog.json','Bind the exact two completed/current calculation outputs by run and commit, ingest every output field, join event clocks and attach aggregates. Audit whether they close G01/G02/G05/G06.','Each output row is pinned or attached; run completeness, exact source hashes and gap closure counts verified.'],
 ['G05','Full order and FIFO context','All four days','Per-trade gaps','trade_spine.csv','Recover order identity, age, size, priority loss, volume ahead, refill/depletion and reset continuity at each decision clock from retained full-book/order sources.','Exact trade/cursor binding and missing/reset states; no top-of-book proxy substituted for far-queue definitions.'],
 ['G06','External-point availability','All four days',13,'Existing workbook: Recovered external / Forecast recovered / Disagreement recovered','Recover original publication/dissemination timestamps and contract/expiry matches for weather, model disagreement, COT, EIA and curve context; retain modeled clocks as modeled until replaced.','All 13 fields retain source, units, valid date and first availability; absent or modeled publication evidence is explicit.'],
 ['G07','99-layer per-trade bindings','All four days',99,'Existing workbook: Layer directory / Layer coverage','Replace example-only coverage with full trade-level values or exact evidence links; distinguish static knowledge, computed market observations and runtime receipts.','All 143270 saved trades have a state for every named layer; no placeholder presented as a computed value.'],
 ['G08','Research attachment and field closure','All four days','All retained sources','source_catalog.json / field_inventory.csv','Keep comparisons, correlations, controls and every candidate family attached with their full denominators and fields; resolve unresolved variables without ranking candidates out.','All source rows reconcile to pinned + attached rows; every field preserved; all candidates passed to paper testing.'],
]
with (OUT/'research_gap_queue.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f);w.writerow(['gap_id','workstream','scope','affected_count','input','work','completion_check']);w.writerows(queue)
text='''# CCode gap-filling handoff

Use the corrected current workbook and companion data. Do not use CCode reanalysis opinions to admit or reject research. Every candidate, comparison and correlation stays available; paper trades determine performance. Do not start a multi-day replay before the reuse audit.

The queue is `research_gap_queue.csv`. `dipole_trade_gaps.csv` gives the exact saved trades requiring map completion. Coverage is a descriptive interval association, not proof that a candidate was causally known at a trade. The current endpoint convention is `opposite_hold3`; do not describe that convention as an independently established natural death.

Start with G02 and G04: check both new workflow calculations and the saved 19-field values. For each missing field, establish whether the value exists, whether only a join is missing, or whether new calculation is necessary. Supply required operands and an estimate from retained data before proposing an expensive run. Preserve negative, flat, adverse and conflicting research.

Fix verified errors in place in the current data. Keep one corrected record, with source identity and correction method; do not retain a second faulty value in the active workbook. Include corrected records in the pins. Do not replace unresolved clocks with guessed timestamps.

G01 then closes dipole maps from prebirth through observed end for every trade/date. Identify missing segments and source coverage, and explicitly record when no observed dipole exists. Never invent a dipole to fill a cell. G03/G05/G06/G07/G08 close the other evidence gaps using the completion checks in the queue.

Twenty newly supplied price-response examples have been independently verified against original path, group and raw rows. Sixteen scheduled-cutoff export values were corrected; all 20 observed endpoint receive clocks were recovered. Use `corrected_price_response.json`.

No new research or replay job was launched for this assembly. The pre-existing October 2 second-set workflow was still running when inspected; its unfinished outputs are not a completed result.
'''
(OUT/'CCODE_GAP_FILLER_HANDOFF.md').write_text(text,encoding='utf-8')
print(json.dumps(summary),flush=True);print('gap trades',len(gaps),'queue',len(queue))
