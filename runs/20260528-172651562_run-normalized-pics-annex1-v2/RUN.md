# PIC/S Annex 1 正規化RUN v2

## 概要

- run_id: `20260528-172651562_run-normalized-pics-annex1-v2`
- branch: `run/normalized-pics-annex1-v2`
- doc_id: `pics_pe00917_annex1_20230825`
- 対象: PIC/S GMP Guide PE 009-17 Annex 1 Manufacture of sterile medicinal products
- 入力: `data/human-readable/pics/pe009-17_annex1_2023-08-25_en.txt`
- source_url: `https://picscheme.org/docview/8881`
- retrieved_at: `2026-02-18`
- 生成コミット: `3e70d16d0484c433f4debc3bdf23946b4f081b08`

## 前提

PR #196でPIC/S Annex 1の全表についてPDF画像ベースの目検確認を実施し、結合セル・折返しセルの復元メタデータとTable 4のGrade帰属修正をmainへ反映済み。

## 実行

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.cli bundle --input data/human-readable/pics/pe009-17_annex1_2023-08-25_en.txt --out-dir runs/20260528-172651562_run-normalized-pics-annex1-v2/promotion_candidate --doc-id pics_pe00917_annex1_20230825 --title "PIC/S GMP Guide (PE 009-17) Annex 1 Manufacture of sterile medicinal products (25 August 2023)" --short-title "PIC/S PE009-17 Annex 1" --doc-type guideline --source-url https://picscheme.org/docview/8881 --source-format pdf --retrieved-at 2026-02-18 --parser-profile src/qai_text2ir/profiles/pics_annex1_default_v2.yaml --jurisdiction INTL --language en --family PICS --pics-doc-id "PE 009-17 (Annexes)" --strict --write-manifest --overwrite-manifest
```

## 出力

- `runs/20260528-172651562_run-normalized-pics-annex1-v2/promotion_candidate/pics_pe00917_annex1_20230825.regdoc_ir.yaml`
- `runs/20260528-172651562_run-normalized-pics-annex1-v2/promotion_candidate/pics_pe00917_annex1_20230825.parser_profile.yaml`
- `runs/20260528-172651562_run-normalized-pics-annex1-v2/promotion_candidate/pics_pe00917_annex1_20230825.regdoc_profile.yaml`
- `runs/20260528-172651562_run-normalized-pics-annex1-v2/promotion_candidate/pics_pe00917_annex1_20230825.meta.yaml`
- `runs/20260528-172651562_run-normalized-pics-annex1-v2/promotion_candidate/manifest.yaml`

## 検証

- `qualitycheck.warnings_count`: `0`
- `goal_check`: `PASS`
- `goal_check warnings`: `none`
- schema: `qai.regdoc_ir.v4`
- node_count: `615`
- source span coverage: `1.0`
- special_structure_audit: `pass`
- source_tables: `6`
- generated_tables: `6`
- generated_rows: `35`
- unresolved_count: `0`

## 表セル確認

- Table 1/5: 二段ヘッダとGrade Dの折返しセルがレビュー済みメタデータとして反映されている。
- Table 2/6: Grade Aの横結合No growthセルが各測定法列へ展開され、展開元メタデータが反映されている。
- Table 3/4: Grade列の縦結合セルが各操作レコードへ展開されている。
- Table 4: 目検で確認したGrade B/Dの帰属修正が反映されている。
  - `Background support for grade A (when not in an isolator).` は Grade B
  - `Cleaning of equipment.` は Grade D
  - `Handling of components, equipment and accessories after cleaning.` は Grade D

## テスト

- `python -m pytest tests\test_pics_annex1_tables.py -q`
  - `9 passed`

## レビュー用サンプル

- `runs/20260528-172651562_run-normalized-pics-annex1-v2/SAMPLE_EXTRACT.md`
- target_nid: `ann1.sec8.tbl4.tblh.tblr12`
- 抽出対象: `Grade D | Cleaning of equipment.`

## 昇格

この親PRでは `data/normalized/` は変更しない。承認後、子PRで `promotion_candidate` から `data/normalized/pics_pe00917_annex1_20230825/` へ複写する。
