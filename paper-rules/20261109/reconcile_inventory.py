import collections,gzip,hashlib,json,pathlib,re,zipfile
ROOT=pathlib.Path(__file__).parent
PRIOR=ROOT.parent/'markets-carry-forward-20261109'
STAGE=pathlib.Path('E:/Markets-consolidation-staging-20261109')
OUT=ROOT/'reconciliation';OUT.mkdir(exist_ok=True)
sources=json.loads(gzip.decompress((PRIOR/'delivery/SOURCE_REGISTER.json.gz').read_bytes()))
manifest=json.loads((STAGE/'MANIFEST.json').read_text())
names={'desktop-tree.json':('Markets','3d0b06aa29781d5e39cc3eb45c6d09e174f195a2'),'desktop_handoff-tree.json':('Markets','beb2104c079045c24832f2279eac5e8e69bc576e'),'ccode-tree.json':('Markets','47b62f934e3bfa20328dd7456971693bb7a99fef'),'codex-tree.json':('Markets','4cf6e85de5de2a9fb479c90b7afb8dd50f1748cb'),'original_research-tree.json':('Markets','418462afeaf0f14aa8129f6f4d02c3867d772fd0'),'workbook-tree.json':('markets-data','586b31f65a12fb9215095a9af6851f8e95e7653b'),'latest-data-tree.json':('markets-data','c01caaf4f327e8fdff21e4e8b9c5153aba8604a8')}
trees={};tree_receipts=[]
with zipfile.ZipFile(STAGE/'research-union-001.zip') as z:
 for name,key in names.items():
  b=z.read(name);r=next(x for x in manifest['files'] if x['path']==name)
  assert hashlib.sha256(b).hexdigest()==r['sha256']
  t=json.loads(b);assert not t.get('truncated')
  trees[key]={x['path']:x for x in t['tree'] if x['type']=='blob'}
  tree_receipts.append({'name':name,'repository':key[0],'commit':key[1],'tree_sha':t['sha'],'sha256':r['sha256'],'file_count':len(trees[key])})

def role(path):
 p=path.lower();ext=pathlib.Path(p).suffix
 if re.search(r'(?:agent-pass/)?reanalysis/claude(?:/|$)',p):return 'metadata_retained_user_content_exclusion'
 if ext in {'.png','.jpg','.svg','.pdf'}:return 'visual_or_reference_evidence'
 if ext in {'.csv','.parquet','.gz','.npz','.xlsx','.part-000000'}:return 'data_or_model_artifact'
 if ext in {'.py','.jl','.sh','.toml'}:return 'implementation_or_runtime_definition'
 if ext=='.md':return 'research_or_handoff_document'
 if ext=='.json':return 'structured_definition_data_or_receipt'
 return 'other_preserved_source'

rows=[];issues=[]
for s in sources:
 checks=[]
 for ref in s['references']:
  t=trees.get((s['repo'],ref))
  if t is None:checks.append({'ref':ref,'state':'tree_not_in_inherited_cache'});continue
  r=t.get(s['path'])
  state='exact_path_blob_match' if r and r['sha']==s['git_blob_sha'] else 'mismatch'
  checks.append({'ref':ref,'state':state})
 if not any(c['state']=='exact_path_blob_match' for c in checks):issues.append({'path':s['path'],'checks':checks})
 rows.append({**s,'artifact_role':role(s['path']),'tree_checks':checks,'paper_excluded':False,'semantic_disposition':'source_preserved; explicit_hypothesis_and_feature_mapping_required','version_policy':'Preserve history; only verified corrections replace wrong active math.'})

covered={(s['repo'],s['path'],s['git_blob_sha']) for s in sources}
branch_scope=[]
for name in ['desktop-tree.json','ccode-tree.json','codex-tree.json']:
 repo,ref=names[name]
 relevant=[x for x in trees[(repo,ref)].values() if x['path'].startswith('tasks/family-research-20261022/')]
 missing=[{'path':x['path'],'git_blob_sha':x['sha']} for x in relevant if (repo,x['path'],x['sha']) not in covered]
 branch_scope.append({'tree':name,'commit':ref,'declared_scope':'tasks/family-research-20261022/','file_count':len(relevant),'missing_from_union':missing})
with gzip.open(OUT/'ARTIFACT_DISPOSITIONS.jsonl.gz','wt',encoding='utf-8') as f:
 for r in rows:f.write(json.dumps(r,ensure_ascii=False)+'\n')
summary={'source_records':len(rows),'roles':dict(collections.Counter(r['artifact_role'] for r in rows)),'exact_tree_match':len(rows)-len(issues),'identity_issues':issues,'three_branch_inventory_coverage':branch_scope,'tree_receipts':tree_receipts,'semantic_reconciliation_complete':False,'identity_checks_are_not_content_review':True,'migration_paused':True}
(OUT/'INVENTORY_RECONCILIATION.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'source_records':len(rows),'identity_issues':issues,'branch_counts':[(x['tree'],x['file_count'],len(x['missing_from_union'])) for x in branch_scope]},indent=2))
