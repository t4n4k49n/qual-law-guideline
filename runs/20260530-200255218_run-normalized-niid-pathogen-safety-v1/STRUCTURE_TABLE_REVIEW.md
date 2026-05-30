# NIID Structure/Table Manual Review

## Scope

- Target: `jp_niid_pathogen_safety_management_20240401`
- Source: `data/human-readable/niid/pathogen_safety_management/source_texts/Kanrikitei3_20240401.txt`
- Review focus: headings, annex/table preservation, merged/wrapped visual-review records, Japanese prose spaces/newlines.

## Root Structure

| kind | num | nid | heading |
|---|---:|---|---|
| chapter | 1 | `cha1` | 総則 |
| chapter | 2 | `cha2` | 安全管理体制 |
| chapter | 3 | `cha3` | 安全管理基準 |
| chapter | 4 | `cha4` | 健康管理 |
| chapter | 5 | `cha5` | 遵守義務と罰則 |
| chapter | 6 | `cha6` | 雑則 |
| annex | 別表1 | `ann1` | 病原体等の取扱いにおいては、病原体等のリスク群分類（付表１－１）を基準として、付表１－ |
| annex | 付表1-1 | `ann1_1` | 病原体等のリスク群による分類 |
| annex | 付表1-2 | `ann1_2` | リスク評価項目 |
| annex | 付表1-3 | `ann1_3` | 動物実験におけるリスク評価項目 |
| annex | 付表2 | `ann2` | 病原体等のリスク群分類と、実験室のＢＳＬ分類、実験室使用目的、実験手技及び安全機器との関連性 |
| annex | 付表3 | `ann3` | ＢＳＬ実験室の安全設備基準 |
| annex | 付表4 | `ann4` | 病原体等取扱動物実験施設のＡＢＳＬ分類、実験手技、安全機器及び設備基準 |
| annex | 別表2 | `ann2_2` | 病原体等取扱実験室の安全設備及び運営基準 |
| annex | 別表3 | `ann3_2` | 病原体等取扱動物実験施設の安全設備及び運営基準 |
| annex | 別表4 | `ann4_2` | 国立感染症研究所における施設の位置、構造及び設備の技術上の基準一覧 |
| annex | 別表5 | `ann5` | 国立感染症研究所における特定病原体等の保管等の技術上の基準一覧 |
| annex | 別表6 | `ann6` | 病原体等安全管理区域運営規則作成基準 |
| annex | 別表7 | `ann7` | 記帳事項に関する一覧（法第５６条の２３関係） |
| annex | 別表8 | `ann8` | 特定病原体等の取扱いに必要な教育訓練（法第５６条の２１関係） |
| annex | 別表9 | `ann9` | 災害時の対応内容（法第５６条の２９関係） |
| annex | 別表10 | `ann10` | 感染症発生予防規程対照表（法第５６条の１８関係） |

## Chapter Check

- Root chapters: `['1', '2', '3', '4', '5', '6']`
- TOC-derived duplicate chapters: none observed; root chapter nums are 1 through 6 once each.
- Candidate visibility excludes `cha1`, `cha5`, and `cha6` while preserving them in IR.

## Annex Check

- Root annex count: `16`
- Expected annexes are preserved: 別表1, 付表1-1, 付表1-2, 付表1-3, 付表2, 付表3, 付表4, 別表2, 別表3, 別表4, 別表5, 別表6, 別表7, 別表8, 別表9, 別表10.
- 付表2 and 付表4 headings were checked for wrapped title continuation and normalized to full titles.

| num | nid | mode | heading sample |
|---|---|---|---|
| 別表1 | `ann1` | annex_text | 病原体等の取扱いにおいては、病原体等のリスク群分類（付表１－１）を基準として、付表１－ |
| 付表1-1 | `ann1_1` | annex_text | 病原体等のリスク群による分類 |
| 付表1-2 | `ann1_2` | annex_text_with_existing_subitems | リスク評価項目 |
| 付表1-3 | `ann1_3` | annex_text_with_existing_subitems | 動物実験におけるリスク評価項目 |
| 付表2 | `ann2` | visual_reviewed_table_records | 病原体等のリスク群分類と、実験室のＢＳＬ分類、実験室使用目的、実験手技及び安全機器との関連性 |
| 付表3 | `ann3` | visual_reviewed_table_records | ＢＳＬ実験室の安全設備基準 |
| 付表4 | `ann4` | visual_reviewed_table_records | 病原体等取扱動物実験施設のＡＢＳＬ分類、実験手技、安全機器及び設備基準 |
| 別表2 | `ann2_2` | annex_text | 病原体等取扱実験室の安全設備及び運営基準 |
| 別表3 | `ann3_2` | annex_text | 病原体等取扱動物実験施設の安全設備及び運営基準 |
| 別表4 | `ann4_2` | annex_text_raw_hold | 国立感染症研究所における施設の位置、構造及び設備の技術上の基準一覧 |
| 別表5 | `ann5` | annex_text_raw_hold | 国立感染症研究所における特定病原体等の保管等の技術上の基準一覧 |
| 別表6 | `ann6` | annex_text | 病原体等安全管理区域運営規則作成基準 |
| 別表7 | `ann7` | visual_reviewed_table_records | 記帳事項に関する一覧（法第５６条の２３関係） |
| 別表8 | `ann8` | annex_text_raw_hold | 特定病原体等の取扱いに必要な教育訓練（法第５６条の２１関係） |
| 別表9 | `ann9` | annex_text | 災害時の対応内容（法第５６条の２９関係） |
| 別表10 | `ann10` | visual_reviewed_table_records | 感染症発生予防規程対照表（法第５６条の１８関係） |

## Table Check

- Generated tables: `5`
- Visual-reviewed tables keep `raw_table_audit` plus reviewed `cells`/`record` values.
- Table adapter removes parser-created row-number item artifacts after table promotion.

| annex | table nid | rows | reconstruction | columns |
|---|---|---:|---|---|
| 付表2 | `ann2.tbl1` | 4 | visual_reviewed_cells / complete | risk_group, laboratory_bsl, laboratory_purpose, laboratory_practice_operation, safety_equipment |
| 付表3 | `ann3.tbl1` | 15 | visual_reviewed_cells / complete | criterion, parent_criterion, bsl1, bsl2, bsl3, bsl4 |
| 付表4 | `ann4.tbl1` | 4 | visual_reviewed_cells / complete | absl, laboratory_practice, safety_equipment, facility_criteria |
| 別表7 | `ann7.tbl1` | 18 | visual_reviewed_cells / complete | category, ordinance_item, record_content, pathogen_type_1, pathogen_type_2, pathogen_type_3 |
| 別表10 | `ann10.tbl1` | 13 | visual_reviewed_cells / complete | category, ordinance_item, specific_content, regulation_reference |

## Prose Normalization Check

- Display `heading`/`text` fields were scanned structurally, excluding table raw metadata.
- Japanese-letter internal spaces: `0` findings.
- Literal `\n` or CR artifacts: `0` findings.
- Page marker lines in display fields: `0` findings.

## Remaining Raw Metadata

- `raw_lines` and `original_text_before_table_adapter` intentionally preserve extracted fixed-width source text for traceability.
- These metadata fields still contain fixed-width spacing by design and are not candidate display text.
