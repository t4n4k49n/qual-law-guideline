## まとめ

EU GMP Vol.4 Chapter 1の正規化候補を正式版として `data/normalized/` に昇格します。親PRでレビュー済みの `promotion_candidate/` をそのまま複写し、DQチェックシート向けの正規化データとして参照できる状態にします。

## 変更内容

- `runs/20260527-133746129_run-normalized-eu-gmp-vol4-chap1-v1/promotion_candidate/` の4ファイルを `data/normalized/eu_gmp_vol4_chap1_20130131/` へ複写
- `RUN.md` に昇格記録を追記

## 確認

- 親PR #188 はmainにマージ済み
- 複写元と複写先の4ファイルはSHA-256一致
- `data/normalized/eu_gmp_vol4_chap1_20130131` のpromotion GOALはPASS
- `manifest.yaml` はRUN記録のため `data/normalized/` へは複写しない

<!-- PR_BODY_FILE: runs/20260527-133746129_run-normalized-eu-gmp-vol4-chap1-v1/PROMOTION_PR.md -->
