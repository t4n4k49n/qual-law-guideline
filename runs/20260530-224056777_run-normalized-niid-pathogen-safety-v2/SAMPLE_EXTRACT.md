# 深い階層サンプル抽出

- source: `runs/20260530-224056777_run-normalized-niid-pathogen-safety-v2/promotion_candidate/jp_niid_pathogen_safety_management_20240401.regdoc_ir.yaml`
- target_nid: `ann1_2.i6`
- method: IR YAMLをparseし、target_nidの祖先経路を抽出

| 階層 | nid | kind | kind_raw | text / heading |
|---:|---|---|---|---|
| 1 | `root` | `document` |  |  |
| 2 | `ann1_2` | `annex` | `付表1` | `リスク評価項目` |
| 3 | `ann1_2.i6` | `item` | `６．` | `有効な治療法があり、それを受けることができるか否か（血清療法、曝露後ワクチン接種及び、抗菌剤、抗ウイルス剤、その他の化学療法剤も考慮する）。` |
