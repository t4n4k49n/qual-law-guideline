# RUN

run_id: 20260204-180511548_feat-ops-rules
branch: feat/ops-rules
started_at: 2026-02-04 18:05 (JST)

## 目的（1文）
- 出力運用ルールの明文化と、次の構成作業のTODO追加、.gitignoreの提案を行う。

## Done Definition（完了条件）
- [x] REFERENCE.md に運用ルールを追記
- [x] TODO.md に次の構成作業を追加
- [x] .gitignore の提案を追加

## 重要：文字化け回避（UTF-8遵守）
- テキストは UTF-8（BOMなし）、改行はLF

## 手順（やった順）
1) run/out ディレクトリを作成
2) REFERENCE.md に運用ルールを追記
3) TODO.md に次タスクを追加
4) .gitignore を追加

## 実行コマンド（コピペで再現できる形）
- `git checkout -b feat/ops-rules`
- `Get-Date -Format yyyyMMdd-HHmmssfff`
- `python -`（run/out 作成）

## 結果（事実ベース）
- 何ができた：運用ルール追記、TODO追加、.gitignore追加
- 何ができなかった：
- 数値（処理時間/件数/フレーム数など）：

## 生成物（上書き禁止）
- `out/20260204-180511548_feat-ops-rules/`

## 影響範囲（変更点）
- 変更ファイル：`docs/REFERENCE.md`, `TODO.md`, `.gitignore`
- ふるまいの変更：運用ルールの明文化と除外ルールの追加

## ロールバック
- 戻し方（git revert / 設定戻し等）
- `git revert <commit>`

## つまずき・学び
- 事象：
- 原因：
- 対策：
- 次回への注意：

## KNOWLEDGE候補（昇格するなら）
- （反復しそう／時間がかかった／定石化した）

## 次のTODO（1〜3個）
- [ ] シンプル構成でリポジトリ構造を実装する
