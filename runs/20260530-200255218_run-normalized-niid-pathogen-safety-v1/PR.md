# NIID病原体等安全管理規程 正規化RUN v1

## まとめ

NIID病原体等安全管理規程を、本文6章と別表・付表16件を含む単一の正式候補として正規化しました。別表・付表のうち5表は過去の視覚レビュー結果を反映した `table_row` として保持し、候補表示では対象外OK範囲を制御しつつ、原文全体を参照できる状態にしています。

## 変更内容

- `runs/20260530-200255218_run-normalized-niid-pathogen-safety-v1/promotion_candidate/` に4ファイルbundleとmanifestを追加。
- 本文用/別表用に分かれていたNIID profileを、正式候補用のfull profileとして統合。
- 表化済みのNIID付表・別表で、元の行番号itemが本文に残らないようtable adapterを修正。
- 日本語表示本文の不要スペース、ページ番号行、不要改行を正規化。
- `付表2` / `付表4` の折返し見出しを補完。

## 確認結果

- goal check: PASS
- special structure audit: PASS
- IR structure check: PASS
- focused tests: `11 passed`
- root chapter: 6
- root annex: 16
- table: 5
- table_row: 54
- display prose scan: 不要スペース/不要改行/ページ番号行 0件

## 目検レビュー

- 章: `第1章` から `第6章` まで重複なし。
- 別表/付表: `別表1` から `別表10`、`付表1-1` から `付表4` を保持。
- 表: `付表2`, `付表3`, `付表4`, `別表7`, `別表10` は視覚レビュー済みrecordを `table_row` 化。
- 見出し: `付表2` と `付表4` のPDF上の折返し見出しをfull headingとして保持。
- 固定幅raw textは、表示本文ではなく監査用metadataに保持。

## レビュー用ファイル

- `runs/20260530-200255218_run-normalized-niid-pathogen-safety-v1/GOAL_CHECK.md`
- `runs/20260530-200255218_run-normalized-niid-pathogen-safety-v1/SPECIAL_STRUCTURE_AUDIT.md`
- `runs/20260530-200255218_run-normalized-niid-pathogen-safety-v1/STRUCTURE_TABLE_REVIEW.md`
- `runs/20260530-200255218_run-normalized-niid-pathogen-safety-v1/SAMPLE_EXTRACT.md`

## 昇格境界

この親PRでは `data/normalized/` は変更しません。承認後、子PRで `promotion_candidate/` の4ファイルのみを `data/normalized/jp_niid_pathogen_safety_management_20240401/` に複写します。

<!-- PR_BODY_FILE: runs/20260530-200255218_run-normalized-niid-pathogen-safety-v1/PR.md -->
