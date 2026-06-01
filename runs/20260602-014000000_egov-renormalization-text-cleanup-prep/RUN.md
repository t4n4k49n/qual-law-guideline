# 旧e-Gov再正規化 テキスト整形準備RUN

- run_id: `20260602-014000000_egov-renormalization-text-cleanup-prep`
- branch: `feat/egov-text-cleanup-prep`
- scope: 旧e-Gov再正規化前に必要な e-Gov 個別部のテキスト整形補正

## 背景

正規化RUN親PR `#260` に `src/qai_xml2ir/egov_parser.py` の追加改修が混在していたため、同PRを閉じた。
正規化RUN親PRには parser 改修を含めない方針に戻し、本RUNで準備改修として分離する。

## 問題

旧e-Gov再正規化候補の検証中、以下の2種類のXML由来空白が残った。

- `AppdxTable` のフォールバック本文がXMLインデントを丸ごと拾う
- 表セル内の改行・インデントが `table_row.text` に残る

## 対応

### xml2ir共通部

- 変更なし

### xml2ir e-Gov個別部

- `src/qai_xml2ir/egov_parser.py`
  - `clean_extracted_text()` を追加
  - ASCIIの空白・タブ・改行だけを1スペースへ畳む
  - 全角スペースは条文内の列挙表現として保持
  - note、table cell、table row、appendix fallback text に適用

### その他

- `tests/test_egov_text_cleanup.py` を追加
- 正規化候補はこの準備PRには含めない
- 一時出力は `out/20260602-014000000_egov-renormalization-text-cleanup-prep/` に生成し、Git追跡対象外

## 検証

```powershell
uv run python -m pytest -q tests/test_egov_text_cleanup.py tests/test_egov_table_spans.py tests/test_egov_table_payload_header_inference.py tests/test_egov_api_wrapper.py tests/test_xml_common.py
```

結果:

```text
8 passed
```

```powershell
uv run python tools/check_ir_structure.py out/20260602-014000000_egov-renormalization-text-cleanup-prep/trial
```

結果:

```text
[OK] no structure problems found (scanned: 20 yaml files)
```

heading/text whitespace audit:

```text
jp_egov_335AC0000000145_20260501_507AC0000000037 0
jp_egov_336CO0000000011_20260501_507CO0000000362 0
jp_egov_336M50000100001_20260501_507M60000100117 0
jp_egov_336M50000100002_20260501_507M60000100117 0
jp_egov_416M60000100179_20260501_507M60000100117 0
```

## 次

この準備PR承認後、`main` 同期のうえ、改めて正規化RUN親PRを作成する。
その親PRには `promotion_candidate/`、RUN文書、PR文書、レビューサンプルのみを含め、parser改修は含めない。
