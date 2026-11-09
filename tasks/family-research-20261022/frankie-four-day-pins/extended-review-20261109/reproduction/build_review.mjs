import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import { Workbook, SpreadsheetFile } from '@oai/artifact-tool';

const root='E:/frankie-excel-review-20261109';
const out=path.join(root,'outputs/extended-four-day-review');
await fs.mkdir(out,{recursive:true});
const read=async p=>JSON.parse(await fs.readFile(path.join(root,p),'utf8'));
const [summary,layers,days,pins,baseSamples,fifo,staticLayers,brainManifest,brainReceipt]=await Promise.all([
  read('sources/SUMMARY.json'),read('sources/LAYERS.json'),read('sources/DAY_COVERAGE.json'),
  read('sources/INPUT_PINS.json'),read('sources/REVIEW_SAMPLES.json'),read('sources/FIFO_SAMPLE.json'),
  read('static-recovery/LAYER_VALUES.json'),read('consolidated-recovery/brain/20261109-search/MANIFEST.json'),
  read('consolidated-recovery/BRAIN_LOAD_RECEIPT.json')]);
const samples=await read('filled-review/REVIEW_SAMPLES.json');
const coverageUpdates=await read('filled-review/COVERAGE_UPDATES.json');
const recoveryPins=await read('filled-review/RECOVERY_PINS.json');
const publications=(await read('recovered-packets/PUBLICATIONS.json')).filter(p=>p.published);
const externalRecovery=await read('external-recovery/october02-external-recovery.json');
const externalValues=await read('filled-review/EXTERNAL_VALUES.json');
const forecastRecovery=await read('external-recovery/october02-mos-reconstruction.json');
const calendarRecovery=await read('filled-review/CALENDAR_VALUES.json');
const externalManifest=await read('external-recovery/MANIFEST.json');
pins.sources=(await read('consolidated-recovery/INPUT_PINS.json')).sources;
const nativePublications=await read('recovered-packets/NATIVE_PUBLICATIONS.json');
const nativeReviews=await read('filled-review/NATIVE_REVIEW_VALUES.json');
const mboDays=await read('mbo-layer-data/ALL_DAYS.json');
const flowCoverage=await read('filled-review/FLOW_COVERAGE.json');
const flowSummary=await read('flow-input-recovery/SUMMARY.json');
const expandedTables=Object.assign(await read('extended-review-data/WORKBOOK_TABLES.json'),
  await read('extended-review-data/WORKFLOW_TABLES.json'));
const dipolePins=await read('extended-review-data/DIPOLE_SOURCE_PINS.json');
const existingPins=new Set(pins.sources.map(p=>[p.repository,p.revision,p.source_path??p.path].join('|')));
for(const p of dipolePins){
  const key=[p.repository,p.revision,p.path].join('|');
  if(!existingPins.has(key)){pins.sources.push(p);existingPins.add(key);}
}
const mboNumbers=[27,28,29,30,31,32,33,34,35,36,37,46];
const nativeBindingColumns=new Set(Object.keys((await read('filled-review/NATIVE_LAYER_BINDINGS.json')).bindings).map(id=>layers.find(l=>l.layer_id===id).column));
const consolidatedUrl='https://github.com/DavisAI1974/markets-data/tree/cb91d0401490024f0d22ab6ecf558bb1c756cea4/tasks/family-research-20261022/frankie-four-day-pins/consolidated-recovery-20261109';
const staticMap=new Map(staticLayers.map(x=>[x.column,x]));
const packetRev='d7807678b52e4e4f746d51a394c32f73b48a6c82';
const staticRev='9358b38fe8253441398367bcd59f65ff2888fe07';
const prefix='tasks/family-research-20261022/frankie-four-day-pins';
const packetUrl=`https://github.com/DavisAI1974/markets-data/tree/${packetRev}/${prefix}/run-42608467894-1`;
const staticUrl=`https://github.com/DavisAI1974/markets-data/tree/${staticRev}/${prefix}/static-recovery-20261109`;
const jobUrl='https://github.com/DavisAI1974/markets-data/actions/runs/42617700678';
const statusNames={
  VERIFIED_BOOK_VALUES_RESTORED:'Verified book values restored',RESTORED_EXTERNAL_ORIGINAL_VALUE:'Original external value restored',
  ORIGINAL_NATIVE_EMISSIONS_RESTORED:'Original Native emissions restored (partial layer evidence)',
  ORIGINAL_NATIVE_FLOW_ASOF:'Original Native flow joined',ORIGINAL_RETAINED_FLOW_ASOF:'Original retained flow joined (partial stream)',NOT_YET_EMITTED:'Not yet emitted at trade clock',
  NO_MATCHING_VALUE_IN_RETAINED_INPUT:'No joined value',MISSING_STATIC_SOURCE:'Missing knowledge source',
  ORIGINAL_VALUES_JOINED:'Original fields joined',STATIC_KNOWLEDGE_PINNED:'Source pin only',
  ORIGINAL_TRADE_OPERANDS_ONLY:'Trade operands only',ORIGINAL_PUBLICATION_VALUES_JOINED:'Publication records joined',
  ORIGINAL_SECOND_SET_WITH_STATES:'Second-set states retained',
  STATIC_KNOWLEDGE_CONTENT_RECOVERED:'Knowledge content restored',
  PROVISIONAL_SOURCE_TEXT_RECOVERED:'Provisional source restored'};

