# GOAL CHECK SUMMARY

## Result

代表9文書は、現行 `goal_check --mode promotion` で全件PASS。

| doc_id | promotion | literal_pua | replacement_char | severe_visible_artifacts | form_artifacts | dot_leader_hits | contamination_guard |
|---|---|---:|---:|---:|---:|---:|---:|
| eu_gmp_vol4_chap1_20130131 | PASS | 0 | 0 | 0 | 0 | 0 | 0 |
| pics_pe00917_annex11_20230825 | PASS | 0 | 0 | 0 | 0 | 0 | 0 |
| pics_pe00917_annex15_20230825 | PASS | 0 | 0 | 0 | 0 | 0 | 0 |
| pics_pe00917_annex1_20230825 | PASS | 0 | 0 | 0 | 0 | 0 | 0 |
| pics_pe00917_annex2a_20230825 | PASS | 0 | 0 | 0 | 0 | 0 | 0 |
| pics_pe00917_annexes_20230825_refined_v3_extends_trace | PASS | 0 | 0 | 0 | 0 | 0 | 0 |
| pics_pe00917_part1_20230825 | PASS | 0 | 0 | 0 | 0 | 0 | 0 |
| pics_pe00917_part2_20230825 | PASS | 0 | 0 | 0 | 0 | 0 | 0 |
| who_lbm_3rd_2004_9241546506 | PASS | 0 | 0 | 0 | 6 | 0 | 0 |

## WHO LBM 3rd spot check

| nid | result |
|---|---|
| `cha8.i5` | 本来の説明文を `item` として保持 |
| `cha8.i5.si1` | `preformatted`, `kind_raw: form_artifact`, `not_selectable`, literal PUAなし、dot leaderなし |
| `cha8.i5.si2` | `preformatted`, `kind_raw: form_artifact`, `not_selectable`, literal PUAなし、dot leaderなし |
| `cha8.i5.art1` | Table 5以降のフォーム本体を分離・sanitize |

## Notes

- artifact監査では、WHO LBMの `raw_text_escaped` に dot leader由来のreview hitが1件残る。これは可読本文ではなく隔離artifactの原形説明欄であり、promotion gateでは失格対象にしていない。
- `raw_text_escaped` は literal PUA ではなく `<PUA-U+...>` 表現へescape済み。

