# SAMPLE_COMPARISON

- doc_id: `pics_pe00917_annex15_20230825`
- review candidate path: `runs/20260522-053004_text2ir-goal-gap-longrun/review_candidate/pics_pe00917_annex15_20230825/`
- source regeneration bundle: `out/20260522-053004_text2ir-goal-gap-longrun/pics_pe00917_annex15_20230825/`

## Scope

This file records representative node samples for human review. It checks that selectable nodes have readable context, traceable `nid`, and source locator information. Table-specific checks are not expected for these three review candidates unless table nodes appear in the source bundle.

## Representative Nodes

### Sample 1

- selectable node: `ann15`
- kind: `annex`
- human readable path: document > QUALIFICATION AND VALIDATION
- heading: QUALIFICATION AND VALIDATION
- text: PRINCIPLE This Annex describes the principles of qualification and validation which are applicable to the facilities, equipment, utilities and processes used for the manufacture...
- source_spans: `26` span(s)
- first source span: `{'source_label': 'PIC/S', 'locator': 'line:1'}`

YAML fragment:

```yaml
nid: ann15
kind: annex
num: '15'
heading: QUALIFICATION AND VALIDATION
text: 'PRINCIPLE


  This Annex describes the principles of qualification and validation which are applicable
  to the facilities, equipment, utilities and processes used for the manufacture of
  medicinal products and may also be used as supplementary optional guidance for active
  substances without introduction of additional requirements to Part II. It is a GMP
  requirement that manufacturers control the critical aspects of their particular
  operations through qualification and validation over the life cycle of the product
  and process. Any planned changes to the facilities, equipment, utilities and processes,
  which may affect the quality of the product, should be formally documented and the
  impact on the validated status or control strategy assessed. Computerised systems
  used for the manufacture of medicinal products should also be validated according
  to the requirements of Annex 11. The relevant concepts and guidance presented in
  ICH Q8, Q9, Q10 and Q11 should also be taken into account.


  GENERAL A quality risk management approach should be applied throughout the lifecycle
  of a medicinal product. As part of a quality risk management system, decisions on
  the scope and extent of qualification and validation should be based on a justified
  and documented risk assessment of the facilities, equipment, utilities and processes.
  Retrospective validation is no longer considered an acceptable approach.


  Data supporting qualification and/or validation studies which were obtained from
  sources outside of the manufacturers own programmes may be used provided that this
  approach has been justified and that there is adequate assurance that controls were
  in place throughout the acquisition of such data.'
ord: 1
role: structural
normativity: null
source_spans:
- source_label: PIC/S
  locator: line:1
- source_label: PIC/S
  locator: line:6
- source_label: PIC/S
  locator: line:8
- source_label: PIC/S
  locator: line:9
- source_label: PIC/S
  locator: line:10
- source_label: PIC/S
  locator: line:11
- source_label: PIC/S
  locator: line:12
- source_label: PIC/S
  locator: line:13
- source_label: PIC/S
  locator: line:14
- source_label: PIC/S
  locator: line:15
- source_label: PIC/S
  locator: line:16
- source_label: PIC/S
  locator: line:17
- source_label: PIC/S
  locator: line:18
- source_label: PIC/S
  locator: line:19
- source_label: PIC/S
  locator: line:20
- source_label: PIC/S
  locator: line:22
- source_label: PIC/S
  locator: line:23
- source_label: PIC/S
  locator: line:24
- source_label: PIC/S
  locator: line:25
- source_label: PIC/S
  locator: line:26
- source_label: PIC/S
  locator: line:27
- source_label: PIC/S
  locator: line:28
- source_label: PIC/S
  locator: line:30
- source_label: PIC/S
  locator: line:31
- source_label: PIC/S
  locator: line:32
- source_label: PIC/S
  locator: line:33
```

Review observations:

- The `nid` is present and can be traced in the hierarchy.
- The human readable path includes ancestor context when available.
- Source locator information is present for audit review when the node has a span.

### Sample 2

- selectable node: `ann15.sec1`
- kind: `section`
- human readable path: document > QUALIFICATION AND VALIDATION > ORGANISING AND PLANNING FOR QUALIFICATION AND VALIDATION
- heading: ORGANISING AND PLANNING FOR QUALIFICATION AND VALIDATION
- text: null
- source_spans: `1` span(s)
- first source span: `{'source_label': 'PIC/S', 'locator': 'line:36'}`

YAML fragment:

```yaml
nid: ann15.sec1
kind: section
num: '1'
heading: ORGANISING AND PLANNING FOR QUALIFICATION AND VALIDATION
text: null
ord: 2
role: structural
normativity: null
source_spans:
- source_label: PIC/S
  locator: line:36
```

Review observations:

- The `nid` is present and can be traced in the hierarchy.
- The human readable path includes ancestor context when available.
- Source locator information is present for audit review when the node has a span.

### Sample 3

- selectable node: `ann15.sec1.p1_1`
- kind: `paragraph`
- human readable path: document > QUALIFICATION AND VALIDATION > ORGANISING AND PLANNING FOR QUALIFICATION AND VALIDATION > 1.1
- heading: null
- text: All qualification and validation activities should be planned and take the life cycle of facilities, equipment, utilities, process and product into consideration.
- source_spans: `2` span(s)
- first source span: `{'source_label': 'PIC/S', 'locator': 'line:38'}`

YAML fragment:

```yaml
nid: ann15.sec1.p1_1
kind: paragraph
num: '1.1'
heading: null
text: All qualification and validation activities should be planned and take the life
  cycle of facilities, equipment, utilities, process and product into consideration.
ord: 3
role: normative
normativity: must
source_spans:
- source_label: PIC/S
  locator: line:38
- source_label: PIC/S
  locator: line:39
```

Review observations:

- The `nid` is present and can be traced in the hierarchy.
- The human readable path includes ancestor context when available.
- Source locator information is present for audit review when the node has a span.

## Ancestor / Descendant Confirmation

- Ancestor context: representative paths above show the containing structural context.
- Descendant context: no table descendant case is expected in these three candidates; table/note descendant behavior is covered by `TABLE_NOTE_REAL_SAMPLE_REVIEW.md` and related fixtures.
- Promotion status: review candidate only; no `data/normalized/` copy was made.
