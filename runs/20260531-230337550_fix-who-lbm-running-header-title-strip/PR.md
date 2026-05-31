# WHO LBM本文中タイトル句の誤削除修正

## まとめ

WHO LBM 3rd の本文で、柱として除去すべき `LABORATORY BIOSAFETY MANUAL` と本文中に現れる `Laboratory biosafety manual` を区別するようにした。正規化候補で本文欠落を出さないための前提修正であり、対象は WHO v4 profile に限定している。

## 変更内容

- `LABORATORY BIOSAFETY MANUAL` を inline strip から standalone line drop に変更
- Chapter 9 冒頭の `The Laboratory biosafety manual has...` が保持される回帰テストを追加

## 検証

```text
$env:PYTHONPATH='src'; python -m pytest tests/test_text2ir_who_lbm_3rd.py tests/test_who_lbm_general_tables.py tests/test_who_lbm_chap8_survey_parser.py tests/test_who_lbm_heading_merge.py tests/test_who_lbm_v4_skip_toc_and_annex_heading.py -q
26 passed
```

## 対象外

- 共通パーサの変更
- 正規化候補の追加
- `data/normalized/` の更新

<!-- PR_BODY_FILE: runs/20260531-230337550_fix-who-lbm-running-header-title-strip/PR.md -->
