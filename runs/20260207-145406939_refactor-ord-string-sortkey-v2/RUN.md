# RUN

- run_id: `20260207-145406939_refactor-ord-string-sortkey-v2`
- branch: `refactor/ord-string-sortkey-v2`
- objective: `ord` を順序キーとして一本化し、`nid/num/ord` の役割分離を明確化する

## Changes

- `qai.regdoc_ir.v2` にスキーマを更新（`ord: Optional[str]`）
- `ord_key.py` を追加し、6桁セグメント連結 + 終端 `000000` の `ord` を実装
- parser 全体で `parent_ord` を伝播し、全ノード（root除く）に文字列 `ord` を付与
- Article の `Num` をフルセグメント（例: `29_2_2`）で `ord` 化
- Subitem1 は `IROHA_ORDER` で順序値を付与（slug依存を排除）
- `verify.py` に `ord` 形式チェックと sibling 昇順チェックを追加
- テストとドキュメントを v2 仕様に追随

## Verification

- `python -m pytest -q`
- result: `6 passed, 1 skipped`
