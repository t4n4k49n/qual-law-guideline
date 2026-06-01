# 深い階層サンプル

このRUNでは 21 CFR Part 11 / Part 211 の両方から深い階層を抽出した。

## 21 CFR Part 11

- file: `SAMPLE_PART11.md`
- target: `part11.subptc.sec11_200.pa.i1.sii`
- path: document -> part -> subpart -> section -> paragraph -> item -> subitem

## 21 CFR Part 211

- file: `SAMPLE_PART211.md`
- target: `part211.subptc.sec211_42.pc.i10.sivi`
- path: document -> part -> subpart -> section -> paragraph -> item -> subitem

## 確認観点

- Part 11: `(a)(1)(i)` が paragraph/item/subitem として保持される。
- Part 211: `§ 211.42(c)(10)(vi)` が item配下のsubitemとして保持される。
- Part 211: `§ 211.67(b)(6)` 後の `(c)` は section直下の paragraph に戻ることをテスト済み。
