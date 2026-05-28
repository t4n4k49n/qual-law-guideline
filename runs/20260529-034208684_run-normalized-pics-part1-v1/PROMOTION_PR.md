# PIC/S Part I 正式版昇格

## まとめ

承認済みのPIC/S Part I正規化候補を正式版ディレクトリへ反映します。これにより `data/normalized/` からPart Iを参照できるようになり、Part IIやAnnex群と並べてチェックシート候補抽出に使える状態になります。

## 変更内容

- `runs/20260529-034208684_run-normalized-pics-part1-v1/promotion_candidate/` から以下4ファイルを複写。
- 複写先: `data/normalized/pics_pe00917_part1_20230825/`
- `runs/20260529-034208684_run-normalized-pics-part1-v1/RUN.md` に昇格準備記録を追記。

## 昇格ファイル

- `pics_pe00917_part1_20230825.regdoc_ir.yaml`
- `pics_pe00917_part1_20230825.parser_profile.yaml`
- `pics_pe00917_part1_20230825.regdoc_profile.yaml`
- `pics_pe00917_part1_20230825.meta.yaml`

## 確認

- 親PR: `#208`
- 親PR merge commit: `3a899979d3412a24b8c50eb0bf3d1e093cd11fb9`
- `promotion_candidate/` と `data/normalized/` のSHA-256一致を確認済み。
- `data/normalized/pics_pe00917_part1_20230825/` のpromotion goal check: pass。
- promotion goal warningは `missing_manifest` のみ。manifestは運用上 `data/normalized/` へ複写しません。
- `data/normalized/pics_pe00917_part1_20230825/` のIR構造チェック: pass。
- このPRではパーサ修正や再生成を含めていません。

<!-- PR_BODY_FILE: runs/20260529-034208684_run-normalized-pics-part1-v1/PROMOTION_PR.md -->
