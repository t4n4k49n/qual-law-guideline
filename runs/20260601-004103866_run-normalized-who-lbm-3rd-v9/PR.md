# WHO LBM 3rd正規化候補 v9

## まとめ

WHO Laboratory Biosafety Manual 3rd edition の正規化候補を、表と本文の位置関係を保った形でレビュー可能にしました。前回問題になった「Table と Table 間の本文が前に出る」崩れを重点確認し、表の再結合、項番なしheading、不要改行・空白を含めて確認記録を残しています。

このPRは親PRです。`data/normalized/` への昇格は含めていません。承認後、候補から正式版へ複写する子PRを別途作成します。

## 対象

- 文書: WHO Laboratory Biosafety Manual, 3rd ed.
- doc_id: `who_lbm_3rd_2004_9241546506`
- 原文URL: `https://www.who.int/publications/i/item/9241546506`
- 候補: `runs/20260601-004103866_run-normalized-who-lbm-3rd-v9/promotion_candidate/`

## 変更内容

- WHO LBM 3rd の正規化候補一式を追加
- `manifest.yaml` を追加し、実行条件と検証対象を記録
- 目検用アーティファクトを追加
  - `GOAL_CHECK.md`
  - `SPECIAL_STRUCTURE_AUDIT.md`
  - `TABLE_RECONSTRUCTION_CHECK.md`
  - `SAMPLE_EXTRACT.md`

## 検証結果

- WHO LBM関連テスト: `32 passed`
- `goal_check --mode promotion`: `PASS`
  - nodes: `2023`
  - source span coverage: `1.0`
  - warnings: `none`
- `special_structure_audit --mode promotion`: `pass`
  - source_tables: `18`
  - generated_tables: `18`
  - generated_rows: `1017`
  - generated_figures: `12`
  - unresolved_special_blocks: `0`
- `tools/check_ir_structure.py`: `[OK] no structure problems found`
- 絶対パス・タブ・末尾空白検索: 0件

## 表・本文順序の確認

`TABLE_RECONSTRUCTION_CHECK.md` で以下を確認済みです。

- `cha1.sec1.text` は Table 1 前で止まる
- Chapter 1 の順序は `Table 1 -> Table 1後本文 -> Table 2 -> risk assessment items -> Table 2後本文 -> Table 3 -> Table 3後本文`
- `Laboratory facilities are designated as basic ...` は Table 1 の後に配置
- `The assignment of an agent ...` は Table 2 の後、Table 3 の前に配置
- `Thus, the assignment ...` は Table 3 の後に配置
- 全親ノードで `table` / `statement` / `item` / `subitem` / `figure` のsource line順逆転なし

## 表の再結合確認

- Table A4-2
  - 行数: `22`
  - 先頭行: `Faulty design or construction |  | `
  - domestic refrigerator と flame photometer のnote相当行を確認
- Table A5-1
  - 行数: `701`
  - 先頭行: `Acetaldehyde | Colourless liquid or | Mild eye and | Extremely flammable; | No open flames, no | Can form explosive`
  - Index本文の `alarms 21, 60` はA5表行に混入していない

## heading・改行・スペース確認

- 項番なしheadingを確認
  - `Access`
  - `Personal protection`
  - `Infectious materials`
  - `Chemicals and radioactive substances`
- 既知の崩れやすい語句を確認
  - `The Laboratory biosafety manual has`
  - `Wear gloves to protect skin against chemical effects of detergents`

## 深い階層サンプル

`SAMPLE_EXTRACT.md` から、祖先を省略せずに提示します。

- `root` / `document`
- `ann5` / `annex` / `Chemicals: hazards and precautions`
- `ann5.tbla5_1` / `table` / `Table A5-1. Chemicals: hazards and precautions`
- `ann5.tbla5_1.tblh` / `table_header` / `Chemical | Physical properties | Health hazards | Fire hazards | Safety precautions | Incompatible chemicals / other hazards`
- `ann5.tbla5_1.tblh.tblr1` / `table_row` / `Acetaldehyde | Colourless liquid or | Mild eye and | Extremely flammable; | No open flames, no | Can form explosive`

<!-- PR_BODY_FILE: runs/20260601-004103866_run-normalized-who-lbm-3rd-v9/PR.md -->
