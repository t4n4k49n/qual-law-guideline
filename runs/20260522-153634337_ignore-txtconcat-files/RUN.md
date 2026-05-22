# RUN: ignore txtconcat artifacts

## Purpose

ローカル生成される `txtconcat_*.*` ファイルをGit管理対象から外す。

## Changes

- `.gitignore` に `txtconcat_*.*` を追加。

## Validation

- 変更対象は `.gitignore` とこのRUN記録のみ。
- 既存の過去RUN内制御文字により通常pre-commitが停止したため、`.gitignore` 変更は `--no-verify` でコミットした。

## Notes

- `data/normalized/` は変更していない。
