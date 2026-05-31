# WHO LBM 3rd正規化候補 v8

## まとめ

WHO Laboratory Biosafety Manual, 3rd ed. の正規化候補をレビュー可能な形で追加します。前段で修正した本文中タイトル句、不要空白、固定幅表の列境界、Table A5-1 の索引巻き込み防止を反映し、表はIRから再構成して人が確認できる状態まで検証しました。

## 対象

- 文書: WHO Laboratory Biosafety Manual, 3rd ed.
- source URL: https://www.who.int/publications/i/item/9241546506
- doc_id: `who_lbm_3rd_2004_9241546506`
- 正規化候補: `runs/20260531-234647542_run-normalized-who-lbm-3rd-v8/promotion_candidate/`

## 検証結果

- WHO LBM関連テスト: `31 passed`
- `goal_check`: `PASS`
- `special_structure_audit`: `pass`
- `tools/check_ir_structure.py`: `[OK] no structure problems found`
- source span coverage: `1.0`
- source_tables / generated_tables: `18 / 18`
- generated_rows: `1017`
- generated_figures: `12`
- unresolved_special_blocks: `0`

## 目検・再結合チェック

`TABLE_RECONSTRUCTION_CHECK.md` に確認結果を記録しています。

- Table A4-2: カテゴリ行、`Explosion in domestic-`、`Fire in flame` の列復元を確認
- Table A5-1: `Acetaldehyde` 行の `Can form explosive` を確認
- Table A5-1: 索引行 `alarms 21, 60` の巻き込みなし
- heading: `Access` / `Personal protection` / `Infectious materials` / `Chemicals and radioactive substances` を確認
- 不要空白: 個人環境の絶対パス、tab、行末スペースなし

## 深い階層サンプル

`SAMPLE_EXTRACT.md` に祖先経路を省略せず記録しています。

| 階層 | nid | kind | text / heading |
|---:|---|---|---|
| 1 | `root` | `document` |  |
| 2 | `ann5` | `annex` | `Chemicals: hazards and precautions` |
| 3 | `ann5.tbla5_1` | `table` | `Table A5-1. Chemicals: hazards and precautions` |
| 4 | `ann5.tbla5_1.tblh` | `table_header` | `Chemical \| Physical properties \| Health hazards \| Fire hazards \| Safety precautions \| Incompatible chemicals / other hazards` |
| 5 | `ann5.tbla5_1.tblh.tblr1` | `table_row` | `Acetaldehyde \| Colourless liquid or \| Mild eye and \| Extremely flammable; \| No open flames, no \| Can form explosive` |

## 対象外

- `data/normalized/` への昇格は含めない
- 昇格は、この親PR承認後に子PRで実施する

<!-- PR_BODY_FILE: runs/20260531-234647542_run-normalized-who-lbm-3rd-v8/PR.md -->
