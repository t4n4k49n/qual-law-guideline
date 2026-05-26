<!-- PR_BODY_FILE: runs/20260527-015708217_docs-plan-normalization-10-12-13/PR.md -->

## まとめ

10 EU GMP、12 PIC/S、13 WHO LBM 3rdについて、正規化へ進めるための共通課題と文書別課題を整理しました。既存のtext2ir系RUNで得たGOALチェック、監査レポート、複合入口設計の知見を再利用し、CFRとは異なりTXTベースで進める前提の実行順を明確にしています。

## 変更内容

- `docs/NORMALIZATION_PLAN_10_12_13.md` を追加
- 10/12/13で共通化できる処理と文書別に分けるべき処理を整理
- 過去RUN/KNOWLEDGEから再利用する知見を明記
- EU GMP、PIC/S、WHO LBM 3rdの推奨順と次アクションを定義
- RUN記録を追加

## 検証

ドキュメントのみの変更。コード・テストは変更していません。

## 次アクション

現行mainで10/12/13の既存GOAL pass文書を再生成し、readiness表を作ったうえで、単体文書からpromotion candidate化へ進みます。
