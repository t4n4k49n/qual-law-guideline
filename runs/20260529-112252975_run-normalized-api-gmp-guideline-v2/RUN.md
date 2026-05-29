# RUN: 原薬GMPガイドライン normalized v2

- run_id: `20260529-112252975_run-normalized-api-gmp-guideline-v2`
- branch: `run/normalized-api-gmp-guideline-v2`
- doc_id: `jp_pmda_api_gmp_guideline_20011102`
- source: `data/human-readable/pmda/api_gmp_guideline/source_texts/000156438.txt`
- source URL: `https://www.pmda.go.jp/files/000156438.pdf`
- parser profile: `src/qai_text2ir/profiles/jp_pmda_api_gmp_guideline_v1.yaml`
- promotion candidate: `runs/20260529-112252975_run-normalized-api-gmp-guideline-v2/promotion_candidate/`
- auxiliary out directory: `out/20260529-112252975_run-normalized-api-gmp-guideline-v2/`

## Purpose

Create a fresh formal promotion candidate for the PMDA API GMP guideline after the pre-normalization Heading/Table review fix was approved and merged.

## Precondition

- Heading/Table review PR: `#213`
- Merged into main at: `211548f1a75bf8a638d88ba58ffb06af73bbddfa`
- The old candidate under `runs/20260525-121645707_run-normalized-api-gmp-guideline-v1/` is not reused.

## Inputs

- `data/human-readable/pmda/api_gmp_guideline/source_texts/000156438.txt`
- `src/qai_text2ir/profiles/jp_pmda_api_gmp_guideline_v1.yaml`

## Command

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.cli bundle --input data/human-readable/pmda/api_gmp_guideline/source_texts/000156438.txt --out-dir runs/20260529-112252975_run-normalized-api-gmp-guideline-v2/promotion_candidate --doc-id jp_pmda_api_gmp_guideline_20011102 --title "原薬GMPのガイドライン" --short-title "原薬GMPガイドライン" --doc-type guideline --source-url https://www.pmda.go.jp/files/000156438.pdf --source-format pdf --retrieved-at 2026-02-18 --parser-profile src/qai_text2ir/profiles/jp_pmda_api_gmp_guideline_v1.yaml --jurisdiction JP --language ja --family JP_GUIDELINE --strict --write-manifest --overwrite-manifest
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
- Nodes: 515.
- Source span coverage: 1.0.
- Goal check errors: none.
- Goal check warnings: none.
- Special structure audit: pass.
- Tables: 1.
- Table rows: 26.
- Figures: 0.
- Unresolved special blocks: 0.
- Focused tests: `20 passed`.
- Full tests: `253 passed, 1 skipped`.

## Heading / Table Review

Review file: `runs/20260529-112252975_run-normalized-api-gmp-guideline-v2/HEADING_TABLE_REVIEW.md`

Key confirmations:

- `cha2.sec2_1` is `section 2.1`, heading `原則`, and owns `cha2.sec2_1.p2_10`.
- `cha3.sec3_1` is `section 3.1`, heading `従業員の適格性`, and owns `cha3.sec3_1.p3_10`.
- `cha12.sec12_3` is `section 12.3`, heading `適格性評価`, and owns `cha12.sec12_3.p12_30`.
- Heading-like short `paragraph` nodes remaining after the fix: `0`.
- Chapters 13, 15, and 16 have no intermediate heading in the source, so their `13.10`, `15.10`, and `16.10` style paragraphs remain directly under their chapters.
- Table 1 remains under `cha1.sec1_3`.

## Deep Sample

- Sample file: `runs/20260529-112252975_run-normalized-api-gmp-guideline-v2/SAMPLE_EXTRACT.md`
- Target nid: `cha2.sec2_2.p2_22.i15`
- Reason: checks chapter -> section heading -> paragraph -> item ancestor path after Heading fix.

## AI Review Note

The sample and Heading/Table review were extracted from the regenerated IR. Human final review is expected in the parent PR.

## Promotion Boundary

This parent PR changes only the run promotion candidate and review artifacts. It does not copy files to `data/normalized/`.

After this parent PR is approved and merged, create a child promotion PR that copies the four candidate files from `promotion_candidate/` to `data/normalized/jp_pmda_api_gmp_guideline_20011102/`.
