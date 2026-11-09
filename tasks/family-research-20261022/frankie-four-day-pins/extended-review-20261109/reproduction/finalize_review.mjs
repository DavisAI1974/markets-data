import fs from 'node:fs/promises';
import path from 'node:path';
import { FileBlob, SpreadsheetFile, Workbook } from '@oai/artifact-tool';

const root = 'E:/frankie-excel-review-20261109';
const input = path.join(root, 'outputs/extended-four-day-review/Frankie_four_day_layer_review.xlsx');
const dest = path.join(root, 'outputs/extended-four-day-review-final');
await fs.mkdir(dest, { recursive: true });
const deltaOnly = process.argv.includes('--delta');
const workbook = deltaOnly ? Workbook.create() : await SpreadsheetFile.importXlsx(await FileBlob.load(input));
console.log(deltaOnly ? 'Building replacement sheets' : 'Imported expanded review');
const tables = JSON.parse(await fs.readFile(path.join(root, 'extended-review-data/WORKFLOW_TABLES.json'), 'utf8'));
for (const name of ['Delayed outcomes', 'Delayed outcome conditions', 'Whole lifecycle parents',
  'Lifecycle component windows']) {
  if (!deltaOnly) workbook.worksheets.getItem(name).delete();
  delete tables[name];
}
const files = tables['Workflow and research files'];
files.rows = files.rows.filter(row => !/(?:b-delayed-outcomes|cross-study-condition-outcomes)\.parquet$/.test(row[2]));
for (const row of files.rows) {
  if (row[2].startsWith('whole-lifecycles/')) row[6] = 'Archived prior second-workflow calculation. Excluded from reanalysis.';
}
const findings = tables['Workflow findings'];
findings.rows = findings.rows.filter(row => row[1] !== 'Whole lifecycle audit' &&
  !['B.delayed_outcomes', 'B.definitions'].includes(row[2]));
const research = tables['Research sets'];
for (const row of research.rows) {
  if (row[0] === 'Whole lifecycle audit') row[0] += ' (prior calculations, archive only)';
}
const clockTables = JSON.parse(await fs.readFile(path.join(root, 'extended-review-data/LATE_CLOCK_TABLES.json'), 'utf8'));
Object.assign(tables, clockTables);
function replaceTable(name, widths) {
  const old = workbook.worksheets.items.find(sheet => sheet.name === name);
  if (old) old.delete();
  const { headers, rows } = tables[name];
  const sheet = workbook.worksheets.add(name);
  sheet.showGridLines = false;
  sheet.getRangeByIndexes(0, 0, rows.length + 1, headers.length).values = [headers, ...rows];
  const header = sheet.getRangeByIndexes(0, 0, 1, headers.length);
  header.format.fill = '#273F5B';
  header.format.font = { name: 'Arial', size: 10, bold: true, color: '#FFFFFF' };
  header.format.rowHeight = 28;
  for (const [i, width] of widths.entries()) sheet.getCell(0, i).format.columnWidth = width;
  sheet.freezePanes.freezeRows(1);
  sheet.freezePanes.freezeColumns(1);
}
replaceTable('Workflow and research files', [36, 16, 65, 17, 46, 46, 47, 65]);
replaceTable('Workflow findings', [16, 35, 45, 60, 65]);
replaceTable('Research sets', [58, 14, 18, 46, 65]);
replaceTable('Late-session clock tables', [23, 26, 26, 72, 16, 16, 20, 17, 46, 65, 65]);
replaceTable('Late-session clock files', [16, 72, 18, 46, 46, 65, 65]);

const timing = tables['Dipole lead timing'];
timing.rows[5] = ['Outcome rule', 'Four archived NG dates', 'Observed result after each decision',
  'Derive the outcome from later observed MBO and FIFO replay for the event.',
  'Review and runtime binding pending', 'Pinned MBO and full-book sources',
  'Record decision and outcome clocks separately. Preserve unresolved outcomes.'];
if (deltaOnly) {
  replaceTable('Dipole lead timing', [36, 33, 44, 68, 66, 66, 66]);
  const lead = workbook.worksheets.getItem('Dipole lead timing');
  lead.getRange('A2:G7').format.rowHeight = 67;
  lead.getRange('A2:G7').format.wrapText = true;
} else {
  workbook.worksheets.getItem('Dipole lead timing').getRange('A7:G7').values = [timing.rows[5]];
}
const review = deltaOnly ? workbook.worksheets.add('Review') : workbook.worksheets.getItem('Review');
review.getRange('A31:B36').values = [[
  'Saved dipole data',
  'Dipole coverage, candidates, episodes and stage series span all four dates. Generated dipole clocks retains the event-study clocks.'], [
  'Four-day workflow sources',
  'Workflow findings includes retained Combined Event Studies metrics. Workflow and research files links both original workflow archives.'], [
  'Dipole lead timing',
  'Historical Bitcoin-to-NG timing sources and the reported roughly 0.5-second NG lead are listed. The exact NG calculation is still open. Derive future analysis outcomes from the observed tape.'], [
  'Late-session dipole and clock pins',
  'Late-session clock tables and files index the complete eligible clock archive and exact corrected Tier 1 files. The source shards remain in Git.'], [
  'Second-workflow refresh',
  'Prior Whole lifecycle audit calculations for all four days are archived only. Refresh this workflow from the populated inputs. The separate in-progress Git replay will be omitted from the initial reanalysis.'], [
  'Review order',
  'Review these unlocked sheets. Lock approved cells, bind Frankie to layer IDs and immutable source files, then reanalyze.']];
review.getRange('A31:B36').format.rowHeight = 52;
review.getRange('B31:B36').format.wrapText = true;

await fs.writeFile(path.join(root, 'extended-review-data/WORKFLOW_FINAL_TABLES.json'), JSON.stringify(tables));
console.log('Saving final unlocked review');
const target = deltaOnly ? path.join(root, 'extended-review-data/review-sheet-replacements.xlsx')
  : path.join(dest, 'Frankie_four_day_layer_review.xlsx');
await (await SpreadsheetFile.exportXlsx(workbook)).save(target);
console.log('Final unlocked review exported');