const workbook=Workbook.create();
const sheets={};
const layouts=[];
function col(n){let s='';for(n++;n;n=Math.floor((n-1)/26))s=String.fromCharCode(65+(n-1)%26)+s;return s;}
function table(name,headers,rows,widths,options={}){
  const sheet=workbook.worksheets.add(name);sheets[name]=sheet;
  sheet.showGridLines=false;
  const last=col(headers.length-1),end=rows.length+1;
  sheet.getRange(`A1:${last}${end}`).values=[headers,...rows];
  const formatEnd=options.dense?Math.min(end,9):end;
  const visible=sheet.getRange(`A1:${last}${formatEnd}`);
  visible.format.font={name:'Arial',size:10,color:'#223044'};
  visible.format.verticalAlignment='center';visible.format.rowHeight=options.rowHeight??32;
  visible.format.wrapText=true;
  const heading=sheet.getRange(`A1:${last}1`);
  heading.format.fill='#273F5B';heading.format.font={name:'Arial',size:10,bold:true,color:'#FFFFFF'};
  heading.format.rowHeight=options.headerHeight??44;
  heading.format.horizontalAlignment='center';
  widths.forEach((w,i)=>sheet.getRange(`${col(i)}1`).format.columnWidth=w);
  sheet.freezePanes.freezeRows(1);
  if(options.freezeColumns)sheet.freezePanes.freezeColumns(options.freezeColumns);
  if(!options.dense)sheet.tables.add(`A1:${last}${end}`,true,name.replace(/[^A-Za-z0-9]/g,'')+'Table');
  layouts.push({name,rows:end,columns:headers.length});
  console.log(`${name}: ${rows.length.toLocaleString('en-US')} rows`);
  return sheet;
}
function coverage(day,column){
  if(staticMap.has(column))return [{status:staticMap.get(column).status,rows:day.trades}];
  if(coverageUpdates[day.day]?.[column])return [coverageUpdates[day.day][column]];
  const found=day.layers.filter(x=>x.column===column);
  if(found.reduce((n,x)=>n+x.rows,0)!==day.trades)throw Error(`Coverage mismatch ${day.day} ${column}`);
  return found;
}
function coverageText(day,column){
 if(['L055 | legacy_native_signed_flow','L056 | legacy_per_second_roll20'].includes(column)){
  const c=flowCoverage[day.day];return `${c.matched.toLocaleString('en-US')} trades joined to saved emissions\n${c.not_yet_emitted} not yet emitted${c.complete_flow_stream?'':'\nRetained projection; full stream unverified'}`;
 }
 const number=layers.find(l=>l.column===column)?.number;
 if(mboNumbers.includes(number))return 'Complete restored MBO stream\nActual counts and values in MBO layer data';
 if(nativeBindingColumns.has(column)&&nativePublications.some(p=>p.day===day.day))return 'Original Native ledger restored\nLatest-emission examples populated; full named-layer semantics remain open';
 return coverage(day,column).map(x=>`${statusNames[x.status]??x.status}: ${x.rows.toLocaleString('en-US')}`).join('\n');
}
function payload(text,kind){
  const sha=crypto.createHash('sha256').update(text).digest('hex');
  if(payloadByHash.has(sha))return payloadByHash.get(sha).id;
  const id='P'+String(payloadByHash.size+1).padStart(5,'0');
  const chunks=[];
  for(let i=0;i<text.length;i+=120)chunks.push(text.slice(i,i+120));
  if(chunks.join('')!==text)throw Error('Payload reconstruction differs');
  payloadByHash.set(sha,{id,text,sha,kind,chunks});
  return id;
}
const payloadByHash=new Map();

