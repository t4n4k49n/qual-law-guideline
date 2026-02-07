## 概要

`ord` 不整合3件について、実装修正は行わず、分析結果のみを記録してrunをクローズするPRです。

## 分析結果

- `check_ord_format_and_order` で3件NG
  - `children ord not sorted under ch4`
  - `children ord not sorted under annex38.art1`
  - `children ord not sorted under annex40.art1`
- 原因は、XMLの `Num` に通常形式ではない値が含まれること

```text
Num="15:16"
Num="1:2"
```

- これらを通常番号と同様に `ord` 計算へ使うと、同一親内で順序逆転が発生しうる

## 変更内容

- `runs/20260208-025301057_fix-ord-order-335/RUN.md` を追加
- 不整合箇所(3件)・原因・仕様検討方針を記録

## 判断（今回の結論）

- 今回runではコード修正を採用しない（analysis-only）
- `ord` の仕様再定義を先に実施し、実装は別run/別PRで対応する
  - 候補A: `ord` を文書内の絶対順序へ一本化（`nid` と役割分離）
  - 候補B: 通常 `Num` のみ順序計算に使用し、通常外 `Num` は出現順で処理

## 補足

- コード変更はありません
- 試作した `src/qai_xml2ir/ord_key.py` の変更は取り下げ済みです
