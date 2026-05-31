# EU GMP Chapter 2 の正規化前提プロファイルを追加

## まとめ

EU GMP Vol.4 Chapter 2 を正規化する前提として、章固有のheading、責務リスト、脚注、PDF由来の改行・空白を安定してIR化できるようにしました。これにより、次の正規化RUNで人がレビューできる構造の候補を生成できる状態にします。

## 変更内容

- EU GMP Chapter 2 専用プロファイル `eu_gmp_chap2_default_v1` を追加
- Chapter 2 専用の空白・改行cleanupを追加
- プロファイルで明示された場合だけcleanupを呼ぶ最小フックを追加
- Chapter 2 のheading、item階層、脚注混入防止の回帰テストを追加

## 検証

- `python -m pytest tests/test_text2ir_eu_gmp_chap1.py -q`
  - `7 passed`

## 注意

- このPRでは `data/normalized/` は変更しない
- このPRでは正規化候補の昇格もしない
- 承認後、main同期してからEU GMP Chapter 2の正規化RUNを作り直す

<!-- PR_BODY_FILE: runs/20260601-034015780_fix-eu-gmp-chap2-profile/PR.md -->
