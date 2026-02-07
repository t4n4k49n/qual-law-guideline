# RUN

- run_id: `20260208-021821722_fix-normalized-promotion-gap`
- branch: `fix/normalized-promotion-gap`
- task: `承認済み正規化RUNの昇格漏れ（336/416）を是正`

## 背景

- 承認済みPR後に行うべき `data/normalized/<doc_id>/` への昇格コピーが2件で未完了だった。
  - `jp_egov_336M50000100002_20260501_507M60000100117` はローカル未追跡のまま
  - `jp_egov_416M60000100179_20260501_507M60000100117` は未配置

## 対応

- `data/normalized/jp_egov_336M50000100002_20260501_507M60000100117/` を正式に版管理へ追加
- `out/20260208-020202287_run-normalized-416M60000100179-v2/` から以下を昇格コピー
  - `jp_egov_416M60000100179_20260501_507M60000100117.regdoc_ir.yaml`
  - `jp_egov_416M60000100179_20260501_507M60000100117.parser_profile.yaml`
  - `jp_egov_416M60000100179_20260501_507M60000100117.regdoc_profile.yaml`
  - `jp_egov_416M60000100179_20260501_507M60000100117.meta.yaml`

## 結果

- 両doc_idの `data/normalized/<doc_id>/` 配下に4ファイルが存在
- 2件とも `regdoc_ir.yaml` の `schema` は `qai.regdoc_ir.v2`
