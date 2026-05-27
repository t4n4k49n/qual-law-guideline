## まとめ

PIC/S Annex 11の正規化候補を正式版として `data/normalized/` に昇格します。親PRでレビュー済みの `promotion_candidate/` をそのまま複写し、PIC/S単体Annexの正式データとして参照できる状態にします。

## 変更内容

- `runs/20260528-042535335_run-normalized-pics-annex11-v2/promotion_candidate/` の4ファイルを `data/normalized/pics_pe00917_annex11_20230825/` へ複写
- `RUN.md` に昇格記録を追記

## 確認

- 親PR #192 はmainにマージ済み
- 複写元と複写先の4ファイルはSHA-256一致
- `data/normalized/pics_pe00917_annex11_20230825` のpromotion GOALはPASS
- `manifest.yaml` はRUN記録のため `data/normalized/` へは複写しない

<!-- PR_BODY_FILE: runs/20260528-042535335_run-normalized-pics-annex11-v2/PROMOTION_PR.md -->
