# PIC/S Annex 2A Table / Warning Review

## Source Pages

Rendered from `data/human-readable/pics/source_docs/pe009-17_annexes_docview_8881.pdf`.

| Source | Rendered file | Reviewed item |
|---|---|---|
| PDF page 77 | `source_pages/annex2a_page-077.png` | Table 1 and table notes |
| PDF page 78 | `source_pages/annex2a_page-078.png` | Figure 1 and Figure 2 |
| PDF page 79 | `source_pages/annex2a_page-079.png` | Figure 3 |

## Table 1

Visible title:

`Table 1. Illustrative guide to manufacturing activities within the scope of Annex 2A`

Visible header structure:

| Header level | Cells |
|---|---|
| Parent / first column | `Example Products` |
| Parent spanning columns 2-5 | `Application of this Annex (see note 1)` |
| Reconstructed IR columns | `Example product / product class`; `Application of this Annex (see note 1) manufacturing step 1`; `Application of this Annex (see note 1) manufacturing step 2`; `Application of this Annex (see note 1) manufacturing step 3`; `Application of this Annex (see note 1) manufacturing step 4` |

Visible data rows:

| Row | Product class | Review |
|---:|---|---|
| 1 | Gene therapy: mRNA | Matches IR cells |
| 2 | Gene therapy: in vivo viral vectors | Matches IR cells |
| 3 | Gene therapy: in vivo non-viral vectors | Matches IR cells |
| 4 | Gene therapy: ex-vivo genetically modified cells | Matches IR cells; split visible subcell is preserved as one semicolon-separated cell value |
| 5 | Somatic cell therapy | Matches IR cells |
| 6 | Tissue engineered products | Matches IR cells |

Visible table notes:

| Note | Review |
|---:|---|
| 1 | Present in IR as table note |
| 2 | Present in IR as table note |
| 3 | Present in IR as table note |

## Figures

| Figure | Source page | IR review |
|---:|---:|---|
| 1 | 78 | Caption and two visible columns match IR figure node |
| 2 | 78 | Caption and two visible columns match IR figure node |
| 3 | 79 | Caption and three visible columns match IR figure node |

## Warning Checks

| Check | Result |
|---|---|
| Strict bundle quality warnings | none |
| Promotion goal warnings | none |
| IR node `warning` / `warn` metadata scan | none |
| `possible_plaintext_table_not_structured` / `possible_form_or_table` scan | none |

## Conclusion

PIC/S Annex 2A Table 1 required a header fix before normalized run. After the fix, all table columns are self-contained and unique, and no warning-bearing nodes remain.
