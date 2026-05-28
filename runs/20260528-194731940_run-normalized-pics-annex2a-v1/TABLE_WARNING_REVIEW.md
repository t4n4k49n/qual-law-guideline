# PIC/S Annex 2A Table / Warning Review

## Source Review Basis

The visual review was completed in the preparatory run:

- `runs/20260528-191035093_feat-pics-annex2a-table-warning-review-v1/TABLE_WARNING_REVIEW.md`
- PDF page 77: Table 1 and notes.
- PDF page 78: Figure 1 and Figure 2.
- PDF page 79: Figure 3.

This normalized run regenerated the promotion candidate after that review fix was merged to `main`.

## Normalized Candidate Table Check

| Item | Result |
|---|---|
| Table count | 1 |
| Table 1 nid | `ann2a.sec2.ib.tbl1` |
| Table rows | 6 |
| Table notes | 3 |
| Figure count | 3 |
| Figure nids | `ann2a.sec2.ib.fig1`, `ann2a.sec2.ib.fig2`, `ann2a.sec2.ib.fig3` |

Table 1 header in the promotion candidate:

`Example product / product class | Application of this Annex (see note 1) manufacturing step 1 | Application of this Annex (see note 1) manufacturing step 2 | Application of this Annex (see note 1) manufacturing step 3 | Application of this Annex (see note 1) manufacturing step 4`

The four application columns preserve the PDF spanning parent header `Application of this Annex (see note 1)`.

## Warning Check

| Check | Result |
|---|---|
| Strict bundle quality warnings | none |
| Promotion goal warnings | none |
| IR `warning` / `warn` metadata scan | none |
| `possible_plaintext_table_not_structured` / `possible_form_or_table` scan | none |

## Conclusion

The promotion candidate keeps the previously reviewed Table 1 reconstruction, including the spanning parent header, and no warning-bearing nodes were found.
