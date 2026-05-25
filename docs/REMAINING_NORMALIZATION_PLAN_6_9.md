# 6/7/8/9 残正規化課題と次期開発計画

## 位置づけ

`docs/INDIVIDUAL_ADAPTER_NEXT_PHASE_PLAN.md` で計画したF-Iは完了した。

- F: 6/7/8/9の列復元・意味正規化棚卸し
- G: 6/7 raw_line tableの列復元プロトタイプ
- H: 8 別表・付表の分類とtable node化
- I: 9 CSV別紙のソース補完
- 追加対応: 9 CSV別紙2の公式page2 HTML table adapter

ここまでの成果は、Parser/adapter開発としての到達点であり、正式な正規化RUNではない。`data/normalized/` への昇格は、別途 `docs/NORMALIZED_RUN_PLAYBOOK.md` に従う。

## 現在の到達点

| 対象 | 到達点 | 正規化完成までの主な残課題 |
| --- | --- | --- |
| 6 原薬GMPガイドライン | 表1に `reconstructed_records` を付与 | recordの確定、正式table_row化判断、PDF視覚情報の扱い |
| 7 無菌操作法指針 | 表1/2/3に `reconstructed_records` を付与 | 複数段ヘッダ、注記対応、候補粒度判断 |
| 8 病原体等安全管理規程 | 5表を `table` / `table_row` 化し、列候補を付与 | セル単位復元、複雑表レビュー、番号/節構造化判断 |
| 9 CSVガイドライン | 別紙2を公式page2 HTMLから `table` / `table_row` 化し、semantic record候補を付与 | 別紙1画像のfigure source化、正規化RUN readiness |

## 次期開発の原則

- 通常開発PRと正規化RUNを混ぜない。
- 1PRでは、判断軸を1つに絞る。
- 共通処理には、文書固有の表番号、列名、URL、OCR判断を入れない。
- `raw_line`、元セル、source spanは、意味正規化後も追跡できるよう残す。
- 正式昇格前に、文書ごとに「追加開発が必要 / 正規化RUNへ進める / 保留」を判定する。
- PDFテキストレイヤーだけでセル結合、複数行セル、折返しセルを復元できない表は、通常コードの汎用化で引き延ばさず、最後に視覚レビュー復元RUNとして扱う。

## 推奨順

### K. 6/7 表record確定レビュー

ブランチ案: `feat/table-record-review-6-7`

目的:

- 6/7で作成済みの `reconstructed_records` をレビュー可能な確定候補へ整える。
- 正式な `table_row` nodeへ昇格するか、table.data上の補助recordに留めるかを判断する。

対象:

- 6 表1: `cha1.p1_3.tbl1`
- 7 表1: `cha7.p7_1.tbl1`
- 7 表2: `cha11.p11_3.tbl2`
- 7 表3: `cha11.p11_3.tbl3`

完了条件:

- 表ごとに、昇格するrecord / raw保持する行 / 保留理由がRUNに残る。
- 注記や複数段ヘッダを、table note、record field、保留のいずれで扱うか明示する。
- DQ候補粒度をraw rowにするかrecordにするか、少なくとも表単位で暫定判断する。

### L. 8 NIID tableセル復元 v1

ブランチ案: `feat/niid-annex-table-cell-reconstruction-v1`

目的:

- 既にtable node化済みの5表について、セル単位の復元を進める。
- 付表系と別表系を同じPRに入れる場合でも、表ごとのadapter設定とwarningを明確に分ける。

対象:

- `付表2`
- `付表3`
- `付表4`
- `別表7`
- `別表10`

完了条件:

- 復元できる行に `cells` と列名対応を付ける。
- 複数行セルや境界不明行は、無理にセル化せずwarning付きで残す。
- `raw_line` とsource spanを維持する。

### M. 8 NIID複雑表・節構造レビュー

ブランチ案: `docs/niid-complex-annex-structure-plan`

目的:

- table化しなかったNIID別表・付表について、次の扱いを決める。

対象:

- 複雑表候補: `別表4`, `別表5`, `別表8`
- 節構造候補: `別表2`, `別表3`
- 番号付き要求事項候補: `別表6`, `別表9`

完了条件:

- adapter化する対象、原文保持する対象、正規化RUN前に保留する対象が分かれる。
- 列復元ではなく節/番号構造化として扱う対象を明示する。

### N. 8 NIID付表/別表 視覚レビュー復元RUN方針

ブランチ案: `docs/niid-visual-table-review-run-plan`

