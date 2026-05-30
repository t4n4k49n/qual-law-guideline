# RUN: NIID病原体等安全管理規程 正規化RUN v4

## 目的

NIID病原体等安全管理規程の正規化候補を、表全件の目検レビューを前提に作り直す。v2/v3では別表4、別表5、別表8を raw-hold として扱っており、表レビューとして不十分だったため、このrunでは列付き表として復元する。

## 入力

- source text: `data/human-readable/niid/pathogen_safety_management/source_texts/Kanrikitei3_20240401.txt`
- source PDF: `https://www.niid.go.jp/niid/images/cepr/kanrikitei/Kanrikitei3_20240401.pdf`
- doc_id: `jp_niid_pathogen_safety_management_20240401`

## 実行

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.cli bundle --input data/human-readable/niid/pathogen_safety_management/source_texts/Kanrikitei3_20240401.txt --out-dir runs/20260530-233420456_run-normalized-niid-pathogen-safety-v4/promotion_candidate --doc-id jp_niid_pathogen_safety_management_20240401 --title "国立感染症研究所病原体等安全管理規程" --short-title "NIID病原体等安全管理規程" --doc-type regulation --source-url https://www.niid.go.jp/niid/images/cepr/kanrikitei/Kanrikitei3_20240401.pdf --source-format pdf --retrieved-at 2026-02-18 --parser-profile src/qai_text2ir/profiles/jp_niid_pathogen_safety_management_full_v1.yaml --candidate-visibility-profile src/qai_text2ir/candidate_visibility_profiles/jp_niid_pathogen_safety_management_full_visibility_v1.yaml --jurisdiction JP --language ja --family JP_GUIDELINE --strict --write-manifest --overwrite-manifest
```

## 修正内容

- 付表2の table heading が途中で切れる問題を修正。
- 別表4、別表5、別表8を raw text ではなく visual reviewed table として復元。
- 付表2、付表3、付表4、別表4、別表5、別表7、別表8、別表10の全表をレビュー対象として記録。
- 番号付き項目の分割、注記抽出、孤立 `。` 除去、本文内番号連結監査は継続。

## 検証

- goal check: PASS
- special structure audit: PASS
- structure check: PASS
- focused tests: `13 passed`
- full tests: `257 passed, 1 skipped`
- 個人環境パス検査: PASS

## 昇格方針

この親PRでは `data/normalized/` は変更しない。承認後、子PRで `promotion_candidate/` の4ファイルのみを `data/normalized/jp_niid_pathogen_safety_management_20240401/` に複写する。

