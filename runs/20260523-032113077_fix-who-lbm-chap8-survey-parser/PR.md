## まとめ

WHO LBM 3rd Chapter 8 の Table 5-7 を、通常本文ではなく survey/checklist table として正規化する専用パーサーを追加した。

従来は dot leader や checkbox/private-use glyph を含むフォーム由来テキストが `cha8.i5.si*` 等の通常 subitem として見えていた。今回の修正では、対象を `who_lbm_3rd_2004_9241546506` の Chapter 8 Table 5-7 に限定し、table caption、section heading、checklist item row を `table/table_header/table_row` として保持する。一方で、Location/Date/YES/NO/N/A/COMMENTS/署名欄/checkbox glyph などのフォーム足場は人間可読テキストから除去する。

これにより、Chapter 8 の survey table をレビューUI・YAML確認・検索・候補出力で扱える形にしつつ、他文書や通常 text2ir には影響しない構成にした。

## 変更内容

- WHO LBM Chapter 8 Table 5-7 専用 parser `who_lbm_chap8_survey.py` を追加。
- WHO LBM profile に `special_parsers.who_lbm_chap8_survey.enabled: true` を追加。
- common parser 側に、canonical doc_id と profile flag の両方で限定起動する hook を追加。
- Table 5=81行、Table 6=37行、Table 7=15行、合計133行の fixture/integration test を追加。
- 処理後の WHO LBM YAML を `out/who_lbm_3rd_review_ui/` に複写し、既存レビューUIで確認できる状態にした。

## 確認結果

- `python -m pytest tests/test_who_lbm_chap8_survey_parser.py -q`
  - `2 passed`
- `python -m pytest tests/test_text2ir_who_lbm_3rd.py tests/test_who_lbm_heading_merge.py tests/test_who_lbm_v4_skip_toc_and_annex_heading.py tests/test_who_lbm_chap8_survey_parser.py -q`
  - `13 passed`
- `python -m pytest tests/test_text2ir_goal_check.py tests/test_text2ir_profiles_pics.py tests/test_pics_annex2a_preformatted.py -q`
  - `12 passed`
- `python -m pytest -q`
  - `169 passed, 1 skipped`

## 代表確認

- `Information on sign accurate and current` -> `cha8.tbl6.tblh2.tblr4`
- `Sign legible and not defaced` -> `cha8.tbl6.tblh2.tblr5`
- `No trash on floor` -> `cha8.tbl5.tblh8.tblr6`
- `Microwave oven(s) clearly labelled “No Food Preparation, Laboratory Use Only”` -> `cha8.tbl5.tblh11.tblr2`

## 対象外

- 一般的なPDFフォーム復元器は実装していない。
- PIC/S、EU GMP、CFR、xml2ir由来文書には作用しない。

<!-- PR_BODY_FILE: runs/20260523-032113077_fix-who-lbm-chap8-survey-parser/PR.md -->
