# RUN: 20260220-044119007_run-normalized-336M50000100001-table-v1

- branch: run/normalized-336M50000100001-table-v1
- doc_id: jp_egov_336M50000100001_20260501_507M60000100117
- source_url: https://laws.e-gov.go.jp/law/336M50000100001/20260501_507M60000100117
- input: %USERPROFILE%/Documents/GitHub/qual-law-guideline_OLD-HANDMADE/data/xml/336M50000100001_20260501_507M60000100117/336M50000100001_20260501_507M60000100117.xml

## 実行
- 実行コマンド:
  - .venv\Scripts\python.exe -m qai_xml2ir.cli --input %USERPROFILE%/Documents/GitHub/qual-law-guideline_OLD-HANDMADE/data/xml/336M50000100001_20260501_507M60000100117/336M50000100001_20260501_507M60000100117.xml --out-dir out/20260220-044119007_run-normalized-336M50000100001-table-v1 --doc-id jp_egov_336M50000100001_20260501_507M60000100117 --retrieved-at 2026-02-20 --source-url https://laws.e-gov.go.jp/law/336M50000100001/20260501_507M60000100117 --emit-only all

## 出力
- $out_dir/jp_egov_336M50000100001_20260501_507M60000100117.regdoc_ir.yaml
- $out_dir/jp_egov_336M50000100001_20260501_507M60000100117.parser_profile.yaml
- $out_dir/jp_egov_336M50000100001_20260501_507M60000100117.regdoc_profile.yaml
- $out_dir/jp_egov_336M50000100001_20260501_507M60000100117.meta.yaml
- $out_dir/manifest.yaml

## 検証
- erify_document: passed
- table構造の確認:
  - schema: qai.regdoc_ir.v3
  - kind: table 26件
  - kind: table_header 26件
  - kind: table_row 681件
- regdoc_profile確認（dq_gmp_checklist）:
  - selectable_kinds に 	able_row を含む
  - grouping_policy に when_kind: table_row / group_under_kind: table を含む
  - context_display_policy の 	able_row で include_descendants_kinds: [note] を含む

## AIレビュー（目視代替）
- 対象NID: rt37.p2.tbl1.tblh.tblr1
- 祖先経路: document -> chapter(第二章) -> article(第三十七条) -> paragraph(2) -> table -> table_header -> table_row
- ヘッダ本文: 第二十七条 | 医薬品、医薬部外品又は化粧品の製造業の許可証 | 医薬品等外国製造業者の認定証
- 行本文（要約）: 様式第十三 | 様式第十九
- 判定: 表行が 	able_header 配下に格納され、条文祖先を含む文脈表示に利用できる構造であることを確認。最終目視はPRで実施する前提。

## 正式版昇格
- まだ実施していない（PR承認後に実施）。
- PR: https://github.com/t4n4k49n/qual-law-guideline/pull/95
