<!-- PR_BODY_FILE: runs/20260531-125138676_run-normalized-mhlw-csv-guideline-v3/PROMOTION_PR.md -->

# MHLW CSVガイドライン 正式版昇格

## まとめ

承認済みのMHLW CSVガイドライン v3 正規化候補を正式版ディレクトリへ反映する。本文階層と別紙2カテゴリ分類表をレビュー済みの候補として `data/normalized/` から参照できるようにし、後続のチェックシート候補抽出や文脈表示で利用する正式データを追加する。

## 変更内容

- `runs/20260531-125138676_run-normalized-mhlw-csv-guideline-v3/promotion_candidate/` から以下4ファイルを複写。
- 複写先: `data/normalized/jp_mhlw_csv_guideline_20101021/`
- `runs/20260531-125138676_run-normalized-mhlw-csv-guideline-v3/RUN.md` に昇格準備記録を追記。

## 昇格ファイル

- `jp_mhlw_csv_guideline_20101021.regdoc_ir.yaml`
- `jp_mhlw_csv_guideline_20101021.parser_profile.yaml`
- `jp_mhlw_csv_guideline_20101021.regdoc_profile.yaml`
- `jp_mhlw_csv_guideline_20101021.meta.yaml`

## 確認

- 親PR: `#232`
- 親PR merge commit: `f0941b7`
- `promotion_candidate/` と `data/normalized/` のSHA-256一致を確認済み。
- `data/normalized/jp_mhlw_csv_guideline_20101021/` のpromotion goal check: pass。
- `data/normalized/jp_mhlw_csv_guideline_20101021/` のspecial structure audit: pass。
- `data/normalized/jp_mhlw_csv_guideline_20101021/` のIR構造チェック: pass。
- `manifest.yaml` は運用どおり `data/normalized/` へ複写していません。
- このPRではパーサ修正や再生成を含めていません。
