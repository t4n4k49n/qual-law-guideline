# RUN

- run_id: `20260208-052912841_fix-ord-absolute-order-int`
- branch: `fix/ord-absolute-order-int`
- task: `ordを文書内絶対順序（int）へ一本化`

## 変更概要

- Node.ord を `Optional[int]` に統一（root以外は連番）
- ord は parser 各所で計算せず、ツリー構築後に preorder 1回走査で付与
- Num（`15` / `15_2` / `15:16` / `1:2` 等）を ord 計算に使用しない
- IR schema を `qai.regdoc_ir.v3` へ更新
- verify を強化（ord存在/型/一意/単調増加/同一親昇順）
- bundle 実行時に verify を必須実行

## テスト

- `python -m pytest -q`
- 結果: `10 passed, 1 skipped`

## 実XML確認（335AC）

- 入力: `%USERPROFILE%\Documents\GitHub\qual-law-guideline_OLD-HANDMADE\data\xml\335AC0000000145_20260501_507AC0000000037\335AC0000000145_20260501_507AC0000000037.xml`
- コマンド: `python -m qai_xml2ir.cli --input <xml> --out-dir out/20260208-052912841_fix-ord-absolute-order-int --doc-id jp_egov_335AC0000000145_20260501_507AC0000000037 --retrieved-at 2026-02-08 --source-url https://laws.e-gov.go.jp/law/335AC0000000145/20260501_507AC0000000037 --emit-only all`
- 出力schema: `qai.regdoc_ir.v3`
- verify: `ord_problems=0`

確認抜粋:
- `ch4`: `art1516`（ord=351） < `art17`（ord=352）
- `annex38.art1`: `annex38.art1.i12`（ord=2279） < `annex38.art1.i3`（ord=2280）
- `annex40.art1`: `annex40.art1.i12`（ord=2290） < `annex40.art1.i3`（ord=2291）

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
