# PR: 正規化RUN 20260206-122710668_run-normalized-run-playbook

## 概要
- 対象法令: 薬局等構造設備規則（昭和三十六年厚生省令第二号）
- 入力XML: 336M50000100002_20260501_507M60000100117.xml
- 正規化RUNの成果物を作成（IR / parser_profile / regdoc_profile / meta）
- `manifest.yaml` と `RUN.md` を記録
- 最小検証（verify.py）を実施

## 検証
- verify.py: assert_unique_nids / check_annex_article_nids / check_appendix_scoped_indices => PASS
- AIレビュー（目視代替）実施済み。人の最終確認はこのPRで行う前提。

## 比較表（人間可読 vs YAML）
基準: 最も深いitemの同列から本文が最も短いものを抽出

| 人間可読 | YAML断片 |
| --- | --- |
| 第二章 医薬品等の製造業 / 第一節 医薬品の製造業 / 第九条 （放射性医薬品区分の医薬品製造業者等の製造所の構造設備） / 1 / 四<br>外部と区画された構造であること。 | `nid: art9.p1.i4.nu.pt1`<br>`kind: point`<br>`num: （１）`<br>`heading: null`<br>`text: 外部と区画された構造であること。` |

## 変更ファイル
- `out/20260206-122710668_run-normalized-run-playbook/jp_test_336M50000100002_20260501.regdoc_ir.yaml`
- `out/20260206-122710668_run-normalized-run-playbook/jp_test_336M50000100002_20260501.parser_profile.yaml`
- `out/20260206-122710668_run-normalized-run-playbook/jp_test_336M50000100002_20260501.regdoc_profile.yaml`
- `out/20260206-122710668_run-normalized-run-playbook/jp_test_336M50000100002_20260501.meta.yaml`
- `out/20260206-122710668_run-normalized-run-playbook/manifest.yaml`
- `runs/20260206-122710668_run-normalized-run-playbook/RUN.md`
