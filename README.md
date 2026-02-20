# qual-law-guideline

## 概要（1〜3行）
- 国内外の製薬クオリフィケーション関連の法令・ガイドラインを共通フォーマットに正規化し、YAMLで管理する。
- 原文（PDF/HTML/TXT/XML等）から中間表現（IR）を作り、条文の文脈を保持したまま参照できるようにする。
- 単一モノリポで、ソースデータから加工データまで一貫運用する。

## ゴール
- 法令・ガイドラインを共通IR（YAML）に正規化するスキーマと運用ルールを確立する。
- DQのGMPチェックシートに「条文選択肢」として提供できるデータ構造を用意する。
- 選択した条文に対して必要な親/先祖文脈を柔軟に表示できる構造を実現する。

## 非目標
- 最終的な適合性の判断や運用責任は本プロジェクトの範囲外とする。
- UIやSaaS本体の実装はこのリポジトリの初期スコープには含めない。

## 方針（固定）
- 1タスク=1run（runs/<run_id>/RUN.md）
- runs と out は同名運用
- 生成物は上書き禁止（タイムスタンプ付与）
- 知見は KNOWLEDGE.md に昇格

## 文字化け回避（UTF-8遵守）
- テキストは UTF-8（BOMなし）、改行はLF

## 次にやること
- TODO.md を参照

---

## xml2ir（e-Gov XML -> RegDoc）
e-Gov「日本法令XML」をRegDoc IRの4部セット（IR + parser_profile + regdoc_profile + meta）へ変換する最小パイプライン。

### 公式スキーマ（参照用）
- e-Gov法令XMLスキーマ: https://laws.e-gov.go.jp/docs/law-data-basic/419a603-xml-schema-for-japanese-law/

### 使い方
```bash
xml2ir bundle --input 416M60000100179_20260501_507M60000100117.xml --out-dir out/ \
  --doc-id jp_mhlw_gmp_ordinance \
  --short-title "GMP省令" \
  --retrieved-at 2026-02-02 \
  --source-url "https://laws.e-gov.go.jp/law/416M60000100179/20260501_507M60000100117"
```

### 出力（同一 out_dir に4ファイル）
- `{doc_id}.regdoc_ir.yaml`
- `{doc_id}.parser_profile.yaml`
- `{doc_id}.regdoc_profile.yaml`
- `{doc_id}.meta.yaml`

### 実データ統合テスト（任意）
環境変数で実XMLを指定すると integration テストが有効になる。
```bash
$env:EGOV_XML_SAMPLE_1="C:\\path\\to\\sample1.xml"
.\.venv\Scripts\python.exe -m pytest -m integration
```

## 指針ドキュメント
- `docs/REFERENCE.md`

## リポジトリ構成（シンプル案）
- `data/` 最新成果・索引・重要版
- `pipelines/` 本流の変換パイプライン

## README/TODO を埋めるためにユーザーへ依頼する情報（必須）
このREADME/TODOはプロジェクト内容に依存する。次のいずれかをユーザーに依頼して、情報が揃ってから追記すること。

- 資料アップロード：要件メモ、仕様、既存コード、対象データ例、期待する出力例 など
または
- 要点共有（文章でOK）：
  1) 目的（何を達成したいか）
  2) 入力（対象データ/形式/想定サイズ）
  3) 出力（成果物の形式/粒度）
  4) 制約（環境、ライブラリ縛り、性能目標、禁止事項）
  5) 優先順位（まず何を動かしたいか）
