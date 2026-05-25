# RUN: 20260525-150333206_feat-niid-pathogen-annex-adapter-v1

## 目的

6/7/8/9 個別adapter開発計画のフェーズBとして、8「病原体等安全管理規程」の別表・付表を本文Parserから分離して保持できるか確認する。

これはParser/adapter開発であり、正式な正規化RUNではない。`data/normalized/` への昇格は行わない。

## 対象

- 入力: `data/human-readable/niid/pathogen_safety_management/source_texts/Kanrikitei3_20240401.txt`
- 対象範囲:
  - `別表１` から `別表１０`
  - `付表１－１` から `付表４`
- 出力確認先: `out/20260525-150333206_feat-niid-pathogen-annex-adapter-v1/`

## 実装

- `src/qai_text2ir/profiles/jp_niid_pathogen_safety_management_annex_v1.yaml` を追加した。
- 既存の本文用 `jp_niid_pathogen_safety_management_v1` は変更していない。
- 共通parser本体には手を入れていない。
- 別表・付表の境界、目次から本文を越えて別表本体へ到達するためのskip条件、別表内の数字付き行を階層化しない判断は、このNIID専用profileへ閉じた。

## 共通化しない理由

NIIDの別表・付表は、目次上の別表、本文後の実体、固定幅表、段落型表、複数ページにまたがる表が混在する。これを共通表検出へ寄せると、通常本文や他文書の番号行を表・階層として誤検出するリスクがある。

今回のprofileでは、列復元ではなく「欠落させず、source span付きで追跡可能に保持する」ことを優先した。

## 結果

- `別表1`, `付表1-1`, `付表1-2`, `付表1-3`, `付表2`, `付表3`, `付表4`, `別表2` から `別表10` の16 markerをroot直下の `annex` として保持した。
- 本文の第1章から第6章は、この別表用profileの出力には含めない。
- 別表内の数字付き行は、現時点では個別の `item` / `subitem` にせず、annex本文として保持する。
- fixed-widthの列復元は未実施。必要なものだけ次段階で個別adapter化する。

## 検証

```text
.\.venv\Scripts\python.exe -m pytest tests\test_text2ir_niid_pathogen_annex.py tests\test_text2ir_niid_pathogen_safety.py tests\test_candidate_visibility_profiles_6_9.py -q
10 passed
```

```text
.\.venv\Scripts\python.exe -m qai_text2ir.cli bundle ... --parser-profile-id jp_niid_pathogen_safety_management_annex_v1 --strict --overwrite-manifest
PASS
```

```text
.\.venv\Scripts\python.exe -m qai_text2ir.goal_check ... --mode normal
Status: PASS
Nodes: 28
Kind counts: annex 16, document 1, note 4, subitem 7
Source span coverage: 1.0
```

```text
.\.venv\Scripts\python.exe -m qai_text2ir.special_structure_audit ... --mode normal
Status: pass
unresolved_special_blocks: 0
```

## 監査ファイル

- `runs/20260525-150333206_feat-niid-pathogen-annex-adapter-v1/goal_check.md`
- `runs/20260525-150333206_feat-niid-pathogen-annex-adapter-v1/special_structure_audit.md`

## 次の個別開発候補

- 別表ごとの列復元要否を判定する。
- 列復元が必要な別表だけ、`niid_pathogen_annex_adapter` 相当の個別部品として扱う。
- 今回のprofileを共通化せず、NIIDの文書固有境界・別表保持profileとして維持する。