const review=workbook.worksheets.add('Review');sheets.Review=review;
review.showGridLines=false;review.tabColor='#273F5B';
review.getRange('A1:D34').format.font={name:'Arial',size:10,color:'#223044'};
review.getRange('A1:D34').format.rowHeight=24;
review.getRange('A1:A34').format.columnWidth=34;
review.getRange('B1:B34').format.columnWidth=95;
review.getRange('A2').values=[['Frankie four-day layer review']];
review.getRange('A2').format.font={name:'Arial',size:14,bold:true};
review.getRange('A4:B17').values=[
 ['Completion','INCOMPLETE — recovery in progress'],
 ['Sheet locking','Unlocked until every required layer is verified'],
 ['Layer columns',layers.length],
 ['Canonical registry entries',99],['External inputs',13],['Second-set components',19],
 ['Saved trade population',summary.trades],['Pinned source files',pins.sources.length],
 ['Knowledge/control layers restored',staticLayers.length],['Restored original source files',72],
 ['Findings documents retained',summary.findings_documents],['Brain manifest entries',brainReceipt.manifest_entries],
 ['Original trade examples',samples.length],['Book/FIFO recovery',`All four calculations verified; ${publications.length} dates published to Git`]];
review.getRange('B4').format.fill='#FCE8E6';review.getRange('B4').format.font={name:'Arial',size:10,color:'#9B2925',bold:true};
review.getRange('B6:B16').setNumberFormat('#,##0');
review.getRange('A19:B25').values=[
 ['Scope','October 2, 3, 17 and 18, 2023. October 2 and 17 retain their archived partial-session scope.'],
 ['Coverage counts','Counts describe saved payload states. A joined row does not prove the entire named layer is complete.'],
 ['Recovered full depth',`Full depth and FIFO replace partial review values for published dates: ${publications.map(p=>p.day).join(', ')}. Earlier assembly payloads are also retained.`],
 ['Layer values','Each labeled layer column contains an exact value or a payload ID. Decode each JSON text chunk, then join in order.'],
 ['Example selection','First, middle and last trade per day, plus the smallest retained FIFO example from the first October 18 shard.'],
 ['Knowledge and findings','Full source text is retained through payload IDs in Brain contents. Research claims retain their original limitations.'],
 ['Next gate','Fill remaining data, verify every required layer, then lock the sheets and connect the runtime by layer ID.']];
review.getRange('B19:B25').format.wrapText=true;review.getRange('A19:B25').format.rowHeight=40;
review.getRange('A27:B29').values=[
 ['MBO records restored','3,301,671 archived-session messages plus 1,650,054 opening-warmup messages; counted separately.'],
 ['Flow tables','143,266 trade rows have saved emissions. Four early October 2 rows remain explicitly not yet emitted.'],
 ['Data source','Git-only recovery. October 2 second-set calculation continues in resumable GitHub segments.']];
review.getRange('A30:B34').values=[
 ['Full book and FIFO','Full book sources and Book packet files identify every pinned shard. FIFO order examples expands every resting order from 12 saved full-depth examples.'],
 ['Saved dipole data','Dipole coverage, candidates, episodes and stage series span all four dates. Generated dipole clocks and Whole lifecycle parents preserve the other workflow views.'],
 ['Both four-day workflows','Workflow findings and Workflow and research files bind the Combined Event Studies and Whole Lifecycle Audit, with their complete output paths.'],
 ['Dipole lead timing','Dipole lead timing preserves the historical Bitcoin-to-NG timing lineage and the reported roughly 0.5-second NG lead. The exact later NG calculation is still open. Delayed outcomes are separate.'],
 ['Review order','Review these unlocked sheets. Lock approved cells, bind Frankie to layer IDs and immutable source files, then reanalyze.']];
