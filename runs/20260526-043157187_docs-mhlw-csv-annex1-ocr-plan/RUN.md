# RUN: 20260526-043157187_docs-mhlw-csv-annex1-ocr-plan

## 目的

9「CSVガイドライン」の `別紙1 コンピュータ化システムのライフサイクルモデル` について、OCR、手入力転記、figure参照のどれで扱うかを決める。

このRUNはドキュメント整備であり、正式な正規化RUNではない。`data/normalized/` への昇格は行わない。

## 対象

- local HTML: `data/human-readable/mhlw/csv_guideline/00tb6573.html`
- 公式画像候補: `https://www.mhlw.go.jp/web/t_img?img=6676058`
- 既存ソース回収RUN: `runs/20260525-235003289_feat-mhlw-csv-annex-source-recovery/`

## 確認した事実

- local HTML上では `画像1 (36KB)` として参照される。
- 画像URLは既存RUNで `reachable_http_200` と判定済み。
- HTML本文には別紙1のテキスト本文はなく、画像参照のみが残る。
- 1.3本文では、ライフサイクル全体の構成を別紙1に示すと説明されている。

## 判断

別紙1はOCRだけで正本化しない。

理由:

- 別紙1はライフサイクルモデルの図であり、文字だけでなく矢印、順序、包含関係が意味を持つ。
- OCRは文字候補取得には使えるが、フロー構造の正規化には視覚判断または手入力レビューが必要。
- OCR結果をそのままIR本文や正式候補にすると、図の意味構造を誤って固定するリスクがある。

## 方針

- 次の実装対象にする場合は、公式画像を `data/human-readable/mhlw/csv_guideline/annex1/` 配下に取得し、ハッシュをRUNに記録する。
- IRではまず別紙1を `figure` nodeとして保持する。
- OCRは補助入力として `out/<run_id>/` に生成し、必要な抜粋だけ `runs/<run_id>/` に残す。
- フロー構造を `lifecycle_step` 相当へ分解する場合は、別RUNで視覚レビューまたは手入力転記に基づいて実施する。

## 実施内容

- `docs/MHLW_CSV_ANNEX1_OCR_PLAN.md` を追加した。
- `docs/REMAINING_NORMALIZATION_PLAN_6_9.md` を更新し、次PRを正規化RUN readiness判定へ進める方針に変更した。

## 次アクション

- 次は `Q. 正規化RUN readiness判定` に進む。
- readiness判定で、CSV別紙1を「figure source化が必要な追加RUN」として扱うか、figure参照のまま正規化RUNへ渡せるかを決める。

## 検証

ドキュメントのみの変更。コード・テストは変更していない。
