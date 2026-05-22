# text2ir candidate contamination audit

<!-- PR_BODY_FILE: runs/20260522-170359710_text2ir-candidate-contamination-audit/PR.md -->

## まとめ

WHO LBM 3rd で見つかった `.............   ` のような入力由来の表示・帳票断片が、text2ir の selectable candidate に混入していないかを、最新の代表候補一式に横断して確認しました。これは正式昇格前の人手レビューで見落としやすい汚染パターンを、文書単位ではなく共通リスクとして扱うための監査です。

## 変更内容

- `runs/20260522-170359710_text2ir-candidate-contamination-audit/` に監査RUNを追加
- WHO LBM 3rd の既知問題を含め、最新 text2ir 候補・review UI コピー・promotion candidate を横断スキャン
- 検出結果を Markdown / JSON / TSV に保存
- 個別profile修正を主軸にしないため、根本原因と対応ポリシーを `ROOT_CAUSE_AND_POLICY.md` に明記
- コード、profile、テスト、`data/normalized/` は変更なし

## 監査結果

- スキャン対象: 19文書バンドル
- findings: 72件（review UI コピー等の重複を含む）
- unique finding keys: 36件
- severe findings: 18件

主な結論:

- EU GMP Chapter 1 / PIC/S Annex 11 / PIC/S Annex 15 は、今回のルールでは severe な selectable candidate 汚染なし
- WHO LBM 3rd は Table 5-7 survey form のドットリーダー・チェック欄が selectable item/subitem に混入
- PIC/S Annex 2A は private-use bullet と固定幅の表状テキストが selectable subitem に混入
- PIC/S Annex 1 / Annexes refined には表キャプション・表テキスト吸収の軽微な確認対象あり

## 確認

- `runs/20260522-170359710_text2ir-candidate-contamination-audit/TEXT2IR_CANDIDATE_CONTAMINATION_AUDIT.md`
- `runs/20260522-170359710_text2ir-candidate-contamination-audit/ROOT_CAUSE_AND_POLICY.md`
- `runs/20260522-170359710_text2ir-candidate-contamination-audit/candidate_contamination_findings.tsv`
- `runs/20260522-170359710_text2ir-candidate-contamination-audit/candidate_contamination_audit.json`

## 補足

今回の監査はコード修正ではなく、正式昇格前に潰すべき候補汚染の棚卸しです。対応方針の主軸は、WHO LBM 3rd や PIC/S Annex 2A の個別profile修正ではなく、text2ir共通側で「selectable candidate に出してはいけない表・フォーム・固定幅崩れ」を検出し、通常 `item` / `subitem` 化を抑止し、promotion gate で止めることです。WHO LBM 3rd と PIC/S Annex 2A は個別パッチ対象ではなく、この共通対策の代表症例・回帰対象として扱います。
