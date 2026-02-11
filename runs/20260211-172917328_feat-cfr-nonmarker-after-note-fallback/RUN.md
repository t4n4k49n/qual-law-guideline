# RUN

run_id: 20260211-172917328_feat-cfr-nonmarker-after-note-fallback
branch: feat/cfr-nonmarker-after-note-fallback
started_at: 2026-02-11 17:29 (JST)

## 目的（1文）
- CFRでnote直後に現れる非マーカー行を、noteへ誤連結せず直前本文へフォールバック連結する。

## Done Definition（完了条件）
- [x] text_parser にフォールバックロジック実装
- [x] note直後の非マーカー行のテスト追加
- [x] 追加テストがパス

## 実装
- `src/qai_text2ir/text_parser.py`
  - 非マーカー行処理で `current` が `note/history` の場合、まず同一親の直前非note兄弟へ連結するフォールバックを追加
  - 兄弟が見つからない場合は、従来より近い非noteノードへフォールバックし、いずれも warning を出力
- `tests/test_text2ir_cfr_notes.py`
  - note直後の非マーカー行が note ではなく paragraph(a) 側へ連結されることを検証するテストを追加

## 検証
- 実行: `python -m pytest -q tests/test_text2ir_cfr_notes.py`
- 結果: `2 passed`
