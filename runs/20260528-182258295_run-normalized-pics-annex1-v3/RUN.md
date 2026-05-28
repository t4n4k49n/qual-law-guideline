# PIC/S Annex 1 正規化RUN v3

## 概要

- run_id: `20260528-182258295_run-normalized-pics-annex1-v3`
- branch: `run/normalized-pics-annex1-v3`
- doc_id: `pics_pe00917_annex1_20230825`
- 対象: PIC/S GMP Guide PE 009-17 Annex 1 Manufacture of sterile medicinal products
- 入力: `data/human-readable/pics/pe009-17_annex1_2023-08-25_en.txt`
- source_url: `https://picscheme.org/docview/8881`
- retrieved_at: `2026-02-18`
- 生成コミット: `e7bbe398c47a709df246aeccb118a6f74ac36a3c`

## 実行前提

- PR #196: 表セルの目検復元、Table 4 Grade帰属修正をmainへ反映済み。
- PR #198: Table 1/5の二段ヘッダを親ヘッダ込みの完全列名へ修正済み。
- `runs/20260528-182258295_run-normalized-pics-annex1-v3/` と `out/20260528-182258295_run-normalized-pics-annex1-v3/` をRUN開始時に同名作成済み。

## 実行

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.cli bundle --input data/human-readable/pics/pe009-17_annex1_2023-08-25_en.txt --out-dir runs/20260528-182258295_run-normalized-pics-annex1-v3/promotion_candidate --doc-id pics_pe00917_annex1_20230825 --title "PIC/S GMP Guide (PE 009-17) Annex 1 Manufacture of sterile medicinal products (25 August 2023)" --short-title "PIC/S PE009-17 Annex 1" --doc-type guideline --source-url https://picscheme.org/docview/8881 --source-format pdf --retrieved-at 2026-02-18 --parser-profile src/qai_text2ir/profiles/pics_annex1_default_v2.yaml --jurisdiction INTL --language en --family PICS --pics-doc-id "PE 009-17 (Annexes)" --strict --write-manifest --overwrite-manifest
```

## 出力

- `runs/20260528-182258295_run-normalized-pics-annex1-v3/promotion_candidate/pics_pe00917_annex1_20230825.regdoc_ir.yaml`
- `runs/20260528-182258295_run-normalized-pics-annex1-v3/promotion_candidate/pics_pe00917_annex1_20230825.parser_profile.yaml`
- `runs/20260528-182258295_run-normalized-pics-annex1-v3/promotion_candidate/pics_pe00917_annex1_20230825.regdoc_profile.yaml`
- `runs/20260528-182258295_run-normalized-pics-annex1-v3/promotion_candidate/pics_pe00917_annex1_20230825.meta.yaml`
- `runs/20260528-182258295_run-normalized-pics-annex1-v3/promotion_candidate/manifest.yaml`

## 検証

- `qualitycheck.warnings_count`: `0`
- `goal_check`: `PASS`
- `goal_check warnings`: `none`
- IR内のwarning/warn系メタデータ: `0`
- schema: `qai.regdoc_ir.v4`
- node_count: `615`
- source span coverage: `1.0`
- special_structure_audit: `pass`
- source_tables: `6`
- generated_tables: `6`
- generated_rows: `35`
- unresolved_count: `0`

## 表ヘッダ・結合セル確認

- Table 1 header:
  - `Grade | Maximum limits for total particle >= 0.5 µm/m3 at rest | Maximum limits for total particle >= 0.5 µm/m3 in operation | Maximum limits for total particle >= 5 µm/m3 at rest | Maximum limits for total particle >= 5 µm/m3 in operation`
- Table 5 header:
  - `Grade | Maximum limits for total particle >= 0.5 μm/m3 at rest | Maximum limits for total particle >= 0.5 μm/m3 in operation | Maximum limits for total particle >= 5 μm/m3 at rest | Maximum limits for total particle >= 5 μm/m3 in operation`
- Table 2/6: Grade Aの横結合No growthセルを各測定法列へ展開済み。
- Table 3/4: Grade列の縦結合セルを各操作レコードへ展開済み。
- Table 4: Grade B/Dの帰属修正を反映済み。

## テスト

- `python -m pytest tests\test_pics_annex1_tables.py -q`
  - `9 passed`

## レビュー用サンプル

- `runs/20260528-182258295_run-normalized-pics-annex1-v3/SAMPLE_EXTRACT.md`
- target_nid: `ann1.sec4.p4_27.tbl1.tblh`
- 抽出対象: Table 1の完全列名ヘッダ

## 昇格

この親PRでは `data/normalized/` は変更しない。承認後、子PRで `promotion_candidate` から `data/normalized/pics_pe00917_annex1_20230825/` へ複写する。

## 昇格準備

- 親PR: #199 merged
- 昇格専用ブランチ: `promote/pics-annex1-v3`
- 昇格元: `runs/20260528-182258295_run-normalized-pics-annex1-v3/promotion_candidate/`
- 昇格先: `data/normalized/pics_pe00917_annex1_20230825/`
- 複写対象: 4ファイルのみ
  - `pics_pe00917_annex1_20230825.regdoc_ir.yaml`
  - `pics_pe00917_annex1_20230825.parser_profile.yaml`
  - `pics_pe00917_annex1_20230825.regdoc_profile.yaml`
  - `pics_pe00917_annex1_20230825.meta.yaml`
- 複写後SHA-256: 昇格元と昇格先の4ファイルがすべて一致
