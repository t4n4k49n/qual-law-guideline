# 旧e-Gov再正規化前のテキスト整形補正

## まとめ

旧e-Gov再正規化RUNに混入していた parser 改修を切り出し、準備PRとして扱い直します。表セルや別表本文に残るXML由来の改行・インデントを e-Gov 個別部で除去することで、次の正規化RUN親PRを「候補生成とレビュー専用」に戻せます。

## 変更内容

- `src/qai_xml2ir/egov_parser.py`
  - `clean_extracted_text()` を追加
  - note、table cell、table row、appendix fallback text のASCII空白・改行を正規化
  - 全角スペースは保持
- `tests/test_egov_text_cleanup.py`
  - XMLインデント除去と全角スペース保持を確認

## 検証

- `uv run python -m pytest -q tests/test_egov_text_cleanup.py tests/test_egov_table_spans.py tests/test_egov_table_payload_header_inference.py tests/test_egov_api_wrapper.py tests/test_xml_common.py`
  - `8 passed`
- 一時出力で旧e-Gov 5件を再生成
  - `check_ir_structure`: OK
  - heading/text whitespace audit: 5件すべて `0`

## 次

承認後、main同期して正規化RUN親PRを切り直します。そのPRには parser 改修を含めません。

<!-- PR_BODY_FILE: runs/20260602-014000000_egov-renormalization-text-cleanup-prep/PR.md -->
