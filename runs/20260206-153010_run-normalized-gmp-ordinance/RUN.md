# RUN 20260206-153010_run-normalized-gmp-ordinance

## Summary
- 入力XML（GMP省令）を `xml2ir` で正規化（IR変換）
- `verify_temp.py` による最小整合性チェックをパス

## Input
- Path: `C:\Users\ryoki\Documents\GitHub\qual-law-guideline_OLD-HANDMADE\data\xml\416M60000100179_20260501_507M60000100117\416M60000100179_20260501_507M60000100117.xml`
- DocID: `jp_egov_416M60000100179_20260501_507M60000100117`

## Outputs
- `out/20260206-153010_run-normalized-gmp-ordinance/`
  - `*.regdoc_ir.yaml`: IR本体
  - `*.parser_profile.yaml`: パーサ設定（再現用）
  - `*.regdoc_profile.yaml`: 文書固有設定
  - `*.meta.yaml`: メタデータ
  - `manifest.yaml`: 実行記録

## Verification
- Script: `verify_temp.py`
- Result: PASS
  - `assert_unique_nids`: OK
  - `check_annex_article_nids`: OK
  - `check_appendix_scoped_indices`: OK

## Notes
- `xml2ir` コマンドライン引数の指定方法を確認（`bundle` サブコマンドは不要）
