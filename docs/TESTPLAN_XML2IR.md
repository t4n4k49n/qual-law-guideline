# TESTPLAN: XML2IR

## 目的
- e-Gov XML を RegDoc IR に変換する xml2ir パイプラインの品質を担保する
- 実データに対する最低限の健全性チェックを自動化する

## 対象
- `src/qai_xml2ir/egov_parser.py`
- `src/qai_xml2ir/cli.py`（`xml2ir bundle`）
- 生成物（IR / parser_profile / regdoc_profile / meta）

## 前提
- 実データXMLはリポジトリ外に配置する
- integration テストは環境変数が設定されている場合のみ実行する

## 手動スモーク手順
1. bundle の実行
```bash
xml2ir bundle --input C:\path\to\sample.xml --out-dir out\ --doc-id jp_sample
```
1. 生成物の存在確認
- `out\jp_sample.regdoc_ir.yaml`
- `out\jp_sample.parser_profile.yaml`
- `out\jp_sample.regdoc_profile.yaml`
- `out\jp_sample.meta.yaml`
1. YAMLの簡易確認
- `schema`, `doc_id`, `content` が存在すること

## 自動統合テスト手順
1. 環境変数を設定
```bash
$env:EGOV_XML_SAMPLE_1="C:\path\to\sample1.xml"
$env:EGOV_XML_SAMPLE_2="C:\path\to\sample2.xml"
```
1. integration テストを実行
```bash
.\.venv\Scripts\python.exe -m pytest -m integration
```

## 合否判定基準
- 生成物 4 ファイルがすべて出力される
- IR に `schema`, `doc_id`, `content` がある
- nid が一意である（重複なし）
- annex の article nid が `annexN.artX` 形式で、main と衝突しない
- appendix の nid が各スコープで 1 始まり（`appdx_*1`, `annexN.appdx_*1`）

## 観測するメトリクス
- 実行時間（pytest 実行時間）
- ノード総数と kind 別件数（`summarize_kinds`）
- unknown tag 警告数（log）

## 結果の保存
- 実行ログは `runs/<run_id>/RUN.md` に要約
- 必要に応じて kind 集計結果を `runs/<run_id>/` に保存
