# RUN: NIID病原体等安全管理規程 正規化RUN v2

## 目的

`jp_niid_pathogen_safety_management_20240401` のv1候補を破棄し、番号付き項目、表、heading、不要な本文連結を見直した親PR用候補を作り直す。

## 入力

- source text: `data/human-readable/niid/pathogen_safety_management/source_texts/Kanrikitei3_20240401.txt`
- source PDF: `https://www.niid.go.jp/niid/images/cepr/kanrikitei/Kanrikitei3_20240401.pdf`
- doc_id: `jp_niid_pathogen_safety_management_20240401`

## 実行

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.cli bundle --input data/human-readable/niid/pathogen_safety_management/source_texts/Kanrikitei3_20240401.txt --out-dir runs/20260530-224056777_run-normalized-niid-pathogen-safety-v2/promotion_candidate --doc-id jp_niid_pathogen_safety_management_20240401 --title "国立感染症研究所病原体等安全管理規程" --short-title "NIID病原体等安全管理規程" --doc-type regulation --source-url https://www.niid.go.jp/niid/images/cepr/kanrikitei/Kanrikitei3_20240401.pdf --source-format pdf --retrieved-at 2026-02-18 --parser-profile src/qai_text2ir/profiles/jp_niid_pathogen_safety_management_full_v1.yaml --candidate-visibility-profile src/qai_text2ir/candidate_visibility_profiles/jp_niid_pathogen_safety_management_full_visibility_v1.yaml --jurisdiction JP --language ja --family JP_GUIDELINE --strict --write-manifest --overwrite-manifest
```

## 修正内容

- `item_digit_dot` を有効化し、付表1-2、付表1-3、別表6、別表9の番号付き項目を item ノードに分割。
- raw-hold表の別表4、別表5、別表8では、表中の `0.01％` や `1分` を item として誤検出しないようにした。
- `註：` を note として抽出対象に追加。
- 孤立した `。` 行を除外し、`。。` の混入を防止。
- 別表1の導入文が heading に入る誤りを修正。

## 検証

- goal check: PASS
- special structure audit: PASS
- structure check: PASS
- focused tests: `8 passed`
- full tests: `257 passed, 1 skipped`
- 個人環境パス検査: PASS

## レビュー記録

- `STRUCTURE_TABLE_REVIEW.md`
- `GOAL_CHECK.md`
- `SPECIAL_STRUCTURE_AUDIT.md`

## 昇格方針

この親PRでは `data/normalized/` は変更しない。承認後、子PRで `promotion_candidate/` の4ファイルのみを `data/normalized/jp_niid_pathogen_safety_management_20240401/` に複写する。
