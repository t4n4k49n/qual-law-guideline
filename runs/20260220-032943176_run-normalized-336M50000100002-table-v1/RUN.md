# RUN: 20260220-032943176_run-normalized-336M50000100002-table-v1

- branch: run/normalized-336M50000100002-table-v1
- doc_id: jp_egov_336M50000100002_20260501_507M60000100117
- source_url: https://laws.e-gov.go.jp/law/336M50000100002/20260501_507M60000100117
- input: %USERPROFILE%/Documents/GitHub/qual-law-guideline_OLD-HANDMADE/data/xml/336M50000100002_20260501_507M60000100117/336M50000100002_20260501_507M60000100117.xml

## 実行
- 実行コマンド:
  - `.venv\Scripts\python.exe -m qai_xml2ir.cli --input %USERPROFILE%/Documents/GitHub/qual-law-guideline_OLD-HANDMADE/data/xml/336M50000100002_20260501_507M60000100117/336M50000100002_20260501_507M60000100117.xml --out-dir out/20260220-032943176_run-normalized-336M50000100002-table-v1 --doc-id jp_egov_336M50000100002_20260501_507M60000100117 --retrieved-at 2026-02-20 --source-url https://laws.e-gov.go.jp/law/336M50000100002/20260501_507M60000100117 --emit-only all`
- 注記:
  - `python -m qai_xml2ir.cli bundle ...` はサブコマンド形式エラーになるため不採用。

## 出力
- `out/20260220-032943176_run-normalized-336M50000100002-table-v1/jp_egov_336M50000100002_20260501_507M60000100117.regdoc_ir.yaml`
- `out/20260220-032943176_run-normalized-336M50000100002-table-v1/jp_egov_336M50000100002_20260501_507M60000100117.parser_profile.yaml`
- `out/20260220-032943176_run-normalized-336M50000100002-table-v1/jp_egov_336M50000100002_20260501_507M60000100117.regdoc_profile.yaml`
- `out/20260220-032943176_run-normalized-336M50000100002-table-v1/jp_egov_336M50000100002_20260501_507M60000100117.meta.yaml`
- `out/20260220-032943176_run-normalized-336M50000100002-table-v1/manifest.yaml`

## 検証
- `verify_document`: passed
- table構造の確認:
  - `schema: qai.regdoc_ir.v3`
  - `kind: table` あり
  - `kind: table_header` あり
  - `kind: table_row` あり
- regdoc_profile確認:
  - `selectable_kinds` に `table_row` を含む
  - `group_under_kind: table` を含む
  - `include_descendants_kinds: [note]` を含む

## AIレビュー（目視代替）
- 対象NID: `appdx_table1.tbl1.tblh.tblr1`
- 祖先経路: `document -> appendix(別表) -> table(別表) -> table_header(標識 | 大きさ | 標識を付ける箇所) -> table_row(...)`
- 判定: 表行選択時に祖先としてタイトル/ヘッダを辿れる構造であり、要件に整合。最終目視はPRで実施する前提。

## 正式版昇格
- まだ実施していない（PR承認後に実施）。
- PR: https://github.com/t4n4k49n/qual-law-guideline/pull/90
