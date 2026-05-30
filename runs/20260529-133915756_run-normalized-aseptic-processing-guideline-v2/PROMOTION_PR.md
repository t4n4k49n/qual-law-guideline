# 無菌操作法指針 正式版昇格

## まとめ

承認済みの無菌操作法指針正規化候補を正式版ディレクトリへ反映します。これにより `data/normalized/` からPMDA無菌操作法指針を参照でき、後続のチェックシート候補抽出で正式データとして扱える状態になります。

## 変更内容

- `runs/20260529-133915756_run-normalized-aseptic-processing-guideline-v2/promotion_candidate/` から以下4ファイルを複写。
- 複写先: `data/normalized/jp_pmda_aseptic_processing_guideline_20110420/`
- `runs/20260529-133915756_run-normalized-aseptic-processing-guideline-v2/RUN.md` に昇格準備記録を追記。

## 昇格ファイル

- `jp_pmda_aseptic_processing_guideline_20110420.regdoc_ir.yaml`
- `jp_pmda_aseptic_processing_guideline_20110420.parser_profile.yaml`
- `jp_pmda_aseptic_processing_guideline_20110420.regdoc_profile.yaml`
- `jp_pmda_aseptic_processing_guideline_20110420.meta.yaml`

## 確認

- 親PR: `#221`
- 親PR merge commit: `99976f2501465113a68e23acd67ee7f6f6edfcd7`
- 昇格コミット: `4e2e73c`
- `promotion_candidate/` と `data/normalized/` のSHA-256一致を確認済み。
- `data/normalized/jp_pmda_aseptic_processing_guideline_20110420/` のpromotion goal check: pass。
- `data/normalized/jp_pmda_aseptic_processing_guideline_20110420/` のIR構造チェック: pass。
- `manifest.yaml` は運用どおり `data/normalized/` へ複写していません。
- このPRではパーサ修正や再生成を含めていません。

<!-- PR_BODY_FILE: runs/20260529-133915756_run-normalized-aseptic-processing-guideline-v2/PROMOTION_PR.md -->
