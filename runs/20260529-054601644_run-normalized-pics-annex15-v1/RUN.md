# RUN: PIC/S Annex 15 normalized v1

- run_id: `20260529-054601644_run-normalized-pics-annex15-v1`
- branch: `run/normalized-pics-annex15-v1`
- doc_id: `pics_pe00917_annex15_20230825`
- source: `data/human-readable/pics/pe009-17_annex15_2023-08-25_en.txt`
- source URL: `https://picscheme.org/docview/8881`
- parser profile: `src/qai_text2ir/profiles/pics_annex15_default_v1.yaml`
- promotion candidate: `runs/20260529-054601644_run-normalized-pics-annex15-v1/promotion_candidate/`
- auxiliary out directory: `out/20260529-054601644_run-normalized-pics-annex15-v1/`

## Purpose

Create the formal promotion candidate for PIC/S PE 009-17 Annex 15 after the final visual/proofreading review PR was merged.

## Inputs

- `data/human-readable/pics/pe009-17_annex15_2023-08-25_en.txt`
- `src/qai_text2ir/profiles/pics_annex15_default_v1.yaml`

## Command

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.cli bundle --input data/human-readable/pics/pe009-17_annex15_2023-08-25_en.txt --out-dir runs/20260529-054601644_run-normalized-pics-annex15-v1/promotion_candidate --doc-id pics_pe00917_annex15_20230825 --title "PIC/S GMP Guide (PE 009-17) Annex 15 Qualification and validation (25 August 2023)" --short-title "PIC/S PE009-17 Annex 15" --doc-type guideline --source-url https://picscheme.org/docview/8881 --source-format pdf --retrieved-at 2026-02-18 --parser-profile src/qai_text2ir/profiles/pics_annex15_default_v1.yaml --jurisdiction INTL --language en --family PICS --pics-doc-id "PE 009-17 (Annexes)" --strict --write-manifest --overwrite-manifest
```

## Environment

- Python: `Python 3.11.6`
- PyYAML: `6.0.3`
- typer: `0.24.0`
- lxml: `6.0.2`

## Generated Files

- `promotion_candidate/pics_pe00917_annex15_20230825.regdoc_ir.yaml`
- `promotion_candidate/pics_pe00917_annex15_20230825.parser_profile.yaml`
- `promotion_candidate/pics_pe00917_annex15_20230825.regdoc_profile.yaml`
- `promotion_candidate/pics_pe00917_annex15_20230825.meta.yaml`
- `promotion_candidate/manifest.yaml`

## Validation

- Strict bundle generation: pass.
- Promotion goal check: pass.
- Schema: `qai.regdoc_ir.v4`.
- Nodes: 142.
- Source span coverage: 1.0.
- Goal check errors: none.
- Goal check warnings: none.
- Manifest quality warnings: none.
- IR warning metadata scan: none.
- Special structure audit: pass.
- Focused tests: `4 passed`.
- Full tests: `252 passed, 1 skipped`.

## Table / Warning Review

- Table count: 0.
- Table row count: 0.
- Note count: 0.
- Figure count: 0.
- Source table-like blocks: 0; unresolved special blocks: 0.
- Warning系は strict / promotion goal / IR metadata scan で該当なし。
- 前段レビューPR `#210` で `PROCESS VALIDATION` と `General` の見出し誤結合を修正済み。
- 今回候補でも `ann15.sec5` は `heading: PROCESS VALIDATION`、`text: General` として分離されている。

## Deep Sample

- Sample file: `runs/20260529-054601644_run-normalized-pics-annex15-v1/SAMPLE_EXTRACT.md`
- Target nid: `ann15.sec5.p5_22.ivi`
- Reason: maximum-depth item under section 5 and paragraph 5.22, preserving the full ancestor path.

## AI Review Note

The sample was extracted from the IR by parsing the YAML and preserving the ancestor path. Human final review is expected in the parent PR.

## Promotion Boundary

This parent PR changes only the run promotion candidate and review artifacts. It does not copy files to `data/normalized/`.

After this parent PR is approved and merged, create a child promotion PR that copies the four candidate files from `promotion_candidate/` to `data/normalized/pics_pe00917_annex15_20230825/`.
