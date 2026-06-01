# EU GMP Vol.4 Chapter 4-9 正規化RUN v1

- run_id: `20260601-163000000_run-normalized-eu-gmp-vol4-chap4-9-v1`
- branch: `run/normalized-eu-gmp-vol4-chap4-9-v1`
- scope: EU GMP Vol.4 Chapter 4-9
- promotion candidate: `runs/20260601-163000000_run-normalized-eu-gmp-vol4-chap4-9-v1/promotion_candidate/`
- source preparation run: `runs/20260601-152632412_eu-gmp-chap4-9-normalization-prep/`

## 前提確認

- `main` は #251 merge後の `origin/main` へ同期済み
- local git hooks: `.githooks`
- Chap4-9向けparser profile `eu_gmp_chap4_9_default_v1` は #251 でmainへ反映済み
- 入力はEU GMP既存運用のhuman-readable text
  - `docs/NORMALIZED_RUN_PLAYBOOK.md` はXML前提を記載しているが、EU GMP Chapter 4-9はChap1/Chap2/Chap3と同じtext2ir系統で扱う
  - この差分はRUNに記録し、候補生成元をmanifestへ残す
- `data/normalized/` はこの親PRでは変更しない

## 対象文書

| chapter | doc_id | source text | official source URL |
|---:|---|---|---|
| 4 | `eu_gmp_vol4_chap4_20110101` | `data/human-readable/eu_gmp/vol4/source_texts/chapter4_01-2011_en.txt` | `https://health.ec.europa.eu/document/download/104b3eb8-81a7-4858-9419-cb06562adb66_en?filename=chapter4_01-2011_en.pdf` |
| 5 | `eu_gmp_vol4_chap5_20150123` | `data/human-readable/eu_gmp/vol4/source_texts/chapter_5.txt` | `https://health.ec.europa.eu/document/download/4a1fdb4f-6f6f-49c4-b264-8056e5bbe078_en?filename=chapter_5.pdf` |
| 6 | `eu_gmp_vol4_chap6_20140328` | `data/human-readable/eu_gmp/vol4/source_texts/2014-11_vol4_chapter_6.txt` | `https://health.ec.europa.eu/document/download/c74c8720-27bf-4252-808f-d65a206a90bb_en?filename=2014-11_vol4_chapter_6.pdf` |
| 7 | `eu_gmp_vol4_chap7_20120628` | `data/human-readable/eu_gmp/vol4/source_texts/vol4-chap7_2012-06_en.txt` | `https://health.ec.europa.eu/document/download/58b5106a-cf6f-4352-9dca-1caf5d27d97e_en?filename=vol4-chap7_2012-06_en.pdf` |
| 8 | `eu_gmp_vol4_chap8_20140813` | `data/human-readable/eu_gmp/vol4/source_texts/2014-08_gmp_chap8.txt` | `https://health.ec.europa.eu/document/download/b1eb2292-cb0d-4e3f-aea9-e3fe79faf6e3_en?filename=2014-08_gmp_chap8.pdf` |
| 9 | `eu_gmp_vol4_chap9_undated` | `data/human-readable/eu_gmp/vol4/source_texts/cap9_en.txt` | `https://health.ec.europa.eu/document/download/07195808-d02e-4d7a-b8f4-f84a83278b62_en?filename=cap9_en.pdf` |

Chapter 9 source text does not expose a publication date in the local text, so this run keeps the preparation doc_id `eu_gmp_vol4_chap9_undated`. Confirm the official date before the promotion child PR if a dated doc_id is required.

## 実行環境

- Python: `3.11.6`
- PyYAML: `6.0.2`
- typer: `0.24.0`
- lxml: `6.0.2`
- base commit: `1a84c1e`

## 候補作成

#251でレビュー済みの準備候補を正規化RUNの正本候補として複写した。

```powershell
$run='runs/20260601-163000000_run-normalized-eu-gmp-vol4-chap4-9-v1'
$src='runs/20260601-152632412_eu-gmp-chap4-9-normalization-prep/trial_candidates_r2'
Copy-Item <each reviewed candidate yaml> "$run/promotion_candidate/<doc_id>/"
```

`manifest.yaml` はこのRUN用に新規作成し、個人環境の絶対パスを含めていない。

