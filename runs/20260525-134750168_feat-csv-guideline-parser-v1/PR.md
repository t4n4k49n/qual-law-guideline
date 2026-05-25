## まとめ

CSVガイドライン向けのParser開発として、専用 `text2ir` profile と実データテストを追加しました。正式な正規化処理や `data/normalized/` への昇格ではなく、MHLW HTMLから抽出した本文を安定して章・節・項目へ解析できることを確認する段階です。

## 変更内容

- `jp_mhlw_csv_guideline_v1` profileを追加
- MHLW通知の前文を本文開始前として除外
- 重複するCSVガイドラインのタイトル行を専用profile側で除外
- MHLW HTML抽出とCSV profile解析の実データテストを追加
- 共通profile、共通parserへの変更はなし

## 個別と共通の整理

- 個別: 通知名、CSVガイドラインの正式タイトル、本文開始境界は `jp_mhlw_csv_guideline_v1` に閉じています。
- 共通: 既存のJP guideline marker、HTML抽出器、profile継承機構だけを利用しています。
- 保留: `別紙1` / `別紙2` は今後の個別adapterや別紙構造化の参考としてRUNに記録し、今回の共通処理には入れていません。

## 検証

- CSV専用テスト: `3 passed`
- 関連回帰テスト: `21 passed`
- 実データbundle: 成功、qualitycheck warningなし
- `goal_check --mode normal`: `PASS`
- `special_structure_audit --mode normal`: `pass`

<!-- PR_BODY_FILE: runs/20260525-134750168_feat-csv-guideline-parser-v1/PR.md -->
