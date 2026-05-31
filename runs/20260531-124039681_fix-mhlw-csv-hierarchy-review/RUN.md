# RUN: MHLW CSVガイドライン階層修正

- run_id: `20260531-124039681_fix-mhlw-csv-hierarchy-review`
- branch: `fix/mhlw-csv-hierarchy-review`
- 種別: 通常の parser/profile/test 修正
- 注意: 正規化RUNではない。`promotion_candidate/` と `data/normalized/` は変更しない。

## 目的

MHLW CSVガイドラインの章3で、`④ 基本的な考え方` 配下の中黒項目が兄弟ノードになっていた問題を修正する。

## 原因

`jp_guideline_default_v1` では丸数字 `①` と中黒 `・` がどちらも `subitem` として扱われる。
一方で `subitem` 配下に `subitem` が許可されていないため、中黒項目が直前の丸数字ではなく上位 item 配下の兄弟として配置されていた。

## 修正内容

- CSV profile で中黒 `・` / `●` を `point` として扱う。
- CSV profile の structure で `subitem -> point` を許可する。
- CSV profile の `section_decimal` に `heading_from_remainder` を付与し、`1.1 目的` などの小見出しを本文ではなく `heading` に分離する。
- parser に `heading_from_remainder` を marker option として追加する。
- 実HTML由来のテストで、`cha3.i1.si4` 配下に5つの `point` が入ることを固定する。

## 目検チェック

詳細は `CSV_HIERARCHY_CHECK.md`。

確認済み:

- `ソフトウェアのカテゴリ分類` など5項目は `cha3.i1.si4` の children。
- `④ 基本的な考え方` と5つの中黒項目の位置関係は原文画像と一致。
- `1.1 目的` / `1.3 カテゴリ分類` は heading/text に分離。

## 検証

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_text2ir_csv_guideline.py tests/test_mhlw_csv_annex2_tables.py tests/test_mhlw_csv_annexes.py tests/test_mhlw_csv_annex_source_recovery.py tests/test_candidate_visibility_profiles_6_9.py -q
```

結果: `17 passed`
