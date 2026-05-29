# 深い階層サンプル抽出

- source: `runs/20260529-114214346_run-normalized-api-gmp-guideline-v3/promotion_candidate/jp_pmda_api_gmp_guideline_20011102.regdoc_ir.yaml`
- target_nid: `cha1.sec1_3.tbl1.tblh.tblr1`
- method: IR YAMLをparseし、target_nidの祖先経路を抽出

| 階層 | nid | kind | kind_raw | text / heading |
|---:|---|---|---|---|
| 1 | `root` | `document` |  |  |
| 2 | `cha1` | `chapter` | `1.` | `序文` |
| 3 | `cha1.sec1_3` | `section` | `1.3` | `適用範囲` |
| 4 | `cha1.sec1_3.tbl1` | `table` | `table` | `表１：原薬生産に対する本ガイドラインの適用` |
| 5 | `cha1.sec1_3.tbl1.tblh` | `table_header` | `table_header` | `生産形態 | 原薬出発物質の製造 | 原薬出発物質の工程への導入又は初期加工処理 | 中間体の製造又は同等工程 | 分離及び精製又は再抽出 | 物理的加工処理及び包装` |
| 6 | `cha1.sec1_3.tbl1.tblh.tblr1` | `table_row` | `table_row` | `化学的合成による原薬 | 原薬出発物質の製造 | 原薬出発物質の工程への導入 | 中間体の製造 | 分離及び精製 | 物理的加工処理及び包装` |
