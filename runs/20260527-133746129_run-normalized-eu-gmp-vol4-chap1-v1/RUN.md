# RUN: 20260527-133746129_run-normalized-eu-gmp-vol4-chap1-v1

## 目的

`eu_gmp_vol4_chap1_20130131` を正規化RUNの親PRレビュー対象として `promotion_candidate/` に配置する。

このRUNは `docs/NORMALIZED_RUN_PLAYBOOK.md` の親PR/子PR運用を適用する。ただし、対象はe-Gov XMLではなく、`docs/NORMALIZATION_PLAN_10_12_13.md` でTXT入口と判断済みのEU GMP Chapter 1である。

## ブランチ

- `run/normalized-eu-gmp-vol4-chap1-v1`

## 対象

- doc_id: `eu_gmp_vol4_chap1_20130131`
- title: `EU GMP Vol.4 Chapter 1 Pharmaceutical Quality System`
- input: `data/human-readable/eu_gmp/vol4/chap1_2013-01_en.txt`
- source_url: [EU GMP Vol.4 Chapter 1 PDF](https://health.ec.europa.eu/document/download/e458c423-f564-4171-b344-030a461c567f_en)
- retrieved_at: `2026-02-18`
- parser_profile: `eu_gmp_chap1_default_v2`
- family: `EU_GMP`

## 事前判断

`runs/20260527-105034029_docs-readiness-10-12-13-rerun/READINESS_10_12_13.md` で、EU GMP Chapter 1は次の理由により第一候補とした。

- `qualitycheck --strict`、GOAL、promotion GOALがpass。
- warningなし。
- table/noteなし。
- レビュー負荷が小さい。

## 実行

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.cli bundle `
  --input data/human-readable/eu_gmp/vol4/chap1_2013-01_en.txt `
  --out-dir runs/20260527-133746129_run-normalized-eu-gmp-vol4-chap1-v1/promotion_candidate `
  --doc-id eu_gmp_vol4_chap1_20130131 `
  --title "EU GMP Vol.4 Chapter 1 Pharmaceutical Quality System" `
  --short-title "EU GMP Ch1 PQS" `
  --doc-type guideline `
  --source-url https://health.ec.europa.eu/document/download/e458c423-f564-4171-b344-030a461c567f_en `
  --source-format pdf `
  --retrieved-at 2026-02-18 `
  --parser-profile-id eu_gmp_chap1_default_v2 `
  --jurisdiction EU `
  --language en `
  --family EU_GMP `
  --eu-volume 4 `
  --strict
```

## 出力

- `runs/20260527-133746129_run-normalized-eu-gmp-vol4-chap1-v1/promotion_candidate/eu_gmp_vol4_chap1_20130131.regdoc_ir.yaml`
- `runs/20260527-133746129_run-normalized-eu-gmp-vol4-chap1-v1/promotion_candidate/eu_gmp_vol4_chap1_20130131.parser_profile.yaml`
- `runs/20260527-133746129_run-normalized-eu-gmp-vol4-chap1-v1/promotion_candidate/eu_gmp_vol4_chap1_20130131.regdoc_profile.yaml`
- `runs/20260527-133746129_run-normalized-eu-gmp-vol4-chap1-v1/promotion_candidate/eu_gmp_vol4_chap1_20130131.meta.yaml`
- `runs/20260527-133746129_run-normalized-eu-gmp-vol4-chap1-v1/promotion_candidate/manifest.yaml`
- `runs/20260527-133746129_run-normalized-eu-gmp-vol4-chap1-v1/SAMPLE_EXTRACT.md`

## 実行環境

- Python: `.\.venv\Scripts\python.exe`
- lxml: `6.0.2`
- PyYAML: `6.0.3`
- typer: `0.24.0`
- base commit: `4d4c404aea0ca27bcb05cb854a1eca8282c0e45a`

## 検証

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.goal_check `
  --bundle-dir runs/20260527-133746129_run-normalized-eu-gmp-vol4-chap1-v1/promotion_candidate `
  --doc-id eu_gmp_vol4_chap1_20130131 `
  --mode promotion `
  --format markdown
```

結果:

- status: PASS
- schema: `qai.regdoc_ir.v4`
- nodes: 72
- verify: pass
- source span coverage: 1.0
- warnings: none
- errors: none
- `dq_gmp_checklist.candidate_visibility`: `allow_rules: []` / `deny_rules: []`
- selectable_kinds: `subitem`, `item`, `paragraph`, `statement`, `table_row`

## AIレビュー（目視代替）

人の最終確認はPRで行う前提。今回の機械確認とサンプル確認では、Chapter 1の章、段落、箇条が祖先関係を保って出力されている。

深い階層サンプル（`SAMPLE_EXTRACT.md` としてIR YAMLから抽出）:

- `root` / `document`
- `cha1` / `chapter` / `Chapter` / heading: `Pharmaceutical Quality System`
- `cha1.p1_8` / `paragraph` / `1.8`
- `cha1.p1_8.iiii` / `item` / `(iii)` / text: `All necessary facilities for GMP are provided including:`
- `cha1.p1_8.iiii.si3` / `subitem` / `•` / text: `Suitable equipment and services;`

評価:

- 祖先経路は `document -> chapter -> paragraph -> item -> subitem` として保持されている。
- `cha1.p1_8.iiii` は `item` のprefix `i` と `num: iii` を連結したNIDであり、`kind_raw` は `(iii)` として保持されている。
- `source_spans` coverageは1.0。
- 表・注記はこの文書では0件で、readiness判断と一致した。
- `meta.doc.family` は `EU_GMP` として出力され、旧warningの `meta_family_missing` は発生していない。

## 昇格状態

- 親PR段階のため、`data/normalized/` への複写は未実施。
- 子PRは親PR承認後にのみ作成する。

## 昇格実施

- 親PR: https://github.com/t4n4k49n/qual-law-guideline/pull/188
- 親PR merge commit: `afa3763`
- 昇格先: `data/normalized/eu_gmp_vol4_chap1_20130131/`
- 昇格元: `runs/20260527-133746129_run-normalized-eu-gmp-vol4-chap1-v1/promotion_candidate/`
- 昇格対象:
  - `eu_gmp_vol4_chap1_20130131.regdoc_ir.yaml`
  - `eu_gmp_vol4_chap1_20130131.parser_profile.yaml`
  - `eu_gmp_vol4_chap1_20130131.regdoc_profile.yaml`
  - `eu_gmp_vol4_chap1_20130131.meta.yaml`
- `manifest.yaml` は正規化RUN記録であり、`data/normalized/` へは複写しない。

昇格前確認:

- 4ファイルのSHA-256が `promotion_candidate/` と `data/normalized/` で一致することを確認した。
- 子PRではパーサコード修正、追加の正規化再実行、無関係なドキュメント更新を含めない。

昇格先検証:

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.goal_check `
  --bundle-dir data/normalized/eu_gmp_vol4_chap1_20130131 `
  --doc-id eu_gmp_vol4_chap1_20130131 `
  --mode promotion `
  --format markdown
```

結果:

- status: PASS
- schema: `qai.regdoc_ir.v4`
- nodes: 72
- verify: pass
- source span coverage: 1.0
- errors: none
- warning: `missing_manifest`
  - `manifest.yaml` はRUN記録であり、子PRの昇格複写対象4ファイルから除外するため想定どおり。

追加確認:

- `.\.venv\Scripts\python.exe -m pytest tests/test_extract_ir_sample.py -q`: PASS（3 passed）
