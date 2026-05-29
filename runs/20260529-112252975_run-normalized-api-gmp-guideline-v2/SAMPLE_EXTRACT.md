# 深い階層サンプル抽出

- source: `runs/20260529-112252975_run-normalized-api-gmp-guideline-v2/promotion_candidate/jp_pmda_api_gmp_guideline_20011102.regdoc_ir.yaml`
- target_nid: `cha2.sec2_2.p2_22.i15`
- method: IR YAMLをparseし、target_nidの祖先経路を抽出

| 階層 | nid | kind | kind_raw | text / heading |
|---:|---|---|---|---|
| 1 | `root` | `document` |  |  |
| 2 | `cha2` | `chapter` | `1.` | `品質マネージメント` |
| 3 | `cha2.sec2_2` | `section` | `2.2` | `品質部門の責任` |
| 4 | `cha2.sec2_2.p2_22` | `paragraph` | `2.22` |  |
| 5 | `cha2.sec2_2.p2_22.i15` | `item` | `15.` | `製品の品質の照査を実施すること(第2.5章で規定)。` |
