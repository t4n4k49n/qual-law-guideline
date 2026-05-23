<!-- PR_BODY_FILE: runs/20260523-130131075_feat-pics-annexes-bundle-specials/PR_BODY.md -->

## まとめ

PIC/S Annexes combined文書で、既存のAnnex 1/Annex 2A特殊パーサーを維持したまま、Annex 2B Table 1とAnnex 20 Figure 1をIR上の構造化ノードとして扱えるようにしました。表・図が本文テキストに埋もれる状態を減らし、DQ/GMPチェックリスト側で行単位・図単位の参照品質を安定させるための追加です。

## 変更内容

- `pics_annexes_bundle_specials` を追加し、Annex 2B Table 1とAnnex 20 Figure 1を後処理で構造化
- `pics_annexes_default_v3` で新パーサーを有効化
- `ANNEX 20*` をAnnex markerとして認識
- annex配下の構造種別として `figure` を許可
- 既存のAnnex 1/Annex 2A特殊パーサー結果を回帰テストで確認
- RUN成果物として報告Markdown/JSONを追加

## 確認結果

- Annex 2B Table 1: 6列、7行、7注記の `table` として出力
- Annex 20 Figure 1: informativeな `figure` として出力
- `verify_document`: pass
- Source span coverage: 1.0
- Promotion goal checkは未解決候補8件によりfailのまま
  - 残件はAnnex 3/7/14/19/20後半で、今回対象のAnnex 2B Table 1とAnnex 20 Figure 1は未解決一覧から除外済み

## テスト

- `python -m pytest tests\test_pics_annexes_bundle_specials.py -q`
- `python -m pytest tests\test_pics_annexes_bundle_specials.py tests\test_pics_annex1_tables.py tests\test_pics_annex2a_structures.py tests\test_pics_annexes_refine_v2.py tests\test_pics_annexes_refine_v3_fallback.py tests\test_pics_annexes_full_profile_v1.py tests\test_special_structure_audit.py -q`
- `python -m pytest tests\test_pics_annexes_bundle_specials.py tests\test_special_structure_audit.py -q`
