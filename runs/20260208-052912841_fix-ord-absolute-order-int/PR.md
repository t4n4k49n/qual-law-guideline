## 概要

ord を「文書内の絶対順序（int）」へ一本化しました。Numの意味解釈で順序を作る方式を廃止し、`Num="15:16"` / `Num="1:2"` のような並列表現でもソース順を壊さない設計に変更しています。

## Breaking Change

- IR schema: `qai.regdoc_ir.v2` -> `qai.regdoc_ir.v3`
- `ord` の型: `Optional[str]` -> `Optional[int]`
- `ord` の意味: 階層パス文字列 -> 文書内絶対順序（preorder連番）

## 変更内容

1. ord付与方式の変更
- parser 各所での `build_ord(...)` 依存を除去
- ツリー構築後に `assign_document_order(root)` を1回実行
- rootを除く全ノードに `1..N` を付与

2. verify強化
- root除く全ノードで ord が int であること
- ord が一意であること
- preorder走査で ord が厳密増加すること
- 同一親 children が ord 昇順であること

3. 実行時検証
- `bundle` 内で verify を必須実行（失敗時は CLI エラー）

4. docs更新
- `nid=構造ID` / `num=表示` / `ord=順序` の責務分離を明記
- ord は Num を解釈しない旨を追記

## 変更ファイル

- `src/qai_xml2ir/models_ir.py`
- `src/qai_xml2ir/models_meta.py`
- `src/qai_xml2ir/egov_parser.py`
- `src/qai_xml2ir/ord_key.py`
- `src/qai_xml2ir/verify.py`
- `src/qai_xml2ir/cli.py`
- `tests/test_ord_key.py`
- `tests/test_ir_structure.py`
- `tests/test_bundle_gmp.py`
- `docs/IR_EGOV_MAPPING.md`
- `docs/REFERENCE.md`
- `docs/NORMALIZED_RUN_PLAYBOOK.md`
- `docs/NORMALIZED_RELEASE_CHECKLIST.md`

## テスト

- `python -m pytest -q`
- 結果: `10 passed, 1 skipped`

## 335AC 実XML確認（順序逆転の解消）

入力:
- `%USERPROFILE%\Documents\GitHub\qual-law-guideline_OLD-HANDMADE\data\xml\335AC0000000145_20260501_507AC0000000037\335AC0000000145_20260501_507AC0000000037.xml`

確認結果:
- `ch4`: `art1516`（ord=351） < `art17`（ord=352）
- `annex38.art1`: `annex38.art1.i12`（ord=2279） < `annex38.art1.i3`（ord=2280）
- `annex40.art1`: `annex40.art1.i12`（ord=2290） < `annex40.art1.i3`（ord=2291）

`Num="15:16"` / `Num="1:2"` が存在しても、ord は Num を解釈しないためソース順を維持します。
