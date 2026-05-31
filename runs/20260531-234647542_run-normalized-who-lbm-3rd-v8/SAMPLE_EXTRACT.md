# 深い階層サンプル抽出

- source: `runs/20260531-234647542_run-normalized-who-lbm-3rd-v8/promotion_candidate/who_lbm_3rd_2004_9241546506.regdoc_ir.yaml`
- target_nid: `ann5.tbla5_1.tblh.tblr1`
- method: IR YAMLをparseし、target_nidの祖先経路を抽出

| 階層 | nid | kind | kind_raw | text / heading |
|---:|---|---|---|---|
| 1 | `root` | `document` |  |  |
| 2 | `ann5` | `annex` | `Annex` | `Chemicals: hazards and precautions` |
| 3 | `ann5.tbla5_1` | `table` | `table` | `Table A5-1. Chemicals: hazards and precautions` |
| 4 | `ann5.tbla5_1.tblh` | `table_header` | `table_header` | `Chemical | Physical properties | Health hazards | Fire hazards | Safety precautions | Incompatible chemicals / other hazards` |
| 5 | `ann5.tbla5_1.tblh.tblr1` | `table_row` | `table_row` | `Acetaldehyde | Colourless liquid or | Mild eye and | Extremely flammable; | No open flames, no | Can form explosive` |
