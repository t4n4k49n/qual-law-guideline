# RUN: 20260217-051524489_feat-who-lbm-3rd-text2ir-v1

- run_id: `20260217-051524489_feat-who-lbm-3rd-text2ir-v1`
- branch: `feat/who-lbm-3rd-text2ir-v1`

## 目的
- `WHO_LBM_3rd.txt` を text2ir で構造化し、WHO向け profile で PDF由来ノイズ除去と chapter/list 分割を安定化する。

## 入力
- 指示元TXT: `%USERPROFILE%\Documents\GitHub\qual-law-guideline_OLD-HANDMADE\data\human-readable\13.WHO LBM 3rd\WHO_LBM_3rd.txt`（0 byte）
- 実使用元PDF: `%USERPROFILE%\Documents\GitHub\qual-law-guideline_OLD-HANDMADE\data\human-readable\13.WHO LBM 3rd\9241546506_eng.pdf`
- 生成入力: `data/human-readable/who/WHO_LBM_3rd.txt`（`pdftotext -layout -enc UTF-8` で抽出後、UTF-8/LFに正規化）

## 実装
- `src/qai_text2ir/profiles/who_lbm_3rd_default_v1.yaml` を追加。
  - `preprocess.drop_line_regexes` で `• 1 •` 形式と `\f` を除去。
  - `preprocess.strip_inline_regexes` で `LABORATORY BIOSAFETY MANUAL` と行内ページ欄外トークンを除去。
  - `chapter/item/subitem` 用 marker と structure を定義。
- `src/qai_text2ir/text_parser.py`
  - `preprocess.strip_inline_regexes` を実装（行内ノイズ除去後に空行化した行は段落区切りにせずスキップ）。
  - 後処理で段落境界を跨ぐ hyphen-wrap も修復。
  - `laboratory-acquired` を hyphen保持語に追加。
- `src/qai_text2ir/profile_loader.py`
  - `family="WHO_LBM"` の既定 profile を `who_lbm_3rd_default_v1.yaml` に追加。
- `tests/test_text2ir_who_lbm_3rd.py` を追加。
  - 行内ページトークン/ランニングヘッダ除去 + chapter/item分割。
  - prose単一改行warning 0 と hyphen-space warning 0 を検証。

## 実行
- `python -m pytest -q tests/test_text2ir_who_lbm_3rd.py tests/test_text2ir_eu_gmp_chap1.py tests/test_text2ir_bundle.py tests/test_text2ir_normalization.py tests/test_text2ir_cfr_quality_v2.py tests/test_text2ir_profiles_pics.py`
- `python -m qai_text2ir.cli --input data/human-readable/who/WHO_LBM_3rd.txt --out-dir out/20260217-051524489_feat-who-lbm-3rd-text2ir-v1 --doc-id who_lbm_3rd_2004_9241546506 --title "WHO Laboratory biosafety manual, 3rd edition (2004)" --short-title "WHO LBM 3rd" --jurisdiction WHO --language en --doc-type guideline --source-url "https://www.who.int/publications/i/item/9241546506" --source-format pdf --retrieved-at "2026-02-17" --who-publication-id "9241546506" --parser-profile src/qai_text2ir/profiles/who_lbm_3rd_default_v1.yaml --qualitycheck --strict --emit-only all`

## 確認結果
- strict: 成功（warning 0）。
- `regdoc_ir` で `LABORATORY BIOSAFETY MANUAL`（大文字ヘッダ）と `• <page> •` トークンは不在。
- chapter / item / subitem が生成されることを確認。
- 出力本文で `single newline remains in prose` は 0。

## 生成物
- `out/20260217-051524489_feat-who-lbm-3rd-text2ir-v1/who_lbm_3rd_2004_9241546506.regdoc_ir.yaml`
- `out/20260217-051524489_feat-who-lbm-3rd-text2ir-v1/who_lbm_3rd_2004_9241546506.parser_profile.yaml`
- `out/20260217-051524489_feat-who-lbm-3rd-text2ir-v1/who_lbm_3rd_2004_9241546506.regdoc_profile.yaml`
- `out/20260217-051524489_feat-who-lbm-3rd-text2ir-v1/who_lbm_3rd_2004_9241546506.meta.yaml`
- `out/20260217-051524489_feat-who-lbm-3rd-text2ir-v1/manifest.yaml`
- `runs/20260217-051524489_feat-who-lbm-3rd-text2ir-v1/RUN.md`

