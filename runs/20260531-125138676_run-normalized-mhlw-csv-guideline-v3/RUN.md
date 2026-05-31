# 正規化RUN: MHLW CSVガイドライン v3

- run_id: `20260531-125138676_run-normalized-mhlw-csv-guideline-v3`
- branch: `run/normalized-mhlw-csv-guideline-v3`
- doc_id: `jp_mhlw_csv_guideline_20101021`
- 対象: 医薬品・医薬部外品製造販売業者等におけるコンピュータ化システム適正管理ガイドライン
- source_url_page1: `https://www.mhlw.go.jp/web/t_doc?dataId=00tb6573&dataType=1&pageNo=1`
- source_url_page2: `https://www.mhlw.go.jp/web/t_doc?dataId=00tb6573&dataType=1&pageNo=2`
- source_format: `html`
- retrieved_at: `2026-05-23`
- base_commit: `92c85ef4c457a4cb3ffb5e4404b82e10908e74fe`

## 目的

MHLW CSVガイドラインを `runs/<run_id>/promotion_candidate/` に正規化候補として作成する。
PR #230 で修正した本文階層を前提に、本文、別紙、別紙2のカテゴリ分類表をレビュー可能な候補として固定する。

## 実行環境

- Python: `3.11.6`
- lxml: `6.0.2`
- PyYAML: `6.0.3`
- typer: `0.24.0`
- parser_profile.id: `jp_mhlw_csv_guideline_v1`
- candidate_visibility_profile.id: `jp_mhlw_csv_guideline_visibility_v1`

## 生成コマンド

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.cli extract-mhlw-html --input data/human-readable/mhlw/csv_guideline/00tb6573.html --output out/20260531-125138676_run-normalized-mhlw-csv-guideline-v3/00tb6573.extracted.txt
.\.venv\Scripts\python.exe -m qai_text2ir.cli bundle --input out/20260531-125138676_run-normalized-mhlw-csv-guideline-v3/00tb6573.extracted.txt --out-dir runs/20260531-125138676_run-normalized-mhlw-csv-guideline-v3/promotion_candidate --doc-id jp_mhlw_csv_guideline_20101021 --title '医薬品・医薬部外品製造販売業者等におけるコンピュータ化システム適正管理ガイドライン' --short-title 'CSVガイドライン' --doc-type guideline --source-url 'https://www.mhlw.go.jp/web/t_doc?dataId=00tb6573&dataType=1&pageNo=1' --source-format html --retrieved-at 2026-05-23 --jurisdiction JP --language ja --family JP_GUIDELINE --parser-profile-id jp_mhlw_csv_guideline_v1 --candidate-visibility-profile-id jp_mhlw_csv_guideline_visibility_v1 --strict --write-manifest --overwrite-manifest
```

## 生成物

- `promotion_candidate/jp_mhlw_csv_guideline_20101021.regdoc_ir.yaml`
- `promotion_candidate/jp_mhlw_csv_guideline_20101021.parser_profile.yaml`
- `promotion_candidate/jp_mhlw_csv_guideline_20101021.regdoc_profile.yaml`
- `promotion_candidate/jp_mhlw_csv_guideline_20101021.meta.yaml`
- `promotion_candidate/manifest.yaml`
- `GOAL_CHECK.md`
- `SPECIAL_STRUCTURE_AUDIT.md`
- `HEADING_HIERARCHY_REVIEW.md`
- `TABLE_NOTE_REVIEW.md`
- `TEXT_CLEANLINESS_REVIEW.md`
- `DOUBLE_CHECK.md`
- `SAMPLE_EXTRACT.md`
- `ANNEX2_TABLE_RECONSTRUCTION_FROM_IR.md`

## 検証結果

```text
focused tests: 17 passed
goal_check: PASS
special_structure_audit: pass
check_ir_structure: [OK] no structure problems found (scanned: 5 yaml files)
```

## 目検チェック

- heading: 章 `1`-`10`、別紙 `別紙1` -> `別紙2` の順序を確認。
- heading/text分離: `1.1 目的`、`1.3 カテゴリ分類` などの小見出しが本文先頭に残らないことを確認。
- 本文階層: `cha3.i1.si4` の配下に5つの中黒項目が `point` として入ることを確認。
- 表: 別紙2配下に `カテゴリ分類表`、`本ガイドラインの対象外` の順で配置されることを確認。
- 結合セル: カテゴリ3の2 display rows が同一 semantic record `csv_annex2.category3` に対応し、`raw_row_nums: [4, 5]` で保持されることを確認。
- 別紙2表復元: `ANNEX2_TABLE_RECONSTRUCTION_FROM_IR.md` で `annex2.tbl1.tblh.tblr1` を表示ヘッダ、`tblr2`-`tblr7` をデータ行として逆組み上げ。原表の20列・カテゴリ1-5の行対応を確認。
- note / 表外: 別紙1は画像参照、別紙2は page2 HTML 表として扱い、表外テキストが表先頭に混入しないことを確認。
- 不要改行・スペース: paragraph の見出し混入は0件。表行 `text` の空セル区切りは結合セル由来の表示用表現として維持。

## ダブルチェック

`DOUBLE_CHECK.md` に、IR再走査による2回目チェック結果を記録した。
全項目 `OK`。

## 深い階層サンプル

`SAMPLE_EXTRACT.md` に `cha3.i1.si4.poi1` の祖先経路と内容を抽出した。

| 階層 | nid | kind | 内容 |
|---:|---|---|---|
| 1 | `root` | `document` | 文書ルート |
| 2 | `cha3` | `chapter` | コンピュータ化システムの開発、検証及び運用管理に関する文書の作成 |
| 3 | `cha3.i1` | `item` | コンピュータ化システムの開発、検証及び運用管理に関する基本方針 |
| 4 | `cha3.i1.si4` | `subitem` | 基本的な考え方 |
| 5 | `cha3.i1.si4.poi1` | `point` | ソフトウェアのカテゴリ分類 |

読み下し:

```text
3. コンピュータ化システムの開発、検証及び運用管理に関する文書の作成
  (1) コンピュータ化システムの開発、検証及び運用管理に関する基本方針
    ④ 基本的な考え方
      ・ソフトウェアのカテゴリ分類
```

## 昇格方針

このPRでは `data/normalized/` へは複写しない。
PR承認後、別ブランチで `promotion_candidate/` から `data/normalized/jp_mhlw_csv_guideline_20101021/` への昇格専用PRを作成する。
