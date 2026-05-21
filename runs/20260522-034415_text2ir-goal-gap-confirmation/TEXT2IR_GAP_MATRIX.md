# TEXT2IR_GAP_MATRIX

| 文書 | 観測された課題 | GOALとの差 | 根拠 | 分類 | 推奨対応 | 優先度 | 備考 |
|---|---|---|---|---|---|---|---|
| EU GMP Vol.4 Chapter 1 | 基礎GOALは到達。表・注記ノードの実データ確認は未了 | 代表出力にtable/noteがない | 再生成結果 table 0/note 0 | 判断保留 | 原文内に表・注記があるか確認し、必要なら入力整形またはprofileで扱う | 中 | 現時点では正式化候補に近い |
| WHO LBM 3rd | 基礎GOALは到達。ただしitem中心でparagraphが出ない | xml2irの条文系とは粒度が異なる | item 754, paragraph 0 | profile変更で済む | DQ候補粒度としてitemでよいか確認し、必要ならmarker/profileを調整 | 中 | 文書性質上、完全同型は不要 |
| PIC/S PE 009-17 Part I | 基礎GOALは到達。表・注記ノードなし | 表/注記GOALの実データ確認なし | table 0/note 0 | 判断保留 | 原文の表・注記有無をサンプル確認 | 中 | 章・paragraph/item構造は安定 |
| PIC/S PE 009-17 Part II | section headingがtext先頭に入る箇所がある | 見出しと本文の分離がxml2ir水準より弱い | 例: section text starts with Objective/Scope/Principles | profile変更で済む | marker/heading continuation/profileの調整で切り分ける | 中 | 共通parser本体へ文書名ベタ書き不要 |
| PIC/S PE 009-17 Annex 15 | 見出し継続が分割される箇所がある | 見出し表示品質がGOAL未満 | 例: heading `ORGANISING AND PLANNING FOR QUALIFICATION AND`, text `VALIDATION` | profile変更で済む | heading continuation条件をprofileで補強 | 高 | 最初のprofile修正候補 |
| PIC/S Annex 11 | section headingがnullで本文先頭へ入る箇所がある | 候補表示時の文脈見出しが弱い | 例: sec1 heading null, text starts `Risk Management` | profile変更で済む | section marker/profileの見出し抽出を調整 | 中 | 小規模で確認しやすい |
| PIC/S Annex 2A | Part A/B階層がchapter textに吸収される箇所がある | 階層・見出しがGOAL未満 | chapter heading null, text starts `Part A...` / `B1...` | profile変更で済む | Part A/B/B1 markerをprofileで調整 | 中 | 文書固有階層として扱う |
| PIC/S PE 009-17 Annexes全体 refined | 基礎GOALは到達。ただし入口がsubtree refine/dispatch/fallback依存 | 単純な共通text2ir文書ではなく複合入口 | manifest refine applied 19件 | 拡張パーサー/特別部品が必要 | 共通parserではなくrefine部品として仕様化 | 高 | 既に拡張部品的性格 |
| 代表文書全体 | table/table_row/table_header/noteが実データで0 | 表・注記GOALを正式判断できない | 9件すべて table 0/note 0 | 判断保留 | 表を含む実入力またはMarkdown化入力で再確認 | 高 | fixtureテストだけで正式化判断しない |
| 代表文書全体 | v4/4ファイル/manifest/source_spansは到達 | GOALとの差は小さい | 9件全件 v4、4ファイル、manifest、source_spansあり | text2ir共通更改が必要 | 更改というよりGOAL検証ハーネスとして固定する | 高 | verify_documentとtext2ir qualitycheckの統合運用 |
| CFR Part 11 | 現行repo内に代表入力なし | 再生成根拠不足 | data/human-readableにCFR入力なし | 判断保留 | 正式入力を追加して再評価 | 中 | fixtureのみ存在 |
| CFR Part 211 | 現行repo内に代表入力なし。eCFR XML入口が有力 | text2irプレーンテキスト評価不能 | data/human-readableにCFR入力なし | 拡張パーサー/特別部品が必要 | eCFR XML専用入口を検討 | 中 | テキストより安定構造入力を優先 |

## 分類件数

- `profile変更で済む`: 5
- `text2ir共通更改が必要`: 1
- `拡張パーサー/特別部品が必要`: 2
- `判断保留`: 4
