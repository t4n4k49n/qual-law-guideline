# WHO LBM A5固定幅表の列境界修正

## まとめ

WHO LBM 3rd の Annex 5 にある化学物質表について、固定幅テキストからの列復元で語が途中分断される箇所を修正した。正規化候補をレビュー可能な品質にするための前提修正であり、対象は WHO 個別パーサに限定している。

## 変更内容

- A5-1 の固定幅 slice 境界を修正
- Acetaldehyde 行の `Can form explosive` が第6列に保持されることをテスト追加

## 検証

```text
$env:PYTHONPATH='src'; python -m pytest tests/test_who_lbm_general_tables.py -q
11 passed
```

## 対象外

- 共通パーサの変更
- 正規化候補の追加
- `data/normalized/` の更新

<!-- PR_BODY_FILE: runs/20260531-224638937_fix-who-lbm-a5-fixed-width-slices/PR.md -->
