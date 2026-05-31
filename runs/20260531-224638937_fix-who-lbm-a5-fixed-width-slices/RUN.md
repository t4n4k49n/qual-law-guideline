# RUN: WHO LBM A5 fixed-width slice correction

- run_id: `20260531-224638937_fix-who-lbm-a5-fixed-width-slices`
- branch: `fix/who-lbm-a5-fixed-width-slices`
- target: WHO Laboratory Biosafety Manual, 3rd ed. Annex 5 table parsing
- scope: WHO-specific parser only

## 背景

正規化RUN `20260531-223152118_run-normalized-who-lbm-3rd-v3` の目検で、`Table A5-1. Chemicals: hazards and precautions` の固定幅切り出しに不整合を検出した。

具体的には、A5-1 の Acetaldehyde 行で原文 `Can form explosive` が `C` / `an form explosive` に分割されていた。これは結合セル由来の許容差ではなく、A5-1 の固定幅 slice 境界指定ミス。

## 対応

- `src/qai_text2ir/who_lbm_general_tables.py`
  - WHO LBM 個別パーサの A5-1 slice 境界のみ変更。
  - 最終2列の境界を `128` から `125` に変更し、`Can form explosive` を第6列に保持。
- `tests/test_who_lbm_general_tables.py`
  - Acetaldehyde 行の第5列/第6列が語中分断されないことを追加検証。

## 検証

```text
$env:PYTHONPATH='src'; python -m pytest tests/test_who_lbm_general_tables.py -q
...........                                                              [100%]
11 passed in 32.94s
```

## 備考

- 共通パーサには触れていない。
- 正規化候補・`data/normalized/` はこのPRに含めない。
