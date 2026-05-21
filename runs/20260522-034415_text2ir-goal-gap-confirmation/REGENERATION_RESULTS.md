# REGENERATION_RESULTS

## 結論

代表9文書はすべて現行最終profileで再生成でき、`--qualitycheck --strict` は全件 exit 0。4ファイル、manifest、v4 schema、source_spans、nid/ord検証も全件で確認できた。CFR Part 11 / Part 211 は現行repo内入力がなく未実行。

## 結果一覧

| 文書 | 入力 | profile | exit | 4ファイル | manifest | schema | verify | warnings | nodes | kind別件数 | source_spans | table/note |
|---|---|---|---:|---|---|---|---|---:|---:|---|---|---|
| EU GMP Vol.4 Chapter 1 | `data/human-readable/eu_gmp/vol4/chap1_2013-01_en.txt` | `src/qai_text2ir/profiles/eu_gmp_chap1_default_v2.yaml` | 0 | yes | yes | `qai.regdoc_ir.v4` | pass | 0 | 72 | chapter:1, document:1, item:50, paragraph:13, preamble:1, subitem:6 | 71/72 nodes | table 0, row 0, note 0 |
| PIC/S Annex 11 | `data/human-readable/pics/pe009-17_annex11_2023-08-25_en.txt` | `src/qai_text2ir/profiles/pics_annex11_default_v1.yaml` | 0 | yes | yes | `qai.regdoc_ir.v4` | pass | 0 | 42 | annex:1, document:1, item:3, paragraph:20, section:17 | 41/42 nodes | table 0, row 0, note 0 |
| PIC/S PE 009-17 Annex 15 | `data/human-readable/pics/pe009-17_annex15_2023-08-25_en.txt` | `src/qai_text2ir/profiles/pics_annex15_default_v1.yaml` | 0 | yes | yes | `qai.regdoc_ir.v4` | pass | 0 | 142 | annex:1, document:1, item:28, paragraph:100, section:12 | 141/142 nodes | table 0, row 0, note 0 |
| PIC/S Annex 1 | `data/human-readable/pics/pe009-17_annex1_2023-08-25_en.txt` | `src/qai_text2ir/profiles/pics_annex1_default_v2.yaml` | 0 | yes | yes | `qai.regdoc_ir.v4` | pass | 0 | 552 | annex:1, document:1, item:224, paragraph:294, section:10, subitem:22 | 551/552 nodes | table 0, row 0, note 0 |
| PIC/S Annex 2A | `data/human-readable/pics/pe009-17_annex2a_2023-08-25_en.txt` | `src/qai_text2ir/profiles/pics_annex2a_default_v1.yaml` | 0 | yes | yes | `qai.regdoc_ir.v4` | pass | 0 | 202 | annex:1, chapter:2, document:1, item:74, paragraph:102, section:11, subitem:11 | 201/202 nodes | table 0, row 0, note 0 |
| PIC/S PE 009-17 Annexes全体 refined | `data/human-readable/pics/pe009-17_annexes_2023-08-25_en.txt` | `src/qai_text2ir/profiles/pics_annexes_default_v3.yaml` | 0 | yes | yes | `qai.regdoc_ir.v4` | pass | 0 | 1748 | annex:19, chapter:2, document:1, item:442, paragraph:647, preamble:1, section:558, subitem:78 | 1747/1748 nodes | table 0, row 0, note 0 |
| PIC/S PE 009-17 Part I | `data/human-readable/pics/pe009-17_part1_2023-08-25_en.txt` | `src/qai_text2ir/profiles/pics_part1_default_v3.yaml` | 0 | yes | yes | `qai.regdoc_ir.v4` | pass | 0 | 342 | chapter:9, document:1, item:114, paragraph:211, preamble:1, subitem:6 | 341/342 nodes | table 0, row 0, note 0 |
| PIC/S PE 009-17 Part II | `data/human-readable/pics/pe009-17_part2_2023-08-25_en.txt` | `src/qai_text2ir/profiles/pics_part2_default_v1.yaml` | 0 | yes | yes | `qai.regdoc_ir.v4` | pass | 0 | 591 | chapter:20, document:1, item:25, paragraph:353, preamble:1, section:87, subitem:104 | 590/591 nodes | table 0, row 0, note 0 |
| WHO LBM 3rd | `data/human-readable/who/WHO_LBM_3rd.txt` | `src/qai_text2ir/profiles/who_lbm_3rd_default_v4.yaml` | 0 | yes | yes | `qai.regdoc_ir.v4` | pass | 0 | 829 | annex:5, chapter:22, document:1, item:754, part:9, preamble:1, subitem:37 | 828/829 nodes | table 0, row 0, note 0 |