review.getRange('A27:B34').format.rowHeight=48;review.getRange('B27:B34').format.wrapText=true;
layouts.push({name:'Review',rows:34,columns:2});

table('Layer coverage',['Trading date','Archived span','Trades',...layers.map(x=>x.column)],
 days.map(d=>[new Date(`${d.day.slice(0,4)}-${d.day.slice(4,6)}-${d.day.slice(6,8)}T00:00:00Z`),
 ['20231002','20231017'].includes(d.day)?'Partial session':'Full session',d.trades,...layers.map(l=>coverageText(d,l.column))]),
 [14,20,12,...layers.map(()=>38)],{headerHeight:78,rowHeight:76,freezeColumns:3});
sheets['Layer coverage'].getRange('A2:A5').setNumberFormat('mm/dd/yy');
sheets['Layer coverage'].getRange('C2:C5').setNumberFormat('#,##0');

table('Layer directory',['Layer number','Column label','Definition','Role','Original source-path count','Interpretation'],
 layers.map(l=>[l.number,l.column,l.description??l.layer_id,l.policy,l.source_paths?.length??l.point?.series?.length??0,
 l.number===39?'Full book values restored for published dates; original aggregate/group-close phases remain separate.':
 l.number>=41&&l.number<=44?'Full original FIFO snapshots restored for published dates. Present-state age does not establish complete cross-time survival.':
 l.policy==='APPEND_ONLY_OUTPUT'?'Runtime output role. Source pins do not establish a produced output.':
 l.policy==='SEALED_FOR_A_SCOPE'?'Outcome/target data must remain separate from earlier causal input values.':
 l.policy==='PROVISIONAL_SHADOW'?'Source text recovered; no claim this runtime was executed.':
 staticMap.has(l.column)?'All named original source texts restored and verified.':
 l.group==='second_set_components'?'October 18 original states retained. Other dates not yet recovered.':
 l.group==='external_13_inputs'?'Original publication records, including missing/invalid states. Publication is not live ingestion.':
 'See per-day coverage and original payload state.']),[13,54,70,32,18,84],{rowHeight:58,freezeColumns:2});

const valueRows=[];
for(const sample of samples){
  const row=[sample.trade_id,'ns '+sample.receive_ns,'ns '+sample.known_by_ns];
  for(const layer of layers){
    const raw=staticMap.has(layer.column)?JSON.stringify(staticMap.get(layer.column)):sample[layer.column];
    if(typeof raw!=='string'||!raw.length)throw Error(`Missing sample cell ${sample.trade_id} ${layer.column}`);
    const state=JSON.parse(raw).status;
    const id=payload(raw,'layer payload JSON');
    const scalar=raw.match(/"values":\s*(-?\d+(?:\.\d+)?)(?=[,}])/);
    row.push(`${statusNames[state]??state}\n${scalar?scalar[1]+'\n':''}${id}`);
  }
  valueRows.push(row);
}
table('Trade layer values',['Trade ID','Receive time (ns, exact text)','Group-known time (ns, exact text)',...layers.map(x=>x.column)],valueRows,
 [28,27,27,...layers.map(()=>38)],{rowHeight:72,headerHeight:78,freezeColumns:1});
sheets['Trade layer values'].getRange(`B2:C${valueRows.length+1}`).setNumberFormat('@');

for(const [name,data] of Object.entries(expandedTables)){
  const widths=data.headers.map(header=>/URL|Git file|Source file|Git file|JSON|array|path/i.test(header)?58:
    /receive|recognition|clock|sha-256|Git blob|commit|boundary/i.test(header)?31:22);
  table(name,data.headers,data.rows,widths,{rowHeight:32,headerHeight:58,freezeColumns:1,dense:data.rows.length>1000});
}

