# WHO_LBM_CANDIDATE_GRANULARITY_REVIEW

## 結論

WHO LBM 3rdは当面item粒度をDQ候補として許容する。抽出した代表10件はいずれも単独の安全要求・推奨事項として読める粒度であり、paragraph相当へ無理に寄せる必要は現時点では低い。

## 代表候補10件

| # | nid | 文脈 | num | 候補本文 | レビュー |
|---:|---|---|---|---|---|
| 1 | `cha1.i1` | document > Biosafety guidelines > General principles | `1` | Pathogenicity of the organism. | item粒度で理解可能 |
| 2 | `cha1.i2` | document > Biosafety guidelines > General principles | `2` | Mode of transmission and host range of the organism. These may be influenced by existing levels of immunity in the local population, density and movement of the host population, presence of appropriate vectors, and standards of environmental hygiene. | item粒度で理解可能 |
| 3 | `cha1.i3` | document > Biosafety guidelines > General principles | `3` | Local availability of effective preventive measures. These may include: prophylaxis by immunization or administration of antisera (passive immunization); sanitary measures, e.g. food and water hygiene; control of animal reservoirs or arthropod vectors. | item粒度で理解可能 |
| 4 | `cha1.i4` | document > Biosafety guidelines > General principles | `4` | Local availability of effective treatment. This includes passive immunization, postexposure vaccination and use of antimicrobials, antivirals and chemotherapeutic agents, and should take into consideration the possibility of the emergence of drug-resistant strains. | item粒度で理解可能 |
| 5 | `cha2.i1` | document > Biosafety guidelines > Microbiological risk assessment | `1` | Pathogenicity of the agent and infectious dose | item粒度で理解可能 |
| 6 | `cha2.i2` | document > Biosafety guidelines > Microbiological risk assessment | `2` | Potential outcome of exposure | item粒度で理解可能 |
| 7 | `cha2.i3` | document > Biosafety guidelines > Microbiological risk assessment | `3` | Natural route of infection | item粒度で理解可能 |
| 8 | `cha2.i4` | document > Biosafety guidelines > Microbiological risk assessment | `4` | Other routes of infection, resulting from laboratory manipulations (parenteral, airborne, ingestion) | item粒度で理解可能 |
| 9 | `cha2.i5` | document > Biosafety guidelines > Microbiological risk assessment | `5` | Stability of the agent in the environment | item粒度で理解可能 |
| 10 | `cha2.i6` | document > Biosafety guidelines > Microbiological risk assessment | `6` | Concentration of the agent and volume of concentrated material to be manipulated | item粒度で理解可能 |

## 判断

- item粒度を初期許容する。
- 表示時はchapter/part/annexなどのancestor contextを併用する。
- 実UIレビューで粒度が粗い/細かいと判明した場合にprofile調整を検討する。
