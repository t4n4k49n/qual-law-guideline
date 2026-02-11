# RUN

run_id: 20260212-042739562_feat-text-unwrap-hyphen-normalization
branch: feat/text-unwrap-hyphen-normalization
started_at: 2026-02-12 04:27 (JST)

## 目的（1文）
- hard wrap解除・単語分断ハイフン復元・preformatted保持を導入し、CFR系IRの本文正規化品質を改善する。

## Done Definition（完了条件）
- [x] parserにunwrap/preformatted状態管理を実装
- [x] hyphenationポストプロセス実装
- [x] qualitycheck実装（strict対応）
- [x] unit+integrationテスト追加
- [x] 全テスト実行

## 実装
- `src/qai_text2ir/text_parser.py`
  - `normalize_visible_chars` / `is_preformatted_line` を追加
  - append状態（段落区切り/整形ブロック）管理で proseはスペース結合、空行で `\n\n` 区切り
  - preformatted は改行・インデント維持
  - ハイフン分断復元ポストプロセスを追加（keep/drop優先規則、allowlist/prefix対応）
  - qualitycheck（分断残り・prose単一改行）を追加
- `src/qai_text2ir/cli.py`
  - `--qualitycheck/--no-qualitycheck` と `--strict` を追加
  - qualitycheck警告表示、`--strict` で失敗化
- `tests/test_text2ir_normalization.py` を新規追加
  - prose unwrap
  - hyphenation drop/keep
  - preformatted保持
  - CFR相当integrationケース

## テスト
- 実行: `python -m pytest -q tests/test_text2ir_bundle.py tests/test_text2ir_cfr_notes.py tests/test_text2ir_cfr_quality_v2.py tests/test_text2ir_normalization.py`
- 結果: `8 passed`
- 実行: `python -m pytest -q`
- 結果: `26 passed, 1 skipped`
