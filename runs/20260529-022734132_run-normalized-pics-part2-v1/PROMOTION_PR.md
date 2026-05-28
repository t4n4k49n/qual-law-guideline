# PIC/S Part II 正式版昇格

## まとめ

承認済みのPIC/S Part II正規化候補を正式版ディレクトリへ反映します。これにより `data/normalized/` からPart IIを参照できるようになり、PIC/S本文系の正式データとして後続のチェックシート候補抽出に使える状態になります。

## 変更内容

- `runs/20260529-022734132_run-normalized-pics-part2-v1/promotion_candidate/` から以下4ファイルを複写。
- 複写先: `data/normalized/pics_pe00917_part2_20230825/`
- `runs/20260529-022734132_run-normalized-pics-part2-v1/RUN.md` に昇格準備記録を追記。

## 昇格ファイル

- `pics_pe00917_part2_20230825.regdoc_ir.yaml`
- `pics_pe00917_part2_20230825.parser_profile.yaml`
- `pics_pe00917_part2_20230825.regdoc_profile.yaml`
- `pics_pe00917_part2_20230825.meta.yaml`

## 確認

- 親PR: `#205`
- 親PR merge commit: `fe39bd673f83402867502a4b821b228c6634b8df`
- `promotion_candidate/` と `data/normalized/` のSHA-256一致を確認済み。
- `data/normalized/pics_pe00917_part2_20230825/` のpromotion goal check: pass。
- `data/normalized/pics_pe00917_part2_20230825/` のIR構造チェック: pass。
- このPRではパーサ修正や再生成を含めていません。

<!-- PR_BODY_FILE: runs/20260529-022734132_run-normalized-pics-part2-v1/PROMOTION_PR.md -->
