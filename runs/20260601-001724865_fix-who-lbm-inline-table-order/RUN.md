# WHO LBM inline table order fix

- run_id: `20260601-001724865_fix-who-lbm-inline-table-order`
- branch: `fix/who-lbm-inline-table-order`
- target: WHO Laboratory Biosafety Manual, 3rd ed.

## 背景

正規化候補 `20260531-234647542_run-normalized-who-lbm-3rd-v8` の目検で、表と表の間にある本文の順番が崩れていることを確認した。

代表例:

- Chapter 1 Introduction で、`Laboratory facilities are designated as basic ...` が Table 1 の後ではなく、section text 内で Table 1 より前に見える構造になっていた。
- 原文上は Table 1 の後に続く本文であり、Table 2 / Table 3 周辺にも同種の表間本文が存在する。

原因は、WHO LBM個別パーサが表ノードを対象sectionの末尾にappendしつつ、section.textには表前後の本文を1つに潰したまま残していたこと。

## 変更内容

- WHO LBM個別処理で、表ブロックを本文内の位置で検出し、対象ノードを次の順に分割するよう修正した。
  - 表前本文: 親ノードの `text`
  - 表: `table` child
  - 表後本文: `statement` child
- table / statement / item / figure の child 順を source line 順で挿入するヘルパを追加した。
- Table 1 / Table 2 / Table 3 の代表例について、表と表間本文の順序を回帰テスト化した。
- 共通パーサには触れていない。

## 検証

- `python -m pytest tests/test_who_lbm_general_tables.py -q`
  - `13 passed`
- `python -m pytest tests/test_who_lbm_general_tables.py tests/test_who_lbm_v4_skip_toc_and_annex_heading.py tests/test_who_lbm_v3_skip_blocks.py tests/test_who_lbm_v2_drop_toc_and_annex_dedupe.py tests/test_who_lbm_heading_merge.py tests/test_who_lbm_chap8_survey_parser.py tests/test_text2ir_who_lbm_3rd.py -q`
  - `32 passed`
- 補助生成: `out/20260601-001724865_fix-who-lbm-inline-table-order/who_lbm_check`
- `qai_text2ir.goal_check --mode promotion`
  - `PASS`
  - nodes: `2023`
  - source span coverage: `1.0`
  - warnings: `none`
- `qai_text2ir.special_structure_audit --mode promotion`
  - `pass`
  - source_tables: `18`
  - generated_tables: `18`
  - generated_rows: `1017`
  - generated_figures: `12`
  - unresolved_special_blocks: `0`
- `python tools/check_ir_structure.py out/20260601-001724865_fix-who-lbm-inline-table-order/who_lbm_check`
  - `[OK] no structure problems found`
- 全親ノードについて、`table` / `statement` / `item` / `subitem` / `figure` child の source line 順が逆転していないことを補助スクリプトで確認した。

## 確認観点

- `cha1.sec1.text` は Table 1 前の Introduction 本文で止まる。
- Table 1 の直後に `Laboratory facilities are designated as basic ...` の `statement` が来る。
- Table 2 の後、Table 3 の前に `The assignment of an agent ...` の `statement` が来る。
- 既存のA4-2/A5-1表復元は維持される。
