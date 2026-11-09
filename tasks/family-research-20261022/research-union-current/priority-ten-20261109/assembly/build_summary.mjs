import fs from 'node:fs/promises';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const out='E:/Markets/outputs/research-union-20261109/priority-now';
const specs=JSON.parse(await fs.readFile(`${out}/summary_sheets.json`,'utf8'));
const wb=Workbook.create();
for(const spec of specs){
 const sh=wb.worksheets.add(spec.name);sh.showGridLines=false;sh.freezePanes.freezeRows(1);
 sh.getRangeByIndexes(0,0,spec.rows.length+1,spec.headers.length).values=[spec.headers,...spec.rows];
 const all=sh.getUsedRange();all.format.font={name:'Aptos',size:11,color:'#172B4D'};all.format.wrapText=true;all.format.verticalAlignment='center';
 spec.widths.forEach((w,i)=>{sh.getRangeByIndexes(0,i,spec.rows.length+1,1).format.columnWidth=w;});
 sh.getRangeByIndexes(0,0,1,spec.headers.length).format.fill='#163A5F';
 sh.getRangeByIndexes(0,0,1,spec.headers.length).format.font={bold:true,color:'#FFFFFF'};
 sh.getRangeByIndexes(0,0,1,spec.headers.length).format.rowHeight=40;
 spec.rows.forEach((r,i)=>{
  const range=sh.getRangeByIndexes(i+1,0,1,spec.headers.length);
  range.format.rowHeight=Math.max(24,...r.map((v,j)=>Math.ceil(String(v??'').length/(spec.widths[j]*0.95))*16+8));
  if(i%2===0)range.format.fill='#EDF3F8';
 });
}
wb.recalculate();
console.log((await wb.inspect({kind:'region',sheetId:'Priority findings',range:'A1:D4',maxChars:1800})).ndjson);
await (await SpreadsheetFile.exportXlsx(wb)).save(`${out}/Priority_summary.xlsx`);
const preview=await wb.render({sheetName:'Priority findings',autoCrop:'all',scale:1,format:'png'});
await fs.writeFile(`${out}/Priority-findings-preview.png`,new Uint8Array(await preview.arrayBuffer()));
console.log('ARTIFACT SUMMARY EXPORTED');
