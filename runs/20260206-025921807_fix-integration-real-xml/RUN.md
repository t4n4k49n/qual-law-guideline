# RUN 20260206-025921807_fix-integration-real-xml

## Summary
- integration テストの CLI 呼び出しを修正（Typer のサブコマンド誤指定を修正）
- 実データの Num 由来 appendices を考慮した検証に調整

## Tests
- python -m pytest -m integration -q

## Notes
- EGOV_XML_SAMPLE_1 を指定して実行
