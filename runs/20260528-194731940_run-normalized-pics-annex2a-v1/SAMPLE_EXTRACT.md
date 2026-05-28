# 深い階層サンプル抽出

- source: `runs/20260528-194731940_run-normalized-pics-annex2a-v1/promotion_candidate/pics_pe00917_annex2a_20230825.regdoc_ir.yaml`
- target_nid: `ann2a.sec2.ib.tbl1.tblh.tblr4`
- method: IR YAMLをparseし、target_nidの祖先経路を抽出

| 階層 | nid | kind | kind_raw | text / heading |
|---:|---|---|---|---|
| 1 | `root` | `document` |  |  |
| 2 | `ann2a` | `annex` | `ANNEX` |  |
| 3 | `ann2a.sec2` | `section` | `APPLICATION OF THIS ANNEX` |  |
| 4 | `ann2a.sec2.ib` | `item` | `(b)` |  |
| 5 | `ann2a.sec2.ib.tbl1` | `table` | `table` | `Table 1. Illustrative guide to manufacturing activities within the scope of Annex 2A` |
| 6 | `ann2a.sec2.ib.tbl1.tblh` | `table_header` | `table_header` | `Example product / product class | Application of this Annex (see note 1) manufacturing step 1 | Application of this Annex (see note 1) manufacturing step 2 | Application of this Annex (see note 1) manufacturing step 3 | Application of this Annex (see note 1) manufacturing step 4` |
| 7 | `ann2a.sec2.ib.tbl1.tblh.tblr4` | `table_row` | `table_row` | `Gene therapy: ex-vivo genetically modified cells | Donation, procurement and testing of starting tissue / cells | Plasmid manufacturing; Vector manufacturing3 | Ex-vivo genetic modification of cells | Formulation, filling` |
