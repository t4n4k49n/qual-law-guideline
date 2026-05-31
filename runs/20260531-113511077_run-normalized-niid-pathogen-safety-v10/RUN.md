# 正規化RUN: NIID病原体等安全管理規程 v10

## 概要

- run_id: `20260531-113511077_run-normalized-niid-pathogen-safety-v10`
- 対象: `jp_niid_pathogen_safety_management_20240401`
- 目的: v8で見落としていた別表5の表外運搬基準の位置関係を修正し、`promotion_candidate/` を作り直す。

## 主な修正

- 別表テーブル化後の annex 直下 child を source locator の行番号で並べ、原文上の順序を保持するようにした。
- 別表5は `ann5.tbl1` が先、表外の運搬基準 `ann5.not3` が後に来る。
- 表外運搬基準は引き続き table_row には含めず、note として保持する。
- PDF抽出由来の孤立した `•` は内容を持たないためnote化しない。
- 再発防止として、別表5の table/note 順序と孤立 `•` 除去をテストで固定した。

## 位置関係確認

`ann5` 直下の順序:

1. `ann5.tbl1` table line:1203
2. `ann5.not1` note line:1240
3. `ann5.not2` note line:1293
4. `ann5.not3` note line:1298

## 検証

- focused tests: `13 passed`
- full tests: `257 passed, 1 skipped`
- goal check: PASS
- special structure audit: PASS
- IR structure check: PASS
- absolute local path check: PASS

## 昇格

- この親PRでは `data/normalized/` は変更しない。
- PR承認後、子PRで `promotion_candidate/` から `data/normalized/` へ複写する。
