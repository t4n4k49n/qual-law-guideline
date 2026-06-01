## まとめ

承認済みの正規化RUN親PR #252 に基づき、EU GMP Vol.4 Chapter 4-9 の6章分を `data/normalized/` へ昇格します。変更内容は `promotion_candidate/` から正式格納先への4ファイル複写のみで、parserや候補生成ロジックの変更は含めていません。

## 昇格対象

| 章 | doc_id |
|---:|---|
| 4 | `eu_gmp_vol4_chap4_20110101` |
| 5 | `eu_gmp_vol4_chap5_20150123` |
| 6 | `eu_gmp_vol4_chap6_20140328` |
| 7 | `eu_gmp_vol4_chap7_20120628` |
| 8 | `eu_gmp_vol4_chap8_20140813` |
| 9 | `eu_gmp_vol4_chap9_undated` |

## 確認

- 親PR #252 はmainへmerge済み
- 各doc_idで `regdoc_ir` / `parser_profile` / `regdoc_profile` / `meta` の4ファイルのみを複写
- 各doc_idの4ファイルは昇格元と昇格先でSHA256一致
- 昇格記録を `RUN.md` に追記

<!-- PR_BODY_FILE: runs/20260601-163000000_run-normalized-eu-gmp-vol4-chap4-9-v1/PROMOTION_PR.md -->
