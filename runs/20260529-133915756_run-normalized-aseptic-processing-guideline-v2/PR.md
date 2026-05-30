# 無菌操作法指針 正規化RUN v2

## まとめ

却下された v1 を破棄し、無菌操作法指針の正規化候補を本文構造から作り直しました。`2.1` / `2.2` などの用語定義を section として分割し、`1）` / `2）` などの番号付き本文を item として分割しています。加えて、PDF由来の折返し改行と不要な本文内スペースを正規化し、`設計・運用`、`工程管理プログラム`、`デッドレグ`、`枝管内径` の形で確認しました。

このPRは親PRです。`data/normalized/` は変更せず、承認後に昇格専用の子PRで `promotion_candidate` から正式版へ複写します。

## 対象

- 文書: 無菌操作法による無菌医薬品の製造に関する指針
- doc_id: `jp_pmda_aseptic_processing_guideline_20110420`
- source PDF: `https://www.pmda.go.jp/files/000206144.pdf`
- source text: `data/human-readable/pmda/aseptic_processing_guideline/source_texts/000206144.txt`
- promotion candidate: `runs/20260529-133915756_run-normalized-aseptic-processing-guideline-v2/promotion_candidate/`
- parser profile: `jp_pmda_aseptic_processing_guideline_v1`
- schema: `qai.regdoc_ir.v4`

## 修正内容

- v1 の不正な run を削除。
- `2.x` を section として分割。
- `1）` / `2）` / `1)` / `2)` を item として分割。
- `用語：説明` を heading と text に分離。
- OCR 揺れの `1５. ４` を `15.4` section として扱う。
- item 分割後に表2/表3の raw table artifact が item 配下に残らないよう table adapter を修正。
- 無菌操作法指針では、非preformatted本文について ASCII 英数字間以外の空白を削除。
- 文末直後ではない空行由来の折返しを段落改行にしない。

## 検証結果

- goal check: PASS
  - nodes: 1116
  - section: 114
  - item: 630
  - table: 3
  - table_header: 3
  - table_row: 12
  - source span coverage: 1.0
- special structure audit: PASS
  - generated_tables: 3
  - generated_rows: 12
  - unresolved_special_blocks: 0
- focused tests: `7 passed`

## 目検確認

- `cha2.sec2_1`: `2.1 アイソレータ(isolator)` を section として確認。
- `cha2.sec2_2`: `2.2 アクセス制限バリアシステム...` を section として確認。
- `cha3.sec3_1.i1`: `1） 全般` を item として確認。
- `cha3.sec3_1.i2`: `2） 適用範囲` を item として確認。
- `cha3.sec3_1.i7`: `設計・運用`、`工程管理プログラム` を確認。
- 製薬用水の dead leg 文: `デッドレグ`、`枝管内径` を確認。
- `cha15.sec15_4`: OCR 揺れ `1５. ４ 保守・管理` を section として確認。
- 表1/2/3: `header_structure.spanning_headers` と 12 件の `table_row` を確認。

## レビュー用ファイル

- `runs/20260529-133915756_run-normalized-aseptic-processing-guideline-v2/RUN.md`
- `runs/20260529-133915756_run-normalized-aseptic-processing-guideline-v2/GOAL_CHECK.md`
- `runs/20260529-133915756_run-normalized-aseptic-processing-guideline-v2/SPECIAL_STRUCTURE_AUDIT.md`
- `runs/20260529-133915756_run-normalized-aseptic-processing-guideline-v2/SAMPLE_EXTRACT.md`
- `runs/20260529-133915756_run-normalized-aseptic-processing-guideline-v2/STRUCTURE_TABLE_REVIEW.md`

## 正式版昇格について

このPRでは `data/normalized/` を変更していません。承認後、子PRで `runs/20260529-133915756_run-normalized-aseptic-processing-guideline-v2/promotion_candidate/` から `data/normalized/jp_pmda_aseptic_processing_guideline_20110420/` へ複写します。

<!-- PR_BODY_FILE: runs/20260529-133915756_run-normalized-aseptic-processing-guideline-v2/PR.md -->
