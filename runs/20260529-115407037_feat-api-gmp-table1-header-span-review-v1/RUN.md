# RUN: 原薬GMPガイドライン 表1 ヘッダ結合セルレビュー v1

- run_id: `20260529-115407037_feat-api-gmp-table1-header-span-review-v1`
- branch: `feat/api-gmp-table1-header-span-review-v1`
- target doc_id: `jp_pmda_api_gmp_guideline_20011102`
- source: `data/human-readable/pmda/api_gmp_guideline/source_texts/000156438.txt`
- PDF source: `data/human-readable/pmda/api_gmp_guideline/000156438.pdf`
- generated output: `out/20260529-115407037_feat-api-gmp-table1-header-span-review-v1/`

## Purpose

Redo the visual review for Table 1 header cells after normalized PR `#216` was rejected.

The rejected candidate restored the table rows, but flattened the merged header cell incorrectly. This run follows the English PIC/S Part II Table 1 pattern: the spanning process header is repeated into `STEP 1` through `STEP 5`, while the PDF leaf-stage labels are retained as metadata.

## Changes

- Updated `src/qai_text2ir/api_gmp_table1.py`.
  - Uses `process_example_step_1` through `process_example_step_5` for the five process columns.
  - Emits column labels as `形態ごとの生産工程の事例 STEP 1` through `STEP 5`.
  - Preserves the original PDF leaf-stage labels in `stage_labels`.
  - Adds `header_structure.spanning_headers` to document the merged header cell.
  - Keeps the seven visual-reviewed data rows and gray applicability cells from the previous table review.
- Updated `tests/test_text2ir_api_gmp_guideline.py`.
  - Verifies the STEP column labels.
  - Verifies spanning header metadata.
  - Verifies stage labels on the header and rows.

## Manual Review

- Review file: `TABLE1_HEADER_REVIEW.md`
- PDF page: 8
- Reference implementation: `src/qai_text2ir/pics_part2_table1.py`
- Reference test: `tests/test_pics_part2_table1.py`
- Header outcome:
  - `生産形態`
  - `形態ごとの生産工程の事例 STEP 1`
  - `形態ごとの生産工程の事例 STEP 2`
  - `形態ごとの生産工程の事例 STEP 3`
  - `形態ごとの生産工程の事例 STEP 4`
  - `形態ごとの生産工程の事例 STEP 5`

## Validation

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.cli bundle --input data/human-readable/pmda/api_gmp_guideline/source_texts/000156438.txt --out-dir out/20260529-115407037_feat-api-gmp-table1-header-span-review-v1 --doc-id jp_pmda_api_gmp_guideline_20011102 --title "原薬GMPのガイドライン" --short-title "原薬GMPガイドライン" --doc-type guideline --source-url https://www.pmda.go.jp/files/000156438.pdf --source-format pdf --retrieved-at 2026-02-18 --parser-profile src/qai_text2ir/profiles/jp_pmda_api_gmp_guideline_v1.yaml --jurisdiction JP --language ja --family JP_GUIDELINE --strict --write-manifest --overwrite-manifest
```

Result: pass.

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.goal_check --bundle-dir out/20260529-115407037_feat-api-gmp-table1-header-span-review-v1 --doc-id jp_pmda_api_gmp_guideline_20011102 --mode promotion --format markdown --out runs/20260529-115407037_feat-api-gmp-table1-header-span-review-v1/GOAL_CHECK.md
```

Result: pass.

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.special_structure_audit --bundle-dir out/20260529-115407037_feat-api-gmp-table1-header-span-review-v1 --doc-id jp_pmda_api_gmp_guideline_20011102 --mode promotion --format markdown --out runs/20260529-115407037_feat-api-gmp-table1-header-span-review-v1/SPECIAL_STRUCTURE_AUDIT.md
```

Result: pass.

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_text2ir_api_gmp_guideline.py tests/test_pics_part2_table1.py -q
```

Result: `10 passed`.

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Result: `253 passed, 1 skipped`.

## Decision

This is a pre-normalization visual review/fix PR. Do not create a normalized run until this table header review is approved and merged.
