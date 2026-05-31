# EU GMP Chapter 2 parser profile fix

- run_id: `20260601-034015780_fix-eu-gmp-chap2-profile`
- branch: `fix/eu-gmp-chap2-profile`
- target source: `data/human-readable/eu_gmp/vol4/source_texts/2014-03_chapter_2.txt`
- scope: 正規化RUN前の個別プロファイル修正

## 背景

EU GMP Vol.4 Chapter 2 の正規化候補を生成して目検したところ、既存の Chapter 1 向けプロファイルでは Chapter 2 固有の構造を復元できなかった。

- `Principle` / `General` / `Key Personnel` などの項番なしheadingが本文へ混入する
- `2.7` / `2.8` / `2.9` 配下の `i.` / `ii.` 形式の責務リストが項目化されない
- PDF脚注本文と脚注番号が本文へ混入する
- インデント由来の不要改行・過剰スペースが残る

このため、正規化候補をPR化する前に、EU GMP Chapter 2 専用の個別プロファイルと後処理を追加した。共通パーサーの挙動変更は、プロファイルで明示的に有効化された場合だけ呼び出す最小フックに限定した。

## 実施内容

- `eu_gmp_chap2_default_v1` を追加
  - `Chapter 2: Personnel` のheading抽出
  - `Principle` / `General` / `Key Personnel` / `Training` / `Personnel Hygiene` / `Consultants` の項番なしsection化
  - `i.` 形式、`a)` 形式、`(a)` 形式のitem化
  - Chapter 2 PDF脚注本文の除去
  - 脚注番号由来の `Revisiona` / `Directive 2001/83/EC1` / `authorisation2` / `Article 49 3` の補正
- Chapter 2 専用cleanupを追加
  - table / preformatted 以外の `heading` / `text` から不要改行・過剰スペースを除去
- 既存のEU GMPテストへ回帰テストを追加
  - 項番なしheading
  - `2.6` 配下の `a)` / `(b)`
  - `2.7` 配下の `i.` / `ii.`
  - 脚注本文・脚注番号混入の防止

## 検証

- `python -m pytest tests/test_text2ir_eu_gmp_chap1.py -q`
  - `7 passed`

## 次工程

このPR承認・main同期後に、EU GMP Vol.4 Chapter 2 の正規化RUNを新規run_idで作り直す。
その際は、表（該当有無、結合、note）、項番なしheading、不要改行・スペース、深い階層サンプル、再合成確認をRUN成果物として残す。
