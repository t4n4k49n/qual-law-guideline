# RUN: 20260523-032113077_fix-who-lbm-chap8-survey-parser

- branch: `fix/who-lbm-chap8-survey-parser`
- base: `main` at `00ac2ca`
- purpose: WHO LBM 3rd Chapter 8 の Table 5-7 だけを対象に、survey/checklist table 専用パーサーで構造化する。

## 背景

WHO Laboratory Biosafety Manual 3rd edition の Chapter 8 では、Table 5-7 が通常本文ではなく laboratory safety survey/checklist form として組まれている。

従来の共通 text2ir パーサーでは、この領域が通常の item/subitem や preformatted に流れ込み、次のような問題が起きていた。

- `cha8.i5.si*` のような通常 subitem として扱われる。
- dot leader、checkbox/control/private-use glyph、form field label が人間可読テキストに残る。
- 本来の checklist item が table row としてレビュー・検索・候補化できない。

今回の判断は、WHO LBM Chapter 8 Table 5-7 だけを特殊構造として扱う専用部品を追加すること。

## 実装

- `src/qai_text2ir/who_lbm_chap8_survey.py`
  - Table 5/6/7 caption を検出。
  - Table 5 は Table 6 直前、Table 6 は Table 7 直前、Table 7 は `PART II` 直前までを対象化。
  - survey section heading と checklist item row を抽出。
  - dot leader、checkbox/control/private-use glyph、YES/NO/N/A/COMMENTS、Location/Date/signature/Brand/Type/Serial no. 等の form scaffolding を除去。
  - table/table_header/table_row ノードを構築。
- `src/qai_text2ir/text_parser.py`
  - profile flag と canonical `doc_id == "who_lbm_3rd_2004_9241546506"` の両方を満たす場合だけ、Chapter 8 survey parser を起動。
  - Table 5-7 の consumed line を通常 parser から外し、重複 item/subitem 化を防止。
  - 生成した table nodes を Chapter 8 配下へ追加。
- `src/qai_text2ir/profiles/who_lbm_3rd_default_v4.yaml`
  - `special_parsers.who_lbm_chap8_survey.enabled: true` を追加。
- `tests/fixtures/who_lbm_chap8_text_layer.txt`
  - Chapter 8 text-layer fixture を追加。
- `tests/test_who_lbm_chap8_survey_parser.py`
  - fixture parser test。
  - full WHO LBM parse integration test。
  - row count、golden rows、禁止文字列、`cha8.i5.si*` 消失を検証。

## 再生成

出力先:

- `out/20260523-032113077_fix-who-lbm-chap8-survey-parser/who_lbm_3rd_2004_9241546506/`
- `out/20260523-032113077_fix-who-lbm-chap8-survey-parser/eu_gmp_vol4_chap1_20130131/`
- `out/20260523-032113077_fix-who-lbm-chap8-survey-parser/pics_pe00917_annex2a_20230825/`

UI確認用に、処理後の WHO LBM 4ファイルを以下へ複写した。

- `out/who_lbm_3rd_review_ui/`

## 検証

- `python -m pytest tests/test_who_lbm_chap8_survey_parser.py -q`
  - `2 passed`
- `python -m pytest tests/test_text2ir_who_lbm_3rd.py tests/test_who_lbm_heading_merge.py tests/test_who_lbm_v4_skip_toc_and_annex_heading.py tests/test_who_lbm_chap8_survey_parser.py -q`
  - `13 passed`
- `python -m pytest tests/test_text2ir_goal_check.py tests/test_text2ir_profiles_pics.py tests/test_pics_annex2a_preformatted.py -q`
  - `12 passed`
- `python -m pytest -q`
  - `169 passed, 1 skipped`

## Chapter 8 Table 5-7 結果

| Table | Rows | Sections |
|---|---:|---:|
| Table 5 | 81 | 14 |
| Table 6 | 37 | 7 |
| Table 7 | 15 | 5 |
| Total | 133 | 26 |

代表行:

- `Information on sign accurate and current` -> `cha8.tbl6.tblh2.tblr4`
- `Sign legible and not defaced` -> `cha8.tbl6.tblh2.tblr5`
- `No trash on floor` -> `cha8.tbl5.tblh8.tblr6`
- `Microwave oven(s) clearly labelled “No Food Preparation, Laboratory Use Only”` -> `cha8.tbl5.tblh11.tblr2`

禁止文字列・フォーム足場の検出結果:

- `\x01`: 0
- ``: 0
- long dot leader: 0
- `CHECKED ITEM (ENTER DATE OF CHECK)`: 0
- `YES NO N/A COMMENTS`: 0
- `Location Date`: 0
- `Person in charge of laboratory`: 0
- `Safety surveyor`: 0
- `Date survey completed`: 0
- `Brand:` / `Type:` / `Serial no.:`: 0
- `cha8.i5.si*`: 0

## GOAL check

`goal_check --mode promotion` を以下3文書で実施し、すべて pass。

- `who_lbm_3rd_2004_9241546506`
- `eu_gmp_vol4_chap1_20130131`
- `pics_pe00917_annex2a_20230825`

## 注意

この parser は WHO LBM 3rd の canonical doc_id と profile flag の両方で限定起動する。PIC/S、EU GMP、CFR、xml2ir 由来文書には作用しない。
