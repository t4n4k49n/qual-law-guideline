<!-- PR_BODY_FILE: runs/20260522-222947088_fix-text2ir-glyph-form-artifact-cleanup/PR.md -->

## まとめ

text2irでPDF抽出由来のPrivate Use Area glyph、dot leader、チェックフォーム残骸がIR本文やYAML可読部に残る問題を、文書個別patchではなく共通処理として閉じます。これにより、WHO LBM 3rdの `cha8.i5.si1` / `cha8.i5.si2` のような壊れたフォーム行は、通常のDQ/GMP選択候補ではなく、sanitize済みの `form_artifact` として明示的に隔離されます。

## 変更内容

- `glyph_sanitizer.py` を追加し、literal PUA検出・marker glyph正規化・可読文字列sanitizeを実装。
- `artifact_classifier.py` を追加し、フォーム/チェックボックス/dot leader由来artifactを共通検出。
- `text_parser.py` に、PUA bullet正規化、フォーム本文分離、`form_artifact` 隔離、再帰sanitizeを追加。
- `goal_check.py` に、promotion/release時のliteral PUA・severe artifact・guard残存の失格判定を追加。
- `artifact_audit.py` を追加し、代表出力の監査レポートを生成可能にした。
- WHO/PIC/S/goal_check向けテストを追加。

## 検証

- `python -m pytest tests/test_text2ir_glyph_form_cleanup.py tests/test_text2ir_goal_check.py -q`
- `python -m pytest tests/test_text2ir_who_lbm_3rd.py tests/test_pics_annex2a_preformatted.py tests/test_table_note_real_samples.py tests/test_text2ir_audit_report.py -q`
- 代表9文書を再生成し、`goal_check --mode promotion` 全件PASS。
- 代表9文書の literal PUA: 0。

## 注意

- `data/normalized/` への昇格は行っていません。
- PIC/S Annex 1の既存single newline qualitycheck warningは本件外として残っています。
