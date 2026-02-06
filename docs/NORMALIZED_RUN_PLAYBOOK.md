# NORMALIZED RUN PLAYBOOK

正規化RUN（normalized run）を迷いなく実行するための手順書。
目的は `out/<run_id>/` の成果物を、正式版として `data/normalized/<doc_id>/<version>/` に昇格できる状態にすること。

## 0) 前提

- 入力はXMLのみを前提とする。
- 生成物は `out/<run_id>/` に出力し、上書きはしない。
- 正式版へ昇格する前に、レビューと検証の記録を残す。

## 1) 実行前確認

- 対象の入力XMLパスを確認
- `doc_id` と `version`（例: `20260501`）を決める
- ブランチ名と `run_id` を決める

## 2) 実行

例:
```bash
xml2ir bundle --input <path-to-xml> --out-dir out/<run_id> --doc-id <doc_id> --emit-only all
```

## 3) エラーハンドリング（最小）

- XMLのパス誤り → パスを修正して再実行
- 出力が欠けている → 再実行し、RUNに理由を記載
- 例外が出る → 例外ログを `runs/<run_id>/RUN.md` に記録し、作業停止

## 4) リリース確認（正規化チェック）

### 4-1) スキーマ検証（最小）

- `verify.py` の最小チェックを実行し、結果を記録
  - `assert_unique_nids`
  - `check_annex_article_nids`
  - `check_appendix_scoped_indices`

### 4-2) AIレビュー（目視代替）

- IRからサンプル断片を抽出し、AIに評価させる
- 出力は RUN に貼り付け、**人の最終確認はPRで行う前提**と明記する

### 4-3) PRでの最終目視（人間）

- PR本文に比較表を添付する
- 比較表のルール:
  - 最も深いitemを選ぶ
  - 同列のitemから最も文量が短いものを抽出
  - ヒューマンリーダブルとYAML構造を並列表記する

## 5) manifest.yaml の作成

- `out/<run_id>/manifest.yaml` を作成
- 入力元・コマンド・コミットハッシュ・検証/レビュー結果を記録

## 6) PR作成

- 変更内容、検証結果、AIレビュー結果をPR本文に記載
- 比較表（人間レビュー用）をPRに添付

## 7) 正式版への昇格

- PR承認後に `data/normalized/<doc_id>/<version>/` へコピー
- 既存版は残す（上書き禁止）
