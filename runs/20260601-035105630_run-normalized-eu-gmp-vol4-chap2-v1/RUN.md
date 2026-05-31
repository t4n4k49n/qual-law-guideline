# EU GMP Vol.4 Chapter 2 正規化RUN v1

- run_id: `20260601-035105630_run-normalized-eu-gmp-vol4-chap2-v1`
- branch: `run/normalized-eu-gmp-vol4-chap2-v1`
- doc_id: `eu_gmp_vol4_chap2_20140328`
- source: `data/human-readable/eu_gmp/vol4/source_texts/2014-03_chapter_2.txt`
- official source URL: `https://health.ec.europa.eu/document/download/11f4f8e6-a6e9-4897-afe3-f21e1dc56cb8_en?filename=2014-03_chapter_2.pdf`
- promotion candidate: `runs/20260601-035105630_run-normalized-eu-gmp-vol4-chap2-v1/promotion_candidate/`

## 前提確認

- `main` は #245 merge後の `origin/main` へ同期済み
- local git hooks: `core.hooksPath=.githooks`
- 入力はEU GMP既存運用のhuman-readable text
  - `docs/NORMALIZED_RUN_PLAYBOOK.md` はXML前提を記載しているが、EU GMP Chapter 2は既存のtext2ir系統で扱う
  - この差分はRUNに記録し、候補生成コマンドもmanifestへ残す

## 実行環境

- Python: `3.11.6`
- PyYAML: `6.0.2`
- typer: `0.24.0`
- lxml: `6.0.2`
- git commit: `88b70317b797adf77483bf15805041b70e7ffa47`

## 生成コマンド

```powershell
$env:PYTHONPATH='src'
python -m qai_text2ir.cli bundle --input data/human-readable/eu_gmp/vol4/source_texts/2014-03_chapter_2.txt --out-dir runs/20260601-035105630_run-normalized-eu-gmp-vol4-chap2-v1/promotion_candidate --doc-id eu_gmp_vol4_chap2_20140328 --title "EU GMP Vol.4 Chapter 2 Personnel" --short-title "EU GMP Ch2 Personnel" --doc-type guideline --source-url "https://health.ec.europa.eu/document/download/11f4f8e6-a6e9-4897-afe3-f21e1dc56cb8_en?filename=2014-03_chapter_2.pdf" --source-format pdf --retrieved-at 2026-02-18 --parser-profile-id eu_gmp_chap2_default_v1 --jurisdiction EU --language en --family EU_GMP --eu-volume 4 --strict --write-manifest --overwrite-manifest
```

## 検証

- `python -m pytest tests/test_text2ir_eu_gmp_chap1.py -q`
  - `7 passed`
- `python -m qai_text2ir.goal_check --mode promotion`
  - `PASS`
  - schema: `qai.regdoc_ir.v4`
  - nodes: `60`
  - source span coverage: `1.0`
  - warnings: `none`
- `python -m qai_text2ir.special_structure_audit --mode promotion`
  - `pass`
  - source_tables: `0`
  - generated_tables: `0`
  - unresolved_special_blocks: `0`
- `python tools/check_ir_structure.py runs/20260601-035105630_run-normalized-eu-gmp-vol4-chap2-v1/promotion_candidate`
  - `[OK] no structure problems found`
- 絶対パス・タブ・末尾空白検索
  - `0件`

## 目検・再合成確認

`STRUCTURE_RECONSTRUCTION_CHECK.md` に以下を記録した。

- Chapter 2本文に表はなく、source/IR/auditのいずれもtable数は`0`
- 項番なしheadingをsection化
  - `Principle`
  - `General`
  - `Key Personnel`
  - `Training`
  - `Personnel Hygiene`
  - `Consultants`
- `2.6`配下の `a, b`、`2.7`配下の `i-vi`、`2.8`配下の `i-vii`、`2.9`配下の `i-xiii` を確認
- 親子内source line逆転は`0`
- PDF脚注本文・脚注番号の混入なし
- heading/textの不要改行・タブ・前後空白・連続スペースなし

## 深い階層サンプル

`SAMPLE_EXTRACT.md` に `cha2.sec3.p2_9.ixiii` の祖先経路を抽出済み。

- `root` / `document`
- `cha2` / `chapter` / `Personnel`
- `cha2.sec3` / `section` / `Key Personnel`
- `cha2.sec3.p2_9` / `paragraph` / `2.9`
- `cha2.sec3.p2_9.ixiii` / `item` / `xiii.`

## 昇格方針

この親PRでは `data/normalized/` は変更しない。
承認後、`runs/20260601-035105630_run-normalized-eu-gmp-vol4-chap2-v1/promotion_candidate/` から `data/normalized/eu_gmp_vol4_chap2_20140328/` へ複写する子PRを別途作成する。

## 昇格実施記録

- 親PR: `#246`
- 親PR main反映確認: `c2a1cfe`
- 昇格先: `data/normalized/eu_gmp_vol4_chap2_20140328/`
- 昇格内容: `promotion_candidate` の4ファイルを複写
  - `eu_gmp_vol4_chap2_20140328.regdoc_ir.yaml`
  - `eu_gmp_vol4_chap2_20140328.parser_profile.yaml`
  - `eu_gmp_vol4_chap2_20140328.regdoc_profile.yaml`
  - `eu_gmp_vol4_chap2_20140328.meta.yaml`
- SHA256確認: `regdoc_ir.yaml` は昇格元と昇格先で一致
