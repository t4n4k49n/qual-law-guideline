# EU GMP Vol.4 Chapter 3 正規化RUN v2

- run_id: `20260601-145404466_run-normalized-eu-gmp-vol4-chap3-v2`
- branch: `run/normalized-eu-gmp-vol4-chap3-v2`
- doc_id: `eu_gmp_vol4_chap3_20150123`
- source: `data/human-readable/eu_gmp/vol4/source_texts/chapter_3.txt`
- official source URL: `https://health.ec.europa.eu/document/download/18d76565-137b-41d2-a602-794527f708c1_en?filename=chapter_3.pdf`
- promotion candidate: `runs/20260601-145404466_run-normalized-eu-gmp-vol4-chap3-v2/promotion_candidate/`

## 前提確認

- `main` は #248 merge後の `origin/main` へ同期済み
- local git hooks: `.githooks`
- Chap3専用parser profile `eu_gmp_chap3_default_v1` は #248 でmainへ反映済み
- 入力はEU GMP既存運用のhuman-readable text
  - `docs/NORMALIZED_RUN_PLAYBOOK.md` はXML前提を記載しているが、EU GMP Chapter 3はChap1/Chap2と同じtext2ir系統で扱う
  - この差分はRUNに記録し、候補生成コマンドもmanifestへ残す

## 実行環境

- Python: `3.11.6`
- PyYAML: `6.0.2`
- typer: `0.24.0`
- lxml: `6.0.2`
- git commit: `b5dc7f3f54589bf8e3af04a50f74662e1a6e117a`

## 生成コマンド

```powershell
$env:PYTHONPATH='src'
python -m qai_text2ir.cli bundle --input data/human-readable/eu_gmp/vol4/source_texts/chapter_3.txt --out-dir runs/20260601-145404466_run-normalized-eu-gmp-vol4-chap3-v2/promotion_candidate --doc-id eu_gmp_vol4_chap3_20150123 --title "EU GMP Vol.4 Chapter 3 Premises and Equipment" --short-title "EU GMP Ch3 Premises and Equipment" --doc-type guideline --source-url "https://health.ec.europa.eu/document/download/18d76565-137b-41d2-a602-794527f708c1_en?filename=chapter_3.pdf" --source-format pdf --retrieved-at 2026-02-18 --parser-profile-id eu_gmp_chap3_default_v1 --jurisdiction EU --language en --family EU_GMP --eu-volume 4 --strict --write-manifest --overwrite-manifest
```

## 検証

- `python -m pytest tests/test_text2ir_eu_gmp_chap1.py -q`
  - `8 passed`
- `python -m qai_text2ir.goal_check --mode promotion --bundle-dir runs/20260601-145404466_run-normalized-eu-gmp-vol4-chap3-v2/promotion_candidate --doc-id eu_gmp_vol4_chap3_20150123`
  - `PASS`
  - schema: `qai.regdoc_ir.v4`
  - nodes: `62`
  - source span coverage: `1.0`
  - warnings: `none`
- `python -m qai_text2ir.special_structure_audit --mode promotion --bundle-dir runs/20260601-145404466_run-normalized-eu-gmp-vol4-chap3-v2/promotion_candidate`
  - `pass`
  - source_tables: `0`
  - generated_tables: `0`
  - unresolved_special_blocks: `0`
- `python tools/check_ir_structure.py runs/20260601-145404466_run-normalized-eu-gmp-vol4-chap3-v2/promotion_candidate`
  - `[OK] no structure problems found`
- 絶対パス・タブ検索
  - `0件`

## 目検・再合成確認

`STRUCTURE_RECONSTRUCTION_CHECK.md` に以下を記録した。

- Chapter 3本文に表はなく、source/IR/auditのいずれもtable数は`0`
- table noteはない
- 項番なしheading 8件をsection化
- 3.6配下の `i.` / `ii.` / `iii.` をitem化
- 3.6 list後の `Further guidance can be found...` を最後のitemから分離
- PDF抽出ノイズ・脚注・不要改行・タブの混入なし

## 深い階層サンプル

`SAMPLE_EXTRACT.md` に `cha3.sec4.p3_6.iiii` の祖先経路を抽出済み。

- `root` / `document`
- `cha3` / `chapter` / `Premises and Equipment`
- `cha3.sec4` / `section` / `Production Area`
- `cha3.sec4.p3_6` / `paragraph` / `3.6`
- `cha3.sec4.p3_6.iiii` / `item` / `iii.`

## 昇格方針

この親PRでは `data/normalized/` は変更しない。
承認後、`runs/20260601-145404466_run-normalized-eu-gmp-vol4-chap3-v2/promotion_candidate/` から `data/normalized/eu_gmp_vol4_chap3_20150123/` へ複写する子PRを別途作成する。

## 昇格実施記録

- 親PR: `#249`
- 親PR main反映確認: `0afa6da`
- 昇格先: `data/normalized/eu_gmp_vol4_chap3_20150123/`
- 昇格内容: `promotion_candidate` の4ファイルを複写
  - `eu_gmp_vol4_chap3_20150123.regdoc_ir.yaml`
  - `eu_gmp_vol4_chap3_20150123.parser_profile.yaml`
  - `eu_gmp_vol4_chap3_20150123.regdoc_profile.yaml`
  - `eu_gmp_vol4_chap3_20150123.meta.yaml`
- SHA256確認: `regdoc_ir.yaml` は昇格元と昇格先で一致
  - `5F60CC15F647BAA388E9CA7AB9363FE873912223F5D0F651D576C70E33F1538E`