const brainRows=[];
for(const entry of brainManifest.entries){
 const text=await fs.readFile(path.join(root,'consolidated-recovery/brain/20261109-search',entry.name),'utf8');
 if(crypto.createHash('sha256').update(text).digest('hex')!==entry.sha256)throw Error('Brain file mismatch '+entry.name);
 brainRows.push([entry.name,entry.kind??'retained document',payload(text,'brain source text'),entry.bytes,entry.sha256,entry.source]);
}
table('Brain contents',['Document','Original role and scope','Full text payload ID','Bytes','SHA-256','Original source'],brainRows,[74,80,22,14,72,120],{rowHeight:58,freezeColumns:1});
sheets['Brain contents'].getRange(`D2:D${brainRows.length+1}`).setNumberFormat('#,##0');

const externalPayloadIds=[];
for(const r of externalValues)externalPayloadIds.push(payload(await fs.readFile(path.join(root,`filled-review/external-point-${String(r.point_id).padStart(2,'0')}.json`),'utf8'),'restored external value JSON'));
const forecastPayloadIds=forecastRecovery.forecast_rows.map(r=>payload(JSON.stringify(r),'restored forecast JSON'));
const disagreementPayloadIds=forecastRecovery.disagreement_cycles.map(r=>payload(JSON.stringify(r),'restored model disagreement JSON'));
const mboPayloadIds=[];
for(const r of mboDays)mboPayloadIds.push(payload(await fs.readFile(path.join(root,`mbo-layer-data/${r.day}.json`),'utf8'),'complete MBO inventory and exact original message examples'));
const payloadRows=[];
for(const p of payloadByHash.values())p.chunks.forEach((chunk,i)=>payloadRows.push([p.id,i+1,p.chunks.length,JSON.stringify(chunk)]));
table('Payload text',['Payload ID','Chunk','Total chunks','JSON text chunk (decode, then concatenate in numeric order)'],payloadRows,[15,10,14,180],{rowHeight:42,headerHeight:34,freezeColumns:1,dense:true});
table('Payload index',['Payload ID','Kind','Characters','SHA-256 of UTF-8 text','Chunks'],[...payloadByHash.values()].map(p=>[p.id,p.kind,p.text.length,p.sha,p.chunks.length]),[15,26,16,74,12],{rowHeight:24,headerHeight:34});

table('Source pins',['Repository','Revision','Original file path','Bytes','SHA-256','Role','Verification'],
 pins.sources.map(p=>[p.repository,p.revision,p.source_path??p.path,p.bytes,p.sha256,p.role,p.status]),[34,47,130,15,74,26,24],{rowHeight:44,freezeColumns:1});
sheets['Source pins'].getRange(`D2:D${pins.sources.length+1}`).setNumberFormat('#,##0');
table('Source locations',['Record','Immutable Git location'],[
 ['Original data assembly',packetUrl],['Original layer registry',packetUrl.replace('/tree/','/blob/')+'/LAYERS.json'],
 ['Combined recovery pins and updated brain',consolidatedUrl],
 ['Static-source and findings recovery',staticUrl],['Native brain loader verification',staticUrl.replace('/tree/','/blob/')+'/BRAIN_LOAD_RECEIPT.json'],
 ['Full book and FIFO recovery workflow',jobUrl],
 ...publications.map(p=>['Recovered full book and FIFO '+p.day,`https://github.com/${p.repository}/tree/${p.revision}/${p.prefix}`]),
 ...nativePublications.map(p=>['Recovered complete Native ledger '+p.day,`https://github.com/${p.repository}/tree/${p.revision}/${p.prefix}`]),
 ['Restored October 2 external observations','https://github.com/DavisAI1974/markets-data/tree/975d79bcb59ecaa7b128c53a774edee5274df8ca/tasks/family-research-20261022/frankie-four-day-pins/external-recovery-20261109'],
 ['All four full-population flow tables','https://github.com/DavisAI1974/markets-data/tree/5828b1ad78d09ebf8da995c822408e759f41ae06/tasks/family-research-20261022/frankie-four-day-pins/flow-input-recovery-20261109'],
 ['MBO action inventory and original examples','https://github.com/DavisAI1974/markets-data/tree/21a8bf9ec122a8156d662e60809d5efe98c043f9/tasks/family-research-20261022/frankie-four-day-pins/mbo-layer-data-20261109'],
 ['Original dipole research workbook','https://github.com/DavisAI1974/markets-data/blob/2fe4aaffe596e01167af24a979bf07a69f40771f/tasks/family-research-20261022/native-dipole/20261108-33693e180/agent-pass/research-tables.xlsx'],
 ['October 2 resumable second-set replay','https://github.com/DavisAI1974/markets-data/actions/runs/42640458600'],
 ['Complete row payloads','Original data assembly contains 143,270 rows in day-specific Parquet shards. The workbook contains 13 declared examples, not all trade rows.'],
 ['Integer clocks','Nanosecond clocks and full JSON payloads are stored as text to preserve every digit.'],
 ['Missing values','Original missing/invalid states are retained. No missing observation is converted to zero.'],
 ['Protection gate','This incomplete workbook is deliberately unlocked. Runtime sheet integration is pending complete verified inputs.'],
 ['Archive correction','Historical ROOT frame archives exist in Git. Exclusion from the frozen packet was not proof that the original data was absent.']],
 [42,150],{rowHeight:48,headerHeight:32});

