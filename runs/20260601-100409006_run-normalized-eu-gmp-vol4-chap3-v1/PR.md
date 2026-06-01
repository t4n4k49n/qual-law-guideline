# EU GMP Vol.4 Chapter 3 正規化候補を追加

## まとめ

EU GMP Vol.4 Chapter 3（Premises and Equipment）を、DQのGMPチェックシートで参照できる正規化候補として追加します。Chap1/Chap2と同じtext2ir系統で処理し、施設・設備に関する要求事項を段落単位で選択・祖先文脈表示できる状態にします。

## 対象

- doc_id: `eu_gmp_vol4_chap3_20150123`
- source: `data/human-readable/eu_gmp/vol4/source_texts/chapter_3.txt`
- official source URL: `https://health.ec.europa.eu/document/download/18d76565-137b-41d2-a602-794527f708c1_en?filename=chapter_3.pdf`
- promotion candidate: `runs/20260601-100409006_run-normalized-eu-gmp-vol4-chap3-v1/promotion_candidate/`

## 変更内容

- Chap3専用parser profile `eu_gmp_chap3_default_v1` を追加
- Chapter 3の正規化候補4ファイルとmanifestを追加
- RUN記録、goal check、special structure audit、深い階層サンプル、構造再合成チェックを追加
- EU GMP text2irテストにChap3の無番号heading・PDF bullet・脚注除去・3.6補足文分離の回帰テストを追加

## 確認ポイント

- Chapter 3本文に表はなく、結合セル複写対応は不要
- table noteはなし
- `PRINCIPLE` / `PREMISES` / `General` / `Production Area` / `Storage Areas` / `Quality Control Areas` / `Ancillary Areas` / `EQUIPMENT` をsection化
- 表紙側deadline箇条書きのPDF private-use bulletをsubitem化
- 3.6のroman list後の `Further guidance can be found...` は最後のitemから分離
- `data/normalized/` はこの親PRでは変更しない

## 検証

- `python -m pytest tests/test_text2ir_eu_gmp_chap1.py -q`
  - `8 passed`
- `python -m qai_text2ir.goal_check --mode promotion --bundle-dir runs/20260601-100409006_run-normalized-eu-gmp-vol4-chap3-v1/promotion_candidate --doc-id eu_gmp_vol4_chap3_20150123`
  - `PASS`
  - schema: `qai.regdoc_ir.v4`
  - nodes: `62`
  - source span coverage: `1.0`
- `python -m qai_text2ir.special_structure_audit --mode promotion --bundle-dir runs/20260601-100409006_run-normalized-eu-gmp-vol4-chap3-v1/promotion_candidate`
  - `pass`
  - source_tables: `0`
  - generated_tables: `0`
  - unresolved_special_blocks: `0`
- `python tools/check_ir_structure.py runs/20260601-100409006_run-normalized-eu-gmp-vol4-chap3-v1/promotion_candidate`
  - `[OK] no structure problems found`

## 深い階層サンプル

| 階層 | nid | kind | kind_raw | text / heading |
|---:|---|---|---|---|
| 1 | `root` | `document` |  |  |
| 2 | `cha3` | `chapter` | `Chapter` | `Premises and Equipment` |
| 3 | `cha3.sec4` | `section` |  | `Production Area` |
| 4 | `cha3.sec4.p3_6` | `paragraph` | `3.6` | `Cross-contamination should be prevented for all products by appropriate design and operation of manufacturing facilities. The measures to prevent cross-contamination should be commensurate with the risks. Quality Risk Management principles should be used to assess and control the risks. Depending of the level of risk, it may be necessary to dedicate premises and equipment for manufacturing and/or packaging operations to control the risk presented by some medicinal products. Dedicated facilities are required for manufacturing when a medicinal product presents a risk because:` |
| 5 | `cha3.sec4.p3_6.iiii` | `item` | `iii.` | `relevant residue limits, derived from the toxicological evaluation, cannot be satisfactorily determined by a validated analytical method.` |

## 昇格方針

承認後、子PRで `runs/20260601-100409006_run-normalized-eu-gmp-vol4-chap3-v1/promotion_candidate/` から `data/normalized/eu_gmp_vol4_chap3_20150123/` へ複写します。

<!-- PR_BODY_FILE: runs/20260601-100409006_run-normalized-eu-gmp-vol4-chap3-v1/PR.md -->
