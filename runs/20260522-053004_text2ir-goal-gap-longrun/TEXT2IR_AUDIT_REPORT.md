# TEXT2IR AUDIT REPORT

- Run out dir: `out/20260522-053004_text2ir-goal-gap-longrun`
- Documents: 9
- GOAL pass: 9
- GOAL fail: 0

## Documents

| doc_id | goal | schema | 4files | manifest | strict | warnings | nodes | source coverage | table | row | note | profile | refine |
|---|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---|---:|
| eu_gmp_vol4_chap1_20130131 | pass | qai.regdoc_ir.v4 | True | True | True | 0 | 72 | 1.0 | 0 | 0 | 0 | eu_gmp_chap1_default_v2 | 0 |
| pics_pe00917_annex11_20230825 | pass | qai.regdoc_ir.v4 | True | True | True | 0 | 42 | 1.0 | 0 | 0 | 0 | pics_annex11_default_v1 | 0 |
| pics_pe00917_annex15_20230825 | pass | qai.regdoc_ir.v4 | True | True | True | 0 | 142 | 1.0 | 0 | 0 | 0 | pics_annex15_default_v1 | 0 |
| pics_pe00917_annex1_20230825 | pass | qai.regdoc_ir.v4 | True | True | True | 0 | 552 | 1.0 | 0 | 0 | 0 | pics_annex1_default_v2 | 0 |
| pics_pe00917_annex2a_20230825 | pass | qai.regdoc_ir.v4 | True | True | True | 0 | 204 | 1.0 | 0 | 0 | 0 | pics_annex2a_default_v1 | 0 |
| pics_pe00917_annexes_20230825_refined_v3_extends_trace | pass | qai.regdoc_ir.v4 | True | True | True | 0 | 1750 | 1.0 | 0 | 0 | 0 | pics_annexes_default_v3 | 19 |
| pics_pe00917_part1_20230825 | pass | qai.regdoc_ir.v4 | True | True | True | 0 | 342 | 1.0 | 0 | 0 | 0 | pics_part1_default_v3 | 0 |
| pics_pe00917_part2_20230825 | pass | qai.regdoc_ir.v4 | True | True | True | 0 | 591 | 1.0 | 0 | 0 | 0 | pics_part2_default_v1 | 0 |
| who_lbm_3rd_2004_9241546506 | pass | qai.regdoc_ir.v4 | True | True | True | 0 | 829 | 1.0 | 0 | 0 | 0 | who_lbm_3rd_default_v4 | 0 |

## GOAL Issues

- `eu_gmp_vol4_chap1_20130131` warning `meta_family_missing`: meta.doc.family is missing; older meta may omit it
- `pics_pe00917_annex11_20230825` warning `meta_family_missing`: meta.doc.family is missing; older meta may omit it
- `pics_pe00917_annex15_20230825` warning `meta_family_missing`: meta.doc.family is missing; older meta may omit it
- `pics_pe00917_annex1_20230825` warning `meta_family_missing`: meta.doc.family is missing; older meta may omit it
- `pics_pe00917_annex2a_20230825` warning `meta_family_missing`: meta.doc.family is missing; older meta may omit it
- `pics_pe00917_annexes_20230825_refined_v3_extends_trace` warning `meta_family_missing`: meta.doc.family is missing; older meta may omit it
- `pics_pe00917_part1_20230825` warning `meta_family_missing`: meta.doc.family is missing; older meta may omit it
- `pics_pe00917_part2_20230825` warning `meta_family_missing`: meta.doc.family is missing; older meta may omit it
- `who_lbm_3rd_2004_9241546506` warning `meta_family_missing`: meta.doc.family is missing; older meta may omit it
