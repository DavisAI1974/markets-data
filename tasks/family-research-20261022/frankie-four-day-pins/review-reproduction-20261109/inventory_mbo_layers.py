"""Account for every restored MBO message, separately from opening warmup."""
import collections,concurrent.futures,gzip,hashlib,json,pathlib,urllib.request
ROOT=pathlib.Path(__file__).parent;OUT=ROOT/'mbo-layer-data';OUT.mkdir(exist_ok=True)
pubs=json.loads((ROOT/'recovered-packets/PUBLICATIONS.json').read_text())
results=[]
for pub in pubs:
    day=pub['day'];cache=ROOT/'mbo-message-cache'/day;cache.mkdir(parents=True,exist_ok=True)
    manifest=json.loads((ROOT/f'recovered-packets/book/{day}/MANIFEST.json').read_text())
    receipt=json.loads((ROOT/f'recovered-packets/book/{day}/RECOVERY_RECEIPT.json').read_text())
    entries=[f for f in manifest['files'] if f['path'].startswith('native-messages-')]
    def fetch(entry):
        path=cache/entry['path']
        if not path.is_file():
            with urllib.request.urlopen(f'https://raw.githubusercontent.com/{pub["repository"]}/{pub["revision"]}/{pub["prefix"]}/{entry["path"]}',timeout=180) as response:data=response.read()
            path.write_bytes(data)
        data=path.read_bytes();assert len(data)==entry['bytes'] and hashlib.sha256(data).hexdigest()==entry['sha256']
        return path
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:paths=list(pool.map(fetch,entries))
    counts={'opening_warmup':collections.Counter(),'archived_session':collections.Counter()};examples={};rows=0
    warmup=receipt['original_replay_receipt'].get('opening_warmup_records',0)
    assert receipt['raw_messages_including_opening_warmup']-receipt['original_replay_receipt']['records']==warmup
    for path in paths:
        with gzip.open(path,'rt',encoding='utf-8') as stream:
            for offset,line in enumerate(stream):
                obj=json.loads(line);assert obj['source_stream_ordinal']==rows
                phase='opening_warmup' if rows<warmup else 'archived_session'
                message=obj['original_message'];action=message['action'];counts[phase]['all_messages']+=1;counts[phase][action]+=1
                categories=['all_messages',action]
                if message.get('is_snapshot'):categories.append('snapshot');counts[phase]['snapshot']+=1
                if obj['original_effect'].get('priority_lost'):categories.append('priority_lost');counts[phase]['priority_lost']+=1
                if obj['original_effect'].get('missing_reference'):counts[phase]['missing_reference']+=1
                for category in categories:
                    key=phase+'/'+category
                    if key not in examples:examples[key]=dict(file=path.name,file_row=offset,original=obj)
                rows+=1
    assert rows==receipt['raw_messages_including_opening_warmup']
    assert counts['opening_warmup']['all_messages']==warmup
    assert counts['archived_session']['all_messages']==receipt['original_replay_receipt']['records']
    result=dict(day=day,source=pub,counts={k:dict(v) for k,v in counts.items()},first_original_examples=examples,
        semantic_rules={'A':'add','C':'cancel/reduce','M':'replace the same order state; price changes or size increases lose priority','R':'clear/reset, not replace','T':'trade','F':'fill','N':'no displayed-book mutation'},
        scope='Complete restored stream; opening warmup counted separately. Daily totals are retrospective audit values, not earlier-trade causal features.',complete_restored_stream=True,complete_all_layers=False)
    (OUT/f'{day}.json').write_text(json.dumps(result,indent=1));results.append(result)
    print(day,json.dumps(result['counts']),flush=True)
(OUT/'ALL_DAYS.json').write_text(json.dumps(results,indent=1))
