## まとめ

text2irの正式候補化に向けて、`meta.doc.family` の欠落を解消し、promotion/release向けのGOAL_CHECKを追加します。これにより、通常確認では後方互換を保ちつつ、正式候補レビューではfamily欠落を明確に失敗扱いできます。

## 変更内容

- `qai_text2ir.cli` で `meta.doc.family` を出力
- family解決順を `--family`、profile、source label の順に整理
- `qai_text2ir.goal_check` に `--mode normal|promotion|release` を追加
- promotion/release modeでは `meta.doc.family` 欠落をerror化
- `has_markers` 判定を `marker_types` 対応に修正
- 関連テストを追加

## 確認

```powershell
.\.venv\Scripts\python.exe -m pytest -q tests\test_text2ir_goal_check.py
```

結果: `8 passed`

`data/normalized/` は変更していません。

<!-- PR_BODY_FILE: runs/20260522-130045_text2ir-final-goal-closure/PR.md -->
