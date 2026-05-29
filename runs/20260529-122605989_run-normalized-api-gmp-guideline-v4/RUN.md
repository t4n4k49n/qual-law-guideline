# RUN: 原薬GMPガイドライン 正規化RUN v4

- run_id: `20260529-122605989_run-normalized-api-gmp-guideline-v4`
- branch: `run/normalized-api-gmp-guideline-v4`
- target doc_id: `jp_pmda_api_gmp_guideline_20011102`
- source: `data/human-readable/pmda/api_gmp_guideline/source_texts/000156438.txt`
- source PDF URL: `https://www.pmda.go.jp/files/000156438.pdf`
- promotion candidate: `runs/20260529-122605989_run-normalized-api-gmp-guideline-v4/promotion_candidate/`
- main base commit: `8e836f2b9c2f5c3a05851644ab20e4c5799efb5f`

## Purpose

Create a fresh normalized-run parent PR for the PMDA API GMP guideline after the Table 1 visual row and merged-header fixes were reviewed and merged.

This parent PR is for review of `promotion_candidate/` only. It does not modify `data/normalized/`.

## Input And Tooling

- Input format: PMDA PDF-derived human-readable text.
- Parser profile: `jp_pmda_api_gmp_guideline_v1`
- IR schema: `qai.regdoc_ir.v4`
- Python executable: `.venv\Scripts\python.exe`
- Python version: `3.11.6`
- Dependencies:
  - `lxml`: `6.0.2`
  - `PyYAML`: `6.0.3`
  - `typer`: `0.24.0`
- Tool version: not set.
- Git hook setup:
  - `.\.venv\Scripts\python.exe scripts/install_git_hooks.py` failed in this local environment because Git required an explicit safe directory.
  - Equivalent hook configuration was applied with `git -c safe.directory=E:/GitHub/qual-law-guideline config core.hooksPath .githooks`.
  - Confirmed `core.hooksPath`: `.githooks`.

## Generation

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.cli bundle --input data/human-readable/pmda/api_gmp_guideline/source_texts/000156438.txt --out-dir runs/20260529-122605989_run-normalized-api-gmp-guideline-v4/promotion_candidate --doc-id jp_pmda_api_gmp_guideline_20011102 --title "原薬GMPのガイドライン" --short-title "原薬GMPガイドライン" --doc-type guideline --source-url https://www.pmda.go.jp/files/000156438.pdf --source-format pdf --retrieved-at 2026-02-18 --parser-profile src/qai_text2ir/profiles/jp_pmda_api_gmp_guideline_v1.yaml --jurisdiction JP --language ja --family JP_GUIDELINE --strict --write-manifest --overwrite-manifest
```

Result: pass.

Generated files:

- `jp_pmda_api_gmp_guideline_20011102.regdoc_ir.yaml`
- `jp_pmda_api_gmp_guideline_20011102.parser_profile.yaml`
- `jp_pmda_api_gmp_guideline_20011102.regdoc_profile.yaml`
- `jp_pmda_api_gmp_guideline_20011102.meta.yaml`
- `manifest.yaml`

## Review Notes

- Table 1 is represented as 1 table, 1 table_header, and 7 table_row nodes.
- Table 1 header text is:
  - `生産形態 | 形態ごとの生産工程の事例 STEP 1 | 形態ごとの生産工程の事例 STEP 2 | 形態ごとの生産工程の事例 STEP 3 | 形態ごとの生産工程の事例 STEP 4 | 形態ごとの生産工程の事例 STEP 5`
- The merged header cell is retained in `header_structure.spanning_headers`.
- The original PDF leaf-stage labels are retained in `stage_labels`.
- Deep hierarchy review sample: `SAMPLE_EXTRACT.md`.
- Final human visual review is expected on the parent PR.

## Validation

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.goal_check --bundle-dir runs/20260529-122605989_run-normalized-api-gmp-guideline-v4/promotion_candidate --doc-id jp_pmda_api_gmp_guideline_20011102 --mode promotion --format markdown --out runs/20260529-122605989_run-normalized-api-gmp-guideline-v4/GOAL_CHECK.md
```

Result: pass.

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.special_structure_audit --bundle-dir runs/20260529-122605989_run-normalized-api-gmp-guideline-v4/promotion_candidate --doc-id jp_pmda_api_gmp_guideline_20011102 --mode promotion --format markdown --out runs/20260529-122605989_run-normalized-api-gmp-guideline-v4/SPECIAL_STRUCTURE_AUDIT.md
```

Result: pass.

```powershell
.\.venv\Scripts\python.exe tools/extract_ir_sample.py --ir runs/20260529-122605989_run-normalized-api-gmp-guideline-v4/promotion_candidate/jp_pmda_api_gmp_guideline_20011102.regdoc_ir.yaml --nid cha2.sec2_2.p2_22.i15 --output runs/20260529-122605989_run-normalized-api-gmp-guideline-v4/SAMPLE_EXTRACT.md
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

## Promotion Status

Promotion prepared in child promotion branch.

- Parent PR: `#218`
- Parent merge commit: `4ca0420`
- Promotion branch: `promote/api-gmp-guideline-v4`
- Destination: `data/normalized/jp_pmda_api_gmp_guideline_20011102/`
- Copied files:
  - `jp_pmda_api_gmp_guideline_20011102.regdoc_ir.yaml`
  - `jp_pmda_api_gmp_guideline_20011102.parser_profile.yaml`
  - `jp_pmda_api_gmp_guideline_20011102.regdoc_profile.yaml`
  - `jp_pmda_api_gmp_guideline_20011102.meta.yaml`
- SHA-256 match between `promotion_candidate/` and `data/normalized/`: confirmed.
- Promotion goal check on `data/normalized/jp_pmda_api_gmp_guideline_20011102/`: pass.
- IR structure check on `data/normalized/jp_pmda_api_gmp_guideline_20011102/`: pass.
