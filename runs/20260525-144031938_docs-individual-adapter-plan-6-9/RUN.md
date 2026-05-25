# RUN: 20260525-144031938_docs-individual-adapter-plan-6-9

## 目的

6/7/8/9のParser開発で見えた個別処理候補を振り返り、後続の個別adapter開発計画として文書化する。

このRUNはドキュメント整備であり、正式な正規化RUNではない。`data/normalized/` への昇格や、正規化承認を前提にしない。

## 対象

- `docs/NORMALIZATION_PLAN_6_9.md`
- `docs/INDIVIDUAL_ADAPTER_PLAN_6_9.md`

## 実施内容

- `docs/INDIVIDUAL_ADAPTER_PLAN_6_9.md` を追加した。
  - 共通化してよいもの、個別profile/adapterに閉じるものの判断基準を整理。
  - 6/7/8/9それぞれの残り個別処理候補を棚卸し。
  - 候補表示制御、8b別表・付表、6表1、7固定幅表候補、9別紙の優先順を整理。
  - 後続フェーズ案とブランチ案を記載。
- `docs/NORMALIZATION_PLAN_6_9.md` から個別adapter計画への参照を追加した。

## 個別と共通の整理

- 共通化判断は、文書名や特定表題に依存しないこと、複数文書で成立すること、回帰テストで副作用がないことを条件にした。
- 表紙、序文、通知名、別表境界、文書別番号階層、対象外OK範囲は個別profile/adapterまたはcandidate visibilityで扱う方針にした。

## 検証

- ドキュメントのみの変更。
- 絶対パス混入チェックを実行し、該当なし。

## 参照

- `runs/20260525-120304474_feat-jp-text2ir-base/RUN.md`
- `runs/20260525-121645707_run-normalized-api-gmp-guideline-v1/RUN.md`
- `runs/20260525-121645707_run-normalized-api-gmp-guideline-v1/ADAPTER_NOTES.md`
- `runs/20260525-133209443_feat-aseptic-processing-parser-v1/RUN.md`
- `runs/20260525-134750168_feat-csv-guideline-parser-v1/RUN.md`
- `runs/20260525-135841668_feat-niid-pathogen-safety-parser-v1/RUN.md`
