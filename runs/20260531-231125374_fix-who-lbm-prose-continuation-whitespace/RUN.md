# RUN: WHO LBM prose continuation whitespace correction

- run_id: `20260531-231125374_fix-who-lbm-prose-continuation-whitespace`
- branch: `fix/who-lbm-prose-continuation-whitespace`
- target: WHO LBM 3rd general table/figure postprocess
- scope: WHO-specific postprocess and regression tests only

## 背景

正規化RUN `20260531-230645907_run-normalized-who-lbm-3rd-v5` の目検で、表 raw line ではない通常ノードに PDF 継続行インデントが残っていることを検出した。

例:

```text
Wear gloves to protect skin against chemical
                                               effects of detergents.
```

これは正規化後の本文としては不要な空白・改行であり、表や図の raw line 保存とは別扱いにする必要がある。

## 対応

- `who_lbm_general_tables` の WHO 個別後処理で、表・図の既知ブロック除去後に通常本文ノードの継続行インデントを畳む。
- `table_row.data.raw_line` や固定幅表の再構成用データには触れない。
- Annex 4 の箇条書きと Chapter 9 の本文保持を回帰テスト化。

## 検証

```text
$env:PYTHONPATH='src'; python -m pytest tests/test_text2ir_who_lbm_3rd.py tests/test_who_lbm_general_tables.py tests/test_who_lbm_chap8_survey_parser.py tests/test_who_lbm_heading_merge.py tests/test_who_lbm_v4_skip_toc_and_annex_heading.py -q
27 passed
```

## 備考

- 共通パーサには触れていない。
- 正規化候補・`data/normalized/` はこのPRに含めない。
