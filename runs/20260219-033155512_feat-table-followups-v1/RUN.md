# RUN: 20260219-033155512_feat-table-followups-v1

## 目的
- 実データ由来 Markdown 表 fixture から `text2ir` の4ファイル出力を実行し、表構造が `regdoc_ir` に反映されることを確認する。

## 入力
- `tests/fixtures/markdown_table_real_excerpt.md`
- parser profile:
  - `src/qai_text2ir/profiles/markdown_table_test_v1.yaml`

## 実行コマンド
- `PYTHONPATH=src python -m qai_text2ir.cli --input tests/fixtures/markdown_table_real_excerpt.md --out-dir out/20260219-033155512_feat-table-followups-v1 --doc-id markdown_table_real_excerpt_v1 --title "Markdown Table Real Excerpt" --short-title "MD Table Real" --jurisdiction INTL --family TEST --language en --doc-type guideline --source-url "https://example.local/markdown-table-real-excerpt" --source-format txt --retrieved-at "2026-02-19" --parser-profile src/qai_text2ir/profiles/markdown_table_test_v1.yaml --qualitycheck --strict --write-manifest --emit-only all`

## 出力
- `out/20260219-033155512_feat-table-followups-v1/markdown_table_real_excerpt_v1.regdoc_ir.yaml`
- `out/20260219-033155512_feat-table-followups-v1/markdown_table_real_excerpt_v1.parser_profile.yaml`
- `out/20260219-033155512_feat-table-followups-v1/markdown_table_real_excerpt_v1.regdoc_profile.yaml`
- `out/20260219-033155512_feat-table-followups-v1/markdown_table_real_excerpt_v1.meta.yaml`
- `out/20260219-033155512_feat-table-followups-v1/manifest.yaml`

## 確認結果
- `qualitycheck --strict`: warning 0（成功）
- `regdoc_ir` で以下を確認:
  - `table` ノード生成
  - `table_header` 配下に `table_row` が複数生成
  - `table` 配下に `note`（注1/注2）生成
  - table heading: `表１ 清浄区域の分類`

## 追加仕様（表に関する追加仕様.txt）との照合
1. 表レコードを選択可能にする（md書式）
- 充足。`table_row` が IR ノードとして生成され、`regdoc_profile` の `selectable_kinds` に含まれる。

2. 表タイトル・ヘッダ（th相当）を親/先祖として同時表示可能にする
- 充足。`table.heading`（タイトル）と `table_header` が生成され、`table_row` 選択時の文脈解決で祖先側に含められる。

3. 表下注記（子・子孫）を同時表示可能にする。加えて条文側にも子孫表示を適用可能にする
- 充足。表直後の注記が `note` として `table` 配下に生成される。
- 併せて、`include_descendants*` 設定により条文系（subitem/item/paragraph/statement）でも note 子孫表示が可能。

## 備考
- 本runは fixture 入力に対する4ファイル出力検証であり、source URL はダミー（`example.local`）を使用。
