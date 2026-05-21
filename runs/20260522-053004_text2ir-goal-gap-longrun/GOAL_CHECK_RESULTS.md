# GOAL_CHECK_RESULTS

## 結論

代表9文書はすべてGOAL_CHECK pass。全件でv4、4ファイル、manifest、strict、verify、source_spans coverage 1.0を確認した。GOAL warningとして、現行meta出力に `doc.family` が存在しない点が全件で出ているが、doc識別子・jurisdiction・language・source・bundle・generationは確認できるためPhase 6では非ブロッキングとした。

## 結果一覧

| doc_id | goal | schema | 4files | manifest | strict | nodes | source coverage | table | row | note | warnings |
|---|---|---|---|---|---|---:|---:|---:|---:|---:|---:|
| eu_gmp_vol4_chap1_20130131 | pass | qai.regdoc_ir.v4 | True | True | True | 72 | 1.0 | 0 | 0 | 0 | 1 |
| pics_pe00917_annex11_20230825 | pass | qai.regdoc_ir.v4 | True | True | True | 42 | 1.0 | 0 | 0 | 0 | 1 |
| pics_pe00917_annex15_20230825 | pass | qai.regdoc_ir.v4 | True | True | True | 142 | 1.0 | 0 | 0 | 0 | 1 |
| pics_pe00917_annex1_20230825 | pass | qai.regdoc_ir.v4 | True | True | True | 552 | 1.0 | 0 | 0 | 0 | 1 |
| pics_pe00917_annex2a_20230825 | pass | qai.regdoc_ir.v4 | True | True | True | 204 | 1.0 | 0 | 0 | 0 | 1 |
| pics_pe00917_annexes_20230825_refined_v3_extends_trace | pass | qai.regdoc_ir.v4 | True | True | True | 1750 | 1.0 | 0 | 0 | 0 | 1 |
| pics_pe00917_part1_20230825 | pass | qai.regdoc_ir.v4 | True | True | True | 342 | 1.0 | 0 | 0 | 0 | 1 |
| pics_pe00917_part2_20230825 | pass | qai.regdoc_ir.v4 | True | True | True | 591 | 1.0 | 0 | 0 | 0 | 1 |
| who_lbm_3rd_2004_9241546506 | pass | qai.regdoc_ir.v4 | True | True | True | 829 | 1.0 | 0 | 0 | 0 | 1 |

## Warning概要

- 全件: `meta_family_missing`。現行 `qai_text2ir.cli` のmeta構造では `doc.family` ではなく identifiers等でfamily相当を管理しているため、Phase 6ではGOALハーネス側の注意喚起として扱う。
- 代表9文書本体の table/note 件数は0。表・注記の合格条件はPhase 3の代表文書由来fixtureで確認済み。
