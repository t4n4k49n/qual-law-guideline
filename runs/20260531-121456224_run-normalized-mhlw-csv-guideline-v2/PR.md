# MHLW CSVガイドライン 正規化RUN v2

## まとめ

MHLW CSVガイドラインを、チェックシート等で参照しやすい正規化候補として整備した。本文の階層、別紙、別紙2のカテゴリ分類表を同じIRで扱えるようにし、カテゴリ分類表は結合セルを含む表示行と semantic record の対応が追える状態にした。

## 対象

- 文書: 医薬品・医薬部外品製造販売業者等におけるコンピュータ化システム適正管理ガイドライン
- doc_id: `jp_mhlw_csv_guideline_20101021`
- source_url: `https://www.mhlw.go.jp/web/t_doc?dataId=00tb6573`
- source_format: `html`
- 正本候補: `runs/20260531-121456224_run-normalized-mhlw-csv-guideline-v2/promotion_candidate/`

## 変更内容

- CSVガイドライン用の正規化候補4ファイルと manifest を追加。
- `1.1 目的` などの section_decimal 残部を本文ではなく `heading` に入れる profile オプションを追加。
- 別紙2のHTML表を、表示行、セル配列、semantic record として保持。
- heading、表/note、不要改行・スペースの目検レビュー資料とダブルチェック記録を追加。

## 検証結果

- `pytest tests/test_text2ir_csv_guideline.py tests/test_mhlw_csv_annex2_tables.py tests/test_mhlw_csv_annexes.py tests/test_mhlw_csv_annex_source_recovery.py tests/test_candidate_visibility_profiles_6_9.py -q`: `17 passed`
- `goal_check`: `PASS`
- `special_structure_audit`: `pass`
- `tools/check_ir_structure.py`: `[OK] no structure problems found`

## 目検ポイント

- heading: 章 `1`-`10`、別紙 `別紙1`→`別紙2` の順序を確認。小見出しは `heading` に分離済み。
- 表: 別紙2に `カテゴリ分類表`、`本ガイドラインの対象外` の2表を配置。
- 結合セル: カテゴリ3は `annex2.tbl1.tblh.tblr4` と `annex2.tbl1.tblh.tblr5` を `csv_annex2.category3` に対応付け。
- note / 表外: 別紙1は画像参照、別紙2は page2 HTML 表として扱い、表外テキストの表先頭混入なし。
- 不要改行・スペース: paragraph の見出し混入は0件。表行 `text` の空セル区切りは結合セル由来の表示用表現として維持。

## 深い階層サンプル

`runs/20260531-121456224_run-normalized-mhlw-csv-guideline-v2/SAMPLE_EXTRACT.md`:

```text
root
  annex2
    annex2.tbl1
      annex2.tbl1.tblh
        annex2.tbl1.tblh.tblr5
```

対象行はカテゴリ3の2行目で、同じ semantic record `csv_annex2.category3` に対応する。

## 注意

このPRでは `data/normalized/` へは反映しない。承認後に昇格専用PRで `promotion_candidate/` から `data/normalized/jp_mhlw_csv_guideline_20101021/` へ複写する。

<!-- PR_BODY_FILE: runs/20260531-121456224_run-normalized-mhlw-csv-guideline-v2/PR.md -->
