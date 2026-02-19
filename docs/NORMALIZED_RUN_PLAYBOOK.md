# NORMALIZED RUN PLAYBOOK

正規化RUN（normalized run）を迷いなく実行するための手順書。
目的は `out/<run_id>/` の成果物を、正式版として `data/normalized/<doc_id>/` に昇格できる状態にすること。

## 0) 前提

- 入力はXMLのみを前提とする。
- 生成物は `out/<run_id>/` に出力し、上書きはしない。
- 正式版へ昇格する前に、レビューと検証の記録を残す。

## 1) 実行前確認

- 対象の入力XMLパスを確認
- **出力差分の管理方針（必須）**:
  - `schema` が同一でも、`qai_xml2ir` のパーサ実装や profile 変更により出力内容は変わり得る
  - table/note 拡張のような変更は「スキーマ改定」ではなく「パーサ/プロファイル改定」として扱う
  - 正規化RUNでは `schema` の一致だけで同一性を判断しない
- **機密情報対策（必須）**:
  - `RUN.md` / `PR.md` / PR本文に、`C:\Users\...` などの個人環境の絶対パスを書かない
  - パスは `%USERPROFILE%` などの環境変数表記、または `<workspace-relative-path>` を使う
  - 例:
    - NG: `%USERPROFILE%\Documents\...`
    - OK: `%USERPROFILE%\Documents\...`
- `doc_id` を決める
  - **e-GovのURIに準拠**: `jp_egov_<law_id>_<as_of(yyyymmdd)>_<revision_id>`
  - 例: `https://laws.e-gov.go.jp/law/336M50000100002/20260501_507M60000100117` → `jp_egov_336M50000100002_20260501_507M60000100117`
- ブランチ名と `run_id` を決める
- 正規化RUNのPRブランチは `run/normalized-...` 命名を使用する（CI判定キー）。
- 使用する実行環境を固定する
  - 推奨: `.venv` を利用し、Python と依存パッケージをプロジェクト単位で固定する
  - 例: `.venv\Scripts\python.exe -m pip install -e .[dev]`

## 2) 実行

例:
```bash
xml2ir bundle --input <path-to-xml> --out-dir out/<run_id> --doc-id <doc_id> --emit-only all
```

実行時に以下を `runs/<run_id>/RUN.md` または `out/<run_id>/manifest.yaml` へ記録する:
- `schema`（例: `qai.regdoc_ir.v3`）
- `parser_profile.id`（出力 `*.parser_profile.yaml` の `id`）
- `tool_version`（取得できる場合）
- 実行Python（例: `.venv\Scripts\python.exe`）
- 主要依存バージョン（最低: `lxml`, `PyYAML`, `typer`）

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
  - `check_ord_format_and_order`（ord存在/一意/単調増加）

### 4-2) AIレビュー（目視代替）

- IRからサンプル断片を抽出し、AIに評価させる
- 出力は RUN に貼り付け、**人の最終確認はPRで行う前提**と明記する

### 4-3) PRでの最終目視（人間）

- PR本文に比較表を添付する
- 比較表のルール:
  - 最も深いitemを選ぶ
  - 同列のitemから最も文量が短いものを抽出
  - ヒューマンリーダブルとYAML構造を並列表記する
  - **人間可読の経路は対象ノードの祖先をすべて含める**
  - **章/節/条/項/号/イロハ/枝番など、`num` がある階層は省略しない**
  - **YAML断片の `nid` から辿れる祖先数と人間可読の階層数が一致することを確認する**

## 5) manifest.yaml の作成

- `out/<run_id>/manifest.yaml` を作成
- 入力元・コマンド・コミットハッシュ・検証/レビュー結果を記録
- 追加で以下も記録する:
  - `schema`
  - `parser_profile.id`
  - `tool_version`（未設定なら未設定である旨）
  - 実行環境（Python実行ファイル、主要依存バージョン）

## 6) PR作成

- PR本文は `runs/<run_id>/PR.md` に作成する
- **PR.md のタイトルと表の見出しは日本語で書く**
- PRをあげる準備として、RUN系書類（`RUN.md` / `PR.md`）を `git add` しておく
- 変更内容、検証結果、AIレビュー結果をPR本文に記載
- 対象e-Gov法令URLを必ず記載する
  - 形式: `https://laws.e-gov.go.jp/law/<law_id>/<as_of_revision>`
  - 変換例: `416M60000100179_20260501_507M60000100117` → `https://laws.e-gov.go.jp/law/416M60000100179/20260501_507M60000100117`
- 比較表（人間レビュー用）をPRに添付
- PR作成前に、本文・`RUN.md`・`PR.md` から `C:\\Users\\` を検索し、0件であることを確認する
- **GitHubでPRを作成し、リンクを共有する**
- PR本文には昇格実施結果を書かない（昇格実施は承認後に `RUN.md` のみに記録する）

## 7) 正式版への昇格

- **PR承認が確認できたら** `data/normalized/<doc_id>/` を最新成果物で置換（上書き）する
- **承認前の `data/normalized/` 複写は厳禁**
- 昇格実施結果は `runs/<run_id>/RUN.md` に記録し、PR本文（`runs/<run_id>/PR.md`）は承認時点の内容を後追い更新しない
- `data/normalized/` の履歴管理はGit（commit/PR diff）で行う
- 昇格コミットをpushしたら、**同一PRに含めて `main` 反映まで完了させる**（昇格専用の別PRは作成しない）。
- 昇格完了条件（自動判定）:
  - `promotion_commit` が存在する
  - `promotion_commit` が `origin/main` の祖先である
  - 条件2が偽なら「未完了」で停止（完了報告禁止）
- 必須コマンド:
  - `git rev-parse --verify <promotion_commit>`
  - `git fetch origin`
  - `git merge-base --is-ancestor <promotion_commit> origin/main`
- 反映確認: `main` で `data/normalized/<doc_id>/` の更新を確認し、確認結果を `RUN.md` に追記する。
