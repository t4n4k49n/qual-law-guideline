# RUN: 20260525-153057355_feat-api-gmp-table1-adapter-v1

## 目的

6/7/8/9 個別adapter開発計画のフェーズCとして、6「原薬GMPガイドライン」の `表１：原薬生産に対する本ガイドラインの適用` を、RUN内の手作業置換なしで保持する。

これはParser/adapter開発であり、正式な正規化RUNではない。`data/normalized/` への昇格は行わない。

## 対象

- 入力: `data/human-readable/pmda/api_gmp_guideline/source_texts/000156438.txt`
- 対象範囲: `表１：原薬生産に対する本ガイドラインの適用` から `2. 品質マネージメント` の直前まで
- 出力確認先: `out/20260525-153057355_feat-api-gmp-table1-adapter-v1/`

## 実装

- `src/qai_text2ir/api_gmp_table1.py` を追加した。
- `jp_pmda_api_gmp_guideline_v1` profileでのみ `api_gmp_table1.enabled` を有効化した。
- 共通の緩い固定幅表検出は追加していない。
- raw TXTの表1ブロックを、`table -> table_header -> table_row` として保持した。
- table headerは `raw_line` 1列、table_rowは原文非空行ごとの26行とした。

## 共通化しない理由

原薬GMPガイドライン表1は、PDF由来TXTで列位置が崩れている。一般的な固定幅表検出として共通parserに入れると、通常本文や箇条書きをtable扱いするリスクが高い。

今回のadapterは、対象captionと次章境界が明確なAPI GMP表1だけに閉じ、本文階層へ副作用を出さないことを優先した。

## 結果

- raw source `000156438.txt` から、手作業でmarkdown tableへ置換せずに表1を保持できた。
- `cha1.p1_3.tbl1` にtableを追加した。
- `cha1.p1_3.tbl1.tblh.tblr1` から `tblr26` まで、原文非空行を1行1rowで保持した。
- `cha1.p1_3` の本文から表1ブロックを除去し、表は子nodeとして保持した。
- source spanはcaption行および各raw行の行番号を保持する。

## 正規化度

このRUNの正規化度は中程度未満であり、「表を構造nodeとして保持する段階」とする。

達成済み:

- 表1が `table` / `table_header` / `table_row` としてIR上で追跡できる。
- raw sourceから再生成でき、RUN内の入力置換に依存しない。
- DQ候補に出せる `table_row` 粒度は確保した。

未達:

- 列復元。
- rowを製造形態ごとの意味単位へ再結合する処理。
- 灰色部分の視覚情報復元。
- 各工程セルの意味付け。

したがって、この出力は「表1を完全に列正規化したもの」ではなく、「後続で列復元・意味付けを検討できるraw row保持形」として扱う。

## この開発に入れない課題

- 列復元はこのフェーズに入れない。PDF抽出TXTだけではセル境界が崩れており、推定ルールを入れるとAPI GMP固有の解釈が強くなるため、別フェーズで必要性を確認する。
- `special_structure_audit` の日本語固定幅表検出強化はこのフェーズに入れない。共通監査の検出条件を緩めると他文書への誤検出リスクがあるため、今回はadapter生成結果で `generated_tables=1` / `generated_rows=26` を確認する。
- 灰色部分の復元はこのフェーズに入れない。テキスト層では視覚情報が失われており、PDFレイアウト解析または画像参照が必要になる。

## 検証

```text
.\.venv\Scripts\python.exe -m pytest tests\test_text2ir_api_gmp_guideline.py tests\test_text2ir_jp_guideline.py tests\test_markdown_table_parsing.py tests\test_table_note_real_samples.py -q
16 passed
```

```text
.\.venv\Scripts\python.exe -m qai_text2ir.cli bundle ... --input data\human-readable\pmda\api_gmp_guideline\source_texts\000156438.txt --parser-profile-id jp_pmda_api_gmp_guideline_v1 --strict --overwrite-manifest
PASS
```

```text
.\.venv\Scripts\python.exe -m qai_text2ir.goal_check ... --mode normal
Status: PASS
Nodes: 515
Kind counts: table 1, table_header 1, table_row 26
Source span coverage: 1.0
```

```text
.\.venv\Scripts\python.exe -m qai_text2ir.special_structure_audit ... --mode normal
Status: pass
generated_tables: 1
generated_rows: 26
unresolved_special_blocks: 0
```

## 監査ファイル

- `runs/20260525-153057355_feat-api-gmp-table1-adapter-v1/goal_check.md`
- `runs/20260525-153057355_feat-api-gmp-table1-adapter-v1/special_structure_audit.md`

## 次の個別開発候補

- 表1の列復元が本当に必要かレビューする。
- 必要な場合のみ、API GMP表1専用の列復元adapterを別フェーズで設計する。
- 今回のraw row保持adapterは、共通parserへ昇格せず文書固有部品として維持する。
