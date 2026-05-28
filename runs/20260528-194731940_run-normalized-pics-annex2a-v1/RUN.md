# RUN: PIC/S Annex 2A normalized v1

- run_id: `20260528-194731940_run-normalized-pics-annex2a-v1`
- branch: `run/normalized-pics-annex2a-v1`
- doc_id: `pics_pe00917_annex2a_20230825`
- source: `data/human-readable/pics/pe009-17_annex2a_2023-08-25_en.txt`
- source URL: `https://picscheme.org/docview/8881`
- parser profile: `src/qai_text2ir/profiles/pics_annex2a_default_v1.yaml`
- promotion candidate: `runs/20260528-194731940_run-normalized-pics-annex2a-v1/promotion_candidate/`
- auxiliary out directory: `out/20260528-194731940_run-normalized-pics-annex2a-v1/`

## Purpose

Create the formal promotion candidate for PIC/S PE 009-17 Annex 2A after the table and warning review fix was merged.

## Inputs

- `data/human-readable/pics/pe009-17_annex2a_2023-08-25_en.txt`
- `src/qai_text2ir/profiles/pics_annex2a_default_v1.yaml`

## Command

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.cli bundle --input data/human-readable/pics/pe009-17_annex2a_2023-08-25_en.txt --out-dir runs/20260528-194731940_run-normalized-pics-annex2a-v1/promotion_candidate --doc-id pics_pe00917_annex2a_20230825 --title "PIC/S GMP Guide (PE 009-17) Annex 2A Manufacture of ATMP biological medicinal substances and products for human use (25 August 2023)" --short-title "PIC/S PE009-17 Annex 2A" --doc-type guideline --source-url https://picscheme.org/docview/8881 --source-format pdf --retrieved-at 2026-02-18 --parser-profile src/qai_text2ir/profiles/pics_annex2a_default_v1.yaml --jurisdiction INTL --language en --family PICS --pics-doc-id "PE 009-17 (Annexes)" --strict --write-manifest --overwrite-manifest
```

## Environment

- Python: `Python 3.11.6`
- PyYAML: `6.0.3`
- typer: `0.24.0`
- lxml: `6.0.2`

## Generated Files

- `promotion_candidate/pics_pe00917_annex2a_20230825.regdoc_ir.yaml`
- `promotion_candidate/pics_pe00917_annex2a_20230825.parser_profile.yaml`
- `promotion_candidate/pics_pe00917_annex2a_20230825.regdoc_profile.yaml`
- `promotion_candidate/pics_pe00917_annex2a_20230825.meta.yaml`
- `promotion_candidate/manifest.yaml`

## Validation

- Strict bundle generation: pass.
- Promotion goal check: pass.
- Schema: `qai.regdoc_ir.v4`.
- Nodes: 215.
- Source span coverage: 1.0.
- Goal check errors: none.
- Goal check warnings: none.
- Manifest quality warnings: none.
- IR warning metadata scan: none.
- Focused tests: `13 passed`.

## Table / Figure Review

- Table count: 1.
- Table row count: 6.
- Table note count: 3.
- Figure count: 3.
- Table 1 header keeps the spanning parent header:
  - `Application of this Annex (see note 1) manufacturing step 1`
  - `Application of this Annex (see note 1) manufacturing step 2`
  - `Application of this Annex (see note 1) manufacturing step 3`
  - `Application of this Annex (see note 1) manufacturing step 4`
- Visual review basis:
  - `runs/20260528-191035093_feat-pics-annex2a-table-warning-review-v1/TABLE_WARNING_REVIEW.md`
  - PDF page 77: Table 1 and notes.
  - PDF page 78: Figure 1 and Figure 2.
  - PDF page 79: Figure 3.

## Deep Sample

- Sample file: `runs/20260528-194731940_run-normalized-pics-annex2a-v1/SAMPLE_EXTRACT.md`
- Target nid: `ann2a.sec2.ib.tbl1.tblh.tblr4`
- Reason: table row under a table header with a reconstructed spanning parent header.

## Promotion Boundary

This parent PR changes only the run promotion candidate and review artifacts. It does not copy files to `data/normalized/`.

After this parent PR is approved and merged, create a child promotion PR that copies the four candidate files from `promotion_candidate/` to `data/normalized/pics_pe00917_annex2a_20230825/`.
