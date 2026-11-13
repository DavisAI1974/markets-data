"""Prepare exact cell replacements and complete in-workbook source payloads."""
import collections
import gzip
import hashlib
import json
from pathlib import Path
import sys
from rebuild_fields import book_projection,lifecycle_projection

OUT=Path(__file__).resolve().parent
AUDIT=OUT.parent/'evidence-availability-20261113'


def read(p):return json.loads(p.read_text(encoding='utf8'))
def lines(p):
    with gzip.open(p,'rt',encoding='utf8') as f:
        yield from (json.loads(line) for line in f)
def packed(v):return json.dumps(v,ensure_ascii=False,separators=(',',':'))
def col(n):
    result=''
    while n>=0:n,r=divmod(n,26);result=chr(65+r)+result;n-=1
    return result


class PayloadStore:
    def __init__(self):
        self.row=2;self.references={}
        self.file=gzip.open(OUT/'cache/workbook_payloads.jsonl.gz','wt',encoding='utf8',compresslevel=1)
    def add(self,key,value):
        if key in self.references:return self.references[key]
        text=packed(value);chunks=[text[i:i+20000] for i in range(0,len(text),20000)]
        start=self.row
        for i,chunk in enumerate(chunks):
            self.file.write(packed([key,i+1,len(chunks),chunk])+'\n');self.row+=1
        ref={'sheet':'Recovered payloads','first_row':start,'last_row':self.row-1,
             'json_column':'D','sha256_utf8':hashlib.sha256(text.encode()).hexdigest(),'id':key}
        self.references[key]=ref
        return ref


