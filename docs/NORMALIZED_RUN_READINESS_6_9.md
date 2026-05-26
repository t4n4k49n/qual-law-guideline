# 6/7/8/9 正規化RUN readiness判定

## 位置づけ

この文書は、6/7/8/9の通常開発RUNを受けて、正式な正規化RUNへ進める範囲と、追加RUNへ送る範囲を判定する。

ここでの判定は、まだ正式な正規化RUNではない。`data/normalized/` への昇格は、別途 `docs/NORMALIZED_RUN_PLAYBOOK.md` に従って親PR・子PRで行う。

## 総合判定

| 番号 | 文書 | 判定 | 正規化RUNでの扱い | 追加RUN |
| ---: | --- | --- | --- | --- |
| 6 | 原薬GMPガイドライン | 正規化RUNへ進める | 本文階層 + 表1 raw table + reconstructed recordsをreview対象にする | 任意: 表1のPDF視覚情報レビュー |
| 7 | 無菌操作法指針 | 正規化RUNへ進める | 本文階層 + 表1/2/3 raw table + reconstructed recordsをreview対象にする | 任意: 複数段ヘッダ・注記リンクの精査 |
| 8 | 病原体等安全管理規程 | 正規化RUNへ進めるが、NIID難表は視覚レビューRUN対象 | 別表・付表16件をmixed modeでreview対象にする | 必須候補: NIID付表/別表 視覚レビュー復元RUN |
| 9 | CSVガイドライン | 条件付きで正規化RUNへ進める | 本文 + 別紙2 table/semantic recordsをreview対象にする | 推奨: 別紙1 figure source化RUN |

## 6 原薬GMPガイドライン

判定: 正規化RUNへ進める。

根拠:

- 本文階層は既存parser profileで安定している。
- 表1はraw table rowを保持し、`reconstructed_records` 7件を付与済み。
- `goal_check` と関連テストは直近RUNで通過済み。

正規化RUNでレビューする範囲:

- 本文章・節・項目。
- 表1のraw row保持。
- 表1の `reconstructed_records` を正式候補として採用するか。

追加RUNへ送る可能性:

- 表1のPDF視覚情報、特に灰色領域の意味を正規化する場合は、別途視覚レビューRUNで扱う。

## 7 無菌操作法指針

判定: 正規化RUNへ進める。

根拠:

- 本文階層は既存parser profileで安定している。
- 表1/2/3はraw table rowを保持し、`reconstructed_records` を付与済み。
- 複数段ヘッダや注記リンクは残るが、raw rowとsource spanを維持している。

正規化RUNでレビューする範囲:

- 本文章・節・項目。
- 表1/2/3のraw row保持。
- `reconstructed_records` を正式候補として採用するか。

追加RUNへ送る可能性:

- 注記とセルの厳密なリンク。
- 複数段ヘッダを正式なtable schemaへ昇格する判断。

## 8 病原体等安全管理規程

判定: 正規化RUNへ進める。ただし、完全な表セル正規化を目指すなら、NIID視覚レビュー復元RUNを先に行う。

根拠:

- 別表・付表16件は欠落せず保持済み。
- 5表は `table` / `table_row` 化済み。
- 全16件に `normalization_readiness` を付与済み。
- 複雑表はraw annex textまたはpartial cell tableとして保持し、無理な誤復元を避けている。

正規化RUNでレビューする範囲:

- `別表1`, `付表1-1`: annex text。
- `付表1-2`, `付表1-3`, `別表6`, `別表9`: numbered annex text。
- `別表2`, `別表3`: sectioned annex text。
- `別表4`, `別表5`, `別表8`: raw annex text。
- `付表2`: raw table。
- `付表3`, `付表4`, `別表7`, `別表10`: partial cell table。

追加RUNへ送る対象:

- `付表2`, `付表4`, `別表7`, `別表10` は、PDFページ画像を根拠にした視覚レビュー復元RUNへ送る。
- 必要に応じて `付表3` も同RUNに含める。

## 9 CSVガイドライン

判定: 条件付きで正規化RUNへ進める。

根拠:

- 本文階層は既存parser profileで安定している。
- 別紙2は公式page2 HTMLをsourceとしてtable化済み。
- 別紙2はカテゴリ単位semantic records、記号値、脚注参照まで分解済み。
- 別紙1はHTML本文に画像参照しかなく、figure source化が未実装。

正規化RUNでレビューする範囲:

- 本文章・節・項目。
- 別紙2のtable rows。
- 別紙2のsemantic recordsを正式候補として採用するか。

追加RUNへ送る対象:

- 別紙1は公式画像をlocal sourceとして取得し、まず `figure` nodeとして保持するRUNを推奨する。
- 別紙1のフロー意味分解は、OCRだけで正本化せず、視覚レビューまたは手入力転記RUNで扱う。

## 次に行う追加RUN

元計画KからQは、このreadiness判定で完了とする。

次に着手する優先順:

1. `NIID付表/別表 視覚レビュー復元RUN`
2. `CSV別紙1 figure source化RUN`
3. 6/7表の視覚情報・注記リンク精査RUN

ユーザーが「視覚処理に入る」と指示した場合は、1を開始する。

## 正規化RUNへの進め方

正式な正規化RUNは、文書単位に分ける。

推奨:

- `run/normalized-api-gmp-guideline-v1`
- `run/normalized-aseptic-processing-guideline-v1`
- `run/normalized-niid-pathogen-safety-v1`
- `run/normalized-mhlw-csv-guideline-v1`

各RUNでは、`runs/<run_id>/promotion_candidate/` に4ファイルとmanifestを置き、親PRでレビューする。`data/normalized/` への複写は、親PR承認後の子PRでのみ行う。
