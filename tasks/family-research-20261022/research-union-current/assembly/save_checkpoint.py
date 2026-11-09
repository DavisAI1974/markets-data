from acquire import ROOT
from xlsx_stream import build
import json,csv
O=ROOT/'current';styles=json.loads((O/'template_style_map.json').read_text())
def cs(name,file):
 def rows():
  with (O/file).open(encoding='utf8',newline='') as f:
   r=csv.reader(f);next(r);yield from r
 with (O/file).open(encoding='utf8',newline='') as f:heads=next(csv.reader(f))
 return {'name':name,'headers':heads,'rows':rows(),**styles}
spec=[cs('Screenshot source trace','screenshot_source_map.csv'),cs('Full saved trade clocks','trade_spine.csv'),cs('Every trade dipole map','trade_dipole_map.csv'),cs('Saved lifecycle intervals','dipole_lifecycle_index.csv'),cs('Gap queue current','research_gap_queue.csv')]
for s in json.loads((O/'case_table_inventory.json').read_text()):spec.append(cs(s['name'],s['file']))
dest=O/'Frankie_four_day_research_current.xlsx';report=build(O/'merged-template.xlsx',dest,spec)
(O/'workbook_population.json').write_text(json.dumps(report,indent=2));print('Saved',dest,dest.stat().st_size)
