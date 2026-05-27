## まとめ

正規化RUNの深い階層サンプルを、手書きではなくIR YAMLから抽出できるようにしました。レビュー表の体裁は既存運用のまま維持しつつ、`kind_raw` や `nid` の転記ミスを避けられるようになります。

## 変更内容

- IR祖先経路のMarkdown抽出ツール `tools/extract_ir_sample.py` を追加
- 使い方を `docs/IR_SAMPLE_EXTRACT.md` に追加
- 正規化RUN playbookに `SAMPLE_EXTRACT.md` の作成手順を追加
- 抽出ツールの単体テストを追加

## 検証

- `python -m pytest tests/test_extract_ir_sample.py -q`
- 実データ `eu_gmp_vol4_chap1_20130131.regdoc_ir.yaml` からの抽出

<!-- PR_BODY_FILE: runs/20260527-144134077_feat-ir-sample-extract-tool/PR.md -->
