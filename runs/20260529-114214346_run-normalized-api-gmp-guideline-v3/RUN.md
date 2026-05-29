# RUN: 原薬GMPガイドライン normalized v3

- run_id: `20260529-114214346_run-normalized-api-gmp-guideline-v3`
- branch: `run/normalized-api-gmp-guideline-v3`
- doc_id: `jp_pmda_api_gmp_guideline_20011102`
- source: `data/human-readable/pmda/api_gmp_guideline/source_texts/000156438.txt`
- source URL: `https://www.pmda.go.jp/files/000156438.pdf`
- parser profile: `src/qai_text2ir/profiles/jp_pmda_api_gmp_guideline_v1.yaml`
- promotion candidate: `runs/20260529-114214346_run-normalized-api-gmp-guideline-v3/promotion_candidate/`
- auxiliary out directory: `out/20260529-114214346_run-normalized-api-gmp-guideline-v3/`

## Purpose

Create a fresh formal promotion candidate for the PMDA API GMP guideline after both pre-normalization fixes were approved and merged.

## Precondition

- Heading/Table heading review PR: `#213`
- Table 1 visual review PR: `#215`
- Current main merge commit: `d9610c8122016732ae2bfa3148b9207482e7524f`
- Rejected normalized candidate PR: `#214`
- The old candidates under `runs/20260525-121645707_run-normalized-api-gmp-guideline-v1/` and `runs/20260529-112252975_run-normalized-api-gmp-guideline-v2/` are not reused.

## Inputs

- `data/human-readable/pmda/api_gmp_guideline/source_texts/000156438.txt`
- `src/qai_text2ir/profiles/jp_pmda_api_gmp_guideline_v1.yaml`

## Command

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.cli bundle --input data/human-readable/pmda/api_gmp_guideline/source_texts/000156438.txt --out-dir runs/20260529-114214346_run-normalized-api-gmp-guideline-v3/promotion_candidate --doc-id jp_pmda_api_gmp_guideline_20011102 --title "原薬GMPのガイドライン" --short-title "原薬GMPガイドライン" --doc-type guideline --source-url https://www.pmda.go.jp/files/000156438.pdf --source-format pdf --retrieved-at 2026-02-18 --parser-profile src/qai_text2ir/profiles/jp_pmda_api_gmp_guideline_v1.yaml --jurisdiction JP --language ja --family JP_GUIDELINE --strict --write-manifest --overwrite-manifest
```

## Environment

- Python: `Python 3.11.6`
- PyYAML: `6.0.3`
- typer: `0.24.0`
- lxml: `6.0.2`

## Generated Files

- `promotion_candidate/jp_pmda_api_gmp_guideline_20011102.regdoc_ir.yaml`
- `promotion_candidate/jp_pmda_api_gmp_guideline_20011102.parser_profile.yaml`
- `promotion_candidate/jp_pmda_api_gmp_guideline_20011102.regdoc_profile.yaml`
- `promotion_candidate/jp_pmda_api_gmp_guideline_20011102.meta.yaml`
- `promotion_candidate/manifest.yaml`

Note: `manifest.yaml` command path was sanitized from a local absolute path to a workspace-relative path after generation. The generated IR/profile/meta content was not changed by that sanitization.

## Validation

- Strict bundle generation: pass.
- Promotion goal check: pass.
- Schema: `qai.regdoc_ir.v4`.
- Nodes: 496.
- Source span coverage: 1.0.
- Goal check errors: none.
- Goal check warnings: none.
- Special structure audit: pass.
- Tables: 1.
- Table rows: 7.
- Figures: 0.
- Unresolved special blocks: 0.
- Focused tests: `18 passed`.
- Full tests: `253 passed, 1 skipped`.

## Table 1 Review

Review file: `runs/20260529-114214346_run-normalized-api-gmp-guideline-v3/TABLE1_REVIEW.md`

Key confirmations:

- Table 1 is represented as 7 visual-reviewed `table_row` nodes, not 26 raw text rows.
- Each row has 6 restored cells.
- Gray cells are represented by per-row `guideline_applicable`.
- `ＧＭＰ要求事項の増大` is retained as table-level `visual_notes`, not as a data row.

## Deep Samples

- Table sample: `runs/20260529-114214346_run-normalized-api-gmp-guideline-v3/SAMPLE_EXTRACT_TABLE1.md`
  - Target nid: `cha1.sec1_3.tbl1.tblh.tblr1`
- Text hierarchy sample: `runs/20260529-114214346_run-normalized-api-gmp-guideline-v3/SAMPLE_EXTRACT.md`
  - Target nid: `cha2.sec2_2.p2_22.i15`

## AI Review Note

The samples and Table 1 review were extracted from the regenerated IR. Human final review is expected in the parent PR.

## Promotion Boundary

This parent PR changes only the run promotion candidate and review artifacts. It does not copy files to `data/normalized/`.

After this parent PR is approved and merged, create a child promotion PR that copies the four candidate files from `promotion_candidate/` to `data/normalized/jp_pmda_api_gmp_guideline_20011102/`.
