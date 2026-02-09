# RUN

- run_id: 20260209-125137789_run-normalized-336CO0000000011-v3
- branch: run/normalized-336CO0000000011-v3
- input: $env:USERPROFILE\Documents\\GitHub\\qual-law-guideline_OLD-HANDMADE\\data\\xml\\336CO0000000011_20260501_507CO0000000362\\336CO0000000011_20260501_507CO0000000362.xml
- doc_id: jp_egov_336CO0000000011_20260501_507CO0000000362

## 実行コマンド

`python -m qai_xml2ir.cli --input <xml> --out-dir out/20260209-125137789_run-normalized-336CO0000000011-v3 --doc-id jp_egov_336CO0000000011_20260501_507CO0000000362 --retrieved-at 2026-02-09 --source-url https://laws.e-gov.go.jp/law/336CO0000000011/20260501_507CO0000000362 --emit-only all`

## 出力

- `out/20260209-125137789_run-normalized-336CO0000000011-v3/jp_egov_336CO0000000011_20260501_507CO0000000362.regdoc_ir.yaml`
- `out/20260209-125137789_run-normalized-336CO0000000011-v3/jp_egov_336CO0000000011_20260501_507CO0000000362.parser_profile.yaml`
- `out/20260209-125137789_run-normalized-336CO0000000011-v3/jp_egov_336CO0000000011_20260501_507CO0000000362.regdoc_profile.yaml`
- `out/20260209-125137789_run-normalized-336CO0000000011-v3/jp_egov_336CO0000000011_20260501_507CO0000000362.meta.yaml`
- `out/20260209-125137789_run-normalized-336CO0000000011-v3/manifest.yaml`

## 検証結果（verify）

- schema: `qai.regdoc_ir.v3`
- doc_id: `jp_egov_336CO0000000011_20260501_507CO0000000362`
- `assert_unique_nids`: OK
- `check_annex_article_nids`: OK
- `check_appendix_scoped_indices`: OK
- `check_ord_format_and_order`: OK

## AIレビュー（目視代替）

- 最深サンプル: `art80.p2.i3.i`
- 人間可読経路: `第十五章 > 第八十条 > ２ > 三 > イ`
- YAML経路: `root > ch15 > art80 > art80.p2 > art80.p2.i3 > art80.p2.i3.i`
- ノード本文: `生物学的製剤`
- 所見: 祖先経路の段数が一致し、階層対応に破綻なし
- 注記: 最終的な人間レビューはPRで実施する前提

## 正式版への昇格

- PR承認確認後に昇格を実施（2026-02-09）
- `data/normalized/jp_egov_336CO0000000011_20260501_507CO0000000362/` を作成し、4ファイルをコピー
- コピー元: `out/20260209-125137789_run-normalized-336CO0000000011-v3/`
- 既存の同名正式版は存在しないため、ARCHIVE退避は未実施
