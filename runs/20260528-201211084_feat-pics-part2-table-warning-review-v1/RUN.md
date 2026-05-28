# RUN: PIC/S Part II table / warning review

- run_id: `20260528-201211084_feat-pics-part2-table-warning-review-v1`
- branch: `feat-pics-part2-table-warning-review-v1`
- target: `pics_pe00917_part2_20230825`
- input: `data/human-readable/pics/pe009-17_part2_2023-08-25_en.txt`
- parser profile: `src/qai_text2ir/profiles/pics_part2_default_v1.yaml`
- output bundle: `out/20260528-201211084_feat-pics-part2-table-warning-review-v1/pics_pe00917_part2_20230825/`

## Purpose

PIC/S Part II normalized run preparation. Confirm table and warning handling before creating a strict normalized run.

## Generated Artifacts

- `runs/20260528-201211084_feat-pics-part2-table-warning-review-v1/GOAL_CHECK_PROMOTION.md`
- `runs/20260528-201211084_feat-pics-part2-table-warning-review-v1/GOAL_CHECK_PROMOTION.json`
- `runs/20260528-201211084_feat-pics-part2-table-warning-review-v1/TABLE_WARNING_REVIEW.md`
- `runs/20260528-201211084_feat-pics-part2-table-warning-review-v1/source_pages/part2_page-08.png`

## Checks

- Generated Part II bundle with `--strict`: pass.
- Promotion goal check: pass.
- Promotion goal warnings: none.
- Manifest quality warnings: none.
- IR warning metadata scan: none.
- Part II focused tests: pass.
- Full test suite: `250 passed, 1 skipped`.

## Table Review Result

- Table count: 1.
- Table 1 source page: PDF page 8.
- Table 1 structure:
  - 6 columns.
  - 1 parent header over application columns: `Application of this Guide to steps (shown in grey) used in this type of manufacturing`.
  - 7 data rows.
  - 1 table annotation: `Increasing GMP requirements`.
- Corrective action:
  - Updated Table 1 columns so every application step column includes the spanning parent header.
  - Preserved source quotes in `“Classical” Fermentation to produce an API`.
  - Added a regression test that asserts complete, unique Table 1 column names.

## Warning Review Result

- Strict bundle quality warnings: none.
- Promotion goal warnings: none.
- IR `warning` / `warn` metadata scan: none.
- `possible_plaintext_table_not_structured` / `possible_form_or_table` scan: none.

## Next

After this PR is merged, create a normalized run for PIC/S Part II.
