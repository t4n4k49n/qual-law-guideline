# RUN: 無菌操作法指針 heading/table review v1

- run_id: `20260529-124531478_feat-aseptic-heading-table-review-v1`
- branch: `feat/aseptic-heading-table-review-v1`
- target doc_id: `jp_pmda_aseptic_processing_guideline_20110420`
- source: `data/human-readable/pmda/aseptic_processing_guideline/source_texts/000206144.txt`
- PDF source: `data/human-readable/pmda/aseptic_processing_guideline/000206144.pdf`
- review output: `out/20260529-124531478_feat-aseptic-heading-table-review-v1/`

## Purpose

Run a pre-normalization review for the PMDA aseptic processing guideline before creating a formal normalized run.

The review focuses on:

- Heading hierarchy around numbered headings such as `7.1 -> 7.1.1`.
- Tables with merged header cells.
- Table row promotion from raw fixed-width rows to reviewed visual records.

## Findings

- Heading hierarchy was too flat:
  - `7.1`, `11.3`, and similar heading nodes were emitted as `paragraph`.
  - Dependent provisions such as `7.1.1` were siblings rather than children.
- Tables were still raw-row centric:
  - Table 1 had 14 raw rows.
  - Table 2 had 9 raw rows.
  - Table 3 had 7 raw rows.
  - The reviewed records existed only in metadata and were not promoted to `table_row`.
- Table 1 was appended after `7.1.1` through `7.1.3`, although the PDF places it before `7.1.1`.
- Table 1 notes were duplicated as both parent notes and table notes.

## Fix

- Updated `src/qai_text2ir/profiles/jp_pmda_aseptic_processing_guideline_v1.yaml`.
  - Adds `section` as a structural kind.
  - Emits `x.y` headings, except chapter 2 definitions, as `section`.
  - Emits `x.y.z` headings as child `paragraph`.
- Updated `src/qai_text2ir/aseptic_processing_tables.py`.
  - Promotes visually reviewed records to `table_row`.
  - Adds `columns`, `column_labels`, and `header_structure.spanning_headers`.
  - Preserves raw source lines as trace metadata.
  - Inserts tables by source order.
  - Removes duplicate parent notes for table notes.
- Updated `tests/test_text2ir_aseptic_processing_guideline.py`.

## Review Result

- `cha7.sec7_1` is `section 7.1`, heading `清浄度レベルによる作業所の分類`.
- `cha7.sec7_1.tbl1` is a child of `7.1` and appears before `cha7.sec7_1.p7_1_1`.
- `cha7.sec7_1.p7_1_1` is a child paragraph under `7.1`.
- `cha11.sec11_3` is `section 11.3`, heading `環境モニタリング判定基準例`.
- Table 1 is 4 reviewed data rows with merged headers:
  - `名称`
  - `最大許容微粒子数（個／m3）`
  - `非作業時`
  - `作業時`
- Table 2 is 4 reviewed data rows with merged `表面付着微生物` header.
- Table 3 is 4 reviewed data rows with merged `空中微生物` and `表面付着微生物` headers.
- Generated table rows: `12`.
- Unresolved special blocks: `0`.

## Visual Review Basis

- PDF page 20: Table 1 `清浄区域の分類`.
- PDF page 33: Table 2 `微生物管理に係る環境モニタリングの頻度` and Table 3 `環境微生物の許容基準(作業時)`.
- Review memo: `HEADING_TABLE_REVIEW.md`.
- Deep hierarchy sample: `SAMPLE_EXTRACT.md`.

## Validation

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.cli bundle --input data/human-readable/pmda/aseptic_processing_guideline/source_texts/000206144.txt --out-dir out/20260529-124531478_feat-aseptic-heading-table-review-v1 --doc-id jp_pmda_aseptic_processing_guideline_20110420 --title "無菌操作法による無菌医薬品の製造に関する指針" --short-title "無菌操作法指針" --doc-type guideline --source-url https://www.pmda.go.jp/files/000206144.pdf --source-format pdf --retrieved-at 2026-02-18 --parser-profile src/qai_text2ir/profiles/jp_pmda_aseptic_processing_guideline_v1.yaml --jurisdiction JP --language ja --family JP_GUIDELINE --strict --write-manifest --overwrite-manifest
```

Result: pass.

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.goal_check --bundle-dir out/20260529-124531478_feat-aseptic-heading-table-review-v1 --doc-id jp_pmda_aseptic_processing_guideline_20110420 --mode promotion --format markdown --out runs/20260529-124531478_feat-aseptic-heading-table-review-v1/GOAL_CHECK.md
```

Result: pass.

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.special_structure_audit --bundle-dir out/20260529-124531478_feat-aseptic-heading-table-review-v1 --doc-id jp_pmda_aseptic_processing_guideline_20110420 --mode promotion --format markdown --out runs/20260529-124531478_feat-aseptic-heading-table-review-v1/SPECIAL_STRUCTURE_AUDIT.md
```

Result: pass.

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_text2ir_aseptic_processing_guideline.py tests/test_text2ir_api_gmp_guideline.py -q
```

Result: `7 passed`.

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Result: `253 passed, 1 skipped`.

## Decision

This is a pre-normalization review/fix PR. Do not create the normalized run until this heading and table review is approved and merged.
