## 概要

`data/normalized` 配下の v1 時代成果物 2件を、現行 v2 成果物と明確に分離するため `ARCHIVE_` プレフィックス付きディレクトリへ移動しました。

## 変更内容

- ディレクトリ名変更（`git mv`）
  - `data/normalized/jp_egov_336M50000100002_20260501_507M60000100117`
  - -> `data/normalized/ARCHIVE_jp_egov_336M50000100002_20260501_507M60000100117`
  - `data/normalized/jp_egov_416M60000100179_20260501_507M60000100117`
  - -> `data/normalized/ARCHIVE_jp_egov_416M60000100179_20260501_507M60000100117`

## 理由

- 2件はいずれも `qai.regdoc_ir.v1` 出力であり、現行の `qai.regdoc_ir.v2` 運用対象と混在させないため。
