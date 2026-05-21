# TEXT2IR_GAP_RESOLUTION_MATRIX

| 文書/課題 | 確認RUNでの課題 | 分類 | 今回対応 | 変更ファイル | 検証結果 | 残課題 | 次アクション |
|---|---|---|---|---|---|---|---|
| GOAL検証 | strict成功だけでは不足 | 共通更改済み | GOALチェックハーネス追加 | `src/qai_text2ir/goal_check.py` | 代表9文書 pass | meta.family warning | GOAL項目の厳格度をレビュー |
| 監査レポート | 再生成結果集計が手作業 | 共通更改済み | audit report追加 | `src/qai_text2ir/audit_report.py` | 9文書集計成功 | なし | 正規化RUNへ組み込み検討 |
| 表・注記 | 代表9文書でtable/note 0 | 一部解消 | 代表文書由来fixture追加、Markdown table構造化確認 | `tests/test_table_note_real_samples.py`, `text_parser.py` | fixture pass | 実文書全体ではtable/note 0 | 表を含む入力整形方針レビュー |
| Plaintext table | PDF抽出表の黙殺懸念 | 一部解消 | profile有効時にpossible_tableとして保持 | `text_parser.py` | plaintext fixture pass | 複雑表の構造化は未対応 | 拡張部品候補へ |
| PIC/S Annex 15 | 見出し継続が分割 | 解消 | profileと汎用継続オプションで改善 | `pics_annex15_default_v1.yaml`, `text_parser.py` | 実データでsection heading改善 | なし | review candidate候補 |
| PIC/S Annex 11 | section headingがtextへ吸収 | 解消 | `section`をstructural化 | `pics_annex11_default_v1.yaml` | 実データでheading分離 | なし | review candidate候補 |
| PIC/S Annex 2A | Part/B1階層が弱い | 一部解消 | B1 marker追加 | `pics_annex2a_default_v1.yaml` | B1 fixture pass、再生成 pass | Part A説明文の扱いは要レビュー | 実データサンプルレビュー |
| PIC/S Part II | section heading/text分離が弱い | 解消 | `section`をstructural化 | `pics_part2_default_v1.yaml` | Objective/Scope/Principles分離 | なし | 再生成差分レビュー |
| WHO LBM 3rd | item粒度判断 | 判断保留 | 代表10件レビュー | `WHO_LBM_CANDIDATE_GRANULARITY_REVIEW.md` | item粒度を当面許容 | UI実レビュー未了 | 人間レビュー |
| PIC/S Annexes refined | 複合入口 | 拡張入口へ移管 | 設計文書化 | `EXTENSION_ENTRANCE_DESIGN.md` | refine 19件、GOAL pass | 複合入口仕様の正式化 | 専用設計レビュー |
| CFR Part 211/11 | 正式入力なし | 拡張入口へ移管 | eCFR XML入口方針を文書化 | `EXTENSION_ENTRANCE_DESIGN.md` | 再生成対象外 | 入力配置未決定 | eCFR入口RUN |
