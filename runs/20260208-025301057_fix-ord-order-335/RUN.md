# RUN

- run_id: `20260208-025301057_fix-ord-order-335`
- branch: `fix/ord-order-335`
- task: `ord不整合の原因分析（修正は保留）`
- status: `closed (analysis-only)`

## 対象

- `out/20260208-023854899_run-normalized-335AC0000000145-v2/jp_egov_335AC0000000145_20260501_507AC0000000037.regdoc_ir.yaml`

## 分析結果

- `check_ord_format_and_order` で3件NG
  - `children ord not sorted under ch4`
  - `children ord not sorted under annex38.art1`
  - `children ord not sorted under annex40.art1`
- 原因は、XMLの `Num` に通常形式ではない値があること

```text
Num="15:16"
Num="1:2"
```

- これらを通常番号と同様に `ord` 計算へ使うと、同一親内で順序逆転を起こしうる

## 判断

- 今回runではコード修正を採用しない
- `ord` の仕様を再定義してから実装する
  - 候補A: `ord` を文書内の絶対順序へ一本化（`nid` と役割分離）
  - 候補B: 通常 `Num` のみ順序計算に使用し、通常外 `Num` は出現順で処理

## 実施ログ

- 途中で試作した `src/qai_xml2ir/ord_key.py` の変更は `git restore` で取り下げ済み
- 現在のコード差分はなし（run記録のみ）
