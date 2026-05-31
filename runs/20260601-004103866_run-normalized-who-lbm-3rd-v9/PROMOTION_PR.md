# WHO LBM 3rd正式版昇格

## まとめ

承認済みのWHO LBM 3rd正規化候補 v9 を正式版領域へ昇格します。レビュー済み候補をそのまま `data/normalized/` に反映するだけの子PRで、パーサ修正や再生成は含めていません。

## 対象

- 親PR: `#243`
- doc_id: `who_lbm_3rd_2004_9241546506`
- 原文URL: `https://www.who.int/publications/i/item/9241546506`
- 昇格元: `runs/20260601-004103866_run-normalized-who-lbm-3rd-v9/promotion_candidate/`
- 昇格先: `data/normalized/who_lbm_3rd_2004_9241546506/`

## 変更内容

- `promotion_candidate` から正式版領域へ4ファイルを複写
  - `who_lbm_3rd_2004_9241546506.regdoc_ir.yaml`
  - `who_lbm_3rd_2004_9241546506.parser_profile.yaml`
  - `who_lbm_3rd_2004_9241546506.regdoc_profile.yaml`
  - `who_lbm_3rd_2004_9241546506.meta.yaml`
- `RUN.md` に昇格記録を追記

## 検証

- 親PR #243 で確認済み
  - WHO LBM関連テスト: `32 passed`
  - `goal_check --mode promotion`: `PASS`
  - `special_structure_audit --mode promotion`: `pass`
  - `tools/check_ir_structure.py`: `[OK] no structure problems found`
  - 表・本文順序、表再結合、heading、不要改行・空白を確認済み

<!-- PR_BODY_FILE: runs/20260601-004103866_run-normalized-who-lbm-3rd-v9/PROMOTION_PR.md -->
