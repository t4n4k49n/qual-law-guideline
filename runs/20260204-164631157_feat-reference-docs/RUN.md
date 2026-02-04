# RUN

run_id: 20260204-164631157_feat-reference-docs
branch: feat/reference-docs
started_at: 2026-02-04 16:46 (JST)

## 目的（1文）
- 旧管理メモHTMLを原典として保存し、指針ドキュメントと参照導線を整備する。

## Done Definition（完了条件）
- [x] 原典HTMLをリポジトリ内に保管する
- [x] 指針ドキュメントを作成する
- [x] README/KNOWLEDGE/TODOから参照できる

## 重要：文字化け回避（UTF-8遵守）
- テキストは UTF-8（BOMなし）、改行はLF

## 手順（やった順）
1) runディレクトリとoutディレクトリを作成
2) 旧管理メモHTMLを references/administrators-memos/ にコピー
3) docs/REFERENCE.md を作成
4) README/KNOWLEDGE/TODO を更新

## 実行コマンド（コピペで再現できる形）
- `git checkout -b feat/reference-docs`
- `Get-Date -Format yyyyMMdd-HHmmssfff`
- `python -`（run/out/参照ファイル作成とHTMLコピー）

## 結果（事実ベース）
- 何ができた：原典HTMLの保存、指針ドキュメント作成、参照導線の追加
- 何ができなかった：
- 数値（処理時間/件数/フレーム数など）：HTML 3件

## 生成物（上書き禁止）
- `out/20260204-164631157_feat-reference-docs/`

## 影響範囲（変更点）
- 変更ファイル：`README.md`, `TODO.md`, `KNOWLEDGE.md`, `docs/REFERENCE.md`
- ふるまいの変更：参照ドキュメントの導線を追加

## ロールバック
- 戻し方（git revert / 設定戻し等）
- `git revert <commit>`

## つまずき・学び
- 事象：
- 原因：
- 対策：
- 次回への注意：

## KNOWLEDGE候補（昇格するなら）
- 参照資料の保持ルール

## 次のTODO（1〜3個）
- [ ] IRスキーマの確定版作成
- [ ] 表示プロファイルの具体化
