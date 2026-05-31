# MHLW CSVガイドライン 正規化RUN v3

## まとめ

MHLW CSVガイドラインを、本文階層と別紙2のカテゴリ分類表を含めてレビューできる正規化候補として整備した。前段の修正で確認した `④ 基本的な考え方` 配下の中黒項目も含め、本文構造と表構造を同じIRで追える状態にした。

## 対象

- 文書: 医薬品・医薬部外品製造販売業者等におけるコンピュータ化システム適正管理ガイドライン
- doc_id: `jp_mhlw_csv_guideline_20101021`
- source_url: `https://www.mhlw.go.jp/web/t_doc?dataId=00tb6573`
- source_format: `html`
- 正本候補: `runs/20260531-125138676_run-normalized-mhlw-csv-guideline-v3/promotion_candidate/`

## 変更内容

- CSVガイドライン用の正規化候補4ファイルと manifest を追加。
- heading、本文階層、表/note、不要改行・スペースの目検レビュー資料を追加。
- IR再走査によるダブルチェック記録を追加。

## 検証結果

- `pytest tests/test_text2ir_csv_guideline.py tests/test_mhlw_csv_annex2_tables.py tests/test_mhlw_csv_annexes.py tests/test_mhlw_csv_annex_source_recovery.py tests/test_candidate_visibility_profiles_6_9.py -q`: `17 passed`
- `goal_check`: `PASS`
- `special_structure_audit`: `pass`
- `tools/check_ir_structure.py`: `[OK] no structure problems found`

## 目検ポイント

- heading: 章 `1`-`10`、別紙 `別紙1` -> `別紙2` の順序を確認。
- heading/text分離: `1.1 目的`、`1.3 カテゴリ分類` は `heading` に分離され、本文先頭に残っていない。
- 本文階層: `cha3.i1.si4` の配下に5つの中黒項目が `point` として入る。
- 表: 別紙2に `カテゴリ分類表`、`本ガイドラインの対象外` の2表を配置。
- 結合セル: カテゴリ3は `annex2.tbl1.tblh.tblr4` と `annex2.tbl1.tblh.tblr5` を `csv_annex2.category3` に対応付け。
- note / 表外: 別紙1は画像参照、別紙2は page2 HTML 表として扱い、表外テキストの表先頭混入なし。
- 不要改行・スペース: paragraph の見出し混入は0件。表行 `text` の空セル区切りは結合セル由来の表示用表現として維持。

## 深い階層サンプル

`runs/20260531-125138676_run-normalized-mhlw-csv-guideline-v3/SAMPLE_EXTRACT.md`:

```text
root
  cha3
    cha3.i1
      cha3.i1.si4
        cha3.i1.si4.poi1
```

対象は `ソフトウェアのカテゴリ分類` で、原文上の `④ 基本的な考え方` 配下にある。

## 注意

このPRでは `data/normalized/` へは反映しない。承認後に昇格専用PRで `promotion_candidate/` から `data/normalized/jp_mhlw_csv_guideline_20101021/` へ複写する。

<!-- PR_BODY_FILE: runs/20260531-125138676_run-normalized-mhlw-csv-guideline-v3/PR.md -->
