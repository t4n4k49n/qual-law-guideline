# 原薬GMPガイドライン 表1 視覚レビュー

## 判定

PR `#214` の正規化候補は、表1がraw text由来の26行table_rowであり、PDF上の表セル構造を表現できていなかったため不採用。

このRUNでは、PDF 8ページ目の表1を目検し、6列 x 7データ行のtableとして復元する。

## 復元方針

- table_headerは6列を持つ。
- table_rowは7件のみ作る。
- 各table_rowは `cells` に6セルを持つ。
- PDFの灰色セルは `guideline_applicable` で保持する。
- 下部の矢印 `ＧＭＰ要求事項の増大` はtable_rowにせず、tableの `visual_notes` に保持する。
- 元TXTの崩れた行は `raw_lines` / `raw_row_nums` として追跡用に保持する。

## 列

| index | column | label |
|---:|---|---|
| 0 | `production_type` | 生産形態 |
| 1 | `api_starting_material_manufacture` | 原薬出発物質の製造 |
| 2 | `api_starting_material_introduction_or_preliminary_processing` | 原薬出発物質の工程への導入又は初期加工処理 |
| 3 | `intermediate_manufacture_or_equivalent` | 中間体の製造又は同等工程 |
| 4 | `isolation_and_purification_or_further_extraction` | 分離及び精製又は再抽出 |
| 5 | `physical_processing_and_packaging` | 物理的加工処理及び包装 |

## 復元行

`guideline_applicable` は生産形態列を除く5工程列に対応する。

| row | production_type | stage 1 | stage 2 | stage 3 | stage 4 | stage 5 | guideline_applicable |
|---:|---|---|---|---|---|---|---|
| 1 | 化学的合成による原薬 | 原薬出発物質の製造 | 原薬出発物質の工程への導入 | 中間体の製造 | 分離及び精製 | 物理的加工処理及び包装 | `[false, true, true, true, true]` |
| 2 | 動物由来の原薬 | 器官、液体又は組織の収集 | 細断、混合、及び初期加工処理 | 原薬出発物質の工程への導入 | 分離及び精製 | 物理的加工処理及び包装 | `[false, false, true, true, true]` |
| 3 | 植物から抽出する原薬 | 植物の収集 | 細断及び初期抽出 | 原薬出発物質の工程への導入 | 分離及び精製 | 物理的加工処理及び包装 | `[false, false, true, true, true]` |
| 4 | 原薬として使用する生薬抽出物 | 植物の収集 | 細断及び初期抽出 |  | 再抽出 | 物理的加工処理及び包装 | `[false, false, false, true, true]` |
| 5 | 粉砕又は粉末化した生薬で構成する原薬 | 植物の収集又は栽培及び収穫 | 細断／粉砕 |  |  | 物理的加工処理及び包装 | `[false, false, false, false, true]` |
| 6 | バイオテクノロジー（発酵・細胞培養）を応用した原薬 | マスターセルバンク及びワーキングセルバンクの確立 | ワーキングセルバンクの維持管理 | 細胞培養又は発酵 | 分離及び精製 | 物理的加工処理及び包装 | `[false, true, true, true, true]` |
| 7 | クラシカル発酵を応用した原薬 | セルバンクの確立 | セルバンクの維持管理 | セルの発酵工程への導入 | 分離及び精製 | 物理的加工処理及び包装 | `[false, true, true, true, true]` |

## 出力確認

- `table_row` count: `7`
- `generated_rows`: `7`
- `column_reconstruction`: `visual_reviewed`
- `column_reconstruction_status`: `complete_for_table1`
- `record_review.table_row_promotion`: `promoted`
- `record_review.deferred_raw_rows`: `[]`
- `visual_notes[0].meaning`: `guideline_applicable=true`

## 残る注意

この復元はPDF目検とTXT行の照合によるもの。自動OCRだけで再現したものではないため、正規化RUN前にこのレビューPRで人間確認する。
