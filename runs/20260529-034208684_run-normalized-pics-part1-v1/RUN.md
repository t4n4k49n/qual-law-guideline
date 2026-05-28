# RUN: PIC/S Part I normalized v1

- run_id: `20260529-034208684_run-normalized-pics-part1-v1`
- branch: `run/normalized-pics-part1-v1`
- doc_id: `pics_pe00917_part1_20230825`
- source: `data/human-readable/pics/pe009-17_part1_2023-08-25_en.txt`
- source URL: `https://picscheme.org/docview/6606`
- parser profile: `src/qai_text2ir/profiles/pics_part1_default_v3.yaml`
- promotion candidate: `runs/20260529-034208684_run-normalized-pics-part1-v1/promotion_candidate/`
- auxiliary out directory: `out/20260529-034208684_run-normalized-pics-part1-v1/`

## Purpose

Create the formal promotion candidate for PIC/S PE 009-17 Part I after the table/warning review and Chapter 7 note attachment fix was merged.

## Inputs

- `data/human-readable/pics/pe009-17_part1_2023-08-25_en.txt`
- `src/qai_text2ir/profiles/pics_part1_default_v3.yaml`

## Command

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.cli bundle --input data/human-readable/pics/pe009-17_part1_2023-08-25_en.txt --out-dir runs/20260529-034208684_run-normalized-pics-part1-v1/promotion_candidate --doc-id pics_pe00917_part1_20230825 --title "PIC/S GMP Guide (PE 009-17) Part I Basic Requirements for Medicinal Products (25 August 2023)" --short-title "PIC/S PE009-17 Part I" --doc-type guideline --source-url https://picscheme.org/docview/6606 --source-format pdf --retrieved-at 2026-02-18 --parser-profile src/qai_text2ir/profiles/pics_part1_default_v3.yaml --jurisdiction INTL --language en --family PICS --pics-doc-id "PE 009-17 (Part I)" --strict --write-manifest --overwrite-manifest
```

## Environment

- Python: `Python 3.11.6`
- PyYAML: `6.0.3`
- typer: `0.24.0`
- lxml: `6.0.2`

## Generated Files

- `promotion_candidate/pics_pe00917_part1_20230825.regdoc_ir.yaml`
- `promotion_candidate/pics_pe00917_part1_20230825.parser_profile.yaml`
- `promotion_candidate/pics_pe00917_part1_20230825.regdoc_profile.yaml`
- `promotion_candidate/pics_pe00917_part1_20230825.meta.yaml`
- `promotion_candidate/manifest.yaml`

## Validation

- Strict bundle generation: pass.
- Promotion goal check: pass.
- Schema: `qai.regdoc_ir.v4`.
- Nodes: 344.
- Source span coverage: 1.0.
- Goal check errors: none.
- Goal check warnings: none.
- Manifest quality warnings: none.
- IR warning metadata scan: none.
- Special structure audit: pass.
- Focused tests: `9 passed`.
- Full test suite: `251 passed, 1 skipped`.

## Table / Warning Review

- Table count: 0.
- Table row count: 0.
- Figure count: 0.
- Unresolved special blocks: 0.
- Note count: 2.
- `cha4.p4_20.not1`: attached to paragraph `4.20`.
- `cha7.not1`: attached to Chapter 7.
- Visual/review basis:
  - `runs/20260529-033231419_feat-pics-part1-table-warning-review-v1/TABLE_WARNING_REVIEW.md`
  - `runs/20260529-033231419_feat-pics-part1-table-warning-review-v1/SAMPLE_EXTRACT.md`

## Deep Sample

- Sample file: `runs/20260529-034208684_run-normalized-pics-part1-v1/SAMPLE_EXTRACT.md`
- Target nid: `cha1.p1_8.iiii.si5`
- Reason: one of the deepest nodes in the promotion candidate (`document > chapter > paragraph > item > subitem`).

## AI Review Note

The sample was extracted from the IR by parsing the YAML and preserving the ancestor path. Human final review is expected in the parent PR.

## Promotion Boundary

This parent PR changes only the run promotion candidate and review artifacts. It does not copy files to `data/normalized/`.

After this parent PR is approved and merged, create a child promotion PR that copies the four candidate files from `promotion_candidate/` to `data/normalized/pics_pe00917_part1_20230825/`.

## Promotion Preparation

- Parent PR: `#208`
- Parent merge commit: `3a899979d3412a24b8c50eb0bf3d1e093cd11fb9`
- Promotion branch: `promote/pics-part1-v1`
- Destination: `data/normalized/pics_pe00917_part1_20230825/`
- Copied files:
  - `pics_pe00917_part1_20230825.regdoc_ir.yaml`
  - `pics_pe00917_part1_20230825.parser_profile.yaml`
  - `pics_pe00917_part1_20230825.regdoc_profile.yaml`
  - `pics_pe00917_part1_20230825.meta.yaml`
- SHA-256 match between `promotion_candidate/` and `data/normalized/`: confirmed.
- Promotion goal check on `data/normalized/pics_pe00917_part1_20230825/`: pass.
- Promotion goal warning: `missing_manifest` only; manifest is intentionally not copied to `data/normalized/`.
- IR structure check on `data/normalized/pics_pe00917_part1_20230825/`: pass.
