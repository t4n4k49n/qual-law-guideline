<!-- PR_BODY_FILE: runs/20260601-183000000_cfr-part11-xml-normalization-prep/PR_BODY.md -->

## まとめ

21 CFR Part 11 の eCFR XML を、正式な正規化RUNへ進めるための準備を追加しました。e-Gov専用だった `xml2ir` の入口を壊さずにCFR XMLを扱えるようにし、公式ECFR XML User Guideを参照したうえで、Part/Subpart/Section、本文項番、Authority/Source/Citation注記をIRへ分離できる試行候補を作成しています。

## 変更内容

- xml2ir共通部
  - `xml2ir bundle --xml-family egov|ecfr` を追加し、既定値は従来どおり `egov`
  - XML local-name、inline text flatten、空白正規化の共通ヘルパーを追加
  - meta生成にUS/CFR向けのjurisdiction/language/source label/CFR identifiersを追加し、e-Gov既定値は維持

- xml2ir CFR個別部
  - eCFR XML用 `ecfr_parser` を追加
  - `DIV5 TYPE="PART"`、`DIV6 TYPE="SUBPART"`、`DIV8 TYPE="SECTION"` をIR階層へ変換
  - `P` の `(a)`、`(1)`、`(i)` などを paragraph/item/subitem へ分解
  - `AUTH`、`SOURCE`、`CITA` を informative note として分離

- その他
  - Part 11 trial candidate bundleを `runs/20260601-183000000_cfr-part11-xml-normalization-prep/trial_candidate/` に作成
  - `RUN.md` に公式資料、切り分け、検証結果、正式正規化RUN前の残確認を記録
  - Part 11 XML向けテストを追加

## 検証

- `python -m pytest tests/test_ecfr_parser.py tests/test_text2ir_cfr_quality_v2.py tests/test_text2ir_cfr_notes.py -q`
  - `5 passed`
- `uv run python -m pytest tests/test_ecfr_parser.py tests/test_xml2ir_no_fold_article.py tests/test_egov_article_structure.py -q`
  - `6 passed`
- `uv run python -m pytest tests/test_ecfr_parser.py tests/test_text2ir_cfr_quality_v2.py tests/test_text2ir_cfr_notes.py tests/test_xml2ir_no_fold_article.py tests/test_egov_article_structure.py -q`
  - `9 passed`
