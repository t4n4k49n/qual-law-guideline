# 原薬GMPガイドライン 表1 正規化候補レビュー

## 判定

PR `#215` の表1視覚レビュー修正を取り込んだmainからfreshに生成した正規化候補である。

表1はraw text 26行ではなく、PDF表に対応する7件の `table_row` として復元されている。

## 表1構造

```text
root > cha1 > cha1.sec1_3 > cha1.sec1_3.tbl1 > cha1.sec1_3.tbl1.tblh > table_row
```

確認内容:

- `table_row` count: `7`
- `column_reconstruction`: `visual_reviewed`
- `column_reconstruction_status`: `complete_for_table1`
- `record_review.table_row_promotion`: `promoted`
- `record_review.deferred_raw_rows`: `[]`
- `visual_notes[0].meaning`: `guideline_applicable=true`

## 代表行

| nid | production_type | guideline_applicable |
|---|---|---|
| `cha1.sec1_3.tbl1.tblh.tblr1` | 化学的合成による原薬 | `[false, true, true, true, true]` |
| `cha1.sec1_3.tbl1.tblh.tblr5` | 粉砕又は粉末化した生薬で構成する原薬 | `[false, false, false, false, true]` |
| `cha1.sec1_3.tbl1.tblh.tblr7` | クラシカル発酵を応用した原薬 | `[false, true, true, true, true]` |

## 見出し構造

Heading修正PR `#213` の結果も維持されている。

- `cha2.sec2_1` owns `cha2.sec2_1.p2_10`
- `cha3.sec3_1` owns `cha3.sec3_1.p3_10`
- `cha12.sec12_3` owns `cha12.sec12_3.p12_30`

## 検証結果

- GOAL check: pass
- Special structure audit: pass
- Source span coverage: `1.0`
- Focused tests: `18 passed`
- Full tests: `253 passed, 1 skipped`

## 結論

このpromotion candidateは、親PRレビューへ進める。

`data/normalized/` への複写は、親PR承認後の子PRでのみ実施する。
