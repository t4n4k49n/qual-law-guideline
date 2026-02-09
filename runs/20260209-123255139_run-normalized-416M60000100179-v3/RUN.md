# RUN

- run_id: 20260209-123255139_run-normalized-416M60000100179-v3
- branch: run/normalized-416M60000100179-v3
- input: %USERPROFILE%\\Documents\\GitHub\\qual-law-guideline_OLD-HANDMADE\\data\\xml\\416M60000100179_20260501_507M60000100117\\416M60000100179_20260501_507M60000100117.xml
- doc_id: jp_egov_416M60000100179_20260501_507M60000100117

## 実行コマンド

`python -m qai_xml2ir.cli --input <xml> --out-dir out/20260209-123255139_run-normalized-416M60000100179-v3 --doc-id jp_egov_416M60000100179_20260501_507M60000100117 --retrieved-at 2026-02-09 --source-url https://laws.e-gov.go.jp/law/416M60000100179/20260501_507M60000100117 --emit-only all`

## 出力

- `out/20260209-123255139_run-normalized-416M60000100179-v3/jp_egov_416M60000100179_20260501_507M60000100117.regdoc_ir.yaml`
- `out/20260209-123255139_run-normalized-416M60000100179-v3/jp_egov_416M60000100179_20260501_507M60000100117.parser_profile.yaml`
- `out/20260209-123255139_run-normalized-416M60000100179-v3/jp_egov_416M60000100179_20260501_507M60000100117.regdoc_profile.yaml`
- `out/20260209-123255139_run-normalized-416M60000100179-v3/jp_egov_416M60000100179_20260501_507M60000100117.meta.yaml`
- `out/20260209-123255139_run-normalized-416M60000100179-v3/manifest.yaml`

## 検証結果（verify）

- schema: `qai.regdoc_ir.v3`
- doc_id: `jp_egov_416M60000100179_20260501_507M60000100117`
- `assert_unique_nids`: OK
- `check_annex_article_nids`: OK
- `check_appendix_scoped_indices`: OK
- `check_ord_format_and_order`: OK

## AIレビュー（目視代替）

- 最深サンプル: `art27.p1.i9.ni`
- 人間可読経路: `第二章 > 第四節 > 第二十七条 > 1 > 九 > ニ`
- YAML経路: `root > ch2 > ch2.sec4 > art27 > art27.p1 > art27.p1.i9 > art27.p1.i9.ni`
- ノード本文: `継代培養の状況`
- 所見: 祖先経路の段数が一致し、階層対応に破綻なし
- 注記: 最終的な人間レビューはPRで実施する前提

## 正式版への昇格

- PR承認確認後に昇格を実施（2026-02-09）
- `data/normalized/jp_egov_416M60000100179_20260501_507M60000100117/` を作成し、4ファイルをコピー
- コピー元: `out/20260209-123255139_run-normalized-416M60000100179-v3/`
- 既存の同名正式版は存在しないため、ARCHIVE退避は未実施
- 参考: 承認前複写の取り消し退避先 `out/20260209-123255139_run-normalized-416M60000100179-v3/pre_approval_copy/jp_egov_416M60000100179_20260501_507M60000100117/`