const externalDisplay=p=>{
 const original=p.original_available_reconstruction;
 if(original)return Object.entries(original).filter(([k,v])=>typeof v==='number'||['units','report_date','week_ending','print_date'].includes(k)).map(([k,v])=>`${k}: ${v}`).join('\n');
 if(p.point_id===2)return '71 restored forecast records in Forecast recovered; release clock remains held.';
 if(p.point_id===9)return '6 restored model comparisons in Disagreement recovered; release clock remains held.';
 const fields={5:['wind_mwh'],7:['est_gas_burn_bcfd_rate'],10:['gw_hdd'],13:['front_next_spread','slope_1','slope_back']};
 const values=p.latest_retained_examples.flatMap(r=>(fields[p.point_id]??[]).filter(k=>k in r.numeric).map(k=>`${r.point_name} / ${k}: ${r.numeric[k]}`));
 return 'Retained examples; availability remains held:\n'+values.join('\n');
};
table('Recovered external',['Trading date',...layers.filter(l=>l.group==='external_13_inputs').map(l=>l.column)],
 [['20231002',...externalValues.map((p,i)=>`${p.status}\n${externalDisplay(p)}\nFull values and source clocks: ${externalPayloadIds[i]}`)]],
 [15,...externalValues.map(()=>82)],{rowHeight:200,headerHeight:74,freezeColumns:1});
table('Forecast recovered',['Model','Model runtime UTC','Target date','X02 | weather_forecast.forecast_gw_hdd','Related GW CDD','Coverage','Modeled availability (ns)','Full original payload','Availability restriction'],
 forecastRecovery.forecast_rows.map((r,i)=>[r.model,r.runtime_utc,r.target_day,r.gw_hdd,r.gw_cdd,r.coverage,'ns '+r.catalog_modeled_available_ns,forecastPayloadIds[i],forecastRecovery.clock_limit]),
 [12,24,16,30,20,14,30,24,85],{rowHeight:56,headerHeight:68});
table('Disagreement recovered',['Model runtime UTC','Target date of maximum','X09 | model_disagreement.summary.max_abs_spread_gw_hdd','Modeled availability (ns)','Full original payload','Availability restriction'],
 forecastRecovery.disagreement_cycles.map((r,i)=>[r.runtime_utc,r.max_at_target,r.max_abs_spread_gw_hdd,'ns '+r.catalog_modeled_available_ns,disagreementPayloadIds[i],forecastRecovery.clock_limit]),
 [24,24,44,30,24,85],{rowHeight:56,headerHeight:68});
table('Calendar values',['Trading date','X06 | squeeze_watch.sessions_since_prompt_expiry','Previous prompt symbol','Previous expiry date','Availability meaning'],
 Object.entries(calendarRecovery.values).map(([day,r])=>[day,r.sessions_since_prompt_expiry,r.last_prompt_symbol,r.last_prompt_expiry,calendarRecovery.availability_rule]),
 [16,36,24,24,100],{rowHeight:56,headerHeight:68});

