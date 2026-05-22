# TEXT2IR FINAL GAP STATUS

## Conclusion

- 代表9文書は通常GOAL_CHECK: 9/9 pass。
- 代表9文書はpromotion GOAL_CHECK: 9/9 pass。
- `meta.doc.family` は代表9文書すべてで出力済み。
- 残GAP分類: {'none': 6, 'table_rows_pending': 3}

## Document Status

| 文書 | doc_id | goal | promotion | family | source coverage | warnings | table | row | note | possible_table | remaining_gap |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| EU GMP Vol.4 Chapter 1 | `eu_gmp_vol4_chap1_20130131` | pass | pass | EU_GMP | 1.0 | 0 | 0 | 0 | 0 | 0 | none |
| PIC/S Annex 1 | `pics_pe00917_annex1_20230825` | pass | pass | PICS | 1.0 | 0 | 0 | 0 | 9 | 4 | table_rows_pending |
| PIC/S Annex 11 | `pics_pe00917_annex11_20230825` | pass | pass | PICS | 1.0 | 0 | 0 | 0 | 0 | 0 | none |
| PIC/S Annex 15 | `pics_pe00917_annex15_20230825` | pass | pass | PICS | 1.0 | 0 | 0 | 0 | 0 | 0 | none |
| PIC/S Annex 2A | `pics_pe00917_annex2a_20230825` | pass | pass | PICS | 1.0 | 0 | 0 | 0 | 2 | 0 | none |
| PIC/S Annexes refined | `pics_pe00917_annexes_20230825_refined_v3_extends_trace` | pass | pass | PICS | 1.0 | 0 | 0 | 0 | 11 | 4 | table_rows_pending |
| PIC/S Part I | `pics_pe00917_part1_20230825` | pass | pass | PICS | 1.0 | 0 | 0 | 0 | 2 | 0 | none |
| PIC/S Part II | `pics_pe00917_part2_20230825` | pass | pass | PICS | 1.0 | 0 | 0 | 0 | 0 | 0 | none |
| WHO LBM 3rd | `who_lbm_3rd_2004_9241546506` | pass | pass | WHO | 1.0 | 0 | 0 | 0 | 1 | 1 | table_rows_pending |

## Interpretation

- `none`: 4ファイル、manifest、schema v4、source_spans、meta.family、通常/promotion GOAL_CHECKに明確な未達なし。
- `table_rows_pending`: 表候補は保持されているが、複雑な固定幅表を安全に `table_row` へ分解する追加改善余地がある。
- Phase 9D時点では、表を黙殺しないこととGOAL_CHECK promotion合格を優先し、危険な行分解は避けた。
