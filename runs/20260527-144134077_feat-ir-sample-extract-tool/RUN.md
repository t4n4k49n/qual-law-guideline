# RUN: 20260527-144134077_feat-ir-sample-extract-tool

## 目的

正規化RUNの深い階層サンプルを手書きせず、IR YAMLから再実行可能に抽出するツールと手順を追加する。

## ブランチ

- `feat-ir-sample-extract-tool`

## 変更

- `tools/extract_ir_sample.py` を追加
- `docs/IR_SAMPLE_EXTRACT.md` を追加
- `docs/NORMALIZED_RUN_PLAYBOOK.md` に抽出手順を追記
- `tests/test_extract_ir_sample.py` を追加

## 検証

- `python -m pytest tests/test_extract_ir_sample.py -q`: PASS（3 passed）
- 実データ抽出:

```powershell
python tools/extract_ir_sample.py `
  --ir runs/20260522-130045_text2ir-final-goal-closure/promotion_candidate/eu_gmp_vol4_chap1_20130131/eu_gmp_vol4_chap1_20130131.regdoc_ir.yaml `
  --nid cha1.p1_8.iiii.si3 `
  --output out/20260527-144134077_feat-ir-sample-extract-tool/eu_gmp_sample_extract.md `
  --blank-text-kind paragraph
```

結果:

- 既存PRで使っている `階層 / nid / kind / kind_raw / text / heading` の表体裁で出力できた。
- `cha1.p1_8.iiii` の `kind_raw` はIR由来で `(iii)` として出力された。
