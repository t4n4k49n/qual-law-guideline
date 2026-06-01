# 旧e-Gov正規化 再正規化RUN v2

## まとめ

旧e-Gov正規化データ5件を、公式e-Gov XMLから現行IR基準で再生成する正規化RUNです。parser改修は準備PR `#261` で分離済みであり、このPRは `promotion_candidate/` のレビューに絞っています。これにより、旧構造の `article.text` や article 直下 item を解消し、DQチェックシートで一貫して参照できる階層へ更新します。

## 対象

- `jp_egov_335AC0000000145_20260501_507AC0000000037`
- `jp_egov_336CO0000000011_20260501_507CO0000000362`
- `jp_egov_336M50000100001_20260501_507M60000100117`
- `jp_egov_336M50000100002_20260501_507M60000100117`
- `jp_egov_416M60000100179_20260501_507M60000100117`

## 変更内容

- `promotion_candidate/` に5文書分の正規化候補を作成
- `manifest.yaml` に入力XML、生成コマンド、件数、SHA256、検証結果を記録
- 深い階層サンプルを `SAMPLE_EXTRACT.md` に記録

## 検証

- `uv run python tools/check_ir_structure.py runs/20260602-021000000_run-normalized-jp-egov-renormalization-v2/promotion_candidate`
  - `[OK] no structure problems found (scanned: 20 yaml files)`
- `uv run python -m pytest -q tests/test_xml_common.py tests/test_egov_api_wrapper.py tests/test_egov_text_cleanup.py tests/test_egov_article_structure.py tests/test_egov_table_spans.py tests/test_egov_table_payload_header_inference.py tests/test_xml2ir_no_fold_article.py tests/test_xml2ir_profiles_table_context.py tests/test_ecfr_parser.py`
  - `19 passed`
- `verify_document`
  - 5文書すべて `OK`
- heading/text whitespace audit
  - 5文書すべて `0`

## 昇格方針

このPRでは `data/normalized/` は変更しません。承認後、子PRで `promotion_candidate/` から `data/normalized/<doc_id>/` へ5文書を複写します。`ARCHIVE_jp_egov_*` は昇格対象外です。

<!-- PR_BODY_FILE: runs/20260602-021000000_run-normalized-jp-egov-renormalization-v2/PR.md -->
