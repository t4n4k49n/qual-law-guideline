# PIC/S Part II Table / Warning Review

## Source Pages

Rendered from `data/human-readable/pics/source_docs/pe009-17_part2_docview_6607.pdf`.

| Source | Rendered file | Reviewed item |
|---|---|---|
| PDF page 8 | `source_pages/part2_page-08.png` | Table 1 and increasing GMP requirements annotation |

## Table 1

Visible title:

`Table 1: Application of this Guide to API Manufacturing`

Visible header structure:

| Header level | Cells |
|---|---|
| First column | `Type of Manufacturing` |
| Parent spanning columns 2-6 | `Application of this Guide to steps (shown in grey) used in this type of manufacturing` |
| Reconstructed IR columns | `Type of Manufacturing`; `Application of this Guide to steps (shown in grey) used in this type of manufacturing step 1`; `Application of this Guide to steps (shown in grey) used in this type of manufacturing step 2`; `Application of this Guide to steps (shown in grey) used in this type of manufacturing step 3`; `Application of this Guide to steps (shown in grey) used in this type of manufacturing step 4`; `Application of this Guide to steps (shown in grey) used in this type of manufacturing step 5` |

Visible data rows:

| Row | Manufacturing type | Review |
|---:|---|---|
| 1 | Chemical Manufacturing | Matches IR cells |
| 2 | API derived from animal sources | Matches IR cells |
| 3 | API extracted from plant sources | Matches IR cells |
| 4 | Herbal extracts used as API | Matches IR cells, including blank step 3 |
| 5 | API consisting of comminuted or powdered herbs | Matches IR cells, including blank steps 3 and 4 |
| 6 | Biotechnology: fermentation / cell culture | Matches IR cells |
| 7 | “Classical” Fermentation to produce an API | Matches IR cells, including source quotation marks |

Visible annotation:

| Annotation | Review |
|---|---|
| `Increasing GMP requirements` | Present in IR as table annotation note |

## Warning Checks

| Check | Result |
|---|---|
| Strict bundle quality warnings | none |
| Promotion goal warnings | none |
| IR node `warning` / `warn` metadata scan | none |
| `possible_plaintext_table_not_structured` / `possible_form_or_table` scan | none |

## Conclusion

PIC/S Part II Table 1 required a header fix before normalized run. After the fix, all application step columns are self-contained and unique, the source quotation marks in row 7 are preserved, and no warning-bearing nodes remain.
