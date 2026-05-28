# RUN: PIC/S Part II normalized v1

- run_id: `20260529-022734132_run-normalized-pics-part2-v1`
- branch: `run/normalized-pics-part2-v1`
- doc_id: `pics_pe00917_part2_20230825`
- source: `data/human-readable/pics/pe009-17_part2_2023-08-25_en.txt`
- source URL: `https://picscheme.org/docview/6607`
- parser profile: `src/qai_text2ir/profiles/pics_part2_default_v1.yaml`
- promotion candidate: `runs/20260529-022734132_run-normalized-pics-part2-v1/promotion_candidate/`
- auxiliary out directory: `out/20260529-022734132_run-normalized-pics-part2-v1/`

## Purpose

Create the formal promotion candidate for PIC/S PE 009-17 Part II after the Table 1 header and warning review PR was merged.

## Inputs

- `data/human-readable/pics/pe009-17_part2_2023-08-25_en.txt`
- `src/qai_text2ir/profiles/pics_part2_default_v1.yaml`

## Command

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.cli bundle --input data/human-readable/pics/pe009-17_part2_2023-08-25_en.txt --out-dir runs/20260529-022734132_run-normalized-pics-part2-v1/promotion_candidate --doc-id pics_pe00917_part2_20230825 --title "PIC/S GMP Guide (PE 009-17) Part II Basic Requirements for Active Pharmaceutical Ingredients (25 August 2023)" --short-title "PIC/S PE009-17 Part II" --doc-type guideline --source-url https://picscheme.org/docview/6607 --source-format pdf --retrieved-at 2026-02-18 --parser-profile src/qai_text2ir/profiles/pics_part2_default_v1.yaml --jurisdiction INTL --language en --family PICS --pics-doc-id "PE 009-17 (Part II)" --strict --write-manifest --overwrite-manifest
```

## Environment

- Python: `Python 3.11.6`
- PyYAML: `6.0.3`
- typer: `0.24.0`
- lxml: `6.0.2`

## Generated Files

- `promotion_candidate/pics_pe00917_part2_20230825.regdoc_ir.yaml`
- `promotion_candidate/pics_pe00917_part2_20230825.parser_profile.yaml`
- `promotion_candidate/pics_pe00917_part2_20230825.regdoc_profile.yaml`
- `promotion_candidate/pics_pe00917_part2_20230825.meta.yaml`
- `promotion_candidate/manifest.yaml`

## Validation

- Strict bundle generation: pass.
- Promotion goal check: pass.
- Schema: `qai.regdoc_ir.v4`.
- Nodes: 601.
- Source span coverage: 1.0.
- Goal check errors: none.
- Goal check warnings: none.
- Manifest quality warnings: none.
- IR warning metadata scan: none.
- Special structure audit: pass.
- Focused tests: `8 passed`.

## Table / Warning Review

- Table count: 1.
- Table row count: 7.
- Table note count: 1.
- Figure count: 0.
- Source table-like blocks: 2; unresolved special blocks: 0.
- Table 1 header keeps the spanning parent header in all application step columns:
  - `Application of this Guide to steps (shown in grey) used in this type of manufacturing step 1`
  - `Application of this Guide to steps (shown in grey) used in this type of manufacturing step 2`
  - `Application of this Guide to steps (shown in grey) used in this type of manufacturing step 3`
  - `Application of this Guide to steps (shown in grey) used in this type of manufacturing step 4`
  - `Application of this Guide to steps (shown in grey) used in this type of manufacturing step 5`
- Visual review basis:
  - `runs/20260528-201211084_feat-pics-part2-table-warning-review-v1/TABLE_WARNING_REVIEW.md`
  - PDF page 8: Table 1 and `Increasing GMP requirements` annotation.

## Deep Sample

- Sample file: `runs/20260529-022734132_run-normalized-pics-part2-v1/SAMPLE_EXTRACT.md`
- Target nid: `cha1.sec1_2.tbl1.tblh.tblr7`
- Reason: table row under a table header with a reconstructed spanning parent header and quoted source text.

## AI Review Note

The sample was extracted from the IR by parsing the YAML and preserving the ancestor path. Human final review is expected in the parent PR.

## Promotion Boundary

This parent PR changes only the run promotion candidate and review artifacts. It does not copy files to `data/normalized/`.

After this parent PR is approved and merged, create a child promotion PR that copies the four candidate files from `promotion_candidate/` to `data/normalized/pics_pe00917_part2_20230825/`.
