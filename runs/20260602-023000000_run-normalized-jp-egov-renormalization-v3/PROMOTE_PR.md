# 旧e-Gov正規化データを正式版へ昇格

## まとめ

承認済みの正規化RUN `#263` の候補を `data/normalized/` へ反映します。旧e-Gov正規化5件が現行IR基準の正式版となり、既存の参照先を変えずに、`article -> paragraph -> item` の一貫した構造を利用できる状態になります。

## 変更内容

- `runs/20260602-023000000_run-normalized-jp-egov-renormalization-v3/promotion_candidate/` から5文書を `data/normalized/<doc_id>/` へ複写
- `RUN.md` に昇格実施記録を追記
- `ARCHIVE_jp_egov_*` は昇格対象外として未変更

## 検証

- `tools/check_ir_structure.py data/normalized/<doc_id>`
  - 5件すべて `OK`
- SHA256確認
  - 各doc_idの4ファイルが昇格元と昇格先で一致

<!-- PR_BODY_FILE: runs/20260602-023000000_run-normalized-jp-egov-renormalization-v3/PROMOTE_PR.md -->
