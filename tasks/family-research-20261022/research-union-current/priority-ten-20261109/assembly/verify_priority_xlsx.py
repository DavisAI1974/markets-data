"""Read back every new cell and compare with the frozen source-row projections."""
import collections,hashlib,itertools,json,zipfile
from pathlib import Path
from priority_cell_analysis import sheets,rows
from build_priority_workbook import data_rows
R=Path(__file__).parent;P=R/'priority-now'

def text_value(v):
 if v is None:return None
 if isinstance(v,bool):return '1' if v else '0'
 return str(v)

def main():
 selection=json.loads((P/'priority_selection.json').read_text())
 reports=[];preview=[]
 with zipfile.ZipFile(P/'before-priority.xlsx') as original,zipfile.ZipFile(P/'Frankie_four_day_priority_ten.xlsx') as master,zipfile.ZipFile(P/'Priority_native_flow.xlsx') as flow:
  mapping=sheets(master);fm=sheets(flow)
  preserved=[]
  for name,path in sheets(original).items():
   assert name in mapping,name
   assert original.getinfo(path).CRC==master.getinfo(mapping[name]).CRC,name
   assert original.getinfo(path).file_size==master.getinfo(mapping[name]).file_size,name
   preserved.append(name)
  for item in selection['families']:
   z=flow if item['rank']==1 else master;part=(fm if item['rank']==1 else mapping)[item['sheet']]
   n=0;cells=0;h=hashlib.sha256();sample=[]
   for expected,actual in itertools.zip_longest(data_rows(item),rows(z,part)):
    assert expected is not None and actual is not None,item['sheet']
    rowno,row=actual;values=list(row.values());ev=[text_value(v) for v in expected]
    assert values==ev,(item['sheet'],rowno,[(i,a,b) for i,(a,b) in enumerate(zip(values,ev)) if a!=b][:4])
    h.update(json.dumps(values,ensure_ascii=False,separators=(',',':')).encode());h.update(b'\n');n+=1;cells+=len(values)
    if n<=8:sample.append([rowno,row])
   assert n==item['rows']
   reports.append({'sheet':item['sheet'],'file':'Priority_native_flow.xlsx' if item['rank']==1 else 'Frankie_four_day_priority_ten.xlsx','rows_verified':n,'cells_verified':cells,'cell_values_sha256':h.hexdigest()})
   preview.append({'sheet':item['sheet'],'rows':sample})
   print('VERIFIED ALL CELLS',item['sheet'],n,cells,flush=True)
 result={'original_sheets_unchanged':preserved,'new_sheets':reports,'source_policy':'Every selected source blob Git-hash verified before projection; all projected cells independently read back and matched.'}
 (P/'priority_cell_verification.json').write_text(json.dumps(result,indent=2))
 (P/'preview_actual_cells.json').write_text(json.dumps(preview,indent=2))
 print('VERIFICATION COMPLETE',sum(r['rows_verified'] for r in reports),flush=True)

if __name__=='__main__':main()
