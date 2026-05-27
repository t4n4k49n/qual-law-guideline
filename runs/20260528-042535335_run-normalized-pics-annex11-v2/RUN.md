# RUN: 20260528-042535335_run-normalized-pics-annex11-v2

## 目的

`pics_pe00917_annex11_20230825` を正規化RUNの親PRレビュー対象として `promotion_candidate/` に配置する。

このRUNは `docs/NORMALIZED_RUN_PLAYBOOK.md` の親PR/子PR運用を適用する。ただし、対象はe-Gov XMLではなく、`docs/NORMALIZATION_PLAN_10_12_13.md` でTXT入口と判断済みのPIC/S Annex 11である。

## ブランチ

- `run/normalized-pics-annex11-v2`

## 対象

- doc_id: `pics_pe00917_annex11_20230825`
- title: `PIC/S GMP Guide (PE 009-17) Annex 11 Computerised systems (25 August 2023)`
- input: `data/human-readable/pics/pe009-17_annex11_2023-08-25_en.txt`
- source_url: [PIC/S PE 009-17 Annexes](https://picscheme.org/docview/8881)
- retrieved_at: `2026-02-18`
- parser_profile: `pics_annex11_default_v1`
- family: `PICS`

## 事前判断

`runs/20260527-105034029_docs-readiness-10-12-13-rerun/READINESS_10_12_13.md` で、PIC/S Annex 11は次の理由により第二候補とした。

- `qualitycheck --strict`、GOAL、promotion GOALがpass。
- warningなし。
- table/noteなし。
- PIC/S単体Annexの最初の候補としてレビュー負荷が小さい。

前回準備中に `section.kind_raw` がprofile固定例示値になる問題を検出したため、PR #191で修正してから本RUNを再生成した。

## 実行

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.cli bundle `
  --input data/human-readable/pics/pe009-17_annex11_2023-08-25_en.txt `
  --out-dir runs/20260528-042535335_run-normalized-pics-annex11-v2/promotion_candidate `
  --doc-id pics_pe00917_annex11_20230825 `
  --title "PIC/S GMP Guide (PE 009-17) Annex 11 Computerised systems (25 August 2023)" `
  --short-title "PIC/S PE009-17 Annex 11" `
  --doc-type guideline `
  --source-url https://picscheme.org/docview/8881 `
  --source-format pdf `
  --retrieved-at 2026-02-18 `
  --parser-profile src/qai_text2ir/profiles/pics_annex11_default_v1.yaml `
  --jurisdiction INTL `
  --language en `
  --family PICS `
  --pics-doc-id "PE 009-17 (Annexes)" `
  --strict `
  --write-manifest `
  --overwrite-manifest
```

## 出力

- `runs/20260528-042535335_run-normalized-pics-annex11-v2/promotion_candidate/pics_pe00917_annex11_20230825.regdoc_ir.yaml`
- `runs/20260528-042535335_run-normalized-pics-annex11-v2/promotion_candidate/pics_pe00917_annex11_20230825.parser_profile.yaml`
- `runs/20260528-042535335_run-normalized-pics-annex11-v2/promotion_candidate/pics_pe00917_annex11_20230825.regdoc_profile.yaml`
- `runs/20260528-042535335_run-normalized-pics-annex11-v2/promotion_candidate/pics_pe00917_annex11_20230825.meta.yaml`
- `runs/20260528-042535335_run-normalized-pics-annex11-v2/promotion_candidate/manifest.yaml`
- `runs/20260528-042535335_run-normalized-pics-annex11-v2/promotion_candidate/GOAL_CHECK_RESULT.md`
- `runs/20260528-042535335_run-normalized-pics-annex11-v2/promotion_candidate/goal_check_result.json`
- `runs/20260528-042535335_run-normalized-pics-annex11-v2/SAMPLE_EXTRACT.md`

## 実行環境

- Python: `.\.venv\Scripts\python.exe`
- Python version: `3.11.6`
- lxml: `6.0.2`
- PyYAML: `6.0.3`
- typer: `0.24.0`
- base commit: `a8bb316cc6e38e775a6177f336774c12985dcc10`

## 検証

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.goal_check `
  --bundle-dir runs/20260528-042535335_run-normalized-pics-annex11-v2/promotion_candidate `
  --doc-id pics_pe00917_annex11_20230825 `
  --mode promotion `
  --format markdown
```

結果:

- status: PASS
- schema: `qai.regdoc_ir.v4`
- nodes: 42
- verify: pass
- source span coverage: 1.0
- warnings: none
- errors: none
- `dq_gmp_checklist.candidate_visibility`: `allow_rules: []` / `deny_rules: []`
- selectable_kinds: `subitem`, `item`, `paragraph`, `statement`, `table_row`

## AIレビュー（目視代替）

人の最終確認はPRで行う前提。今回の機械確認とサンプル確認では、Annex 11のannex、section、itemが祖先関係を保って出力されている。

深い階層サンプル（`SAMPLE_EXTRACT.md` としてIR YAMLから抽出）:

| 階層 | nid | kind | kind_raw | text / heading |
|---:|---|---|---|---|
| 1 | `root` | `document` |  |  |
| 2 | `ann11` | `annex` | `ANNEX` | `COMPUTERISED SYSTEMS` |
| 3 | `ann11.sec14` | `section` | `14.` | `Electronic Signature` |
| 4 | `ann11.sec14.ic` | `item` | `c.` | `include the time and date that they were applied.` |

評価:

- 祖先経路は `document -> annex -> section -> item` として保持されている。
- `ann11.sec14.kind_raw` は原文マーカーの `14.` として保持されている。
- `ann11.sec14.ic` は `item` prefix `i` + `num: c` のNIDであり、`kind_raw` は `c.` として保持されている。
- `source_spans` coverageは1.0。
- 表・注記はこの文書では0件で、readiness判断と一致した。
- `meta.doc.family` は `PICS` として出力され、旧warningの `meta_family_missing` は発生していない。

## 昇格状態

- 親PR段階のため、`data/normalized/` への複写は未実施。
- 子PRは親PR承認後にのみ作成する。