目的:

- PDFページ画像を根拠にしないと復元できないNIID難表を、通常コードの汎用化対象から分離する。
- 全体計画を一定範囲まで進めた後、Codex視覚処理でセル結合、複数行セル、折返しセルを補正するRUNの入力と記録方式を決める。

対象:

- `付表2`
- `付表4`
- `別表7`
- `別表10`
- 必要に応じて `付表3`

実施方針:

- parser/adapterは、raw row、source span、warning、PDFページ参照を失わない。
- 視覚レビュー復元RUNでは、PDFページ画像、復元後JSON/Markdown、視覚判断で結合・改行復元したセル、既存TXTと照合できた文字列をRUNに残す。
- 視覚判断で補正した表は、コードだけで再生成できる成果物と区別する。
- 正式な `data/normalized/` 昇格は、視覚レビュー復元RUNの成果を正規化RUNでレビューした後に行う。

完了条件:

- どの表を視覚レビュー復元へ送るかがRUNに残る。
- どのPDFページを根拠にするかが特定される。
- 完全セル復元できない場合も、warningとraw保持で正規化RUNへ渡せる。

### O. 9 CSV別紙2 意味値分解

ブランチ案: `feat/mhlw-csv-annex2-semantic-records`

目的:

- 別紙2のHTML table cellを、カテゴリ単位recordと文書・試験ごとの意味値へ分解する。

対象:

- `別紙2` 表1 `カテゴリ分類表`
- `別紙2` 表2 `本ガイドラインの対象外`

完了条件:

- `◎` / `○` / `△` / `―` を、実施要否や適用度の候補値として分解する。
- 脚注番号をセル値から分離し、脚注参照として保持する。
- カテゴリ3のような複数表示行を、必要に応じてカテゴリ単位recordへ束ねる。
- 分解不能なセルは元値を残し、warningを付ける。

### P. 9 CSV別紙1 OCR/転記方針決定

ブランチ案: `docs/mhlw-csv-annex1-ocr-plan`

目的:

- `別紙1` 画像を、OCRするか、手入力転記するか、figure参照に留めるか判断する。

対象:

- `https://www.mhlw.go.jp/web/t_img?img=6676058`

完了条件:

- 画像をGit管理対象にするか判断する。
- OCRを使う場合の再現手順、手入力の場合のレビュー方法を決める。
- IR上でfigure扱い、説明ノード、表/フロー構造のどれにするか方針を決める。

方針:

- OCRだけで正本化しない。
- 公式画像をlocal sourceとしてGit管理対象にし、まずIR上では `figure` として保持する。
- OCRは補助入力に留め、フロー構造の分解は視覚レビューまたは手入力転記に基づく別RUNで扱う。
- 詳細は `docs/MHLW_CSV_ANNEX1_OCR_PLAN.md` に記録する。

### Q. 正規化RUN readiness判定

ブランチ案: `docs/normalized-run-readiness-6-9`

目的:

- 6/7/8/9について、正式な正規化RUNへ進む準備状況を判定する。

完了条件:

- 文書ごとに「正規化RUNへ進める / 追加開発が必要 / 保留」を明示する。
- 親PRでレビューすべき `promotion_candidate` の対象を定義する。
- 子PRで `data/normalized/` へ昇格する範囲を、文書単位で分ける。

## 推奨する次PR

次の実装PRは `docs/normalized-run-readiness-6-9` を推奨する。

理由:

- KからPまでの通常開発・方針決定が一通り終わる。
- 正式な正規化RUNへ進める文書と、追加RUNへ送る対象を分ける段階に入る。
- NIID視覚レビュー復元RUNやCSV別紙1 figure source化は、readiness判定で正規化RUN前の追加作業として明示できる。

## 正規化完成度の見通し

この計画を最後まで進めると、6/7/8/9は「正式な正規化RUNに進めるかどうかを文書ごとに判定できる地点」まで到達する。

ただし、全ての表・別紙が完全な意味正規化済みになるとは限らない。特に以下は、保留または別RUNになる可能性が高い。

- PDF視覚情報が必要な6表1。
- NIIDの複雑横長表 `別表4`, `別表5`, `別表8`。
- NIIDのセル結合・複数行セルを含む `付表2`, `付表4`, `別表7`, `別表10`。
- CSV `別紙1` の画像由来フロー。ただしOCRだけで正本化せず、まずfigure sourceとして保持する方針。

正式昇格は、この計画の最後に readiness を確認してから、正規化RUNとして実施する。
