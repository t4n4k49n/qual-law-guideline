# RUN: 20260525-121645707_run-normalized-api-gmp-guideline-v1

## 目的

`docs/NORMALIZATION_PLAN_6_9.md` のフェーズ2として、6「原薬GMPガイドライン」を正規化する。

親PRでは `runs/20260525-121645707_run-normalized-api-gmp-guideline-v1/promotion_candidate/` の4ファイルとmanifestをレビュー対象とし、`data/normalized/` は変更しない。

## 入力

- 原ソース: `data/human-readable/pmda/api_gmp_guideline/source_texts/000156438.txt`
- 整形済み入力: `runs/20260525-121645707_run-normalized-api-gmp-guideline-v1/input/000156438_table1_markdown.txt`
- 公開元URL: `https://www.pmda.go.jp/files/000156438.pdf`

## 入力整形

表1はPDF由来TXT上で固定幅表が崩れており、本文階層の解析を不安定にするため、RUN内で表1のみを1列markdown tableへ置換した。

- 対象: `表１：原薬生産に対する本ガイドラインの適用` から `2. 品質マネージメント` の直前まで
- 方針: 列復元はせず、原文行を `raw_line` のtable rowとして保持
- 目的: 表1を落とさず、本文の章・節・項目構造を安定させる

共通parserへ個別事情を入れないため、採用しなかった共通parser案は `ADAPTER_NOTES.md` に記録した。

## 実施内容

- API GMP専用parser profile `jp_pmda_api_gmp_guideline_v1` を追加した。
  - 共通 `jp_guideline_default_v1` を継承する。
  - 冒頭通知と目次を本文IRから除外する。
  - API GMP本文の章見出し形式を扱う。
- 正規化候補4ファイルを `promotion_candidate/` に生成した。
- 表1を `table -> table_header -> table_row` として保持した。

## 生成物

- `promotion_candidate/jp_pmda_api_gmp_guideline_20011102.regdoc_ir.yaml`
- `promotion_candidate/jp_pmda_api_gmp_guideline_20011102.parser_profile.yaml`
- `promotion_candidate/jp_pmda_api_gmp_guideline_20011102.regdoc_profile.yaml`
- `promotion_candidate/jp_pmda_api_gmp_guideline_20011102.meta.yaml`
- `promotion_candidate/manifest.yaml`

## 検証

```powershell
python -m pytest tests\test_text2ir_api_gmp_guideline.py tests\test_text2ir_jp_guideline.py tests\test_text2ir_eu_gmp_chap1.py tests\test_text2ir_who_lbm_3rd.py tests\test_text2ir_profiles_pics.py tests\test_text2ir_cfr_quality_v2.py tests\test_text2ir_goal_check.py tests\test_profile_loader_extends.py tests\test_markdown_table_parsing.py tests\test_table_note_real_samples.py -q
```

結果: `41 passed`

```powershell
.venv\Scripts\python.exe -m qai_text2ir.goal_check --bundle-dir runs\20260525-121645707_run-normalized-api-gmp-guideline-v1\promotion_candidate --doc-id jp_pmda_api_gmp_guideline_20011102 --mode promotion --format markdown --out runs\20260525-121645707_run-normalized-api-gmp-guideline-v1\goal_check.md
```

結果: `PASS`

```powershell
.venv\Scripts\python.exe -m qai_text2ir.special_structure_audit --bundle-dir runs\20260525-121645707_run-normalized-api-gmp-guideline-v1\promotion_candidate --doc-id jp_pmda_api_gmp_guideline_20011102 --mode promotion --format markdown --out runs\20260525-121645707_run-normalized-api-gmp-guideline-v1\special_structure_audit.md
```

結果: `pass`

## 環境

- Python: `.venv\Scripts\python.exe`
- Python version: `3.11.6`
- lxml: `6.0.2`
- PyYAML: `6.0.3`
- typer: `0.24.0`

## 深い階層サンプル

祖先経路:

`document/root` → `chapter cha3`（3 従業員） → `paragraph cha3.p3_10`（3.10）

該当テキスト:

`中間体・原薬の生産を実施し監督するために、適切な教育訓練を受け、又は経験を有する適任者を適切な人数配置すること。`

表1サンプル:

`document/root` → `chapter cha1`（1 序文） → `paragraph cha1.p1_3`（1.3 適用範囲） → `table cha1.p1_3.tbl1`（表1） → `table_row cha1.p1_3.tbl1.tblh1.tblr1`

## 人による確認前提

AIによる構造確認では、目次由来の章重複は除去され、本文は1章から20章までroot直下に保持されている。最終判断はPRレビューで行う。

