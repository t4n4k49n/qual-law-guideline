# RUN: 原薬GMPガイドライン 表1 視覚レビュー v1

- run_id: `20260529-113304540_feat-api-gmp-table1-visual-review-v1`
- branch: `feat/api-gmp-table1-visual-review-v1`
- target doc_id: `jp_pmda_api_gmp_guideline_20011102`
- source: `data/human-readable/pmda/api_gmp_guideline/source_texts/000156438.txt`
- PDF source: `data/human-readable/pmda/api_gmp_guideline/000156438.pdf`
- review output: `out/20260529-113304540_feat-api-gmp-table1-visual-review-v1/`

## Purpose

Redo Table 1 review for the PMDA API GMP guideline after normalized PR `#214` was rejected.

The rejected candidate represented Table 1 as 26 raw text rows, so it did not preserve the actual PDF table cells or gray applicability cells.

## Changes

- Updated `src/qai_text2ir/api_gmp_table1.py`.
  - Promotes Table 1 into 7 visual-reviewed `table_row` nodes.
  - Each `table_row` has 6 restored cells.
  - Gray cells are represented by `guideline_applicable`.
  - Raw TXT rows are retained as trace data only.
  - The arrow note `ＧＭＰ要求事項の増大` is stored as a table-level visual note, not as a row.
- Updated tests:
  - `tests/test_text2ir_api_gmp_guideline.py`
  - `tests/test_table_record_review_6_7.py`

## Review

- Review file: `TABLE1_VISUAL_REVIEW.md`
- PDF page: 8
- Reconstructed data rows: 7
- Reconstructed columns: 6
- Generated `table_row`: 7

## Validation

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.cli bundle --input data/human-readable/pmda/api_gmp_guideline/source_texts/000156438.txt --out-dir out/20260529-113304540_feat-api-gmp-table1-visual-review-v1 --doc-id jp_pmda_api_gmp_guideline_20011102 --title "原薬GMPのガイドライン" --short-title "原薬GMPガイドライン" --doc-type guideline --source-url https://www.pmda.go.jp/files/000156438.pdf --source-format pdf --retrieved-at 2026-02-18 --parser-profile src/qai_text2ir/profiles/jp_pmda_api_gmp_guideline_v1.yaml --jurisdiction JP --language ja --family JP_GUIDELINE --strict --write-manifest --overwrite-manifest
```

Result: pass.

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.goal_check --bundle-dir out/20260529-113304540_feat-api-gmp-table1-visual-review-v1 --doc-id jp_pmda_api_gmp_guideline_20011102 --mode promotion --format markdown --out runs/20260529-113304540_feat-api-gmp-table1-visual-review-v1/GOAL_CHECK.md
```

Result: pass.

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.special_structure_audit --bundle-dir out/20260529-113304540_feat-api-gmp-table1-visual-review-v1 --doc-id jp_pmda_api_gmp_guideline_20011102 --mode promotion --format markdown --out runs/20260529-113304540_feat-api-gmp-table1-visual-review-v1/SPECIAL_STRUCTURE_AUDIT.md
```

Result: pass.

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_text2ir_api_gmp_guideline.py tests/test_table_record_review_6_7.py -q
```

Result: `5 passed`.

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Result: `253 passed, 1 skipped`.

## Decision

This is a pre-normalization visual review/fix PR. Do not create a normalized run until this table review is approved and merged.
