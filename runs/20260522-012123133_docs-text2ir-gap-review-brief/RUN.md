# RUN: 20260522-012123133_docs-text2ir-gap-review-brief

## 目的
- text2ir系文書を、xml2ir最終正規化レベルへ近づけるための外部レビュー用ブリーフを作成する。
- 現時点の事実と推定を分け、ピックアップすべき文書リストと進め方を整理する。

## ブランチ
- `docs/text2ir-gap-review-brief`

## 実施内容
- `README.md` / `local_notes/TODO.md` を確認。
- 既存RUN、`data/human-readable/`、`out/`、`src/qai_text2ir/profiles/` の状況を前提に整理。
- 外部レビュー用文書を追加。

## 成果物
- `runs/20260522-012123133_docs-text2ir-gap-review-brief/EXTERNAL_REVIEW_BRIEF.md`

## 検証
- 文書作成のみ。コード実行・正規化再生成・テスト実行は未実施。

## 補足
- 本RUNでは `data/normalized/` への昇格や、profile/text2irの変更は行っていない。
- 次段は「GOALチェックリスト」を作り、各最終profileで再生成してギャップ表を作る評価RUN。
