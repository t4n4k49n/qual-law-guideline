# WHO LBM表間本文の順序保持修正

## まとめ

WHO LBM正規化候補で、表と表の間にある本文が親sectionのtextへ巻き戻って見える問題を修正します。表を単に末尾へ追加するのではなく、本文中の表ブロック位置で分割し、表後本文を `statement` として表ノードの後ろに置くことで、原文の読解順をIR上でも追えるようにします。

## 変更内容

- WHO LBM個別処理で表ブロック位置に基づく本文分割を追加
- 表後本文を `statement` child として表の後ろへ配置
- child挿入をsource line順に揃えるヘルパを追加
- Chapter 1の Table 1 / Table 2 / Table 3 周辺を回帰テスト化

## 検証

- `python -m pytest tests/test_who_lbm_general_tables.py -q`
  - `13 passed`
- `python -m pytest tests/test_who_lbm_general_tables.py tests/test_who_lbm_v4_skip_toc_and_annex_heading.py tests/test_who_lbm_v3_skip_blocks.py tests/test_who_lbm_v2_drop_toc_and_annex_dedupe.py tests/test_who_lbm_heading_merge.py tests/test_who_lbm_chap8_survey_parser.py tests/test_text2ir_who_lbm_3rd.py -q`
  - `32 passed`
- 補助生成候補で `goal_check`: `PASS`
- 補助生成候補で `special_structure_audit`: `pass`
- 補助生成候補で `tools/check_ir_structure.py`: `[OK] no structure problems found`
- 全親ノードで、表・本文statement・item等のsource line順に逆転がないことを確認

## 対象外

- `data/normalized/` への昇格は含めない
- 正規化候補PRはこの修正後に作り直す
- 共通パーサの変更は含めない

<!-- PR_BODY_FILE: runs/20260601-001724865_fix-who-lbm-inline-table-order/PR.md -->
