# RUN: WHO LBM running header title strip correction

- run_id: `20260531-230337550_fix-who-lbm-running-header-title-strip`
- branch: `fix/who-lbm-running-header-title-strip`
- target: WHO LBM 3rd parser profile v4
- scope: WHO-specific profile and regression test only

## 背景

正規化RUN `20260531-225950608_run-normalized-who-lbm-3rd-v4` の目検で、Chapter 9 冒頭の本文が壊れていることを検出した。

原文:

```text
The Laboratory biosafety manual has in the past focused on traditional biosafety
```

生成IR:

```text
The  has in the past focused on traditional biosafety
```

原因は `who_lbm_3rd_default_v4.yaml` の `strip_inline_regexes` が、独立した柱だけでなく本文中の `Laboratory biosafety manual` も削っていたこと。

## 対応

- `LABORATORY BIOSAFETY MANUAL` の除去を inline strip から standalone line drop に変更。
- Chapter 9 の本文で `The Laboratory biosafety manual has...` が保持される回帰テストを追加。

## 検証

```text
$env:PYTHONPATH='src'; python -m pytest tests/test_text2ir_who_lbm_3rd.py tests/test_who_lbm_general_tables.py tests/test_who_lbm_chap8_survey_parser.py tests/test_who_lbm_heading_merge.py tests/test_who_lbm_v4_skip_toc_and_annex_heading.py -q
26 passed
```

## 備考

- 共通パーサには触れていない。
- 正規化候補・`data/normalized/` はこのPRに含めない。
