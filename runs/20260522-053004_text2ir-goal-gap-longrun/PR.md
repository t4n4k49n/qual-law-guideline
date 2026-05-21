## まとめ

text2ir正規化GOAL到達に向けた長期RUNのPhase 2として、複数bundleを横断する監査レポート生成を追加します。代表文書再生成後に、GOALチェック結果、node数、kind分布、source_spans coverage、table/note件数、profile provenance、refine適用数を一括で人間レビュー用に集計できる状態にします。

## 変更内容

- `src/qai_text2ir/audit_report.py` を追加
- `tests/test_text2ir_audit_report.py` を追加
- `RUN.md` にPhase 2の実装・検証結果を追記

## 確認

- `.\.venv\Scripts\python.exe -m pytest -q tests\test_text2ir_audit_report.py tests\test_text2ir_goal_check.py`
- `.\.venv\Scripts\python.exe -m pytest -q`
- 結果: `155 passed, 1 skipped`

<!-- PR_BODY_FILE: runs/20260522-053004_text2ir-goal-gap-longrun/PR.md -->
