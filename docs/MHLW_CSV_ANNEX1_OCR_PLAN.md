# CSVガイドライン 別紙1 OCR/転記方針

## 位置づけ

この文書は、9「CSVガイドライン」の `別紙1 コンピュータ化システムのライフサイクルモデル` について、画像由来情報をどう扱うかを決める。

ここで扱うのは通常の開発方針であり、正式な正規化RUNではない。`data/normalized/` への昇格は別途正規化RUNで行う。

## 入力

| 項目 | 内容 |
| --- | --- |
| HTML上の表示 | `画像1 (36KB)` |
| local HTML | `data/human-readable/mhlw/csv_guideline/00tb6573.html` |
| 画像候補URL | `https://www.mhlw.go.jp/web/t_img?img=6676058` |
| 既存判定 | `reachable_http_200` |
| 既存RUN | `runs/20260525-235003289_feat-mhlw-csv-annex-source-recovery/` |

## 判断

別紙1はOCRだけで正本化しない。

理由:

- HTML本文には画像リンクだけがあり、テキスト本文は存在しない。
- 対象はライフサイクルモデルの図であり、文字列だけでなく矢印、流れ、包含関係が意味を持つ。
- OCRは文字候補の取得には使えるが、フロー構造の正規化には視覚判断または手入力レビューが必要。
- OCR結果をそのまま正規化すると、矢印方向やフェーズ境界を欠落させるリスクが高い。

## 方針

### 1. 画像の扱い

- 次の実装RUNで公式画像を取得し、`data/human-readable/mhlw/csv_guideline/annex1/` 配下に保存する。
- 取得元URL、取得日時、ハッシュをRUNに記録する。
- 画像ファイルは正本ソースの一部としてGit管理対象にする。

### 2. OCRの扱い

- OCRは補助入力としてのみ使う。
- OCR結果は `out/<run_id>/` に生成し、レビューに使う抜粋だけを `runs/<run_id>/` に残す。
- OCR結果をそのままIR本文や正式候補にしない。

### 3. IR上の扱い

最初の実装では、別紙1を `figure` として保持する。

保持する情報:

- 図タイトル: `コンピュータ化システムのライフサイクルモデル`
- 公式画像URL
- local image path
- image hash
- `figure_reconstruction_status: source_image_preserved`

フロー構造を分解する場合は、別RUNで `lifecycle_step` 相当の補助recordを作る。ただし、これは画像の視覚レビューまたは手入力転記に基づくため、コードだけで再生成できる成果物と区別する。

### 4. レビュー方法

- 画像を正として、OCR文字列または手入力文字列を照合する。
- 矢印・順序・分岐・包含関係は視覚レビューで確認する。
- 転記したテキストには、根拠画像と確認者向けのレビュー表を付ける。

## 次アクション

次の実装対象にする場合は、`feat/mhlw-csv-annex1-figure-source` として切る。

完了条件:

- 公式画像をlocal sourceとして取得し、ハッシュを記録する。
- 別紙1 annex配下に `figure` nodeを追加する。
- OCRを実施する場合でも、OCR結果は補助扱いに留める。
- フローの意味分解をするかどうかは、正規化RUN readinessで判断する。
