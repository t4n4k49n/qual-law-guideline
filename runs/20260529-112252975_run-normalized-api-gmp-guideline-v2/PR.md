# 原薬GMPガイドライン 正規化候補 v2

## まとめ

原薬GMPガイドラインを、条文見出しの親子関係を保った正式候補として再生成しました。これにより、チェックシート利用時に「品質部門の責任」「従業員の適格性」などの見出し文脈を含めて条文を参照でき、表1も適用範囲の文脈に接続された状態でレビューできます。

## 変更内容

- `runs/20260529-112252975_run-normalized-api-gmp-guideline-v2/promotion_candidate/` に正規化候補4ファイルとmanifestを追加。
- Heading/Tableレビュー結果をRUNに記録。
- 深い階層サンプルを追加。
- `data/normalized/` は変更しない。

## 対象

- doc_id: `jp_pmda_api_gmp_guideline_20011102`
- source: `data/human-readable/pmda/api_gmp_guideline/source_texts/000156438.txt`
- source URL: `https://www.pmda.go.jp/files/000156438.pdf`
- parser profile: `src/qai_text2ir/profiles/jp_pmda_api_gmp_guideline_v1.yaml`

## 前提

- Heading/Tableレビュー修正PR `#213` をmainへ取り込み済み。
- 旧 `20260525-121645707_run-normalized-api-gmp-guideline-v1` の候補は使わず、修正後mainからfreshに生成。

## 確認

- GOAL check: pass
- Special structure audit: pass
- Source span coverage: `1.0`
- Nodes: `515`
- Tables: `1`
- Table rows: `26`
- Heading-like short `paragraph`: `0`
- Focused tests: `20 passed`
- Full tests: `253 passed, 1 skipped`

## Heading / Table確認

- `2.1 原則` 配下に `2.10` 以降が入ることを確認。
- `3.1 従業員の適格性` 配下に `3.10` 以降が入ることを確認。
- `12.3 適格性評価` 配下に `12.30` が入ることを確認。
- `1.3 適用範囲` 配下に表1が残ることを確認。
- 見出しがない章13/15/16はparagraphを章直下に保持。

## 深い階層サンプル

`runs/20260529-112252975_run-normalized-api-gmp-guideline-v2/SAMPLE_EXTRACT.md` に記録。

対象: `cha2.sec2_2.p2_22.i15`

```text
root -> cha2 -> cha2.sec2_2 -> cha2.sec2_2.p2_22 -> cha2.sec2_2.p2_22.i15
```

## 昇格境界

このPRは親PRです。`data/normalized/` への複写は含めません。

承認・マージ後に、子PRで `promotion_candidate/` の4ファイルのみを `data/normalized/jp_pmda_api_gmp_guideline_20011102/` へ複写します。

<!-- PR_BODY_FILE: runs/20260529-112252975_run-normalized-api-gmp-guideline-v2/PR.md -->
