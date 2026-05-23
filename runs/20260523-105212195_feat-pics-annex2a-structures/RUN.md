# RUN: PICS Annex 2A Table and Flow Figures

- run_id: `20260523-105212195_feat-pics-annex2a-structures`
- branch: `feat/pics-annex2a-structures`
- prompt: `out/administrators-memos/20260523.........問題発展型特殊パーサー/104.PICS_Annex2A_Talbes_Figures/codex_pics_annex2a_table_figures_prompt.md`
- target: `data/human-readable/pics/pe009-17_annex2a_2023-08-25_en.txt`

## 実施内容

- PIC/S Annex 2A の Table 1 を `table` / `table_header` / `table_row` / `note` として構造化した。
- PDF shading はテキスト層から信頼復元できないため、`shading_reconstructed: false` と `shading_note` をtable dataへ記録した。
- Figure 1/2 の横並びテキスト層ブロックを2つの `figure` ノードへ分離した。
- Figure 3 を `figure` ノードとして構造化した。
- Annex 2A単独プロファイルと複合Annexの subtree refine 双方で同正規化が動くようにした。
- figureは `role: informative` とし、通常のDQ/GMPチェックリスト候補ではなく検索・レビュー用の情報として保持した。

## 生成・監査結果

- Annex 2A 再生成先: `out/20260523-105212195_feat-pics-annex2a-structures/after_annex2a_v2`
- 複合Annex再生成先: `out/20260523-105212195_feat-pics-annex2a-structures/after_annexes_v2`
- Annex 2A special structure audit: pass
  - source_tables: 1
  - source_figures: 2
  - generated_tables: 1
  - generated_rows: 6
  - generated_figures: 3
  - unresolved_special_blocks: 0
- Annex 2A GOAL check: pass
  - table: 1
  - table_header: 1
  - table_row: 6
  - figure: 3
  - warnings: none
- 複合Annex GOAL check: pass
- 複合Annex special structure audit: warn
  - Annex 1およびAnnex 2Aの対象構造は構造化済み
  - 残る unresolved は Annex 2B/3/7/14/19 で、今回対象外

## 成果物

- `PICS_ANNEX2A_TABLE_FIGURE_REPORT.md`
- `PICS_ANNEX2A_TABLE_FIGURE_REPORT.json`
- `SPECIAL_STRUCTURE_AUDIT.md`
- `SPECIAL_STRUCTURE_AUDIT.json`
- `GOAL_CHECK_RESULT.md`
- `COMBINED_ANNEXES_SPECIAL_STRUCTURE_AUDIT.md`
- `COMBINED_ANNEXES_SPECIAL_STRUCTURE_AUDIT.json`
- `COMBINED_ANNEXES_GOAL_CHECK_RESULT.md`

## テスト

- `python -m pytest tests/test_pics_annex2a_structures.py tests/test_pics_annex2a_preformatted.py tests/test_pics_annex2a_profile.py -q`
  - 6 passed
- `python -m pytest -q`
  - 187 passed, 1 skipped
