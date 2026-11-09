from acquire import ROOT
import json,csv,pathlib
O=ROOT/'current';spec=[]
def add(name,heads,rows,widths=None,text=None,file=None):
    spec.append({'name':name,'headers':heads,'sample':rows,'widths':widths,'textColumns':text or [],'dataFile':file})
def csvsheet(name,filename,widths=None):
    with (O/filename).open(encoding='utf-8-sig',newline='') as f:
        rs=list(csv.reader(f));add(name,rs[0],rs[1:],widths,file=filename)
coverage=json.loads((O/'dipole_gap_summary.json').read_text())
add('Research coverage',['Trading date','Saved trades','Complete saved associations','Missing association or segment','Status'],[[d['day'],d['trades'],d.get('Covered by saved prebirth and complete observed lifecycle',0),d['trades']-d.get('Covered by saved prebirth and complete observed lifecycle',0),'Population in progress; corrected price clocks verified'] for d in coverage],[16,18,25,28,65])
cases=json.loads((ROOT/'corrected_price_response.json').read_text())
ch=['example_ordinal','case_id','day','scheduled_observation_cutoff_ns','scheduled_outcome_cutoff_ns','observed_endpoint_receive_ns','observed_start_receive_ns','observation_cursor','endpoint_cursor','endpoint_raw_record_index','path_source','path_source_row','endpoint_path_row','group_source','raw_source','clock_status']
add('Corrected price clocks',[k.replace('_',' ') for k in ch],[[str(r[k]) if j in [3,4,5,6,7,8] else r[k] for j,k in enumerate(ch)] for r in cases],[18,64,14,34,34,34,34,20,20,24,18,18,18,18,18,60],text=[3,4,5,6,7,8])
csvsheet('Research gap queue','research_gap_queue.csv',[12,34,22,18,40,100,100])
csvsheet('19-field reuse','nineteen_field_reuse.csv',[45,18,40,18,18,30,65,100])
sources=json.loads((ROOT/'active_sources.json').read_text())
heads=['Source ID','Research owner','Current Git path','Bytes','Git blob','Commit','Source URL','Review / population status']
rs=[[s['id'],s['owner'],s['path'],s.get('size',0),s['sha'],s['ref'],s['url'],s['read_status']] for s in sources]
add('Research source inventory',heads,rs,[14,26,90,16,44,44,100,50])
renders=[r for r in rs if r[2].lower().endswith(('.png','.svg','.pdf','.html','.npz'))]
add('Render and array attachments',heads,renders,[14,26,90,16,44,44,100,50])
add('Workflow calculations',['Calculation family','October 2','October 3','October 17','October 18','Status'],[['Original SQLite clock and family calculations','Tracing exact extension','Tracing exact extension','Tracing exact extension','Original source found','Do not mark complete until row-level outputs reconciled'],['Julia model and full-depth calculation suite','Tracing exact extension','Tracing exact extension','Tracing exact extension','Original source found','Both user-requested calculation families require exact source trace']],[50,30,30,30,30,90])
(O/'workbook_sheets.json').write_text(json.dumps(spec),encoding='utf-8')
print('spec sheets',len(spec),'populated rows',sum(len(x['sample']) for x in spec))
