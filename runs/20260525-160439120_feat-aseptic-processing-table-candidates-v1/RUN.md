# RUN: 20260525-160439120_feat-aseptic-processing-table-candidates-v1

## 目的

6/7/8/9 個別adapter開発計画のフェーズDとして、7「無菌操作法指針」で残っていた固定幅表候補を確認し、必要な範囲だけ個別adapterで保持する。

これはParser/adapter開発であり、正式な正規化RUNではない。`data/normalized/` への昇格は行わない。

## 対象

- 入力: `data/human-readable/pmda/aseptic_processing_guideline/source_texts/000206144.txt`
- 対象候補:
  - `cha7.p7_1`: lines 778-804, 表1「清浄区域の分類」
  - `cha11.p11_3`: lines 1285-1321, 表2「微生物管理に係る環境モニタリングの頻度」
  - `cha11.p11_3.pre1`: lines 1324-1331, 表3「環境微生物の許容基準(作業時)」
- 出力確認先: `out/20260525-160439120_feat-aseptic-processing-table-candidates-v1/`

## 判断

| 候補 | 判定 | 対応 |
| --- | --- | --- |
| `cha7.p7_1` | table化する | `表1` をraw line tableとして `cha7.p7_1.tbl1` へ分離 |
| `cha11.p11_3` | table化する | `表2` をraw line tableとして `cha11.p11_3.tbl2` へ分離 |
| `cha11.p11_3.pre1` | table化する | 既存preformattedを `表3` raw line table `cha11.p11_3.tbl3` へ置換 |

## 実装

- `src/qai_text2ir/aseptic_processing_tables.py` を追加した。
- `jp_pmda_aseptic_processing_guideline_v1` profileでのみ `aseptic_processing_tables.enabled` を有効化した。
- 共通の固定幅表検出は緩めていない。
- 3表を `table -> table_header -> table_row` として保持した。
- table headerは `raw_line` 1列、table_rowは原文非空行ごとのraw rowとした。

## 共通化しない理由

対象3表は、PDF由来TXT上でヘッダ分割、複数行セル、注記、空行、ページ番号が混在する。共通parserでこの崩れ方を一律にtable化すると、通常本文や箇条書きを誤ってtable扱いするリスクがある。

今回は無菌操作法指針の既知captionと既知章節に閉じた個別adapterとして扱う。

## 結果

- `cha7.p7_1.tbl1`: table row 14件。
- `cha11.p11_3.tbl2`: table row 9件。
- `cha11.p11_3.tbl3`: table row 7件。
- 合計 `table` 3件、`table_row` 30件を生成した。
- `special_structure_audit` の未解決候補は 3件から 0件になった。
- 表1/表2は親paragraph本文から表ブロックを除去し、表を子nodeに分離した。
- 表3は既存の `preformatted possible_table` からtable nodeへ置換した。

## 正規化度

このRUNの正規化度は中程度未満であり、「表候補をtable nodeとして分離保持する段階」とする。

達成済み:

- 表1/表2/表3が `table` / `table_header` / `table_row` としてIR上で追跡できる。
- DQ候補に出せる `table_row` 粒度は確保した。
- source span付きで原文行へ戻れる。
- 既存の未解決特殊構造候補は解消した。

未達:

- 列復元。
- 複数行セルの再結合。
- ヘッダ階層の意味付け。
- 注記参照とセルの対応付け。

したがって、この出力は「表内容をセル単位で正規化済み」ではなく、「後続で列復元・意味付けを検討できるraw row保持形」として扱う。

## この開発に入れない課題

- 列復元はこのフェーズに入れない。表1/表2は複数行セルが多く、表3もヘッダが複数段に分かれるため、推定でセル化すると誤った意味付けを固定するリスクがある。
- 共通parserの固定幅表検出強化はこのフェーズに入れない。対象3表はPMDA無菌操作法指針の既知captionと章節に依存するため、共通化条件を満たしていない。
- 注記とセルの対応付けはこのフェーズに入れない。表1の注1/注2、表3の注1/注2はtable noteとして保持するに留める。

## 検証

```text
.\.venv\Scripts\python.exe -m pytest tests\test_text2ir_aseptic_processing_guideline.py tests\test_text2ir_jp_guideline.py tests\test_text2ir_goal_check.py tests\test_special_structure_audit.py -q
20 passed
```

```text
.\.venv\Scripts\python.exe -m qai_text2ir.cli bundle ... --input data\human-readable\pmda\aseptic_processing_guideline\source_texts\000206144.txt --parser-profile-id jp_pmda_aseptic_processing_guideline_v1 --strict --overwrite-manifest
PASS
```

```text
.\.venv\Scripts\python.exe -m qai_text2ir.goal_check ... --mode normal
Status: PASS
Nodes: 505
Kind counts: table 3, table_header 3, table_row 30
Source span coverage: 1.0
```

```text
.\.venv\Scripts\python.exe -m qai_text2ir.special_structure_audit ... --mode normal
Status: pass
generated_tables: 3
generated_rows: 30
unresolved_special_blocks: 0
```

## 監査ファイル

- `runs/20260525-160439120_feat-aseptic-processing-table-candidates-v1/goal_check.md`
- `runs/20260525-160439120_feat-aseptic-processing-table-candidates-v1/special_structure_audit.md`

## 次の個別開発候補

- 表1/表2/表3の列復元が本当に必要かレビューする。
- 必要な場合のみ、無菌操作法指針専用の列復元adapterを別フェーズで設計する。
- 今回のraw row保持adapterは、共通parserへ昇格せず文書固有部品として維持する。
