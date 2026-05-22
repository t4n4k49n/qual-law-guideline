# FINAL IMPLEMENTATION REPORT

## 結論

- text2irは、代表9文書について基礎GOALとpromotion GOAL_CHECKに到達した。
- EU GMP Chapter 1のpromotion candidateを作成済み。
- `data/normalized/` は変更していない。
- 残GAPは、複雑な固定幅表を安全に `table_row` 化する後続改善と、CFR XML adapterの別RUN実装。

## 代表9文書の再生成結果

| doc_id | goal | promotion goal | schema | family | table | table_row | note | possible_table | source coverage |
|---|---|---|---|---|---:|---:|---:|---:|---:|
| `eu_gmp_vol4_chap1_20130131` | pass | pass | qai.regdoc_ir.v4 | EU_GMP | 0 | 0 | 0 | 0 | 1.0 |
| `pics_pe00917_annex1_20230825` | pass | pass | qai.regdoc_ir.v4 | PICS | 0 | 0 | 9 | 4 | 1.0 |
| `pics_pe00917_annex11_20230825` | pass | pass | qai.regdoc_ir.v4 | PICS | 0 | 0 | 0 | 0 | 1.0 |
| `pics_pe00917_annex15_20230825` | pass | pass | qai.regdoc_ir.v4 | PICS | 0 | 0 | 0 | 0 | 1.0 |
| `pics_pe00917_annex2a_20230825` | pass | pass | qai.regdoc_ir.v4 | PICS | 0 | 0 | 2 | 0 | 1.0 |
| `pics_pe00917_annexes_20230825_refined_v3_extends_trace` | pass | pass | qai.regdoc_ir.v4 | PICS | 0 | 0 | 11 | 4 | 1.0 |
| `pics_pe00917_part1_20230825` | pass | pass | qai.regdoc_ir.v4 | PICS | 0 | 0 | 2 | 0 | 1.0 |
| `pics_pe00917_part2_20230825` | pass | pass | qai.regdoc_ir.v4 | PICS | 0 | 0 | 0 | 0 | 1.0 |
| `who_lbm_3rd_2004_9241546506` | pass | pass | qai.regdoc_ir.v4 | WHO | 0 | 0 | 1 | 1 | 1.0 |

## 表・注記の扱い

- 入力側にTable/Note候補がある文書では、`note` または `preformatted kind_raw=possible_table` として保持した。
- 複雑な固定幅表は、誤った列分割を避けるため `possible_table` として保持した。
- `table_row` への完全構造化は後続改善対象。

## Promotion Candidate

- 対象: `eu_gmp_vol4_chap1_20130131`
- 場所: `runs/20260522-130045_text2ir-final-goal-closure/promotion_candidate/eu_gmp_vol4_chap1_20130131/`
- promotion GOAL_CHECK: pass
- `data/normalized/` は未変更。

## CFR / 複合入口

- CFR Part 211はeCFR XML adapterを優先する設計に分離。
- PIC/S Annexes refinedは複合入口review candidateとして維持し、最初のpromotion candidateにはしない。

## テスト

- `python -m pytest -q`: `167 passed, 1 skipped`
- related tests: `17 passed`

## GitHub反映状況

- Phase 9D / 9E / 9F branches are pushed to origin.
- Direct push to remote main is blocked by repository rules requiring PR.
- `gh` token refresh is blocked by the current network/auth state, so remote main merge remains pending.
