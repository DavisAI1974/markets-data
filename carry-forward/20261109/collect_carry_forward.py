import concurrent.futures,gzip,hashlib,json,pathlib,re,urllib.request,zipfile
ROOT=pathlib.Path(__file__).parent;OUT=ROOT/'delivery';OUT.mkdir(exist_ok=True)
base=json.loads((ROOT/'source_catalog.json').read_text()); inventories={'published_source_catalog':base}
stage=pathlib.Path('E:/Markets-consolidation-staging-20261109')
m=json.loads((stage/'MANIFEST.json').read_text()); receipts=json.loads((stage/'REMOTE_VERIFICATION_COMBINED.json').read_text())
names=['source_inventory.json','active_sources.json','expanded_sources.json','workflow_sources.json','remaining_research_sources.json']
for name in names:
 row=next(x for x in m['files'] if x['path']==name);assert row['asset'] in receipts
 with zipfile.ZipFile(stage/row['asset']) as z:b=z.read(name)
 assert hashlib.sha256(b).hexdigest()==row['sha256']
 inventories[name]=json.loads(b)
merged={}
for inv,rows in inventories.items():
 for r in rows:
  if not all(k in r for k in ['repo','path','sha']):continue
  key=(r['repo'],r['path'],r['sha']);e=merged.setdefault(key,{'repo':r['repo'],'path':r['path'],'git_blob_sha':r['sha'],'bytes':r.get('size'),'source_ids':[],'branches':[],'references':[],'inventories':[],'prior_handling':[]})
  for field,value in [('source_ids',r.get('id')),('references',r.get('ref')),('inventories',inv),('prior_handling',r.get('handling'))]:
   if value and value not in e[field]:e[field].append(value)
  e['branches']=sorted(set(e['branches']+r.get('branches',[])))
sources=list(merged.values()); forbidden={e['git_blob_sha'] for e in sources if re.search(r'(?:agent-pass/)?reanalysis/claude(?:/|$)',e['path'])}
for e in sources:
 e['carry_forward']='required';e['paper_policy']='All defined hypotheses are included; evidence strength is not an eligibility filter.'
 e['content_status']='unread_user_exclusion' if e['git_blob_sha'] in forbidden else 'retained_for_full_content_reconciliation'
 e['source_url']='https://github.com/DavisAI1974/'+e['repo']+'/blob/'+e['references'][0]+'/'+e['path'] if e['references'] else None
docs={}
for e in sources:
 if e['path'].endswith('.md') and e['git_blob_sha'] not in forbidden:docs.setdefault(e['git_blob_sha'],e)
cache=pathlib.Path('E:/Markets/outputs/research-union-20261109/objects');downloaded=ROOT/'documents';downloaded.mkdir(exist_ok=True)
def get_doc(item):
 sha,e=item;p=cache/sha;dest=downloaded/(sha+'.md')
 if dest.exists():b=dest.read_bytes()
 elif p.exists():b=p.read_bytes()
 else:
  url='https://raw.githubusercontent.com/DavisAI1974/'+e['repo']+'/'+e['references'][0]+'/'+urllib.parse.quote(e['path'],safe='/')
  with urllib.request.urlopen(url,timeout=120) as response:b=response.read()
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==sha,sha
 dest.write_bytes(b)
 return sha,b.decode('utf-8-sig',errors='strict')
documents={};errors=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 futures={pool.submit(get_doc,x):x for x in docs.items()}
 for i,f in enumerate(concurrent.futures.as_completed(futures),1):
  try:sha,body=f.result();documents[sha]=body
  except Exception as exc:errors.append({'sha':futures[f][0],'error':str(exc)})
  if i%100==0:print('DOCUMENTS',i,'of',len(docs),'errors',len(errors),flush=True)
sections=[]
for sha,body in documents.items():
 lines=body.splitlines();starts=[i for i,s in enumerate(lines) if re.match(r'^#{1,6}\s+',s)]
 if not starts or starts[0]!=0:starts.insert(0,0)
 aliases=[{'source_ids':e['source_ids'],'url':e['source_url'],'path':e['path']} for e in sources if e['git_blob_sha']==sha]
 for j,start in enumerate(starts):
  end=starts[j+1] if j+1<len(starts) else len(lines);text='\n'.join(lines[start:end]);sid='SEC-'+sha[:12]+'-'+str(start+1)
  sections.append({'section_id':sid,'git_blob_sha':sha,'start_line':start+1,'end_line':end,'heading':lines[start] if start<len(lines) else '', 'text':text,'sources':aliases,'status':'preserved_not_claimed_as_unique_or_executable_strategy','paper_inclusion':'all_hypotheses_included_after_rule_definition','requires_interpretive_mapping':True})
for e in sources:
 if e['git_blob_sha'] in documents:e['content_status']='complete_document_preserved_and_section_indexed; semantic_mapping_pending'
with gzip.open(OUT/'SOURCE_REGISTER.json.gz','wt',encoding='utf-8') as f:json.dump(sources,f,ensure_ascii=False)
with gzip.open(OUT/'RESEARCH_SECTIONS.jsonl.gz','wt',encoding='utf-8') as f:
 for s in sections:f.write(json.dumps(s,ensure_ascii=False)+'\n')
(ROOT/'sections.json').write_text(json.dumps(sections,ensure_ascii=False),encoding='utf-8')
(OUT/'SOURCE_COVERAGE.json').write_text(json.dumps({'source_records':len(sources),'inventory_record_counts':{k:len(v) for k,v in inventories.items()},'unique_markdown_documents':len(documents),'document_sections':len(sections),'document_errors':errors,'user_excluded_blob_count':len(forbidden),'semantic_reconciliation_complete':False,'all_strategies_executable':False,'policy':'Preserve all source records and all defined hypotheses; no evidence-based paper admission veto.'},indent=2))
print('COMPLETE',len(sources),len(documents),len(sections),'ERRORS',len(errors),flush=True)
