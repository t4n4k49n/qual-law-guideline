## まとめ

無菌操作法指針向けのParser開発として、専用 `text2ir` profile とテストを追加しました。正式な正規化処理や `data/normalized/` への昇格ではなく、本文・参考情報の階層を安定して解析できるところまでを確認しています。

## 変更内容

- `jp_pmda_aseptic_processing_guideline_v1` profileを追加
- 冒頭通知、作成者一覧、目次を本文開始前として除外
- `Ａ１` / `A1.1` 系の参考情報を共通 `JP_GUIDELINE` profileへ追加
- 全角英字を番号正規化で半角化
- 共通profileから文書固有のタイトル・機関名除去を外し、必要な文書名除去は専用profile側へ移動
- 実データに基づくテストを追加

## 検証

- `pytest`: `43 passed`
- 実データbundle: 成功
- `goal_check --mode normal`: `PASS`
- `special_structure_audit --mode normal`: `warn`

## 残課題

固定幅表候補が3件残っています。今回のPRでは共通parserへ個別の表処理を入れず、次の個別table adapter検討材料として記録しています。

<!-- PR_BODY_FILE: runs/20260525-133209443_feat-aseptic-processing-parser-v1/PR.md -->
