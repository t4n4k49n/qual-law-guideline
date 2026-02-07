## 概要

正規化RUNのPR本文に、対象e-Gov法令URLを必ず記載する運用ルールを追加しました。

## 変更内容

- `docs/NORMALIZED_RUN_PLAYBOOK.md`
  - `6) PR作成` に以下を追加
    - e-Gov法令URLの必須記載
    - URL形式: `https://laws.e-gov.go.jp/law/<law_id>/<as_of_revision>`
    - 変換例: `416M60000100179_20260501_507M60000100117` → `https://laws.e-gov.go.jp/law/416M60000100179/20260501_507M60000100117`

## 期待効果

- 正規化RUNのPRから根拠法令へ即時遷移できる
- PR本文の記載品質を統一できる
