# TEST_RESULTS

## Phase 6関連テスト

```powershell
.\.venv\Scripts\python.exe -m pytest -q tests\test_text2ir_goal_check.py tests\test_text2ir_audit_report.py tests\test_table_note_real_samples.py tests\test_pics_annex15_profile.py tests\test_pics_annex11_profile.py tests\test_pics_annex2a_profile.py tests\test_pics_part2_v1.py
```

結果: `17 passed`

## 全体テスト

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

結果: `160 passed, 1 skipped`

## 代表9文書再生成

`out/20260522-053004_text2ir-goal-gap-longrun/<doc_id>/exit_code.txt` で全件 `0` を確認。

## GOAL_CHECK

代表9文書すべて `python -m qai_text2ir.goal_check` exit 0。

## audit_report

`python -m qai_text2ir.audit_report --run-out-dir out/20260522-053004_text2ir-goal-gap-longrun` を実行し、Markdown/JSONを作成。
