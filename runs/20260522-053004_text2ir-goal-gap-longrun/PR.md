## まとめ

text2ir正規化GOAL到達に向けた長期RUNのPhase 1として、strict成功だけに依存しないGOAL検証ハーネスを追加します。bundle単位でv4、4ファイル、manifest、source_spans、nid/ord、dq_gmp_checklistを確認できるようにし、正式化前レビューの判断材料を機械的に揃えられる状態にします。

## 変更内容

- `src/qai_text2ir/goal_check.py` を追加
- `tests/test_text2ir_goal_check.py` を追加
- `RUN.md` にPhase 1の実装・検証結果を追記

## 確認

- `.\.venv\Scripts\python.exe -m pytest -q tests\test_text2ir_goal_check.py`
- `.\.venv\Scripts\python.exe -m pytest -q tests\test_text2ir_bundle.py tests\test_markdown_table_parsing.py tests\test_normal_note_descendants.py tests\test_text2ir_goal_check.py`
- `.\.venv\Scripts\python.exe -m pytest -q`
- 結果: `153 passed, 1 skipped`

<!-- PR_BODY_FILE: runs/20260522-053004_text2ir-goal-gap-longrun/PR.md -->
