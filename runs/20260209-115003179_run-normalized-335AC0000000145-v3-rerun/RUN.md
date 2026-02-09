# RUN

- run_id: 20260209-115003179_run-normalized-335AC0000000145-v3-rerun
- branch: run/normalized-335AC0000000145-v3-rerun
- input: %USERPROFILE%\\Documents\\GitHub\\qual-law-guideline_OLD-HANDMADE\\data\\xml\\335AC0000000145_20260501_507AC0000000037\\335AC0000000145_20260501_507AC0000000037.xml
- doc_id: jp_egov_335AC0000000145_20260501_507AC0000000037

## 実行コマンド

`python -m qai_xml2ir.cli --input <xml> --out-dir out/20260209-115003179_run-normalized-335AC0000000145-v3-rerun --doc-id jp_egov_335AC0000000145_20260501_507AC0000000037 --retrieved-at 2026-02-09 --source-url https://laws.e-gov.go.jp/law/335AC0000000145/20260501_507AC0000000037 --emit-only all`

## 出力

- `out/20260209-115003179_run-normalized-335AC0000000145-v3-rerun/jp_egov_335AC0000000145_20260501_507AC0000000037.regdoc_ir.yaml`
- `out/20260209-115003179_run-normalized-335AC0000000145-v3-rerun/jp_egov_335AC0000000145_20260501_507AC0000000037.parser_profile.yaml`
- `out/20260209-115003179_run-normalized-335AC0000000145-v3-rerun/jp_egov_335AC0000000145_20260501_507AC0000000037.regdoc_profile.yaml`
- `out/20260209-115003179_run-normalized-335AC0000000145-v3-rerun/jp_egov_335AC0000000145_20260501_507AC0000000037.meta.yaml`
- `out/20260209-115003179_run-normalized-335AC0000000145-v3-rerun/manifest.yaml`

## 検証結果（verify）

- schema: `qai.regdoc_ir.v3`
- doc_id: `jp_egov_335AC0000000145_20260501_507AC0000000037`
- `assert_unique_nids`: OK
- `check_annex_article_nids`: OK
- `check_appendix_scoped_indices`: OK
- `check_ord_format_and_order`: OK

## AIレビュー（目視代替）

- 最深サンプル: `art29_2.p1.i2.ro`
- 人間可読経路: `第七章 > 第一節 > 第二十九条の二 > 1 > 二 > ロ`
- YAML経路: `root > ch7 > ch7.sec1 > art29_2 > art29_2.p1 > art29_2.p1.i2 > art29_2.p1.i2.ro`
- ノード本文: `一般用医薬品`
- 所見: 祖先経路の段数が一致し、階層対応に破綻なし
- 注記: 最終的な人間レビューはPRで実施する前提

## 正式版への昇格

- ルールにより、`data/normalized/jp_egov_335AC0000000145_20260501_507AC0000000037/` への複写はPR承認確認後に実施
