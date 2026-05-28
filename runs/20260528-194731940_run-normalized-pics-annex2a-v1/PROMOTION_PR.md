# PIC/S Annex 2A 正式版昇格

## まとめ

承認済みのPIC/S Annex 2A正規化候補を正式版ディレクトリへ反映します。これにより `data/normalized/` からAnnex 2Aを参照できるようになり、Annex 1 / Annex 11 と同じ運用対象に加わります。

## 変更内容

- `runs/20260528-194731940_run-normalized-pics-annex2a-v1/promotion_candidate/` から以下4ファイルを複写。
- 複写先: `data/normalized/pics_pe00917_annex2a_20230825/`

## 昇格ファイル

- `pics_pe00917_annex2a_20230825.regdoc_ir.yaml`
- `pics_pe00917_annex2a_20230825.parser_profile.yaml`
- `pics_pe00917_annex2a_20230825.regdoc_profile.yaml`
- `pics_pe00917_annex2a_20230825.meta.yaml`

## 確認

- 親PR: `#202`
- 親PR merge commit: `614228eb08d96d2cd0c09b03f59025ce17b3fde6`
- `promotion_candidate/` と `data/normalized/` のSHA-256一致を確認済み。
- 子PRにはパーサ修正や再生成を含めていません。

<!-- PR_BODY_FILE: runs/20260528-194731940_run-normalized-pics-annex2a-v1/PROMOTION_PR.md -->
