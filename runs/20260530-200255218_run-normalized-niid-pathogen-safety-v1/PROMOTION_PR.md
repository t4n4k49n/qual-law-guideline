# NIID病原体等安全管理規程 正式版昇格

## まとめ

承認済みのNIID病原体等安全管理規程正規化候補を正式版ディレクトリへ反映します。これにより `data/normalized/` から本文6章と別表・付表16件を含む正式データを参照でき、後続のチェックシート候補抽出で利用できる状態になります。

## 変更内容

- `runs/20260530-200255218_run-normalized-niid-pathogen-safety-v1/promotion_candidate/` から以下4ファイルを複写。
- 複写先: `data/normalized/jp_niid_pathogen_safety_management_20240401/`
- `runs/20260530-200255218_run-normalized-niid-pathogen-safety-v1/RUN.md` に昇格準備記録を追記。

## 昇格ファイル

- `jp_niid_pathogen_safety_management_20240401.regdoc_ir.yaml`
- `jp_niid_pathogen_safety_management_20240401.parser_profile.yaml`
- `jp_niid_pathogen_safety_management_20240401.regdoc_profile.yaml`
- `jp_niid_pathogen_safety_management_20240401.meta.yaml`

## 確認

- 親PR: `#223`
- 親PR merge commit: `925652b6dfc6e383479cf125934f77395fdd0502`
- 昇格コミット: `f5614dcb1ee7e3312da6af846e5cf923aff5d761`
- `promotion_candidate/` と `data/normalized/` のSHA-256一致を確認済み。
- `data/normalized/jp_niid_pathogen_safety_management_20240401/` のpromotion goal check: pass。
- `data/normalized/jp_niid_pathogen_safety_management_20240401/` のIR構造チェック: pass。
- `manifest.yaml` は運用どおり `data/normalized/` へ複写していません。
- このPRではパーサ修正や再生成を含めていません。

<!-- PR_BODY_FILE: runs/20260530-200255218_run-normalized-niid-pathogen-safety-v1/PROMOTION_PR.md -->
