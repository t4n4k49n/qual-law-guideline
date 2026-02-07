## 概要

`ord` を「文書内の絶対順序（出現順）」へ一本化しました。Numの意味解釈で `ord` を作る方式を廃止し、`Num="15:16"` や `Num="1:2"` を含むデータでも順序破綻しないようにしています。

## Breaking Change

- IR schema: `qai.regdoc_ir.v2` -> `qai.regdoc_ir.v3`
- `ord` 仕様変更:
  - 旧: 多段セグメント（例: `000029.000002.000000...`）
  - 新: 8桁ゼロ埋め連番（例: `00000001`）
- `ord` は順序専用キー（ID用途は `nid`）

## 実装内容

- `src/qai_xml2ir/ord_key.py`
  - `ORD_WIDTH=8`
  - `assign_document_order(root)` を追加（DFS pre-orderで root除外連番）
- `src/qai_xml2ir/egov_parser.py`
  - 解析中の `build_ord(...)` 依存を停止
  - ツリー構築後に `assign_document_order(root_node)` を実行
- `src/qai_xml2ir/verify.py`
  - ord検証を強化
    - ord必須（root除く）
    - 形式 `^[0-9]{8}$`
    - 一意
    - walk順で厳密増加
    - 同一親の children 昇順
- `src/qai_xml2ir/cli.py`
  - `bundle` 実行時に verify を必須実行（失敗時は終了）

## ドキュメント更新

- `docs/IR_EGOV_MAPPING.md`
- `docs/REFERENCE.md`
- `docs/NORMALIZED_RUN_PLAYBOOK.md`
- `docs/NORMALIZED_RELEASE_CHECKLIST.md`

## テスト

- `python -m pytest -q`
- 結果: `10 passed, 1 skipped`

## 再生成・normalized反映（3件）

- `jp_egov_336M50000100002_20260501_507M60000100117`
- `jp_egov_416M60000100179_20260501_507M60000100117`
- `jp_egov_335AC0000000145_20260501_507AC0000000037`（新規昇格）

## `15:16` / `1:2` 問題の解消確認

335AC 再生成の ord 昇順確認:
- `ch4`: `art1516`（`00000351`） < `art17`（`00000352`）
- `annex38.art1`: `annex38.art1.i12`（`00002279`） < `annex38.art1.i3`（`00002280`）
- `annex40.art1`: `annex40.art1.i12`（`00002290`） < `annex40.art1.i3`（`00002291`）

Num値:
```text
Num="15:16"
Num="1:2"
```
これらを ord 計算に使わないため、Num解釈起因の逆転は発生しません。

## マイグレーション注意

- `ord` の既存前提（多段セグメント解析）は破棄してください
- ソートは `ord` の昇順のみを使用
- ID/参照用途は `nid` を使用
