# RUN: PIC/S Annex 2A table / warning review

- run_id: `20260528-191035093_feat-pics-annex2a-table-warning-review-v1`
- branch: `feat-pics-annex2a-table-warning-review-v1`
- target: `pics_pe00917_annex2a_20230825`
- input: `data/human-readable/pics/pe009-17_annex2a_2023-08-25_en.txt`
- parser profile: `src/qai_text2ir/profiles/pics_annex2a_default_v1.yaml`
- output bundle: `out/20260528-191035093_feat-pics-annex2a-table-warning-review-v1/pics_pe00917_annex2a_20230825/`

## Purpose

PIC/S Annex 2A normalized run preparation. Confirm table and warning handling before creating a strict normalized run.

## Generated Artifacts

- `runs/20260528-191035093_feat-pics-annex2a-table-warning-review-v1/GOAL_CHECK_PROMOTION.md`
- `runs/20260528-191035093_feat-pics-annex2a-table-warning-review-v1/GOAL_CHECK_PROMOTION.json`
- `runs/20260528-191035093_feat-pics-annex2a-table-warning-review-v1/TABLE_WARNING_REVIEW.md`
- `runs/20260528-191035093_feat-pics-annex2a-table-warning-review-v1/source_pages/annex2a_page-077.png`
- `runs/20260528-191035093_feat-pics-annex2a-table-warning-review-v1/source_pages/annex2a_page-078.png`
- `runs/20260528-191035093_feat-pics-annex2a-table-warning-review-v1/source_pages/annex2a_page-079.png`

## Checks

- Generated Annex 2A bundle with `--strict`: pass.
- Promotion goal check: pass.
- Promotion goal warnings: none.
- Manifest quality warnings: none.
- IR warning metadata scan: none.
- Annex 2A focused tests: pass.
- Full test suite: `249 passed, 1 skipped`.

## Table Review Result

- Table count: 1.
- Table 1 source page: PDF page 77.
- Table 1 structure:
  - 5 columns.
  - 1 parent header over the 4 application columns: `Application of this Annex (see note 1)`.
  - 6 data rows.
  - 3 table notes.
- Corrective action:
  - Updated Table 1 columns so every application column includes the spanning parent header.
  - Added a regression test that asserts complete, unique Table 1 column names.

## Figure Review Result

- Figure count: 3.
- Figure 1 and Figure 2 source page: PDF page 78.
- Figure 3 source page: PDF page 79.
- IR figure nodes match the visible source captions and column groupings.

## Next

After this PR is merged, create a new normalized run for PIC/S Annex 2A.
