<!-- PR_BODY_FILE: runs/20260601-193000000_cfr-part211-xml-normalization-prep/PR_BODY.md -->

## まとめ

21 CFR Part 211 の eCFR XML を正式正規化RUNへ進めるための準備を追加しました。Part 11で追加したeCFR XML対応を流用しつつ、Part 211で露出した項番判定と改正リンク注記の落ちを修正し、Part 11/Part 211を後でまとめて正規化RUNに載せられる状態へ近づけています。

## 変更内容

- xml2ir共通部
  - Part 11で追加済みの `--xml-family ecfr`、XML flatten、US/CFR metadataを再利用
  - 今回の追加共通APIはなし

- xml2ir CFR個別部
  - `(c)` のような英字段落が、直前のitem配下のsubitemへ誤分類されるケースを修正
  - `§ 211.42(c)(10)(i)` から `(vi)` のようなローマ数字subitemはitem配下に維持
  - `XREF` 改正リンクを informative note として保持
  - eCFR parser profileに `XREF` markerを追加

- その他
  - Part 211 trial candidate bundleを `runs/20260601-193000000_cfr-part211-xml-normalization-prep/trial_candidate_r3/` に作成
  - `RUN.md` に公式資料、切り分け、検証結果、正式正規化RUN前の残確認を記録
  - Part 211固有ケースのテストを追加

## 検証

- `uv run python -m pytest tests/test_ecfr_parser.py tests/test_text2ir_cfr_quality_v2.py tests/test_text2ir_cfr_notes.py tests/test_xml2ir_no_fold_article.py tests/test_egov_article_structure.py -q`
  - `12 passed`
