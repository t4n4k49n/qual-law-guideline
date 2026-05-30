# 深い階層サンプル抽出

- source: `runs/20260530-200255218_run-normalized-niid-pathogen-safety-v1/promotion_candidate/jp_niid_pathogen_safety_management_20240401.regdoc_ir.yaml`
- target_nid: `ann7.tbl1.tblh_visual.tblr2`
- method: IR YAMLをparseし、target_nidの祖先経路を抽出

| 階層 | nid | kind | kind_raw | text / heading |
|---:|---|---|---|---|
| 1 | `root` | `document` |  |  |
| 2 | `ann7` | `annex` | `別表1` | `記帳事項に関する一覧（法第５６条の２３関係）` |
| 3 | `ann7.tbl1` | `table` | `table` | `記帳事項に関する一覧（法第５６条の２３関係）` |
| 4 | `ann7.tbl1.tblh_visual` | `table_header` | `table_header` | `category | 省令での記載項目 | 記帳の内容 | 1種病原体等 | 2種病原体等 | 3種病原体等` |
| 5 | `ann7.tbl1.tblh_visual.tblr2` | `table_row` | `table_row` | `病原体等 | 病原体等の受入れ又は払出しの日時 | 事業所ごとに記帳（同上） | 年月日・時刻 | 年月日 | 年月日` |