def main():
    import pyarrow.parquet as pq
    import pyarrow.compute as pc
    layout=read(Path('E:/Markets/outputs/dipole-experiment-20261110/layout.json'))
    (OUT/'WORKBOOK_LAYOUT.json').write_text(packed(layout)+'\n',encoding='utf8')
    package=json.loads(gzip.decompress((AUDIT/'raw/package.json.gz').read_bytes()))
    static=read(OUT/'STATIC_FIELD_VALUES.json');store=PayloadStore();static_cells={}
    for field,entry in static.items():
        value=dict(entry)
        value['values']=[dict(item,content_utf8=gzip.decompress((OUT/item['content_path']).read_bytes()).decode('utf8')) for item in entry['values']]
        ref=store.add('static:'+field,value)
        static_cells[field]={'status':'RECOVERED_STATIC_CONTENT','source_count':len(value['values']),
            'values_in_workbook':ref,'role':entry['role'],'historical_market_clock':None}
    flows={}
    for day in ['20231002','20231003','20231017','20231018']:
        ordinals=set()
        for item in package['cases']:
            if item['day']==day:ordinals.update(range(item['first_trade_ordinal'],item['last_trade_ordinal']+1))
        table=pq.read_table(OUT/f'flow_inputs/{day}/trade-flow-inputs.parquet')
        import pyarrow as pa
        table=table.filter(pc.is_in(table['trade_ordinal'],value_set=pa.array(sorted(ordinals))))
        flows[day]={r['trade_ordinal']:r for r in table.to_pylist()}
    native={day:{r['id']:r for r in lines(OUT/f'native_records/{day}.jsonl.gz')} for day in flows}
    native_refs={}
    counts=collections.Counter();remaining=collections.Counter();old_missing=collections.Counter();newly=collections.Counter()
    native_binding={'L049':['absorption','replenishment'],'L050':['replenishment'],'L051':['queue','absorption'],
                    'L058':['candidate','episode'],'L059':['candidate','episode'],'L076':['candidate','episode']}
    updates=gzip.open(OUT/'cache/workbook_updates.jsonl.gz','wt',encoding='utf8',compresslevel=1)
    examples=[]
    for item in package['cases']:
        case=f"{item['day']}-{item['category_index']}";day=item['day']
        original=json.loads(gzip.decompress((AUDIT/f'raw/{case}.json.gz').read_bytes()))
        location=next(x for x in layout['loc'] if x['candidate']==item['life']['candidate_id'])
        books={r['case_row']:r for r in lines(OUT/f'book_records/{case}.jsonl.gz')}
        events={r['case_row']:r for r in lines(OUT/f'event_records/{case}.jsonl.gz')}
        joins={r['case_row']:r for r in lines(OUT/f'native_joins/{case}.jsonl.gz')}
        heads=original['headers'];idx={h:i for i,h in enumerate(heads)}
        for i,row in enumerate(original['rows']):
            b=books[i]['original'];book=b['book_full'];trade=b['original_trade'];clock=trade['receive_ns']
            ordinal=int(row[idx['trade_ordinal']]);assert ordinal==b['trade_ordinal']
            bref=store.add('book:'+case+':'+str(i),books[i])
            ev=events[i];raw_events=[v['original'] for v in ev['events']]
            eref=store.add('events:'+case+':'+str(i),ev)
            assert ev['end_cursor']==trade['trade_input_cursor'] and ev['available_by_trade_receive']
            changes=dict(static_cells)
            def put(code,values,status='RECOVERED_ORIGINAL_VALUES',**more):
                field=next(h for h in heads if h.startswith(code+' | '))
                changes[field]=dict(status=status,phase='at_trade_input',known_by_ns=clock,values=values,**more)
            for code in ['L039','L040','L041','L042','L043','L044','L045','L052','L054','L057']:
                if code in ('L041','L042','L044'):
                    put(code,None,'RECOVERED_COMPLETE_SOURCE_PAYLOAD',values_in_workbook=bref,
                        projection={'module':'rebuild_fields.py','function':'book_projection','field':code,'input':'original.book_full'},
                        values_summary={k:book[k] for k in ['bid_order_count_full','ask_order_count_full','bid_depth_full','ask_depth_full']})
                    if code=='L042':changes[next(h for h in heads if h.startswith(code+' | '))]['unresolved']='Snapshot ages recovered; longitudinal identity survival requires a declared observation interval.'
                    continue
                value=book_projection(book,code)
                extra={}
                if code=='L042':extra['unresolved']='Snapshot age recovered; longitudinal identity survival requires a declared observation interval.'
                if len(packed(value))>24000:
                    put(code,None,'RECOVERED_COMPLETE_SOURCE_PAYLOAD',values_in_workbook=bref,
                        projection={'module':'rebuild_fields.py','function':'book_projection','field':code,'input':'original.book_full'},**extra)
                    changes[next(h for h in heads if h.startswith(code+' | '))]['values_summary']={k:book[k] for k in ['bid_order_count_full','ask_order_count_full','bid_depth_full','ask_depth_full']}
                else:put(code,value,**extra)
            for code in ['L027','L028','L030','L031','L032','L033','L034','L035','L036','L037']:
                values=lifecycle_projection(raw_events,code)
                scope={'start_cursor':ev['start_cursor'],'end_cursor':ev['end_cursor'],
                       'rule':'All native messages after prior retained trade through current trade. First case row starts after strict-prior group close.'}
                if len(packed(values))>24000:
                    put(code,None,'RECOVERED_COMPLETE_SOURCE_PAYLOAD',values_in_workbook=eref,
                        projection={'module':'rebuild_fields.py','function':'lifecycle_projection','field':code,'input':'events[*].original'},interval=scope,observed_event_count=len(values))
                else:put(code,values,interval=scope,observed_event_count=len(values))
                if code in ('L032','L033'):
                    changes[next(h for h in heads if h.startswith(code+' | '))]['semantic_note']='Native M modifies/replaces the same order state; these are the same original events, not two independent counts. R is reset.'
            put('L029',{'trade':trade,'book_source':books[i]['source'],'book_known_by_ns':clock,
                        'event_interval':{'start_cursor':ev['start_cursor'],'end_cursor':ev['end_cursor']}})
            put('L038',{'instrument_id':trade['instrument_id'],
                        'raw_symbols':sorted({r['original_message']['raw_symbol'] for r in raw_events if r['original_message'].get('raw_symbol')}),
                        'source_tape_day':trade['source_tape_day']},'RECOVERED_PARTIAL_SEMANTICS',
                        unresolved='Observed contract identity. Full expiry/roll transition state is a separate dependency.')
            receipt=read(OUT/f'source_manifests/book-{day}.json')['receipt']
            field=next(h for h in heads if h.startswith('L046 | '))
            changes[field]={'status':'RECOVERED_REPLAY_RECEIPT','values':receipt,
                'role':'Reconstruction provenance; retrospective receipt, not a historical signal clock.'}
            put('L047',raw_events if len(packed(raw_events))<=24000 else None,
                values_in_workbook=eref,interval_start_cursor=ev['start_cursor'],interval_end_cursor=ev['end_cursor'])
            put('L048',{'aggressor_side':trade['aggressor_side'],'trade_size':trade['size'],
                'signed_trade_size':trade['size']*(1 if trade['aggressor_side']=='B' else -1) if trade['aggressor_side'] in ('A','B') else None,
                'latest_completed_native_flow':json.loads(flows[day][ordinal]['L055 | legacy_native_signed_flow'])})
            put('L053',{'integrity':b['integrity'],'fifo_priority_reconstructed':b['fifo_priority_reconstructed'],
                'native_priority_id_exposed':b['native_priority_id_exposed'],'archive_scope':receipt['scope']})
            for code in ['L055','L056']:
                field=next(h for h in heads if h.startswith(code+' | '));value=json.loads(flows[day][ordinal][field])
                if value.get('known_by_ns') is not None:assert value['known_by_ns']<=clock
                changes[field]=value
            for code,sections in native_binding.items():
                available={s:joins[i]['sections'][s] for s in sections if s in joins[i]['sections']}
                if not available:continue
                values={}
                for section,join in available.items():
                    refs=[]
                    for key in join['record_ids']:
                        native_record=native[day][key]
                        refkey=day+':'+key
                        if refkey not in native_refs:native_refs[refkey]=store.add('native:'+refkey,native_record)
                        refs.append(native_refs[refkey])
                    values[section]={'known_by_ns':join['known_by_ns'],'records_in_workbook':refs}
                put(code,values,'RECOVERED_NATIVE_OBSERVATIONS',
                    unresolved='Latest saved section observations and all clock ties; not proof of full active-state or full named-layer semantics.')
            put('L066',{'book':clock,'actions_through_cursor':trade['trade_input_cursor'],
                'flow':changes['L055 | legacy_native_signed_flow'].get('known_by_ns'),
                'native_sections':{s:v['known_by_ns'] for s,v in joins[i]['sections'].items()}},
                'RECOVERED_FEATURE_CLOCKS',unresolved='Clock map covers recovered features; unproduced fields have no invented availability time.')
            for field,value in changes.items():
                j=idx[field];prior=json.loads(row[j]);was_missing=prior.get('status') in ('MISSING_STATIC_SOURCE','NO_MATCHING_VALUE_IN_RETAINED_INPUT')
                if was_missing:old_missing[field]+=1;newly[field]+=1
                if field.startswith('S'):raise AssertionError('S mutation')
                # The earlier group-close payload remains available, explicitly separate from trade input.
                if not was_missing and field not in static and field[:4] not in ('L055','L056'):
                    value=dict(value,original_cell=prior)
                text=packed(value)
                if len(text)>30000:
                    ref=store.add('cell:'+case+':'+str(i)+':'+field,value)
                    text=packed({'status':value['status'],'values_in_workbook':ref,'known_by_ns':value.get('known_by_ns'),
                        'scope':'Complete cell JSON is stored in the referenced contiguous payload chunks. No truncation.'})
                address=col(location['base']+layout['tickPositions'][j])+str(location['headRow']+i+2)
                updates.write(packed({'sheet':1,'cell':address,'value':text,'field':field,'case':case,'row':i})+'\n')
                counts[field]+=1
                if i==0 and field.startswith(('L041','L055')) and case=='20231002-0':examples.append({'cell':address,'field':field,'value':text})
            for field in package['all_layer_fields']:
                if ' | ' not in field:continue
                prior=json.loads(row[idx[field]])
                if field not in changes and prior.get('status') in ('MISSING_STATIC_SOURCE','NO_MATCHING_VALUE_IN_RETAINED_INPUT'):remaining[field]+=1
        print('Prepared actual workbook replacements',case,flush=True)
    store.file.close();updates.close()
    report={'selected_ticks':5513,'cases':32,'original_fields':141,'changed_cells':sum(counts.values()),
        'fields_changed':dict(counts),'formerly_empty_fields_with_recovered_content':dict(newly),
        'still_missing_field_rows':dict(remaining),'payload_rows':store.row-2,'s_fields_changed':0,
        'all_fields_complete':False,'source_payloads_embedded_in_workbook':True,'examples':examples}
    (OUT/'WORKBOOK_REPAIR_PREPARATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
    print('Prepared',sum(counts.values()),'cells and',store.row-2,'payload chunks',flush=True)


if __name__=='__main__':
    sys.path.insert(0,'E:/frankie-excel-review-20261109/python-deps');main()
