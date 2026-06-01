# EU GMP Vol.4 Chapter 3 正規化版へ昇格

## まとめ

レビュー済みのEU GMP Vol.4 Chapter 3（Premises and Equipment）正規化候補を正式版へ昇格します。施設・設備に関する要求事項を `data/normalized/` から参照できるようにし、DQのGMPチェックシートでChap1/Chap2と同じ運用に乗せます。

## 対象

- doc_id: `eu_gmp_vol4_chap3_20150123`
- 親PR: `#249`
- 昇格元: `runs/20260601-145404466_run-normalized-eu-gmp-vol4-chap3-v2/promotion_candidate/`
- 昇格先: `data/normalized/eu_gmp_vol4_chap3_20150123/`

## 変更内容

- `promotion_candidate` の4ファイルを `data/normalized/eu_gmp_vol4_chap3_20150123/` へ複写
  - `eu_gmp_vol4_chap3_20150123.regdoc_ir.yaml`
  - `eu_gmp_vol4_chap3_20150123.parser_profile.yaml`
  - `eu_gmp_vol4_chap3_20150123.regdoc_profile.yaml`
  - `eu_gmp_vol4_chap3_20150123.meta.yaml`
- `RUN.md` に昇格実施記録を追記

## 確認

- 親PR `#249` はmainへ反映済み
- `regdoc_ir.yaml` のSHA256は昇格元と昇格先で一致
  - `5F60CC15F647BAA388E9CA7AB9363FE873912223F5D0F651D576C70E33F1538E`

<!-- PR_BODY_FILE: runs/20260601-145404466_run-normalized-eu-gmp-vol4-chap3-v2/PROMOTION_PR.md -->
