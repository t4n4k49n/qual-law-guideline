## 概要

承認済み正規化RUNの昇格手続き漏れを是正するPRです。  
`data/normalized` への反映が未完了だった 2件（336 / 416）を正式に配置しました。

## 対象

- `data/normalized/jp_egov_336M50000100002_20260501_507M60000100117/`
- `data/normalized/jp_egov_416M60000100179_20260501_507M60000100117/`

## 変更内容

- 336:
  - 既にローカルへ昇格済みだったが未追跡だったため、版管理に追加
- 416:
  - 承認済みRUN出力 `out/20260208-020202287_run-normalized-416M60000100179-v2/` から4ファイルを昇格コピー

## 確認

- 両doc_idとも以下4ファイルが存在
  - `*.regdoc_ir.yaml`
  - `*.parser_profile.yaml`
  - `*.regdoc_profile.yaml`
  - `*.meta.yaml`
- `regdoc_ir.yaml` の `schema` は両方 `qai.regdoc_ir.v2`

## 再発防止メモ

- 正規化RUN承認後の昇格コピー完了を、`git status` で未追跡有無まで確認する運用にする。
- `AGENTS.md` に「正規化RUNは必ず 7) 正式版への昇格（文書コミット）まで実施」と明記し、完了条件を固定した。
