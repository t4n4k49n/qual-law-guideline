# RUN: 20260218-041935361_feat-pics-annex11-v1-strict

- run_id: `20260218-041935361_feat-pics-annex11-v1-strict`
- branch: `feat/pics-annex11-v1-strict`

## 目的
- PIC/S PE 009-17 (Annexes) の Annex 11（Computerised systems）を単体文書として正規化する。
- strict qualitycheck で構造崩れなく 4 YAML を生成する。

## 一次ソース
- `https://picscheme.org/docview/8881`
- retrieved_at: `2026-02-18`

## 入力作成手順
- Annexes全文TXT:
  - `pdftotext -layout -nopgbrk pe009-17_annexes_2023-08-25_en.pdf data/human-readable/pics/pe009-17_annexes_2023-08-25_en.txt`
- Annex 11抽出:
  - `python scripts/slice_pics_annex.py --input data/human-readable/pics/pe009-17_annexes_2023-08-25_en.txt --output data/human-readable/pics/pe009-17_annex11_2023-08-25_en.txt --annex-no 11`
- 生成後に UTF-8/LF 正規化を実施。

## 実装
- `scripts/slice_pics_annex.py` を追加
  - `ANNEX 11` 行から `ANNEX 12` 直前までを抽出
  - 前後空行トリム、UTF-8/LF 出力
- `src/qai_text2ir/profiles/pics_annex11_default_v1.yaml` を追加
  - context root: `annex`
  - footer/header ノイズ除去
  - 行末連結ヘッダ (`...Annex 11 Computerised systems`) 除去
  - annex heading 継続結合
  - section/paragraph/item/subitem の抽出
- `tests/test_pics_annex11_profile.py` を追加
  - footer drop / inline header strip / annex heading merge / 4.→4.1→a./b. 階層を確認

## 実行
- `python -m pytest -q`
- `python -m qai_text2ir.cli --input data/human-readable/pics/pe009-17_annex11_2023-08-25_en.txt --out-dir out/20260218-041935361_feat-pics-annex11-v1-strict --doc-id pics_pe00917_annex11_20230825 --title "PIC/S GMP Guide (PE 009-17) Annex 11 Computerised systems (25 August 2023)" --short-title "PIC/S PE009-17 Annex 11" --jurisdiction INTL --language en --doc-type guideline --source-url "https://picscheme.org/docview/8881" --source-format pdf --retrieved-at "2026-02-18" --pics-doc-id "PE 009-17 (Annexes)" --parser-profile src/qai_text2ir/profiles/pics_annex11_default_v1.yaml --qualitycheck --strict --emit-only all`

## 結果
- tests: `56 passed, 1 skipped`
- strict: 成功（warning 0）
- root 配下に annex(11) が 1件
- annex heading: `COMPUTERISED SYSTEMS`
- section 1..17 を生成
- section 4 配下に paragraph 4.1..4.8 を生成
- a./b./c. 系 item を生成
- `PE 009-17 (Annexes) -...- 25 August 2023` の本文混入なし
- `Annex 11 Computerised systems` ランニングヘッダ混入なし

## 既知の残課題
- Annexes 全体（Annex 1〜22）の一括正規化は次PRで対応。
- Annex 11 の section 見出しは現仕様上 `section.text` 側に保持される箇所がある（構造整合は維持）。

## まとめ
Annex 11 を単体で strict 通過できる状態にしたことで、Part I/Part II に続く PDF 由来パイプラインの横展開が実証できた。再現可能な抽出スクリプトと専用プロファイルを揃えたため、今後は Annexes 全体への拡張を低リスクに進められる。

## 生成物
- `out/20260218-041935361_feat-pics-annex11-v1-strict/pics_pe00917_annex11_20230825.regdoc_ir.yaml`
- `out/20260218-041935361_feat-pics-annex11-v1-strict/pics_pe00917_annex11_20230825.parser_profile.yaml`
- `out/20260218-041935361_feat-pics-annex11-v1-strict/pics_pe00917_annex11_20230825.regdoc_profile.yaml`
- `out/20260218-041935361_feat-pics-annex11-v1-strict/pics_pe00917_annex11_20230825.meta.yaml`
- `out/20260218-041935361_feat-pics-annex11-v1-strict/manifest.yaml`
