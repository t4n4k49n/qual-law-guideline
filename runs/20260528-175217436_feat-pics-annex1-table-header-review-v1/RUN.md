# PIC/S Annex 1 table header review v1

## Scope

- Target parser: `src/qai_text2ir/pics_annex1_tables.py`
- Target tests: `tests/test_pics_annex1_tables.py`
- Related rejected PR: #197
- Matching output directory: `out/20260528-175217436_feat-pics-annex1-table-header-review-v1/`

## Problem

The previous visual review focused on merged value cells and row-spanned grade cells, but did not adequately verify whether multi-row table headers remained readable as final normalized column names.

For PIC/S Annex 1 Table 1 and Table 5, the PDF has a two-tier header:

- Parent merged headers: `Maximum limits for total particle >= 0.5 ...` and `Maximum limits for total particle >= 5 ...`
- Child headers: `at rest` and `in operation`

The final IR must not rely on the visual parent cell being nearby. Each normalized column name must include the parent header text.

## Fix

Updated Table 1 and Table 5 columns to include the full parent header:

- `Maximum limits for total particle >= 0.5 µm/m3 at rest`
- `Maximum limits for total particle >= 0.5 µm/m3 in operation`
- `Maximum limits for total particle >= 5 µm/m3 at rest`
- `Maximum limits for total particle >= 5 µm/m3 in operation`

Table 5 uses the source's `μm/m3` spelling.

## Verification

- `python -m pytest tests\test_pics_annex1_tables.py -q`
  - Result: `9 passed`
- Generated verification bundle under `out/20260528-175217436_feat-pics-annex1-table-header-review-v1/`
- Confirmed generated `table_header.text` for Table 1 and Table 5 contains full parent header text.

## Process Correction

For every future RUN, including normalized RUNs, create both:

- `runs/<run_id>/`
- `out/<run_id>/`

For normalized RUNs, `runs/<run_id>/promotion_candidate/` remains the promotion source of record; `out/<run_id>/` may be empty or used for auxiliary verification.
