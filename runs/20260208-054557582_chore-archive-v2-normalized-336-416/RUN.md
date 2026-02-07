# RUN

- run_id: `20260208-054557582_chore-archive-v2-normalized-336-416`
- branch: `chore/archive-v2-normalized-336-416`
- task: `v2で生成したnormalized成果(336/416)をARCHIVE_へ移動`

## 実施内容

- 以下2ディレクトリを `data/normalized/ARCHIVE_...` へ移動
  - `jp_egov_336M50000100002_20260501_507M60000100117`
  - `jp_egov_416M60000100179_20260501_507M60000100117`
- 既存の `ARCHIVE_...` と名称衝突したため、連番ルールで `_2` を付与
  - `ARCHIVE_jp_egov_336M50000100002_20260501_507M60000100117_2`
  - `ARCHIVE_jp_egov_416M60000100179_20260501_507M60000100117_2`

## 理由

- 現行は `ord=int` の `qai.regdoc_ir.v3` が正とし、旧方針での成果を明示的に退避するため。
