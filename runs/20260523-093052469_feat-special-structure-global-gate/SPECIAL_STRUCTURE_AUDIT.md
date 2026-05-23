# SPECIAL STRUCTURE AUDIT

- Run out dir: `out/20260523-093052469_feat-special-structure-global-gate/bundles`
- Mode: `normal`
- Status: `warn`

| doc_id | source_tables | source_figures | generated_tables | generated_rows | generated_figures | unresolved_special_blocks | status |
|---|---:|---:|---:|---:|---:|---:|---|
| pics_annex1 | 6 | 0 | 0 | 0 | 0 | 14 | warn |
| pics_annex2a | 1 | 2 | 0 | 0 | 0 | 8 | warn |
| pics_part2 | 2 | 0 | 0 | 0 | 0 | 3 | warn |
| who_lbm_3rd | 18 | 12 | 0 | 0 | 0 | 43 | warn |

## Unresolved Blocks

| doc_id | source_path | line_range | trigger | generated_node_nid | recommended_resolution |
|---|---|---:|---|---|---|
| pics_annex1 | `data\human-readable\pics\pe009-17_annex1_2023-08-25_en.txt` | 711-734 | fixed_width_block_in_ordinary_text | ann1.sec4.p4_27 | targeted_parser |
| pics_annex1 | `data\human-readable\pics\pe009-17_annex1_2023-08-25_en.txt` | 715-718 | possible_plaintext_table_not_structured, possible_table | ann1.sec4.p4_27.pre1 | targeted_parser |
| pics_annex1 | `data\human-readable\pics\pe009-17_annex1_2023-08-25_en.txt` | 792-800 | possible_plaintext_table_not_structured, possible_table | ann1.sec4.p4_31.pre1 | targeted_parser |
| pics_annex1 | `data\human-readable\pics\pe009-17_annex1_2023-08-25_en.txt` | 1395-1407 | caption_with_fixed_width_in_ordinary_text, fixed_width_block_in_ordinary_text | ann1.sec8.p8_6 | targeted_parser |
| pics_annex1 | `data\human-readable\pics\pe009-17_annex1_2023-08-25_en.txt` | 1437-1468 | caption_with_fixed_width_in_ordinary_text, fixed_width_block_in_ordinary_text | ann1.sec8.p8_10 | targeted_parser |
| pics_annex1 | `data\human-readable\pics\pe009-17_annex1_2023-08-25_en.txt` | 2957-2965 | possible_plaintext_table_not_structured, possible_table | ann1.sec9.p9_15.pre1 | targeted_parser |
| pics_annex1 | `data\human-readable\pics\pe009-17_annex1_2023-08-25_en.txt` | 3097-3121 | fixed_width_block_in_ordinary_text | ann1.sec9.p9_30 | targeted_parser |
| pics_annex1 | `data\human-readable\pics\pe009-17_annex1_2023-08-25_en.txt` | 3099-3103 | possible_plaintext_table_not_structured, possible_table | ann1.sec9.p9_30.pre1 | targeted_parser |
| pics_annex1 | `data/human-readable/pics/pe009-17_annex1_2023-08-25_en.txt` | 715 | Table 1: Maximum permitted total particle concentration for classification |  | targeted_parser |
| pics_annex1 | `data/human-readable/pics/pe009-17_annex1_2023-08-25_en.txt` | 792 | Table 2: Maximum permitted microbial contamination level during qualification |  | targeted_parser |
| pics_annex1 | `data/human-readable/pics/pe009-17_annex1_2023-08-25_en.txt` | 1398 | Table 3: Examples of operations and grades for terminally sterilised preparation and |  | targeted_parser |
| pics_annex1 | `data/human-readable/pics/pe009-17_annex1_2023-08-25_en.txt` | 1440 | Table 4:   Examples of operations and grades for aseptic preparation and processing |  | targeted_parser |
| pics_annex1 | `data/human-readable/pics/pe009-17_annex1_2023-08-25_en.txt` | 2957 | Table 5: Maximum permitted total particle concentration for monitoring. |  | targeted_parser |
| pics_annex1 | `data/human-readable/pics/pe009-17_annex1_2023-08-25_en.txt` | 3099 | Table 6: Maximum action limits for viable particle contamination |  | targeted_parser |
| pics_annex2a | `data\human-readable\pics\pe009-17_annex2a_2023-08-25_en.txt` | 74-217 | caption_with_fixed_width_in_ordinary_text, fixed_width_block_in_ordinary_text | ann2a.sec2.ib | targeted_parser |
| pics_annex2a | `data\human-readable\pics\pe009-17_annex2a_2023-08-25_en.txt` | 220-231 | fixed_width_block_in_ordinary_text, form_control_in_ordinary_text | ann2a.sec2.ib.si1 | targeted_parser |
| pics_annex2a | `data\human-readable\pics\pe009-17_annex2a_2023-08-25_en.txt` | 232-269 | caption_with_fixed_width_in_ordinary_text, fixed_width_block_in_ordinary_text, form_control_in_ordinary_text | ann2a.sec2.ib.si2 | targeted_parser |
| pics_annex2a | `data\human-readable\pics\pe009-17_annex2a_2023-08-25_en.txt` | 272-281 | fixed_width_block_in_ordinary_text, form_control_in_ordinary_text | ann2a.sec2.ib.si3 | targeted_parser |
| pics_annex2a | `data\human-readable\pics\pe009-17_annex2a_2023-08-25_en.txt` | 282-286 | fixed_width_block_in_ordinary_text | ann2a.sec2.ib.si4 | targeted_parser |
| pics_annex2a | `data/human-readable/pics/pe009-17_annex2a_2023-08-25_en.txt` | 113 | Table 1. Illustrative guide to manufacturing activities within the scope of Annex 2A |  | targeted_parser |
| pics_annex2a | `data/human-readable/pics/pe009-17_annex2a_2023-08-25_en.txt` | 188 | Figure 1: Example of gene therapy mRNA                     Figure 2: Example of in vivo viral vector gene |  | targeted_parser |
| pics_annex2a | `data/human-readable/pics/pe009-17_annex2a_2023-08-25_en.txt` | 247 | Figure 3: Example of autologous CAR-T therapy ATMP manufacturing |  | targeted_parser |
| pics_part2 | `data\human-readable\pics\pe009-17_part2_2023-08-25_en.txt` | 256-377 | caption_with_fixed_width_in_ordinary_text, fixed_width_block_in_ordinary_text | cha1.sec1_2 | targeted_parser |
| pics_part2 | `data/human-readable/pics/pe009-17_part2_2023-08-25_en.txt` | 311 | Table 1. It does not imply that all steps shown should be completed. The stringency of |  | targeted_parser |
| pics_part2 | `data/human-readable/pics/pe009-17_part2_2023-08-25_en.txt` | 328 | Table 1:    Application of this Guide to API Manufacturing |  | targeted_parser |
| who_lbm_3rd | `data\human-readable\who\WHO_LBM_3rd.txt` | 315-462 | caption_with_fixed_width_in_ordinary_text, fixed_width_block_in_ordinary_text | cha1 | targeted_parser |
| who_lbm_3rd | `data\human-readable\who\WHO_LBM_3rd.txt` | 363-365 | possible_plaintext_table_not_structured, possible_table | cha1.pre1 | targeted_parser |
| who_lbm_3rd | `data\human-readable\who\WHO_LBM_3rd.txt` | 555-1022 | form_control_in_ordinary_text | cha3 | profile_rule |
| who_lbm_3rd | `data\human-readable\who\WHO_LBM_3rd.txt` | 1383-1422 | caption_with_fixed_width_in_ordinary_text, fixed_width_block_in_ordinary_text | cha6 | targeted_parser |
| who_lbm_3rd | `data\human-readable\who\WHO_LBM_3rd.txt` | 1742-2159 | caption_with_fixed_width_in_ordinary_text, checklist_header_in_ordinary_text, fixed_width_block_in_ordinary_text, form_control_in_ordinary_text | cha8.i5 | targeted_parser |
| who_lbm_3rd | `data\human-readable\who\WHO_LBM_3rd.txt` | 2013-2014 | form_control_in_ordinary_text | cha8.i5.si1 | profile_rule |
| who_lbm_3rd | `data\human-readable\who\WHO_LBM_3rd.txt` | 2015-2015 | form_control_in_ordinary_text | cha8.i5.si2 | profile_rule |
| who_lbm_3rd | `data\human-readable\who\WHO_LBM_3rd.txt` | 2259-2756 | caption_with_fixed_width_in_ordinary_text, fixed_width_block_in_ordinary_text | cha10 | targeted_parser |
| who_lbm_3rd | `data\human-readable\who\WHO_LBM_3rd.txt` | 2763-3055 | caption_with_fixed_width_in_ordinary_text, fixed_width_block_in_ordinary_text | cha11 | targeted_parser |
| who_lbm_3rd | `data\human-readable\who\WHO_LBM_3rd.txt` | 3662-4091 | caption_with_fixed_width_in_ordinary_text, fixed_width_block_in_ordinary_text | cha14 | targeted_parser |
| who_lbm_3rd | `data\human-readable\who\WHO_LBM_3rd.txt` | 4095-4171 | caption_with_fixed_width_in_ordinary_text, fixed_width_block_in_ordinary_text | cha14.i4 | targeted_parser |
| who_lbm_3rd | `data\human-readable\who\WHO_LBM_3rd.txt` | 4563-4702 | caption_with_fixed_width_in_ordinary_text, fixed_width_block_in_ordinary_text | cha17 | targeted_parser |
| who_lbm_3rd | `data\human-readable\who\WHO_LBM_3rd.txt` | 4738-4797 | caption_with_fixed_width_in_ordinary_text, fixed_width_block_in_ordinary_text | cha18.i11 | targeted_parser |
| who_lbm_3rd | `data/human-readable/who/WHO_LBM_3rd.txt` | 325 | Table 1. Classification of infective microorganisms by risk group |  | targeted_parser |
| who_lbm_3rd | `data/human-readable/who/WHO_LBM_3rd.txt` | 363 | Table 2. Relation of risk groups to biosafety levels, practices and equipment |  | targeted_parser |
| who_lbm_3rd | `data/human-readable/who/WHO_LBM_3rd.txt` | 427 | Table 3. Summary of biosafety level requirements |  | targeted_parser |
| who_lbm_3rd | `data/human-readable/who/WHO_LBM_3rd.txt` | 1398 | Table 4. Animal facility containment levels: summary of practices and safety |  | targeted_parser |
| who_lbm_3rd | `data/human-readable/who/WHO_LBM_3rd.txt` | 1796 | Table 5. Basic Laboratory – Biosafety Level 1: laboratory safety survey |  | targeted_parser |
| who_lbm_3rd | `data/human-readable/who/WHO_LBM_3rd.txt` | 1978 | Table 6. Basic laboratory – Biosafety Level 2: laboratory safety survey. |  | targeted_parser |
| who_lbm_3rd | `data/human-readable/who/WHO_LBM_3rd.txt` | 2102 | Table 7. Containment laboratory – Biosafety Level 3: laboratory safety survey. |  | targeted_parser |
| who_lbm_3rd | `data/human-readable/who/WHO_LBM_3rd.txt` | 2304 | Table 8. Selection of a biological safety cabinet (BSC), by type of protection needed |  | targeted_parser |
| who_lbm_3rd | `data/human-readable/who/WHO_LBM_3rd.txt` | 2496 | Table 9. Differences between Class I, II and III biological safety cabinets (BSCs) |  | targeted_parser |
| who_lbm_3rd | `data/human-readable/who/WHO_LBM_3rd.txt` | 2808 | Table 10. Biosafety equipment |  | targeted_parser |
| who_lbm_3rd | `data/human-readable/who/WHO_LBM_3rd.txt` | 2972 | Table 11. Personal protective equipment |  | targeted_parser |
| who_lbm_3rd | `data/human-readable/who/WHO_LBM_3rd.txt` | 3756 | Table 12. Recommended dilutions of chlorine-releasing compounds |  | targeted_parser |
| who_lbm_3rd | `data/human-readable/who/WHO_LBM_3rd.txt` | 4607 | Table 13. General rules for chemical incompatibilities |  | targeted_parser |
| who_lbm_3rd | `data/human-readable/who/WHO_LBM_3rd.txt` | 4678 | Table 14. Storage of compressed and liquefied gases |  | targeted_parser |
| who_lbm_3rd | `data/human-readable/who/WHO_LBM_3rd.txt` | 4753 | Table 15. Types and uses of fire extinguishers |  | targeted_parser |
| who_lbm_3rd | `data/human-readable/who/WHO_LBM_3rd.txt` | 5707 | Table A4-1. Equipment and operations that may create hazards |  | targeted_parser |
| who_lbm_3rd | `data/human-readable/who/WHO_LBM_3rd.txt` | 5843 | Table A4-2. Common causes of equipment-related accidents |  | targeted_parser |
| who_lbm_3rd | `data/human-readable/who/WHO_LBM_3rd.txt` | 5893 | Table A5-1. Chemicals: hazards and precautions |  | targeted_parser |
| who_lbm_3rd | `data/human-readable/who/WHO_LBM_3rd.txt` | 600 | Figure 1. Biohazard warning sign for laboratory doors |  | targeted_parser |
| who_lbm_3rd | `data/human-readable/who/WHO_LBM_3rd.txt` | 745 | Figure 2. A typical Biosafety Level 1 laboratory |  | targeted_parser |
| who_lbm_3rd | `data/human-readable/who/WHO_LBM_3rd.txt` | 823 | Figure 3. A typical Biosafety Level 2 laboratory |  | targeted_parser |
| who_lbm_3rd | `data/human-readable/who/WHO_LBM_3rd.txt` | 1171 | Figure 4. A typical Biosafety Level 3 laboratory |  | targeted_parser |
| who_lbm_3rd | `data/human-readable/who/WHO_LBM_3rd.txt` | 1238 | Figure 5. Suggested format for medical contact card |  | targeted_parser |
| who_lbm_3rd | `data/human-readable/who/WHO_LBM_3rd.txt` | 2350 | Figure 6. Schematic diagram of a Class I biological safety cabinet. |  | targeted_parser |
| who_lbm_3rd | `data/human-readable/who/WHO_LBM_3rd.txt` | 2432 | Figure 7. Schematic representation of a Class IIA1 biological safety cabinet. |  | targeted_parser |
| who_lbm_3rd | `data/human-readable/who/WHO_LBM_3rd.txt` | 2489 | Figure 8. Schematic diagram of a Class IIB1 biological safety cabinet. |  | targeted_parser |
| who_lbm_3rd | `data/human-readable/who/WHO_LBM_3rd.txt` | 2566 | Figure 9. Schematic representation of a Class III biological safety cabinet (glove box). |  | targeted_parser |
| who_lbm_3rd | `data/human-readable/who/WHO_LBM_3rd.txt` | 4143 | Figure 10. Gravity displacement autoclave |  | targeted_parser |
| who_lbm_3rd | `data/human-readable/who/WHO_LBM_3rd.txt` | 4345 | Figure 11. Examples of triple packaging systems |  | targeted_parser |
| who_lbm_3rd | `data/human-readable/who/WHO_LBM_3rd.txt` | 4901 | Figure 12. International radiation |  | targeted_parser |

