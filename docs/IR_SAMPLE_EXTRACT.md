# IRサンプル抽出ツール

正規化RUNのPRに載せる「深い階層サンプル」を、手書きではなく `*.regdoc_ir.yaml` から抽出するためのツール。

## 使い方

```powershell
python tools/extract_ir_sample.py `
  --ir runs/<run_id>/promotion_candidate/<doc_id>.regdoc_ir.yaml `
  --nid <target_nid> `
  --output runs/<run_id>/SAMPLE_EXTRACT.md
```

PRで長いparagraph本文を省略したい場合は、既存のレビュー表の体裁に合わせて次のようにする。

```powershell
python tools/extract_ir_sample.py `
  --ir runs/<run_id>/promotion_candidate/<doc_id>.regdoc_ir.yaml `
  --nid <target_nid> `
  --output runs/<run_id>/SAMPLE_EXTRACT.md `
  --blank-text-kind paragraph
```

## 出力

出力はMarkdownで、既存PRのレビュー表と同じ列を使う。

| 階層 | nid | kind | kind_raw | text / heading |
|---:|---|---|---|---|

## 運用

- `SAMPLE_EXTRACT.md` は `runs/<run_id>/` に置く。
- PR本文の表は、`SAMPLE_EXTRACT.md` の表を転記する。
- 手書きで `kind_raw` や `nid` を補正しない。誤りに見える場合は、先にIRと抽出結果を確認する。
- target nidは、レビューしたい深い階層の代表ノードを選ぶ。
