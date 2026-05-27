<!-- PR_BODY_FILE: docs/pr_bodies/pr-readiness-10-12-13-rerun.md -->

## まとめ

10 EU GMP、12 PIC/S、13 WHO LBM 3rd の正規化を進める順番と判断根拠を、現行mainでの再生成結果に基づいて更新しました。次に着手すべき正式化対象を絞り、表・注記レビューや対象範囲判断が必要な文書を分けたことで、正規化RUNを小さく安全に進められる状態にしています。

## 変更内容

- 10/12/13 の既存GOAL pass文書を現行mainで再生成し、readinessを記録
- `docs/NORMALIZATION_PLAN_10_12_13.md` に再生成後の判断と優先順位を反映
- `runs/20260527-105034029_docs-readiness-10-12-13-rerun/` にRUN記録、readiness表、監査レポートを追加

## 主な判断

- EU GMP Chapter 1を次の正規化RUNの第一候補にする
- PIC/S Annex 11をPIC/S単体Annexの第一候補にする
- PIC/S Annex 1とWHO LBM 3rdはreadyだが、表・注記レビューまたは対象範囲判断を先に挟む
- PIC/S Annexes refinedは現行mainでstrict failのため、正式化初手から外す

## 検証

- `git diff --check`
- `.\.venv\Scripts\python.exe -m pytest -q tests/test_text2ir_goal_check.py tests/test_text2ir_audit_report.py`
