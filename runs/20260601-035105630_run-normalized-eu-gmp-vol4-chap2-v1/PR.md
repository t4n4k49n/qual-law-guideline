# EU GMP Vol.4 Chapter 2 正規化候補 v1

## まとめ

EU GMP Vol.4 Chapter 2 Personnel の正規化候補を、項番なしheadingと責務リスト階層を保った形でレビュー可能にしました。前段のプロファイル修正を反映し、脚注混入、不要改行・空白、source順序、表・noteの有無を確認しています。

このPRは親PRです。`data/normalized/` への昇格は含めていません。承認後、候補から正式版へ複写する子PRを別途作成します。

## 対象

- 文書: EU GMP Vol.4 Chapter 2 Personnel
- doc_id: `eu_gmp_vol4_chap2_20140328`
- 原文URL: `https://health.ec.europa.eu/document/download/11f4f8e6-a6e9-4897-afe3-f21e1dc56cb8_en?filename=2014-03_chapter_2.pdf`
- 対象e-Gov法令URL: 該当なし（EU GMP公式PDF）
- 候補: `runs/20260601-035105630_run-normalized-eu-gmp-vol4-chap2-v1/promotion_candidate/`

## 変更内容

- EU GMP Chapter 2 の正規化候補一式を追加
- `manifest.yaml` を追加し、実行条件と検証対象を記録
- 目検用アーティファクトを追加
  - `GOAL_CHECK.md`
  - `SPECIAL_STRUCTURE_AUDIT.md`
  - `STRUCTURE_RECONSTRUCTION_CHECK.md`
  - `SAMPLE_EXTRACT.md`

## 検証結果

- EU GMP関連テスト: `7 passed`
- `goal_check --mode promotion`: `PASS`
  - schema: `qai.regdoc_ir.v4`
  - nodes: `60`
  - source span coverage: `1.0`
  - warnings: `none`
- `special_structure_audit --mode promotion`: `pass`
  - source_tables: `0`
  - generated_tables: `0`
  - unresolved_special_blocks: `0`
- `tools/check_ir_structure.py`: `[OK] no structure problems found`
- 絶対パス・タブ・末尾空白検索: 0件

## 表・note確認

Chapter 2本文に表はありません。`STRUCTURE_RECONSTRUCTION_CHECK.md` でsource上の `Table` 見出し候補、IR table nodes、IR note nodesがすべて`0`であることを確認しました。

## heading・階層確認

項番なしheadingをsectionとして確認済みです。

- `Principle`
- `General`
- `Key Personnel`
- `Training`
- `Personnel Hygiene`
- `Consultants`

リスト階層も確認済みです。

- `2.6`: `a, b`
- `2.7`: `i, ii, iii, iv, v, vi`
- `2.8`: `i, ii, iii, iv, v, vi, vii`
- `2.9`: `i, ii, iii, iv, v, vi, vii, viii, ix, x, xi, xii, xiii`

## 脚注・改行・スペース確認

- PDF脚注本文・脚注番号の混入なし
- heading/textの不要改行・タブ・前後空白・連続スペースなし
- 親子内source line逆転なし

## 深い階層サンプル

`SAMPLE_EXTRACT.md` から、祖先を省略せずに提示します。

- `root` / `document`
- `cha2` / `chapter` / `Personnel`
- `cha2.sec3` / `section` / `Key Personnel`
- `cha2.sec3.p2_9` / `paragraph` / `The heads of Production, Quality Control and where relevant, Head of Quality Assurance or Head of Quality Unit, generally have some shared, or jointly exercised, responsibilities relating to quality including in particular the design, effective implementation, monitoring and maintenance of the quality management system. These may include, subject to any national regulations:`
- `cha2.sec3.p2_9.ixiii` / `item` / `Ensuring that a timely and effective communication and escalation process exists to raise quality issues to the appropriate levels of management.`

<!-- PR_BODY_FILE: runs/20260601-035105630_run-normalized-eu-gmp-vol4-chap2-v1/PR.md -->
