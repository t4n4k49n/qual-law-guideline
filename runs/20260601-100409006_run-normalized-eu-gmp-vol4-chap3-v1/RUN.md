# EU GMP Vol.4 Chapter 3 正規化準備RUN v1

- run_id: `20260601-100409006_run-normalized-eu-gmp-vol4-chap3-v1`
- branch: `run/normalized-eu-gmp-vol4-chap3-v1`
- doc_id: `eu_gmp_vol4_chap3_20150123`
- source: `data/human-readable/eu_gmp/vol4/source_texts/chapter_3.txt`
- official source URL: `https://health.ec.europa.eu/document/download/18d76565-137b-41d2-a602-794527f708c1_en?filename=chapter_3.pdf`
- trial candidate: `runs/20260601-100409006_run-normalized-eu-gmp-vol4-chap3-v1/promotion_candidate/`

## 位置づけ

このRUNは **正規化RUN親PRではない**。
Chapter 3を正規化RUNとして成立させるためのparser/profile改定と試作候補の記録である。

理由:

- Chap3専用parser profile `src/qai_text2ir/profiles/eu_gmp_chap3_default_v1.yaml` を新規追加している
- 回帰テスト `tests/test_text2ir_eu_gmp_chap1.py` を更新している
- 正規化RUN親PRは、playbook上 `runs/<run_id>/...` のレビュー成果物に限定する運用であり、parser/profile/test改定を同梱しない

このPRをmergeした後、mainから改めて正規化RUNを切り直す。

## 前提確認

- `main` は `origin/main` と同期済み
- local git hooks: `.githooks`
- 入力はEU GMP既存運用のhuman-readable text
  - `docs/NORMALIZED_RUN_PLAYBOOK.md` はXML前提を記載しているが、EU GMP Chapter 3はChap1/Chap2と同じtext2ir系統で扱う
  - この差分と、正規化RUN親PRではないことをRUNに記録する

## 実行環境

- Python: `3.11.6`
- PyYAML: `6.0.2`
- typer: `0.24.0`
- lxml: `6.0.2`
- git commit: `41669de128e080bb806492990c3bb0019ed2809c`

## 準備で反映した過去知見

- 表の結合セル
  - Chapter 3本文に表はなく、結合セル複写対応は不要
  - special auditで `source_tables=0` / `generated_tables=0` を確認
- 表のnote
  - table noteはなし
  - `kind: note` も生成されていない
- 項番なしheading
  - Chap3専用profile `eu_gmp_chap3_default_v1` を追加
  - `PRINCIPLE` / `PREMISES` / `General` / `Production Area` / `Storage Areas` / `Quality Control Areas` / `Ancillary Areas` / `EQUIPMENT` をsection化
- 無駄な改行・空白
  - Chap2 cleanupを継承し、heading/textの不要改行・連続空白を正規化
  - tab検索は0件
- PDF抽出ノイズ
  - `PT CHAPTER 5 PRODUCTION` と `ER 3 PREMISES AND EQUIPMENT` を削除
  - 表紙脚注 `a` と脚注本文を削除
  - 表紙側deadline箇条書きの `\uF0B7` bulletをsubitem化し、普通文へのprivate-use文字混入を回避
- 3.6 roman list後の補足文
  - `Further guidance can be found...` が最後のroman itemへ吸収されないよう、番号なしparagraphとして分離

## 生成コマンド

```powershell
$env:PYTHONPATH='src'
python -m qai_text2ir.cli bundle --input data/human-readable/eu_gmp/vol4/source_texts/chapter_3.txt --out-dir runs/20260601-100409006_run-normalized-eu-gmp-vol4-chap3-v1/promotion_candidate --doc-id eu_gmp_vol4_chap3_20150123 --title "EU GMP Vol.4 Chapter 3 Premises and Equipment" --short-title "EU GMP Ch3 Premises and Equipment" --doc-type guideline --source-url "https://health.ec.europa.eu/document/download/18d76565-137b-41d2-a602-794527f708c1_en?filename=chapter_3.pdf" --source-format pdf --retrieved-at 2026-02-18 --parser-profile-id eu_gmp_chap3_default_v1 --jurisdiction EU --language en --family EU_GMP --eu-volume 4 --strict --write-manifest --overwrite-manifest
```

## 検証

- `python -m pytest tests/test_text2ir_eu_gmp_chap1.py -q`
  - `8 passed`
- `python -m qai_text2ir.goal_check --mode promotion --bundle-dir runs/20260601-100409006_run-normalized-eu-gmp-vol4-chap3-v1/promotion_candidate --doc-id eu_gmp_vol4_chap3_20150123`
  - `PASS`
  - schema: `qai.regdoc_ir.v4`
  - nodes: `62`
  - source span coverage: `1.0`
  - warnings: `none`
- `python -m qai_text2ir.special_structure_audit --mode promotion --bundle-dir runs/20260601-100409006_run-normalized-eu-gmp-vol4-chap3-v1/promotion_candidate`
  - `pass`
  - source_tables: `0`
  - generated_tables: `0`
  - unresolved_special_blocks: `0`
- `python tools/check_ir_structure.py runs/20260601-100409006_run-normalized-eu-gmp-vol4-chap3-v1/promotion_candidate`
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

## 次工程

この準備PRでは `data/normalized/` は変更しない。
このPRのmerge後、mainから新しい正規化RUNを切り直し、playbook準拠の親PRを別途作成する。
`data/normalized/eu_gmp_vol4_chap3_20150123/` への複写は、その親PR承認後の子PRで実施する。