const actionByLayer={27:'all_messages',29:'all_messages',30:'A',31:'C',32:'M',33:'M',34:'T',35:'F',36:'R',37:'all_messages'};
table('MBO layer data',['Trading date',...mboNumbers.map(n=>layers.find(l=>l.number===n).column)],mboDays.map((r,i)=>[r.day,...mboNumbers.map(n=>{
 const session=r.counts.archived_session,warmup=r.counts.opening_warmup,action=actionByLayer[n];
 const text=action?`Archived ${action}: ${(session[action]??0).toLocaleString('en-US')}\nWarmup ${action}: ${(warmup[action]??0).toLocaleString('en-US')}`:
  `Archived snapshots: ${session.snapshot??0}\nArchived resets: ${session.R??0}\nWarmup snapshots: ${warmup.snapshot??0}\nWarmup resets: ${warmup.R??0}\nSnapshots and resets can overlap.`;
 return `${text}\n${n===33?'M replaces the same order state; R clears.\n':''}${n===37?'Every original order ID and effect retained.\n':''}Full examples and immutable source: ${mboPayloadIds[i]}\nDaily audit totals; not earlier-trade features.`;
})]),[16,...mboNumbers.map(()=>48)],{rowHeight:160,headerHeight:78,freezeColumns:1});
table('Flow coverage',['Trading date','Saved trades','L055 | legacy_native_signed_flow — matched trade rows','L056 | legacy_per_second_roll20 — matched trade rows','Not yet emitted','Original flow rows','Source scope'],
 flowSummary.map(r=>[r.day,r.trades,r.matched_original_emissions,r.matched_original_emissions,r.not_yet_emitted??r.not_yet_emitted_in_retained_projection??0,r.original_flow_rows,r.complete_flow_stream===false?'Original retained projection; complete Native stream unverified':'Complete recovered Native lifecycle ledger']),
 [16,16,38,38,22,22,74],{rowHeight:58,headerHeight:80});

const check=await workbook.inspect({kind:'table',range:'Review!A4:B17',include:'values,formulas',tableMaxRows:14,tableMaxCols:2,maxChars:3000});
await fs.writeFile(path.join(root,'review-inspection.ndjson'),check.ndjson);
for(const layout of layouts.filter(x=>['Review','Layer coverage','Trade layer values','Full book sources','FIFO order examples','Dipole coverage','Dipole candidates','Dipole lead timing','Delayed outcomes','Workflow findings'].includes(x.name))){
 const range=layout.name==='Review'?'A2:B34':layout.name==='Layer coverage'?'A1:F5':layout.name==='Trade layer values'?'A1:E4':layout.name==='Payload text'?'A1:D8':
 layout.name==='Layer directory'?'A1:C5':layout.name==='Brain contents'?'A1:C5':layout.name==='Source pins'?'A1:C5':`A1:${col(Math.min(layout.columns,4)-1)}${Math.min(layout.rows,8)}`;
 const rendered=await workbook.render({sheetName:layout.name,range,scale:1,format:'png'});
 await fs.writeFile(path.join(root,layout.name.replaceAll(' ','_')+'.png'),new Uint8Array(await rendered.arrayBuffer()));
}
const filename=path.join(out,'Frankie_four_day_layer_review.xlsx');
console.log('Exporting XLSX');
await (await SpreadsheetFile.exportXlsx(workbook)).save(filename);
await fs.writeFile(path.join(root,'workbook-verification.json'),JSON.stringify({file:filename,layer_columns:layers.length,trade_examples:samples.length,
  source_pins:pins.sources.length,static_layers_restored:staticLayers.length,brain_entries:brainRows.length,
  payloads:payloadByHash.size,payload_chunks:payloadRows.length,sheets:layouts,complete_all_layers:false,locked:false,
  payload_roundtrip:'all exact source strings reconstructed from ordered JSON-encoded chunks',packet_revision:packetRev,static_recovery_revision:staticRev},null,2));
console.log(JSON.stringify({file:filename,sheets:layouts.length,layer_columns:layers.length,payload_chunks:payloadRows.length,complete_all_layers:false}));
