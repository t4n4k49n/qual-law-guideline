## まとめ

text2irの代表9文書を再生成し、通常GOAL_CHECKとpromotion GOAL_CHECKの両方で正式候補前の監査を実施しました。文書ファミリ、4ファイル構成、manifest、source_spans、表・注記の保持状況を同じ観点で一覧化し、残る論点を「複雑な表の安全な行分解」に限定しました。

## 変更内容

- `qai_text2ir.audit_report` を拡張
- 代表9文書を再生成し、各文書のGOAL_CHECK結果を作成
- `TEXT2IR_AUDIT_REPORT.md/json` を追加
- `TABLE_NOTE_INVENTORY.md/json` を追加
- `TEXT2IR_FINAL_GAP_STATUS.md` を追加
- Phase 9DのRUN記録を更新

## 確認

```powershell
.\.venv\Scripts\python.exe -m pytest -q tests\test_text2ir_audit_report.py tests\test_text2ir_goal_check.py
```

結果: `10 passed`

代表9文書:

- normal GOAL_CHECK: `9/9 pass`
- promotion GOAL_CHECK: `9/9 pass`
- `meta.doc.family`: `9/9 present`
- 残GAP: `none=6`, `table_rows_pending=3`

`data/normalized/` は変更していません。

<!-- PR_BODY_FILE: runs/20260522-130045_text2ir-final-goal-closure/PR.md -->
