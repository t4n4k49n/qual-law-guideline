<!-- PR_BODY_FILE: runs/20260523-105212195_feat-pics-annex2a-structures/PR.md -->

## まとめ

PIC/S Annex 2A の Table 1 と Flow Figure 1-3 を構造化し、ATMP製造ステップの表・フローを本文混入ではなくレビュー可能な専用ノードとして扱えるようにしました。表行はチェックリスト選択肢として使える粒度にし、図はinformativeな参照情報として保持することで、通常の規制本文候補との混同を避けています。

## 変更内容

- Annex 2A専用の `pics_annex2a_structures` 正規化を追加
- `pics_annex2a_default_v1` でのみ有効化
- 複合Annexの subtree refine でも Annex 2A 子プロファイルの正規化を適用
- Table 1を6行の `table_row` と3つの脚注 `note` に構造化
- PDF shadingは復元せず、復元不可であることをtable dataへ明示
- Figure 1/2/3を `figure` ノードとして構造化
- 専用テストとRUN成果物を追加

## 確認結果

- Annex 2A special structure audit: pass
  - source_tables: 1
  - source_figures: 2
  - generated_tables: 1
  - generated_rows: 6
  - generated_figures: 3
  - unresolved_special_blocks: 0
- Annex 2A GOAL check: pass
- 複合Annex GOAL check: pass
- 複合Annex special structure audit: warn
  - Annex 1およびAnnex 2Aの対象構造は構造化済み
  - 残る unresolved は Annex 2B/3/7/14/19 で、今回対象外

## テスト

- `python -m pytest tests/test_pics_annex2a_structures.py tests/test_pics_annex2a_preformatted.py tests/test_pics_annex2a_profile.py -q`
  - 6 passed
- `python -m pytest -q`
  - 187 passed, 1 skipped

## 関連成果物

- `runs/20260523-105212195_feat-pics-annex2a-structures/RUN.md`
- `runs/20260523-105212195_feat-pics-annex2a-structures/PICS_ANNEX2A_TABLE_FIGURE_REPORT.md`
- `runs/20260523-105212195_feat-pics-annex2a-structures/SPECIAL_STRUCTURE_AUDIT.md`
- `runs/20260523-105212195_feat-pics-annex2a-structures/COMBINED_ANNEXES_SPECIAL_STRUCTURE_AUDIT.md`
