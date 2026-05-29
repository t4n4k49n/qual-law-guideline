# 原薬GMPガイドライン 正規化候補 v3

## まとめ

原薬GMPガイドラインを、条文見出しの親子関係と表1のセル構造を保った正式候補として再生成しました。これにより、チェックシート利用時に本文の見出し文脈をたどれるだけでなく、表1も生産形態ごとの工程セルと適用対象工程を確認できる形でレビューできます。

## 変更内容

- `runs/20260529-114214346_run-normalized-api-gmp-guideline-v3/promotion_candidate/` に正規化候補4ファイルとmanifestを追加。
- 表1レビュー結果をRUNに記録。
- 深い階層サンプルを2件追加。
- `data/normalized/` は変更しない。

## 対象

- doc_id: `jp_pmda_api_gmp_guideline_20011102`
- source: `data/human-readable/pmda/api_gmp_guideline/source_texts/000156438.txt`
- source URL: `https://www.pmda.go.jp/files/000156438.pdf`
- parser profile: `src/qai_text2ir/profiles/jp_pmda_api_gmp_guideline_v1.yaml`

## 前提

- Headingレビュー修正PR `#213` をmainへ取り込み済み。
- 表1視覚レビュー修正PR `#215` をmainへ取り込み済み。
- 旧正規化候補PR `#214` は表1不備のため取り下げ済み。
- このPRは修正後mainからfreshに生成。

## 確認

- GOAL check: pass
- Special structure audit: pass
- Source span coverage: `1.0`
- Nodes: `496`
- Tables: `1`
- Table rows: `7`
- Focused tests: `18 passed`
- Full tests: `253 passed, 1 skipped`

## 表1確認

- 表1はraw 26行ではなく、7件のvisual-reviewed `table_row`。
- 各行に6セルの `cells` を保持。
- 灰色セルは `guideline_applicable` で保持。
- `ＧＭＰ要求事項の増大` はtable-level `visual_notes` に保持。

## 深い階層サンプル

- Table sample: `runs/20260529-114214346_run-normalized-api-gmp-guideline-v3/SAMPLE_EXTRACT_TABLE1.md`
- Text hierarchy sample: `runs/20260529-114214346_run-normalized-api-gmp-guideline-v3/SAMPLE_EXTRACT.md`

## 昇格境界

このPRは親PRです。`data/normalized/` への複写は含めません。

承認・マージ後に、子PRで `promotion_candidate/` の4ファイルのみを `data/normalized/jp_pmda_api_gmp_guideline_20011102/` へ複写します。

<!-- PR_BODY_FILE: runs/20260529-114214346_run-normalized-api-gmp-guideline-v3/PR.md -->
