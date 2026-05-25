<!-- PR_BODY_FILE: runs/20260526-043157187_docs-mhlw-csv-annex1-ocr-plan/PR.md -->

## まとめ

CSVガイドライン別紙1の画像由来フローについて、OCRだけで正本化せず、まず公式画像をsourceとして保持し、IRではfigureとして扱う方針を明記しました。これにより、文字認識だけで図の矢印や順序を誤って固定せず、必要な場合は後段の視覚レビューまたは手入力転記RUNで意味分解できます。

## 変更内容

- `docs/MHLW_CSV_ANNEX1_OCR_PLAN.md` を追加
- 別紙1をOCRだけで正本化しない方針を明記
- 公式画像をlocal sourceとして保持し、IRではまず `figure` nodeにする方針を記録
- `docs/REMAINING_NORMALIZATION_PLAN_6_9.md` の残課題と次PR推奨を更新
- RUN記録を追加

## 検証

ドキュメントのみの変更。コード・テストは変更していません。

## 残る課題

- 次は `Q. 正規化RUN readiness判定` で、6/7/8/9を正式正規化RUNへ進める範囲と追加RUNへ送る範囲に分けます。
