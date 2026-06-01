# STRUCTURE RECONSTRUCTION CHECK

## 対象

- doc_id: `eu_gmp_vol4_chap3_20150123`
- source: `data/human-readable/eu_gmp/vol4/source_texts/chapter_3.txt`
- candidate: `runs/20260601-145404466_run-normalized-eu-gmp-vol4-chap3-v2/promotion_candidate/`

## 確認結果

- Chapter 3本文に表はない
  - special audit: `source_tables=0`
  - generated IR: `generated_tables=0`
  - 結合セルの複写対応は不要
- table noteはない
  - generated IR: `kind: note` なし
  - 表note区別の追加対応は不要
- 項番なしheadingをsection化
  - `PRINCIPLE`
  - `PREMISES`
  - `General`
  - `Production Area`
  - `Storage Areas`
  - `Quality Control Areas`
  - `Ancillary Areas`
  - `EQUIPMENT`
- 表紙側のPDF抽出ノイズをprofileで補正
  - `PT CHAPTER 5 PRODUCTION` を削除
  - `ER 3 PREMISES AND EQUIPMENT` を削除
  - 脚注 `a` と脚注本文を削除
  - `\uF0B7` bulletはsubitemとして構造化し、本文中にprivate-use bulletを残さない
- 3.6配下のroman listを確認
  - `i.` / `ii.` / `iii.` をitem化
  - list後の `Further guidance can be found...` は最後のitem本文から分離し、番号なしparagraphとしてsection直下に保持
- 空白正規化
  - `eu_gmp_chap2_cleanup` を継承し、heading/textの不要改行・連続空白を正規化
  - tab検索: 0件
- source span
  - source span coverage: `1.0`
  - `tools/check_ir_structure.py` は `[OK] no structure problems found`

## 残リスク

- `Further guidance can be found...` は原文上は3.6の補足文だが、現行IRでは番号なしparagraphとして `Production Area` section直下に置いた。最後のroman itemへ吸収されるよりは文脈破壊が少ないため、このRUNではこの形を採用する。
