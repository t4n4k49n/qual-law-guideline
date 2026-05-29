# RUN: API GMP heading/table review before normalization

- run_id: `20260529-110631398_feat-api-gmp-heading-table-review-v1`
- branch: `feat/api-gmp-heading-table-review-v1`
- target doc_id: `jp_pmda_api_gmp_guideline_20011102`
- source: `data/human-readable/pmda/api_gmp_guideline/source_texts/000156438.txt`
- previous candidate: `runs/20260525-121645707_run-normalized-api-gmp-guideline-v1/promotion_candidate/`
- review output: `out/20260529-110631398_feat-api-gmp-heading-table-review-v1/`

## Purpose

Run a Codex pre-normalization review for the PMDA API GMP guideline before starting the formal normalized run.

The review focuses on:

- Table 1 structure and record metadata.
- Heading handling where a heading appears above numbered provisions.
- Cases where chapters intentionally have no intermediate section heading.

## Finding

The previous candidate passed mechanical checks, but heading review found a structural issue:

- `2.1 原則`, `3.1 従業員の適格性`, `12.3 適格性評価`, and similar heading-only nodes were emitted as `paragraph` siblings.
- Their dependent provisions such as `2.10`, `3.10`, and `12.30` were not grouped under those heading nodes.
- This loses ancestor context for DQ checklist display.

This is not suitable for the formal normalized run as-is.

## Fix

- Updated `src/qai_text2ir/profiles/jp_pmda_api_gmp_guideline_v1.yaml`.
  - `x.y` markers are now `section`.
  - `x.y0` / `x.yy` markers are now `paragraph`.
  - `chapter -> section -> paragraph` is now explicit for this document.
- Updated `src/qai_text2ir/api_gmp_table1.py`.
  - Table 1 adapter can attach to a `section` parent.
- Updated `tests/test_text2ir_api_gmp_guideline.py`.
  - Added heading hierarchy regression checks.
  - Added `1.3 適用範囲` text + Table 1 context regression checks.

## Review Result

After the fix:

- `cha2.sec2_1` is `section 2.1`, heading `原則`.
- `cha2.sec2_1.p2_10` is a child paragraph under `section 2.1`.
- `cha3.sec3_1` is `section 3.1`, heading `従業員の適格性`.
- `cha3.sec3_1.p3_10` is a child paragraph under `section 3.1`.
- `cha12.sec12_3` is `section 12.3`, heading `適格性評価`.
- `cha12.sec12_3.p12_30` is a child paragraph under `section 12.3`.
- `cha1.sec1_3.tbl1` remains under `section 1.3`.
- Heading-like short `paragraph` nodes remaining after the fix: `0`.
- Chapters with no intermediate heading remain direct chapter paragraphs:
  - Chapter 13 `変更管理`
  - Chapter 15 `苦情及び回収`
  - Chapter 16 `受託製造業者（試験機関を含む）`

## Generated Review Files

- `GOAL_CHECK.md`
- `SPECIAL_STRUCTURE_AUDIT.md`
- `SAMPLE_EXTRACT.md`
- `HEADING_TABLE_REVIEW.md`

## Validation

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.cli bundle --input data/human-readable/pmda/api_gmp_guideline/source_texts/000156438.txt --out-dir out/20260529-110631398_feat-api-gmp-heading-table-review-v1 --doc-id jp_pmda_api_gmp_guideline_20011102 --title "原薬GMPのガイドライン" --short-title "原薬GMPガイドライン" --doc-type guideline --source-url https://www.pmda.go.jp/files/000156438.pdf --source-format pdf --retrieved-at 2026-02-18 --parser-profile src/qai_text2ir/profiles/jp_pmda_api_gmp_guideline_v1.yaml --jurisdiction JP --language ja --family JP_GUIDELINE --strict --write-manifest --overwrite-manifest
```

Result: pass.

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.goal_check --bundle-dir out/20260529-110631398_feat-api-gmp-heading-table-review-v1 --doc-id jp_pmda_api_gmp_guideline_20011102 --mode promotion --format markdown --out runs/20260529-110631398_feat-api-gmp-heading-table-review-v1/GOAL_CHECK.md
```

Result: pass.

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.special_structure_audit --bundle-dir out/20260529-110631398_feat-api-gmp-heading-table-review-v1 --doc-id jp_pmda_api_gmp_guideline_20011102 --mode promotion --format markdown --out runs/20260529-110631398_feat-api-gmp-heading-table-review-v1/SPECIAL_STRUCTURE_AUDIT.md
```

Result: pass.

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_text2ir_api_gmp_guideline.py -q
```

Result: `4 passed`.

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_text2ir_api_gmp_guideline.py tests/test_text2ir_jp_guideline.py tests/test_text2ir_goal_check.py tests/test_table_note_real_samples.py -q
```

Result: `20 passed`.

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Result: `253 passed, 1 skipped`.

## Decision

The heading issue was confirmed and fixed in this pre-normalization review RUN.

Do not reuse the old `20260525-121645707_run-normalized-api-gmp-guideline-v1` promotion candidate for formal promotion. The next formal normalized run should regenerate a fresh `promotion_candidate/` from the fixed parser/profile.
