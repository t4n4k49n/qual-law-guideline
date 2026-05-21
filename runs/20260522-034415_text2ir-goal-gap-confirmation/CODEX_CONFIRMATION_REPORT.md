# CODEX_CONFIRMATION_REPORT

## 実行したこと

- `docs/text2ir-goal-gap-confirmation` ブランチで確認RUNを作成した。
- 指定ファイルと管理者向け指南書を確認した。
- xml2ir正式版のGOALをv4/4ファイル/dq_gmp_checklist/source_spans/nid/ord/verify観点で整理した。
- text2irの現行機能を棚卸しした。
- 代表9文書を現行profileで再生成し、strictとverifyを確認した。
- ギャップを4分類へ整理した。

## 実行できなかったこと

- CFR Part 11 / Part 211 は現行repo内に代表入力が見つからず、再生成しなかった。
- 代表9文書では表・注記ノードが出力されず、実データでのtable/note/descendant表示品質は確認できなかった。

## 代表文書ごとの結果サマリ

| 文書 | 結果 |
|---|---|
| EU GMP Vol.4 Chapter 1 | strict exit 0, verify pass, nodes 72, warnings 0, table 0, note 0 |
| PIC/S Annex 11 | strict exit 0, verify pass, nodes 42, warnings 0, table 0, note 0 |
| PIC/S PE 009-17 Annex 15 | strict exit 0, verify pass, nodes 142, warnings 0, table 0, note 0 |
| PIC/S Annex 1 | strict exit 0, verify pass, nodes 552, warnings 0, table 0, note 0 |
| PIC/S Annex 2A | strict exit 0, verify pass, nodes 202, warnings 0, table 0, note 0 |
| PIC/S PE 009-17 Annexes全体 refined | strict exit 0, verify pass, nodes 1748, warnings 0, table 0, note 0 |
| PIC/S PE 009-17 Part I | strict exit 0, verify pass, nodes 342, warnings 0, table 0, note 0 |
| PIC/S PE 009-17 Part II | strict exit 0, verify pass, nodes 591, warnings 0, table 0, note 0 |
| WHO LBM 3rd | strict exit 0, verify pass, nodes 829, warnings 0, table 0, note 0 |

## GOALチェックリストの結論

9件とも基礎GOALである v4、4ファイル、manifest、source_spans、nid/ord検証、strict 成功までは到達している。残る主課題は、表・注記の実データ確認、見出し/階層のprofile調整、複合文書やCFR系の入口設計である。

## ギャップ分類の件数

- `profile変更で済む`: 5
- `text2ir共通更改が必要`: 1
- `拡張パーサー/特別部品が必要`: 2
- `判断保留`: 4

## 最も重要な課題

1. 表・注記ノードが代表9文書で0件のため、実データでのGOAL確認が未了。
2. PIC/S Annex 15/11/2A/Part IIに、見出し継続・見出し抽出・階層化のprofile課題が残る。
3. PIC/S Annexes全体 refined は複合入口として扱うべきで、共通parser本体へ文書固有処理を混ぜない方がよい。
4. CFR Part 11/211は正式入力がなく、Part 211はeCFR XML入口を検討すべき。
5. strict成功を正式昇格可能と扱わず、GOAL検証ハーネスと人間レビューを固定する必要がある。

## 1往復でユーザーに確認すべき質問

- `必須確認`: 表・注記の正式評価は、今回のhuman-readable入力に含まれる範囲で十分ですか。それとも原PDFから表・注記サンプルを別途作るべきですか。
- `必須確認`: WHO LBM 3rdはitem粒度をDQ候補として許容しますか。それともparagraph相当へ寄せますか。
- `推奨確認`: 最初の正式化候補はEU GMP Chapter 1で進めてよいですか。
- `推奨確認`: PIC/S Annex 15の見出し継続修正を、次のprofile修正RUNの先頭に置いてよいですか。
- `判断保留でよい`: CFR Part 211はeCFR XML入口を前提に設計検討へ回してよいですか。

## 次に進むための推奨プロンプト要点

- text2ir GOAL検証ハーネスを追加する。
- 代表文書由来の表・注記サンプルfixtureを作る。
- PIC/S Annex 15、Annex 11、Annex 2Aのprofile修正を小分けで実施する。
- PIC/S Annexes全体 refinedとCFR Part 211は拡張入口として設計文書化する。
