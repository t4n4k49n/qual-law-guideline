<!-- PR_BODY_FILE: runs/20260603-014940040_feat-yaml-4set-gap-report-v1/PR_BODY.md -->

# まとめ

旧zip版4点YAMLと現行正式4点YAMLの差分を、実装判断に使える形で整理しました。Devin 側で固定doc_idや旧YAML構造を前提にした実装が残っている場合の影響範囲を明確にし、現行27件の正式データを動的ロード・profile駆動で扱う必要性を確認できるようにしています。

## 変更内容

- `runs/20260603-014940040_feat-yaml-4set-gap-report-v1/` にRUN記録を追加
- 旧zip版と現行 `data/normalized` の4点YAML比較スクリプトを追加
- YAML契約の集計補助スクリプトを追加
- Devin向けのギャップレポートを追加

## 検証

- `python -m py_compile runs\20260603-014940040_feat-yaml-4set-gap-report-v1\analyze_yaml_contract.py runs\20260603-014940040_feat-yaml-4set-gap-report-v1\compare_yaml_4sets.py`
