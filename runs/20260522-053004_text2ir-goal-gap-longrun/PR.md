## まとめ

text2ir正規化GOAL到達に向けた長期RUNのPhase 3として、代表文書由来の表・注記fixtureを追加し、Markdown tableの構造化とPDF抽出風プレーンテキスト表の非黙殺を確認します。表レコードを候補化し、表タイトル・ヘッダ・表下注記をcontextに含める下流利用品質を実データ相当の小サンプルで検証します。

## 変更内容

- PIC/S Annex 1由来のMarkdown table fixtureを追加
- PIC/S Annex 1由来のplaintext table fixtureを追加
- table/header/row/noteへdata payloadを付与
- profile有効時にplaintext tableを `preformatted` / `possible_table` として保持
- `TABLE_NOTE_REAL_SAMPLE_REVIEW.md` を追加
- `RUN.md` にPhase 3の実装・検証結果を追記

## 確認

- `.\.venv\Scripts\python.exe -m pytest -q tests\test_table_note_real_samples.py tests\test_markdown_table_parsing.py tests\test_normal_note_descendants.py tests\test_text2ir_goal_check.py`
- `.\.venv\Scripts\python.exe -m pytest -q`
- 結果: `158 passed, 1 skipped`

<!-- PR_BODY_FILE: runs/20260522-053004_text2ir-goal-gap-longrun/PR.md -->
