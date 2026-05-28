## まとめ

PIC/S Annex 11を、正規化RUNのレビュー対象として `promotion_candidate/` に配置しました。EU GMP Chapter 1に続くPIC/S単体Annexの最初の候補であり、表・注記なしの小さな単位でPIC/S正式化の運用型を確認できます。承認後は子PRで `data/normalized/` へ昇格します。

## 対象

| 項目 | 内容 |
|---|---|
| doc_id | `pics_pe00917_annex11_20230825` |
| 文書 | `PIC/S GMP Guide (PE 009-17) Annex 11 Computerised systems` |
| 入力 | `data/human-readable/pics/pe009-17_annex11_2023-08-25_en.txt` |
| source_url | [PIC/S PE 009-17 Annexes](https://picscheme.org/docview/8881) |
| parser_profile | `pics_annex11_default_v1` |
| family | `PICS` |

## 変更内容

- `runs/20260527-153334008_run-normalized-pics-annex11-v1/promotion_candidate/` に4ファイルbundleとmanifestを追加
- promotion GOAL結果を `GOAL_CHECK_RESULT.md` / `goal_check_result.json` として追加
- 深い階層サンプルのIR抽出結果を `SAMPLE_EXTRACT.md` として追加
- RUN記録を追加
- `data/normalized/` は変更なし

## 検証結果

| 確認項目 | 結果 |
|---|---|
| schema | `qai.regdoc_ir.v4` |
| files | pass |
| manifest | pass |
| qualitycheck strict | pass |
| promotion GOAL | pass |
| verify | pass |
| source span coverage | `1.0` |
| warnings | none |
| errors | none |
| nodes | `42` |

## 深い階層サンプル

祖先経路を省略せずに確認したサンプル。表は `SAMPLE_EXTRACT.md` と同じIR抽出結果:

| 階層 | nid | kind | kind_raw | text / heading |
|---:|---|---|---|---|
| 1 | `root` | `document` |  |  |
| 2 | `ann11` | `annex` | `ANNEX` | `COMPUTERISED SYSTEMS` |
| 3 | `ann11.sec14` | `section` | `4.` | `Electronic Signature` |
| 4 | `ann11.sec14.ic` | `item` | `c.` | `include the time and date that they were applied.` |

## レビュー観点

- Annex 11のannex、section、paragraph、itemが祖先関係を保っていること
- `ann11.sec14.ic` は `item` prefix `i` + `num: c` のNIDであり、`kind_raw` は `c.` として保持されていること
- `dq_gmp_checklist.candidate_visibility` が `allow_rules: []` / `deny_rules: []` であること
- `meta.doc.family` が `PICS` として出力されていること
- 親PRでは `data/normalized/` が変更されていないこと

## 次の手順

この親PR承認後、子PRで `promotion_candidate/` の4ファイルを `data/normalized/pics_pe00917_annex11_20230825/` へ複写する。

<!-- PR_BODY_FILE: runs/20260527-153334008_run-normalized-pics-annex11-v1/PR.md -->
