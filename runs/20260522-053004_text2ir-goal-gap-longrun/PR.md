## まとめ

text2ir正規化GOAL到達に向けた長期RUNのPhase 0として、作業前ベースラインを固定します。既存テストの成功状態と、現行text2ir機能の実装済み範囲を明文化し、以降のPhaseでGOAL検証ハーネス、監査レポート、表・注記fixture、profile修正へ進める前提を整えます。

## 変更内容

- 長期RUNの `RUN.md` を追加
- Phase 0の `BASELINE.md` を追加
- Phase 0のPR本文を追加

## 確認

- `.\.venv\Scripts\python.exe -m pytest -q`
- 結果: `148 passed, 1 skipped`

<!-- PR_BODY_FILE: runs/20260522-053004_text2ir-goal-gap-longrun/PR.md -->
