# RUN

- run_id: 20260209-141050252_run-normalized-336M50000100001-v3
- branch: run/normalized-336M50000100001-v3
- input: %USERPROFILE%\\Documents\\GitHub\\qual-law-guideline_OLD-HANDMADE\\data\\xml\\336M50000100001_20260501_507M60000100117\\336M50000100001_20260501_507M60000100117.xml
- doc_id: jp_egov_336M50000100001_20260501_507M60000100117

## 実行コマンド

`python -m qai_xml2ir.cli --input <xml> --out-dir out/20260209-141050252_run-normalized-336M50000100001-v3 --doc-id jp_egov_336M50000100001_20260501_507M60000100117 --retrieved-at 2026-02-09 --source-url https://laws.e-gov.go.jp/law/336M50000100001/20260501_507M60000100117 --emit-only all`

## 出力

- `out/20260209-141050252_run-normalized-336M50000100001-v3/jp_egov_336M50000100001_20260501_507M60000100117.regdoc_ir.yaml`
- `out/20260209-141050252_run-normalized-336M50000100001-v3/jp_egov_336M50000100001_20260501_507M60000100117.parser_profile.yaml`
- `out/20260209-141050252_run-normalized-336M50000100001-v3/jp_egov_336M50000100001_20260501_507M60000100117.regdoc_profile.yaml`
- `out/20260209-141050252_run-normalized-336M50000100001-v3/jp_egov_336M50000100001_20260501_507M60000100117.meta.yaml`
- `out/20260209-141050252_run-normalized-336M50000100001-v3/manifest.yaml`

## 検証結果（verify）

- schema: `qai.regdoc_ir.v3`
- doc_id: `jp_egov_336M50000100001_20260501_507M60000100117`
- `assert_unique_nids`: OK
- `check_annex_article_nids`: OK
- `check_appendix_scoped_indices`: OK
- `check_ord_format_and_order`: OK

## AIレビュー（目視代替）

- 最深サンプル: `art228_20.p1.i1.ha.pt1`
- 人間可読経路: `第九章 > 第二百二十八条の二十 > 1 > 一 > ハ > （１）`
- YAML経路: `root > ch9 > art228_20 > art228_20.p1 > art228_20.p1.i1 > art228_20.p1.i1.ha > art228_20.p1.i1.ha.pt1`
- ノード本文: `障害`
- 所見: 祖先経路の段数が一致し、階層対応に破綻なし
- 注記: 最終的な人間レビューはPRで実施する前提

## 正式版への昇格

- 未実施（PR承認確認後に実施予定）
- 実施時は `data/normalized/jp_egov_336M50000100001_20260501_507M60000100117/` へ4ファイルをコピーし、結果を本RUN.mdに追記する
