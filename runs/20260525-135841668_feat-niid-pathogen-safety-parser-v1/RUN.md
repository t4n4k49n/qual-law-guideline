# RUN: 20260525-135841668_feat-niid-pathogen-safety-parser-v1

## 目的

8「病原体等安全管理規程」向けの `text2ir` parser profile を開発する。

このRUNはParser開発であり、正式な正規化RUNではない。`data/normalized/` への昇格や、正規化承認を前提にしない。

## 対象

- ソース: `data/human-readable/niid/pathogen_safety_management/source_texts/Kanrikitei3_20240401.txt`
- 公開元URL: `https://www.niid.go.jp/niid/images/biosafe/Kanrikitei3_20240401.pdf`
- 出力確認先: `out/20260525-135841668_feat-niid-pathogen-safety-parser-v1/body_v1/`

## 実施内容

- 病原体等安全管理規程専用profile `jp_niid_pathogen_safety_management_v1` を追加した。
  - 共通 `jp_guideline_default_v1` を継承する。
  - 表紙、序文、目次を本文開始の `第１章 総則` まで除外する。
  - 今回の8a本文Parser開発では、`別表１` 以降を対象外として除外する。
  - 条文本文の `第１章` / `第１条` / `第９条の２` は既存のJP共通markerを利用する。
  - この文書の条文内階層に合わせ、丸括弧番号 `(1)` は専用profile側で `subitem` として扱う。
  - 条文中の裸数字段落 `２ ...` は専用profile側で `item` として扱う。
- 共通parserに `skip_blocks.skip_to_eof` を追加した。
  - これは任意profileが明示した場合だけ有効になる汎用機能。
  - `別表１` という文書固有境界は共通parserに持たせず、NIID専用profileだけに置いた。
- 実データbundleを `out/` に生成し、構造確認を行った。

## 個別と共通の整理

- 共通に入れたもの:
  - `skip_to_eof`: 終端まで除外するブロック指定という汎用Parser機能。
- 個別profileに閉じたもの:
  - 表紙・序文・目次の除外境界。
  - `別表１` 以降を8a本文Parser対象外にする境界。
  - 丸括弧番号を `subitem` とする扱い。
  - 裸数字段落を `item` とする扱い。
  - standaloneの括弧付き条見出し行を落とす扱い。

## 検証

```powershell
.venv\Scripts\python.exe -m qai_text2ir.cli bundle --input data\human-readable\niid\pathogen_safety_management\source_texts\Kanrikitei3_20240401.txt --out-dir out\20260525-135841668_feat-niid-pathogen-safety-parser-v1\body_v1 --doc-id jp_niid_pathogen_safety_management_20240401_body_v1 --title "国立感染症研究所病原体等安全管理規程" --short-title "病原体等安全管理規程" --doc-type guideline --source-url https://www.niid.go.jp/niid/images/biosafe/Kanrikitei3_20240401.pdf --source-format txt --retrieved-at 2026-05-23 --jurisdiction JP --language ja --family JP_GUIDELINE --parser-profile-id jp_niid_pathogen_safety_management_v1 --strict
```

結果: bundle生成成功、qualitycheck warning なし。

```powershell
.venv\Scripts\python.exe -m qai_text2ir.goal_check --bundle-dir out\20260525-135841668_feat-niid-pathogen-safety-parser-v1\body_v1 --doc-id jp_niid_pathogen_safety_management_20240401_body_v1 --mode normal --out runs\20260525-135841668_feat-niid-pathogen-safety-parser-v1\goal_check.md
```

結果: `PASS`

```powershell
.venv\Scripts\python.exe -m qai_text2ir.special_structure_audit --bundle-dir out\20260525-135841668_feat-niid-pathogen-safety-parser-v1\body_v1 --doc-id jp_niid_pathogen_safety_management_20240401_body_v1 --mode normal --out runs\20260525-135841668_feat-niid-pathogen-safety-parser-v1\special_structure_audit.md
```

結果: `pass`

```powershell
.venv\Scripts\python.exe -m pytest tests\test_text2ir_niid_pathogen_safety.py tests\test_text2ir_csv_guideline.py tests\test_text2ir_aseptic_processing_guideline.py tests\test_text2ir_jp_guideline.py tests\test_text2ir_api_gmp_guideline.py tests\test_text2ir_eu_gmp_chap1.py tests\test_text2ir_who_lbm_3rd.py tests\test_text2ir_profiles_pics.py tests\test_text2ir_cfr_quality_v2.py tests\test_text2ir_goal_check.py tests\test_profile_loader_extends.py tests\test_markdown_table_parsing.py tests\test_table_note_real_samples.py -q
```

結果: `48 passed`

## 実データ確認サンプル

- `document/root` -> `chapter cha1`（第1章 総則）
- `chapter cha1` -> `paragraph cha1.p1`（第1条）
- `paragraph cha1.p1` -> `item cha1.p1.i2`（第1条第2項相当）
- `chapter cha2` -> `paragraph ... p9_2`（第9条の2）

## 残課題

- 別表・付表は今回の8a本文Parserでは除外した。次フェーズで `別表１` 以降を対象に、table/preformatted保持から個別adapter化の順に検討する。
- standaloneの括弧付き条見出し行は現時点では除外している。将来、条見出しを `heading` として保持する必要が出た場合は、文書固有ではなく「直前見出しを次の構造markerへ付与する」汎用前処理として設計する。
