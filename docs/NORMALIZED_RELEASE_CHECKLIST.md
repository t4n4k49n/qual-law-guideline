# 正式版（data/normalized）への格納チェックリスト

このチェックリストは `docs/NORMALIZED_RUN_PLAYBOOK.md` に統合済み。
重複運用を避けるため、以後はPlaybookのみを正本とする。

## 最小確認（参照用）

- 親PR: `runs/<run_id>/promotion_candidate/` のレビューPR
- 子PR: 承認後の昇格専用PR（`promotion_candidate -> data/normalized` 複写のみ）
- 昇格完了判定: `promotion_commit` が `origin/main` の祖先

詳細手順は `docs/NORMALIZED_RUN_PLAYBOOK.md` を参照。
