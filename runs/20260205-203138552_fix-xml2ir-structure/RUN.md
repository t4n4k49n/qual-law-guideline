# RUN 20260205-203138552_fix-xml2ir-structure

## Summary
- 実データ統合テスト用の verify ユーティリティを追加
- integration テストを追加（環境変数がない場合は skip）
- テスト計画書と README に実行手順を追記
- pytest marker に integration を登録

## Tests
- python -m pytest

## Notes
- EGOV_XML_SAMPLE_* が未設定のため integration は skip される想定
