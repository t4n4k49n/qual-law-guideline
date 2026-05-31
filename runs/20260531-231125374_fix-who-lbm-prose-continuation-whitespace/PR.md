# WHO LBM本文継続行の不要空白除去

## まとめ

WHO LBM 3rd の通常本文ノードに残っていた PDF 由来の継続行インデントを、WHO 個別後処理で畳むようにした。表の固定幅 raw line は維持したまま、本文として読むべき箇条書きや章本文の不要改行・空白を減らすための前提修正。

## 変更内容

- WHO 個別後処理で通常本文の継続行インデントを空白1つに正規化
- A4 箇条書きの継続行が `...chemical effects...` と読めることをテスト追加
- Chapter 9 の `Laboratory biosafety manual` が保持されることも併せて確認

## 検証

```text
$env:PYTHONPATH='src'; python -m pytest tests/test_text2ir_who_lbm_3rd.py tests/test_who_lbm_general_tables.py tests/test_who_lbm_chap8_survey_parser.py tests/test_who_lbm_heading_merge.py tests/test_who_lbm_v4_skip_toc_and_annex_heading.py -q
27 passed
```

## 対象外

- 共通パーサの変更
- 固定幅表の `raw_line` 正規化
- 正規化候補の追加
- `data/normalized/` の更新

<!-- PR_BODY_FILE: runs/20260531-231125374_fix-who-lbm-prose-continuation-whitespace/PR.md -->
