# SAMPLE COMPARISON: PIC/S Annex 1 tables and notes

対象出力:

- `out/20260528-102010880_review-pics-annex1-table-note/pics_pe00917_annex1_20230825_after_footer_fix/pics_pe00917_annex1_20230825.regdoc_ir.yaml`

## Summary

Annex 1の表・注記を確認した。6 table、35 table_row、16 note が構造化され、promotion goalはPASSした。

初回出力ではページフッターがTable 2/4/6に混入したため、`PAGE_RE` を修正し、修正後出力でフッター残存が0件であることを確認した。

## Table Samples

| table | nid | rows | notes | heading | first row | last row |
|---:|---|---:|---:|---|---|---|
| 1 | `ann1.sec4.p4_27.tbl1` | 4 | 2 | Table 1: Maximum permitted total particle concentration for classification | `ann1.sec4.p4_27.tbl1.tblh.tblr1`: A / 3 520 / 3 520 / Not specified (a) / Not specified (a) | `ann1.sec4.p4_27.tbl1.tblh.tblr4`: D / 3 520 000 / Not predetermined (b) / 29 300 / Not predetermined (b) |
| 2 | `ann1.sec4.p4_31.tbl2` | 4 | 5 | Table 2: Maximum permitted microbial contamination level during qualification | `ann1.sec4.p4_31.tbl2.tblh.tblr1`: A / No growth / No growth / No growth | `ann1.sec4.p4_31.tbl2.tblh.tblr4`: D / 200 / 100 / 50 |
| 3 | `ann1.sec8.tbl3` | 4 | 0 | Table 3: Examples of operations and grades for terminally sterilised preparation and processing operations | `ann1.sec8.tbl3.tblh.tblr1`: Grade A / Filling of products, when unusually at risk. | `ann1.sec8.tbl3.tblh.tblr4`: Grade D / Preparation of solutions and components for subsequent filling. |
| 4 | `ann1.sec8.tbl4` | 15 | 0 | Table 4: Examples of operations and grades for aseptic preparation and processing operations | `ann1.sec8.tbl4.tblh.tblr1`: Grade A / Aseptic assembly of filling equipment. | `ann1.sec8.tbl4.tblh.tblr15`: Grade D / Assembly of closed and sterilised SUS using intrinsic sterile connection devices. |
| 5 | `ann1.sec9.p9_15.tbl5` | 4 | 3 | Table 5: Maximum permitted total particle concentration for monitoring. | `ann1.sec9.p9_15.tbl5.tblh.tblr1`: A / 3 520 / 3 520 / 29 / 29 | `ann1.sec9.p9_15.tbl5.tblh.tblr4`: D / 3 520 000 / Not predetermined (a) / 29 300 / Not predetermined (a) |
| 6 | `ann1.sec9.p9_30.tbl6` | 4 | 5 | Table 6: Maximum action limits for viable particle contamination | `ann1.sec9.p9_30.tbl6.tblh.tblr1`: A / No growth (c) / No growth (c) / No growth (c) / No growth (c) | `ann1.sec9.p9_30.tbl6.tblh.tblr4`: D / 200 / 100 / 50 / - |

## Checks

- Table 1 and 5 preserve Grade A-D particle limits.
- Table 2 and 6 preserve Grade A-D microbial limits and table notes.
- Table 3 and 4 preserve operation rows under Grade A-D.
- `PE 009-17` / `25 August 2023` page footer remnants are absent from the fixed IR.
- No `possible_plaintext_table_not_structured` remains in Annex 1 table output.

## Result

Annex 1 is ready to proceed to a formal normalized run, using a fresh `runs/<run_id>/promotion_candidate/` output as the promotion source.
