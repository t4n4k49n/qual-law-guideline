# RUN

run_id: 20260204-181132107_feat-repo-structure
branch: feat/repo-structure
started_at: 2026-02-04 18:11 (JST)

## 目的（1文）
- コードと出力を同時に版管理するシンプル構成をリポジトリに追加する。

## Done Definition（完了条件）
- [x] データ/コードの基本構成ディレクトリを作成
- [x] REFERENCE.md と README.md に構成の記載を追加
- [x] TODO.md のブランチ表記を更新

## 重要：文字化け回避（UTF-8遵守）
- テキストは UTF-8（BOMなし）、改行はLF

## 手順（やった順）
1) run/out を作成
2) data/normalized, data/registry, data/releases, pipelines を追加
3) REFERENCE/README を更新
4) TODO.md の Current Branch を更新

## 実行コマンド（コピペで再現できる形）
- `git checkout -b feat/repo-structure`
- `Get-Date -Format yyyyMMdd-HHmmssfff`
- `python -`（run/out/構成ディレクトリ作成）

## 結果（事実ベース）
- 何ができた：シンプル構成ディレクトリの追加とドキュメント反映
- 何ができなかった：
- 数値（処理時間/件数/フレーム数など）：

## 生成物（上書き禁止）
- `out/20260204-181132107_feat-repo-structure/`

## 影響範囲（変更点）
- 変更ファイル：`docs/REFERENCE.md`, `README.md`, `TODO.md`
- ふるまいの変更：リポジトリの基本構成を追加

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
- [ ] IRスキーマの確定