## 検証

- `python -m pytest tests/test_text2ir_eu_gmp_chap1.py -q`
  - `9 passed`
- 各doc_idで `python -m qai_text2ir.goal_check --mode promotion`
  - `PASS`
- 各doc_idで `python -m qai_text2ir.special_structure_audit --mode promotion`
  - `pass`
  - source_tables: `0`
  - generated_tables: `0`
  - unresolved_special_blocks: `0`
- 各doc_idで `python tools/check_ir_structure.py <bundle>`
  - `[OK] no structure problems found`
- heading/text空白検索
  - leading/trailing whitespace: `0`
  - tabs: `0`
  - embedded newlines: `0`
  - repeated spaces: `0`

## 目検・再合成確認

`STRUCTURE_RECONSTRUCTION_CHECK.md` に以下を記録した。

- Chap4-9各文書はchapter nodeが1件
- 項番なしheadingはsection化され、前段落本文への吸収なし
- Chap8本文中の `Chapter 1` / `Chapter 7` 参照はchapter node化されない
- 表はsource/generatedともに0件で、結合セル複写は不要
- Chap4/Chap7の通常noteは`note` nodeとして分離
- 無駄な改行・空白・タブ混入なし

## 深い階層サンプル

`SAMPLE_EXTRACT.md` に `cha6.sec8.p6_39.iiv` の祖先経路を抽出済み。

- `root` / `document`
- `cha6` / `chapter` / `Quality Control`
- `cha6.sec8` / `section` / `Technical transfer of testing methods`
- `cha6.sec8.p6_39` / `paragraph` / `6.39`
- `cha6.sec8.p6_39.iiv` / `item` / `iv.`

## 昇格方針

この親PRでは `data/normalized/` は変更しない。
承認後、`runs/20260601-163000000_run-normalized-eu-gmp-vol4-chap4-9-v1/promotion_candidate/` の各doc_id配下から `data/normalized/<doc_id>/` へ複写する子PRを別途作成する。

## 昇格実施記録

- 親PR: `#252`
- 親PR main反映確認: `034bb71`
- 昇格ブランチ: `promote/eu-gmp-vol4-chap4-9`
- 昇格先:
  - `data/normalized/eu_gmp_vol4_chap4_20110101/`
  - `data/normalized/eu_gmp_vol4_chap5_20150123/`
  - `data/normalized/eu_gmp_vol4_chap6_20140328/`
  - `data/normalized/eu_gmp_vol4_chap7_20120628/`
  - `data/normalized/eu_gmp_vol4_chap8_20140813/`
  - `data/normalized/eu_gmp_vol4_chap9_undated/`
- 昇格内容: 各doc_idで `promotion_candidate` の4ファイルを複写
  - `regdoc_ir.yaml`
  - `parser_profile.yaml`
  - `regdoc_profile.yaml`
  - `meta.yaml`
- SHA256確認: 各doc_idの4ファイルは昇格元と昇格先で一致
  - `eu_gmp_vol4_chap4_20110101.regdoc_ir.yaml`: `4AD367910455F8DFC9C43FECFC277424DE83B0D8D41D0797715D71A1750E755A`
  - `eu_gmp_vol4_chap5_20150123.regdoc_ir.yaml`: `E02ACEC57DD2A4DE5D1180B9C6E82B7241A2C9BECDB5B21069E9B6573E6A6139`
  - `eu_gmp_vol4_chap6_20140328.regdoc_ir.yaml`: `0F2D7DA11B6C676DA8928A0D395E5544B9374495048F460E14E42305E743ED2A`
  - `eu_gmp_vol4_chap7_20120628.regdoc_ir.yaml`: `CCA15F94BC7202237080A697910A75C1A77A23E0FB17B163B53553AEDEC6F4D4`
  - `eu_gmp_vol4_chap8_20140813.regdoc_ir.yaml`: `B5C653DADC4AC4A25C69FF1B858175046013554D5143A90ADCF65273CFCB0837`
  - `eu_gmp_vol4_chap9_undated.regdoc_ir.yaml`: `DDEABD753BE3316427B08114E30C2D9B72AF353A8F920920DEBDF8DB390D5205`