## 実行コマンド

### EU GMP Vol.4 Chapter 1

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.cli --input data\human-readable\eu_gmp\vol4\chap1_2013-01_en.txt --out-dir out\20260522-034415_text2ir-goal-gap-confirmation\eu_gmp_vol4_chap1_20130131 --doc-id eu_gmp_vol4_chap1_20130131 --title "EU GMP Vol.4 Chapter 1 Pharmaceutical Quality System" --short-title "EU GMP Ch1 PQS" --doc-type guideline --source-format pdf --retrieved-at 2026-02-18 --jurisdiction EU --language en --family EU_GMP --parser-profile src\qai_text2ir\profiles\eu_gmp_chap1_default_v2.yaml --qualitycheck --strict --write-manifest --overwrite-manifest --emit-only all --eu-volume 4 --source-url https://health.ec.europa.eu/document/download/e458c423-f564-4171-b344-030a461c567f_en
```

### PIC/S Annex 11

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.cli --input data\human-readable\pics\pe009-17_annex11_2023-08-25_en.txt --out-dir out\20260522-034415_text2ir-goal-gap-confirmation\pics_pe00917_annex11_20230825 --doc-id pics_pe00917_annex11_20230825 --title "PIC/S GMP Guide (PE 009-17) Annex 11 Computerised systems (25 August 2023)" --short-title "PIC/S PE009-17 Annex 11" --doc-type guideline --source-format pdf --retrieved-at 2026-02-18 --jurisdiction INTL --language en --family PICS --parser-profile src\qai_text2ir\profiles\pics_annex11_default_v1.yaml --qualitycheck --strict --write-manifest --overwrite-manifest --emit-only all --pics-doc-id "PE 009-17 (Annexes)" --source-url https://picscheme.org/docview/8881
```

### PIC/S PE 009-17 Annex 15

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.cli --input data\human-readable\pics\pe009-17_annex15_2023-08-25_en.txt --out-dir out\20260522-034415_text2ir-goal-gap-confirmation\pics_pe00917_annex15_20230825 --doc-id pics_pe00917_annex15_20230825 --title "PIC/S GMP Guide (PE 009-17) Annex 15 Qualification and validation (25 August 2023)" --short-title "PIC/S PE009-17 Annex 15" --doc-type guideline --source-format pdf --retrieved-at 2026-02-18 --jurisdiction INTL --language en --family PICS --parser-profile src\qai_text2ir\profiles\pics_annex15_default_v1.yaml --qualitycheck --strict --write-manifest --overwrite-manifest --emit-only all --pics-doc-id "PE 009-17 (Annexes)" --source-url https://picscheme.org/docview/8881
```

### PIC/S Annex 1

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.cli --input data\human-readable\pics\pe009-17_annex1_2023-08-25_en.txt --out-dir out\20260522-034415_text2ir-goal-gap-confirmation\pics_pe00917_annex1_20230825 --doc-id pics_pe00917_annex1_20230825 --title "PIC/S GMP Guide (PE 009-17) Annex 1 Manufacture of sterile medicinal products (25 August 2023)" --short-title "PIC/S PE009-17 Annex 1" --doc-type guideline --source-format pdf --retrieved-at 2026-02-18 --jurisdiction INTL --language en --family PICS --parser-profile src\qai_text2ir\profiles\pics_annex1_default_v2.yaml --qualitycheck --strict --write-manifest --overwrite-manifest --emit-only all --pics-doc-id "PE 009-17 (Annexes)" --source-url https://picscheme.org/docview/8881
```

