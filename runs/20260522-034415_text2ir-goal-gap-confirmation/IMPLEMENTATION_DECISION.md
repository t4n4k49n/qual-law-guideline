# IMPLEMENTATION_DECISION

## 結論

最初に大規模なtext2ir本体改修へ入る必要はない。まずはGOAL検証ハーネスを固定し、PIC/S Annex 15、Annex 11、Annex 2Aなどの見出し・階層ギャップをprofileで潰すのが妥当。PIC/S Annexes全体 refined とCFR Part 211は、共通parserではなく拡張入口・特別部品として扱う候補。

## 先に実装すべき共通更改

1. text2ir出力に対するGOAL検証コマンドを固定する。v4、4ファイル、manifest、source_spans、nid/ord、dq_gmp_checklistを一括チェックする。
2. 表・注記・子孫表示の実データ検証fixtureを追加する。既存fixtureではなく、代表文書由来の小サンプルを使う。
3. manifest/qualitycheck/verify結果をRUN報告へ機械集計する小さな監査レポートを整える。

## profile修正で済ませるもの

- PIC/S Annex 15の見出し継続。
- PIC/S Annex 11のsection見出し抽出。
- PIC/S Annex 2AのPart A/B/B1階層。
- PIC/S Part IIのsection heading/text分離。
- WHO LBM 3rdの候補粒度をitem中心でよいか、またはparagraph相当へ寄せるかのprofile判断。

## 拡張パーサー/特別部品候補

- PIC/S PE 009-17 Annexes全体 refined: 親profileでAnnexを切り、子profileへdispatch/fallbackする複合入口として仕様化する。
- CFR Part 211: プレーンテキストよりeCFR XML等の安定構造入力を優先する入口を検討する。
- 複雑表・PDF複数カラム崩れ: 共通parserへ無理に入れず、前処理または専用部品化する。

## 判断保留と追加確認事項

- 代表文書原文に表・注記があるか。ある場合、現在のhuman-readable入力で失われているか。
- CFR Part 11 / Part 211 の正式入力をどこに置くか。
- WHO LBM 3rdをDQ候補としてitem粒度で扱うか。

## 推奨する最初の正式化候補文書

1. EU GMP Vol.4 Chapter 1: 小さく、v4/4ファイル/strict/verifyが通り、構造ギャップが少ない。
2. PIC/S PE 009-17 Annex 15: GMPクオリフィケーション上の重要度が高いが、見出し継続のprofile修正を先に行う。
3. PIC/S Annex 11: 小規模で、見出し抽出の改善効果を確認しやすい。

## 次にCodexへ投げるべき実装プロンプトの要点

- コード本体ではなく、まずGOAL検証ハーネスと代表文書由来の表・注記fixtureを追加する。
- 次にPIC/S Annex 15/11/2Aのprofile修正を小分けRUNで行う。
- PIC/S Annexes全体 refinedは、共通parser改修ではなく拡張入口として設計文書化してから触る。
- CFRは現行repoへ正式入力を追加してから評価し、Part 211はeCFR XML入口を優先検討する。
