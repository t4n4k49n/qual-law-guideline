## まとめ

text2irの最終GOAL到達に向けて、表・注記の本番入力適用を進めます。安全な固定幅表は構造化し、不安定な表は `possible_table` として保持することで、表・注記を黙殺しない状態にします。

## 変更内容

- `qai_text2ir.table_note_inventory` を追加
- 固定幅表のcaption検出を拡張
- 安全な固定幅表を `table/table_header/table_row` 化
- 不安定な固定幅表を `preformatted possible_table` として保持
- table直後のnoteを保持
- 表・注記を持つ代表profileで検出を有効化
- skip block処理の行index上書きバグを修正
- 関連fixture/testを追加・更新

## 確認

```powershell
.\.venv\Scripts\python.exe -m pytest -q tests\test_table_note_real_samples.py tests\test_table_note_inventory.py tests\test_markdown_table_parsing.py tests\test_text2ir_goal_check.py
```

結果: `20 passed`

PIC/S Annex 1 full input smoke regeneration:

- strict exit 0
- observed: `preformatted=4`, `note=9`

`data/normalized/` は変更していません。

<!-- PR_BODY_FILE: runs/20260522-130045_text2ir-final-goal-closure/PR.md -->
