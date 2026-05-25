# NIID別表・付表 table inventory

| 対象 | 見出し | 形式 | 列復元 | 次アクション | 根拠 |
| --- | --- | --- | --- | --- | --- |
| 別表1 | 病原体等の取扱いにおいては、病原体等のリスク群分類（付表１－１）を基準として、付表１－ | narrative_reference | not_applicable | keep_as_annex_text | 別表・付表の適用関係を説明する短い本文であり、表列復元対象ではない |
| 付表1-1 | 病原体等のリスク群による分類 | narrative_reference | not_applicable | keep_as_annex_text | リスク群分類の説明本文であり、列境界を持つ表ではない |
| 付表1-2 | リスク評価項目 | numbered_assessment_items | not_applicable | consider_numbered_item_structure_later | リスク評価項目の列挙であり、表列復元より番号付き項目化の検討が先 |
| 付表1-3 | 動物実験におけるリスク評価項目 | numbered_assessment_items | not_applicable | consider_numbered_item_structure_later | 動物実験リスク評価項目の列挙であり、表列復元対象ではない |
| 付表2 | 病原体等のリスク群分類と、実験室のＢＳＬ分類、実験室使用目的、 | fixed_width_matrix | candidate | table_adapter_candidate | BSL分類、使用目的、実験手技、安全機器の関係を複数列で示す固定幅表 |
| 付表3 | ＢＳＬ実験室の安全設備基準 | fixed_width_matrix | candidate | table_adapter_candidate | BSL1-4の安全設備基準を横持ち列で比較する固定幅表 |
| 付表4 | 病原体等取扱動物実験施設のＡＢＳＬ分類、実験手技、安全機器 | fixed_width_matrix | candidate | table_adapter_candidate | ABSL1-4の実験手技・安全機器・設備基準を横持ち列で比較する固定幅表 |
| 別表2 | 病原体等取扱実験室の安全設備及び運営基準 | sectioned_text | not_applicable | consider_section_structure_later | BSLごとの文章型基準であり、列復元ではなく節構造化の検討対象 |
| 別表3 | 病原体等取扱動物実験施設の安全設備及び運営基準 | sectioned_text | not_applicable | consider_section_structure_later | ABSLごとの文章型基準であり、列復元ではなく節構造化の検討対象 |
| 別表4 | 国立感染症研究所における施設の位置、構造及び設備の技術上の基準一覧 | large_fixed_width_matrix | candidate_complex | table_adapter_candidate_after_manual_review | 特定病原体等区分ごとの技術基準一覧で、横長かつ複数行セルが多い |
| 別表5 | 国立感染症研究所における特定病原体等の保管等の技術上の基準一覧 | large_fixed_width_matrix | candidate_complex | table_adapter_candidate_after_manual_review | 保管等の技術基準一覧で、横長かつ注記・滅菌基準の複数行セルが多い |
| 別表6 | 病原体等安全管理区域運営規則作成基準 | numbered_requirements | not_applicable | consider_numbered_item_structure_later | 運営規則作成基準の番号付き要求事項であり、表列復元対象ではない |
| 別表7 | 記帳事項に関する一覧（法第５６条の２３関係） | fixed_width_matrix | candidate | table_adapter_candidate | 記帳項目、記帳内容、1-3種病原体等の要否を並べた固定幅表 |
| 別表8 | 特定病原体等の取扱いに必要な教育訓練（法第５６条の２１関係） | fixed_width_matrix_with_embedded_items | candidate_complex | table_adapter_candidate_after_manual_review | 教育訓練対象、記載項目、回数、備考の表だが、箇条書きがセル内に混在する |
| 別表9 | 災害時の対応内容（法第５６条の２９関係） | numbered_requirements | not_applicable | consider_numbered_item_structure_later | 災害時対応の番号付き要求事項であり、表列復元対象ではない |
| 別表10 | 感染症発生予防規程対照表（法第５６条の１８関係） | fixed_width_comparison_table | candidate | table_adapter_candidate | 省令項目、具体的内容、規程該当部分を対応付ける比較表 |
