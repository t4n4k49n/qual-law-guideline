# RUN

- run_id: `20260529-133915756_run-normalized-aseptic-processing-guideline-v2`
- branch: `run/normalized-aseptic-processing-guideline-v1`
- generation_commit: `ce9724f`
- target: 無菌操作法による無菌医薬品の製造に関する指針
- doc_id: `jp_pmda_aseptic_processing_guideline_20110420`
- source_pdf: `https://www.pmda.go.jp/files/000206144.pdf`
- source_text: `data/human-readable/pmda/aseptic_processing_guideline/source_texts/000206144.txt`
- promotion_candidate: `runs/20260529-133915756_run-normalized-aseptic-processing-guideline-v2/promotion_candidate/`

## Purpose

却下された v1 では、本文構造の目検確認が不足し、2.1/2.2 などの用語定義節と 1）/2）などの番号付き項目が本文に畳み込まれていた。

v2 では parser/profile を修正し、本文階層を再生成したうえで、表・heading・本文内の折返し空白を再確認する。

この親PRでは `data/normalized/` を変更しない。正式版への複写は親PR承認後の子PRで実施する。

## Parser Fixes

- `2.x` を section として分割する。
- `1）` / `2）` / `1)` / `2)` を item として分割する。
- 定義形式の `用語：説明` は section heading と section text に分ける。
- OCR 揺れの `1５. ４` を `15.4` section として扱う。
- item 分割後に表2/表3の raw table artifact が item 配下に残らないよう、table adapter の掃除範囲を拡張する。
- 無菌操作法指針では、非preformatted本文について ASCII 英数字間以外の空白を削除する。
- 空行による折返しは、直前が文末記号でない限り段落改行にしない。

## Command

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.cli bundle --input data/human-readable/pmda/aseptic_processing_guideline/source_texts/000206144.txt --out-dir runs/20260529-133915756_run-normalized-aseptic-processing-guideline-v2/promotion_candidate --doc-id jp_pmda_aseptic_processing_guideline_20110420 --title "無菌操作法による無菌医薬品の製造に関する指針" --short-title "無菌操作法指針" --doc-type guideline --source-url https://www.pmda.go.jp/files/000206144.pdf --source-format pdf --retrieved-at 2026-02-18 --parser-profile src/qai_text2ir/profiles/jp_pmda_aseptic_processing_guideline_v1.yaml --jurisdiction JP --language ja --family JP_GUIDELINE --strict --write-manifest --overwrite-manifest
```

## Environment

- python_executable: `.venv\Scripts\python.exe`
- python_version: `3.11.6`
- lxml: `6.0.2`
- PyYAML: `6.0.3`
- typer: `0.24.0`
- tool_version: not set

## Validation

- `qai_text2ir.goal_check`: PASS
  - schema: `qai.regdoc_ir.v4`
  - nodes: 1116
  - source span coverage: 1.0
  - section: 114
  - item: 630
  - table: 3
  - table_header: 3
  - table_row: 12
- `qai_text2ir.special_structure_audit`: PASS
  - generated_tables: 3
  - generated_rows: 12
  - unresolved_special_blocks: 0
- focused tests: `7 passed`

## Manual Review Notes

- `cha2.sec2_1`: heading `アイソレータ(isolator)`、text は説明本文。
- `cha2.sec2_2`: heading `アクセス制限バリアシステム（RABS:Restricted Access Barrier System）`、text は説明本文。
- `cha3.sec3_1.i1`: `1） 全般` が item。
- `cha3.sec3_1.i2`: `2） 適用範囲` が item。
- `cha3.sec3_1.i7`: `設計・運用`、`工程管理プログラム` に正規化済み。
- `cha15.sec15_4`: OCR 揺れ `1５. ４ 保守・管理` を section として復元。
- 製薬用水の dead leg 文は `デッドレグ`、`枝管内径` に正規化済み。
- 表1、表2、表3は `header_structure.spanning_headers` と 12 `table_row` を保持。

## Promotion Status

- Parent PR stage only.
- `data/normalized/` is intentionally unchanged in this run.

## Promotion Preparation

- Parent PR: `#221`
- Parent merge commit: `99976f2501465113a68e23acd67ee7f6f6edfcd7`
- Promotion branch: `promote/aseptic-processing-guideline-v2`
- Promotion commit: `4e2e73c`
- Promotion source: `runs/20260529-133915756_run-normalized-aseptic-processing-guideline-v2/promotion_candidate/`
- Destination: `data/normalized/jp_pmda_aseptic_processing_guideline_20110420/`
- Copied files:
  - `jp_pmda_aseptic_processing_guideline_20110420.regdoc_ir.yaml`
  - `jp_pmda_aseptic_processing_guideline_20110420.parser_profile.yaml`
  - `jp_pmda_aseptic_processing_guideline_20110420.regdoc_profile.yaml`
  - `jp_pmda_aseptic_processing_guideline_20110420.meta.yaml`
- SHA-256 match between `promotion_candidate/` and `data/normalized/`: confirmed.
- Promotion goal check on `data/normalized/jp_pmda_aseptic_processing_guideline_20110420/`: pass. `manifest.yaml` is not copied to `data/normalized/` by design.
- IR structure check on `data/normalized/jp_pmda_aseptic_processing_guideline_20110420/`: pass.
