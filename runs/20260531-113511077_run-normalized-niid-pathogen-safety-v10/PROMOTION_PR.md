<!-- PR_BODY_FILE: runs/20260531-113511077_run-normalized-niid-pathogen-safety-v10/PROMOTION_PR.md -->

# NIID病原体等安全管理規程 v10 正式版昇格

## まとめ

承認済みのNIID病原体等安全管理規程 v10 正規化候補を正式版ディレクトリへ反映します。別表5の表外運搬基準を原文どおり表の後ろに保持したデータを `data/normalized/` から参照できるようにし、後続のチェックシート候補抽出や文脈表示で利用する正式データを更新します。

## 変更内容

- `runs/20260531-113511077_run-normalized-niid-pathogen-safety-v10/promotion_candidate/` から以下4ファイルを複写。
- 複写先: `data/normalized/jp_niid_pathogen_safety_management_20240401/`
- `runs/20260531-113511077_run-normalized-niid-pathogen-safety-v10/RUN.md` に昇格準備記録を追記。

## 昇格ファイル

- `jp_niid_pathogen_safety_management_20240401.regdoc_ir.yaml`
- `jp_niid_pathogen_safety_management_20240401.parser_profile.yaml`
- `jp_niid_pathogen_safety_management_20240401.regdoc_profile.yaml`
- `jp_niid_pathogen_safety_management_20240401.meta.yaml`

## 確認

- 親PR: `#227`
- 親PR merge commit: `83ab4a8`
- `promotion_candidate/` と `data/normalized/` のSHA-256一致を確認済み。
- `data/normalized/jp_niid_pathogen_safety_management_20240401/` のpromotion goal check: pass。
- `data/normalized/jp_niid_pathogen_safety_management_20240401/` のIR構造チェック: pass。
- `data/normalized/` 上で `ann5.tbl1` -> `ann5.not1` -> `ann5.not2` -> `ann5.not3` の順序を確認済み。
- `manifest.yaml` は運用どおり `data/normalized/` へ複写していません。
- このPRではパーサ修正や再生成を含めていません。
