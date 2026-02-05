# RUN 20260205-195222266_fix-xml2ir-structure

## Summary
- appendix(Appdx*) の idx を親スコープ内の appendix 専用連番に変更（len(children) 依存を排除）
- SupplProvision 内の SupplProvisionAppdx* を annex 内 appendices だけで 1 開始に安定化
- Appdx* の should_skip 対応を追加
- 回帰テスト追加（appendix 連番が他ノード数に依存しないことを検証）

## Tests
- python -m pytest

## Notes
- 変更差分は egov_parser の appendix カウンタ導入と tests 追加のみ
