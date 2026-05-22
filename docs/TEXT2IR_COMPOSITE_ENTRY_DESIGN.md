# Text2IR Composite Entry Design

## Conclusion

PIC/S PE 009-17 Annexes refined は、単一文書を一つのprofileで読む入口ではなく、親profileでAnnex単位に切り、子profileへdispatch/fallbackする複合入口として扱う。

## Target Case

- `data/human-readable/pics/pe009-17_annexes_2023-08-25_en.txt`
- profile: `pics_annexes_default_v3`
- 出力例: `pics_pe00917_annexes_20230825_refined_v3_extends_trace`

## Architecture

```text
parent profile
  detect annex boundary
  create annex subtree
  dispatch subtree to child profile
    Annex 1 profile
    Annex 11 profile
    Annex 15 profile
    generic fallback profile
  merge refined subtree
  record provenance and applied refine
```

## Parent Profile Responsibilities

- Annex境界を検出する。
- Annex見出しと番号を安定した親nodeにする。
- 子profileへ渡す範囲を保持する。
- dispatchできないAnnexはfallback profileで構造を保つ。
- 表・注記候補を黙殺しない。

## Child Profile Responsibilities

- Annex固有のmarker、heading continuation、skip blockを扱う。
- 文書固有の階層補正はprofileで閉じる。
- text2ir本体にAnnex名や文書名をベタ書きしない。

## Manifest Provenance

`manifest.yaml` には親profileだけでなく、子profileの適用履歴を残す。

```yaml
parser_profile:
  id: pics_annexes_default_v3
  provenance:
    - profile_id: pics_annexes_default_v3
      path: src/qai_text2ir/profiles/pics_annexes_default_v3.yaml
    - profile_id: pics_annex1_default_v2
      path: src/qai_text2ir/profiles/pics_annex1_default_v2.yaml
refine:
  kind: annex
  applied:
    - nid: annex1
      profile_id: pics_annex1_default_v2
    - nid: annex15
      profile_id: pics_annex15_default_v1
```

## GOAL_CHECK Treatment

GOAL_CHECKでは、単一文書入口と複合入口を区別する。

共通要件:

- 4ファイル構成
- manifest
- `schema: qai.regdoc_ir.v4`
- `meta.doc.family`
- source_spans
- strict / verify

複合入口の追加要件:

- `manifest.refine.applied` が存在する。
- dispatch/fallbackの履歴が説明できる。
- fallbackを使ったAnnexがレビュー対象として分かる。
- 子profile由来の構造が親profileのsource_spansを壊していない。

## Display Policy

複合入口でも、DQチェックシート側は単一文書と同じように扱う。

- selectable node: `paragraph`, `item`, `subitem`, `table_row`
- ancestor: Part / Annex / section
- descendant: item / subitem / note
- possible table: `preformatted` with `kind_raw=possible_table`

## Risks

- 子profileごとの粒度差が同一出力内に混在する。
- Annex全体入力は大きく、表・注記候補も多い。
- fallbackが多い場合、正式候補としては説明負荷が高い。

## Recommendation

- 正式昇格の最初の候補には使わない。
- Annexes refinedは、検索・横断確認用のreview candidateとして維持する。
- Annex単体でpromotion candidateを作れるものから順に正式化する。
