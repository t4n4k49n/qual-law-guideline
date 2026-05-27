## まとめ

EU GMP Vol.4 Chapter 1を、正規化RUNのレビュー対象として `promotion_candidate/` に配置しました。10/12/13のreadiness結果で最初の正式化候補と判断した文書を、親PRで確認できる状態にしています。これにより、TXT入口のEU GMP正規化を小さな単位で始め、承認後に子PRで `data/normalized/` へ昇格できるようになります。

## 対象

| 項目 | 内容 |
|---|---|
| doc_id | `eu_gmp_vol4_chap1_20130131` |
| 文書 | `EU GMP Vol.4 Chapter 1 Pharmaceutical Quality System` |
| 入力 | `data/human-readable/eu_gmp/vol4/chap1_2013-01_en.txt` |
| source_url | [EU GMP Vol.4 Chapter 1 PDF](https://health.ec.europa.eu/document/download/e458c423-f564-4171-b344-030a461c567f_en) |
| parser_profile | `eu_gmp_chap1_default_v2` |
| family | `EU_GMP` |

## 変更内容

- `runs/20260527-133746129_run-normalized-eu-gmp-vol4-chap1-v1/promotion_candidate/` に4ファイルbundleとmanifestを追加
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
| nodes | `72` |

## 深い階層サンプル

祖先経路を省略せずに確認したサンプル。表は `SAMPLE_EXTRACT.md` と同じIR抽出結果:

| 階層 | nid | kind | kind_raw | text / heading |
|---:|---|---|---|---|
| 1 | `root` | `document` |  |  |
| 2 | `cha1` | `chapter` | `Chapter` | `Pharmaceutical Quality System` |
| 3 | `cha1.p1_8` | `paragraph` | `1.8` |  |
| 4 | `cha1.p1_8.iiii` | `item` | `(iii)` | `All necessary facilities for GMP are provided including:` |
| 5 | `cha1.p1_8.iiii.si3` | `subitem` | `•` | `Suitable equipment and services;` |

## レビュー観点

- Chapter 1の章、段落、箇条、サブ箇条が祖先関係を保っていること
- `cha1.p1_8.iiii` は `item` prefix `i` + `num: iii` のNIDであり、`kind_raw` は `(iii)` として保持されていること
- `dq_gmp_checklist.candidate_visibility` が `allow_rules: []` / `deny_rules: []` であること
- `meta.doc.family` が `EU_GMP` として出力されていること
- 親PRでは `data/normalized/` が変更されていないこと

## 次の手順

この親PR承認後、子PRで `promotion_candidate/` の4ファイルを `data/normalized/eu_gmp_vol4_chap1_20130131/` へ複写する。

<!-- PR_BODY_FILE: runs/20260527-133746129_run-normalized-eu-gmp-vol4-chap1-v1/PR.md -->
