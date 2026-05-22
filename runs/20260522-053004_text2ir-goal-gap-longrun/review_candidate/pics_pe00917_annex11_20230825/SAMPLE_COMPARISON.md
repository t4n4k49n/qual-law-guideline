# SAMPLE_COMPARISON

- doc_id: `pics_pe00917_annex11_20230825`
- review candidate path: `runs/20260522-053004_text2ir-goal-gap-longrun/review_candidate/pics_pe00917_annex11_20230825/`
- source regeneration bundle: `out/20260522-053004_text2ir-goal-gap-longrun/pics_pe00917_annex11_20230825/`

## Scope

This file records representative node samples for human review. It checks that selectable nodes have readable context, traceable `nid`, and source locator information. Table-specific checks are not expected for these three review candidates unless table nodes appear in the source bundle.

## Representative Nodes

### Sample 1

- selectable node: `ann11`
- kind: `annex`
- human readable path: document > COMPUTERISED SYSTEMS
- heading: COMPUTERISED SYSTEMS
- text: PRINCIPLE This annex applies to all forms of computerised systems used as part of a GMP regulated activities. A computerised system is a set of software and hardware components ...
- source_spans: `10` span(s)
- first source span: `{'source_label': 'PIC/S', 'locator': 'line:1'}`

YAML fragment:

```yaml
nid: ann11
kind: annex
num: '11'
heading: COMPUTERISED SYSTEMS
text: 'PRINCIPLE This annex applies to all forms of computerised systems used as part
  of a GMP regulated activities. A computerised system is a set of software and hardware
  components which together fulfil certain functionalities.


  The application should be validated; IT infrastructure should be qualified.


  Where a computerised system replaces a manual operation, there should be no resultant
  decrease in product quality, process control or quality assurance. There should
  be no increase in the overall risk of the process.


  GENERAL'
ord: 1
role: structural
normativity: null
source_spans:
- source_label: PIC/S
  locator: line:1
- source_label: PIC/S
  locator: line:6
- source_label: PIC/S
  locator: line:7
- source_label: PIC/S
  locator: line:8
- source_label: PIC/S
  locator: line:9
- source_label: PIC/S
  locator: line:11
- source_label: PIC/S
  locator: line:13
- source_label: PIC/S
  locator: line:14
- source_label: PIC/S
  locator: line:15
- source_label: PIC/S
  locator: line:19
```

Review observations:

- The `nid` is present and can be traced in the hierarchy.
- The human readable path includes ancestor context when available.
- Source locator information is present for audit review when the node has a span.

### Sample 2

- selectable node: `ann11.sec1`
- kind: `section`
- human readable path: document > COMPUTERISED SYSTEMS > Risk Management
- heading: Risk Management
- text: Risk management should be applied throughout the lifecycle of the computerised system taking into account patient safety, data integrity and product quality. As part of a risk m...
- source_spans: `6` span(s)
- first source span: `{'source_label': 'PIC/S', 'locator': 'line:21'}`

YAML fragment:

```yaml
nid: ann11.sec1
kind: section
num: '1'
heading: Risk Management
text: Risk management should be applied throughout the lifecycle of the computerised
  system taking into account patient safety, data integrity and product quality. As
  part of a risk management system, decisions on the extent of validation and data
  integrity controls should be based on a justified and documented risk assessment
  of the computerised system.
ord: 2
role: structural
normativity: null
source_spans:
- source_label: PIC/S
  locator: line:21
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
```

Review observations:

- The `nid` is present and can be traced in the hierarchy.
- The human readable path includes ancestor context when available.
- Source locator information is present for audit review when the node has a span.

### Sample 3

- selectable node: `ann11.sec2`
- kind: `section`
- human readable path: document > COMPUTERISED SYSTEMS > Personnel
- heading: Personnel
- text: There should be close cooperation between all relevant personnel such as Process Owner, System Owner, Authorised Persons and IT. All personnel should have appropriate qualificat...
- source_spans: `5` span(s)
- first source span: `{'source_label': 'PIC/S', 'locator': 'line:29'}`

YAML fragment:

```yaml
nid: ann11.sec2
kind: section
num: '2'
heading: Personnel
text: There should be close cooperation between all relevant personnel such as Process
  Owner, System Owner, Authorised Persons and IT. All personnel should have appropriate
  qualifications, level of access and defined responsibilities to carry out their
  assigned duties.
ord: 3
role: structural
normativity: null
source_spans:
- source_label: PIC/S
  locator: line:29
- source_label: PIC/S
  locator: line:31
- source_label: PIC/S
  locator: line:32
- source_label: PIC/S
  locator: line:33
- source_label: PIC/S
  locator: line:34
```

Review observations:

- The `nid` is present and can be traced in the hierarchy.
- The human readable path includes ancestor context when available.
- Source locator information is present for audit review when the node has a span.

## Ancestor / Descendant Confirmation

- Ancestor context: representative paths above show the containing structural context.
- Descendant context: no table descendant case is expected in these three candidates; table/note descendant behavior is covered by `TABLE_NOTE_REAL_SAMPLE_REVIEW.md` and related fixtures.
- Promotion status: review candidate only; no `data/normalized/` copy was made.
