# 表1確認

- target: `jp_pmda_api_gmp_guideline_20011102`
- source PDF URL: `https://www.pmda.go.jp/files/000156438.pdf`
- PDF page: 8
- generated IR: `promotion_candidate/jp_pmda_api_gmp_guideline_20011102.regdoc_ir.yaml`

## Header

Generated `table_header.text`:

```text
生産形態 | 形態ごとの生産工程の事例 STEP 1 | 形態ごとの生産工程の事例 STEP 2 | 形態ごとの生産工程の事例 STEP 3 | 形態ごとの生産工程の事例 STEP 4 | 形態ごとの生産工程の事例 STEP 5
```

The merged PDF header cell is represented as:

```yaml
spanning_headers:
- label: 形態ごとの生産工程の事例
  columns:
  - process_example_step_1
  - process_example_step_2
  - process_example_step_3
  - process_example_step_4
  - process_example_step_5
  column_range:
  - 1
  - 5
```

The original leaf-stage labels are retained as `stage_labels`:

```yaml
stage_labels:
- null
- 原薬出発物質の製造
- 原薬出発物質の工程への導入又は初期加工処理
- 中間体の製造又は同等工程
- 分離及び精製又は再抽出
- 物理的加工処理及び包装
```

## Rows

- Generated `table_row`: `7`
- `guideline_applicable` keeps the gray-cell meaning.
- `guideline_applicable_columns` now uses `process_example_step_1` through `process_example_step_5`.
- The arrow note `ＧＭＰ要求事項の増大` is retained as a table visual note, not as a data row.

## Decision

The normalized candidate keeps the visually reviewed row structure from PR `#215` and the merged-header STEP structure from PR `#217`.
