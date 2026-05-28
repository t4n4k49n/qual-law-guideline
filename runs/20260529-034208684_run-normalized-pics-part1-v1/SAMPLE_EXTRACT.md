# 深い階層サンプル抽出

- source: `runs/20260529-034208684_run-normalized-pics-part1-v1/promotion_candidate/pics_pe00917_part1_20230825.regdoc_ir.yaml`
- target_nid: `cha7.not1`
- method: IR YAMLをparseし、target_nidの祖先経路を抽出

| 階層 | nid | kind | kind_raw | text / heading |
|---:|---|---|---|---|
| 1 | `root` | `document` |  |  |
| 2 | `cha7` | `chapter` | `CHAPTER` |  |
| 3 | `cha7.not1` | `note` | `note` | `Note: This Chapter deals with the responsibilities of manufacturers towards the  Competent Regulatory Authorities with respect to the granting of marketing and  manufacturing authorisations. It is not intended in any way to affect the respective  liability of Contract Acceptors and Contract Givers to consumers; this is governed  by other provisions of national law.` |
