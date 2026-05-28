# PIC/S Annex 1 table visual review v1

## Scope

- Target: `data/human-readable/pics/pe009-17_annex1_2023-08-25_en.txt`
- Source PDF: `data/human-readable/pics/source_docs/pe009-17_annexes_docview_8881.pdf`
- Parser: `src/qai_text2ir/pics_annex1_tables.py`
- Tests: `tests/test_pics_annex1_tables.py`

## Visual Review

Reviewed all PIC/S Annex 1 tables against rendered PDF page images.

- Table 1: two-tier particle headers; Grade D wrapped in-operation cells.
- Table 2: Grade A `No growth` cell spans all monitoring-method columns.
- Table 3: Grade C cell spans two operation rows.
- Table 4: Grade A/B/D cells span multiple operation rows. Text extraction placed some labels mid-group, so row grades were corrected from the visual row spans.
- Table 5: two-tier particle headers; Grade D wrapped in-operation cells.
- Table 6: Grade A `No growth(c)` cell spans all monitoring-method columns.

## Outputs

- `source_pages/*.png`: rendered PDF pages used for review.
- `visual_reconstruction.json`: structured review notes for merged and wrapped cells.
- `visual_reconstruction.md`: human-readable review summary.

## Verification

- `python -m pytest tests\test_pics_annex1_tables.py -q`
  - Result: `9 passed`
