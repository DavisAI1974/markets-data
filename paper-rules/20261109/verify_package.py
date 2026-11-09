"""Structural and causal-logic verification only; no trading replay or fills."""
import gzip,hashlib,json,pathlib,subprocess,sys
ROOT=pathlib.Path(__file__).parent
def reject(v):raise ValueError('Non-JSON numeric token: '+v)
def read(p):return json.loads(p.read_text(encoding='utf-8'),parse_constant=reject)
def rows(p):return [json.loads(s,parse_constant=reject) for s in gzip.decompress(p.read_bytes()).decode().splitlines()]

machine=ROOT/'machine'
for p in machine.glob('*.json'):read(p)
core=rows(machine/'PAPER_RULE_CORE.jsonl.gz')
manifest=read(machine/'PAPER_UNIVERSE_MANIFEST.json')
assert len(core)==manifest['core_record_count']==32701
assert len({r['id'] for r in core})==len(core)
hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in machine.iterdir() if p.is_file()}
for r in core:
    assert r['paper_included'] is True and r['execution_enabled'] is False
    assert r['requires_full_definition'] is True and r['standalone_execution_allowed'] is False
    assert hashes[r['definition_ref']['path']]==r['definition_ref']['sha256']
assert manifest['core']['sha256']==hashes['PAPER_RULE_CORE.jsonl.gz']
coverage=read(ROOT/'reconciliation/INHERITED_82_CROSSWALK.json')
assert len(coverage)==82 and all(r['paper_included'] and not r['dropped'] for r in coverage)
assert len(rows(machine/'OCTOBER_SOURCE_CELLS.jsonl.gz'))==1459
run=subprocess.run([sys.executable,'-B','-m','unittest','discover','-s','tests'],cwd=ROOT,capture_output=True,text=True)
assert run.returncode==0,run.stdout+run.stderr
result={'schema':'package-verification-v1','machine_json_strict_parse':'passed','unique_core_ids':len(core),'all_included':True,'all_execution_disabled':True,'all_full_definition_hashes_match':True,'inherited_candidate_count':82,'source_report_cells_separate':1459,'unit_test_output':run.stdout+run.stderr,'validation_scope':'JSON,coverage,bindings,and synthetic logic','market_replay_performed':False,'platform_fills':0,'platform_ready':False}
(ROOT/'PACKAGE_VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='unit_test_output'}))
