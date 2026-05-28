# PIC/S Part I Table / Warning Review

## Scope

- Source: `data/human-readable/pics/pe009-17_part1_2023-08-25_en.txt`
- PDF: `data/human-readable/pics/source_docs/pe009-17_part1_docview_6606.pdf`
- Parser profile: `src/qai_text2ir/profiles/pics_part1_default_v3.yaml`
- Reviewed output: `out/20260529-033231419_feat-pics-part1-table-warning-review-v1/pics_pe00917_part1_20230825_after_fix/`

## Table / Figure Scan

| Check | Result |
|---|---:|
| Source table-like blocks | 0 |
| Source figure-like blocks | 0 |
| Generated tables | 0 |
| Generated table rows | 0 |
| Generated figures | 0 |
| Unresolved special blocks | 0 |

Source text scan:

- `TABLE OF CONTENT` / `Table of contents`: TOC only.
- `Table ` body hits: none.
- `Figure` body hits: none.
- `organisation chart`: prose in paragraph `2.2`, not a rendered figure/table.

## Warning Scan

| Check | Result |
|---|---|
| strict bundle generation | pass |
| promotion goal check | pass |
| promotion goal warnings | none |
| special structure audit | pass |
| IR `warning` / `warn` metadata scan | none |
| `possible_plaintext_table_not_structured` / `possible_form_or_table` scan | none |

## Corrected Issue

Before the fix, the Chapter 7 running header and note were incorrectly associated with the previous Chapter 6 paragraph:

- `cha6.p6_41.text` contained `Chapter 7     Outsourced activities`.
- Chapter 7's principle note was attached as `cha6.p6_41.not1`.

After the fix:

- `cha6.p6_41.text` contains only paragraph 6.41.
- Chapter 7's principle note is `cha7.not1`.
- `cha7.not1` source lines are 2540-2544.

## Conclusion

PIC/S Part I does not need table reconstruction before the normalized run. The note/context issue found during review is fixed and covered by regression test.
