## まとめ

承認済みの正規化RUN親PR #257 の候補を、正式版 `data/normalized/` へ昇格します。変更は `promotion_candidate/` から `data/normalized/<doc_id>/` への2文書分の複写と、`RUN.md` への昇格記録追記に限定しています。

## 昇格対象

| 文書 | doc_id | 昇格先 |
|---|---|---|
| 21 CFR Part 11 | `us_cfr_title21_part11_20251027` | `data/normalized/us_cfr_title21_part11_20251027/` |
| 21 CFR Part 211 | `us_cfr_title21_part211_20251027` | `data/normalized/us_cfr_title21_part211_20251027/` |

## 確認結果

- 親PR: #257
- 親PR main反映確認: `1906087`
- 各doc_idの4ファイルは昇格元と昇格先でSHA256一致

## 昇格方針

このPRではパーサコード修正、追加再生成、無関係な文書更新は行っていません。

<!-- PR_BODY_FILE: runs/20260601-201000000_run-normalized-us-cfr-title21-part11-211-v1/PROMOTE_PR.md -->
