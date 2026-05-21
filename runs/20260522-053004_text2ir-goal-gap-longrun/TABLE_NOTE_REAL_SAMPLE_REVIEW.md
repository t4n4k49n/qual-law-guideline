# TABLE_NOTE_REAL_SAMPLE_REVIEW

## 結論

PIC/S Annex 1由来の小サンプルを追加し、Markdown化された表では `table` / `table_header` / `table_row` / `note` が生成され、`table_row` 選択時に表タイトル・ヘッダ・表下注記をcontextとして取得できることを確認した。

PDF抽出プレーンテキスト風の固定幅表は、profileで明示有効化した場合のみ `preformatted` / `possible_table` として保持し、`possible_plaintext_table_not_structured` タグとsource_spansを付ける。低信頼な表を無理に `table_row` 化せず、黙殺もしない方針とした。

## 使用fixture

| fixture | 由来 | 目的 |
|---|---|---|
| `tests/fixtures/text2ir/pics_annex1_table2_markdown_excerpt.txt` | PIC/S Annex 1 Table 2相当 | Markdown tableの構造化確認 |
| `tests/fixtures/text2ir/pics_annex1_table2_plaintext_excerpt.txt` | PIC/S Annex 1 Table 2相当 | PDF抽出風固定幅表の非黙殺確認 |

## Markdown table確認

- `table` ノード: 生成される。
- `table_header` ノード: 生成され、`data.columns` にヘッダセルが入る。
- `table_row` ノード: 生成され、`data.cells` に行セルが入る。
- 表下注記: `note` ノードとしてtable直下に生成され、`data.note_type: table_note` を持つ。
- source_spans: table/header/row/noteに付与される。
- context_display: `table_row` 選択時に `table`, `table_header`, `note` が含まれる。

## Plaintext table確認

- profile設定 `preprocess.detect_plaintext_tables.enabled: true` の場合のみ検出する。
- 検出結果は `kind: preformatted`, `kind_raw: possible_table`。
- `tags` に `possible_plaintext_table_not_structured` を付与する。
- `data.warning` に同名warningを記録する。
- source_spansで該当行範囲を追跡できる。

## 実行テスト

```powershell
.\.venv\Scripts\python.exe -m pytest -q tests\test_table_note_real_samples.py tests\test_markdown_table_parsing.py tests\test_normal_note_descendants.py tests\test_text2ir_goal_check.py
.\.venv\Scripts\python.exe -m pytest -q
```

結果:

- `15 passed`
- `158 passed, 1 skipped`
