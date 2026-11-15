"""Make the exact remaining 35-field status durable; never fill blanks with reasons."""
import hashlib
import json
from pathlib import Path
from remaining_fields import OUT, NEW, read, write, pin


def main():
    baseline = read(OUT / 'WORKBOOK_REPAIR_PREPARATION.json')
    supplement = read(OUT / 'REMAINING_FIELD_RECOVERY.json')
    fields = [k for k, v in baseline['still_missing_field_rows'].items() if k.startswith('L') and v == 5513]
    assert len(fields) == 35
    reasons = {
        'L024': 'Exact 2021 object identities/bytes/SHA256 are recovered in CANONICAL_2021_OBJECT_IDENTITIES.json. Raw DBN bytes were not fetched or replayed. The four 2023 tapes are not substitutes. AWS is unavailable per user.',
        'L026': 'Needs the exact bootstrap object selection and continuous replay receipt for the intended canonical run. A guessed predecessor date or a 2023 opening snapshot is insufficient.',
        'L060': 'Needs the binding D-family geometry producer and its full causal input sequence. The saved C15 D1-D6 implementation is a different, explicitly scoped surface and would also recompute stopped S components; it was not run.',
        'L061': 'Needs the binding P/O/S/X predecessor-state producer and complete state transitions. Latest native observations do not establish active predecessor state.',
        'L062': 'Needs structural ancestry identities and gap calculations under the same binding geometry definition. Native order lineage and inter-message recurrence gaps are not substitutes.',
        'L063': 'Needs the complete unresolved-age and chain/extension state history from its exact producer. Existing S values were preserved, not recalculated or repurposed as full state.',
        'L067': 'Needs a prospective predecessor-defined risk-set producer and complete opportunity ledger, including opportunities with no later discovery.',
        'L068': 'Needs prospective unresolved chain/extension state before onset, with explicit availability. A candidate emitted after detection is not pre-birth state.',
        'L069': 'Needs causal ancestry/successor opportunity identities and the matching producer, not retrospective candidate membership.',
        'L070': 'Needs the exact stopped-chain/false-context control population and producer. No arbitrary timeout or fabricated negative label was introduced.',
        'L071': 'Needs the complete prospectively defined negative-opportunity denominator and observation/censoring outcomes. Missing discoveries are not automatically negative cases.',
        'L077': 'Needs actual model evaluation records bound to the intended run and market cutoff. The recovered native calculation runner explicitly does not execute Frankie.',
        'L078': 'Needs actual immutable first-lock records from the intended model run. Candidate recognition times are not model lock times.',
        'L079': 'Needs the exact target outcome/reveal package and run binding. Retrospective printed-leg endpoints and native flow reversal labels are not substituted.',
        'L080': 'Needs answer-derived Step-1 ground-truth onset values under the exact target definition. Native candidate event seconds are a different clock.',
        'L083': 'Needs exact October Step-1 seconds from the sealed target package. Native 2023 flow seconds do not identify the canonical Step-1 package.',
        'L084': 'Needs exact Step-1 target populations and population manifest, not the selected 32 cases or the trade population relabeled as Step-1.',
        'L085': 'Needs exact Step-1 identity crosswalks to the intended source/target run. No positional join or inferred identity was used.',
        'L086': 'Needs target-membership receipts from the exact Step-1 package. Candidate membership is not Step-1 target membership.',
        'L087': 'Needs original Step-1 labels/classifications and source identities. The eight print-leg category labels remain separate provenance.',
        'L088': 'Needs the exact produced Step-1 result locations and artifact identities; launch configuration alone is not proof outputs exist.',
        'L089': 'Needs Step-1 reconciliation products tying the precise target population, clocks, classifications and source manifest together.',
        'L091': 'Needs actual Frankie reasoning records from the intended model run; native calculation evidence is not model reasoning.',
        'L092': 'Needs actual immutable probability outputs from the intended model run. No fitted probabilities, zero vectors or unrelated forecasts were substituted.',
        'L094': 'Needs genuine first-lock/no-lock run ledgers; not-running is not evidence for a completed no-lock decision.',
        'L095': 'Needs actual model abstention/weak/negative/sparse/inconclusive results. Reconstruction missingness is not a model result.',
        'L096': 'Needs actual knowledge-retrieval invocation receipts bound to the intended run. Static source files are not evidence the model retrieved them.',
        'L097': 'Needs actual provider requests/responses and invocation receipts. No provider was invoked by this repair.',
        'L098': 'Needs actual answer-wall access/no-access audit records for the intended run. The current retrospective user permission is not a historical no-access receipt.'
    }
    scopes = {
        'L025': 'Exact inventory metadata: [2021-10-01, 2021-11-01). Explicitly does not apply as the date window of a 2023 trade.',
        'L064': 'Complete selected-case trade prefix, exact price/flow/book values and consecutive-tick deltas. Intervening non-trade/per-second state is not asserted.',
        'L065': 'Original full FIFO/book and adapter activity contents with archived window definitions. Not a complete V4 geometry feature vector.',
        'L090': 'New hash-chained selected-tick state/delta movie for the recovered price/flow/book surface. Not a full experimental state movie or model run.',
        'L093': 'Every original archived native candidate discovery eligible at each trade clock/cursor. Calculation discoveries are not principal-model execution.',
        'L099': 'Actual reconstruction source/state/manifest/code hashes. Model and primary experiment run remain absent and explicitly null.'
    }
    rows = []
    for field in fields:
        code = field.split(' | ')[0]
        populated = supplement['fields_populated'].get(field, 0)
        rows.append(dict(field=field, newly_populated_rows=populated,
                         status='EXACT_METADATA' if code == 'L025' else 'SCOPED_CONTENT_RECOVERED' if populated else 'UNRESOLVED',
                         full_named_semantics_complete=code == 'L025',
                         evidence_or_required_dependency=scopes[code] if populated else reasons[code]))
    manifest_path = Path('E:/Markets/research/kalshi/NG_EXHAUSTION_MBO_5Y_CANONICAL_OBJECT_MANIFEST_20260822.json')
    manifest = read(manifest_path)
    objects = [r for r in manifest['canonical_dbn_objects'] if r['segment'] in ('20210901_20211001','20211001_20211101','20211101_20211201')]
    write(NEW / 'CANONICAL_2021_OBJECT_IDENTITIES.json', dict(source_manifest=pin(manifest_path),
          source_manifest_declared_sha256=manifest['manifest_sha256'], objects=objects,
          object_count=len(objects), raw_object_bytes_verified_this_run=False,
          scope='Canonical 2021 identity metadata only; not 2023 trade input and not a raw payload recovery.'))
    write(OUT / 'REMAINING_35_FIELD_STATUS.json', dict(fields=rows, exact_metadata_fields=1,
          scoped_content_fields=5, fields_without_produced_values=29, all_35_complete=False,
          aws_available=False, no_s_calculations_started=True, no_new_claude_results_consulted=True))
    paragraphs = [
        '# Remaining 35 fields: actual recovery and exact dependencies',
        '',
        'This repair adds 33,078 cell values across six previously empty fields and all 5,513 selected ticks. One is exact source-window metadata; five contain explicitly scoped recovered data. **This is not completion of all 35 fields.** Twenty-nine still have no produced values. Scope limitations remain inside the populated cells.',
        '',
        'All 32 cases, eight types, four dates and original S cells remain. No stopped S producer, model inference, new strategy, arbitrary horizon, or new independent Claude result was used. The complete 143,270-trade rebuild remains unfinished.',
        '',
        'AWS is unavailable. Local archives and the pinned Git source catalog were inspected. Canonical 2021 object identities are preserved separately, but the 2023 tapes are not relabeled as those objects. The native calculation runner explicitly says it does not execute Frankie or create locks; missing model output fields cannot be truthfully filled from it.',
        '',
        '| Field | Rows populated | Status | Evidence or remaining dependency |',
        '|---|---:|---|---|'
    ]
    for r in rows:
        paragraphs.append('| '+r['field'].replace(' | ',' — ')+' | '+str(r['newly_populated_rows'])+' | '+r['status']+' | '+r['evidence_or_required_dependency'].replace('|','/')+' |')
    paragraphs.extend(['', 'Oct18 L050/L051 also remain missing on 1,447 selected rows. Existing non-S partial semantics from the first repair remain documented in the cells.', '',
                       'Workbook readback is reported separately in WORKBOOK_READBACK_VERIFICATION.json. Supplemental source comparisons and hash-chain checks are in REMAINING_FIELD_VERIFICATION.json.'])
    (OUT / 'REMAINING_FIELDS.md').write_text('\n'.join(paragraphs)+'\n', encoding='utf8')


if __name__ == '__main__':
    main()
