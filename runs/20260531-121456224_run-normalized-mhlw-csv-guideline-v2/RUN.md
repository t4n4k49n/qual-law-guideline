# 正規化RUN: MHLW CSVガイドライン v2

- run_id: `20260531-121456224_run-normalized-mhlw-csv-guideline-v2`
- branch: `run/normalized-mhlw-csv-guideline-v2`
- doc_id: `jp_mhlw_csv_guideline_20101021`
- 対象: 医薬品・医薬部外品製造販売業者等におけるコンピュータ化システム適正管理ガイドライン
- source_url: `https://www.mhlw.go.jp/web/t_doc?dataId=00tb6573`
- source_format: `html`
- retrieved_at: `2026-05-23`
- base_commit: `a4f72663ef186fa48c7a82829a5e4a34a4bb8b06`

## 目的

MHLW CSVガイドラインを `runs/<run_id>/promotion_candidate/` に正規化候補として作成する。
別紙2のカテゴリ分類表は、HTML page2 の表をセル配列と semantic record の両方で保持する。

## 実行環境

- Python: `3.11.6`
- lxml: `6.0.2`
- PyYAML: `6.0.3`
- typer: `0.24.0`
- parser_profile.id: `jp_mhlw_csv_guideline_v1`
- candidate_visibility_profile.id: `jp_mhlw_csv_guideline_visibility_v1`

## 生成コマンド

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.cli extract-mhlw-html --input data/human-readable/mhlw/csv_guideline/00tb6573.html --output runs/20260531-121456224_run-normalized-mhlw-csv-guideline-v2/00tb6573.extracted.txt
.\.venv\Scripts\python.exe -m qai_text2ir.cli bundle --input runs/20260531-121456224_run-normalized-mhlw-csv-guideline-v2/00tb6573.extracted.txt --out-dir runs/20260531-121456224_run-normalized-mhlw-csv-guideline-v2/promotion_candidate --doc-id jp_mhlw_csv_guideline_20101021 --title '医薬品・医薬部外品製造販売業者等におけるコンピュータ化システム適正管理ガイドライン' --short-title 'CSVガイドライン' --doc-type guideline --source-url https://www.mhlw.go.jp/web/t_doc?dataId=00tb6573 --source-format html --retrieved-at 2026-05-23 --jurisdiction JP --language ja --family JP_GUIDELINE --parser-profile-id jp_mhlw_csv_guideline_v1 --candidate-visibility-profile-id jp_mhlw_csv_guideline_visibility_v1 --strict --write-manifest --overwrite-manifest
```

## 生成物

- `promotion_candidate/jp_mhlw_csv_guideline_20101021.regdoc_ir.yaml`
- `promotion_candidate/jp_mhlw_csv_guideline_20101021.parser_profile.yaml`
- `promotion_candidate/jp_mhlw_csv_guideline_20101021.regdoc_profile.yaml`
- `promotion_candidate/jp_mhlw_csv_guideline_20101021.meta.yaml`
- `promotion_candidate/manifest.yaml`
- `GOAL_CHECK.md`
- `SPECIAL_STRUCTURE_AUDIT.md`
- `HEADING_REVIEW.md`
- `TABLE_NOTE_REVIEW.md`
- `TEXT_CLEANLINESS_REVIEW.md`
- `DOUBLE_CHECK.md`
- `SAMPLE_EXTRACT.md`

## 検証結果

```text
focused tests: 17 passed
goal_check: PASS
special_structure_audit: pass
check_ir_structure: [OK] no structure problems found (scanned: 5 yaml files)
```

## 目検チェック

- heading: `1.1 目的`、`1.3 カテゴリ分類`、`4.1 開発計画に関する文書の作成` などの小見出しを `heading` に分離し、本文先頭に残らないことを確認。
- 表: 別紙2配下に `カテゴリ分類表`、`本ガイドラインの対象外` の順で配置されることを確認。
- 結合セル: カテゴリ3の2 display rows が同一 semantic record `csv_annex2.category3` に対応し、`raw_row_nums: [4, 5]` で保持されることを確認。
- note / 表外: 別紙1は画像参照、別紙2は page2 HTML 表として扱い、表外テキストが表先頭に混入しないことを確認。
- 不要改行・スペース: paragraph の見出し混入は0件。表行 `text` の空セル区切りは結合セル由来の表示用表現として維持。

## 深い階層サンプル

`SAMPLE_EXTRACT.md` に `annex2.tbl1.tblh.tblr5` の祖先経路を抽出した。

経路:

```text
root
  annex2
    annex2.tbl1
      annex2.tbl1.tblh
        annex2.tbl1.tblh.tblr5
```

## 昇格方針

このPRでは `data/normalized/` へは複写しない。
PR承認後、別ブランチで `promotion_candidate/` から `data/normalized/jp_mhlw_csv_guideline_20101021/` への昇格専用PRを作成する。
