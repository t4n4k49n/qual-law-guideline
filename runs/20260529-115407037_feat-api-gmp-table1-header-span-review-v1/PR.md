# 原薬GMPガイドライン 表1ヘッダ結合セル修正

## まとめ

原薬GMPガイドライン表1の結合ヘッダを、英語版相当の表と同じSTEP列として読める形に修正しました。これにより、表の横方向に進むほどGMP要求事項が増大する構造を、崩れた見出しではなく一貫した列ラベルとして扱えます。

## 背景

正規化候補PR `#216` は、表1のデータ行は復元できていましたが、ヘッダの結合セル表現が不十分でした。

特に、`形態ごとの生産工程の事例` が5つの工程列にまたがる親見出しである点を、英語版PIC/S Part II Table 1と同様に `STEP 1` から `STEP 5` として展開する必要がありました。

## 変更内容

- 表1の工程列IDを `process_example_step_1` から `process_example_step_5` に変更。
- 表示用列ラベルを `形態ごとの生産工程の事例 STEP 1` から `STEP 5` に変更。
- PDF上の下段見出しは `stage_labels` として保持。
- `header_structure.spanning_headers` に結合ヘッダの情報を保持。
- ヘッダ・行データ・テーブル全体で、結合ヘッダと下段見出しの両方を検証するテストを追加。

## 確認

- GOAL check: pass
- Special structure audit: pass
- Generated table rows: `7`
- Header label: `形態ごとの生産工程の事例 STEP 1..5`
- Focused tests: `10 passed`
- Full tests: `253 passed, 1 skipped`

## 注意

このPRは正規化RUNではありません。表1のヘッダ結合セルに対する目検レビュー修正です。

このPR承認・マージ後に、改めて正規化RUNをfreshに作成します。

<!-- PR_BODY_FILE: runs/20260529-115407037_feat-api-gmp-table1-header-span-review-v1/PR.md -->
