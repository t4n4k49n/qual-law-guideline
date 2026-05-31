# WHO LBM 3rd 項番なしheading修正

- run_id: `20260531-210228467_fix-who-lbm-unnumbered-headings`
- branch: `fix/who-lbm-unnumbered-headings`
- 対象: WHO Laboratory Biosafety Manual, 3rd ed.
- doc_id: `who_lbm_3rd_2004_9241546506`

## 目的

正規化RUN前チェックで、`Code of practice`、`Access`、`Personal protection` などの項番なし小見出しが章本文へ連結される問題を確認した。
正規化候補を作る前に、WHO専用profileでこれらを `section` として構造化し、配下の番号付き項目を見出し配下に保持する。

## 変更

- `who_lbm_3rd_default_v4` の `structural_kinds` に `section` を追加。
- WHO LBM 3rd の既知の項番なし小見出し行を `section` として認識するマーカーを追加。
- `part` / `chapter` / `annex` 直下に `section` を許可し、`section` 配下に `item` 等を許可。
- 章3の `Access` 配下に番号付き項目が入ることを回帰テスト化。
- table/figure正規化後処理が `section` 配下でも機能するように対象kindへ `section` を追加。
- `Figure 1` の固定幅表示が `Access` 本文に残らないようにstrip対象を追加。
- 見出し検出をcase-sensitiveにし、Annex 4の表セル内 `infectious materials` を誤って `section` 化しないようにした。

## 検証

```text
python -m pytest tests/test_text2ir_who_lbm_3rd.py tests/test_who_lbm_general_tables.py tests/test_who_lbm_chap8_survey_parser.py tests/test_who_lbm_heading_merge.py tests/test_who_lbm_v4_skip_toc_and_annex_heading.py -q
24 passed
```

```text
python -m qai_text2ir.cli bundle ... --strict --out-dir out/20260531-210228467_fix-who-lbm-unnumbered-headings/who_lbm_check_20260531-212500
success
```

```text
python -m qai_text2ir.goal_check --bundle-dir out/20260531-210228467_fix-who-lbm-unnumbered-headings/who_lbm_check_20260531-212500 --doc-id who_lbm_3rd_2004_9241546506 --mode promotion
PASS
Nodes: 1196
tables: 15
table_rows: 210
figures: 12
notes: 14
sections: 80
```

```text
python -m qai_text2ir.special_structure_audit --bundle-dir out/20260531-210228467_fix-who-lbm-unnumbered-headings/who_lbm_check_20260531-212500 --doc-id who_lbm_3rd_2004_9241546506 --mode promotion --format markdown
pass
source_tables: 18
generated_tables: 15
generated_rows: 210
generated_figures: 12
unresolved_special_blocks: 0
```

```text
python tools/check_ir_structure.py out/20260531-210228467_fix-who-lbm-unnumbered-headings/who_lbm_check_20260531-212500
[OK] no structure problems found (scanned: 5 yaml files)
```

## 目検確認

- `cha3.sec2` が `heading: Access` で、配下に `i1` から `i6` と `fig1` を保持することを確認。
- `cha3.sec3` が `heading: Personal protection` で、`Access` 配下のitemと混ざっていないことを確認。
- `Figure 1` の固定幅本文は `Access.text` から除去され、`cha3.sec2.fig1` の `raw_lines` に保持されることを確認。
- `cha22.sec8: Infectious materials` と `cha22.sec9: Chemicals and radioactive substances` は見出しとして保持されることを確認。
- Annex 4の表セル内 `infectious materials` が `ann4.sec1` として誤section化されないことを確認。

## 正規化RUNへの影響

このPRは通常修正であり、`data/normalized/` と正規化候補は変更しない。
このPRを反映後、WHO LBM 3rd の正規化RUNを作り直し、表・note・項番なしheading・不要改行/スペースを再確認する。
