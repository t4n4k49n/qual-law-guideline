# RUN: 20260224-122811435_fix-egov-no-fold-article

- branch: fix/egov-no-fold-article
- purpose: fold廃止後の既存normalized IR影響調査（Article->Paragraph構造違反の可視化）

## 実施内容

1. `tools/check_ir_structure.py` を追加
   - 入力: IR YAMLファイル or ディレクトリ
   - 検査:
     - A: `article.text != null/empty`
     - B: `article` 直下に `item/subitem/point`
     - C: `article` 直下に `paragraph` 不在
   - 終了コード:
     - 問題なし: 0
     - 問題あり: 1

2. `tools/migrate_folded_article_ir.py` を追加（救済用）
   - 原則はXML再生成
   - XML再取得不可時のみ旧IRを移行可能

3. `data/normalized` 全件に対して構造チェック実行

## 実行コマンド

```powershell
.\.venv\Scripts\python.exe tools/check_ir_structure.py data/normalized
```

## 結果

- 判定: NG（問題あり）
- 主要ログ: `out/20260224-122811435_fix-egov-no-fold-article/check_ir_structure_data_normalized.txt`
- 問題IR一覧: `out/20260224-122811435_fix-egov-no-fold-article/problem_ir_files.txt`
- 対象doc_id一覧: `out/20260224-122811435_fix-egov-no-fold-article/problem_doc_ids.txt`

### 要再生成（fold由来の壊れIRが検出されたdoc_id）

- ARCHIVE_jp_egov_336M50000100002_20260501_507M60000100117
- jp_egov_335AC0000000145_20260501_507AC0000000037
- jp_egov_336CO0000000011_20260501_507CO0000000362
- jp_egov_336M50000100001_20260501_507M60000100117
- jp_egov_336M50000100002_20260501_507M60000100117
- jp_egov_416M60000100179_20260501_507M60000100117

## 方針

- 原則: XMLから `out/<run_id>/` に再生成し、レビュー後に `data/normalized` 更新
- 救済: XML再取得不可時のみ `tools/migrate_folded_article_ir.py` を使用
- 注意: NID変更（例: `art2.i1 -> art2.p1.i1`）に伴い、外部保存の参照ID更新が必要

## CI組み込みについて

- `tools/check_ir_structure.py data/normalized` はCIへ組み込み可能。
- ただし現時点で既存 `data/normalized` に違反が残るため、先に再生成完了が必要。

## 救済移行スクリプト検証（任意）

- 入力: `data/normalized/jp_egov_336M50000100002_20260501_507M60000100117/...regdoc_ir.yaml`
- 実行:
  - `tools/migrate_folded_article_ir.py --input <old_ir> --output <migrated_ir>`
  - `tools/check_ir_structure.py <migrated_ir>`
- 結果:
  - migrate: `articles=29`, `nids_rewritten=157`
  - check: `no structure problems found`
- ログ:
  - `out/20260224-122811435_fix-egov-no-fold-article/migrate_sample_log.txt`
  - `out/20260224-122811435_fix-egov-no-fold-article/check_migrated_sample.txt`

## 補足

- CIへの即時組み込みは可能だが、現時点の `data/normalized` に違反が残るため現状ではCIが失敗する。
- 先に対象doc_idの再生成（または救済移行）を完了させた後、CIチェックを有効化する。