### PIC/S Annex 2A

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.cli --input data\human-readable\pics\pe009-17_annex2a_2023-08-25_en.txt --out-dir out\20260522-034415_text2ir-goal-gap-confirmation\pics_pe00917_annex2a_20230825 --doc-id pics_pe00917_annex2a_20230825 --title "PIC/S GMP Guide (PE 009-17) Annex 2A Manufacture of ATMP biological medicinal substances and products for human use (25 August 2023)" --short-title "PIC/S PE009-17 Annex 2A" --doc-type guideline --source-format pdf --retrieved-at 2026-02-18 --jurisdiction INTL --language en --family PICS --parser-profile src\qai_text2ir\profiles\pics_annex2a_default_v1.yaml --qualitycheck --strict --write-manifest --overwrite-manifest --emit-only all --pics-doc-id "PE 009-17 (Annexes)" --source-url https://picscheme.org/docview/8881
```

### PIC/S PE 009-17 Annexes全体 refined

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.cli --input data\human-readable\pics\pe009-17_annexes_2023-08-25_en.txt --out-dir out\20260522-034415_text2ir-goal-gap-confirmation\pics_pe00917_annexes_20230825_refined_v3_extends_trace --doc-id pics_pe00917_annexes_20230825_refined_v3_extends_trace --title "PIC/S PE 009-17 Annexes (25 August 2023) refined v3 extends trace" --short-title "PICS Annexes trace" --doc-type guideline --source-format pdf --retrieved-at 2026-02-18 --jurisdiction INTL --language en --family PICS --parser-profile src\qai_text2ir\profiles\pics_annexes_default_v3.yaml --qualitycheck --strict --write-manifest --overwrite-manifest --emit-only all --pics-doc-id "PE 009-17 (Annexes)" --source-url https://picscheme.org/docview/8881
```

### PIC/S PE 009-17 Part I

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.cli --input data\human-readable\pics\pe009-17_part1_2023-08-25_en.txt --out-dir out\20260522-034415_text2ir-goal-gap-confirmation\pics_pe00917_part1_20230825 --doc-id pics_pe00917_part1_20230825 --title "PIC/S GMP Guide (PE 009-17) Part I (25 August 2023)" --short-title "PIC/S PE009-17 Part I" --doc-type guideline --source-format pdf --retrieved-at 2026-02-18 --jurisdiction INTL --language en --family PICS --parser-profile src\qai_text2ir\profiles\pics_part1_default_v3.yaml --qualitycheck --strict --write-manifest --overwrite-manifest --emit-only all --pics-doc-id "PE 009-17 (Part I)" --source-url https://picscheme.org/docview/6606
```

### PIC/S PE 009-17 Part II

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.cli --input data\human-readable\pics\pe009-17_part2_2023-08-25_en.txt --out-dir out\20260522-034415_text2ir-goal-gap-confirmation\pics_pe00917_part2_20230825 --doc-id pics_pe00917_part2_20230825 --title "PIC/S GMP Guide (PE 009-17) Part II (25 August 2023)" --short-title "PIC/S PE009-17 Part II" --doc-type guideline --source-format pdf --retrieved-at 2026-02-18 --jurisdiction INTL --language en --family PICS --parser-profile src\qai_text2ir\profiles\pics_part2_default_v1.yaml --qualitycheck --strict --write-manifest --overwrite-manifest --emit-only all --pics-doc-id "PE 009-17 (Part II)" --source-url https://picscheme.org/docview/6607
```

### WHO LBM 3rd

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.cli --input data\human-readable\who\WHO_LBM_3rd.txt --out-dir out\20260522-034415_text2ir-goal-gap-confirmation\who_lbm_3rd_2004_9241546506 --doc-id who_lbm_3rd_2004_9241546506 --title "WHO Laboratory biosafety manual, 3rd edition (2004)" --short-title "WHO LBM 3rd" --doc-type guideline --source-format pdf --retrieved-at 2026-02-18 --jurisdiction WHO --language en --family WHO --parser-profile src\qai_text2ir\profiles\who_lbm_3rd_default_v4.yaml --qualitycheck --strict --write-manifest --overwrite-manifest --emit-only all --who-publication-id 9241546506 --source-url https://www.who.int/publications/i/item/9241546506
```

## 未実行

- CFR Part 11: 現行repo内に入力ファイルなし。`tests/fixtures/CFR_PART11_with_notes.txt` はfixtureであり代表文書全体ではないため、正式評価対象から外した。
- CFR Part 211: 現行repo内に入力ファイルなし。eCFR XML等の安定構造入力を使う拡張入口候補として扱う。
