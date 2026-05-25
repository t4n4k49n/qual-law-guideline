<!-- PR_BODY_FILE: runs/20260525-195555541_feat-mhlw-csv-annex-adapter-v1/PR.md -->

## まとめ

CSVガイドラインの別紙1/2を本文末尾に混入させたままにせず、個別adapterで別紙プレースホルダとして保持できるようにしました。別紙1は画像参照、別紙2は表題のみという現状をinventoryで追跡できるため、次の列復元・OCR・ソース補完フェーズへ進むための判断材料が明確になります。

## 変更内容

- `mhlw_csv_annex_adapter` を追加し、CSVガイドライン専用profileで明示的に有効化
- `別紙1` / `別紙2` をroot直下の `annex` ノードへ分離
- HTML inventoryで、`別紙1` の画像hrefと `別紙2` の表行有無を記録
- RUNに、今回扱わない課題として画像OCR、別紙2表本体復元、列復元を明記
- 残した次フェーズの個別adapter開発計画を `docs/INDIVIDUAL_ADAPTER_NEXT_PHASE_PLAN.md` に整理

## 検証

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_mhlw_csv_annexes.py tests\test_text2ir_csv_guideline.py tests\test_candidate_visibility_profiles_6_9.py -q
```

結果: `12 passed`

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.goal_check --bundle-dir out\20260525-195555541_feat-mhlw-csv-annex-adapter-v1 --doc-id jp_mhlw_csv_guideline_annex_adapter_v1 --mode normal --out runs\20260525-195555541_feat-mhlw-csv-annex-adapter-v1\goal_check.md
```

結果: `PASS`

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.special_structure_audit --bundle-dir out\20260525-195555541_feat-mhlw-csv-annex-adapter-v1 --doc-id jp_mhlw_csv_guideline_annex_adapter_v1 --mode normal --out runs\20260525-195555541_feat-mhlw-csv-annex-adapter-v1\special_structure_audit.md
```

結果: `pass`

## 補足

- このPRは開発PRであり、正式な正規化RUNではありません。
- `data/normalized/` への昇格は行っていません。
- 別紙内容の完全正規化、OCR、列復元は次フェーズ扱いです。
