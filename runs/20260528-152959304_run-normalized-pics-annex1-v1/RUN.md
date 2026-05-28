# RUN: 20260528-152959304_run-normalized-pics-annex1-v1

## 目的

`pics_pe00917_annex1_20230825` を正規化RUNの親PRレビュー対象として `promotion_candidate/` に配置する。

このRUNは `docs/NORMALIZED_RUN_PLAYBOOK.md` の親PR/子PR運用を適用する。ただし、対象はe-Gov XMLではなく、`docs/NORMALIZATION_PLAN_10_12_13.md` でTXT入口と判断済みのPIC/S Annex 1である。

## ブランチ

- `run/normalized-pics-annex1-v1`

## 対象

- doc_id: `pics_pe00917_annex1_20230825`
- title: `PIC/S GMP Guide (PE 009-17) Annex 1 Manufacture of sterile medicinal products (25 August 2023)`
- input: `data/human-readable/pics/pe009-17_annex1_2023-08-25_en.txt`
- source_url: `https://picscheme.org/docview/8881`
- retrieved_at: `2026-02-18`
- parser_profile: `pics_annex1_default_v2`
- family: `PICS`

## 事前判断

`runs/20260528-102010880_review-pics-annex1-table-note/` で、Annex 1の表・注記レビューを通常RUNとして実施した。

- 初回確認で Table 2 / Table 4 / Table 6 にページフッター混入を検出した。
- PR #194で `src/qai_text2ir/pics_annex1_tables.py` を修正し、再発防止テストを追加した。
- 修正後の通常RUNで promotion GOAL がpassし、フッター残存検索も0件だった。

このため、今回の正規化RUNでは `out/` から昇格せず、現行mainの修正済みパーサで `promotion_candidate/` に再生成した。

## 実行

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.cli bundle `
  --input data/human-readable/pics/pe009-17_annex1_2023-08-25_en.txt `
  --out-dir runs/20260528-152959304_run-normalized-pics-annex1-v1/promotion_candidate `
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

- `runs/20260528-152959304_run-normalized-pics-annex1-v1/promotion_candidate/pics_pe00917_annex1_20230825.regdoc_ir.yaml`
- `runs/20260528-152959304_run-normalized-pics-annex1-v1/promotion_candidate/pics_pe00917_annex1_20230825.parser_profile.yaml`
- `runs/20260528-152959304_run-normalized-pics-annex1-v1/promotion_candidate/pics_pe00917_annex1_20230825.regdoc_profile.yaml`
- `runs/20260528-152959304_run-normalized-pics-annex1-v1/promotion_candidate/pics_pe00917_annex1_20230825.meta.yaml`
- `runs/20260528-152959304_run-normalized-pics-annex1-v1/promotion_candidate/manifest.yaml`
- `runs/20260528-152959304_run-normalized-pics-annex1-v1/promotion_candidate/GOAL_CHECK_RESULT.md`
- `runs/20260528-152959304_run-normalized-pics-annex1-v1/promotion_candidate/goal_check_result.json`
- `runs/20260528-152959304_run-normalized-pics-annex1-v1/SAMPLE_EXTRACT.md`

## 実行環境

- Python: `.\.venv\Scripts\python.exe`
- Python version: `3.11.6`
- lxml: `6.0.2`
- PyYAML: `6.0.3`
- typer: `0.24.0`
- base commit: `ec63e7522b1b866fe62fb12719a3525fae07fb05`

## 検証

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.goal_check `
  --bundle-dir runs/20260528-152959304_run-normalized-pics-annex1-v1/promotion_candidate `
  --doc-id pics_pe00917_annex1_20230825 `
  --mode promotion `
  --format markdown
```

結果:

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
- `dq_gmp_checklist.candidate_visibility`: `allow_rules: []` / `deny_rules: []`
- selectable_kinds: `subitem`, `item`, `paragraph`, `statement`, `table_row`

フッター残存検索:

```powershell
Select-String -Path runs/20260528-152959304_run-normalized-pics-annex1-v1/promotion_candidate/pics_pe00917_annex1_20230825.regdoc_ir.yaml -Pattern "PE 009-17|25 August 2023"
```

結果: 文書タイトル・メタデータ・manifest上の正当な文書識別文字列のみ。IR本文中のページフッター混入は0件。

関連テスト:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_pics_annex1_tables.py tests/test_text2ir_profiles_pics.py tests/test_pics_annexes_bundle_specials.py -q
```

結果:

- 18 passed

## AIレビュー（目視代替）

人の最終確認はPRで行う前提。今回の機械確認とサンプル確認では、Annex 1のannex、section、paragraph、table、table_header、table_rowが祖先関係を保って出力されている。

深い階層サンプル（`SAMPLE_EXTRACT.md` としてIR YAMLから抽出）:

| 階層 | nid | kind | kind_raw | text / heading |
|---:|---|---|---|---|
| 1 | `root` | `document` |  |  |
| 2 | `ann1` | `annex` | `ANNEX` | `MANUFACTURE OF STERILE MEDICINAL PRODUCTS` |
| 3 | `ann1.sec9` | `section` | `9` | `Environmental & process monitoring` |
| 4 | `ann1.sec9.p9_30` | `paragraph` | `9.30` | `Action limits for viable particle contamination are shown in Table 6.` |
| 5 | `ann1.sec9.p9_30.tbl6` | `table` | `table` | `Table 6: Maximum action limits for viable particle contamination` |
| 6 | `ann1.sec9.p9_30.tbl6.tblh` | `table_header` | `table_header` | `Grade | Air sample CFU/m3 | Settle plates (diameter 90 mm) CFU/4 hours (a) | Contact plates (diameter 55 mm) CFU/plate (b) | Glove print, including 5 fingers on both hands CFU/glove` |
| 7 | `ann1.sec9.p9_30.tbl6.tblh.tblr1` | `table_row` | `table_row` | `A | No growth (c) | No growth (c) | No growth (c) | No growth (c)` |

評価:

- 祖先経路は `document -> annex -> section -> paragraph -> table -> table_header -> table_row` として保持されている。
- `table_row` は `dq_gmp_checklist.selectable_kinds` に含まれる。
- Annex 1の表は6件、table_rowは35件、noteは16件として構造化されている。
- 通常RUNで検出したページフッター混入は今回の正本では再発していない。

## 昇格状態

- 親PR段階のため、`data/normalized/` への複写は未実施。
- 子PRは親PR承認後にのみ作成する。
