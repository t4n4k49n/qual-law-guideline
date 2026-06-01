## まとめ

EU GMP Vol.4 Chapter 4-9 の正式昇格前レビュー用に、6章分の正規化RUN親PRを作成します。#251で確認済みの準備候補を正本候補として `promotion_candidate/` に配置し、各章についてpromotion modeの検証、特殊構造監査、IR構造チェック、見出し・note・空白の再確認を実施しました。

## 対象文書

| 章 | doc_id | 公式ソース |
|---:|---|---|
| 4 | `eu_gmp_vol4_chap4_20110101` | `chapter4_01-2011_en.pdf` |
| 5 | `eu_gmp_vol4_chap5_20150123` | `chapter_5.pdf` |
| 6 | `eu_gmp_vol4_chap6_20140328` | `2014-11_vol4_chapter_6.pdf` |
| 7 | `eu_gmp_vol4_chap7_20120628` | `vol4-chap7_2012-06_en.pdf` |
| 8 | `eu_gmp_vol4_chap8_20140813` | `2014-08_gmp_chap8.pdf` |
| 9 | `eu_gmp_vol4_chap9_undated` | `cap9_en.pdf` |

公式URLは `RUN.md` と `promotion_candidate/manifest.yaml` に記録しています。Chapter 9はローカルsource textで日付を確認できないため、準備RUNと同じく `undated` を維持しています。

## 確認結果

- `python -m pytest tests/test_text2ir_eu_gmp_chap1.py -q`
  - `9 passed`
- Chapter 4-9 各候補で `qai_text2ir.goal_check --mode promotion`
  - `PASS`
- Chapter 4-9 各候補で `qai_text2ir.special_structure_audit --mode promotion`
  - `pass`
  - source/generated table: `0`
  - unresolved special blocks: `0`
- Chapter 4-9 各候補で `tools/check_ir_structure.py`
  - `[OK] no structure problems found`
- heading/textの空白監査
  - leading/trailing whitespace、tab、embedded newline、repeated spaces: `0`

## レビュー観点

- 項番なしheadingはsection化済みで、前セクション本文への吸収なし
- Chap8本文中の `Chapter 1` / `Chapter 7` 参照はchapter node化されない
- 表は検出0件のため、結合セル複写とtable note対応は不要
- Chap4/Chap7の通常noteは`note` nodeとして分離済み

## 深い階層サンプル

`SAMPLE_EXTRACT.md` に Chapter 6 の祖先経路を省略せず記録しています。

| 階層 | nid | kind | text / heading |
|---:|---|---|---|
| 1 | `root` | `document` |  |
| 2 | `cha6` | `chapter` | `Quality Control` |
| 3 | `cha6.sec8` | `section` | `Technical transfer of testing methods` |
| 4 | `cha6.sec8.p6_39` | `paragraph` | `The transfer protocol should include, but not be limited to, the following parameters:` |
| 5 | `cha6.sec8.p6_39.iiv` | `item` | `Identification of any special transport and storage conditions of test items;` |

## 昇格方針

この親PRでは `data/normalized/` は変更しません。承認後、子PRで `promotion_candidate/` から `data/normalized/<doc_id>/` へ6章分を複写します。

<!-- PR_BODY_FILE: runs/20260601-163000000_run-normalized-eu-gmp-vol4-chap4-9-v1/PR.md -->
