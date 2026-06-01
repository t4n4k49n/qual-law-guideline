<!-- PR_BODY_FILE: runs/20260601-152632412_eu-gmp-chap4-9-normalization-prep/PR.md -->

## まとめ

EU GMP Vol.4 Chapter 4-9 を次の正規化RUNでまとめて処理できるよう、共通parser profile、サンプルテスト、章別trial candidate、監査ログを追加しました。項番なし見出しの誤吸収と不要な改行・空白を重点確認し、参照文中の `Chapter 1` / `Chapter 7` が章見出し化する問題も事前に抑えています。

## 変更内容

- Chapter 4-9向け parser profile `eu_gmp_chap4_9_default_v1` を追加
- Chapter 4-9の見出し・note・footnote noise・空白正規化を確認するテストを追加
- `runs/20260601-152632412_eu-gmp-chap4-9-normalization-prep/` に準備RUN記録、trial candidate、監査ログを追加
- Chap4/Chap7の通常noteを `note` node として分離
- 表は検出0件のため、結合セル複写やtable note対応は不要と記録

## 確認結果

- `python -m pytest tests/test_text2ir_eu_gmp_chap1.py -q`
  - `9 passed`
- Chapter 4-9 各trial candidateで以下を実行済み
  - `qai_text2ir.goal_check --mode promotion`: PASS
  - `qai_text2ir.special_structure_audit --mode promotion`: pass
  - `tools/check_ir_structure.py`: OK

## 注意点

- これは正規化RUN本体ではなく、次RUNに向けた正規化準備PRです。
- Chapter 9はローカルsource textから日付を確認できないため、trial doc_id は `eu_gmp_vol4_chap9_undated` としています。正式な正規化RUNでは公式日付または採番方針を確認してください。
