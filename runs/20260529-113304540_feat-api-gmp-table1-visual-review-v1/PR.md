# 原薬GMPガイドライン 表1 視覚レビュー修正

## まとめ

原薬GMPガイドラインの表1を、PDF上の表として読める単位に復元しました。これにより、表1をチェックシート候補として扱う際に、崩れたraw行ではなく、生産形態ごとの工程セルと「本ガイドラインを適用する工程」を確認できます。

## 背景

正規化候補PR `#214` は、表1がraw text由来の26行table_rowになっており、PDFの表セル構造を表現できていなかったため取り下げました。

## 変更内容

- 表1を7件のvisual-reviewed `table_row` に変更。
- 各行に6セルの `cells` を保持。
- 灰色セルを `guideline_applicable` で保持。
- 下部矢印 `ＧＭＰ要求事項の増大` は行ではなく `visual_notes` に保持。
- 元TXTの崩れた行は `raw_lines` / `raw_row_nums` として追跡用に残す。
- 関連テストを更新。

## 確認

- GOAL check: pass
- Special structure audit: pass
- Generated table rows: `7`
- Focused tests: `5 passed`
- Full tests: `253 passed, 1 skipped`

## 注意

このPRは正規化RUNではありません。表1の目検レビュー修正です。

このPR承認・マージ後に、改めて正規化RUNをfreshに作成します。

<!-- PR_BODY_FILE: runs/20260529-113304540_feat-api-gmp-table1-visual-review-v1/PR.md -->
