# 原薬GMPガイドライン 正規化RUN v4

## まとめ

原薬GMPガイドラインの正規化候補をfreshに作成しました。直前に承認された表1の目検修正を反映し、表1は7件のtable_row、結合ヘッダは `形態ごとの生産工程の事例 STEP 1..5` として確認できる状態です。

## 対象

- doc_id: `jp_pmda_api_gmp_guideline_20011102`
- source PDF URL: `https://www.pmda.go.jp/files/000156438.pdf`
- promotion candidate: `runs/20260529-122605989_run-normalized-api-gmp-guideline-v4/promotion_candidate/`
- parser profile: `jp_pmda_api_gmp_guideline_v1`
- schema: `qai.regdoc_ir.v4`

## 変更内容

- `promotion_candidate/` に正規化候補5ファイルを生成。
  - `jp_pmda_api_gmp_guideline_20011102.regdoc_ir.yaml`
  - `jp_pmda_api_gmp_guideline_20011102.parser_profile.yaml`
  - `jp_pmda_api_gmp_guideline_20011102.regdoc_profile.yaml`
  - `jp_pmda_api_gmp_guideline_20011102.meta.yaml`
  - `manifest.yaml`
- RUN記録、GOAL check、special structure audit、深い階層サンプル、表1確認メモを追加。
- `data/normalized/` は変更していません。

## 表1確認

- table: `1`
- table_header: `1`
- table_row: `7`
- header: `生産形態 | 形態ごとの生産工程の事例 STEP 1 | ... | 形態ごとの生産工程の事例 STEP 5`
- merged header metadata: `header_structure.spanning_headers`
- PDF下段見出し: `stage_labels`

詳細は `TABLE1_REVIEW.md` を参照してください。

## 深い階層サンプル

`SAMPLE_EXTRACT.md` より:

| 階層 | nid | kind | text / heading |
|---:|---|---|---|
| 1 | `root` | `document` |  |
| 2 | `cha2` | `chapter` | `品質マネージメント` |
| 3 | `cha2.sec2_2` | `section` | `品質部門の責任` |
| 4 | `cha2.sec2_2.p2_22` | `paragraph` | `独立した品質部門の主要な責任は委任しないこと。その責任は文書化され、かつ、 以下の事項を含むこと。` |
| 5 | `cha2.sec2_2.p2_22.i15` | `item` | `製品の品質の照査を実施すること(第2.5章で規定)。` |

## 検証結果

- GOAL check: pass
- Special structure audit: pass
- Source span coverage: `1.0`
- Generated nodes: `496`
- Focused tests: `10 passed`
- Full tests: `253 passed, 1 skipped`

## 注意

これは正規化RUNの親PRです。レビュー対象は `runs/20260529-122605989_run-normalized-api-gmp-guideline-v4/promotion_candidate/` です。

承認後に、子PRで `promotion_candidate/` から `data/normalized/jp_pmda_api_gmp_guideline_20011102/` へ昇格します。

<!-- PR_BODY_FILE: runs/20260529-122605989_run-normalized-api-gmp-guideline-v4/PR.md -->
