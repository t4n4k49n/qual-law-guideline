# RUN: 20260528-102010880_review-pics-annex1-table-note

## 目的

`pics_pe00917_annex1_20230825` を正規化RUNへ進められるか、通常RUNとして表・注記の構造化状態を確認する。

正規化RUNではなく、`promotion_candidate/` は作成しない。出力は `out/20260528-102010880_review-pics-annex1-table-note/` に置く。

## ブランチ

- `chore/archive-pics-annex11-v1-run`

## 対象

- doc_id: `pics_pe00917_annex1_20230825`
- title: `PIC/S GMP Guide (PE 009-17) Annex 1 Manufacture of sterile medicinal products (25 August 2023)`
- input: `data/human-readable/pics/pe009-17_annex1_2023-08-25_en.txt`
- source_url: `https://picscheme.org/docview/8881`
- retrieved_at: `2026-02-18`
- parser_profile: `src/qai_text2ir/profiles/pics_annex1_default_v2.yaml`
- family: `PICS`

## 実行

初回生成:

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.cli bundle `
  --input data/human-readable/pics/pe009-17_annex1_2023-08-25_en.txt `
  --out-dir out/20260528-102010880_review-pics-annex1-table-note/pics_pe00917_annex1_20230825 `
  --doc-id pics_pe00917_annex1_20230825 `
  --title "PIC/S GMP Guide (PE 009-17) Annex 1 Manufacture of sterile medicinal products (25 August 2023)" `
  --short-title "PIC/S PE009-17 Annex 1" `
  --doc-type guideline `
  --source-url https://picscheme.org/docview/8881 `
  --source-format pdf `
  --retrieved-at 2026-02-18 `
  --parser-profile src/qai_text2ir/profiles/pics_annex1_default_v2.yaml `
  --jurisdiction INTL `
  --language en `
  --family PICS `
  --pics-doc-id "PE 009-17 (Annexes)" `
  --strict `
  --write-manifest `
  --overwrite-manifest
```

初回確認で、Table 2のNote 4、Table 4の最終行、Table 6のNote 2にページフッターが混入していた。

対応:

- `src/qai_text2ir/pics_annex1_tables.py` の `PAGE_RE` を修正し、`PE 009-17 (Annexes)` 行を確実にページフッターとして扱うようにした。
- table `data.raw_lines` からもページフッターと繰り返しヘッダーを除外した。
- `tests/test_pics_annex1_tables.py` にフッター混入の再発防止テストを追加した。

修正後は上書き禁止のため、別ディレクトリに再生成した。

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.cli bundle `
  --input data/human-readable/pics/pe009-17_annex1_2023-08-25_en.txt `
  --out-dir out/20260528-102010880_review-pics-annex1-table-note/pics_pe00917_annex1_20230825_after_footer_fix `
  --doc-id pics_pe00917_annex1_20230825 `
  --title "PIC/S GMP Guide (PE 009-17) Annex 1 Manufacture of sterile medicinal products (25 August 2023)" `
  --short-title "PIC/S PE009-17 Annex 1" `
  --doc-type guideline `
  --source-url https://picscheme.org/docview/8881 `
  --source-format pdf `
  --retrieved-at 2026-02-18 `
  --parser-profile src/qai_text2ir/profiles/pics_annex1_default_v2.yaml `
  --jurisdiction INTL `
  --language en `
  --family PICS `
  --pics-doc-id "PE 009-17 (Annexes)" `
  --strict `
  --write-manifest `
  --overwrite-manifest
```

## 出力

- `out/20260528-102010880_review-pics-annex1-table-note/pics_pe00917_annex1_20230825/`
  - 初回出力。ページフッター混入あり。
- `out/20260528-102010880_review-pics-annex1-table-note/pics_pe00917_annex1_20230825_after_footer_fix/`
  - 修正後出力。正規化RUN候補として使うべき確認済み出力。
- `runs/20260528-102010880_review-pics-annex1-table-note/SAMPLE_COMPARISON.md`
- `runs/20260528-102010880_review-pics-annex1-table-note/GOAL_CHECK_RESULT.md`

## 検証

promotion goal:

- status: PASS
- schema: `qai.regdoc_ir.v4`
- nodes: 615
- verify: pass
- source span coverage: 1.0
- table: 6
- table_row: 35
- note: 16
- warnings: none
- errors: none

フッター残存検索:

```powershell
Select-String -Path out/20260528-102010880_review-pics-annex1-table-note/pics_pe00917_annex1_20230825_after_footer_fix/pics_pe00917_annex1_20230825.regdoc_ir.yaml -Pattern "PE 009-17|25 August 2023"
```

結果: 0件。

テスト:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_pics_annex1_tables.py -q
.\.venv\Scripts\python.exe -m pytest tests/test_pics_annex1_tables.py tests/test_text2ir_profiles_pics.py tests/test_pics_annexes_bundle_specials.py -q
```

結果:

- `tests/test_pics_annex1_tables.py`: 9 passed
- 関連テスト3ファイル: 18 passed

## 判断

修正後の `pics_pe00917_annex1_20230825` は、正規化RUNへ進めてよい。

次の正規化RUNでは、昇格候補の正本を `runs/<new_run_id>/promotion_candidate/` に再生成する。昇格元は今回の `out/` ではなく、正規化RUNの `promotion_candidate/` とする。
