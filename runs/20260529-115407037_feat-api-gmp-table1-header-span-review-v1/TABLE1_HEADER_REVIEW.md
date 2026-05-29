# TABLE 1 HEADER REVIEW

- Document: `jp_pmda_api_gmp_guideline_20011102`
- Source PDF: `000156438.pdf`
- Page: 8
- Table: `表１：原薬生産に対する本ガイドラインの適用`
- Review target: merged header cells only

## Visual Finding

The PDF table has one left header column and one merged process-example header spanning five process columns.

- Left header: `生産形態`
- Spanning process header: `形態ごとの生産工程の事例`
- Process-header note: `（灰色部分：本ガイドラインを適用する工程）`
- Leaf stage labels under the spanning header:
  - `原薬出発物質の製造`
  - `原薬出発物質の工程への導入又は初期加工処理`
  - `中間体の製造又は同等工程`
  - `分離及び精製又は再抽出`
  - `物理的加工処理及び包装`

## Reference Pattern

The English PIC/S Part II Table 1 adapter flattens the comparable spanning header into repeated STEP columns:

- `Application of this Guide to steps ... step 1`
- `Application of this Guide to steps ... step 2`
- `Application of this Guide to steps ... step 3`
- `Application of this Guide to steps ... step 4`
- `Application of this Guide to steps ... step 5`

The Japanese API GMP table now follows the same pattern.

## Reviewed Reconstruction

The generated header row is:

```text
生産形態 | 形態ごとの生産工程の事例 STEP 1 | 形態ごとの生産工程の事例 STEP 2 | 形態ごとの生産工程の事例 STEP 3 | 形態ごとの生産工程の事例 STEP 4 | 形態ごとの生産工程の事例 STEP 5
```

The five original leaf-stage labels are retained in `stage_labels`, so no PDF heading information is discarded.

## Data Contract

- `columns[0]`: `production_type`
- `columns[1..5]`: `process_example_step_1` through `process_example_step_5`
- `column_labels[1..5]`: repeated spanning header with `STEP 1` through `STEP 5`
- `header_structure.spanning_headers[0].label`: `形態ごとの生産工程の事例`
- `header_structure.leaf_stage_labels`: PDF leaf-stage labels
- `table_header.data.stage_labels`: PDF leaf-stage labels
- `table_row.data.stage_labels`: PDF leaf-stage labels

## Generated Output Check

- Generated table count: `1`
- Generated table rows: `7`
- Header text includes `STEP 1` through `STEP 5`
- Gray applicability columns still use `guideline_applicable` and `guideline_applicable_columns`

## Decision

Accept the STEP-column flattening for the merged header cell. It preserves the visual meaning of the arrow `ＧＭＰ要求事項の増大`, aligns with the English equivalent, and keeps the original Japanese leaf labels as metadata.
