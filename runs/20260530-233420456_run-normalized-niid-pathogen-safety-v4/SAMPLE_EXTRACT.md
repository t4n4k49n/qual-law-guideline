# 深い階層サンプル抽出

- source: `runs/20260530-233420456_run-normalized-niid-pathogen-safety-v4/promotion_candidate/jp_niid_pathogen_safety_management_20240401.regdoc_ir.yaml`
- target_nid: `ann4_2.tbl1.tblh_visual.tblr22`
- method: IR YAMLをparseし、target_nidの祖先経路を抽出

| 階層 | nid | kind | kind_raw | text / heading |
|---:|---|---|---|---|
| 1 | `root` | `document` |  |  |
| 2 | `ann4_2` | `annex` | `別表1` | `国立感染症研究所における施設の位置、構造及び設備の技術上の基準一覧` |
| 3 | `ann4_2.tbl1` | `table` | `table` | `国立感染症研究所における施設の位置、構造及び設備の技術上の基準一覧` |
| 4 | `ann4_2.tbl1.tblh_visual` | `table_header` | `table_header` | `区分 | 基準 | 1種 BSL4 | 2種 BSL3 | 2種 BSL2 | 3種 BSL3 | 3種 BSL2 | 4種 BSL3 | 4種 BSL2` |
| 5 | `ann4_2.tbl1.tblh_visual.tblr22` | `table_row` | `table_row` | `実験室内 | 安全キャビネット | ○（高度：クラスIII） | ○（クラスII以上） | ○（クラスII以上） | ○（クラスII以上） | ○（クラスII以上） | ○（クラスII以上） | ○（クラスII以上）` |
