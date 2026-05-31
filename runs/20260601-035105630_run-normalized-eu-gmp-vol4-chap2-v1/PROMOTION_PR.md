# EU GMP Vol.4 Chapter 2 正式版昇格

## まとめ

承認済みの正規化候補を正式な `data/normalized/` 配下へ反映します。レビュー済み候補と同一内容を昇格するだけの子PRで、パーサ変更や再生成は含めていません。

## 変更内容

- `runs/20260601-035105630_run-normalized-eu-gmp-vol4-chap2-v1/promotion_candidate/` の4ファイルを `data/normalized/eu_gmp_vol4_chap2_20140328/` へ複写
- `RUN.md` に昇格実施記録を追記
- 子PR本文のポリシー確認用に、このPR本文ファイルを追加

## 検証

- `tools/check_ir_structure.py data/normalized/eu_gmp_vol4_chap2_20140328`: OK
- `regdoc_ir.yaml` のSHA256が昇格元と昇格先で一致

## 注意

- 親PR: #246
- このPRにはパーサコード修正や追加の正規化再実行を含めていません

<!-- PR_BODY_FILE: runs/20260601-035105630_run-normalized-eu-gmp-vol4-chap2-v1/PROMOTION_PR.md -->
