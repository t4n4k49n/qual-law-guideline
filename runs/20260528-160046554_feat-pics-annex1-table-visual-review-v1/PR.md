<!-- PR_BODY_FILE: runs/20260528-160046554_feat-pics-annex1-table-visual-review-v1/PR.md -->

## まとめ

PIC/S Annex 1の正規化前に、全表をPDFページ画像で目検確認し、結合セル・折返しセルの復元根拠をIRとRUN成果物に残しました。Table 4では、テキスト抽出だけでは縦結合セルの中央配置により一部操作が前グレードへ誤帰属していたため、視覚上のrow spanに基づいて修正しています。

## 変更内容

- Table 1/5: 二段ヘッダとGrade Dの折返しセルをレビュー済みメタデータとして追加
- Table 2/6: Grade Aの横結合No growthセルを各測定法列へ展開し、展開元をメタデータ化
- Table 3/4: Grade列の縦結合セルを各操作レコードへ展開し、Table 4のGrade B/D帰属を修正
- 目検根拠としてRUN配下にPDFレンダリング画像、JSON、Markdownを追加
- Annex 1表テストで結合セル復元とTable 4の正しいグレード配列を固定

## 確認

- `python -m pytest tests\test_pics_annex1_tables.py -q`
- `python -m pytest -q`
