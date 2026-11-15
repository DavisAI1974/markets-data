"""Memory-only workbook patch. Reads pinned GitHub inputs, preserves unaffected XML."""
import base64,collections,gzip,hashlib,io,json,re,subprocess,urllib.request,zipfile
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape
REPO='DavisAI1974/markets-data'
BRANCH='codex/evidence-availability-20261113'
ROOT='tasks/family-research-20261022/research-union-current/'
DEST=ROOT+'oct18-native-recovery-20261115/'
DATA_COMMIT='87e5931b4927963f4b877c75956d1550f3c7d4ac'
BASE_ASSET=750614098
BASE_SHA='3db8c90fdbe02a8dd1bbda875521caa7f372a7ddf62dd38a141ecdd30bebc479'
BASE_BYTES=497012214
TAG='eight-trade-types-repair-20261115-r2'
NAME='Claude-Eight-Trade-Types-Rebuilt.xlsx'
CELL=re.compile(rb'<c\b[^>]*\br="([A-Z]+)(\d+)"[^>]*(?:/>|>.*?</c>)',re.S)
def packed(v):return json.dumps(v,ensure_ascii=False,separators=(',',':'))
def sha(b):return hashlib.sha256(b).hexdigest()
def gitsha(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def api(path,method='GET',data=None):
    args=['gh','api','repos/'+REPO+'/'+path]
    if method!='GET':args+=['--method',method]
    if data is not None:args+=['--input','-']
    r=subprocess.run(args,input=None if data is None else packed(data).encode(),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if r.returncode:raise RuntimeError(r.stderr.decode()[:1000])
    return json.loads(r.stdout)
def get(ref,path):
    with urllib.request.urlopen('https://raw.githubusercontent.com/'+REPO+'/'+ref+'/'+path,timeout=120) as f:return f.read()
def commit(files,message):
    head=api('git/ref/heads/'+BRANCH)['object']['sha']
    tree=api('git/commits/'+head)['tree']['sha'];entries=[]
    for name,raw in files.items():
        b=api('git/blobs','POST',{'content':base64.b64encode(raw).decode(),'encoding':'base64'})
        assert b['sha']==gitsha(raw)
        entries.append({'path':DEST+name,'mode':'100644','type':'blob','sha':b['sha']})
    newtree=api('git/trees','POST',{'base_tree':tree,'tree':entries})['sha']
    c=api('git/commits','POST',{'message':message,'tree':newtree,'parents':[head]})['sha']
    assert api('git/ref/heads/'+BRANCH)['object']['sha']==head
    api('git/refs/heads/'+BRANCH,'PATCH',{'sha':c,'force':False})
    for name,raw in files.items():assert get(c,DEST+name)==raw
    return c
def asset(asset_id,keep):
    p=subprocess.Popen(['gh','api','repos/'+REPO+'/releases/assets/'+str(asset_id),'-H','Accept: application/octet-stream'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out=io.BytesIO() if keep else None
    h=hashlib.sha256();size=0
    while b:=p.stdout.read(1024*1024):
        h.update(b);size+=len(b)
        if keep:out.write(b)
    err=p.stderr.read();assert p.wait()==0,err.decode()[:1000]
    if keep:out.seek(0)
    return out,h.hexdigest(),size
def rows(stream):
    buffer=b''
    while True:
        chunk=stream.read(1024*1024)
        if not chunk:
            yield False,buffer;break
        buffer+=chunk
        while True:
            start=buffer.find(b'<row ')
            if start<0:break
            end=buffer.find(b'</row>',start)
            if end<0:
                if start:yield False,buffer[:start];buffer=buffer[start:]
                break
            if start:yield False,buffer[:start]
            yield True,buffer[start:end+6];buffer=buffer[end+6:]
def inline(address,value,old=None):
    assert len(value)<=30000
    if old is None:head=('<c r="'+address+'"').encode()
    else:
        head=old.split(b'>',1)[0].rstrip(b'/')
        head=re.sub(rb'\s+t="[^"]*"',b'',head)
    return head+b' t="inlineStr"><is><t xml:space="preserve">'+escape(value).encode()+b'</t></is></c>'
def string_value(raw):
    root=ET.fromstring(raw)
    return ''.join(x.text or '' for x in root.iter() if x.tag.split('}')[-1]=='t')
def digest_stream(stream):
    h=hashlib.sha256()
    while b:=stream.read(1024*1024):h.update(b)
    return h.hexdigest()
def main(script_source):
    report=json.loads(get(DATA_COMMIT,DEST+'RECOVERY_VERIFICATION.json'))
    patch_raw=get(DATA_COMMIT,DEST+'workbook-native-updates.jsonl.gz')
    assert sha(patch_raw)==report['output_sha256']['workbook-native-updates.jsonl.gz']
    patch=[json.loads(x) for x in gzip.decompress(patch_raw).splitlines()]
    assert len(patch)==2894
    original_values={x['cell']:json.loads(x['value']) for x in patch}
    assert len(original_values)==2894
    prepared={};payload_refs={};payload_rows=[];payload_texts={}
    first_added_row=128084;nextrow=first_added_row
    for p in patch:
        value=json.loads(p['value'])
        assert value['status'].startswith('RECOVERED_ORIGINAL_')
        if len(p['value'])>30000:
            full=packed(value.pop('values'));key=sha(full.encode())
            if key not in payload_refs:
                chunks=[full[i:i+20000] for i in range(0,len(full),20000)]
                begin=nextrow
                for i,chunk in enumerate(chunks):
                    payload_rows.append([key,i+1,len(chunks),chunk]);nextrow+=1
                payload_refs[key]={'sheet':'Recovered payloads','first_row':begin,'last_row':nextrow-1,'json_column':'D','sha256_utf8':key,'id':key}
                payload_texts[key]=full
            value['values_in_workbook']=payload_refs[key]
        prepared[p['cell']]=packed(value)
        assert len(prepared[p['cell']])<=30000
        reconstructed=dict(value)
        if 'values_in_workbook' in value:
            reconstructed['values']=json.loads(payload_texts[reconstructed.pop('values_in_workbook')['id']])
        assert reconstructed==original_values[p['cell']]
    assert nextrow<=1048577
    print(packed({'stage':'downloading_verified_base','updates':len(prepared),'new_payload_chunks':len(payload_rows)}),flush=True)
    original_buf,h,size=asset(BASE_ASSET,True)
    assert h==BASE_SHA and size==BASE_BYTES,(h,size)
    result_buf=io.BytesIO();expected_hashes={};invariants={};counts=collections.Counter();unchanged_parts=[]
    notes={'A2':'Recovered source observations only. Frankie has not run on these days; model outputs await execution. Unavailable values remain empty.'}
    payload_xml=b''.join(('<row r="'+str(rowno)+'">').encode()+b''.join(inline(chr(65+i)+str(rowno),str(v)) for i,v in enumerate(row))+b'</row>' for rowno,row in enumerate(payload_rows,first_added_row))
    with zipfile.ZipFile(original_buf) as original,zipfile.ZipFile(result_buf,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=1,allowZip64=True) as out:
        with original.open('xl/worksheets/sheet4.xml') as src:
            header=src.read(2000)
            assert b'<dimension ref="A1:D128083"' in header
        for info in original.infolist():
            name=info.filename;written=hashlib.sha256()
            if name in ('xl/worksheets/sheet1.xml','xl/worksheets/sheet3.xml'):
                changes=prepared if name.endswith('sheet1.xml') else notes
                inv=hashlib.sha256()
                def normalize(m):
                    a=(m[1]+m[2]).decode()
                    return ('<changed-cell r="'+a+'"/>').encode() if a in changes else m[0]
                def replace(m):
                    a=(m[1]+m[2]).decode()
                    if a not in changes:return m[0]
                    assert b'<f' not in m[0],'Refuse to replace a formula'
                    counts[name]+=1
                    return inline(a,changes[a],m[0])
                with original.open(name) as src,out.open(name,'w',force_zip64=True) as dst:
                    for isrow,data in rows(src):
                        inv.update(CELL.sub(normalize,data) if isrow else data)
                        changed=CELL.sub(replace,data) if isrow else data
                        dst.write(changed);written.update(changed)
                invariants[name]=inv.hexdigest()
                print(packed({'stage':'sheet_written','part':name,'cells':counts[name]}),flush=True)
            elif name=='xl/worksheets/sheet4.xml':
                with original.open(name) as src,out.open(name,'w',force_zip64=True) as dst:
                    first=src.read(1024*1024)
                    first=first.replace(b'<dimension ref="A1:D128083"',('<dimension ref="A1:D'+str(nextrow-1)+'"').encode(),1)
                    tail=first
                    while b:=src.read(1024*1024):
                        data=tail[:-64];dst.write(data);written.update(data);tail=tail[-64:]+b
                    assert tail.count(b'</sheetData>')==1
                    left,right=tail.split(b'</sheetData>',1)
                    for data in (left,payload_xml,b'</sheetData>',right):dst.write(data);written.update(data)
                print(packed({'stage':'payloads_appended','chunks':len(payload_rows)}),flush=True)
            else:
                with original.open(name) as src,out.open(name,'w',force_zip64=True) as dst:
                    while b:=src.read(1024*1024):dst.write(b);written.update(b)
                unchanged_parts.append(name)
            expected_hashes[name]=written.hexdigest()
    assert counts['xl/worksheets/sheet1.xml']==2894 and counts['xl/worksheets/sheet3.xml']==1
    print(packed({'stage':'verifying_export','bytes':result_buf.getbuffer().nbytes}),flush=True)
    recovered_payload=[];verified=collections.Counter()
    with zipfile.ZipFile(result_buf) as out,zipfile.ZipFile(original_buf) as original:
        assert out.namelist()==original.namelist()
        for name in out.namelist():
            with out.open(name) as src:assert digest_stream(src)==expected_hashes[name],name
            if name in unchanged_parts:
                with original.open(name) as src:assert digest_stream(src)==expected_hashes[name],name
            if name in invariants:
                changes=prepared if name.endswith('sheet1.xml') else notes
                inv=hashlib.sha256()
                def verify(m):
                    a=(m[1]+m[2]).decode()
                    if a not in changes:return m[0]
                    assert string_value(m[0])==changes[a],a
                    verified[name]+=1
                    return ('<changed-cell r="'+a+'"/>').encode()
                with out.open(name) as src:
                    for isrow,data in rows(src):inv.update(CELL.sub(verify,data) if isrow else data)
                assert inv.hexdigest()==invariants[name],name
        with out.open('xl/worksheets/sheet4.xml') as src:
            # Existing payload content is covered by the full-part byte hash.
            skip=out.getinfo('xl/worksheets/sheet4.xml').file_size-len(payload_xml)-len(b'</sheetData></worksheet>')
            assert skip>=0
            while skip:
                b=src.read(min(skip,1024*1024));assert b;skip-=len(b)
            tail=src.read()
            assert tail==payload_xml+b'</sheetData></worksheet>'
            elements=ET.fromstring(b'<root>'+payload_xml+b'</root>')
            for element in elements:
                recovered_payload.append([string_value(ET.tostring(c)) for c in element])
    assert recovered_payload==[[str(v) for v in row] for row in payload_rows]
    assert verified==counts
    for key,ref in payload_refs.items():
        texts=recovered_payload[ref['first_row']-first_added_row:ref['last_row']-first_added_row+1]
        full=''.join(row[3] for row in texts);assert sha(full.encode())==key and full==payload_texts[key]
    size=result_buf.getbuffer().nbytes;checksum=sha(result_buf.getbuffer())
    receipt={'base_release_asset':BASE_ASSET,'base_sha256':BASE_SHA,'data_commit':DATA_COMMIT,
      'file':NAME,'bytes':size,'sha256':checksum,'additional_data_cells':2894,'notes_updated':1,
      'new_payload_chunks':len(payload_rows),'existing_payload_chunks_preserved':128082,
      'unaffected_parts_verified':len(unchanged_parts),'all_unaffected_sheet_cells_preserved_byte_for_byte':True,
      'every_changed_cell_and_new_payload_verified':True,'s_values_and_missing_states_unchanged':True,
      'frankie_has_run':False,'unavailable_values_invented':0,'local_task_files_written':0,
      'native_excel_opened':False,'visual_render_performed':False,
      'authoring_method':'Memory-only OOXML update; prior artifact-tool import failed with out-of-memory. No formulas or layout changed.',
      'field_status':{'exact_metadata':1,'scoped_content':5,'pre_run_unresolved':19,'awaiting_frankie_run':10}}
    files={'WORKBOOK_R2_VERIFICATION.json':(json.dumps(receipt,indent=2)+'\n').encode(),'publish_workbook_memory.py':script_source.encode()}
    c=commit(files,'research: verify Oct18 workbook recovery without local files')
    try:release=api('releases/tags/'+TAG)
    except RuntimeError as e:
        if '404' not in str(e):raise
        release=api('releases','POST',{'tag_name':TAG,'target_commitish':c,'name':'Eight trade types: Oct18 source recovery','draft':True,'prerelease':True,
          'body':'Adds 2,894 source-backed Oct18 L050/L051 cells, with lossless embedded payloads. Preserves other ticks, formulas, S values, missing states, and all four days/eight types. Frankie has not run; model outputs remain unavailable. 19 pre-run fields remain unresolved. No invented values. Built and verified in memory; GitHub is the only new persistent destination. SHA256: '+checksum})
    existing=[x for x in release['assets'] if x['name']==NAME]
    if existing:
        uploaded=existing[0];assert uploaded['size']==size
    else:
        print(packed({'stage':'uploading_workbook','bytes':size,'commit':c}),flush=True)
        token=subprocess.run(['gh','auth','token'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True).stdout.decode().strip()
        url=release['upload_url'].split('{')[0]+'?name='+NAME
        request=urllib.request.Request(url,data=result_buf.getbuffer(),method='POST',headers={
           'Authorization':'Bearer '+token,'Accept':'application/vnd.github+json','Content-Type':'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet','Content-Length':str(size)})
        with urllib.request.urlopen(request,timeout=1800) as response:uploaded=json.load(response)
        del token,request
    assert uploaded['size']==size
    print(packed({'stage':'verifying_github_asset','asset_id':uploaded['id']}),flush=True)
    _,check,n=asset(uploaded['id'],False);assert check==checksum and n==size
    if release['draft']:release=api('releases/'+str(release['id']),'PATCH',{'draft':False})
    receipt.update({'release_url':release['html_url'],'asset_id':uploaded['id'],'download_url':uploaded['browser_download_url'],'github_download_sha256_verified':True})
    c2=commit({'WORKBOOK_R2_PUBLICATION.json':(json.dumps(receipt,indent=2)+'\n').encode()},'research: record verified GitHub workbook release')
    print(packed({'commit':c2,'release':release['html_url'],'verification':receipt}),flush=True)
if __name__=='__main__':main(SCRIPT_SOURCE)
