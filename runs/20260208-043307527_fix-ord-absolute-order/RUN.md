# RUN

- run_id: `20260208-043307527_fix-ord-absolute-order`
- branch: `fix/ord-absolute-order`
- task: `ordを文書内絶対順序（出現順）へ一本化し、Num解釈依存を除去`

## 変更概要

- `ord` をツリー構築後の document order（DFS pre-order）連番へ変更
- `ord` 形式を 8 桁ゼロ埋め文字列に統一（root除く全ノード）
- 旧仕様の多段セグメント（`000001.000000...`）を廃止
- `bundle` 実行時に verify を必須化
- IR schema を `qai.regdoc_ir.v3` へ更新

## 実装ポイント

- `src/qai_xml2ir/ord_key.py`
  - `ORD_WIDTH=8`
  - `assign_document_order(root)` を追加
- `src/qai_xml2ir/egov_parser.py`
  - 解析中の `build_ord(...)` を使った ord 付与を停止
  - `build_root(children)` 後に `assign_document_order(root_node)` を実行
- `src/qai_xml2ir/verify.py`
  - ord チェックを強化
    - root除く全ノードで ord 必須
    - `^[0-9]{8}$` 形式
    - 一意
    - walk順で厳密増加
    - 同一親 children の昇順
- `src/qai_xml2ir/cli.py`
  - bundle 内で verify を実行し、NGなら終了

## テスト

- `python -m pytest -q`
- 結果: `10 passed, 1 skipped`

## 再生成（3件）

入力XML（%USERPROFILE%表記）:
- `%USERPROFILE%\Documents\GitHub\qual-law-guideline_OLD-HANDMADE\data\xml\336M50000100002_20260501_507M60000100117\336M50000100002_20260501_507M60000100117.xml`
- `%USERPROFILE%\Documents\GitHub\qual-law-guideline_OLD-HANDMADE\data\xml\416M60000100179_20260501_507M60000100117\416M60000100179_20260501_507M60000100117.xml`
- `%USERPROFILE%\Documents\GitHub\qual-law-guideline_OLD-HANDMADE\data\xml\335AC0000000145_20260501_507AC0000000037\335AC0000000145_20260501_507AC0000000037.xml`

出力先:
- `out/20260208-043307527_fix-ord-absolute-order/`

normalized更新:
- `data/normalized/jp_egov_336M50000100002_20260501_507M60000100117/`
- `data/normalized/jp_egov_416M60000100179_20260501_507M60000100117/`
- `data/normalized/jp_egov_335AC0000000145_20260501_507AC0000000037/`（新規）

## verify結果（再生成3件）

- `jp_egov_336M50000100002_20260501_507M60000100117`: annex=0 / appendix=0 / ord=0
- `jp_egov_416M60000100179_20260501_507M60000100117`: annex=0 / appendix=0 / ord=0
- `jp_egov_335AC0000000145_20260501_507AC0000000037`: annex=0 / appendix=0 / ord=0

## 問題解消確認（Num="15:16" / Num="1:2"）

335ACの再生成結果（ord昇順）:
- `ch4`: `art1516`（第十五条及び第十六条, `00000351`）が `art17`（第十七条, `00000352`）より前
- `annex38.art1`: `annex38.art1.i12`（一及び二, `00002279`）が `annex38.art1.i3`（三, `00002280`）より前
- `annex40.art1`: `annex40.art1.i12`（一及び二, `00002290`）が `annex40.art1.i3`（三, `00002291`）より前

## 判定

- ord の絶対順序化と verify 強化を反映
- Num解釈由来の順序破綻（`15:16` / `1:2`）が再発しないことを確認
